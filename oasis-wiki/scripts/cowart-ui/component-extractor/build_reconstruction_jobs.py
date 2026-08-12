#!/usr/bin/env python3
"""Create one image-edit instruction file per reusable artwork or skin target."""

import argparse
import json
import re
import sys
from pathlib import Path

from validate_extraction_plan import load_json, validate_plan


def instruction_for(component):
    if component["mode"] == "reconstruct_skin":
        return (
            "Use every equivalent source instance. Remove baked dynamic content: "
            f"{', '.join(component['remove_content']) or 'none'}. Preserve border, material, gradient, highlight, "
            "shadow, and corner proportions. Repair obscured regions. Output a text-free, dynamic-icon-free transparent PNG."
        )
    return (
        "Keep only the named artwork. Remove panel, card, text, badge, and button framing. Preserve silhouette, "
        "material, lighting, and proportion. Repair occluded edges and output a transparent PNG."
    )


def filename(target):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", target) + ".json"


def build_jobs(plan):
    validate_plan(plan)
    jobs = []
    for component in plan["components"]:
        if component["mode"] not in {"extract_artwork", "reconstruct_skin"}:
            continue
        jobs.append({
            "artifact_type": "reconstruction_job",
            "target_component_id": component["target_component_id"],
            "category": component["category"],
            "mode": component["mode"],
            "source_image": plan["source"]["image"],
            "instances": component["instances"],
            "remove_content": component["remove_content"],
            "transparent": True,
            "evaluate_nine_slice": component["evaluate_nine_slice"],
            "output": component["output"],
            "instruction": instruction_for(component),
            "status": "pending_ai_edit",
        })
    return jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        jobs = build_jobs(load_json(args.plan))
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for job in jobs:
            (args.output_dir / filename(job["target_component_id"])).write_text(
                json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Wrote {len(jobs)} reconstruction job(s): {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
