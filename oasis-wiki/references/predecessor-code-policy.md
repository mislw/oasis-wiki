# Predecessor Code Policy

This policy is mandatory whenever `oasis-wiki` is loaded for project analysis, teaching, review, or implementation.

## Load Acknowledgement

- The first user-visible progress update must include exactly: `已加载 oasis-wiki Skill。`
- Say it once per task. Continue with the actual investigation in the same or next short update.

## Required Search Before Output

Before the final response, inspect same-type predecessor implementations instead of designing from memory alone:

1. Run `git blame` on the exact functions, tables, and nearby blocks involved.
2. Run `git log` or `git show` for the owning commits and recent same-feature history.
3. Prefer a same-type implementation authored by the protected predecessor in the current project.
4. If the current project lacks a complete example, inspect the related `StealItem` (偷鸡) and `StarMon`/灵兽 project code available in the same UGCProjects checkout.
5. Confirm that the chosen reference matches the current runtime, configuration, server/client ownership, archive, replication, and UI flow before adapting it.
6. Report the reference file and commit used. If no matching reference exists, say so instead of inventing a precedent.

## Ownership And Modification Rules

Identify the protected predecessor internally by Git author name `HeQirui` and confirm ownership with repository `git blame` / `git log` evidence.

- Protected predecessor code is frozen by default. If the task can be completed by adding a hook before, after, or beside that block, do not modify the protected block at all.
- Do not reformat, rename, reorder, wrap, extract, clean up, or add defensive scaffolding around protected predecessor code.
- Touch protected predecessor code only when the requested behavior cannot be implemented through a compatible external hook. Before editing, state the exact reason it is unavoidable and change only the necessary lines.
- Code owned by other authors may be changed after ownership is checked, but still use the smallest compatible diff and preserve established behavior.
- Never overwrite unrelated user or teammate changes in a dirty worktree.

## Implementation Style Baseline

For RedCliff work, follow the protected predecessor's confirmed same-type code style:

- Reuse existing data owners, tables, RPC/event paths, archive keys, replication patterns, and UI refresh flow.
- Match naming, function placement, call order, comment density, nil-check style, and change size.
- Prefer direct local hooks over new wrappers, managers, generic abstractions, or broad refactors.
- Use the 偷鸡 or 灵兽 implementation only when it matches the current feature shape; adapt names and paths without importing unrelated architecture.

## User-Facing Attribution

- For protected predecessor code, say `前辈的代码`; do not print the person's name or email in the user-facing response.
- For code owned by anyone else, state the Git username when attribution matters.
- Always separate confirmed authorship from inference and include the reference commit when reporting a precedent.
