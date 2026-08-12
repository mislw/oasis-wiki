#!/usr/bin/env python3
"""Build a reusable-component extraction plan from an approved UI tree."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from validate_extraction_plan import VALID_MODES, validate_plan


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def extraction_component(node):
    extraction = node.get("extraction")
    if not isinstance(extraction, dict):
        return None
    mode = extraction.get("mode")
    target = extraction.get("target_component_id")
    if mode not in VALID_MODES or not isinstance(target, str):
        raise ValueError(f"node {node.get('id')} needs a valid extraction mode and target_component_id")
    if not isinstance(node.get("id"), str) or not isinstance(node.get("bounds"), dict):
        raise ValueError("each extracted UI-tree node needs id and bounds")
    output = extraction.get("output")
    if output is None and mode in {"extract_artwork", "reconstruct_skin"}:
        output = f"layers/{target}.png"
    if mode in {"native", "composite"}:
        output = None
    return {
        "target_component_id": target,
        "category": node.get("category", "unknown"),
        "mode": mode,
        "status": extraction.get("status", "candidate"),
        "source_nodes": [node["id"]],
        "instances": [{"node_id": node["id"], "bounds": node["bounds"]}],
        "remove_content": extraction.get("remove_content", []),
        "source_content_clean": extraction.get("source_content_clean", mode == "native"),
        "transparent": extraction.get("transparent", mode in {"extract_artwork", "reconstruct_skin"}),
        "evaluate_nine_slice": extraction.get("evaluate_nine_slice", False),
        "output": output,
        "confidence": extraction.get("confidence", 0.0),
        "reason": extraction.get("reason", ""),
    }


def build_plan(ui_tree, visual_review, image_path):
    if ui_tree.get("artifact_type") != "ui_tree":
        raise ValueError("ui_tree artifact_type must be ui_tree")
    if visual_review.get("artifact_type") != "visual_review" or visual_review.get("status") != "approved":
        raise ValueError("visual_review must be an approved visual_review artifact")
    image_sha256 = hashlib.sha256(Path(image_path).read_bytes()).hexdigest()
    review_sha256 = visual_review.get("source_sha256", visual_review.get("sha256"))
    if review_sha256 != image_sha256:
        raise ValueError("approved visual-review SHA-256 does not match image")
    page_size = ui_tree.get("page_size", {"width": 1920, "height": 1080})

    grouped = {}
    for node in ui_tree.get("nodes", []):
        component = extraction_component(node)
        if component is None:
            continue
        target = component["target_component_id"]
        existing = grouped.get(target)
        if existing is None:
            grouped[target] = component
            continue
        for key in ("category", "mode", "status", "remove_content", "source_content_clean", "transparent", "evaluate_nine_slice", "output"):
            if existing[key] != component[key]:
                raise ValueError(f"equivalent target {target} has conflicting {key}")
        existing["source_nodes"].extend(component["source_nodes"])
        existing["instances"].extend(component["instances"])
        existing["confidence"] = min(existing["confidence"], component["confidence"])
        if component["reason"] and component["reason"] not in existing["reason"]:
            existing["reason"] = "; ".join(filter(None, [existing["reason"], component["reason"]]))

    plan = {
        "schema_version": 1,
        "artifact_type": "extraction_plan",
        "source": {"image": Path(image_path).name, "sha256": image_sha256, "page_size": page_size},
        "components": [grouped[target] for target in sorted(grouped)],
    }
    return validate_plan(plan)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ui-tree", required=True, type=Path)
    parser.add_argument("--visual-review", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        plan = build_plan(load_json(args.ui_tree), load_json(args.visual_review), args.image)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Wrote extraction plan: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
