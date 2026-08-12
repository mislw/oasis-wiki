#!/usr/bin/env python3
"""Report whether reconstructed assets are complete and await visual review."""

import argparse
import json
import sys
from pathlib import Path

from validate_extraction_plan import load_json, png_has_alpha, validate_plan


def build_report(plan, assets_dir, preview):
    validate_plan(plan)
    checks = []
    errors = []
    for component in plan["components"]:
        output = component["output"]
        if output is None:
            checks.append({"target_component_id": component["target_component_id"], "required": False, "ok": True})
            continue
        asset = Path(assets_dir) / output
        ok = asset.is_file() and asset.suffix.lower() == ".png" and png_has_alpha(asset)
        checks.append({"target_component_id": component["target_component_id"], "required": True, "asset": str(asset), "ok": ok})
        if not ok:
            errors.append(f"missing or non-transparent PNG: {asset}")
    if not Path(preview).is_file():
        errors.append(f"missing recomposed preview: {preview}")
    return {
        "artifact_type": "reconstruction_report",
        "source": plan["source"],
        "checks": checks,
        "preview": str(preview),
        "visual_similarity": None,
        "visual_review_required": True,
        "status": "pending_review" if not errors else "incomplete",
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--assets-dir", required=True, type=Path)
    parser.add_argument("--preview", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = build_report(load_json(args.plan), args.assets_dir, args.preview)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    if report["errors"]:
        print("\n".join(report["errors"]), file=sys.stderr)
        return 1
    print(f"Reconstruction report requires visual review: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
