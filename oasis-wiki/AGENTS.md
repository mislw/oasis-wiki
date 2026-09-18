# Agent Instructions For This Skill Folder

Use this folder as a portable Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua knowledge bundle.

Codex should use `SKILL.md`. Other AI coding agents should follow this file.

## Always Invoke

Always use this folder when a question appears related to a 绿洲启元/绿洲起源/和平精英 UGC project, UGCProjects workspace, UGC Lua code, UGCAskQ MCP/editor automation, or project-level planning material for a UGC project.

Strong signals include `UGCGameSystem`, `UnrealNetwork`, `GetAvailableServerRPCs`, `LuaQuickFireEvent`, `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UIManager`, `EventDefine`, `Action_*`, UI, RPC, replication, countdowns, loadouts, skills, teams, respawn, reconnect, debugging, logs, DSlog, Clientlog, `UGCClientLog`, `UGCServerLog`, `PIE日志面板`, `ugcprint`, `game_id`, performance, editor workflows, `UGCAskQ`, `MCP`, `MCP Server`, `Model Context Protocol`, `.mcp.json`, `mcpServers`, `SSE`, `Port 33444`, `Start Server`, `Enable MCP Call Logging`, AI editor automation, `长连接 MCP`, `MCP 代理`, `绕过直连 MCP`, `让 Codex 用 MCP`, `直接修改编辑器`, `正在重新连接`, `reconnecting`, `stream disconnected before completion`, `response.completed`, `原生 MCP`, `native MCP`, `做一下 UI 生成`, `我有一个 UI 需要生图`, `帮我做个 UI`, `启动 UI 生图工具`, `策划案`, `玩法案`, `需求文档`, `项目方案`, `系统设计`, `全局规划`, `版本规划`, `数值表`, `UI流程`, `关卡流程`, `经济系统`, `养成系统`, `项目细节`, and `项目记忆`.

If a path, current workspace, or uploaded filename contains a known project name, route the question through that project's local planning memory and cache before answering.

## Rules

- Search `references/` before answering.
- For official wiki freshness checks, run `scripts/sync_official_wiki.py --dry-run`. Run it without `--dry-run` only after the user explicitly asks to synchronize the bundled wiki, then inspect the generated diff and validate the article count and IDs.
- For new official developer-forum material from 绿洲启妹, run `scripts/sync_official_forum.py --dry-run`. Run it without `--dry-run` only after explicit synchronization approval, then verify the author, approval state, requested thread IDs, and absence of duplicate IDs in `references/wiki/论坛经验帖_绿洲启妹.md`.
- Read `references/task-router.md` first for UGC project work. Classify the request as project analysis, feature development, debugging/errors, MCP operation, config/balancing, UI/interaction, or project safety. Choose one primary branch and at most one secondary branch before loading detailed references.
- For AI UI generation, SOURCE 文字引导, editable component extraction, layer manifests, or RedCliff UI delivery plans, read `references/cowart-ui-workflow.md`. Keep Game UI Design System as the upstream style/UI Tree gate and require explicit authorization before any UGC project mutation.
- For a real PSD whose group/layer hierarchy must become UMG controls, read `references/cowart-ui/psd-to-umg.md`. Parse the structured PSD tree, review the normalized manifest and UI Tree, and never flatten all layers into sibling widgets.
- The native Companion UI workflow is enabled. When the user explicitly asks to open, start, continue, or review the UI workflow or Workbench, use the native handoff and open the applicable registered page after verifying its session identity. Opening Companion or Workbench never authorizes editor writes.
- When UI image generation, interface mockup work, control slicing/separation, component extraction, layer splitting, or PSD hierarchy import is detected outside an already active Cowart UI flow, ask once per task: `检测到你正在进行 UI 生图、控件拆分或 PSD 层级导入，是否需要我接入 UI 工具链，帮你同步当前进度并继续协助？` On acceptance, summarize and synchronize the current context before continuing the applicable stage. Open Companion or Workbench only after an explicit request or when presenting the generated handoff is part of the requested review. On refusal, continue the current task and do not ask again.
- After Workbench `保存布局`, phrases such as `确认导入` and `按刚保存的位置导入` require the Agent to explicitly read the applicable `layout-review.json`, require `pending_chat_confirmation`, and verify `source.session_sha256` against the current `session.json`. Workbench does not automatically return the file to chat. Use the page already identified by the conversation or the sole pending page when there is exactly one; never select the newest snapshot when multiple pages are pending. 保存布局不等于编辑器写入授权: retain the exact WidgetBlueprint `load_path`, project match, frozen UMG plan, read-only preflight, project-external backup, and explicit-write authorization gates.
- For feature/API/system questions (`怎么用`, `怎么做`, `有没有`, `支持吗`, class/API names, editor feature names, templates, systems, components), search the official documentation bundle before giving a conclusion. This includes the base official wiki teaching docs in `references/wiki/*.md`, plus `references/wiki/官方API参考手册.md`, `references/wiki/新增内容_1.37版本.md`, `references/wiki/论坛经验帖_绿洲启妹.md`, and `references/wiki/官方宣讲会回顾.md` for 宣讲会/绿洲工坊 briefings and version details the wiki snapshot does not cover yet.
- For MCP/editor automation questions, search `references/wiki/新增内容_1.37版本.md` for `UGCAskQ MCP 使用说明` when setup or official behavior is uncertain and read `references/mcp-integration.md`. Then branch: use `references/mcp-ui-widget.md` for UI/Widget/UMG/Blueprint viewing or generation, and `references/mcp-datatable.md` for config tables/DataTable/UAEDataTable work. Use both only for genuinely mixed UI+table tasks. Confirm the feature is experimental, the editor MCP Server is running locally, the SSE URL/port match the panel, `.mcp.json` or client MCP settings are configured correctly, call logging is enabled when debugging, and users save or back up the project before AI-driven editor operations. If Codex direct/native MCP registration enters reconnect loops (`正在重新连接 1/5`, `正在重新连接 4/5`, `reconnecting`) or fails with stream-completion errors (`stream disconnected before completion`, missing `response.completed`), immediately stop retrying native MCP and use the local HTTP proxy workflow in `references/mcp-integration.md` instead. Also use the proxy when the user asks for `长连接 MCP` / `MCP 代理` / `绕过直连 MCP` / `让 Codex 用 MCP`.
- PIE debugging must use `ue_pie` for start, stop, Lua hot reload, and client/DS Lua execution, and must not use computer control to click editor PIE controls. Every `ue_pie` call with `action=start` must explicitly set `simulation_platform=mobile`; never omit this field and never use the PC platform value `pchd`. Other actions do not need the platform field. If `ue_pie` is absent or unavailable, inspect the MCP connection and `tools/list`, report the blocker, and do not fall back to computer control. Read `references/mcp-integration.md` for the fast Lua loop, PIE session resource, and log-verification requirements.
- Read `references/answer-modes.md` before choosing concise normal mode or detailed teaching mode. Default to normal mode.
- Read `references/teaching-mode.md` only when the user explicitly asks for `教学模式`, detailed explanation, step-by-step guidance, or beginner-friendly walkthrough output. Teaching mode is always read-only for UGC project files; do not directly edit project code, assets, or configs in teaching mode.
- During an active teaching task, `收尾` explicitly switches to normal/direct mode and authorizes implementation of only the already explained and agreed current-task plan. Complete implementation and verification, then remain in the default normal mode. The phrase does not bypass unresolved product choices, protected-history rules, editor/binary-write approval, deletion, commit, push, paid actions, or other separate authorization gates.
- Read `references/code-style.md` before writing or reviewing Lua code, especially config tables, member variables, methods, or `GlobalConfig` entries.
- Read `references/feature-development-flow.md` for end-to-end feature work that crosses config, server logic, RPC, UI, replication, save/archive, and reconnect.
- Before teaching or planning a new feature, summarize the project's existing foundation first: already declared configs, attributes, event IDs, RPC names, UI widgets, save keys, replicated fields, helper methods, current data owners, and teammate partial implementations. Then explain the missing pieces and the overall config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect plan.
- Hard code-change rule: never directly rewrite, restructure, wrap, rename, or reorder existing teammate/predecessor code just to make a cleaner implementation. Prefer extending the existing feature's variables, functions, data owners, RPC/event paths, archive keys, replication, and refresh flow instead of adding a parallel field, helper, manager, or second flow. Add something new only when the existing implementation cannot satisfy the required semantics, ownership boundary, lifecycle, compatibility, or verification path; first explain that concrete reason and the affected behavior, then make only the smallest compatible change.
- For UI replacement or rebinding, preserve the existing runtime behavior exactly and only remap the new Widget controls to the existing callbacks, events, RPCs, data owners, and refresh functions. Do not change gameplay rules or unrelated code.
- Before any project code or Lua binding edit, use focused `git blame` and `git log` on the exact target block and resolve protected ownership from private local agent instructions. Never publish or reveal the protected person's identity. Protected code is frozen; an unavoidable UI rebinding compatibility edit requires anonymous, exact, task-specific user authorization before any protected line is touched.
- Before explaining, planning, or implementing a feature, resolve the configured primary predecessor from private local instructions. Search same-type implementations authored by the primary predecessor only by default, in the current project and then `RedCliff`, `StarMon`, and `StealItem`. Search the bundled knowledge base in the same pass. Search the secondary predecessor only when the user explicitly requests a broader predecessor search; use other authors only for exact-block ownership, compatibility, and current-project foundation checks. When a relevant code or knowledge-base document is confirmed, include the exact standalone sentence `已查到相关实现` without revealing any configured identity. Report code evidence as project, file, function/table, and commit; report documentation evidence as knowledge-base file and section/article.
- Knowledge-first feature change gate: Before modifying or adding a gameplay or UI feature, configuration-backed behavior, editor workflow, or other UGC capability, search the bundled knowledge base in `references/wiki/*.md` before the first edit, using the feature/system name, class/API names, and synonyms. A confirmed knowledge-base hit uses the same `已查到相关实现` acknowledgement and evidence format. Before a third implementation attempt, if two consecutive edit-and-verify attempts have failed, stop and search the bundled knowledge base again using the observed symptom and exact error text before changing code or assets again.
- When confirmed implementation or usage guidance comes from a synchronized official Wiki article, include a clickable Markdown link to that exact article in the user-facing evidence, using the matched article's own `官网原文` URL rather than guessing from its title or category. Keep the local knowledge-base file and section/article citation as well. Link every official article that materially supports the answer. Do not present distilled local references as official Wiki pages. For official API evidence, use the exact API URL already stored in the matched entry when available; otherwise link only the official API root and say that no exact deep link was confirmed.
- When checks find unexpected generated project files such as `__pycache__/`, `*.pyc`, temporary automation output, or unplanned Markdown, inspect and explain the file before acting. Classify it as untracked, staged, committed, or pushed; ask the user whether to delete it and add a narrow ignore rule. If already pushed, ask whether to create a normal cleanup commit. Never delete automatically or amend, reset, force-push, or rewrite published history without separate explicit authorization. Read `references/pitfalls.md` under `Unexpected Editor-Incompatible Or Generated Files`.
- Keep defensive code narrow: guard real boundaries such as user input, missing config, async UI lifecycle, RPC payloads, destroyed actors, or optional data. Do not wrap trusted internal project flow in repeated `if` / `UE.IsValid` scaffolding; prefer direct project-style code and small diffs.
- For current-project questions, read `references/project-cache.md` when local project memory may help. Check `%USERPROFILE%\.codex\oasis-project-cache` before broad project scans. If the user asks to cache, parse, or broadly analyze a project, run `scripts/index-oasis-project.ps1`. If the user says `记住这个功能`, `同步一下项目知识`, `记录这次改动`, or similar after completing a feature, run `scripts/remember-oasis-feature.ps1`. Never write cache files inside the UGC project workspace.
- For project-level planning, uploaded design docs, requirements, economy/numerical/UI/stage/system details, or any question where a path/current workspace/uploaded filename contains a known project name, read `references/project-planning-memory.md`. Resolve the project identity from the path first, then load that project's local planning memory, feature memories, and index before proposing implementation. Prefer whole-project architecture, system boundaries, data flow, long-term maintainability, and future compatibility over one-off patches.
- For log/debugging questions, search the focused wiki entries for `调试日志说明`, `PIE日志面板`, `日志提取`, `客户端调试管理器`, and `战斗日志`. Distinguish editor PIE logs, local `Clientlog`/`DSlog`, phone client logs, management-platform DS logs, MCP call logs (`Saved/log/MCP_YYYYMMDD.log`), and battle logs. When the user asks why something errored or how an error happened, proactively inspect available project/editor logs first instead of asking the user to look them up. Filesystem log reads are valid verification and are not computer control.
- Read `references/skill-evolution.md` when deciding whether a conversation, correction, or project pattern should be added to this knowledge bundle.
- After updating either the Skill or Oasis Companion, run `python scripts/check_companion_skill_versions.py`. Treat the update as incomplete unless the actual running Companion process matches the installed Skill `VERSION`.
- For flattened AI-generated UI that needs reusable controls, read `references/cowart-ui-workflow.md`, `references/cowart-ui/precision-reconstruction.md`, and `references/cowart-ui/transparent-asset-extraction.md`. Use one complete mother background plus transparent or intentionally translucent controls. Preserve runtime-dynamic text, numbers, timers, progress, labels, and hit targets as native controls by default; developer-confirmed fixed visual lettering may be extracted as a glyph-only transparent asset without changing runtime bindings. Require alpha/checker inspection, parent-residual cleanup, recomposition, profile/catalog validation, and developer review before Stage 3 confirmation.
- UGC project files may be read and analyzed freely.
- Do not directly modify UGC project files unless the user explicitly overrides project-file read-only behavior for the current task.
- In teaching mode, never change UGC project files directly. If existing code must change, give exact file-line instructions, reason through the affected feature path, confirm the prior behavior remains intact, and explain what the changed code does.
- Give exact edit guidance: file path, line number, function/table, code snippet, caveats, and test steps.
- If an API or behavior is not confirmed in the bundled wiki or examples, say so.

## High-Value References

- `references/task-router.md`: task-intent router for project analysis, feature development, debugging/errors, MCP operations, config/balancing, UI/interaction, and project safety.
- `references/cowart-ui-workflow.md`: separate Cowart UI production category for generation, automatic canvas handoff, editable layers, component confirmation, and RedCliff delivery planning.
- `references/cowart-ui/psd-to-umg.md`: structured PSD parsing, manifest validation, reviewed UMG hierarchy mapping, editor-write gates, and the reusable PSD-to-UI prompt.
- `references/wiki/README.md`: wiki overview.
- `references/wiki/*.md`: base official wiki teaching docs by category, including UI, GamePlay systems, skills, items, monsters, editor workflows, templates, debugging, and performance.
- `references/wiki/官方API参考手册.md`: official class, enum, function, parameter, and API lookup.
- `references/wiki/新增内容_1.37版本.md`: official 1.37 feature additions, behavior updates, and UGCAskQ MCP/editor automation guidance.
- `references/wiki/论坛经验帖_绿洲启妹.md`: official forum tutorials, setup steps, and implementation examples.
- `references/wiki/官方宣讲会回顾.md`: hand-maintained archive of official 宣讲会/绿洲工坊 briefings, limited to details the synchronized wiki snapshot does not cover yet (功能模板, 管理平台 grouping and 工单管理, lobby 灰度/新潜榜/Banner, 赛事征集, 光谱计划).
- `references/wiki/API参考索引.md`: API/class lookup.
- `scripts/sync_official_wiki.py`: official wiki catalog/article validation and authorized full snapshot regeneration.
- `scripts/sync_official_forum.py`: selected official forum-thread validation and authorized collection refresh.
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
- `references/mcp-integration.md`: shared UGCAskQ MCP connection, local long-lived HTTP proxy for Codex, setup, branch routing, safety, and evidence workflow.
- `references/mcp-ui-widget.md`: MCP UI/Widget/UMG/Blueprint viewing and generation workflow.
- `references/mcp-datatable.md`: MCP config table/DataTable/UAEDataTable workflow.
- `references/skill-evolution.md`: controlled protocol for updating the knowledge bundle.
- `references/cowart-ui-workflow.md`: staged workflow for turning approved UI visuals into reviewable reusable controls.
- `references/cowart-ui/precision-reconstruction.md`: Stage 2A/2B recognition, reconstruction, recomposition, and review gate.
- `references/cowart-ui/transparent-asset-extraction.md`: Mother-background composition, visual-text extraction, child-icon separation, transparency decisions, and validation gates.
- `references/cowart-ui/component-extractor.md`: extraction-plan schema and local command-line tools.

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
