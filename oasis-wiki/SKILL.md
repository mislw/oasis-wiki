---
name: oasis-wiki
description: Use for Oasis/绿洲启元/绿洲起源/和平精英 UGC projects, UGC Lua, UGCAskQ MCP/editor automation, DataTable/WidgetBlueprint, logs/debugging, project planning, game UI systems, Cowart UI generation, or requests such as 做一下 UI 生成, 我有一个 UI 需要生图, 帮我做个 UI, and 启动 UI 生图工具. Trigger on common UGC classes and APIs including GameMode, GameState, PlayerController, UIManager, EventDefine, UnrealNetwork, LuaQuickFireEvent, UGCGameSystem, RPC, and replication.
---

# Oasis Wiki

For game UI reference analysis, reusable control libraries, project-specific asset catalogs and preview caches, UI Tree planning, or screenshot-to-UI work, use the integrated Game UI Design System branch in `references/game-ui-design-system.md` before MCP WidgetBlueprint operations.

For AI UI generation, automatic native Cowart handoff, editable layer extraction, component confirmation, or RedCliff delivery planning, use the separate Cowart UI Production branch in `references/cowart-ui-workflow.md`. For staged Agent questions, approvals, review gates, backtracking, and result reporting around that existing workflow, also read `references/oasis-ui-agent-interaction.md`.

Natural-language requests such as `做一下 UI 生成`, `我有一个 UI 需要生图`, `帮我做个 UI`, or `启动 UI 生图工具` immediately enter Cowart UI Production. Run `scripts/cowart-ui/component-extractor/open_ui_workflow.py` to open or focus Companion's native UI generation workflow, then continue the SOURCE stage in the same conversation.

Use this skill for Oasis/绿洲启元 and 和平精英 UGC development questions. The bundled wiki is the source of truth for Lua APIs, editor workflows, gameplay systems, UI, templates, troubleshooting, and examples. The project-pattern references summarize generic UGC Lua architecture habits without private project names, local paths, or planning details.

## Always Invoke

Invoke this skill for every user question that looks like it belongs to a 绿洲启元/绿洲起源/和平精英 UGC project, even when the user asks casually or only mentions a project file/class/API name.

Treat these as strong signals:

- Chinese project/domain wording: `绿洲启元`, `绿洲起源`, `起源UGC`, `和平精英UGC`, `UGC项目`, `玩法`, `编辑器`, `脚本`, `蓝图`, `项目工程`.
- Workspace/path wording: `UGCProjects`, `ShadowTrackerExtra`, `Script/Blueprint`, `Script/gamemode`, `Script/GameConfigs`, `Script/UI`.
- Common code names: `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `GlobalConfig`, `Action_*`.
- Common APIs/patterns: `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCEventSystem`, `UGCTimerTools`, `UGCBackPackSystem`, `UGCTeamSystem`, `GameplayStatics`, `UE.LoadClass`, `UE.LoadObject`, `AddToViewport`, `RepLazyProperty`, `ugcprint`.
- MCP/editor automation wording: `UGCAskQ`, `MCP`, `MCP Server`, `Model Context Protocol`, `.mcp.json`, `mcpServers`, `SSE`, `Port 33444`, `Start Server`, `Enable MCP Call Logging`, editor AI automation, AI reads selected actors, AI operates the editor, `长连接 MCP`, `MCP 代理`, `绕过直连 MCP`, `让 Codex 用 MCP`, `直接修改编辑器`, `正在重新连接`, `reconnecting`, `stream disconnected before completion`, `response.completed`, `原生 MCP`, or `native MCP`.
- Logs and debugging wording: `日志`, `调试日志`, `PIE日志面板`, `战斗日志`, `日志提取`, `DS日志`, `客户端日志`, `服务端日志`, `DSlog`, `Clientlog`, `FullLog`, `UGCClientLog`, `UGCServerLog`, `game_id`.
- Planning and project-level wording: `策划案`, `玩法案`, `需求文档`, `项目方案`, `系统设计`, `全局规划`, `版本规划`, `数值表`, `UI流程`, `关卡流程`, `经济系统`, `养成系统`, `项目细节`, `项目记忆`.
- UI generation wording: `做一下 UI 生成`, `我有一个 UI 需要生图`, `帮我做个 UI`, `启动 UI 生图工具`, `生成一张游戏 UI`, `做个界面效果图`.
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
   - MCP operation: `references/mcp-integration.md`, then either `references/mcp-ui-widget.md` or `references/mcp-datatable.md`; use both only for genuinely mixed UI+table tasks.
   - Config/balancing: table schema/usage lookup, `references/mcp-datatable.md` when editor tables are involved, and project code consumers.
   - UI/interaction: UIManager, `Script/UI`, existing button bindings, and `references/mcp-ui-widget.md` only for WidgetBlueprint work.
   - UI design system: `references/game-ui-design-system.md`, then only the required file under `references/game-ui/`. Resolve the project profile and its `.game-ui-system` manifests before extracting controls or generating a page. Use `project_library_asset` references only for confirmed components or resolved semantic items.
   - Cowart UI production: `references/cowart-ui-workflow.md` and `references/oasis-ui-agent-interaction.md`, then `references/cowart-ui/component-extractor.md` or `references/cowart-ui/delivery.md` for the active stage. Use the UI design system as its upstream style and UI Tree gate. The interaction reference adds approval orchestration only; it does not add persistent task state or runtime communication.
   - Project safety: `references/pitfalls.md`, binary asset precautions, dirty file distinction, and backup rules.
7. For MCP/editor automation, search `references/wiki/新增内容_1.37版本.md` for `UGCAskQ MCP 使用说明` when setup or official behavior is uncertain. Confirm the editor MCP Server is running locally, the SSE URL/port match the panel, call logging is enabled when debugging, and backups for `.uasset` files live outside the UGC project tree. If Codex direct/native MCP registration enters reconnect loops (`正在重新连接 1/5`, `正在重新连接 4/5`, `reconnecting`) or fails with stream-completion errors (`stream disconnected before completion`, missing `response.completed`), immediately stop retrying native MCP and use the local HTTP proxy workflow in `references/mcp-integration.md` instead. Also use the proxy when the user asks for `长连接 MCP` / `MCP 代理` / `绕过直连 MCP` / `让 Codex 用 MCP`.
8. For log/debugging questions, inspect available project/editor logs first when possible, and distinguish PIE logs, local `Clientlog`/`DSlog`, phone logs, management-platform DS logs, MCP call logs (`Saved/log/MCP_YYYYMMDD.log`), and battle logs.
9. If the user asks whether knowledge should be added to this skill, read `references/skill-evolution.md`, follow the controlled update protocol, and run `scripts/check-skill-hygiene.ps1` before finishing.
10. For flattened AI-generated UI that needs reusable controls, read `references/cowart-ui-workflow.md` and `references/cowart-ui/precision-reconstruction.md`. Keep text, numbers, timers, progress, labels, and hit targets native; use reconstruction only for reusable artwork and skins; require recomposition plus developer review before Stage 3 confirmation.
11. Hard code-change rule: never directly rewrite, restructure, wrap, rename, or reorder existing teammate/predecessor code just to make a cleaner implementation. Add new logic beside or after the existing flow, keep the original block intact, and make the smallest compatible hook.
12. Keep defensive code narrow: guard only real boundary risks such as user input, missing config, async UI lifecycle, RPC payloads, destroyed actors, or optional data. If an internal required value is supposed to exist for the whole flow, prefer letting the bug surface over wrapping every step in repeated `if` / `UE.IsValid` checks.
13. For implementation answers, cite relevant local file paths and line numbers when possible. Preserve existing teammate behavior, names, call order, formatting, RPC names, event IDs, save keys, and project style unless the change is required and explained.

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
- `references/mcp-integration.md`: UGCAskQ MCP shared connection, setup, local long-lived HTTP proxy for Codex, branch routing, safety checks, PRV, and evidence workflow.
- `references/mcp-ui-widget.md`: MCP branch for viewing/generating UI, WidgetBlueprint/UMG hierarchy, layout, colors, and click interaction.
- `references/mcp-datatable.md`: MCP branch for config tables, DataTable/UAEDataTable lookup, low-token row reads, row mutation, and table-backed gameplay/UI.
- `references/game-ui-design-system.md`: project-routed screenshot analysis, reusable control-library maintenance, UI Tree gates, generation workflow, and automatic UI validation.
- `scripts/game-ui/project_library.py`: project manifest validation and local preview-key resolution used by the Game UI Design System.
- `references/cowart-ui-workflow.md`: separate AI UI generation, automatic Cowart opening, editable component extraction, layer-manifest, confirmation, and RedCliff delivery category.
- `references/oasis-ui-agent-interaction.md`: interaction-only orchestration for Cowart/UI stages, contextual approval gates, review prompts, backtracking, and fail-closed reporting without runtime changes.
- `references/companion-versioning.md`: `M.YYMMDD.N` versioning contract for Companion and bundled Skill builds, including synchronized release metadata.
- `references/answer-modes.md`: rules for choosing normal mode or teaching mode.
- `references/teaching-mode.md`: code-teaching workflow and project-file read-only constraint.
- `references/code-style.md`: lightweight project code style for comments, config tables, variable names, member variables, and methods.
- `references/feature-development-flow.md`: end-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `references/recipes.md`: common implementation recipes for UGC coding tasks.
- `references/snippets.md`: small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `references/pitfalls.md`: gotchas and verification reminders to check before giving code advice.
- `references/skill-evolution.md`: controlled protocol for deciding when and how to update this skill.
- `references/cowart-ui-workflow.md`: staged workflow for turning approved UI visuals into reviewable reusable controls.
- `references/cowart-ui/precision-reconstruction.md`: Stage 2A/2B recognition, reconstruction, recomposition, and review gate.
- `references/cowart-ui/component-extractor.md`: extraction-plan schema and local command-line tools.
