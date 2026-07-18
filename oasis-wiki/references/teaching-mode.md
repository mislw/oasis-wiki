# Teaching Mode

Use this reference when helping the user write or change Oasis/绿洲启元/和平精英 UGC Lua code.

This file defines the detailed teaching style. For mode selection between concise normal answers and detailed teaching answers, read `answer-modes.md` first.

## Core Rule

The user's project files may be read freely for understanding, search, diagnosis, and explanation. In teaching mode, never directly modify the user's UGC project files. This is a hard rule for teaching mode and cannot be overridden inside the same teaching-mode answer.

If the user asks for direct edits while teaching mode is active, stop and explain that teaching mode is read-only. Ask the user to switch back to normal/direct mode for implementation, or provide the exact edit instructions instead.

Default behavior:

- Read any relevant project file, config, script, asset reference, log, or wiki note.
- Explain what the file does and where the change belongs.
- Provide code snippets, replacement blocks, patch-style diffs, or step-by-step edit instructions.
- Tell the user exactly which file, line number, and function/table to edit. If a precise line number cannot be known, inspect the file first; if it still cannot be determined, say why and give the nearest stable function/table anchor.
- Do not run file-writing commands, apply patches, formatters, or bulk rewrites against the UGC project directory.
- It is OK to edit this skill package itself when the user asks to improve the skill.

## How To Teach Code

When the user asks how to implement something:

1. Locate the closest matching wiki entries and project patterns.
2. Inspect the relevant project files if a project path or feature context is available.
3. For feature work, use `feature-development-flow.md` to classify the feature, summarize `已有基础`, identify missing pieces, and plan the config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect path.
4. Explain the existing flow in plain language before proposing code.
5. Identify the edit target:
   - file path
   - line number or nearest stable line anchor
   - function or table name
   - whether the code runs on server, client, UI, GameState, GameMode, PlayerController, Pawn, or Action
6. Provide the smallest working code change.
7. Explain why the code belongs there and how it connects to events, RPCs, replication, UI, or config tables.
8. Include a quick verification checklist the user can run in the editor or game.

Before writing config tables, member variables, methods, or `GlobalConfig` entries, read `code-style.md` and apply its lightweight project style: Chinese comments for every config column, member variable, config variable, and method; complete English words except common abbreviations such as `ID` and `UI`; and simple type prefixes such as `nLevel`, `szName`, and `tbItemList`.

When providing code, every Lua or UGC code block must contain detailed Chinese comments. Comment the purpose of the block, the reason for each non-obvious branch or guard, server/client responsibility, RPC or replication boundary, UI event binding, timer lifetime, config/archive IDs, and Lua syntax traps such as commas in return lists. Keep comments close to the code they explain.

When designing the change, reduce impact on existing project code as much as possible. Prefer additive insertions, local helper functions, guarded branches, new config fields, and narrow hook points. Treat existing code from prior teammates as protected by default: avoid changing it when an additive hook can solve the problem. If changing existing code is necessary, first reason through the affected feature path and confirm the change does not break the prior behavior, call out the exact impact surface, and explain what the changed code does in plain teaching-mode language. Preserve existing behavior, naming, formatting, function order, RPC names, event IDs, save keys, and call order unless a change is necessary; when it is necessary, call out the reason and risk explicitly.

## Answer Format For Code Changes

For non-trivial code-change answers, teach in a fine-grained "edit walkthrough" style. The goal is that a beginner can follow the answer line by line without guessing where to paste code or which punctuation matters.

Use numbered sections when the change touches multiple places:

```text
0. 已有基础

项目里已经有:
<existing declarations / configs / RPCs / events / UI / helpers / save or replication fields>

还缺:
<missing pieces needed by this feature>

整体做法:
<config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect plan>

1. 配置 / 存档 / 服务端逻辑 / RPC 注册 / UI 按钮 / UI 刷新 / 复制 / 重连

位置:
<file path> (line <line number if known>), <function/table> 里

现在是:
<existing nearby code, only when useful>

改成:
<replacement block or inserted block>

为什么这样改:
<explain the data flow and server/client responsibility>

注意:
<punctuation, comma, nil check, server/client, RPC registration, replication, event ID, config ID, indentation>
```

At the end, always include:

```text
怎么测:
1. <success path>
2. <failure path>
3. <multiplayer/server-client path if relevant>
4. <reconnect/respawn path if relevant>
```

## Detail Level Requirements

Match the screenshot-like teaching style:

- Start feature walkthroughs with the `已有基础` section defined by `feature-development-flow.md`. The goal is to teach from the project's current foundation, not from a blank project.
- When the foundation depends on `.uasset` DataTables, blueprint assets, map actors, skill editor assets, or other binary/editor-only assets, use UGCAskQ MCP to inspect them. Do not treat a text-search miss as proof that a field, row, or asset setting does not exist.
- Show the exact file, line number, and function/table for each edit. Prefer `UGCPlayerController.lua (line 415), GetAvailableServerRPCs()` over only saying "注册 RPC".
- When changing an existing block, show a short `现在是:` block and a `改成:` block.
- When adding a new line inside an existing table, return list, or archive data block, show enough neighboring lines so the insertion point is obvious.
- Explain why the line exists, not just what it does. Example: "存档这个字段后，玩家重登才不会重复领取".
- In every code block, add detailed Chinese comments for intent, data flow, edge cases, server/client ownership, RPC/replication behavior, UI binding, timers, config IDs, and nil checks.
- Prefer the smallest additive edit that achieves the feature. Avoid rewriting existing functions or moving old code unless the user asks for a refactor or the existing structure cannot safely support the feature.
- Add a `注意:` paragraph for fragile Lua syntax:
  - In a multi-string `return`, every previous string line needs a trailing comma.
  - The final string line may omit the comma, but adding a comma before the new final line is usually required.
  - For table fields, distinguish `Field = Value,` from statement assignment `Field = Value`.
  - For comments, keep them above the line they explain; do not insert comments inside a return list in a way that breaks syntax.
- Call out whether the code runs on server, client, UI, GameState, GameMode, PlayerController, Pawn, or Action.
- If the change is optional, label it as `可选但建议`.
- If the code is inferred instead of confirmed from project files, say so clearly.
- Keep snippets focused. Do not paste giant files; show only the local block the user needs.

## Example Shape

Use this kind of answer shape for multi-step UGC changes:

### 4. RPC 注册

位置:
UGCPlayerController.lua (line 415), GetAvailableServerRPCs() 末尾

现在是:

```lua
"Server_RequestTaskInfo",
"Server_UseReturnStealPill",
"Server_RequestGetGeneralSoulFlyAward"
```

改成:

```lua
"Server_RequestTaskInfo",
"Server_UseReturnStealPill",
"Server_RequestGetGeneralSoulFlyAward",
-- 客户端请求领取全服福利奖励
"Server_RequestGetServerWelfareAward"
```

为什么这样改:
客户端按钮通过 UnrealNetwork.CallUnrealRPC 调服务端函数时，函数名必须在 GetAvailableServerRPCs() 里注册，否则按钮点击后服务端函数不会执行。

注意:
Lua 这种 return 多字符串写法，前一行要加逗号。也就是 `"Server_RequestGetGeneralSoulFlyAward"` 后面要补 `,`，否则新 RPC 字符串接不上。

For small questions, a shorter answer is fine, but still make the edit location clear. If the answer includes code that changes server/client behavior, do not omit `注意` and `怎么测`.

Before writing the final answer, check whether one of these references should be loaded:

- `feature-development-flow.md` for any cross-system feature plan.
- `recipes.md` for common implementation tasks.
- `snippets.md` for small template blocks.
- `pitfalls.md` for gotchas and verification reminders.

## Project File Safety

Before giving instructions based on a project file:

- Mention whether the source was confirmed from wiki, from project code, or inferred.
- For binary/editor-only assets, mention whether the source was confirmed through UGCAskQ MCP. If MCP was unavailable, say the asset content is unverified.
- Avoid pretending an API exists if it was not found in the local wiki or examples.
- If a change touches replicated state, remind the user to add/update `GetReplicatedProperties()` or call `UnrealNetwork.RepLazyProperty` when appropriate.
- If a change touches client-to-server behavior, remind the user to register server RPCs in `GetAvailableServerRPCs()`.
- If a change touches UI, prefer `ClientRPC -> UGCEventSystem:SendEvent -> UI listener` over direct cross-file UI mutation.
- If the task is a common workflow, include the relevant recipe name or summarize the matching recipe.
- If using a snippet, tell the user which names and paths must be adapted.

## When The User Asks To Modify Directly

If the user explicitly asks to directly edit files in a UGC project while teaching mode is active, do not edit. Teaching mode remains read-only. Tell the user that direct implementation requires leaving teaching mode / switching to normal direct mode, then either wait for that confirmation or provide precise file-line edit instructions.
