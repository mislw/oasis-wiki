from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable


ELEMENT_KEYS = ("elements", "layers", "components", "items")
ID_KEYS = ("element_id", "elementId", "id", "uuid")
FILE_KEYS = ("file", "fileName", "filename", "asset", "image", "src")
PARENT_KEYS = ("parent_id", "parentId", "group_id", "groupId", "parent")
Z_KEYS = ("z_index", "zIndex", "z", "order", "index")


def first(mapping: dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return default


def elements_from(raw: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ELEMENT_KEYS:
        value = raw.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    for container_key in ("document", "export", "data"):
        container = raw.get(container_key)
        if isinstance(container, dict):
            nested = elements_from(container)
            if nested:
                return nested
    return []


def page_size_from(raw: dict[str, Any]) -> dict[str, int] | None:
    candidates: list[Any] = [
        raw.get("page_size"), raw.get("pageSize"), raw.get("source_size"),
        raw.get("canvas"), raw.get("page")
    ]
    pages = raw.get("pages")
    if isinstance(pages, list) and pages:
        candidates.append(pages[0])
    candidates.append(raw)
    for value in candidates:
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            width, height = value[0], value[1]
        elif isinstance(value, dict):
            width = first(value, ("width", "w", "pixelWidth"))
            height = first(value, ("height", "h", "pixelHeight"))
        else:
            continue
        try:
            width_i, height_i = int(round(float(width))), int(round(float(height)))
        except (TypeError, ValueError):
            continue
        if width_i > 0 and height_i > 0:
            return {"width": width_i, "height": height_i}
    return None


def bounds_from(element: dict[str, Any]) -> dict[str, float] | None:
    value = first(
        element,
        ("bounds", "layout_rect", "layoutRect", "source_rect", "sourceRect", "rect", "frame", "position"),
        element,
    )
    if not isinstance(value, dict):
        return None
    x = first(value, ("x", "left"), first(element, ("x", "left"), 0))
    y = first(value, ("y", "top"), first(element, ("y", "top"), 0))
    width = first(value, ("width", "w"), first(element, ("width", "w")))
    height = first(value, ("height", "h"), first(element, ("height", "h")))
    try:
        result = {
            "x": round(float(x), 4),
            "y": round(float(y), 4),
            "width": round(float(width), 4),
            "height": round(float(height), 4),
        }
    except (TypeError, ValueError):
        return None
    return result if result["width"] > 0 and result["height"] > 0 else None


def slug_component_id(value: Any, index: int) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", ".", text).strip(".")
    if not text or "." not in text:
        text = f"layer.{text or f'item{index:04d}'}"
    return text[:96].rstrip(".")


def infer_category(element: dict[str, Any]) -> str:
    explicit = element.get("category")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip().lower()
    text = " ".join(str(element.get(key, "")) for key in ("category", "type", "kind", "name")).lower()
    for category, tokens in (
        ("button", ("button", "cta", "purchase", "buy")),
        ("text", ("text", "label", "title", "caption")),
        ("icon", ("icon", "glyph")),
        ("badge", ("badge", "tag", "status")),
        ("card", ("card", "tile", "slot")),
        ("panel", ("panel", "container", "group", "frame")),
        ("image", ("image", "photo", "illustration")),
    ):
        if any(token in text for token in tokens):
            return category
    return "unknown"


def semantic_layer(category: str) -> int:
    return {
        "panel": 20,
        "card": 30,
        "image": 40,
        "icon": 40,
        "text": 50,
        "button": 60,
        "badge": 70,
    }.get(category, 30)


def resolve_file(element: dict[str, Any], base_dir: Path) -> Path | None:
    value = first(element, FILE_KEYS)
    if isinstance(value, dict):
        value = first(value, ("file", "fileName", "filename", "path", "src", "url"))
    if not isinstance(value, str) or value.startswith(("http://", "https://", "data:")):
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    if candidate.is_file():
        return candidate.resolve()
    name = Path(value).name
    matches = list(base_dir.rglob(name))
    return matches[0].resolve() if len(matches) == 1 else None
