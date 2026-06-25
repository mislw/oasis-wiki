# Oasis Wiki Codex Skill

This repository packages a portable AI-agent knowledge bundle for Oasis / 绿洲启元 / 和平精英 UGC Lua development.

It is Codex-native through `oasis-wiki/SKILL.md`, and also includes generic instructions for other AI coding agents through `AGENTS.md` and `AGENT_PROMPT.md`.

The skill bundles a local Markdown export of the Oasis wiki and instructs Codex to search it before answering questions about Lua APIs, gameplay systems, UI systems, editor workflows, templates, debugging, performance, release notes, and terminology.

It also includes distilled project-architecture notes mined from local UGC sample projects. These notes summarize reusable patterns without copying whole project source trees.

The skill is designed for teaching-oriented project help: Codex can read project files to understand them, but should explain edits instead of directly modifying UGC project files unless explicitly overridden.

## Install

Copy the `oasis-wiki` folder into your Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

Restart Codex or refresh skills after copying.

## Use With Other AI Agents

For agents that do not support Codex skills directly:

1. Open `AGENTS.md` as the repository-level instruction file.
2. If the agent accepts a setup prompt, paste `AGENT_PROMPT.md`.
3. Point the agent at the `oasis-wiki/references` folder for search and citation.

The important behavior is the same across agents: search the local wiki and distilled references first, teach code changes clearly, and do not directly modify UGC project files unless explicitly allowed for that task.

Trigger expectation: if a question looks related to a 绿洲启元 / 绿洲起源 / 和平精英 UGC project, UGCProjects workspace, or UGC Lua code, the agent should use this bundle by default.

## Use

Ask Codex questions such as:

```text
Use $oasis-wiki to explain how to revive a player in Oasis.
Use $oasis-wiki to find UGCGameSystem examples.
Use $oasis-wiki to write Lua code for toggling damage.
```

## Search The Bundled Wiki

From inside the `oasis-wiki` folder:

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" .\references\wiki
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\scripts\search-oasis-wiki.mjs "角色复活" --max 10
```

## Contents

- `AGENTS.md`: Generic instructions for AI coding agents.
- `AGENT_PROMPT.md`: Copy-paste prompt for agents that do not auto-read repository instructions.
- `oasis-wiki/AGENTS.md`: Generic instructions kept inside the portable skill folder.
- `oasis-wiki/SKILL.md`: Codex skill instructions and trigger metadata.
- `oasis-wiki/agents/openai.yaml`: UI metadata.
- `oasis-wiki/references/wiki`: Markdown wiki export.
- `oasis-wiki/references/project-patterns.md`: Curated UGC project architecture and Lua patterns.
- `oasis-wiki/references/project-mining-index.md`: Representative project paths and targeted search commands.
- `oasis-wiki/references/answer-modes.md`: Rules for choosing concise normal mode or detailed teaching mode.
- `oasis-wiki/references/teaching-mode.md`: Code teaching workflow and read-only project-file constraint.
- `oasis-wiki/references/feature-development-flow.md`: End-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `oasis-wiki/references/recipes.md`: Common implementation recipes for UGC coding tasks.
- `oasis-wiki/references/snippets.md`: Small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `oasis-wiki/references/pitfalls.md`: Gotchas and verification reminders for UGC Lua work.
- `oasis-wiki/references/skill-evolution.md`: Controlled protocol for deciding when and how to update the skill.
- `oasis-wiki/scripts`: Search helpers.

The bundled wiki export was generated on 2026-06-16 and contains 59 Markdown files, about 278 articles, 263 Lua examples, and 1140 API/class references.
