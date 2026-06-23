---
name: oasis-wiki
description: Always use when a user question appears related to an Oasis/绿洲启元/绿洲起源/和平精英 UGC project, UGCProjects workspace, or UGC Lua code, even if the user does not explicitly name this skill. Trigger on Chinese or English mentions such as 绿洲启元, 绿洲起源, 起源UGC, 和平精英UGC, UGC项目, UGCProjects, UGC Lua, GameMode, GameState, PlayerController, PlayerState, PlayerPawn, UIManager, EventDefine, Action_*, LuaQuickFireEvent, GetAvailableServerRPCs, UnrealNetwork, UGCGameSystem, UGCEventSystem, UGCTimerTools, UGCBackPackSystem, UGCTeamSystem, GameplayStatics, UE.LoadClass, UE.LoadObject, AddToViewport, replication, RPC, UI, countdowns, loadouts, skills, teams, respawn, reconnect, debugging, performance, templates, and editor workflows. Use when answering questions or teaching code for Oasis/绿洲启元/和平精英 UGC Lua development, including API lookup, gameplay systems, UI systems, editor workflows, examples, templates, debugging, performance, release notes, terminology, practical project architecture patterns, common implementation recipes, code snippets, and pitfalls mined from local UGC sample projects. Search the bundled local wiki and distilled project references before giving technical guidance or code for these domains. Default to teaching-only mode: project files may be read freely, but do not directly modify UGC project files unless explicitly overridden.
---

# Oasis Wiki

Use this skill for Oasis/绿洲启元 and 和平精英 UGC development questions. The bundled wiki is the source of truth for Lua APIs, editor workflows, gameplay systems, UI, templates, troubleshooting, and examples. The project-pattern references add distilled practices mined from local UGC projects, including reusable lessons from project-specific examples.

## Always Invoke

Invoke this skill for every user question that looks like it belongs to a 绿洲启元/绿洲起源/和平精英 UGC project, even when the user asks casually or only mentions a project file/class/API name.

Treat these as strong signals:

- Chinese project/domain wording: `绿洲启元`, `绿洲起源`, `起源UGC`, `和平精英UGC`, `UGC项目`, `玩法`, `编辑器`, `脚本`, `蓝图`, `项目工程`.
- Workspace/path wording: `UGCProjects`, `ShadowTrackerExtra`, `Script/Blueprint`, `Script/gamemode`, `Script/GameConfigs`, `Script/UI`.
- Common code names: `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, `UIManager`, `EventDefine`, `GlobalConfig`, `Action_*`.
- Common APIs/patterns: `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCEventSystem`, `UGCTimerTools`, `UGCBackPackSystem`, `UGCTeamSystem`, `GameplayStatics`, `UE.LoadClass`, `UE.LoadObject`, `AddToViewport`, `RepLazyProperty`.
- Gameplay tasks: UI buttons, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, damage, items, widgets, game phases, debugging, performance.

Default to teaching-only mode for UGC project files: read freely, analyze freely, and explain exact edits, but do not directly modify project files unless the user explicitly overrides this rule. Read `references/teaching-mode.md` before giving code-change guidance.

## Workflow

1. Search first; do not load the full wiki into context.
2. Prefer the focused index files when starting:
   - `references/wiki/README.md` for the knowledge base overview.
   - `references/wiki/API参考索引.md` for API and class names.
   - `references/wiki/代码示例库.md` for Lua examples.
   - `references/wiki/术语表.md` for terminology.
   - Project-specific quick-reference files only when the user is explicitly discussing that project or when mining reusable project lessons.
3. For code-change guidance, read `references/teaching-mode.md` and teach the user where and how to edit instead of modifying UGC project files directly.
4. For common tasks such as UI buttons, RPCs, countdowns, phases, loadouts, widgets, skills, reconnects, or debugging, read `references/recipes.md`.
5. For end-to-end feature work, especially UI -> ServerRPC -> ClientRPC/event -> replication -> reconnect, read `references/feature-development-flow.md`.
6. For template code blocks, read `references/snippets.md` and adapt names/paths/IDs to the user's project.
7. Before finalizing code advice, scan `references/pitfalls.md` for gotchas that apply.
8. For practical architecture or "how should I structure this project?" questions, read `references/project-patterns.md`.
9. If the project-pattern summary is not enough and the local project corpus is available, use `references/project-mining-index.md` for targeted search commands and representative source paths.
10. If the user asks whether new knowledge should be added to this skill, read `references/skill-evolution.md` and follow the controlled update protocol.
11. For implementation answers, cite the relevant local file paths and line numbers when possible.
12. When writing Lua, match the wiki examples and API naming exactly. If a detail is not found, say that the local wiki did not confirm it.
13. For broad questions, synthesize from 2-4 relevant files rather than one giant context load.

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
- `references/teaching-mode.md`: code-teaching workflow and project-file read-only constraint.
- `references/feature-development-flow.md`: end-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `references/recipes.md`: common implementation recipes for UGC coding tasks.
- `references/snippets.md`: small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `references/pitfalls.md`: gotchas and verification reminders to check before giving code advice.
- `references/skill-evolution.md`: controlled protocol for deciding when and how to update this skill.
