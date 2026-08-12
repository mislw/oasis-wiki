import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


WIKI_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = WIKI_ROOT / "scripts" / "cowart-ui" / "component-extractor"
sys.path.insert(0, str(SCRIPT_ROOT))

import apply_component_decisions
import build_cowart_shape_plan
import build_extraction_plan
import create_ui_workbench
import normalize_canva_export
import validate_manifest


def write_png(path: Path, size=(64, 32), color=(220, 160, 40, 255)) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", size, color).save(path)


class WorkbenchParentComponentDisplayTests(unittest.TestCase):
    def test_workbench_session_copies_clean_and_assembly_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_png(root / "assets" / "button-clean.png")
            write_png(root / "preview" / "button-assembly.png", (160, 60))
            controls_path = root / "ui-tree.json"
            controls_path.write_text(json.dumps({
                "controls": [{
                    "id": "button.primary.gold",
                    "category": "button",
                    "node_kind": "skin",
                    "bounds": {"x": 0, "y": 0, "width": 120, "height": 40},
                    "visual_assets": {
                        "source_crop": "__source__",
                        "clean_asset": "assets/button-clean.png",
                        "assembly_preview": "preview/button-assembly.png",
                    },
                    "review": {"status": "pending_review", "cleanup_status": "clean"},
                }],
            }), encoding="utf-8")

            session = root / "session"
            session.mkdir()
            controls = create_ui_workbench.normalize_controls(controls_path, session, 320, 180)
            component = controls[0]
            self.assertEqual(component["visual_assets"]["clean_asset"], "layers/button.primary.gold.png")
            self.assertEqual(component["visual_assets"]["assembly_preview"], "preview/button.primary.gold.png")
            self.assertTrue((session / component["visual_assets"]["clean_asset"]).is_file())
            self.assertTrue((session / component["visual_assets"]["assembly_preview"]).is_file())
            self.assertTrue(component["reusable_bitmap"])

    def test_standard_ui_tree_nodes_infer_parent_hierarchy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            controls_path = root / "ui-tree.json"
            controls_path.write_text(json.dumps({
                "artifact_type": "ui_tree",
                "nodes": [
                    {"id": "panel.main", "category": "panel", "bounds": {"x": 0, "y": 0, "width": 640, "height": 360}, "extraction": {"mode": "reconstruct_skin", "target_component_id": "panel.main.background"}},
                    {"id": "button.draw.single", "category": "button", "bounds": {"x": 40, "y": 270, "width": 220, "height": 60}, "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.draw.gold"}},
                    {"id": "text.draw.single", "category": "text", "bounds": {"x": 80, "y": 280, "width": 140, "height": 32}, "extraction": {"mode": "native", "target_component_id": "text.draw.single"}},
                ],
            }), encoding="utf-8")

            controls = create_ui_workbench.normalize_controls(controls_path, root, 640, 360)
            by_id = {item["component_id"]: item for item in controls}
            self.assertEqual(by_id["button.draw.single"]["parent_id"], "panel.main")
            self.assertEqual(by_id["text.draw.single"]["parent_id"], "button.draw.single")
            self.assertEqual(by_id["panel.main"]["node_kind"], "composite")
            self.assertEqual(by_id["button.draw.single"]["node_kind"], "composite")
            self.assertIn("panel.main.background", by_id)
            self.assertIn("button.draw.single.background", by_id)

    def test_workbench_normalizes_parent_components_and_native_children(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            controls_path = root / "ui-tree.json"
            controls_path.write_text(json.dumps({
                "controls": [
                    {
                        "id": "panel.main",
                        "category": "panel",
                        "parent_id": "root",
                        "bounds": {"x": 0, "y": 0, "width": 640, "height": 360},
                        "extraction": {"mode": "reconstruct_skin", "target_component_id": "panel.main.background"},
                    },
                    {
                        "id": "pool.cards",
                        "category": "artwork",
                        "parent_id": "panel.main",
                        "bounds": {"x": 180, "y": 40, "width": 280, "height": 180},
                        "extraction": {"mode": "extract_artwork", "target_component_id": "artwork.pool.cards"},
                    },
                    {
                        "id": "button.draw.single",
                        "category": "button",
                        "parent_id": "panel.main",
                        "bounds": {"x": 40, "y": 270, "width": 220, "height": 60},
                        "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.draw.gold"},
                    },
                    {
                        "id": "text.draw.single",
                        "category": "text",
                        "parent_id": "button.draw.single",
                        "bounds": {"x": 80, "y": 280, "width": 140, "height": 32},
                        "extraction": {"mode": "native", "target_component_id": "text.draw.single"},
                    },
                    {
                        "id": "tabs.pool",
                        "category": "tabs",
                        "parent_id": "root",
                        "bounds": {"x": 650, "y": 0, "width": 160, "height": 360},
                        "extraction": {"mode": "composite", "target_component_id": "tabs.pool"},
                    },
                ]
            }), encoding="utf-8")

            controls = create_ui_workbench.normalize_controls(controls_path, root, 900, 500)
            by_id = {item["component_id"]: item for item in controls}

            self.assertEqual(by_id["panel.main"]["node_kind"], "composite")
            self.assertEqual(by_id["panel.main"]["render_mode"], "outline")
            self.assertFalse(by_id["panel.main"]["reusable_bitmap"])
            self.assertEqual(by_id["button.draw.single"]["node_kind"], "composite")
            self.assertEqual(by_id["text.draw.single"]["node_kind"], "native")
            self.assertIn(by_id["text.draw.single"]["render_mode"], {"outline", "hidden"})
            self.assertEqual(by_id["pool.cards"]["node_kind"], "artwork")
            self.assertEqual(by_id["tabs.pool"]["node_kind"], "composite")

            panel_skin = by_id["panel.main.background"]
            button_skin = by_id["button.draw.single.background"]
            self.assertEqual(panel_skin["node_kind"], "skin")
            self.assertEqual(button_skin["node_kind"], "skin")
            self.assertEqual(button_skin["parent_id"], "button.draw.single")
            self.assertIsNotNone(button_skin["visual_assets"]["source_crop"])
            self.assertIsNone(button_skin["visual_assets"]["clean_asset"])
            self.assertEqual(button_skin["review"]["cleanup_status"], "needs_cleanup")

    def test_normalized_manifest_distinguishes_clean_assets_from_source_crops(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source_dir = root / "source"
            source_dir.mkdir()
            write_png(source_dir / "panel.png", (200, 120))
            write_png(source_dir / "button.png", (120, 40))
            write_png(source_dir / "text.png", (80, 20))
            manifest_path = source_dir / "export.json"
            manifest_path.write_text(json.dumps({
                "page_size": {"width": 320, "height": 180},
                "elements": [
                    {"id": "panel", "component_id": "panel.main", "node_kind": "composite", "file": "panel.png", "x": 0, "y": 0, "width": 200, "height": 120},
                    {"id": "button", "component_id": "button.primary.gold", "node_kind": "skin", "file": "button.png", "parent_id": "panel", "x": 20, "y": 60, "width": 120, "height": 40},
                    {"id": "text", "component_id": "text.button.label", "node_kind": "native", "file": "text.png", "parent_id": "button", "x": 40, "y": 70, "width": 80, "height": 20},
                ],
            }), encoding="utf-8")

            output = root / "normalized"
            normalized = normalize_canva_export.normalize(manifest_path, output)
            manifest = json.loads(normalized.read_text(encoding="utf-8"))
            by_id = {item["component_id"]: item for item in manifest["components"]}

            self.assertEqual(by_id["panel.main"]["node_kind"], "composite")
            self.assertIsNone(by_id["panel.main"]["visual_assets"]["clean_asset"])
            self.assertIsNotNone(by_id["panel.main"]["visual_assets"]["source_crop"])
            self.assertEqual(by_id["button.primary.gold"]["visual_assets"]["clean_asset"], "layers/button.primary.gold.png")
            self.assertEqual(by_id["button.primary.gold"]["review"]["cleanup_status"], "clean")
            self.assertIsNone(by_id["text.button.label"]["visual_assets"]["clean_asset"])

    def test_shape_plan_imports_only_clean_skin_and_artwork_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_png(root / "layers" / "button.png")
            write_png(root / "layers" / "cards.png")
            manifest = {
                "schema_version": 2,
                "source": {"page_size": {"width": 320, "height": 180}},
                "components": [
                    {"component_id": "panel.main", "node_kind": "composite", "render_mode": "outline", "parent_id": "root", "layer": 10, "z_index": 0, "bounds": {"x": 0, "y": 0, "width": 300, "height": 160}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_asset": None, "assembly_preview": None}, "review": {"status": "pending_review", "cleanup_status": "not_applicable"}},
                    {"component_id": "button.primary.gold", "node_kind": "skin", "render_mode": "bitmap", "parent_id": "panel.main", "layer": 30, "z_index": 1, "bounds": {"x": 20, "y": 100, "width": 120, "height": 40}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_asset": "layers/button.png", "assembly_preview": None}, "review": {"status": "pending_review", "cleanup_status": "clean"}},
                    {"component_id": "artwork.pool.cards", "node_kind": "artwork", "render_mode": "bitmap", "parent_id": "panel.main", "layer": 20, "z_index": 2, "bounds": {"x": 80, "y": 20, "width": 140, "height": 70}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_asset": "layers/cards.png", "assembly_preview": None}, "review": {"status": "pending_review", "cleanup_status": "clean"}},
                    {"component_id": "text.button.label", "node_kind": "native", "render_mode": "outline", "parent_id": "button.primary.gold", "layer": 50, "z_index": 3, "bounds": {"x": 40, "y": 110, "width": 80, "height": 20}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_asset": None, "assembly_preview": None}, "review": {"status": "pending_review", "cleanup_status": "not_applicable"}},
                ],
            }
            manifest_path = root / "layer-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            self.assertEqual(validate_manifest.validate_manifest(manifest_path), [])
            plan = build_cowart_shape_plan.build_plan(manifest_path)
            self.assertEqual({shape["component_id"] for shape in plan["shapes"]}, {"button.primary.gold", "artwork.pool.cards"})
            self.assertEqual(plan["move_groups"][0]["component_id"], "panel.main")

    def test_clean_asset_gate_rejects_source_and_assembly_only_nodes(self):
        skin = {
            "component_id": "button.primary.gold",
            "node_kind": "skin",
            "visual_assets": {"source_crop": "source/button.png", "clean_asset": None, "assembly_preview": "preview/button.png"},
            "review": {"cleanup_status": "needs_cleanup"},
        }
        composite = {
            "component_id": "panel.main",
            "node_kind": "composite",
            "visual_assets": {"source_crop": "source/panel.png", "clean_asset": None, "assembly_preview": "preview/panel.png"},
            "review": {"cleanup_status": "not_applicable"},
        }
        ready_skin = {
            "component_id": "button.primary.gold",
            "node_kind": "skin",
            "visual_assets": {"source_crop": "source/button.png", "clean_asset": "layers/button.png", "assembly_preview": None},
            "review": {"cleanup_status": "clean"},
        }

        self.assertTrue(apply_component_decisions.activation_gate_errors(skin))
        self.assertTrue(apply_component_decisions.activation_gate_errors(composite))
        self.assertEqual(apply_component_decisions.activation_gate_errors(ready_skin), [])

    def test_extraction_plan_marks_dirty_skin_without_clean_asset(self):
        node = {
            "id": "button.draw.single.background",
            "category": "button",
            "node_kind": "skin",
            "bounds": {"x": 0, "y": 0, "width": 120, "height": 40},
            "visual_assets": {"source_crop": "source/button.png", "clean_asset": None, "assembly_preview": None},
            "extraction": {
                "mode": "reconstruct_skin",
                "target_component_id": "button.draw.gold",
                "remove_content": ["text.draw.single"],
            },
        }
        component = build_extraction_plan.extraction_component(node)
        self.assertEqual(component["node_kind"], "skin")
        self.assertEqual(component["render_mode"], "bitmap")
        self.assertEqual(component["review"]["cleanup_status"], "needs_cleanup")
        self.assertEqual(component["status"], "candidate")

    def test_workbench_template_has_structure_asset_and_visual_asset_views(self):
        template = (WIKI_ROOT / "assets" / "cowart-ui" / "workbench-template" / "index.html").read_text(encoding="utf-8")
        for marker in (
            "assetTab",
            "structureTab",
            "viewSource",
            "viewClean",
            "viewAssembly",
            "showSourceCrops",
            "defaultAssetItems",
            "Clean asset not generated",
            "净化母版",
        ):
            self.assertIn(marker, template)
        self.assertNotIn("function inpaintRect", template)


if __name__ == "__main__":
    unittest.main()
