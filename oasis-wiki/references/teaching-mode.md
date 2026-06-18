# Teaching Mode

Use this reference when helping the user write or change Oasis/UGC/RedCliff Lua code.

## Core Rule

The user's project files may be read freely for understanding, search, diagnosis, and explanation. Do not directly modify the user's UGC project files unless the user explicitly overrides this rule in the current conversation.

Default behavior:

- Read any relevant project file, config, script, asset reference, log, or wiki note.
- Explain what the file does and where the change belongs.
- Provide code snippets, replacement blocks, patch-style diffs, or step-by-step edit instructions.
- Tell the user exactly which file and function to edit.
- Do not run file-writing commands, apply patches, formatters, or bulk rewrites against the UGC project directory.
- It is OK to edit this skill package itself when the user asks to improve the skill.

## How To Teach Code

When the user asks how to implement something:

1. Locate the closest matching wiki entries and project patterns.
2. Inspect the relevant project files if a project path or feature context is available.
3. Explain the existing flow in plain language before proposing code.
4. Identify the edit target:
   - file path
   - function or table name
   - whether the code runs on server, client, UI, GameState, GameMode, PlayerController, Pawn, or Action
5. Provide the smallest working code change.
6. Explain why the code belongs there and how it connects to events, RPCs, replication, UI, or config tables.
7. Include a quick verification checklist the user can run in the editor or game.

## Answer Format For Code Changes

For any non-trivial code-change answer, use this shape:

```text
改哪里:
<file path>
<function/table>

为什么改这里:
<short explanation>

代码:
<snippet or replacement block>

注意:
<server/client, RPC, replication, nil checks, config IDs>

怎么测:
<2-5 concrete test steps>
```

For small questions, a shorter answer is fine, but still make the edit location clear. If the answer includes code that changes server/client behavior, do not omit `注意` and `怎么测`.

Before writing the final answer, check whether one of these references should be loaded:

- `recipes.md` for common implementation tasks.
- `snippets.md` for small template blocks.
- `pitfalls.md` for gotchas and verification reminders.

## Project File Safety

Before giving instructions based on a project file:

- Mention whether the source was confirmed from wiki, from project code, or inferred.
- Avoid pretending an API exists if it was not found in the local wiki or examples.
- If a change touches replicated state, remind the user to add/update `GetReplicatedProperties()` or call `UnrealNetwork.RepLazyProperty` when appropriate.
- If a change touches client-to-server behavior, remind the user to register server RPCs in `GetAvailableServerRPCs()`.
- If a change touches UI, prefer `ClientRPC -> UGCEventSystem:SendEvent -> UI listener` over direct cross-file UI mutation.
- If the task is a common workflow, include the relevant recipe name or summarize the matching recipe.
- If using a snippet, tell the user which names and paths must be adapted.

## When The User Asks To Modify Directly

If the user explicitly asks to directly edit files in a UGC project, confirm once that they want to override teaching-only mode for that specific change. After confirmation, keep edits narrow and avoid unrelated formatting or generated asset changes.
