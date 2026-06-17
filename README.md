# Oasis Wiki Codex Skill

This repository packages a Codex skill for Oasis / 绿洲启元 / RedCliff Lua development.

The skill bundles a local Markdown export of the Oasis wiki and instructs Codex to search it before answering questions about Lua APIs, gameplay systems, UI systems, editor workflows, templates, debugging, performance, release notes, and terminology.

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
- `oasis-wiki/scripts`: Search helpers.

The bundled wiki export was generated on 2026-06-16 and contains 59 Markdown files, about 278 articles, 263 Lua examples, and 1140 API/class references.
