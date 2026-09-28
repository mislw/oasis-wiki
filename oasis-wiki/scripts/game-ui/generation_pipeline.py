from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from math import gcd
from pathlib import Path
from typing import Any, Iterable

from PIL import Image


REFERENCE_ROLES = {"style", "layout", "content", "edit-target"}
IMAGE_OPERATIONS = {"generate", "edit", "variation"}
IMAGE_MEDIA_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
MAX_SAFE_INTEGER = 9_007_199_254_740_991
TRUSTED_SOURCE_KINDS = {
    "input_image_attachment",
    "user_provided_file",
    "project_library_asset",
}
REVIEW_SOURCE_KINDS = {"html_screenshot", "browser_screenshot", "cowart_screenshot", "collage"}
PREVIEW_KEY = re.compile(r"^sha256:[0-9a-f]{64}$")
STYLE_REVIEW_CHECKS = (
    "header_language",
    "panel_language",
    "button_language",
    "border_language",
    "shadow_language",
    "title_language",
    "icon_language",
    "spacing_rhythm",
    "visual_density",
)


class GenerationPipelineError(ValueError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GenerationPipelineError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GenerationPipelineError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def require_object(value: object, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GenerationPipelineError(f"{path} must be an object")
    return value


def require_closed_object(
    value: object,
    path: str,
    required: Iterable[str],
    optional: Iterable[str] = (),
) -> dict[str, Any]:
    record = require_object(value, path)
    required_fields = set(required)
    allowed_fields = required_fields | set(optional)
    missing = sorted(required_fields - record.keys())
    if missing:
        raise GenerationPipelineError(f"{path}.{missing[0]} is required")
    extra = sorted(record.keys() - allowed_fields)
    if extra:
        raise GenerationPipelineError(
            f"{path} has undeclared fields: {', '.join(extra)}"
        )
    return record


def require_array(value: object, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise GenerationPipelineError(f"{path} must be an array")
    return value


def require_string_array(value: object, path: str) -> list[str]:
    values = require_array(value, path)
    for index, item in enumerate(values):
        if not isinstance(item, str) or not item.strip():
            raise GenerationPipelineError(
                f"{path}[{index}] must be a non-empty string"
            )
    return values


def require_nonempty_string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GenerationPipelineError(f"{path} must be a non-empty string")
    return value


def require_positive_integer(value: object, path: str) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value <= 0
        or value > MAX_SAFE_INTEGER
    ):
        raise GenerationPipelineError(f"{path} must be a positive safe integer")
    return value


def validate_aspect_ratio(value: object, path: str) -> str:
    ratio = require_nonempty_string(value, path)
    normalized_ratio = ratio.strip()
    match = re.fullmatch(r"([1-9]\d*):([1-9]\d*)", normalized_ratio)
    if match is None:
        raise GenerationPipelineError(
            f"{path} must be a reduced positive integer ratio"
        )
    try:
        width = require_positive_integer(int(match.group(1)), path)
        height = require_positive_integer(int(match.group(2)), path)
    except ValueError as exc:
        raise GenerationPipelineError(
            f"{path} must be a reduced positive integer ratio"
        ) from exc
    if gcd(width, height) != 1:
        raise GenerationPipelineError(
            f"{path} must be a reduced positive integer ratio"
        )
    return normalized_ratio


def validate_image_spec(spec_value: object) -> dict[str, Any]:
    spec = require_closed_object(
        spec_value,
        "imageSpec",
        (
            "schemaVersion",
            "operation",
            "canonicalPrompt",
            "references",
            "composition",
            "visualStyle",
            "scene",
            "exactText",
            "output",
            "preserve",
            "negativeConstraints",
            "requiredCapabilities",
            "evidence",
            "warnings",
        ),
    )
    if (
        isinstance(spec["schemaVersion"], bool)
        or not isinstance(spec["schemaVersion"], int)
        or spec["schemaVersion"] != 1
    ):
        raise GenerationPipelineError("imageSpec.schemaVersion must be 1")
    if not isinstance(spec["operation"], str) or spec["operation"] not in IMAGE_OPERATIONS:
        raise GenerationPipelineError("imageSpec.operation must be generate, edit, or variation")
    require_nonempty_string(spec["canonicalPrompt"], "imageSpec.canonicalPrompt")
    references = require_array(spec["references"], "imageSpec.references")
    for position, reference_value in enumerate(references):
        reference_path = f"imageSpec.references[{position}]"
        reference = require_closed_object(
            reference_value,
            reference_path,
            ("inputIndex", "role", "priority", "attachment"),
        )
        require_positive_integer(
            reference["inputIndex"], f"{reference_path}.inputIndex"
        )
        if not isinstance(reference["role"], str) or reference["role"] not in REFERENCE_ROLES:
            raise GenerationPipelineError(f"{reference_path}.role is invalid")
        require_positive_integer(reference["priority"], f"{reference_path}.priority")
        attachment_path = f"{reference_path}.attachment"
        attachment = require_closed_object(
            reference["attachment"],
            attachment_path,
            ("attachmentId", "mediaType", "bytes", "width", "height"),
            ("name", "originalDimensions"),
        )
        require_nonempty_string(
            attachment["attachmentId"], f"{attachment_path}.attachmentId"
        )
        if (
            not isinstance(attachment["mediaType"], str)
            or attachment["mediaType"] not in IMAGE_MEDIA_TYPES
        ):
            raise GenerationPipelineError(f"{attachment_path}.mediaType is invalid")
        for field in ("bytes", "width", "height"):
            require_positive_integer(attachment[field], f"{attachment_path}.{field}")
        if "name" in attachment:
            require_nonempty_string(attachment["name"], f"{attachment_path}.name")
        if "originalDimensions" in attachment:
            original_path = f"{attachment_path}.originalDimensions"
            original = require_closed_object(
                attachment["originalDimensions"],
                original_path,
                ("width", "height"),
            )
            require_positive_integer(original["width"], f"{original_path}.width")
            require_positive_integer(original["height"], f"{original_path}.height")
    target_count = sum(reference["role"] == "edit-target" for reference in references)
    if spec["operation"] == "edit" and target_count != 1:
        raise GenerationPipelineError(
            "edit imageSpec must contain exactly one edit-target reference"
        )
    if spec["operation"] == "variation":
        if target_count != 0:
            raise GenerationPipelineError(
                "variation imageSpec must not contain an edit-target reference"
            )
        if not any(reference["role"] == "content" for reference in references):
            raise GenerationPipelineError(
                "variation imageSpec must contain at least one content reference"
            )
    for field in (
        "composition",
        "visualStyle",
        "scene",
        "preserve",
        "negativeConstraints",
        "requiredCapabilities",
        "warnings",
    ):
        require_string_array(spec[field], f"imageSpec.{field}")
    exact_text = require_array(spec["exactText"], "imageSpec.exactText")
    for position, entry_value in enumerate(exact_text):
        entry_path = f"imageSpec.exactText[{position}]"
        entry = require_closed_object(
            entry_value,
            entry_path,
            ("text", "preserveCase"),
            ("placement",),
        )
        require_nonempty_string(entry["text"], f"{entry_path}.text")
        if "placement" in entry:
            require_nonempty_string(entry["placement"], f"{entry_path}.placement")
        if not isinstance(entry["preserveCase"], bool):
            raise GenerationPipelineError(f"{entry_path}.preserveCase must be boolean")
    output = require_closed_object(
        spec["output"],
        "imageSpec.output",
        ("transparentBackground", "count"),
        ("aspectRatio", "width", "height"),
    )
    if not isinstance(output["transparentBackground"], bool):
        raise GenerationPipelineError("imageSpec.output.transparentBackground must be boolean")
    require_positive_integer(output["count"], "imageSpec.output.count")
    has_width = "width" in output
    has_height = "height" in output
    if has_width != has_height:
        raise GenerationPipelineError(
            "imageSpec.output width and height must be supplied together"
        )
    if has_width:
        width = require_positive_integer(output["width"], "imageSpec.output.width")
        height = require_positive_integer(output["height"], "imageSpec.output.height")
    else:
        width = None
        height = None
    if "aspectRatio" in output:
        ratio = validate_aspect_ratio(output["aspectRatio"], "imageSpec.output.aspectRatio")
        if width is not None and height is not None:
            divisor = gcd(width, height)
            if ratio != f"{width // divisor}:{height // divisor}":
                raise GenerationPipelineError(
                    "imageSpec.output.aspectRatio does not match width and height"
                )
    evidence = require_array(spec["evidence"], "imageSpec.evidence")
    for position, evidence_value in enumerate(evidence):
        evidence_path = f"imageSpec.evidence[{position}]"
        item = require_closed_object(
            evidence_value,
            evidence_path,
            ("provider", "caseIds", "visualStyleTags", "sceneTags"),
            ("templateId",),
        )
        require_nonempty_string(item["provider"], f"{evidence_path}.provider")
        if "templateId" in item:
            require_nonempty_string(item["templateId"], f"{evidence_path}.templateId")
        for field in ("caseIds", "visualStyleTags", "sceneTags"):
            require_string_array(item[field], f"{evidence_path}.{field}")
    return spec


def load_prepared_image_spec(optimization_path: Path) -> dict[str, Any]:
    optimization_value = read_json(optimization_path.resolve())
    if optimization_value.get("status") != "prepared":
        raise GenerationPipelineError("image optimization result must have status prepared")
    optimization = require_closed_object(
        optimization_value,
        "imageOptimizationResult",
        ("status", "spec"),
    )
    return validate_image_spec(optimization["spec"])


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_metadata(path: Path) -> tuple[int, int, str]:
    try:
        with Image.open(path) as image:
            image_format = image.format
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
    except (OSError, ValueError) as exc:
        raise GenerationPipelineError(f"reference is not a readable image: {path}") from exc
    media_type = {
        "PNG": "image/png",
        "JPEG": "image/jpeg",
        "WEBP": "image/webp",
        "GIF": "image/gif",
    }.get(image_format or "")
    if media_type is None:
        raise GenerationPipelineError(f"reference image format is unsupported: {path}")
    return width, height, media_type


def image_size(path: Path) -> tuple[int, int]:
    width, height, _media_type = image_metadata(path)
    return width, height


def relative_file(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def normalize_reference(reference: dict[str, Any], index: int) -> dict[str, Any]:
    prefix = f"references[{index}]"
    source_value = reference.get("source")
    if not isinstance(source_value, str) or not source_value.strip():
        raise GenerationPipelineError(f"{prefix}.source is required")
    source = Path(source_value).expanduser().resolve()
    if not source.is_file():
        raise GenerationPipelineError(f"{prefix}.source is not a file: {source}")
    role = reference.get("role")
    if role not in REFERENCE_ROLES:
        raise GenerationPipelineError(f"{prefix}.role must be style, layout, content, or edit-target")
    priority = reference.get("priority")
    if isinstance(priority, bool) or not isinstance(priority, (int, float)):
        raise GenerationPipelineError(f"{prefix}.priority must be numeric")
    copy_visual_style = reference.get("copy_visual_style", role == "style")
    if not isinstance(copy_visual_style, bool):
        raise GenerationPipelineError(f"{prefix}.copy_visual_style must be boolean")
    if role == "layout" and copy_visual_style:
        raise GenerationPipelineError(f"{prefix}.copy_visual_style must be false for layout references")
    source_kind = reference.get("source_kind")
    if source_kind not in TRUSTED_SOURCE_KINDS | REVIEW_SOURCE_KINDS:
        raise GenerationPipelineError(
            f"{prefix}.source_kind must identify an input image, project library asset, or review-only screenshot source"
        )
    user_authorized = reference.get("user_authorized", False)
    if source_kind in REVIEW_SOURCE_KINDS and user_authorized is not True:
        raise GenerationPipelineError(f"{prefix}.user_authorized must be true for {source_kind}")
    width, height, media_type = image_metadata(source)
    digest = sha256_file(source)
    normalized = {
        "source": source,
        "role": role,
        "priority": priority,
        "copy_visual_style": copy_visual_style,
        "source_kind": source_kind,
        "user_authorized": bool(user_authorized),
        "width": width,
        "height": height,
        "media_type": media_type,
        "sha256": digest,
    }
    if source_kind == "project_library_asset":
        library = reference.get("library")
        if not isinstance(library, dict):
            raise GenerationPipelineError(f"{prefix}.library is required")
        asset_id = library.get("asset_id")
        preview_key = library.get("preview_key")
        source_asset = library.get("source_asset")
        if not isinstance(asset_id, str) or not asset_id:
            raise GenerationPipelineError(f"{prefix}.library.asset_id is required")
        if not isinstance(preview_key, str) or not PREVIEW_KEY.fullmatch(preview_key):
            raise GenerationPipelineError(f"{prefix}.library.preview_key is invalid")
        if preview_key != f"sha256:{digest}":
            raise GenerationPipelineError(
                f"{prefix}.library.preview_key does not match the source image"
            )
        if not isinstance(source_asset, str) or not source_asset.startswith("/"):
            raise GenerationPipelineError(f"{prefix}.library.source_asset is required")
        normalized_library = {
            "asset_id": asset_id,
            "preview_key": preview_key,
            "source_asset": source_asset,
        }
        for field in ("component_ids", "semantic_keys", "states"):
            values = library.get(field, [])
            if not isinstance(values, list) or not all(
                isinstance(value, str) for value in values
            ):
                raise GenerationPipelineError(f"{prefix}.library.{field} must be strings")
            normalized_library[field] = list(dict.fromkeys(values))
        normalized["library"] = normalized_library
    return normalized


def load_reference_inputs(
    metadata_path: Path, require_style: bool = True
) -> list[dict[str, Any]]:
    metadata = read_json(metadata_path)
    if metadata.get("schema_version") != 1:
        raise GenerationPipelineError("reference metadata schema_version must be 1")
    references = metadata.get("references")
    if not isinstance(references, list):
        raise GenerationPipelineError("reference metadata references must be an array")
    normalized = []
    for index, reference in enumerate(references):
        if not isinstance(reference, dict):
            raise GenerationPipelineError(f"references[{index}] must be an object")
        normalized.append(normalize_reference(reference, index))
    if require_style and not any(reference["role"] == "style" for reference in normalized):
        raise GenerationPipelineError("at least one style reference image is required; a style profile or prompt cannot replace it")
    return normalized


def assert_tree_reference_alignment(ui_tree: dict[str, Any], references: list[dict[str, Any]]) -> None:
    visual = ui_tree.get("visual", {})
    tree_references = visual.get("reference_images", []) if isinstance(visual, dict) else []
    if not isinstance(tree_references, list):
        raise GenerationPipelineError("ui-tree visual.reference_images must be an array")
    expected = {
        (str(reference["source"]), reference["role"], reference["priority"])
        for reference in references
        if reference["role"] in {"style", "layout"}
    }
    actual = set()
    for index, reference in enumerate(tree_references):
        if not isinstance(reference, dict):
            raise GenerationPipelineError(f"ui-tree visual.reference_images[{index}] must be an object")
        source = reference.get("source")
        if isinstance(source, str):
            source = str(Path(source).expanduser().resolve())
        actual.add((source, reference.get("role"), reference.get("priority")))
    if expected != actual:
        raise GenerationPipelineError("reference metadata must match ui-tree visual.reference_images")


def tree_reuse_component_ids(ui_tree: dict[str, Any]) -> list[str]:
    values: list[str] = []
    nodes = ui_tree.get("components")
    if not isinstance(nodes, list):
        nodes = ui_tree.get("nodes")
    if not isinstance(nodes, list):
        return values
    for node in nodes:
        if not isinstance(node, dict):
            continue
        reuse_of = node.get("reuse_of")
        if isinstance(reuse_of, str) and reuse_of and reuse_of not in values:
            values.append(reuse_of)
    return values


def validate_tree_component_reuse(
    style_profile: dict[str, Any],
    component_ids: Iterable[str],
    library_references: list[dict[str, Any]],
) -> None:
    component_map = {
        item.get("component_id"): item
        for item in style_profile.get("components", [])
        if isinstance(item, dict) and isinstance(item.get("component_id"), str)
    }
    resolved = {
        component_id
        for reference in library_references
        for component_id in (
            reference.get("library", {}).get("component_ids", [])
            if isinstance(reference.get("library"), dict)
            else []
        )
        if isinstance(component_id, str)
    }
    for component_id in component_ids:
        component = component_map.get(component_id)
        if component is None:
            continue
        if component.get("status") != "active":
            raise GenerationPipelineError(
                f"reused component is not active: {component_id}; confirm it before generation"
            )
        if component_id not in resolved:
            raise GenerationPipelineError(
                f"active reused component has no project library reference: {component_id}; "
                "resolve the component asset instead of redesigning it"
            )


def build_oasis_constraints(
    ui_tree: dict[str, Any],
    reuse_components: Iterable[str],
) -> dict[str, Any]:
    model_visible_tree = json.loads(json.dumps(ui_tree, ensure_ascii=False))
    visual = model_visible_tree.get("visual")
    if isinstance(visual, dict):
        references = visual.get("reference_images")
        if isinstance(references, list):
            for reference in references:
                if isinstance(reference, dict):
                    reference.pop("source", None)
                    reference.pop("source_kind", None)
                    reference.pop("user_authorized", None)
    return {
        "schemaVersion": 1,
        "dynamicText": True,
        "dynamicNumbers": True,
        "dynamicProgress": True,
        "hitTargets": True,
        "reusableControls": list(dict.fromkeys(reuse_components)),
        "uiTree": model_visible_tree,
        "editorWriteRestrictions": {
            "authorized": False,
            "requiresExplicitAuthorization": True,
            "prohibitedTargets": ["WidgetBlueprint", "Lua", "DataTable", ".uasset", ".umap"],
        },
        "cowartReviewStages": [
            "style_validation",
            "visual_review",
            "component_extraction",
            "component_confirmation",
        ],
    }


def compile_generation_prompt(
    image_spec: dict[str, Any],
    oasis_constraints: dict[str, Any],
) -> str:
    reusable = oasis_constraints["reusableControls"]
    tree = oasis_constraints["uiTree"]
    appendix = "\n".join(
        [
            "## Oasis UI constraints",
            "Keep runtime-dynamic text, numbers, progress, and interactive hit targets as runtime-native controls.",
            f"Reusable control IDs: {json.dumps(reusable, ensure_ascii=False)}",
            "UI Tree:",
            json.dumps(tree, ensure_ascii=False, indent=2, sort_keys=True),
            "Do not write WidgetBlueprint, Lua, DataTable, .uasset, or .umap content without explicit user authorization.",
            "Cowart review stages: style validation, visual review, component extraction, component confirmation.",
            "",
        ]
    )
    canonical_prompt = image_spec["canonicalPrompt"]
    separator = "" if canonical_prompt.endswith("\n\n") else "\n" if canonical_prompt.endswith("\n") else "\n\n"
    return canonical_prompt + separator + appendix


def build_generation_package(
    ui_tree_path: Path,
    style_profile_path: Path,
    reference_metadata_path: Path,
    optimization_path: Path,
    output_dir: Path,
    reuse_components: Iterable[str] = (),
    library_reference_metadata_path: Path | None = None,
) -> Path:
    ui_tree = read_json(ui_tree_path.resolve())
    style_profile = read_json(style_profile_path.resolve())
    image_spec = load_prepared_image_spec(optimization_path)
    if ui_tree.get("artifact_type") != "ui_tree":
        raise GenerationPipelineError("ui-tree must be produced by build_ui_tree.py")
    explicit_references = load_reference_inputs(
        reference_metadata_path.resolve(),
        require_style=False,
    )
    assert_tree_reference_alignment(ui_tree, explicit_references)
    library_references = (
        load_reference_inputs(library_reference_metadata_path.resolve(), require_style=False)
        if library_reference_metadata_path is not None
        else []
    )
    spec_references = sorted(image_spec["references"], key=lambda item: item["inputIndex"])
    if len(spec_references) != len(explicit_references):
        raise GenerationPipelineError(
            "prepared imageSpec references must match the direct-user local references"
        )
    for position, (reference, spec_reference) in enumerate(zip(explicit_references, spec_references)):
        if reference["role"] != spec_reference["role"] or reference["priority"] != spec_reference["priority"]:
            raise GenerationPipelineError(
                f"prepared imageSpec reference {position + 1} role/priority does not match local metadata"
            )
        attachment = spec_reference["attachment"]
        if (
            attachment["mediaType"] != reference["media_type"]
            or attachment["bytes"] != reference["source"].stat().st_size
            or attachment["width"] != reference["width"]
            or attachment["height"] != reference["height"]
        ):
            raise GenerationPipelineError(
                f"prepared imageSpec reference {position + 1} attachment does not match the local image"
            )
    tree_reuse_components = tree_reuse_component_ids(ui_tree)
    validate_tree_component_reuse(style_profile, tree_reuse_components, library_references)
    requested_reuse_components = list(dict.fromkeys([*reuse_components, *tree_reuse_components]))
    if image_spec["operation"] == "generate" and not any(
        reference["role"] == "style"
        for reference in [*explicit_references, *library_references]
    ):
        raise GenerationPipelineError(
            "at least one style reference image is required; a style profile or prompt cannot replace it"
        )
    output = output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise GenerationPipelineError(f"output directory must be empty: {output}")
    reference_dir = output / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)

    counters = dict.fromkeys(REFERENCE_ROLES, 0)
    manifest_items = []
    packaged_references = list(zip(explicit_references, spec_references))
    packaged_references.extend((reference, None) for reference in library_references)
    for reference, spec_reference in packaged_references:
        role = reference["role"]
        counters[role] += 1
        reference_id = f"{role}-{counters[role]:02d}"
        suffix = reference["source"].suffix.lower() or ".png"
        target = reference_dir / f"{reference_id}{suffix}"
        shutil.copy2(reference["source"], target)
        manifest_item = {
            "id": reference_id,
            "file": relative_file(target, output),
            "role": role,
            "priority": reference["priority"],
            "copy_visual_style": reference["copy_visual_style"],
            "source_kind": reference["source_kind"],
            "width": reference["width"],
            "height": reference["height"],
            "sha256": sha256_file(target),
        }
        if spec_reference is not None:
            manifest_item["input_index"] = spec_reference["inputIndex"]
            manifest_item["attachment"] = spec_reference["attachment"]
        if "library" in reference:
            manifest_item["library"] = reference["library"]
        manifest_items.append(manifest_item)
    manifest = {"schema_version": 1, "references": manifest_items}
    shutil.copy2(ui_tree_path.resolve(), output / "ui-tree.json")
    shutil.copy2(style_profile_path.resolve(), output / "style-profile.json")
    write_json(output / "reference-manifest.json", manifest)
    write_json(output / "image-spec.json", image_spec)
    oasis_constraints = build_oasis_constraints(ui_tree, requested_reuse_components)
    write_json(output / "oasis-constraints.json", oasis_constraints)
    prompt = compile_generation_prompt(image_spec, oasis_constraints)
    prompt_path = output / "generation-prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    project = style_profile.get("project", {})
    project_slug = project.get("slug", "redcliff") if isinstance(project, dict) else "redcliff"
    request = {
        "schema_version": 1,
        "artifact_type": "image_generation_request",
        "project": project_slug,
        "prompt_file": "generation-prompt.txt",
        "prompt_sha256": sha256_file(prompt_path),
        "reference_manifest": "reference-manifest.json",
        "image_spec": "image-spec.json",
        "oasis_constraints": "oasis-constraints.json",
        "reference_files": [item["file"] for item in manifest_items],
        "style_references": [item["file"] for item in manifest_items if item["role"] == "style"],
        "layout_references": [item["file"] for item in manifest_items if item["role"] == "layout"],
        "required_capabilities": image_spec["requiredCapabilities"],
        "required_capability": "codex_builtin_image_gen",
        "generation_backend": "codex_builtin",
        "tool": "image_gen",
        "credential_mode": "codex_managed",
        "fallback_policy": "forbid_html_screenshot",
        "status": "ready_for_image_generation",
    }
    write_json(output / "generation-request.json", request)
    validate_generation_package(output)
    return output


def validate_generation_package(package_dir: Path) -> dict[str, Any]:
    package = package_dir.resolve()
    required = (
        "reference-manifest.json",
        "ui-tree.json",
        "style-profile.json",
        "image-spec.json",
        "oasis-constraints.json",
        "generation-prompt.txt",
        "generation-request.json",
    )
    for name in required:
        if not (package / name).is_file():
            raise GenerationPipelineError(f"missing {name}")
    manifest = read_json(package / "reference-manifest.json")
    image_spec = validate_image_spec(read_json(package / "image-spec.json"))
    oasis_constraints = read_json(package / "oasis-constraints.json")
    request = read_json(package / "generation-request.json")
    references = manifest.get("references")
    if manifest.get("schema_version") != 1 or not isinstance(references, list):
        raise GenerationPipelineError("reference-manifest.json is invalid")
    if image_spec["operation"] == "generate" and not any(
        item.get("role") == "style" for item in references if isinstance(item, dict)
    ):
        raise GenerationPipelineError("at least one style reference image is required")
    for index, item in enumerate(references):
        if not isinstance(item, dict):
            raise GenerationPipelineError(f"reference-manifest references[{index}] must be an object")
        if item.get("role") not in REFERENCE_ROLES:
            raise GenerationPipelineError(f"reference-manifest references[{index}].role is invalid")
        if item.get("role") == "layout" and item.get("copy_visual_style") is not False:
            raise GenerationPipelineError("layout references must set copy_visual_style to false")
        image_path = package / str(item.get("file", ""))
        if not image_path.is_file():
            raise GenerationPipelineError(f"missing reference image: {item.get('file')}")
        width, height = image_size(image_path)
        if item.get("width") != width or item.get("height") != height:
            raise GenerationPipelineError(f"reference dimensions do not match: {item.get('file')}")
        if item.get("sha256") != sha256_file(image_path):
            raise GenerationPipelineError(f"reference sha256 does not match: {item.get('file')}")
        if item.get("source_kind") == "project_library_asset":
            library = item.get("library")
            if not isinstance(library, dict):
                raise GenerationPipelineError("project library reference is missing provenance")
            if not isinstance(library.get("asset_id"), str) or not library["asset_id"]:
                raise GenerationPipelineError("project library asset_id is missing")
            if not isinstance(library.get("source_asset"), str) or not library[
                "source_asset"
            ].startswith("/"):
                raise GenerationPipelineError("project library source_asset is missing")
            for field in ("component_ids", "semantic_keys", "states"):
                values = library.get(field)
                if not isinstance(values, list) or not all(
                    isinstance(value, str) for value in values
                ):
                    raise GenerationPipelineError(
                        f"project library {field} must be an array of strings"
                    )
            if library.get("preview_key") != f"sha256:{item.get('sha256')}":
                raise GenerationPipelineError("project library preview_key does not match")
    direct_references = []
    for index, item in enumerate(references):
        has_input_index = "input_index" in item
        has_attachment = "attachment" in item
        if has_input_index != has_attachment:
            raise GenerationPipelineError(
                f"reference-manifest references[{index}] must pair input_index and attachment"
            )
        if has_input_index:
            direct_references.append(item)
        elif item.get("source_kind") != "project_library_asset":
            raise GenerationPipelineError(
                f"reference-manifest references[{index}] outside image-spec.json must be a project library asset"
            )
    spec_references = sorted(
        image_spec["references"],
        key=lambda item: (
            item["inputIndex"],
            item["role"],
            item["priority"],
            json.dumps(item["attachment"], sort_keys=True),
        ),
    )
    direct_references.sort(
        key=lambda item: (
            item.get("input_index"),
            item.get("role"),
            item.get("priority"),
            json.dumps(item.get("attachment"), sort_keys=True),
        )
    )
    if len(spec_references) != len(direct_references):
        raise GenerationPipelineError("image-spec.json references do not match reference-manifest.json")
    for index, (item, spec_reference) in enumerate(
        zip(direct_references, spec_references)
    ):
        if item.get("input_index") != spec_reference["inputIndex"]:
            raise GenerationPipelineError(f"reference-manifest references[{index}].input_index does not match")
        if item.get("role") != spec_reference["role"] or item.get("priority") != spec_reference["priority"]:
            raise GenerationPipelineError(f"reference-manifest references[{index}] role/priority does not match")
        if item.get("attachment") != spec_reference["attachment"]:
            raise GenerationPipelineError(f"reference-manifest references[{index}].attachment does not match")
    expected_constraints = build_oasis_constraints(
        read_json(package / "ui-tree.json"),
        require_string_array(
            oasis_constraints.get("reusableControls"),
            "oasisConstraints.reusableControls",
        ),
    )
    if oasis_constraints != expected_constraints:
        raise GenerationPipelineError("oasis-constraints.json is invalid")
    prompt_path = package / str(request.get("prompt_file", ""))
    if not prompt_path.is_file() or request.get("prompt_sha256") != sha256_file(prompt_path):
        raise GenerationPipelineError("generation prompt is missing or its sha256 does not match")
    expected_prompt = compile_generation_prompt(image_spec, oasis_constraints)
    if prompt_path.read_text(encoding="utf-8") != expected_prompt:
        raise GenerationPipelineError("generation prompt does not match image-spec.json and oasis-constraints.json")
    style_files = [item["file"] for item in references if item.get("role") == "style"]
    layout_files = [item["file"] for item in references if item.get("role") == "layout"]
    if request.get("style_references") != style_files or request.get("layout_references") != layout_files:
        raise GenerationPipelineError("generation request reference lists do not match reference-manifest.json")
    reference_files = [item["file"] for item in references]
    if request.get("reference_files") != reference_files:
        raise GenerationPipelineError("generation request reference_files do not match reference-manifest.json")
    if request.get("image_spec") != "image-spec.json":
        raise GenerationPipelineError("generation request must reference image-spec.json")
    if request.get("oasis_constraints") != "oasis-constraints.json":
        raise GenerationPipelineError("generation request must reference oasis-constraints.json")
    if request.get("required_capabilities") != image_spec["requiredCapabilities"]:
        raise GenerationPipelineError("generation request required_capabilities do not match image-spec.json")
    if request.get("required_capability") != "codex_builtin_image_gen":
        raise GenerationPipelineError("generation request must require the Codex built-in image_gen tool")
    if request.get("generation_backend") != "codex_builtin" or request.get("tool") != "image_gen":
        raise GenerationPipelineError("generation request must use the Codex built-in image_gen backend")
    if request.get("credential_mode") != "codex_managed":
        raise GenerationPipelineError("generation request credentials must be managed by Codex")
    if request.get("fallback_policy") != "forbid_html_screenshot":
        raise GenerationPipelineError("generation request must forbid HTML screenshot fallback")
    return {
        "package": package,
        "manifest": manifest,
        "request": request,
        "image_spec": image_spec,
        "oasis_constraints": oasis_constraints,
    }


def record_generation_result(
    package_dir: Path,
    output_image: Path,
    generated_at: str | None = None,
    generation_backend: str | None = None,
    model: str | None = None,
) -> Path:
    context = validate_generation_package(package_dir)
    package = context["package"]
    source = output_image.resolve()
    if not source.is_file():
        raise GenerationPipelineError(f"generated output image does not exist: {source}")
    image_size(source)
    outputs = package / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    target = outputs / f"generated-ui{source.suffix.lower() or '.png'}"
    shutil.copy2(source, target)
    request = context["request"]
    result = {
        "schema_version": 1,
        "status": "generated",
        "output_image": relative_file(target, package),
        "output_sha256": sha256_file(target),
        "references_used": request["reference_files"],
        "prompt_sha256": request["prompt_sha256"],
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
    }
    if generation_backend:
        result["generation_backend"] = generation_backend
    if model:
        result["model"] = model
    result_path = package / "generation-result.json"
    write_json(result_path, result)
    return result_path


def validate_generation_result(package_dir: Path, expected_image: Path | None = None) -> dict[str, Any]:
    context = validate_generation_package(package_dir)
    package = context["package"]
    result_path = package / "generation-result.json"
    if not result_path.is_file():
        raise GenerationPipelineError("missing generation-result.json")
    result = read_json(result_path)
    if result.get("schema_version") != 1 or result.get("status") != "generated":
        raise GenerationPipelineError("generation-result.json must record status generated")
    output = package / str(result.get("output_image", ""))
    if not output.is_file():
        raise GenerationPipelineError("generation result output image is missing")
    image_size(output)
    if result.get("output_sha256") != sha256_file(output):
        raise GenerationPipelineError("generation result output sha256 does not match")
    request = context["request"]
    expected_references = request["reference_files"]
    if result.get("references_used") != expected_references:
        raise GenerationPipelineError("generation result references_used does not match the request")
    if result.get("prompt_sha256") != request["prompt_sha256"]:
        raise GenerationPipelineError("generation result prompt_sha256 does not match the request")
    if expected_image is not None and sha256_file(expected_image.resolve()) != result["output_sha256"]:
        raise GenerationPipelineError("Cowart candidate image does not match generation-result.json")
    return {**context, "result": result, "output": output}


def create_style_review(package_dir: Path) -> Path:
    context = validate_generation_result(package_dir)
    package = context["package"]
    review = {
        "schema_version": 1,
        "status": "pending_developer_review",
        "generated_image": context["result"]["output_image"],
        "style_references": context["request"]["style_references"],
        "checks": {name: "pending_comparison" for name in STYLE_REVIEW_CHECKS},
        "measurement": "qualitative_review_only",
    }
    review_path = package / "style-review.json"
    write_json(review_path, review)
    return review_path
