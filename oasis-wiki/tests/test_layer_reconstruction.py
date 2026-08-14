import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = SKILL_ROOT / "scripts" / "cowart-ui" / "component-extractor"
sys.path.insert(0, str(SCRIPT_ROOT))

import build_extraction_plan
import build_reconstruction_jobs
import recompose_ui
import validate_reconstruction


def write_png(path: Path, size, color) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", size, color).save(path)


class LayerReconstructionTests(unittest.TestCase):
    def approved_inputs(self, directory: Path):
        image = directory / "visual-final.png"
        write_png(image, (10, 10), (20, 30, 40, 255))
        ui_tree = {
            "artifact_type": "ui_tree",
            "page_size": {"width": 10, "height": 10},
            "nodes": [
                {
                    "id": "panel.main",
                    "parent_id": "root",
                    "category": "panel",
                    "bounds": {"x": 1, "y": 1, "width": 8, "height": 8},
                    "visual_assets": {"source_crop": "source/panel.main.png", "clean_layer": None, "assembly_preview": None},
                    "extraction": {"mode": "reconstruct_skin", "target_component_id": "panel.main"},
                },
                {
                    "id": "button.draw.single",
                    "parent_id": "panel.main",
                    "category": "button",
                    "bounds": {"x": 2, "y": 6, "width": 3, "height": 2},
                    "visual_assets": {"source_crop": "source/button.png", "clean_layer": None, "assembly_preview": None},
                    "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.draw.single"},
                },
                {
                    "id": "text.draw.single",
                    "parent_id": "button.draw.single",
                    "category": "text",
                    "bounds": {"x": 2, "y": 6, "width": 2, "height": 1},
                    "segmentation_mask": "masks/text.draw.single.png",
                    "extraction": {"mode": "native", "target_component_id": "text.draw.single"},
                },
                {
                    "id": "artwork.pool",
                    "parent_id": "panel.main",
                    "category": "artwork",
                    "bounds": {"x": 5, "y": 2, "width": 3, "height": 3},
                    "alpha_mask": "masks/artwork.pool.alpha.png",
                    "extraction": {"mode": "extract_artwork", "target_component_id": "artwork.pool"},
                },
            ],
        }
        review = {
            "artifact_type": "visual_review",
            "status": "approved",
            "source_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
        }
        return image, ui_tree, review

    def test_plan_uses_clean_layer_leaf_to_root_order_and_union_masks(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            image, ui_tree, review = self.approved_inputs(directory)

            plan = build_extraction_plan.build_plan(ui_tree, review, image)
            serialized = json.dumps(plan)
            by_id = {item["target_component_id"]: item for item in plan["components"]}

            self.assertEqual(3, plan["schema_version"])
            self.assertEqual("layer_reconstruction_plan", plan["artifact_type"])
            self.assertNotIn("clean_asset", serialized)
            self.assertIn("background.root", by_id)
            self.assertIsNone(by_id["text.draw.single"]["visual_assets"]["clean_layer"])
            self.assertEqual("layers/panel.main.png", by_id["panel.main"]["visual_assets"]["clean_layer"])
            self.assertLess(plan["reconstruction_order"].index("button.draw.single"), plan["reconstruction_order"].index("panel.main"))
            self.assertLess(plan["reconstruction_order"].index("panel.main"), plan["reconstruction_order"].index("background.root"))

            panel_reconstruction = by_id["panel.main"]["layer_reconstruction"]
            self.assertEqual(
                ["button.draw.single", "text.draw.single", "artwork.pool"],
                panel_reconstruction["remove_nodes"],
            )
            self.assertEqual("union", panel_reconstruction["mask"]["operation"])
            self.assertTrue(panel_reconstruction["mask"]["deduplicate_pixels"])
            mask_by_node = {entry["node_id"]: entry for entry in panel_reconstruction["mask"]["sources"]}
            self.assertEqual("alpha_mask", mask_by_node["artwork.pool"]["source_type"])
            self.assertEqual("semantic_mask", mask_by_node["text.draw.single"]["source_type"])
            self.assertEqual("clean_layer_alpha", mask_by_node["button.draw.single"]["source_type"])

    def test_mask_priority_is_alpha_then_semantic_then_bounds_fallback(self):
        bounds = {"x": 1, "y": 2, "width": 3, "height": 4}
        alpha = build_extraction_plan.mask_source_for(
            {"id": "icon", "bounds": bounds, "alpha_mask": "masks/icon.alpha.png", "segmentation_mask": "masks/icon.semantic.png"},
            "layers/icon.png",
        )
        semantic = build_extraction_plan.mask_source_for(
            {"id": "text", "bounds": bounds, "segmentation_mask": "masks/text.semantic.png"},
            None,
        )
        fallback = build_extraction_plan.mask_source_for({"id": "unknown", "bounds": bounds}, None)

        self.assertEqual("alpha_mask", alpha["source_type"])
        self.assertEqual("semantic_mask", semantic["source_type"])
        self.assertEqual("bounds_fallback", fallback["source_type"])
        self.assertGreater(fallback["padding"], 0)

    def test_jobs_follow_hierarchy_and_require_pluggable_executor(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            image, ui_tree, review = self.approved_inputs(directory)
            plan = build_extraction_plan.build_plan(ui_tree, review, image)

            jobs = build_reconstruction_jobs.build_jobs(plan)
            by_id = {job["target_component_id"]: job for job in jobs}

            self.assertEqual("job_created", by_id["button.draw.single"]["status"])
            self.assertEqual(["button.draw.single", "artwork.pool"], by_id["panel.main"]["depends_on"])
            self.assertEqual(["panel.main"], by_id["background.root"]["depends_on"])
            self.assertEqual("image_edit_inpainting", by_id["panel.main"]["executor"]["required_capability"])
            self.assertIsNone(by_id["panel.main"]["executor"]["provider"])

    def test_missing_executor_fails_closed_without_creating_clean_layer(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            jobs = directory / "jobs"
            jobs.mkdir()
            (jobs / "panel.main.json").write_text(json.dumps({
                "artifact_type": "layer_reconstruction_job",
                "target_component_id": "panel.main",
                "output": "layers/panel.main.png",
                "status": "waiting_executor",
            }), encoding="utf-8")
            output = directory / "layers" / "panel.main.png"

            result = subprocess.run(
                [sys.executable, str(SCRIPT_ROOT / "execute_reconstruction_jobs.py"), "--jobs-dir", str(jobs), "--output-root", str(directory)],
                capture_output=True,
                check=False,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("LAYER_RECONSTRUCTION_UNAVAILABLE", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(output.exists())
            failed_job = json.loads((jobs / "panel.main.json").read_text(encoding="utf-8"))
            self.assertEqual("failed", failed_job["status"])
            self.assertEqual("LAYER_RECONSTRUCTION_UNAVAILABLE", failed_job["error"])

    def test_pluggable_executor_can_reconstruct_and_emit_execution_report(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            jobs = directory / "jobs"
            jobs.mkdir()
            (jobs / "panel.main.json").write_text(json.dumps({
                "artifact_type": "layer_reconstruction_job",
                "target_component_id": "panel.main",
                "sequence": 0,
                "depends_on": [],
                "output": "layers/panel.main.png",
                "status": "job_created",
                "executor": {"required_capability": "image_edit_inpainting", "provider": None},
            }), encoding="utf-8")
            (directory / "fake_executor.py").write_text(
                "from pathlib import Path\n"
                "from PIL import Image\n"
                "from image_reconstruction_executor import ImageReconstructionExecutor\n"
                "class FakeExecutor(ImageReconstructionExecutor):\n"
                "    executor_id = 'fake-image-edit'\n"
                "    def capabilities(self): return {'image_edit_inpainting'}\n"
                "    def reconstruct(self, job, source_root, output_root):\n"
                "        target = Path(output_root) / job['output']\n"
                "        target.parent.mkdir(parents=True, exist_ok=True)\n"
                "        Image.new('RGBA', (2, 2), (1, 2, 3, 255)).save(target)\n"
                "        return {'method': 'fixture'}\n",
                encoding="utf-8",
            )
            environment = dict(os.environ)
            environment["PYTHONPATH"] = os.pathsep.join([str(directory), str(SCRIPT_ROOT), environment.get("PYTHONPATH", "")])

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_ROOT / "execute_reconstruction_jobs.py"),
                    "--jobs-dir", str(jobs),
                    "--output-root", str(directory),
                    "--executor", "fake_executor:FakeExecutor",
                ],
                capture_output=True,
                check=False,
                text=True,
                env=environment,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((directory / "layers" / "panel.main.png").is_file())
            report = json.loads((directory / "layer-reconstruction-execution.json").read_text(encoding="utf-8"))
            self.assertEqual("fake-image-edit", report["executor_id"])
            self.assertEqual("completed", report["status"])

    def test_executor_resumes_reconstructed_jobs_without_calling_provider_again(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            jobs = directory / "jobs"
            jobs.mkdir()
            write_png(directory / "layers" / "panel.main.png", (2, 2), (1, 2, 3, 255))
            (jobs / "panel.main.json").write_text(json.dumps({
                "artifact_type": "layer_reconstruction_job",
                "target_component_id": "panel.main",
                "sequence": 0,
                "depends_on": [],
                "output": "layers/panel.main.png",
                "status": "reconstructed",
                "executor": {"required_capability": "image_edit_inpainting", "provider": "fake-image-edit"},
            }), encoding="utf-8")
            (directory / "fake_executor.py").write_text(
                "from image_reconstruction_executor import ImageReconstructionExecutor\n"
                "class FakeExecutor(ImageReconstructionExecutor):\n"
                "    executor_id = 'fake-image-edit'\n"
                "    def capabilities(self): return {'image_edit_inpainting'}\n"
                "    def reconstruct(self, job, source_root, output_root):\n"
                "        raise AssertionError('provider must not be called for reconstructed output')\n",
                encoding="utf-8",
            )
            environment = dict(os.environ)
            environment["PYTHONPATH"] = os.pathsep.join([str(directory), str(SCRIPT_ROOT), environment.get("PYTHONPATH", "")])

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_ROOT / "execute_reconstruction_jobs.py"),
                    "--jobs-dir", str(jobs),
                    "--output-root", str(directory),
                    "--executor", "fake_executor:FakeExecutor",
                ],
                capture_output=True,
                check=False,
                text=True,
                env=environment,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads((directory / "layer-reconstruction-execution.json").read_text(encoding="utf-8"))
            self.assertTrue(report["results"][0]["reused"])
            self.assertEqual("reconstructed", report["results"][0]["status"])

    def test_validation_rejects_pngs_without_executor_evidence_or_clean_assembly(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            plan = self.synthetic_plan()
            write_png(directory / "layers" / "background.root.png", (10, 10), (10, 20, 30, 255))
            write_png(directory / "layers" / "panel.main.png", (6, 6), (20, 160, 80, 255))
            write_png(directory / "layers" / "button.draw.single.png", (2, 2), (220, 40, 40, 255))
            preview = directory / "assembly.png"
            write_png(preview, (10, 10), (0, 0, 0, 0))
            preview.with_suffix(".png.json").write_text(json.dumps({
                "artifact_type": "assembly_preview",
                "source_crop_used": True,
                "sources": [{"source_type": "source_crop"}],
            }), encoding="utf-8")

            report = validate_reconstruction.build_report(plan, directory, preview)

            self.assertIn("LAYER_RECONSTRUCTION_UNAVAILABLE", "\n".join(report["errors"]))
            self.assertIn("source_crop", "\n".join(report["errors"]))

    def synthetic_plan(self):
        def layer(component_id, parent_id, bounds, clean_layer, z_index):
            return {
                "target_component_id": component_id,
                "parent_id": parent_id,
                "mode": "reconstruct_skin",
                "node_kind": "skin",
                "render_mode": "bitmap",
                "status": "candidate",
                "confidence": 1.0,
                "z_index": z_index,
                "instances": [{"node_id": component_id, "parent_id": parent_id, "bounds": bounds}],
                "visual_assets": {"source_crop": f"source/{component_id}.png", "clean_layer": clean_layer, "assembly_preview": None},
                "output": clean_layer,
                "transparent": True,
                "evaluate_nine_slice": False,
                "source_content_clean": True,
                "layer_reconstruction": {
                    "status": "ready",
                    "method": "image_reconstruction",
                    "depends_on": [],
                    "remove_nodes": [],
                    "mask": {"operation": "union", "deduplicate_pixels": True, "sources": []},
                },
            }

        return {
            "schema_version": 3,
            "artifact_type": "layer_reconstruction_plan",
            "source": {"image": "source.png", "sha256": "a" * 64, "page_size": {"width": 10, "height": 10}},
            "reconstruction_order": ["button.draw.single", "panel.main", "background.root"],
            "components": [
                layer("background.root", "root", {"x": 0, "y": 0, "width": 10, "height": 10}, "layers/background.root.png", 0),
                layer("panel.main", "root", {"x": 1, "y": 1, "width": 6, "height": 6}, "layers/panel.main.png", 1),
                layer("button.draw.single", "panel.main", {"x": 2, "y": 2, "width": 2, "height": 2}, "layers/button.draw.single.png", 2),
            ],
        }

    def test_composite_node_groups_children_without_requiring_bitmap_asset(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_png(directory / "layers" / "background.root.png", (10, 10), (10, 20, 30, 255))
            write_png(directory / "layers" / "panel.main.png", (6, 6), (20, 160, 80, 255))
            write_png(directory / "layers" / "button.draw.single.png", (2, 2), (220, 40, 40, 255))
            plan = self.synthetic_plan()
            composite = {
                "target_component_id": "group.main",
                "parent_id": "root",
                "mode": "composite",
                "node_kind": "composite",
                "render_mode": "outline",
                "status": "candidate",
                "confidence": 1.0,
                "z_index": 1,
                "instances": [{
                    "node_id": "group.main",
                    "parent_id": "root",
                    "bounds": {"x": 0, "y": 0, "width": 8, "height": 8},
                }],
                "visual_assets": {"source_crop": "source/group.png", "clean_layer": None, "assembly_preview": None},
                "output": None,
                "transparent": False,
                "evaluate_nine_slice": False,
                "source_content_clean": False,
                "layer_reconstruction": {"status": "not_applicable"},
            }
            plan["components"].append(composite)
            plan["reconstruction_order"].append("group.main")
            panel = next(component for component in plan["components"] if component["target_component_id"] == "panel.main")
            panel["parent_id"] = "group.main"
            panel["instances"][0]["parent_id"] = "group.main"

            preview = recompose_ui.compose_preview(plan, directory, placements={"group.main": {"x": 1, "y": 0}})

            self.assertEqual((10, 20, 30, 255), preview.getpixel((1, 1)))
            self.assertEqual((20, 160, 80, 255), preview.getpixel((2, 1)))
            self.assertEqual((220, 40, 40, 255), preview.getpixel((3, 2)))
            preview_path = directory / "assembly.png"
            preview.save(preview_path)
            preview_path.with_suffix(".png.json").write_text(json.dumps({
                "artifact_type": "assembly_preview",
                "source_crop_used": False,
                "sources": [
                    {"target_component_id": "background.root", "source_type": "clean_layer"},
                    {"target_component_id": "panel.main", "source_type": "clean_layer"},
                    {"target_component_id": "button.draw.single", "source_type": "clean_layer"},
                ],
            }), encoding="utf-8")
            execution = {
                "artifact_type": "layer_reconstruction_execution",
                "status": "completed",
                "executor_id": "fake-image-edit",
                "capability": "image_edit_inpainting",
                "results": [
                    {"target_component_id": component_id, "status": "reconstructed"}
                    for component_id in ("background.root", "panel.main", "button.draw.single")
                ],
            }

            report = validate_reconstruction.build_report(plan, directory, preview_path, execution_report=execution)

            self.assertEqual([], report["errors"])

    def test_moving_child_leaves_only_parent_clean_layer_at_old_position(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_png(directory / "layers" / "background.root.png", (10, 10), (10, 20, 30, 255))
            write_png(directory / "layers" / "panel.main.png", (6, 6), (20, 160, 80, 255))
            write_png(directory / "layers" / "button.draw.single.png", (2, 2), (220, 40, 40, 255))

            preview = recompose_ui.compose_preview(
                self.synthetic_plan(),
                directory,
                placements={"button.draw.single": {"x": 7, "y": 7}},
            )

            self.assertEqual((20, 160, 80, 255), preview.getpixel((2, 2)))
            self.assertEqual((220, 40, 40, 255), preview.getpixel((7, 7)))

    def test_moving_parent_leaves_clean_root_background_and_moves_children(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_png(directory / "layers" / "background.root.png", (10, 10), (10, 20, 30, 255))
            write_png(directory / "layers" / "panel.main.png", (6, 6), (20, 160, 80, 255))
            write_png(directory / "layers" / "button.draw.single.png", (2, 2), (220, 40, 40, 255))

            preview = recompose_ui.compose_preview(
                self.synthetic_plan(),
                directory,
                placements={"panel.main": {"x": 4, "y": 1}},
            )

            self.assertEqual((10, 20, 30, 255), preview.getpixel((1, 1)))
            self.assertEqual((20, 160, 80, 255), preview.getpixel((4, 1)))
            self.assertEqual((220, 40, 40, 255), preview.getpixel((5, 2)))


if __name__ == "__main__":
    unittest.main()
