from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


NATIVE_WIDGETS = {
    "text": "TextBlock", "counter": "TextBlock", "input": "EditableTextBox",
    "button": "Button", "progress": "ProgressBar", "icon": "Image", "badge": "Image",
    "background": "CanvasPanel", "panel": "CanvasPanel", "card": "CanvasPanel",
    "grid": "UniformGridPanel", "row": "HorizontalBox", "slot": "SizeBox",
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be an object")
    return value


def widget_name(component_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", component_id).strip("_")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a RedCliff UMG and Lua delivery plan without mutating the project.")
    parser.add_argument("--ui-tree", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    tree, profile = read_json(args.ui_tree.resolve()), read_json(args.profile.resolve())
    if tree.get("artifact_type") != "ui_tree" or not isinstance(tree.get("components"), list):
        raise SystemExit("ERROR: ui-tree must be produced by build_ui_tree.py")
    active = {item.get("component_id") for item in profile.get("components", []) if item.get("status") == "active"}
    widgets, bindings, blockers = [], [], []
    for node in tree["components"]:
        component_id, category = node["component_id"], node["category"]
        reuse_of = node.get("reuse_of")
        if reuse_of and reuse_of not in active:
            blockers.append({"component_id": component_id, "reuse_of": reuse_of, "reason": "component is not active"})
        widget = {
            "widget_name": widget_name(component_id),
            "component_id": component_id,
            "widget_class": NATIVE_WIDGETS.get(category, "CanvasPanel"),
            "category": category,
            "parent_id": node["parent_id"],
            "layer": node["layer"],
            "z_index": node["z_index"],
            "bounds": node["bounds"],
            "asset_policy": node["asset_policy"],
            "reuse_of": reuse_of,
            "dynamic": bool(node.get("dynamic", False)),
        }
        widgets.append(widget)
        for key in node.get("bindings", []):
            bindings.append({"component_id": component_id, "data_key": key, "refresh_owner": "UI Lua controller"})
    operations = tree.get("operations", [])
    acceptance = [
        "Widget hierarchy matches widgets and every child has the declared parent.",
        "Editor preview visually matches the approved bitmap at the declared canvas size.",
        "Every operation has a bound input and an authoritative owner.",
        "Dynamic bindings refresh after open, action completion, reconnect, and relevant data change.",
        "PIE proves visible behavior; static plan validation is not sufficient.",
    ]
    plan = {
        "schema_version": 1,
        "artifact_type": "redcliff_ui_delivery_plan",
        "page": tree.get("page", {}),
        "ready_for_editor": not blockers,
        "review_blockers": blockers,
        "widgets": widgets,
        "bindings": bindings,
        "operations": operations,
        "acceptance": acceptance,
    }
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"delivery_plan": str(output), "ready_for_editor": plan["ready_for_editor"], "blockers": len(blockers)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
