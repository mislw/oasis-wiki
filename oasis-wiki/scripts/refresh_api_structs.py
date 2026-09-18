"""Refresh the UGC/本平精英 scope struct section of 官方API参考手册.md.

The API site (https://developer.gp.qq.com/api/) is a single-page app backed by
plain static JSON, so the manual can be checked without a browser. Only structs
whose name starts with FUGC or FPE are Oasis/和平精英 scope; everything else on
the site is UE engine internals that the curated manual deliberately omits.
"""

import json
import pathlib
import re
import urllib.request

API = "https://developer.gp.qq.com/api"
MANUAL = pathlib.Path(
    r"C:\Users\Administrator\.codex\skills\oasis-wiki\references\wiki\官方API参考手册.md"
)
SCOPE_PREFIXES = ("FUGC", "FPE")


def get(path: str):
    req = urllib.request.Request(f"{API}/{path}", headers={"User-Agent": "oasis-wiki-api/1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect_names(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str):
                out[key] = value
            else:
                collect_names(value, out)
    elif isinstance(node, list):
        for item in node:
            collect_names(item, out)


def build_section(structs: list[dict]) -> str:
    lines = ["## 数据结构（Structs）", ""]
    lines.append(
        f"> 来源: https://developer.gp.qq.com/api/ | 收录范围: 名称以 "
        f"`{'` / `'.join(SCOPE_PREFIXES)}` 开头的绿洲启元 / 和平精英结构体（共 {len(structs)} 个）。"
    )
    lines.append("> UE 引擎内部结构体（如 `FClipmap*`）不在本手册范围内。")
    lines.append("")
    for struct in structs:
        name = struct.get("Name") or ""
        desc = (struct.get("Description") or "").strip()
        lines.append(f"### {name}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")
        variables = struct.get("Variables") or []
        if variables:
            lines.append("| 字段 | 类型 | 说明 |")
            lines.append("| :--- | :--- | :--- |")
            for var in variables:
                vname = str(var.get("Name") or "").replace("|", "\\|")
                vtype = str(var.get("Type") or "").replace("|", "\\|")
                vdesc = str(var.get("Description") or "").replace("|", "\\|").replace("\n", " ")
                lines.append(f"| `{vname}` | `{vtype}` | {vdesc} |")
            lines.append("")
        else:
            lines.append("_（无字段定义）_")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    listing = {}
    collect_names(get("cppstruct/list/sorted_list.json"), listing)
    in_scope = sorted(n for n in listing if n.startswith(SCOPE_PREFIXES))
    print(f"线上结构体 {len(listing)} 个 | 范围内（{SCOPE_PREFIXES}）{len(in_scope)} 个")

    structs = []
    for name in in_scope:
        try:
            structs.append(get(f"cppstruct/detail/{name}.json"))
        except Exception as error:  # noqa: BLE001
            print(f"  跳过 {name}: {error}")

    section = build_section(structs)
    text = MANUAL.read_text(encoding="utf-8")
    pattern = re.compile(r"## 数据结构（Structs）.*?(?=## 全局函数（Global Functions）)", re.S)
    if not pattern.search(text):
        raise SystemExit("anchor not found: 数据结构（Structs）")
    updated = pattern.sub(section + "\n", text)

    # 修正头部统计
    updated = re.sub(
        r"> 统计：.*",
        f"> 统计：290 个类、3692 个枚举、{len(structs)} 个结构体（仅绿洲/和平范围）、3 个全局函数",
        updated,
        count=1,
    )
    updated = re.sub(r"> 抓取时间：.*", "> 抓取时间：2026-07-10（结构体章节 2026-09-18 补录）", updated, count=1)
    MANUAL.write_text(updated, encoding="utf-8")
    print(f"已写入 {MANUAL.name} | 新大小 {MANUAL.stat().st_size} 字节")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
