from __future__ import annotations

import argparse
import sys
from pathlib import Path

from generation_pipeline import GenerationPipelineError, compile_generation_prompt, read_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a reference-driven game UI image-generation prompt.")
    parser.add_argument("--style-profile", required=True, type=Path)
    parser.add_argument("--ui-tree", required=True, type=Path)
    parser.add_argument("--reference-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--page-purpose", default="")
    parser.add_argument("--reuse-component", action="append", default=[])
    args = parser.parse_args()
    try:
        prompt = compile_generation_prompt(
            read_json(args.style_profile.resolve()),
            read_json(args.ui_tree.resolve()),
            read_json(args.reference_manifest.resolve()),
            args.page_purpose,
            args.reuse_component,
        )
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(prompt, encoding="utf-8")
    except GenerationPipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
