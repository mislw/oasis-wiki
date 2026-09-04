import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sync_official_forum import (  # noqa: E402
    html_to_markdown,
    merge_forum_collection,
    render_thread_block,
    validate_thread_payload,
)


class OfficialForumSyncTests(unittest.TestCase):
    def setUp(self):
        self.thread = {
            "threadId": 2739,
            "userId": 7825,
            "categoryName": "创意交流",
            "title": "【策划面对面04】编辑器高频需求研发规划",
            "viewCount": 36,
            "isApproved": 1,
            "createdAt": "2026-08-19 17:33:16",
            "issueAt": "2026-08-19 17:34:42",
            "updatedAt": "2026-08-27 17:14:48",
            "content": {
                "text": (
                    "<h4>一、新功能</h4>"
                    "<p><strong>高频需求</strong><br>使用 MCP 批量修改。</p>"
                    '<p><a href="https://example.com/doc">文档</a></p>'
                    '<p><img src="https://example.com/5068.png" '
                    'alt="attachmentId-5068" title="5068" /></p>'
                    "<ul><li>背包 UI 开放</li><li>AI 模拟玩家</li></ul>"
                )
            },
        }

    def test_html_to_markdown_preserves_supported_rich_text(self):
        markdown = html_to_markdown(self.thread["content"]["text"])

        self.assertIn("#### 一、新功能", markdown)
        self.assertIn("**高频需求**", markdown)
        self.assertIn("使用 MCP 批量修改。", markdown)
        self.assertIn("[文档](https://example.com/doc)", markdown)
        self.assertIn("[图片#5068]", markdown)
        self.assertIn("- 背包 UI 开放", markdown)
        self.assertIn("- AI 模拟玩家", markdown)

    def test_validate_thread_payload_rejects_wrong_author_or_unapproved_content(self):
        payload = {"Code": 0, "Data": dict(self.thread)}

        validated = validate_thread_payload(payload, expected_thread_id=2739)
        self.assertEqual(2739, validated["threadId"])

        wrong_author = {"Code": 0, "Data": {**self.thread, "userId": 1}}
        with self.assertRaisesRegex(ValueError, "author"):
            validate_thread_payload(wrong_author, expected_thread_id=2739)

        unapproved = {"Code": 0, "Data": {**self.thread, "isApproved": 0}}
        with self.assertRaisesRegex(ValueError, "approved"):
            validate_thread_payload(unapproved, expected_thread_id=2739)

    def test_render_thread_block_uses_issue_and_update_times(self):
        block = render_thread_block(self.thread)

        self.assertTrue(
            block.startswith(
                "## [【策划面对面04】编辑器高频需求研发规划]"
                "(https://forum.developer.gp.qq.com/thread/2739)"
            )
        )
        self.assertIn("**发布：** 2026-08-19 17:34:42", block)
        self.assertIn("**更新：** 2026-08-27 17:14:48", block)
        self.assertIn("#### 一、新功能", block)

    def test_merge_updates_fetch_date_and_replaces_duplicate_thread_ids(self):
        existing = """# 绿洲启妹论坛经验帖合集

> 来源：绿洲开发者论坛 https://forum.developer.gp.qq.com/user/7825
> 用户：绿洲启妹 (userId:7825, 超级管理员/官方运营)
> 抓取时间：2026-07-10
> 说明：官方管理员发布的技术经验帖和策划专题分享，包含大量实操代码示例

---

## [旧标题](https://forum.developer.gp.qq.com/thread/2739)

旧内容

---

旧文章内部水平线后的尾部

---

## [保留文章](https://forum.developer.gp.qq.com/thread/2485)

保留内容
"""
        merged = merge_forum_collection(
            existing,
            [render_thread_block(self.thread)],
            fetched_at="2026-08-27",
        )

        self.assertIn("> 抓取时间：2026-08-27", merged)
        self.assertEqual(1, merged.count("/thread/2739)"))
        self.assertNotIn("旧标题", merged)
        self.assertNotIn("旧文章内部水平线后的尾部", merged)
        self.assertIn("保留文章", merged)
        self.assertLess(merged.index("/thread/2739)"), merged.index("/thread/2485)"))

    def test_skill_documents_the_official_forum_refresh_path(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        evolution = (ROOT / "references" / "skill-evolution.md").read_text(
            encoding="utf-8"
        )

        for document in (skill, agents, evolution):
            self.assertIn("scripts/sync_official_forum.py", document)
            self.assertIn("scripts/sync_official_forum.py --dry-run", document)


if __name__ == "__main__":
    unittest.main()
