import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERACTION_GUIDE = (
    ROOT / 'references' / 'oasis-ui-agent-interaction.md'
).read_text(encoding='utf-8')
SKILL_GUIDE = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
TASK_ROUTER = (ROOT / 'references' / 'task-router.md').read_text(encoding='utf-8')
COWART_GUIDE = (
    ROOT / 'references' / 'cowart-ui-workflow.md'
).read_text(encoding='utf-8')


class OasisUiAgentInteractionTests(unittest.TestCase):
    def test_interaction_only_boundary_is_explicit(self):
        markers = [
            'INTERACTION_ONLY_NO_RUNTIME_CHANGE',
            'one pending decision',
            'visual approval',
            'do not claim persisted task state',
            '不是新的运行时状态模型',
            '不改变任何生产功能',
        ]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION_GUIDE)

    def test_required_review_and_write_gates_are_documented(self):
        markers = [
            'WORKBENCH_REVIEW',
            'UMG_REQUIREMENTS',
            'UMG_BUILD',
            'LOGIC_BINDING',
            'FINAL_REVIEW',
            'USER_APPROVAL_REQUIRED',
            'POSITION_PRESERVATION=PASS',
            '切图确认',
        ]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION_GUIDE)

    def test_modification_backtracking_and_stale_approval_rules_exist(self):
        markers = [
            '修改请求',
            'Backtracking',
            '旧的 layer approval 立即失效',
            'Visual 改动会使下游',
            '不得用“回到上一阶段”暗示自动回滚',
        ]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION_GUIDE)

    def test_skill_router_and_cowart_workflow_route_to_interaction_guide(self):
        marker = 'references/oasis-ui-agent-interaction.md'
        for guide in (SKILL_GUIDE, TASK_ROUTER, COWART_GUIDE):
            with self.subTest(guide_length=len(guide)):
                self.assertIn(marker, guide)


if __name__ == '__main__':
    unittest.main()
