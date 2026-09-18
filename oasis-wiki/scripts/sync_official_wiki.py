#!/usr/bin/env python3
"""Synchronize the bundled Oasis Wiki snapshot from the official wiki API."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_BASE_URL = "https://developer.gp.qq.com/wikieditor"
SHANGHAI = timezone(timedelta(hours=8))
UPDATE_CUTOFF = datetime(2026, 7, 15, tzinfo=SHANGHAI)
PRESERVED_WIKI_FILES = {
    "官方API参考手册.md",
    "论坛经验帖_绿洲启妹.md",
    "术语表.md",
}
FIXED_MANAGED_FILES = {
    ".md",
    "README.md",
    "API参考索引.md",
    "代码示例库.md",
    "新增内容_1.37版本.md",
    "绿洲启元Wiki目录.txt",
}


@dataclass(frozen=True)
class CatalogArticle:
    id: int
    title: str
    path: str
    category: str


def flatten_catalog(nodes: Iterable[dict], parents: tuple[str, ...] = ()) -> list[CatalogArticle]:
    articles: list[CatalogArticle] = []
    for node in nodes:
        label = str(node.get("label", "")).strip()
        node_type = int(node.get("type", 0))
        if node_type == 1:
            article_id = int(node["id"])
            path_parts = (*parents, label)
            articles.append(
                CatalogArticle(
                    id=article_id,
                    title=label,
                    path="/".join(path_parts),
                    category="/".join(parents),
                )
            )
            continue
        children = node.get("children") or []
        articles.extend(flatten_catalog(children, (*parents, label)))
    return articles


def category_filename(category: str) -> str:
    if not category:
        return "根目录.md"
    name = category.replace("/", "_")
    name = re.sub(r'[<>:"\\|?*]', "_", name).strip(" .")
    return f"{name}.md"


def format_epoch(value: object) -> str:
    try:
        timestamp = int(value or 0)
    except (TypeError, ValueError):
        timestamp = 0
    if not timestamp:
        return ""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(SHANGHAI).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def _article_timestamp(row: dict) -> int:
    return max(int(row.get("AddTime") or 0), int(row.get("UpdateTime") or 0))


def normalize_body(body: object) -> str:
    text = str(body or "").replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip(" \t") for line in text.split("\n")).strip()


def extract_api_names(body: str) -> set[str]:
    names: set[str] = set()
    for match in re.finditer(r"https://developer\.gp\.qq\.com/api/[^)\s]+", body):
        url = match.group(0).replace("&amp;", "&")
        parsed = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(parsed.query)
        fragment_query = urllib.parse.parse_qs(urllib.parse.urlsplit(parsed.fragment).query)
        for key in ("apiLabel", "autoJump"):
            for value in (*query.get(key, []), *fragment_query.get(key, [])):
                names.add(urllib.parse.unquote(value))

    for match in re.finditer(r"`{1,2}([^`\r\n]{1,120})`{1,2}", body):
        candidate = match.group(1).strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:[.:][A-Za-z_][A-Za-z0-9_]*)*", candidate):
            names.add(candidate)

    for match in re.finditer(
        r"\b(?:UGC[A-Za-z0-9_]*|UE|GameplayStatics|UnrealNetwork)\."
        r"[A-Za-z_][A-Za-z0-9_]*",
        body,
    ):
        names.add(match.group(0))

    return {name for name in names if 1 < len(name) <= 120}


def extract_code_blocks(body: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(r"```([^\r\n`]*)\r?\n(.*?)```", body, flags=re.DOTALL):
        language = match.group(1).strip().lower()
        code = normalize_body(match.group(2))
        if not code:
            continue
        looks_like_lua = bool(
            re.search(r"\b(function|local|return|then|end)\b|UGC[A-Za-z0-9_]*\.", code)
        )
        if language in {"lua", "luau"} or (not language and looks_like_lua):
            blocks.append((language or "lua", code))
    return blocks


def _render_article(article: CatalogArticle, row: dict) -> str:
    body = normalize_body(row.get("Body"))
    api_names = sorted(extract_api_names(body), key=lambda value: (value.casefold(), value))
    lines = [
        f"## {article.title}",
        "",
        f"> 文档路径: {article.path.replace('/', ' > ')}",
        "",
        f"> 文档ID: {article.id} | [官网原文]({DEFAULT_BASE_URL}/#/catalog/{article.id})",
    ]
    added = format_epoch(row.get("AddTime"))
    updated = format_epoch(row.get("UpdateTime"))
    if added or updated:
        metadata = []
        if added:
            metadata.append(f"新增: {added}")
        if updated:
            metadata.append(f"更新: {updated}")
        lines.extend(["", f"> {' | '.join(metadata)}"])
    if api_names:
        preview = ", ".join(f"`{name}`" for name in api_names[:40])
        if len(api_names) > 40:
            preview += f"，另有 {len(api_names) - 40} 项"
        lines.extend(["", f"**涉及API/标识符:** {preview}"])
    lines.extend(["", body, "", "---", ""])
    return "\n".join(lines)


def _render_category(
    category: str, articles: list[CatalogArticle], article_rows: dict[int, dict]
) -> str:
    display_name = category or "根目录"
    lines = [
        f"# {display_name}",
        "",
        f"> 官方知识库同步分类，共 {len(articles)} 篇文章",
        "",
        "---",
        "",
    ]
    for article in articles:
        lines.append(_render_article(article, article_rows[article.id]))
    return "\n".join(lines).rstrip() + "\n"


def _render_directory(nodes: Iterable[dict]) -> str:
    lines: list[str] = []

    def walk(items: Iterable[dict], depth: int) -> None:
        for item in items:
            label = str(item.get("label", "")).strip()
            item_id = item.get("id", "")
            item_type = int(item.get("type", 0))
            suffix = f" [id:{item_id}]" if item_type == 1 else f" [目录:{item_id}]"
            lines.append(f"{'  ' * depth}- {label}{suffix}")
            walk(item.get("children") or [], depth + 1)

    walk(nodes, 0)
    return "\n".join(lines) + "\n"


def _render_api_index(
    articles: list[CatalogArticle], article_rows: dict[int, dict]
) -> tuple[str, int]:
    references: dict[str, list[CatalogArticle]] = defaultdict(list)
    for article in articles:
        for api_name in extract_api_names(str(article_rows[article.id].get("Body") or "")):
            references[api_name].append(article)

    lines = [
        "# 绿洲启元 Lua API 参考索引",
        "",
        f"> 共收录 {len(references)} 个API/类/标识符，来自 {len(articles)} 篇官网文档",
        "",
        "---",
        "",
    ]
    grouped: dict[str, list[str]] = defaultdict(list)
    for name in references:
        first = name[0].upper()
        grouped[first if first.isascii() and first.isalnum() else "#"].append(name)
    for group in sorted(grouped, key=lambda value: (value == "#", value)):
        lines.extend([f"## {group}", ""])
        for name in sorted(grouped[group], key=lambda value: (value.casefold(), value)):
            refs = sorted(references[name], key=lambda item: (item.path, item.id))
            lines.extend([f"### `{name}`", "", f"出现于 {len(refs)} 篇文档：", ""])
            for article in refs[:20]:
                lines.append(f"- [{article.title}](id:{article.id}) ({article.category or '根目录'})")
            if len(refs) > 20:
                lines.append(f"- ...另有 {len(refs) - 20} 篇")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n", len(references)


def _render_code_examples(
    articles: list[CatalogArticle], article_rows: dict[int, dict]
) -> tuple[str, int]:
    lines = [
        "# 绿洲启元 Lua 代码示例库",
        "",
        f"> 从 {len(articles)} 篇官网文档中提取",
        "",
        "---",
        "",
    ]
    count = 0
    for article in articles:
        blocks = extract_code_blocks(str(article_rows[article.id].get("Body") or ""))
        if not blocks:
            continue
        lines.extend(
            [
                f"## {article.title}",
                "",
                f"> 来源: {article.category or '根目录'} (id:{article.id})",
                "",
            ]
        )
        for index, (language, code) in enumerate(blocks, start=1):
            count += 1
            lines.extend([f"### 示例 {index}", "", f"```{language}", code, "```", ""])
    return "\n".join(lines).rstrip() + "\n", count


def _render_update_summary(
    articles: list[CatalogArticle], article_rows: dict[int, dict], catalog_version: int
) -> str:
    cutoff_epoch = int(UPDATE_CUTOFF.timestamp())
    changed = [
        article
        for article in articles
        if _article_timestamp(article_rows[article.id]) >= cutoff_epoch
    ]
    changed.sort(key=lambda item: (_article_timestamp(article_rows[item.id]), item.id))
    lines = [
        "# 绿洲启元 1.37 版本官方更新",
        "",
        f"> 官网目录 Version {catalog_version}，本文件由官网当前文章自动生成。",
        "",
        "> 完整正文同时按分类收录在本目录其他 Markdown 文件中。",
        "",
        "## 2026-07-15 后新增或更新文章",
        "",
        "| ID | 标题 | 路径 | 新增时间 | 更新时间 |",
        "|---:|---|---|---|---|",
    ]
    for article in changed:
        row = article_rows[article.id]
        lines.append(
            f"| {article.id} | {article.title} | {article.category or '根目录'} | "
            f"{format_epoch(row.get('AddTime'))} | {format_epoch(row.get('UpdateTime'))} |"
        )
    for article_id, heading in (
        (20418, "当前 1.37 Release Notes"),
        (20414, "当前 UGCAskQ MCP 使用说明"),
    ):
        article = next((item for item in articles if item.id == article_id), None)
        if not article:
            continue
        lines.extend(
            [
                "",
                "---",
                "",
                f"## {heading} (id:{article_id})",
                "",
                normalize_body(article_rows[article_id].get("Body")),
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_artifacts(
    *,
    catalog: list[dict],
    article_rows: dict[int, dict],
    catalog_version: int,
    catalog_updated_at: int,
    generated_at: datetime,
) -> dict[str, str]:
    articles = flatten_catalog(catalog)
    ids = [article.id for article in articles]
    if len(ids) != len(set(ids)):
        raise ValueError("Official catalog contains duplicate article IDs")
    missing = sorted(set(ids) - set(article_rows))
    if missing:
        raise ValueError(f"Missing article rows: {missing}")
    for article in articles:
        row_title = str(article_rows[article.id].get("Title") or "").strip()
        if row_title and row_title != article.title:
            raise ValueError(
                f"Article title mismatch for {article.id}: catalog={article.title!r}, row={row_title!r}"
            )

    grouped: dict[str, list[CatalogArticle]] = defaultdict(list)
    for article in articles:
        grouped[article.category].append(article)
    for group in grouped.values():
        group.sort(key=lambda item: (item.path, item.id))

    api_index, api_count = _render_api_index(articles, article_rows)
    code_examples, code_count = _render_code_examples(articles, article_rows)
    generated_text = generated_at.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S")
    catalog_updated_text = format_epoch(catalog_updated_at)

    artifacts: dict[str, str] = {}
    for category in sorted(grouped, key=lambda value: (value == "", value)):
        artifacts[category_filename(category)] = _render_category(
            category, grouped[category], article_rows
        )

    readme = [
        "# 绿洲启元Wiki知识库 - 总索引",
        "",
        f"> 同步时间: {generated_text}",
        "",
        f"> 官网目录: Version {catalog_version} | 更新时间: {catalog_updated_text}",
        "",
        f"> 文章总数: {len(articles)}",
        "",
        f"> Lua代码示例: {code_count}",
        "",
        f"> API/类/标识符引用: {api_count}",
        "",
        "---",
        "",
        "## 保留的补充资料",
        "",
        "- `官方API参考手册.md`: 独立 API 站点快照。",
        "- `论坛经验帖_绿洲启妹.md`: 官方论坛教程快照。",
        "- `术语表.md`: 术语速查。",
        "- `新增内容_1.37版本.md`: 当前 1.37 日志、MCP 说明和近期更新索引。",
        "",
        "## 分类文档",
        "",
        "| 分类 | 文章数 | 文件 |",
        "|---|---:|---|",
    ]
    for category in sorted(grouped, key=lambda value: (value == "", value)):
        readme.append(
            f"| {category or '根目录'} | {len(grouped[category])} | {category_filename(category)} |"
        )
    readme.extend(["", "## 文章ID速查表", "", "按文章ID排序：", ""])
    for article in sorted(articles, key=lambda item: item.id):
        api_names = extract_api_names(str(article_rows[article.id].get("Body") or ""))
        blocks = extract_code_blocks(str(article_rows[article.id].get("Body") or ""))
        suffix = []
        if api_names:
            suffix.append(f"{len(api_names)}个API/标识符")
        if blocks:
            suffix.append(f"{len(blocks)}个代码示例")
        extra = f" | {' | '.join(suffix)}" if suffix else ""
        readme.append(
            f"- id:{article.id} | {article.title} | {article.category or '根目录'}{extra}"
        )

    artifacts["README.md"] = "\n".join(readme).rstrip() + "\n"
    artifacts["API参考索引.md"] = api_index
    artifacts["代码示例库.md"] = code_examples
    artifacts["新增内容_1.37版本.md"] = _render_update_summary(
        articles, article_rows, catalog_version
    )
    artifacts["绿洲启元Wiki目录.txt"] = _render_directory(catalog)
    return artifacts


def discover_previous_managed_files(wiki_dir: Path) -> set[str]:
    managed = set(FIXED_MANAGED_FILES)
    readme = wiki_dir / "README.md"
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\|\s*.*?\s*\|\s*\d+\s*\|\s*([^|]+\.md)\s*\|$", line)
            if match:
                managed.add(match.group(1).strip())
    managed -= PRESERVED_WIKI_FILES
    return managed


def write_artifacts(
    wiki_dir: Path,
    artifacts: dict[str, str],
    *,
    previous_managed_files: set[str],
) -> None:
    wiki_dir.mkdir(parents=True, exist_ok=True)
    for name in sorted(previous_managed_files - set(artifacts)):
        target = wiki_dir / name
        if target.is_file():
            target.unlink()
    for name, content in artifacts.items():
        (wiki_dir / name).write_text(content, encoding="utf-8", newline="\n")


def fetch_json(url: str, *, retries: int = 3, timeout: int = 30) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "oasis-wiki-sync/1"})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except Exception as error:  # pragma: no cover - exercised only on network errors
            last_error = error
            if attempt + 1 < retries:
                time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}") from last_error


def fetch_official_snapshot(base_url: str, workers: int) -> tuple[list[dict], dict[int, dict], dict]:
    category_response = fetch_json(f"{base_url.rstrip('/')}/_api/look-Category")
    if category_response.get("code") != 0 or not category_response.get("data"):
        raise RuntimeError(f"Invalid category response: {category_response.get('message')}")
    category_row = category_response["data"][0]
    catalog = json.loads(category_row["Body"])
    articles = flatten_catalog(catalog)
    article_rows: dict[int, dict] = {}

    def fetch_article(article: CatalogArticle) -> tuple[int, dict]:
        response = fetch_json(
            f"{base_url.rstrip('/')}/_api/query-articles?Id={article.id}"
        )
        if response.get("code") != 0 or not response.get("data"):
            raise RuntimeError(f"Article {article.id} returned no data")
        return article.id, response["data"][0]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fetch_article, article): article for article in articles}
        for future in as_completed(futures):
            article_id, row = future.result()
            article_rows[article_id] = row
    return catalog, article_rows, category_row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-path",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the oasis-wiki skill root",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_path = args.skill_path.resolve()
    wiki_dir = skill_path / "references" / "wiki"
    catalog, article_rows, category_row = fetch_official_snapshot(
        args.base_url, max(1, args.workers)
    )
    generated_at = datetime.now(tz=SHANGHAI)
    artifacts = build_artifacts(
        catalog=catalog,
        article_rows=article_rows,
        catalog_version=int(category_row.get("Version") or 0),
        catalog_updated_at=int(category_row.get("UpdateTime") or 0),
        generated_at=generated_at,
    )
    if not args.dry_run:
        write_artifacts(
            wiki_dir,
            artifacts,
            previous_managed_files=discover_previous_managed_files(wiki_dir),
        )
    result = {
        "status": "validated" if args.dry_run else "synchronized",
        "catalog_version": int(category_row.get("Version") or 0),
        "catalog_updated_at": format_epoch(category_row.get("UpdateTime")),
        "articles": len(article_rows),
        "generated_files": len(artifacts),
        "skill_path": str(skill_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
