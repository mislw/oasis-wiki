import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = SKILL_ROOT / "scripts" / "cowart-ui" / "component-extractor"


class PrecisionComponentReconstructionTests(unittest.TestCase):
    def write_json(self, directory, name, payload):
        path = directory / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def run_script(self, name, *args, check=True):
        return subprocess.run(
            [sys.executable, str(SCRIPT_ROOT / name), *map(str, args)],
            capture_output=True,
            check=check,
            text=True,
        )

    def valid_plan(self):
        return {
            "schema_version": 1,
            "artifact_type": "extraction_plan",
            "source": {
                "image": "visual-final.png",
                "sha256": "a" * 64,
                "page_size": {"width": 1920, "height": 1080},
            },
            "components": [
                {
                    "target_component_id": "button.purchase.gold",
                    "category": "button",
                    "mode": "reconstruct_skin",
                    "status": "candidate",
                    "source_nodes": ["button.offer.01", "button.offer.02", "button.offer.03"],
                    "instances": [
                        {"node_id": "button.offer.01", "bounds": {"x": 0, "y": 0, "width": 120, "height": 44}},
                        {"node_id": "button.offer.02", "bounds": {"x": 0, "y": 50, "width": 120, "height": 44}},
                        {"node_id": "button.offer.03", "bounds": {"x": 0, "y": 100, "width": 120, "height": 44}},
                    ],
                    "remove_content": ["cost_text", "currency_icon"],
                    "source_content_clean": False,
                    "transparent": True,
                    "evaluate_nine_slice": True,
                    "output": "layers/button.purchase.gold.png",
                    "confidence": 0.96,
                    "reason": "Equivalent purchase button skins share one target.",
                },
                {
                    "target_component_id": "text.offer.price",
                    "category": "text",
                    "mode": "native",
                    "status": "candidate",
                    "source_nodes": ["text.offer.price"],
                    "instances": [
                        {"node_id": "text.offer.price", "bounds": {"x": 10, "y": 10, "width": 40, "height": 20}},
                    ],
                    "remove_content": [],
                    "source_content_clean": True,
                    "transparent": False,
                    "evaluate_nine_slice": False,
                    "output": None,
                    "confidence": 1.0,
                    "reason": "Dynamic price must remain native.",
                },
            ],
        }

    def test_groups_equivalent_button_instances_into_one_target(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            image = directory / "visual-final.png"
            image.write_bytes(b"approved image")
            ui_tree = self.write_json(directory, "ui-tree.json", {
                "artifact_type": "ui_tree",
                "nodes": [
                    {"id": "button.offer.01", "category": "button", "asset_policy": "reconstruction_candidate", "bounds": {"x": 0, "y": 0, "width": 120, "height": 44}, "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.purchase.gold", "remove_content": ["cost_text", "currency_icon"], "transparent": True, "evaluate_nine_slice": True, "confidence": 0.96, "reason": "Repeated skin."}},
                    {"id": "button.offer.02", "category": "button", "asset_policy": "reconstruction_candidate", "bounds": {"x": 0, "y": 50, "width": 120, "height": 44}, "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.purchase.gold", "remove_content": ["cost_text", "currency_icon"], "transparent": True, "evaluate_nine_slice": True, "confidence": 0.96, "reason": "Repeated skin."}},
                    {"id": "button.offer.03", "category": "button", "asset_policy": "reconstruction_candidate", "bounds": {"x": 0, "y": 100, "width": 120, "height": 44}, "extraction": {"mode": "reconstruct_skin", "target_component_id": "button.purchase.gold", "remove_content": ["cost_text", "currency_icon"], "transparent": True, "evaluate_nine_slice": True, "confidence": 0.96, "reason": "Repeated skin."}},
                    {"id": "text.offer.price", "category": "text", "asset_policy": "native", "bounds": {"x": 10, "y": 10, "width": 40, "height": 20}, "extraction": {"mode": "native", "target_component_id": "text.offer.price", "confidence": 1.0, "reason": "Native price."}},
                ],
            })
            review = self.write_json(directory, "visual-review.json", {
                "artifact_type": "visual_review",
                "status": "approved",
                "source_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
            })
            output = directory / "extraction-plan.json"

            self.run_script("build_extraction_plan.py", "--ui-tree", ui_tree, "--visual-review", review, "--image", image, "--output", output)

            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(2, len(plan["components"]))
            button = next(component for component in plan["components"] if component["target_component_id"] == "button.purchase.gold")
            native = next(component for component in plan["components"] if component["target_component_id"] == "text.offer.price")
            self.assertEqual(3, len(button["instances"]))
            self.assertIsNone(native["output"])

    def test_rejects_skin_without_content_removal_or_clean_source(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            plan = self.valid_plan()
            plan["components"][0]["remove_content"] = []
            path = self.write_json(directory, "unsafe-plan.json", plan)

            result = self.run_script("validate_extraction_plan.py", "--plan", path, check=False)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("remove_content", result.stderr)

    def test_creates_one_reconstruction_job_for_many_instances(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            path = self.write_json(directory, "plan.json", self.valid_plan())
            jobs = directory / "reconstruction-jobs"

            self.run_script("build_reconstruction_jobs.py", "--plan", path, "--output-dir", jobs)

            job_paths = list(jobs.glob("*.json"))
            self.assertEqual(1, len(job_paths))
            job = json.loads(job_paths[0].read_text(encoding="utf-8"))
            self.assertEqual("button.purchase.gold", job["target_component_id"])
            self.assertEqual(3, len(job["instances"]))

    def test_rejects_automatic_active_status(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            plan = self.valid_plan()
            plan["components"][0]["status"] = "active"
            path = self.write_json(directory, "active-plan.json", plan)

            result = self.run_script("validate_extraction_plan.py", "--plan", path, check=False)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("status", result.stderr)

    def test_skill_hygiene_allows_the_bundled_workflow_files(self):
        script = SKILL_ROOT / "scripts" / "check-skill-hygiene.ps1"
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script)],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_recomposes_transparent_skin_and_marks_visual_review_required(self):
        from PIL import Image

        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            plan = self.valid_plan()
            plan["source"]["page_size"] = {"width": 4, "height": 4}
            plan["components"] = [plan["components"][0]]
            plan["components"][0]["instances"] = [
                {"node_id": "button.offer.01", "bounds": {"x": 0, "y": 0, "width": 2, "height": 2}},
                {"node_id": "button.offer.02", "bounds": {"x": 2, "y": 2, "width": 2, "height": 2}},
            ]
            path = self.write_json(directory, "plan.json", plan)
            assets = directory / "assets"
            asset = assets / "layers" / "button.purchase.gold.png"
            asset.parent.mkdir(parents=True)
            Image.new("RGBA", (1, 1), (255, 200, 0, 128)).save(asset)
            preview = directory / "reconstructed-preview.png"
            report = directory / "reconstruction-report.json"

            self.run_script("recompose_ui.py", "--plan", path, "--assets-dir", assets, "--output", preview)
            self.run_script("validate_reconstruction.py", "--plan", path, "--assets-dir", assets, "--preview", preview, "--output", report)

            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertTrue(preview.is_file())
            self.assertEqual("pending_review", payload["status"])
            self.assertIsNone(payload["visual_similarity"])
            self.assertTrue(payload["visual_review_required"])


if __name__ == "__main__":
    unittest.main()
