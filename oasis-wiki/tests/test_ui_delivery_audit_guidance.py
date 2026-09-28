import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
COWART = (ROOT / "references" / "cowart-ui-workflow.md").read_text(encoding="utf-8")
INTERACTION = (ROOT / "references" / "oasis-ui-agent-interaction.md").read_text(
    encoding="utf-8"
)
MCP_WIDGET = (ROOT / "references" / "mcp-ui-widget.md").read_text(encoding="utf-8")


class UiDeliveryAuditGuidanceTests(unittest.TestCase):
    def test_skill_routes_ui_delivery_to_the_contract_reference(self):
        self.assertIn("references/ui-delivery-contract.md", SKILL)

    def test_visual_workflow_requires_pixel_lock_for_exact_reuse(self):
        for marker in (
            "UI_VISUAL_LOCK_FAILED",
            "verify_ui_visual_lock.py",
            "不可重绘区域",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, COWART)

    def test_delivery_contract_and_designer_first_policy_are_documented(self):
        for guide in (INTERACTION, MCP_WIDGET):
            for marker in (
                "ui_delivery_contract",
                "Designer-first",
                "属性回读",
                "Designer 视觉",
                "PIE 功能",
                "validate_ui_delivery_contract.py",
            ):
                with self.subTest(guide_length=len(guide), marker=marker):
                    self.assertIn(marker, guide)

    def test_project_external_artifact_rule_is_explicit(self):
        for marker in (
            "审计脚本",
            "提示词",
            "项目外",
            "不得写入 UGC 工程目录",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION)


if __name__ == "__main__":
    unittest.main()
