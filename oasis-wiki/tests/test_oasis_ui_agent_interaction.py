import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERACTION_GUIDE = (
    ROOT / 'references' / 'oasis-ui-agent-interaction.md'
).read_text(encoding='utf-8')
SKILL_GUIDE = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
AGENTS_GUIDE = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
TASK_ROUTER = (ROOT / 'references' / 'task-router.md').read_text(encoding='utf-8')
COWART_GUIDE = (
    ROOT / 'references' / 'cowart-ui-workflow.md'
).read_text(encoding='utf-8')
COMPONENT_GUIDE = (
    ROOT / 'references' / 'cowart-ui' / 'component-extractor.md'
).read_text(encoding='utf-8')
USAGE_GUIDE = (
    ROOT / 'references' / 'cowart-ui' / 'usage-guide.md'
).read_text(encoding='utf-8')
OPENAI_AGENT_GUIDE = (ROOT / 'agents' / 'openai.yaml').read_text(encoding='utf-8')


class OasisUiAgentInteractionTests(unittest.TestCase):
    def test_persisted_workflow_and_delivery_boundaries_are_explicit(self):
        markers = [
            '持久保存每个 UI 页面的八阶段任务',
            '完整 `load_path` 是唯一资产身份',
            '只调用 `ue_read` 和 `ue_py`',
            '最终重验',
            'one pending decision',
            'visual approval',
            '不是新的运行时状态模型',
            '不得把未持久化的聊天推断',
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

    def test_ui_generation_requests_open_native_tool_only_when_requested(self):
        trigger_examples = [
            '做一下 UI 生成',
            '我有一个 UI 需要生图',
            '帮我做个 UI',
            '启动 UI 生图工具',
        ]
        for trigger in trigger_examples:
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, SKILL_GUIDE)
                self.assertIn(trigger, TASK_ROUTER)

        enabled_markers = [
            (SKILL_GUIDE, 'The native Companion workflow is enabled.'),
            (AGENTS_GUIDE, 'The native Companion UI workflow is enabled.'),
            (TASK_ROUTER, 'The native Companion workflow is enabled:'),
            (INTERACTION_GUIDE, '原生 Companion `UI 生图工具链` 已启用'),
            (COWART_GUIDE, '原生 Companion 工作流已启用'),
            (COMPONENT_GUIDE, 'The native Companion control surface is enabled:'),
        ]
        for guide, marker in enabled_markers:
            with self.subTest(guide_length=len(guide), marker=marker):
                self.assertIn(marker, guide)

        for guide in (INTERACTION_GUIDE, COWART_GUIDE, COMPONENT_GUIDE):
            with self.subTest(guide_length=len(guide)):
                self.assertIn('open_ui_workflow.py', guide)

        forbidden_directives = [
            'immediately run `scripts/cowart-ui/component-extractor/open_ui_workflow.py`',
            '直接启动或聚焦 Companion 的 `UI 生图工具链`',
            'Run `scripts/cowart-ui/component-extractor/open_ui_workflow.py` to open or focus',
        ]
        combined_guides = '\n'.join(
            (SKILL_GUIDE, AGENTS_GUIDE, INTERACTION_GUIDE)
        )
        for directive in forbidden_directives:
            with self.subTest(directive=directive):
                self.assertNotIn(directive, combined_guides)

        for marker in [
            'native Companion UI workflow is enabled',
            'only after an explicit request',
            'verify the session identity',
            'never treat opening Companion as editor-write authorization',
        ]:
            with self.subTest(openai_agent_marker=marker):
                self.assertIn(marker, OPENAI_AGENT_GUIDE)

    def test_ui_work_detection_offers_toolchain_assistance_once(self):
        prompt = (
            '检测到你正在进行 UI 生图或控件拆分，是否需要我接入 UI 工具链，'
            '帮你同步当前进度并继续协助？'
        )
        for marker in (
            'UI 生图',
            '界面效果图',
            '切控件',
            '拆控件',
            '组件提取',
            '图层拆分',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION_GUIDE)

        for marker in (
            prompt,
            '每个任务最多询问一次',
            '先总结并同步当前上下文',
            '继续当前任务且不重复询问',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION_GUIDE)

        for guide in (SKILL_GUIDE, AGENTS_GUIDE):
            with self.subTest(guide_length=len(guide)):
                self.assertIn(prompt, guide)

        for marker in (
            'UI image generation or control slicing',
            'offer the UI toolchain once per task',
            'do not ask again',
        ):
            with self.subTest(openai_agent_marker=marker):
                self.assertIn(marker, OPENAI_AGENT_GUIDE)

    def test_saved_workbench_layout_requires_chat_confirmation_and_fresh_source(self):
        interaction_markers = [
            'layout-review.json',
            'pending_chat_confirmation',
            'session_sha256',
            '确认导入',
            '按刚保存的位置导入',
            '不会自动回传到对话',
            '恰好一份',
            '不能只按保存时间选择',
            '保存布局不等于编辑器写入授权',
            '精确 WidgetBlueprint `load_path`',
            '项目外备份',
            '明确授权本次写入',
        ]
        for marker in interaction_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, INTERACTION_GUIDE)

        for guide in (SKILL_GUIDE, AGENTS_GUIDE, USAGE_GUIDE):
            for marker in ('layout-review.json', '确认导入', '保存布局不等于编辑器写入授权'):
                with self.subTest(guide_length=len(guide), marker=marker):
                    self.assertIn(marker, guide)

        for marker in (
            'layout-review.json',
            'pending_chat_confirmation',
            'session_sha256',
            'must not choose the newest snapshot when multiple pages are pending',
            'does not authorize an editor write',
        ):
            with self.subTest(openai_agent_marker=marker):
                self.assertIn(marker, OPENAI_AGENT_GUIDE)


if __name__ == '__main__':
    unittest.main()
