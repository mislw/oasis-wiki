#!/usr/bin/env python3
"""Initialize project-owned manifests for the game UI design system."""

from __future__ import annotations

import argparse
from pathlib import Path

from project_library import ProjectLibraryError, read_json_object, write_json_object
from validate_library import validate_profile


def initialize_library(project_root: Path, source_profile: Path) -> Path:
    """Create the project library from one validated profile."""

    library = project_root / ".game-ui-system"
    profile = read_json_object(source_profile)
    errors = validate_profile(profile)
    if profile.get("schema_version") != 1:
        errors.insert(0, "schema_version must be 1")
    if errors:
        raise ProjectLibraryError("source profile is invalid: " + "; ".join(errors))

    project = profile["project"]
    write_json_object(library / "profile.json", profile)
    write_json_object(
        library / "catalogs" / "assets.json",
        {"schema_version": 1, "project": project, "assets": []},
    )
    write_json_object(
        library / "catalogs" / "item-icons.json",
        {"schema_version": 1, "project": project, "items": []},
    )
    write_json_object(
        library / "catalogs" / "component-assets.json",
        {"schema_version": 1, "project": project, "components": []},
    )
    history = library / "history" / "catalog-history.jsonl"
    history.parent.mkdir(parents=True, exist_ok=True)
    history.touch(exist_ok=True)
    return library


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a project UI library.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--source-profile", required=True, type=Path)
    args = parser.parse_args()
    try:
        library = initialize_library(args.project_root.resolve(), args.source_profile.resolve())
    except ProjectLibraryError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(library)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
