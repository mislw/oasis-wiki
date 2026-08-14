from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from PIL import Image


REFERENCE_ROLES = {"style", "layout"}
TRUSTED_SOURCE_KINDS = {"input_image_attachment", "user_provided_file"}
REVIEW_SOURCE_KINDS = {"html_screenshot", "browser_screenshot", "cowart_screenshot", "collage"}
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            return image.size
    except (OSError, ValueError) as exc:
        raise GenerationPipelineError(f"reference is not a readable image: {path}") from exc


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
        raise GenerationPipelineError(f"{prefix}.role must be style or layout")
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
            f"{prefix}.source_kind must identify an input_image_attachment, user_provided_file, or review-only screenshot source"
        )
    user_authorized = reference.get("user_authorized", False)
    if source_kind in REVIEW_SOURCE_KINDS and user_authorized is not True:
        raise GenerationPipelineError(f"{prefix}.user_authorized must be true for {source_kind}")
    width, height = image_size(source)
    return {
        "source": source,
        "role": role,
        "priority": priority,
        "copy_visual_style": copy_visual_style,
        "source_kind": source_kind,
        "user_authorized": bool(user_authorized),
        "width": width,
        "height": height,
        "sha256": sha256_file(source),
    }


def load_reference_inputs(metadata_path: Path) -> list[dict[str, Any]]:
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
    if not any(reference["role"] == "style" for reference in normalized):
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


def compile_generation_prompt(
    style_profile: dict[str, Any],
    ui_tree: dict[str, Any],
    reference_manifest: dict[str, Any],
    page_purpose: str = "",
    reuse_components: Iterable[str] = (),
) -> str:
    project = style_profile.get("project", {})
    project_name = project.get("name", "RedCliff") if isinstance(project, dict) else "RedCliff"
    style_guide = style_profile.get("style_guide", {})
    components = style_profile.get("components", [])
    requested_ids = list(dict.fromkeys(reuse_components))
    component_map = {
        item.get("component_id"): item
        for item in components
        if isinstance(item, dict) and isinstance(item.get("component_id"), str)
    }
    existing_components = [component_map[component_id] for component_id in requested_ids if component_id in component_map]
    references = reference_manifest.get("references", [])
    style_references = [item for item in references if item.get("role") == "style"]
    layout_references = [item for item in references if item.get("role") == "layout"]
    native_components = [item for item in ui_tree.get("components", []) if item.get("asset_policy") == "native"]
    bitmap_components = [item for item in ui_tree.get("components", []) if item.get("asset_policy") != "native"]
    purpose = page_purpose.strip() or str(ui_tree.get("page", {}).get("purpose", ""))

    def dump(value: object) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)

    return "\n".join(
        [
            "PROJECT",
            str(project_name),
            "",
            "STYLE REFERENCES",
            "These images define the visual language.",
            "Treat them as UI from the same game, same art team and same design system.",
            dump(style_references),
            "",
            "LAYOUT REFERENCES",
            "These images define only:",
            "- information hierarchy",
            "- approximate placement",
            "- required content",
            "Do NOT copy their visual style.",
            dump(layout_references),
            "",
            "STYLE PROFILE",
            "The profile is supplementary and must not replace the STYLE reference images.",
            dump(style_guide),
            "",
            "EXISTING COMPONENTS",
            dump(existing_components),
            "",
            "UI TREE",
            dump(ui_tree),
            "",
            "LAYOUT REQUIREMENTS",
            purpose,
            "",
            "NATIVE / BITMAP BOUNDARIES",
            "Keep text, counters, values, progress, and interactive hit targets as native controls.",
            "Native controls:",
            dump(native_components),
            "Bitmap/layer artwork:",
            dump(bitmap_components),
            "",
            "VISUAL MATCH REQUIREMENTS",
            "Same game.",
            "Same art team.",
            "Same UI design system.",
            "Match the STYLE reference images in:",
            "- panel geometry",
            "- border thickness",
            "- corner treatment",
            "- bevel",
            "- highlight",
            "- shadow",
            "- material",
            "- title rendering",
            "- button rendering",
            "- icon rendering",
            "- spacing rhythm",
            "- visual density",
            "Reuse existing RedCliff component language wherever applicable.",
            "",
            "NEGATIVE CONSTRAINTS",
            "Do not produce:",
            "- generic mobile shop UI",
            "- generic fantasy UI",
            "- modern flat UI",
            "- web dashboard styling",
            "- simplified CSS-like controls",
            "Layout reference controls hierarchy only.",
            "Do not inherit visual styling from layout references.",
            "Do not use HTML/CSS/Chromium screenshots as final game UI artwork.",
            "",
        ]
    )


def build_generation_package(
    ui_tree_path: Path,
    style_profile_path: Path,
    reference_metadata_path: Path,
    output_dir: Path,
    page_purpose: str = "",
    reuse_components: Iterable[str] = (),
) -> Path:
    ui_tree = read_json(ui_tree_path.resolve())
    style_profile = read_json(style_profile_path.resolve())
    if ui_tree.get("artifact_type") != "ui_tree":
        raise GenerationPipelineError("ui-tree must be produced by build_ui_tree.py")
    references = load_reference_inputs(reference_metadata_path.resolve())
    assert_tree_reference_alignment(ui_tree, references)
    output = output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise GenerationPipelineError(f"output directory must be empty: {output}")
    reference_dir = output / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)

    counters = {"style": 0, "layout": 0}
    manifest_items = []
    for reference in references:
        role = reference["role"]
        counters[role] += 1
        reference_id = f"{role}-{counters[role]:02d}"
        suffix = reference["source"].suffix.lower() or ".png"
        target = reference_dir / f"{reference_id}{suffix}"
        shutil.copy2(reference["source"], target)
        manifest_items.append(
            {
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
        )
    manifest = {"schema_version": 1, "references": manifest_items}
    shutil.copy2(ui_tree_path.resolve(), output / "ui-tree.json")
    shutil.copy2(style_profile_path.resolve(), output / "style-profile.json")
    write_json(output / "reference-manifest.json", manifest)
    prompt = compile_generation_prompt(style_profile, ui_tree, manifest, page_purpose, reuse_components)
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
        "style_references": [item["file"] for item in manifest_items if item["role"] == "style"],
        "layout_references": [item["file"] for item in manifest_items if item["role"] == "layout"],
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
        "generation-prompt.txt",
        "generation-request.json",
    )
    for name in required:
        if not (package / name).is_file():
            raise GenerationPipelineError(f"missing {name}")
    manifest = read_json(package / "reference-manifest.json")
    request = read_json(package / "generation-request.json")
    references = manifest.get("references")
    if manifest.get("schema_version") != 1 or not isinstance(references, list):
        raise GenerationPipelineError("reference-manifest.json is invalid")
    if not any(item.get("role") == "style" for item in references if isinstance(item, dict)):
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
    prompt_path = package / str(request.get("prompt_file", ""))
    if not prompt_path.is_file() or request.get("prompt_sha256") != sha256_file(prompt_path):
        raise GenerationPipelineError("generation prompt is missing or its sha256 does not match")
    style_files = [item["file"] for item in references if item.get("role") == "style"]
    layout_files = [item["file"] for item in references if item.get("role") == "layout"]
    if request.get("style_references") != style_files or request.get("layout_references") != layout_files:
        raise GenerationPipelineError("generation request reference lists do not match reference-manifest.json")
    if request.get("required_capability") != "codex_builtin_image_gen":
        raise GenerationPipelineError("generation request must require the Codex built-in image_gen tool")
    if request.get("generation_backend") != "codex_builtin" or request.get("tool") != "image_gen":
        raise GenerationPipelineError("generation request must use the Codex built-in image_gen backend")
    if request.get("credential_mode") != "codex_managed":
        raise GenerationPipelineError("generation request credentials must be managed by Codex")
    if request.get("fallback_policy") != "forbid_html_screenshot":
        raise GenerationPipelineError("generation request must forbid HTML screenshot fallback")
    return {"package": package, "manifest": manifest, "request": request}


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
        "references_used": [*request["style_references"], *request["layout_references"]],
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
    expected_references = [*request["style_references"], *request["layout_references"]]
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
