import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_MEMORY = (
    ROOT / 'references' / 'project-planning-memory.md'
).read_text(encoding='utf-8')


class ProjectPlanningSourceVersioningTests(unittest.TestCase):
    def test_known_project_planning_uploads_are_ingested_automatically(self):
        for marker in (
            'Automatic Project Ingestion',
            'explicitly identifies the project',
            'reliably resolves the project',
            'ingest it without requiring a separate remember-this request',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, PLANNING_MEMORY)

    def test_logical_source_identity_and_duplicate_content_are_defined(self):
        for marker in (
            'Logical Source Identity',
            'copy suffixes such as `(1)`, `(2)`, `copy`, and `副本`',
            'SHA-256 digests match',
            'do not ingest or index it again',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, PLANNING_MEMORY)

    def test_newer_version_selection_has_an_explicit_priority(self):
        expected_order = (
            '1. The user explicitly identifies one file as the new/current version.',
            '2. An embedded document revision, semantic version, or unambiguous date identifies the newer version.',
            '3. The current conversation upload/arrival order identifies the replacement.',
            '4. Filesystem modification time is supporting evidence only.',
        )
        positions = [PLANNING_MEMORY.find(marker) for marker in expected_order]
        self.assertTrue(all(position >= 0 for position in positions))
        self.assertEqual(positions, sorted(positions))
        self.assertIn('ask the user which file is authoritative', PLANNING_MEMORY)

    def test_replacement_cleans_only_superseded_project_memory(self):
        for marker in (
            'Transactional Replacement',
            'Only after the new source is parsed successfully',
            'remove the superseded filename, digest, and provenance',
            'rewrite or remove claims supported only by the old version',
            'Never delete or rename the user\'s original uploaded files',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, PLANNING_MEMORY)


if __name__ == '__main__':
    unittest.main()
