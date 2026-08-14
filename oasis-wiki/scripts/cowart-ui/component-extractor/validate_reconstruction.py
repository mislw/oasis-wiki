#!/usr/bin/env python3
"""Validate clean layers, executor evidence, assembly provenance, and movement proofs."""

import argparse
import json
import sys
from pathlib import Path

from image_reconstruction_executor import UNAVAILABLE_CODE
from validate_extraction_plan import load_json, png_has_alpha, validate_plan


def _load_optional_json(value):
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    path = Path(value)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def build_report(plan, assets_dir, preview, execution_report=None, movement_report=None):
    validate_plan(plan)
    assets_dir = Path(assets_dir)
    preview = Path(preview)
    checks = []
    errors = []
    schema_three = plan.get("schema_version") == 3
    for component in plan["components"]:
        clean_layer = component.get("visual_assets", {}).get("clean_layer") if schema_three else component.get("output")
        if clean_layer is None:
            required = component.get("mode") not in {"native", "composite"}
            checks.append({"target_component_id": component["target_component_id"], "required": required, "ok": not required})
            if required:
                errors.append(f"missing clean_layer path: {component['target_component_id']}")
            continue
        asset = assets_dir / clean_layer
        ok = asset.is_file() and asset.suffix.lower() == ".png" and png_has_alpha(asset)
        checks.append({"target_component_id": component["target_component_id"], "required": True, "clean_layer": str(asset), "ok": ok})
        if not ok:
            errors.append(f"missing or non-transparent clean_layer PNG: {asset}")

    execution = _load_optional_json(execution_report)
    if schema_three:
        if not execution or execution.get("artifact_type") != "layer_reconstruction_execution" or execution.get("status") != "completed":
            errors.append(UNAVAILABLE_CODE)
        elif execution.get("capability") != "image_edit_inpainting" or not execution.get("executor_id"):
            errors.append(f"{UNAVAILABLE_CODE}: execution report lacks image_edit_inpainting capability")
        else:
            reconstructed = {
                result.get("target_component_id")
                for result in execution.get("results", [])
                if result.get("status") == "reconstructed"
            }
            required = {
                component["target_component_id"]
                for component in plan["components"]
                if component.get("mode") in {"extract_artwork", "reconstruct_skin"}
            }
            missing = sorted(required - reconstructed)
            if missing:
                errors.append(f"execution report is missing reconstructed targets: {', '.join(missing)}")

    if not preview.is_file():
        errors.append(f"missing assembly preview: {preview}")
        assembly = None
    else:
        sidecar = preview.with_suffix(preview.suffix + ".json")
        assembly = _load_optional_json(sidecar)
        if schema_three and not assembly:
            errors.append(f"missing assembly preview provenance: {sidecar}")
        elif schema_three:
            source_types = {source.get("source_type") for source in assembly.get("sources", []) if isinstance(source, dict)}
            if assembly.get("source_crop_used") is not False or "source_crop" in source_types:
                errors.append("assembly_preview used source_crop; only clean_layer and native_placeholder sources are allowed")
            forbidden = source_types - {"clean_layer", "native_placeholder"}
            if forbidden:
                errors.append(f"assembly_preview has forbidden sources: {', '.join(sorted(forbidden))}")

    movement = _load_optional_json(movement_report)
    movement_checks = None
    if movement is not None:
        movement_checks = {
            "child_move": movement.get("child_move") is True,
            "parent_move": movement.get("parent_move") is True,
        }
        if not movement_checks["child_move"]:
            errors.append("child movement residual test failed")
        if not movement_checks["parent_move"]:
            errors.append("parent movement residual test failed")

    return {
        "artifact_type": "layer_reconstruction_report" if schema_three else "reconstruction_report",
        "source": plan["source"],
        "checks": checks,
        "executor": execution,
        "preview": str(preview),
        "assembly_provenance": assembly,
        "movement_checks": movement_checks,
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
    parser.add_argument("--execution-report", type=Path)
    parser.add_argument("--movement-report", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = build_report(
            load_json(args.plan),
            args.assets_dir,
            args.preview,
            execution_report=args.execution_report,
            movement_report=args.movement_report,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    if report["errors"]:
        print("\n".join(report["errors"]), file=sys.stderr)
        return 1
    print(f"Layer reconstruction report requires visual review: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
