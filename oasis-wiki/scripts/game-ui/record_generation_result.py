from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generation_pipeline import GenerationPipelineError, read_json, record_generation_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a real game UI image-generation result.")
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--output-image", required=True, type=Path)
    parser.add_argument("--generated-at")
    args = parser.parse_args()
    try:
        result_path = record_generation_result(args.package, args.output_image, args.generated_at)
        result = read_json(result_path)
    except GenerationPipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"generation_result": str(result_path), "output_sha256": result["output_sha256"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
