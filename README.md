# Oasis Wiki Codex Skill

This repository packages a Codex skill for Oasis / 绿洲启元 / 和平精英 UGC Lua development.

The skill bundles a local Markdown export of the Oasis wiki and instructs Codex to search it before answering questions about Lua APIs, gameplay systems, UI systems, editor workflows, templates, debugging, performance, release notes, and terminology.

It also includes distilled project-architecture notes mined from local UGC sample projects. These notes summarize reusable patterns without copying whole project source trees.

The skill is designed for teaching-oriented project help: Codex can read project files to understand them, but should explain edits instead of directly modifying UGC project files unless explicitly overridden.

## Install

Copy the `oasis-wiki` folder into your Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

Restart Codex or refresh skills after copying.

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

- `oasis-wiki/SKILL.md`: Codex skill instructions and trigger metadata.
- `oasis-wiki/agents/openai.yaml`: UI metadata.
- `oasis-wiki/references/wiki`: Markdown wiki export.
- `oasis-wiki/references/project-patterns.md`: Curated UGC project architecture and Lua patterns.
- `oasis-wiki/references/project-mining-index.md`: Representative project paths and targeted search commands.
- `oasis-wiki/references/teaching-mode.md`: Code teaching workflow and read-only project-file constraint.
- `oasis-wiki/references/recipes.md`: Common implementation recipes for UGC coding tasks.
- `oasis-wiki/references/snippets.md`: Small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `oasis-wiki/references/pitfalls.md`: Gotchas and verification reminders for UGC Lua work.
- `oasis-wiki/scripts`: Search helpers.

The bundled wiki export was generated on 2026-06-16 and contains 59 Markdown files, about 278 articles, 263 Lua examples, and 1140 API/class references.
