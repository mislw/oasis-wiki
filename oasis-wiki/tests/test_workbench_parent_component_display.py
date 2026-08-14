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
                        "clean_layer": "assets/button-clean.png",
                        "assembly_preview": "preview/button-assembly.png",
                    },
                    "layer_reconstruction": {"status": "ready", "method": "image_reconstruction", "error": None},
                    "review": {"status": "pending_review", "cleanup_status": "ready"},
                }],
            }), encoding="utf-8")

            session = root / "session"
            session.mkdir()
            controls = create_ui_workbench.normalize_controls(controls_path, session, 320, 180)
            component = controls[0]
            self.assertEqual(component["visual_assets"]["clean_layer"], "layers/button.primary.gold.png")
            self.assertEqual(component["visual_assets"]["assembly_preview"], "preview/button.primary.gold.png")
            self.assertTrue((session / component["visual_assets"]["clean_layer"]).is_file())
            self.assertTrue((session / component["visual_assets"]["assembly_preview"]).is_file())
            self.assertTrue(component["reusable_bitmap"])

    def test_standard_ui_tree_nodes_infer_parent_hierarchy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            controls_path = root / "ui-tree.json"
            controls_path.write_text(json.dumps({
                "artifact_type": "ui_tree",
                "nodes": [
                    {"id": "panel.main", "category": "panel", "bounds": {"x": 0, "y": 0, "width": 640, "height": 360}, "extraction": {"mode": "reconstruct_skin", "target_component_id": "panel.main"}},
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
            self.assertIn("background.root", by_id)
            self.assertIsNone(by_id["panel.main"]["visual_assets"]["clean_layer"])
            self.assertIsNone(by_id["button.draw.single"]["visual_assets"]["clean_layer"])

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
                        "extraction": {"mode": "reconstruct_skin", "target_component_id": "panel.main"},
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
            self.assertEqual(by_id["tabs.pool"]["layer_reconstruction"]["status"], "not_applicable")

            panel = by_id["panel.main"]
            button = by_id["button.draw.single"]
            background = by_id["background.root"]
            self.assertIsNotNone(panel["visual_assets"]["source_crop"])
            self.assertIsNone(panel["visual_assets"]["clean_layer"])
            self.assertIsNone(button["visual_assets"]["clean_layer"])
            self.assertEqual(button["layer_reconstruction"]["status"], "pending")
            self.assertIn("text.draw.single", button["layer_reconstruction"]["remove_nodes"])
            self.assertIn("panel.main", background["layer_reconstruction"]["remove_nodes"])

    def test_normalized_manifest_distinguishes_clean_layers_from_source_crops(self):
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
            self.assertIsNone(by_id["panel.main"]["visual_assets"]["clean_layer"])
            self.assertIsNotNone(by_id["panel.main"]["visual_assets"]["source_crop"])
            self.assertEqual(by_id["button.primary.gold"]["visual_assets"]["clean_layer"], "layers/button.primary.gold.png")
            self.assertEqual(by_id["button.primary.gold"]["layer_reconstruction"]["status"], "ready")
            self.assertIsNone(by_id["text.button.label"]["visual_assets"]["clean_layer"])

    def test_shape_plan_imports_only_clean_skin_and_artwork_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_png(root / "layers" / "button.png")
            write_png(root / "layers" / "cards.png")
            manifest = {
                "schema_version": 3,
                "source": {"page_size": {"width": 320, "height": 180}},
                "components": [
                    {"component_id": "panel.main", "node_kind": "composite", "render_mode": "outline", "parent_id": "root", "layer": 10, "z_index": 0, "bounds": {"x": 0, "y": 0, "width": 300, "height": 160}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_layer": None, "assembly_preview": None}, "layer_reconstruction": {"status": "pending", "method": "image_reconstruction"}, "review": {"status": "pending_review", "cleanup_status": "pending"}},
                    {"component_id": "button.primary.gold", "node_kind": "skin", "render_mode": "bitmap", "parent_id": "panel.main", "layer": 30, "z_index": 1, "bounds": {"x": 20, "y": 100, "width": 120, "height": 40}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_layer": "layers/button.png", "assembly_preview": None}, "layer_reconstruction": {"status": "ready", "method": "image_reconstruction"}, "review": {"status": "pending_review", "cleanup_status": "ready"}},
                    {"component_id": "artwork.pool.cards", "node_kind": "artwork", "render_mode": "bitmap", "parent_id": "panel.main", "layer": 20, "z_index": 2, "bounds": {"x": 80, "y": 20, "width": 140, "height": 70}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_layer": "layers/cards.png", "assembly_preview": None}, "layer_reconstruction": {"status": "ready", "method": "image_reconstruction"}, "review": {"status": "pending_review", "cleanup_status": "ready"}},
                    {"component_id": "text.button.label", "node_kind": "native", "render_mode": "outline", "parent_id": "button.primary.gold", "layer": 50, "z_index": 3, "bounds": {"x": 40, "y": 110, "width": 80, "height": 20}, "status": "pending_review", "visual_assets": {"source_crop": None, "clean_layer": None, "assembly_preview": None}, "layer_reconstruction": {"status": "not_applicable"}, "review": {"status": "pending_review", "cleanup_status": "not_applicable"}},
                ],
            }
            manifest_path = root / "layer-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            self.assertEqual(validate_manifest.validate_manifest(manifest_path), [])
            plan = build_cowart_shape_plan.build_plan(manifest_path)
            self.assertEqual({shape["component_id"] for shape in plan["shapes"]}, {"button.primary.gold", "artwork.pool.cards"})
            self.assertEqual(plan["move_groups"][0]["component_id"], "panel.main")

    def test_clean_layer_gate_rejects_source_and_assembly_only_nodes(self):
        skin = {
            "component_id": "button.primary.gold",
            "node_kind": "skin",
            "visual_assets": {"source_crop": "source/button.png", "clean_layer": None, "assembly_preview": "preview/button.png"},
            "layer_reconstruction": {"status": "pending"},
        }
        composite = {
            "component_id": "panel.main",
            "node_kind": "composite",
            "visual_assets": {"source_crop": "source/panel.png", "clean_layer": None, "assembly_preview": "preview/panel.png"},
            "layer_reconstruction": {"status": "pending"},
        }
        ready_skin = {
            "component_id": "button.primary.gold",
            "node_kind": "skin",
            "visual_assets": {"source_crop": "source/button.png", "clean_layer": "layers/button.png", "assembly_preview": None},
            "layer_reconstruction": {"status": "ready"},
        }

        self.assertTrue(apply_component_decisions.activation_gate_errors(skin))
        self.assertTrue(apply_component_decisions.activation_gate_errors(composite))
        self.assertEqual(apply_component_decisions.activation_gate_errors(ready_skin), [])

    def test_extraction_plan_marks_dirty_skin_without_clean_layer(self):
        node = {
            "id": "button.draw.single",
            "category": "button",
            "node_kind": "skin",
            "bounds": {"x": 0, "y": 0, "width": 120, "height": 40},
            "visual_assets": {"source_crop": "source/button.png", "clean_layer": None, "assembly_preview": None},
            "extraction": {
                "mode": "reconstruct_skin",
                "target_component_id": "button.draw.gold",
                "remove_content": ["text.draw.single"],
            },
        }
        component = build_extraction_plan.extraction_component(node)
        self.assertEqual(component["node_kind"], "skin")
        self.assertEqual(component["render_mode"], "bitmap")
        self.assertEqual(component["layer_reconstruction"]["status"], "pending")
        self.assertEqual(component["status"], "candidate")

    def test_completed_execution_report_enables_workbench_capability(self):
        with tempfile.TemporaryDirectory() as temp:
            report_path = Path(temp) / "layer-reconstruction-execution.json"
            report_path.write_text(json.dumps({
                "artifact_type": "layer_reconstruction_execution",
                "status": "completed",
                "executor_id": "codex-upstream-gpt-image-2",
                "capability": "image_edit_inpainting",
                "results": [],
            }), encoding="utf-8")

            capability = create_ui_workbench.load_reconstruction_capability(report_path)

            self.assertTrue(capability["available"])
            self.assertEqual("codex-upstream-gpt-image-2", capability["executor"])
            self.assertIsNone(capability["error"])
            self.assertEqual(str(report_path.resolve()), capability["execution_report"])

    def test_missing_execution_report_keeps_workbench_fail_closed(self):
        capability = create_ui_workbench.load_reconstruction_capability(None)

        self.assertFalse(capability["available"])
        self.assertEqual("LAYER_RECONSTRUCTION_UNAVAILABLE", capability["error"])

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
            "Clean layer not generated",
            "LAYER_RECONSTRUCTION_UNAVAILABLE",
            "job_created",
            "waiting_executor",
            "reconstructing",
            "reconstructed",
            "validation",
            "syncInitialCanvasMode",
            "hasReadyCleanLayer",
            "拖动只调整选区",
            "生成 Clean Layer 后才能移动控件图像",
            "净化母版",
        ):
            self.assertIn(marker, template)
        self.assertNotIn("function inpaintRect", template)


if __name__ == "__main__":
    unittest.main()
