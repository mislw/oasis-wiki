#!/usr/bin/env python3
"""Detect a project from a workspace path and resolve its UI profile sources."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    chunks = re.findall(r"[^\W_]+", normalized, flags=re.UNICODE)
    return "-".join(chunks) or "unknown-project"


def canonical_slug(project_name: str, registry: dict[str, Any]) -> str:
    candidate_forms = {project_name.casefold(), slugify(project_name)}
    for slug, entry in registry.get("projects", {}).items():
        aliases = [slug, entry.get("name", ""), *entry.get("aliases", [])]
        alias_forms = {form for value in aliases for form in (str(value).casefold(), slugify(str(value)))}
        if candidate_forms & alias_forms:
            return slug
    return slugify(project_name)


def find_git_root(path: Path) -> Path | None:
    current = path if path.is_dir() else path.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def detect_project(cwd: Path, registry: dict[str, Any]) -> dict[str, Any]:
    path = cwd.expanduser()
    parts = path.parts
    project_name = ""
    project_root = path
    method = "directory"

    for index, part in enumerate(parts[:-1]):
        if part.casefold() == "ugcprojects" and index + 1 < len(parts):
            project_name = parts[index + 1]
            project_root = Path(*parts[: index + 2])
            method = "ugcprojects"
            break

    if not project_name:
        git_root = find_git_root(path)
        if git_root:
            project_root = git_root
            project_name = git_root.name
            method = "git"
        else:
            project_name = path.name or "unknown-project"

    slug = canonical_slug(project_name, registry)
    home = Path.home()
    skill_root = Path(__file__).resolve().parents[2]
    sources = [
        {"tier": "project", "path": str(project_root / ".game-ui-system" / "profile.json")},
        {"tier": "user", "path": str(home / ".codex" / "game-ui-design-system" / "projects" / slug / "profile.json")},
        {"tier": "bundled", "path": str(skill_root / "references" / "game-ui" / "projects" / f"{slug}.json")},
        {"tier": "default", "path": str(skill_root / "assets" / "game-ui" / "project-profile-template" / "profile.json")},
    ]
    selected = next((source for source in sources if Path(source["path"]).exists()), sources[-1])
    return {
        "project_name": project_name,
        "slug": slug,
        "project_root": str(project_root),
        "detection_method": method,
        "selected_profile": selected,
        "profile_sources": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", default=str(Path.cwd()))
    parser.add_argument("--registry")
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parents[2]
    registry_path = (
        Path(args.registry)
        if args.registry
        else skill_root / "references" / "game-ui" / "project-registry.json"
    )
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    print(json.dumps(detect_project(Path(args.cwd), registry), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
