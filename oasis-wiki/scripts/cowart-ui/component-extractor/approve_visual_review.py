from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Lock an explicitly approved Cowart UI visual for componentization.")
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--final-image", required=True, type=Path)
    args = parser.parse_args()

    review_path = args.review.resolve()
    final_image = args.final_image.resolve()
    review = json.loads(review_path.read_text(encoding="utf-8-sig"))
    if review.get("schema_version") != 1 or review.get("workflow_stage") != "visual_review":
        raise ValueError("Review file is not a supported visual-review.json package.")
    if review.get("status") == "approved":
        raise ValueError("Review is already approved. Create a new visual-review package for a new revision.")
    if not final_image.is_file():
        raise FileNotFoundError(final_image)
    with Image.open(final_image) as image:
        width, height = image.size
    final_name = f"visual-final{final_image.suffix.lower()}"
    locked_image = review_path.parent / final_name
    shutil.copy2(final_image, locked_image)
    review["status"] = "approved"
    review["approved_at"] = datetime.now(timezone.utc).isoformat()
    review["approved_image"] = {
        "file": final_name,
        "source_name": final_image.name,
        "sha256": sha256_file(locked_image),
        "page_size": {"width": width, "height": height},
    }
    review["next_action"] = "Build the complete UI Tree and componentize this exact locked image."
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"review": str(review_path), "locked_image": str(locked_image), "sha256": review["approved_image"]["sha256"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
