---
name: oasis-wiki
description: Always use for Oasis/绿洲启元/绿洲起源/和平精英 UGC projects, UGCProjects workspaces, or UGC Lua code, even if the skill is not named. Trigger on 绿洲启元, 绿洲起源, 起源UGC, 和平精英UGC, UGC项目, 策划案, 玩法案, 需求文档, 项目方案, 系统设计, 全局规划, 版本规划, 数值表, UI流程, 关卡流程, 经济系统, 养成系统, UGC Lua, GameMode, GameState, PlayerController, PlayerState, PlayerPawn, UIManager, EventDefine, Action_*, UnrealNetwork, LuaQuickFireEvent, GetAvailableServerRPCs, UGCGameSystem, UGCEventSystem, GameplayStatics, replication, RPC, UI, logs, DSlog, Clientlog, UGCClientLog, UGCServerLog, PIE日志面板, ugcprint, game_id, countdowns, skills, respawn, reconnect, debugging, performance, templates, and editor workflows. When a path, current workspace, or uploaded file can be associated with a known project name, route through that project's local planning memory and cache before answering. Search the bundled local wiki and distilled project references before giving technical guidance or code. Default to concise normal mode; use teaching mode only when the user explicitly asks to learn, asks for detailed reasoning, or names teaching mode. Read project files freely, but do not directly modify UGC project files unless explicitly overridden.
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
- Logs and debugging wording: `日志`, `调试日志`, `PIE日志面板`, `战斗日志`, `日志提取`, `DS日志`, `客户端日志`, `服务端日志`, `DSlog`, `Clientlog`, `FullLog`, `UGCClientLog`, `UGCServerLog`, `game_id`.
- Planning and project-level wording: `策划案`, `玩法案`, `需求文档`, `项目方案`, `系统设计`, `全局规划`, `版本规划`, `数值表`, `UI流程`, `关卡流程`, `经济系统`, `养成系统`, `项目细节`, `项目记忆`.
- Gameplay tasks: UI buttons, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, damage, items, widgets, game phases, debugging, logs, performance.

Default to concise normal mode. Use teaching mode only when the user explicitly asks to learn, asks for detailed reasoning, names teaching mode, or asks for step-by-step explanation. Feature planning can still use `references/feature-development-flow.md`, but the answer style remains normal unless teaching mode is requested. For UGC project files, read freely and analyze freely, but do not directly modify project files unless the user explicitly overrides this rule.

## Workflow

1. Search first; do not load the full wiki into context. Start with focused indexes such as `references/wiki/README.md`, `references/wiki/API参考索引.md`, `references/wiki/代码示例库.md`, and `references/wiki/术语表.md`.
2. Choose answer style with `references/answer-modes.md`. Read `references/teaching-mode.md` only when teaching mode is explicitly requested.
3. For current-project context, read `references/project-cache.md`; for uploaded plans, project docs, or project-name/path routing, read `references/project-planning-memory.md`.
4. For feature implementation planning, read `references/feature-development-flow.md`. Start by summarizing `已有基础`, then plan config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect.
5. For Lua code style or review, read `references/code-style.md`. Match wiki/project style and avoid excessive defensive checks that add noise without recovery behavior.
6. For common tasks, snippets, gotchas, or architecture planning, read only the relevant file: `references/recipes.md`, `references/snippets.md`, `references/pitfalls.md`, or `references/project-patterns.md`.
7. For log/debugging questions, inspect available project/editor logs first when possible, and distinguish PIE logs, local `Clientlog`/`DSlog`, phone logs, management-platform DS logs, and battle logs.
8. If the user asks whether knowledge should be added to this skill, read `references/skill-evolution.md` and follow the controlled update protocol.
9. For implementation answers, cite relevant local file paths and line numbers when possible. Preserve existing teammate behavior, names, call order, formatting, RPC names, event IDs, save keys, and project style unless the change is required and explained.

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

The full markdown export lives in `references/wiki`. It contains 58 Markdown files + 1 incremental update file, about 278 articles + ~15 new (1.37), 263 Lua examples + ~40 new, and 1140 API/class references + ~50 new. The bundled export was generated on 2026-06-16, with a 1.37 incremental update added on 2026-07-10 in `references/wiki/新增内容_1.37版本.md`.

Additional distilled references:

- `references/project-patterns.md`: reusable architecture and coding patterns without private project names or local paths.
- `references/project-cache.md`: local computer cache workflow for reusing parsed information from a specific UGC project.
- `references/project-planning-memory.md`: project-name/path routing workflow for uploaded planning docs, requirements, system details, and whole-project design memory.
- `references/answer-modes.md`: rules for choosing normal mode or teaching mode.
- `references/teaching-mode.md`: code-teaching workflow and project-file read-only constraint.
- `references/code-style.md`: lightweight project code style for comments, config tables, variable names, member variables, and methods.
- `references/feature-development-flow.md`: end-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `references/recipes.md`: common implementation recipes for UGC coding tasks.
- `references/snippets.md`: small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `references/pitfalls.md`: gotchas and verification reminders to check before giving code advice.
- `references/skill-evolution.md`: controlled protocol for deciding when and how to update this skill.
