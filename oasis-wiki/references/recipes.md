# UGC Recipes

Use these recipes when the user asks how to implement a common UGC gameplay or UI task. These are teaching recipes, not files to copy blindly.

## Add A Client Button That Calls Server Logic

Use when the user wants a UI button to trigger gameplay, buy an item, select a skill, start an action, teleport, or change a config.

Steps:

1. Find the widget script, usually under `Script/UI/`.
2. Bind the button click in the widget's construct/init function.
3. In the button callback, get the local player controller.
4. Call a `ServerRPC_*` function on the player controller.
5. Add that `ServerRPC_*` name to `UGCPlayerController:GetAvailableServerRPCs()`.
6. Implement the server function in `UGCPlayerController.lua`.
7. If UI needs feedback, call a `ClientRPC_*` function back and dispatch a local `UGCEventSystem` event.

Key checks:

- UI code runs on client.
- Real gameplay changes run on server.
- Server RPC names must be registered.
- Validate player pawn/state exists before changing gameplay.

## Add A New Client UI Event

Use when server or controller state should update an existing UI widget.

Steps:

1. Add a new ID in `GameConfigs/EventDefine.lua`.
2. In the widget, call `UGCEventSystem:AddListener(EventDefine.X, self.OnX, self)`.
3. Implement `OnX(...)` in the widget.
4. In `UGCPlayerController:ClientRPC_X(...)`, call `UGCEventSystem:SendEvent(EventDefine.X, ...)`.
5. Trigger `ClientRPC_X` from the server when the authoritative state changes.

Prefer this route over directly reaching from PlayerController into a widget instance.

## Add Replicated GameState Data

Use when clients need to display score, phase, countdown, win team, player info, skill state, or other shared match state.

Steps:

1. Add the field to the `UGCGameState` table defaults.
2. Add the field name to `UGCGameState:GetReplicatedProperties()`.
3. Only mutate the authoritative source on server.
4. For table-heavy data, call `UnrealNetwork.RepLazyProperty(UGCGameSystem.GameState, "FieldName")` after mutation when the local project pattern uses lazy replication.
5. Call `ForceNetUpdate()` if the template/project already does so for similar data.
6. On client, react through `OnRep_*` if present, or use a `ClientRPC -> UGCEventSystem` bridge if immediate UI behavior is needed.

Do not replicate large temporary tables unless the UI truly needs them.

## Add A Countdown

Use when implementing prepare time, round time, cooldown display, interaction progress, or delayed transition.

Authoritative countdown:

1. Store `StartTime` with `GameplayStatics.GetRealTimeSeconds(self)` or server time.
2. Store duration in config or Action property.
3. Update remaining time on server once per second or in `UGCGameState:ReceiveTick`.
4. Replicate/display only the remaining value clients need.
5. When remaining time reaches 0, stop the action tick and transition with `LuaQuickFireEvent`.

Local UI-only countdown:

1. Use `UGCTimerTools:InsertTimer(...)`.
2. Make sure `UGCTimerTools:Tick(DeltaTime)` is called regularly.
3. Keep the timer handle if it may need cancellation.

## Add A New Game Phase

Use when adding phases such as warmup, choosing, preparing, fighting, settlement, or next round.

Steps:

1. Add the phase value to `GlobalConfig.lua` or the local game-state enum table.
2. Add or update an `Action_*` script under `Script/gamemode/`.
3. In `Action_X:Execute`, set the authoritative `UGCGameSystem.GameState.CurGameStatus`.
4. Put per-phase setup in the action: team refresh, equipment grant, UI notification, countdown setup.
5. If the action needs time, set `self.bEnableActionTick = true` and implement `Update`.
6. End by calling `LuaQuickFireEvent("NextPhaseName", self)`.
7. Ensure UI observes the phase through replicated GameState or ClientRPC.

## Grant Items Or Loadouts

Use when giving weapons, bullets, armor, supplies, or skill-related items.

Steps:

1. Put item IDs and counts in a config table instead of hardcoding inside UI.
2. Run grant logic on server, usually in PlayerController, GameMode, Action, or Pawn depending on ownership.
3. Get the player pawn from `UGCGameSystem.GetPlayerPawnByPlayerKey(PlayerKey)` or controller safety helpers.
4. Check current count with `UGCBackPackSystem.GetItemCount`.
5. Add missing items with `UGCBackPackSystem.AddItem`.
6. Send UI feedback with ClientRPC if needed.

## Create A Widget Through UIManager

Use when adding Main UI, guide UI, settlement UI, shop UI, voting UI, or any reusable screen.

Steps:

1. Add a path constant to `UIManager.lua`.
2. Build the path from `UGCMapInfoLib.GetRootLongPackagePath()`.
3. Load the class with `UE.LoadClass`.
4. Get local player controller.
5. Create the widget with `UserWidget.NewWidgetObjectBP`.
6. Call `AddToViewport(ZOrder)` if needed.
7. Store the widget on `UIManager` if it will be reused/hidden later.

Always nil-check class, player controller, and widget creation.

## Add A Skill Button Or Cooldown

Use when adding a custom skill, skill selection, cooldown progress, remaining uses, or a second-stage skill button.

Steps:

1. Add skill data to config: name, description, icons, cooldown, use cooldown, max charges, round cap.
2. Initialize per-player skill state in GameState tables keyed by `PlayerKey`.
3. Use PlayerController server RPC for skill selection or activation.
4. Server validates pawn, current phase, remaining uses, and cooldown.
5. Trigger the skill manager or spawn the skill actor on server.
6. Update replicated cooldown/use tables.
7. Send UI events via ClientRPC for icon state, CD, remaining uses, and special button visibility.

## Handle Reconnect Or Respawn

Use when UI disappears, equipment is missing, team data is wrong, or skill state is stale after reconnect/respawn.

Steps:

1. Register controller delegates on server:
   - `PlayerControllerRespawnedDelegate`
   - `PlayerControllerReconnectedDelegate`
   - `PlayerControllerRecoveredDelegate`
2. In callbacks, check current game phase.
3. Regrant equipment only if needed.
4. Re-send team, score, phase, chosen loadout/skill, and UI visibility with ClientRPC.
5. Make UI event handlers idempotent so duplicate updates are safe.

## Add A World Actor Lookup

Use when finding spawn points, triggers, target actors, pickups, or skill helper actors.

Steps:

1. Prefer a resource helper such as `ResourcesTools.GetAllActorsOfClass(WorldContext, "Asset/...Foo_C")`.
2. Use tags when class alone is too broad.
3. Nil-check and empty-check actor arrays.
4. Avoid scanning every tick unless cached or very small.
5. Store stable references in GameState/GameMode only if lifetime is clear.

## Debug A Feature That Does Nothing

Use this checklist:

1. Is the code running on the expected side: server or client?
2. Did `ReceiveBeginPlay`, `Construct`, or `Execute` actually print?
3. Is the Blueprint class/object path correct, including `_C` for classes?
4. Is the ServerRPC registered in `GetAvailableServerRPCs()`?
5. Is the target PlayerController/Pawn/State nil?
6. If UI should update, did the ClientRPC run and send the `UGCEventSystem` event?
7. If replicated data should update, is it in `GetReplicatedProperties()` and, for tables, was lazy replication triggered?
