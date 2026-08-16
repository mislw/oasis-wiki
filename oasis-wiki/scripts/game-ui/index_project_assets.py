#!/usr/bin/env python3
"""Index project UI assets without reading or modifying Unreal packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from project_library import (
    ProjectLibraryError,
    read_json_object,
    validate_asset_catalog,
    write_json_object,
)


STATE_SUFFIXES = {
    "_normal": "default",
    "_selected": "selected",
    "_active": "selected",
    "_pressed": "pressed",
    "_disabled": "disabled",
    "_gray": "disabled",
    "_locked": "locked",
}
PRESERVED_CLASSIFICATION_FIELDS = {
    "asset_type",
    "visual_role",
    "state_group",
    "state",
    "tags",
    "preview_key",
    "preview_width",
    "preview_height",
    "preview_mode",
    "catalog_status",
}


def sha256_file(path: Path) -> str:
    """Return a streaming SHA-256 digest for *path*."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_asset_segment(value: str) -> str:
    """Normalize one path segment for a stable catalog identifier."""

    normalized = re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")
    normalized = normalized or "asset"
    return f"n_{normalized}" if normalized[0].isdigit() else normalized


def asset_id_for(relative_without_suffix: PurePosixPath, project_slug: str) -> str:
    """Build one stable asset identifier from its UIresources-relative path."""

    normalized = ".".join(normalize_asset_segment(part) for part in relative_without_suffix.parts)
    return f"{normalize_asset_segment(project_slug)}.uiresources.{normalized}"


def state_suggestion(asset_name: str) -> dict[str, str] | None:
    """Return a non-authoritative state grouping suggestion from a known suffix."""

    lowered = asset_name.lower()
    for suffix, state in STATE_SUFFIXES.items():
        if lowered.endswith(suffix):
            return {
                "state_group": asset_name[: -len(suffix)],
                "state": state,
                "reason": f"filename suffix {suffix}",
            }
    return None


def build_asset_catalog(
    project_root: Path,
    project_slug: str,
    previous_catalog: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Build a deterministic catalog and drift records for `Asset/UIresources`."""

    ui_root = project_root / "Asset" / "UIresources"
    previous_entries = {
        entry["asset_id"]: entry
        for entry in (previous_catalog or {}).get("assets", [])
        if isinstance(entry, dict) and isinstance(entry.get("asset_id"), str)
    }
    assets: list[dict[str, Any]] = []
    history: list[dict[str, Any]] = []
    timestamp = datetime.now(timezone.utc).isoformat()

    source_files = sorted(
        (path for path in ui_root.rglob("*.uasset") if path.is_file()),
        key=lambda path: path.relative_to(project_root).as_posix().casefold(),
    ) if ui_root.is_dir() else []

    for source in source_files:
        project_relative = source.relative_to(project_root)
        ui_relative = source.relative_to(ui_root)
        source_file = project_relative.as_posix()
        asset_name = source.stem
        asset_id = asset_id_for(PurePosixPath(*ui_relative.with_suffix("").parts), project_slug)
        digest = sha256_file(source)
        category = ui_relative.parent.as_posix()
        if category == ".":
            category = "root"
        source_asset = (
            f"/{project_root.name}/Asset/UIresources/"
            f"{ui_relative.with_suffix('').as_posix()}.{asset_name}"
        )
        entry: dict[str, Any] = {
            "asset_id": asset_id,
            "source_asset": source_asset,
            "source_file": source_file,
            "category": category,
            "asset_type": "unknown",
            "source_size": source.stat().st_size,
            "source_sha256": digest,
            "catalog_status": "indexed",
        }
        suggestion = state_suggestion(asset_name)
        if suggestion:
            entry["classification_suggestion"] = suggestion

        previous = previous_entries.get(asset_id)
        if previous and previous.get("source_sha256") == digest:
            for field in PRESERVED_CLASSIFICATION_FIELDS:
                if field in previous:
                    entry[field] = previous[field]
        elif previous:
            history.append({
                "timestamp": timestamp,
                "action": "asset_changed",
                "asset_id": asset_id,
                "source_file": source_file,
                "old_source_sha256": previous.get("source_sha256"),
                "new_source_sha256": digest,
            })
        else:
            history.append({
                "timestamp": timestamp,
                "action": "asset_added",
                "asset_id": asset_id,
                "source_file": source_file,
                "source_sha256": digest,
            })
        assets.append(entry)

    current_ids = {entry["asset_id"] for entry in assets}
    for asset_id, previous in sorted(previous_entries.items()):
        if asset_id not in current_ids:
            history.append({
                "timestamp": timestamp,
                "action": "asset_removed",
                "asset_id": asset_id,
                "source_file": previous.get("source_file"),
                "source_sha256": previous.get("source_sha256"),
            })

    project = dict((previous_catalog or {}).get("project") or {})
    project.setdefault("name", project_root.name)
    project["slug"] = project_slug
    return {"schema_version": 1, "project": project, "assets": assets}, history


def append_history(path: Path, records: list[dict[str, Any]]) -> None:
    """Append drift records as UTF-8 JSON Lines."""

    if not records:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Index project UIresources assets.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--history", required=True, type=Path)
    args = parser.parse_args()
    project_root = args.project_root.resolve()
    catalog_path = args.catalog.resolve()
    try:
        previous = read_json_object(catalog_path) if catalog_path.is_file() else None
        project_slug = (
            str(previous.get("project", {}).get("slug"))
            if previous and previous.get("project", {}).get("slug")
            else project_root.name.lower()
        )
        catalog, history = build_asset_catalog(project_root, project_slug, previous)
        errors = validate_asset_catalog(catalog, project_root)
        if errors:
            raise ProjectLibraryError("; ".join(errors))
        write_json_object(catalog_path, catalog)
        append_history(args.history.resolve(), history)
    except ProjectLibraryError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps({"assets": len(catalog["assets"]), "history": len(history)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
