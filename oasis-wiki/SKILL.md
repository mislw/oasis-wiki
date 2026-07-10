---
name: oasis-wiki
description: Always use for Oasis/绿洲启元/绿洲起源/和平精英 UGC projects, UGCProjects workspaces, or UGC Lua code, even if the skill is not named. Trigger on 绿洲启元, 绿洲起源, 起源UGC, 和平精英UGC, UGC项目, 策划案, 玩法案, 需求文档, 项目方案, 系统设计, 全局规划, 版本规划, 数值表, UI流程, 关卡流程, 经济系统, 养成系统, UGC Lua, GameMode, GameState, PlayerController, PlayerState, PlayerPawn, UIManager, EventDefine, Action_*, UnrealNetwork, LuaQuickFireEvent, GetAvailableServerRPCs, UGCGameSystem, UGCEventSystem, GameplayStatics, replication, RPC, UI, logs, DSlog, Clientlog, UGCClientLog, UGCServerLog, PIE日志面板, ugcprint, game_id, countdowns, skills, respawn, reconnect, debugging, performance, templates, and editor workflows. When a path, current workspace, or uploaded file can be associated with a known project name, route through that project's local planning memory and cache before answering. Search the bundled local wiki and distilled project references before giving technical guidance or code. Default to concise normal mode; use teaching mode only when the user explicitly asks for teaching mode, detailed explanation, step-by-step guidance, or beginner-friendly walkthrough output. Read project files freely, but do not directly modify UGC project files unless explicitly overridden.
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

Default to normal mode. Use teaching mode only when the user explicitly asks for `教学模式`, says `详细讲` / `教我` / `一步一步` / `拆一下`, or asks for beginner-friendly walkthrough output. Feature planning should still use `references/feature-development-flow.md`, and normal mode should still briefly summarize the existing project foundation before giving the smallest practical plan. For UGC project files, read freely and analyze freely, but do not directly modify project files unless the user explicitly overrides this rule.

## Workflow

1. Search first; do not load the full wiki into context. Start with `references/wiki/README.md` to confirm available indexes.
2. For feature/API/system questions (`怎么用`, `怎么做`, `有没有`, `支持吗`, class/API names, editor feature names, templates, systems, components), search the official documentation bundle before giving a conclusion. This includes both the base official wiki teaching docs in `references/wiki/*.md` and the 2026-07-10 official update files:
   - `references/wiki/官方API参考手册.md` for class, enum, function, parameter, and API existence.
   - `references/wiki/新增内容_1.37版本.md` for new/changed official features and 1.37 behavior.
   - `references/wiki/论坛经验帖_绿洲启妹.md` for official forum tutorials, practical setup steps, and implementation examples.
3. Use `references/wiki/README.md` to choose the matching official wiki teaching document by category, such as UI, GamePlay systems, skills, items, monsters, editor workflows, templates, debugging, and performance. Use `references/wiki/API参考索引.md`, `references/wiki/代码示例库.md`, and `references/wiki/术语表.md` as focused lookup indexes.
4. Choose answer style with `references/answer-modes.md`. Use normal mode by default. Read `references/teaching-mode.md` only when the user explicitly requests teaching mode, detailed explanation, step-by-step guidance, or beginner-friendly walkthrough output.
5. For current-project context, read `references/project-cache.md`; for uploaded plans, project docs, or project-name/path routing, read `references/project-planning-memory.md`.
6. For feature implementation planning, read `references/feature-development-flow.md`. Start by summarizing `已有基础`, then plan config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect.
7. For Lua code style or review, read `references/code-style.md`. Match wiki/project style and avoid excessive defensive checks that add noise without recovery behavior.
8. For common tasks, snippets, gotchas, or architecture planning, read only the relevant file: `references/recipes.md`, `references/snippets.md`, `references/pitfalls.md`, or `references/project-patterns.md`.
9. For log/debugging questions, inspect available project/editor logs first when possible, and distinguish PIE logs, local `Clientlog`/`DSlog`, phone logs, management-platform DS logs, and battle logs.
10. If the user asks whether knowledge should be added to this skill, read `references/skill-evolution.md` and follow the controlled update protocol.
11. For implementation answers, cite relevant local file paths and line numbers when possible. Preserve existing teammate behavior, names, call order, formatting, RPC names, event IDs, save keys, and project style unless the change is required and explained.

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

The full markdown export lives in `references/wiki`. It contains 58 base Markdown files plus official 2026-07-10 updates: `新增内容_1.37版本.md`, `论坛经验帖_绿洲启妹.md`, and `官方API参考手册.md`. Use `官方API参考手册.md` for class/enum/API lookup, `新增内容_1.37版本.md` for 1.37 release changes, and `论坛经验帖_绿洲启妹.md` for official forum tutorials and implementation examples.

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
