# Agent Instructions

This repository contains a portable knowledge bundle for Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua development.

Codex should use `oasis-wiki/SKILL.md` as a native skill. Other AI coding agents should follow this file as the repository entry point, then read the skill folder references.

## Scope

Always use this bundle when a question appears related to:

- Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC projects.
- `UGCProjects`, `ShadowTrackerExtra`, UGC Lua, project scripts, UI, RPC, replication, logs, debugging, performance, editor workflows.
- `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `GlobalConfig`, `Action_*`.
- `UnrealNetwork`, `GetAvailableServerRPCs`, `UGCEventSystem`, `UGCGameSystem`, `LuaQuickFireEvent`, `ugcprint`.
- `UGCAskQ`, `MCP`, MCP Server, `.mcp.json`, SSE, PRV, editor automation, DataTable, WidgetBlueprint.

Keep private project source, screenshots, planning docs, and local caches out of this public repository.

## Required Routing

1. Read `oasis-wiki/SKILL.md`.
2. Read `oasis-wiki/references/task-router.md` and choose one primary branch, with at most one secondary branch.
3. Search official/local references before answering. Do not load the whole wiki into context.
4. Open real project files before giving exact code edits or line references.

Primary branches:

- Project analysis: `project-cache.md`, `project-planning-memory.md`, targeted source files.
- Feature development: `feature-development-flow.md`, `code-style.md` when writing/reviewing Lua.
- Debugging/errors: logs first, then `pitfalls.md` and the symptom branch.
- MCP operation: `mcp-integration.md`, then either `mcp-ui-widget.md` or `mcp-datatable.md`.
- Config/balancing: table schema, code consumers, `mcp-datatable.md` when editor tables are involved.
- UI/interaction: UIManager, `Script/UI`, existing bindings, `mcp-ui-widget.md` only for WidgetBlueprint work.
- Project safety: `pitfalls.md`, binary asset precautions, dirty file distinction, backup rules.

## Answer Modes

Read `oasis-wiki/references/answer-modes.md` before choosing mode.

Default to normal mode: concise, direct, review-friendly.

Use teaching mode only when the user explicitly asks for `教学模式`, `详细讲`, `教我`, `一步一步`, `拆一下`, or beginner-friendly walkthrough output.

Teaching mode is always read-only for UGC project files:

- Do not directly edit project code, assets, or configs in teaching mode.
- If direct implementation is needed, ask the user to switch to normal/direct mode.
- For every code-change instruction, include file path, line number, and function/table name.

## Code And Feature Rules

- Before writing/reviewing Lua, read `oasis-wiki/references/code-style.md`.
- Feature flow stays: existing foundation -> config -> authoritative server logic -> Server RPC -> UI/input binding -> UI refresh -> replication/save -> reconnect/recovery -> GM/log verification.
- Preserve teammate behavior, names, call order, RPC names, event IDs, save keys, and formatting unless a change is required and explained.
- Do not mutate DataTable/UAEDataTable row objects directly in runtime code; copy rows into normal Lua tables before changing derived values.
- For MCP/editor asset writes, use PRV/safety rules and place `.uasset` backups outside the UGC project tree.

## Useful Searches

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
node oasis-wiki/scripts/search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```

## High-Value References

- `oasis-wiki/references/task-router.md`
- `oasis-wiki/references/answer-modes.md`
- `oasis-wiki/references/teaching-mode.md`
- `oasis-wiki/references/feature-development-flow.md`
- `oasis-wiki/references/code-style.md`
- `oasis-wiki/references/mcp-integration.md`
- `oasis-wiki/references/mcp-ui-widget.md`
- `oasis-wiki/references/mcp-datatable.md`
- `oasis-wiki/references/project-cache.md`
- `oasis-wiki/references/project-planning-memory.md`
- `oasis-wiki/references/pitfalls.md`
- `oasis-wiki/references/wiki/README.md`
- `oasis-wiki/references/wiki/官方API参考手册.md`
- `oasis-wiki/references/wiki/新增内容_1.37版本.md`
- `oasis-wiki/references/wiki/论坛经验帖_绿洲启妹.md`
