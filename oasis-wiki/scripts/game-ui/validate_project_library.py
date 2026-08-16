#!/usr/bin/env python3
"""Validate one project-specific game UI library."""

from __future__ import annotations

import argparse
from pathlib import Path

from project_library import validate_project_library


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a project UI library.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--library-root", required=True, type=Path)
    parser.add_argument("--cache-root", type=Path)
    args = parser.parse_args()
    errors = validate_project_library(
        args.library_root.resolve(),
        args.project_root.resolve(),
        args.cache_root.resolve() if args.cache_root else None,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
