from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generation_pipeline import GenerationPipelineError, build_generation_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a self-contained game UI image-generation package.")
    parser.add_argument("--ui-tree", required=True, type=Path)
    parser.add_argument("--style-profile", required=True, type=Path)
    parser.add_argument("--references", required=True, type=Path)
    parser.add_argument("--library-references", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--page-purpose", default="")
    parser.add_argument("--reuse-component", action="append", default=[])
    args = parser.parse_args()
    try:
        output = build_generation_package(
            args.ui_tree,
            args.style_profile,
            args.references,
            args.output,
            args.page_purpose,
            args.reuse_component,
            args.library_references,
        )
    except GenerationPipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"generation_package": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
