---
name: oasis-wiki
description: Always use for Oasis/绿洲启元/绿洲起源/和平精英 UGC projects, UGCProjects workspaces, or UGC Lua code, even if the skill is not named. Trigger on 绿洲启元, 绿洲起源, 起源UGC, 和平精英UGC, UGC项目, UGC Lua, GameMode, GameState, PlayerController, PlayerState, PlayerPawn, UIManager, EventDefine, Action_*, UnrealNetwork, LuaQuickFireEvent, GetAvailableServerRPCs, UGCGameSystem, UGCEventSystem, GameplayStatics, replication, RPC, UI, logs, DSlog, Clientlog, UGCClientLog, UGCServerLog, PIE日志面板, ugcprint, game_id, countdowns, skills, respawn, reconnect, debugging, performance, templates, and editor workflows. Search the bundled local wiki and distilled project references before giving technical guidance or code. Default to teaching-only mode: read project files freely, but do not directly modify UGC project files unless explicitly overridden.
---

# Oasis Wiki

Use this skill for Oasis/绿洲启元 and 和平精英 UGC development questions. The bundled wiki is the source of truth for Lua APIs, editor workflows, gameplay systems, UI, templates, troubleshooting, and examples. The project-pattern references add distilled practices mined from local UGC projects, including reusable lessons from project-specific examples.

## Always Invoke

Invoke this skill for every user question that looks like it belongs to a 绿洲启元/绿洲起源/和平精英 UGC project, even when the user asks casually or only mentions a project file/class/API name.

Treat these as strong signals:

- Chinese project/domain wording: `绿洲启元`, `绿洲起源`, `起源UGC`, `和平精英UGC`, `UGC项目`, `玩法`, `编辑器`, `脚本`, `蓝图`, `项目工程`.
- Workspace/path wording: `UGCProjects`, `ShadowTrackerExtra`, `Script/Blueprint`, `Script/gamemode`, `Script/GameConfigs`, `Script/UI`.
- Common code names: `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `GlobalConfig`, `Action_*`.
- Common APIs/patterns: `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCEventSystem`, `UGCTimerTools`, `UGCBackPackSystem`, `UGCTeamSystem`, `GameplayStatics`, `UE.LoadClass`, `UE.LoadObject`, `AddToViewport`, `RepLazyProperty`, `ugcprint`.
- Logs and debugging wording: `日志`, `调试日志`, `PIE日志面板`, `战斗日志`, `日志提取`, `DS日志`, `客户端日志`, `服务端日志`, `DSlog`, `Clientlog`, `FullLog`, `UGCClientLog`, `UGCServerLog`, `game_id`.
- Gameplay tasks: UI buttons, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, damage, items, widgets, game phases, debugging, logs, performance.

Default to teaching-only mode for UGC project files: read freely, analyze freely, and explain exact edits, but do not directly modify project files unless the user explicitly overrides this rule. Read `references/teaching-mode.md` before giving code-change guidance.

## Workflow

1. Search first; do not load the full wiki into context.
2. Prefer the focused index files when starting:
   - `references/wiki/README.md` for the knowledge base overview.
   - `references/wiki/API参考索引.md` for API and class names.
   - `references/wiki/代码示例库.md` for Lua examples.
   - `references/wiki/术语表.md` for terminology.
   - Project-specific quick-reference files only when the user is explicitly discussing that project or when mining reusable project lessons.
3. For code-change guidance, read `references/answer-modes.md` first to choose normal mode or teaching mode, then read `references/teaching-mode.md` when teaching-mode detail is needed.
4. Teach the user where and how to edit instead of modifying UGC project files directly.
5. For common tasks such as UI buttons, RPCs, countdowns, phases, loadouts, widgets, skills, reconnects, or debugging, read `references/recipes.md`.
6. For log and debugging questions, search and read the focused wiki entries for `调试日志说明`, `PIE日志面板`, `日志提取`, `客户端调试管理器`, and `战斗日志`. Distinguish editor PIE logs, local `Clientlog`/`DSlog`, phone client logs, management-platform DS logs, and battle logs.
7. For end-to-end feature work, especially UI -> ServerRPC -> ClientRPC/event -> replication -> reconnect, read `references/feature-development-flow.md`.
8. For template code blocks, read `references/snippets.md` and adapt names/paths/IDs to the user's project.
9. Before finalizing code advice, scan `references/pitfalls.md` for gotchas that apply.
10. For practical architecture or "how should I structure this project?" questions, read `references/project-patterns.md`.
11. If the project-pattern summary is not enough and the local project corpus is available, use `references/project-mining-index.md` for targeted search commands and representative source paths.
12. If the user asks whether new knowledge should be added to this skill, read `references/skill-evolution.md` and follow the controlled update protocol.
13. For implementation answers, cite the relevant local file paths and line numbers when possible.
14. When writing Lua, match the wiki examples and API naming exactly. If a detail is not found, say that the local wiki did not confirm it.
15. When providing Lua or UGC code snippets, include detailed Chinese comments in every code block. Explain intent, control flow, key variables, server/client boundaries, RPC/replication behavior, UI bindings, timers, config IDs, nil guards, and fragile Lua syntax near the lines they affect.
16. When designing or explaining a feature change, minimize impact on existing code. Prefer small additive changes, local helper functions, guarded branches, config-driven hooks, and narrow insertion points over rewrites. Preserve existing behavior, formatting, naming, and call order unless changing them is required and explicitly explained.
17. For broad questions, synthesize from 2-4 relevant files rather than one giant context load.

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

The full markdown export lives in `references/wiki`. It contains 59 Markdown files, about 278 articles, 263 Lua examples, and 1140 API/class references as of the bundled export generated on 2026-06-16.

Additional distilled references:

- `references/project-patterns.md`: reusable architecture and coding patterns mined from local UGC projects.
- `references/project-mining-index.md`: representative project paths and search commands for deeper inspection.
- `references/answer-modes.md`: rules for choosing normal mode or teaching mode.
- `references/teaching-mode.md`: code-teaching workflow and project-file read-only constraint.
- `references/feature-development-flow.md`: end-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `references/recipes.md`: common implementation recipes for UGC coding tasks.
- `references/snippets.md`: small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `references/pitfalls.md`: gotchas and verification reminders to check before giving code advice.
- `references/skill-evolution.md`: controlled protocol for deciding when and how to update this skill.
