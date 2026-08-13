from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_manifest import validate_manifest
from component_semantics import render_layer_gate_errors


def build_move_group(component_id: str, children: dict[str, list[str]]) -> dict[str, Any]:
    return {
        "component_id": component_id,
        "children": [build_move_group(child, children) for child in children.get(component_id, [])],
    }


def build_plan(manifest_path: Path) -> dict[str, Any]:
    errors = validate_manifest(manifest_path)
    if errors:
        raise ValueError("; ".join(errors))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    components = sorted(manifest["components"], key=lambda item: (item["z_index"], item["layer"], item["component_id"]))
    children: dict[str, list[str]] = {"root": []}
    for item in components:
        children.setdefault(item["parent_id"], []).append(item["component_id"])
        children.setdefault(item["component_id"], [])
    shapes = []
    for item in components:
        if manifest.get("schema_version") in {2, 3} and render_layer_gate_errors(item):
            continue
        bounds = item["bounds"]
        padding = max(0, float(item.get("padding", 0) or 0))
        asset_value = item.get("visual_assets", {}).get("clean_layer") if manifest.get("schema_version") in {2, 3} else item["file"]
        shapes.append({
            "component_id": item["component_id"],
            "asset_path": str((manifest_path.parent / asset_value).resolve()),
            "logical_parent_id": item["parent_id"],
            "x": bounds["x"] - padding, "y": bounds["y"] - padding,
            "width": bounds["width"] + padding * 2, "height": bounds["height"] + padding * 2,
            "rotation": item.get("rotation", 0),
            "opacity": item.get("opacity", 1),
            "layer": item["layer"], "z_index": item["z_index"],
            "shape_meta": {
                "cowartLayerImport": True,
                "componentId": item["component_id"],
                "logicalParentId": item["parent_id"],
                "layer": item["layer"],
                "zIndex": item["z_index"],
                "sourceBounds": bounds,
                "padding": padding,
                "reviewStatus": item["status"],
                "nodeKind": item.get("node_kind"),
                "assetSource": "clean_layer" if manifest.get("schema_version") in {2, 3} else "file",
            },
        })
    return {
        "schema_version": 1,
        "source_manifest": str(manifest_path),
        "page_size": manifest["source"]["page_size"],
        "shapes": shapes,
        "move_groups": [build_move_group(item, children) for item in children["root"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Cowart layer import plan from a validated manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        plan = build_plan(args.manifest.resolve())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
