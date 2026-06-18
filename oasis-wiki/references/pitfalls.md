# UGC Pitfalls

Use this checklist before finalizing advice or code snippets.

## Server And Client Confusion

Symptoms:

- UI button prints but gameplay does not change.
- Code works in standalone but not multiplayer.
- Client sees a local value, server ignores it.

Check:

- Gameplay state, inventory, damage, team, score, spawning, and skill activation should be server-authoritative.
- UI should call a server RPC on PlayerController.
- Client RPCs should only update local UI/feedback.

## Server RPC Not Registered

Symptoms:

- `UnrealNetwork.CallUnrealRPC` appears to do nothing.
- Client-to-server call never reaches the function.

Check:

- Add the server function name to `UGCPlayerController:GetAvailableServerRPCs()`.
- Match the string exactly.
- Keep server RPC functions on the correct PlayerController class.

## Replicated Field Missing

Symptoms:

- Server value changes but client UI never updates.
- Reconnect loses expected display state.

Check:

- Add the field to `GetReplicatedProperties()`.
- For tables, use `UnrealNetwork.RepLazyProperty` if the project uses lazy replication.
- Call `ForceNetUpdate()` for template-style table updates when similar code does so.
- Avoid mutating nested tables without replication notification.

## Blueprint Path `_C` Mistakes

Symptoms:

- `UE.LoadClass` returns nil.
- Widget or actor class cannot be created.

Check:

- `UE.LoadClass` for Blueprint classes usually needs `Foo.Foo_C`.
- `UE.LoadObject` for non-class assets usually uses `Foo.Foo`.
- Root-relative UGC paths often need `UGCMapInfoLib.GetRootLongPackagePath()` or `UGCGameSystem.GetUGCResourcesFullPath(...)`.

## Missing Nil Checks

Symptoms:

- Runtime errors after login, reconnect, respawn, or phase transition.

Check:

- Nil-check PlayerController, PlayerPawn, PlayerState, GameState, widget class, widget object, and actor arrays.
- Player pawn can be nil during login/reconnect/respawn.
- UI can be nil after reconnect or if creation failed.

## Tick Does Too Much

Symptoms:

- Lag, repeated logs, inconsistent countdowns.

Check:

- Avoid scanning all actors or all players every frame unless necessary.
- Update countdown UI once per second.
- Cache actor lists when safe.
- Disable `bEnableActionTick` when an Action finishes.

## UI Direct Coupling

Symptoms:

- PlayerController reaches into UI fields and breaks when UI is recreated.
- Reconnect or settlement screen creates duplicate/invalid widgets.

Check:

- Prefer `ClientRPC -> UGCEventSystem:SendEvent -> UI listener`.
- UI widgets should register/unregister listeners.
- UIManager should own widget creation and viewport ordering.

## Listener Leaks

Symptoms:

- UI callback fires multiple times.
- Old widget still receives events.

Check:

- Pair `UGCEventSystem:AddListener` with `RemoveListener`.
- Remove listeners in `Destruct`, close, or end-play paths.
- Avoid creating the same singleton UI repeatedly without checking existing instance.

## Reconnect State Missing

Symptoms:

- Player reconnects without weapons, wrong UI, wrong team, or stale skill cooldown.

Check:

- Register respawn/reconnect/recovered delegates on server.
- Re-send phase, team, loadout, skill choice, score, and UI visibility.
- Make repeated ClientRPC events safe.

## Config Hidden In Logic

Symptoms:

- Hard to balance or change mode rules.
- Same item IDs/timings repeated in several files.

Check:

- Move item IDs, durations, skill cooldowns, text, and icon paths into `GlobalConfig.lua` or focused config files.
- Keep Actions focused on flow, not giant data tables.

## Wrong Player Lookup

Symptoms:

- Change affects the wrong player or nil target.

Check:

- Use `PlayerKey` for stable player-specific lookup.
- Prefer `UGCGameSystem.GetPlayerControllerByPlayerKey`, `GetPlayerPawnByPlayerKey`, and `GetPlayerStateByPlayerKey`.
- Be careful with local player controller helpers in server-side code.

## Unreliable RPC Used For Critical State

Symptoms:

- Occasional missing state, button stuck, wrong settlement result.

Check:

- Use unreliable RPC only for high-frequency visual/progress refresh where the next update can correct it.
- Use reliable RPC or replicated state for critical choices, phase changes, inventory grants, team assignments, and settlement.

## Damage Or Team Logic Runs Too Broadly

Symptoms:

- Friendly fire behaves wrong.
- Damage blocked for everyone.

Check:

- In `LuaModifyDamage`, nil-check instigator/victim PlayerState.
- Compare TeamID carefully.
- Return original `Damage` unless intentionally blocking or scaling it.

## Action Flow Dead End

Symptoms:

- Game gets stuck in prepare or round end.

Check:

- Every Action that starts a timer must eventually call `LuaQuickFireEvent` or intentionally end the flow.
- `Update` only runs when `bEnableActionTick` is true.
- Reset timer counters when re-entering the same Action.

## Teaching Answer Checklist

Before answering with code, make sure the answer says:

- Which file and function/table to edit.
- Whether the code is server, client, UI, GameState, GameMode, PlayerController, Pawn, or Action.
- Whether an RPC must be registered.
- Whether replication must be updated.
- How to test in editor/game.
