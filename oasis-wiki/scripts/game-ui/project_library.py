#!/usr/bin/env python3
"""Read and validate project-specific game UI library manifests."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from validate_library import validate_profile


class ProjectLibraryError(ValueError):
    """Raised when project UI library data cannot be read or validated."""


CATALOG_STATUSES = {"indexed", "previewed", "classified", "ignored"}
PREVIEW_SOURCES = {"asset_export", "approved_transparent_cutout", "editor_reconstruction", "user_reference"}
COMPONENT_STATUSES = {"active", "candidate", "pending_review", "deprecated", "rejected"}
ITEM_RESOLUTION_STATUSES = {"resolved", "candidate"}
PREVIEW_KEY = re.compile(r"^sha256:[0-9a-f]{64}$")
UNREAL_OBJECT_PATH = re.compile(
    r"^/[A-Za-z0-9_]+(?:/[A-Za-z0-9_]+)+\.[A-Za-z0-9_]+$"
)
IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")


def read_json_object(path: Path) -> dict[str, Any]:
    """Read one UTF-8 JSON object from *path*."""

    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProjectLibraryError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProjectLibraryError(f"JSON root must be an object: {path}")
    return value


def write_json_object(path: Path, value: object) -> None:
    """Write one stable UTF-8 JSON document."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _is_machine_absolute_path(value: str) -> bool:
    normalized = value.strip()
    if not normalized:
        return False
    if re.match(r"^[A-Za-z]:[\\/]", normalized):
        return True
    if normalized.startswith(("\\\\", "//", "file:")):
        return True
    if normalized.startswith("/") and not UNREAL_OBJECT_PATH.fullmatch(normalized):
        return True
    return False


def _absolute_path_errors(value: object, prefix: str = "manifest") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            errors.extend(_absolute_path_errors(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_absolute_path_errors(child, f"{prefix}[{index}]"))
    elif isinstance(value, str) and _is_machine_absolute_path(value):
        errors.append(f"{prefix} contains a machine-specific absolute path")
    return errors


def _validate_common_catalog(catalog: dict[str, Any], array_name: str) -> list[str]:
    errors: list[str] = []
    if catalog.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    project = catalog.get("project")
    if not isinstance(project, dict) or not project.get("name") or not project.get("slug"):
        errors.append("project requires name and slug")
    if not isinstance(catalog.get(array_name), list):
        errors.append(f"{array_name} must be an array")
    errors.extend(_absolute_path_errors(catalog))
    return errors


def _is_project_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if "\\" in value or value.startswith("/") or _is_machine_absolute_path(value):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "." not in path.parts


def _asset_map(assets: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = assets.get("assets", [])
    if not isinstance(entries, list):
        return {}
    return {
        entry["asset_id"]: entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("asset_id"), str)
    }


def validate_asset_catalog(catalog: dict[str, Any], project_root: Path) -> list[str]:
    """Validate the source-asset inventory against *project_root*."""

    errors = _validate_common_catalog(catalog, "assets")
    entries = catalog.get("assets")
    if not isinstance(entries, list):
        return sorted(set(errors))

    identifiers: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"assets[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        asset_id = entry.get("asset_id")
        if not isinstance(asset_id, str) or not IDENTIFIER.fullmatch(asset_id):
            errors.append(f"{prefix}.asset_id is invalid")
        elif asset_id in identifiers:
            errors.append(f"duplicate asset_id: {asset_id}")
        else:
            identifiers.add(asset_id)

        source_file = entry.get("source_file")
        if not _is_project_relative_path(source_file):
            errors.append(f"{prefix}.source_file must be project-relative with forward slashes")
        elif not (project_root / PurePosixPath(source_file)).is_file():
            errors.append(f"{prefix}.source_file does not exist: {source_file}")

        source_asset = entry.get("source_asset")
        if not isinstance(source_asset, str) or not UNREAL_OBJECT_PATH.fullmatch(source_asset):
            errors.append(f"{prefix}.source_asset must be a normalized Unreal object path")

        category = entry.get("category")
        if not _is_project_relative_path(category):
            errors.append(f"{prefix}.category must be a forward-slash relative path")

        status = entry.get("catalog_status")
        if status not in CATALOG_STATUSES:
            errors.append(f"{prefix}.catalog_status is invalid: {status}")

        preview_key = entry.get("preview_key")
        if preview_key is not None and (
            not isinstance(preview_key, str) or not PREVIEW_KEY.fullmatch(preview_key)
        ):
            errors.append(f"{prefix}.preview_key is invalid")
        if status in {"previewed", "classified"} and preview_key is None:
            errors.append(f"{prefix}.preview_key is required for {status} status")
        preview_source = entry.get("preview_source")
        if preview_source is not None and preview_source not in PREVIEW_SOURCES:
            errors.append(f"{prefix}.preview_source is invalid: {preview_source}")
    return sorted(set(errors))


def validate_item_icon_catalog(
    catalog: dict[str, Any], assets: dict[str, Any]
) -> list[str]:
    """Validate semantic item-to-icon relationships."""

    errors = _validate_common_catalog(catalog, "items")
    entries = catalog.get("items")
    if not isinstance(entries, list):
        return sorted(set(errors))
    known_assets = _asset_map(assets)
    semantic_keys: set[str] = set()
    item_ids: set[int] = set()

    for index, entry in enumerate(entries):
        prefix = f"items[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        semantic_key = entry.get("semantic_key")
        if not isinstance(semantic_key, str) or not IDENTIFIER.fullmatch(semantic_key):
            errors.append(f"{prefix}.semantic_key is invalid")
        elif semantic_key in semantic_keys:
            errors.append(f"duplicate semantic_key: {semantic_key}")
        else:
            semantic_keys.add(semantic_key)

        item_id = entry.get("item_id")
        if isinstance(item_id, bool) or not isinstance(item_id, int) or item_id <= 0:
            errors.append(f"{prefix}.item_id must be a positive integer")
        elif item_id in item_ids:
            errors.append(f"duplicate item_id: {item_id}")
        else:
            item_ids.add(item_id)

        resolution_status = entry.get("resolution_status")
        if resolution_status not in ITEM_RESOLUTION_STATUSES:
            errors.append(f"{prefix}.resolution_status is invalid: {resolution_status}")
        icon_asset = entry.get("icon_asset")
        asset_id = entry.get("asset_id")
        if resolution_status == "resolved":
            if not isinstance(icon_asset, str) or not UNREAL_OBJECT_PATH.fullmatch(icon_asset):
                errors.append(f"{prefix}.icon_asset must be a normalized Unreal object path")
            if not isinstance(asset_id, str) or asset_id not in known_assets:
                errors.append(f"{prefix} references missing asset_id: {asset_id}")
            elif known_assets[asset_id].get("source_asset") != icon_asset:
                errors.append(f"{prefix}.icon_asset does not match asset_id {asset_id}")
        elif resolution_status == "candidate":
            if icon_asset is not None and (
                not isinstance(icon_asset, str) or not UNREAL_OBJECT_PATH.fullmatch(icon_asset)
            ):
                errors.append(f"{prefix}.icon_asset must be null or a normalized Unreal object path")
            if asset_id is not None and asset_id not in known_assets:
                errors.append(f"{prefix} references missing asset_id: {asset_id}")
            if not isinstance(entry.get("resolution_reason"), str) or not entry[
                "resolution_reason"
            ].strip():
                errors.append(f"{prefix}.resolution_reason is required for candidate status")

        fingerprint = entry.get("row_fingerprint")
        if not isinstance(fingerprint, str) or not PREVIEW_KEY.fullmatch(fingerprint):
            errors.append(f"{prefix}.row_fingerprint is invalid")
        aliases = entry.get("aliases")
        if not isinstance(aliases, list) or not all(isinstance(alias, str) for alias in aliases):
            errors.append(f"{prefix}.aliases must be an array of strings")
        for field in ("name", "description", "source_table"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{prefix}.{field} is required")
    return sorted(set(errors))


def validate_component_asset_catalog(
    catalog: dict[str, Any], assets: dict[str, Any], profile: dict[str, Any]
) -> list[str]:
    """Validate component-state references without promoting component status."""

    errors = _validate_common_catalog(catalog, "components")
    entries = catalog.get("components")
    if not isinstance(entries, list):
        return sorted(set(errors))
    known_assets = set(_asset_map(assets))
    profile_components = profile.get("components", [])
    known_components = {
        entry.get("component_id")
        for entry in profile_components
        if isinstance(entry, dict) and entry.get("status") in COMPONENT_STATUSES
    } if isinstance(profile_components, list) else set()
    identifiers: set[str] = set()

    for index, entry in enumerate(entries):
        prefix = f"components[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        component_id = entry.get("component_id")
        if not isinstance(component_id, str) or not IDENTIFIER.fullmatch(component_id):
            errors.append(f"{prefix}.component_id is invalid")
        elif component_id in identifiers:
            errors.append(f"duplicate component_id: {component_id}")
        else:
            identifiers.add(component_id)
        if component_id not in known_components:
            errors.append(f"{component_id} is missing from profile")

        states = entry.get("states")
        if not isinstance(states, dict) or not states:
            errors.append(f"{prefix}.states must be a non-empty object")
            continue
        for state, asset_ids in states.items():
            state_prefix = f"{prefix}.states.{state}"
            if not isinstance(state, str) or not state:
                errors.append(f"{prefix}.states contains an invalid state")
            if not isinstance(asset_ids, list) or not asset_ids:
                errors.append(f"{state_prefix} must be a non-empty array")
                continue
            for asset_id in asset_ids:
                if not isinstance(asset_id, str) or asset_id not in known_assets:
                    errors.append(f"{state_prefix} references missing asset_id: {asset_id}")
    return sorted(set(errors))


def preview_path_for_key(cache_root: Path, preview_key: str) -> Path:
    """Resolve a validated preview key inside the local cache."""

    if not PREVIEW_KEY.fullmatch(preview_key):
        raise ProjectLibraryError(f"invalid preview key: {preview_key}")
    return cache_root / "previews" / f"{preview_key.removeprefix('sha256:')}.png"


def validate_project_library(
    library_root: Path, project_root: Path, cache_root: Path | None
) -> list[str]:
    """Validate a complete project library and, when supplied, its preview cache."""

    paths = {
        "profile": library_root / "profile.json",
        "assets": library_root / "catalogs" / "assets.json",
        "items": library_root / "catalogs" / "item-icons.json",
        "components": library_root / "catalogs" / "component-assets.json",
    }
    values: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for name, path in paths.items():
        try:
            values[name] = read_json_object(path)
        except ProjectLibraryError as exc:
            errors.append(str(exc))
    if errors:
        return sorted(set(errors))

    if values["profile"].get("schema_version") != 1:
        errors.append("profile.schema_version must be 1")
    errors.extend(f"profile.{error}" for error in validate_profile(values["profile"]))
    errors.extend(_absolute_path_errors(values["profile"], "profile"))
    errors.extend(validate_asset_catalog(values["assets"], project_root))
    errors.extend(validate_item_icon_catalog(values["items"], values["assets"]))
    errors.extend(
        validate_component_asset_catalog(
            values["components"], values["assets"], values["profile"]
        )
    )

    project_slugs = {
        value.get("project", {}).get("slug")
        for value in values.values()
        if isinstance(value.get("project"), dict)
    }
    if len(project_slugs) != 1:
        errors.append("profile and catalog project slugs must match")

    if cache_root is not None:
        for entry in values["assets"].get("assets", []):
            if not isinstance(entry, dict) or not isinstance(entry.get("preview_key"), str):
                continue
            try:
                preview = preview_path_for_key(cache_root, entry["preview_key"])
            except ProjectLibraryError as exc:
                errors.append(str(exc))
                continue
            if not preview.is_file():
                errors.append(f"cached preview is missing for {entry.get('asset_id')}: {entry['preview_key']}")
    return sorted(set(errors))
