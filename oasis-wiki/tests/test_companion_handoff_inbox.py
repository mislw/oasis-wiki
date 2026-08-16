import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "scripts"
    / "cowart-ui"
    / "component-extractor"
    / "companion_handoff.py"
)


def load_helper():
    if not SCRIPT.is_file():
        return None
    spec = importlib.util.spec_from_file_location("companion_handoff", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeProcess:
    pid = 2468


class CompanionHandoffInboxTests(unittest.TestCase):
    def test_running_companion_queues_without_starting_a_duplicate_process(self):
        helper = load_helper()
        self.assertIsNotNone(helper)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "oasis-companion.exe"
            executable.touch()
            with patch.object(
                helper,
                "companion_is_running",
                return_value=True,
            ), patch.object(helper.subprocess, "Popen") as popen:
                result = helper.dispatch_companion_handoff(
                    executable,
                    {"schema_version": 1, "kind": "open_ui_workflow"},
                    state_dir=root / "state",
                )

            self.assertEqual(result["status"], "queued")
            popen.assert_not_called()
            handoff = Path(result["handoff"])
            self.assertEqual(
                json.loads(handoff.read_text(encoding="utf-8")),
                {"schema_version": 1, "kind": "open_ui_workflow"},
            )

    def test_stopped_companion_starts_once_in_silent_background_mode(self):
        helper = load_helper()
        self.assertIsNotNone(helper)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "oasis-companion.exe"
            executable.touch()
            with patch.object(
                helper,
                "companion_is_running",
                return_value=False,
            ), patch.object(
                helper.subprocess,
                "Popen",
                return_value=FakeProcess(),
            ) as popen:
                result = helper.dispatch_companion_handoff(
                    executable,
                    {"schema_version": 1, "kind": "open_ui_workflow"},
                    state_dir=root / "state",
                )

            self.assertEqual(result["status"], "launched")
            self.assertEqual(result["pid"], 2468)
            self.assertEqual(
                popen.call_args.args[0],
                [
                    str(executable.resolve()),
                    "--background",
                    "--no-autostart-sync",
                ],
            )
            self.assertEqual(popen.call_args.kwargs["stdin"], subprocess.DEVNULL)
            self.assertEqual(popen.call_args.kwargs["stdout"], subprocess.DEVNULL)
            self.assertEqual(popen.call_args.kwargs["stderr"], subprocess.DEVNULL)


if __name__ == "__main__":
    unittest.main()
