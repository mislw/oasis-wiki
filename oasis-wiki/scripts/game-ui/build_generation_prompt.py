from __future__ import annotations

import argparse
import sys
from pathlib import Path

from generation_pipeline import (
    GenerationPipelineError,
    compile_generation_prompt,
    read_json,
    validate_image_spec,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append Oasis UI constraints to a prepared image-generation prompt.")
    parser.add_argument("--image-spec", required=True, type=Path)
    parser.add_argument("--oasis-constraints", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        prompt = compile_generation_prompt(
            validate_image_spec(read_json(args.image_spec.resolve())),
            read_json(args.oasis_constraints.resolve()),
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
