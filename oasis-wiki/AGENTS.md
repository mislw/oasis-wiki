# Agent Instructions For This Skill Folder

Use this folder as a portable Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua knowledge bundle.

Codex should use `SKILL.md`. Other AI coding agents should follow this file.

## Always Invoke

Always use this folder when a question appears related to a 绿洲启元/绿洲起源/和平精英 UGC project, UGCProjects workspace, or UGC Lua code.

Strong signals include `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UIManager`, `EventDefine`, `Action_*`, UI, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, debugging, logs, DSlog, Clientlog, `UGCClientLog`, `UGCServerLog`, `PIE日志面板`, `ugcprint`, `game_id`, performance, and editor workflows.

## Rules

- Search `references/` before answering.
- Read `references/answer-modes.md` before choosing concise normal mode or detailed teaching mode.
- Read `references/teaching-mode.md` when teaching mode applies.
- Read `references/code-style.md` before writing or reviewing Lua code, especially config tables, member variables, methods, or `GlobalConfig` entries.
- Read `references/feature-development-flow.md` for end-to-end feature work that crosses config, server logic, RPC, UI, replication, and reconnect.
- For log/debugging questions, search the focused wiki entries for `调试日志说明`, `PIE日志面板`, `日志提取`, `客户端调试管理器`, and `战斗日志`. Distinguish editor PIE logs, local `Clientlog`/`DSlog`, phone client logs, management-platform DS logs, and battle logs.
- Read `references/skill-evolution.md` when deciding whether a conversation, correction, or project pattern should be added to this knowledge bundle.
- UGC project files may be read and analyzed freely.
- Do not directly modify UGC project files unless the user explicitly overrides teaching-only mode for the current task.
- Give exact edit guidance: file path, function/table, code snippet, caveats, and test steps.
- If an API or behavior is not confirmed in the bundled wiki or examples, say so.

## High-Value References

- `references/wiki/README.md`: wiki overview.
- `references/wiki/API参考索引.md`: API/class lookup.
- `references/wiki/代码示例库.md`: Lua examples.
- `references/answer-modes.md`: normal mode vs teaching mode selection.
- `references/code-style.md`: lightweight project code style.
- `references/feature-development-flow.md`: end-to-end feature development flow.
- `references/recipes.md`: common implementation recipes.
- `references/snippets.md`: reusable Lua snippets.
- `references/pitfalls.md`: gotchas and verification reminders.
- `references/project-patterns.md`: project architecture patterns.
- `references/skill-evolution.md`: controlled protocol for updating the knowledge bundle.

## Search

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" references
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\scripts\search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```

## Answer Shape For Code Help

Choose the answer mode first:

- Normal mode: concise, practical, review-friendly, and direct. Use when the user asks for a quick answer, a narrow low-risk fix, or an answer intended for experienced teammates to review.
- Teaching mode: detailed, step-by-step. Use when the user asks to learn, says `教学模式`, asks `为什么` / `从底层讲` / `详细讲`, or the change crosses RPC, save data, replication, reconnect, or multiplayer authority.

Normal mode shape:

```text
结论:
<short direct answer>

依据:
<confirmed from project code / confirmed from wiki / inferred from existing pattern>

改哪里:
<file path + function/table>

最小改动:
<focused snippet with detailed Chinese comments inside the code block>

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

For teaching-mode code changes, answer like a detailed edit walkthrough:

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

When changing an existing block, show both `现在是:` and `改成:`. For Lua return lists, tables, and RPC registration, explicitly call out commas and separators.
