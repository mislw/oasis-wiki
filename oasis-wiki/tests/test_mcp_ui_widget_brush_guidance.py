import unittest
from pathlib import Path


WIKI_ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = WIKI_ROOT / "references" / "mcp-ui-widget.md"


class McpUiWidgetBrushGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = GUIDE_PATH.read_text(encoding="utf-8")

    def test_unbound_brush_diagnosis_and_repair_are_documented(self):
        required = [
            "UMG_IMAGE_BRUSH_RESOURCE_UNBOUND",
            "Brush.ResourceObject",
            "get_property('Brush').ref()",
            "set_field('ResourceObject', texture)",
            "set_field('DrawAs', 3)",
            "assert missing == []",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.guide)

    def test_layer_conflict_and_end_to_end_validation_are_required(self):
        self.assertIn("UMG_IMAGE_LAYER_CONFLICT", self.guide)
        self.assertIn("Reload and assert every expected `ResourceObject` is non-null", self.guide)
        self.assertIn("Reopen the WidgetBlueprint and visually verify", self.guide)
        self.assertIn("does not prove that a bitmap rendered", self.guide)
        self.assertIn("Do not collapse a parent", self.guide)


if __name__ == "__main__":
    unittest.main()
