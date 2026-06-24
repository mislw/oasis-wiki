# Teaching Mode

Use this reference when helping the user write or change Oasis/绿洲启元/和平精英 UGC Lua code.

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

For non-trivial code-change answers, teach in a fine-grained "edit walkthrough" style. The goal is that a beginner can follow the answer line by line without guessing where to paste code or which punctuation matters.

Use numbered sections when the change touches multiple places:

```text
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

- Show the exact file and function for each edit. Prefer `UGCPlayerController.lua (line 415), GetAvailableServerRPCs()` over only saying "注册 RPC".
- When changing an existing block, show a short `现在是:` block and a `改成:` block.
- When adding a new line inside an existing table, return list, or archive data block, show enough neighboring lines so the insertion point is obvious.
- Explain why the line exists, not just what it does. Example: "存档这个字段后，玩家重登才不会重复领取".
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
