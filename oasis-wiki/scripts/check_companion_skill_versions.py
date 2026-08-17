from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


CANONICAL_VERSION_PATTERN = re.compile(r"(?<!\d)(\d+)\.(\d{6})\.(\d+)(?!\d)")
MSI_VERSION_PATTERN = re.compile(
    r"(?<!\d)(\d+)\.(\d{2})\.(\d{1,4})(?:\+|\.)(\d+)(?!\d)"
)


def normalize_companion_version(value: str | None) -> str | None:
    if not value:
        return None
    canonical_match = CANONICAL_VERSION_PATTERN.search(value.strip())
    if canonical_match:
        return ".".join(canonical_match.groups())
    msi_match = MSI_VERSION_PATTERN.search(value.strip())
    if not msi_match:
        return None
    major, year, month_day, iteration = msi_match.groups()
    return f"{major}.{year}{int(month_day):04d}.{iteration}"


def powershell_executable() -> str:
    system_root = Path(os.environ.get("SystemRoot", r"C:\Windows"))
    bundled = system_root / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
    return str(bundled) if bundled.is_file() else "powershell.exe"


def run_powershell(script: str, extra_environment: dict[str, str] | None = None) -> str:
    environment = os.environ.copy()
    if extra_environment:
        environment.update(extra_environment)
    completed = subprocess.run(
        [
            powershell_executable(),
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            script,
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8-sig",
        env=environment,
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(message or f"PowerShell exited with {completed.returncode}")
    return completed.stdout.strip()


def running_companion_paths() -> list[Path]:
    if os.name != "nt":
        return []
    output = run_powershell(
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; "
        "Get-CimInstance Win32_Process -Filter \"Name='oasis-companion.exe'\" | "
        "ForEach-Object { $_.ExecutablePath } | Where-Object { $_ }"
    )
    return [Path(line.strip()) for line in output.splitlines() if line.strip()]


def read_companion_version(executable: Path) -> dict[str, str | None]:
    if os.name != "nt":
        raise RuntimeError("Companion version inspection is supported on Windows only")
    output = run_powershell(
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; "
        "$path=[Environment]::GetEnvironmentVariable('OASIS_VERSION_PROBE'); "
        "$version=(Get-Item -LiteralPath $path).VersionInfo; "
        "[pscustomobject]@{product_version=[string]$version.ProductVersion; "
        "file_version=[string]$version.FileVersion} | ConvertTo-Json -Compress",
        {"OASIS_VERSION_PROBE": str(executable)},
    )
    data = json.loads(output)
    product_version = data.get("product_version")
    file_version = data.get("file_version")
    canonical_version = normalize_companion_version(product_version)
    if canonical_version is None:
        canonical_version = normalize_companion_version(file_version)
    return {
        "product_version": product_version,
        "file_version": file_version,
        "canonical_version": canonical_version,
    }


def default_companion_paths() -> list[Path]:
    candidates: list[Path] = []
    for environment_name in ("ProgramW6432", "ProgramFiles"):
        root = os.environ.get(environment_name)
        if root:
            candidates.append(Path(root) / "Oasis Companion" / "oasis-companion.exe")
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.append(
            Path(local_app_data)
            / "Programs"
            / "Oasis Companion"
            / "oasis-companion.exe"
        )
    return candidates


def unique_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = os.path.normcase(str(path.expanduser().absolute()))
        if key in seen:
            continue
        seen.add(key)
        unique.append(path.expanduser().absolute())
    return unique


def load_skill_version(skill_root: Path) -> str:
    version_file = skill_root / "VERSION"
    version = version_file.read_text(encoding="utf-8").strip()
    if normalize_companion_version(version) != version:
        raise ValueError(f"invalid Skill VERSION: {version!r}")
    return version


def check_versions(
    skill_root: Path,
    companion_executable: Path | None = None,
) -> dict[str, Any]:
    skill_version = load_skill_version(skill_root)
    running_paths = running_companion_paths()
    configured_path = os.environ.get("OASIS_COMPANION_EXE")
    candidates = unique_paths(
        running_paths
        + ([companion_executable] if companion_executable else [])
        + ([Path(configured_path)] if configured_path else [])
        + default_companion_paths()
    )
    running_keys = {
        os.path.normcase(str(path.expanduser().absolute())) for path in running_paths
    }
    probes: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate_key = os.path.normcase(str(candidate))
        is_running = candidate_key in running_keys
        if not is_running and not candidate.is_file():
            continue
        try:
            version = read_companion_version(candidate)
            probes.append(
                {
                    "path": str(candidate),
                    "running": is_running,
                    **version,
                    "error": None,
                }
            )
        except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
            probes.append(
                {
                    "path": str(candidate),
                    "running": is_running,
                    "product_version": None,
                    "file_version": None,
                    "canonical_version": None,
                    "error": str(error),
                }
            )

    active_probes = [probe for probe in probes if probe["running"]]
    evaluated_probes = active_probes or probes[:1]
    if not evaluated_probes:
        status = "blocked"
        message = "Oasis Companion executable was not found"
    elif any(probe["canonical_version"] is None for probe in evaluated_probes):
        status = "blocked"
        message = "The Companion version could not be read"
    elif any(
        probe["canonical_version"] != skill_version for probe in evaluated_probes
    ):
        status = "mismatch"
        message = "The running Companion and installed Skill versions do not match"
    else:
        status = "match"
        message = "The Companion and Skill versions match"

    return {
        "status": status,
        "skill_version": skill_version,
        "message": message,
        "companions": probes,
    }


def print_human(result: dict[str, Any]) -> None:
    print(f"status={result['status']}")
    print(f"skill={result['skill_version']}")
    for companion in result["companions"]:
        role = "running" if companion["running"] else "installed"
        version = companion["canonical_version"] or "unreadable"
        print(f"companion={version} role={role} path={companion['path']}")
        if companion["error"]:
            print(f"error={companion['error']}")
    print(result["message"])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that Oasis Companion and oasis-wiki use the same version.",
    )
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--companion-executable", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = check_versions(args.skill_root, args.companion_executable)
    except (OSError, ValueError, RuntimeError) as error:
        result = {
            "status": "blocked",
            "skill_version": None,
            "message": str(error),
            "companions": [],
        }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)
    return {"match": 0, "mismatch": 1, "blocked": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
