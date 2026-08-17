from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path, PurePosixPath

from PIL import Image


WIKI_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = WIKI_ROOT / "scripts" / "game-ui"
sys.path.insert(0, str(SCRIPT_DIR))

from project_library import (  # type: ignore  # noqa: E402
    ProjectLibraryError,
    preview_path_for_key,
    validate_asset_catalog,
    validate_component_asset_catalog,
    validate_item_icon_catalog,
    validate_project_library,
)
from index_project_assets import asset_id_for, build_asset_catalog  # type: ignore  # noqa: E402
from import_project_previews import (  # type: ignore  # noqa: E402
    build_contact_sheet,
    group_assets_by_categories,
    import_previews,
)
from build_item_icon_catalog import build_item_icon_catalog  # type: ignore  # noqa: E402
from initialize_project_library import initialize_library  # type: ignore  # noqa: E402
from resolve_project_references import resolve_project_references  # type: ignore  # noqa: E402


PREVIEW_KEY = "sha256:" + "0" * 64
ASSET_ID = "redcliff.uiresources.common.icon_item.icon_item_10"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def minimal_profile(status: str = "active") -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": {"name": "RedCliff", "slug": "redcliff", "aliases": []},
        "style_guide": {},
        "components": [{
            "component_id": "button.primary.gold",
            "name": "Primary Button",
            "category": "button",
            "description": "Primary action",
            "states": ["default"],
            "parent_types": ["panel"],
            "layer": 60,
            "reusable": True,
            "confidence": 1.0,
            "status": status,
            "version": 1,
            "confirmed_by": "developer" if status == "active" else None,
        }],
        "pages": [],
        "history": [],
    }


def minimal_asset_catalog() -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": {"name": "RedCliff", "slug": "redcliff"},
        "assets": [{
            "asset_id": ASSET_ID,
            "source_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
            "source_file": "Asset/UIresources/Common/Icon_Item/Icon_Item_10.uasset",
            "category": "Common/Icon_Item",
            "catalog_status": "previewed",
            "preview_key": PREVIEW_KEY,
            "preview_source": "asset_export",
        }],
    }


def minimal_item_icon_catalog() -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": {"name": "RedCliff", "slug": "redcliff"},
        "items": [{
            "semantic_key": "currency.dragon_jade",
            "item_id": 1001,
            "name": "Dragon Jade",
            "description": "Premium currency",
            "icon_asset": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
            "asset_id": ASSET_ID,
            "aliases": ["CommodityCoin"],
            "source_table": "Asset/Data/Table/UGCObject",
            "row_fingerprint": "sha256:" + "1" * 64,
            "resolution_status": "resolved",
        }],
    }


def ugcobject_export(values: dict[str, object], row_name: str = "1001") -> dict[str, object]:
    return {
        "schema_version": 1,
        "load_path": "/RedCliff/Asset/Data/Table/UGCObject.UGCObject",
        "rows": [{
            "row_name": row_name,
            "values": values,
        }],
    }


def minimal_component_asset_catalog() -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": {"name": "RedCliff", "slug": "redcliff"},
        "components": [{
            "component_id": "button.primary.gold",
            "states": {"default": [ASSET_ID]},
        }],
    }


class GameUiProjectLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.project_root = self.root / "RedCliff"
        self.library_root = self.project_root / ".game-ui-system"
        self.cache_root = self.root / "cache"
        self.staging = self.root / "staging"
        self.staging.mkdir()
        source = self.project_root / "Asset/UIresources/Common/Icon_Item/Icon_Item_10.uasset"
        source.parent.mkdir(parents=True)
        source.write_bytes(b"synthetic-uasset")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_valid_library(self) -> None:
        write_json(self.library_root / "profile.json", minimal_profile())
        write_json(self.library_root / "catalogs/assets.json", minimal_asset_catalog())
        write_json(self.library_root / "catalogs/item-icons.json", minimal_item_icon_catalog())
        write_json(
            self.library_root / "catalogs/component-assets.json",
            minimal_component_asset_catalog(),
        )
        preview = preview_path_for_key(self.cache_root, PREVIEW_KEY)
        preview.parent.mkdir(parents=True)
        preview.write_bytes(b"cached-preview")

    def test_asset_catalog_rejects_machine_absolute_source_file(self) -> None:
        catalog = minimal_asset_catalog()
        catalog["assets"][0]["source_file"] = r"E:\private\Icon.uasset"
        self.assertIn(
            "source_file must be project-relative",
            "\n".join(validate_asset_catalog(catalog, self.project_root)),
        )

    def test_asset_catalog_rejects_duplicate_ids_and_invalid_preview_keys(self) -> None:
        catalog = minimal_asset_catalog()
        duplicate = dict(catalog["assets"][0])
        duplicate["preview_key"] = "sha256:not-a-digest"
        catalog["assets"].append(duplicate)
        errors = validate_asset_catalog(catalog, self.project_root)
        self.assertTrue(any("duplicate asset_id" in error for error in errors))
        self.assertTrue(any("preview_key is invalid" in error for error in errors))

    def test_asset_catalog_rejects_non_normalized_unreal_path(self) -> None:
        catalog = minimal_asset_catalog()
        catalog["assets"][0]["source_asset"] = r"\RedCliff\Asset\Icon.Icon"
        errors = validate_asset_catalog(catalog, self.project_root)
        self.assertTrue(any("source_asset must be a normalized Unreal object path" in error for error in errors))

    def test_item_catalog_rejects_duplicate_item_ids_and_missing_assets(self) -> None:
        catalog = minimal_item_icon_catalog()
        duplicate = dict(catalog["items"][0])
        duplicate["semantic_key"] = "currency.dragon_jade_duplicate"
        duplicate["asset_id"] = "redcliff.uiresources.missing.icon"
        catalog["items"].append(duplicate)
        errors = validate_item_icon_catalog(catalog, minimal_asset_catalog())
        self.assertTrue(any("duplicate item_id" in error for error in errors))
        self.assertTrue(any("references missing asset_id" in error for error in errors))

    def test_item_catalog_rejects_absolute_paths_anywhere(self) -> None:
        catalog = minimal_item_icon_catalog()
        catalog["items"][0]["aliases"].append(r"C:\private\alias")
        errors = validate_item_icon_catalog(catalog, minimal_asset_catalog())
        self.assertTrue(any("machine-specific absolute path" in error for error in errors))

    def test_item_catalog_rejects_posix_absolute_paths_anywhere(self) -> None:
        catalog = minimal_item_icon_catalog()
        catalog["items"][0]["aliases"].append("/opt/private/alias")
        errors = validate_item_icon_catalog(catalog, minimal_asset_catalog())
        self.assertTrue(any("machine-specific absolute path" in error for error in errors))

    def test_component_catalog_requires_known_profile_component(self) -> None:
        profile = minimal_profile()
        profile["components"] = []
        errors = validate_component_asset_catalog(
            minimal_component_asset_catalog(), minimal_asset_catalog(), profile
        )
        self.assertTrue(any("missing from profile" in error for error in errors))

    def test_component_catalog_allows_pending_component_for_review(self) -> None:
        errors = validate_component_asset_catalog(
            minimal_component_asset_catalog(), minimal_asset_catalog(), minimal_profile("pending_review")
        )
        self.assertEqual(errors, [])

    def test_component_catalog_rejects_missing_asset_reference(self) -> None:
        catalog = minimal_component_asset_catalog()
        catalog["components"][0]["states"]["default"] = ["redcliff.uiresources.missing.icon"]
        errors = validate_component_asset_catalog(catalog, minimal_asset_catalog(), minimal_profile())
        self.assertTrue(any("references missing asset_id" in error for error in errors))

    def test_complete_project_library_validates_with_cache(self) -> None:
        self.write_valid_library()
        self.assertEqual(
            validate_project_library(self.library_root, self.project_root, self.cache_root),
            [],
        )

    def test_complete_project_library_reports_missing_cached_preview(self) -> None:
        self.write_valid_library()
        preview_path_for_key(self.cache_root, PREVIEW_KEY).unlink()
        errors = validate_project_library(self.library_root, self.project_root, self.cache_root)
        self.assertTrue(any("cached preview is missing" in error for error in errors))

    def test_complete_project_library_rejects_invalid_profile_schema(self) -> None:
        self.write_valid_library()
        profile = minimal_profile()
        profile["schema_version"] = 2
        write_json(self.library_root / "profile.json", profile)
        errors = validate_project_library(self.library_root, self.project_root, self.cache_root)
        self.assertIn("profile.schema_version must be 1", errors)

    def test_complete_project_library_rejects_absolute_path_in_profile(self) -> None:
        self.write_valid_library()
        profile = minimal_profile()
        profile["style_guide"] = {"source": r"C:\private\style.png"}
        write_json(self.library_root / "profile.json", profile)
        errors = validate_project_library(self.library_root, self.project_root, self.cache_root)
        self.assertTrue(any("profile" in error and "absolute path" in error for error in errors))

    def test_validation_cli_prints_one_error_per_line(self) -> None:
        self.write_valid_library()
        assets = minimal_asset_catalog()
        assets["assets"][0]["source_file"] = r"E:\private\Icon.uasset"
        write_json(self.library_root / "catalogs/assets.json", assets)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_project_library.py"),
                "--project-root",
                str(self.project_root),
                "--library-root",
                str(self.library_root),
                "--cache-root",
                str(self.cache_root),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        lines = [line for line in result.stdout.splitlines() if line]
        self.assertTrue(lines)
        self.assertTrue(all(line.startswith("ERROR: ") for line in lines))

    def test_initialize_library_creates_valid_empty_manifests(self) -> None:
        source_profile = self.root / "source-profile.json"
        write_json(source_profile, minimal_profile())
        library = initialize_library(self.project_root, source_profile)
        self.assertEqual(library, self.library_root)
        self.assertEqual(
            json.loads((library / "catalogs/assets.json").read_text(encoding="utf-8"))["assets"],
            [],
        )
        self.assertEqual(
            json.loads((library / "catalogs/item-icons.json").read_text(encoding="utf-8"))["items"],
            [],
        )
        self.assertEqual(
            json.loads((library / "catalogs/component-assets.json").read_text(encoding="utf-8"))["components"],
            [],
        )
        self.assertTrue((library / "history/catalog-history.jsonl").is_file())

    def test_initialize_library_rejects_invalid_source_profile(self) -> None:
        source_profile = self.root / "source-profile.json"
        profile = minimal_profile("active")
        profile["components"][0]["confirmed_by"] = None
        write_json(source_profile, profile)
        with self.assertRaisesRegex(ValueError, "source profile is invalid"):
            initialize_library(self.project_root, source_profile)

    def test_scanner_indexes_uasset_without_absolute_paths(self) -> None:
        asset = self.project_root / "Asset/UIresources/Common/Btn_Confirm_Normal.uasset"
        asset.parent.mkdir(parents=True, exist_ok=True)
        asset.write_bytes(b"synthetic-button")
        catalog, history = build_asset_catalog(self.project_root, "redcliff", None)
        entry = next(item for item in catalog["assets"] if item["source_file"].endswith("Btn_Confirm_Normal.uasset"))
        self.assertEqual(entry["source_file"], "Asset/UIresources/Common/Btn_Confirm_Normal.uasset")
        self.assertEqual(entry["catalog_status"], "indexed")
        self.assertEqual(entry["classification_suggestion"]["state"], "default")
        self.assertNotIn(str(self.project_root), json.dumps(catalog))
        self.assertTrue(any(item["action"] == "asset_added" and item["asset_id"] == entry["asset_id"] for item in history))

    def test_scanner_builds_stable_asset_and_unreal_paths(self) -> None:
        catalog, _ = build_asset_catalog(self.project_root, "redcliff", None)
        entry = catalog["assets"][0]
        self.assertEqual(entry["asset_id"], ASSET_ID)
        self.assertEqual(
            entry["source_asset"],
            "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        )
        self.assertRegex(entry["source_sha256"], r"^[0-9a-f]{64}$")

    def test_scanner_prefixes_numeric_asset_path_segments(self) -> None:
        self.assertEqual(
            asset_id_for(PurePosixPath("Tutorial/2"), "redcliff"),
            "redcliff.uiresources.tutorial.n_2",
        )

    def test_scanner_assigns_root_category_to_top_level_asset(self) -> None:
        asset = self.project_root / "Asset/UIresources/CdMask.uasset"
        asset.write_bytes(b"synthetic-root-asset")
        catalog, _ = build_asset_catalog(self.project_root, "redcliff", None)
        entry = next(item for item in catalog["assets"] if item["source_file"].endswith("CdMask.uasset"))
        self.assertEqual(entry["category"], "root")
        self.assertEqual(validate_asset_catalog(catalog, self.project_root), [])

    def test_rescan_records_changed_and_removed_assets(self) -> None:
        first, _ = build_asset_catalog(self.project_root, "redcliff", None)
        self.assertEqual(len(first["assets"]), 1)
        source = self.project_root / first["assets"][0]["source_file"]
        source.write_bytes(b"changed")
        second, changed_history = build_asset_catalog(self.project_root, "redcliff", first)
        self.assertEqual([item["action"] for item in changed_history], ["asset_changed"])
        source.unlink()
        _, removed_history = build_asset_catalog(self.project_root, "redcliff", second)
        self.assertEqual([item["action"] for item in removed_history], ["asset_removed"])

    def test_rescan_preserves_reviewed_classification_for_unchanged_asset(self) -> None:
        first, _ = build_asset_catalog(self.project_root, "redcliff", None)
        first["assets"][0].update({
            "catalog_status": "classified",
            "visual_role": "item_icon",
            "tags": ["currency"],
            "preview_key": PREVIEW_KEY,
        })
        second, history = build_asset_catalog(self.project_root, "redcliff", first)
        entry = second["assets"][0]
        self.assertEqual(entry["catalog_status"], "classified")
        self.assertEqual(entry["visual_role"], "item_icon")
        self.assertEqual(entry["tags"], ["currency"])
        self.assertEqual(entry["preview_key"], PREVIEW_KEY)
        self.assertEqual(history, [])

    def test_preview_import_caches_rgba_png_by_hash(self) -> None:
        assets = minimal_asset_catalog()
        entry = assets["assets"][0]
        entry["catalog_status"] = "indexed"
        entry.pop("preview_key")
        source = self.staging / "Icon_Item_10.tga"
        Image.new("RGBA", (48, 48), (20, 180, 90, 255)).save(source)

        updated = import_previews(assets, self.staging, self.cache_root, {})

        imported = updated["assets"][0]
        self.assertRegex(imported["preview_key"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(imported["catalog_status"], "previewed")
        self.assertEqual(imported["preview_width"], 48)
        self.assertEqual(imported["preview_height"], 48)
        self.assertEqual(imported["preview_mode"], "RGBA")
        self.assertEqual(imported["preview_source"], "asset_export")
        cached = preview_path_for_key(self.cache_root, imported["preview_key"])
        self.assertTrue(cached.is_file())
        with Image.open(cached) as image:
            self.assertEqual(image.mode, "RGBA")
        digest = imported["preview_key"].removeprefix("sha256:")
        metadata = json.loads(
            (self.cache_root / "metadata" / f"{digest}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["width"], 48)
        self.assertEqual(metadata["height"], 48)
        self.assertEqual(metadata["mode"], "RGBA")
        self.assertRegex(metadata["source_export_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(metadata["preview_sha256"], digest)
        self.assertNotIn(str(self.staging), json.dumps(metadata))

    def test_duplicate_export_stems_require_explicit_mapping(self) -> None:
        assets = minimal_asset_catalog()
        assets["assets"][0]["catalog_status"] = "indexed"
        assets["assets"][0].pop("preview_key")
        duplicate = dict(assets["assets"][0])
        duplicate["asset_id"] = "redcliff.uiresources.preferential.icon_item_10"
        duplicate["source_asset"] = (
            "/RedCliff/Asset/UIresources/Preferential/Icon_Item_10.Icon_Item_10"
        )
        duplicate["source_file"] = "Asset/UIresources/Preferential/Icon_Item_10.uasset"
        duplicate["category"] = "Preferential"
        assets["assets"].append(duplicate)
        Image.new("RGB", (16, 16), "red").save(self.staging / "Icon_Item_10.png")

        with self.assertRaisesRegex(ProjectLibraryError, "ambiguous export stem"):
            import_previews(assets, self.staging, self.cache_root, {})

    def test_explicit_mapping_resolves_duplicate_export_stems(self) -> None:
        assets = minimal_asset_catalog()
        assets["assets"][0]["catalog_status"] = "indexed"
        assets["assets"][0].pop("preview_key")
        duplicate = dict(assets["assets"][0])
        duplicate["asset_id"] = "redcliff.uiresources.preferential.icon_item_10"
        duplicate["source_asset"] = (
            "/RedCliff/Asset/UIresources/Preferential/Icon_Item_10.Icon_Item_10"
        )
        duplicate["source_file"] = "Asset/UIresources/Preferential/Icon_Item_10.uasset"
        duplicate["category"] = "Preferential"
        assets["assets"].append(duplicate)
        common = self.staging / "common.png"
        preferential = self.staging / "preferential.png"
        Image.new("RGB", (16, 16), "red").save(common)
        Image.new("RGB", (24, 24), "blue").save(preferential)

        updated = import_previews(
            assets,
            self.staging,
            self.cache_root,
            {
                ASSET_ID: common,
                duplicate["asset_id"]: preferential,
            },
        )

        self.assertEqual(
            [entry["preview_width"] for entry in updated["assets"]],
            [16, 24],
        )

    def test_corrupt_preview_does_not_mutate_asset_catalog(self) -> None:
        assets = minimal_asset_catalog()
        assets["assets"][0]["catalog_status"] = "indexed"
        assets["assets"][0].pop("preview_key")
        original = deepcopy(assets)
        (self.staging / "Icon_Item_10.png").write_bytes(b"not-an-image")

        with self.assertRaisesRegex(ProjectLibraryError, "cannot import preview"):
            import_previews(assets, self.staging, self.cache_root, {})

        self.assertEqual(assets, original)

    def test_category_groups_prefer_specific_paths_without_duplicates(self) -> None:
        assets = minimal_asset_catalog()["assets"]
        common = dict(assets[0])
        common.update({
            "asset_id": "redcliff.uiresources.common.button_confirm",
            "source_file": "Asset/UIresources/Common/Button_Confirm.uasset",
            "source_asset": "/RedCliff/Asset/UIresources/Common/Button_Confirm.Button_Confirm",
            "category": "Common",
        })
        groups = group_assets_by_categories(
            [assets[0], common],
            ["Common", "Common/Icon_Item"],
        )

        self.assertEqual(
            [entry["asset_id"] for entry in groups["Common/Icon_Item"]],
            [ASSET_ID],
        )
        self.assertEqual(
            [entry["asset_id"] for entry in groups["Common"]],
            [common["asset_id"]],
        )

    def test_contact_sheet_uses_cached_previews(self) -> None:
        source = self.staging / "Icon_Item_10.png"
        Image.new("RGBA", (48, 48), (20, 180, 90, 255)).save(source)
        assets = minimal_asset_catalog()
        assets["assets"][0]["catalog_status"] = "indexed"
        assets["assets"][0].pop("preview_key")
        updated = import_previews(assets, self.staging, self.cache_root, {})
        output = self.cache_root / "contact-sheets" / "common-icon-item.png"

        result = build_contact_sheet(updated["assets"], self.cache_root, output, columns=2)

        self.assertEqual(result, output)
        with Image.open(output) as sheet:
            self.assertEqual(sheet.mode, "RGBA")
            self.assertGreater(sheet.width, 48)
            self.assertGreater(sheet.height, 48)

    def test_preview_cli_filters_categories_and_builds_contact_sheets(self) -> None:
        assets = minimal_asset_catalog()
        icon = assets["assets"][0]
        icon["catalog_status"] = "indexed"
        icon.pop("preview_key")
        common = dict(icon)
        common.update({
            "asset_id": "redcliff.uiresources.common.button_confirm",
            "source_file": "Asset/UIresources/Common/Button_Confirm.uasset",
            "source_asset": "/RedCliff/Asset/UIresources/Common/Button_Confirm.Button_Confirm",
            "category": "Common",
        })
        assets["assets"].append(common)
        catalog_path = self.library_root / "catalogs/assets.json"
        write_json(catalog_path, assets)
        Image.new("RGB", (20, 20), "green").save(self.staging / "Icon_Item_10.png")
        Image.new("RGB", (30, 20), "gold").save(self.staging / "Button_Confirm.jpg")

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "import_project_previews.py"),
                "--asset-catalog",
                str(catalog_path),
                "--staging",
                str(self.staging),
                "--cache-root",
                str(self.cache_root),
                "--category",
                "Common",
                "--category",
                "Common/Icon_Item",
                "--contact-sheets",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        updated = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.assertTrue(all(entry["catalog_status"] == "previewed" for entry in updated["assets"]))
        self.assertTrue(
            (self.cache_root / "contact-sheets/common-icon-item.png").is_file()
        )
        self.assertTrue((self.cache_root / "contact-sheets/common.png").is_file())
        catalog_text = json.dumps(updated)
        self.assertNotIn(str(self.staging), catalog_text)
        self.assertNotIn(str(self.cache_root), catalog_text)

    def test_preview_cli_allows_full_mapping_with_category_filter(self) -> None:
        assets = minimal_asset_catalog()
        icon = assets["assets"][0]
        icon["catalog_status"] = "indexed"
        icon.pop("preview_key")
        preferential = dict(icon)
        preferential.update({
            "asset_id": "redcliff.uiresources.preferential.icon_item_10",
            "source_file": "Asset/UIresources/Preferential/Icon_Item_10.uasset",
            "source_asset": "/RedCliff/Asset/UIresources/Preferential/Icon_Item_10.Icon_Item_10",
            "category": "Preferential",
        })
        assets["assets"].append(preferential)
        catalog_path = self.library_root / "catalogs/assets.json"
        mapping_path = self.root / "mapping.json"
        write_json(catalog_path, assets)
        Image.new("RGB", (20, 20), "green").save(self.staging / "common.png")
        Image.new("RGB", (30, 20), "gold").save(self.staging / "preferential.png")
        write_json(mapping_path, {
            "mappings": {
                ASSET_ID: "common.png",
                preferential["asset_id"]: "preferential.png",
            }
        })

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "import_project_previews.py"),
                "--asset-catalog",
                str(catalog_path),
                "--staging",
                str(self.staging),
                "--cache-root",
                str(self.cache_root),
                "--mapping",
                str(mapping_path),
                "--category",
                "Common/Icon_Item",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        updated = json.loads(catalog_path.read_text(encoding="utf-8"))
        by_id = {entry["asset_id"]: entry for entry in updated["assets"]}
        self.assertEqual(by_id[ASSET_ID]["catalog_status"], "previewed")
        self.assertEqual(by_id[preferential["asset_id"]]["catalog_status"], "indexed")

    def test_preview_cli_preserves_catalog_when_export_is_corrupt(self) -> None:
        assets = minimal_asset_catalog()
        assets["assets"][0]["catalog_status"] = "indexed"
        assets["assets"][0].pop("preview_key")
        catalog_path = self.library_root / "catalogs/assets.json"
        write_json(catalog_path, assets)
        original = catalog_path.read_bytes()
        (self.staging / "Icon_Item_10.png").write_bytes(b"not-an-image")

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "import_project_previews.py"),
                "--asset-catalog",
                str(catalog_path),
                "--staging",
                str(self.staging),
                "--cache-root",
                str(self.cache_root),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR: cannot import preview", result.stdout)
        self.assertEqual(catalog_path.read_bytes(), original)

    def test_dragon_jade_resolves_to_icon_item_10(self) -> None:
        export = ugcobject_export({
            "项目ItemID": 1001,
            "物品名称": "龙玉",
            "物品描述": "高级货币，用于兑换珍稀资源",
            "小icon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        })

        catalog = build_item_icon_catalog(
            export,
            minimal_asset_catalog(),
            None,
            {1001: "currency.dragon_jade"},
            {1001: ["付费货币", "CommodityCoin"]},
        )

        item = catalog["items"][0]
        self.assertEqual(item["semantic_key"], "currency.dragon_jade")
        self.assertEqual(item["item_id"], 1001)
        self.assertEqual(item["name"], "龙玉")
        self.assertEqual(item["description"], "高级货币，用于兑换珍稀资源")
        self.assertEqual(item["asset_id"], ASSET_ID)
        self.assertEqual(item["resolution_status"], "resolved")
        self.assertEqual(item["aliases"], ["付费货币", "CommodityCoin"])
        self.assertRegex(item["row_fingerprint"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(validate_item_icon_catalog(catalog, minimal_asset_catalog()), [])

    def test_item_catalog_accepts_english_field_aliases(self) -> None:
        export = ugcobject_export({
            "ItemID": 1001,
            "ItemName": "Dragon Jade",
            "ItemDesc": "Premium currency",
            "ItemIcon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        })

        catalog = build_item_icon_catalog(export, minimal_asset_catalog(), None, {}, {})

        item = catalog["items"][0]
        self.assertEqual(item["semantic_key"], "item.id_1001")
        self.assertEqual(item["name"], "Dragon Jade")
        self.assertEqual(item["asset_id"], ASSET_ID)
        self.assertEqual(item["resolution_status"], "resolved")

    def test_item_catalog_accepts_redcliff_small_icon_field(self) -> None:
        export = ugcobject_export({
            "ItemID": 1001,
            "ItemName": "龙玉",
            "ItemDesc": "高级货币，用于兑换珍稀资源",
            "ItemSmallIcon_n": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        })

        catalog = build_item_icon_catalog(export, minimal_asset_catalog(), None, {}, {})

        item = catalog["items"][0]
        self.assertEqual(item["asset_id"], ASSET_ID)
        self.assertEqual(item["resolution_status"], "resolved")

    def test_item_catalog_rejects_duplicate_item_ids(self) -> None:
        export = ugcobject_export({
            "ItemID": 1001,
            "ItemName": "Dragon Jade",
            "ItemDesc": "Premium currency",
            "SmallIcon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        })
        export["rows"].append({
            "row_name": "duplicate",
            "values": {
                "项目ItemID": 1001,
                "物品名称": "Duplicate",
                "物品描述": "Duplicate row",
                "小icon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
            },
        })

        with self.assertRaisesRegex(ProjectLibraryError, "duplicate item_id"):
            build_item_icon_catalog(export, minimal_asset_catalog(), None, {}, {})

    def test_item_catalog_keeps_missing_icon_as_candidate(self) -> None:
        export = ugcobject_export({
            "ItemID": 1002,
            "ItemName": "Mystery Token",
            "ItemDesc": "No icon yet",
        }, row_name="1002")

        catalog = build_item_icon_catalog(export, minimal_asset_catalog(), None, {}, {})

        item = catalog["items"][0]
        self.assertEqual(item["semantic_key"], "item.id_1002")
        self.assertIsNone(item["icon_asset"])
        self.assertIsNone(item["asset_id"])
        self.assertEqual(item["resolution_status"], "candidate")
        self.assertEqual(item["resolution_reason"], "missing icon field")
        self.assertEqual(validate_item_icon_catalog(catalog, minimal_asset_catalog()), [])

    def test_item_catalog_explains_icon_missing_from_asset_catalog(self) -> None:
        export = ugcobject_export({
            "ItemID": 1002,
            "ItemName": "Mystery Token",
            "ItemDesc": "Unknown icon",
            "ItemIcon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Unknown.Unknown",
        }, row_name="1002")

        catalog = build_item_icon_catalog(export, minimal_asset_catalog(), None, {}, {})

        item = catalog["items"][0]
        self.assertEqual(item["resolution_status"], "candidate")
        self.assertEqual(
            item["resolution_reason"],
            "icon asset is absent from asset catalog",
        )

    def test_item_catalog_preserves_semantic_key_and_aliases_on_resync(self) -> None:
        previous = minimal_item_icon_catalog()
        previous["items"][0]["semantic_key"] = "currency.dragon_jade"
        previous["items"][0]["aliases"] = ["old alias"]
        export = ugcobject_export({
            "ItemID": 1001,
            "ItemName": "Dragon Jade",
            "ItemDesc": "Updated text",
            "SmallIcon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        })

        catalog = build_item_icon_catalog(export, minimal_asset_catalog(), previous, {}, {})

        item = catalog["items"][0]
        self.assertEqual(item["semantic_key"], "currency.dragon_jade")
        self.assertEqual(item["aliases"], ["old alias"])
        self.assertEqual(item["description"], "Updated text")

    def test_item_catalog_cli_writes_dragon_jade_mapping(self) -> None:
        export = ugcobject_export({
            "项目ItemID": 1001,
            "物品名称": "龙玉",
            "物品描述": "高级货币，用于兑换珍稀资源",
            "小icon": "/RedCliff/Asset/UIresources/Common/Icon_Item/Icon_Item_10.Icon_Item_10",
        })
        export_path = self.root / "ugcobject-export.json"
        assets_path = self.library_root / "catalogs/assets.json"
        output_path = self.library_root / "catalogs/item-icons.json"
        write_json(export_path, export)
        write_json(assets_path, minimal_asset_catalog())

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "build_item_icon_catalog.py"),
                "--table-export",
                str(export_path),
                "--asset-catalog",
                str(assets_path),
                "--semantic-key",
                "1001=currency.dragon_jade",
                "--alias",
                "1001=付费货币",
                "--alias",
                "1001=CommodityCoin",
                "--output",
                str(output_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        catalog = json.loads(output_path.read_text(encoding="utf-8"))
        item = catalog["items"][0]
        self.assertEqual(item["semantic_key"], "currency.dragon_jade")
        self.assertEqual(item["aliases"], ["付费货币", "CommodityCoin"])
        self.assertNotIn(str(self.root), json.dumps(catalog))
        self.assertEqual(validate_item_icon_catalog(catalog, minimal_asset_catalog()), [])

    def test_resolver_rejects_every_non_active_component(self) -> None:
        for status in ("pending_review", "candidate", "deprecated", "rejected"):
            with self.subTest(status=status):
                with self.assertRaisesRegex(
                    ProjectLibraryError, "button.primary.gold is not active"
                ):
                    resolve_project_references(
                        minimal_profile(status),
                        minimal_asset_catalog(),
                        minimal_item_icon_catalog(),
                        minimal_component_asset_catalog(),
                        self.cache_root,
                        ["button.primary.gold"],
                        [],
                    )

    def test_resolver_rejects_content_browser_screenshot_as_component_preview(self) -> None:
        assets = minimal_asset_catalog()
        assets["assets"][0]["preview_source"] = "user_reference"
        preview = preview_path_for_key(self.cache_root, PREVIEW_KEY)
        preview.parent.mkdir(parents=True)
        Image.new("RGBA", (20, 20), "gold").save(preview)

        with self.assertRaisesRegex(ProjectLibraryError, "component preview is not reusable-quality"):
            resolve_project_references(
                minimal_profile("active"),
                assets,
                minimal_item_icon_catalog(),
                minimal_component_asset_catalog(),
                self.cache_root,
                ["button.primary.gold"],
                [],
            )

    def test_resolver_returns_component_and_dragon_jade_previews(self) -> None:
        assets = minimal_asset_catalog()
        button_asset = dict(assets["assets"][0])
        button_asset.update({
            "asset_id": "redcliff.uiresources.common.button_confirm",
            "source_asset": "/RedCliff/Asset/UIresources/Common/Button_Confirm.Button_Confirm",
            "source_file": "Asset/UIresources/Common/Button_Confirm.uasset",
            "category": "Common",
            "preview_key": "sha256:" + "2" * 64,
        })
        assets["assets"].append(button_asset)
        components = minimal_component_asset_catalog()
        components["components"][0]["states"]["default"] = [button_asset["asset_id"]]
        for key, color in ((PREVIEW_KEY, "green"), (button_asset["preview_key"], "gold")):
            preview = preview_path_for_key(self.cache_root, key)
            preview.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGBA", (20, 20), color).save(preview)

        result = resolve_project_references(
            minimal_profile("active"),
            assets,
            minimal_item_icon_catalog(),
            components,
            self.cache_root,
            ["button.primary.gold"],
            ["currency.dragon_jade"],
        )

        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(len(result["references"]), 2)
        self.assertTrue(
            all(reference["source_kind"] == "project_library_asset" for reference in result["references"])
        )
        by_asset = {reference["library"]["asset_id"]: reference for reference in result["references"]}
        self.assertEqual(
            by_asset[button_asset["asset_id"]]["library"]["component_ids"],
            ["button.primary.gold"],
        )
        self.assertEqual(
            by_asset[ASSET_ID]["library"]["semantic_keys"],
            ["currency.dragon_jade"],
        )

    def test_resolver_collapses_duplicate_asset_usage_with_provenance(self) -> None:
        preview = preview_path_for_key(self.cache_root, PREVIEW_KEY)
        preview.parent.mkdir(parents=True)
        Image.new("RGBA", (20, 20), "gold").save(preview)

        result = resolve_project_references(
            minimal_profile("active"),
            minimal_asset_catalog(),
            minimal_item_icon_catalog(),
            minimal_component_asset_catalog(),
            self.cache_root,
            ["button.primary.gold"],
            ["currency.dragon_jade"],
        )

        self.assertEqual(len(result["references"]), 1)
        library = result["references"][0]["library"]
        self.assertEqual(library["component_ids"], ["button.primary.gold"])
        self.assertEqual(library["semantic_keys"], ["currency.dragon_jade"])
        self.assertEqual(library["states"], ["default"])

    def test_resolver_rejects_unresolved_semantic_key(self) -> None:
        items = minimal_item_icon_catalog()
        items["items"][0].update({
            "resolution_status": "candidate",
            "asset_id": None,
            "resolution_reason": "icon asset is absent from asset catalog",
        })
        with self.assertRaisesRegex(ProjectLibraryError, "currency.dragon_jade is not resolved"):
            resolve_project_references(
                minimal_profile("active"),
                minimal_asset_catalog(),
                items,
                minimal_component_asset_catalog(),
                self.cache_root,
                [],
                ["currency.dragon_jade"],
            )

    def test_resolver_rejects_missing_cached_preview(self) -> None:
        with self.assertRaisesRegex(ProjectLibraryError, "cached preview is missing"):
            resolve_project_references(
                minimal_profile("active"),
                minimal_asset_catalog(),
                minimal_item_icon_catalog(),
                minimal_component_asset_catalog(),
                self.cache_root,
                [],
                ["currency.dragon_jade"],
            )

    def test_resolver_rejects_asset_that_requires_a_fresh_preview(self) -> None:
        assets = minimal_asset_catalog()
        assets["assets"][0]["catalog_status"] = "indexed"
        preview = preview_path_for_key(self.cache_root, PREVIEW_KEY)
        preview.parent.mkdir(parents=True)
        Image.new("RGBA", (20, 20), "gold").save(preview)

        with self.assertRaisesRegex(ProjectLibraryError, "asset is not preview-ready"):
            resolve_project_references(
                minimal_profile("active"),
                assets,
                minimal_item_icon_catalog(),
                minimal_component_asset_catalog(),
                self.cache_root,
                [],
                ["currency.dragon_jade"],
            )

    def test_resolver_rejects_duplicate_semantic_keys(self) -> None:
        items = minimal_item_icon_catalog()
        duplicate = dict(items["items"][0])
        duplicate["item_id"] = 1002
        items["items"].append(duplicate)
        preview = preview_path_for_key(self.cache_root, PREVIEW_KEY)
        preview.parent.mkdir(parents=True)
        Image.new("RGBA", (20, 20), "gold").save(preview)

        with self.assertRaisesRegex(ProjectLibraryError, "duplicate semantic_key"):
            resolve_project_references(
                minimal_profile("active"),
                minimal_asset_catalog(),
                items,
                minimal_component_asset_catalog(),
                self.cache_root,
                [],
                ["currency.dragon_jade"],
            )

    def test_resolver_cli_writes_project_library_references(self) -> None:
        self.write_valid_library()
        output_path = self.root / "references.json"

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "resolve_project_references.py"),
                "--library-root",
                str(self.library_root),
                "--cache-root",
                str(self.cache_root),
                "--component",
                "button.primary.gold",
                "--semantic-key",
                "currency.dragon_jade",
                "--output",
                str(output_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        resolved = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(resolved["references"][0]["source_kind"], "project_library_asset")
        self.assertNotIn(str(self.library_root), json.dumps(resolved))


if __name__ == "__main__":
    unittest.main()
