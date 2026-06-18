# Agent Instructions For This Skill Folder

Use this folder as a portable Oasis / 绿洲启元 / 和平精英 UGC Lua knowledge bundle.

Codex should use `SKILL.md`. Other AI coding agents should follow this file.

## Rules

- Search `references/` before answering.
- Read `references/teaching-mode.md` before giving code-change guidance.
- UGC project files may be read and analyzed freely.
- Do not directly modify UGC project files unless the user explicitly overrides teaching-only mode for the current task.
- Give exact edit guidance: file path, function/table, code snippet, caveats, and test steps.
- If an API or behavior is not confirmed in the bundled wiki or examples, say so.

## High-Value References

- `references/wiki/README.md`: wiki overview.
- `references/wiki/API参考索引.md`: API/class lookup.
- `references/wiki/代码示例库.md`: Lua examples.
- `references/recipes.md`: common implementation recipes.
- `references/snippets.md`: reusable Lua snippets.
- `references/pitfalls.md`: gotchas and verification reminders.
- `references/project-patterns.md`: project architecture patterns.

## Search

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" references
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\scripts\search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```
