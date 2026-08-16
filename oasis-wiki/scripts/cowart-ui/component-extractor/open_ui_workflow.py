from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from companion_handoff import dispatch_companion_handoff


DEFAULT_COMPANION_EXECUTABLE = (
    Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    / "Oasis Companion"
    / "oasis-companion.exe"
)


def find_companion_executable(explicit: Path | None) -> Path | None:
    candidates = [
        explicit,
        Path(os.environ["OASIS_COMPANION_EXE"])
        if os.environ.get("OASIS_COMPANION_EXE")
        else None,
        DEFAULT_COMPANION_EXECUTABLE,
    ]
    for candidate in candidates:
        if candidate is None:
            continue
        resolved = candidate.expanduser().resolve()
        if resolved.is_file():
            return resolved
    return None


def open_ui_workflow(
    companion_executable: Path | None = None,
) -> dict[str, Any]:
    executable = find_companion_executable(companion_executable)
    if executable is None:
        return {"status": "blocked", "reason": "companion_not_found"}
    return dispatch_companion_handoff(
        executable,
        {"schema_version": 1, "kind": "open_ui_workflow"},
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open the native Oasis Companion UI generation workflow.",
    )
    parser.add_argument("--companion-executable", type=Path)
    args = parser.parse_args()
    result = open_ui_workflow(args.companion_executable)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in {"queued", "launched"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
