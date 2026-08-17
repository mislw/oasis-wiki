from __future__ import annotations

import argparse
import subprocess
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, Sequence


class QuietHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass


def build_worker_command(directory: Path, host: str, port: int) -> list[str]:
    return [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "--directory",
        str(directory.resolve()),
        "--host",
        host,
        "--port",
        str(port),
    ]


def supervise_worker(
    command: Sequence[str],
    *,
    restart_delay: float = 0.25,
    popen_factory: Callable[..., subprocess.Popen] = subprocess.Popen,
    sleep: Callable[[float], None] = time.sleep,
    max_runs: int | None = None,
) -> int:
    runs = 0
    last_exit_code = 0
    while max_runs is None or runs < max_runs:
        process = popen_factory(
            list(command),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        runs += 1
        try:
            last_exit_code = int(process.wait())
        except KeyboardInterrupt:
            process.terminate()
            return 0
        if max_runs is None or runs < max_runs:
            sleep(restart_delay)
    return last_exit_code


def run_worker(directory: Path, host: str, port: int) -> int:
    handler = partial(QuietHandler, directory=str(directory.resolve()))
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    server.serve_forever()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve one generated UI control workbench.")
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--restart-delay", type=float, default=0.25, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        return run_worker(args.directory, args.host, args.port)
    return supervise_worker(
        build_worker_command(args.directory, args.host, args.port),
        restart_delay=max(0.05, args.restart_delay),
    )


if __name__ == "__main__":
    raise SystemExit(main())
