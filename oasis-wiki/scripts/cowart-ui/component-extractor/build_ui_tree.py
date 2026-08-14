from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_ui_spec import load_json, validate_spec


def canonicalize_visual(visual: object) -> dict:
    result = dict(visual) if isinstance(visual, dict) else {}
    references = []
    for reference in result.get("reference_images", []):
        item = dict(reference)
        item.setdefault("copy_visual_style", item.get("role") == "style")
        references.append(item)
    result["reference_images"] = references
    return result


def build_tree(spec: dict) -> dict:
    errors = validate_spec(spec)
    if errors:
        raise ValueError("ui-spec is invalid:\n" + "\n".join(f"- {error}" for error in errors))
    page = spec["page"]
    nodes = []
    for node in spec["nodes"]:
        item = dict(node)
        item["dynamic"] = bool(item.get("dynamic", False))
        item["bindings"] = list(item.get("bindings", []))
        nodes.append(item)
    return {
        "schema_version": 1,
        "artifact_type": "ui_tree",
        "page": {key: value for key, value in page.items() if key != "operations"},
        "operations": page.get("operations", []),
        "visual": canonicalize_visual(spec.get("visual", {})),
        "data_contract": spec.get("data_contract", []),
        "components": nodes,
        "ui_tree": {"root_id": "root", "children": [node["component_id"] for node in nodes if node["parent_id"] == "root"]},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a canonical UI Tree from a validated ui-spec.json.")
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    spec_path = args.spec.resolve()
    try:
        spec = load_json(spec_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
    try:
        tree = build_tree(spec)
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ui_tree": str(output), "components": len(tree["components"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
