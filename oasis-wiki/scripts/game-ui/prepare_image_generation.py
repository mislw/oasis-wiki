from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generation_pipeline import GenerationPipelineError, validate_generation_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Require the Codex built-in image_gen tool before invoking a game UI request.")
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--available-tool", action="append", default=[])
    args = parser.parse_args()
    try:
        context = validate_generation_package(args.package)
    except GenerationPipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if "image_gen" not in args.available_tool:
        print("IMAGE_GENERATION_UNAVAILABLE")
        return 3
    package = context["package"]
    request = context["request"]
    payload = {
        "status": "ready_for_codex_builtin_image_generation",
        "generation_backend": "codex_builtin",
        "tool": "image_gen",
        "credential_mode": "codex_managed",
        "prompt": str(package / request["prompt_file"]),
        "style_references": [str(package / path) for path in request["style_references"]],
        "layout_references": [str(package / path) for path in request["layout_references"]],
        "fallback_policy": request["fallback_policy"],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
