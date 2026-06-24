# Agent Instructions

This repository contains a portable knowledge bundle for Oasis / 绿洲启元 / 和平精英 UGC Lua development.

Codex can use `oasis-wiki/SKILL.md` as a native skill. Other AI coding agents should follow this file as the entry point.

## Scope

Always use this bundle when a question appears related to an Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC project, even if the user does not explicitly request it.

Use this bundle when helping with:

- Oasis / 绿洲启元 / 和平精英 UGC Lua APIs.
- Gameplay systems, UI systems, editor workflows, templates, debugging, performance, release notes, and terminology.
- Teaching the user how to modify UGC project code.
- Mining reusable practices from local UGC project examples.

Strong trigger signals include:

- `绿洲启元`, `绿洲起源`, `起源UGC`, `和平精英UGC`, `UGC项目`, `UGCProjects`, `ShadowTrackerExtra`.
- `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `Action_*`.
- `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCEventSystem`, `UGCTimerTools`, `UGCBackPackSystem`, `UGCTeamSystem`.
- UI, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, damage, items, game phases, debugging, performance, and editor workflows in a UGC context.

Do not treat a single project name as the whole domain. Project-specific files are examples and should be mined for reusable patterns only when relevant.

## Safety Rule

Default to teaching-only mode for UGC project files:

- You may read, search, inspect, and analyze project files freely.
- Do not directly modify UGC project files unless the user explicitly overrides this rule for the current task.
- Give exact edit instructions, snippets, replacement blocks, or patch-style guidance for the user to apply.
- You may edit this repository when the user asks to improve the knowledge bundle.

Read `oasis-wiki/references/teaching-mode.md` before giving code-change guidance.

## Required Workflow

1. Search before answering. Do not load the full wiki into context.
2. Start with the focused references:
   - `oasis-wiki/references/wiki/README.md`
   - `oasis-wiki/references/wiki/API参考索引.md`
   - `oasis-wiki/references/wiki/代码示例库.md`
   - `oasis-wiki/references/wiki/术语表.md`
3. For implementation help, load the relevant distilled references:
   - `oasis-wiki/references/teaching-mode.md`
   - `oasis-wiki/references/feature-development-flow.md`
   - `oasis-wiki/references/recipes.md`
   - `oasis-wiki/references/snippets.md`
   - `oasis-wiki/references/pitfalls.md`
   - `oasis-wiki/references/project-patterns.md`
4. If more evidence is needed and the local UGC project corpus is available, use:
   - `oasis-wiki/references/project-mining-index.md`
5. If the user asks whether a conversation, correction, or project pattern should be added to the bundle, read `oasis-wiki/references/skill-evolution.md` and use its controlled update protocol.
6. Cite local file paths and line numbers when possible.
7. If a Lua API or behavior is not found in the bundled wiki or examples, say it was not confirmed.

## Search Commands

From the repository root:

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
powershell -ExecutionPolicy Bypass -File .\oasis-wiki\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\oasis-wiki\scripts\search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```

## Answer Shape For Code Help

For non-trivial code changes, answer in a detailed walkthrough shape. Use numbered sections when a feature touches multiple files or systems:

```text
1. <配置 / 存档 / 服务端逻辑 / RPC 注册 / UI 按钮 / UI 刷新 / 复制 / 重连>

位置:
<file path> (line <line if known>), <function/table> 里

现在是:
<existing nearby code, when useful>

改成:
<replacement block or inserted block>

为什么这样改:
<explain the data flow and server/client responsibility>

注意:
<punctuation, comma, nil check, server/client, RPC registration, replication, event ID, config ID>

怎么测:
1. <success path>
2. <failure path>
3. <multiplayer/server-client path if relevant>
4. <reconnect/respawn path if relevant>
```

When changing an existing block, show both `现在是:` and `改成:`. For fragile Lua syntax, explicitly call out commas, table separators, return-list formatting, and where comments can safely go. Keep answers practical and specific. Prefer small, teachable changes over broad rewrites.
