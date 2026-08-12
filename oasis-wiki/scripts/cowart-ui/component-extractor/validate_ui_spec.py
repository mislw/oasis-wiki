from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)+$")
COMPONENT_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_]*){2,}$")
STATUSES = {"pending_review", "candidate"}
NATIVE_CATEGORIES = {"text", "button", "input", "progress", "counter"}
REFERENCE_ROLES = {"style", "layout"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("UI spec root must be an object.")
    return value


def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if spec.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    page = spec.get("page")
    if not isinstance(page, dict):
        return errors + ["page is required"]
    if not isinstance(page.get("page_id"), str) or not ID_PATTERN.fullmatch(page["page_id"]):
        errors.append("page.page_id must be a lowercase dot-separated ID")
    if not isinstance(page.get("name"), str) or not page["name"].strip():
        errors.append("page.name is required")
    canvas = page.get("canvas")
    if not isinstance(canvas, dict):
        errors.append("page.canvas is required")
        width = height = None
    else:
        width, height = canvas.get("width"), canvas.get("height")
        if not isinstance(width, (int, float)) or width <= 0:
            errors.append("page.canvas.width must be positive")
        if not isinstance(height, (int, float)) or height <= 0:
            errors.append("page.canvas.height must be positive")
    operations = page.get("operations", [])
    if not isinstance(operations, list):
        errors.append("page.operations must be an array")
        operations = []
    operation_ids = set()
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            errors.append(f"page.operations[{index}] must be an object")
            continue
        operation_id = operation.get("operation_id")
        if not isinstance(operation_id, str) or not ID_PATTERN.fullmatch(operation_id):
            errors.append(f"page.operations[{index}].operation_id is invalid")
        elif operation_id in operation_ids:
            errors.append(f"duplicate operation_id: {operation_id}")
        else:
            operation_ids.add(operation_id)
        for key in ("trigger", "action", "owner"):
            if not isinstance(operation.get(key), str) or not operation[key].strip():
                errors.append(f"page.operations[{index}].{key} is required")
    data_contract = spec.get("data_contract", [])
    if not isinstance(data_contract, list):
        errors.append("data_contract must be an array")
    visual = spec.get("visual", {})
    if not isinstance(visual, dict):
        errors.append("visual must be an object")
    else:
        references = visual.get("reference_images", [])
        if not isinstance(references, list):
            errors.append("visual.reference_images must be an array")
        else:
            for index, reference in enumerate(references):
                prefix = f"visual.reference_images[{index}]"
                if not isinstance(reference, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                if not isinstance(reference.get("source"), str) or not reference["source"].strip():
                    errors.append(f"{prefix}.source is required")
                role = reference.get("role")
                if role not in REFERENCE_ROLES:
                    errors.append(f"{prefix}.role must be style or layout")
                priority = reference.get("priority")
                if isinstance(priority, bool) or not isinstance(priority, (int, float)):
                    errors.append(f"{prefix}.priority must be numeric")
                copy_visual_style = reference.get("copy_visual_style")
                if copy_visual_style is not None and not isinstance(copy_visual_style, bool):
                    errors.append(f"{prefix}.copy_visual_style must be boolean")
                if role == "layout" and copy_visual_style is True:
                    errors.append(f"{prefix}.copy_visual_style must be false for layout references")
    nodes = spec.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return errors + ["nodes must be a non-empty array"]
    ids: set[str] = set()
    parents: dict[str, str] = {}
    for index, node in enumerate(nodes):
        prefix = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{prefix} must be an object")
            continue
        component_id = node.get("component_id")
        if not isinstance(component_id, str) or not COMPONENT_PATTERN.fullmatch(component_id):
            errors.append(f"{prefix}.component_id must have at least three dot-separated segments")
            continue
        if component_id in ids:
            errors.append(f"duplicate component_id: {component_id}")
        ids.add(component_id)
        parent_id = node.get("parent_id")
        if not isinstance(parent_id, str):
            errors.append(f"{prefix}.parent_id is required")
        else:
            parents[component_id] = parent_id
        if not isinstance(node.get("category"), str) or not node["category"].strip():
            errors.append(f"{prefix}.category is required")
        if node.get("status") not in STATUSES:
            errors.append(f"{prefix}.status must be pending_review or candidate")
        for key in ("layer", "z_index"):
            if not isinstance(node.get(key), (int, float)):
                errors.append(f"{prefix}.{key} must be numeric")
        bounds = node.get("bounds")
        if not isinstance(bounds, dict):
            errors.append(f"{prefix}.bounds is required")
        else:
            values = [bounds.get(key) for key in ("x", "y", "width", "height")]
            if not all(isinstance(value, (int, float)) for value in values):
                errors.append(f"{prefix}.bounds requires numeric x/y/width/height")
            elif bounds["width"] <= 0 or bounds["height"] <= 0:
                errors.append(f"{prefix}.bounds width/height must be positive")
            elif isinstance(width, (int, float)) and isinstance(height, (int, float)) and (
                bounds["x"] < 0 or bounds["y"] < 0 or bounds["x"] + bounds["width"] > width or bounds["y"] + bounds["height"] > height
            ):
                errors.append(f"{prefix}.bounds must remain inside page.canvas")
        policy = node.get("asset_policy")
        if policy not in {"layer", "native", "reconstruction_candidate"}:
            errors.append(f"{prefix}.asset_policy must be layer, native, or reconstruction_candidate")
        elif node.get("category") in NATIVE_CATEGORIES and policy != "native":
            errors.append(f"{prefix} must use native asset_policy")
        operation_id = node.get("operation_id")
        if operation_id is not None and operation_id not in operation_ids:
            errors.append(f"{prefix}.operation_id references missing operation {operation_id}")
    for component_id, parent_id in parents.items():
        if parent_id != "root" and parent_id not in ids:
            errors.append(f"{component_id} references missing parent {parent_id}")
    for start in ids:
        current, seen = start, set()
        while current != "root" and current in parents:
            if current in seen:
                errors.append(f"parent cycle detected at {start}")
                break
            seen.add(current)
            current = parents[current]
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a UI generation specification.")
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_spec(load_json(args.spec.resolve()))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
