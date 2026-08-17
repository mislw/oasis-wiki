import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
GUIDE = (ROOT / 'references' / 'companion-versioning.md').read_text(
    encoding='utf-8'
)
SKILL = (ROOT / 'SKILL.md').read_text(encoding='utf-8')


class CompanionVersioningTests(unittest.TestCase):
    def test_version_uses_major_date_iteration_format(self):
        self.assertRegex(VERSION, re.compile(r'^\d+\.\d{6}\.\d+$'))
        self.assertEqual(VERSION, '1.260817.5')

    def test_versioning_contract_is_documented_and_routed(self):
        for marker in (
            'M.YYMMDD.N',
            'M.YY.MMDD+N',
            'tauri.build.conf.json',
            'Asia/Shanghai',
            'one-based distributable iteration number',
            'Do not reuse',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, GUIDE)
        self.assertIn('references/companion-versioning.md', SKILL)


if __name__ == '__main__':
    unittest.main()
