#!/usr/bin/env python3
"""Validate a game UI project profile using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


STATUSES = {"active", "candidate", "pending_review", "deprecated", "rejected"}
COMPONENT_ID = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_]*){2,}$")
REQUIRED_COMPONENT_FIELDS = {
    "component_id", "name", "category", "description", "states", "parent_types",
    "layer", "reusable", "confidence", "status", "version",
}


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("schema_version", "project", "style_guide", "components", "pages", "history"):
        if field not in profile:
            errors.append(f"missing top-level field: {field}")
    if errors:
        return errors

    project = profile["project"]
    if not project.get("name") or not project.get("slug"):
        errors.append("project requires name and slug")

    identifiers: set[str] = set()
    for index, component in enumerate(profile["components"]):
        prefix = f"components[{index}]"
        missing = REQUIRED_COMPONENT_FIELDS - component.keys()
        if missing:
            errors.append(f"{prefix} missing: {', '.join(sorted(missing))}")
            continue
        component_id = component["component_id"]
        if not COMPONENT_ID.fullmatch(component_id):
            errors.append(f"{prefix}.component_id is invalid: {component_id}")
        if component_id in identifiers:
            errors.append(f"duplicate component_id: {component_id}")
        identifiers.add(component_id)
        if component["status"] not in STATUSES:
            errors.append(f"{component_id}.status is invalid: {component['status']}")
        confidence = component["confidence"]
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"{component_id}.confidence must be between 0 and 1")
        if not isinstance(component["version"], int) or component["version"] < 1:
            errors.append(f"{component_id}.version must be a positive integer")
        if not isinstance(component["layer"], int) or not 0 <= component["layer"] <= 100:
            errors.append(f"{component_id}.layer must be an integer from 0 to 100")
        if not component["states"] or not component["parent_types"]:
            errors.append(f"{component_id} requires non-empty states and parent_types")
        if component["status"] == "active" and not component.get("confirmed_by"):
            errors.append(f"{component_id}.confirmed_by is required for active status")
        if confidence < 0.85 and component["status"] == "active":
            errors.append(f"{component_id} cannot be active below 0.85 confidence")

    for page in profile["pages"]:
        for component_id in page.get("components", []):
            if component_id not in identifiers:
                errors.append(f"page {page.get('page_id', '<unknown>')} references missing component: {component_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True)
    args = parser.parse_args()
    path = Path(args.profile)
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}")
        return 2
    errors = validate_profile(profile)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {path}")
    print(f"components={len(profile['components'])} pages={len(profile['pages'])} history={len(profile['history'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
