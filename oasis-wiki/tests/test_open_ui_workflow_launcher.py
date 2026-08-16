import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts" / "cowart-ui" / "component-extractor"
SCRIPT = SCRIPT_DIR / "open_ui_workflow.py"
sys.path.insert(0, str(SCRIPT_DIR))


def load_launcher():
    if not SCRIPT.is_file():
        return None
    spec = importlib.util.spec_from_file_location("open_ui_workflow", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeProcess:
    pid = 2468


class OpenUiWorkflowLauncherTests(unittest.TestCase):
    def test_launcher_exists_and_opens_the_native_workflow_window(self):
        launcher = load_launcher()
        self.assertIsNotNone(launcher)
        companion = Path(r"C:\Program Files\Oasis Companion\oasis-companion.exe")

        with patch.object(
            launcher,
            "find_companion_executable",
            return_value=companion,
        ), patch.object(
            launcher,
            "dispatch_companion_handoff",
            return_value={"status": "queued", "handoff": "handoff.json"},
        ) as dispatch:
            result = launcher.open_ui_workflow()

        self.assertEqual(
            result,
            {"status": "queued", "handoff": "handoff.json"},
        )
        self.assertEqual(
            dispatch.call_args.args,
            (
                companion,
                {"schema_version": 1, "kind": "open_ui_workflow"},
            ),
        )


if __name__ == "__main__":
    unittest.main()
