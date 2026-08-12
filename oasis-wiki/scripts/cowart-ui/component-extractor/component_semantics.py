from __future__ import annotations

from typing import Any


NODE_KINDS = {"composite", "skin", "artwork", "native"}
RENDER_MODES = {"bitmap", "outline", "ghost", "assembly", "hidden"}
CLEANUP_STATUSES = {"not_applicable", "needs_cleanup", "requested", "in_progress", "clean", "failed"}

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
    clean_asset = raw.get("clean_asset", item.get("clean_asset"))
    assembly_preview = raw.get("assembly_preview", item.get("assembly_preview"))

    legacy_file = file_value or (item.get("file") if isinstance(item.get("file"), str) else None)
    if legacy_file and not source_crop and not clean_asset:
        asset_policy = str(item.get("asset_policy") or "").lower()
        cleanup = _explicit_cleanup_status(item)
        if node_kind in {"composite", "native"} or asset_policy == "reconstruction_candidate" or cleanup == "needs_cleanup":
            source_crop = legacy_file
        else:
            clean_asset = legacy_file

    return {
        "source_crop": source_crop,
        "clean_asset": clean_asset,
        "assembly_preview": assembly_preview,
    }


def _explicit_cleanup_status(item: dict[str, Any]) -> str | None:
    review = item.get("review") if isinstance(item.get("review"), dict) else {}
    value = review.get("cleanup_status", item.get("cleanup_status"))
    return str(value) if value in CLEANUP_STATUSES else None


def cleanup_status_for(item: dict[str, Any], node_kind: str, visual_assets: dict[str, Any]) -> str:
    explicit = _explicit_cleanup_status(item)
    if node_kind in {"composite", "native"}:
        return "not_applicable"
    if visual_assets.get("clean_asset"):
        return "clean"
    if explicit in {"requested", "in_progress", "failed"}:
        return explicit
    return "needs_cleanup"


def review_for(item: dict[str, Any], node_kind: str, visual_assets: dict[str, Any]) -> dict[str, str]:
    raw = item.get("review") if isinstance(item.get("review"), dict) else {}
    status = str(raw.get("status") or item.get("status") or "pending_review")
    if status not in {"pending_review", "candidate"}:
        status = "candidate"
    cleanup_status = cleanup_status_for(item, node_kind, visual_assets)
    if cleanup_status in {"needs_cleanup", "requested", "in_progress", "failed"}:
        status = "candidate"
    return {"status": status, "cleanup_status": cleanup_status}


def reusable_bitmap_for(node_kind: str, visual_assets: dict[str, Any], review: dict[str, Any]) -> bool:
    return (
        node_kind in {"skin", "artwork"}
        and bool(visual_assets.get("clean_asset"))
        and review.get("cleanup_status") == "clean"
    )


def normalize_node_semantics(item: dict[str, Any], has_children: bool = False, file_value: str | None = None) -> dict[str, Any]:
    node_kind = node_kind_for(item, has_children)
    visual_assets = visual_assets_for(item, node_kind, file_value)
    review = review_for(item, node_kind, visual_assets)
    return {
        "node_kind": node_kind,
        "render_mode": render_mode_for(node_kind, item.get("render_mode") or item.get("renderMode")),
        "visual_assets": visual_assets,
        "review": review,
        "reusable_bitmap": reusable_bitmap_for(node_kind, visual_assets, review),
    }


def default_asset_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [node for node in nodes if node.get("node_kind") in {"skin", "artwork"}]


def structure_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [node for node in nodes if node.get("node_kind") in {"composite", "native"}]


def activation_gate_errors(component: dict[str, Any]) -> list[str]:
    component_id = str(component.get("component_id") or "component")
    node_kind = component.get("node_kind")
    assets = component.get("visual_assets") if isinstance(component.get("visual_assets"), dict) else {}
    review = component.get("review") if isinstance(component.get("review"), dict) else {}
    errors: list[str] = []
    if node_kind not in {"skin", "artwork"}:
        errors.append(f"{component_id} is {node_kind or 'unclassified'} and cannot become a reusable bitmap")
    if not assets.get("clean_asset"):
        errors.append(f"{component_id} has no clean_asset; source_crop and assembly_preview are not reusable assets")
    if review.get("cleanup_status") != "clean":
        errors.append(f"{component_id} cleanup_status must be clean")
    return errors
