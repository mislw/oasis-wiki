#!/usr/bin/env python3
"""Import exported UI images into a project-local content-addressed cache."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from project_library import (
    ProjectLibraryError,
    preview_path_for_key,
    read_json_object,
    write_json_object,
)


SUPPORTED_EXTENSIONS = {".png", ".tga", ".jpg", ".jpeg"}


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _export_files(staging_root: Path) -> dict[str, list[Path]]:
    if not staging_root.is_dir():
        raise ProjectLibraryError(f"staging directory does not exist: {staging_root}")
    by_stem: dict[str, list[Path]] = {}
    for path in sorted(staging_root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if path.is_file() and path.suffix.casefold() in SUPPORTED_EXTENSIONS:
            by_stem.setdefault(path.stem.casefold(), []).append(path)
    return by_stem


def _asset_stem(entry: dict[str, Any]) -> str:
    source_file = entry.get("source_file")
    if not isinstance(source_file, str) or not source_file:
        raise ProjectLibraryError(f"asset has no source_file: {entry.get('asset_id')}")
    return Path(source_file).stem.casefold()


def _mapping_path(staging_root: Path, value: Path) -> Path:
    path = value if value.is_absolute() else staging_root / value
    if not path.is_file():
        raise ProjectLibraryError(f"mapped preview does not exist: {value}")
    if path.suffix.casefold() not in SUPPORTED_EXTENSIONS:
        raise ProjectLibraryError(f"mapped preview has unsupported extension: {value}")
    return path


def _resolve_exports(
    entries: list[dict[str, Any]],
    staging_root: Path,
    explicit_mapping: dict[str, Path],
) -> dict[str, Path]:
    by_stem = _export_files(staging_root)
    entries_by_stem: dict[str, list[dict[str, Any]]] = {}
    known_ids: set[str] = set()
    for entry in entries:
        asset_id = entry.get("asset_id")
        if not isinstance(asset_id, str) or not asset_id:
            raise ProjectLibraryError("asset entry has no asset_id")
        if asset_id in known_ids:
            raise ProjectLibraryError(f"duplicate asset_id: {asset_id}")
        known_ids.add(asset_id)
        if entry.get("catalog_status") != "ignored":
            entries_by_stem.setdefault(_asset_stem(entry), []).append(entry)

    unknown_mapping = sorted(set(explicit_mapping) - known_ids)
    if unknown_mapping:
        raise ProjectLibraryError(
            "mapping references unknown asset_id: " + ", ".join(unknown_mapping)
        )

    resolved: dict[str, Path] = {}
    for stem, stem_entries in sorted(entries_by_stem.items()):
        candidates = by_stem.get(stem, [])
        if len(stem_entries) > 1:
            missing = [
                entry["asset_id"]
                for entry in stem_entries
                if entry["asset_id"] not in explicit_mapping
            ]
            if candidates and missing:
                raise ProjectLibraryError(
                    f"ambiguous export stem {stem}; explicit mapping required for: "
                    + ", ".join(missing)
                )
        for entry in stem_entries:
            asset_id = entry["asset_id"]
            mapped = explicit_mapping.get(asset_id)
            if mapped is not None:
                resolved[asset_id] = _mapping_path(staging_root, mapped)
            elif len(candidates) == 1:
                resolved[asset_id] = candidates[0]
            elif len(candidates) > 1:
                raise ProjectLibraryError(
                    f"ambiguous export stem {stem}; explicit mapping required for: {asset_id}"
                )
    return resolved


def _normalize_preview(source: Path) -> tuple[bytes, int, int]:
    try:
        with Image.open(source) as image:
            image.load()
            normalized = image.convert("RGBA")
            width, height = normalized.size
            buffer = io.BytesIO()
            normalized.save(buffer, format="PNG")
    except (OSError, ValueError) as exc:
        raise ProjectLibraryError(f"cannot import preview {source.name}: {exc}") from exc
    if width <= 0 or height <= 0:
        raise ProjectLibraryError(f"cannot import preview {source.name}: empty image")
    return buffer.getvalue(), width, height


def _write_bytes_once(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        if path.read_bytes() != value:
            raise ProjectLibraryError(f"cache hash collision: {path.name}")
        return
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def import_previews(
    asset_catalog: dict[str, Any],
    staging_root: Path,
    cache_root: Path,
    explicit_mapping: dict[str, Path],
) -> dict[str, Any]:
    """Cache readable exports and return an updated copy of *asset_catalog*."""

    raw_entries = asset_catalog.get("assets")
    if not isinstance(raw_entries, list) or not all(
        isinstance(entry, dict) for entry in raw_entries
    ):
        raise ProjectLibraryError("asset catalog assets must be an array of objects")
    updated = deepcopy(asset_catalog)
    entries = updated["assets"]
    resolved = _resolve_exports(entries, staging_root.resolve(), explicit_mapping)
    imported: dict[str, tuple[str, int, int, str]] = {}

    for entry in entries:
        asset_id = entry["asset_id"]
        source = resolved.get(asset_id)
        if source is None:
            continue
        png_bytes, width, height = _normalize_preview(source)
        preview_digest = _sha256_bytes(png_bytes)
        preview_key = f"sha256:{preview_digest}"
        cached = preview_path_for_key(cache_root, preview_key)
        _write_bytes_once(cached, png_bytes)
        metadata = {
            "schema_version": 1,
            "width": width,
            "height": height,
            "mode": "RGBA",
            "source_export_sha256": _sha256_file(source),
            "preview_sha256": preview_digest,
        }
        write_json_object(cache_root / "metadata" / f"{preview_digest}.json", metadata)
        imported[asset_id] = (preview_key, width, height, "RGBA")

    for entry in entries:
        imported_values = imported.get(entry["asset_id"])
        if imported_values is None:
            continue
        preview_key, width, height, mode = imported_values
        entry["preview_key"] = preview_key
        entry["preview_width"] = width
        entry["preview_height"] = height
        entry["preview_mode"] = mode
        entry["preview_source"] = "asset_export"
        if entry.get("catalog_status") == "indexed":
            entry["catalog_status"] = "previewed"
    return updated


def group_assets_by_categories(
    asset_entries: list[dict[str, Any]], categories: list[str]
) -> dict[str, list[dict[str, Any]]]:
    """Assign each asset to the most specific requested category once."""

    if not categories:
        return {"all": list(asset_entries)}
    unique = list(dict.fromkeys(category.strip("/") for category in categories if category.strip("/")))
    ordered = sorted(unique, key=lambda value: (-len(Path(value).parts), unique.index(value)))
    assigned: set[str] = set()
    groups: dict[str, list[dict[str, Any]]] = {}
    for category in ordered:
        prefix = category + "/"
        matches = []
        for entry in asset_entries:
            asset_id = entry.get("asset_id")
            entry_category = entry.get("category")
            if (
                isinstance(asset_id, str)
                and asset_id not in assigned
                and isinstance(entry_category, str)
                and (entry_category == category or entry_category.startswith(prefix))
            ):
                matches.append(entry)
                assigned.add(asset_id)
        groups[category] = matches
    return groups


def build_contact_sheet(
    asset_entries: list[dict[str, Any]],
    cache_root: Path,
    output: Path,
    columns: int = 6,
) -> Path:
    """Render cached previews and asset identifiers into one review sheet."""

    if columns <= 0:
        raise ProjectLibraryError("contact sheet columns must be positive")
    entries = sorted(
        (entry for entry in asset_entries if isinstance(entry.get("preview_key"), str)),
        key=lambda entry: str(entry.get("source_file", entry.get("asset_id", ""))).casefold(),
    )
    if not entries:
        raise ProjectLibraryError("contact sheet has no cached previews")

    actual_columns = min(columns, len(entries))
    cell_width = 220
    cell_height = 190
    preview_box = (180, 128)
    rows = (len(entries) + actual_columns - 1) // actual_columns
    sheet = Image.new(
        "RGBA",
        (actual_columns * cell_width, rows * cell_height),
        (32, 35, 40, 255),
    )
    draw = ImageDraw.Draw(sheet)

    for index, entry in enumerate(entries):
        preview = preview_path_for_key(cache_root, entry["preview_key"])
        if not preview.is_file():
            raise ProjectLibraryError(f"cached preview is missing for {entry.get('asset_id')}")
        try:
            with Image.open(preview) as image:
                image.load()
                thumbnail = image.convert("RGBA")
        except (OSError, ValueError) as exc:
            raise ProjectLibraryError(
                f"cannot read cached preview for {entry.get('asset_id')}: {exc}"
            ) from exc
        thumbnail.thumbnail(preview_box, Image.Resampling.LANCZOS)
        column = index % actual_columns
        row = index // actual_columns
        cell_x = column * cell_width
        cell_y = row * cell_height
        image_x = cell_x + (cell_width - thumbnail.width) // 2
        image_y = cell_y + 8 + (preview_box[1] - thumbnail.height) // 2
        sheet.alpha_composite(thumbnail, (image_x, image_y))
        draw.rectangle(
            (cell_x, cell_y, cell_x + cell_width - 1, cell_y + cell_height - 1),
            outline=(82, 88, 98, 255),
        )
        source_file = str(entry.get("source_file", "unknown"))
        label = Path(source_file).stem
        if len(label) > 34:
            label = label[:31] + "..."
        draw.text((cell_x + 8, cell_y + 144), label, fill=(240, 242, 245, 255))
        draw.text(
            (cell_x + 8, cell_y + 162),
            str(entry.get("category", ""))[:34],
            fill=(170, 178, 190, 255),
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG")
    return output


def _read_mapping(path: Path | None) -> dict[str, Path]:
    if path is None:
        return {}
    value = read_json_object(path)
    raw = value.get("mappings", value)
    if not isinstance(raw, dict) or not all(
        isinstance(asset_id, str) and isinstance(source, str)
        for asset_id, source in raw.items()
    ):
        raise ProjectLibraryError("mapping JSON must map asset IDs to file paths")
    return {asset_id: Path(source) for asset_id, source in raw.items()}


def _sheet_name(category: str) -> str:
    name = re.sub(r"[^a-z0-9]+", "-", category.casefold()).strip("-")
    return name or "all"


def main() -> int:
    parser = argparse.ArgumentParser(description="Import project UI preview exports.")
    parser.add_argument("--asset-catalog", required=True, type=Path)
    parser.add_argument("--staging", required=True, type=Path)
    parser.add_argument("--cache-root", required=True, type=Path)
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--mapping", type=Path)
    parser.add_argument("--contact-sheets", action="store_true")
    args = parser.parse_args()

    try:
        catalog_path = args.asset_catalog.resolve()
        catalog = read_json_object(catalog_path)
        raw_entries = catalog.get("assets")
        if not isinstance(raw_entries, list) or not all(
            isinstance(entry, dict) for entry in raw_entries
        ):
            raise ProjectLibraryError("asset catalog assets must be an array of objects")
        groups = group_assets_by_categories(raw_entries, args.category)
        selected_ids = {
            entry["asset_id"]
            for entries in groups.values()
            for entry in entries
            if isinstance(entry.get("asset_id"), str)
        }
        selected_catalog = deepcopy(catalog)
        selected_catalog["assets"] = [
            entry for entry in selected_catalog["assets"] if entry.get("asset_id") in selected_ids
        ]
        raw_mapping = _read_mapping(args.mapping.resolve() if args.mapping else None)
        selected_mapping = {
            asset_id: path for asset_id, path in raw_mapping.items() if asset_id in selected_ids
        }
        updated_selected = import_previews(
            selected_catalog,
            args.staging.resolve(),
            args.cache_root.resolve(),
            selected_mapping,
        )
        updates = {entry["asset_id"]: entry for entry in updated_selected["assets"]}
        updated_catalog = deepcopy(catalog)
        updated_catalog["assets"] = [
            updates.get(entry.get("asset_id"), entry) for entry in updated_catalog["assets"]
        ]

        sheets: list[str] = []
        if args.contact_sheets:
            updated_by_id = {entry["asset_id"]: entry for entry in updated_catalog["assets"]}
            for category, entries in groups.items():
                contact_entries = [
                    updated_by_id[entry["asset_id"]]
                    for entry in entries
                    if isinstance(updated_by_id[entry["asset_id"]].get("preview_key"), str)
                ]
                if not contact_entries:
                    continue
                output = args.cache_root.resolve() / "contact-sheets" / f"{_sheet_name(category)}.png"
                build_contact_sheet(contact_entries, args.cache_root.resolve(), output)
                sheets.append(output.name)

        write_json_object(catalog_path, updated_catalog)
    except ProjectLibraryError as exc:
        print(f"ERROR: {exc}")
        return 1

    imported_count = sum(
        1 for entry in updated_selected["assets"] if entry.get("catalog_status") == "previewed"
    )
    print(json.dumps({"previewed": imported_count, "contact_sheets": sheets}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
