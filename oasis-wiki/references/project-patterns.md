# UGC Project Patterns

This reference summarizes reusable UGC Lua architecture patterns. It avoids project-specific names, local paths, and private planning details. Keep project-specific notes in local project memory instead of this public bundle.

Common repeated script names:

- `UGCGameMode.lua`, `UGCGameState.lua`, `UGCPlayerController.lua`, `UGCPlayerPawn.lua`, `UGCPlayerState.lua`
- `EventDefine.lua`, `GlobalConfig.lua`, `CommonConfigPackage.lua`
- `UGCEventSystem.lua`, `UGCTimerTools.lua`, `ResourcesTools.lua`, `TableHelper.lua`, `VectorHelper.lua`
- `UIManager.lua`, `MainUI.lua`, `GuideUI.lua`, `SettlementUI.lua`
- `Action_SendEvent.lua`, `Action_PlayerLogin.lua`, `Action_WaitingPlayer.lua`, `Action_GamePrepare.lua`, `Action_GameStart.lua`, `Action_RoundPrepare.lua`, `Action_RoundStart.lua`, `Action_RoundEnd.lua`, `Action_GameEnd.lua`

## Standard Project Shape

Prefer this organization when creating or explaining a non-trivial gameplay project:

```text
Script/
  Blueprint/
    UGCGameMode.lua
    UGCGameState.lua
    UGCPlayerController.lua
    UGCPlayerPawn.lua
    UGCPlayerState.lua
  Common/
    UGCEventSystem.lua
    UGCTimerTools.lua
    ResourcesTools.lua
    TableHelper.lua
    VectorHelper.lua
  GameConfigs/
    CommonConfigPackage.lua
    EventDefine.lua
    GlobalConfig.lua
    DropItemConfig.lua
  gamemode/
    Action_*.lua
  UI/
    MainUI.lua
    GuideUI.lua
    SettlementUI.lua
  UIManager.lua
```

Use `CommonConfigPackage.lua` as the aggregation point for common helpers and configs. Use `EventDefine.lua` for numeric/local event IDs. Put tunable gameplay data such as item loadouts, skill cooldowns, UI labels, round durations, and scoring rules in `GlobalConfig.lua` or a focused config file.

## Runtime Responsibility Split

Use these boundaries:

- `UGCGameMode`: server-only authority. Handle team allocation, login decisions, damage modification, match state entry, and server-owned actor spawning.
- `UGCGameState`: replicated match state. Store current game state, countdowns, round number, team scores, player summaries, and replicated per-player tables. Tick shared timers and server-side countdown math here when clients need the result.
- `UGCPlayerController`: player-specific RPC bridge. Register server RPC names in `GetAvailableServerRPCs`, receive UI requests from the owning client, execute server validation/changes, and send client RPCs back.
- `UGCPlayerPawn`: character-side interaction, movement, overlap, skill effects, and pawn-owned replicated fields.
- `UGCPlayerState`: persistent player data such as team, score, kills, deaths, UID/profile fields, and reconnection-friendly state.
- `UIManager`: client UI factory and base UI hiding/showing. It loads widget classes, creates widgets through `UserWidget.NewWidgetObjectBP`, and adds them to viewport.
- `Action_*`: level-flow/game-mode action units. Keep actions small and chain phases with `LuaQuickFireEvent`.

## Game Flow Pattern

A common flow is:

```text
PlayerLogin -> WaitingPlayer -> GamePrepare/RoundPrepare -> GameStart/RoundStart -> RoundEnd -> WaitingNextRound -> GameEnd
```

Use `Action_SendEvent.lua` style bridge actions for configurable transitions:

```lua
LuaQuickFireEvent(self.SendEventName, self)
```

Use `bEnableActionTick = true` only for actions that really need per-frame or per-second work. For countdowns, store a start time from `GameplayStatics.GetRealTimeSeconds(self)` and update visible remaining time once per second.

## Replication Pattern

For replicated state, define `GetReplicatedProperties()` on GameState, PlayerState, Pawn, or Controller and list only fields clients need.

When manually mutating team/player tables in template-style projects, call:

```lua
UnrealNetwork.RepLazyProperty(GameState, "TeamCurPlayerNum")
GameState:ForceNetUpdate()
```

For simple projects, repeated code often mutates `UGCGameSystem.GameState.SomeField` directly and relies on replicated properties. For table-heavy state, prefer explicit lazy replication after mutation.

## RPC Pattern

In `UGCPlayerController`, whitelist client-to-server calls:

```lua
function UGCPlayerController:GetAvailableServerRPCs()
    return "ServerRPC_DoThing", "ServerRPC_ChooseOption"
end
```

From UI/client code, call:

```lua
UnrealNetwork.CallUnrealRPC(PlayerController, PlayerController, "ServerRPC_DoThing", Arg)
```

For frequent UI countdown/progress updates, projects often use:

```lua
UnrealNetwork.CallUnrealRPC_Unreliable(PlayerController, PlayerController, "ClientRPC_UpdateProgress", Value)
```

For server-to-all visual/audio effects, use multicast carefully:

```lua
UnrealNetwork.CallUnrealRPC_Multicast(ActorOrGameState, "MulticastRPC_PlayEffect", ...)
```

Client RPCs commonly translate into local UI events rather than directly manipulating every widget:

```lua
UGCEventSystem:SendEvent(EventDefine.PlayerShowTips, Text)
```

## Local Event Bus Pattern

Use `UGCEventSystem` for Lua-side decoupling between PlayerController RPCs, GameState changes, and UI widgets.

Typical use:

```lua
UGCEventSystem:AddListener(EventDefine.PlayerShowTips, self.OnPlayerShowTips, self)
UGCEventSystem:SendEvent(EventDefine.PlayerShowTips, "text")
UGCEventSystem:RemoveListener(EventDefine.PlayerShowTips, self.OnPlayerShowTips, self)
```

Important habits:

- Define event IDs centrally in `EventDefine.lua`.
- Remove listeners in UI destruct/end-play paths when the widget can be recreated.
- Keep event payloads small and explicit.

## Timer Pattern

Many projects include `UGCTimerTools`:

- `InsertTimer(seconds, callback, perSecondCallback)` returns a handle.
- `RemoveTimer(handle)` clears pending callbacks.
- `Tick(deltaTime)` must be called regularly, commonly from `UGCGameState:ReceiveTick`.

Use this for local Lua scheduling. Use real server time or replicated countdown fields when the result must stay authoritative across clients/reconnects.

## UI Pattern

Common UI creation sequence:

1. Build paths from `UGCMapInfoLib.GetRootLongPackagePath()`.
2. Load widget class via `UE.LoadClass`.
3. Get local player controller through `GameplayStatics.GetPlayerController(UGCGameSystem.GameState, 0)` or `UGCGameSystem.GetLocalPlayerController()`.
4. Create widget via `UserWidget.NewWidgetObjectBP`.
5. Call `AddToViewport`, often with a high Z-order for settlement/guide overlays.

Common visibility constants:

- `ESlateVisibility.Visible`
- `ESlateVisibility.Collapsed`
- `ESlateVisibility.SelfHitTestInvisible`

Base Peace UI is often accessed through:

```lua
GameBusinessManager.GetWidgetFromName(ingame, "MainControlPanelTochButton_C")
```

Then projects hide panels with `AddAdvancedCollapsedCount(1)` or `UGCWidgetManagerSystem.AddWidgetHiddenLayer(...)`.

## Resource Loading Pattern

Keep a small resource helper:

```lua
local FullPath = UGCMapInfoLib.GetRootLongPackagePath() .. "Asset/Blueprint/Foo.Foo_C"
local Class = UE.LoadClass(FullPath)
```

Use `_C` for Blueprint classes loaded with `UE.LoadClass`. Omit `_C` for objects loaded with `UE.LoadObject`.

Common helpers:

- `UGCGameSystem.GetUGCResourcesFullPath("Asset/...")`
- `UGCObjectUtility.LoadClass(...)`
- `GameplayStatics.GetAllActorsOfClass(...)`
- `GameplayStatics.GetAllActorsWithTag(...)`

## Team And Player Handling

Common player iteration:

```lua
local PlayerStates = UGCGameSystem.GetAllPlayerState()
local PlayerControllers = UGCGameSystem.GetAllPlayerController()
```

Common lookup:

```lua
UGCGameSystem.GetPlayerControllerByPlayerKey(PlayerKey)
UGCGameSystem.GetPlayerPawnByPlayerKey(PlayerKey)
UGCGameSystem.GetPlayerStateByPlayerKey(PlayerKey)
```

When assigning teams, update PlayerState, PlayerController, and Pawn where applicable, then call the team system:

```lua
UGCTeamSystem.ChangePlayerTeamID(PlayerState.PlayerKey, TeamID)
```

Template-style code may also call `ServerChangeTeam`, `TeamModeComponent:GetTeamInfo`, or `TeamModeComponent:RemoveTeam` for official team competition modes.

## Items, Loadouts, And Skills

Put item IDs and quantities in config tables, then apply them server-side:

```lua
if UGCBackPackSystem.GetItemCount(PlayerPawn, ItemID) <= 0 then
    UGCBackPackSystem.AddItem(PlayerPawn, ItemID, Count)
end
```

Common pattern for skill loadouts:

- `GenerateWeaponAndItemConfig[SkillIndex]`: item IDs and counts.
- `SkillAndWeaponText[SkillIndex]`: UI names, descriptions, and icon paths.
- `SkillConfig[SkillIndex]`: cooldown, use cooldown, initial uses, stack cap, round cap.

For skill activation, PlayerController server RPCs often call:

```lua
local SkillManager = PlayerPawn:GetSkillManagerComponent()
SkillManager:TriggerEvent(SkillNum, UTSkillEventType.SET_KEY_DOWN)
```

Then update replicated GameState tables and send UI client RPCs.

## Reconnect And Respawn

Robust projects register server-side controller delegates:

- `PlayerControllerRespawnedDelegate`
- `PlayerControllerReconnectedDelegate`
- `PlayerControllerRecoveredDelegate`

On reconnect/respawn:

- Regenerate missing equipment if the player is in fighting state.
- Re-send team, score, chosen skill/loadout, and UI state with client RPCs.
- Avoid assuming UI still exists; send events that UI can handle idempotently.

## Common API Hotspots

These APIs are common UGC hotspots and are worth checking in the wiki before use:

- `UGCGameSystem.GameState`
- `UGCGameSystem.GameMode`
- `UGCGameSystem.GetAllPlayerController`
- `UGCGameSystem.GetAllPlayerState`
- `UGCGameSystem.GetPlayerControllerByPlayerKey`
- `UGCGameSystem.GetPlayerPawnByPlayerKey`
- `UGCGameSystem.GetPlayerStateByPlayerKey`
- `UGCGameSystem.GetUGCResourcesFullPath`
- `UGCGameSystem.GetServerTimeSec`
- `UGCGameSystem.IsServer`
- `UnrealNetwork.CallUnrealRPC`
- `UnrealNetwork.CallUnrealRPC_Unreliable`
- `UnrealNetwork.CallUnrealRPC_Multicast`
- `UnrealNetwork.RepLazyProperty`
- `GameplayStatics.GetPlayerController`
- `GameplayStatics.GetRealTimeSeconds`
- `UE.LoadClass`
- `UE.LoadObject`
- `UE.IsValid`
- `UserWidget.NewWidgetObjectBP`
- `UGCBackPackSystem.AddItem`
- `UGCTeamSystem.ChangePlayerTeamID`
- `UGCSoundManagerSystem.PlaySound2D`
- `ScriptGameplayStatics.SpawnActor`

## Practical Defaults

- Put authoritative game changes on the server side.
- Make clients ask through Controller server RPCs, not direct GameState mutation.
- Replicate only fields the UI needs.
- Use ClientRPC -> local `UGCEventSystem` -> UI handler for UI updates.
- Use config tables for IDs, timings, text, and icons.
- Check all object/class loads for nil and print useful path errors.
- Prefer `GetPlayer...ByPlayerKey` for per-player targeting.
- Use unreliable RPC only for high-frequency UI refreshes where dropped updates are acceptable.
