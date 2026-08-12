from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


WIKI_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_ROOT = Path(__file__).resolve().parent
DELIVERY_ROOT = WIKI_ROOT / "scripts" / "cowart-ui" / "delivery"
UI_TEMPLATE = WIKI_ROOT / "assets" / "cowart-ui" / "ui-spec-template.json"
HTML_TEMPLATE = WIKI_ROOT / "assets" / "cowart-ui" / "workflow-console" / "index.html"
PROFILE = Path.home() / ".codex" / "game-ui-design-system" / "projects" / "redcliff" / "profile.json"


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "generated-ui"


def command(*args: str) -> dict[str, Any]:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True, timeout=60)
    output = (result.stdout + result.stderr).strip()
    if result.returncode:
        raise RuntimeError(output or f"Command failed with exit code {result.returncode}")
    try:
        return json.loads(result.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"output": output}


class Workflow:
    def __init__(self, root: Path, name: str) -> None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.directory = root / f"{stamp}-{slug(name)}"
        self.directory.mkdir(parents=True, exist_ok=False)
        shutil.copy2(UI_TEMPLATE, self.directory / "ui-spec.json")
        self.state_path = self.directory / "console-state.json"
        self.write_state({"name": name, "workbench_url": None, "cowart_handoff": {"status": "not_started"}})

    def read_state(self) -> dict[str, Any]:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def write_state(self, value: dict[str, Any]) -> None:
        self.state_path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def find_review(self) -> Path | None:
        reviews = sorted((self.directory / "visual").glob("*/visual-review.json")) if (self.directory / "visual").is_dir() else []
        return reviews[-1] if reviews else None

    def safe_relative(self, path: Path) -> str | None:
        try:
            return path.resolve().relative_to(self.directory.resolve()).as_posix()
        except ValueError:
            return None

    def snapshot(self) -> dict[str, Any]:
        profile = json.loads(PROFILE.read_text(encoding="utf-8-sig")) if PROFILE.is_file() else {"components": [], "pages": []}
        status_counts: dict[str, int] = {}
        for component in profile.get("components", []):
            status = component.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        review = self.find_review()
        review_data = json.loads(review.read_text(encoding="utf-8-sig")) if review else None
        preview = None
        final = None
        if review_data:
            preview = self.safe_relative(review.parent / review_data["candidate_image"]["file"])
            approved = review_data.get("approved_image")
            if isinstance(approved, dict):
                final = self.safe_relative(review.parent / approved["file"])
        return {
            "session": str(self.directory),
            "state": self.read_state(),
            "ui_spec": (self.directory / "ui-spec.json").read_text(encoding="utf-8"),
            "tree_exists": (self.directory / "ui-tree.json").is_file(),
            "review": str(review) if review else None,
            "review_status": review_data.get("status") if review_data else None,
            "preview": preview,
            "final": final,
            "delivery_exists": (self.directory / "delivery-plan.json").is_file(),
            "profile": {"path": str(PROFILE), "components": len(profile.get("components", [])), "pages": len(profile.get("pages", [])), "statuses": status_counts},
        }

    def save_spec(self, spec_text: str) -> dict[str, Any]:
        candidate = self.directory / "ui-spec.next.json"
        candidate.write_text(spec_text, encoding="utf-8")
        try:
            command(str(SCRIPT_ROOT / "validate_ui_spec.py"), str(candidate))
            command(str(SCRIPT_ROOT / "build_ui_tree.py"), "--spec", str(candidate), "--output", str(self.directory / "ui-tree.next.json"))
            candidate.replace(self.directory / "ui-spec.json")
            (self.directory / "ui-tree.next.json").replace(self.directory / "ui-tree.json")
        except Exception:
            candidate.unlink(missing_ok=True)
            (self.directory / "ui-tree.next.json").unlink(missing_ok=True)
            raise
        return {"message": "UI Tree updated", "ui_tree": str(self.directory / "ui-tree.json")}

    def stage_visual(self, source_path: str) -> dict[str, Any]:
        source = Path(source_path).expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        return command(
            str(SCRIPT_ROOT / "create_visual_review.py"),
            "--image",
            str(source),
            "--name",
            self.read_state()["name"],
            "--output-root",
            str(self.directory / "visual"),
            "--source-type",
            "external_source",
        )

    def approve_visual(self, final_path: str) -> dict[str, Any]:
        review = self.find_review()
        if review is None:
            raise RuntimeError("Stage a Codex-generated preview before approval.")
        final = Path(final_path).expanduser().resolve()
        if not final.is_file():
            raise FileNotFoundError(final)
        return command(str(SCRIPT_ROOT / "approve_visual_review.py"), "--review", str(review), "--final-image", str(final))

    def create_workbench(self) -> dict[str, Any]:
        review = self.find_review()
        if review is None:
            raise RuntimeError("No visual review is available.")
        review_data = json.loads(review.read_text(encoding="utf-8-sig"))
        approved = review_data.get("approved_image")
        if review_data.get("status") != "approved" or not isinstance(approved, dict):
            raise RuntimeError("Approve the exact final visual before opening the component workbench.")
        result = command(
            str(SCRIPT_ROOT / "create_ui_workbench.py"),
            "--image", str(review.parent / approved["file"]),
            "--controls", str(self.directory / "ui-tree.json"),
            "--visual-review", str(review),
            "--name", self.read_state()["name"],
            "--output-root", str(self.directory / "workbenches"),
        )
        state = self.read_state()
        state["workbench_url"] = result["url"]
        self.write_state(state)
        return result

    def apply_decisions(self, manifest: str, atlas: str, decisions: str, dry_run: bool) -> dict[str, Any]:
        args = [str(SCRIPT_ROOT / "apply_component_decisions.py"), "--manifest", str(Path(manifest).expanduser().resolve()), "--decisions", str(Path(decisions).expanduser().resolve()), "--profile", str(PROFILE)]
        if atlas.strip():
            args.extend(["--atlas", str(Path(atlas).expanduser().resolve())])
        if dry_run:
            args.append("--dry-run")
        return command(*args)

    def build_delivery(self) -> dict[str, Any]:
        tree = self.directory / "ui-tree.json"
        if not tree.is_file():
            raise RuntimeError("Save a valid UI specification first.")
        result = command(str(DELIVERY_ROOT / "build_delivery_plan.py"), "--ui-tree", str(tree), "--profile", str(PROFILE), "--output", str(self.directory / "delivery-plan.json"))
        command(str(DELIVERY_ROOT / "validate_delivery_plan.py"), str(self.directory / "delivery-plan.json"))
        return result

    def create_codex_brief(self) -> dict[str, Any]:
        path = self.directory / "codex-brief.md"
        text = "\n".join([
            f"# {self.read_state()['name']} - Codex Local Visual Task",
            "",
            "Use the current ui-spec.json as the functional and hierarchy contract.",
            "Generate or edit the bitmap locally in this Codex conversation, then save the final PNG outside the UGC project.",
            "Do not bake text, counters, prices, progress, button labels, or interaction states into the bitmap.",
            f"Session: {self.directory}",
            f"Spec: {self.directory / 'ui-spec.json'}",
        ])
        path.write_text(text, encoding="utf-8")
        return {"brief": str(path)}


class Handler(BaseHTTPRequestHandler):
    workflow: Workflow

    def log_message(self, format: str, *args: object) -> None:
        pass

    def respond(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path == "/api/state":
            self.respond(HTTPStatus.OK, self.workflow.snapshot())
            return
        if path == "/":
            body = HTML_TEMPLATE.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path.startswith("/files/"):
            target = (self.workflow.directory / path.removeprefix("/files/")).resolve()
            try:
                target.relative_to(self.workflow.directory.resolve())
            except ValueError:
                self.send_error(HTTPStatus.FORBIDDEN)
                return
            if target.is_file():
                body = target.read_bytes()
                content_type = "image/png" if target.suffix.lower() == ".png" else "application/octet-stream"
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/api/action":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            action, payload = body.get("action"), body.get("payload", {})
            if action == "save_spec":
                result = self.workflow.save_spec(payload["spec"])
            elif action == "stage_visual":
                result = self.workflow.stage_visual(payload["source_path"])
            elif action == "approve_visual":
                result = self.workflow.approve_visual(payload["final_path"])
            elif action == "create_workbench":
                result = self.workflow.create_workbench()
            elif action == "apply_decisions":
                result = self.workflow.apply_decisions(payload["manifest"], payload.get("atlas", ""), payload["decisions"], bool(payload.get("dry_run")))
            elif action == "build_delivery":
                result = self.workflow.build_delivery()
            elif action == "create_codex_brief":
                result = self.workflow.create_codex_brief()
            else:
                raise ValueError(f"Unsupported action: {action}")
            self.respond(HTTPStatus.OK, {"ok": True, "result": result, "state": self.workflow.snapshot()})
        except Exception as exc:
            self.respond(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc), "state": self.workflow.snapshot()})


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch the local Codex UI workflow console.")
    parser.add_argument("--name", default="Generated UI")
    parser.add_argument("--session-root", type=Path, default=Path.home() / ".codex" / "ui-workflow-sessions")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=55290)
    args = parser.parse_args()
    workflow = Workflow(args.session_root.resolve(), args.name)
    Handler.workflow = workflow
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/"
    (workflow.directory / "Open Codex UI Workflow.url").write_text(
        f"[InternetShortcut]\nURL={url}\n",
        encoding="utf-8",
    )
    print(json.dumps({"url": url, "session": str(workflow.directory)}, ensure_ascii=False), flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
