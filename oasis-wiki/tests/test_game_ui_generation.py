from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


WIKI_ROOT = Path(__file__).resolve().parents[1]
UI_SPEC_SCRIPT_DIR = WIKI_ROOT / "scripts" / "cowart-ui" / "component-extractor"
sys.path.insert(0, str(UI_SPEC_SCRIPT_DIR))

from build_ui_tree import build_tree  # type: ignore  # noqa: E402
from validate_ui_spec import validate_spec  # type: ignore  # noqa: E402


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_png(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path, format="PNG")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimal_spec(references: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "page": {
            "page_id": "page.exchange.shop",
            "name": "Exchange Shop",
            "canvas": {"width": 1280, "height": 720},
            "purpose": "Exchange resources for rewards.",
            "operations": [],
        },
        "visual": {
            "profile": "redcliff",
            "reference_images": references,
            "art_direction": "Reuse confirmed RedCliff controls.",
        },
        "data_contract": [],
        "nodes": [
            {
                "component_id": "background.exchange.scene",
                "category": "background",
                "parent_id": "root",
                "layer": 0,
                "z_index": 0,
                "bounds": {"x": 0, "y": 0, "width": 1280, "height": 720},
                "status": "pending_review",
                "asset_policy": "layer",
                "dynamic": False,
            }
        ],
    }


def minimal_profile() -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": {"name": "RedCliff", "slug": "redcliff", "aliases": []},
        "style_guide": {"colors": {"window": "warm cream"}},
        "components": [
            {
                "component_id": "button.primary.gold",
                "status": "active",
                "visual_style": {"fill": "gold-orange gradient"},
            }
        ],
        "pages": [],
        "history": [],
    }


class GameUiGenerationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.style = self.root / "style.png"
        self.layout = self.root / "layout.png"
        self.output = self.root / "generated.png"
        write_png(self.style, (64, 40), (104, 54, 31))
        write_png(self.layout, (80, 45), (230, 225, 210))
        write_png(self.output, (128, 72), (201, 146, 53))
        self.profile = self.root / "redcliff.json"
        write_json(self.profile, minimal_profile())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, relative_path: str, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(WIKI_ROOT / relative_path), *(str(arg) for arg in args)],
            cwd=WIKI_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_tree(self, references: list[dict[str, object]]) -> Path:
        path = self.root / "ui-tree.json"
        write_json(path, build_tree(minimal_spec(references)))
        return path

    def write_reference_metadata(self, references: list[dict[str, object]]) -> Path:
        path = self.root / "references.json"
        write_json(path, {"schema_version": 1, "references": references})
        return path

    def build_valid_package(self) -> Path:
        tree = self.write_tree(
            [
                {"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"},
                {"source": str(self.layout), "role": "layout", "priority": 1, "source_kind": "input_image_attachment"},
            ]
        )
        references = self.write_reference_metadata(
            [
                {"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"},
                {"source": str(self.layout), "role": "layout", "priority": 1, "source_kind": "input_image_attachment"},
            ]
        )
        package = self.root / "generation-package"
        result = self.run_script(
            "scripts/game-ui/build_generation_package.py",
            "--ui-tree",
            tree,
            "--style-profile",
            self.profile,
            "--references",
            references,
            "--output",
            package,
            "--page-purpose",
            "Resource exchange shop",
            "--reuse-component",
            "button.primary.gold",
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        return package

    def record_valid_result(self, package: Path) -> None:
        result = self.run_script(
            "scripts/game-ui/record_generation_result.py",
            "--package",
            package,
            "--output-image",
            self.output,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_ui_spec_references_are_structured_and_validated(self) -> None:
        valid = minimal_spec(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        self.assertEqual(validate_spec(valid), [])

        missing_source = minimal_spec([{"role": "style", "priority": 1}])
        invalid_role = minimal_spec([{"source": "x.png", "role": "mood", "priority": 1}])
        invalid_priority = minimal_spec([{"source": "x.png", "role": "style", "priority": "high"}])
        self.assertTrue(any("source" in error for error in validate_spec(missing_source)))
        self.assertTrue(any("role" in error for error in validate_spec(invalid_role)))
        self.assertTrue(any("priority" in error for error in validate_spec(invalid_priority)))

    def test_layout_reference_defaults_to_no_style_copy_in_ui_tree(self) -> None:
        tree = build_tree(
            minimal_spec(
                [{"source": str(self.layout), "role": "layout", "priority": 1, "source_kind": "input_image_attachment"}]
            )
        )
        reference = tree["visual"]["reference_images"][0]
        self.assertIs(reference["copy_visual_style"], False)

    def test_generation_gate_rejects_missing_style_reference(self) -> None:
        tree = self.write_tree(
            [{"source": str(self.layout), "role": "layout", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        references = self.write_reference_metadata(
            [{"source": str(self.layout), "role": "layout", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        result = self.run_script(
            "scripts/game-ui/build_generation_package.py",
            "--ui-tree",
            tree,
            "--style-profile",
            self.profile,
            "--references",
            references,
            "--output",
            self.root / "package",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("at least one style reference", (result.stderr + result.stdout).lower())

    def test_style_profile_alone_cannot_replace_style_image(self) -> None:
        tree = self.write_tree([])
        references = self.write_reference_metadata([])
        result = self.run_script(
            "scripts/game-ui/build_generation_package.py",
            "--ui-tree",
            tree,
            "--style-profile",
            self.profile,
            "--references",
            references,
            "--output",
            self.root / "package",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("at least one style reference", (result.stderr + result.stdout).lower())

    def test_valid_style_and_layout_package_records_images_hashes_and_dimensions(self) -> None:
        package = self.build_valid_package()
        manifest = json.loads((package / "reference-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual([item["role"] for item in manifest["references"]], ["style", "layout"])
        self.assertEqual(manifest["references"][0]["width"], 64)
        self.assertEqual(manifest["references"][0]["height"], 40)
        copied_style = package / manifest["references"][0]["file"]
        self.assertTrue(copied_style.is_file())
        self.assertEqual(manifest["references"][0]["sha256"], sha256_file(copied_style))
        self.assertIs(manifest["references"][1]["copy_visual_style"], False)

    def test_generation_request_separates_style_and_layout_references(self) -> None:
        package = self.build_valid_package()
        request = json.loads((package / "generation-request.json").read_text(encoding="utf-8"))
        self.assertEqual(request["style_references"], ["references/style-01.png"])
        self.assertEqual(request["layout_references"], ["references/layout-01.png"])
        self.assertEqual(request["required_capability"], "codex_builtin_image_gen")
        self.assertEqual(request["generation_backend"], "codex_builtin")
        self.assertEqual(request["credential_mode"], "codex_managed")
        self.assertEqual(request["fallback_policy"], "forbid_html_screenshot")
        prompt = (package / request["prompt_file"]).read_text(encoding="utf-8")
        self.assertIn("STYLE REFERENCES", prompt)
        self.assertIn("LAYOUT REFERENCES", prompt)
        self.assertIn("Same game.\nSame art team.\nSame UI design system.", prompt)
        self.assertIn("Do NOT copy their visual style.", prompt)
        self.assertIn("simplified CSS-like controls", prompt)

    def test_screenshot_like_style_reference_requires_explicit_user_authorization(self) -> None:
        tree = self.write_tree(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "html_screenshot"}]
        )
        references = self.write_reference_metadata(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "html_screenshot"}]
        )
        result = self.run_script(
            "scripts/game-ui/build_generation_package.py",
            "--ui-tree",
            tree,
            "--style-profile",
            self.profile,
            "--references",
            references,
            "--output",
            self.root / "package",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("user_authorized", result.stderr + result.stdout)

    def test_unavailable_image_generation_stops_without_html_fallback(self) -> None:
        package = self.build_valid_package()
        result = self.run_script("scripts/game-ui/prepare_image_generation.py", "--package", package)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout.strip(), "IMAGE_GENERATION_UNAVAILABLE")
        self.assertNotIn("html", result.stdout.lower())
        self.assertFalse((package / "generation-result.json").exists())

    def test_prepare_generation_uses_only_codex_builtin_image_gen(self) -> None:
        package = self.build_valid_package()
        result = self.run_script(
            "scripts/game-ui/prepare_image_generation.py",
            "--package",
            package,
            "--available-tool",
            "image_gen",
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["generation_backend"], "codex_builtin")
        self.assertEqual(payload["tool"], "image_gen")
        self.assertEqual(payload["credential_mode"], "codex_managed")
        self.assertEqual(len(payload["style_references"]), 1)
        self.assertEqual(len(payload["layout_references"]), 1)
        serialized = json.dumps(payload).lower()
        self.assertNotIn("openai_api_key", serialized)
        self.assertNotIn("gpt-image", serialized)
        self.assertNotIn("cli", serialized)

    def test_prepare_generation_allows_explicit_codex_provider_direct_fallback(self) -> None:
        package = self.build_valid_package()
        result = self.run_script(
            "scripts/game-ui/prepare_image_generation.py",
            "--package",
            package,
            "--allow-provider-direct",
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["generation_backend"], "codex_provider_direct")
        self.assertEqual(payload["credential_mode"], "codex_managed")
        self.assertEqual(payload["model_suffix"], "gpt-image-2")
        self.assertTrue(payload["user_authorized"])
        serialized = json.dumps(payload).lower()
        self.assertNotIn("openai_api_key", serialized)
        self.assertNotIn("bearer", serialized)

    def test_provider_direct_resolves_channel_prefixed_image_model(self) -> None:
        script = WIKI_ROOT / "scripts" / "game-ui" / "generate_with_codex_provider.py"
        sys.path.insert(0, str(script.parent))
        spec = importlib.util.spec_from_file_location("generate_with_codex_provider", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(
            module.resolve_provider_model(
                ["[EXPRESS]gemini-3-pro-image", "[l]gpt-image-2"],
                "gpt-image-2",
            ),
            "[l]gpt-image-2",
        )
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            module.resolve_provider_model(
                ["[a]gpt-image-2", "[b]gpt-image-2"],
                "gpt-image-2",
            )

    def test_provider_direct_runner_requires_explicit_user_authorization(self) -> None:
        package = self.build_valid_package()
        result = self.run_script(
            "scripts/game-ui/generate_with_codex_provider.py",
            "--package",
            package,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit user authorization", result.stderr)

    def test_generation_result_requires_a_real_output_image(self) -> None:
        package = self.build_valid_package()
        result = self.run_script(
            "scripts/game-ui/record_generation_result.py",
            "--package",
            package,
            "--output-image",
            self.root / "missing.png",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((package / "generation-result.json").exists())

    def test_ai_generated_cowart_review_requires_generation_result(self) -> None:
        package = self.build_valid_package()
        result = self.run_script(
            "scripts/cowart-ui/component-extractor/create_visual_review.py",
            "--image",
            self.output,
            "--name",
            "Exchange Shop",
            "--output-root",
            self.root / "reviews",
            "--source-type",
            "ai_generated",
            "--generation-package",
            package,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generation-result.json", result.stderr + result.stdout)

    def test_external_user_image_can_enter_cowart_review(self) -> None:
        result = self.run_script(
            "scripts/cowart-ui/component-extractor/create_visual_review.py",
            "--image",
            self.output,
            "--name",
            "External UI",
            "--output-root",
            self.root / "reviews",
            "--source-type",
            "external_source",
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        review = json.loads(Path(payload["review"]).read_text(encoding="utf-8"))
        self.assertEqual(review["source_type"], "external_source")

    def test_valid_generation_result_allows_style_review_and_cowart_review(self) -> None:
        package = self.build_valid_package()
        self.record_valid_result(package)
        style_result = self.run_script("scripts/game-ui/create_style_review.py", "--package", package)
        self.assertEqual(style_result.returncode, 0, style_result.stderr or style_result.stdout)
        style_review = json.loads((package / "style-review.json").read_text(encoding="utf-8"))
        self.assertEqual(style_review["status"], "pending_developer_review")
        self.assertEqual(
            set(style_review["checks"]),
            {
                "header_language",
                "panel_language",
                "button_language",
                "border_language",
                "shadow_language",
                "title_language",
                "icon_language",
                "spacing_rhythm",
                "visual_density",
            },
        )
        self.assertNotRegex(json.dumps(style_review), r"\b\d{1,3}%\b")

        review_result = self.run_script(
            "scripts/cowart-ui/component-extractor/create_visual_review.py",
            "--image",
            package / "outputs" / "generated-ui.png",
            "--name",
            "Generated Exchange Shop",
            "--output-root",
            self.root / "reviews",
            "--source-type",
            "ai_generated",
            "--generation-package",
            package,
        )
        self.assertEqual(review_result.returncode, 0, review_result.stderr or review_result.stdout)
        payload = json.loads(review_result.stdout)
        review = json.loads(Path(payload["review"]).read_text(encoding="utf-8"))
        self.assertEqual(review["source_type"], "ai_generated")
        self.assertEqual(review["generation"]["status"], "generated")


if __name__ == "__main__":
    unittest.main()
