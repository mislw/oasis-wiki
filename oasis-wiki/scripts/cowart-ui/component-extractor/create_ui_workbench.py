from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

from companion_handoff import dispatch_companion_handoff
from component_semantics import normalize_node_semantics


WIKI_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_ROOT = Path(__file__).resolve().parent
TEMPLATE = WIKI_ROOT / "assets" / "cowart-ui" / "workbench-template" / "index.html"
SERVER_SCRIPT = SCRIPT_ROOT / "serve_workbench.py"
DEFAULT_COMPANION_EXECUTABLE = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Oasis Companion" / "oasis-companion.exe"
HIDDEN_BRIDGE_HTML = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>Oasis UI 工作台后台会话</title>
<style>html,body{display:none!important}</style></head><body aria-hidden="true"></body></html>
"""

CLOSE_BUTTON_TEXT_STYLE = {
    "font_size": 30,
    "color": "#fff3cf",
    "outline_color": "#6b3515",
    "outline_size": 2,
    "horizontal_alignment": "center",
    "vertical_alignment": "middle",
}


def slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or "ui-workbench"


def is_native_close_button(item: dict[str, Any], component_id: str, node_kind: str) -> bool:
    category = str(item.get("category") or item.get("type") or "").lower()
    if node_kind != "native" or category not in {"button", "hit_target"}:
        return False
    extraction = item.get("extraction") if isinstance(item.get("extraction"), dict) else {}
    identifiers = (component_id, extraction.get("target_component_id"))
    return any(
        isinstance(value, str) and "close" in re.split(r"[^a-z0-9]+", value.lower())
        for value in identifiers
    )


def load_library_preview_records(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    references = data.get("references") if isinstance(data, dict) else None
    if not isinstance(references, list):
        raise ValueError("Library references JSON has no references array.")
    records: list[dict[str, Any]] = []
    for reference in references:
        if not isinstance(reference, dict):
            continue
        library = reference.get("library") if isinstance(reference.get("library"), dict) else {}
        status = library.get("status", reference.get("status"))
        if status not in (None, "active", "resolved", "approved"):
            continue
        source = reference.get("source")
        if not isinstance(source, str) or not Path(source).is_file():
            continue
        records.append({"source": Path(source).resolve(), "library": library})
    return records


def resolve_library_preview(item: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any] | None:
    texture_asset = item.get("texture_asset") or item.get("currency_texture_asset")
    reuse_of = item.get("reuse_of")
    semantic_key = item.get("semantic_key")
    for record in records:
        library = record["library"]
        if isinstance(texture_asset, str) and library.get("source_asset") == texture_asset:
            return record
        if isinstance(reuse_of, str) and reuse_of in library.get("component_ids", []):
            return record
        if isinstance(semantic_key, str) and semantic_key in library.get("semantic_keys", []):
            return record
    return None


def library_component_reuse(item: dict[str, Any], record: dict[str, Any] | None) -> dict[str, Any] | None:
    if record is None:
        return None
    reuse_of = item.get("reuse_of")
    library = record["library"]
    component_ids = library.get("component_ids", [])
    if not isinstance(reuse_of, str) or reuse_of not in component_ids:
        return None
    source_asset = library.get("source_asset")
    if not isinstance(source_asset, str) or not source_asset.startswith("/"):
        return None
    return {
        "component_id": reuse_of,
        "source_asset": source_asset,
        "asset_id": library.get("asset_id"),
        "state": str(item.get("state") or "default"),
        "status": "ready",
    }


def resolve_page_id(explicit: str | None, title: str) -> str:
    value = explicit.strip() if explicit else ""
    if value:
        resolved = slug(value)
        if resolved == "ui-workbench" and value.lower() != "ui-workbench":
            raise ValueError("--page-id must contain at least one ASCII letter or digit")
        return resolved
    resolved = slug(title)
    if resolved != "ui-workbench" or title.lower() == "ui-workbench":
        return resolved
    digest = hashlib.sha256(title.strip().encode("utf-8")).hexdigest()[:12]
    return f"ui-{digest}"


def capture_agent_context(
    environ: dict[str, str],
    _which: Any,
    workspace: Path,
) -> dict[str, str] | None:
    thread_id = environ.get("CODEX_THREAD_ID", "").strip()
    if not thread_id:
        return None
    session_id = environ.get("CODEX_SESSION_ID", "").strip() or thread_id
    return {
        "provider": "codex",
        "thread_id": thread_id,
        "session_id": session_id,
        "workspace": str(workspace.resolve()),
    }


def create_thumbnail(image_path: Path, target: Path) -> None:
    with Image.open(image_path) as source:
        contained = ImageOps.contain(source.convert("RGB"), (320, 180), Image.Resampling.LANCZOS)
        thumbnail = Image.new("RGB", (320, 180), (24, 27, 30))
        offset = ((320 - contained.width) // 2, (180 - contained.height) // 2)
        thumbnail.paste(contained, offset)
        thumbnail.save(target, "WEBP", quality=82, method=6)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_visual_review(review_path: Path, image_path: Path) -> dict[str, Any]:
    review = json.loads(review_path.read_text(encoding="utf-8-sig"))
    if review.get("schema_version") != 1 or review.get("workflow_stage") != "visual_review":
        raise ValueError("Visual review is not a supported visual-review.json package.")
    if review.get("status") != "approved":
        raise ValueError("Visual review is not approved. Run approve_visual_review.py after Cowart visual confirmation.")
    approved = review.get("approved_image")
    if not isinstance(approved, dict) or approved.get("sha256") != sha256_file(image_path):
        raise ValueError("The supplied image does not match the approved visual review. Approve this exact final image first.")
    return review


def load_reconstruction_capability(execution_report_path: Path | None) -> dict[str, Any]:
    unavailable = {
        "available": False,
        "required_capability": "image_edit_inpainting",
        "executor": None,
        "error": "LAYER_RECONSTRUCTION_UNAVAILABLE",
        "execution_report": None,
    }
    if execution_report_path is None:
        return unavailable
    report_path = execution_report_path.resolve()
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    valid = (
        report.get("artifact_type") == "layer_reconstruction_execution"
        and report.get("status") == "completed"
        and report.get("capability") == "image_edit_inpainting"
        and isinstance(report.get("executor_id"), str)
        and bool(report["executor_id"])
    )
    if not valid:
        unavailable["error"] = "LAYER_RECONSTRUCTION_UNAVAILABLE: invalid execution report"
        unavailable["execution_report"] = str(report_path)
        return unavailable
    return {
        "available": True,
        "required_capability": "image_edit_inpainting",
        "executor": report["executor_id"],
        "error": None,
        "execution_report": str(report_path),
    }


def first(mapping: dict[str, Any], keys: tuple[str, ...], default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return default


def bounds_from(item: dict[str, Any]) -> dict[str, float] | None:
    value = first(item, ("bounds", "layout_rect", "layoutRect", "source_rect", "sourceRect", "rect"), item)
    if not isinstance(value, dict):
        return None
    try:
        bounds = {
            "x": float(first(value, ("x", "left"), 0)),
            "y": float(first(value, ("y", "top"), 0)),
            "width": float(first(value, ("width", "w"))),
            "height": float(first(value, ("height", "h"))),
        }
    except (TypeError, ValueError):
        return None
    return bounds if bounds["width"] > 0 and bounds["height"] > 0 else None


def component_id_for(item: dict[str, Any], index: int) -> str:
    value = first(item, ("component_id", "componentId", "control_id", "controlId", "id", "name"))
    text = re.sub(r"[^a-z0-9_]+", ".", str(value or "").lower()).strip(".")
    if not text or "." not in text:
        text = f"layer.{text or f'item{index:03d}'}"
    return text


def raw_controls(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    for key in ("controls", "components", "elements", "layers", "items", "nodes"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def reconstruction_bindings(
    plan_path: Path | None,
    execution_report_path: Path | None,
    controls_directory: Path,
) -> dict[str, dict[str, Any]]:
    if plan_path is None or execution_report_path is None or not plan_path.is_file() or not execution_report_path.is_file():
        return {}
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    execution = json.loads(execution_report_path.read_text(encoding="utf-8-sig"))
    if execution.get("status") != "completed":
        return {}
    completed = {
        item.get("target_component_id")
        for item in execution.get("results", [])
        if item.get("status") == "reconstructed"
    }
    bindings: dict[str, dict[str, Any]] = {}
    for component in plan.get("components", []):
        target_id = component.get("target_component_id")
        clean_layer = component.get("visual_assets", {}).get("clean_layer")
        if target_id not in completed or not isinstance(clean_layer, str):
            continue
        source_asset = (plan_path.parent / clean_layer).resolve()
        if not source_asset.is_file():
            continue
        relative_asset = Path(os.path.relpath(source_asset, controls_directory)).as_posix()
        mode = component.get("mode")
        node_kind = "skin" if mode == "reconstruct_skin" else "artwork" if mode == "extract_artwork" else component.get("node_kind")
        payload = {
            "target_component_id": target_id,
            "category": component.get("category", "unknown"),
            "node_kind": node_kind,
            "render_mode": component.get("render_mode", "bitmap"),
            "visual_assets": {"source_crop": "__source__", "clean_layer": relative_asset, "assembly_preview": None},
            "layer_reconstruction": {**component.get("layer_reconstruction", {}), "status": "ready", "error": None},
            "review": {"status": "pending_review", "cleanup_status": "ready"},
            "reusable_bitmap": node_kind in {"skin", "artwork"},
            "bounds": component.get("instances", [{}])[0].get("bounds"),
            "parent_id": component.get("parent_id", "root"),
            "z_index": component.get("z_index", 0),
        }
        node_ids = set(component.get("source_nodes", []))
        node_ids.update(item.get("node_id") for item in component.get("instances", []) if isinstance(item.get("node_id"), str))
        for node_id in node_ids:
            if isinstance(node_id, str):
                bindings[node_id] = payload
    return bindings


def hydrate_reconstructed_controls(items: list[dict[str, Any]], bindings: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    hydrated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source in items:
        item = dict(source)
        node_id = str(first(item, ("element_id", "elementId", "id", "uuid", "component_id", "componentId"), ""))
        seen.add(node_id)
        binding = bindings.get(node_id)
        if binding:
            item["visual_assets"] = dict(binding["visual_assets"])
            item["layer_reconstruction"] = dict(binding["layer_reconstruction"])
            item["review"] = dict(binding["review"])
            item["node_kind"] = binding["node_kind"]
            item["render_mode"] = binding["render_mode"]
            item["reusable_bitmap"] = binding["reusable_bitmap"]
            item["asset_policy"] = "layer"
            item["status"] = "pending_review"
        hydrated.append(item)
    root = bindings.get("background.root")
    if root and "background.root" not in seen:
        hydrated.append({
            "id": "background.root",
            "component_id": "background.root",
            "parent_id": "root",
            "category": "background",
            "bounds": root["bounds"],
            "layer": 0,
            "z_index": root["z_index"],
            "status": "pending_review",
            "asset_policy": "layer",
            "visual_assets": root["visual_assets"],
            "layer_reconstruction": root["layer_reconstruction"],
            "review": root["review"],
            "node_kind": root["node_kind"],
            "render_mode": root["render_mode"],
            "reusable_bitmap": root["reusable_bitmap"],
            "extraction": {"mode": "reconstruct_skin", "target_component_id": "background.root"},
        })
    return hydrated


def normalize_controls(
    controls_path: Path | None,
    session_dir: Path,
    width: int,
    height: int,
    extraction_plan_path: Path | None = None,
    execution_report_path: Path | None = None,
    library_references_path: Path | None = None,
) -> list[dict[str, Any]]:
    if controls_path is None:
        return [{
            "component_id": "background.root",
            "category": "background",
            "parent_id": "root",
            "layer": 0,
            "z_index": -100000,
            "bounds": {"x": 0, "y": 0, "width": width, "height": height},
            "status": "candidate",
            "confidence": 0.25,
            "reason": "No generated UI Tree was supplied; only the source image is available.",
            "asset_policy": "reconstruction_candidate",
            "node_kind": "skin",
            "render_mode": "bitmap",
            "visual_assets": {"source_crop": "__source__", "clean_layer": None, "assembly_preview": None},
            "layer_reconstruction": {
                "status": "pending",
                "remove_nodes": [],
                "direct_children": [],
                "visible_descendants": [],
                "native_descendants": [],
                "artwork_descendants": [],
                "mask": {"operation": "union", "deduplicate_pixels": True, "sources": []},
                "method": "image_reconstruction",
                "transparent": True,
                "error": None,
            },
            "review": {"status": "candidate", "cleanup_status": "pending"},
            "reusable_bitmap": False,
            "children": [],
        }]

    data = json.loads(controls_path.read_text(encoding="utf-8-sig"))
    items = raw_controls(data)
    bindings = reconstruction_bindings(extraction_plan_path, execution_report_path, controls_path.parent)
    items = hydrate_reconstructed_controls(items, bindings)
    library_preview_records = load_library_preview_records(library_references_path)
    if not items:
        raise ValueError("Controls JSON has no controls/components/elements/layers/items/nodes array.")
    id_map: dict[str, str] = {}
    prepared: list[tuple[dict[str, Any], str, str]] = []
    used: set[str] = set()
    for index, item in enumerate(items, 1):
        element_id = str(first(item, ("element_id", "elementId", "id", "uuid"), f"element-{index}"))
        original_component_id = str(first(item, ("component_id", "componentId", "control_id", "controlId", "id", "name"), ""))
        component_id = component_id_for(item, index)
        base, suffix = component_id, 2
        while component_id in used:
            component_id = f"{base}.v{suffix}"
            suffix += 1
        used.add(component_id)
        id_map[element_id] = component_id
        if original_component_id:
            id_map[original_component_id] = component_id
        id_map[component_id] = component_id
        prepared.append((item, element_id, component_id))

    parent_keys = ("parent_id", "parentId", "parent", "group_id", "groupId")
    prepared_bounds = {component_id: bounds_from(item) for item, _element_id, component_id in prepared}
    parent_by_component: dict[str, str] = {}
    child_counts: dict[str, int] = {}
    for item, _element_id, component_id in prepared:
        parent_value = first(item, parent_keys)
        parent_raw = str(parent_value) if parent_value is not None else None
        if parent_raw is not None:
            parent_id = id_map.get(parent_raw, "root") if parent_raw != "root" else "root"
        else:
            bounds = prepared_bounds[component_id]
            candidates: list[tuple[float, str]] = []
            if bounds is not None:
                area = bounds["width"] * bounds["height"]
                for _candidate_item, _candidate_element, candidate_id in prepared:
                    candidate = prepared_bounds[candidate_id]
                    if candidate_id == component_id or candidate is None:
                        continue
                    candidate_area = candidate["width"] * candidate["height"]
                    contains = (
                        candidate_area > area
                        and candidate["x"] <= bounds["x"]
                        and candidate["y"] <= bounds["y"]
                        and candidate["x"] + candidate["width"] >= bounds["x"] + bounds["width"]
                        and candidate["y"] + candidate["height"] >= bounds["y"] + bounds["height"]
                    )
                    if contains:
                        candidates.append((candidate_area, candidate_id))
            parent_id = min(candidates)[1] if candidates else "root"
        parent_by_component[component_id] = parent_id
        child_counts[parent_id] = child_counts.get(parent_id, 0) + 1

    layer_dir = session_dir / "layers"
    controls: list[dict[str, Any]] = []
    for index, (item, element_id, component_id) in enumerate(prepared, 1):
        bounds = bounds_from(item)
        if bounds is None:
            raise ValueError(f"{component_id} has no valid bounds.")
        if bounds["x"] < 0 or bounds["y"] < 0 or bounds["x"] + bounds["width"] > width or bounds["y"] + bounds["height"] > height:
            raise ValueError(f"{component_id} bounds exceed the source image.")
        parent_value = first(item, parent_keys)
        parent_raw = str(parent_value) if parent_value is not None else None
        parent_id = parent_by_component[component_id]
        reasons: list[str] = []
        if parent_raw not in (None, "root") and parent_id == "root":
            reasons.append(f"Missing parent {parent_raw}; attached to root.")
        status = str(item.get("status") or "pending_review")
        if status not in ("pending_review", "candidate"):
            status = "candidate"
            reasons.append("Generated controls cannot be auto-promoted to active.")
        copied_file = None
        file_value = item.get("file")
        if isinstance(file_value, str):
            source_file = (controls_path.parent / file_value).resolve()
            if source_file.is_file():
                layer_dir.mkdir(exist_ok=True)
                target = layer_dir / f"{component_id}{source_file.suffix.lower()}"
                shutil.copy2(source_file, target)
                copied_file = target.relative_to(session_dir).as_posix()

        copied_visual_assets: dict[str, Any] = {}
        raw_visual_assets = dict(item.get("visual_assets")) if isinstance(item.get("visual_assets"), dict) else {}
        extraction = item.get("extraction") if isinstance(item.get("extraction"), dict) else {}
        declared_native = (
            item.get("node_kind") == "native"
            or item.get("asset_policy") == "native"
            or extraction.get("mode") == "native"
        )
        explicit_native_preview = item.get("native_preview")
        if isinstance(explicit_native_preview, str) and not raw_visual_assets.get("native_preview"):
            raw_visual_assets["native_preview"] = explicit_native_preview
        library_preview = resolve_library_preview(item, library_preview_records)
        component_reuse = library_component_reuse(item, library_preview)
        library_preview_slot = "native_preview" if declared_native else "clean_layer"
        if library_preview and not raw_visual_assets.get(library_preview_slot):
            raw_visual_assets[library_preview_slot] = str(library_preview["source"])
        asset_directories = {
            "source_crop": session_dir / "source",
            "clean_layer": session_dir / "layers",
            "assembly_preview": session_dir / "preview",
            "native_preview": session_dir / "native",
        }
        for asset_name, asset_directory in asset_directories.items():
            asset_value = raw_visual_assets.get(asset_name)
            if asset_value in (None, "__source__"):
                copied_visual_assets[asset_name] = asset_value
                continue
            if not isinstance(asset_value, str):
                copied_visual_assets[asset_name] = None
                continue
            source_asset = (controls_path.parent / asset_value).resolve()
            if not source_asset.is_file():
                copied_visual_assets[asset_name] = None
                reasons.append(f"Missing {asset_name}: {asset_value}.")
                continue
            asset_directory.mkdir(exist_ok=True)
            target_asset = asset_directory / f"{component_id}{source_asset.suffix.lower()}"
            shutil.copy2(source_asset, target_asset)
            copied_visual_assets[asset_name] = target_asset.relative_to(session_dir).as_posix()

        semantic_input = dict(item)
        if raw_visual_assets:
            semantic_input["visual_assets"] = copied_visual_assets
        semantics = normalize_node_semantics(semantic_input, child_counts.get(component_id, 0) > 0, copied_file)
        if semantics["visual_assets"]["source_crop"] is None:
            semantics["visual_assets"]["source_crop"] = "__source__"
        status = semantics["review"]["status"]
        if reasons:
            status = "candidate"
            semantics["review"]["status"] = status

        control = {
            "component_id": component_id,
            "element_id": element_id,
            "category": str(item.get("category") or item.get("type") or "unknown").lower(),
            "parent_id": parent_id,
            "layer": int(float(first(item, ("layer", "semantic_layer", "semanticLayer"), 30))),
            "z_index": float(first(item, ("z_index", "zIndex", "z", "order", "index"), index - 1)),
            "bounds": bounds,
            "state": str(item.get("state") or "default"),
            "status": status,
            "confidence": float(item.get("confidence", 0.96)),
            "reason": "; ".join(reasons) or item.get("reason"),
            "asset_policy": item.get("asset_policy") or ("native" if semantics["node_kind"] == "native" else "layer" if semantics["layer_reconstruction"]["status"] == "ready" else "reconstruction_candidate"),
            "extraction": item.get("extraction") if isinstance(item.get("extraction"), dict) else None,
            **semantics,
        }
        for field in (
            "reuse_of",
            "texture_asset",
            "currency_texture_asset",
            "item_id",
            "currency_item_id",
            "semantic_key",
            "operation_id",
        ):
            if field in item:
                control[field] = item[field]
        if library_preview:
            control["library_reference"] = dict(library_preview["library"])
        if component_reuse:
            control["component_reuse"] = component_reuse
            control.setdefault("texture_asset", component_reuse["source_asset"])
        display_text = item.get("display_text")
        if not isinstance(display_text, str) or not display_text.strip():
            display_text = item.get("content_hint")
        defaulted_close_button = False
        if (
            (not isinstance(display_text, str) or not display_text.strip())
            and is_native_close_button(item, component_id, semantics["node_kind"])
            and component_reuse is None
        ):
            display_text = "×"
            defaulted_close_button = True
        if isinstance(display_text, str) and display_text.strip():
            control["display_text"] = display_text.strip()
        text_style = item.get("text_style")
        if defaulted_close_button:
            merged_style = dict(CLOSE_BUTTON_TEXT_STYLE)
            if isinstance(text_style, dict):
                merged_style.update(text_style)
            control["text_style"] = merged_style
        elif isinstance(text_style, dict):
            control["text_style"] = dict(text_style)
        if copied_file:
            control["file"] = copied_file
        controls.append(control)

    children_by_parent: dict[str, list[str]] = {}
    for control in controls:
        children_by_parent.setdefault(control["parent_id"], []).append(control["component_id"])
    foreground_ids = [control["component_id"] for control in controls]
    if "background.root" not in foreground_ids:
        controls.append({
            "component_id": "background.root",
            "element_id": "background-root",
            "category": "background",
            "parent_id": "root",
            "layer": 0,
            "z_index": -100000,
            "bounds": {"x": 0, "y": 0, "width": width, "height": height},
            "state": "default",
            "status": "candidate",
            "confidence": 1.0,
            "reason": "Root clean-background reconstruction target; source crop is trace-only.",
            "asset_policy": "reconstruction_candidate",
            "extraction": {"mode": "reconstruct_skin", "target_component_id": "background.root"},
            "node_kind": "skin",
            "render_mode": "bitmap",
            "visual_assets": {"source_crop": "__source__", "clean_layer": None, "assembly_preview": None},
            "layer_reconstruction": {"status": "pending", "method": "image_reconstruction", "transparent": True, "error": None},
            "review": {"status": "candidate", "cleanup_status": "pending"},
            "reusable_bitmap": False,
        })
        children_by_parent.setdefault("root", []).append("background.root")
        children_by_parent.setdefault("background.root", [])

    by_id = {control["component_id"]: control for control in controls}

    def descendants(component_id: str) -> list[str]:
        result: list[str] = []
        for child_id in children_by_parent.get(component_id, []):
            if child_id == "background.root":
                continue
            result.append(child_id)
            result.extend(descendants(child_id))
        return result

    for control in controls:
        component_id = control["component_id"]
        control["children"] = [child for child in children_by_parent.get(component_id, []) if child != "background.root"]
        remove_nodes = foreground_ids if component_id == "background.root" else descendants(component_id)
        reconstruction = control.get("layer_reconstruction") if isinstance(control.get("layer_reconstruction"), dict) else {}
        if control["node_kind"] == "native":
            reconstruction["status"] = "not_applicable"
            control["layer_reconstruction"] = reconstruction
            continue
        mask_sources = []
        for remove_id in remove_nodes:
            removed = by_id[remove_id]
            clean_layer = removed.get("visual_assets", {}).get("clean_layer")
            if clean_layer and removed.get("node_kind") != "native":
                mask_sources.append({"node_id": remove_id, "source_type": "clean_layer_alpha", "path": clean_layer})
            else:
                mask_sources.append({"node_id": remove_id, "source_type": "bounds_fallback", "bounds": removed["bounds"], "padding": 2, "fallback_only": True})
        reconstruction.update({
            "remove_nodes": remove_nodes,
            "direct_children": control["children"] if component_id != "background.root" else [item for item in children_by_parent.get("root", []) if item != "background.root"],
            "visible_descendants": remove_nodes,
            "native_descendants": [item for item in remove_nodes if by_id[item]["node_kind"] == "native"],
            "artwork_descendants": [item for item in remove_nodes if by_id[item]["node_kind"] == "artwork"],
            "mask": {
                "operation": "union",
                "deduplicate_pixels": True,
                "priority": ["alpha_mask", "clean_layer_alpha", "semantic_mask", "bounds_fallback"],
                "sources": mask_sources,
            },
            "method": "image_reconstruction",
            "transparent": True,
            "error": reconstruction.get("error"),
        })
        control["layer_reconstruction"] = reconstruction
    return controls


def free_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def start_server(directory: Path, host: str, port: int) -> int:
    python = Path(sys.executable)
    pythonw = python.with_name("pythonw.exe")
    executable = pythonw if pythonw.is_file() else python
    flags = 0
    if sys.platform == "win32":
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    process = subprocess.Popen(
        [str(executable), str(SERVER_SCRIPT), "--directory", str(directory), "--host", host, "--port", str(port)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        creationflags=flags,
    )
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return process.pid
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("Workbench server did not start within 5 seconds.")


def find_companion_executable(explicit: Path | None) -> Path | None:
    if explicit is not None:
        candidate = explicit.expanduser().resolve()
        return candidate if candidate.is_file() else None
    environment_value = os.environ.get("OASIS_COMPANION_EXE")
    if environment_value:
        candidate = Path(environment_value).expanduser().resolve()
        if candidate.is_file():
            return candidate
    candidate = DEFAULT_COMPANION_EXECUTABLE.expanduser().resolve()
    return candidate if candidate.is_file() else None


def start_companion_handoff(
    executable: Path,
    url: str,
    session_dir: Path | None = None,
) -> dict[str, Any]:
    return dispatch_companion_handoff(
        executable,
        {
            "schema_version": 1,
            "kind": "ui_workbench",
            "url": url,
            "session_dir": str(session_dir.resolve()) if session_dir is not None else None,
        },
    )


def create_companion_handoff(
    explicit: Path | None,
    url: str,
    session_dir: Path | None = None,
) -> dict[str, Any]:
    executable = find_companion_executable(explicit)
    if executable is None:
        return {"status": "fallback", "reason": "companion_not_found"}
    try:
        handoff = start_companion_handoff(executable, url, session_dir)
    except OSError as error:
        return {
            "status": "fallback",
            "reason": "companion_launch_failed",
            "error_type": type(error).__name__,
        }
    return {**handoff, "url": url}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and launch a local UI control workbench.")
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--controls", type=Path)
    parser.add_argument("--visual-review", type=Path, help="Approved visual-review.json from the Cowart review stage.")
    parser.add_argument("--execution-report", type=Path, help="Completed layer-reconstruction-execution.json evidence.")
    parser.add_argument("--extraction-plan", type=Path, help="Validated extraction-plan.json used to bind reconstructed Clean assets.")
    parser.add_argument("--library-references", type=Path, help="Resolved active project-library references used for reusable assets and native previews.")
    parser.add_argument("--allow-unreviewed", action="store_true", help="Diagnostic only: bypass the required visual approval gate.")
    parser.add_argument("--name", default="Generated UI")
    parser.add_argument("--page-id")
    parser.add_argument("--output-root", type=Path, default=Path.home() / ".codex" / "ui-workbenches")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--companion-executable", type=Path)
    parser.add_argument("--no-start", action="store_true")
    args = parser.parse_args()

    image_path = args.image.resolve()
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    if args.visual_review:
        review = validate_visual_review(args.visual_review.resolve(), image_path)
    elif args.allow_unreviewed:
        review = None
    else:
        raise ValueError("An approved --visual-review is required. Use --allow-unreviewed only for diagnostics.")
    with Image.open(image_path) as image:
        width, height = image.size
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    session_dir = args.output_root.resolve() / f"{stamp}-{slug(args.name)}"
    session_dir.mkdir(parents=True, exist_ok=False)
    (session_dir / "index.html").write_text(HIDDEN_BRIDGE_HTML, encoding="utf-8")
    source_name = f"source{image_path.suffix.lower()}"
    shutil.copy2(image_path, session_dir / source_name)
    thumbnail_name = "thumbnail.webp"
    create_thumbnail(image_path, session_dir / thumbnail_name)
    controls_path = args.controls.resolve() if args.controls else None
    execution_report_path = args.execution_report.resolve() if args.execution_report else None
    extraction_plan_path = args.extraction_plan.resolve() if args.extraction_plan else None
    library_references_path = args.library_references.resolve() if args.library_references else None
    if extraction_plan_path is None and controls_path is not None:
        candidate = controls_path.parent / "extraction-plan.json"
        extraction_plan_path = candidate if candidate.is_file() else None
    controls = normalize_controls(
        controls_path,
        session_dir,
        width,
        height,
        extraction_plan_path=extraction_plan_path,
        execution_report_path=execution_report_path,
        library_references_path=library_references_path,
    )
    page_id = resolve_page_id(args.page_id, args.name)
    agent_context = capture_agent_context(os.environ, shutil.which, Path.cwd())
    session = {
        "schema_version": 3,
        "page_id": page_id,
        "title": args.name,
        "source_image": source_name,
        "thumbnail_image": thumbnail_name,
        "source_name": image_path.name,
        "source_size": {"width": width, "height": height},
        "controls": controls,
        "layer_reconstruction_capability": load_reconstruction_capability(args.execution_report),
        "visual_review": {
            "status": review["status"] if review else "unreviewed_diagnostic",
            "path": str(args.visual_review.resolve()) if args.visual_review else None,
            "image_sha256": sha256_file(image_path),
        },
        "workflow_task": {"schema_version": 1, "task_id": page_id},
        "agent_context": agent_context,
    }
    (session_dir / "session.json").write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")
    port = args.port or free_port(args.host)
    url = f"http://localhost:{port}/"
    shortcut = session_dir / "Open UI Workbench.url"
    shortcut.write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    pid = None if args.no_start else start_server(session_dir, args.host, port)
    companion_handoff = (
        {"status": "disabled", "reason": "no_start"}
        if args.no_start
        else create_companion_handoff(args.companion_executable, url, session_dir)
    )
    result = {
        "url": url,
        "session_dir": str(session_dir),
        "shortcut": str(shortcut),
        "server_pid": pid,
        "companion_handoff": companion_handoff,
        "control_count": len(controls),
        "legacy_extractor_ui_hidden": True,
        "extraction_plan": str(extraction_plan_path) if extraction_plan_path else None,
        "library_references": str(library_references_path) if library_references_path else None,
    }
    (session_dir / "workbench.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
