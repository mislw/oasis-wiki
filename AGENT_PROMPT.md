# Portable Agent Prompt

Copy this prompt into any AI coding agent that does not support Codex skills natively.

```text
Use the Oasis Wiki knowledge bundle in this repository for Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua development.

Always use this bundle when my question appears related to UGCProjects, UGC Lua, RPC, UI, replication, logs, DSlog, Clientlog, UGCAskQ MCP, editor automation, DataTable, WidgetBlueprint, or Oasis/Peace Elite UGC project architecture.

Entry points:
- Read AGENTS.md first.
- Treat oasis-wiki/SKILL.md as the Codex-native version.
- Read oasis-wiki/references/task-router.md before loading detailed references.
- Search oasis-wiki/references before answering; do not load the whole wiki.

Task routing:
- Project analysis: project-cache.md, project-planning-memory.md, targeted project files.
- Feature development: feature-development-flow.md, code-style.md when writing/reviewing Lua.
- Debugging/errors: inspect available logs first, then pitfalls.md and the symptom branch.
- MCP operation: mcp-integration.md, then either mcp-ui-widget.md or mcp-datatable.md.
- Config/balancing: table schema, code consumers, mcp-datatable.md when editor tables are involved.
- UI/interaction: UIManager, Script/UI, existing bindings, mcp-ui-widget.md only for WidgetBlueprint work.
- Project safety: pitfalls.md, binary asset precautions, dirty file distinction, backup rules.

Answer modes:
- Use normal mode by default: concise, direct, review-friendly.
- Use teaching mode only when I explicitly say 教学模式, 详细讲, 教我, 一步一步, 拆一下, or ask for a beginner-friendly walkthrough.
- Teaching mode is read-only for UGC project files. Do not directly edit project code, assets, or configs in teaching mode.
- In teaching mode, every code-change instruction must include file path, line number, and function/table name.
- If I ask for direct edits while teaching mode is active, tell me to switch back to normal/direct mode first.

Feature development flow:
existing foundation -> config -> authoritative server logic -> Server RPC -> UI/input binding -> UI refresh -> replication/save -> reconnect/recovery -> GM/log verification.

Code style:
- Before writing/reviewing Lua, read oasis-wiki/references/code-style.md.
- New config fields, member variables, GlobalConfig variables, and methods need Chinese comments.
- Preserve existing teammate naming, call order, RPC names, event IDs, save keys, and formatting unless a change is required and explained.
- Do not add noisy nil/UE.IsValid guards everywhere; guard real boundaries such as user input, config absence, RPC payloads, async UI lifecycle, destroyed actors, and optional data.
- Do not mutate DataTable/UAEDataTable row objects directly at runtime; copy rows into normal Lua tables before changing derived values.

MCP:
- For UGCAskQ MCP/editor automation, read mcp-integration.md first.
- UI/Widget/UMG/Blueprint work uses mcp-ui-widget.md.
- Config table/DataTable/UAEDataTable work uses mcp-datatable.md.
- Use both MCP branches only for genuinely mixed UI+table tasks.
- Back up binary assets outside the UGC project tree.

Project memory:
- Use local project caches under %USERPROFILE%\.codex\oasis-project-cache.
- Do not write cache files into the UGC project workspace.
- Use cache summaries and symbols to narrow search, then open real source files before giving line-level edits.

Useful references:
- oasis-wiki/references/task-router.md
- oasis-wiki/references/answer-modes.md
- oasis-wiki/references/teaching-mode.md
- oasis-wiki/references/feature-development-flow.md
- oasis-wiki/references/code-style.md
- oasis-wiki/references/mcp-integration.md
- oasis-wiki/references/mcp-ui-widget.md
- oasis-wiki/references/mcp-datatable.md
- oasis-wiki/references/project-cache.md
- oasis-wiki/references/project-planning-memory.md
- oasis-wiki/references/pitfalls.md
- oasis-wiki/references/wiki/README.md
- oasis-wiki/references/wiki/官方API参考手册.md
- oasis-wiki/references/wiki/新增内容_1.37版本.md
- oasis-wiki/references/wiki/论坛经验帖_绿洲启妹.md

Search examples:
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
node oasis-wiki/scripts/search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```
