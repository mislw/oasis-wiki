from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a completed native Cowart visual-review handoff.")
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--shape-id", required=True)
    parser.add_argument("--index")
    args = parser.parse_args()

    review_path = args.review.resolve()
    review = json.loads(review_path.read_text(encoding="utf-8-sig"))
    handoff = {
        "status": "inserted",
        "project_dir": str(args.project_dir.resolve()),
        "page_id": args.page_id,
        "shape_id": args.shape_id,
        "index": args.index,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    review.setdefault("cowart", {})["handoff"] = handoff
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")

    session_dir = review_path.parent.parent.parent
    state_path = session_dir / "console-state.json"
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8-sig"))
        state["cowart_handoff"] = handoff
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"review": str(review_path), "cowart_handoff": handoff}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
