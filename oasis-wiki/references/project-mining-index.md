# UGC Project Mining Index

Use this file to decide where to look next in the local project corpus. It records high-signal files and patterns found while distilling the projects into `project-patterns.md`.

## High-Signal Project Folders

- `Solo`: compact round-based PvP structure with `Action_*`, `UGCEventSystem`, `UGCTimerTools`, `UIManager`, skills, loadouts, and reconnect handling.
- `HappyParty` / `HappyParty2`: UI-heavy party mode examples with many widgets and gamemode actions.
- `Defend`: RPC-heavy attack/defense flow with team score, weapon choice, spectating, and custom interactions.
- `ZombieFight`: PvE/store/reconnect examples with PlayerController and GameState RPC usage.
- `DancingCard`: rhythm-style UI and server event examples.
- `Template_CTCompetition`: official team competition style using `TeamModeComponent`, `RepLazyProperty`, `ForceNetUpdate`, `K2_PostLogin`, and ParamSetting.
- `Template_RogueShooting`: modern template using `UGCGameSystem.UGCRequire`, `UGCGenericMessageSystem`, `UGCLevelFlowSystem`, stream levels, and monster kill rewards.

## Search Commands

Run from any directory:

```powershell
rg -n "GetAvailableServerRPCs|CallUnrealRPC|RepLazyProperty|ForceNetUpdate" "E:\Program Files (x86)\2001776(2001776)\ShadowTrackerExtra\UGCProjects" -g "*.lua"
rg -n "LuaQuickFireEvent|Action_.*:Execute|bEnableActionTick" "E:\Program Files (x86)\2001776(2001776)\ShadowTrackerExtra\UGCProjects" -g "*.lua"
rg -n "UGCEventSystem:AddListener|UGCEventSystem:SendEvent|EventDefine" "E:\Program Files (x86)\2001776(2001776)\ShadowTrackerExtra\UGCProjects" -g "*.lua"
rg -n "UserWidget.NewWidgetObjectBP|AddToViewport|MainControlPanelTochButton_C" "E:\Program Files (x86)\2001776(2001776)\ShadowTrackerExtra\UGCProjects" -g "*.lua"
rg -n "UGCBackPackSystem.AddItem|GetSkillManagerComponent|TriggerEvent" "E:\Program Files (x86)\2001776(2001776)\ShadowTrackerExtra\UGCProjects" -g "*.lua"
```

## Representative Files

Open these when a task needs project-style examples:

- `Solo\Script\Blueprint\UGCGameMode.lua`: server ranking sync, damage modification.
- `Solo\Script\Blueprint\UGCGameState.lua`: replicated state, UI initialization, timer tick, skill cooldown state.
- `Solo\Script\Blueprint\UGCPlayerController.lua`: server RPC whitelist, respawn/reconnect delegates, client RPC -> UI event bridge.
- `Solo\Script\UIManager.lua`: widget path loading, viewport add, base Peace UI hiding.
- `Solo\Script\Common\UGCEventSystem.lua`: local Lua event bus.
- `Solo\Script\Common\UGCTimerTools.lua`: lightweight timer manager.
- `Solo\Script\Common\ResourcesTools.lua`: root-relative class/object loading and actor lookup helpers.
- `Solo\Script\gamemode\Action_RoundPrepare.lua`: phase action with countdown, team refresh, equipment/skill setup, and transition to `RoundStart`.
- `Solo\Script\GameConfigs\GlobalConfig.lua`: data-driven item/skill/UI config tables.
- `Template_CTCompetition\Script\Blueprint\ClassicTeamDeathMatchGameMode.lua`: team template, login/team reassignment, lazy replication.
- `Template_RogueShooting\Script\Blueprint\UGCGameMode.lua`: modern template APIs, level flow, stream level loading, global message listener.

## What Not To Import Into The Skill

- Full project source trees.
- Asset paths that are only meaningful to one project unless they illustrate a generic path rule.
- Large business-specific config tables.
- Repeated generated files where the only useful information is already summarized in `project-patterns.md`.

When in doubt, add a short derived note, a search command, or a representative path instead of copying source.
