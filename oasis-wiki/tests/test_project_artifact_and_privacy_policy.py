import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
AGENTS = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
PITFALLS = (ROOT / 'references' / 'pitfalls.md').read_text(encoding='utf-8')
PREDECESSOR_POLICY = (
    ROOT / 'references' / 'predecessor-code-policy.md'
).read_text(encoding='utf-8')
FEATURE_FLOW = (
    ROOT / 'references' / 'feature-development-flow.md'
).read_text(encoding='utf-8')


class ProjectArtifactAndPrivacyPolicyTests(unittest.TestCase):
    def test_unexpected_project_artifact_gate_is_routed(self):
        for marker in (
            'Unexpected project artifact gate',
            '__pycache__/',
            '*.pyc',
            'unexpected Markdown',
            'normal cleanup commit',
            'force-push',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, SKILL + AGENTS + PITFALLS)

    def test_public_policy_does_not_embed_a_named_git_author(self):
        self.assertIsNone(
            re.search(r'Git author name\s+`[^`]+`', PREDECESSOR_POLICY)
        )
        self.assertIn('private local agent instructions', PREDECESSOR_POLICY)
        self.assertIn('Never store, publish, quote, or reveal', PREDECESSOR_POLICY)

    def test_feature_reference_search_uses_primary_predecessor_by_default(self):
        combined = SKILL + AGENTS + PREDECESSOR_POLICY + FEATURE_FLOW
        for marker in (
            'configured primary predecessor',
            'primary predecessor only by default',
            'secondary predecessor only when the user explicitly requests',
            'RedCliff',
            'StarMon',
            'StealItem',
            'references/wiki/官方API参考手册.md',
            'references/wiki/新增内容_1.37版本.md',
            'references/wiki/论坛经验帖_绿洲启妹.md',
            '已查到相关实现',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, combined)

        old_confirmation = '已找到相关的' + '代码实现。'
        self.assertNotIn(old_confirmation, combined)

    def test_code_and_knowledge_hits_share_confirmation_and_evidence(self):
        combined = SKILL + AGENTS + PREDECESSOR_POLICY + FEATURE_FLOW
        for marker in (
            'code or knowledge-base document',
            '已查到相关实现',
            'project, file, function/table, and commit',
            'knowledge-base file and section/article',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, combined)

    def test_same_type_extension_parity_gate_is_explicit(self):
        for marker in (
            'structural template',
            'archive migrations',
            'missing-key backfills',
            'line-ending changes',
            'focused `git diff`',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, PREDECESSOR_POLICY)

    def test_feature_changes_have_first_attempt_and_retry_knowledge_gates(self):
        combined = SKILL + AGENTS + FEATURE_FLOW
        for marker in (
            'Knowledge-first feature change gate',
            'Before modifying or adding a gameplay or UI feature',
            'search the bundled knowledge base',
            'Before a third implementation attempt',
            'two consecutive edit-and-verify attempts',
            'references/wiki/*.md',
            'symptom and exact error text',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, combined)

        for portable_entrypoint in (SKILL, AGENTS):
            self.assertIn('Knowledge-first feature change gate', portable_entrypoint)
            self.assertIn('Before a third implementation attempt', portable_entrypoint)


if __name__ == '__main__':
    unittest.main()
