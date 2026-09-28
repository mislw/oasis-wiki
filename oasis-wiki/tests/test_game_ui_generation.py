from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

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


def prepared_optimization(
    references: list[dict[str, object]],
    operation: str = "generate",
) -> dict[str, object]:
    image_references = []
    for input_index, reference in enumerate(references, start=1):
        source = Path(str(reference["source"]))
        if source.is_file():
            with Image.open(source) as image:
                width, height = image.size
            attachment = {
                "attachmentId": "sha256:" + sha256_file(source),
                "mediaType": "image/png",
                "bytes": source.stat().st_size,
                "width": width,
                "height": height,
                "name": source.name,
            }
        else:
            attachment = {
                "attachmentId": "missing-reference",
                "mediaType": "image/png",
                "bytes": 1,
                "width": 1,
                "height": 1,
                "name": source.name,
            }
        image_references.append(
            {
                "inputIndex": input_index,
                "role": reference["role"],
                "priority": reference["priority"],
                "attachment": attachment,
            }
        )
    return {
        "status": "prepared",
        "spec": {
            "schemaVersion": 1,
            "operation": operation,
            "canonicalPrompt": "## Task\nCreate an optimized game UI image.\n\n## Avoid\nwatermark",
            "references": image_references,
            "composition": ["clear information hierarchy"],
            "visualStyle": ["project-authored game UI"],
            "scene": ["resource exchange screen"],
            "exactText": [{"text": "EXCHANGE", "placement": "header", "preserveCase": True}],
            "output": {
                "width": 1280,
                "height": 720,
                "transparentBackground": False,
                "count": 1,
            },
            "preserve": ["approved icon identity"],
            "negativeConstraints": ["watermark"],
            "requiredCapabilities": ["image-generation", "exact-text"],
            "evidence": [
                {
                    "provider": "library",
                    "templateId": "game-ui",
                    "caseIds": ["exchange-shop"],
                    "visualStyleTags": ["game-ui"],
                    "sceneTags": ["shop"],
                }
            ],
            "warnings": ["fixture warning"],
        },
    }


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
            [sys.executable, "-B", str(WIKI_ROOT / relative_path), *(str(arg) for arg in args)],
            cwd=WIKI_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_child_script_does_not_write_bytecode_into_bundled_skill(self) -> None:
        result = self.run_script("scripts/game-ui/build_generation_prompt.py", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        game_ui_root = WIKI_ROOT / "scripts" / "game-ui"
        bytecode = sorted(
            path.relative_to(WIKI_ROOT).as_posix()
            for path in game_ui_root.rglob("*")
            if path.name == "__pycache__" or path.suffix == ".pyc"
        )
        self.assertEqual(bytecode, [])

    def load_provider_module(self):
        script = WIKI_ROOT / "scripts" / "game-ui" / "generate_with_codex_provider.py"
        sys.path.insert(0, str(script.parent))
        spec = importlib.util.spec_from_file_location("generate_with_codex_provider", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def write_tree(self, references: list[dict[str, object]]) -> Path:
        path = self.root / "ui-tree.json"
        write_json(path, build_tree(minimal_spec(references)))
        return path

    def write_reference_metadata(
        self,
        references: list[dict[str, object]],
        name: str = "references.json",
    ) -> Path:
        path = self.root / name
        write_json(path, {"schema_version": 1, "references": references})
        return path

    def write_optimization(
        self,
        *metadata_paths: Path,
        value: dict[str, object] | None = None,
        name: str = "optimization.json",
    ) -> Path:
        path = self.root / name
        if value is None:
            references = []
            for metadata_path in metadata_paths:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                references.extend(metadata["references"])
            value = prepared_optimization(references)
        write_json(path, value)
        return path

    def run_build_script(
        self,
        *args: object,
        optimization: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        arguments = list(args)
        if optimization is None:
            metadata_paths = []
            for flag in ("--references",):
                if flag in arguments:
                    metadata_paths.append(Path(str(arguments[arguments.index(flag) + 1])))
            optimization = self.write_optimization(*metadata_paths)
        return self.run_script(
            "scripts/game-ui/build_generation_package.py",
            *arguments,
            "--optimization",
            optimization,
        )

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
        result = self.run_build_script(
            "--ui-tree",
            tree,
            "--style-profile",
            self.profile,
            "--references",
            references,
            "--output",
            package,
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
        result = self.run_build_script(
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
        result = self.run_build_script(
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

    def test_project_library_reference_can_supply_required_style_image(self) -> None:
        library_refs = self.write_reference_metadata(
            [{
                "source": str(self.style),
                "role": "style",
                "priority": 1,
                "source_kind": "project_library_asset",
                "library": {
                    "asset_id": "redcliff.uiresources.common.icon_item.icon_item_10",
                    "preview_key": "sha256:" + sha256_file(self.style),
                    "component_ids": ["item.currency.dragon_jade"],
                    "semantic_keys": ["currency.dragon_jade"],
                    "states": ["default"],
                    "source_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
                },
            }],
            name="library-references.json",
        )
        explicit_refs = self.write_reference_metadata([], name="explicit-references.json")
        package = self.root / "library-package"

        result = self.run_build_script(
            "--ui-tree",
            self.write_tree([]),
            "--style-profile",
            self.profile,
            "--references",
            explicit_refs,
            "--library-references",
            library_refs,
            "--output",
            package,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        manifest = json.loads((package / "reference-manifest.json").read_text(encoding="utf-8"))
        reference = manifest["references"][0]
        self.assertEqual(reference["source_kind"], "project_library_asset")
        self.assertEqual(
            reference["library"]["semantic_keys"],
            ["currency.dragon_jade"],
        )
        prompt = (package / "generation-prompt.txt").read_text(encoding="utf-8")
        self.assertNotIn("currency.dragon_jade", prompt)
        self.assertNotIn("Icon_Item_10.Icon_Item_10", prompt)
        self.assertNotIn(str(self.style), prompt)

    def test_project_library_references_are_supplemental_and_reach_execution(self) -> None:
        direct_reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([direct_reference])
        library_references = self.write_reference_metadata(
            [{
                "source": str(self.layout),
                "role": "layout",
                "priority": 2,
                "source_kind": "project_library_asset",
                "library": {
                    "asset_id": "redcliff.uiresources.common.panel.exchange",
                    "preview_key": "sha256:" + sha256_file(self.layout),
                    "component_ids": [],
                    "semantic_keys": ["panel.exchange"],
                    "states": ["default"],
                    "source_asset": "/RedCliff/Asset/UIresources/Common/Panel/Exchange.Exchange",
                },
            }],
            name="supplemental-library-references.json",
        )
        package = self.root / "supplemental-library-package"

        result = self.run_build_script(
            "--ui-tree", self.write_tree([direct_reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--library-references", library_references,
            "--output", package,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        image_spec = json.loads((package / "image-spec.json").read_text(encoding="utf-8"))
        manifest = json.loads((package / "reference-manifest.json").read_text(encoding="utf-8"))
        request = json.loads((package / "generation-request.json").read_text(encoding="utf-8"))
        self.assertEqual(len(image_spec["references"]), 1)
        self.assertEqual(len(manifest["references"]), 2)
        self.assertEqual(
            request["reference_files"],
            ["references/style-01.png", "references/layout-01.png"],
        )
        prepared = self.run_script(
            "scripts/game-ui/prepare_image_generation.py",
            "--package", package,
            "--available-tool", "image_gen",
        )
        self.assertEqual(prepared.returncode, 0, prepared.stderr or prepared.stdout)
        self.assertEqual(
            json.loads(prepared.stdout)["references"],
            [str(package / path) for path in request["reference_files"]],
        )
        prompt = (package / "generation-prompt.txt").read_text(encoding="utf-8")
        self.assertNotIn("panel.exchange", prompt)

    def test_project_library_reference_rejects_preview_hash_mismatch(self) -> None:
        library_refs = self.write_reference_metadata(
            [{
                "source": str(self.style),
                "role": "style",
                "priority": 1,
                "source_kind": "project_library_asset",
                "library": {
                    "asset_id": "redcliff.uiresources.common.icon_item.icon_item_10",
                    "preview_key": "sha256:" + "0" * 64,
                    "source_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
                },
            }],
            name="library-references.json",
        )

        result = self.run_build_script(
            "--ui-tree",
            self.write_tree([]),
            "--style-profile",
            self.profile,
            "--references",
            self.write_reference_metadata([], name="explicit-references.json"),
            "--library-references",
            library_refs,
            "--output",
            self.root / "package",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("preview_key", result.stderr + result.stdout)

    def test_project_library_reference_rejects_missing_cached_file(self) -> None:
        library_refs = self.write_reference_metadata(
            [{
                "source": str(self.root / "missing.png"),
                "role": "style",
                "priority": 1,
                "source_kind": "project_library_asset",
                "library": {
                    "asset_id": "redcliff.uiresources.common.icon_item.icon_item_10",
                    "preview_key": "sha256:" + "0" * 64,
                    "source_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
                },
            }],
            name="library-references.json",
        )

        result = self.run_build_script(
            "--ui-tree",
            self.write_tree([]),
            "--style-profile",
            self.profile,
            "--references",
            self.write_reference_metadata([], name="explicit-references.json"),
            "--library-references",
            library_refs,
            "--output",
            self.root / "package",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source is not a file", result.stderr + result.stdout)

    def test_tree_reuse_requires_resolved_active_component_reference(self) -> None:
        tree = self.write_tree(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        tree_data = json.loads(tree.read_text(encoding="utf-8"))
        tree_data["components"][0]["reuse_of"] = "button.primary.gold"
        write_json(tree, tree_data)
        references = self.write_reference_metadata(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"}]
        )

        result = self.run_build_script(
            "--ui-tree", tree,
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "missing-component-package",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("resolve the component asset instead of redesigning it", result.stderr + result.stdout)

    def test_tree_reuse_is_auto_included_when_library_reference_is_resolved(self) -> None:
        tree = self.write_tree(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        tree_data = json.loads(tree.read_text(encoding="utf-8"))
        tree_data["components"][0]["reuse_of"] = "button.primary.gold"
        write_json(tree, tree_data)
        references = self.write_reference_metadata(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        library_references = self.write_reference_metadata(
            [{
                "source": str(self.style),
                "role": "style",
                "priority": 1,
                "copy_visual_style": True,
                "source_kind": "project_library_asset",
                "library": {
                    "asset_id": "redcliff.uiresources.common.btn.primary",
                    "preview_key": "sha256:" + sha256_file(self.style),
                    "component_ids": ["button.primary.gold"],
                    "semantic_keys": [],
                    "states": ["default"],
                    "source_asset": "/RedCliff/Asset/UIresources/Common/Btn/Btn1_Large.Btn1_Large",
                },
            }],
            "library-references.json",
        )
        package = self.root / "resolved-component-package"

        result = self.run_build_script(
            "--ui-tree", tree,
            "--style-profile", self.profile,
            "--references", references,
            "--library-references", library_references,
            "--output", package,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        prompt = (package / "generation-prompt.txt").read_text(encoding="utf-8")
        self.assertIn('Reusable control IDs: ["button.primary.gold"]', prompt)
        self.assertNotIn('"visual_style":', prompt)

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
        self.assertEqual(request["reference_files"], ["references/style-01.png", "references/layout-01.png"])
        self.assertEqual(request["image_spec"], "image-spec.json")
        self.assertEqual(request["oasis_constraints"], "oasis-constraints.json")
        self.assertEqual(request["required_capabilities"], ["image-generation", "exact-text"])
        self.assertEqual(request["required_capability"], "codex_builtin_image_gen")
        self.assertEqual(request["generation_backend"], "codex_builtin")
        self.assertEqual(request["credential_mode"], "codex_managed")
        self.assertEqual(request["fallback_policy"], "forbid_html_screenshot")
        prompt = (package / request["prompt_file"]).read_text(encoding="utf-8")
        self.assertTrue(prompt.startswith("## Task\nCreate an optimized game UI image."))
        self.assertIn("## Oasis UI constraints", prompt)
        self.assertIn("runtime-native", prompt)
        self.assertIn("Cowart", prompt)
        self.assertNotIn('"source":', prompt)
        self.assertNotIn("STYLE PROFILE", prompt)
        self.assertNotIn("Same art team.", prompt)
        self.assertNotIn("simplified CSS-like controls", prompt)

    def test_generation_package_requires_prepared_optimization_result(self) -> None:
        references = self.write_reference_metadata(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "input_image_attachment"}]
        )
        optimization = self.write_optimization(
            value={"status": "needs_clarification", "issues": []},
            name="needs-clarification.json",
        )

        result = self.run_build_script(
            "--ui-tree", self.write_tree(json.loads(references.read_text(encoding="utf-8"))["references"]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "clarification-package",
            optimization=optimization,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prepared", (result.stderr + result.stdout).lower())

    def test_generation_package_rejects_wrong_image_spec_schema_version(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        optimization_value["spec"]["schemaVersion"] = 2
        optimization = self.write_optimization(
            value=optimization_value,
            name="schema-version-2.json",
        )

        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "schema-version-package",
            optimization=optimization,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schemaversion", (result.stderr + result.stdout).lower())

    def test_oasis_constraints_extend_canonical_spec_without_reselecting_generic_guidance(self) -> None:
        package = self.build_valid_package()
        image_spec = json.loads((package / "image-spec.json").read_text(encoding="utf-8"))
        expected = prepared_optimization(
            [
                {"source": str(self.style), "role": "style", "priority": 1},
                {"source": str(self.layout), "role": "layout", "priority": 1},
            ]
        )["spec"]
        self.assertEqual(image_spec, expected)

        constraints = json.loads((package / "oasis-constraints.json").read_text(encoding="utf-8"))
        self.assertIs(constraints["dynamicText"], True)
        self.assertIs(constraints["dynamicNumbers"], True)
        self.assertIs(constraints["dynamicProgress"], True)
        self.assertIs(constraints["hitTargets"], True)
        self.assertEqual(constraints["uiTree"]["artifact_type"], "ui_tree")
        self.assertIn("button.primary.gold", constraints["reusableControls"])
        self.assertFalse(constraints["editorWriteRestrictions"]["authorized"])
        self.assertEqual(
            constraints["cowartReviewStages"],
            ["style_validation", "visual_review", "component_extraction", "component_confirmation"],
        )
        serialized = json.dumps({"imageSpec": image_spec, "oasisConstraints": constraints})
        self.assertNotIn("templateSelection", serialized)
        self.assertNotIn("caseSelection", serialized)

    def test_generation_prompt_preserves_canonical_prompt_bytes_before_oasis_appendix(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        canonical_prompt = "## Task\nPreserve this exact prompt.  \n"
        optimization_value["spec"]["canonicalPrompt"] = canonical_prompt
        optimization = self.write_optimization(
            value=optimization_value,
            name="exact-canonical-prompt.json",
        )
        package = self.root / "exact-canonical-package"

        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", package,
            optimization=optimization,
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        prompt = (package / "generation-prompt.txt").read_text(encoding="utf-8")
        self.assertEqual(prompt[:len(canonical_prompt)], canonical_prompt)

    def test_generation_package_preserves_optimizer_operation_variants(self) -> None:
        cases = (
            ("generate", "style"),
            ("edit", "edit-target"),
            ("variation", "content"),
        )
        for operation, role in cases:
            with self.subTest(operation=operation, role=role):
                reference = {
                    "source": str(self.style),
                    "role": role,
                    "priority": 1,
                    "source_kind": "input_image_attachment",
                }
                references = self.write_reference_metadata(
                    [reference],
                    name=f"{operation}-references.json",
                )
                optimization = self.write_optimization(
                    value=prepared_optimization([reference], operation),
                    name=f"{operation}-optimization.json",
                )
                package = self.root / f"{operation}-package"
                result = self.run_build_script(
                    "--ui-tree", self.write_tree([reference] if role in {"style", "layout"} else []),
                    "--style-profile", self.profile,
                    "--references", references,
                    "--output", package,
                    optimization=optimization,
                )
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                image_spec = json.loads((package / "image-spec.json").read_text(encoding="utf-8"))
                self.assertEqual(image_spec["operation"], operation)
                attachment_id = image_spec["references"][0]["attachment"]["attachmentId"]
                self.assertEqual(attachment_id, "sha256:" + sha256_file(self.style))
                manifest = json.loads((package / "reference-manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["references"][0]["attachment"]["attachmentId"], attachment_id)
                self.assertEqual(manifest["references"][0]["sha256"], sha256_file(self.style))

    def test_generation_package_preserves_multiple_roles_for_one_input_ordinal(self) -> None:
        style_reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 50,
            "source_kind": "input_image_attachment",
        }
        target_reference = {
            "source": str(self.style),
            "role": "edit-target",
            "priority": 100,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata(
            [style_reference, target_reference],
            name="shared-ordinal-references.json",
        )
        optimization_value = prepared_optimization(
            [style_reference, target_reference],
            "edit",
        )
        optimization_value["spec"]["references"][1]["inputIndex"] = 1
        package = self.root / "shared-ordinal-package"

        result = self.run_build_script(
            "--ui-tree", self.write_tree([style_reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", package,
            optimization=self.write_optimization(value=optimization_value),
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        image_spec = json.loads((package / "image-spec.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [(item["inputIndex"], item["role"]) for item in image_spec["references"]],
            [(1, "style"), (1, "edit-target")],
        )
        manifest = json.loads((package / "reference-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [(item["input_index"], item["role"]) for item in manifest["references"]],
            [(1, "style"), (1, "edit-target")],
        )
        self.assertEqual(
            {item["attachment"]["attachmentId"] for item in manifest["references"]},
            {"sha256:" + sha256_file(self.style)},
        )

    def test_prepared_image_spec_rejects_invalid_operation_reference_combinations(self) -> None:
        style_reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 50,
            "source_kind": "input_image_attachment",
        }
        target_reference = {
            "source": str(self.style),
            "role": "edit-target",
            "priority": 100,
            "source_kind": "input_image_attachment",
        }
        second_target_reference = {
            "source": str(self.layout),
            "role": "edit-target",
            "priority": 90,
            "source_kind": "input_image_attachment",
        }
        cases = (
            ("edit-without-target", "edit", [style_reference], "exactly one edit-target"),
            (
                "edit-with-multiple-targets",
                "edit",
                [target_reference, second_target_reference],
                "exactly one edit-target",
            ),
            (
                "variation-with-target",
                "variation",
                [target_reference],
                "must not contain an edit-target",
            ),
            (
                "variation-without-content",
                "variation",
                [style_reference],
                "at least one content reference",
            ),
        )
        for name, operation, source_references, error_text in cases:
            with self.subTest(name=name):
                references = self.write_reference_metadata(
                    source_references,
                    name=f"{name}-references.json",
                )
                optimization = self.write_optimization(
                    value=prepared_optimization(source_references, operation),
                    name=f"{name}-optimization.json",
                )
                result = self.run_build_script(
                    "--ui-tree",
                    self.write_tree(
                        [
                            reference
                            for reference in source_references
                            if reference["role"] in {"style", "layout"}
                        ]
                    ),
                    "--style-profile", self.profile,
                    "--references", references,
                    "--output", self.root / f"{name}-package",
                    optimization=optimization,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(error_text, result.stderr + result.stdout)

    def test_generation_package_rejects_local_reference_metadata_that_does_not_match_attachment(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        optimization_value["spec"]["references"][0]["attachment"]["bytes"] += 1
        optimization = self.write_optimization(
            value=optimization_value,
            name="wrong-attachment.json",
        )

        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "wrong-attachment-package",
            optimization=optimization,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("attachment", (result.stderr + result.stdout).lower())

    def test_generation_package_rejects_malformed_output(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        invalid_outputs = (
            {"width": 1280, "transparentBackground": False, "count": 1},
            {"aspectRatio": "4:2", "transparentBackground": False, "count": 1},
            {"width": 1280, "height": 720, "aspectRatio": "1:1", "transparentBackground": False, "count": 1},
        )
        for index, output in enumerate(invalid_outputs):
            with self.subTest(output=output):
                optimization_value = prepared_optimization([reference])
                optimization_value["spec"]["output"] = output
                result = self.run_build_script(
                    "--ui-tree", self.write_tree([reference]),
                    "--style-profile", self.profile,
                    "--references", references,
                    "--output", self.root / f"malformed-output-{index}",
                    optimization=self.write_optimization(
                        value=optimization_value,
                        name=f"malformed-output-{index}.json",
                    ),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("output", (result.stderr + result.stdout).lower())

    def test_generation_package_rejects_malformed_evidence(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        invalid_evidence = (
            {"provider": "library", "caseIds": [], "visualStyleTags": [], "sceneTags": "shop"},
            {"provider": "", "caseIds": [], "visualStyleTags": [], "sceneTags": []},
        )
        for index, evidence in enumerate(invalid_evidence):
            with self.subTest(evidence=evidence):
                optimization_value = prepared_optimization([reference])
                optimization_value["spec"]["evidence"] = [evidence]
                result = self.run_build_script(
                    "--ui-tree", self.write_tree([reference]),
                    "--style-profile", self.profile,
                    "--references", references,
                    "--output", self.root / f"malformed-evidence-{index}",
                    optimization=self.write_optimization(
                        value=optimization_value,
                        name=f"malformed-evidence-{index}.json",
                    ),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("evidence", (result.stderr + result.stdout).lower())

    def test_generation_package_rejects_non_integer_priority(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        optimization_value["spec"]["references"][0]["priority"] = 1.5
        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "non-integer-priority-package",
            optimization=self.write_optimization(value=optimization_value),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("priority", (result.stderr + result.stdout).lower())

    def test_generation_package_rejects_unsupported_attachment_media_type(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        optimization_value["spec"]["references"][0]["attachment"]["mediaType"] = "image/bmp"
        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "unsupported-media-type-package",
            optimization=self.write_optimization(value=optimization_value),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mediatype", (result.stderr + result.stdout).lower())

    def test_generation_package_rejects_non_string_enum_fields(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        mutations = (
            ("operation", lambda result: result["spec"].update({"operation": []})),
            ("role", lambda result: result["spec"]["references"][0].update({"role": []})),
            (
                "mediaType",
                lambda result: result["spec"]["references"][0]["attachment"].update({"mediaType": []}),
            ),
        )
        for index, (label, mutate) in enumerate(mutations):
            with self.subTest(label=label):
                optimization_value = prepared_optimization([reference])
                mutate(optimization_value)
                result = self.run_build_script(
                    "--ui-tree", self.write_tree([reference]),
                    "--style-profile", self.profile,
                    "--references", references,
                    "--output", self.root / f"non-string-enum-{index}",
                    optimization=self.write_optimization(
                        value=optimization_value,
                        name=f"non-string-enum-{index}.json",
                    ),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(label.lower(), (result.stderr + result.stdout).lower())

    def test_generation_package_accepts_declared_optional_schema_fields(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        attachment = optimization_value["spec"]["references"][0]["attachment"]
        attachment["originalDimensions"] = {"width": 128, "height": 80}
        optimization_value["spec"]["output"]["aspectRatio"] = "16:9"
        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", self.root / "optional-schema-fields-package",
            optimization=self.write_optimization(value=optimization_value),
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_generation_package_accepts_and_preserves_spaced_aspect_ratio(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        optimization_value = prepared_optimization([reference])
        optimization_value["spec"]["output"]["aspectRatio"] = " 16:9 "
        package = self.root / "spaced-aspect-ratio-package"
        result = self.run_build_script(
            "--ui-tree", self.write_tree([reference]),
            "--style-profile", self.profile,
            "--references", references,
            "--output", package,
            optimization=self.write_optimization(value=optimization_value),
        )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        image_spec = json.loads((package / "image-spec.json").read_text(encoding="utf-8"))
        self.assertEqual(image_spec["output"]["aspectRatio"], " 16:9 ")

    def test_generation_package_rejects_undeclared_schema_fields(self) -> None:
        reference = {
            "source": str(self.style),
            "role": "style",
            "priority": 1,
            "source_kind": "input_image_attachment",
        }
        references = self.write_reference_metadata([reference])
        mutations = (
            ("result", lambda result: result.update({"extra": True})),
            ("spec", lambda result: result["spec"].update({"extra": True})),
            ("reference", lambda result: result["spec"]["references"][0].update({"extra": True})),
            ("attachment", lambda result: result["spec"]["references"][0]["attachment"].update({"extra": True})),
            ("exactText", lambda result: result["spec"]["exactText"][0].update({"extra": True})),
            ("output", lambda result: result["spec"]["output"].update({"extra": True})),
            ("evidence", lambda result: result["spec"]["evidence"][0].update({"extra": True})),
        )
        for index, (label, mutate) in enumerate(mutations):
            with self.subTest(label=label):
                optimization_value = prepared_optimization([reference])
                mutate(optimization_value)
                result = self.run_build_script(
                    "--ui-tree", self.write_tree([reference]),
                    "--style-profile", self.profile,
                    "--references", references,
                    "--output", self.root / f"extra-field-{index}",
                    optimization=self.write_optimization(
                        value=optimization_value,
                        name=f"extra-field-{index}.json",
                    ),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("undeclared", (result.stderr + result.stdout).lower())

    def test_screenshot_like_style_reference_requires_explicit_user_authorization(self) -> None:
        tree = self.write_tree(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "html_screenshot"}]
        )
        references = self.write_reference_metadata(
            [{"source": str(self.style), "role": "style", "priority": 1, "source_kind": "html_screenshot"}]
        )
        result = self.run_build_script(
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
        module = self.load_provider_module()
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

    def test_provider_direct_discovers_image_model_candidates(self) -> None:
        module = self.load_provider_module()
        candidates = module.discover_image_model_candidates(
            [
                {
                    "id": "vendor-image-edit",
                    "capabilities": {"image_generation": True, "image_edit": True},
                },
                {"id": "[l]gpt-image-2"},
                {"id": "vision-model", "modalities": ["text", "image"]},
                {"id": "gpt-5.6-sol", "capabilities": {"text": True}},
            ]
        )

        self.assertEqual(
            [(candidate.model_id, candidate.confidence) for candidate in candidates],
            [
                ("vendor-image-edit", "confirmed"),
                ("[l]gpt-image-2", "likely"),
                ("vision-model", "uncertain"),
            ],
        )
        self.assertIn("capability:image_generation", candidates[0].evidence)
        self.assertIn("model_id:gpt-image", candidates[1].evidence)
        self.assertIn("modality:image", candidates[2].evidence)

    def test_provider_direct_confirms_explicit_image_output_metadata(self) -> None:
        module = self.load_provider_module()
        candidates = module.discover_image_model_candidates(
            [
                {"id": "endpoint-model", "endpoints": ["/v1/images/generations"]},
                {"id": "output-model", "output_modalities": ["image"]},
                {"id": "text-image-model", "capabilities": {"text_to_image": True}},
            ]
        )

        self.assertEqual(
            [(candidate.model_id, candidate.confidence) for candidate in candidates],
            [
                ("endpoint-model", "confirmed"),
                ("output-model", "confirmed"),
                ("text-image-model", "confirmed"),
            ],
        )
        self.assertIn("endpoint:/v1/images/generations", candidates[0].evidence)
        self.assertIn("output_modality:image", candidates[1].evidence)
        self.assertIn("capability:text_to_image", candidates[2].evidence)

    def test_provider_direct_discovery_merges_configured_models(self) -> None:
        module = self.load_provider_module()
        candidates = module.discover_image_model_candidates(
            [{"id": "text-only"}],
            configured_models=("flux-pro", "flux-pro"),
        )

        self.assertEqual(
            [(candidate.model_id, candidate.confidence) for candidate in candidates],
            [("flux-pro", "likely")],
        )
        self.assertIn("configured_model", candidates[0].evidence)

    def test_provider_direct_discovery_cli_is_read_only(self) -> None:
        module = self.load_provider_module()
        connection = module.ProviderConnection(
            base_url="https://provider.example/v1",
            api_key="managed-secret",
            configured_models=("[l]gpt-image-2",),
            source="codex",
        )
        stdout = io.StringIO()

        with (
            mock.patch.object(sys, "argv", ["generate_with_codex_provider.py", "--discover-image-models"]),
            mock.patch.object(module, "load_configured_provider", return_value=connection),
            mock.patch.object(
                module,
                "list_provider_model_records",
                return_value=[{"id": "[l]gpt-image-2"}],
            ),
            mock.patch.object(
                module,
                "create_image_edit",
                side_effect=AssertionError("discovery must not generate"),
            ),
            redirect_stdout(stdout),
        ):
            exit_code = module.main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertFalse(payload["generation_attempted"])
        self.assertTrue(payload["selection_required"])
        self.assertEqual(payload["provider_source"], "codex")
        self.assertEqual(payload["provider_host"], "provider.example")
        self.assertEqual(payload["candidates"][0]["model_id"], "[l]gpt-image-2")
        self.assertNotIn("managed-secret", stdout.getvalue())

    def test_provider_direct_falls_back_to_dsh_profile(self) -> None:
        module = self.load_provider_module()
        codex_home = self.root / "codex-home"
        codex_home.mkdir()
        (codex_home / "config.toml").write_text('model = "gpt-5.6-sol"\n', encoding="utf-8")
        write_json(codex_home / "auth.json", {})
        dsh_home = self.root / "dsh-home"
        dsh_home.mkdir()
        (dsh_home / "settings.yaml").write_text(
            """llm-pi-ai:
  providers:
    chirei:
      apiKeyEnv: CHIREI_API_KEY
      baseURL: https://proxy.example/v1
      models:
        - id: "[l]gpt-5.6-sol"
        - id: "[l]gpt-image-2"
agent-default-model:
  provider: chirei
  model: "[l]gpt-5.6-sol"
""",
            encoding="utf-8",
        )
        (dsh_home / ".credentials.yaml").write_text(
            "CHIREI_API_KEY: dsh-test-secret\n",
            encoding="utf-8",
        )

        connection = module.load_configured_provider(codex_home, dsh_home)

        self.assertEqual(connection.base_url, "https://proxy.example/v1")
        self.assertEqual(connection.api_key, "dsh-test-secret")
        self.assertEqual(connection.configured_models, ("[l]gpt-5.6-sol", "[l]gpt-image-2"))
        self.assertEqual(connection.source, "dsh")

    def test_provider_direct_prefers_complete_codex_provider(self) -> None:
        module = self.load_provider_module()
        codex_home = self.root / "codex-home"
        codex_home.mkdir()
        (codex_home / "config.toml").write_text(
            'model_provider = "custom"\n[model_providers.custom]\nbase_url = "https://codex.example/v1"\n',
            encoding="utf-8",
        )
        write_json(codex_home / "auth.json", {"OPENAI_API_KEY": "codex-test-secret"})
        dsh_home = self.root / "dsh-home"
        dsh_home.mkdir()
        (dsh_home / "settings.yaml").write_text(
            """llm-pi-ai:
  providers:
    chirei:
      apiKeyEnv: CHIREI_API_KEY
      baseURL: https://proxy.example/v1
      models:
        - id: "[l]gpt-image-2"
agent-default-model:
  provider: chirei
""",
            encoding="utf-8",
        )
        (dsh_home / ".credentials.yaml").write_text(
            "CHIREI_API_KEY: dsh-test-secret\n",
            encoding="utf-8",
        )

        connection = module.load_configured_provider(codex_home, dsh_home)

        self.assertEqual(connection.base_url, "https://codex.example/v1")
        self.assertEqual(connection.api_key, "codex-test-secret")
        self.assertEqual(connection.source, "codex")

    def test_provider_direct_missing_dsh_credential_is_secret_safe(self) -> None:
        module = self.load_provider_module()
        codex_home = self.root / "codex-home"
        codex_home.mkdir()
        (codex_home / "config.toml").write_text('model = "gpt-5.6-sol"\n', encoding="utf-8")
        write_json(codex_home / "auth.json", {})
        dsh_home = self.root / "dsh-home"
        dsh_home.mkdir()
        (dsh_home / "settings.yaml").write_text(
            """llm-pi-ai:
  providers:
    chirei:
      apiKeyEnv: CHIREI_API_KEY
      baseURL: https://proxy.example/v1
      models:
        - id: "[l]gpt-image-2"
agent-default-model:
  provider: chirei
""",
            encoding="utf-8",
        )
        (dsh_home / ".credentials.yaml").write_text(
            "OTHER_KEY: should-never-appear\n",
            encoding="utf-8",
        )

        with self.assertRaises(module.GenerationPipelineError) as caught:
            module.load_configured_provider(codex_home, dsh_home)

        message = str(caught.exception)
        self.assertIn("CHIREI_API_KEY", message)
        self.assertNotIn("should-never-appear", message)

    def test_provider_direct_uses_dependency_free_multi_image_transport(self) -> None:
        module = self.load_provider_module()
        generated_bytes = self.output.read_bytes()
        captured: dict[str, object] = {}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                return

            def do_GET(self) -> None:
                captured["get_path"] = self.path
                captured["get_authorization"] = self.headers.get("Authorization")
                payload = json.dumps({"data": [{"id": "[l]gpt-image-2"}]}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                captured["post_path"] = self.path
                captured["post_authorization"] = self.headers.get("Authorization")
                captured["post_content_type"] = self.headers.get("Content-Type")
                captured["post_body"] = self.rfile.read(length)
                payload = json.dumps(
                    {"data": [{"b64_json": __import__("base64").b64encode(generated_bytes).decode("ascii")}]}
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            connection = module.ProviderConnection(
                base_url=f"http://127.0.0.1:{server.server_port}/v1",
                api_key="transport-test-secret",
                configured_models=("[l]gpt-image-2",),
                source="dsh",
            )
            models = module.list_provider_models(connection)
            model = module.resolve_provider_model(models, "gpt-image-2")
            response = module.create_image_edit(
                connection,
                model,
                "Generate a matching game UI.",
                [self.style, self.layout],
                "auto",
                "high",
            )
            output = self.root / "transport-output.png"
            module.save_image_response(response["data"][0], output)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        body = captured["post_body"]
        self.assertIsInstance(body, bytes)
        self.assertEqual(captured["get_path"], "/v1/models")
        self.assertEqual(captured["post_path"], "/v1/images/edits")
        self.assertEqual(captured["get_authorization"], "Bearer transport-test-secret")
        self.assertEqual(captured["post_authorization"], "Bearer transport-test-secret")
        self.assertIn("multipart/form-data; boundary=", str(captured["post_content_type"]))
        self.assertEqual(body.count(b'name="image[]"'), 2)
        self.assertIn(b'name="model"', body)
        self.assertIn(b"[l]gpt-image-2", body)
        self.assertIn(b'name="prompt"', body)
        self.assertEqual(output.read_bytes(), generated_bytes)

    def test_provider_direct_http_errors_are_bounded_and_secret_safe(self) -> None:
        module = self.load_provider_module()
        secret = "http-error-test-secret"

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                return

            def do_GET(self) -> None:
                payload = (secret + ":" + ("x" * 2000)).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            connection = module.ProviderConnection(
                base_url=f"http://127.0.0.1:{server.server_port}/v1",
                api_key=secret,
                configured_models=("[l]gpt-image-2",),
                source="dsh",
            )
            with self.assertRaises(module.GenerationPipelineError) as caught:
                module.list_provider_models(connection)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        message = str(caught.exception)
        self.assertNotIn(secret, message)
        self.assertIn("HTTP 500", message)
        self.assertLess(len(message), 800)

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
