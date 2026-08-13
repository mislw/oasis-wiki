from __future__ import annotations

from typing import Any


NODE_KINDS = {"composite", "skin", "artwork", "native"}
RENDER_MODES = {"bitmap", "outline", "ghost", "assembly", "hidden"}
RECONSTRUCTION_STATUSES = {
    "not_applicable",
    "pending",
    "requested",
    "job_created",
    "waiting_executor",
    "reconstructing",
    "reconstructed",
    "validation",
    "ready",
    "failed",
}
CLEANUP_STATUSES = RECONSTRUCTION_STATUSES

NATIVE_CATEGORIES = {"text", "label", "value", "price", "counter", "progress", "timer", "input", "hit_target"}
ARTWORK_CATEGORIES = {"artwork", "icon", "portrait", "hero", "equipment", "gem", "illustration", "decoration"}
STRUCTURE_CATEGORIES = {"grid", "row", "tabs", "group", "container", "layout", "composite"}
SKIN_CATEGORIES = {"background", "panel", "card", "button", "badge", "header", "tab", "slot", "skin", "frame", "scrollbar"}

MODE_TO_KIND = {
    "native": "native",
    "extract_artwork": "artwork",
    "reconstruct_skin": "skin",
    "composite": "composite",
}

DEFAULT_RENDER_MODE = {
    "composite": "outline",
    "skin": "bitmap",
    "artwork": "bitmap",
    "native": "outline",
}


def node_kind_for(item: dict[str, Any], has_children: bool = False) -> str:
    explicit = item.get("node_kind") or item.get("nodeKind")
    if explicit in NODE_KINDS:
        return str(explicit)

    extraction = item.get("extraction") if isinstance(item.get("extraction"), dict) else {}
    mode = extraction.get("mode")
    if mode in MODE_TO_KIND:
        inferred = MODE_TO_KIND[mode]
        if has_children and inferred == "skin":
            return "composite"
        return inferred

    asset_policy = str(item.get("asset_policy") or "").lower()
    if asset_policy == "native":
        return "native"
    if asset_policy == "composite":
        return "composite"

    category = str(item.get("category") or item.get("type") or "unknown").lower()
    if category in NATIVE_CATEGORIES:
        return "native"
    if category in ARTWORK_CATEGORIES:
        return "artwork"
    if has_children or category in STRUCTURE_CATEGORIES:
        return "composite"
    if category in SKIN_CATEGORIES:
        return "skin"
    return "artwork"


def render_mode_for(node_kind: str, explicit: Any = None) -> str:
    return str(explicit) if explicit in RENDER_MODES else DEFAULT_RENDER_MODE[node_kind]


def visual_assets_for(item: dict[str, Any], node_kind: str, file_value: str | None = None) -> dict[str, Any]:
    raw = item.get("visual_assets") if isinstance(item.get("visual_assets"), dict) else {}
    source_crop = raw.get("source_crop", item.get("source_crop"))
    clean_layer = raw.get("clean_layer", item.get("clean_layer"))
    assembly_preview = raw.get("assembly_preview", item.get("assembly_preview"))

    legacy_file = file_value or (item.get("file") if isinstance(item.get("file"), str) else None)
    if legacy_file and not source_crop and not clean_layer:
        asset_policy = str(item.get("asset_policy") or "").lower()
        status = _explicit_reconstruction_status(item)
        if node_kind in {"composite", "native"} or asset_policy == "reconstruction_candidate" or status in RECONSTRUCTION_STATUSES - {"ready", "not_applicable"}:
            source_crop = legacy_file
        else:
            clean_layer = legacy_file

    return {
        "source_crop": source_crop,
        "clean_layer": clean_layer,
        "assembly_preview": assembly_preview,
    }


def _explicit_reconstruction_status(item: dict[str, Any]) -> str | None:
    reconstruction = item.get("layer_reconstruction") if isinstance(item.get("layer_reconstruction"), dict) else {}
    review = item.get("review") if isinstance(item.get("review"), dict) else {}
    value = reconstruction.get("status", review.get("cleanup_status", item.get("cleanup_status")))
    return str(value) if value in RECONSTRUCTION_STATUSES else None


def reconstruction_status_for(item: dict[str, Any], node_kind: str, visual_assets: dict[str, Any]) -> str:
    explicit = _explicit_reconstruction_status(item)
    extraction = item.get("extraction") if isinstance(item.get("extraction"), dict) else {}
    if node_kind == "native" or extraction.get("mode") == "composite":
        return "not_applicable"
    if visual_assets.get("clean_layer") and explicit not in {"failed"}:
        return explicit if explicit in {"reconstructed", "validation", "ready"} else "ready"
    if explicit in RECONSTRUCTION_STATUSES - {"not_applicable", "ready"}:
        return explicit
    return "pending"


def layer_reconstruction_for(item: dict[str, Any], node_kind: str, visual_assets: dict[str, Any]) -> dict[str, Any]:
    raw = item.get("layer_reconstruction") if isinstance(item.get("layer_reconstruction"), dict) else {}
    result = dict(raw)
    result["status"] = reconstruction_status_for(item, node_kind, visual_assets)
    if node_kind != "native":
        result.setdefault("method", "image_reconstruction")
        result.setdefault("transparent", True)
        result.setdefault("error", None)
    return result


def review_for(item: dict[str, Any], reconstruction: dict[str, Any]) -> dict[str, str]:
    raw = item.get("review") if isinstance(item.get("review"), dict) else {}
    status = str(raw.get("status") or item.get("status") or "pending_review")
    if status not in {"pending_review", "candidate"}:
        status = "candidate"
    reconstruction_status = reconstruction["status"]
    if reconstruction_status not in {"ready", "not_applicable"}:
        status = "candidate"
    return {"status": status, "cleanup_status": reconstruction_status}


def reusable_bitmap_for(node_kind: str, visual_assets: dict[str, Any], reconstruction: dict[str, Any]) -> bool:
    return (
        node_kind in {"skin", "artwork"}
        and bool(visual_assets.get("clean_layer"))
        and reconstruction.get("status") == "ready"
    )


def normalize_node_semantics(item: dict[str, Any], has_children: bool = False, file_value: str | None = None) -> dict[str, Any]:
    node_kind = node_kind_for(item, has_children)
    visual_assets = visual_assets_for(item, node_kind, file_value)
    reconstruction = layer_reconstruction_for(item, node_kind, visual_assets)
    review = review_for(item, reconstruction)
    return {
        "node_kind": node_kind,
        "render_mode": render_mode_for(node_kind, item.get("render_mode") or item.get("renderMode")),
        "visual_assets": visual_assets,
        "layer_reconstruction": reconstruction,
        "review": review,
        "reusable_bitmap": reusable_bitmap_for(node_kind, visual_assets, reconstruction),
    }


def default_asset_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [node for node in nodes if node.get("node_kind") in {"skin", "artwork", "composite"}]


def structure_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [node for node in nodes if node.get("node_kind") in {"composite", "native"}]


def render_layer_gate_errors(component: dict[str, Any]) -> list[str]:
    component_id = str(component.get("component_id") or component.get("target_component_id") or "component")
    node_kind = component.get("node_kind")
    assets = component.get("visual_assets") if isinstance(component.get("visual_assets"), dict) else {}
    reconstruction = component.get("layer_reconstruction") if isinstance(component.get("layer_reconstruction"), dict) else {}
    errors: list[str] = []
    if node_kind == "native":
        errors.append(f"{component_id} is native and has no bitmap layer")
    if not assets.get("clean_layer"):
        errors.append(f"{component_id} has no clean_layer; source_crop and assembly_preview cannot render as clean layers")
    if reconstruction.get("status") != "ready":
        errors.append(f"{component_id} layer_reconstruction.status must be ready")
    return errors


def activation_gate_errors(component: dict[str, Any]) -> list[str]:
    errors = render_layer_gate_errors(component)
    component_id = str(component.get("component_id") or component.get("target_component_id") or "component")
    if component.get("node_kind") not in {"skin", "artwork"}:
        errors.insert(0, f"{component_id} is {component.get('node_kind') or 'unclassified'} and cannot become a reusable bitmap")
    return errors
