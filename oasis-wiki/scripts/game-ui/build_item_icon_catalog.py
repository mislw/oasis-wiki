#!/usr/bin/env python3
"""Build semantic item-icon mappings from a normalized UGCObject export."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from project_library import (
    ProjectLibraryError,
    read_json_object,
    write_json_object,
)


FIELD_ALIASES = {
    "item_id": ("ItemID", "项目ItemID"),
    "name": ("ItemName", "物品名称"),
    "description": ("ItemDesc", "物品描述"),
    "icon": ("ItemIcon", "ItemSmallIcon_n", "小icon", "SmallIcon"),
}

SEMANTIC_KEY = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _fingerprint(row: dict[str, Any]) -> str:
    digest = hashlib.sha256(_canonical_json(row).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _field(values: dict[str, Any], name: str) -> Any:
    for alias in FIELD_ALIASES[name]:
        if alias in values:
            return values[alias]
    return None


def _positive_item_id(value: object, row_name: object) -> int:
    candidate = value if value is not None else row_name
    if isinstance(candidate, bool):
        raise ProjectLibraryError(f"invalid item_id: {candidate}")
    if isinstance(candidate, int):
        item_id = candidate
    elif isinstance(candidate, str) and candidate.isdecimal():
        item_id = int(candidate)
    else:
        raise ProjectLibraryError(f"invalid item_id: {candidate}")
    if item_id <= 0:
        raise ProjectLibraryError(f"invalid item_id: {candidate}")
    return item_id


def _required_text(value: object, field: str, item_id: int) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise ProjectLibraryError(f"item {item_id} missing {field}")


def _asset_by_unreal_path(assets: dict[str, Any]) -> dict[str, str]:
    entries = assets.get("assets")
    if not isinstance(entries, list):
        raise ProjectLibraryError("asset catalog assets must be an array")
    result: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        source_asset = entry.get("source_asset")
        asset_id = entry.get("asset_id")
        if isinstance(source_asset, str) and isinstance(asset_id, str):
            result[source_asset] = asset_id
    return result


def _previous_by_item_id(previous_catalog: dict[str, Any] | None) -> dict[int, dict[str, Any]]:
    if previous_catalog is None:
        return {}
    entries = previous_catalog.get("items")
    if not isinstance(entries, list):
        raise ProjectLibraryError("previous item catalog items must be an array")
    previous: dict[int, dict[str, Any]] = {}
    for entry in entries:
        if isinstance(entry, dict) and isinstance(entry.get("item_id"), int):
            previous[entry["item_id"]] = entry
    return previous


def _semantic_key_for(
    item_id: int,
    previous: dict[int, dict[str, Any]],
    overrides: dict[int, str],
) -> str:
    override = overrides.get(item_id)
    if override is not None:
        if not SEMANTIC_KEY.fullmatch(override):
            raise ProjectLibraryError(f"invalid semantic key override for {item_id}: {override}")
        return override
    previous_key = previous.get(item_id, {}).get("semantic_key")
    if isinstance(previous_key, str) and SEMANTIC_KEY.fullmatch(previous_key):
        return previous_key
    return f"item.id_{item_id}"


def _aliases_for(
    item_id: int,
    previous: dict[int, dict[str, Any]],
    alias_overrides: dict[int, list[str]],
) -> list[str]:
    if item_id in alias_overrides:
        return list(dict.fromkeys(alias_overrides[item_id]))
    previous_aliases = previous.get(item_id, {}).get("aliases")
    if isinstance(previous_aliases, list) and all(
        isinstance(alias, str) for alias in previous_aliases
    ):
        return list(dict.fromkeys(previous_aliases))
    return []


def _rows(export: dict[str, Any]) -> list[dict[str, Any]]:
    if export.get("schema_version") != 1:
        raise ProjectLibraryError("UGCObject export schema_version must be 1")
    rows = export.get("rows")
    if not isinstance(rows, list):
        raise ProjectLibraryError("UGCObject export rows must be an array")
    if not isinstance(export.get("load_path"), str) or not export["load_path"].strip():
        raise ProjectLibraryError("UGCObject export load_path is required")
    return rows


def build_item_icon_catalog(
    export: dict[str, Any],
    assets: dict[str, Any],
    previous_catalog: dict[str, Any] | None,
    semantic_overrides: dict[int, str],
    alias_overrides: dict[int, list[str]],
) -> dict[str, Any]:
    """Return a project item-icon catalog from a normalized UGCObject export."""

    asset_by_path = _asset_by_unreal_path(assets)
    previous = _previous_by_item_id(previous_catalog)
    rows = _rows(export)
    seen_item_ids: set[int] = set()
    items: list[dict[str, Any]] = []

    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("values"), dict):
            raise ProjectLibraryError("UGCObject rows must contain values objects")
        values = row["values"]
        item_id = _positive_item_id(_field(values, "item_id"), row.get("row_name"))
        if item_id in seen_item_ids:
            raise ProjectLibraryError(f"duplicate item_id: {item_id}")
        seen_item_ids.add(item_id)

        name = _required_text(_field(values, "name"), "name", item_id)
        description = _required_text(_field(values, "description"), "description", item_id)
        raw_icon = _field(values, "icon")
        icon_asset = raw_icon.strip() if isinstance(raw_icon, str) and raw_icon.strip() else None
        asset_id = asset_by_path.get(icon_asset)
        item = {
            "semantic_key": _semantic_key_for(item_id, previous, semantic_overrides),
            "item_id": item_id,
            "name": name,
            "description": description,
            "icon_asset": icon_asset,
            "asset_id": asset_id,
            "aliases": _aliases_for(item_id, previous, alias_overrides),
            "source_table": export["load_path"],
            "row_fingerprint": _fingerprint(row),
            "resolution_status": "resolved" if asset_id is not None else "candidate",
        }
        if asset_id is None:
            item["resolution_reason"] = (
                "missing icon field"
                if icon_asset is None
                else "icon asset is absent from asset catalog"
            )
        items.append(item)

    return {
        "schema_version": 1,
        "project": assets.get("project", {"name": "RedCliff", "slug": "redcliff"}),
        "items": sorted(items, key=lambda item: item["item_id"]),
    }


def _parse_semantic_override(value: str) -> tuple[int, str]:
    raw_item_id, separator, semantic_key = value.partition("=")
    if not separator or not raw_item_id.isdecimal():
        raise ProjectLibraryError(f"semantic override must be ITEM_ID=semantic.key: {value}")
    return int(raw_item_id), semantic_key


def _parse_alias_override(value: str) -> tuple[int, list[str]]:
    raw_item_id, separator, aliases = value.partition("=")
    if not separator or not raw_item_id.isdecimal():
        raise ProjectLibraryError(f"alias override must be ITEM_ID=alias[,alias]: {value}")
    return int(raw_item_id), [alias.strip() for alias in aliases.split(",") if alias.strip()]


def _alias_overrides(values: list[str]) -> dict[int, list[str]]:
    result: dict[int, list[str]] = {}
    for value in values:
        item_id, aliases = _parse_alias_override(value)
        combined = result.setdefault(item_id, [])
        for alias in aliases:
            if alias not in combined:
                combined.append(alias)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a semantic UGCObject item-icon catalog.")
    parser.add_argument("--table-export", required=True, type=Path)
    parser.add_argument("--asset-catalog", required=True, type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--semantic-key", action="append", default=[])
    parser.add_argument("--alias", action="append", default=[])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        semantic_overrides = dict(_parse_semantic_override(value) for value in args.semantic_key)
        alias_overrides = _alias_overrides(args.alias)
        catalog = build_item_icon_catalog(
            read_json_object(args.table_export),
            read_json_object(args.asset_catalog),
            read_json_object(args.previous) if args.previous else None,
            semantic_overrides,
            alias_overrides,
        )
        write_json_object(args.output, catalog)
    except ProjectLibraryError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps({"items": len(catalog["items"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
