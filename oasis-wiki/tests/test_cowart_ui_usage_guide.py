import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USAGE_GUIDE_PATH = ROOT / 'references' / 'cowart-ui' / 'usage-guide.md'


class CowartUiUsageGuideTests(unittest.TestCase):
    def test_usage_guide_is_routed_from_skill_and_workflow(self):
        self.assertTrue(USAGE_GUIDE_PATH.is_file())
        route = 'references/cowart-ui/usage-guide.md'
        for path in (
            ROOT / 'SKILL.md',
            ROOT / 'references' / 'cowart-ui-workflow.md',
        ):
            with self.subTest(path=path.name):
                self.assertIn(route, path.read_text(encoding='utf-8'))

    def test_usage_guide_explains_entry_points_and_next_actions(self):
        content = USAGE_GUIDE_PATH.read_text(encoding='utf-8')
        for marker in (
            '启动 UI 工具链',
            '帮我做 UI',
            '继续上次的 UI',
            'Workbench',
            '组件确认',
            'UMG',
            '编辑器交付',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_documentation_updates_do_not_authorize_editor_writes(self):
        content = USAGE_GUIDE_PATH.read_text(encoding='utf-8')
        for marker in (
            '只更新说明',
            '不等于授权修改编辑器',
            '精确的 WidgetBlueprint',
            '备份',
            '明确授权',
            '先澄清一次',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_usage_guide_documents_proactive_ui_work_detection(self):
        content = USAGE_GUIDE_PATH.read_text(encoding='utf-8')
        for marker in (
            '检测到你正在进行 UI 生图或控件拆分',
            '每个任务最多询问一次',
            '同步当前进度',
            '拒绝后继续当前任务',
            '只有用户明确要求打开/继续工作台',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)


if __name__ == '__main__':
    unittest.main()
