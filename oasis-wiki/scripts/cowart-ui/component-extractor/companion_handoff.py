from __future__ import annotations

import ctypes
import json
import os
import subprocess
import sys
import uuid
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_DIR_ENV = "OASIS_COMPANION_STATE_DIR"


def companion_state_dir() -> Path:
    override = os.environ.get(STATE_DIR_ENV)
    return (
        Path(override).expanduser().resolve()
        if override
        else Path.home() / ".oasis-companion"
    )


def enqueue_handoff(
    payload: dict[str, Any],
    *,
    state_dir: Path | None = None,
) -> Path:
    root = (state_dir or companion_state_dir()).expanduser().resolve()
    inbox = root / "handoffs"
    inbox.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    name = f"{stamp}-{os.getpid()}-{uuid.uuid4().hex}.json"
    target = inbox / name
    temporary = inbox / f".{name}.tmp"
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(temporary, target)
    return target


def _windows_process_path(process_id: int) -> Path | None:
    process_query_limited_information = 0x1000
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    open_process = kernel32.OpenProcess
    open_process.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    open_process.restype = wintypes.HANDLE
    query_path = kernel32.QueryFullProcessImageNameW
    query_path.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]
    query_path.restype = wintypes.BOOL
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    handle = open_process(process_query_limited_information, False, process_id)
    if not handle:
        return None
    try:
        capacity = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(capacity.value)
        if not query_path(handle, 0, buffer, ctypes.byref(capacity)):
            return None
        return Path(buffer.value)
    finally:
        close_handle(handle)


def _process_path(process_id: int) -> Path | None:
    if process_id <= 0:
        return None
    if sys.platform == "win32":
        return _windows_process_path(process_id)
    proc_exe = Path("/proc") / str(process_id) / "exe"
    try:
        return proc_exe.resolve(strict=True)
    except OSError:
        return None


def companion_is_running(
    executable: Path,
    *,
    state_dir: Path | None = None,
) -> bool:
    root = (state_dir or companion_state_dir()).expanduser().resolve()
    runtime_path = root / "runtime.json"
    try:
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        if runtime.get("schema_version") != 1:
            return False
        process_id = int(runtime["pid"])
        recorded = Path(runtime["executable"]).expanduser().resolve()
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False
    expected = executable.expanduser().resolve()
    if os.path.normcase(str(recorded)) != os.path.normcase(str(expected)):
        return False
    running = _process_path(process_id)
    return running is not None and os.path.normcase(
        str(running.resolve())
    ) == os.path.normcase(str(expected))


def dispatch_companion_handoff(
    executable: Path,
    payload: dict[str, Any],
    *,
    state_dir: Path | None = None,
) -> dict[str, Any]:
    resolved = executable.expanduser().resolve()
    handoff = enqueue_handoff(payload, state_dir=state_dir)
    if companion_is_running(resolved, state_dir=state_dir):
        return {"status": "queued", "handoff": str(handoff)}

    flags = 0
    if sys.platform == "win32":
        flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
    process = subprocess.Popen(
        [str(resolved), "--background", "--no-autostart-sync"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        creationflags=flags,
    )
    return {
        "status": "launched",
        "pid": process.pid,
        "handoff": str(handoff),
    }
