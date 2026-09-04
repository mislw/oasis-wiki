import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(ROOT / "scripts"))

from sync_official_wiki import build_artifacts, flatten_catalog, normalize_body, write_artifacts


class OfficialWikiSyncTests(unittest.TestCase):
    def setUp(self):
        self.catalog = [
            {
                "id": 52,
                "label": "版本日志",
                "type": 0,
                "children": [
                    {"id": 20418, "label": "1.37 Release Notes", "type": 1}
                ],
            },
            {
                "id": 11,
                "label": "绿洲编辑器基础内容",
                "type": 0,
                "children": [
                    {
                        "id": 1001,
                        "label": "UGCAskQ MCP",
                        "type": 0,
                        "children": [
                            {
                                "id": 20414,
                                "label": "UGCAskQ MCP 使用说明",
                                "type": 1,
                            }
                        ],
                    }
                ],
            },
            {"id": 336, "label": "资源商店", "type": 1},
        ]
        self.articles = {
            20418: {
                "Id": 20418,
                "Title": "1.37 Release Notes",
                "Body": "# 1.37 Release Notes\n\n## 1.37.10.16430 版本说明\n",
                "AddTime": 100,
                "UpdateTime": 200,
            },
            20414: {
                "Id": 20414,
                "Title": "UGCAskQ MCP 使用说明",
                "Body": (
                    "# UGCAskQ MCP 使用说明\n\n"
                    "调用 `UGCGameSystem.GetPlayerStateByPlayerKey`。\n\n"
                    "```lua\nlocal ps = UGCGameSystem.GetPlayerStateByPlayerKey(1)\n```\n"
                ),
                "AddTime": 300,
                "UpdateTime": 400,
            },
            336: {
                "Id": 336,
                "Title": "资源商店",
                "Body": "# 资源商店\n",
                "AddTime": 500,
                "UpdateTime": 0,
            },
        }

    def test_flatten_catalog_preserves_paths_and_root_articles(self):
        articles = flatten_catalog(self.catalog)

        self.assertEqual(3, len(articles))
        self.assertEqual(
            "绿洲编辑器基础内容/UGCAskQ MCP/UGCAskQ MCP 使用说明",
            next(item.path for item in articles if item.id == 20414),
        )
        self.assertEqual("", next(item.category for item in articles if item.id == 336))

    def test_build_artifacts_generates_current_indexes_and_root_file(self):
        artifacts = build_artifacts(
            catalog=self.catalog,
            article_rows=self.articles,
            catalog_version=40,
            catalog_updated_at=600,
            generated_at=datetime(2026, 8, 27, 12, 0, tzinfo=timezone.utc),
        )

        self.assertIn("根目录.md", artifacts)
        self.assertIn("绿洲编辑器基础内容_UGCAskQ MCP.md", artifacts)
        self.assertIn("1.37.10.16430", artifacts["新增内容_1.37版本.md"])
        self.assertIn("id:20414", artifacts["README.md"])
        self.assertIn(
            "UGCGameSystem.GetPlayerStateByPlayerKey", artifacts["API参考索引.md"]
        )
        self.assertIn("local ps =", artifacts["代码示例库.md"])
        self.assertIn("Version 40", artifacts["README.md"])

    def test_normalize_body_removes_only_line_end_whitespace(self):
        body = "```lua\r\n  local value = 1  \r\n\treturn value\t\r\n```\r\n"

        self.assertEqual(
            "```lua\n  local value = 1\n\treturn value\n```",
            normalize_body(body),
        )

    def test_write_artifacts_removes_only_stale_managed_wiki_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            wiki_dir = Path(temp_dir)
            (wiki_dir / ".md").write_text("stale", encoding="utf-8")
            (wiki_dir / "旧分类.md").write_text("stale", encoding="utf-8")
            (wiki_dir / "论坛经验帖_绿洲启妹.md").write_text(
                "preserve", encoding="utf-8"
            )

            write_artifacts(
                wiki_dir,
                {"README.md": "new", "根目录.md": "root"},
                previous_managed_files={".md", "旧分类.md", "README.md"},
            )

            self.assertFalse((wiki_dir / ".md").exists())
            self.assertFalse((wiki_dir / "旧分类.md").exists())
            self.assertEqual(
                "preserve",
                (wiki_dir / "论坛经验帖_绿洲启妹.md").read_text(encoding="utf-8"),
            )
            self.assertEqual("new", (wiki_dir / "README.md").read_text(encoding="utf-8"))

    def test_skill_routes_official_refresh_through_sync_script(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("scripts/sync_official_wiki.py", skill)
        self.assertIn("scripts/sync_official_wiki.py", agents)
        self.assertIn("references/wiki/README.md", skill)
        self.assertNotIn("58 base Markdown files", skill)
        self.assertNotIn("2026-07-10 official update files", skill)


if __name__ == "__main__":
    unittest.main()
