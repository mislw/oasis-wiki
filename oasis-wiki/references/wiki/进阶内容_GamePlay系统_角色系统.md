# 进阶内容/GamePlay系统/角色系统

> 本分类共 4 篇文章

---


## 角色出生点

> 文档路径: 进阶内容 > GamePlay系统 > 角色系统 > 角色出生点

**涉及API:** `BP_PlayerStartManager`, `BP_STPlayerStart`, `ComponentManager`, `DebugPlayerSettings`, `FindPlayerStartByBornPointID`, `GetUGCModePlayerStart`, `HasAuthority`, `IsMarkOccupied`, `KismetSystemLibrary.GetObjectName`, `PlayerBornPointID`, `PlayerStartManager`, `SetMarkOccupied`, `UGCGameMode`, `UGCGameSystem`

#  角色出生点

在绿洲启元编辑器中，开发者可以放置角色出生点来划定玩家们的出生位置，也可以通过配置不同的ID属性，以决定不同队伍在地图上的出生位置。

<br>

## 创建出生点

出生点是一种名为 ``BP_STPlayerStart`` 的蓝图，该蓝图有三种获取方式：模式面板、资源目录及蓝图创建。

**模式面板**

点击编辑器的菜单栏 ``窗口 -> 模式``，可以开启模式面板：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yDq1kimage.png)

在模式面板中搜索“PlayerStart”即可找到该蓝图：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/H1EB8image.png)

> 另一个“PlayerStart”为UE原生的出生点蓝图，不建议使用

**资源目录**

在资源目录下也可以通过“PlayerStart”查找到该蓝图：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/obdLeimage.png)

**蓝图创建**

在工程任意目录下右键点击 ``Blueprint Class``，搜索“PlayerStart”找到该蓝图，选中后即可创建出生点蓝图：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/H3ztqimage.png)

以上任意方式获得出生点蓝图后，将该蓝图放置在关卡中合适的位置进行实例化，PlayerPawn会根据该出生点结合指定规则进行出生。

![企业微信截图_1686711110328.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686711110328.png)

<br>

## 配置出生规则

玩家角色的出生规则一般由开发者定义，如果关卡场景中存在多个出生点蓝图实例，且未实现出生逻辑，则默认会从多个出生点内随机一个点位进行出生；当玩法中存在多个阵营时，开发者需要实现出生规则以避免不同阵营的玩家出生在同一点位。

**1. 设置PlayerBornPointID**

出生点蓝图的 ``PlayerBornPointID`` 属性标识该出生点用于带有指定ID的玩家出生，常见的做法是将该属性值设置为队伍ID。

![企业微信截图_168671112293.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_168671112293.png)

**2. 创建及配置PlayerStartManager**

``PlayerStartManager`` 负责管理出生规则，具体的逻辑实现都写在该类文件中。

右键点击 ``Blueprint Class``，搜索“PlayerStartManager”，找到名为 ``BP_PlayerStartManager`` 的组件，选择创建并命名为“MyStartManager”。

![企业微信截图_16867111639124.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867111639124.png)

打开工程Blueprint目录下的 ``UGCGameMode`` 蓝图，在【细节面板】中找到``ComponentManager``属性，展开 ``GMComponentManager/ComponentConfigs`` 子属性，添加一个配置项，并设置以下参数：
- SubSystemId：ESSPlayerStartManager
- SubSystemClass：MyStartManager

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MfDiVimage.png)

**3. 实现自定义出生规则**

双击打开MyStartManager蓝图，点击组件菜单栏的“Lua”按钮，打开MyStartManage类脚本文件：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2LoOyimage.png)

``GetUGCModePlayerStart`` 函数可以覆写出生规则，以下为示例：

```lua
--角色出生点管理器
local MyStartManager = {}; 

function MyStartManager:GetUGCModePlayerStart(Controller)

    --标记当前属于服务器还是客户端
    if UGCGameSystem.GameState:HasAuthority() == true then 
        print("MMG_Lua MyStartManager:GetUGCModePlayerStart Server");
    else
        print("MMG_Lua MyStartManager:GetUGCModePlayerStart Client");
    end

    --获取当前控制器的玩家状态（PlayerState）
    local PlayerState = Controller.PlayerState;

    --PlayerState为空时，打印警告
    if PlayerState == nil then
        print( "Error: MyStartManager:GetUGCModePlayerStart PlayerState is nil!");
    end

    --根据玩家团队编号获取玩家出生点（PlayerStart）
    local SelectedPlayerStart = self:FindPlayerStartByBornPointID(PlayerState.TeamID, true);--当一个出生点已经被使用过一次，用于出生玩家时，自动寻找其他未被使用的出生点

    --打印当前玩家的队伍编号（TeamID）
    print(string.format("MMG_Lua MyStartManager:GetUGCModePlayerStart PlayerState.TeamID[%s]", PlayerState.TeamID));

    --若找到玩家出生点（PlayerStart），打印当前玩家出生点名称和对应BornID，否则输出错误信息
    if SelectedPlayerStart ~= nil then
        print(string.format("MyStartManager:GetUGCModePlayerStart SelectedPlayerStart[%s] BornID[%d] PlayerID[%s]",   
        KismetSystemLibrary.GetObjectName(SelectedPlayerStart), SelectedPlayerStart.PlayerBornPointID, Controller.PlayerKey));
        --设置当前PlayerStart被占用
        SelectedPlayerStart:SetMarkOccupied();
        print(string.format( "PlayerStartOccupied?[%s]",SelectedPlayerStart:IsMarkOccupied()));
        return SelectedPlayerStart;
    else
        print("Error: MyStartManager:GetUGCModePlayerStart SelectedPlayerStart is nil!");
    end

    return nil;
end

return MyStartManager;
```

> 玩家复活时，也是通过GetUGCModePlayerStart函数决定复活点，因此需要在该函数内对初始出生和复活按需区分处理逻辑


<br>

## 运行调试

在 ``DebugPlayerSettings`` 面板中设置好队伍数量及每队的玩家数量后，点击“调试”按钮即可查看最终出生效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gbLtVimage.png)

![企业微信截图_1686711975945.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686711975945.png)



---


## 队伍与阵营

> 文档路径: 进阶内容 > GamePlay系统 > 角色系统 > 队伍与阵营

**涉及API:** `Camp`, `ChangePlayerTeamID`, `DA_GameModeGeneral`, `PlayerBornPointID`, `SetCampForActor`, `SetCampForTeam`, `UGCPlayerPawn`

# 队伍与阵营

## 队伍系统

和平精英内置了一套完整的队伍系统，玩法可以按需求设置匹配时的队伍构成，也允许对处于局内的玩家重新分队，同队伍的玩家头顶会显示带有队内编号的UI，大 [小地图](https://developer.gp.qq.com/wikieditor/#/catalog/152) 上也会显示同队玩家的实时位置，如果 [启用了组队面板](https://developer.gp.qq.com/wikieditor/#/catalog/239) 还会显示同队玩家的状态。

![企业微信截图_17441867608036.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l1lRW%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17441867608036.png)

### 设置队伍

玩法可以设置匹配时的队伍数及每队人数，匹配系统将优先参考设置将满足人数条件的玩家拉入对局，具体设置可参考 [队伍设置](https://developer.gp.qq.com/wikieditor/#/catalog/127?autoJump=1.1+%E9%98%9F%E4%BC%8D%E8%AE%BE%E7%BD%AE:~:text=1.1-,%E9%98%9F%E4%BC%8D%E8%AE%BE%E7%BD%AE,-%E3%80%90%E9%98%9F%E4%BC%8D%E6%95%B0%E9%87%8F%E3%80%91%EF%BC%9A%E6%8C%87) 部分内容。
> 和平大厅组队人数最多4人，如果匹配设置单队人数过多，会导致拉入对局的玩家队伍组成存在不稳定的情况

---

### 动态分队

所有进入对局的玩家都会拥有各自的队伍编号，即使玩家以单人进入对局，系统也会为其分配一个默认的队伍编号；如果涉及二次分队，例如非对称类型的玩法，则需要调用 [``ChangePlayerTeamID``](https://developer.gp.qq.com/api/#/searchContent/UGCTeamSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%A4%BE%E4%BA%A4%E7%B3%BB%E7%BB%9F%2FUGCTeamSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCTeamSystem&autoJump=ChangePlayerTeamID) 进行动态调整。

代码示例：

``` lua
local Pawns = UGCGameSystem.GetAllPlayerPawn()

if Pawns[1] then
	local PlayerKey = UGCPawnAttrSystem.GetPlayerKeyInt64(Pawns[1])
	UGCTeamSystem.ChangePlayerTeamID(PlayerKey, NewTeamID)
end
```

---

### 大厅组队与玩法队伍

和平大厅的组队与玩法队伍系统是两套独立的队伍关系，队伍系统中的分队是临时性的队伍关系，当该对局结束时即结束队伍关系；和平大厅的队伍关系仅作为匹配成局时的分队参考，不影响玩法内的重新分队，且分队后也不影响和平大厅的队伍组成关系，即从玩法返回大厅时队伍关系仍然保留。

> [二次匹配](https://developer.gp.qq.com/wikieditor/#/catalog/376) 功能扩展了大厅队伍关系的能力，支持加入大厅队伍和同进同出子模式

![613b8712bfa4d139ca688a2280aa54ba.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7yjVw613b8712bfa4d139ca688a2280aa54ba.png)

<br>

## 阵营系统

队伍系统虽然满足了组队需求，但是分配机制和角色定位较为固定，不同队伍之间固定为敌对关系，缺乏竞技对抗的深度，为此额外构建了阵营系统。

新的阵营系统提供了更灵活的敌对关系配置，同时配合新的 [怪物系统](https://developer.gp.qq.com/wikieditor/#/catalog/20144) 同步支持怪物的阵营分配，开发者仅需通过蓝图参数设置即可实现阵营的分配，也支持通过 [UGCCampSystem](https://developer.gp.qq.com/api/#/searchContent/UGCCampSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%A4%BE%E4%BA%A4%E7%B3%BB%E7%BB%9F%2FUGCCampSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCampSystem) 提供的接口动态调整阵营。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/J8Lx3image.png)

---

### 阵营关系配置

工程已有一套默认的阵营配置表，该表入口位于 ``玩法通用设置``，在编辑器菜单栏点击【玩法通用设置】按钮,或在 ``Asset/Data`` 目录下找到通用配置数据资产蓝图 ``DA_GameModeGeneral``。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UkHGaimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Nt4mCimage.png)

> 如果数据资产蓝图被误删除，可通过点击【玩法通用设置】按钮重新生成该蓝图

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AOJ4vimage.png)

双击打开 ``DA_GameModeGeneral``，在 ``Camp`` 属性项中添加需要配置的阵营信息。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pyXnximage.png)

各阵营之间必须存在明确的对立/共存关系，例如：当阵营1与阵营2设置为中立关系，阵营2与阵营3设置为敌对关系时，阵营1与阵营3的关系仍需独立设置，因此必须确保每个阵营之间的关系（中立/敌对/结盟）都被明确配置，以保证游戏逻辑的正确性和可预测性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6e8f0image.png)

|属性名|属性说明|
|-|-|
|阵营设置|Camp ID：阵营的唯一ID<br>Camp Name：阵营的名称|
|阵营出生方式配置|支持按阵营设置出生点的逻辑，数组结构为 ``阵营id + 出生配置``的形式，其中0为占位阵营无法变更设置<br>- 阵营出生方式：指定出生点或者指定位置坐标<br>- 指定PlayerStartID：当 ``阵营出生方式``选为“指定PlayerStartID”时有效，对应 [``PlayerBornPointID``](https://developer.gp.qq.com/wikieditor/#/catalog/362?autoJump=%E9%85%8D%E7%BD%AE%E5%87%BA%E7%94%9F%E8%A7%84%E5%88%99)<br>- 当有多个PlayerStartID时是否随机选择：当 ``阵营出生方式``选为“指定PlayerStartID”时有效，如果关卡中放置了多个出生点，则会从这些出生点里随机选择一个<br>- 指定世界坐标：当 ``阵营出生方式``选为“指定世界坐标”时有效，填写具体的坐标值|
|阵营关系|Camp A/B ID：建立关系的阵营ID<br>Releation：具体阵营关系<br>- Same：同阵营（友方）<br>- Enemy：敌人<br>- Neutral：中立|
|默认阵营关系|所有配置的阵营，若未指定阵营关系，将使用此默认关系|
|不同队伍属于不同阵营|针对玩家角色的选项，如果勾选，则优先按队伍ID设置阵营，确保每个玩家都有初始阵营，但不保证阵营ID值一定等于队伍ID；否则，阵营ID默认全为1|

> 阵营ID相同默认为同阵营关系

---

### 设置怪物阵营
	
当怪物未主动配置阵营时，系统默认将其阵营ID设为0；如需调整怪物阵营，在怪物蓝图中，搜索“General Camp”，将 ``General Camp ID`` 属性设置为目标阵营ID，该怪物生成后将被分配在对应的阵营下。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IwZvuimage.png)

如果使用了 [怪物刷新器](https://developer.gp.qq.com/wikieditor/#/catalog/20156) 生成怪物，会以 [怪物组表](https://developer.gp.qq.com/wikieditor/#/catalog/20156?autoJump=%E6%80%AA%E7%89%A9%E7%BB%84%E8%A1%A8) 里配置的阵营ID为准。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/COOJbimage.png)
	
---
	
### 设置角色阵营
	
玩家角色阵营取决于 ``不同队伍属于不同阵营`` 的属性设置，若未勾选，系统默认将其阵营ID设为1；否则，将玩家队伍ID同步到阵营ID。

> ``UGCPlayerPawn`` 蓝图的 ``General Camp ID`` 属性设置无效
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dslerimage.png)

---
	
### 动态修改阵营

**玩家阵营**

如果希望在玩法进程中动态修改玩家的阵营，可以调用 [`SetCampForTeam`](https://developer.gp.qq.com/api/#/searchContent/UGCCampSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%A4%BE%E4%BA%A4%E7%B3%BB%E7%BB%9F%2FUGCCampSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCampSystem&autoJump=SetCampForTeam) 进行修改，需要注意的是单个玩家无法单独设置阵营，仅能通过队伍所属阵营间接修改玩家阵营。

代码示例：

``` lua
local TargetCampID = 3
local PlayerTeamID = UGCPawnAttrSystem.GetTeamID(PlayerPawn)
UGCCampSystem.SetCampForTeam(PlayerTeamID, TargetCampID)
```

<br>
	
**怪物阵营**

如果希望在玩法进程中动态修改怪物的阵营，可以调用 [`SetCampForActor`](https://developer.gp.qq.com/api/#/searchContent/UGCCampSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%A4%BE%E4%BA%A4%E7%B3%BB%E7%BB%9F%2FUGCCampSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCampSystem&autoJump=SetCampForActor) 进行修改。

代码示例：

``` lua
local TargetCampID = 3
local ClassPath = UGCObjectUtility.LoadClass(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Prefabs/Monsters/Boss.Boss_C'))
local BossActor = UGCGenericCharacterSystem.SpawnGenericCharacter(self, ClassPath, { X = 20460.0, Y = 29410.0, Z = 200 }, { Roll = 0, Pitch = 0, Yaw = 0 }, { X = 1, Y = 1, Z = 1 })

if BossActor then
		UGCCampSystem.SetCampForActor(BossActor, TargetCampID)
end
```

<br>

## API参考
	
|函数库/类名|函数类型|函数功能范围|
|-|-|-|
|[UGCTeamSystem](https://developer.gp.qq.com/api/#/searchContent/UGCTeamSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%A4%BE%E4%BA%A4%E7%B3%BB%E7%BB%9F%2FUGCTeamSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCTeamSystem)|静态函数|动态设置、获取玩家队伍ID，查询队友、队长等|
|[UGCCampSystem](https://developer.gp.qq.com/api/#/searchContent/UGCCampSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%A4%BE%E4%BA%A4%E7%B3%BB%E7%BB%9F%2FUGCCampSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCampSystem)|静态函数|动态修改、获取阵营关系|

---


## 物品掉落与保留

> 文档路径: 进阶内容 > GamePlay系统 > 角色系统 > 物品掉落与保留

**涉及API:** `DA_GameModeGeneral`, `IsSkipSpawnDeadTombBox`, `UGCPlayerPawn`

# 物品掉落与保留

和平精英基于大逃杀玩法的机制设计，当玩家死亡时固定以死亡盒子的形式掉落背包物品，为了提高物品掉落策略的灵活性，在物资编辑器2.0的基础上对物品属性及掉落功能进行了扩展，允许开发者自定义玩家角色的物品掉落与保留规则。

<br>

## 设置死亡掉落类型

角色物品掉落特指玩家角色死亡时触发的掉落行为，因此需要先指定死亡掉落物品的形式。

点击编辑器菜单栏【玩法通用设置】按钮，在 ``DA_GameModeGeneral`` 数据资产蓝图中找到“Pawn”属性类目，该类别下定义了一个名为 ``玩家死亡掉落类型`` 的属性，该属性决定玩家角色死亡时是否允许掉落背包物品及掉落的形式，开发者需设置合适的掉落类型。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UlDxKimage.png)

**生成死亡盒子**

默认的掉落类型，背包中能够掉落的物品都收集在盒子中，与和平精英的角色物品掉落方式保持一致。

![QQ2025624-212438-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/V1cf2QQ2025624-212438-HD-ezgif.com-video-to-gif-converter.gif)

**散落**

能够掉落的物品将以可拾取物的形态分散掉落在角色死亡的位置附近。

![QQ2025624-211856-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4Do6LQQ2025624-211856-HD-ezgif.com-video-to-gif-converter.gif)

**不生成盒子也不散落**

设置为该类型将禁止角色掉落背包物品。

![QQ2025624-214634-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/d0OlbQQ2025624-214634-HD-ezgif.com-video-to-gif-converter.gif)

<br>

## 配置物品掉落属性

各类物品模板属性的 [V2背包配置](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=V2%E8%83%8C%E5%8C%85%E9%85%8D%E7%BD%AE) 类目中都具有 ``死亡物品掉落配置`` 属性，该属性决定了此类型的物品能否掉落或者保留，结合死亡掉落类型的组合配置可以实现不同的掉落与保留效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/u1MRvimage.png)

| |留在背包|掉落|直接删除|
|:-:|:-:|:-:|:-:|
|**生成死亡盒子**|保留|掉落|✖|
|**散落**|保留|掉落|✖|
|**不生成盒子也不散落**|保留|✖|✖|

<br>

## 注意事项

- 以上配置方式仅适用于 [物品编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20101) 创建的物品，且需要启用新的 [背包系统](https://developer.gp.qq.com/wikieditor/#/catalog/20104)；对于使用和平原生物品及经典背包的场景，仅支持控制是否生成死亡盒子，通过覆写 **UGCPlayerPawn** 的 ``IsSkipSpawnDeadTombBox`` 函数实现：
	```lua
	function UGCPlayerPawn:IsSkipSpawnDeadTombBox(EventInstigater)
    		return true
	end
	```
- 枪械的配件及子弹也属于独立的物品，因此需要配合枪械单独配置掉落属性，否则会出现保留或掉落效果不一致的现象






---


## 角色Avatar复制

> 文档路径: 进阶内容 > GamePlay系统 > 角色系统 > 角色Avatar复制

# 角色Avatar复制

编辑器已提供专用于玩家角色Avatar的展示Actor，该Actor属于静态物件，开发者可通过调用特定的API将玩家角色的Avatar复制到此物件中，以实现展示角色Avatar的效果。

![ScreenShot_2025-10-21_103538_182.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TPMxnScreenShot_2025-10-21_103538_182.png)

<br>

## 添加Avatar展示Actor

在【模式】中搜索“UGCClientAvatarShowcaseActor_Base_BP”，将该Actor放置在场景中。

![Avater-加入avatar.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2IT0cAvater-%E5%8A%A0%E5%85%A5avatar.drawio.png)

<br>

## 复制Avatar

Avatar展示Actor可用于展示角色Avatar，通过API调用实现，目前提供两种方法，适用于不同场景需求：

|方法|生效范围|适用场景|
|:-:|:-:|-|
|[ClientShowAvatar](https://developer.gp.qq.com/api/#/searchContent/UGCCharAvatarShowcaseActor?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCCharAvatarShowcaseActor.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCharAvatarShowcaseActor&autoJump=ClientShowAvatar)|客户端|适用于小场景展示，确保需展示的角色在当前客户端视野范围内且未被剔除|
|[ServerShowAvatar](https://developer.gp.qq.com/api/#/searchContent/UGCCharAvatarShowcaseActor?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCCharAvatarShowcaseActor.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCharAvatarShowcaseActor&autoJump=ServerShowAvatar)|服务器|适用于大场景展示，可确保所有客户端都能看到Avatar展示，需展示的角色不受视野限制|

以下为使用示例，界面设计如下：

![Avater-第 9 页.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/p42SMAvater-%E7%AC%AC%209%20%E9%A1%B5.drawio.png)

为按钮添加对应功能逻辑，点击“ClientShowAvatar”按键的执行代码如下:

``` lua
--Main.lua部分代码

function MainUI:ButtonClientShowAvatarOnClicked()
	ugcprint("客户端执行展示角色");
	--根据ID名称获取Actor
  local AvatarDisplayActor = UGCObjectUtility.FindObject("AvatarDisplayActor");
	--获取客户端当前的 PlayerController
  local PlayerController = UGCGameSystem.GetLocalPlayerController();
	--获取PlayerController对应的Uid
	local Uid = UGCGameSystem.GetUIDByPlayerController(PlayerController);
	--根据Uid展示对应玩家形象（客户端执行）
  AvatarDisplayActor:ClientShowAvatar(Uid);
	return nil;
end

```

点击“ServerShowAvatar”按键的执行代码如下:

``` lua
--Main.lua部分代码

function MainUI:ButtonServerShowAvatarOnClicked()
	ugcprint("服务器执行展示角色");
	--获取客户端当前的 PlayerController
  local PlayerController = UGCGameSystem.GetLocalPlayerController();
	--调用PlayerController的ServerRPC函数
  UnrealNetwork.CallUnrealRPC(PlayerController, PlayerController, "ShowAvatarByServer");
	return nil;
end

--UGCPlayerController.lua部分代码

--接收RPC调用
function UGCPlayerController:GetAvailableServerRPCs()
	return
  "ShowAvatarByServer"
end

function UGCPlayerController:ShowAvatarByServer()
  --根据ID名称获取Actor
  local AvatarDisplayActor = UGCObjectUtility.FindObject("AvatarDisplayActor");
  --获取PlayerController对应的Uid
	local uid = UGCGameSystem.GetUIDByPlayerController(self);
  --根据Uid展示对应玩家形象（服务器执行）
  AvatarDisplayActor:ServerShowAvatar(uid);
end

```

调试效果如下，点击“ClientShowAvatar”按键，Avatar展示Actor显示当前玩家的角色Avatar。

![avt显示客户端.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WxwA6avt%E6%98%BE%E7%A4%BA%E5%AE%A2%E6%88%B7%E7%AB%AF.gif)

如果在需展示的角色被剔除时再点击“ClientShowAvatar”按键，Avatar展示Actor不会显示Avatar。

![ScreenShot_2025-10-20_150428_271.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5KKMfScreenShot_2025-10-20_150428_271.png)

点击“ServerShowAvatar”按键，Avatar展示Actor显示当前玩家的角色Avatar，无论角色是否被剔除。

![avt显示服务端.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8HZ4Lavt%E6%98%BE%E7%A4%BA%E6%9C%8D%E5%8A%A1%E7%AB%AF.gif)
![ScreenShot_2025-10-20_150445_218.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UYpFNScreenShot_2025-10-20_150445_218.png)

<br>

## 播放角色动画

[PlayAnim](https://developer.gp.qq.com/api/#/searchContent/UGCCharAvatarShowcaseActor?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCCharAvatarShowcaseActor.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCCharAvatarShowcaseActor&autoJump=PlayAnim) 方法可控制Avatar展示Actor循环播放或停止指定动画。以下为使用示例，界面设计如下：

![Avater-第 7 页 的副本.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RvPHJAvater-%E7%AC%AC%207%20%E9%A1%B5%20%E7%9A%84%E5%89%AF%E6%9C%AC.drawio.png)

为按钮添加对应功能逻辑，部分代码如下：

``` lua
--Main.lua部分代码

function MainUI:ButtonPlayAnimOnClicked()
	ugcprint("播放动画");
	--根据路径加载动画资源（该路径对应动画蒙太奇“机动兵投掷物飞行_Montage”）
  local Animation = UE.LoadObject('/Game/Arts_Timeliness/CG005_Hero/Arts_Player/Anim/AgileSoldier/AgileSoldier_Grenade_Fly_Montage.AgileSoldier_Grenade_Fly_Montage');
	--根据ID名称获取Actor
	local AvatarDisplayActor = UGCObjectUtility.FindObject("AvatarDisplayActor");
	--循环播放动画
	AvatarDisplayActor:PlayAnim(Animation, true);
	return nil;
end

function MainUI:ButtonStopAnimOnClicked()
	ugcprint("停止动画");
	--根据路径加载动画资源（该路径对应动画蒙太奇“机动兵投掷物飞行_Montage”）
  local Animation = UE.LoadObject('/Game/Arts_Timeliness/CG005_Hero/Arts_Player/Anim/AgileSoldier/AgileSoldier_Grenade_Fly_Montage.AgileSoldier_Grenade_Fly_Montage');
	--根据ID名称获取Actor
	local AvatarDisplayActor = UGCObjectUtility.FindObject("AvatarDisplayActor");
	--停止播放动画
	AvatarDisplayActor:PlayAnim(Animation, false);
	return nil;
end

```

Avatar展示Actor显示Avatar后，点击“PlayAnim”按键，该Actor会循环播放指定动画。

![循环播放3.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UL3hM%E5%BE%AA%E7%8E%AF%E6%92%AD%E6%94%BE3.gif)

点击“StopAnim”按键，该Actor播放一次指定动画后停止。

![停止播放2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7gpGn%E5%81%9C%E6%AD%A2%E6%92%AD%E6%94%BE2.gif)

---
