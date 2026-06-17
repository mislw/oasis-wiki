---
name: oasis-wiki
description: Use when answering questions or writing code about Oasis/绿洲启元/和平精英 UGC/RedCliff Lua development, including API lookup, gameplay systems, UI systems, editor workflows, examples, templates, debugging, performance, release notes, terminology, and practical project architecture patterns mined from local UGC sample projects. Search the bundled local wiki and distilled project references before giving technical guidance or code for these domains.
---

# Oasis Wiki

Use this skill for Oasis/绿洲启元 and RedCliff development questions. The bundled wiki is the source of truth for Lua APIs, editor workflows, gameplay systems, UI, templates, troubleshooting, and examples. The project-pattern references add distilled practices mined from local UGC projects.

## Workflow

1. Search first; do not load the full wiki into context.
2. Prefer the focused index files when starting:
   - `references/wiki/README.md` for the knowledge base overview.
   - `references/wiki/API参考索引.md` for API and class names.
   - `references/wiki/代码示例库.md` for Lua examples.
   - `references/wiki/术语表.md` for terminology.
   - `references/wiki/RedCliff开发速查.md` for RedCliff-specific guidance.
3. For practical architecture or "how should I structure this project?" questions, read `references/project-patterns.md`.
4. If the project-pattern summary is not enough and the local project corpus is available, use `references/project-mining-index.md` for targeted search commands and representative source paths.
5. For implementation answers, cite the relevant local file paths and line numbers when possible.
6. When writing Lua, match the wiki examples and API naming exactly. If a detail is not found, say that the local wiki did not confirm it.
7. For broad questions, synthesize from 2-4 relevant files rather than one giant context load.

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
