from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts" / "cowart-ui" / "component-extractor"
REFERENCE_DIR = Path(__file__).resolve().parents[1] / "references"
sys.path.insert(0, str(SCRIPT_DIR))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


create_workbench = load_module("create_ui_workbench", SCRIPT_DIR / "create_ui_workbench.py")
serve_workbench = load_module("serve_ui_workbench", SCRIPT_DIR / "serve_workbench.py")
report_progress = load_module(
    "report_ui_workflow_progress",
    SCRIPT_DIR / "report_ui_workflow_progress.py",
)
workflow_console = load_module(
    "launch_ui_workflow_console",
    SCRIPT_DIR / "launch_ui_workflow_console.py",
)


class FakeProcess:
    pid = 4321


class ExitingProcess:
    def __init__(self, exit_code: int) -> None:
        self.exit_code = exit_code

    def wait(self) -> int:
        return self.exit_code


class UIWorkbenchCompanionHandoffTests(unittest.TestCase):
    def test_skill_documents_native_visual_reuse_and_superseded_page_cleanup(self) -> None:
        game_ui_guide = (REFERENCE_DIR / "game-ui-design-system.md").read_text(encoding="utf-8")
        cowart_guide = (REFERENCE_DIR / "cowart-ui-workflow.md").read_text(encoding="utf-8")

        for marker in (
            "sole Workbench visual",
            "fallback glyph only when no reusable visual is available",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, game_ui_guide)

        for marker in (
            "Superseded Workbench cleanup",
            "keep only the latest same-interface page",
            "Recycle Bin",
            "expected Workbench root",
            "restart or refresh Companion",
            "do not delete source visual",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, cowart_guide)

    def test_workbench_server_supervisor_restarts_a_crashed_worker(self) -> None:
        commands: list[list[str]] = []
        exit_codes = iter((1, 0))
        delays: list[float] = []

        def launch(command: list[str], **_: object) -> ExitingProcess:
            commands.append(command)
            return ExitingProcess(next(exit_codes))

        command = serve_workbench.build_worker_command(Path("session"), "127.0.0.1", 50691)
        result = serve_workbench.supervise_worker(
            command,
            restart_delay=0.1,
            popen_factory=launch,
            sleep=delays.append,
            max_runs=2,
        )

        self.assertEqual(result, 0)
        self.assertEqual(commands, [command, command])
        self.assertEqual(delays, [0.1])
        self.assertIn("--worker", command)

    def test_delivery_references_require_exact_read_only_widget_blueprint_preflight(self) -> None:
        documentation = "\n".join(
            (
                (REFERENCE_DIR / "cowart-ui" / "component-extractor.md").read_text(encoding="utf-8"),
                (REFERENCE_DIR / "oasis-ui-agent-interaction.md").read_text(encoding="utf-8"),
            )
        )

        for marker in (
            "load_path",
            "UGCWidgetBlueprint",
            "只读 MCP 预检",
            "不得从 `/Game/`",
            "最终重验",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, documentation)

    def test_captures_codex_agent_context_only_from_the_current_process(self) -> None:
        context = create_workbench.capture_agent_context(
            {
                "CODEX_THREAD_ID": "01a0066c-5e42-7241-815d-43d19f0bd3d6",
                "CODEX_SESSION_ID": "01a0066c-5e42-7241-815d-43d19f0bd3d6",
            },
            lambda name: str(Path(r"C:\Program Files\WindowsApps\OpenAI.Codex\codex.exe"))
            if name in {"codex", "codex.exe"}
            else None,
            Path(r"E:\UGCProjects\RedCliff"),
        )

        self.assertEqual(
            context,
            {
                "provider": "codex",
                "thread_id": "01a0066c-5e42-7241-815d-43d19f0bd3d6",
                "session_id": "01a0066c-5e42-7241-815d-43d19f0bd3d6",
                "workspace": str(Path(r"E:\UGCProjects\RedCliff").resolve()),
            },
        )
        self.assertIsNone(create_workbench.capture_agent_context({}, lambda _: None, Path.cwd()))

    def test_normalized_controls_preserve_native_display_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            controls_path = root / "controls.json"
            session_dir = root / "session"
            session_dir.mkdir()
            controls_path.write_text(
                json.dumps(
                    {
                        "components": [
                            {
                                "component_id": "text.currency.title",
                                "category": "text",
                                "parent_id": "root",
                                "bounds": {"x": 10, "y": 10, "width": 180, "height": 40},
                                "asset_policy": "native",
                                "content_hint": "货币兑换",
                            },
                            {
                                "component_id": "text.currency.element_title",
                                "category": "text",
                                "parent_id": "root",
                                "bounds": {"x": 10, "y": 60, "width": 180, "height": 40},
                                "asset_policy": "native",
                                "content_hint": "旧提示",
                                "display_text": "元素兑换",
                                "text_style": {
                                    "font_size": 32,
                                    "color": "#f8e8c0",
                                    "horizontal_alignment": "center",
                                },
                            },
                            {
                                "component_id": "button.currency.close",
                                "category": "hit_target",
                                "parent_id": "root",
                                "bounds": {"x": 350, "y": 10, "width": 40, "height": 40},
                                "asset_policy": "native",
                            },
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            controls = create_workbench.normalize_controls(
                controls_path,
                session_dir,
                400,
                200,
            )

        by_id = {control["component_id"]: control for control in controls}
        self.assertEqual(by_id["text.currency.title"]["display_text"], "货币兑换")
        self.assertEqual(by_id["text.currency.element_title"]["display_text"], "元素兑换")
        self.assertEqual(
            by_id["text.currency.element_title"]["text_style"],
            {
                "font_size": 32,
                "color": "#f8e8c0",
                "horizontal_alignment": "center",
            },
        )
        self.assertEqual(by_id["button.currency.close"]["display_text"], "×")
        self.assertEqual(
            by_id["button.currency.close"]["text_style"],
            {
                "font_size": 30,
                "color": "#fff3cf",
                "outline_color": "#6b3515",
                "outline_size": 2,
                "horizontal_alignment": "center",
                "vertical_alignment": "middle",
            },
        )

    def test_normalized_controls_resolve_only_approved_library_previews(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preview = root / "approved.png"
            pending_preview = root / "pending.png"
            Image.new("RGBA", (24, 24), (255, 210, 40, 255)).save(preview)
            Image.new("RGBA", (24, 24), (255, 0, 0, 255)).save(pending_preview)
            library_references = root / "library-references.json"
            library_references.write_text(
                json.dumps(
                    {
                        "references": [
                            {
                                "source": str(preview),
                                "library": {
                                    "status": "active",
                                    "source_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
                                    "component_ids": ["button.primary.gold"],
                                    "semantic_keys": ["currency.dragon_jade"],
                                },
                            },
                            {
                                "source": str(preview),
                                "library": {
                                    "status": "active",
                                    "asset_id": "redcliff.uiresources.common.btn.btn_close_01",
                                    "source_asset": "/RedCliff/Asset/UIresources/Common/Btn/Btn_Close_01.Btn_Close_01",
                                    "component_ids": ["button.close.default"],
                                    "semantic_keys": [],
                                    "states": ["default"],
                                },
                            },
                            {
                                "source": str(pending_preview),
                                "library": {
                                    "status": "pending_review",
                                    "source_asset": "/RedCliff/Pending.Pending",
                                    "component_ids": ["button.pending"],
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            controls_path = root / "controls.json"
            controls_path.write_text(
                json.dumps(
                    {
                        "components": [
                            {
                                "component_id": "icon.currency.dragon_jade",
                                "category": "icon",
                                "parent_id": "root",
                                "bounds": {"x": 10, "y": 10, "width": 40, "height": 40},
                                "asset_policy": "native",
                                "extraction": {"mode": "native", "target_component_id": "UGCObject.ItemSmallIcon"},
                                "reuse_of": "UGCObject.ItemSmallIcon",
                                "texture_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
                                "item_id": 1001,
                            },
                            {
                                "component_id": "button.purchase",
                                "category": "button",
                                "parent_id": "root",
                                "bounds": {"x": 60, "y": 10, "width": 120, "height": 40},
                                "asset_policy": "layer",
                                "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.primary.gold"},
                                "reuse_of": "button.primary.gold",
                            },
                            {
                                "component_id": "button.close.instance",
                                "category": "hit_target",
                                "parent_id": "root",
                                "bounds": {"x": 190, "y": 10, "width": 40, "height": 40},
                                "asset_policy": "native",
                                "extraction": {"mode": "native", "target_component_id": "button.close.default"},
                                "reuse_of": "button.close.default",
                            },
                            {
                                "component_id": "button.pending",
                                "category": "button",
                                "parent_id": "root",
                                "bounds": {"x": 190, "y": 10, "width": 120, "height": 40},
                                "asset_policy": "native",
                                "extraction": {"mode": "native", "target_component_id": "button.pending"},
                                "texture_asset": "/RedCliff/Pending.Pending",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            session_dir = root / "session"
            session_dir.mkdir()

            controls = create_workbench.normalize_controls(
                controls_path,
                session_dir,
                400,
                200,
                library_references_path=library_references,
            )

        by_id = {control["component_id"]: control for control in controls}
        native = by_id["icon.currency.dragon_jade"]
        self.assertEqual(native["texture_asset"], "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10")
        self.assertEqual(native["reuse_of"], "UGCObject.ItemSmallIcon")
        self.assertEqual(native["item_id"], 1001)
        self.assertTrue(native["visual_assets"]["native_preview"].startswith("native/"))
        self.assertFalse(native["reusable_bitmap"])
        self.assertEqual(native["library_reference"]["status"], "active")

        reusable = by_id["button.purchase"]
        self.assertTrue(reusable["visual_assets"]["clean_layer"].startswith("layers/"))
        self.assertTrue(reusable["reusable_bitmap"])
        self.assertEqual(reusable["layer_reconstruction"]["status"], "ready")

        close = by_id["button.close.instance"]
        self.assertEqual(close["component_reuse"]["status"], "ready")
        self.assertEqual(close["component_reuse"]["component_id"], "button.close.default")
        self.assertEqual(close["texture_asset"], "/RedCliff/Asset/UIresources/Common/Btn/Btn_Close_01.Btn_Close_01")
        self.assertTrue(close["visual_assets"]["native_preview"].startswith("native/"))
        self.assertNotIn("display_text", close)

        pending = by_id["button.pending"]
        self.assertIsNone(pending["visual_assets"]["native_preview"])
        self.assertNotIn("library_reference", pending)
    def test_resolves_explicit_environment_and_default_executables_in_priority_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            explicit = root / "explicit.exe"
            environment = root / "environment.exe"
            default = root / "default.exe"
            for executable in (explicit, environment, default):
                executable.touch()

            with patch.dict(os.environ, {"OASIS_COMPANION_EXE": str(environment)}), patch.object(
                create_workbench, "DEFAULT_COMPANION_EXECUTABLE", default
            ):
                self.assertEqual(create_workbench.find_companion_executable(explicit), explicit.resolve())
                self.assertEqual(create_workbench.find_companion_executable(None), environment.resolve())

            with patch.dict(os.environ, {}, clear=True), patch.object(
                create_workbench, "DEFAULT_COMPANION_EXECUTABLE", default
            ):
                self.assertEqual(create_workbench.find_companion_executable(None), default.resolve())

            default.unlink()
            with patch.dict(os.environ, {}, clear=True), patch.object(
                create_workbench, "DEFAULT_COMPANION_EXECUTABLE", default
            ):
                self.assertIsNone(create_workbench.find_companion_executable(None))

    def test_launches_companion_with_the_normalized_workbench_url(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "oasis-companion.exe"
            executable.touch()
            session_dir = Path(directory) / "session"
            session_dir.mkdir()
            with patch.object(
                create_workbench,
                "dispatch_companion_handoff",
                return_value={"status": "queued", "handoff": "handoff.json"},
            ) as dispatch:
                result = create_workbench.start_companion_handoff(
                    executable,
                    "http://localhost:50691/",
                    session_dir,
                )

            self.assertEqual(
                result,
                {"status": "queued", "handoff": "handoff.json"},
            )
            self.assertEqual(
                dispatch.call_args.args,
                (
                    executable,
                    {
                        "schema_version": 1,
                        "kind": "ui_workbench",
                        "url": "http://localhost:50691/",
                        "session_dir": str(session_dir.resolve()),
                    },
                ),
            )

    def test_derives_stable_distinct_page_ids_for_chinese_titles(self) -> None:
        currency = create_workbench.resolve_page_id(None, "货币兑换")

        self.assertEqual(currency, create_workbench.resolve_page_id(None, "货币兑换"))
        self.assertNotEqual(currency, create_workbench.resolve_page_id(None, "宝石抽奖"))
        self.assertRegex(currency, r"^ui-[0-9a-f]{12}$")
        self.assertEqual(create_workbench.resolve_page_id("castle-defence", "城防"), "castle-defence")

    def test_generated_session_contains_page_metadata_and_thumbnail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "source.png"
            output = root / "workbenches"
            Image.new("RGB", (800, 400), "white").save(image)
            argv = [
                "create_ui_workbench.py",
                "--image",
                str(image),
                "--allow-unreviewed",
                "--name",
                "货币兑换",
                "--output-root",
                str(output),
                "--no-start",
            ]
            with patch.object(sys, "argv", argv), patch.dict(
                os.environ,
                {
                    "CODEX_THREAD_ID": "01a0066c-5e42-7241-815d-43d19f0bd3d6",
                    "CODEX_SESSION_ID": "01a0066c-5e42-7241-815d-43d19f0bd3d6",
                },
            ), patch.object(create_workbench.shutil, "which", return_value=r"C:\Codex\codex.exe"):
                self.assertEqual(create_workbench.main(), 0)

            session_dir = next(output.iterdir())
            session = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))
            self.assertEqual(session["title"], "货币兑换")
            self.assertEqual(session["page_id"], create_workbench.resolve_page_id(None, "货币兑换"))
            self.assertEqual(session["thumbnail_image"], "thumbnail.webp")
            self.assertEqual(
                session["workflow_task"],
                {"schema_version": 1, "task_id": session["page_id"]},
            )
            self.assertEqual(
                session["agent_context"]["thread_id"],
                "01a0066c-5e42-7241-815d-43d19f0bd3d6",
            )
            with Image.open(session_dir / "thumbnail.webp") as thumbnail:
                self.assertEqual(thumbnail.size, (320, 180))

    def test_progress_helper_writes_a_scoped_update_and_launches_companion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            companion = root / "oasis-companion.exe"
            companion.touch()
            with patch.object(
                report_progress,
                "dispatch_companion_handoff",
                return_value={"status": "queued", "handoff": "handoff.json"},
            ) as dispatch:
                result = report_progress.report_progress(
                    session_dir=session,
                    task_id="currency-exchange",
                    stage="umg",
                    status="in_progress",
                    message="正在通过 MCP 创建 WidgetBlueprint",
                    artifacts=["deliveries/one/delivery-request.json"],
                    companion_executable=companion,
                )

            update_path = Path(result["update"])
            update = json.loads(update_path.read_text(encoding="utf-8"))
            self.assertEqual(update["task_id"], "currency-exchange")
            self.assertEqual(update["stage"], "umg")
            self.assertEqual(update["status"], "in_progress")
            self.assertEqual(update["artifacts"], ["deliveries/one/delivery-request.json"])
            self.assertEqual(
                dispatch.call_args.args,
                (
                    companion.resolve(),
                    {
                        "schema_version": 1,
                        "kind": "workflow_update",
                        "update_path": str(update_path),
                    },
                ),
            )

    def test_browser_fallback_derives_the_same_eight_workflow_stages(self) -> None:
        stages = workflow_console.derive_workflow_stages(
            tree_exists=True,
            review_status="approved",
            workbench_exists=True,
            delivery_exists=True,
        )

        self.assertEqual(list(stages), [
            "source",
            "ui_tree",
            "visual",
            "layering",
            "workbench",
            "umg",
            "logic",
            "review",
        ])
        self.assertEqual(stages["workbench"], "awaiting_confirmation")
        self.assertEqual(stages["umg"], "awaiting_confirmation")

    def test_launch_failure_record_does_not_expose_the_executable_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "private-location" / "oasis-companion.exe"
            executable.parent.mkdir()
            executable.touch()
            with patch.object(
                create_workbench,
                "dispatch_companion_handoff",
                side_effect=FileNotFoundError(2, "missing", str(executable)),
            ):
                result = create_workbench.create_companion_handoff(
                    executable,
                    "http://localhost:50691/",
                )

            self.assertEqual(
                result,
                {
                    "status": "fallback",
                    "reason": "companion_launch_failed",
                    "error_type": "FileNotFoundError",
                },
            )
            self.assertNotIn(str(executable), json.dumps(result))

    def test_missing_companion_returns_a_localhost_fallback_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True), patch.object(
            create_workbench,
            "DEFAULT_COMPANION_EXECUTABLE",
            Path(directory) / "missing.exe",
        ):
            result = create_workbench.create_companion_handoff(None, "http://localhost:50691/")

        self.assertEqual(result, {"status": "fallback", "reason": "companion_not_found"})

    def test_missing_companion_does_not_prevent_workbench_manifest_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "source.png"
            output = root / "workbenches"
            Image.new("RGB", (16, 12), "white").save(image)
            argv = [
                "create_ui_workbench.py",
                "--image",
                str(image),
                "--allow-unreviewed",
                "--output-root",
                str(output),
                "--port",
                "50691",
            ]
            with patch.object(sys, "argv", argv), patch.object(
                create_workbench, "start_server", return_value=2468
            ), patch.dict(os.environ, {"OASIS_COMPANION_EXE": ""}), patch.object(
                create_workbench,
                "DEFAULT_COMPANION_EXECUTABLE",
                root / "missing.exe",
            ):
                self.assertEqual(create_workbench.main(), 0)

            manifests = list(output.glob("*/workbench.json"))
            self.assertEqual(len(manifests), 1)
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
            self.assertEqual(manifest["server_pid"], 2468)
            self.assertEqual(
                manifest["companion_handoff"],
                {"status": "fallback", "reason": "companion_not_found"},
            )

    def test_loopback_server_allows_tauri_webview_reads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "session.json").write_text('{"title":"currency"}', encoding="utf-8")
            handler = partial(serve_workbench.QuietHandler, directory=str(root))
            server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.addCleanup(server.server_close)
            self.addCleanup(server.shutdown)

            with urllib.request.urlopen(
                f"http://127.0.0.1:{server.server_port}/session.json",
                timeout=2,
            ) as response:
                self.assertEqual(response.read(), b'{"title":"currency"}')
                self.assertEqual(response.headers["Access-Control-Allow-Origin"], "*")
                self.assertEqual(response.headers["Access-Control-Allow-Methods"], "GET, HEAD, OPTIONS")


if __name__ == "__main__":
    unittest.main()
