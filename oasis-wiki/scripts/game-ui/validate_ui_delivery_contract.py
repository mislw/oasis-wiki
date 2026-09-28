#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_file(value, field: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{field} is required")
        return None
    path = Path(value).resolve()
    if not path.is_file():
        errors.append(f"{field} does not exist: {path}")
        return None
    return path


def validate_hash(path: Path | None, expected, field: str, errors: list[str]) -> None:
    if path is None:
        return
    if not isinstance(expected, str) or sha256_file(path).lower() != expected.lower():
        errors.append(f"{field} is stale")


def is_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def widget_map(snapshot: dict) -> dict[str, dict]:
    widgets = snapshot.get("widgets", [])
    if not isinstance(widgets, list):
        return {}
    return {
        widget.get("name"): widget
        for widget in widgets
        if isinstance(widget, dict) and isinstance(widget.get("name"), str)
    }


def validate_contract(contract_path: Path) -> dict:
    contract_path = contract_path.resolve()
    contract = read_json(contract_path)
    errors: list[str] = []
    warnings: list[str] = []

    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if contract.get("artifact_type") != "ui_delivery_contract":
        errors.append("artifact_type must be ui_delivery_contract")

    project = contract.get("project", {})
    outputs = contract.get("outputs", {})
    project_root_value = project.get("root") if isinstance(project, dict) else None
    output_root_value = outputs.get("root") if isinstance(outputs, dict) else None
    if not isinstance(project_root_value, str) or not project_root_value:
        errors.append("project.root is required")
        project_root = None
    else:
        project_root = Path(project_root_value).resolve()
    if not isinstance(output_root_value, str) or not output_root_value:
        errors.append("outputs.root is required")
    elif project_root is not None and is_inside(Path(output_root_value), project_root):
        errors.append("outputs.root must be outside project.root")

    visual = contract.get("visual", {})
    if not isinstance(visual, dict) or visual.get("status") != "approved":
        errors.append("visual.status must be approved")
    else:
        visual_path = resolve_file(visual.get("path"), "visual.path", errors)
        validate_hash(visual_path, visual.get("sha256"), "visual.sha256", errors)
        if visual_path is not None:
            with Image.open(visual_path) as image:
                if [image.width, image.height] != [visual.get("width"), visual.get("height")]:
                    errors.append("visual dimensions do not match the approved file")

    layout = contract.get("layout", {})
    if not isinstance(layout, dict):
        errors.append("layout is required")
    else:
        session_path = resolve_file(layout.get("session_path"), "layout.session_path", errors)
        validate_hash(session_path, layout.get("session_sha256"), "layout.session_sha256", errors)
        review_path = resolve_file(
            layout.get("layout_review_path"), "layout.layout_review_path", errors
        )
        validate_hash(
            review_path,
            layout.get("layout_review_sha256"),
            "layout.layout_review_sha256",
            errors,
        )
        if review_path is not None and session_path is not None:
            review = read_json(review_path)
            if review.get("artifact_type") != "ui_layout_review":
                errors.append("layout review artifact_type is invalid")
            if review.get("schema_version") != 1:
                errors.append("layout review schema_version is invalid")
            if review.get("status") != "pending_chat_confirmation":
                errors.append("layout review status must be pending_chat_confirmation")
            source = review.get("source", {})
            if not isinstance(source, dict) or source.get("session_sha256", "").lower() != sha256_file(
                session_path
            ).lower():
                errors.append("layout review source.session_sha256 is stale")

    target = contract.get("target", {})
    snapshot = None
    if not isinstance(target, dict):
        errors.append("target is required")
    else:
        load_path = target.get("load_path")
        if not isinstance(load_path, str) or not load_path.startswith("/") or "." not in load_path:
            errors.append("target.load_path must be an exact object load path")
        snapshot_path = resolve_file(
            target.get("snapshot_path"), "target.snapshot_path", errors
        )
        validate_hash(
            snapshot_path,
            target.get("snapshot_sha256"),
            "target.snapshot_sha256",
            errors,
        )
        if snapshot_path is not None:
            try:
                snapshot = read_json(snapshot_path)
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"target snapshot is invalid: {exc}")

    if isinstance(snapshot, dict) and isinstance(target, dict):
        expected_root = target.get("root", {})
        actual_root = snapshot.get("root", {})
        if not isinstance(expected_root, dict) or not isinstance(actual_root, dict):
            errors.append("target root evidence is missing")
        else:
            if actual_root.get("name") != expected_root.get("name"):
                errors.append("target root name does not match")
            if actual_root.get("size") != expected_root.get("size"):
                errors.append("target root size does not match")
            if actual_root.get("coordinate_space") != expected_root.get("coordinate_space"):
                errors.append("target root coordinate_space does not match")

        widgets = widget_map(snapshot)
        for requirement in target.get("required_controls", []):
            if not isinstance(requirement, dict):
                continue
            name = requirement.get("name")
            widget = widgets.get(name)
            if widget is None:
                errors.append(f"required control is missing: {name}")
                continue
            if widget.get("class") != requirement.get("class"):
                errors.append(f"{name} class does not match")
            if requirement.get("require_brush_resource"):
                brush = widget.get("brush", {})
                if not isinstance(brush, dict) or not brush.get("resource_object"):
                    errors.append(f"{name} Brush.ResourceObject is missing")

        rules = target.get("layout_rules", {})
        if isinstance(rules, dict):
            if rules.get("forbid_negative_positions"):
                for widget in widgets.values():
                    position = widget.get("position")
                    if (
                        isinstance(position, list)
                        and len(position) == 2
                        and any(isinstance(value, (int, float)) and value < 0 for value in position)
                    ):
                        errors.append(f"{widget.get('name')} has a negative position")
            for name in rules.get("forbid_auto_size", []):
                widget = widgets.get(name)
                if widget is None:
                    errors.append(f"auto_size rule target is missing: {name}")
                elif widget.get("auto_size") is not False:
                    errors.append(f"{name} must disable auto_size")
            for rule in rules.get("scrollbars", []):
                if not isinstance(rule, dict):
                    continue
                name = rule.get("name")
                widget = widgets.get(name)
                if widget is None:
                    errors.append(f"scrollbar rule target is missing: {name}")
                elif widget.get("scrollbar_visibility") != rule.get("visibility"):
                    errors.append(f"{name} scrollbar visibility does not match")

    verification = contract.get("verification", {})
    if not isinstance(verification, dict):
        errors.append("verification is required")
    else:
        if verification.get("property_readback") != "pass":
            errors.append("verification.property_readback must be pass before delivery")
        if verification.get("designer_visual") != "pass":
            errors.append("verification.designer_visual must be pass before delivery")
        screenshot_path = resolve_file(
            verification.get("designer_screenshot"),
            "verification.designer_screenshot",
            errors,
        )
        validate_hash(
            screenshot_path,
            verification.get("designer_screenshot_sha256"),
            "verification.designer_screenshot_sha256",
            errors,
        )
        if verification.get("pie") not in {"pass", "fail", "not_run"}:
            errors.append("verification.pie must be pass, fail, or not_run")
        if verification.get("pie") == "not_run":
            warnings.append("PIE has not been run; functional verification remains pending")

    return {
        "schema_version": 1,
        "artifact_type": "ui_delivery_contract_validation",
        "contract": str(contract_path),
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate an Oasis UI delivery contract.")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--report", type=Path)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    report = validate_contract(args.contract)
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        report_path = args.report.resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
