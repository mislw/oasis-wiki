import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


WIKI_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = WIKI_ROOT / "scripts" / "cowart-ui" / "component-extractor"
sys.path.insert(0, str(SCRIPT_ROOT))

import codex_upstream_image_executor


class CodexUpstreamImageExecutorTests(unittest.TestCase):
    def test_merge_masked_edit_preserves_every_unmasked_pixel(self):
        original = Image.new("RGBA", (4, 4), (200, 20, 20, 255))
        edited = Image.new("RGBA", (4, 4), (20, 40, 220, 255))
        edit_mask = Image.new("L", (4, 4), 0)
        edit_mask.putpixel((1, 1), 255)
        edit_mask.putpixel((2, 2), 255)

        merged = codex_upstream_image_executor.merge_masked_edit(original, edited, edit_mask)

        self.assertEqual((20, 40, 220, 255), merged.getpixel((1, 1)))
        self.assertEqual((20, 40, 220, 255), merged.getpixel((2, 2)))
        self.assertEqual((200, 20, 20, 255), merged.getpixel((0, 0)))
        self.assertEqual((200, 20, 20, 255), merged.getpixel((3, 3)))

    def test_build_union_mask_uses_dependency_alpha_before_bounds_fallback(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            layer = root / "layers" / "child.png"
            layer.parent.mkdir()
            child = Image.new("RGBA", (2, 2), (255, 255, 255, 0))
            child.putpixel((0, 0), (255, 255, 255, 255))
            child.save(layer)
            (root / "extraction-plan.json").write_text(json.dumps({
                "components": [{
                    "target_component_id": "child",
                    "instances": [{
                        "node_id": "child.node",
                        "bounds": {"x": 11, "y": 21, "width": 2, "height": 2},
                    }],
                }],
            }), encoding="utf-8")
            job = {
                "mask": {"sources": [{
                    "node_id": "child.node",
                    "source_type": "clean_layer_alpha",
                    "path": "layers/child.png",
                    "padding": 0,
                }]},
            }

            mask = codex_upstream_image_executor.build_union_mask(
                job,
                root,
                {"x": 10, "y": 20, "width": 4, "height": 4},
            )

            self.assertEqual(255, mask.getpixel((1, 1)))
            self.assertEqual(0, mask.getpixel((2, 2)))

    def test_clean_layer_alpha_expands_for_shadow_alignment_without_becoming_bounds(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            layer = root / "layers" / "child.png"
            layer.parent.mkdir()
            child = Image.new("RGBA", (9, 9), (255, 255, 255, 0))
            child.putpixel((4, 4), (255, 255, 255, 255))
            child.save(layer)
            (root / "extraction-plan.json").write_text(json.dumps({
                "components": [{
                    "target_component_id": "child",
                    "instances": [{
                        "node_id": "child.node",
                        "bounds": {"x": 0, "y": 0, "width": 9, "height": 9},
                    }],
                }],
            }), encoding="utf-8")
            job = {
                "mask": {"sources": [{
                    "node_id": "child.node",
                    "source_type": "clean_layer_alpha",
                    "path": "layers/child.png",
                }]},
            }

            mask = codex_upstream_image_executor.build_union_mask(
                job,
                root,
                {"x": 0, "y": 0, "width": 9, "height": 9},
            )

            self.assertEqual(255, mask.getpixel((1, 4)))
            self.assertEqual(255, mask.getpixel((7, 4)))
            self.assertEqual(0, mask.getpixel((0, 0)))
            self.assertEqual(0, mask.getpixel((8, 8)))

    def test_parent_panel_uses_continuous_descendant_envelope_fallback(self):
        job = {
            "category": "panel",
            "mask": {"sources": [
                {
                    "node_id": "first",
                    "source_type": "bounds_fallback",
                    "bounds": {"x": 2, "y": 2, "width": 3, "height": 2},
                    "padding": 0,
                },
                {
                    "node_id": "second",
                    "source_type": "bounds_fallback",
                    "bounds": {"x": 12, "y": 6, "width": 3, "height": 2},
                    "padding": 0,
                },
            ]},
        }

        mask = codex_upstream_image_executor.build_union_mask(
            job,
            Path("."),
            {"x": 0, "y": 0, "width": 20, "height": 12},
        )

        self.assertEqual(255, mask.getpixel((9, 5)))
        self.assertEqual(0, mask.getpixel((19, 11)))

    def test_button_keeps_disjoint_precise_masks(self):
        job = {
            "category": "button",
            "mask": {"sources": [
                {
                    "node_id": "first",
                    "source_type": "bounds_fallback",
                    "bounds": {"x": 2, "y": 2, "width": 3, "height": 2},
                    "padding": 0,
                },
                {
                    "node_id": "second",
                    "source_type": "bounds_fallback",
                    "bounds": {"x": 12, "y": 6, "width": 3, "height": 2},
                    "padding": 0,
                },
            ]},
        }

        mask = codex_upstream_image_executor.build_union_mask(
            job,
            Path("."),
            {"x": 0, "y": 0, "width": 20, "height": 12},
        )

        self.assertEqual(0, mask.getpixel((9, 5)))

    def test_chroma_key_to_alpha_removes_flat_background(self):
        image = Image.new("RGBA", (3, 3), (255, 0, 255, 255))
        image.putpixel((1, 1), (230, 180, 30, 255))

        result = codex_upstream_image_executor.chroma_key_to_alpha(image, (255, 0, 255))

        self.assertEqual(0, result.getpixel((0, 0))[3])
        self.assertEqual(255, result.getpixel((1, 1))[3])

    def test_chroma_key_flood_removes_purple_noise_and_small_dark_island(self):
        image = Image.new("RGBA", (7, 7), (255, 0, 255, 255))
        image.putpixel((0, 3), (70, 5, 76, 180))
        image.putpixel((1, 1), (18, 18, 18, 255))
        for y in range(2, 5):
            for x in range(2, 5):
                image.putpixel((x, y), (220, 150, 35, 255))
        image.putpixel((3, 3), (25, 25, 25, 255))

        result = codex_upstream_image_executor.chroma_key_to_alpha(image, (255, 0, 255))

        self.assertEqual(0, result.getpixel((0, 3))[3])
        self.assertEqual(0, result.getpixel((1, 1))[3])
        self.assertEqual((25, 25, 25, 255), result.getpixel((3, 3)))

    def test_api_canvas_clears_masked_pixels_before_image_edit(self):
        image = Image.new("RGBA", (4, 4), (120, 80, 40, 255))
        edit_mask = Image.new("L", (4, 4), 0)
        edit_mask.putpixel((1, 1), 255)

        canvas, api_mask, transform = codex_upstream_image_executor._api_canvas(image, edit_mask)

        offset_x, offset_y = transform["offset"]
        scale_x = transform["rendered_size"][0] // image.width
        scale_y = transform["rendered_size"][1] // image.height
        masked_x = offset_x + scale_x
        masked_y = offset_y + scale_y
        self.assertEqual(0, canvas.getpixel((masked_x, masked_y))[3])
        self.assertEqual(0, api_mask.getpixel((masked_x, masked_y))[3])
        self.assertEqual(255, canvas.getpixel((offset_x, offset_y))[3])
        self.assertEqual(255, api_mask.getpixel((offset_x, offset_y))[3])


if __name__ == "__main__":
    unittest.main()
