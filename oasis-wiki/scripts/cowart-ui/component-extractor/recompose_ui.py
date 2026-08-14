#!/usr/bin/env python3
"""Assemble clean layers and native placeholders without using source crops."""

import argparse
import json
import sys
from pathlib import Path

from validate_extraction_plan import load_json, validate_plan


def _instance_records(plan):
    records = {}
    for component in plan["components"]:
        for instance in component["instances"]:
            record = dict(instance)
            record["component"] = component
            records[instance["node_id"]] = record
    return records


def _resolved_bounds(records, placements):
    resolved = {}

    def resolve(node_id):
        if node_id in resolved:
            return resolved[node_id]
        record = records[node_id]
        original = record["bounds"]
        parent_id = record.get("parent_id", "root")
        parent_delta = (0, 0)
        if parent_id in records:
            parent_bounds = resolve(parent_id)
            parent_original = records[parent_id]["bounds"]
            parent_delta = (parent_bounds["x"] - parent_original["x"], parent_bounds["y"] - parent_original["y"])
        placement = placements.get(node_id) or placements.get(record["component"]["target_component_id"])
        if placement:
            x = placement.get("x", original["x"] + parent_delta[0])
            y = placement.get("y", original["y"] + parent_delta[1])
        else:
            x = original["x"] + parent_delta[0]
            y = original["y"] + parent_delta[1]
        resolved[node_id] = {"x": x, "y": y, "width": original["width"], "height": original["height"]}
        return resolved[node_id]

    for node_id in records:
        resolve(node_id)
    return resolved


def compose_preview(plan, assets_dir, placements=None, native_placeholders=True):
    from PIL import Image, ImageDraw

    validate_plan(plan)
    page_size = plan["source"]["page_size"]
    canvas = Image.new("RGBA", (page_size["width"], page_size["height"]), (0, 0, 0, 0))
    records = _instance_records(plan)
    resolved = _resolved_bounds(records, placements or {})
    ordered = sorted(records.items(), key=lambda item: (item[1]["component"].get("z_index", 0), item[0]))
    native_draw = ImageDraw.Draw(canvas, "RGBA")
    for node_id, record in ordered:
        component = record["component"]
        bounds = resolved[node_id]
        if component["mode"] == "native":
            if native_placeholders:
                native_draw.rectangle(
                    (bounds["x"], bounds["y"], bounds["x"] + bounds["width"] - 1, bounds["y"] + bounds["height"] - 1),
                    outline=(80, 180, 255, 180),
                    width=1,
                )
            continue
        if component["mode"] == "composite":
            continue
        clean_layer = component.get("visual_assets", {}).get("clean_layer")
        if not clean_layer:
            raise ValueError(f"{component['target_component_id']} has no clean_layer; source_crop fallback is forbidden")
        asset_path = Path(assets_dir) / clean_layer
        if not asset_path.is_file():
            raise ValueError(f"missing reconstructed clean layer: {asset_path}")
        asset = Image.open(asset_path).convert("RGBA")
        rendered = asset.resize((int(bounds["width"]), int(bounds["height"])), Image.Resampling.LANCZOS)
        canvas.alpha_composite(rendered, (int(bounds["x"]), int(bounds["y"])))
    return canvas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--assets-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--placements", type=Path, help="Optional JSON mapping node IDs to moved x/y positions.")
    parser.add_argument("--background", type=Path, help="Legacy plans only; schema 3 must use background.root.clean_layer.")
    args = parser.parse_args()
    try:
        from PIL import Image
    except ImportError:
        print("recompose_ui.py requires Pillow: install with python -m pip install Pillow", file=sys.stderr)
        return 1
    try:
        plan = validate_plan(load_json(args.plan))
        if plan.get("schema_version") == 3:
            if args.background:
                raise ValueError("schema 3 assembly cannot use --background; use background.root clean_layer")
            placements = load_json(args.placements) if args.placements else {}
            canvas = compose_preview(plan, args.assets_dir, placements)
            sources = []
            for component in plan["components"]:
                if component["mode"] != "composite":
                    source_type = "native_placeholder" if component["mode"] == "native" else "clean_layer"
                    sources.append({"target_component_id": component["target_component_id"], "source_type": source_type})
        else:
            page_size = plan["source"]["page_size"]
            if args.background:
                canvas = Image.open(args.background).convert("RGBA")
                if canvas.size != (page_size["width"], page_size["height"]):
                    raise ValueError("background dimensions must match source.page_size")
            else:
                canvas = Image.new("RGBA", (page_size["width"], page_size["height"]), (0, 0, 0, 0))
            for component in plan["components"]:
                if component["output"] is None:
                    continue
                asset_path = args.assets_dir / component["output"]
                if not asset_path.is_file():
                    raise ValueError(f"missing reconstructed asset: {asset_path}")
                asset = Image.open(asset_path).convert("RGBA")
                for instance in component["instances"]:
                    bounds = instance["bounds"]
                    rendered = asset.resize((bounds["width"], bounds["height"]), Image.Resampling.LANCZOS)
                    canvas.alpha_composite(rendered, (bounds["x"], bounds["y"]))
            sources = [{"target_component_id": component["target_component_id"], "source_type": "legacy_output"} for component in plan["components"]]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(args.output, "PNG")
        sidecar = args.output.with_suffix(args.output.suffix + ".json")
        sidecar.write_text(json.dumps({
            "artifact_type": "assembly_preview",
            "preview": str(args.output),
            "sources": sources,
            "source_crop_used": False,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Wrote assembly preview: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
