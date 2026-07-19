# Agent Instructions For This Skill Folder

Use this folder as a portable Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua knowledge bundle.

Codex should use `SKILL.md`. Other AI coding agents should follow this file.

## Always Invoke

Always use this folder when a question appears related to a 绿洲启元/绿洲起源/和平精英 UGC project, UGCProjects workspace, UGC Lua code, UGCAskQ MCP/editor automation, or project-level planning material for a UGC project.

Strong signals include `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UIManager`, `EventDefine`, `Action_*`, UI, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, debugging, logs, DSlog, Clientlog, `UGCClientLog`, `UGCServerLog`, `PIE日志面板`, `ugcprint`, `game_id`, performance, editor workflows, `UGCAskQ`, `MCP`, `MCP Server`, `Model Context Protocol`, `.mcp.json`, `mcpServers`, `SSE`, `Port 33444`, `Start Server`, `Enable MCP Call Logging`, AI editor automation, `策划案`, `玩法案`, `需求文档`, `项目方案`, `系统设计`, `全局规划`, `版本规划`, `数值表`, `UI流程`, `关卡流程`, `经济系统`, `养成系统`, `项目细节`, and `项目记忆`.

If a path, current workspace, or uploaded filename contains a known project name, route the question through that project's local planning memory and cache before answering.

## Rules

- Search `references/` before answering.
- Read `references/task-router.md` first for UGC project work. Classify the request as project analysis, feature development, debugging/errors, MCP operation, config/balancing, UI/interaction, or project safety. Choose one primary branch and at most one secondary branch before loading detailed references.
- For feature/API/system questions (`怎么用`, `怎么做`, `有没有`, `支持吗`, class/API names, editor feature names, templates, systems, components), search the official documentation bundle before giving a conclusion. This includes the base official wiki teaching docs in `references/wiki/*.md`, plus `references/wiki/官方API参考手册.md`, `references/wiki/新增内容_1.37版本.md`, and `references/wiki/论坛经验帖_绿洲启妹.md`.
- For MCP/editor automation questions, search `references/wiki/新增内容_1.37版本.md` for `UGCAskQ MCP 使用说明` when setup or official behavior is uncertain and read `references/mcp-integration.md`. Use `references/mcp-ui-widget.md` for UI/Widget work, `references/mcp-datatable.md` for DataTable/UAEDataTable work, and `references/mcp-config-driven-ui.md` when a table-backed UI must change through Lua/RPC. Confirm the editor MCP Server, SSE URL/port, call logging, and external `.uasset` backup before writes.
- Read `references/answer-modes.md` before choosing concise normal mode or detailed teaching mode. Default to normal mode.
- Read `references/teaching-mode.md` only when the user explicitly asks for `教学模式`, detailed explanation, step-by-step guidance, or beginner-friendly walkthrough output. Teaching mode is always read-only for UGC project files; do not directly edit project code, assets, or configs in teaching mode.
- Read `references/code-style.md` before writing or reviewing Lua code, especially config tables, member variables, methods, or `GlobalConfig` entries.
- Read `references/feature-development-flow.md` for end-to-end feature work that crosses config, server logic, RPC, UI, replication, save/archive, and reconnect.
- Before teaching or planning a new feature, summarize the project's existing foundation first: already declared configs, attributes, event IDs, RPC names, UI widgets, save keys, replicated fields, helper methods, current data owners, and teammate partial implementations. Then explain the missing pieces and the overall config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect plan.
- For current-project questions, read `references/project-cache.md` when local project memory may help. Check `%USERPROFILE%\.codex\oasis-project-cache` before broad project scans. If the user asks to cache, parse, or broadly analyze a project, run `scripts/index-oasis-project.ps1`. If the user says `记住这个功能`, `同步一下项目知识`, `记录这次改动`, or similar after completing a feature, run `scripts/remember-oasis-feature.ps1`. Never write cache files inside the UGC project workspace.
- For project-level planning, uploaded design docs, requirements, economy/numerical/UI/stage/system details, or any question where a path/current workspace/uploaded filename contains a known project name, read `references/project-planning-memory.md`. Resolve the project identity from the path first, then load that project's local planning memory, feature memories, and index before proposing implementation. Prefer whole-project architecture, system boundaries, data flow, long-term maintainability, and future compatibility over one-off patches.
- For log/debugging questions, search the focused wiki entries for `调试日志说明`, `PIE日志面板`, `日志提取`, `客户端调试管理器`, and `战斗日志`. Distinguish editor PIE logs, local `Clientlog`/`DSlog`, phone client logs, management-platform DS logs, MCP call logs (`Saved/log/MCP_YYYYMMDD.log`), and battle logs. When the user asks why something errored or how an error happened, proactively inspect available project/editor logs first instead of asking the user to look them up.
- Read `references/skill-evolution.md` when deciding whether a conversation, correction, or project pattern should be added to this knowledge bundle.
- UGC project files may be read and analyzed freely.
- Do not directly modify UGC project files unless the user explicitly overrides project-file read-only behavior for the current task.
- In teaching mode, never change UGC project files directly. If existing code must change, give exact file-line instructions, reason through the affected feature path, confirm the prior behavior remains intact, and explain what the changed code does.
- Give exact edit guidance: file path, line number, function/table, code snippet, caveats, and test steps.
- If an API or behavior is not confirmed in the bundled wiki or examples, say so.

## High-Value References

- `references/task-router.md`: task-intent router for project analysis, feature development, debugging/errors, MCP operations, config/balancing, UI/interaction, and project safety.
- `references/wiki/README.md`: wiki overview.
- `references/wiki/*.md`: base official wiki teaching docs by category, including UI, GamePlay systems, skills, items, monsters, editor workflows, templates, debugging, and performance.
- `references/wiki/官方API参考手册.md`: official class, enum, function, parameter, and API lookup.
- `references/wiki/新增内容_1.37版本.md`: official 1.37 feature additions, behavior updates, and UGCAskQ MCP/editor automation guidance.
- `references/wiki/论坛经验帖_绿洲启妹.md`: official forum tutorials, setup steps, and implementation examples.
- `references/wiki/API参考索引.md`: API/class lookup.
- `references/wiki/代码示例库.md`: Lua examples.
- `references/answer-modes.md`: normal mode vs teaching mode selection.
- `references/code-style.md`: lightweight project code style.
- `references/feature-development-flow.md`: end-to-end feature development flow.
- `references/recipes.md`: common implementation recipes.
- `references/snippets.md`: reusable Lua snippets.
- `references/pitfalls.md`: gotchas and verification reminders.
- `references/project-patterns.md`: project architecture patterns.
- `references/project-cache.md`: local computer cache workflow for reusing parsed information from a specific UGC project.
- `references/project-planning-memory.md`: project-name/path routing workflow for uploaded planning docs, requirements, system details, and whole-project design memory.
- `references/mcp-integration.md`: shared UGCAskQ MCP connection, setup, branch routing, safety, and evidence workflow.
- `references/mcp-ui-widget.md`: MCP UI/Widget/UMG/Blueprint viewing and generation workflow.
- `references/mcp-datatable.md`: MCP config table/DataTable/UAEDataTable workflow.
- `references/mcp-config-driven-ui.md`: combined DataTable -> Lua/RPC -> Widget refresh workflow and failure matrix.
- `references/skill-evolution.md`: controlled protocol for updating the knowledge bundle.

## Search

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" references
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\scripts\search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```

## Answer Shape For Code Help

Choose the answer mode first:

- Normal mode: concise, practical, review-friendly, and direct. Use by default.
- Teaching mode: detailed, step-by-step. Use only when the user asks for `教学模式`, says `详细讲` / `教我` / `一步一步` / `拆一下`, or explicitly wants beginner-friendly walkthrough output.

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

For teaching-mode code changes, answer like a detailed edit walkthrough:

```text
0. 已有基础

项目里已经有:
<existing declarations / configs / RPCs / events / UI / helpers / save or replication fields>

还缺:
<missing pieces needed by this feature>

整体做法:
<config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect plan>

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
