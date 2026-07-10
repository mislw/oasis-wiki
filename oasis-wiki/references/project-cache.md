# Oasis Project Cache

Use this reference when the user works in a specific Oasis / UGC project and future questions should reuse known project structure or remembered feature intent instead of re-parsing the whole project every turn.

## Core Rule

Keep project-specific parsed knowledge on the local computer, not in the project workspace and not in the global skill:

```text
%USERPROFILE%\.codex\oasis-project-cache\<project-name>-<path-hash>\
```

This avoids copying private project source into the skill and avoids adding cache files to team repositories while still giving future agents a fast, searchable project map.

## When To Build Or Refresh

Build or refresh the project index when:

- The user asks to remember, cache, parse, index, scan, or learn the current project.
- A project question requires broad structure discovery across many files.
- The local `index\manifest.json` is missing.
- The manifest says files changed, or the user says the project changed significantly.

Refresh the cache with:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-root>\scripts\index-oasis-project.ps1" -ProjectRoot "<project-root>" -Force
```

Record a completed feature when the user says `记住这个功能`, `同步一下项目知识`, `记录这次改动`, `沉淀这个功能`, or similar:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-root>\scripts\remember-oasis-feature.ps1" -ProjectRoot "<project-root>" -Title "<feature title>" -Summary "<short human intent>" -Author "luojiawei"
```

## What The Cache Contains

- `index\manifest.json`: project root, cache key, generated time, file counts, indexed extensions, skipped folders, and per-file hash/mtime data.
- `index\summary.md`: compact human-readable architecture overview, key files, Lua classes, RPCs, events, timers, replication, UI hints, and frequent APIs.
- `index\symbols.tsv`: searchable line-oriented facts extracted from Lua files.
- `index\files.tsv`: searchable file inventory with size, mtime, hash, and relative path.
- `features\*.md`: feature memories created on explicit trigger.
- `features.tsv`: searchable feature-memory index.
- `feature-memory.json`: latest feature-memory metadata, preferred author, git user, and cache location.

The cache is an index, not a source replacement. Use it to decide where to inspect next, then open the real project files for exact code and line-level guidance.

## Answer Workflow

1. Determine the local cache root from the current project path. The scripts do this automatically using `<project-name>-<path-hash>`.
2. If the user asks about a known project, check `index\summary.md` and `features.tsv` first.
3. Search `index\symbols.tsv`, `index\files.tsv`, `index\summary.md`, and feature memories with `rg` before scanning the project tree:

```powershell
rg --line-number --smart-case "ServerRPC|UIManager|EventDefine|RepLazyProperty|keyword" "%USERPROFILE%\.codex\oasis-project-cache"
```

4. Open only the real source files identified by the cache.
5. If the cache is missing or stale, run `scripts/index-oasis-project.ps1`.
6. If the user explicitly says to remember a completed feature, run `scripts/remember-oasis-feature.ps1`.
7. Do not copy generated project cache files into the project workspace, `references/`, or global skill files.

## Staleness Checks

Treat the cache as stale when:

- The manifest is older than the latest changed Lua/config/UI file relevant to the question.
- The target file is absent from `index\files.tsv`.
- Search results contradict current source files.
- The user mentions recent edits after the cache was generated.

When stale, refresh before relying on project-wide conclusions.

## Privacy And Scope

- Keep caches under `%USERPROFILE%\.codex\oasis-project-cache`.
- Never create `.codex` or cache files inside the UGC project workspace.
- Do not add one project's cache to the skill repository.
- Do not treat cached snippets as authoritative over source files.
- Keep UGC project file safety intact: read and analyze freely, but do not directly modify project files unless the user explicitly allows it.
