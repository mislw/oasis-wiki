import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
AGENTS = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
MCP_INTEGRATION = (
    ROOT / 'references' / 'mcp-integration.md'
).read_text(encoding='utf-8')


class UePieDebuggingPolicyTests(unittest.TestCase):
    def test_entrypoints_require_ue_pie_instead_of_computer_control(self):
        for entrypoint in (SKILL, AGENTS):
            with self.subTest(entrypoint=entrypoint[:20]):
                self.assertIn('PIE debugging must use `ue_pie`', entrypoint)
                self.assertIn('must not use computer control', entrypoint)
                self.assertIn('do not fall back to computer control', entrypoint)

    def test_entrypoints_require_mobile_platform_for_start(self):
        for entrypoint in (SKILL, AGENTS):
            with self.subTest(entrypoint=entrypoint[:20]):
                self.assertIn('`action=start`', entrypoint)
                self.assertIn('`simulation_platform=mobile`', entrypoint)
                self.assertIn('never omit this field', entrypoint)
                self.assertIn('PC platform value `pchd`', entrypoint)

    def test_documented_actions_match_the_live_tool_contract(self):
        for marker in (
            'Tool version `2.4.0`',
            '`start`',
            '`stop`',
            '`reloadlua`',
            '`doluastring`',
            '`client`',
            '`ds`',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, MCP_INTEGRATION)

    def test_start_examples_use_mobile_and_forbid_pc_platform(self):
        for marker in (
            'Every `ue_pie` call with `action=start` must explicitly set '
            '`simulation_platform=mobile`',
            'Never omit `simulation_platform` from a start call',
            'never use the PC platform value `pchd`',
            'simulation_platform = "mobile"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, MCP_INTEGRATION)

    def test_lua_iteration_prefers_hot_reload_without_restarting_pie(self):
        for marker in (
            'save the modified Lua files first',
            '`reloadlua` automatically discovers all saved modified project Lua files',
            'do not stop and restart PIE',
            'non-Lua assets',
            're-run BeginPlay',
            'unrecoverable session',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, MCP_INTEGRATION)

    def test_one_way_actions_require_resource_and_log_verification(self):
        for marker in (
            'one-way triggers',
            'empty JSON object',
            '`ugc://pie/session/current`',
            'DoString Success/Error',
            'editor, client, and DS log paths',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, MCP_INTEGRATION)


if __name__ == '__main__':
    unittest.main()
