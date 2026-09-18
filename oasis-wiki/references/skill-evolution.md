# Skill Evolution Protocol

Use this reference when the user asks whether new knowledge, a conversation, a project pattern, or a repeated failure should be added to this Oasis Wiki skill.

This is a controlled improvement protocol, not silent self-modification.

Project-specific feature memory is separate from global skill evolution. When the user says `记住这个功能`, `同步一下项目知识`, `记录这次改动`, or similar after finishing a feature, write a local project feature memory with `scripts/remember-oasis-feature.ps1`. Do not update global `references/` unless the user explicitly asks to make the lesson reusable across projects.

## When To Propose A Skill Update

Suggest updating the skill when at least one is true:

- A conversation reveals a reusable workflow that applies across many UGC projects.
- The same bug, confusion, API, or project pattern appears repeatedly.
- The user corrects the agent on domain behavior that should be remembered for future answers.
- A project example contains a general pattern useful beyond that project.
- A missing trigger caused the skill not to be used for an obviously related UGC question.
- A new reference, script, or checklist would reduce repeated explanation.

Do not add:

- Raw chat transcripts.
- Whole project source trees.
- Local project cache or feature-memory files.
- One-off project names as global triggers.
- Unverified guesses.
- Secrets, private IDs, account data, or user-specific credentials.
- Large duplicated material already covered by the wiki or existing references.

## Update Style

Distill, do not dump.

Prefer:

- A short reference file.
- A concise checklist.
- A reusable code pattern with placeholders.
- A new search phrase or trigger.
- A pitfall entry with symptoms and checks.
- A recipe entry linked from `SKILL.md`.

Avoid:

- Long prose copied from conversation history.
- Project-specific names unless the reference is explicitly about that project.
- Massive examples that consume context without improving future answers.
- Extra top-level documentation files such as `README.md`, `CHANGELOG.md`, `QUICK_REFERENCE.md`, or ad-hoc notes. Keep root-level agent instructions in `SKILL.md` or `AGENTS.md`; put necessary supporting material under `references/`.

## Approval Rule

Before changing the skill, tell the user:

- What will be added.
- Why it is broadly useful.
- Which files will change.
- Whether it affects trigger behavior, answer style, or only optional references.

Only write files after user approval or when the current user request clearly asks to update the skill.

## Implementation Checklist

1. Inspect current `SKILL.md` and related references.
2. Choose the smallest durable home for the knowledge:
   - Trigger/routing: `SKILL.md`, `AGENTS.md`, `AGENT_PROMPT.md`.
   - Detailed workflow: `references/*.md`.
   - Common code: `references/snippets.md`.
   - Common task process: `references/recipes.md` or a dedicated workflow reference.
   - Gotchas: `references/pitfalls.md`.
3. Add or update only the needed files.
4. Keep `SKILL.md` lean and link to the reference instead of copying detailed material into it.
5. Sync portable agent docs if behavior changes for non-Codex agents.
6. Run a quick search/validation check.
7. Copy the updated `oasis-wiki` folder into the local Codex skills directory if this machine should use it immediately.
8. Commit and push when the user wants GitHub updated.

## Validation Checklist

After editing:

- `SKILL.md` frontmatter still has `name` and `description`.
- New reference files are linked from `SKILL.md`.
- `scripts/check-skill-hygiene.ps1` passes, and there are no extra top-level Markdown files or unrelated generated notes.
- Search terms find the new material.
- No raw private project source was copied unnecessarily.
- Teaching-only mode remains intact for UGC project files.
- Redundant or project-only trigger names were not added as global triggers.

## Official Wiki Snapshot Refresh

Use the deterministic sync script when the user asks whether the official wiki changed or explicitly requests a refresh:

```powershell
python scripts/sync_official_wiki.py --dry-run
python scripts/sync_official_wiki.py
```

The dry run validates the live catalog, downloads every published article, checks duplicate IDs and title consistency, and builds all artifacts in memory without changing files. Write mode regenerates the category Markdown, `README.md`, article ID index, API index, Lua example library, directory tree, and `新增内容_1.37版本.md`. It preserves the separately maintained official API manual, forum tutorial export, and glossary.

After write mode, inspect the diff for unexpected removals, confirm the live catalog version/update time and article count in `references/wiki/README.md`, run the sync tests, and complete the normal Skill and Companion version checks.

## Official Forum Snapshot Refresh

Use the forum sync script when the user asks whether 绿洲启妹 published new developer documentation or explicitly requests those threads to be added:

```powershell
python scripts/sync_official_forum.py --dry-run
python scripts/sync_official_forum.py
```

The script reads the public thread-detail API, requires the official author ID and approved state, converts the published rich text to Markdown, and replaces matching thread IDs before inserting the selected articles at the front of `references/wiki/论坛经验帖_绿洲启妹.md`. Keep event notices and other time-limited posts out of the default thread list unless the user explicitly requests them.

After write mode, verify the requested thread IDs occur exactly once, inspect titles and issue/update times, run `tests.test_official_forum_sync`, and complete the normal Skill and Companion version checks.

## Reference File Refresh Check

`references/wiki/` mixes generated and hand-maintained material. Before claiming the knowledge base matches the official site, classify the file first — the wiki sync only owns part of the directory:

| Class | Files | Covered by |
|---|---|---|
| Generated | every file returned by `build_artifacts()` (category docs, `API参考索引.md`, `代码示例库.md`, `README.md`, `新增内容_1.37版本.md`, `绿洲启元Wiki目录.txt`, …) | `sync_official_wiki.py` |
| Preserved | `官方API参考手册.md`, `术语表.md`, `论坛经验帖_绿洲启妹.md` | their own source, **not** the wiki sync |
| Hand-maintained | `官方宣讲会回顾.md` and any future briefing archive | this protocol |

A catalog version match in `README.md` is **not** evidence the preserved files are current. Check them separately.

### Official API Manual Freshness

`官方API参考手册.md` is a curated snapshot of the separate API site (`https://developer.gp.qq.com/api/`). The site is a single-page app, but its data is plain static JSON, so freshness can be verified without a browser:

```text
https://developer.gp.qq.com/api/class/list/tree.json             # classes
https://developer.gp.qq.com/api/cppenum/list/sorted_list.json    # enums (nested by first letter)
https://developer.gp.qq.com/api/cppstruct/list/sorted_list.json  # structs (nested by first letter)
https://developer.gp.qq.com/api/globalfunc/list/sorted_list.json # global functions
```

Compare the live names against the manual text and report the gap by category. Only UGC/和平精英-scope gaps matter; UE-internal types (`UMaterialExpression*`, `FClipmap*`, `Ak*`, `EABF_*`) are outside the manual's stated scope and do not by themselves mean the manual is stale. Also re-check the counts in the manual header, which have drifted from the body before.

Scope rule: a struct belongs in the manual only when its name starts with `FUGC` or `FPE`. Refresh that section with:

```powershell
python scripts/refresh_api_structs.py
```

The script fetches the in-scope struct details and rewrites the `## 数据结构（Structs）` section and the header statistics. It is idempotent. Do not bulk-import the ~1100 UE engine structs.

### Glossary Quality

`术语表.md` is hand-maintained. It was originally produced by a regex that allowed `**…**` spans to cross newlines, so stray bold markers swallowed headings, table rows, and `<br>` tags into the "term" position — those entries spanned several lines and broke the Markdown. The cleaned form keeps only single-line `术语 — 出现于: 文章路径` entries, with leading `#`/`|`/list markers and residual `**` and `\_` escapes stripped.

When the glossary is touched again:

- Keep every entry on one line, matching `- **term** — 出现于: path`; drop anything that cannot be reduced to that shape.
- Do not delete a term just because it starts with `#` — strip the marker and keep the token (this is how names like `InitAllPlayerScore()` were recovered).
- Confirm the 出现于 paths still exist in the generated category docs after a wiki sync.
- Be honest about precision: the 出现于 values are **category/section level** (about 123 sources, sometimes merged as `A, B 等N处`), not exact article paths. The generated docs carry a `> 文档路径:` marker per article (332 of them) and `README.md` lists the categories — point readers there when an exact article is needed. `API参考索引.md` and `代码示例库.md` are the precise indexes; the glossary is coarse.
- It remains a partial index rather than a full one.


## Suggested Answer When A New Conversation May Be Useful

Use this decision pattern:

```text
This is worth adding if it teaches a reusable UGC workflow, not just one implementation.
I would add it as <reference/checklist/recipe>, summarized into <N> steps, and link it from SKILL.md.
I would not copy the raw conversation.
For automatic evolution, I recommend a controlled maintenance protocol: propose -> distill -> ask approval -> edit -> validate -> commit/push.
```

