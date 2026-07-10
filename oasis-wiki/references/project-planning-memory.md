# Oasis Project Planning Memory

Use this reference when a question is about a whole UGC project rather than a single isolated feature, especially when the user uploads or mentions planning documents, design notes, economy/numerical tables, UI flows, stage flows, system rules, or project details.

## Goal

Route project-level work through the correct project's local memory so answers consider the full design context, existing architecture, future systems, and long-term maintainability.

Do not treat uploaded planning material as temporary chat-only context when the user wants the project to remember it. Distill it into local project planning memory under the user's machine cache, then reuse it in later answers.

## Project Identity Routing

Resolve the project before answering:

1. Prefer the current workspace root when it is inside `UGCProjects\<project-name>`.
2. If the user uploads or references a file path, inspect the path segments and filename for a project name.
3. Match the project name against local cache folders under:

```text
%USERPROFILE%\.codex\oasis-project-cache\<project-name>-<path-hash>\
```

4. If more than one cache folder has the same project name, open each `index\manifest.json` and choose the one whose `projectRoot` matches the current workspace or the referenced path.
5. If no cache exists but the project root is available, read `references/project-cache.md` and run `scripts/index-oasis-project.ps1` before doing broad project planning.
6. If the path clearly names a project but the project root is unavailable, say which project name was inferred and rely only on uploaded material plus existing local planning memory for that project.

## Storage Layout

Keep project planning memory outside the UGC workspace:

```text
%USERPROFILE%\.codex\oasis-project-cache\<project-name>-<path-hash>\
  planning\
    overview.md
    requirements.md
    systems.md
    economy.md
    ui-flow.md
    stage-flow.md
    open-questions.md
    decisions.md
  planning.tsv
```

Use only the files that fit the uploaded material. Do not create empty placeholder files.

Planning files should contain distilled project knowledge, not raw private documents copied wholesale. Keep source filenames, upload dates, and a short provenance note so future agents know where the summary came from.

## Trigger Phrases

Treat these as project-planning triggers:

- `策划案`, `玩法案`, `需求文档`, `项目方案`, `系统设计`, `全局规划`, `版本规划`.
- `数值表`, `经济系统`, `养成系统`, `资源循环`, `奖励`, `消耗`, `产出`.
- `UI流程`, `界面流程`, `交互流程`, `关卡流程`, `阶段流程`.
- `项目细节`, `项目记忆`, `同步项目资料`, `记住这个策划`, `记录这个方案`, `后面都按这个项目来`.
- Any file path or uploaded filename containing a known project name, such as `<project-name>`.

## Ingestion Workflow

When the user uploads planning material or asks to remember project-level details:

1. Identify the project with Project Identity Routing.
2. Read existing `planning\*.md`, `planning.tsv`, `features.tsv`, and `index\summary.md` for that project.
3. Distill the new material into the smallest relevant planning file:
   - Core project intent and pillars -> `planning\overview.md`.
   - Feature requirements and acceptance rules -> `planning\requirements.md`.
   - Cross-system architecture and ownership boundaries -> `planning\systems.md`.
   - Resource, economy, numerical, reward, and cost rules -> `planning\economy.md`.
   - UI screens, navigation, user actions, and display states -> `planning\ui-flow.md`.
   - Stage, level, phase, or match flow -> `planning\stage-flow.md`.
   - Unknowns, risks, and pending choices -> `planning\open-questions.md`.
   - Confirmed design choices and why they were chosen -> `planning\decisions.md`.
4. Append or update `planning.tsv` with searchable one-line records: project, timestamp, kind, title, file path, key terms.
5. Refresh the normal project index only if source files changed or the existing index is missing/stale.
6. Never write planning memory into the UGC project workspace.

## Answer Workflow

For any later question routed to a known project:

1. Load the project's relevant planning files before proposing code or architecture.
2. Search planning memory and feature memory before broad source scans:

```powershell
rg --line-number --smart-case "keyword|system|UI|economy|stage" "%USERPROFILE%\.codex\oasis-project-cache\<project-name>-<path-hash>"
```

3. Use planning memory to decide which real source files to inspect next.
4. Open real source files before giving exact code edits or line references.
5. Explain solutions at the project level first: intent, affected systems, data ownership, server/client boundary, UI flow, persistence/reconnect implications, future extension points, and risks.
6. Only then provide narrow implementation steps or code snippets.

## Answer Bias

When planning memory exists, prefer:

- Whole-project consistency over a quick local patch.
- Config-driven and data-driven design over hardcoded one-offs.
- Clear ownership boundaries between GameMode, GameState, PlayerController, PlayerState, PlayerPawn, UI, actions, and config files.
- Reusable event/RPC/data-flow patterns that match the existing project.
- Explicit open questions when the planning docs are incomplete or conflict with current source.

If a request asks for a small feature but planning memory shows broader constraints, mention the constraint and shape the answer around the long-term project direction.

## Privacy And Scope

- Store only distilled summaries and indexes locally.
- Do not copy full uploaded documents into global skill files.
- Do not copy private project source into this skill.
- Do not treat planning memory as more authoritative than current source code for implementation details.
- If planning memory conflicts with current source, call out the conflict and inspect source before advising changes.
