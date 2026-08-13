#!/usr/bin/env python3
"""Create provider-neutral image-reconstruction jobs in hierarchy order."""

import argparse
import json
import re
import sys
from pathlib import Path

from validate_extraction_plan import load_json, validate_plan


def instruction_for(component):
    if component["mode"] == "reconstruct_skin":
        return (
            "Reconstruct the clean layer from its source crop. Remove the union mask for all listed descendants, "
            "including native text, icons, artwork, shadows, and occluded pixels. Repair the removed regions with "
            "semantically consistent background, border, material, lighting, and texture. Do not return a crop, "
            "transparent hole, flat fill, HTML/CSS render, canvas paint, or browser screenshot."
        )
    return (
        "Extract only the named artwork as a transparent independent layer. Remove panel, card, text, badge, and "
        "button framing, preserve the complete silhouette and occluded edges, and do not return a rectangular crop."
    )


def filename(target):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", target) + ".json"


def build_jobs(plan):
    validate_plan(plan)
    components = {component["target_component_id"]: component for component in plan["components"]}
    order = plan.get("reconstruction_order", [component["target_component_id"] for component in plan["components"]])
    jobs = []
    for sequence, target in enumerate(order):
        component = components[target]
        if component["mode"] not in {"extract_artwork", "reconstruct_skin"}:
            continue
        reconstruction = component.get("layer_reconstruction", {})
        jobs.append({
            "schema_version": 1,
            "artifact_type": "layer_reconstruction_job",
            "target_component_id": target,
            "sequence": sequence,
            "category": component["category"],
            "mode": component["mode"],
            "source_image": plan["source"]["image"],
            "source_crop": component.get("visual_assets", {}).get("source_crop"),
            "instances": component["instances"],
            "remove_nodes": reconstruction.get("remove_nodes", component.get("remove_content", [])),
            "mask": reconstruction.get("mask"),
            "depends_on": reconstruction.get("depends_on", []),
            "transparent": True,
            "evaluate_nine_slice": component["evaluate_nine_slice"],
            "output": component["output"],
            "executor": {"required_capability": "image_edit_inpainting", "provider": None},
            "instruction": instruction_for(component),
            "status": "job_created",
            "error": None,
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
    print(f"Wrote {len(jobs)} layer reconstruction job(s): {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
