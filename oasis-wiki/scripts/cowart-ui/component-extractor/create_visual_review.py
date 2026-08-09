from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


def slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or "ui-visual-review"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Cowart visual-review package before UI componentization.")
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--output-root", type=Path, default=Path.home() / ".codex" / "ui-visual-reviews")
    args = parser.parse_args()

    image_path = args.image.resolve()
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    with Image.open(image_path) as image:
        width, height = image.size
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    session_dir = args.output_root.resolve() / f"{stamp}-{slug(args.name)}"
    session_dir.mkdir(parents=True, exist_ok=False)
    candidate_name = f"visual-candidate{image_path.suffix.lower()}"
    candidate_path = session_dir / candidate_name
    shutil.copy2(image_path, candidate_path)
    review = {
        "schema_version": 1,
        "workflow_stage": "visual_review",
        "title": args.name,
        "status": "pending_visual_review",
        "candidate_image": {
            "file": candidate_name,
            "source_name": image_path.name,
            "sha256": sha256_file(candidate_path),
            "page_size": {"width": width, "height": height},
        },
        "approved_image": None,
        "cowart": {
            "handoff": {
                "status": "pending_auto_insert",
                "project_dir": None,
                "page_id": None,
                "shape_id": None,
            },
            "required_shape_meta": {
                "workflowStage": "visual_review",
                "reviewStatus": "pending_visual_review",
                "sourceRole": "ui_preview",
            }
        },
        "next_action": "Automatically insert into native Cowart, refine the visual candidate, then explicitly approve the final bitmap.",
    }
    review_path = session_dir / "visual-review.json"
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"session_dir": str(session_dir), "review": str(review_path), "candidate_image": str(candidate_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
