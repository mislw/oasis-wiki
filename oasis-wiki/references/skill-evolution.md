# Skill Evolution Protocol

Use this reference when the user asks whether new knowledge, a conversation, a project pattern, or a repeated failure should be added to this Oasis Wiki skill.

This is a controlled improvement protocol, not silent self-modification.

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
- Search terms find the new material.
- No raw private project source was copied unnecessarily.
- Teaching-only mode remains intact for UGC project files.
- Redundant or project-only trigger names were not added as global triggers.

## Suggested Answer When A New Conversation May Be Useful

Use this decision pattern:

```text
This is worth adding if it teaches a reusable UGC workflow, not just one implementation.
I would add it as <reference/checklist/recipe>, summarized into <N> steps, and link it from SKILL.md.
I would not copy the raw conversation.
For automatic evolution, I recommend a controlled maintenance protocol: propose -> distill -> ask approval -> edit -> validate -> commit/push.
```

