import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "game-ui" / "validate_ui_delivery_contract.py"
sys.dont_write_bytecode = True


def load_module():
    spec = importlib.util.spec_from_file_location("validate_ui_delivery_contract", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class UiDeliveryContractTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def make_fixture(self, root: Path):
        project_root = root / "UGCProject"
        output_root = root / "audits"
        project_root.mkdir()
        output_root.mkdir()

        visual = root / "approved.png"
        Image.new("RGBA", (8, 6), (30, 60, 90, 255)).save(visual)

        session = root / "session.json"
        session.write_text('{"revision": 4}', encoding="utf-8")
        layout_review = root / "layout-review.json"
        layout_review.write_text(
            json.dumps(
                {
                    "artifact_type": "ui_layout_review",
                    "schema_version": 1,
                    "status": "pending_chat_confirmation",
                    "source": {"session_sha256": sha256(session)},
                }
            ),
            encoding="utf-8",
        )

        snapshot = root / "umg-snapshot.json"
        snapshot.write_text(
            json.dumps(
                {
                    "root": {
                        "name": "CanvasPanel_0",
                        "size": [1920, 1080],
                        "coordinate_space": "full_viewport",
                    },
                    "widgets": [
                        {
                            "name": "BG",
                            "class": "Image",
                            "position": [171, 21],
                            "size": [1561, 948],
                            "auto_size": False,
                            "brush": {
                                "image": "/Game/UI/BG",
                                "resource_object": "/Game/UI/BG",
                            },
                        },
                        {
                            "name": "Button_CloseShop",
                            "class": "Button",
                            "position": [1592, 97],
                            "size": [86, 97],
                            "auto_size": False,
                        },
                        {
                            "name": "ScrollBox_0",
                            "class": "ScrollBox",
                            "position": [271, 280],
                            "size": [1380, 689],
                            "scrollbar_visibility": "Collapsed",
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )

        designer = root / "designer.png"
        Image.new("RGB", (16, 9), (10, 10, 10)).save(designer)

        contract = {
            "schema_version": 1,
            "artifact_type": "ui_delivery_contract",
            "project": {"slug": "fixture", "root": str(project_root)},
            "outputs": {"root": str(output_root)},
            "visual": {
                "status": "approved",
                "path": str(visual),
                "sha256": sha256(visual),
                "width": 8,
                "height": 6,
            },
            "layout": {
                "page_id": "page.item-shop",
                "revision": 4,
                "session_path": str(session),
                "session_sha256": sha256(session),
                "layout_review_path": str(layout_review),
                "layout_review_sha256": sha256(layout_review),
            },
            "target": {
                "load_path": "/Fixture/Asset/UI/ItemShopUI.ItemShopUI",
                "snapshot_path": str(snapshot),
                "snapshot_sha256": sha256(snapshot),
                "root": {
                    "name": "CanvasPanel_0",
                    "size": [1920, 1080],
                    "coordinate_space": "full_viewport",
                },
                "required_controls": [
                    {"name": "BG", "class": "Image", "require_brush_resource": True},
                    {"name": "Button_CloseShop", "class": "Button"},
                ],
                "layout_rules": {
                    "forbid_negative_positions": True,
                    "forbid_auto_size": ["BG"],
                    "scrollbars": [
                        {"name": "ScrollBox_0", "visibility": "Collapsed"}
                    ],
                },
            },
            "verification": {
                "property_readback": "pass",
                "designer_visual": "pass",
                "designer_screenshot": str(designer),
                "designer_screenshot_sha256": sha256(designer),
                "pie": "not_run",
            },
        }
        path = root / "contract.json"
        path.write_text(json.dumps(contract), encoding="utf-8")
        return path, contract

    def test_accepts_fresh_external_contract_with_designer_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            path, _contract = self.make_fixture(Path(temp))
            report = self.module.validate_contract(path)
            self.assertEqual("pass", report["status"])
            self.assertEqual([], report["errors"])

    def test_rejects_stale_layout_and_snapshot_hashes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, contract = self.make_fixture(root)
            Path(contract["layout"]["session_path"]).write_text(
                '{"revision": 5}', encoding="utf-8"
            )
            Path(contract["target"]["snapshot_path"]).write_text(
                '{"changed": true}', encoding="utf-8"
            )

            report = self.module.validate_contract(path)

            self.assertEqual("fail", report["status"])
            self.assertIn("layout.session_sha256 is stale", report["errors"])
            self.assertIn("target.snapshot_sha256 is stale", report["errors"])

    def test_rejects_missing_brush_wrong_root_auto_size_and_scrollbar(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, contract = self.make_fixture(root)
            snapshot_path = Path(contract["target"]["snapshot_path"])
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            snapshot["root"]["size"] = [1561, 948]
            snapshot["widgets"][0]["auto_size"] = True
            snapshot["widgets"][0]["brush"]["resource_object"] = None
            snapshot["widgets"][2]["scrollbar_visibility"] = "Hidden"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            contract["target"]["snapshot_sha256"] = sha256(snapshot_path)
            path.write_text(json.dumps(contract), encoding="utf-8")

            report = self.module.validate_contract(path)

            joined = "\n".join(report["errors"])
            self.assertIn("root size", joined)
            self.assertIn("BG Brush.ResourceObject is missing", joined)
            self.assertIn("BG must disable auto_size", joined)
            self.assertIn("ScrollBox_0 scrollbar visibility", joined)

    def test_rejects_output_inside_project_and_missing_designer_visual_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, contract = self.make_fixture(root)
            contract["outputs"]["root"] = str(Path(contract["project"]["root"]) / "Tests")
            contract["verification"]["designer_visual"] = "not_run"
            contract["verification"]["designer_screenshot"] = ""
            contract["verification"]["designer_screenshot_sha256"] = ""
            path.write_text(json.dumps(contract), encoding="utf-8")

            report = self.module.validate_contract(path)

            self.assertIn("outputs.root must be outside project.root", report["errors"])
            self.assertIn(
                "verification.designer_visual must be pass before delivery",
                report["errors"],
            )


if __name__ == "__main__":
    unittest.main()
