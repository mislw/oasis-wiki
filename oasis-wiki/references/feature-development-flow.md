# Feature Development Flow

Use this reference when the user asks how to add a new Oasis / UGC gameplay feature, button, reward, item action, skill, task flow, shop action, respawn behavior, or any change that crosses UI, server logic, RPC, replication, and reconnect handling.

## Core Pipeline

Default pipeline:

0. Summarize the existing project foundation.
1. Add configuration.
2. Add authoritative server logic.
3. Register Server RPC when the client needs to request the action.
4. Bind the client UI button or input to call the Server RPC.
5. Refresh UI through ClientRPC, `UGCEventSystem`, existing data update calls, or `OnRep_*`.
6. Add replication for persistent state that the client must keep seeing.
7. Handle reconnect / recovery by resending or reconstructing state.

The key idea: start from where the authoritative data lives, not from the button.

## Step 0: Classify The Feature

Before writing code, decide:

- Is this only local display, or does it change gameplay state?
- Does it affect coins, backpack, tasks, loadouts, teams, skills, house/base state, score, rank, respawn, or match phase?
- Does the result need to survive reconnect?
- Is it one-shot feedback, persistent state, or both?

If the feature changes gameplay results, the server must decide the result. The client can request, animate, and display, but should not directly change authoritative resources.

## Step 0.1: Knowledge-First Checkpoints

The Knowledge-first feature change gate applies before implementation and again when repeated changes are not working.

- Before modifying or adding a gameplay or UI feature, configuration-backed behavior, editor workflow, or other UGC capability, search the bundled knowledge base in `references/wiki/*.md` before the first edit.
- Search by the feature and system names, relevant class/API names, UI or DataTable identifiers, and Chinese/English synonyms. Start from `references/wiki/README.md`, then inspect the matching category file, `官方API参考手册.md`, `新增内容_1.37版本.md`, and `论坛经验帖_绿洲启妹.md` when relevant.
- Use the result to identify an official implementation, supported API, required editor setup, known limitation, or established troubleshooting path. Reconcile it with the current project's ownership and data flow instead of copying it blindly.
- When a relevant knowledge-base document is confirmed, say the exact standalone sentence `已查到相关实现`, then identify the knowledge-base file and section/article before presenting the plan.
- Before a third implementation attempt, if two consecutive edit-and-verify attempts have not succeeded, stop editing. Search again using the observed symptom and exact error text, affected class/API names, and the failed behavior. Compare the new evidence with the current logs, project code, and same-type predecessor implementation before selecting the next change.
- If the knowledge base has no relevant result, state that explicitly and continue from current-project evidence; do not claim that a matching official implementation exists.

## Step 0.25: Find And Verify A Same-Type Implementation

Before designing the feature, follow `predecessor-code-policy.md`:

- Resolve the configured primary predecessor from private local instructions, then search the primary predecessor only by default. Search the secondary predecessor only when the user explicitly requests a broader predecessor search.
- Search the current project first, then the available `RedCliff`, `StarMon`, and `StealItem` repositories.
- Inspect the complete config -> authority -> RPC/event -> UI -> replication/save -> reconnect path instead of copying an isolated function.
- Cross-check the candidate with `references/wiki/官方API参考手册.md`, `references/wiki/新增内容_1.37版本.md`, the matching official category document, and `references/wiki/论坛经验帖_绿洲启妹.md`.
- If a relevant code or knowledge-base document is confirmed, say the exact standalone sentence `已查到相关实现`. Identify code by project, file, function/table, and commit; identify documentation by knowledge-base file and section/article. Never reveal a configured predecessor identity.
- If no relevant implementation is found, state that clearly and continue from verified current-project structure and official documentation.

## Step 0.5: Summarize Existing Foundation

Before planning edits, inspect and summarize what the project already has. Do not make the user rebuild context that is already present in code.

Look for:

- Existing declarations: config tables, attribute IDs, enum/status values, event IDs, archive/save keys, replicated fields, RPC names, UI widget names, and manager member variables.
- Existing entry points: UI buttons, `GetAvailableServerRPCs()`, ClientRPCs, `UGCEventSystem` listeners, `OnRep_*`, request-data/reconnect methods, Action flow hooks, and manager init functions.
- Existing data owners: whether the state currently lives in `GlobalConfig`, `UGCGameMode`, `UGCGameState`, `UGCPlayerController`, `UGCPlayerState`, `UGCPlayerPawn`, UI scripts, feature managers, or Actions.
- Existing helper APIs: resource add/remove helpers, backpack helpers, task helpers, attribute helpers, UI refresh helpers, save/load helpers, and project-specific manager methods.
- Existing partial implementations from teammates. Treat them as protected by default. Do not rewrite their structure, reorder their flow, wrap their blocks, rename their fields, or refactor them for cleanliness. Preserve their names, call order, formatting, and behavior; add the smallest compatible hook beside or after the existing flow.
- Prefer extending the nearest existing variable, function, UI button, RPC, data owner, helper, archive key, replication path, or refresh flow over adding a parallel implementation. Only introduce a new field, helper, manager, branch, or flow when the existing implementation cannot satisfy the required semantics, ownership boundary, lifecycle, compatibility, or verification path; state that concrete reason before proposing or making the addition.

Then answer with:

1. `已有基础`: short list of the relevant declarations, helpers, files, and flows already in the project.
2. `缺口`: what is missing for the requested feature.
3. `整体做法`: planned config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect path.
4. `最小改动点`: exact files/functions to touch.

If local project planning memory exists, read it before this step so the foundation summary considers both design intent and current source code.

## Step 1: Add Configuration

Common locations:

- `Script/GameConfigs/GlobalConfig.lua`: feature switches, prices, rewards, cooldowns, IDs, limits, labels, status enums.
- `Script/GameConfigs/EventDefine.lua`: local Lua UI/event IDs.
- Feature manager config tables: task, item, shop, rebirth, skill, loadout, or base/house configs.

If configuration lives in `.uasset` DataTables or other editor-only binary assets, use UGCAskQ MCP to inspect the table schema, row count, key fields, sample rows, and warnings before planning fields or code. Do not assume a field is absent only because text search cannot read the asset.

Prefer config for values that designers or future edits may tune: costs, rewards, cooldowns, text, item IDs, maximum counts, phase requirements, distance limits.

## Step 2: Add Server Logic

Most player-initiated UI actions belong in `UGCPlayerController.lua` or a feature manager called by it.

Server logic should usually:

- Check match phase or feature state.
- Check `PlayerController`, `PlayerState`, `PlayerPawn`, and `GameState` availability.
- Validate ownership, resources, range, cooldowns, item existence, and current status.
- Modify authoritative data.
- Trigger replication, save/update derived data, and notify the client.

Prefer reusing existing helper methods such as resource add/remove functions, task update functions, backpack helpers, rank refresh functions, and existing UI data refresh RPCs. Do not duplicate a project-specific resource algorithm unless there is no reusable path.

## Step 3: Register Server RPC

If the client calls the server function, add the exact function name to `GetAvailableServerRPCs()`.

Checklist:

- The string exactly matches the Lua function name.
- Only client-callable server functions are registered.
- The registration lives in the class that receives the RPC, commonly `UGCPlayerController`.
- The client call uses the correct target object, usually the local `PlayerController`.

Failure symptom: the UI button appears to do nothing because the server function never runs.

## Step 4: Bind Client UI

UI code usually belongs under `Script/UI`.

The UI side should:

- Resolve `UGCGameSystem.GetLocalPlayerController()`.
- Nil-check required widgets and controller objects.
- Call `UnrealNetwork.CallUnrealRPC(PlayerController, PlayerController, "Server_FunctionName", ...)`.
- Avoid directly changing authoritative coins, inventory, tasks, team data, or match state.

Local optimistic effects are acceptable only when they are cosmetic and corrected by server response.

## Step 5: Refresh UI

Choose the lightest reliable path:

- One-shot tips, result popups, animation triggers: `ClientRPC` plus `UGCEventSystem`.
- Persistent player data: replicated property plus `OnRep_*`, or reuse an existing data refresh RPC.
- Shared match or phase state: `UGCGameState` replication or a GameState-driven UI event.
- Existing UI dashboards: prefer the project's existing `Client_UpdateData` / `Server_RequestData` style if present.

Keep UI updates idempotent. Repeated refreshes should not double-add rewards, duplicate listeners, or stack permanent UI state.

## Step 6: Add Replication

Add replication when the client must keep seeing the state after the initial RPC.

Common owners:

- `UGCGameState`: shared match state, phase data, global timers, team-wide state.
- `UGCPlayerController` / `UGCPlayerState`: player-owned resources, task state, UI-visible stats.
- `UGCPlayerPawn`: body, movement, combat, or current pawn state.

For table-like state, check whether the project uses lazy replication helpers such as `UnrealNetwork.RepLazyProperty` and `ForceNetUpdate()`. Mutating an inner table value may not notify clients unless the existing replication pattern is followed.

## Step 7: Handle Reconnect

ClientRPCs that happened while the player was disconnected will not replay automatically. Important state must be recoverable.

Check:

- Does `Server_RequestData` need to include the new state?
- Do reconnect / recovered / respawn delegates resend the state?
- Does MainUI reconstruct itself from replicated fields or current server data?
- Can the same UI event run twice without breaking state?

For features that only show a transient tip, reconnect handling may be unnecessary. For coins, inventory, tasks, house/base state, cooldowns, loadouts, or phase state, reconnect handling is usually required.

## Teaching Answer Shape

For a user asking "how do I add this feature?", use this section as the planning order. Use `answer-modes.md` to decide normal mode or teaching mode. When teaching mode applies, use `teaching-mode.md` for the presentation format instead of duplicating a second format here.

1. Existing project foundation: declarations, helpers, files, current flow, teammate partial code.
2. What data/config to add.
3. Which server function owns the rule.
4. Which RPC to register.
5. Which UI button/input calls it.
6. How the server tells UI the result.
7. What must replicate.
8. What to add to reconnect/request-data flow.
9. How to test success and failure paths.

For each non-trivial edit, make sure the final answer can identify:

- `位置`: exact file, line number when known, and function/table name.
- `现在是`: nearby existing code when the edit modifies an existing block.
- `改成`: focused replacement or insertion block.
- `为什么这样改`: how this line connects to config, server authority, RPC, UI refresh, replication, or reconnect.
- `注意`: Lua syntax, commas, nil checks, RPC registration strings, event IDs, replicated fields, and server/client responsibility.
- `怎么测`: success path, failure path, multiplayer/server-client path, and reconnect/respawn path when relevant.

Include exact file paths and function names when available. If the project files are accessible, inspect them first and adapt the pipeline to the project's current architecture.

## Example: Collect All Base Income

This is a generic example. Adapt names to the actual project.

Flow:

1. Add config: cooldown, success/no-income tips, maybe a feature switch.
2. Add `Server_RequestCollectAllCoins()` in `UGCPlayerController`.
3. Register `"Server_RequestCollectAllCoins"` in `GetAvailableServerRPCs()`.
4. Bind `Button_CollectAllCoins_OnClicked()` in `MainUI`.
5. On the server, validate phase and ownership, sum available income, clear collected slots, add coins through existing resource helper, then notify the client.
6. Refresh UI through existing coin replication / `Client_UpdateData` / `UGCEventSystem`.
7. Ensure `Server_RequestData` or reconnect recovery sends current coins and any visible income-slot state.

Testing:

- Button works when income exists.
- Button shows a tip when income is zero.
- The client cannot grant itself coins by editing UI state.
- Two players do not affect each other's income.
- Reconnect shows the correct current coin count and income state.
