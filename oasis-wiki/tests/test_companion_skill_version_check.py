import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_companion_skill_versions.py"


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_companion_skill_versions",
        SCRIPT,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CompanionSkillVersionCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = load_checker()

    def test_normalizes_canonical_and_msi_versions(self):
        cases = {
            "1.260816.2": "1.260816.2",
            "1.26.816+2": "1.260816.2",
            "1.26.816.2": "1.260816.2",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(
                    self.checker.normalize_companion_version(raw),
                    expected,
                )

    def test_running_companion_must_match_skill(self):
        old_companion = Path(r"C:\Old\oasis-companion.exe")
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_root = Path(temporary_directory)
            (skill_root / "VERSION").write_text("1.260816.2\n", encoding="utf-8")
            with patch.object(
                self.checker,
                "running_companion_paths",
                return_value=[old_companion],
            ), patch.object(
                self.checker,
                "default_companion_paths",
                return_value=[],
            ), patch.object(
                self.checker,
                "read_companion_version",
                return_value={
                    "product_version": "1.260814.4",
                    "file_version": "1.260814.4",
                    "canonical_version": "1.260814.4",
                },
            ):
                result = self.checker.check_versions(skill_root)

        self.assertEqual(result["status"], "mismatch")
        self.assertTrue(result["companions"][0]["running"])

    def test_matching_running_companion_passes(self):
        companion = Path(r"C:\Program Files\Oasis Companion\oasis-companion.exe")
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_root = Path(temporary_directory)
            (skill_root / "VERSION").write_text("1.260816.2\n", encoding="utf-8")
            with patch.object(
                self.checker,
                "running_companion_paths",
                return_value=[companion],
            ), patch.object(
                self.checker,
                "default_companion_paths",
                return_value=[],
            ), patch.object(
                self.checker,
                "read_companion_version",
                return_value={
                    "product_version": "1.26.816+2",
                    "file_version": "1.26.816.2",
                    "canonical_version": "1.260816.2",
                },
            ):
                result = self.checker.check_versions(skill_root)

        self.assertEqual(result["status"], "match")


if __name__ == "__main__":
    unittest.main()
