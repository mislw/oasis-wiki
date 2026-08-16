from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from companion_handoff import dispatch_companion_handoff


STAGES = {"source", "ui_tree", "visual", "layering", "workbench", "umg", "logic", "review"}
STATUSES = {"not_started", "in_progress", "awaiting_confirmation", "completed", "blocked", "stale"}
DEFAULT_COMPANION_EXECUTABLE = (
    Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    / "Oasis Companion"
    / "oasis-companion.exe"
)


def find_companion_executable(explicit: Path | None) -> Path | None:
    candidates = [
        explicit,
        Path(os.environ["OASIS_COMPANION_EXE"]) if os.environ.get("OASIS_COMPANION_EXE") else None,
        DEFAULT_COMPANION_EXECUTABLE,
    ]
    for candidate in candidates:
        if candidate is not None:
            resolved = candidate.expanduser().resolve()
            if resolved.is_file():
                return resolved
    return None


def report_progress(
    *,
    session_dir: Path,
    task_id: str,
    stage: str,
    status: str,
    message: str = "",
    artifacts: list[str] | None = None,
    companion_executable: Path | None = None,
) -> dict[str, Any]:
    session = session_dir.expanduser().resolve()
    if not session.is_dir():
        raise FileNotFoundError(session)
    if stage not in STAGES:
        raise ValueError(f"unsupported workflow stage: {stage}")
    if status not in STATUSES:
        raise ValueError(f"unsupported workflow status: {status}")
    safe_artifacts = []
    for artifact in artifacts or []:
        candidate = (session / artifact).resolve()
        candidate.relative_to(session)
        safe_artifacts.append(candidate.relative_to(session).as_posix())

    updates = session / "workflow-updates"
    updates.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    update_path = updates / f"{stamp}-{stage}.json"
    update = {
        "schema_version": 1,
        "task_id": task_id,
        "stage": stage,
        "status": status,
        "message": message,
        "artifacts": safe_artifacts,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    update_path.write_text(json.dumps(update, ensure_ascii=False, indent=2), encoding="utf-8")

    executable = find_companion_executable(companion_executable)
    if executable is None:
        return {"status": "saved", "reason": "companion_not_found", "update": str(update_path)}
    handoff = dispatch_companion_handoff(
        executable,
        {
            "schema_version": 1,
            "kind": "workflow_update",
            "update_path": str(update_path),
        },
    )
    return {**handoff, "update": str(update_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Report Oasis UI workflow progress to Companion.")
    parser.add_argument("--session-dir", required=True, type=Path)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--stage", required=True, choices=sorted(STAGES))
    parser.add_argument("--status", required=True, choices=sorted(STATUSES))
    parser.add_argument("--message", default="")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--companion-executable", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            report_progress(
                session_dir=args.session_dir,
                task_id=args.task_id,
                stage=args.stage,
                status=args.status,
                message=args.message,
                artifacts=args.artifact,
                companion_executable=args.companion_executable,
            ),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
