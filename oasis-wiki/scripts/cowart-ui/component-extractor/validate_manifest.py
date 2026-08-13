from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from component_semantics import NODE_KINDS, RECONSTRUCTION_STATUSES, RENDER_MODES, activation_gate_errors


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)+$")


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"invalid JSON: {exc}"]
    schema_version = manifest.get("schema_version")
    if schema_version not in (1, 2, 3):
        errors.append("schema_version must be 1, 2, or 3")
    source = manifest.get("source")
    page_size = source.get("page_size") if isinstance(source, dict) else None
    width = page_size.get("width") if isinstance(page_size, dict) else None
    height = page_size.get("height") if isinstance(page_size, dict) else None
    if not isinstance(width, (int, float)) or width <= 0:
        errors.append("source.page_size.width must be positive")
    if not isinstance(height, (int, float)) or height <= 0:
        errors.append("source.page_size.height must be positive")
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        return errors + ["components must be a non-empty array"]

    ids: set[str] = set()
    parents: dict[str, str] = {}
    for index, component in enumerate(components):
        prefix = f"components[{index}]"
        if not isinstance(component, dict):
            errors.append(f"{prefix} must be an object")
            continue
        component_id = component.get("component_id")
        if not isinstance(component_id, str) or not ID_PATTERN.fullmatch(component_id):
            errors.append(f"{prefix}.component_id must be a lowercase dot-separated ID")
            continue
        if component_id in ids:
            errors.append(f"duplicate component_id: {component_id}")
        ids.add(component_id)
        parent_id = component.get("parent_id")
        if not isinstance(parent_id, str):
            errors.append(f"{prefix}.parent_id is required")
        else:
            parents[component_id] = parent_id
        if component.get("status") not in ("pending_review", "candidate"):
            errors.append(f"{prefix}.status must be pending_review or candidate")
        for field in ("layer", "z_index"):
            if not isinstance(component.get(field), (int, float)):
                errors.append(f"{prefix}.{field} must be numeric")
        file_values: list[tuple[str, str]] = []
        if schema_version == 1:
            file_value = component.get("file")
            if not isinstance(file_value, str):
                errors.append(f"{prefix}.file is required")
            else:
                file_values.append(("file", file_value))
        else:
            node_kind = component.get("node_kind")
            render_mode = component.get("render_mode")
            visual_assets = component.get("visual_assets")
            review = component.get("review")
            if node_kind not in NODE_KINDS:
                errors.append(f"{prefix}.node_kind must be one of {sorted(NODE_KINDS)}")
            if render_mode not in RENDER_MODES:
                errors.append(f"{prefix}.render_mode must be one of {sorted(RENDER_MODES)}")
            if not isinstance(visual_assets, dict):
                errors.append(f"{prefix}.visual_assets is required")
            else:
                expected_assets = ("source_crop", "clean_layer", "assembly_preview")
                if schema_version == 3 and set(visual_assets) != set(expected_assets):
                    errors.append(f"{prefix}.visual_assets must contain only source_crop, clean_layer, and assembly_preview")
                for asset_name in expected_assets:
                    asset_value = visual_assets.get(asset_name)
                    if asset_value is not None and not isinstance(asset_value, str):
                        errors.append(f"{prefix}.visual_assets.{asset_name} must be a path or null")
                    elif isinstance(asset_value, str):
                        file_values.append((f"visual_assets.{asset_name}", asset_value))
            if not isinstance(review, dict):
                errors.append(f"{prefix}.review is required")
            else:
                if review.get("cleanup_status") not in RECONSTRUCTION_STATUSES:
                    errors.append(f"{prefix}.review.cleanup_status is invalid")
            reconstruction = component.get("layer_reconstruction")
            if schema_version == 3:
                if not isinstance(reconstruction, dict):
                    errors.append(f"{prefix}.layer_reconstruction is required")
                elif reconstruction.get("status") not in RECONSTRUCTION_STATUSES:
                    errors.append(f"{prefix}.layer_reconstruction.status is invalid")
            reusable = component.get("reusable_bitmap")
            if reusable is True:
                for gate_error in activation_gate_errors(component):
                    errors.append(f"{prefix}: {gate_error}")
        for file_field, file_value in file_values:
            file_path = (path.parent / file_value).resolve()
            try:
                file_path.relative_to(path.parent.resolve())
            except ValueError:
                errors.append(f"{prefix}.{file_field} must stay inside the package")
            if not file_path.is_file():
                errors.append(f"{prefix}.{file_field} does not exist: {file_value}")
        bounds = component.get("bounds")
        if not isinstance(bounds, dict):
            errors.append(f"{prefix}.bounds is required")
        else:
            values = [bounds.get(key) for key in ("x", "y", "width", "height")]
            if not all(isinstance(value, (int, float)) for value in values):
                errors.append(f"{prefix}.bounds must contain numeric x/y/width/height")
            elif bounds["width"] <= 0 or bounds["height"] <= 0:
                errors.append(f"{prefix}.bounds width/height must be positive")
            elif isinstance(width, (int, float)) and isinstance(height, (int, float)):
                if bounds["x"] < 0 or bounds["y"] < 0 or bounds["x"] + bounds["width"] > width or bounds["y"] + bounds["height"] > height:
                    errors.append(f"{prefix}.bounds must remain inside the page")

    for component_id, parent_id in parents.items():
        if parent_id != "root" and parent_id not in ids:
            errors.append(f"{component_id} references missing parent {parent_id}")
    for start in ids:
        seen: set[str] = set()
        current = start
        while current != "root" and current in parents:
            if current in seen:
                errors.append(f"parent cycle detected at {start}")
                break
            seen.add(current)
            current = parents[current]
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a canonical Cowart layer manifest.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    errors = validate_manifest(args.manifest.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
