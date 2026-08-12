from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


WIKI_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_ROOT = Path(__file__).resolve().parent
TEMPLATE = WIKI_ROOT / "assets" / "cowart-ui" / "workbench-template" / "index.html"
SERVER_SCRIPT = SCRIPT_ROOT / "serve_workbench.py"


def slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or "ui-workbench"


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
    for key in ("controls", "components", "elements", "layers", "items"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def normalize_controls(
    controls_path: Path | None,
    session_dir: Path,
    width: int,
    height: int,
) -> list[dict[str, Any]]:
    if controls_path is None:
        return [{
            "component_id": "background.ui.source",
            "category": "background",
            "parent_id": "root",
            "layer": 0,
            "z_index": 0,
            "bounds": {"x": 0, "y": 0, "width": width, "height": height},
            "status": "candidate",
            "confidence": 0.25,
            "reason": "No generated UI Tree was supplied; only the source image is available.",
        }]

    data = json.loads(controls_path.read_text(encoding="utf-8-sig"))
    items = raw_controls(data)
    if not items:
        raise ValueError("Controls JSON has no controls/components/elements/layers/items array.")
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

    layer_dir = session_dir / "layers"
    controls: list[dict[str, Any]] = []
    for index, (item, element_id, component_id) in enumerate(prepared, 1):
        bounds = bounds_from(item)
        if bounds is None:
            raise ValueError(f"{component_id} has no valid bounds.")
        if bounds["x"] < 0 or bounds["y"] < 0 or bounds["x"] + bounds["width"] > width or bounds["y"] + bounds["height"] > height:
            raise ValueError(f"{component_id} bounds exceed the source image.")
        parent_raw = str(first(item, ("parent_id", "parentId", "parent", "group_id", "groupId"), "root"))
        parent_id = id_map.get(parent_raw, "root") if parent_raw != "root" else "root"
        reasons: list[str] = []
        if parent_raw != "root" and parent_id == "root":
            reasons.append(f"Missing parent {parent_raw}; attached to root.")
        status = str(item.get("status") or "pending_review")
        if status not in ("pending_review", "candidate"):
            status = "candidate"
            reasons.append("Generated controls cannot be auto-promoted to active.")
        control = {
            "component_id": component_id,
            "element_id": element_id,
            "category": str(item.get("category") or item.get("type") or "unknown").lower(),
            "parent_id": parent_id,
            "layer": int(float(first(item, ("layer", "semantic_layer", "semanticLayer"), 30))),
            "z_index": float(first(item, ("z_index", "zIndex", "z", "order", "index"), index - 1)),
            "bounds": bounds,
            "state": str(item.get("state") or "default"),
            "status": "candidate" if reasons else status,
            "confidence": float(item.get("confidence", 0.96)),
            "reason": "; ".join(reasons) or item.get("reason"),
        }
        file_value = item.get("file")
        if isinstance(file_value, str):
            source_file = (controls_path.parent / file_value).resolve()
            if source_file.is_file():
                layer_dir.mkdir(exist_ok=True)
                target = layer_dir / f"{component_id}{source_file.suffix.lower()}"
                shutil.copy2(source_file, target)
                control["file"] = target.relative_to(session_dir).as_posix()
        controls.append(control)
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and launch a local UI control workbench.")
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--controls", type=Path)
    parser.add_argument("--visual-review", type=Path, help="Approved visual-review.json from the Cowart review stage.")
    parser.add_argument("--allow-unreviewed", action="store_true", help="Diagnostic only: bypass the required visual approval gate.")
    parser.add_argument("--name", default="Generated UI")
    parser.add_argument("--output-root", type=Path, default=Path.home() / ".codex" / "ui-workbenches")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
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
    shutil.copy2(TEMPLATE, session_dir / "index.html")
    source_name = f"source{image_path.suffix.lower()}"
    shutil.copy2(image_path, session_dir / source_name)
    controls = normalize_controls(args.controls.resolve() if args.controls else None, session_dir, width, height)
    session = {
        "schema_version": 1,
        "title": args.name,
        "source_image": source_name,
        "source_name": image_path.name,
        "source_size": {"width": width, "height": height},
        "controls": controls,
        "visual_review": {
            "status": review["status"] if review else "unreviewed_diagnostic",
            "path": str(args.visual_review.resolve()) if args.visual_review else None,
            "image_sha256": sha256_file(image_path),
        },
    }
    (session_dir / "session.json").write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")
    port = args.port or free_port(args.host)
    url = f"http://localhost:{port}/"
    shortcut = session_dir / "Open UI Workbench.url"
    shortcut.write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    pid = None if args.no_start else start_server(session_dir, args.host, port)
    result = {
        "url": url,
        "session_dir": str(session_dir),
        "shortcut": str(shortcut),
        "server_pid": pid,
        "control_count": len(controls),
    }
    (session_dir / "workbench.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
