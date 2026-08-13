from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from component_semantics import activation_gate_errors


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be an object")
    return value


def profile_validator() -> Any:
    script = Path(__file__).resolve().parents[3] / "scripts" / "game-ui" / "validate_library.py"
    if not script.is_file():
        raise FileNotFoundError(f"Game UI validator not found: {script}")
    spec = importlib.util.spec_from_file_location("game_ui_validator", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load game UI validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_profile


def source_components(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    values = manifest.get("components")
    if not isinstance(values, list):
        raise ValueError("manifest.components must be an array")
    result = {}
    for component in values:
        if isinstance(component, dict) and isinstance(component.get("component_id"), str):
            result[component["component_id"]] = component
    return result


def copy_asset(component: dict[str, Any], manifest_path: Path, atlas: Path | None, target_dir: Path) -> str | None:
    component_id = component["component_id"]
    target_dir.mkdir(parents=True, exist_ok=True)
    if atlas is not None:
        rect = component.get("atlas_rect")
        if not isinstance(rect, dict):
            raise ValueError(f"{component_id} has no atlas_rect")
        with Image.open(atlas) as image:
            x, y = int(rect["x"]), int(rect["y"])
            width, height = int(rect["width"]), int(rect["height"])
            crop = image.crop((x, y, x + width, y + height)).convert("RGBA")
            name = f"{component_id}.png"
            crop.save(target_dir / name)
            return name
    visual_assets = component.get("visual_assets") if isinstance(component.get("visual_assets"), dict) else {}
    file_value = visual_assets.get("clean_layer") or component.get("file")
    if not isinstance(file_value, str):
        return None
    source = (manifest_path.parent / file_value).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    name = f"{component_id}{source.suffix.lower()}"
    shutil.copy2(source, target_dir / name)
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply explicit component review decisions to a user-level component profile.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--decisions", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--atlas", type=Path, help="Atlas PNG exported beside a workbench candidate manifest.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest_path, decisions_path, profile_path = args.manifest.resolve(), args.decisions.resolve(), args.profile.resolve()
    manifest, decisions, profile = read_json(manifest_path), read_json(decisions_path), read_json(profile_path)
    if decisions.get("schema_version") != 1 or not isinstance(decisions.get("reviewed_by"), str) or not decisions["reviewed_by"].strip():
        raise SystemExit("ERROR: decisions require schema_version=1 and reviewed_by")
    source = source_components(manifest)
    raw_decisions = decisions.get("decisions")
    if not isinstance(raw_decisions, list) or not raw_decisions:
        raise SystemExit("ERROR: decisions must be a non-empty array")
    existing = {item["component_id"]: item for item in profile.get("components", []) if isinstance(item, dict) and "component_id" in item}
    assets_dir = profile_path.parent / "assets" / "components"
    history = list(profile.get("history", []))
    changed = []
    timestamp = datetime.now(timezone.utc).isoformat()
    for decision in raw_decisions:
        if not isinstance(decision, dict):
            raise SystemExit("ERROR: every decision must be an object")
        component_id, action = decision.get("component_id"), decision.get("action")
        if component_id not in source:
            raise SystemExit(f"ERROR: decision references missing component {component_id}")
        if action not in {"activate", "reject"}:
            raise SystemExit(f"ERROR: {component_id}.action must be activate or reject")
        current = source[component_id]
        old = existing.get(component_id)
        old_version = old.get("version", 0) if old else 0
        if action == "reject":
            if old is None:
                continue
            old["status"] = "rejected"
            old["confirmed_by"] = decisions["reviewed_by"]
            old["version"] = old_version + 1
            history.append({"timestamp": timestamp, "component_id": component_id, "old_version": old_version, "new_version": old_version + 1, "action": "rejected", "reason": decision.get("reason", "developer rejected"), "affected_pages": []})
            changed.append(component_id)
            continue
        gate_errors = activation_gate_errors(current) if manifest.get("schema_version") == 2 else []
        if gate_errors:
            raise SystemExit("ERROR: " + "; ".join(gate_errors))
        confidence = float(current.get("confidence", 0))
        if confidence < 0.85:
            raise SystemExit(f"ERROR: {component_id} cannot become active below 0.85 confidence")
        required = ("name", "description", "usage", "states", "parent_types")
        missing = [key for key in required if not decision.get(key)]
        if missing:
            raise SystemExit(f"ERROR: {component_id} activation is missing: {', '.join(missing)}")
        asset = None if args.dry_run else copy_asset(current, manifest_path, args.atlas.resolve() if args.atlas else None, assets_dir)
        item = {
            "component_id": component_id,
            "name": decision["name"],
            "category": decision.get("category", current.get("category", "unknown")),
            "description": decision["description"],
            "usage": decision["usage"],
            "states": decision["states"],
            "parent_types": decision["parent_types"],
            "layer": int(current.get("layer", 30)),
            "reusable": bool(decision.get("reusable", True)),
            "visual_style": decision.get("visual_style", {}),
            "interaction": decision.get("interaction", {}),
            "source": {"manifest": str(manifest_path), "component_id": component_id, "asset": f"assets/components/{asset}" if asset else None},
            "confidence": confidence,
            "status": "active",
            "version": old_version + 1,
            "confirmed_by": decisions["reviewed_by"],
        }
        if old is None:
            profile.setdefault("components", []).append(item)
        else:
            profile["components"][profile["components"].index(old)] = item
        history.append({"timestamp": timestamp, "component_id": component_id, "old_version": old_version or None, "new_version": old_version + 1, "action": "activated", "reason": "explicit developer decision", "affected_pages": []})
        changed.append(component_id)
    profile["history"] = history
    errors = profile_validator()(profile)
    if errors:
        raise SystemExit("ERROR: profile would be invalid:\n" + "\n".join(f"- {error}" for error in errors))
    if not args.dry_run:
        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"profile": str(profile_path), "changed": changed, "dry_run": args.dry_run}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
