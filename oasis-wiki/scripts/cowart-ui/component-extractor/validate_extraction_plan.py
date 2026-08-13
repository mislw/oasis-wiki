#!/usr/bin/env python3
"""Validate deterministic extraction and layer-reconstruction plans."""

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

from component_semantics import NODE_KINDS, RECONSTRUCTION_STATUSES, RENDER_MODES


VALID_MODES = {"native", "extract_artwork", "reconstruct_skin", "composite"}
VALID_STATUSES = {"candidate", "pending_review"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _is_relative_png(path):
    if not isinstance(path, str) or not path.endswith(".png"):
        return False
    candidate = PurePosixPath(path.replace("\\", "/"))
    return not candidate.is_absolute() and ".." not in candidate.parts


def _valid_bounds(bounds, page_size):
    if not isinstance(bounds, dict):
        return False
    values = [bounds.get(key) for key in ("x", "y", "width", "height")]
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in values):
        return False
    x, y, width, height = values
    return x >= 0 and y >= 0 and width > 0 and height > 0 and x + width <= page_size["width"] and y + height <= page_size["height"]


def _validate_schema_three_component(component, prefix, mode, output, errors):
    visual_assets = component.get("visual_assets")
    if not isinstance(visual_assets, dict):
        errors.append(f"{prefix}.visual_assets is required")
        return
    if set(visual_assets) != {"source_crop", "clean_layer", "assembly_preview"}:
        errors.append(f"{prefix}.visual_assets must contain only source_crop, clean_layer, and assembly_preview")
    clean_layer = visual_assets.get("clean_layer")
    if clean_layer != output:
        errors.append(f"{prefix}.output must equal visual_assets.clean_layer")

    reconstruction = component.get("layer_reconstruction")
    if not isinstance(reconstruction, dict):
        errors.append(f"{prefix}.layer_reconstruction is required")
        return
    if reconstruction.get("status") not in RECONSTRUCTION_STATUSES:
        errors.append(f"{prefix}.layer_reconstruction.status is invalid")
    if mode == "native":
        if clean_layer is not None:
            errors.append(f"{prefix}.native must keep clean_layer null")
        if reconstruction.get("status") != "not_applicable":
            errors.append(f"{prefix}.native layer reconstruction must be not_applicable")
        return
    if mode in {"extract_artwork", "reconstruct_skin"}:
        if not _is_relative_png(clean_layer):
            errors.append(f"{prefix}.clean_layer must be a relative PNG path")
        if reconstruction.get("method") != "image_reconstruction":
            errors.append(f"{prefix}.layer_reconstruction.method must be image_reconstruction")
        mask = reconstruction.get("mask")
        if not isinstance(mask, dict) or mask.get("operation") != "union" or mask.get("deduplicate_pixels") is not True:
            errors.append(f"{prefix}.layer_reconstruction.mask must use a deduplicating union")
        if mode == "reconstruct_skin" and not component.get("source_content_clean") and not reconstruction.get("remove_nodes") and not component.get("remove_content") and component.get("target_component_id") != "background.root":
            errors.append(f"{prefix}.reconstruct_skin requires descendant removal unless source_content_clean is true")


def validation_errors(plan):
    errors = []
    if not isinstance(plan, dict):
        return ["plan must be a JSON object"]
    schema_version = plan.get("schema_version")
    if schema_version not in (1, 2, 3):
        errors.append("schema_version must be 1, 2, or 3")
    expected_artifact = "layer_reconstruction_plan" if schema_version == 3 else "extraction_plan"
    if plan.get("artifact_type") != expected_artifact:
        errors.append(f"artifact_type must be {expected_artifact}")

    source = plan.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
        return errors
    if not isinstance(source.get("image"), str) or not source["image"]:
        errors.append("source.image is required")
    if not isinstance(source.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
        errors.append("source.sha256 must be a lowercase SHA-256 digest")
    page_size = source.get("page_size")
    if not isinstance(page_size, dict) or any(not isinstance(page_size.get(key), int) or page_size[key] <= 0 for key in ("width", "height")):
        errors.append("source.page_size must contain positive width and height")
        return errors

    components = plan.get("components")
    if not isinstance(components, list):
        return errors + ["components must be an array"]
    seen_targets = set()
    for index, component in enumerate(components):
        prefix = f"components[{index}]"
        if not isinstance(component, dict):
            errors.append(f"{prefix} must be an object")
            continue
        target = component.get("target_component_id")
        if not isinstance(target, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", target):
            errors.append(f"{prefix}.target_component_id is invalid")
        elif target in seen_targets:
            errors.append(f"{prefix}.target_component_id must be unique")
        else:
            seen_targets.add(target)

        mode = component.get("mode")
        if mode not in VALID_MODES:
            errors.append(f"{prefix}.mode must be one of {sorted(VALID_MODES)}")
        if component.get("status") not in VALID_STATUSES:
            errors.append(f"{prefix}.status must be candidate or pending_review")
        if schema_version in {2, 3}:
            if component.get("node_kind") not in NODE_KINDS:
                errors.append(f"{prefix}.node_kind is invalid")
            if component.get("render_mode") not in RENDER_MODES:
                errors.append(f"{prefix}.render_mode is invalid")
        confidence = component.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            errors.append(f"{prefix}.confidence must be between 0 and 1")

        instances = component.get("instances")
        if not isinstance(instances, list) or not instances:
            errors.append(f"{prefix}.instances must be a non-empty array")
        else:
            for instance_index, instance in enumerate(instances):
                if not isinstance(instance, dict) or not isinstance(instance.get("node_id"), str) or not _valid_bounds(instance.get("bounds"), page_size):
                    errors.append(f"{prefix}.instances[{instance_index}] has invalid bounds")

        output = component.get("output")
        if mode in {"native", "composite"} and output is not None:
            errors.append(f"{prefix}.{mode} must not have bitmap output")
        if mode in {"extract_artwork", "reconstruct_skin"}:
            if not _is_relative_png(output):
                errors.append(f"{prefix}.{mode} output must be a relative PNG path")
            if component.get("transparent") is not True:
                errors.append(f"{prefix}.{mode} must require transparent output")
        if schema_version == 3:
            _validate_schema_three_component(component, prefix, mode, output, errors)
        elif mode == "reconstruct_skin" and not component.get("source_content_clean") and not component.get("remove_content"):
            errors.append(f"{prefix}.reconstruct_skin requires remove_content unless source_content_clean is true")

    if schema_version == 3:
        order = plan.get("reconstruction_order")
        if not isinstance(order, list) or set(order) != seen_targets or len(order) != len(seen_targets):
            errors.append("reconstruction_order must contain each target exactly once")
        else:
            positions = {target: index for index, target in enumerate(order)}
            for component in components:
                target = component.get("target_component_id")
                reconstruction = component.get("layer_reconstruction", {})
                for dependency in reconstruction.get("depends_on", []):
                    if dependency not in positions or positions[dependency] >= positions[target]:
                        errors.append(f"{target} dependency {dependency} must appear earlier in reconstruction_order")
    return errors


def validate_plan(plan):
    errors = validation_errors(plan)
    if errors:
        raise ValueError("\n".join(errors))
    return plan


def png_has_alpha(path):
    data = Path(path).read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        return False
    offset = len(PNG_SIGNATURE)
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset:offset + 4], "big")
        chunk_type = data[offset + 4:offset + 8]
        chunk_data = data[offset + 8:offset + 8 + length]
        if chunk_type == b"IHDR" and len(chunk_data) >= 10:
            return chunk_data[9] in {4, 6}
        if chunk_type == b"tRNS":
            return True
        offset += 12 + length
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    args = parser.parse_args()
    try:
        validate_plan(load_json(args.plan))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Layer reconstruction plan is valid: {args.plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
