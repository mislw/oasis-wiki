# Predecessor Code Policy

This policy is mandatory whenever `oasis-wiki` is loaded for project analysis, teaching, review, or implementation.

## Load Acknowledgement

- The first user-visible progress update must include exactly: `已加载 oasis-wiki Skill。`
- Say it once per task. Continue with the actual investigation in the same or next short update.

## Required Search Before Output

Before explaining, planning, reviewing, or implementing a feature, inspect same-type predecessor implementations instead of designing from memory alone:

1. Resolve the configured primary predecessor identity from private local agent instructions. Never copy that identity into this repository or user-facing output.
2. Search feature-reference candidates authored by the primary predecessor only by default, using focused `git log --author`, `git show`, and path/function searches. Search the secondary predecessor only when the user explicitly requests a broader predecessor search. Other authors may still appear in ownership checks for the exact target block, compatibility checks, and current-project foundation analysis, but do not use them as predecessor-reference candidates.
3. Search the current project first. If it lacks a complete same-type example, search the available `RedCliff` (赤壁), `StarMon` (灵兽), and `StealItem` (偷鸡) repositories in that order, skipping the current project when repeated.
4. Inspect the exact functions, tables, configs, RPC/event paths, UI callbacks, archive/save keys, replication, reconnect handling, and owning commits. Use `git blame` on the relevant blocks to confirm the candidate rather than matching only by filename or keyword.
5. Validate the implementation against the bundled official sources: `references/wiki/官方API参考手册.md`, `references/wiki/新增内容_1.37版本.md`, the matching category document selected through `references/wiki/README.md`, and `references/wiki/论坛经验帖_绿洲启妹.md` for the downloaded developer-forum material.
6. Confirm that the code and documentation agree with the current runtime, configuration, server/client authority, data ownership, archive, replication, UI, and reconnect flow. When they differ, state the difference and follow confirmed current-project behavior plus current official API constraints.
7. Treat a relevant same-type code implementation or a relevant knowledge-base document as a confirmed related implementation. Before presenting the plan, include the exact standalone user-facing sentence `已查到相关实现`. For code, report the project, file, function/table, and commit. For documentation, report the knowledge-base file and section/article. If neither source has a relevant result, say so instead of inventing a precedent and base the proposal on verified current-project structure and supported APIs. Never reveal any configured predecessor identity.

## Ownership And Modification Rules

Resolve the protected primary predecessor from private local agent instructions and confirm ownership with repository `git blame` / `git log` evidence. Resolve the secondary reference predecessor only when the user explicitly requests that broader search. Never store, publish, quote, or reveal any configured person's name, email, identity, priority, or local matching rule in this repository or in user-facing output. If the private identifier is unavailable, do not guess or infer a person from nearby history; ask the user to identify the protected history without suggesting a name.

- Protected predecessor code is frozen by default. If the task can be completed by adding a hook before, after, or beside that block, do not modify the protected block at all.
- Do not reformat, rename, reorder, wrap, extract, clean up, or add defensive scaffolding around protected predecessor code.
- Touch protected predecessor code only when the requested behavior cannot be implemented through a compatible external hook. Before editing, state the exact reason it is unavoidable and change only the necessary lines.
- Code owned by other authors may be changed after ownership is checked, but still use the smallest compatible diff and preserve established behavior.
- Never overwrite unrelated user or teammate changes in a dirty worktree.

## Implementation Style Baseline

For RedCliff work, follow the protected predecessor's confirmed same-type code style:

- Extend the existing feature in place whenever its current variables, functions, data owners, RPC/event paths, archive keys, replication, or UI refresh flow can express the requested behavior. Do not add a parallel field, helper, manager, or second flow merely to avoid a small compatible edit.
- Introduce a new field, helper, manager, or flow only when the existing implementation cannot satisfy the required semantics, ownership boundary, lifecycle, compatibility, or verification path. Before doing so, state the concrete reason the existing implementation is unusable and the smallest resulting impact surface.
- Reuse existing data owners, tables, RPC/event paths, archive keys, replication patterns, and UI refresh flow.
- Match naming, function placement, call order, comment density, nil-check style, and change size.
- Treat a confirmed same-type predecessor implementation as the structural template for every editable extension point. Add only the table entry, control binding, branch, case, or field required by the requested behavior, in the same relative location and style. Do not add archive migrations, missing-key backfills, nil/default guards, compatibility branches, helper functions, explanatory comments, branch reordering, formatting cleanup, line-ending changes, or EOF changes unless the confirmed reference already uses them or a verified runtime/API requirement makes the deviation necessary. Before finishing, inspect a focused `git diff`, remove every unrequired difference, and explain each remaining deviation to the user before keeping it.
- Prefer direct local hooks over new wrappers, managers, generic abstractions, or broad refactors.
- Use the 偷鸡 or 灵兽 implementation only when it matches the current feature shape; adapt names and paths without importing unrelated architecture.

## User-Facing Attribution

- For protected predecessor code, say `前辈的代码`; do not print the person's name or email in the user-facing response.
- For code owned by anyone else, state the Git username when attribution matters.
- Always separate confirmed authorship from inference and include the reference commit when reporting a precedent.
