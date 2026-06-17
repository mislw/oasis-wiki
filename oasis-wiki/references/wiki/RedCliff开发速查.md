# RedCliff（赤壁）项目开发速查指南

> 基于绿洲启元Wiki文档整理，聚焦塔防+Roguelike开发所需

---

## 目录

- [1. 核心系统速查](#1-核心系统速查)
- [2. 关键API参考](#2-关键api参考)
- [3. 常用代码模式](#3-常用代码模式)
- [4. 编辑器操作指南](#4-编辑器操作指南)
- [5. 性能优化要点](#5-性能优化要点)

---


## 1. 核心系统速查


### 技能系统

- **快速入门** (id:178)
  - API: `GameState`, `GetSkillManagerComponent`, `SkillArchetypes`, `SkillEntry_CommonDown`, `SkillIndex`, `TriggerEvent`, `UGCSkillPaths`, `UTSkillEventType`
- **技能设置，技能阶段设置详解** (id:181)
- **新建技能阶段，新建技能Action** (id:182)
  - API: `EventEffectMapForEditor`, `GetCurSkillIndex`, `GetSkillManagerComponent`, `TriggerCurSkillEvent`, `TriggerEvent`, `TriggerStringEvent`, `UTSkillEventType`
- **自定义自己的技能Action节点** (id:183)
  - API: `Action开始执行调用`, `Action每一帧调用`, `GetOwnerPawn`, `OnRealDoAction`, `OnReset`, `OnUpdateAction`
- **Buff简介** (id:195)
  - API: `AActor`, `AController`, `AddBuff`, `FName`, `NeedSimulateToClient`, `PlayerPawn`
- **自定义自己的BuffAction** (id:196)
  - API: `LuaDoAction`, `LuaResetAction`, `LuaUndoAction`, `LuaUpdateAction`
- **技能编辑器节点查询** (id:259)
- **技能抛体** (id:20075)
  - API: `CastSkill`, `NewProj`, `NewSkill`
- **技能Task查询手册** (id:20094)
  - API: `AUniversalProjectileCore`, `Anim3DTransformWarpingTargetType_Custom`, `Anim3DTransformWarpingTargetType_SelectTarget`, `Anim3DTransformWarpingTargetType_SelectTransform`, `AnimListComp`, `InitTask_BP`, `Interval`, `None`
- **状态互斥** (id:20106)
  - API: `Action`, `Add`, `AllowDynamicState`, `DA_UGCTagMappingTemplate`, `DynamicStateInterruptedHandle`, `DynamicStateTagRelationshipMapping`, `EnterDynamicState`, `GetOwnerActor`
- **技能属性绑定** (id:20108)
  - API: `CastSkill`, `Getter`, `Indicator`, `PESkillTask_StateBranch`, `Radius`, `Setter`
- **被动技能** (id:20110)
  - API: `BP_PoisonGas`, `ECA配置`, `OnMerge_BP`
- **技能Condition查询手册** (id:20111)
  - API: `LuaFunction`
- **技能Event查询手册** (id:20112)
- **技能调试工具** (id:20114)
  - API: `RemoveBuffByClass`, `RemoveSkillInstance`
- **BuffAction查询手册** (id:20117)
  - API: `None`
- **技能状态图** (id:20152)
- **法术场** (id:20217)
  - API: `Actor类型`, `CheckType`, `OverlapAllDynamic`, `OverlapCheckArea`
- **变参Buff模板** (id:20253)
  - API: `ABP_TransformPreset_Chicken`

### 怪物系统

- **框架介绍** (id:168)
- **寻路网格烘焙以及组件配置** (id:169)
  - API: `ComponentManager`, `DataManager`, `ESS_MonsterCrowdMove`, `ESS_Navigation`, `GameMode`, `Navigation`
- **新建怪物蓝图并配置动画** (id:170)
  - API: `CapsuleHalfHeight`, `CapsuleRadius`, `MoveSpeed`, `UAEMonsterAnimList`
- **让怪物移动起来** (id:171)
  - API: `AIController`, `BaseClass`, `GetBehaviorTreeObjectPath`, `OnPossess`, `RunBehaviorTree`, `SuperClass.OnPossess`, `Target`, `UE.LoadObject`
- **让怪物释放技能进行攻击** (id:172)
  - API: `Actor`, `SelfActor`
- **常用参数和接口详解** (id:173)
- **附件工程** (id:174)
- **行为树基本概念** (id:175)
- **使用导航网格NavMesh** (id:177)
- **利用和平的角色拓展玩法内容** (id:179)
  - API: `AIPlayerKey`, `UGCFakePlayerSystem`, `UGCFakePlayerSystem.GetRandomAIPlayerKey`, `UGCFakePlayerSystem.SpawnFakePlayer`
- **引擎** (id:252)
- **引擎** (id:253)
- **和平** (id:254)
- **引擎** (id:255)
- **和平** (id:256)
- **引擎** (id:257)
- **和平** (id:258)
- **自定义节点** (id:358)
- **怪物动画蓝图复用功能** (id:20017)
  - API: `BP_Magic_Master`
- **怪物快速配置指南** (id:20144)
  - API: `AIWorldVolume`, `AttrModifyComp`, `BehaviorControlComp`, `Filter`, `GetEntityTypeTag`, `LogicPartManagerComp`, `PESkill_Monster_Claw`, `PersistBaseComponent`
- **怪物血条** (id:20145)
  - API: `BP_CharacterHPChange`, `BP_CharacterNameChange`, `DA_GameModeGeneral`, `Event_InitParamEnd`, `FName`, `UGCGenericCharacterPositionWidget`, `UGC_BOSS_Generic_HealthBar_UIBP`, `UGC_NPC_Generic_HealthBar_UIBP`
- **怪物刷新器** (id:20156)
  - API: `Attr`, `AttrItem`, `AttributeName`, `Attributes`, `BP_UGCMobSpawner`, `BP_UGCMobSpawnerManager`, `CustomSpawnMob`, `FinallyMonsterID`
- **怪物调试工具** (id:20161)
- **怪物逻辑管理组件** (id:20162)
  - API: `AIWorldVolume`, `BP_UGCTargetProducer_EnemyHatred`, `BT_UGC_GenericMob_MainTree`, `CalculateHatredValueOfBasic`, `CalculateHatredValueOfDamage`, `LogicPartManagerComp`, `TargetProducer`, `TargetProducer_AllyForHelp`
- **移动与避障** (id:20168)
  - API: `CrowdMove`, `DynamicObstacleAvoidance`, `MoveControlComponent`, `SetAvoidanceGroup`
- **服务节点查询手册** (id:20174)
  - API: `Actor`
- **装饰器节点查询手册** (id:20178)
  - API: `Actor`, `FVector`, `HasTag`, `Vector`
- **任务节点查询手册** (id:20179)
  - API: `Actor`, `OnBehaviorNotify_BP`, `Vector`
- **怪物动画** (id:20251)
  - API: `AnimListComp`, `Death`, `SK_CH_UGC_Elements_Skeleton`, `UGCSimpleMobAnimConfig`, `UGCSimpleMobSharingAnimConfig`
- **路点移动** (id:20254)
  - API: `FollowWaypointPart`, `LogicPartManagerComp`, `STSpawnerWayPoint`, `SpawnConfig`, `StopRadiusScale`, `UGC怪物MOBA小怪巡逻行为树`, `UGC怪物行为树`, `WayPointArr`
- **修改怪物模型** (id:20255)
  - API: `ColorTint`, `M_UGC_Character`, `Master_UGC_Mask_Base`, `Material`, `Parent`, `Texture`
- **导航网格** (id:20266)
  - API: `DataManager`, `ESS_MonsterCrowdMove`, `ESS_Navigation`, `NavMeshVolume`, `UGCGameMode`
- **动态更新导航网格** (id:20274)
  - API: `Add`, `AddDynamicNavAffect`, `AgentName`, `AsyncBuildNavmesh`, `AsyncIncrementalBuild`, `FName`, `Fbox`, `FinishedDelegate`
- **无骨骼怪物模板** (id:20285)
  - API: `CustomRotatingMovement`, `SpawnGenericCharacter`, `StaticMesh`
- **丧尸法师案例** (id:20323)
  - API: `BehaviorControlComp`, `CastSkill`, `K2_SetActorLocation`, `LogicPartManagerComp`, `MoveControlComp`, `OverlapCheckArea`, `PESkillTargetPickerBase`, `PersistClientStateComponent`

### 属性与伤害

- **通用属性系统** (id:20098)
  - API: `AttrModifyComp`, `AttributeOwnerActor`, `FGameMagnitudeContext`, `GetEndurance_Override`, `TestAttribute`, `UGCAttributeGroup_Character`, `UGCAttributeSystem`, `UGCAttributeSystem.GetGameAttributeValue`
- **全局伤害公式** (id:20099)
  - API: `Add`, `Context`, `DamageContext`, `ExtraResult`, `GetCalculationResult`, `GetDamageTagsFromContext`, `GetDamageTypeFromContext`, `GetSourceMagnitudeFromContext`
- **属性修改器** (id:20153)
- **枪械属性对照表** (id:20159)
  - API: `UGC全自动射击间隔`, `UGC切枪时间影响因子`, `UGC后坐力影响因子`, `UGC后坐力影响因子RecoilFactorWrapper`, `UGC子弹基础伤害`, `UGC弹匣容量`, `UGC换弹时间影响因子`, `UGC连发子弹间隔`
- **受击数据资产** (id:20169)
- **角色属性与状态** (id:20205)
  - API: `AdditiveSpeedValueWrapper`
- **全局治疗公式** (id:20216)
  - API: `Add`, `Context`, `ExtraResult`, `GetCalculationResult`, `GetDamageTagsFromContext`, `GetSourceMagnitudeFromContext`, `GetVictimFromContext`, `RecoverGenericCharacterHealth`
- **载具属性对照表** (id:20246)

### 物资系统

- **概述** (id:185)
  - API: `SkillConfig`, `SkillTriggerEvent`
- **创建新的药品** (id:186)
  - API: `ActionWithConditions条件Action`, `Equippable`, `SkillArchetypes`, `SkillEntryConfigs`, `StaticMesh`, `UAESkillManager`
- **枪械物资** (id:187)
  - API: `BP_Rifle_M416`, `CrossHair`, `CrossHairData`, `HUDOwner`, `IsSpreadEnable`, `OnWeaponDrawHUDDelegate`, `PartDamage`, `ShootWeaponEntity`
- **投掷物物资** (id:188)
  - API: `BP_Grenade_Shoulei_Weapon`, `BP_ThrowComponent`, `EffectScale`, `EliteProjectile`, `ItemHandle`, `PickupWrapper`, `ProjGrenade_BP`, `ProjectileMesh`
- **为玩家添加初始道具** (id:193)
  - API: `AddItem`, `GetPlayerCharacterSafety`, `HasAuthority`, `KismetSystemLibrary.K2_SetTimerDelegateForLua`, `ObjectExtend.CreateDelegate`, `ReceiveBeginPlay`, `ReceiveEndPlay`, `ReceiveTick`
- **物资刷新示例** (id:194)
  - API: `AddConcomitants`, `AddItem`, `AddItemGroup`, `DropItemConfig`, `DropItemConfig.GetDropItems`, `DropItemGroup`, `HasAuthority`, `K2_DestroyActor`
- **物品编辑器** (id:20101)
  - API: `AddBuffByClass`, `AddItem`, `AddItemByDefineIDV2`, `AddItemV2`, `Asset`, `BP_UGC_MachineGun_P90`, `BP_UGC_MeleeWeap_Machete`, `CanUseItemV2`
- **自定义枪械** (id:20103)
  - API: `BulletTemplate`, `Loop`, `M416`, `OverrideHitEffectDataAsset`, `ShootWeaponEntity`, `State`
- **背包系统** (id:20104)
  - API: `AddCellCapacity`, `AddMaxCellCapacity`, `AsyncLoadObjectBySoftPath`, `BP_BackpackComponentV2`, `BP_BackpackComponentV2_Custom`, `BP_BackpackUIComponentV2`, `BP_BackpackUIComponentV2_Custom`, `BP_BackpackUIComponentV2_Custom.CompareQuantity`
- **物资刷新器** (id:20155)
  - API: `BP_UGCItemSpawner`, `CustomID`, `EventName`, `Lua脚本`, `M16A4`, `NewPointManager`, `TestSpawn`, `UGCDrop`
- **自定义投掷物** (id:20157)
  - API: `P_White_Smoke_02`, `Smoking`, `Spine`
- **自定义近战武器** (id:20158)
- **物品与背包槽位** (id:20210)
  - API: `EquipmentSlot`, `GetEquipSlotEnable`, `Lock`, `SetEquipSlotEnable`
- **自定义物品模型** (id:20212)
  - API: `Root`, `WeaponSocket_01`

### 角色系统

- **角色出生点** (id:362)
  - API: `BP_PlayerStartManager`, `BP_STPlayerStart`, `ComponentManager`, `DebugPlayerSettings`, `FindPlayerStartByBornPointID`, `GetUGCModePlayerStart`, `HasAuthority`, `IsMarkOccupied`
- **队伍与阵营** (id:20095)
  - API: `Camp`, `ChangePlayerTeamID`, `DA_GameModeGeneral`, `PlayerBornPointID`, `SetCampForActor`, `SetCampForTeam`, `UGCPlayerPawn`
- **物品掉落与保留** (id:20148)
  - API: `DA_GameModeGeneral`, `IsSkipSpawnDeadTombBox`, `UGCPlayerPawn`
- **角色Avatar复制** (id:20228)

### 通用功能

- **通用掉落表** (id:20058)
  - API: `AddVector`, `DropItems`, `K2_GetActorLocation`, `StartCustomizeDrop`, `UGCDropActor_BP`, `UGCGameSystem`, `UGCGameSystem.GetPlayerPawnByPlayerController`, `UGCItemSystemV2`
- **GamePart模块化** (id:20090)
  - API: `AUGCGamePartGlobalActor`, `Add`, `AddItemResultDelegate`, `CommodityOperationManager`, `DA_GameModeGeneral`, `GP_CommodityOperationManager`, `GamePartName`, `GetAllProductData`
- **通用掉落组件** (id:20142)
  - API: `OnComponentBeginOverlap`, `StartDrop`, `StartDropByProduceID`, `Wrapper`
- **通用运动组件** (id:20150)
  - API: `Asset`, `PauseMotion`, `ResetMotion`, `ServerRPC_TestUGCMotion`, `StartMotion`, `UGCActorComponentUtility`, `UGCActorComponentUtility.GetAllActorsOfClass`, `UGCGameSystem`
- **通用消息系统** (id:20163)
  - API: `BroadcastUserDefinedGlobalMessage`, `BroadcastUserDefinedObjectMessage`, `Callback`, `FName`, `GoldUI`, `HandleDamage`, `ListenGlobalMessage`, `ListenID`
- **通用抛体** (id:20165)
  - API: `AUniversalProjectileCore`, `ApplyActionEffect`, `Asset`, `CreateProjectile`, `GetActorForwardVector`, `GetPlayerCharacterSafety`, `InitBP`, `K2_GetActorLocation`
- **表格管理器** (id:20208)
- **通用过滤器** (id:20218)
- **实体类型** (id:20298)
  - API: `CommonEntityTypeConfigDataAsset`, `EntityType`
- **Tween功能** (id:20351)
  - API: `Actor`, `AnimatedWidget`, `BindCompletedDelegate`, `Callback`, `ChainTween`, `Config`, `Construct`, `Delay`

### 多人PVE模板

- **概览** (id:20190)
- **模式配置（单人PVE模式）** (id:20191)
- **模式配置（多人PVE模式）** (id:20192)
- **怪物刷新** (id:20193)
- **物品刷新** (id:20194)
- **战斗内商店** (id:20195)
- **关卡管理** (id:20196)
  - API: `Actor`, `Add`, `AllPlayer`, `Asset`, `Beginplay`, `CallReset`, `CallSettle`, `CallShop`
- **游戏大厅系统** (id:20197)
- **角色系统** (id:20198)
- **天赋系统** (id:20371)
- **装备随机词条** (id:20372)
  - API: `UGCAffixDetails`, `UGCEquippmentRandomAffix`, `UGCItemMapAffixId`
- **怪物配置** (id:20375)

### UI系统

- **UMG Lua的结构** (id:199)
  - API: `ReceiveTick`
- **创建3D UI** (id:201)
- **富文本框** (id:202)
- **和平主界面控件** (id:250)
- **和平全局观战界面控件** (id:251)
- **快速入门** (id:347)
  - API: `Asset`, `Blueprint`
- **异形屏适配** (id:357)
- **和平主界面控件布局** (id:20019)
  - API: `AddToSlot`, `SetWidgetLayout`, `UGCWidgetManagerSystem`, `WidgetLayout`
- **和平控件锚点** (id:20097)
  - API: `AddToSlot`
- **通用屏幕指示器** (id:20295)
  - API: `ActorMark`, `Event_InitParam`, `InDistanPanel`, `ObjectPositionWidget`, `SetStateWidgetPanel`, `UTextBlock`, `UWidget`
- **技能元件** (id:20325)
  - API: `Construct`, `IsSkillEnable`, `OnSkillBound_BP`, `PlayerPawn`, `SuperClass.InitCDProgress`, `SuperClass.OnSkillBound_BP`, `UE.IsValid`
- **头像框组件** (id:20365)
- **强引导组件** (id:20383)
  - API: `Border`, `Border_0`, `ButtonBP`, `CanvasPanel_0`, `GameState`, `Image_2`, `ItemBP`, `SelfHitTestInvisible`
- **通用进度条UI** (id:20392)
  - API: `SetPercent`, `UGCPlayerController`

## 2. 关键API参考


### 技能系统API

- `AActor` — Buff简介
- `ABP_TransformPreset_Chicken` — 变参Buff模板
- `AController` — Buff简介
- `AUniversalProjectileCore` — 技能Task查询手册
- `Action` — 状态互斥
- `Action开始执行调用` — 自定义自己的技能Action节点
- `Action每一帧调用` — 自定义自己的技能Action节点
- `Actor类型` — 法术场
- `AddBuff` — Buff简介
- `Add` — 状态互斥
- `AllowDynamicState` — 状态互斥
- `Anim3DTransformWarpingTargetType_Custom` — 技能Task查询手册
- `Anim3DTransformWarpingTargetType_SelectTarget` — 技能Task查询手册
- `Anim3DTransformWarpingTargetType_SelectTransform` — 技能Task查询手册
- `AnimListComp` — 技能Task查询手册
- `BP_PoisonGas` — 被动技能
- `CastSkill` — 技能属性绑定
- `CastSkill` — 技能抛体
- `CheckType` — 法术场
- `DA_UGCTagMappingTemplate` — 状态互斥
- `DynamicStateInterruptedHandle` — 状态互斥
- `DynamicStateTagRelationshipMapping` — 状态互斥
- `ECA配置` — 被动技能
- `EnterDynamicState` — 状态互斥
- `EventEffectMapForEditor` — 新建技能阶段，新建技能Action
- `FName` — Buff简介
- `GameState` — 快速入门
- `GetCurSkillIndex` — 新建技能阶段，新建技能Action
- `GetOwnerActor` — 状态互斥
- `GetOwnerPawn` — 自定义自己的技能Action节点
- ...共94条

### 怪物/AI系统API

- `AIController` — 让怪物移动起来
- `AIPlayerKey` — 利用和平的角色拓展玩法内容
- `AIWorldVolume` — 怪物快速配置指南
- `AIWorldVolume` — 怪物逻辑管理组件
- `Actor` — 任务节点查询手册
- `Actor` — 服务节点查询手册
- `Actor` — 装饰器节点查询手册
- `Actor` — 让怪物释放技能进行攻击
- `AddDynamicNavAffect` — 动态更新导航网格
- `Add` — 动态更新导航网格
- `AgentName` — 动态更新导航网格
- `AnimListComp` — 怪物动画
- `AsyncBuildNavmesh` — 动态更新导航网格
- `AsyncIncrementalBuild` — 动态更新导航网格
- `AttrItem` — 怪物刷新器
- `AttrModifyComp` — 怪物快速配置指南
- `Attr` — 怪物刷新器
- `AttributeName` — 怪物刷新器
- `Attributes` — 怪物刷新器
- `BP_CharacterHPChange` — 怪物血条
- `BP_CharacterNameChange` — 怪物血条
- `BP_Magic_Master` — 怪物动画蓝图复用功能
- `BP_UGCMobSpawnerManager` — 怪物刷新器
- `BP_UGCMobSpawner` — 怪物刷新器
- `BP_UGCTargetProducer_EnemyHatred` — 怪物逻辑管理组件
- `BT_UGC_GenericMob_MainTree` — 怪物逻辑管理组件
- `BaseClass` — 让怪物移动起来
- `BehaviorControlComp` — 丧尸法师案例
- `BehaviorControlComp` — 怪物快速配置指南
- `CalculateHatredValueOfBasic` — 怪物逻辑管理组件
- ...共155条

### 属性与伤害API

- `Add` — 全局伤害公式
- `Add` — 全局治疗公式
- `AdditiveSpeedValueWrapper` — 角色属性与状态
- `AttrModifyComp` — 通用属性系统
- `AttributeOwnerActor` — 通用属性系统
- `Context` — 全局伤害公式
- `Context` — 全局治疗公式
- `DamageContext` — 全局伤害公式
- `ExtraResult` — 全局伤害公式
- `ExtraResult` — 全局治疗公式
- `FGameMagnitudeContext` — 通用属性系统
- `GetCalculationResult` — 全局伤害公式
- `GetCalculationResult` — 全局治疗公式
- `GetDamageTagsFromContext` — 全局伤害公式
- `GetDamageTagsFromContext` — 全局治疗公式
- `GetDamageTypeFromContext` — 全局伤害公式
- `GetEndurance_Override` — 通用属性系统
- `GetSourceMagnitudeFromContext` — 全局伤害公式
- `GetSourceMagnitudeFromContext` — 全局治疗公式
- `GetVictimFromContext` — 全局伤害公式
- `GetVictimFromContext` — 全局治疗公式
- `RecoverGenericCharacterHealth` — 全局治疗公式
- `TestAttribute` — 通用属性系统
- `UGCAttributeGroup_Character` — 通用属性系统
- `UGCAttributeSystem.GetDamageTagsFromContext` — 全局伤害公式
- `UGCAttributeSystem.GetDamageTagsFromContext` — 全局治疗公式
- `UGCAttributeSystem.GetDamageTypeFromContext` — 全局伤害公式
- `UGCAttributeSystem.GetGameAttributeValue` — 通用属性系统
- `UGCAttributeSystem` — 全局伤害公式
- `UGCAttributeSystem` — 全局治疗公式
- ...共55条

### 物品与背包API

- `ActionWithConditions条件Action` — 创建新的药品
- `AddBuffByClass` — 物品编辑器
- `AddCellCapacity` — 背包系统
- `AddConcomitants` — 物资刷新示例
- `AddItemByDefineIDV2` — 物品编辑器
- `AddItemGroup` — 物资刷新示例
- `AddItemV2` — 物品编辑器
- `AddItem` — 为玩家添加初始道具
- `AddItem` — 物品编辑器
- `AddItem` — 物资刷新示例
- `AddMaxCellCapacity` — 背包系统
- `Asset` — 物品编辑器
- `AsyncLoadObjectBySoftPath` — 背包系统
- `BP_BackpackComponentV2_Custom` — 背包系统
- `BP_BackpackComponentV2` — 背包系统
- `BP_BackpackUIComponentV2_Custom.CompareQuantity` — 背包系统
- `BP_BackpackUIComponentV2_Custom` — 背包系统
- `BP_BackpackUIComponentV2` — 背包系统
- `BP_Grenade_Shoulei_Weapon` — 投掷物物资
- `BP_Grid_Tag` — 背包系统
- `BP_Rifle_M416` — 枪械物资
- `BP_ThrowComponent` — 投掷物物资
- `BP_UGCItemSpawner` — 物资刷新器
- `BP_UGC_MachineGun_P90` — 物品编辑器
- `BP_UGC_MeleeWeap_Machete` — 物品编辑器
- `BackpackUIComponent.CompareQuality` — 背包系统
- `BulletTemplate` — 自定义枪械
- `CanUseItemV2` — 物品编辑器
- `CheckCustomItem` — 背包系统
- `CheckUseItem` — 背包系统
- ...共149条

### UI系统API

- `ActorMark` — 通用屏幕指示器
- `AddToSlot` — 和平主界面控件布局
- `AddToSlot` — 和平控件锚点
- `Asset` — 快速入门
- `Blueprint` — 快速入门
- `Border_0` — 强引导组件
- `Border` — 强引导组件
- `ButtonBP` — 强引导组件
- `CanvasPanel_0` — 强引导组件
- `Construct` — 技能元件
- `Event_InitParam` — 通用屏幕指示器
- `GameState` — 强引导组件
- `Image_2` — 强引导组件
- `InDistanPanel` — 通用屏幕指示器
- `IsSkillEnable` — 技能元件
- `ItemBP` — 强引导组件
- `ObjectPositionWidget` — 通用屏幕指示器
- `OnSkillBound_BP` — 技能元件
- `PlayerPawn` — 技能元件
- `ReceiveTick` — UMG Lua的结构
- `SelfHitTestInvisible` — 强引导组件
- `SetPercent` — 通用进度条UI
- `SetStateWidgetPanel` — 通用屏幕指示器
- `SetWidgetLayout` — 和平主界面控件布局
- `SizeBox_0` — 强引导组件
- `SuperClass.InitCDProgress` — 技能元件
- `SuperClass.OnSkillBound_BP` — 技能元件
- `UE.IsValid` — 技能元件
- `UGCPlayerController` — 通用进度条UI
- `UGCWidgetManagerSystem` — 和平主界面控件布局
- ...共35条

### 通用功能API

- `AUGCGamePartGlobalActor` — GamePart模块化
- `AUniversalProjectileCore` — 通用抛体
- `Actor` — Tween功能
- `AddItemResultDelegate` — GamePart模块化
- `AddVector` — 通用掉落表
- `Add` — GamePart模块化
- `AnimatedWidget` — Tween功能
- `ApplyActionEffect` — 通用抛体
- `Asset` — 通用抛体
- `Asset` — 通用运动组件
- `BindCompletedDelegate` — Tween功能
- `BroadcastUserDefinedGlobalMessage` — 通用消息系统
- `BroadcastUserDefinedObjectMessage` — 通用消息系统
- `Callback` — Tween功能
- `Callback` — 通用消息系统
- `ChainTween` — Tween功能
- `CommodityOperationManager` — GamePart模块化
- `CommonEntityTypeConfigDataAsset` — 实体类型
- `Config` — Tween功能
- `Construct` — Tween功能
- `CreateProjectile` — 通用抛体
- `DA_GameModeGeneral` — GamePart模块化
- `Delay` — Tween功能
- `DropItems` — 通用掉落表
- `Duration` — Tween功能
- `Easing` — Tween功能
- `EntityType` — 实体类型
- `FName` — 通用消息系统
- `FTweenHandle` — Tween功能
- `FUnrealTweenConfig` — Tween功能
- ...共155条

## 3. 常用代码模式


### 技能系统


#### 快速入门

```lua
--获取技能管理器
local SkillManager = self:GetSkillManagerComponent()
if SkillManager ~= nil then
	--释放120号技能
	SkillManager:TriggerEvent(120, UTSkillEventType.SET_KEY_DOWN)
end
```


#### 新建技能阶段，新建技能Action

```lua
--获取技能管理器
local SkillManager = self:GetSkillManagerComponent()
if SkillManager ~= nil then
	--获得当前正在运行的技能的Index
	local SkillIndex = SkillManager:GetCurSkillIndex()
	--向此技能发送SkillCancel事件
	SkillManager:TriggerEvent(SkillIndex, UTSkillEventType.SET_SKILL_CANCEL)
end
```

```lua
--获取技能管理器
local SkillManager = PlayerPawn:GetSkillManagerComponent()
if SkillManager ~= nil then
	--获得当前正在运行的技能的Index
	local SkillIndex = SkillManager:GetCurSkillIndex()
	--向此技能发送自定义事件
	SkillManager:TriggerStringEvent(SkillID, “MySkillEvent”)
end
```


#### 自定义自己的技能Action节点

```lua
--技能执行完毕调用
function mySkillAction:OnReset()
    print("mySkillAction:OnReset")
    return true
end

--Action每一帧调用
function mySkillAction:OnUpdateAction(DeltaSeconds)
    print("mySkillAction:OnUpdateAction")
    return true
end

--Action开始执行调用
function mySkillAction:OnRealDoAction()
    print("mySkillAction:OnRealDoAction")
    return true
end
```

```lua
--获取技能释放者Pawn
--进而获取PlayerKey
--其他定义在Pawn的属性也可以获取
local SkillPawn = self:GetOwnerPawn()
print(SkillPawn.PlayerKey)
```


#### 技能Task查询手册

```lua
local TestCustomLua = {}

-- 该Task初始化时调用,即Task获取到SkillOwner,即该Task所属Section触发时调用
function TestCustomLua:InitTask_BP()
end

-- 该Task是否支持RPC
function TestCustomLua:TaskSupportRPC_BP()
  return false
end

-- 当该Task被激活时调用
function TestCustomLua:OnActivate_BP()
end

-- 当该Task被反激活时调用
function TestCustomLua:OnDeactivate_BP()
end

-- 当该Task被Trigger时调用，Trigger的间隔由Task配置的间隔决定
function TestCustomLua:OnTrigger_BP(Delta)
end
```


#### Buff简介

```lua
--判断是否拥有此Buff
HasBuff:fun(BuffName:FName):bool

--移除Buff，可指定只移除层数
RemoveBuff:fun(BuffName:FName,RemoveLayerOnly:bool,BuffApplierActor:AActor):bool

--添加Buff，可指定来源以及添加层数
AddBuff:fun(BuffName:FName,BuffCauser:AController,LayerCount:int32,BuffApplierActor:AActor,CauserActor:AActor):int32
```

```lua
PlayerPawn:AddBuff("MyBuff", nil, 1, nil, nil)
```


### 怪物系统


#### 怪物快速配置指南

```lua
-- 设置实体类型标签
local EntityTypeTag = UGCGameplayTagSystem.RequestGameplayTag("LogicPart.Filter.EntityType.Melee")
MonsterObject:SetEntityTypeTag(EntityTypeTag)

-- 查询实体类型标签
local TagInfo = MonsterObject:GetEntityTypeTag()
ugcprint(string.format("Monster Entity Type: %s", TagInfo.TagName))
```


#### 怪物血条

```lua
---@class WBP_Custom1_C:UGCGenericCharacterPositionWidget
local WBP_Custom1 = { bInitDoOnce = false } 

-- 角色的名字发生变化
---@param Name FName 变化后的名字
function WBP_Custom1:BP_CharacterNameChange(Name)
    ugcprint(self.OwnerCharacter)
end

-- 角色的血量发生变化
---@param InHPCurrent float 变化后的血量
---@param InHPMax float 变化后的血量上限
function WBP_Custom1:BP_CharacterHPChange(InHPCurrent,InHPMax)
    
end

-- 初始化参数结束
function WBP_Custom1:Event_InitParamEnd()
    
end

return WBP_Custom1
```


#### 动态更新导航网格

```lua
local min  = UGCMathUtility.MakeVector(18610.0,21590.0,0)
 local max  = UGCMathUtility.MakeVector(20660.0,22530.0,520.0)
 local Fbox = UGCMathUtility.MakeBox(min,max)
 UGCNavigationSystem.AddDynamicNavAffect(self, "Mannequin", Fbox)
```

```lua
---生效范围：服务器
---@param WorldContext UObject 当前世界上下文
---@param AgentName FName 作用Agent的寻路图名称一般为"Mannequin"
UGCNavigationSystem.AsyncIncrementalBuild(self, "Mannequin")
```


#### 怪物刷新器

```lua
-- 从怪物路径配置表中获取蓝图类
function MonsterSpawner:GetMonsterClass(MonsterID, MonsterType)
    print("MonsterSpawner:GetMonsterClass")
    local FinallyMonsterID = -1
    if MonsterType == "LittleMonster" then
        FinallyMonsterID = tonumber(tostring(10)..MonsterID)
    end

    if MonsterType == "EliteMonster" then
        FinallyMonsterID = tonumber(tostring(20)..MonsterID)
    end

    if MonsterType == "Boss" then
        FinallyMonsterID = tonumber(tostring(30)..MonsterID)
    end

    local MonsterPathTable = UGCGameSystem.GetTableData("Data/Table/MonsterPathTable")
    if not MonsterPathTable then
        print("MonsterSpawner:GetMonsterClass1")
        return nil
    end

    for _, value in pairs(MonsterPathTable) do
        print("MonsterSpawner:GetMonsterClass"..value.MonsterID)
        if value.MonsterID == FinallyMonsterID then
						return UGCObjectUtility.LoadObjectBySoftPath(value.MonsterPath)
				end
		end
		
    return nil
end

-- 从怪物详情配置表中查找怪物属性配置
function MonsterSpawner:GetMonsterAttributes(MonsterID, MonsterType)
    print("MonsterSpawner:GetMonsterAttributes")
    local FinallyMonsterID = -1
    if MonsterType == "LittleMonster" then
        FinallyMonsterID = tonumber(tostring(10)..MonsterID)
    end

    if MonsterType == "EliteMonster" then
        FinallyMonsterID = tonumber(tostring(20)..MonsterID)
    end

    if MonsterType == "Boss" then
        FinallyMonsterID = tonumber(tostring(30)..MonsterID)
    end

    local MonsterAttributeTable = UGCGameSystem.GetTableData("Data/Table/MonsterAttributeTable")
    if not MonsterAttributeTable then
        return nil
    end

    print("MonsterSpawner:GetMonsterAttributes1")
    for _, value in pairs(MonsterAttributeTable) do
        print("MonsterSpawner:GetMonsterAttributes"..value.MonsterID..FinallyMonsterID)
        if value.MonsterID == FinallyMonsterID then
        		print("MonsterSpawner:GetMonsterAttributes2")
        		return value.Attributes
    		end
		end

    return nil
end


function MonsterSpawner:CustomSpawnMob(InCustomParam)
    print("MonsterSpawner:CustomSpawnMob")
    -- 查找怪物蓝图路径
    local MonsterClass = self:GetMonsterClass(InCustomParam.MonsterID, InCustomParam.MonsterType)
    if not MonsterClass then
        return nil
    end

    local SpawnedMonster = self:SpawnMob(MonsterClass)

    -- 查找怪物属性配置
    local MonsterAttributes = self:GetMonsterAttributes(InCustomParam.MonsterID, InCustomParam.MonsterType)
    if not MonsterAttributes then
        return SpawnedMonster
    end

    -- 初始化怪物属性
    self:InitMonsterAttr(SpawnedMonster, MonsterAttributes)

		--对于自定义方法进行刷怪，在使用路点移动时，需要手动调用
		--黑板设置使用路点值
  	UGCGenericCharacterSystem.GetBlackboard(SpawnedMonster):SetValueAsBool("bUsePathPoint",true)
		
		--获取路点Location信息
    self.WaypointsLocation={}
    for index, pointActor in pairs(self.STSpawnerWaypoint.WayPointArr) do
        self.WaypointsLocation[index] = pointActor:K2_GetActorLocation()
    end
		
		--把路点信息传递给刷出的怪
    SpawnedMonster:GetLogicPartManagerInterface():GetFollowWayPointPartInterface():SetWaypoints(self.WaypointsLocation,true)
		
    return SpawnedMonster
end


-- 初始化怪物的指定属性值
function MonsterSpawner:InitMonsterAttr(Monster, Attributes)
    print("MonsterSpawner:InitMonsterAttr")
    if not Monster then
        return
    end

    for _, AttrItem in pairs(Attributes) do
        UGCAttributeSystem.SetGameAttributeValue(Monster, AttrItem.Attr.AttributeName, AttrItem.Value)
    end
end
```


#### 让怪物移动起来

```lua
local MyAIC = {}; 

function MyAIC:GetBehaviorTreeObjectPath()
    return string.format('%sAsset/Blueprint/MyBT.MyBT', UGCMapInfoLib.GetRootLongPackagePath())
end

function MyAIC:OnPossess()
    self.SuperClass.OnPossess(self)

    self:RunBehaviorTree(UE.LoadObject(self:GetBehaviorTreeObjectPath()))
end

return MyAIC;
```


### 通用功能


#### GamePart模块化

```lua
-- 获取GamePartGlobalActor的实例对象
local GamePartActorInstance = UGCGamePartSystem.GetGamePartGlobalActor("CommodityOperationManager");

-- 调用模块GamePart接口获取商品配置信息
local CommodityConfigData = GamePartActorInstance:GetAllProductData();
log_tree(CommodityConfigData)
```

```lua
function UGCGameState:ReceiveBeginPlay()
		local GamePartActorInstance = UGCGamePartSystem.GetGamePartGlobalActor("VirtualItemManager");
  	if GamePartActorInstance then
    		GamePartActorInstance.AddItemResultDelegate:Add(self.OnAddVirtualItemResult, self)
  	else
    		UGCGenericMessageSystem.ListenGlobalMessage(self, UGCGenericMessageSystem.Messages.UGC.GamePart.GamePartLoaded, self, self.OnGamePartLoaded)
  	end
end

function UGCGameState:OnGamePartLoaded(GamePartName)
    if GamePartName == 'VirtualItemManager' then
        local GamePartActorInstance = UGCGamePartSystem.GetGamePartGlobalActor("VirtualItemManager");
        GamePartActorInstance.AddItemResultDelegate:Add(self.OnAddVirtualItemResult, self);
    end
end

function UGCGameState:OnAddVirtualItemResult()
	-- 当获得虚拟物品时执行的逻辑
end
```


#### 通用掉落表

```lua
local CurrentPlayerPawn = UGCGameSystem.GetPlayerPawnByPlayerController(self)
local CurrentLocation = CurrentPlayerPawn:K2_GetActorLocation()
local DropLocation = UGCMathUtility.AddVector(CurrentLocation, Vector.New(200,0,0))
UGCItemSystemV2.StartCustomizeDrop(DropLocation, DropID, -1, EUGCGenerateItemEntityType.GenerateItemEntity_WrapperActor, CurrentPlayerPawn)
```


#### 通用抛体

```lua
local ProjectileClass = UGCObjectUtility.LoadClass(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Prefabs/Projectiles/Proj_Poison.Proj_Poison_C'))
local PlayerPawn = self:GetPlayerCharacterSafety()
local SelfPosition = PlayerPawn:K2_GetActorLocation()
local PlayerDirection = PlayerPawn:GetActorForwardVector()

local LaunchPosition = Vector.New(SelfPosition.X, SelfPosition.Y + 300, SelfPosition.Z + 100)
UGCProjectileSystemV2.CreateProjectile(ProjectileClass, self, LaunchPosition, PlayerDirection, 2000, 1, 20, ERestrictedDamageType.SkillDamage)
```


#### 通用运动组件

```lua
function UGCPlayerController:ServerRPC_TestUGCMotion(TestType, MotionIndex)
    --调用测试函数ServerRPC_TestUGCMotion，传入运动器当前状态TestType和运动器id MotionIndex
    
    local UGCMotionTestActorClassPath = UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Cube_Blueprint.Cube_Blueprint_C')
		--获取添加了运动器组件的Cube_Blueprint组件的完整路径，赋值给UGCMotionTestActorClassPath
		
    local UGCMotionTestActorClass = UGCObjectUtility.LoadClass(UGCMotionTestActorClassPath)
    --创建一个运动对象的类 UGCMotionTestClass，获取赋值给UGCMotionTestActorClassPath的完整路径

		---@type Cube_Blueprint_C[]
    local UGCMotionTestActorList = UGCActorComponentUtility.GetAllActorsOfClass(self, UGCMotionTestActorClass)
    --获取场景中所有根据UGCMotionTestClass类创建出来的对象
    
    for _, MotionActor in pairs(UGCMotionTestActorList) do
        --遍历场景中所有的运动对象
        local UGCMotionComp = MotionActor.UGCMotion
        --获取每个运动对象的运动组件实例
				UGCMotionComp:StartMotion(MotionIndex)
				--调用运动组件实例的方法
    end
end
```

```lua
function UGCPlayerController:ServerRPC_TestUGCMotion(TestType, MotionIndex)
    --调用测试函数ServerRPC_TestUGCMotion，传入运动器当前状态TestType和运动器id MotionIndex
    
    local UGCMotionTestActorClassPath = UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Cube_Blueprint.Cube_Blueprint_C')
		--获取添加了运动器组件的Cube_Blueprint组件的完整路径，赋值给UGCMotionTestActorClassPath
		
    local UGCMotionTestActorClass = UGCObjectUtility.LoadClass(UGCMotionTestActorClassPath)
    --创建一个运动对象的类 UGCMotionTestClass，获取赋值给UGCMotionTestActorClassPath的完整路径

		---@type Cube_Blueprint_C[]
    local UGCMotionTestActorList = UGCActorComponentUtility.GetAllActorsOfClass(self, UGCMotionTestActorClass)
    --获取场景中所有根据UGCMotionTestClass类创建出来的对象
    
    for _, MotionActor in pairs(UGCMotionTestActorList) do
        --遍历场景中所有的运动对象
        local UGCMotionComp = MotionActor.UGCMotion
        --获取每个运动对象的运动组件实例
				UGCMotionComp:PauseMotion(MotionIndex)
				--调用运动组件实例的方法
    end
end
```


#### Tween功能

```lua
Linear,
QuadIn, QuadOut, QuadInOut,
CubicIn, CubicOut, CubicInOut,
QuartIn, QuartOut, QuartInOut,
QuintIn, QuintOut, QuintInOut,
SineIn, SineOut, SineInOut,
ExpoIn, ExpoOut, ExpoInOut,
CircIn, CircOut, CircInOut,
ElasticIn, ElasticOut, ElasticInOut,
BackIn, BackOut, BackInOut,
BounceIn, BounceOut, BounceInOut
```

```lua
local Config = UGCTweenSystem.MakeConfig(0, 1, false, 0)
```


### 属性与伤害


#### 通用属性系统

```lua
-- 获得的耐力值*3
function UGCAttributeGroup_Character:GetEndurance_Override(OriginalValue, AttributeOwnerActor)  
    return OriginalValue * 3  
end  

return UGCAttributeGroup_Character
```

```lua
UGCGameSystem.UGCRequire('Script.GameAttribute.game_attribute_type')

local Hp = UGCAttributeSystem.GetGameAttributeValue(CauserActor, UGCNativeGameAttributeType.Character_Health)
-- 获取血量后的其他逻辑处理
```


#### 属性修改器

```lua
f(X) = 值覆盖修改器 ? 值覆盖修改器 : (X + 加法修改器1 + 加法修改器2...) * (乘法修改器1 + 乘法修改器2...) * 独立乘法修改器1 * 独立乘法修改器2... + 独立加法修改器1 + 独立加法修改器2...
```


#### 全局伤害公式

```lua
local RestrictedDamageType = UGCAttributeSystem.GetDamageTypeFromContext(Context)
local DamageTypeTags = UGCAttributeSystem.GetDamageTagsFromContext(Context)
 
for _, Tag in pairs(DamageTypeTags) do
	if Tag then
		print("[UGCGlobalDamageCalculation] Context Tag: --->"..Tag)
	end
end
```

```lua
local CritTag = UGCGameplayTagSystem.RequestGameplayTag("UGC.Damage.Result.Critical")
if CritTag then
	ExtraResult.ResultTags:Add(CritTag)
end
```


#### 全局治疗公式

```lua
local RecoverTypeTags = UGCAttributeSystem.GetDamageTagsFromContext(Context)
 
for _, Tag in pairs(RecoverTypeTags) do
	if Tag then
		print("[UGCGlobalRecoveryCalculation] Context Tag: --->"..Tag)
	end
end
```

```lua
local CritTag = UGCGameplayTagSystem.RequestGameplayTag("UGC.Damage.Result.Critical")
if CritTag then
	ExtraResult.ResultTags:Add(CritTag)
end
```


## 4. 编辑器操作指南


### 脚本编写

- **游戏结束时的逻辑处理** (id:272)
- **绿洲启元Lua脚本开发指南** (id:346)
- **使用Lua编写玩法功能** (id:351)
- **Actor实例路径使用** (id:20352)

### 调试游戏

- **Lua控制台** (id:224)
- **编辑器Debug调试** (id:307)
- **调试日志说明** (id:354)
- **编辑器联机调试** (id:20033)
- **客户端调试管理器** (id:20042)
- **通用GM面板** (id:20109)
- **战斗日志** (id:20242)

### 模式编辑器

- **通过模式编辑器创建游戏规则** (id:155)
- **模式编辑器Event,Condition,Action** (id:157)
- **使用脚本创建全新的规则** (id:167)

## 5. 性能优化要点

- **使用笔刷创建植被** (id:261)
- **使用同模角色优化性能** (id:263)
- **渲染剔除** (id:264)
- **附件工程** (id:265)
- **网络裁剪** (id:266)
- **异步加载** (id:267)
- **预加载** (id:268)
- **流量优化** (id:269)
- **弱网，断线重连处理** (id:270)
- **性能优化总览** (id:348)
- **场景物件合批** (id:366)
- **防外挂逻辑自检** (id:20309)
- **网络重连机制使用指南** (id:20348)
- **PIE日志面板** (id:20353)
- **性能报告与内存记录** (id:20401)