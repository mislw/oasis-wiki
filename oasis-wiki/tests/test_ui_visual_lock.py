import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "game-ui" / "verify_ui_visual_lock.py"
sys.dont_write_bytecode = True


def load_module():
    spec = importlib.util.spec_from_file_location("verify_ui_visual_lock", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class UiVisualLockTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_allows_changes_only_inside_editable_mask(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            baseline = Image.new("RGBA", (4, 4), (20, 40, 60, 255))
            candidate = baseline.copy()
            candidate.putpixel((1, 1), (200, 100, 20, 255))
            mask = Image.new("L", (4, 4), 0)
            mask.putpixel((1, 1), 255)
            baseline.save(root / "baseline.png")
            candidate.save(root / "candidate.png")
            mask.save(root / "mask.png")

            report = self.module.verify_visual_lock(
                root / "baseline.png",
                root / "candidate.png",
                root / "mask.png",
                root / "diff.png",
            )

            self.assertEqual("pass", report["status"])
            self.assertEqual(1, report["changed_pixels_total"])
            self.assertEqual(0, report["changed_pixels_locked"])
            self.assertTrue((root / "diff.png").is_file())

    def test_reports_locked_pixel_changes_and_writes_machine_readable_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            baseline = Image.new("RGBA", (3, 3), (10, 20, 30, 255))
            candidate = baseline.copy()
            candidate.putpixel((2, 2), (255, 0, 0, 255))
            mask = Image.new("L", (3, 3), 0)
            baseline.save(root / "baseline.png")
            candidate.save(root / "candidate.png")
            mask.save(root / "mask.png")

            exit_code = self.module.main(
                [
                    "--baseline",
                    str(root / "baseline.png"),
                    "--candidate",
                    str(root / "candidate.png"),
                    "--editable-mask",
                    str(root / "mask.png"),
                    "--report",
                    str(root / "report.json"),
                    "--diff-image",
                    str(root / "diff.png"),
                ]
            )

            report = json.loads((root / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(2, exit_code)
            self.assertEqual("fail", report["status"])
            self.assertEqual(1, report["changed_pixels_locked"])
            self.assertEqual([2, 2, 3, 3], report["locked_difference_bounds"])

    def test_rejects_dimension_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            Image.new("RGBA", (4, 4)).save(root / "baseline.png")
            Image.new("RGBA", (5, 4)).save(root / "candidate.png")

            with self.assertRaisesRegex(ValueError, "dimensions"):
                self.module.verify_visual_lock(
                    root / "baseline.png",
                    root / "candidate.png",
                    None,
                    None,
                )


if __name__ == "__main__":
    unittest.main()
