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


if __name__ == '__main__':
    unittest.main()
