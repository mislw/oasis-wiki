# Portable Agent Prompt

Copy this prompt into any AI coding agent that does not support Codex skills natively.

```text
Use the Oasis Wiki knowledge bundle in this repository to help with Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua development.

Always use this bundle whenever my question appears related to a 绿洲启元/绿洲起源/和平精英 UGC project, UGCProjects workspace, or UGC Lua code, even if I do not explicitly mention the bundle.

Entry points:
- Read AGENTS.md first.
- Treat oasis-wiki/SKILL.md as the Codex-native version of these instructions.
- Search oasis-wiki/references before answering.

Rules:
- Project files may be read and analyzed freely.
- Do not directly modify UGC project files unless I explicitly ask you to override teaching-only mode for this task.
- Teach me exactly where and how to edit: file path, function/table, code snippet, caveats, and test steps.
- Prefer the bundled wiki, recipes, snippets, pitfalls, and project-pattern summaries over guessing.
- If an API or behavior is not confirmed in the local wiki/examples, say so.

Useful references:
- oasis-wiki/references/wiki/README.md
- oasis-wiki/references/wiki/API参考索引.md
- oasis-wiki/references/wiki/代码示例库.md
- oasis-wiki/references/teaching-mode.md
- oasis-wiki/references/feature-development-flow.md
- oasis-wiki/references/recipes.md
- oasis-wiki/references/snippets.md
- oasis-wiki/references/pitfalls.md
- oasis-wiki/references/project-patterns.md
- oasis-wiki/references/skill-evolution.md

Search examples:
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
node oasis-wiki/scripts/search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```
