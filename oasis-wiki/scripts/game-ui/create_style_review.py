from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generation_pipeline import GenerationPipelineError, create_style_review


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an auditable qualitative style-review record.")
    parser.add_argument("--package", required=True, type=Path)
    args = parser.parse_args()
    try:
        review_path = create_style_review(args.package)
    except GenerationPipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"style_review": str(review_path), "status": "pending_developer_review"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
