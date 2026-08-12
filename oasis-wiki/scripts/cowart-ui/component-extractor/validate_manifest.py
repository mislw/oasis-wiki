from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)+$")


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"invalid JSON: {exc}"]
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
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
        file_value = component.get("file")
        if not isinstance(file_value, str):
            errors.append(f"{prefix}.file is required")
        else:
            file_path = (path.parent / file_value).resolve()
            try:
                file_path.relative_to(path.parent.resolve())
            except ValueError:
                errors.append(f"{prefix}.file must stay inside the package")
            if not file_path.is_file():
                errors.append(f"{prefix}.file does not exist: {file_value}")
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
