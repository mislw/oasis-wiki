# UGC Snippets

Use these snippets as small teaching templates. Adapt names, paths, IDs, and validation to the current project.

## PlayerController Server RPC

```lua
function UGCPlayerController:GetAvailableServerRPCs()
    return "ServerRPC_DoThing"
end

function UGCPlayerController:ServerRPC_DoThing(SomeValue)
    print(string.format("ServerRPC_DoThing SomeValue[%s]", tostring(SomeValue)))

    if not self:HasAuthority() then
        return
    end

    local PlayerPawn = self:GetPlayerCharacterSafety()
    if not PlayerPawn then
        print("ServerRPC_DoThing failed: PlayerPawn is nil")
        return
    end

    -- server-side gameplay change here
    UnrealNetwork.CallUnrealRPC(self, self, "ClientRPC_DoThingResult", true)
end

function UGCPlayerController:ClientRPC_DoThingResult(bSuccess)
    UGCEventSystem:SendEvent(EventDefine.DoThingResult, bSuccess)
end
```

## UI Button Calling Server RPC

```lua
function MainUI:Construct()
    self.Button_DoThing.OnClicked:Add(self.OnClickDoThing, self)
end

function MainUI:OnClickDoThing()
    local PlayerController = UGCGameSystem.GetLocalPlayerController()
    if not PlayerController then
        print("OnClickDoThing failed: PlayerController is nil")
        return
    end

    UnrealNetwork.CallUnrealRPC(PlayerController, PlayerController, "ServerRPC_DoThing", 1)
end
```

## ClientRPC To UI Event

```lua
-- EventDefine.lua
EventDefine.PlayerShowTips = 202

-- UGCPlayerController.lua
function UGCPlayerController:ClientRPC_PlayerShowTips(Text)
    UGCEventSystem:SendEvent(EventDefine.PlayerShowTips, Text)
end

-- MainUI.lua
function MainUI:Construct()
    UGCEventSystem:AddListener(EventDefine.PlayerShowTips, self.OnPlayerShowTips, self)
end

function MainUI:Destruct()
    UGCEventSystem:RemoveListener(EventDefine.PlayerShowTips, self.OnPlayerShowTips, self)
end

function MainUI:OnPlayerShowTips(Text)
    self.Text_Tips:SetText(tostring(Text))
end
```

## Replicated GameState Field

```lua
local UGCGameState = {
    RoundScore = 0,
    TeamScore = {},
}

function UGCGameState:GetReplicatedProperties()
    return
        "RoundScore",
        "TeamScore"
end

function UGCGameState:SetTeamScore(TeamID, Score)
    if not self:HasAuthority() then
        return
    end

    self.TeamScore[TeamID] = Score
    UnrealNetwork.RepLazyProperty(self, "TeamScore")
    self:ForceNetUpdate()
end
```

## Action Phase With Countdown

```lua
local Action_RoundPrepare = {
    PrepareTime = 20,
}

function Action_RoundPrepare:Execute()
    self.bEnableActionTick = true
    self.StartTime = GameplayStatics.GetRealTimeSeconds(self)
    self.LastShownSecond = -1

    UGCGameSystem.GameState.CurGameStatus = EGameState.GameReadyState
    UGCGameSystem.GameMode.bEnableDamage = false
    UGCGameSystem.GameState.ShownCountDown = self.PrepareTime

    return true
end

function Action_RoundPrepare:Update(DeltaSeconds)
    local Now = GameplayStatics.GetRealTimeSeconds(self)
    local Left = math.ceil(self.PrepareTime - (Now - self.StartTime))

    if Left ~= self.LastShownSecond then
        self.LastShownSecond = Left
        UGCGameSystem.GameState.ShownCountDown = math.max(Left, 0)
    end

    if Left <= 0 then
        self.bEnableActionTick = false
        LuaQuickFireEvent("RoundStart", self)
    end
end

return Action_RoundPrepare
```

## UIManager Widget Creation

```lua
UIManager.ShopUIPath = UGCMapInfoLib.GetRootLongPackagePath() .. "Asset/UI/ShopUI.ShopUI_C"

function UIManager:CreateShopUI()
    local UIClass = UE.LoadClass(self.ShopUIPath)
    if not UIClass then
        print(string.format("CreateShopUI failed: class path[%s]", tostring(self.ShopUIPath)))
        return nil
    end

    local PlayerController = GameplayStatics.GetPlayerController(UGCGameSystem.GameState, 0)
    if not PlayerController then
        print("CreateShopUI failed: PlayerController is nil")
        return nil
    end

    self.ShopUI = UserWidget.NewWidgetObjectBP(PlayerController, UIClass)
    if not self.ShopUI then
        print("CreateShopUI failed: widget is nil")
        return nil
    end

    self.ShopUI:AddToViewport(10050)
    return self.ShopUI
end
```

## Resource Helper

```lua
ResourcesTools = ResourcesTools or {}

function ResourcesTools.LoadClass(Path)
    return UE.LoadClass(UGCMapInfoLib.GetRootLongPackagePath() .. Path)
end

function ResourcesTools.LoadObject(Path)
    return UE.LoadObject(UGCMapInfoLib.GetRootLongPackagePath() .. Path)
end

function ResourcesTools.GetAllActorsOfClass(WorldContext, Path)
    local Class = ResourcesTools.LoadClass(Path)
    if not Class then
        print(string.format("GetAllActorsOfClass failed: class path[%s]", tostring(Path)))
        return {}
    end
    return GameplayStatics.GetAllActorsOfClass(WorldContext, Class)
end
```

## Grant Loadout

```lua
function UGCPlayerController:GiveLoadout(ItemList)
    if not self:HasAuthority() then
        return
    end

    local PlayerPawn = self:GetPlayerCharacterSafety()
    if not PlayerPawn then
        print("GiveLoadout failed: PlayerPawn is nil")
        return
    end

    for _, Item in ipairs(ItemList) do
        local ItemID = Item[1]
        local Count = Item[2]
        if Count > 0 and UGCBackPackSystem.GetItemCount(PlayerPawn, ItemID) <= 0 then
            UGCBackPackSystem.AddItem(PlayerPawn, ItemID, Count)
        end
    end
end
```

## EventDefine Layout

```lua
EventDefine = EventDefine or {}

EventDefine.GameStateChanged = 101
EventDefine.GameReady = 102

EventDefine.CountDownChanged = 201
EventDefine.PlayerShowTips = 202

EventDefine.TeamScoreChanged = 401
EventDefine.PlayerKilled = 501
```

Keep event ranges grouped by feature so future additions are easy to scan.
