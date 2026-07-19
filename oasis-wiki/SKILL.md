---
name: oasis-wiki
description: Use when working on Oasis/绿洲启元/绿洲起源/和平精英 UGC projects, UGCProjects workspaces, UGC Lua, or UGCAskQ MCP/editor automation. Trigger on UGCGameMode, GameState, PlayerController, UIManager, EventDefine, UnrealNetwork, UGCGameSystem, RPC, replication, UI/WidgetBlueprint, DataTable/UAEDataTable, 数值表, 配置表, table-backed UI, DSlog, Clientlog, PIE日志, debugging, project planning, and editor workflows. Search the bundled wiki and distilled references before giving technical guidance or code. Route known project paths through local project memory/cache. Default to concise normal mode; use teaching mode only when explicitly requested. Read project files freely, but modify them only when the user explicitly authorizes edits.
---

# Oasis Wiki

Use this skill for Oasis/绿洲启元 and 和平精英 UGC development questions. The bundled wiki is the source of truth for Lua APIs, editor workflows, gameplay systems, UI, templates, troubleshooting, and examples. The project-pattern references summarize generic UGC Lua architecture habits without private project names, local paths, or planning details.

## Always Invoke

Invoke this skill for every user question that looks like it belongs to a 绿洲启元/绿洲起源/和平精英 UGC project, even when the user asks casually or only mentions a project file/class/API name.

Treat these as strong signals:

- Chinese project/domain wording: `绿洲启元`, `绿洲起源`, `起源UGC`, `和平精英UGC`, `UGC项目`, `玩法`, `编辑器`, `脚本`, `蓝图`, `项目工程`.
- Workspace/path wording: `UGCProjects`, `ShadowTrackerExtra`, `Script/Blueprint`, `Script/gamemode`, `Script/GameConfigs`, `Script/UI`.
- Common code names: `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `GlobalConfig`, `Action_*`.
- Common APIs/patterns: `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCEventSystem`, `UGCTimerTools`, `UGCBackPackSystem`, `UGCTeamSystem`, `GameplayStatics`, `UE.LoadClass`, `UE.LoadObject`, `AddToViewport`, `RepLazyProperty`, `ugcprint`.
- MCP/editor automation wording: `UGCAskQ`, `MCP`, `MCP Server`, `Model Context Protocol`, `.mcp.json`, `mcpServers`, `SSE`, `Port 33444`, `Start Server`, `Enable MCP Call Logging`, editor AI automation, AI reads selected actors, or AI operates the editor.
- Logs and debugging wording: `日志`, `调试日志`, `PIE日志面板`, `战斗日志`, `日志提取`, `DS日志`, `客户端日志`, `服务端日志`, `DSlog`, `Clientlog`, `FullLog`, `UGCClientLog`, `UGCServerLog`, `game_id`.
- Planning and project-level wording: `策划案`, `玩法案`, `需求文档`, `项目方案`, `系统设计`, `全局规划`, `版本规划`, `数值表`, `UI流程`, `关卡流程`, `经济系统`, `养成系统`, `项目细节`, `项目记忆`.
- Gameplay tasks: UI buttons, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, damage, items, widgets, game phases, debugging, logs, performance.

Default to normal mode. Use teaching mode only when the user explicitly asks for `教学模式`, says `详细讲` / `教我` / `一步一步` / `拆一下`, or asks for beginner-friendly walkthrough output. Feature planning should still use `references/feature-development-flow.md`, and normal mode should still briefly summarize the existing project foundation before giving the smallest practical plan. For UGC project files, read freely and analyze freely. Teaching mode is always read-only for UGC project files and must provide exact file paths, line numbers, and function/table anchors for code guidance.

## Workflow

1. Classify the user request with `references/task-router.md`. Choose one primary task branch and at most one secondary branch before loading detailed references.
2. Search first; do not load the full wiki into context. Start with `references/wiki/README.md` to confirm available indexes when official docs are relevant.
3. For feature/API/system questions (`怎么用`, `怎么做`, `有没有`, `支持吗`, class/API names, editor feature names, templates, systems, components), search the official documentation bundle before giving a conclusion. This includes both the base official wiki teaching docs in `references/wiki/*.md` and the 2026-07-10 official update files:
   - `references/wiki/官方API参考手册.md` for class, enum, function, parameter, and API existence.
   - `references/wiki/新增内容_1.37版本.md` for new/changed official features, 1.37 behavior, the UGCAskQ MCP setup guide, MCP Server panel options, `.mcp.json`/SSE configuration, logging, safety notes, and troubleshooting.
   - `references/wiki/论坛经验帖_绿洲启妹.md` for official forum tutorials, practical setup steps, and implementation examples.
4. Use `references/wiki/README.md` to choose the matching official wiki teaching document by category, such as UI, GamePlay systems, skills, items, monsters, editor workflows, templates, debugging, and performance. Use `references/wiki/API参考索引.md`, `references/wiki/代码示例库.md`, and `references/wiki/术语表.md` as focused lookup indexes.
5. Choose answer style with `references/answer-modes.md`. Use normal mode by default. Read `references/teaching-mode.md` only when the user explicitly requests teaching mode, detailed explanation, step-by-step guidance, or beginner-friendly walkthrough output. In teaching mode, do not directly modify UGC project files; give file-line edit instructions instead.
6. Follow the branch chosen by `references/task-router.md`:
   - Project analysis: `references/project-cache.md`, `references/project-planning-memory.md`, and targeted project files.
   - Feature development: `references/feature-development-flow.md`, plus `references/code-style.md` when editing or reviewing Lua.
   - Debugging/errors: available logs first, then `references/pitfalls.md` and only the branch tied to the symptom.
   - MCP operation: `references/mcp-integration.md`, then either `references/mcp-ui-widget.md` or `references/mcp-datatable.md`. For table-backed UI whose visible values change through Lua/RPC, read `references/mcp-config-driven-ui.md` first and use the branch references only for API detail.
   - Config/balancing: table schema/usage lookup, `references/mcp-datatable.md` when editor tables are involved, and project code consumers.
   - UI/interaction: UIManager, `Script/UI`, existing button bindings, and `references/mcp-ui-widget.md` only for WidgetBlueprint work.
   - Project safety: `references/pitfalls.md`, binary asset precautions, dirty file distinction, and backup rules.
7. For MCP/editor automation, search `references/wiki/新增内容_1.37版本.md` for `UGCAskQ MCP 使用说明` when setup or official behavior is uncertain. Confirm the editor MCP Server is running locally, the SSE URL/port match the panel, call logging is enabled when debugging, and backups for `.uasset` files live outside the UGC project tree.
8. For log/debugging questions, inspect available project/editor logs first when possible, and distinguish PIE logs, local `Clientlog`/`DSlog`, phone logs, management-platform DS logs, MCP call logs (`Saved/log/MCP_YYYYMMDD.log`), and battle logs.
9. If the user asks whether knowledge should be added to this skill, read `references/skill-evolution.md` and follow the controlled update protocol.
10. For implementation answers, cite relevant local file paths and line numbers when possible. Preserve existing teammate behavior, names, call order, formatting, RPC names, event IDs, save keys, and project style unless the change is required and explained.

## Search

Prefer `rg` directly when available:

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" .\references\wiki
rg --line-number --smart-case --glob "*.md" "角色复活" .\references\wiki
```

Helper scripts are also included:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "UGCGameSystem" -MaxResults 20
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "角色复活" -Context 2
node .\scripts\search-oasis-wiki.mjs "UGCGameSystem" --max 20
node .\scripts\search-oasis-wiki.mjs "角色复活" --context 2
```

If running from outside the skill directory, pass an absolute path to the script or set the working directory to the skill folder first.

## Reference Layout

The full markdown export lives in `references/wiki`. It contains 58 base Markdown files plus official 2026-07-10 updates: `新增内容_1.37版本.md`, `论坛经验帖_绿洲启妹.md`, and `官方API参考手册.md`. Use `官方API参考手册.md` for class/enum/API lookup, `新增内容_1.37版本.md` for 1.37 release changes and UGCAskQ MCP/editor automation guidance, and `论坛经验帖_绿洲启妹.md` for official forum tutorials and implementation examples.

Additional distilled references:

- `references/task-router.md`: task-intent router for project analysis, feature development, debugging/errors, MCP operations, config/balancing, UI/interaction, and project safety.
- `references/project-patterns.md`: reusable architecture and coding patterns without private project names or local paths.
- `references/project-cache.md`: local computer cache workflow for reusing parsed information from a specific UGC project.
- `references/project-planning-memory.md`: project-name/path routing workflow for uploaded planning docs, requirements, system details, and whole-project design memory.
- `references/mcp-integration.md`: UGCAskQ MCP shared connection, setup, branch routing, safety checks, PRV, and evidence workflow.
- `references/mcp-ui-widget.md`: MCP branch for viewing/generating UI, WidgetBlueprint/UMG hierarchy, layout, colors, and click interaction.
- `references/mcp-datatable.md`: MCP branch for config tables, DataTable/UAEDataTable lookup, low-token row reads, row mutation, and table-backed gameplay/UI.
- `references/mcp-config-driven-ui.md`: end-to-end MCP workflow for row-struct creation, UAEDataTable population, Lua/RPC state flow, Widget variable binding, Chinese/style/layout handling, runtime logs, and failure diagnosis.
- `references/answer-modes.md`: rules for choosing normal mode or teaching mode.
- `references/teaching-mode.md`: code-teaching workflow and project-file read-only constraint.
- `references/code-style.md`: lightweight project code style for comments, config tables, variable names, member variables, and methods.
- `references/feature-development-flow.md`: end-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `references/recipes.md`: common implementation recipes for UGC coding tasks.
- `references/snippets.md`: small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `references/pitfalls.md`: gotchas and verification reminders to check before giving code advice.
- `references/skill-evolution.md`: controlled protocol for deciding when and how to update this skill.
