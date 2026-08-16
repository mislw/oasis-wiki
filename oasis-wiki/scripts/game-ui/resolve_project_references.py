#!/usr/bin/env python3
"""Resolve active project-library components and semantic item icons to references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from project_library import (
    ProjectLibraryError,
    preview_path_for_key,
    read_json_object,
    validate_component_asset_catalog,
    validate_item_icon_catalog,
    write_json_object,
)


ACTIVE_STATUS = "active"


def _asset_map(assets: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = assets.get("assets")
    if not isinstance(entries, list):
        raise ProjectLibraryError("asset catalog assets must be an array")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        asset_id = entry.get("asset_id")
        if isinstance(asset_id, str):
            if asset_id in result:
                raise ProjectLibraryError(f"duplicate asset_id: {asset_id}")
            result[asset_id] = entry
    return result


def _profile_component_map(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = profile.get("components")
    if not isinstance(entries, list):
        raise ProjectLibraryError("profile components must be an array")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        component_id = entry.get("component_id")
        if isinstance(component_id, str):
            if component_id in result:
                raise ProjectLibraryError(f"duplicate component_id: {component_id}")
            result[component_id] = entry
    return result


def _component_asset_map(component_assets: dict[str, Any]) -> dict[str, dict[str, list[str]]]:
    entries = component_assets.get("components")
    if not isinstance(entries, list):
        raise ProjectLibraryError("component asset catalog components must be an array")
    result: dict[str, dict[str, list[str]]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        component_id = entry.get("component_id")
        states = entry.get("states")
        if not isinstance(component_id, str) or not isinstance(states, dict):
            continue
        if component_id in result:
            raise ProjectLibraryError(f"duplicate component_id: {component_id}")
        state_map: dict[str, list[str]] = {}
        for state, asset_ids in states.items():
            if isinstance(state, str) and isinstance(asset_ids, list):
                state_map[state] = [
                    asset_id for asset_id in asset_ids if isinstance(asset_id, str)
                ]
        result[component_id] = state_map
    return result


def _item_map(items: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = items.get("items")
    if not isinstance(entries, list):
        raise ProjectLibraryError("item icon catalog items must be an array")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        semantic_key = entry.get("semantic_key")
        if isinstance(semantic_key, str):
            if semantic_key in result:
                raise ProjectLibraryError(f"duplicate semantic_key: {semantic_key}")
            result[semantic_key] = entry
    return result


def _reference_record(
    records: dict[str, dict[str, Any]],
    assets_by_id: dict[str, dict[str, Any]],
    cache_root: Path,
    asset_id: str,
) -> dict[str, Any]:
    asset = assets_by_id.get(asset_id)
    if asset is None:
        raise ProjectLibraryError(f"missing asset_id: {asset_id}")
    if asset.get("catalog_status") not in {"previewed", "classified"}:
        raise ProjectLibraryError(f"asset is not preview-ready: {asset_id}")
    preview_key = asset.get("preview_key")
    if not isinstance(preview_key, str):
        raise ProjectLibraryError(f"asset has no preview_key: {asset_id}")
    source = preview_path_for_key(cache_root, preview_key)
    if not source.is_file():
        raise ProjectLibraryError(f"cached preview is missing for {asset_id}: {preview_key}")
    record = records.get(asset_id)
    if record is not None:
        return record
    source_asset = asset.get("source_asset")
    if not isinstance(source_asset, str):
        raise ProjectLibraryError(f"asset has no source_asset: {asset_id}")
    record = {
        "source": str(source.resolve()),
        "role": "style",
        "priority": 1,
        "copy_visual_style": True,
        "source_kind": "project_library_asset",
        "library": {
            "asset_id": asset_id,
            "preview_key": preview_key,
            "component_ids": [],
            "semantic_keys": [],
            "states": [],
            "source_asset": source_asset,
        },
    }
    records[asset_id] = record
    return record


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def resolve_project_references(
    profile: dict[str, Any],
    assets: dict[str, Any],
    items: dict[str, Any],
    component_assets: dict[str, Any],
    cache_root: Path,
    component_ids: list[str],
    semantic_keys: list[str],
) -> dict[str, Any]:
    """Resolve requested active components and semantic items to style references."""

    errors = validate_component_asset_catalog(component_assets, assets, profile)
    errors.extend(validate_item_icon_catalog(items, assets))
    if errors:
        raise ProjectLibraryError("; ".join(sorted(set(errors))))
    assets_by_id = _asset_map(assets)
    profile_components = _profile_component_map(profile)
    component_mappings = _component_asset_map(component_assets)
    items_by_key = _item_map(items)
    records: dict[str, dict[str, Any]] = {}

    for component_id in dict.fromkeys(component_ids):
        component = profile_components.get(component_id)
        if component is None:
            raise ProjectLibraryError(f"unknown component_id: {component_id}")
        if component.get("status") != ACTIVE_STATUS:
            raise ProjectLibraryError(f"{component_id} is not active")
        states = component_mappings.get(component_id)
        if not states:
            raise ProjectLibraryError(f"{component_id} has no component asset mapping")
        for state, asset_ids in states.items():
            for asset_id in asset_ids:
                record = _reference_record(records, assets_by_id, cache_root, asset_id)
                library = record["library"]
                _append_unique(library["component_ids"], component_id)
                _append_unique(library["states"], state)

    for semantic_key in dict.fromkeys(semantic_keys):
        item = items_by_key.get(semantic_key)
        if item is None:
            raise ProjectLibraryError(f"unknown semantic_key: {semantic_key}")
        if item.get("resolution_status") != "resolved":
            raise ProjectLibraryError(f"{semantic_key} is not resolved")
        asset_id = item.get("asset_id")
        if not isinstance(asset_id, str):
            raise ProjectLibraryError(f"{semantic_key} has no asset_id")
        record = _reference_record(records, assets_by_id, cache_root, asset_id)
        _append_unique(record["library"]["semantic_keys"], semantic_key)

    references = sorted(
        records.values(),
        key=lambda reference: (
            reference["library"]["component_ids"],
            reference["library"]["semantic_keys"],
            reference["library"]["asset_id"],
        ),
    )
    for index, reference in enumerate(references, start=1):
        reference["priority"] = index
    return {"schema_version": 1, "references": references}


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve project UI library references.")
    parser.add_argument("--library-root", required=True, type=Path)
    parser.add_argument("--cache-root", required=True, type=Path)
    parser.add_argument("--component", action="append", default=[])
    parser.add_argument("--semantic-key", action="append", default=[])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        library_root = args.library_root.resolve()
        references = resolve_project_references(
            read_json_object(library_root / "profile.json"),
            read_json_object(library_root / "catalogs" / "assets.json"),
            read_json_object(library_root / "catalogs" / "item-icons.json"),
            read_json_object(library_root / "catalogs" / "component-assets.json"),
            args.cache_root.resolve(),
            args.component,
            args.semantic_key,
        )
        write_json_object(args.output, references)
    except ProjectLibraryError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps({"references": len(references["references"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
