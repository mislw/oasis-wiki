import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIDGET_GUIDE = (ROOT / 'references' / 'mcp-ui-widget.md').read_text(encoding='utf-8')
COWART_GUIDE = (ROOT / 'references' / 'cowart-ui-workflow.md').read_text(encoding='utf-8')


class McpUiWidgetHierarchyGuidanceTests(unittest.TestCase):
    def test_component_ownership_and_coordinate_rules(self):
        markers = [
            'UMG_HIERARCHY_VISUALLY_GROUPED_BUT_FLAT',
            'Group by business responsibility, not visual overlap alone',
            'Preserve existing `Button` identity',
            'old_position.x - group_x',
            'Do not assign `CanvasPanelSlot.LayoutData`',
            ':WidgetTree.',
        ]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, WIDGET_GUIDE)

    def test_rollback_validation_and_cowart_handoff(self):
        markers = [
            'widget_add: widget',
            'already exists',
            'transport timeout is not proof that the editor mutation failed',
            'POSITION_PRESERVATION=PASS',
            'package_is_dirty() == False',
            'Refine An Existing Widget Hierarchy Without Moving The UI',
        ]
        combined = WIDGET_GUIDE + COWART_GUIDE
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, combined)


if __name__ == '__main__':
    unittest.main()
