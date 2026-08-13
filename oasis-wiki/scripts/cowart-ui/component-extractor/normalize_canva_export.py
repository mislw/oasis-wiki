from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from canva_adapter import (
    ID_KEYS,
    PARENT_KEYS,
    Z_KEYS,
    bounds_from,
    elements_from,
    first,
    infer_category,
    page_size_from,
    resolve_file,
    semantic_layer,
    slug_component_id,
)
from component_semantics import normalize_node_semantics


MANIFEST_NAMES = ("layer-manifest.json", "manifest.json", "export.json", "metadata.json")


def find_manifest(directory: Path) -> Path | None:
    for name in MANIFEST_NAMES:
        direct = directory / name
        if direct.is_file():
            return direct
    json_files = sorted(directory.glob("*.json"))
    return json_files[0] if len(json_files) == 1 else None


def load_source(input_path: Path, allow_png_fallback: bool) -> tuple[dict[str, Any], Path, str]:
    if input_path.is_file():
        return json.loads(input_path.read_text(encoding="utf-8-sig")), input_path.parent, input_path.name
    manifest = find_manifest(input_path)
    if manifest:
        return json.loads(manifest.read_text(encoding="utf-8-sig")), manifest.parent, manifest.name
    if not allow_png_fallback:
        raise ValueError("No metadata JSON found. Re-run with --allow-png-fallback for candidate-only import.")
    png_files = sorted(input_path.rglob("*.png"))
    if not png_files:
        raise ValueError("No metadata JSON or PNG files found.")
    elements = []
    for index, path in enumerate(png_files):
        with Image.open(path) as image:
            width, height = image.size
        elements.append({
            "id": f"png-{index + 1}", "name": path.stem, "file": str(path),
            "x": 0, "y": 0, "width": width, "height": height, "order": index,
            "_fallback": True,
        })
    max_width = max(item["width"] for item in elements)
    max_height = max(item["height"] for item in elements)
    return {"page_size": {"width": max_width, "height": max_height}, "elements": elements}, input_path, "(png-only)"


def find_atlas(raw: dict[str, Any], base_dir: Path, source_name: str) -> Path | None:
    atlas_value = raw.get("atlas_file") or raw.get("atlasFile")
    candidates = []
    if isinstance(atlas_value, str):
        candidates.append(base_dir / atlas_value)
    if source_name not in ("(png-only)", ""):
        candidates.append(base_dir / f"{Path(source_name).stem}.png")
    candidates.extend(
        [
            base_dir / "redcliff-component-candidates.png",
            base_dir / "component-candidates.png",
            base_dir / "atlas.png",
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    png_files = sorted(base_dir.glob("*.png"))
    return png_files[0].resolve() if len(png_files) == 1 else None


def crop_atlas_layer(atlas: Image.Image, atlas_rect: dict[str, Any], target: Path) -> bool:
    try:
        x = int(round(float(atlas_rect.get("x", 0))))
        y = int(round(float(atlas_rect.get("y", 0))))
        width = int(round(float(atlas_rect.get("width", atlas_rect.get("w")))))
        height = int(round(float(atlas_rect.get("height", atlas_rect.get("h")))))
    except (TypeError, ValueError):
        return False
    if width <= 0 or height <= 0 or x < 0 or y < 0 or x + width > atlas.width or y + height > atlas.height:
        return False
    atlas.crop((x, y, x + width, y + height)).save(target)
    return True


def normalize(input_path: Path, output_dir: Path, allow_png_fallback: bool = False, force: bool = False) -> Path:
    raw, base_dir, source_name = load_source(input_path, allow_png_fallback)
    page_size = page_size_from(raw)
    elements = elements_from(raw)
    if not elements:
        raise ValueError("Metadata does not contain an elements/layers/components/items array.")

    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise FileExistsError(f"Output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    layers_dir = output_dir / "layers"
    layers_dir.mkdir(exist_ok=True)
    source_dir = output_dir / "source"
    source_dir.mkdir(exist_ok=True)

    warnings: list[str] = []
    if source_name == "(png-only)":
        warnings.append("PNG-only fallback cannot recover positions, hierarchy, rotation, or true z-order.")

    used_ids: set[str] = set()
    element_to_component: dict[str, str] = {}
    prepared: list[dict[str, Any]] = []
    for index, element in enumerate(elements, 1):
        element_id = str(first(element, ID_KEYS, f"element-{index}"))
        proposed = first(element, ("component_id", "componentId", "control_id", "controlId", "name"), element_id)
        component_id = slug_component_id(proposed, index)
        base_id, suffix = component_id, 2
        while component_id in used_ids:
            component_id = f"{base_id}.v{suffix}"
            suffix += 1
        used_ids.add(component_id)
        element_to_component[element_id] = component_id
        element_to_component[component_id] = component_id
        element_to_component[str(proposed)] = component_id
        prepared.append({"raw": element, "element_id": element_id, "component_id": component_id, "index": index})

    components: list[dict[str, Any]] = []
    raw_parent_ids = {
        str(first(item["raw"], PARENT_KEYS))
        for item in prepared
        if first(item["raw"], PARENT_KEYS) is not None
    }
    atlas_path = find_atlas(raw, base_dir, source_name)
    atlas_image = None
    if atlas_path:
        with Image.open(atlas_path) as source_atlas:
            atlas_image = source_atlas.convert("RGBA")
    for prepared_item in prepared:
        element = prepared_item["raw"]
        index = prepared_item["index"]
        component_id = prepared_item["component_id"]
        file_path = resolve_file(element, base_dir)
        bounds = bounds_from(element)
        category = infer_category(element)
        parent_raw = first(element, PARENT_KEYS)
        parent_id = element_to_component.get(str(parent_raw), "root") if parent_raw else "root"
        issues = []
        atlas_rect = first(element, ("atlas_rect", "atlasRect"))
        if bounds is None:
            issues.append("page-space bounds are missing")
        if parent_raw and parent_id == "root":
            issues.append(f"parent element was not found: {parent_raw}")
        if page_size is None:
            issues.append("page size is missing")
        if element.get("_fallback"):
            issues.append("PNG-only fallback requires manual placement and hierarchy review")

        has_children = prepared_item["element_id"] in raw_parent_ids or component_id in raw_parent_ids
        initial_semantics = normalize_node_semantics(element, has_children=has_children)
        asset_directory = source_dir if initial_semantics["node_kind"] in {"composite", "native"} else layers_dir
        asset_prefix = "source" if asset_directory == source_dir else "layers"
        relative_file = None
        target_name = f"{component_id}.png"
        target = asset_directory / target_name
        if file_path is not None:
            if file_path.resolve() != target.resolve():
                shutil.copy2(file_path, target)
            relative_file = f"{asset_prefix}/{target_name}"
            if bounds is None:
                with Image.open(file_path) as image:
                    bounds = {"x": 0, "y": 0, "width": image.width, "height": image.height}
        elif atlas_image is not None and isinstance(atlas_rect, dict) and crop_atlas_layer(atlas_image, atlas_rect, target):
            relative_file = f"{asset_prefix}/{target_name}"
        else:
            issues.append("layer PNG could not be resolved")

        z_raw = first(element, Z_KEYS, index - 1)
        try:
            z_index = float(z_raw)
        except (TypeError, ValueError):
            z_index = float(index - 1)
            issues.append("z-index was invalid and replaced by source order")
        layer_raw = first(element, ("layer", "semantic_layer", "semanticLayer"), semantic_layer(category))
        try:
            layer = int(round(float(layer_raw)))
        except (TypeError, ValueError):
            layer = semantic_layer(category)
            issues.append("semantic layer was invalid and inferred from category")

        source_status = str(element.get("status") or "").lower()
        source_reason = element.get("reason") if isinstance(element.get("reason"), str) else None
        if source_status == "candidate" and source_reason:
            issues.insert(0, source_reason)
        semantics = normalize_node_semantics(element, has_children=has_children, file_value=relative_file)
        component = {
            "component_id": component_id,
            "element_id": prepared_item["element_id"],
            "name": str(element.get("name") or component_id),
            "category": category,
            "file": semantics["visual_assets"].get("clean_layer"),
            "parent_id": parent_id,
            "layer": layer,
            "z_index": z_index,
            "bounds": bounds,
            "rotation": float(first(element, ("rotation", "angle"), 0) or 0),
            "opacity": float(first(element, ("opacity", "alpha"), 1) or 0),
            "padding": max(0, float(element.get("padding", 0) or 0)),
            "mask": first(element, ("mask", "clip", "clipPath")),
            "text": first(element, ("text", "content", "characters")),
            "font": first(element, ("font", "fontFamily", "typography")),
            "status": "candidate" if issues or semantics["review"]["status"] == "candidate" or source_status == "candidate" else "pending_review",
            "reason": "; ".join(issues) if issues else None,
            "source_fields": element,
            **semantics,
        }
        components.append(component)
        warnings.extend(f"{component_id}: {issue}" for issue in issues)

    if atlas_image is not None:
        atlas_image.close()

    if page_size is None:
        max_x = max((item["bounds"] or {}).get("x", 0) + (item["bounds"] or {}).get("width", 0) for item in components)
        max_y = max((item["bounds"] or {}).get("y", 0) + (item["bounds"] or {}).get("height", 0) for item in components)
        page_size = {"width": max(1, int(round(max_x))), "height": max(1, int(round(max_y)))}

    children_by_parent: dict[str, list[str]] = {"root": []}
    for item in components:
        children_by_parent.setdefault(item["parent_id"], []).append(item["component_id"])
        children_by_parent.setdefault(item["component_id"], [])
    for item in components:
        item["children"] = children_by_parent[item["component_id"]]
    root_children = children_by_parent["root"]
    manifest = {
        "schema_version": 3,
        "batch_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "source": {
            "kind": "png_only_fallback" if source_name == "(png-only)" else "canva_magic_layers",
            "manifest_file": source_name,
            "page_size": page_size,
        },
        "components": components,
        "ui_tree": {"root_id": "root", "children": root_children},
        "warnings": warnings,
    }
    destination = output_dir / "layer-manifest.json"
    destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Canva layer exports into the Cowart layer manifest contract.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--allow-png-fallback", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        output = normalize(args.input.resolve(), args.output.resolve(), args.allow_png_fallback, args.force)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
