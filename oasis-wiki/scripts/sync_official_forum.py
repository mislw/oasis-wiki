#!/usr/bin/env python3
"""Synchronize selected official forum threads into the bundled Markdown collection."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FORUM_BASE_URL = "https://forum.developer.gp.qq.com"
OFFICIAL_USER_ID = 7825
DEFAULT_THREAD_IDS = (2739, 1769, 2285, 2622, 2553)
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "references" / "wiki" / "论坛经验帖_绿洲启妹.md"
ARTICLE_SEPARATOR = "\n\n---\n\n"
ARTICLE_START_RE = re.compile(
    r"^## \[.*?\]\(https://forum\.developer\.gp\.qq\.com/thread/(\d+)\)",
    re.MULTILINE,
)


def _append_block_break(parts: list[str]) -> None:
    current = "".join(parts)
    if not current.endswith("\n\n"):
        parts.append("\n\n" if not current.endswith("\n") else "\n")


class _MarkdownParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []
        self.lists: list[dict[str, int | str]] = []
        self.pre_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): value or "" for key, value in attrs}

        if tag in {"p", "div"}:
            _append_block_break(self.parts)
        elif tag == "br":
            self.parts.append("\n")
        elif re.fullmatch(r"h[1-6]", tag):
            _append_block_break(self.parts)
            self.parts.append("#" * int(tag[1]) + " ")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "a":
            self.parts.append("[")
            self.links.append(attr_map.get("href", ""))
        elif tag == "img":
            title = attr_map.get("title", "")
            alt = attr_map.get("alt", "")
            src = attr_map.get("src", "")
            attachment_id = title if title.isdigit() else ""
            if not attachment_id:
                match = re.search(r"attachmentId-(\d+)", alt, re.IGNORECASE)
                attachment_id = match.group(1) if match else ""
            if attachment_id:
                self.parts.append(f"[图片#{attachment_id}]")
            elif src:
                self.parts.append(f"![{alt or '图片'}]({src})")
        elif tag in {"ul", "ol"}:
            _append_block_break(self.parts)
            self.lists.append({"tag": tag, "count": 0})
        elif tag == "li":
            current = "".join(self.parts)
            if current and not current.endswith("\n"):
                self.parts.append("\n")
            depth = max(0, len(self.lists) - 1)
            prefix = "- "
            if self.lists and self.lists[-1]["tag"] == "ol":
                self.lists[-1]["count"] = int(self.lists[-1]["count"]) + 1
                prefix = f"{self.lists[-1]['count']}. "
            self.parts.append("  " * depth + prefix)
        elif tag == "hr":
            _append_block_break(self.parts)
            self.parts.append("---")
            _append_block_break(self.parts)
        elif tag == "pre":
            _append_block_break(self.parts)
            self.parts.append("```\n")
            self.pre_depth += 1
        elif tag == "code" and not self.pre_depth:
            self.parts.append("`")
        elif tag == "blockquote":
            _append_block_break(self.parts)
            self.parts.append("> ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"p", "div"} or re.fullmatch(r"h[1-6]", tag):
            _append_block_break(self.parts)
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "a":
            href = self.links.pop() if self.links else ""
            self.parts.append(f"]({href})" if href else "]")
        elif tag == "li":
            if not "".join(self.parts).endswith("\n"):
                self.parts.append("\n")
        elif tag in {"ul", "ol"}:
            if self.lists:
                self.lists.pop()
            _append_block_break(self.parts)
        elif tag == "pre":
            self.pre_depth = max(0, self.pre_depth - 1)
            if not "".join(self.parts).endswith("\n"):
                self.parts.append("\n")
            self.parts.append("```")
            _append_block_break(self.parts)
        elif tag == "code" and not self.pre_depth:
            self.parts.append("`")
        elif tag == "blockquote":
            _append_block_break(self.parts)

    def handle_data(self, data: str) -> None:
        if self.pre_depth:
            self.parts.append(data)
            return
        normalized = re.sub(r"[\t\r\f\v ]+", " ", data)
        self.parts.append(normalized)


def html_to_markdown(source: str) -> str:
    parser = _MarkdownParser()
    parser.feed(source or "")
    parser.close()
    markdown = "".join(parser.parts).replace("\r\n", "\n").replace("\r", "\n")
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def validate_thread_payload(
    payload: dict, expected_thread_id: int, expected_user_id: int = OFFICIAL_USER_ID
) -> dict:
    code = payload.get("Code", payload.get("code"))
    if code != 0:
        raise ValueError(f"forum API failed for thread {expected_thread_id}: code={code}")

    data = payload.get("Data", payload.get("data")) or {}
    if data.get("threadId") != expected_thread_id:
        raise ValueError(f"thread ID mismatch for {expected_thread_id}")
    if data.get("userId") != expected_user_id:
        raise ValueError(f"unexpected author for thread {expected_thread_id}")
    if data.get("isApproved") != 1:
        raise ValueError(f"thread {expected_thread_id} is not approved")
    if not data.get("title") or not (data.get("content") or {}).get("text"):
        raise ValueError(f"thread {expected_thread_id} has no published content")
    return data


def fetch_thread(thread_id: int, timeout: float = 30.0) -> dict:
    query = urlencode({"threadId": thread_id})
    url = f"{FORUM_BASE_URL}/api/v3/thread.detail?{query}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "Referer": f"{FORUM_BASE_URL}/thread/{thread_id}",
            "User-Agent": "oasis-wiki-forum-sync/1.0",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    return validate_thread_payload(payload, expected_thread_id=thread_id)


def render_thread_block(thread: dict) -> str:
    thread_id = int(thread["threadId"])
    title = str(thread["title"]).strip()
    category = str(thread.get("categoryName") or "未分类").strip()
    view_count = int(thread.get("viewCount") or 0)
    published_at = thread.get("issueAt") or thread.get("createdAt") or "未知"
    updated_at = thread.get("updatedAt") or published_at
    body = html_to_markdown((thread.get("content") or {}).get("text", ""))

    metadata = (
        f"**分类：** {category} | **浏览：** {view_count} | "
        f"**发布：** {published_at} | **更新：** {updated_at}"
    )
    return (
        f"## [{title}]({FORUM_BASE_URL}/thread/{thread_id})\n\n"
        f"{metadata}\n\n{body}"
    ).strip()


def _thread_id_from_block(block: str) -> int | None:
    match = ARTICLE_START_RE.search(block)
    return int(match.group(1)) if match else None


def _split_article_blocks(region: str) -> list[str]:
    matches = list(ARTICLE_START_RE.finditer(region))
    blocks: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(region)
        block = region[match.start() : end].strip()
        block = re.sub(r"\n\n---\s*$", "", block).rstrip()
        blocks.append(block)
    return blocks


def merge_forum_collection(
    existing: str, new_blocks: Iterable[str], fetched_at: str
) -> str:
    normalized = existing.replace("\r\n", "\n").replace("\r", "\n").strip()
    first_article = ARTICLE_START_RE.search(normalized)
    if not first_article:
        raise ValueError("forum collection has no recognizable thread blocks")

    prefix = normalized[: first_article.start()].rstrip()
    old_region = normalized[first_article.start() :].strip()
    old_blocks = _split_article_blocks(old_region)
    rendered_blocks = [block.strip() for block in new_blocks]
    replacement_ids = {
        thread_id
        for thread_id in (_thread_id_from_block(block) for block in rendered_blocks)
        if thread_id is not None
    }
    preserved = [
        block
        for block in old_blocks
        if _thread_id_from_block(block) not in replacement_ids
    ]

    prefix = re.sub(
        r"(?m)^> 抓取时间：.*$", f"> 抓取时间：{fetched_at}", prefix
    )
    prefix = re.sub(r"\n---\s*$", "", prefix).rstrip()
    all_blocks = rendered_blocks + preserved
    return f"{prefix}\n\n---\n\n{ARTICLE_SEPARATOR.join(all_blocks)}\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--thread-id",
        dest="thread_ids",
        action="append",
        type=int,
        help="Thread ID to synchronize. Repeat for multiple threads.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    thread_ids = tuple(args.thread_ids or DEFAULT_THREAD_IDS)
    if len(thread_ids) != len(set(thread_ids)):
        raise ValueError("duplicate thread IDs requested")

    threads = [fetch_thread(thread_id) for thread_id in thread_ids]
    existing = args.output.read_text(encoding="utf-8")
    merged = merge_forum_collection(
        existing,
        [render_thread_block(thread) for thread in threads],
        fetched_at=date.today().isoformat(),
    )

    summary = {
        "status": "validated" if args.dry_run else "written",
        "output": str(args.output),
        "thread_ids": list(thread_ids),
        "titles": [thread["title"] for thread in threads],
        "changed": merged != existing.replace("\r\n", "\n").replace("\r", "\n"),
    }
    if not args.dry_run:
        args.output.write_text(merged, encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
