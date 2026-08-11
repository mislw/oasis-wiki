from __future__ import annotations

import argparse
import sys
from pathlib import Path

from generation_pipeline import GenerationPipelineError, validate_generation_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a game UI image-generation package.")
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    try:
        validate_generation_package(args.package)
    except GenerationPipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
