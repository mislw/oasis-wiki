#!/usr/bin/env python3
"""Build a hierarchical layer-reconstruction plan from an approved UI tree."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from component_semantics import normalize_node_semantics
from validate_extraction_plan import VALID_MODES, validate_plan


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def mask_source_for(node, clean_layer):
    node_id = node["id"]
    bounds = node["bounds"]
    if isinstance(node.get("alpha_mask"), str):
        return {"node_id": node_id, "source_type": "alpha_mask", "path": node["alpha_mask"]}
    if clean_layer:
        return {"node_id": node_id, "source_type": "clean_layer_alpha", "path": clean_layer}
    if isinstance(node.get("segmentation_mask"), str):
        return {"node_id": node_id, "source_type": "semantic_mask", "path": node["segmentation_mask"]}
    extraction = node.get("extraction") if isinstance(node.get("extraction"), dict) else {}
    padding = int(extraction.get("mask_padding", node.get("mask_padding", 2)))
    return {
        "node_id": node_id,
        "source_type": "bounds_fallback",
        "bounds": bounds,
        "padding": max(1, padding),
        "fallback_only": True,
    }


def _postorder(root_ids, children):
    result = []

    def visit(node_id):
        for child_id in children.get(node_id, []):
            visit(child_id)
        result.append(node_id)

    for root_id in root_ids:
        visit(root_id)
    return result


def _descendants(node_id, children):
    result = []
    for child_id in children.get(node_id, []):
        result.append(child_id)
        result.extend(_descendants(child_id, children))
    return result


def _clean_layer_path(node, mode, target):
    if mode in {"native", "composite"}:
        return None
    visual_assets = node.get("visual_assets") if isinstance(node.get("visual_assets"), dict) else {}
    explicit = visual_assets.get("clean_layer")
    if isinstance(explicit, str):
        return explicit
    extraction = node.get("extraction") if isinstance(node.get("extraction"), dict) else {}
    output = extraction.get("output")
    return output if isinstance(output, str) else f"layers/{target}.png"


def extraction_component(node, has_children=False, descendants=None, children=None, node_by_id=None, target_by_node=None):
    extraction = node.get("extraction")
    if not isinstance(extraction, dict):
        return None
    mode = extraction.get("mode")
    target = extraction.get("target_component_id")
    if mode not in VALID_MODES or not isinstance(target, str):
        raise ValueError(f"node {node.get('id')} needs a valid extraction mode and target_component_id")
    if not isinstance(node.get("id"), str) or not isinstance(node.get("bounds"), dict):
        raise ValueError("each extracted UI-tree node needs id and bounds")

    descendants = descendants or []
    children = children or {}
    node_by_id = node_by_id or {node["id"]: node}
    target_by_node = target_by_node or {node["id"]: target}
    clean_layer = _clean_layer_path(node, mode, target)
    visual_assets = node.get("visual_assets") if isinstance(node.get("visual_assets"), dict) else {}
    source_crop = visual_assets.get("source_crop", "__source__")
    assembly_preview = visual_assets.get("assembly_preview")
    semantics_input = dict(node)
    semantics_input["visual_assets"] = {
        "source_crop": source_crop,
        "clean_layer": clean_layer,
        "assembly_preview": assembly_preview,
    }
    semantics = normalize_node_semantics(semantics_input, has_children)

    native_descendants = [node_id for node_id in descendants if node_by_id[node_id].get("extraction", {}).get("mode") == "native"]
    artwork_descendants = [node_id for node_id in descendants if node_by_id[node_id].get("extraction", {}).get("mode") == "extract_artwork"]
    mask_sources = []
    for descendant_id in descendants:
        descendant = node_by_id[descendant_id]
        descendant_mode = descendant.get("extraction", {}).get("mode")
        descendant_target = target_by_node.get(descendant_id, descendant_id)
        descendant_clean = _clean_layer_path(descendant, descendant_mode, descendant_target)
        mask_sources.append(mask_source_for(descendant, descendant_clean))

    direct_dependencies = []
    for child_id in children.get(node["id"], []):
        child_mode = node_by_id[child_id].get("extraction", {}).get("mode")
        if child_mode in {"extract_artwork", "reconstruct_skin"}:
            child_target = target_by_node[child_id]
            if child_target not in direct_dependencies:
                direct_dependencies.append(child_target)

    reconstruction_status = "not_applicable" if mode in {"native", "composite"} else "pending"
    layer_reconstruction = {
        "status": reconstruction_status,
        "remove_nodes": list(descendants),
        "direct_children": list(children.get(node["id"], [])),
        "visible_descendants": list(descendants),
        "native_descendants": native_descendants,
        "artwork_descendants": artwork_descendants,
        "mask": {
            "operation": "union",
            "deduplicate_pixels": True,
            "priority": ["alpha_mask", "clean_layer_alpha", "semantic_mask", "bounds_fallback"],
            "sources": mask_sources,
        },
        "depends_on": direct_dependencies,
        "transparent": mode in {"extract_artwork", "reconstruct_skin"},
        "method": "image_reconstruction" if mode in {"extract_artwork", "reconstruct_skin"} else None,
        "error": None,
    }
    semantics["layer_reconstruction"] = layer_reconstruction
    semantics["review"] = {"status": "candidate", "cleanup_status": reconstruction_status}
    semantics["reusable_bitmap"] = False
    semantics["visual_assets"] = semantics_input["visual_assets"]
    return {
        "target_component_id": target,
        "parent_id": node.get("parent_id", "root"),
        "category": node.get("category", "unknown"),
        "mode": mode,
        "status": extraction.get("status", "candidate"),
        "z_index": float(node.get("z_index", node.get("layer", 0))),
        "source_nodes": [node["id"]],
        "instances": [{"node_id": node["id"], "parent_id": node.get("parent_id", "root"), "bounds": node["bounds"]}],
        "remove_content": list(dict.fromkeys([*extraction.get("remove_content", []), *descendants])),
        "source_content_clean": extraction.get("source_content_clean", False),
        "transparent": mode in {"extract_artwork", "reconstruct_skin"},
        "evaluate_nine_slice": extraction.get("evaluate_nine_slice", False),
        "output": clean_layer,
        "confidence": extraction.get("confidence", 0.0),
        "reason": extraction.get("reason", ""),
        **semantics,
    }


def build_plan(ui_tree, visual_review, image_path):
    if ui_tree.get("artifact_type") != "ui_tree":
        raise ValueError("ui_tree artifact_type must be ui_tree")
    review_kind = visual_review.get("artifact_type") or visual_review.get("workflow_stage")
    if review_kind != "visual_review" or visual_review.get("status") != "approved":
        raise ValueError("visual_review must be an approved visual_review artifact")
    image_sha256 = hashlib.sha256(Path(image_path).read_bytes()).hexdigest()
    approved_image = visual_review.get("approved_image")
    approved_sha256 = approved_image.get("sha256") if isinstance(approved_image, dict) else None
    review_sha256 = visual_review.get("source_sha256", visual_review.get("sha256", approved_sha256))
    if review_sha256 != image_sha256:
        raise ValueError("approved visual-review SHA-256 does not match image")
    page_size = ui_tree.get("page_size", {"width": 1920, "height": 1080})

    nodes = [dict(node) for node in ui_tree.get("nodes", []) if isinstance(node, dict)]
    ids = {node.get("id") for node in nodes}
    if "background.root" not in ids:
        nodes.append({
            "id": "background.root",
            "parent_id": "root",
            "category": "background",
            "bounds": {"x": 0, "y": 0, "width": page_size["width"], "height": page_size["height"]},
            "z_index": -100000,
            "visual_assets": {"source_crop": "__source__", "clean_layer": None, "assembly_preview": None},
            "extraction": {"mode": "reconstruct_skin", "target_component_id": "background.root", "reason": "Clean root background."},
            "reconstruction_scope": "root",
        })

    node_by_id = {node["id"]: node for node in nodes}
    target_by_node = {node["id"]: node.get("extraction", {}).get("target_component_id", node["id"]) for node in nodes}
    children = {node_id: [] for node_id in node_by_id}
    root_ids = []
    for node in nodes:
        node_id = node["id"]
        parent_id = node.get("parent_id", "root")
        if parent_id == "root":
            root_ids.append(node_id)
        elif parent_id in children:
            children[parent_id].append(node_id)
        else:
            raise ValueError(f"node {node_id} references missing parent {parent_id}")

    original_roots = [node_id for node_id in root_ids if node_id != "background.root"]
    grouped = {}
    postorder = _postorder(original_roots, children)
    postorder.append("background.root")
    order = []
    for node_id in postorder:
        node = node_by_id[node_id]
        descendants = _descendants(node_id, children)
        if node_id == "background.root":
            descendants = []
            for root_id in original_roots:
                descendants.append(root_id)
                descendants.extend(_descendants(root_id, children))
            children["background.root"] = original_roots
        component = extraction_component(
            node,
            has_children=bool(descendants),
            descendants=descendants,
            children=children,
            node_by_id=node_by_id,
            target_by_node=target_by_node,
        )
        if component is None:
            continue
        target = component["target_component_id"]
        existing = grouped.get(target)
        if existing is None:
            grouped[target] = component
            order.append(target)
            continue
        for key in ("category", "mode", "status", "transparent", "evaluate_nine_slice", "output"):
            if existing[key] != component[key]:
                raise ValueError(f"equivalent target {target} has conflicting {key}")
        existing["source_nodes"].extend(component["source_nodes"])
        existing["instances"].extend(component["instances"])
        existing["remove_content"] = list(dict.fromkeys([*existing["remove_content"], *component["remove_content"]]))
        for key in ("remove_nodes", "direct_children", "visible_descendants", "native_descendants", "artwork_descendants", "depends_on"):
            existing["layer_reconstruction"][key] = list(dict.fromkeys([
                *existing["layer_reconstruction"][key],
                *component["layer_reconstruction"][key],
            ]))
        existing_sources = existing["layer_reconstruction"]["mask"]["sources"]
        known = {entry["node_id"] for entry in existing_sources}
        existing_sources.extend(entry for entry in component["layer_reconstruction"]["mask"]["sources"] if entry["node_id"] not in known)
        existing["confidence"] = min(existing["confidence"], component["confidence"])

    plan = {
        "schema_version": 3,
        "artifact_type": "layer_reconstruction_plan",
        "source": {"image": Path(image_path).name, "sha256": image_sha256, "page_size": page_size},
        "reconstruction_order": order,
        "components": [grouped[target] for target in order],
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
    print(f"Wrote layer reconstruction plan: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
