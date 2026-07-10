# Agent Instructions

This repository contains a portable knowledge bundle for Oasis / 绿洲启元 / 和平精英 UGC Lua development.

Codex can use `oasis-wiki/SKILL.md` as a native skill. Other AI coding agents should follow this file as the entry point.

## Scope

Always use this bundle when a question appears related to an Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC project, even if the user does not explicitly request it.

Use this bundle when helping with:

- Oasis / 绿洲启元 / 和平精英 UGC Lua APIs.
- Gameplay systems, UI systems, editor workflows, templates, debugging, logs, performance, release notes, and terminology.
- Teaching the user how to modify UGC project code.
- Applying reusable UGC Lua project architecture patterns.

Strong trigger signals include:

- `绿洲启元`, `绿洲起源`, `起源UGC`, `和平精英UGC`, `UGC项目`, `UGCProjects`, `ShadowTrackerExtra`.
- `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `Action_*`.
- `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCEventSystem`, `UGCTimerTools`, `UGCBackPackSystem`, `UGCTeamSystem`, `ugcprint`.
- UI, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, damage, items, game phases, debugging, logs, DSlog, Clientlog, `UGCClientLog`, `UGCServerLog`, `PIE日志面板`, `game_id`, performance, and editor workflows in a UGC context.

Do not treat a single project name as the whole domain. Keep project-specific notes, names, paths, plans, screenshots, and spreadsheets in local project memory instead of this public bundle.

## Safety Rule

Default to teaching answer mode, while keeping UGC project files read-only by default:

- You may read, search, inspect, and analyze project files freely.
- Do not directly modify UGC project files unless the user explicitly overrides this rule for the current task.
- Give exact edit instructions, snippets, replacement blocks, or patch-style guidance for the user to apply.
- You may edit this repository when the user asks to improve the knowledge bundle.

Read `oasis-wiki/references/answer-modes.md` before choosing detailed teaching mode or concise normal mode. Read `oasis-wiki/references/teaching-mode.md` by default for implementation, planning, code explanation, and project-reading tasks. Use concise normal mode only when the user explicitly asks for `正常模式`, brevity, direct code, or review-friendly output.

## Required Workflow

1. Search before answering. Do not load the full wiki into context.
2. For feature/API/system questions (`怎么用`, `怎么做`, `有没有`, `支持吗`, class/API names, editor feature names, templates, systems, components), search the official documentation bundle before giving a conclusion:
   - `oasis-wiki/references/wiki/README.md`
   - `oasis-wiki/references/wiki/官方API参考手册.md`
   - `oasis-wiki/references/wiki/新增内容_1.37版本.md`
   - `oasis-wiki/references/wiki/论坛经验帖_绿洲启妹.md`
   - matching base official wiki teaching docs under `oasis-wiki/references/wiki/*.md`
3. Use focused indexes as needed:
   - `oasis-wiki/references/wiki/API参考索引.md`
   - `oasis-wiki/references/wiki/代码示例库.md`
   - `oasis-wiki/references/wiki/术语表.md`
4. For implementation help, load the relevant distilled references:
   - `oasis-wiki/references/answer-modes.md`
   - `oasis-wiki/references/teaching-mode.md`
   - `oasis-wiki/references/code-style.md`
   - `oasis-wiki/references/feature-development-flow.md`
   - `oasis-wiki/references/recipes.md`
   - `oasis-wiki/references/snippets.md`
   - `oasis-wiki/references/pitfalls.md`
   - `oasis-wiki/references/project-patterns.md`
5. Before writing or reviewing Lua code, especially config tables, member variables, methods, or `GlobalConfig` entries, read `oasis-wiki/references/code-style.md`.
6. For log/debugging questions, search the focused wiki entries for `调试日志说明`, `PIE日志面板`, `日志提取`, `客户端调试管理器`, and `战斗日志`. Distinguish editor PIE logs, local `Clientlog`/`DSlog`, phone client logs, management-platform DS logs, and battle logs.
7. If the user asks whether a conversation, correction, or project pattern should be added to the bundle, read `oasis-wiki/references/skill-evolution.md` and use its controlled update protocol.
8. Cite local file paths and line numbers when possible.
9. If a Lua API or behavior is not found in the bundled wiki or examples, say it was not confirmed.

## Search Commands

From the repository root:

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
powershell -ExecutionPolicy Bypass -File .\oasis-wiki\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\oasis-wiki\scripts\search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```

## Answer Shape For Code Help

Choose the answer mode first:

- Teaching mode: detailed, step-by-step. Use by default.
- Normal mode: concise, practical, review-friendly, and direct. Use only when the user asks for `正常模式`, says `简短点` / `直接说` / `给我代码`, or explicitly wants experienced teammates to review.

Normal mode shape:

```text
结论:
<short direct answer>

依据:
<confirmed from project code / confirmed from wiki / inferred from existing pattern>

改哪里:
<file path + function/table>

最小改动:
<focused snippet with only brief summary comments before functions/methods or major blocks>

影响范围:
<server/client/UI/save/replication/RPC/reconnect/log impact, or "only affects this local function">

风险:
<低/中/高 + one short reason>

注意:
<only the key risks and compatibility notes>

日志:
<DSlog/Clientlog/PIE log panel/battle log keywords to search, or "not needed">

怎么测:
<2-4 short checks>

回滚:
<the smallest revert point>
```

Teaching mode shape:

For teaching-mode code changes, answer in a detailed walkthrough shape. Use numbered sections when a feature touches multiple files or systems:

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

In normal mode, do not add line-by-line teaching comments inside code blocks. Prefer one brief Chinese summary comment before a function/method or major logic block. When changing an existing block, show both `现在是:` and `改成:`. For fragile Lua syntax, explicitly call out commas, table separators, return-list formatting, and where comments can safely go. Keep answers practical and specific.
