from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a RedCliff UI delivery plan.")
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.resolve().read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = []
    if plan.get("schema_version") != 1 or plan.get("artifact_type") != "redcliff_ui_delivery_plan":
        errors.append("unsupported delivery plan")
    widgets = plan.get("widgets")
    if not isinstance(widgets, list) or not widgets:
        errors.append("widgets must be a non-empty array")
        widgets = []
    ids = {item.get("component_id") for item in widgets if isinstance(item, dict)}
    for item in widgets:
        if not isinstance(item, dict):
            errors.append("widget must be an object")
            continue
        for key in ("widget_name", "component_id", "widget_class", "parent_id", "bounds"):
            if key not in item:
                errors.append(f"widget missing {key}")
        if item.get("parent_id") != "root" and item.get("parent_id") not in ids:
            errors.append(f"{item.get('component_id')} references missing parent")
    if plan.get("ready_for_editor") and plan.get("review_blockers"):
        errors.append("ready_for_editor cannot be true with review blockers")
    if errors:
        for error in sorted(set(errors)):
            print(f"ERROR: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
