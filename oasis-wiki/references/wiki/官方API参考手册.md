# 绿洲启元官方API参考手册

> 来源：https://developer.gp.qq.com/api/#/
> 抓取时间：2026-07-10
> 包含：UGC核心类、和平精英类、重要枚举和数据结构
> 统计：57 个类、174 个枚举、0 个结构体、3 个全局函数

## UGC核心类速查

- ASTExtraGameStateBase
- ASTExtraShootWeapon
- AUGCGameModeTDM
- AUGCGenericCharacter
- AUGCItemSpawner
- AUGCMobCharacter
- AUGCMobSpawner
- AUGCPickUpWrapperActor
- BP_UGCPickUpListComponent
- BP_UGCVehicleRefresherTool
- FUGCActivityTask
- FUGCCustomDamageNumberItemParams
- FUGCDamageNumberParams
- FUGCGamePartPlayerComponentConfig
- FUGCGenerateDropItemInfo
- FUGCItemSpawnerInfo
- FUGCItemSpawnerItemConfig
- FUGCItemTransferResult
- FUGCLevelTaskLineConfig
- FUGCMobBTBlackBoardInfo
- FUGCMobBTDebugInfo
- FUGCMobBTDebugTreeElemInfo
- FUGCMobBTDebugTreeInfo
- FUGCMobSpawnerMobConfig
- FUGCPercentTaskAward
- FUGCPercentTaskLineConfig
- FUGCPickupItemData
- FUGCRankingListAwardItem
- FUGCRankingListData
- FUGCSpawnActorNumLimitCfg
- FUGCTaskConfig
- FUGCTaskLineConfig
- FUserActivity
- UGCActivitySystem
- UGCAirAttachSystem
- UGCAirAttackManager
- UGCCharAvatarShowcaseActor
- UGCCommonDragDropItem
- UGCCommonUISystem
- UGCEMPZoneManager
- UGCEMPZoneSystem
- UGCEntityTypeSystem
- UGCGameplayTag
- UGCInputSystem
- UGCMailSystem
- UGCMathUtility
- UGCNavigationSystem
- UGCPlayerPawnSystem
- UGCStringTextUtility
- UGCVehicleSystemV2
- UGC_Backpack_Item_UIBP
- USTExtraGameMagnitudeCalculation
- UUGCBackpackAvatarHandle
- UUGCCommonProduceDropItemComponent
- UUGCGamePartConfig
- UUGCItemWarehouseBase
- UUGCMotionComponent

## 类（Classes）

### AUGCGameModeTDM

团竞游戏模式类

**分类：** Others

**继承：** ABRGameModeTeam_DeathMatch, IUGCGetDynamicConfigInterface


---

### AUGCGenericCharacter

怪物角色类

**分类：** Others

**继承：** AGenericCharacter

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| HealthBarWidgetClass | TSoftClassPtr < UUGCGenericCharacterPositionWidget > | 血条控件蓝图路径 |
| bHealthBarShowWhenOcclusionHide | bool | 被遮挡后血条是否仍显示 |
| HealthBarMaxShowDistance | float | 血条实时显示最大距离，单位厘米 |
| HealthBarLocOffset | FVector | 血条位置偏移 |
| bHealthBarUseSocket | bool | 血条是否附着到特定部位 |
| HealthBarSocketName | FName | 血条附着的部位名 |
| bHealthBarShowWhenTakeDamage | bool | 怪物受伤时显示血条 |
| bHealthBarShowWhenLockPlayer | bool | 当怪物将玩家作为当前目标时显示血条 |
| bHealthBarShowWhenBeAimAt | bool | 当玩家瞄准怪物时显示血条 |
| HealthBarConditionShowDistance | float | 能触发瞄准显示的最大距离 |
| HealthBarShowDuration | float | 血条显示条件触发后显示时间 |
| HealthBarCampFilter | int32 | 阵营过滤 |
| HealthBarDamageFilter | EShowHPBarDamageType | 伤害来源过滤 |

**函数：**

- **GetBlackBoardComponent**() -> UBlackboardComponent *  — 获取黑板组件    生效范围：服务器
- **SetForceHatredTarget**(NewTarget: AActor *) -> void  — 设置当前强制仇恨目标    生效范围：服务器
- **RemoveForceHatredTarget**() -> void  — 清除强制仇恨目标    生效范围：服务器
- **AddTargetHatredValue**(Target: AActor *, HatredValue: float) -> void  — 增加目标仇恨值    生效范围：服务器

---

### AUGCItemSpawner

物资刷新系统：物资刷新器

**分类：** Others

**继承：** AActor

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ItemConfig | FUGCItemSpawnerItemConfig | 配置刷出的物资类别和数量 |
| bNeedSpawnerManager | bool | 物资刷新点是否能独立运作，还是依赖于物资刷新管理器 |
| bLoopSpawn | bool | 独立运作模式时，物资被拾取后是否会自动生成 |
| SpawnCD | float | 开启循环生成后，物资被拾取后间隔重新刷新 |
| bTraceGround | bool | 物资是否一定刷新在地面上 |
| bRandomRotator | bool | 物资方向是否随机 |
| StartRadius | int32 | 物资刷新位置到刷新点的最小距离 |
| EndRadius | int32 | 物资刷新位置到刷新点的最大距离 |

**函数：**

- **SpawnItem**(ItemID: int32, ItemCount: int32) -> AActor *  — 生效范围 服务器    刷物资
- **SetItemConfig**(InItemConfig: FUGCItemSpawnerItemConfig) -> void  — 生效范围 服务器    修改物资刷新配置
- **CleanItems**() -> void  — 生效范围 服务器    清除刷出的物资

---

### AUGCMobCharacter

怪物角色类

**分类：** Others

**继承：** ACharacter, IObjectPoolInterface, IDamageableInterface, IAttrModifyInterface, IGameAttributeCarrierInterface, IRegionObjectInterface, IBulletEffectInterface, IBulletHitInterface

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Health | float | 当前生命值 |
| HealthAddScale | float | 加血速率 |
| HealthMax | float | 最大生命值 |
| bInvincible | int | 是否无敌 |
| SkillCDRecoverRate | FGameAttributeProperty | 技能急速，值越大技能冷却越快结束 |
| IsShowDamageNum | bool | 是否显示伤害数字 |
| HealthBarWidget | UUGCCharacterPositionWidget * | 血条的蓝图类 |
| bIsShowHealthBar | bool | 是否显示血条 |
| ShowName | FName | 血条上显示的名字 |
| PlayBeHitedAnimTimeInterval | float | 受击动画播放最小间隔，小于受击动画长度时无效 |
| bNeedDestroyOnDeath | bool | 是否启用尸体消失后延迟销毁 |
| DisappearOnDeathLifeSpan | float | 尸体消失后延迟多久销毁 |
| DelayRemoveDeadBody | float | 死亡后尸体存在时间 |
| BornTime | float | 出生状态持续时间 |
| StunDuration | float | 硬直状态持续时间 |
| UGCGeneralMoveSpeedScale | float | 移动速度倍率 |
| AttackMeActorRemainTime | float | 活动范围，处于活动范围外时索敌无效，仇恨随时间消失      UGC    处于活动范围外时仇恨持续时间 |
| SpawnLoc | FVector | 出生地点 |
| bOutOfActivityRange | bool | 是否在活动范围外 |

**函数：**

- **IsAlive**() -> bool  — 是否存活
- **IsInvincible**() -> FORCEINLINE int  — 是否无敌
- **ForceDie**() -> void  — 生效范围 服务器    强制杀死怪物
- **GetCurrentSpeed**() -> float  — 生效范围 服务器&客户端    获取当前速度值
- **GetVelocity**() -> FVector  — 生效范围 服务器&客户端    获取当前速度向量

---

### AUGCMobSpawner

刷怪系统：刷怪器

**分类：** Others

**继承：** AActor

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| bNeedSpawnerManager | bool | 是否刷怪点是否能独立运行，还是必须依赖刷怪管理器. 废弃, 请使用SpawnerContrMode |
| SpawnerContrMode | EUGCMobSpawnerContrMode | 刷怪器控制模式. |
| MobConfig | FUGCMobSpawnerMobConfig | 配置刷出的怪物 |
| bUseNavMesh | bool | 是否优先在有移动网格的地面上刷新 |
| Range | float | 配置怪物的生成范围的半径 |
| Height | float | 配置刷新点位置与实际生成位置的最大高度差 |
| RandomRotYaw | bool | 怪物的出生面向是否随机，否则使用刷新点的朝向 |
| MinSpawnCount | int32 | 配置总的最小刷怪数量 |
| MaxSpawnCount | int32 | 配置总的最大刷怪数量 |
| SpawnCD | float | 配置两次刷怪之间的时间间隔 |
| MobCountPerSpawn | int32 | 配置单次刷怪的数量 |
| bTraceGround | bool | 是否保证怪物刷到地面上 |

**函数：**

- **SpawnMob**(MobClass: UClass *) -> AActor *  — 生效范围 服务器    刷出指定怪物
- **SetMobConfig**(InMobConfig: FUGCMobSpawnerMobConfig) -> void  — 生效范围 服务器    修改怪物刷新配置
- **ModifyMinMaxSpawnCount**(InMinSpawnCount: int32, InMaxSpawnCount: int32) -> void  — 生效范围 服务器    修改最小最大刷怪数量

---

### AUGCPickUpWrapperActor

地面拾取物Actor

**分类：** Others

**继承：** APickUpWrapperActor

**函数：**

- **GetDefineID**() -> FItemDefineID  — 获取拾取物物品的实例ID    DS & 客户端 可调用
- **GetItemCount**() -> int32  — 获取拾取物物品的物品数量    DS & 客户端 可调用

---

### BP_UGCPickUpListComponent

UGC物品拾取组件

**分类：** Others

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| BP_UGCPickUpListComponent.PauseAutoPickDelay |  |  |
| BP_UGCPickUpListComponent.bCanAutoPickC |  |  |
| BP_UGCPickUpListComponent.HideForAimC |  |  |
| BP_UGCPickUpListComponent.bNeedRefresh |  |  |
| BP_UGCPickUpListComponent.LastItemCount |  |  |
| BP_UGCPickUpListComponent.LastCheckSum |  |  |
| BP_UGCPickUpListComponent.LastRefreshTime |  |  |
| BP_UGCPickUpListComponent.ItemUsefulCache |  |  |
| BP_UGCPickUpListComponent.PickupItemListCache |  |  |
| BP_UGCPickUpListComponent.TomBoxItemListCache |  |  |
| BP_UGCPickUpListComponent.PickupItemListCacheChange |  |  |
| BP_UGCPickUpListComponent.TomBoxItemListCacheChange |  |  |
| BP_UGCPickUpListComponent.bUpDateListDataChange |  |  |

**函数：**

- **SortItems**() -> void  — 物品排序比较函数：按有用性、规则优先级、自动拾取标记、OrderWeight排序  @param a table 物品数据A  @param b table 物品数据B  @return boolean a是否应该排在b前面
- **RuleWeapon**() -> void  — 武器规则：排除近战/弩 → 检查长枪/手枪槽位  手枪: 当前无手枪 + 长枪没满 + 开启"自动拾取手枪" → 自动拾取  长枪: 不足两把 → 自动拾取  @param ItemDefineID FItemDefineID 物品定义ID
- **RuleAttachment**() -> void  — 配件规则：遍历所有武器检查配件适配性  有空位 → 拾取；比同槽位配件更好(OrderWeight/品质) → 替换拾取  快扩(Tag=Item.Attachments.Magazine)最高优先级：品质优先，OrderWeight次之 
- **RuleAmmo**() -> void  — 弹药规则：遍历所有武器检查是否使用此弹药  需求总量 = RecommendPickCount(配表默认弹药量) * 使用该弹药的武器数  背包总弹量低于需求总量 → 拾取差值  @param ItemDefineID FItemDefin
- **RuleMedicine**() -> void  — 药品规则：每种药品单独配置拾取数量(RecommendPickCount)  背包数量低于推荐值 → 拾取差值  @param ItemDefineID FItemDefineID 物品定义ID  @param Count number 物
- **RuleThrowable**() -> void  — 投掷物规则：背包数量低于RecommendPickCount → 拾取差值  @param ItemDefineID FItemDefineID 物品定义ID  @param Count number 物品数量  @return table
- **RuleArmorBackpack**() -> void  — 防具背包规则：遍历背包找同类型装备比较  背包: 比较 OrderWeight（排序权重高的优先）  装备(头盔/护甲): 比较品质和耐久度    品质更高 → 替换；同品质比较 OrderWeight    高品质耐久低于阈值(Armor
- **RuleGeneralOrder**() -> void  — 通用排序规则(所有物品)：score = Handle.OrderWeight * 100 + 品质  用于兜底排序，不触发自动拾取  @param ItemDefineID FItemDefineID 物品定义ID  @param Cou

---

### BP_UGCVehicleRefresherTool

载具刷新器工具，用于管理载具的自动刷新和生成

**分类：** Others

**函数：**

- **AddVehicleEventListener**(callback: function, context: any) -> void  — 添加载具生成事件监听器，外部代码调用此方法注册载具生成事件监听 生效范围：服务器
- **AddVehicleDriveAwayEventListener**(callback: function, context: any) -> void  — 添加载具开走事件监听器，外部代码调用此方法注册载具开走事件监听 生效范围：服务器
- **RemoveVehicleEventListener**(callback: function, context: any) -> void  — 移除载具生成事件监听器 生效范围：服务器
- **RemoveVehicleDriveAwayEventListener**(callback: function, context: any) -> void  — 移除载具开走事件监听器 生效范围：服务器
- **GenerateVehicle**() -> boolean  — 根据权重配置随机生成载具 生效范围：服务器
- **GenerateCustomizeVehicle**(VehiclePath: string) -> boolean  — 生成指定的载具蓝图 生效范围：服务器
- **DestroyCurrentVehicle**() -> boolean  — 销毁当前刷新点管理的载具 生效范围：服务器
- **ResetVehicleRespawnPoint**() -> boolean  — 重置载具刷新点，如果载具还在原地，先销毁再重新刷新 生效范围：服务器
- **GetVehicleRespawnPointConfig**() -> table  — 获取配置的载具列表信息 生效范围：服务器&客户端
- **GetVehicleStatusConfig**() -> table  — 获取当前车辆的实时状态信息 生效范围：服务器&客户端

---

### FUGCActivityTask

活动任务结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| TaskID | int32 | 任务ID |
| ResetType | EUGCActivityTaskResetType | 重置类型 |


---

### FUGCCustomDamageNumberItemParams

自定义伤害数字单元

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ImagePath | FString | 图片路径 |
| Text | FString | 文本，只支持数字和符号，图片路径为空时才有效 |
| ImageScaleX | float | 图片X轴缩放比例 |
| ImageScaleY | float | 图片Y轴缩放比例 |


---

### FUGCDamageNumberParams

自定义伤害数字参数

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Items | TArray < FUGCCustomDamageNumberItemParams > | 显示单元列表 |
| TimeLife | float | 显示时间 |
| MoveTimeLife | float | 飞行时间 |
| DrawColor | FLinearColor | 数字的颜色 |
| DrawOutlineColor | FLinearColor | 数字的描边颜色 |
| DrawOutlineSize | float | 数字的描边大小 |
| FadeInTime | float | 淡入时间 |
| FadeOutTime | float | 淡出时间 |
| SizeScaleRange | FVector2D | 初始尺寸缩放范围 |
| MoveScaleRange | FVector2D | 移动距离缩放范围 |
| OriginPositionRangeX | FVector2D | 初始位置水平偏移范围 |
| OriginPositionRangeY | FVector2D | 初始位置垂直偏移范围 |
| MoveDirection | FVector2D | 飞行角度范围，范围-180到180 |
| bFollowTarget | bool | 是否跟随目标 |


---

### FUGCGamePartPlayerComponentConfig

PlayerComponent配置

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| PlayerComponentName | FName | PlayerComponent名称 |
| PlayerComponentClass | TSubclassOf < UActorComponent > | PlayerComponent类配置 |


---

### FUGCGenerateDropItemInfo

蓝图配置掉落物信息

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ItemID | int32 | 掉落物ItemID |
| Count | int32 | 掉落物数量 |


---

### FUGCItemSpawnerInfo

物资生成管理器上每个刷新点的配置

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Spawner | AUGCItemSpawner * | 使用的刷新点 |
| bOverrideItemConfig | bool | 是否覆盖该刷新点上的物资配置，开启则刷新点上的配置无效，使用这里的配置 |
| ItemConfig | FUGCItemSpawnerItemConfig | 配置刷新点上的物资配置 |


---

### FUGCItemSpawnerItemConfig

物资配置

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ConfigMode | EUGCItemSpawnerConfigMode | 刷出物资的配置方式 |
| ItemID | int32 | 使用物资ID模式时，物资的ID |
| ItemCount | int32 | 使用物资ID模式时，物资的数量 |
| DropID | int32 | 使用掉落表模式时，掉落表的ID |
| DropGroupID | int32 | 使用掉落组表模式时，掉落组表的ID |
| CustomParam | TMap < FString , FString > | 使用自定义模式时，用于自定义的ID |


---

### FUGCItemTransferResult

物品转移结果

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| CanTransfer | bool | 转移是否成功 |
| TransferErrorReason | TArray < FName > | 如果转移失败，失败原因来自于转移者 |
| ItemErrorReason | TMap < FItemDefineID , FName > | 如果转移失败，失败原因来自于物品 |


---

### FUGCLevelTaskLineConfig

成长任务线配置结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Level | int32 | 等级 |
| TaskIDList | TArray < int32 > | 任务ID列表 |


---

### FUGCMobBTBlackBoardInfo

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Key | FName |  |
| Value | FString |  |
| ValueType | FName |  |


---

### FUGCMobBTDebugInfo

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Trees | TArray < FUGCMobBTDebugTreeInfo > |  |
| Elems | TArray < FUGCMobBTDebugTreeElemInfo > |  |


---

### FUGCMobBTDebugTreeElemInfo

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Name | FName |  |
| ExecutionIndex | int32 |  |
| ParentExecutionIndex | int32 |  |
| TickInternal | float |  |
| RandomDeviation | float |  |
| Value | bool |  |


---

### FUGCMobBTDebugTreeInfo

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Name | FName |  |
| NodeStartIndex | int32 |  |
| DecoratorStartIndex | int32 |  |
| ServiceStartIndex | int32 |  |
| ParallelTaskStartIndex | int32 |  |
| EndIndex | int32 |  |


---

### FUGCMobSpawnerMobConfig

刷怪系统：怪物刷新配置

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ConfigMode | EUGCMobSpawnerConfigMode | 刷出怪物类型的配置方式 |
| MobClass | TSubclassOf < AGenericCharacter > | 使用蓝图配置时，刷出的怪物类 |
| MobGroupID | int32 | 使用怪物组表时，怪物组表的ID |
| CustomParam | TMap < FString , FString > | 使用自定义模式时，自定义参数列表 |


---

### FUGCPercentTaskAward

活跃任务线奖励结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| Percent | int32 | 活跃度 |
| ItemList | TArray < FUGCRankingListAwardItem > | 奖励道具列表 |


---

### FUGCPercentTaskLineConfig

活跃任务线配置结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| PercentTaskID | int32 | 任务ID |
| Priority | int32 | 任务排序优先级 |


---

### FUGCPickupItemData

拾取物物品数据

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| PickupWrapper | AActor * | 物品所在的拾取物Actor |
| ItemDefineID | FItemDefineID | 物品 DefineID |
| ItemCount | int32 | 物品数量 |


---

### FUGCRankingListAwardItem

排行榜物品结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ItemID | int32 | 物品ID |
| ItemNum | int32 | 物品数量 |


---

### FUGCRankingListData

排行榜表格结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ID | int32 | 排行榜索引ID |
| PeopleNum | int32 | 排行榜最大上榜人数 |
| PeriodType | ERankListPeriodType | 排行榜周期类型 |
| BeginDate | FDateTime | 排行榜开始时间 |
| SettleDate | FDateTime | 非周期榜结算时间 |
| EndDate | FDateTime | 排行榜结束时间 |
| SortPropertyName | FString | 排序属性名称 |
| SortType | ERankListSortType | 排序类型 |
| RankAward | TArray < FRankListAward > | 排行榜奖励列表 |
| TabName | FString | 排行榜页签名称 |
| EnableType | ERankListEnableType | 是否启用排行榜 |
| ShowInGame | ERankListDisplayType | 是否在玩法内展示 |
| ShowInDetails | ERankListDisplayType | 是否在玩法详情页展示 |
| Desc | FString | 排行榜说明 |
| ScoreFormatType | ERankListScoreFormatType | 分数显示格式 |


---

### FUGCSpawnActorNumLimitCfg

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ActorName | FString |  |
| NumLimit | int32 |  |


---

### FUGCTaskConfig

任务结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| TaskID | int32 | 任务ID |
| TaskName | FString | 任务名称 |
| TaskType | UUGCTaskTypeBase * | 任务类型 |
| TaskDesc | FString | 任务说明 |
| TaskAwardList | TArray < FUGCRankingListAwardItem > | 任务奖励列表 |
| BeginDate | FDateTime | 开始时间 |
| EndDate | FDateTime | 结束时间 |
| IsShowOutDate | bool | 过期后是否显示 |
| IsShowGotoBtn | bool | 是否显示任务的前往按钮 |


---

### FUGCTaskLineConfig

任务线配置结构体

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| TaskLineType | EUGCTaskLineType | 任务线类型 |
| TaskLineName | FString | 任务线名称 |
| LevelTaskLineConfig | TArray < FUGCLevelTaskLineConfig > | 成长任务线配置 |
| PercentTaskLineConfig | TArray < FUGCPercentTaskLineConfig > | 活跃任务线配置 |
| LevelTaskPropertyName | FString | 成长等级属性名称 |
| PercentAwardList | TArray < FUGCPercentTaskAward > | 进度奖励列表 |
| ResetType | EUGCPercentTaskResetType | 活跃任务线重置类型 |
| WeeklyResetTime | EUGCTaskCustomWeekResetType | 活跃任务线周重置类型 |
| DailyResetTime | FString | 活跃任务线重置时间 |
| ItemID | int32 | 活跃度道具ID |
| BeginDate | FDateTime | 开始时间 |
| EndDate | FDateTime | 结束时间 |


---

### UGCActivitySystem

活动系统库（需要启用活动GamePart）

**分类：** Others

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| UGCActivitySystem.OnActivityInfoReadyDelegate |  | 活动信息准备好时触发的委托 生效范围：客户端&&服务器 |
| UGCActivitySystem.OnUpdateValidActivityIDsDelegate |  | 更新有效活动时触发的委托 活动系统会按照每个活动配置的生效周期来定期更新有效活动 生效范围：客户端&&服务器 |

**函数：**

- **IsActivityInfoReady**() -> bool  — 活动信息是否已准备好 生效范围：客户端&&服务器
- **GetAllActivityInfos**() -> UGCActivityInfo[]  — 获取所有活动的信息 生效范围：客户端&&服务器
- **GetActivityInfo**(ActivityID: int) -> UGCActivityInfo  — 获取指定活动ID的活动信息 生效范围：客户端&&服务器
- **GetValidActivityIDs**() -> int[]  — 获取所有有效的活动ID 生效范围：客户端&&服务器
- **GetNearestPeriodIndex**(ActivityID: int) -> int  — 获取指定活动距当前时间最近的生效周期序号， 如果已经没有符合条件的开启周期，则返回最后一个生效周期的序号 生效范围：服务器&客户端

---

### UGCAirAttachSystem

轰炸区接口库

**分类：** Others

**函数：**

- **GenerateBombingArea**(ConfigID: number, Location: FVector) -> number  — 生成轰炸区 生效范围：服务器
- **StopBombingArea**(InstanceID: number) -> bool  — 停止轰炸区 生效范围：服务器
- **ModifyBombingAreaConfig**(ConfigID: number, ParameterType: string, NewValue: number) -> bool  — 修改轰炸区参数 生效范围：服务器
- **GetAllConfigBombingArea**() -> UGCAirAttackConfig>  — 查看当前全部轰炸区 生效范围：服务器
- **GetSpecifyBombingAreaList**(InstanceID: number) -> UGCAirAttackConfig  — 查看指定轰炸区参数 生效范围：服务器
- **GetAirAttackManager**() -> UGCAirAttackManager  — 获取轰炸区管理器 生效范围：服务器&客户端

---

### UGCAirAttackManager

UGC轰炸区全局管理器

**分类：** Others

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| UGCAirAttackManager.SuccessfullyGeneratedBombing |  | 轰炸区生成成功事件 当轰炸区域成功创建并准备开始预警时触发 生效范围：服务器&客户端 @param InstanceID number @轰炸实例唯一标识符 @param CenterLocation FVector @轰炸中心位置坐标 |
| UGCAirAttackManager.SuccessfullyStopBombing |  | 轰炸区停止成功事件 当轰炸区域被成功停止（主动停止或异常结束）时触发 生效范围：服务器&客户端 @param InstanceID number @被停止的轰炸实例唯一标识符 |
| UGCAirAttackManager.NormalEndBombing |  | 轰炸正常结束事件 当轰炸区域按计划完成所有炸弹投放后正常结束时触发 生效范围：服务器&客户端 @param InstanceID number @结束的轰炸实例唯一标识符 @param TotalBombsDropped number @实际投放的炸弹总数 |
| UGCAirAttackManager.SuccessfullyStartBombing |  | 轰炸正式开始事件 当轰炸预警结束后，开始正式投放炸弹时触发 生效范围：服务器&客户端 @param InstanceID number @开始轰炸的实例唯一标识符 |
| UGCAirAttackManager.AffectedBombingPlayers |  | 玩家受影响事件 当炸弹爆炸并对范围内玩家造成伤害时触发 生效范围：服务器&客户端 @param BombLocation FVector @炸弹爆炸位置坐标 @param AffectedPlayerKeys number[] @受到影响的玩家PlayerKey数组 |
| UGCAirAttackManager.__BombingPromiseFutures |  |  |
| UGCAirAttackManager.__WarningTimers |  |  |
| UGCAirAttackManager.__AirAttackMarks |  |  |
| UGCAirAttackManager.__MarkGraphIDs |  |  |

**函数：**

- **ExecuteAirAttack**(ConfigInput: number|UGCAirAttackConfig, CenterLocation: FVector|nil) -> number
- **AbortAirAttack**(InstanceID: number) -> void
- **Multicast_ExecuteAirAttack**(BroadcastData: table) -> void
- **Multicast_AbortAirAttack**(InstanceID: number) -> void

---

### UGCCharAvatarShowcaseActor

复制玩家角色Avatar的Actor

**分类：** Others

**函数：**

- **ClientShowAvatar**(PlayerUID: number) -> void  — 显示PlayerUID的Avatar 生效范围：客户端
- **ServerShowAvatar**(PlayerUID: number) -> void  — 显示PlayerUID的Avatar 生效范围：服务端
- **PlayAnim**(NewAnimToPlay: UAnimationAsset, bLooping: boolean) -> void  — 播放动画 生效范围：客户端

---

### UGCCommonDragDropItem

拖拽控件

**分类：** Others

**函数：**

- **SetDragWidget**(Widget: UUserWidget|Class, bCreate: boolean) -> void  — 设置拖拽时的控件
- **SetDragDirectionMode**(DirectionMode: EDragDirectionMode) -> void  — 设置拖拽方向模式
- **SetDragDropMode**(DragDropMode: EDragDropMode) -> void  — 设置拖拽模式
- **RegisterDragDropData**(DragDropData: table, DragDropMode: EDragDropMode) -> void  — 注册拖拽(入口)
- **SetData**(Data: table) -> void  — 设置拖拽数据

---

### UGCCommonUISystem

UI通用响应库

**分类：** Others

**函数：**

- **AddDragSuccess**(InFunc: function, Context: table) -> void  — 拖拽成功添加监听 生效范围：客户端
- **RemoveDragSuccess**(InFunc: function, Context: table) -> void  — 拖拽成功移除监听 生效范围：客户端

---

### UGCEMPZoneManager

电磁干扰区管理器

**分类：** Others

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| UGCEMPZoneManager.SuccessfullyGeneratedElectromagnetic |  | param InstanceID number @param CenterLocation FVector |
| UGCEMPZoneManager.SuccessfullyStopElectromagnetic |  | param InstanceID number |
| UGCEMPZoneManager.NormalEndElectromagnetic |  | param InstanceID number |
| UGCEMPZoneManager.SuccessfullyStartElectromagnetic |  | param InstanceID number |
| UGCEMPZoneManager.AffectedElectromagneticPlayers |  | param AffectedPlayerKeys number |
| UGCEMPZoneManager.__EMPZoneMarkTypeID |  |  |
| UGCEMPZoneManager.__EMPZoneMarkInstIDs |  |  |

**函数：**

- **_ValidateAndClampConfig**(Config: UGCEMPZoneConfig) -> UGCEMPZoneConfig
- **_GetInstanceDetailData**(InstanceID: number) -> table|nil
- **_GetConfigByIndex**(Index: number) -> table|nil
- **_ModifyConfigByIndex**(Index: number, NewConfig: table) -> bool
- **_GetElectromagneticAreaConfigs**(InstanceID: number|nil) -> table|nil
- **_ConvertToLuaConfigs**(ElectromagneticInstances: table) -> table
- **_GenerateNextInstanceID**() -> number
- **_MapLuaConfigToComponent**(LuaConfig: UGCEMPZoneConfig) -> FEMPZoneCfg
- **_SyncCapsuleRadius**(EMPZoneActor: AEMPZoneActor, InstanceData: table) -> boolean
- **_WriteConfigToComponent**(Comp: UEMPZoneControlComponent, ComponentConfig: FEMPZoneCfg) -> boolean
- **CreateEMPZone**(ConfigID: string, CenterLocation: FVector) -> void
- **_CreateEMPZoneActor**(InstanceID: number) -> boolean
- **DestroyElectromagneticArea**(InstanceID: number) -> boolean
- **_DestroyAllElectromagneticAreas**() -> boolean
- **ModifyConfigElectromagneticArea**(ConfigIndex: number, ParameterName: string, NewValue: any) -> boolean
- **GetAllConfigElectromagneticArea**() -> table
- **GetSpecifyElectromagneticAreaList**(InstanceID: number) -> table
- **_NotifyClientHideMapMark**(InstanceID: number) -> void  — 当 EMPZone 销毁时隐藏小地图标记
- **Client_OnEMPZoneMapMarkShow**(InstanceID: number, LocX: number, LocY: number, LocZ: number, EffectRadius: number, ZoneState: number) -> void  — [Client RPC] 显示 EMPZone 小地图标记
- **Client_OnEMPZoneMapMarkHide**(InstanceID: number) -> void  — [Client RPC] 隐藏 EMPZone 小地图标记

---

### UGCEMPZoneSystem

电磁干扰区接口库

**分类：** Others

**函数：**

- **GenerateElectromagneticArea**(ConfigID: number, Location: FVector) -> number  — 生成电磁干扰区 生效范围：服务器
- **DestroyElectromagneticArea**(InstanceID: number) -> bool  — 取消电磁干扰区 生效范围：服务器
- **ModifyConfigElectromagneticArea**(ConfigID: number, ParameterType: string, NewValue: number) -> bool  — 修改电磁干扰区参数 生效范围：服务器
- **GetAllConfigElectromagneticArea**() -> UGCEMPZoneConfig>  — 查看当前全部电磁干扰区 生效范围：服务器
- **GetSpecifyElectromagneticAreaList**(InstanceID: number) -> UGCEMPZoneConfig  — 查看指定电磁干扰区参数 生效范围：服务器
- **GetEMPZoneManager**() -> UGCEMPZoneManager  — 获取电磁干扰区管理器 获取电磁干扰区全局管理器实例，用于绑定电磁干扰区相关事件 生效范围：服务器&客户端

---

### UGCEntityTypeSystem

实体类型查询系统接口库

**分类：** Others

**函数：**

- **IsActorOfEntityType**(Actor: AActor, EntityTypeName: string) -> boolean  — 判断Actor是否属于指定的实体类型 生效范围：服务器&客户端
- **GetActorEntityType**(Actor: AActor) -> string  — 获取Actor的实体类型（返回第一个匹配的） 生效范围：服务器&客户端
- **GetActorEntityTypes**(Actor: AActor) -> string[]  — 获取Actor的所有匹配的实体类型 生效范围：服务器&客户端
- **GetAllEntityTypeNames**() -> string[]  — 获取所有已配置的实体类型名称 生效范围：服务器&客户端
- **OverlapBoxByEntityType**(WorldContext: UObject, EntityTypeName: string, Location: FVector, HalfExtent: FVector, Rotation: FRotator) -> AActor[]  — 使用Box形状检测指定EntityType的Actor 生效范围：服务器&客户端
- **OverlapSphereByEntityType**(WorldContext: UObject, EntityTypeName: string, Location: FVector, Radius: number) -> AActor[]  — 使用Sphere形状检测指定EntityType的Actor 生效范围：服务器&客户端
- **OverlapCapsuleByEntityType**(WorldContext: UObject, EntityTypeName: string, Location: FVector, Radius: number, HalfHeight: number, Rotation: FRotator) -> AActor[]  — 使用Capsule形状检测指定EntityType的Actor 生效范围：服务器&客户端
- **IsActorOfClassType**(Actor: AActor, ActorClassPath: string) -> boolean  — 检查Actor是否为指定的类类型 生效范围：服务器&客户端
- **IsActorOfAnyClassTypes**(Actor: AActor, ActorClassPaths: string[]) -> boolean  — 检查Actor是否为指定类类型数组中的任意一种 生效范围：服务器&客户端
- **IsActorOfEntityTypeByTag**(Actor: AActor, EntityTypeTag: FGameplayTag) -> boolean  — 判断Actor是否属于指定的实体类型（使用GameplayTag） 生效范围：服务器&客户端
- **IsActorOfEntityTypeByTags**(Actor: AActor, EntityTypeTags: FGameplayTagContainer) -> boolean  — 判断Actor是否属于指定的实体类型（使用GameplayTagContainer） 生效范围：服务器&客户端
- **GetActorEntityTypeAsGameplayTag**(Actor: AActor) -> FGameplayTag  — 获取Actor的实体类型（返回GameplayTag） 生效范围：服务器&客户端
- **GetActorEntityTypesAsGameplayTagContainer**(Actor: AActor) -> FGameplayTagContainer  — 获取Actor的所有匹配的实体类型（返回GameplayTagContainer） 生效范围：服务器&客户端
- **OverlapBoxByEntityTypeTag**(WorldContext: UObject, EntityTypeTag: FGameplayTag, Location: FVector, HalfExtent: FVector, Rotation: FRotator) -> AActor[]  — 使用Box形状检测指定EntityType的Actor（使用GameplayTag） 生效范围：服务器&客户端
- **OverlapBoxByEntityTypeTags**(WorldContext: UObject, EntityTypeTags: FGameplayTagContainer, Location: FVector, HalfExtent: FVector, Rotation: FRotator) -> AActor[]  — 使用Box形状检测指定EntityType的Actor（使用GameplayTagContainer） 生效范围：服务器&客户端
- **OverlapSphereByEntityTypeTag**(WorldContext: UObject, EntityTypeTag: FGameplayTag, Location: FVector, Radius: number) -> AActor[]  — 使用Sphere形状检测指定EntityType的Actor（使用GameplayTag） 生效范围：服务器&客户端
- **OverlapSphereByEntityTypeTags**(WorldContext: UObject, EntityTypeTags: FGameplayTagContainer, Location: FVector, Radius: number) -> AActor[]  — 使用Sphere形状检测指定EntityType的Actor（使用GameplayTagContainer） 生效范围：服务器&客户端
- **OverlapCapsuleByEntityTypeTag**(WorldContext: UObject, EntityTypeTag: FGameplayTag, Location: FVector, Radius: number, HalfHeight: number, Rotation: FRotator) -> AActor[]  — 使用Capsule形状检测指定EntityType的Actor（使用GameplayTag） 生效范围：服务器&客户端
- **OverlapCapsuleByEntityTypeTags**(WorldContext: UObject, EntityTypeTags: FGameplayTagContainer, Location: FVector, Radius: number, HalfHeight: number, Rotation: FRotator) -> AActor[]  — 使用Capsule形状检测指定EntityType的Actor（使用GameplayTagContainer） 生效范围：服务器&客户端
- **GetAllEntityTypesAsGameplayTagContainer**() -> FGameplayTagContainer  — 获取所有已配置的实体类型（返回GameplayTagContainer） 生效范围：服务器&客户端
- **ConvertEntityTypeNameToGameplayTag**(EntityTypeName: string) -> FGameplayTag  — 将实体类型名称转换为GameplayTag 生效范围：服务器&客户端
- **ConvertGameplayTagToEntityTypeName**(EntityTypeTag: FGameplayTag) -> string  — 将GameplayTag转换为实体类型名称 生效范围：服务器&客户端
- **SetConfigDataAssetPath**(ConfigDataAssetPath: string) -> void  — 设置自定义配置DataAsset路径 如果不调用此函数，将使用默认路径 生效范围：服务器&客户端
- **ForceReloadConfig**() -> void  — 强制重新加载配置 配合SetConfigDataAssetPath使用，建议设置完路径后调用一次 生效范围：服务器&客户端

---

### UGCGameplayTag

UGCGameplayTag

**分类：** Others

**函数：**

- **__tostring**() -> string  — 返回 UGCGamePlayTag 的字符串
- **IsValid**() -> boolean  — 检查当前这个 UGCGameplayTag 是否合法

---

### UGCInputSystem

输入系统接口库

**分类：** Others

**函数：**

- **BindInputMapping**(BindingOwner: UObject, InputTag: UGCGameplayTag|string|FGameplayTag, TriggerEvent: ETriggerEvent, CallbackFunction: fun(InputValue:float, ElapsedTime:float, TriggeredTime:float, InputTag:FGameplayTag) @事件触发回调函数) -> int32  — 绑定指定InputTag事件的回调函数 生效范围：客户端
- **RemoveBindingToObject**(BindingOwner: UObject) -> void  — 解除与目标Object所有相关的输入事件绑定 生效范围：客户端
- **RemoveBinding**(WorldContext: UObject, InputBindingHandle: int32) -> void  — 解除指定索引的输入事件绑定 生效范围：客户端
- **InjectInputMapping**(WorldContext: UObject, InputTag: UGCGameplayTag|string|FGameplayTag, Value: float) -> void  — 通过脚本手动触发某个InputTag 生效范围：客户端
- **SetBindingConsumeInput**(WorldContext: UObject, InputBindingHandle: int32, bConsumeInput: bool) -> void  — 设置某个输入事件绑定是否消耗输入，消耗输入后，后续的其他输入事件绑定将不被触发 生效范围：客户端
- **GetInputValue**(WorldContext: UObject, InputTag: UGCGameplayTag|string|FGameplayTag) -> float  — 获取指定InputTag对应Input的当前值 生效范围：客户端

---

### UGCMailSystem

邮件系统库

**分类：** Others

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| UGCMailSystem.MailListUpdateDelegate |  | 玩家邮件列表更新时触发 非PIE时，仅在玩家刚进入玩法时触发一次，玩家在局内时后台发送的邮件，会在下一局进入时更新 @param UID int @UID @param MailList UGCMailInfo[] @邮件列表 |
| UGCMailSystem.ClaimMailsResultDelegate |  | 收到领取邮件奖励结果后触发 @param UID int @UID @param ItemList table @奖励物品列表 @param ClaimedMailIDs int[] @已领取的邮件ID数组 @param FailedResults table<ID,EUGCMailOperationFailedReason> @失败邮件 |
| UGCMailSystem.ReadMailsResultDelegate |  | 收到标记邮件已阅读结果后触发 @param UID int @UID @param ReadMailIDs int[] @已阅读的邮件ID数组 @param FailedResults table<ID,EUGCMailOperationFailedReason> @失败邮件 |
| UGCMailSystem.DeleteReadMailsResultDelegate |  | 收到删除已读邮件结果后触发 @param UID int @UID @param DeletedMailIDs int[] @已删除的邮件ID数组 @param FailedResults table<ID,EUGCMailOperationFailedReason> @失败邮件 |

**函数：**

- **GetMailList**(UID: int) -> UGCMailInfo[]  — 获取指定玩家的邮件列表 生效范围：服务器
- **GetMailInfo**(UID: int, MailID: int) -> UGCMailInfo  — 获取指定玩家的邮件信息 生效范围：服务器
- **ClaimMailAward**(UID: int, MailIDs: int[]) -> void  — 请求领取指定玩家的邮件奖励 生效范围：服务器
- **ReadMail**(UID: int, MailIDs: int[]) -> void  — 请求标记指定玩家的邮件已读 生效范围：服务器
- **DeleteReadMail**(UID: int, MailIDs: int[]) -> void  — 请求删除指定玩家的已读邮件 生效范围：服务器
- **PIESendMail**(UID: int, Title: string, Content: string, ExpireTime: int, Attachments: table) -> void  — 发送邮件, 仅PIE环境有效 生效范围：服务器

---

### UGCMathUtility

数学工具接口库

**分类：** Others

**函数：**

- **Sin**(A: number) -> number  — 返回A的正弦值(sin)，结果为弧度制
- **Asin**(A: number) -> number  — 返回A的反正弦值(arcsin)，结果为弧度制
- **Cos**(A: number) -> number  — 返回A的余弦值(cos)，结果为弧度制
- **Acos**(A: number) -> number  — 返回A的反余弦值(arccos)，结果为弧度制
- **Tan**(A: number) -> number  — 返回A的正切值(tan)，结果为弧度制
- **Atan**(A: number) -> number  — 返回A的反正切值(arctan)，结果为弧度制
- **DegSin**(A: number) -> number  — 返回A的正弦值(sin)，结果为角度制
- **DegAsin**(A: number) -> number  — 返回A的反正弦值(arcsin)，结果为角度制
- **DegCos**(A: number) -> number  — 返回A的余弦值(cos)，结果为角度制
- **DegAcos**(A: number) -> number  — 返回A的反余弦值(arccos)，结果为角度制
- **DegTan**(A: number) -> number  — 返回A的正切值(tan)，结果为角度制
- **DegAtan**(A: number) -> number  — 返回A的反正切值(arctan)，结果为角度制
- **DegAtan2**(A: number, B: number) -> number  — 返回A/B的反正切值(atan2)，结果为角度制
- **RandomFloat**() -> number  — 返回一个介于0和1之间的随机浮点数
- **RandomFloatInRange**(InMin: number, InMax: number) -> number  — 生成一个介于Min和Max之间的随机数
- **Lerp**(A: number, B: number, Alpha: number) -> number  — 根据Alpha在A和B之间线性插值（Alpha=0时返回A，Alpha=1时返回B））
- **FClamp**(InValue: number, InMin: number, InMax: number) -> number  — 【废弃】请使用 UGCMathUtility.Clamp 返回限制在A和B之间的值（包含A和B）
- **MapRangeClamped**(InValue: number, InMinIn: number, InMaxIn: number, InMinOut: number, InMaxOut: number) -> number  — 将数值从一个输入范围映射到另一个输出范围（数值会被限制在输入范围内）。（例如：将0.5从0→1范围映射到0→50范围会得到25）
- **NearlyEqualFloat**(A: number, B: number, Tolerance: number) -> boolean  — 返回A是否近似等于B（|A - B| < 误差容限）
- **NotEqualFloat**(A: number, B: number) -> boolean  — 如果A不等于B则返回true
- **Now**() -> FDateTime  — 返回当前计算机的本地日期和时间
- **Today**() -> FDateTime  — 返回当前计算机的本地日期
- **UtcNow**() -> FDateTime  — 返回当前计算机的UTC日期和时间
- **GetYear**(A: FDateTime) -> number  — 返回A的年分量值
- **GetMonth**(A: FDateTime) -> number  — 返回A的月分量值
- **DaysInMonth**(Year: number, Month: number) -> number  — 返回给定年份和月份的天数
- **AddVector**(A: FVector, B: FVector) -> FVector  — 向量加法
- **AddVector2D**(A: FVector2D, B: FVector2D) -> FVector2D  — 返回二维向量A和二维向量B的和（A + B）
- **SubtractVector**(A: FVector, B: FVector) -> FVector  — 向量减法
- **SubtractVector2D**(A: FVector2D, B: FVector2D) -> FVector2D  — 返回二维向量A和二维向量B的差（A - B）
- **MultiplyVector**(A: FVector, B: number) -> FVector  — 将向量A按B缩放
- **MultiplyVector2D**(A: FVector2D, B: number) -> FVector2D  — 将二维向量A按B缩放
- **VSize**(A: FVector) -> number  — 返回向量的长度
- **VSize2D**(A: FVector2D) -> number  — 返回二维向量的长度
- **VSizeSquared**(A: FVector) -> number  — 返回向量的长度的平方
- **VSizeSquared2D**(A: FVector2D) -> number  — 返回二维向量的长度的平方
- **EqualVector**(A: FVector, B: FVector, Tolerance: number) -> boolean  — 判断向量A是否在允许误差范围内等于向量B
- **NotEqualVector**(A: FVector, B: FVector, Tolerance: number) -> boolean  — 判断向量A是否在允许误差范围内不等于向量B
- **DotVector**(A: FVector, B: FVector) -> number  — 返回两个向量的点积
- **CrossVector**(A: FVector, B: FVector) -> FVector  — 返回两个向量的叉积
- **DotVector2D**(A: FVector2D, B: FVector2D) -> number  — 返回两个二维向量的点积
- **CrossVector2D**(A: FVector2D, B: FVector2D) -> number  — 返回两个二维向量的叉积
- **RotateVector**(A: FVector, B: FRotator) -> FVector  — 返回向量A经过 Rotator B 旋转后的结果
- **RotateAngleAxis**(A: FVector, AngleDeg: number, Axis: FVector) -> FVector  — 返回向量A绕Axis轴旋转AngleDeg角度后的结果
- **Normal**(A: FVector) -> FVector  — 返回向量A的单位法向量
- **Normal2D**(A: FVector2D) -> FVector2D  — 返回二维向量A的单位法向量
- **VLerp**(A: FVector, B: FVector, Alpha: number) -> FVector  — 根据Alpha值在向量A和向量B之间线性插值（Alpha=0时返回100%A，Alpha=1时返回100%B）
- **RandomUnitVector**() -> FVector  — 返回一个长度为1的随机向量
- **RandomPointInBoundingBox**(Origin: FVector, BoxExtent: FVector) -> FVector  — 返回指定边界框内的随机点
- **ProjectVectorOnToVector**(V: FVector, Target: FVector) -> FVector  — 将向量V投影到目标向量Target上并返回投影向量，如果Target长度接近零，则返回零向量
- **FInterpTo**(Current: number, Target: number, DeltaTime: number, InterpSpeed: number) -> number  — 根据当前值到目标值的插值进行平滑过渡，实现流畅的过度效果
- **FInterpConstantTo**(Current: number, Target: number, DeltaTime: number, InterpSpeed: number) -> number  — 以恒定速率向目标值变换
- **VInterpTo**(Current: FVector, Target: FVector, DeltaTime: number, InterpSpeed: number) -> FVector  — 根据向量表示的当前位置与目标位置的距离平滑地接近目标位置，实现流畅的追踪效果
- **VInterpConstantTo**(Current: FVector, Target: FVector, DeltaTime: number, InterpSpeed: number) -> FVector  — 以恒定速率向向量表示的目标位置移动
- **Vector2DInterpTo**(Current: FVector2D, Target: FVector2D, DeltaTime: number, InterpSpeed: number) -> FVector2D  — 根据二维向量表示的当前位置与目标位置的距离平滑地接近目标位置，实现流畅的追踪效果
- **Vector2DInterpConstantTo**(Current: FVector2D, Target: FVector2D, DeltaTime: number, InterpSpeed: number) -> FVector2D  — 以恒定速率向二维向量表示的目标位置移动
- **RInterpTo**(Current: FRotator, Target: FRotator, DeltaTime: number, InterpSpeed: number) -> FRotator  — 根据当前旋转角度平滑过渡到目标旋转角度，实现流畅的旋转效果
- **RInterpConstantTo**(Current: FRotator, Target: FRotator, DeltaTime: number, InterpSpeed: number) -> FRotator  — 以恒定速率向目标旋转角度旋转
- **FindClosestPointOnSegment**(Point: FVector, SegmentStart: FVector, SegmentEnd: FVector) -> FVector  — 查找线段上距离给定点最近的点
- **FindClosestPointOnLine**(Point: FVector, LineOrigin: FVector, LineDirection: FVector) -> FVector  — 找到无限长直线上距离给定点最近的点
- **GetPointDistanceToSegment**(Point: FVector, SegmentStart: FVector, SegmentEnd: FVector) -> number  — 计算点到线段的最短距离
- **GetPointDistanceToLine**(Point: FVector, LineOrigin: FVector, LineDirection: FVector) -> number  — 计算点到无限长直线的最短距离
- **ProjectVectorOnToPlane**(V: FVector, PlaneNormal: FVector) -> FVector  — 将向量投影到由法向量定义的平面上
- **NegateVector**(V: FVector) -> FVector  — 向量取反
- **ClampVectorSize**(V: FVector, Min: number, Max: number) -> FVector  — 将向量长度限制在最小值和最大值之间
- **GetMinElement**(V: FVector) -> number  — 找出向量中(X, Y或Z)的最小分量
- **GetMaxElement**(V: FVector) -> number  — 找出向量中(X, Y或Z)的最大分量
- **GetDirectionUnitVector**(From: FVector, To: FVector) -> FVector  — 计算从一个位置指向另一个位置的单位方向向量
- **EqualName**(A: string, B: string) -> boolean  — 如果A和B相等则返回true (A == B)
- **NotEqualName**(A: string, B: string) -> boolean  — 如果A和B不相等则返回true (A ~= B)
- **MakeBox**(Min: FVector, Max: FVector) -> FBox  — 通过最小点和最大点创建一个FBox，并将IsValid设为true
- **MakeBox2D**(Min: FVector2D, Max: FVector2D) -> FBox2D  — 通过最小点和最大点创建一个FBox2D，并将IsValid设为true
- **MakeVector**(X: number, Y: number, Z: number) -> FVector  — 创建一个向量 {X, Y, Z}
- **BreakVector**(V: FVector) -> number,number,number  — 将向量分解为X、Y和Z分量
- **MakeVector2D**(X: number, Y: number) -> FVector2D  — 创建一个二维向量 {X, Y}
- **BreakVector2D**(V: FVector2D) -> number,number  — 将二维向量分解为X和Y分量
- **GetForwardVector**(InRot: FRotator) -> FVector  — 按给定旋转角度旋转世界前向向量
- **GetRightVector**(InRot: FRotator) -> FVector  — 按给定旋转角度旋转世界右向量
- **GetUpVector**(InRot: FRotator) -> FVector  — 按给定旋转角度旋转世界上向量
- **GetYawPitchFromVector**(V: FVector) -> number,number  — 将向量分解为Yaw(偏航角)和Pitch(俯仰角)旋转值(角度制，不限制范围)
- **MakeRotator**(Roll: number, Pitch: number, Yaw: number) -> FRotator  — 使用以度数为单位提供的旋转值创建旋转器{Roll, Pitch, Yaw}
- **FindLookAtRotation**(Start: FVector, Target: FVector) -> FRotator  — 查找一个物体在起始位置指向目标位置所需的旋转角度
- **MakeRotFromX**(XAxis: FVector) -> FRotator  — 仅使用X轴构建Rotator。Y和Z轴未指定但将保持正交归一。X轴无需归一化
- **MakeRotFromY**(YAxis: FVector) -> FRotator  — 仅使用Y轴构建Rotator。X和Z轴未指定但将保持正交归一。Y轴无需归一化
- **MakeRotFromZ**(ZAxis: FVector) -> FRotator  — 仅使用Z轴构建Rotator。X和Y轴未指定但将保持正交归一。Z轴无需归一化
- **MakeRotFromXY**(XAxis: FVector, YAxis: FVector) -> FRotator  — 使用给定的X和Y轴构建矩阵。X轴保持不变，Y轴会微调以确保正交性。Z轴将被计算得出。输入向量无需归一化
- **MakeRotFromXZ**(XAxis: FVector, ZAxis: FVector) -> FRotator  — 使用给定的X和Z轴构建矩阵。X轴保持不变，Z轴会微调以确保正交性。Y轴将被计算得出。输入向量无需归一化
- **MakeRotFromYX**(YAxis: FVector, XAxis: FVector) -> FRotator  — 使用给定的Y和X轴构建矩阵。Y轴保持不变，X轴会微调以确保正交性。Z轴将被计算得出。输入向量无需归一化
- **MakeRotFromYZ**(YAxis: FVector, ZAxis: FVector) -> FRotator  — 使用给定的Y和Z轴构建矩阵。Y轴保持不变，Z轴会微调以确保正交性。X轴将被计算得出。输入向量无需归一化
- **MakeRotFromZX**(ZAxis: FVector, XAxis: FVector) -> FRotator  — 使用给定的Z和X轴构建矩阵。Z轴保持不变，X轴会微调以确保正交性。Y轴将被计算得出。输入向量无需归一化
- **MakeRotFromZY**(ZAxis: FVector, YAxis: FVector) -> FRotator  — 使用给定的Z和Y轴构建矩阵。Z轴保持不变，Y轴会微调以确保正交性。X轴将被计算得出。输入向量无需归一化
- **BreakRotator**(Rotator: FRotator) -> number,number,number  — 将Rotator分解为{Roll, Pitch, Yaw}角度值(单位:度)
- **MakeTransform**(Location: FVector, Rotation: FRotator, Scale: FVector) -> FTransform  — 根据位置、旋转和缩放创建Transform
- **BreakTransform**(Transform: FTransform) -> FVector,FRotator,FVector  — 将transform分解为{Location, Rotation, Scale}值
- **Conv_VectorToLinearColor**(Vector: FVector) -> FLinearColor  — 将向量转换为LinearColor
- **Conv_ColorToLinearColor**(Color: FColor) -> FLinearColor  — 将Color转换为LinearColor
- **Conv_LinearColorToColor**(LinearColor: FLinearColor) -> FColor  — 将LinearColor转换为Color
- **Conv_VectorToVector2D**(Vector: FVector) -> FVector2D  — 将向量转换为二维向量
- **Conv_Vector2DToVector**(Vector2D: FVector2D) -> FVector  — 将二维向量转换为向量
- **HSVToRGB**(H: number, S: number, V: number, A: number) -> FLinearColor  — 根据HSV分量创建颜色
- **RGBToHSV**(Color: FLinearColor) -> number,number,number,number  — 将颜色分解为单独的HSV分量（以及透明度）
- **Conv_HSVToRGB**(HSV: FLinearColor) -> FLinearColor  — 将HSV线性颜色转换为RGB颜色（其中H在R分量，S在G分量，V在B分量）
- **Conv_RGBToHSV**(RGB: FLinearColor) -> FLinearColor  — 将RGB线性颜色转换为HSV（其中H存储在R分量，S存储在G分量，V存储在B分量）
- **HexToRGB**(HexString: string, bSRGB: boolean) -> FLinearColor  — 将十六进制颜色字符串转换为RGB
- **RGBToHex**(RGB: FLinearColor, bSRGB: boolean) -> string  — 将RGB颜色转换为十六进制字符串
- **Conv_VectorToRotator**(XAxis: FVector) -> FRotator  — 创建一个使X轴朝向指定方向向量的Rotator
- **Conv_RotatorToVector**(Rotator: FRotator) -> FVector  — 获取旋转后的X轴方向向量
- **TransformLocation**(T: FTransform, Location: FVector) -> FVector  — 使用指定的变换矩阵转换位置坐标 例如：若T是某物体的变换矩阵，此操作会将局部坐标系的位置转换到世界坐标系
- **TransformDirection**(T: FTransform, Direction: FVector) -> FVector  — 使用指定的变换矩阵转换方向向量 - 不会改变向量长度 例如：若T是某物体的变换矩阵，此操作会将局部坐标系的方向向量转换到世界坐标系
- **TransformRotation**(T: FTransform, Rotation: FRotator) -> FRotator  — 使用指定的变换矩阵转换Rotator 例如：若T是某物体的变换矩阵，此操作会将局部坐标系的旋转转换到世界坐标系
- **RandomBool**() -> boolean  — 随机返回 true 或 false，概率各占 50%
- **RandomBoolWithWeight**(Weight: number) -> boolean  — 根据指定权重获取随机概率结果。权重范围为 0.0 - 1.0 例如：权重 = 0.6，返回值将有 60% 的概率为 True
- **RandomInteger**(Max: number) -> number  — 返回一个随机数，范围在0到Max - 1之间，每个数出现的概率相同
- **Clamp**(Value: number, Min: number, Max: number) -> number  — 返回限制在A和B之间的值(包含A和B)
- **RandomIntegerInRange**(Min: number, Max: number) -> number  — 返回Min和Max之间的随机整数(包含Min和Max)
- **IsPointInBox**(Point: FVector, BoxOrigin: FVector, BoxExtent: FVector) -> boolean  — 判断给定点是否在盒子内（包括在盒子边界上的点）
- **IsPointInBoxWithTransform**(Point: FVector, BoxWorldTransform: FTransform, BoxExtent: FVector) -> boolean  — 判断给定点是否在具有特定变换的盒子内（包含边界点)
- **EqualRotator**(A: FRotator, B: FRotator, ErrorTolerance: number) -> boolean  — 检查Rotator A 和 B 是否在指定误差范围内相等 (A == B)
- **NotEqualRotator**(A: FRotator, B: FRotator, ErrorTolerance: number) -> boolean  — 检查Rotator A 和 B 是否在指定误差范围内不相等 (A != B)
- **ComposeRotators**(A: FRotator, B: FRotator) -> FRotator  — 组合两个旋转，返回先应用A再应用B的结果旋转
- **GetAxes**(Rotator: FRotator) -> FVector,FVector,FVector  — 获取该旋转对应的前向、右向和上向三个基准方向向量
- **NormalRotator**(A: FRotator) -> FRotator  — 标准化Rotator
- **RandomRotator**(bRoll: boolean) -> FRotator  — 生成一个随机旋转角度，可选择是否包含绕Z轴的随机旋转
- **RLerp**(A: FRotator, B: FRotator, Alpha: number, bShortestPath: boolean) -> FRotator  — 基于Alpha值在A和B之间线性插值（Alpha=0时返回100%A，Alpha=1时返回100%B）

---

### UGCNavigationSystem

寻路导航系统接口库

**分类：** Others

**函数：**

- **BuildNavmesh**(WorldContext: UObject, AgentName: FName) -> void  — 同步生成全地图寻路图, 会阻塞服务器运行 生效范围：服务器
- **AsyncBuildNavmesh**(WorldContext: UObject, AgentName: FName) -> void  — 异步生成全地图寻路图 生效范围：服务器
- **AddDynamicNavAffect**(WorldContext: UObject, AgentName: FName, InBounds: FBox) -> bool  — 添加寻路图动态影响区域，标记后可只针对该区域增量更新寻路 生效范围：服务器
- **AsyncIncrementalBuild**(WorldContext: UObject, AgentName: FName) -> bool  — 区域异步增量生成寻路图，和AddDynamicNavAffect配合使用 生效范围：服务器
- **ProjectPointToNavigation**(WorldContext: UObject, Point: FVector, QueryExtent: FVector) -> bool,FVector  — 投影点到寻路图上的位置 生效范围：服务器
- **GetRandomReachablePointInRadius**(WorldContext: UObject, Origin: FVector, Radius: float) -> bool,FVector  — 范围获取随机可寻路到达点位 生效范围：服务器
- **IsNavigationBeingBuilt**(WorldContext: UObject) -> bool  — 寻路图是否构建 生效范围：服务器
- **GetNavigationGenerationFinishedDelegate**(WorldContext: UObject) -> Delegate  — 获取寻路图生成结束Delegate 生效范围：服务器

---

### UGCPlayerPawnSystem

角色系统接口库

**分类：** Others

**函数：**

- **HasPawnState**(PlayerPawn: PlayerPawn, PawnState: EPawnState) -> boolean  — 是否在指定状态下 生效范围：服务器&客户端
- **AllowPawnState**(PlayerPawn: PlayerPawn, PawnState: EPawnState) -> boolean  — 是否允许进入指定状态 生效范围：服务器&客户端
- **SwitchPoseState**(PlayerPawn: PlayerPawn, PoseState: ESTEPoseState) -> boolean  — 切换 Pose 状态 生效范围：客户端
- **EnterPawnState**(PlayerPawn: PlayerPawn, PawnState: EPawnState) -> boolean  — 进入指定状态 生效范围：服务器&客户端
- **LeavePawnState**(PlayerPawn: PlayerPawn, PawnState: EPawnState) -> boolean  — 离开指定状态 生效范围：服务器&客户端
- **DisabledPawnState**(PlayerPawn: PlayerPawn, PawnState: EPawnState, IsDisabled: boolean) -> void  — 禁用指定状态 生效范围：服务器
- **GetIsFPP**(PlayerPawn: PlayerPawn) -> boolean  — 获取是否第一人称视角 生效范围：服务器&客户端
- **SetIsFPP**(PlayerPawn: PlayerPawn, IsFPP: boolean, bForce: boolean) -> boolean  — 设置是否第一人称视角 生效范围：服务器
- **GetIsTPP**(PlayerPawn: PlayerPawn) -> boolean  — 获取是否第三人称视角 生效范围：服务器&客户端
- **SetIsTPP**(PlayerPawn: PlayerPawn, IsTPP: boolean, bForce: boolean) -> boolean  — 设置是否第三人称视角 生效范围：服务器
- **GetIsInvincible**(PlayerPawn: PlayerPawn) -> boolean  — 获取是否无敌 生效范围：服务器&客户端
- **SetIsInvincible**(PlayerPawn: PlayerPawn, IsInvincible: boolean) -> void  — 设置是否无敌 生效范围：服务器
- **TryEnterParachuteState**(PlayerPawn: PlayerPawn, CheckPawnState: EPawnState[], CanOpenParachuteHeight: number, ForceOpenParachuteHeight: number, CloseParachuteHeight: number, bParachuteAvatarNotShown: boolean) -> void  — 尝试进入跳伞状态 生效范围：服务器
- **ExitParachuteState**(PlayerPawn: PlayerPawn) -> void  — 退出跳伞状态 生效范围：服务器
- **HideBoneByBoneName**(PlayerPawn: PlayerPawn, BoneName: string, bHide: boolean) -> void  — 根据玩家角色的骨骼名称修改骨骼的显隐性 生效范围：客户端
- **SetAvatarVisibility**(PlayerPawn: PlayerPawn, bHide: boolean, ExcludingAvatarSlot: EAvatarSlotType[]) -> void  — 设置角色Avatar的显隐 生效范围：客户端
- **ChangeAvatarMesh**(PlayerPawn: PlayerPawn, SkeletalMesh: UClass|string) -> void  — 切换玩家角色使用的全身骨骼体 生效范围：服务器
- **RecoverAvatarMesh**(PlayerPawn: PlayerPawn) -> void  — 恢复玩家角色使用的全身骨骼体 生效范围：服务器
- **SkipSpawnDeadTombBox**(PlayerPawn: PlayerPawn, bIsSkip: boolean) -> void  — 玩家死亡取消生成盒子 生效范围：服务器
- **GetPartTypeSockets**(Character: ACharacter) -> UPartTypeSocket[]  — 获取角色骨骼里所有的PartTypeSocket 生效范围：服务器&客户端
- **SetDefaultPlayerRespawnPointSelectionMethod**(Method: EUGCPlayerRespawnPointSelectionMethod, RespawnMethodInfo: FVector) -> void  — 设置玩家的默认复活方式 生效范围：服务器
- **SetDefaultPlayerSpawnPointSelectionMethod**(Method: EUGCPlayerSpawnPointSelectionMethod, SpawnMethodInfo: FVector|uint8, PlayerStartInfo: boolean) -> void  — 设置玩家默认的出生方式 生效范围：服务器
- **RespawnPlayer**(PlayerKey: number, RespawnDelayTime: number, IsDestoryAlivePawn: boolean, DestroyDelayTime: number) -> void  — 复活单个角色 生效范围：服务器
- **RespawnAllPlayers**(RespawnDelayTime: number, IsDestroyAlivePawn: boolean, DestroyDelayTime: number) -> void  — 复活所有角色 生效范围：服务器
- **SetRescueInterruptable**(InPawn: PlayerPawn, bCanBeInterrupt: boolean, CanBeInterruptWhenOverRadius: number) -> void  — 设置救援队友是否能被打断 生效范围：服务器
- **SetRescueOtherDuration**(InPawn: PlayerPawn, RescueOtherDuration: number) -> void  — 设置救援队友的时长 生效范围：服务器
- **SetRescuingSelfCDTime**(InPawn: PlayerPawn, RescuingSelfCDTime: number) -> void  — 设置自救的冷却时间 生效范围：服务器
- **ConfirmRescueOther**(InPawn: PlayerPawn, InTargetPawn: PlayerPawn) -> void  — 确认救援队友 生效范围：服务器
- **ConfirmRescueOtherImmediately**(InPawn: PlayerPawn, InTargetPawn: PlayerPawn) -> void  — 确认救援队友并将队友立即救起 生效范围：服务器
- **SetIsDirectlyDie**(InPawn: PlayerPawn, bIsDirectlyDie: boolean) -> void  — 设置玩家倒地后立即死亡 生效范围：服务器
- **DrawOutline**(InPawn: PlayerPawn, bIsDrawOutline: boolean, OutlineThickness: number, OutlineColor: FLinearColor) -> void  — 设置玩家描边 生效范围：客户端
- **AddOcclusionHighlight**(TargetCharacter: ACharacter, Causer: AActor, Type: EPEBuffOcclusionHighlightType, Color: FLinearColor) -> number  — 添加透视效果 生效范围：客户端
- **RemoveOcclusionHighlight**(WorldContextObject: UObject, OcclusionID: number) -> void  — 移除透视效果 生效范围：客户端
- **SetOutputBusVolume**(InPawn: PlayerPawn, Volume: number) -> void  — 修改角色发出的声音音量 生效范围：客户端
- **SetEightWayUniformSpeedEnabled**(InPawn: PlayerPawn, Enable: boolean) -> void  — 设置八向移动相同速度 生效范围：客户端
- **SetUpSubViewTargetServer**(InPawn: PlayerPawn, bSetUp: boolean, TargetActor: AActor, BlendTime: number) -> void  — 设置ViewTarget 生效范围：服务端

---

### UGCStringTextUtility

文本系统接口库

**分类：** Others

**函数：**

- **ExportText**(Object: string) -> string  — 导出对象文本，会根据传入的对象类型打印关键信息
- **TrimStartOrEnd**(InStr: string, TrimStart: boolean, TrimEnd: boolean) -> string  — 修剪字符串的起始和结尾，根据传入的TrimStart和TrimEnd去除字符串头尾的空白字符
- **SplitToArray**(InStr: string, Separator: string) -> table  — 将字符串按照分隔符分割成数组
- **StartsWith**(InStr: string, InPrefix: string, SearchCase: ESearchCase) -> boolean  — 判断字符串是否以指定的前缀开头
- **EndWith**(InStr: string, InSuffix: string, SearchCase: ESearchCase) -> boolean  — 判断字符串是否以指定的后缀结尾
- **InsertIntoString**(SourceStr: string, Content: string, Position: number) -> string  — 在字符串的指定位置插入内容
- **JoinArrayIntoString**(InStrArray: table, Separator: string) -> string  — 将字符串数组连接成字符串
- **SplitToCharArray**(InStr: string) -> table  — 将字符串分割成字符数组
- **ComposedOfDigits**(InStr: string) -> boolean  — 判断字符串是否由数字组成
- **LeftChop**(InStr: string, Count: number) -> string  — 截断字符串的前n个字符
- **LeftPad**(InStr: string, StrLen: number) -> string  — 在字符串的左侧填充空白字符使得字符串长度达到指定的长度
- **RightChop**(InStr: string, Count: number) -> string  — 截断字符串的后n个字符
- **RightPad**(InStr: string, StrLen: number) -> string  — 在字符串的右侧填充空白字符使得字符串长度达到指定的长度
- **LogTree**(Desc: string, Var: any) -> void  — 打印变量,特别是对table类型做树形输出,仅DEV打印

---

### UGCVehicleSystemV2

载具系统接口库V2

**分类：** Others

**函数：**

- **SpawnVehicle**(VehiclePath: string, Location: Vector, Rotation: Rotator, SnapFloor: bool, IsForce: bool) -> ASTExtraVehicleBase  — 使用蓝图路径生成载具 不要在 Spawn 之后立马修改载具位置，等载具落地停稳后再修改，不然位置修改会失败（如果有类似需求，建议直接创建在对应点） 生效范围：服务器
- **DestroyVehicle**(Vehicle: ASTExtraVehicleBase) -> void  — 摧毁载具 生效范围：服务器
- **Respawn**(Vehicle: ASTExtraVehicleBase) -> ASTExtraVehicleBase  — 重生载具 重生将创建新载具，旧的载具将被销毁不再可用 生效范围：服务器
- **EnterVehicle**(Player: PlayerPawn | PlayerController @玩家角色或玩家PlayerController, Vehicle: ASTExtraVehicleBase, SeatIndex: int, IsForce: bool) -> bool  — 玩家角色进入载具 生效范围：服务器&客户端(客户端仅能操作自己的玩家角色)
- **LeaveVehicle**(Player: PlayerPawn | PlayerController @玩家角色或玩家PlayerController, IsForce: bool) -> bool  — 玩家角色离开载具 生效范围：服务器&客户端(客户端仅能操作自己的玩家角色)
- **GetVehicleType**(Vehicle: ASTExtraVehicleBase) -> ESTExtraVehicleBaseType  — 获取载具类型 生效范围：服务器&客户端
- **CanDrive**(Vehicle: ASTExtraVehicleBase) -> bool  — 驾驶员是否可以操控载具 生效范围：服务器&客户端
- **MoveForward**(Vehicle: ASTExtraVehicleBase, Throttle: float) -> void  — 操作载具前进/后退 需要在驾驶员所在客户端每帧调用 当地面载具处于前进状态时，输入后退操作，将执行刹车逻辑，受刹车力量系数(BrakeTorqueCoefficient)影响。 当地面载具处于后退状态时，输入前进操作，也将执行刹车逻辑。 生
- **MoveTurn**(Vehicle: ASTExtraVehicleBase, Throttle: float) -> void  — 操作载具打右方向/左方向 需要在驾驶员所在客户端每帧调用 生效范围：客户端
- **CanHandBrake**(Vehicle: ASTExtraVehicleBase) -> bool  — 获得载具是否支持(急刹)手刹 生效范围：服务器&客户端
- **SetHandBrake**(Vehicle: ASTExtraVehicleBase, BrakeScale: float) -> void  — 操作载具(急刹)手刹 需要在驾驶员所在客户端调用 生效范围：客户端
- **CanBoosting**(Vehicle: ASTExtraVehicleBase) -> bool  — 获得载具能否加速 生效范围：服务器&客户端
- **SetBoosting**(Vehicle: ASTExtraVehicleBase, Open: bool) -> void  — 开关载具加速 需要在驾驶员所在客户端调用 生效范围：客户端
- **CanHorn**(Vehicle: ASTExtraVehicleBase) -> bool  — 获得载具能否按喇叭 生效范围：服务器&客户端
- **SetHorn**(Vehicle: ASTExtraVehicleBase, Open: bool) -> void  — 按下/抬起载具喇叭 需要在驾驶员所在客户端调用 生效范围：客户端
- **GetVelocity**(Vehicle: ASTExtraVehicleBase) -> FVector  — 获得载具当前速度(单位是cm/s) 生效范围：服务器&客户端
- **GetVehicleHealthState**(Vehicle: ASTExtraVehicleBase) -> ESTExtraVehicleHealthState  — 获得当前载具健康状态 生效范围：服务器&客户端
- **CanDamage**(Vehicle: ASTExtraVehicleBase) -> bool  — 获得载具是否能受到伤害 生效范围：服务器
- **SetCanDamage**(Vehicle: ASTExtraVehicleBase, CanDamage: bool) -> void  — 设置载具是否能受到伤害 生效范围：服务器
- **GetSeatNum**(Vehicle: ASTExtraVehicleBase) -> int  — 获取座位数量 生效范围：服务器
- **GetSeatDataByIndex**(Vehicle: ASTExtraVehicleBase, SeatIndex: int) -> UGCVehicleSeatData  — 获取座位数据 生效范围：服务器
- **GetAllSeatDatas**(Vehicle: ASTExtraVehicleBase) -> UGCVehicleSeatData[]  — 获取所有座位数据 生效范围：服务器
- **ChangePassengerSeat**(Player: PlayerPawn | PlayerController @玩家角色或玩家PlayerController, SeatIndex: number) -> bool  — 改变玩家乘客的座位 生效范围：服务器&客户端 (客户端执行只能指定空位，否则会失败。服务端执行可以指定有乘客的座位，两人互相交换位置。)
- **StartFireVehicleWeapon**(Vehicle: ASTExtraVehicleBase) -> void  — 车载武器开始攻击 仅限驾驶位车载武器生效 生效范围：客户端

---

### UGC_Backpack_Item_UIBP

背包格子控件

@class UGC_Backpack_Item_UIBP_C:UUserWidget
@field CanvasPanel_Lock UCanvasPanel
@field CanvasPanel_Replace UCanvasPanel
@field UGC_Common_Item_UIBP UUGC_Common_Item_UIBP_C
@field CanvasPanel_New UCanvasPanel
@field UGCCommonDragDropItem UUGCCommonDragDropItem_C
@field HorizontalBox_Unlock UHorizontalBox
@field Text_UnlockCurrencyNum UTextBlock
@field TextBlock_Num UTextBlock
@field Image_Currency UImage

**分类：** Others

**函数：**

- **ShowSelected**(bSelect: boolean) -> void  — 格子显示选中状态
- **UpdateItemData**(ItemDefineID: ItemDefineID, Count: number, AdditionData: table) -> void  — 更新格子数据(!!!)
- **UpdateDragData**(DragType: string, DragDirectionMode: EDragDropDirectionMode, DragClickCallback: function, DragStartCallback: function, DragCancelCallback: function) -> void  — 更新格子拖拽数据(!!!)
- **UpdateItemState**(State: EBackpackItemState) -> void  — 更新格子解锁状态
- **SetCustomUIList**(SoftWidgetPaths: FSoftClassPath[], PostCallback: function) -> void  — 设置格子叠加UI
- **SetUnlockInfo**(bShow: boolean, CoinID: number, CostNum: number) -> void  — 显示解锁信息
- **GetUIData**() -> table  — 控件的UI数据
- **SetIsNewItem**(bNew: boolean) -> void  — 显示 新 标记

---

### UUGCBackpackAvatarHandle

外显装备基类

**分类：** Others

**继承：** UBackpackAvatarHandle, IUGCItemDataInterface, IUGCObjectItemTableInterface, IUGCItemEquipmentInterface, IUGCItemEquipTargetInterface, IUGCCommonDeadDropItemInterface, IUGCBattleEquipHandleAttachInterface


---

### UUGCCommonProduceDropItemComponent

掉落组件

**分类：** Others

**继承：** UCommonProduceDropItemBaseComponent, IObjectPoolInterface

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| StepTime | int32 | 每波掉落次数 |
| StepGap | float | 每波掉落间隔 |
| DelayDropTime | float | 起始掉落延迟 |
| StrategySelector | FUGCDropItemStrategySelector | 掉落方案配置 |

**函数：**

- **StartDrop**(DropItemActor: AActor *, Killer: AController *, TraceIgnoreActors: TArray < AActor * >, AttachComponent: USceneComponent *) -> void  — 按照配置进行一次掉落行为    生效范围：服务器
- **StartDropByProduceID**(ProduceID: int32, ProduceGroupID: int32, EntityType: EUGCGenerateItemEntityType, RelatedPlayer: ACharacter *) -> void  — 指定掉落方案进行一次 Wrapper 掉落    生效范围：服务器
- **SetBluePrintDropItemConfig**(ConfigItem: TArray < FUGCGenerateDropItemInfo >, EntityType: EUGCGenerateItemEntityType, ConfigID: int32) -> void  — 动态设置掉落物组，会强制将掉落物列表生成方式改为蓝图配置    生效范围：服务器
- **SetProduceIDConfig**(InProduceID: int32, ProduceGroupID: int32, EntityType: EUGCGenerateItemEntityType, ConfigID: int32) -> void  — 动态设置掉落串，会强制将掉落物列表生成方式改为读表    生效范围：服务器
- **AddDropConfig**(InProduceID: int32, ProduceGroupID: int32, ConfigItem: TArray < FUGCGenerateDropItemInfo >, EntityType: EUGCGenerateItemEntityType) -> void  — 动态添加掉落，按照选择类型添加    生效范围：服务器
- **ClearDropConfig**(SelectType: EUGCDropItemListGeneratorType) -> void  — 动态清空配置，蓝图或读表    生效范围：服务器
- **SetGeneratorType**(SelectType: EUGCDropItemListGeneratorType) -> void  — 动态修改掉落物列表生成方式    生效范围：服务器
- **SetDynamicCenterOffset**(InDynamicCenterOffset: FVector) -> void  — 动态设置掉落圆环偏移       生效范围：服务器

---

### UUGCGamePartConfig

GamePart配置基类

**分类：** Others

**继承：** UPrimaryDataAsset

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| GamePartName | FName | GamePart名称 |
| DependentGameParts | TArray < FName > | 依赖的的GamePart列表 |
| GlobalActorClass | TSubclassOf < AActor > | GlobalActor类配置 |
| PlayerComponentConfigs | TArray < FUGCGamePartPlayerComponentConfig > | GamePart PlayerComponent配置列表 |


---

### UUGCItemWarehouseBase

仓库对象

**分类：** Others

**继承：** UObject, IUGCItemContainerInterface


---

### UUGCMotionComponent

运动器组件

**分类：** Others

**继承：** UActorComponent

**函数：**

- **StartMotion**(ConfigID: int) -> void  — 开始运行特定运动器   生效范围S
- **PauseMotion**(ConfigID: int) -> void  — 停止特定运动器   生效范围S
- **ResetMotion**(ConfigID: int) -> void  — 重置特定运动器   生效范围S

---

### ASTExtraGameStateBase

游戏状态基类

**分类：** Others

**继承：** AUAEGameState, IUAELevelEventCenterInterface, IImmediateUIInterface


---

### ASTExtraShootWeapon

射击武器类

**分类：** Others

**继承：** ASTExtraWeapon


---

### USTExtraGameMagnitudeCalculation

伤害公式

**分类：** Others

**继承：** UGameMagnitudeCalculationBase, ILocalCalculationVariableSupportInterface

**函数：**

- **IsHeadDamage**(Context: FGameMagnitudeContext &) -> bool  — 获取是否是爆头伤害

---

### FUserActivity

The description of a user activity

**变量：**

| 名称 | 类型 | 说明 |
|------|------|------|
| ActionName | FString | Describes the user's activity |


---

## 枚举（Enums）

### EActivityClientRecoverType

| 名称 | 值 | 说明 |
|------|------|------|
| Recover_None | 0 |  |
| Recover_NewActor | 1 |  |
| Recover_NetLoss | 2 |  |
| Recover_ApplicationReactivated | 3 |  |
| Recover_ObChange | 4 |  |
| Recover_ReInitForReplay | 5 |  |
| Recover_RelvantForReplay | 6 |  |

---

### EActivityEctypeQuitReason

| 名称 | 值 | 说明 |
|------|------|------|
| Normal | 1 |  |
| Interrupt | 2 |  |

---

### EActivityUIShowMode

| 名称 | 值 | 说明 |
|------|------|------|
| EShowMode_OnlyLocal | -1 |  |
| EShowMode_OnlyOB | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| EShowMode_OnlyReplay | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| EShowMode_LocalAndOB | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| EShowMode_LocalAndReplay | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| EShowMode_OBAndReplay | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| EShowMode_All | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |

---

### EConcertActivityType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |

---

### EDynamicWeatherExMgrActivityStatus

| 名称 | 值 | 说明 |
|------|------|------|
| Begin | 0 |  |
| End | 1 |  |

---

### EGT_TestActivityEvent

| 名称 | 值 | 说明 |
|------|------|------|
| TestOver | 1 |  |

---

### EHomelandActivityState

| 名称 | 值 | 说明 |
|------|------|------|
| Default | 0 |  |
| Active_State_One | 1 |  |
| Active_State_Two | 2 |  |
| Active_State_Three | 3 |  |
| Active_State_Four | 4 |  |

---

### ENewYearActivityEventType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| ReadyTime | 1 |  |
| StartLight | 2 |  |
| StartQTE | 3 |  |
| EndQTE | 4 |  |
| StartDropItem | 5 |  |
| EndDropItem | 6 |  |
| StartSpawnActor | 7 |  |
| EndSpawnActor | 8 |  |
| GameEnd | 9 |  |
| LightGravityBegin | 10 |  |
| LightGravityEnd | 11 |  |
| TriggerRainBegin | 12 |  |
| TriggerCreatePiano | 13 |  |
| TriggerPianoBegin | 14 |  |
| TriggerPianoEnd | 15 |  |
| Piano1 | 16 |  |
| Piano2 | 17 |  |
| Piano3 | 18 |  |
| Piano4 | 19 |  |
| Piano5 | 20 |  |
| Piano6 | 21 |  |
| TriggerAddPortalUI | 22 |  |
| TriggerPortalBegin | 23 |  |
| TriggerDanceBegin | 25 |  |
| TriggerDanceEnd | 26 |  |
| TriggerSagmentSequenceStart | 27 |  |
| TriggerSagmentSequenceEnd | 28 |  |
| StartVideo | 29 |  |
| WindTunnelFlyingBegin | 30 |  |
| BalloonsBegin | 31 |  |
| TriggerRainEnd | 33 |  |
| StartMusicGame | 34 |  |

---

### ESTExtraBuffAction_PostAKEvent_AttachTo

| 名称 | 值 | 说明 |
|------|------|------|
| Pawn | 0 |  |
| Controller | 1 |  |

---

### ESTExtraCharToVehiclePer

| 名称 | 值 | 说明 |
|------|------|------|
| ECharacter_DirverAndPassenger | 0 |  |
| ECharacter_OnlyPassenger | 1 |  |
| ECharacter_CannotGetIn | 2 |  |
| ECharacter_Error | 3 |  |

---

### ESTExtraDoorMachineCameraMode

| 名称 | 值 | 说明 |
|------|------|------|
| Shooting | 0 |  |
| Driving | 1 |  |

---

### ESTExtraDoorMachineState

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Charging | 1 |  |
| Follow | 2 |  |
| Dash | 3 |  |

---

### ESTExtraDumpBoxState

| 名称 | 值 | 说明 |
|------|------|------|
| VWS_Normal | 0 |  |
| VWS_Raising | 1 |  |
| VWS_Raised | 2 |  |
| VWS_Lowering | 3 |  |
| VWS_StopRaising | 4 |  |
| VWS_StopLowering | 5 |  |

---

### ESTExtraGlideCarGlideState

| 名称 | 值 | 说明 |
|------|------|------|
| Land | 0 |  |
| Acceleration | 1 |  |
| Glide | 2 |  |

---

### ESTExtraHammerSharkInWaterState

| 名称 | 值 | 说明 |
|------|------|------|
| EHSIWS_Air | 0 |  |
| EHSIWS_Touch | 1 |  |
| EHSIWS_InWater | 2 |  |

---

### ESTExtraHammerSharkRepairCheckResult

| 名称 | 值 | 说明 |
|------|------|------|
| EHSRCR_Success | 0 |  |
| EHSRCR_Already | 1 |  |
| EHSRCR_CD | 2 |  |
| EHSRCR_OverSpeed | 3 |  |
| EHSRCR_FullyHP | 4 |  |
| EHSRCR_BP | 5 |  |

---

### ESTExtraHammerSharkRepairState

| 名称 | 值 | 说明 |
|------|------|------|
| EHSRS_Default | 0 |  |
| EHSRS_Strating | 1 |  |
| EHSRS_Repairing | 2 |  |
| EHSRS_Ending | 3 |  |

---

### ESTExtraLockedVehicleStatus

| 名称 | 值 | 说明 |
|------|------|------|
| ESOnlyOwnerCanDriver | 0 |  |
| EStrangerCannotGetIn | 1 |  |
| EStrangerOnlyPassenger | 2 |  |
| ETeamMateCanBeDriverAndPassenger | 3 |  |
| ESUnlockVehicle | 100 |  |

---

### ESTExtraPenguinVehicleState

| 名称 | 值 | 说明 |
|------|------|------|
| EPVS_Default | 0 |  |
| EPVS_Inflating | 1 |  |
| EPVS_Expanded | 2 |  |
| EPVS_DeflatingAndBoost | 3 |  |
| EPVS_DeflatingAndFlyAway | 4 |  |
| EPVS_EndDeflating | 5 |  |
| EPVS_Max | 6 |  |

---

### ESTExtraTankControlMode

| 名称 | 值 | 说明 |
|------|------|------|
| TCM_JOYSTICK | 0 |  |
| TCM_LOCK_BOOST | 1 |  |

---

### ESTExtraTankMovementMode

| 名称 | 值 | 说明 |
|------|------|------|
| TMM_PIVOTCIRCLE | 0 |  |
| TMM_LOCKTRACK | 1 |  |
| TMM_NOINPUTTRACK | 2 |  |

---

### ESTExtraUAVVehicleOperateState

| 名称 | 值 | 说明 |
|------|------|------|
| Operate_Normal | 0 |  |
| Operate_WithUp | 1 |  |
| Operate_WithDown | 2 |  |
| Operate_Clear | 3 |  |

---

### ESTExtraUAVVehicleState

| 名称 | 值 | 说明 |
|------|------|------|
| UAVS_Init | 0 |  |
| UAVS_Using | 1 |  |
| UAVS_StandBy | 2 |  |
| UAVS_PowerOff | 3 |  |
| UAVS_Recalling | 4 |  |
| UAVS_Disappearing | 5 |  |
| UAVS_Destroy | 6 |  |
| UAVS_SelfDestruct | 7 |  |
| UAVS_InWater | 8 |  |
| UAVS_Max | 9 |  |

---

### ESTExtraVehicleAnimalType

| 名称 | 值 | 说明 |
|------|------|------|
| NONE | 0 |  |
| Animal_SnowLeopard | 1 |  |
| Animal_Capybara | 2 |  |
| Animal_Owl | 3 |  |
| Animal_Panda | 4 |  |

---

### ESTExtraVehicleBaseType

| 名称 | 值 | 说明 |
|------|------|------|
| VBT_WheeledVehicle | 0 |  |
| VBT_Motorbike | 1 |  |
| VBT_Amphibious | 2 |  |
| VBT_Helicopter | 3 |  |
| VBT_FloatingVehicle | 4 |  |
| VBT_Horse | 5 |  |
| VBT_Aircraft | 6 |  |
| VBT_Other | 7 |  |

---

### ESTExtraVehicleCruiseControlState

| 名称 | 值 | 说明 |
|------|------|------|
| VCCS_None | 0 |  |
| VCCS_ShowUI | 1 |  |
| VCCS_NormalCruise | 2 |  |
| VCCS_BoostCruise | 3 |  |

---

### ESTExtraVehicleDampingState

| 名称 | 值 | 说明 |
|------|------|------|
| VDS_AIR | 0 |  |
| VDS_WATER | 1 |  |
| VDS_LAND | 2 |  |

---

### ESTExtraVehicleEnjoyVoiceType

| 名称 | 值 | 说明 |
|------|------|------|
| ESTVEVT_None | 0 |  |
| ESTVEVT_WelcomeToOwner | 1 |  |
| ESTVEVT_WelcomeToPassenger | 2 |  |
| ESTVEVT_ScanSignalCircle | 3 |  |
| ESTVEVT_CheckVehicleStatus | 4 |  |

---

### ESTExtraVehicleHealthState

| 名称 | 值 | 说明 |
|------|------|------|
| VHS_Good | 0 |  |
| VHS_Smoking | 1 |  |
| VHS_Burning | 2 |  |
| VHS_Destroyed | 3 |  |

---

### ESTExtraVehicleSeatType

| 名称 | 值 | 说明 |
|------|------|------|
| ESeatType_DriversSeat | 0 |  |
| ESeatType_PassengersSeat | 1 |  |
| ESeatType_FreeFiringLeftSeat | 2 |  |
| ESeatType_FreeFiringRightSeat | 3 |  |
| ESeatType_GunnerSeat | 4 |  |
| ESeatType_VirtualDriverSeat | 5 |  |
| ESeatType_DriverShoot | 6 |  |
| ESeatType_DriverProxySeat | 7 |  |
| ESeatType_Max | 8 |  |

---

### ESTExtraVehicleShootWeaponHoldType

| 名称 | 值 | 说明 |
|------|------|------|
| VSWT_FirstWeapon | 0 |  |
| VSWT_SecondaryWeapon | 1 |  |
| VSWT_None | 2 |  |

---

### ESTExtraVehicleShootWeaponTypeAtDriverSeat

| 名称 | 值 | 说明 |
|------|------|------|
| VSWT_Flamethrower | 0 |  |
| VSWT_TankRPG | 1 |  |
| VSWT_Gatlin | 2 |  |
| VSWT_HelicopterGatlin | 3 |  |
| VSWT_HelicopterRPG | 4 |  |
| VSWT_CoaxialGatlin | 5 |  |
| VSWT_None | 6 |  |

---

### ESTExtraVehicleStates

| 名称 | 值 | 说明 |
|------|------|------|
| EVS_NONE | 0 |  |
| EVS_SPEED | 1 |  |
| EVS_ELECTRONIC_FAILURE | 2 |  |
| EVS_INVINCIBLE | 3 |  |
| EVS_MAX | 4 |  |

---

### ESTExtraVehicleSyncState

| 名称 | 值 | 说明 |
|------|------|------|
| VSS_None | 0 |  |
| VSS_Client | 1 |  |
| VSS_ServerAuthorize | 2 |  |

---

### ESTExtraVehicleType

| 名称 | 值 | 说明 |
|------|------|------|
| VT_Unknown | 0 |  |
| VT_Motorbike_0 | 1 |  |
| VT_Motorbike_1 | 2 |  |
| VT_Motorbike_SideCart_0 | 3 |  |
| VT_Motorbike_SideCart_1 | 4 |  |
| VT_Dacia_0 | 5 |  |
| VT_Dacia_1 | 6 |  |
| VT_Dacia_2 | 7 |  |
| VT_Dacia_3 | 8 |  |
| VT_UAZ_0 | 9 |  |
| VT_UAZ_1 | 10 |  |
| VT_UAZ_2 | 11 |  |
| VT_Buggy_0 | 12 |  |
| VT_Buggy_1 | 13 |  |
| VT_Buggy_2 | 14 |  |
| VT_PG117 | 15 |  |
| VT_Aquarail | 16 |  |
| VT_MiniBus_1 | 17 |  |
| VT_MiniBus_2 | 18 |  |
| VT_MiniBus_3 | 19 |  |
| VT_PickUp_1 | 20 |  |
| VT_PickUp_2 | 21 |  |
| VT_PickUp_3 | 22 |  |
| VT_PickUp_4 | 23 |  |
| VT_PickUp_5 | 24 |  |
| VT_PickUp_6 | 25 |  |
| VT_PickUp_7 | 26 |  |
| VT_PickUp_8 | 27 |  |
| VT_PickUp_9 | 28 |  |
| VT_PickUp_10 | 29 |  |
| VT_Buggy_4 | 30 |  |
| VT_Buggy_5 | 31 |  |
| VT_Buggy_6 | 32 |  |
| VT_Mirado_Close_1 | 33 |  |
| VT_Mirado_Close_2 | 34 |  |
| VT_Mirado_Close_3 | 35 |  |
| VT_Mirado_Close_4 | 36 |  |
| VT_Mirado_Open_1 | 37 |  |
| VT_Mirado_Open_2 | 38 |  |
| VT_Mirado_Open_3 | 39 |  |
| VT_Mirado_Open_4 | 40 |  |
| VT_UAZ04 | 41 |  |
| VT_Rony_1 | 42 |  |
| VT_Rony_2 | 43 |  |
| VT_Rony_3 | 44 |  |
| VT_Scooter | 45 |  |
| VT_Surfboard | 46 |  |
| VT_UH60 | 47 |  |
| VT_Amphibious | 48 |  |
| VT_TUK | 49 |  |
| VT_Snowboard | 50 |  |
| VT_UAV | 51 |  |
| VT_Telecar | 52 |  |
| VT_UCAV | 53 |  |
| VT_Tank | 54 |  |
| VT_DragonBoat | 55 |  |
| VT_Tesla | 56 |  |
| VT_ExtraMount | 57 |  |
| VT_Motorglider | 58 |  |
| VT_Battleship | 59 |  |
| VT_LootTruck | 60 |  |
| VT_CoupeRB | 61 |  |
| VT_TanabataBalloon | 62 |  |
| VT_ATGMotorCycle | 63 |  |
| VT_LaserSailBoat | 64 |  |
| VT_AirTaxi | 65 |  |
| VT_Kayak | 66 |  |
| VT_BlackCatMotor | 67 |  |
| VT_GZChickenTank | 68 |  |
| VT_NewYearSnowboard | 69 |  |
| VT_GravitySimulationSnowboard | 70 |  |
| VT_Horse | 71 |  |
| VT_LionDance | 72 |  |
| VT_DragonCart | 73 |  |
| VT_ForkLift | 74 |  |
| VT_SciFiMoto | 75 |  |
| VT_Bicycle | 76 |  |
| VT_StationWagon | 77 |  |
| VT_FRCCar | 78 |  |
| VT_ATGCar | 79 |  |
| VT_KiteFlyer | 80 |  |
| VT_Drift | 81 |  |
| VT_SplicedTrain | 82 |  |
| VT_Handcart | 83 |  |
| VT_ATV | 84 |  |
| VT_4SportCar | 85 |  |
| VG_MaglevAircraft | 86 |  |
| VT_Chariot | 87 |  |
| VT_LanternRacing | 88 |  |
| VT_SixWing | 89 |  |
| VT_Bigfoot | 90 |  |
| VT_LadaNiva | 91 |  |
| VT_Snowbike | 92 |  |
| VT_Snowmobile | 93 |  |
| VT_ArmedDacia | 94 |  |
| VT_ArmedBuggy | 95 |  |
| VT_ArmedPickup | 96 |  |
| VT_ArmedUAZ | 97 |  |
| VT_ArmedUH60 | 98 |  |
| VT_ArmedMotorbike_SideCart | 99 |  |
| VT_TrackVehicle | 100 |  |
| VT_FPVDrone | 101 |  |
| VT_BombDrone | 102 |  |
| VT_BF_AH6 | 103 |  |
| VT_BF_UH60 | 104 |  |
| VT_BF_UAZ | 105 |  |
| VT_MotorBoat_GZJ | 106 |  |
| VT_BF_Attack_Tank | 107 |  |
| VT_BF_Defence_Tank | 108 |  |
| VT_BF_Mi28 | 109 |  |
| VT_ReconDrone | 110 |  |
| VT_BF_ATV | 111 |  |
| VT_BF_BRDM | 112 |  |
| VT_Mooncake_Boat | 113 |  |
| VT_Mooncake_Balloon | 114 |  |
| VT_DesertCar | 115 |  |
| VT_AirBag | 116 |  |
| VT_SnowLeopard | 117 |  |
| VT_Mammoth | 118 |  |
| VT_BaseCar | 119 |  |
| VT_BF_AmphibousTank | 120 |  |
| VT_LostMobile | 121 |  |
| VT_AssaultCar | 122 |  |
| VT_Missile | 123 |  |
| VT_Excavator | 124 |  |
| VT_Kite | 125 |  |
| VT_DoorMachine | 126 |  |
| VT_HugeMouthJet | 127 |  |
| VT_Blanc | 128 |  |
| VT_PicoBus | 129 |  |
| VT_AICar | 130 |  |
| VT_DumpTruck | 131 |  |
| VT_BFV_AssaultCar | 132 |  |
| VT_BFV_AntiAirTank | 133 |  |
| VT_Excavator_RD | 134 |  |
| VT_PELAICar | 135 |  |
| VT_HammerHeadShark | 136 |  |
| VT_NezhaLotus | 137 |  |
| VT_SuperMode_PilotUAV | 138 |  |
| VT_Sleigh | 139 |  |
| VT_Hovercraft | 140 |  |
| VT_IceCarriage | 141 |  |
| VT_BBCar | 142 |  |
| VT_SeaPlane | 143 |  |
| VT_Snowball | 144 |  |
| VT_FlyHorse | 145 |  |
| VT_EV3F4 | 146 |  |
| VT_BlackHawkTransport | 147 |  |
| VT_Paraglider | 148 |  |
| VT_SandBoat | 149 |  |
| VT_CamelCaravan | 150 |  |
| VT_IceCarriageHorse | 151 |  |
| VT_Penguin | 152 |  |
| VT_9ColorDeer | 153 |  |
| VT_FlyHorseFromHorse | 154 |  |
| VT_TheSixBoat | 155 |  |
| VT_Deer | 156 |  |

---

### ESTExtraVehicleUserState

| 名称 | 值 | 说明 |
|------|------|------|
| EVUS_OutOfVehicle | 0 |  |
| EVUS_AsDriver | 1 |  |
| EVUS_ASPassenger | 2 |  |

---

### ESTExtraVehicleWheelIconType

| 名称 | 值 | 说明 |
|------|------|------|
| VWheelIcon_None | 0 |  |
| VWheelIcon4W_1 | 1 |  |
| VWheelIcon4W_2 | 2 |  |
| VWheelIcon4W_3 | 3 |  |
| VWheelIcon2W_1 | 4 |  |
| VWheelIcon3W_1 | 5 |  |
| VWheelIcon3W_2 | 6 |  |

---

### ESTExtraVehicleWindowState

| 名称 | 值 | 说明 |
|------|------|------|
| VWS_Opening | 0 |  |
| VWS_Opened | 1 |  |
| VWS_Closing | 2 |  |
| VWS_Closed | 3 |  |
| VWS_Destroied | 4 |  |

---

### ESTExtraWheeledMovementType

| 名称 | 值 | 说明 |
|------|------|------|
| WMT_4W | 0 |  |
| WMT_NW | 1 |  |
| WMT_Tank | 2 |  |

---

### ESTExtraZiplineDirection

| 名称 | 值 | 说明 |
|------|------|------|
| A2B | 0 |  |
| B2A | 1 |  |
| Both | 2 |  |

---

### EUGCAIAmmoEnoughType

| 名称 | 值 | 说明 |
|------|------|------|
| ClipAmmo | 0 |  |
| BackpackAmmo | 1 |  |
| Max | 2 |  |

---

### EUGCAITakeMedicineType

| 名称 | 值 | 说明 |
|------|------|------|
| Bandage | 0 |  |
| Painkiller | 1 |  |
| AdrenalineSyringe | 2 |  |
| FirstAidKit | 3 |  |
| MedKit | 4 |  |
| EnergyDrink | 5 |  |
| Max | 6 |  |

---

### EUGCAIThrowProjectilePhase

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| SwitchWeapon | 1 |  |
| BeforeThrow | 2 |  |
| AfterThrow | 3 |  |

---

### EUGCActivityTaskResetType

| 名称 | 值 | 说明 |
|------|------|------|
| DailyReset | 1 |  |
| WeeklyReset | 2 |  |
| MonthlyReset | 3 |  |
| NotReset | 4 |  |

---

### EUGCActivityType

| 名称 | 值 | 说明 |
|------|------|------|
| Task | 1 |  |
| SignIn | 2 |  |

---

### EUGCAddItemReason

| 名称 | 值 | 说明 |
|------|------|------|
| Default | 0 |  |
| Initialize | 1 |  |
| Transfer | 2 |  |
| Pickup | 3 |  |

---

### EUGCAnimPlayType

| 名称 | 值 | 说明 |
|------|------|------|
| Anim_None | 0 |  |
| BaseAnim | 1 |  |
| BaseBlendAnim | 2 |  |
| BlendAnim | 3 |  |
| CustomAnim | 4 |  |

---

### EUGCBattlePhase

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Matching | 1 |  |
| Prepare | 2 |  |
| InGame | 4 |  |
| End | 8 |  |
| All | -1 |  |

---

### EUGCCampSpawnPointSelectionMethod

| 名称 | 值 | 说明 |
|------|------|------|
| DesignatedCampSpawnLocation | 0 |  |
| DesignatedCampPlayerStartID | 1 |  |

---

### EUGCChooseEnemyStrategy

| 名称 | 值 | 说明 |
|------|------|------|
| Nearest | 0 |  |
| RangeRandom | 1 |  |

---

### EUGCChooseEnemyType

| 名称 | 值 | 说明 |
|------|------|------|
| Player | 0 |  |
| Monster | 1 |  |
| PlayerAndMonster | 2 |  |
| MonsterAndPlayer | 3 |  |

---

### EUGCCommodityCommandType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Buy | 1 |  |
| Use | 2 |  |
| Compensate | 3 |  |
| Redeem | 4 |  |
| ClaimMail | 5 |  |

---

### EUGCCommodityResponseType

| 名称 | 值 | 说明 |
|------|------|------|
| OrderID | 1 |  |
| CommodityID_Count | 2 |  |
| RechargeResult | 3 |  |
| TicketChanged | 4 |  |
| ActiveCoinChanged | 5 |  |

---

### EUGCCommonItemReason

| 名称 | 值 | 说明 |
|------|------|------|
| Default | 0 |  |
| Initialize | 1 |  |
| Transfer | 2 |  |
| Pickup | 3 |  |
| ExceedCellCapacity | 4 |  |
| SortOut | 5 |  |
| OnlySkipCheckCanAddItem | 100 |  |
| OnlySkipCheckCanRemoveItem | 101 |  |
| NoTips | 102 |  |
| SkipCheckCanAddItem_NoTips | 103 |  |
| SkipExceedCellCapacity | 104 |  |

---

### EUGCCommonItemRepType

| 名称 | 值 | 说明 |
|------|------|------|
| Insert | 0 |  |
| Update | 1 |  |
| Delete | 2 |  |
| UpdateReplicated | 255 |  |

---

### EUGCCompareAngleType

| 名称 | 值 | 说明 |
|------|------|------|
| EUGCAngleGreater | 0 |  |
| EUGCAngleLess | 1 |  |
| EUGCAngleEequal | 2 |  |

---

### EUGCCrossHairPresetType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Rifle | 1 |  |
| ShotGun | 2 |  |
| Pistol | 3 |  |
| Other | 4 |  |

---

### EUGCCustomModeInputReason

| 名称 | 值 | 说明 |
|------|------|------|
| UCMIR_Look | 0 |  |
| UCMIR_Skill | 1 |  |
| UCMIR_AutoAim | 2 |  |
| UCMIR_Movement | 3 |  |
| UCMIR_Max | 4 |  |

---

### EUGCDeadDropType

| 名称 | 值 | 说明 |
|------|------|------|
| DeadBox | 0 |  |
| Scatter | 1 |  |
| NoAll | 2 |  |

---

### EUGCDropItemListGeneratorType

| 名称 | 值 | 说明 |
|------|------|------|
| DropItemListGeneratorType_ItemTable | 0 |  |
| DropItemListGeneratorType_BluePrint | 1 |  |

---

### EUGCDropItemPositionDirection

| 名称 | 值 | 说明 |
|------|------|------|
| DropItemPositionDirection_Random | 0 |  |
| DropItemPositionDirection_PseudoRandom | 1 |  |
| DropItemPositionDirection_FacePlayer | 2 |  |

---

### EUGCEnemyHatredMaxDistanceType

| 名称 | 值 | 说明 |
|------|------|------|
| Default | 0 |  |
| Plus | 1 |  |
| Multiply | 2 |  |

---

### EUGCExceptionFlags

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| XPCALL | -1 |  |
| MessageBox | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| NormalLog | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| FightingLog | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| All | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |

---

### EUGCExceptionVerbosity

| 名称 | 值 | 说明 |
|------|------|------|
| Error | 0 |  |
| Warning | 1 |  |
| Log | 2 |  |

---

### EUGCFoliageDistribution

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Uniform | 1 |  |
| Random | 2 |  |
| CenterSqure | 3 |  |

---

### EUGCFoliageMode

| 名称 | 值 | 说明 |
|------|------|------|
| Add | 0 |  |
| Erase | 1 |  |

---

### EUGCGenerateItemEntityType

| 名称 | 值 | 说明 |
|------|------|------|
| GenerateItemEntity_BackPack | 0 |  |
| GenerateItemEntity_WrapperActor | 1 |  |
| GenerateItemEntity_TombBox | 2 |  |

---

### EUGCHPBarShowMode

| 名称 | 值 | 说明 |
|------|------|------|
| Always | 0 |  |
| TakeDamage | 1 |  |
| BeAimAt | 2 |  |
| LockPlayer | 3 |  |

---

### EUGCHatredType

| 名称 | 值 | 说明 |
|------|------|------|
| Sense | 0 |  |
| Damage | 1 |  |

---

### EUGCItemChangeType

| 名称 | 值 | 说明 |
|------|------|------|
| ItemChangeType_Add | 0 |  |
| ItemChangeType_Update | 1 |  |
| ItemChangeType_Remove | 2 |  |

---

### EUGCItemGAActiveCondition

| 名称 | 值 | 说明 |
|------|------|------|
| ActiveOnPickup | 1 |  |
| ActiveOnUse | 2 |  |
| ActiveOnEquip | 3 |  |
| ActiveOnManual | 255 |  |

---

### EUGCItemSpawnerConfigMode

| 名称 | 值 | 说明 |
|------|------|------|
| ItemID | 0 |  |
| DropTable | 1 |  |
| DropGroupTable | 2 |  |
| Custom | 3 |  |

---

### EUGCItemSpawnerManagerStartCondition

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Event | 1 |  |
| FunctionCall | 2 |  |

---

### EUGCMBindErrorCode

| 名称 | 值 | 说明 |
|------|------|------|
| OK | 0 |  |
| CANNOT_BINDSELF | 1 |  |
| PARENT_ISNIL | 2 |  |
| PARENT_DISABLE | 3 |  |
| CHILD_DISABLE | 4 |  |
| CANNOT_BIND_COMBINECHILD | 5 |  |
| CANNOT_BIND_OUTSIDECHILD | 6 |  |
| CANNOT_BIND_OTHERCOMBINE | 7 |  |
| ALWAYS_HASPARENT | 8 |  |
| CANNOT_CYCLE | 9 |  |
| DEPTHMAX | 10 |  |
| PARENT_DISABLE_COMBINE | 11 |  |
| CANNOT_BIND_EDITCOMBCHILD | 12 |  |

---

### EUGCMBrushType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Height | 1 |  |
| Smooth | 2 |  |
| Flatten | 3 |  |
| Erosion | 4 |  |
| Fixed | 5 |  |
| Texture | 6 |  |
| Foliage | 7 |  |

---

### EUGCMCaptureMoveMode

| 名称 | 值 | 说明 |
|------|------|------|
| FOCUS | 0 |  |
| AUTO | 1 |  |

---

### EUGCMDSWaitingExtraState

| 名称 | 值 | 说明 |
|------|------|------|
| CosData | 0 |  |
| NavData | 1 |  |

---

### EUGCMInstigatorType

| 名称 | 值 | 说明 |
|------|------|------|
| Player | 0 |  |
| Vehicle | 1 |  |
| Primitive | 2 |  |

---

### EUGCMItemDecoratorParticleAttachMode

| 名称 | 值 | 说明 |
|------|------|------|
| Bottom | 1 |  |
| Center | 2 |  |
| Top | 3 |  |

---

### EUGCMItemDecoratorType

| 名称 | 值 | 说明 |
|------|------|------|
| Unkown | 0 |  |
| Visual | 1 |  |
| Particle | 2 |  |
| Audio | 3 |  |

---

### EUGCMItemDecoratorVisualSwitchMode

| 名称 | 值 | 说明 |
|------|------|------|
| None | 1 |  |
| UseGradient | 2 |  |

---

### EUGCMItemDecoratorWorkerType

| 名称 | 值 | 说明 |
|------|------|------|
| Unkown | 0 |  |
| Edit | 1 |  |
| Run | 2 |  |
| Task | 3 |  |

---

### EUGCMLoadingUIState

| 名称 | 值 | 说明 |
|------|------|------|
| MAP | 0 |  |
| MATERIAL | 1 |  |
| CosData | 2 |  |

---

### EUGCMMapSerializeRst

| 名称 | 值 | 说明 |
|------|------|------|
| Ser_Success | 0 |  |
| Ser_Failed | 1 |  |
| Ser_Warnnings | 2 |  |

---

### EUGCMMapStatus

| 名称 | 值 | 说明 |
|------|------|------|
| Normal | 0 |  |
| NeedUpdate | 1 |  |
| Expired | 2 |  |

---

### EUGCMPreviewSceneLoadState

| 名称 | 值 | 说明 |
|------|------|------|
| IDLE | 0 |  |
| LOADING | 1 |  |
| LOADED | 2 |  |
| UNLOADING | 3 |  |
| UNLOADED | 4 |  |

---

### EUGCMPreviewSceneStage

| 名称 | 值 | 说明 |
|------|------|------|
| IDLE | 0 |  |
| TO_LOAD | 1 |  |
| TO_LOADLEVEL | 1 |  |
| TO_LEVELINIT | 2 |  |
| FINISH_LOADED | 3 |  |
| TO_UNLOAD | 11 |  |
| TO_LEVELRELEASE | 11 |  |
| TO_UNLOADLEVEL | 12 |  |
| FINISH_UNLOADED | 13 |  |

---

### EUGCMPreviewSceneUpdateMode

| 名称 | 值 | 说明 |
|------|------|------|
| UPDATEALL | 0 |  |
| ADD | 1 |  |
| REMOVE | 2 |  |

---

### EUGCMSerializeType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| OldSerializeSystem | 1 |  |
| NewSerializeSystem | 2 |  |

---

### EUGCM_ActorSelectType

| 名称 | 值 | 说明 |
|------|------|------|
| SkipChild | 0 |  |
| ReplaceChildToRoot | 1 |  |
| EnableChild | 2 |  |
| EnableChildOnlyWhenRootNotSelected | 3 |  |
| Default | 1 |  |

---

### EUGCM_MapSerMask

| 名称 | 值 | 说明 |
|------|------|------|
| ObjData | -1 |  |
| NameTable | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| CustomVersion | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| PropTagTable | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| FullMapData | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| DataHashToItemId | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |

---

### EUGCMailOperationFailedReason

| 名称 | 值 | 说明 |
|------|------|------|
| NotFound | 1 | 邮件ID不存在 |
| AlreadyClaimed | 2 | 邮件已经领取 |
| AlreadyRead | 3 | 邮件已经阅读 |
| NotRead | 4 | 邮件未阅读 |
| NoAttachment | 5 | 邮件没有附件 |
| Expired | 6 | 邮件已经过期 |
| Revoked | 7 | 邮件已经撤销 |
| Other | 100 | 其他原因 |

---

### EUGCMailStatus

| 名称 | 值 | 说明 |
|------|------|------|
| Unread | 0 | 未阅读 |
| Read | 1 | 已阅读 |
| Claimed | 2 | 已领取 |

---

### EUGCMapMarkShortcutActionType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Teleport | 1 |  |
| MoveTo | 2 |  |
| Custom | 3 |  |

---

### EUGCMobDynamicStateOp

| 名称 | 值 | 说明 |
|------|------|------|
| Allow | 0 |  |
| Has | 1 |  |

---

### EUGCMobSidesShiftSideWays

| 名称 | 值 | 说明 |
|------|------|------|
| Left | 0 |  |
| Right | 1 |  |
| Back | 2 |  |

---

### EUGCMobSpawnerConfigMode

| 名称 | 值 | 说明 |
|------|------|------|
| Blueprint | 0 |  |
| MobGroup | 1 |  |
| Custom | 2 |  |

---

### EUGCMobSpawnerContrMode

| 名称 | 值 | 说明 |
|------|------|------|
| SpawnerManager | 0 |  |
| MaxCountLimit | 1 |  |
| None | 2 |  |

---

### EUGCMobSpawnerManagerStartCondition

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Event | 1 |  |
| FunctionCall | 2 |  |

---

### EUGCMobState

| 名称 | 值 | 说明 |
|------|------|------|
| MobState_None | 0 |  |
| MobState_Born | 1 |  |
| MobState_Alive_Stand | 2 |  |
| MobState_Alive_Stun | 3 |  |
| MobState_Alive_Move | 4 |  |
| MobState_Dead | 5 |  |

---

### EUGCMobileActorCategory

| 名称 | 值 | 说明 |
|------|------|------|
| RTEActor | 0 |  |
| MapActor | 1 |  |
| ToCosActor | 2 |  |

---

### EUGCMobileActorPoolingPolicy

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Policy1 | 1 |  |

---

### EUGCMobileArchiveCategory

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Auto | 1 |  |
| Manual | 2 |  |
| Immediate | 3 |  |

---

### EUGCMobileArchiveReturnCode

| 名称 | 值 | 说明 |
|------|------|------|
| Ok | 0 |  |
| AsyncWait | 1 |  |
| WrongDelta | 2 |  |
| Fail | 255 |  |

---

### EUGCMobileArchiveType

| 名称 | 值 | 说明 |
|------|------|------|
| Local | 1 |  |
| Cloud | 2 |  |

---

### EUGCMobileBindLimit

| 名称 | 值 | 说明 |
|------|------|------|
| NOLIMIT | 0 |  |
| ONLYCHILD | 1 |  |
| ONLYPARENT | 2 |  |
| LIMIT | 3 |  |

---

### EUGCMobileCheckMapConstraintReason

| 名称 | 值 | 说明 |
|------|------|------|
| Preview | 0 |  |
| Publish | 1 |  |

---

### EUGCMobileConfigOverrideStatus

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Editing | 1 |  |
| Previewing | 2 |  |
| Capturing | 3 |  |

---

### EUGCMobileDataIOResult

| 名称 | 值 | 说明 |
|------|------|------|
| OK | 0 |  |
| GenericException | 1 |  |
| NoConfig | 2 |  |
| NoActorManager | 3 |  |
| CorruptedHeader | 4 |  |
| CorruptedContent | 5 |  |
| NoStrategy | 6 |  |
| NoStrategyKey | 7 |  |
| StrategyError | 8 |  |
| Obsolete | 9 |  |

---

### EUGCMobileDataOperationCode

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| ClientInit | 1 |  |
| Pull | 2 |  |
| Push | 3 |  |
| Commit | 4 |  |
| Checkout | 5 |  |

---

### EUGCMobileDataOperationReason

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Preview | 1 |  |

---

### EUGCMobileDependencyPropertyHandleUpdateStrategy

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| UpdateTargetOnGetAddress | 1 |  |
| UpdateTargetOnGetAddressAndSourceOnPostChanged | 2 |  |

---

### EUGCMobileEditSplinePointAddRes

| 名称 | 值 | 说明 |
|------|------|------|
| Success | 0 |  |
| OutOfCapacity | 1 |  |
| Fail | 2 |  |
| Invalid | 3 |  |
| OutOfBound | 4 |  |

---

### EUGCMobileEditorStatus

| 名称 | 值 | 说明 |
|------|------|------|
| Editing | 0 |  |
| Previewing | 1 |  |
| PreparingPreview | 2 |  |
| StoppingPreview | 3 |  |
| BeforeReturnLobbyPublish | 4 |  |
| BeforeReturnLobbyQuit | 5 |  |
| UnKnow | 6 |  |

---

### EUGCMobileEndPreviewReason

| 名称 | 值 | 说明 |
|------|------|------|
| UserRequest | 0 |  |
| Win | 1 |  |
| Lose | 2 |  |
| Reconnect | 3 |  |

---

### EUGCMobileEnvType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Editor | 1 |  |
| Game | 2 |  |

---

### EUGCMobileEventScopeType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| RTE | 1 |  |
| Game | 2 |  |

---

### EUGCMobileFeatureScope

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Edit | 1 |  |
| Preview | 2 |  |
| Game | 3 |  |

---

### EUGCMobileGamePhase

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Loading | 1 |  |
| Gaming | 2 |  |

---

### EUGCMobileModeType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| DeathMatch | 1 |  |
| Race | 2 |  |
| Any | 100 |  |

---

### EUGCMobileMotionCheckResult

| 名称 | 值 | 说明 |
|------|------|------|
| NoError | 1 |  |
| PosRotDataInvalid | 2 |  |
| PositionError | 4 |  |
| RotationError | 8 |  |

---

### EUGCMobileMotionCompSpace

| 名称 | 值 | 说明 |
|------|------|------|
| Local | 1 |  |
| World | 2 |  |

---

### EUGCMobileMotionCompType

| 名称 | 值 | 说明 |
|------|------|------|
| Linear | 1 |  |
| Rotation | 2 |  |
| Pendulum | 3 |  |
| Nonuniform | 4 |  |
| Scale | 5 |  |
| Spline | 6 |  |

---

### EUGCMobileMotionEventActionType

| 名称 | 值 | 说明 |
|------|------|------|
| Start | 1 |  |
| Pause | 2 |  |
| Reset | 3 |  |
| SplineRepos | 4 |  |
| Undefined | 99 |  |

---

### EUGCMobileMotionPauseFlag

| 名称 | 值 | 说明 |
|------|------|------|
| NoPause | 0 |  |
| NormalPause | -1 |  |
| SplinePause | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| SplineReposPause | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |

---

### EUGCMobileMotionSplinePathType

| 名称 | 值 | 说明 |
|------|------|------|
| Linear | 0 |  |
| Curve | 1 |  |

---

### EUGCMobileMotionStartType

| 名称 | 值 | 说明 |
|------|------|------|
| Default | 0 |  |
| ImmediateStart | 1 |  |
| ManualStart | 2 |  |

---

### EUGCMobileMotionState

| 名称 | 值 | 说明 |
|------|------|------|
| Forward | 1 |  |
| PauseBack | 2 |  |
| Pause | 3 |  |

---

### EUGCMobileNonUniformMotionExerciseType

| 名称 | 值 | 说明 |
|------|------|------|
| Linear | 1 |  |
| Rotation | 2 |  |

---

### EUGCMobileOperatorStatus

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| Editing | 1 |  |
| Previewing | 2 |  |
| Finishing | 3 |  |

---

### EUGCMobilePendulumAxis

| 名称 | 值 | 说明 |
|------|------|------|
| X | 1 |  |
| Y | 2 |  |
| Z | 3 |  |

---

### EUGCMobilePreviewReason

| 名称 | 值 | 说明 |
|------|------|------|
| UserRequest | 0 |  |
| UserChallenge | 1 |  |

---

### EUGCMobilePropertyChangedType

| 名称 | 值 | 说明 |
|------|------|------|
| Unspecified | -1 |  |
| ArrayAdd | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| ArrayRemove | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| ArrayClear | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| ValueSet | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |
| Interactive | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1.  -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |

---

### EUGCMobileRebuildMapReason

| 名称 | 值 | 说明 |
|------|------|------|
| Init | 1 |  |
| Update | 2 |  |

---

### EUGCMobileRequestEndPreviewResult

| 名称 | 值 | 说明 |
|------|------|------|
| Ok | 1 |  |
| Fail | 2 |  |

---

### EUGCMobileRequestPreviewResult

| 名称 | 值 | 说明 |
|------|------|------|
| Ok | 1 |  |
| Fail | 2 |  |

---

### EUGCMobileSetRTEActorsHiddenReson

| 名称 | 值 | 说明 |
|------|------|------|
| EnterPreView | 0 |  |
| ExitPreview | 1 |  |
| GiveUpPreview | 2 |  |

---

### EUGCMobileSpawnFlag

| 名称 | 值 | 说明 |
|------|------|------|
| SpawnInDS | -1 |  |
| SpawnInClient | -1 | -- the value appears as -1 more due to UHT parse error rather than it actually be -1. |

---

### EUGCMobileSplinePointMode

| 名称 | 值 | 说明 |
|------|------|------|
| NONE | 0 |  |
| PARTICLE | 1 |  |

---

### EUGCMobileSplinePointPositionType

| 名称 | 值 | 说明 |
|------|------|------|
| NORMAL | 0 |  |
| CENTER | 1 |  |

---

### EUGCMobileSplineStyleMode

| 名称 | 值 | 说明 |
|------|------|------|
| SPLINE | 0 |  |
| PARTICLE | 1 |  |

---

### EUGCMobileTestMode

| 名称 | 值 | 说明 |
|------|------|------|
| All | 0 |  |
| Motion | 1 |  |
| Decorator | 2 |  |

---

### EUGCMobileTransformModule

| 名称 | 值 | 说明 |
|------|------|------|
| NORMAL | 0 |  |
| BIND | 1 |  |

---

### EUGCMobile_RTEActorBindingCmdType

| 名称 | 值 | 说明 |
|------|------|------|
| Bind | 0 |  |
| Unbind | 1 |  |

---

### EUGCMobile_RTEActorChildCmdType

| 名称 | 值 | 说明 |
|------|------|------|
| AddChild | 0 |  |
| RemoveChild | 1 |  |

---

### EUGCMobile_RTEActorCombinationCmdType

| 名称 | 值 | 说明 |
|------|------|------|
| Bind | 0 |  |
| Unbind | 1 |  |
| MoveIn | 2 |  |
| MoveOut | 3 |  |

---

### EUGCMobile_RTEActorStateCmdType

| 名称 | 值 | 说明 |
|------|------|------|
| AddState | 0 |  |
| RemoveState | 1 |  |

---

### EUGCMobile_RTEBindEventCmdType

| 名称 | 值 | 说明 |
|------|------|------|
| Bind | 0 |  |
| Unbind | 1 |  |

---

### EUGCMobile_RTECameraCommandType

| 名称 | 值 | 说明 |
|------|------|------|
| CreateCameraConfig | 0 |  |
| DeleteCameraConfig | 1 |  |
| CreateCameraShake | 2 |  |
| DeleteCameraShake | 3 |  |

---

### EUGCMobile_RTECommandType

| 名称 | 值 | 说明 |
|------|------|------|
| Cmd_Unknown | 0 |  |
| Cmd_Composite | 1 |  |
| Cmd_Macro | 2 |  |
| Cmd_Lock | 3 |  |
| Cmd_BoolPropertyChange | 4 |  |
| Cmd_EnumPropertyChange | 5 |  |
| Cmd_Int8PropertyChange | 6 |  |
| Cmd_UInt8PropertyChange | 7 |  |
| Cmd_Int16PropertyChange | 8 |  |
| Cmd_UInt16PropertyChange | 9 |  |
| Cmd_Int32PropertyChange | 10 |  |
| Cmd_UInt32PropertyChange | 11 |  |
| Cmd_Int64PropertyChange | 12 |  |
| Cmd_UInt64PropertyChange | 13 |  |
| Cmd_FloatPropertyChange | 14 |  |
| Cmd_DoublePropertyChange | 15 |  |
| Cmd_StringPropertyChange | 16 |  |
| Cmd_NamePropertyChange | 17 |  |
| Cmd_TextPropertyChange | 18 |  |
| Cmd_ObjectPropertyChange | 19 |  |
| Cmd_ClassPropertyChange | 20 |  |
| Cmd_SoftObjectPropertyChange | 21 |  |
| Cmd_SoftClassPropertyChange | 22 |  |
| Cmd_StructPropertyChange | 23 |  |
| Cmd_ArrayPropertyChange | 24 |  |
| Cmd_MapPropertyChange | 25 |  |
| Cmd_SetPropertyChange | 26 |  |
| Cmd_SpawnActor | 27 |  |
| Cmd_DeleteActor | 28 |  |
| Cmd_ModifyActorTransform | 29 |  |
| Cmd_ModifyCombinationTransform | 30 |  |
| Cmd_ActorCombination | 31 |  |
| Cmd_ActorBinding | 32 |  |
| Cmd_ActorChild | 33 |  |
| Cmd_ActorState | 34 |  |
| Cmd_EventBind | 35 |  |
| Cmd_GizmoTranslationCommand | 36 |  |
| Cmd_Terrain_AddFoliage | 37 |  |
| Cmd_Terrain_EraseFoliage | 38 |  |
| Cmd_Terrain_ChangeShape | 39 |  |
| Cmd_Terrain_ChangeTexture | 40 |  |
| Cmd_Terrain_ChangeTransform | 41 |  |
| Cmd_Terrain_ChangeSize | 42 |  |
| Cmd_BlueprintCommandBegin | 43 |  |
| Cmd_Max | 255 |  |

---

### EUGCMobile_RTEEditableUICmdType

| 名称 | 值 | 说明 |
|------|------|------|
| CreateWidget | 0 |  |
| DeleteWidget | 1 |  |
| ModifyWidget | 2 |  |

---

### EUGCMobile_RTESkyboxCmdType

| 名称 | 值 | 说明 |
|------|------|------|
| CreateSkybox | 0 |  |
| DeleteSkybox | 1 |  |
| ResetSkybox | 2 |  |
| CreateTransform | 3 |  |
| DeleteTransform | 4 |  |

---

### EUGCMobilityType

| 名称 | 值 | 说明 |
|------|------|------|
| Any | 0 |  |
| StaticAndStationary | 1 |  |
| Moveable | 2 |  |

---

### EUGCMotionCompType

| 名称 | 值 | 说明 |
|------|------|------|
| Linear | 1 |  |
| Rotation | 2 |  |
| Pendulum | 3 |  |
| Scale | 4 |  |
| Spline | 5 |  |
| NonuniformLinear | 6 |  |
| NonuniformRotation | 7 |  |

---

### EUGCObjectTemplateType

| 名称 | 值 | 说明 |
|------|------|------|
| Character | 0 |  |
| Entity | 1 |  |
| Item | 2 |  |
| Skill | 3 |  |
| DataTable | 4 |  |
| Asset | 5 |  |
| UI | 6 |  |
| DataAsset | 7 |  |
| None | 8 |  |

---

### EUGCPercentTaskResetType

| 名称 | 值 | 说明 |
|------|------|------|
| NotReset | 1 |  |
| DailyReset | 2 |  |
| WeeklyReset | 3 |  |

---

### EUGCPlayerRespawnPointSelectionMethod

| 名称 | 值 | 说明 |
|------|------|------|
| RespawnOnTheSpot | 0 |  |
| DesignatedRespawnLocation | 1 |  |
| RespawnBySpawnMethod | 2 |  |

---

### EUGCPlayerSpawnPointSelectionMethod

| 名称 | 值 | 说明 |
|------|------|------|
| DefaultSelectionMethod | 0 |  |
| DesignatedSpawnLocation | 1 |  |
| RandomSpawnPoint | 2 |  |
| CampSpawnMethod | 3 |  |
| DesignatedPlayerStartID | 4 |  |

---

### EUGCRemoveItemReason

| 名称 | 值 | 说明 |
|------|------|------|
| Default | 0 |  |
| Transfer | 2 |  |
| ExceedCellCapacity | 4 |  |
| SortOut | 5 |  |

---

### EUGCSpawnWaveStartCondition

| 名称 | 值 | 说明 |
|------|------|------|
| AllMobDie | 0 |  |
| LastWaveEnd | 1 |  |

---

### EUGCStateDealMethod

| 名称 | 值 | 说明 |
|------|------|------|
| Enter | 1 |  |
| Leave | 2 |  |

---

### EUGCTaskCustomWeekResetType

| 名称 | 值 | 说明 |
|------|------|------|
| Monday | 1 |  |
| Tuesday | 2 |  |
| Wednesday | 3 |  |
| Thursday | 4 |  |
| Friday | 5 |  |
| Saturday | 6 |  |
| Sunday | 7 |  |

---

### EUGCTaskLineAwardState

| 名称 | 值 | 说明 |
|------|------|------|
| Lock | 1 |  |
| NotClaimed | 2 |  |
| HasClaimed | 3 |  |

---

### EUGCTaskLineType

| 名称 | 值 | 说明 |
|------|------|------|
| LevelTaskLine | 1 |  |
| PercentTaskLine | 2 |  |

---

### EUGCTaskState

| 名称 | 值 | 说明 |
|------|------|------|
| Lock | 1 |  |
| Incomplete | 2 |  |
| NotClaimed | 3 |  |
| HasClaimed | 4 |  |
| Expired | 5 |  |
| NotBegin | 6 |  |

---

### EUGCTaskTargetType

| 名称 | 值 | 说明 |
|------|------|------|
| Player | 1 |  |
| Monster | 2 |  |

---

### EUGCToastPriorityType

| 名称 | 值 | 说明 |
|------|------|------|
| Low | 0 |  |
| Normal | 1 |  |
| High | 2 |  |

---

### EUGCToastReceiverType

| 名称 | 值 | 说明 |
|------|------|------|
| All | 0 |  |
| InstigatorPlayer | 1 |  |
| InstigatorTeam | 2 |  |
| Enemies | 3 |  |
| SpecificTeam | 4 |  |

---

### EUGCToastSizeType

| 名称 | 值 | 说明 |
|------|------|------|
| Small | 0 |  |
| Medium | 1 |  |
| Large | 2 |  |

---

### EUGCWeaponCooperateType

| 名称 | 值 | 说明 |
|------|------|------|
| None | 0 |  |
| RangedWeapon | 1 |  |
| MeleeWeapon | 2 |  |

---

### FUGCMobileMotionStartStopState

| 名称 | 值 | 说明 |
|------|------|------|
| MotionWaitDelay | 1 |  |
| MotionNormalForward | 2 |  |
| MotionNormalBack | 3 |  |
| MotionCycleForward | 4 |  |
| MotionCycleForwardPause | 5 |  |
| MotionCycleBack | 6 |  |
| MotionCycleBackPause | 7 |  |
| MotionTimeout | 8 |  |

---

### FUGCMobileMotionSyncState

| 名称 | 值 | 说明 |
|------|------|------|
| MotionMoving | 1 |  |
| MotionStoppingWaitSync | 2 |  |
| MotionStoppingNoSync | 3 |  |

---

### FUGCVehiclePhysicsShapeType

| 名称 | 值 | 说明 |
|------|------|------|
| Sphere | 0 |  |
| Box | 1 |  |
| Capsule | 2 |  |

---

### FUGC_ACCharacterEnum

| 名称 | 值 | 说明 |
|------|------|------|
| UGC_None | 0 |  |
| UGC_HumanPlayer | 1 |  |
| UGC_HumanMonster | 2 |  |

---

## 数据结构（Structs）

## 全局函数（Global Functions）

**GetAsyncLoadObjectPromiseFuture**(Outer: UObject, FullPath: string) -> @PromiseFuture

使用 PromiseFuture 异步加载资源并创建对象实例 用法：GetAsyncLoadObjectPromiseFuture(PlayerController, ObjectPath):Then(function (PromiseFuture) local Obj = PromiseFuture:Get() end):AutoResume() 生效范围：服务器&客户端

**TagLogFormatPrint**(...: any) -> void

输出格式化的日志， 有三种使用方式，1.原始日志字符串，2.格式化字符串和参数，3.日志类别和日志详细级别、格式、参数。默认日志类别："LogTagLog"，默认详细级别：Log。 生效范围：服务器&客户端

**TagLogRawPrint**(LogCategory: string, LogVerbosity: ELogVerbosity, LogContent: string) -> void

输出原始日志

## 附录：完整API索引

### 全部类列表

- AAIController
- AActivityBaseActor
- AActor
- AAggregatedCollisionActor
- AAmbientSound
- AAtmosphericFog
- AAtmosphericSkyBoxActor
- AAudioVolume
- ABoxGIVolume
- ABrush
- ACameraActor
- ACameraRig_Crane
- ACameraRig_Rail
- ACharacter
- ACineCameraActor
- AConsoleCMDVolume
- AController
- ACullDistanceVolume
- ADebugCameraController
- ADecalActor
- ADecalBakingParameterActor
- ADefaultPawn
- ADocumentationActor
- AEQSTestingPawn
- AEliteProjectile
- AEmitter
- AEmitterCameraLensEffectBase
- AExponentialHeightFog
- AGameMode
- AGameModeBase
- AGameNetworkManager
- AGameSession
- AGameState
- AGameStateBase
- AInfo
- AInteractiveFoliageActor
- ALODActor
- ALandscape
- ALandscapeMeshProxyActor
- ALandscapeProxy
- ALandscapeStreamingProxy
- ALevelBounds
- ALevelScriptActor
- ALevelSequenceActor
- ALevelStreamingVolume
- ALight
- ALightmassPortal
- AMaterialInstanceActor
- AMatineeActor
- AMatineeActorCameraAnim
- ANavLinkProxy
- ANavMeshBoundsVolume
- ANavModifierVolume
- ANavigationData
- ANavigationObjectBase
- ANavigationTestingActor
- ANote
- AOcean
- APESkillProjectileBase
- APVSExtraVisibilityActor
- APainCausingVolume
- APaperCharacter
- APaperFlipbookActor
- APaperGroupedSpriteActor
- APaperSpriteActor
- APaperTerrainActor
- APaperTileMapActor
- APawn
- APhysicsConstraintActor
- APhysicsThruster
- APhysicsVolume
- APickUpWrapperActor
- APixelProjectedReflection
- APixelProjectedReflectionHeightAdjustmentVolume
- APixelProjectedReflectionVisibilityVolume
- APlanarReflection
- APlayerCameraManager
- APlayerController
- APlayerStart
- APlayerState
- APointLight
- APostProcessVolume
- APrecomputedVisibilityItemPoolVolume
- APrecomputedVisibilityOverrideVolume
- APrecomputedVisibilityVolume
- AProceduralFoliageBlockingVolume
- AProceduralFoliageVolume
- ARadialForceActor
- ARecastNavMesh
- AReflectionCapture
- ASTExtraBaseCharacter
- ASTExtraCharacter
- ASTExtraGameStateBase
- ASTExtraPlayerController
- ASTExtraShootWeapon
- ASTExtraVehicleBase
- ASTExtraWeapon
- ASceneCapture
- ASceneCapture2D
- ASceneCaptureCube
- ASkeletalMeshActor
- ASkyLight
- ASphereReflectionCapture
- ASplineMeshActor
- ASpotLight
- AStaticMeshActor
- AStaticMeshIndoorVolume
- ATargetPoint
- ATextRenderActor
- ATriggerBase
- AUGCGameModeBase
- AUGCGameModeTDM
- AUGCGenericCharacter
- AUGCItemSpawner
- AUGCItemSpawnerManager
- AUGCMobCharacter
- AUGCMobSpawner
- AUGCMobSpawnerManager
- AUGCPickUpWrapperActor
- AUniversalProjectileBase
- AUniversalProjectileCore
- AUtilityTickActor
- AVectorFieldVolume
- AVolume
- AWindDirectionalSource
- AWorldSettings
- BackpackUIComponent
- BP_UGCPickUpListComponent
- BP_UGCVehicleRefresherTool
- CommodityOperationManager
- Delegate
- PromiseFuture
- RankingListManager
- RankingListPlayerComponent
- TaskManager
- TaskPlayerComponent
- UAIAsyncTaskBlueprintProxy
- UAIBlueprintHelperLibrary
- UAIDataProvider_QueryParams
- UAIDataProvider_Random
- UAIPerceptionComponent
- UAIPerceptionStimuliSourceComponent
- UAIPerceptionSystem
- UAISense
- UAISenseConfig
- UAISenseConfig_Blueprint
- UAISenseConfig_Damage
- UAISenseConfig_Hearing
- UAISenseConfig_Sight
- UAISenseEvent_Damage
- UAISenseEvent_Hearing
- UAISense_Blueprint
- UAISense_Damage
- UAISense_Hearing
- UAISense_Prediction
- UAISense_Sight
- UAISense_Team
- UAISense_Touch
- UAISystem
- UAISystemBase
- UAITask
- UAITask_MoveTo
- UAITask_RunEQS
- UActivityFakePossessComponent
- UActorChannel
- UActorComponent
- UAggregatedCollisionComponent
- UAnimBlueprint
- UAnimBlueprintGeneratedClass
- UAnimClassData
- UAnimComposite
- UAnimCompress
- UAnimCompress_Automatic
- UAnimCompress_PerTrackCompression
- UAnimCompress_PerTrackVariableBit
- UAnimCompress_RemoveEverySecondKey
- UAnimCompress_RemoveLinearKeys
- UAnimCompress_RemoveTrivialKeys
- UAnimFuntionBoneModifyLibrary
- UAnimInstance
- UAnimInstanceUpdateCondition
- UAnimMontage
- UAnimNotify
- UAnimNotifyState
- UAnimNotifyStateBoneRetargetAdaptInfoObj
- UAnimNotifyState_TimedParticleEffect
- UAnimNotifyState_Trail
- UAnimNotify_PlayMontageNotify
- UAnimNotify_PlayMontageNotifyWindow
- UAnimNotify_PlayParticleEffect
- UAnimNotify_PlaySound
- UAnimSequence
- UAnimSequenceBase
- UAnimSequencerInstance
- UAnimSet
- UAnimSingleNodeInstance
- UAnimationAsset
- UAnimationSettings
- UApplicationLifecycleComponent
- UArrowComponent
- UAssetManager
- UAssetManagerSettings
- UAssetMappingTable
- UAssetRegistryHelpers
- UAsyncTaskDownloadImage
- UAtmosphericFogComponent
- UAtmosphericSkyBoxComponent
- UAudioComponent
- UAudioMixerBlueprintLibrary
- UAudioSettings
- UAutomatedLevelSequenceCapture
- UAutomationTestSettings
- UBTAttachment_LuaBase
- UBTCompositeNode
- UBTComposite_SimpleParallel
- UBTCondition_LuaBase
- UBTDecorator
- UBTDecorator_Blackboard
- UBTDecorator_BlackboardBase
- UBTDecorator_BlueprintBase
- UBTDecorator_CheckGameplayTagsOnActor
- UBTDecorator_CompareBBEntries
- UBTDecorator_ConeCheck
- UBTDecorator_Cooldown
- UBTDecorator_DoesPathExist
- UBTDecorator_IsAtLocation
- UBTDecorator_IsBBEntryOfClass
- UBTDecorator_KeepInCone
- UBTDecorator_Loop
- UBTDecorator_SetTagCooldown
- UBTDecorator_TagCooldown
- UBTDecorator_TimeLimit
- UBTFunctionLibrary
- UBTNode
- UBTService
- UBTService_BlackboardBase
- UBTService_BlueprintBase
- UBTService_DefaultFocus
- UBTService_RunEQS
- UBTTaskNode
- UBTTask_BlackboardBase
- UBTTask_BlueprintBase
- UBTTask_GameplayTaskBase
- UBTTask_LuaBase
- UBTTask_MakeNoise
- UBTTask_MoveDirectlyToward
- UBTTask_MoveTo
- UBTTask_PlayAnimation
- UBTTask_PlaySound
- UBTTask_PushPawnAction
- UBTTask_RotateToFaceBBEntry
- UBTTask_RunBehavior
- UBTTask_RunBehaviorDynamic
- UBTTask_RunEQSQuery
- UBTTask_SetTagCooldown
- UBTTask_Wait
- UBTTask_WaitBlackboardTime
- UBackgroundBlur
- UBackgroundBlurSlot
- UBackpackComponent
- UBackpackComponentV2
- UBaseMediaSource
- UBasicOverlays
- UBehaviorTree
- UBehaviorTreeComponent
- UBehaviorTreeManager
- UBillboardComponent
- UBlackboardComponent
- UBlackboardData
- UBlackboardKeyType_Class
- UBlackboardKeyType_Enum
- UBlackboardKeyType_NativeEnum
- UBlackboardKeyType_Object
- UBlackboardKeyType_String
- UBlendProfile
- UBlendSpace
- UBlendSpace1D
- UBlendSpaceBase
- UBlueprint
- UBlueprintAsyncActionBase
- UBlueprintCore
- UBlueprintGameplayTagLibrary
- UBlueprintMapLibrary
- UBlueprintPlatformLibrary
- UBlueprintRuntimeSettings
- UBlueprintSetLibrary
- UBoneMaskFilter
- UBookMark
- UBookMark2D
- UBoolBinding
- UBorder
- UBorderSlot
- UBoxComponent
- UBoxReflectionCaptureComponent
- UBrainComponent
- UBreakpoint
- UBrushBinding
- UBrushBuilder
- UBrushComponent
- UButton
- UButtonSlot
- UButtonStyleAsset
- UButtonWidgetStyle
- UCameraAnim
- UCameraAnimInst
- UCameraComponent
- UCameraModifier
- UCameraModifier_CameraShake
- UCameraShake
- UCanvas
- UCanvasPanel
- UCanvasPanelSlot
- UCanvasRenderTarget2D
- UCapsuleComponent
- UCascadeDebuggerSystem
- UChannel
- UCharacterMovementComponent
- UCheatManager
- UCheckBox
- UCheckBoxStyleAsset
- UCheckBoxWidgetStyle
- UCheckedStateBinding
- UChildActorComponent
- UChildConnection
- UChunkLabel
- UCineCameraComponent
- UCircularThrobber
- UClickActorComponentBase
- UClothingAsset
- UClothingAssetBase
- UCloudStorageBase
- UCollisionProfile
- UColorBinding
- UColorGradient
- UColorGradientSlider
- UColorPicker
- UColorSlider
- UComboBox
- UComboBoxKey
- UComboBoxString
- UComboBoxWidgetStyle
- UComboButtonWidgetStyle
- UCommandlet
- UCommonBattleItemHandleBase
- UCommonDeviceProfileMatchingRules
- UComponentDelegateBinding
- UCompositionGraphCaptureSettings
- UConfigOverriderFor120fps
- UConsole
- UConsoleSettings
- UContentWidget
- UCopyMotionMathLibrary
- UCrowdFollowingComponent
- UCrowdManager
- UCurveBase
- UCurveFloat
- UCurveLinearColor
- UCurveVector
- UCustomActorMoveComponent
- UCustomInstancedStaticMeshComponent
- UDamageType
- UDataAsset
- UDataTable
- UDataTableFunctionLibrary
- UDecalBakingParameterComponent
- UDecalComponent
- UDefaultLevelSequenceInstanceData
- UDemoNetConnection
- UDemoNetDriver
- UDeviceProfile
- UDeviceProfileManager
- UDialogueVoice
- UDialogueWave
- UDirectionalLightComponent
- UDistributionFloat
- UDistributionFloatConstant
- UDistributionFloatConstantCurve
- UDistributionFloatParameterBase
- UDistributionFloatUniform
- UDistributionFloatUniformCurve
- UDistributionVector
- UDistributionVectorConstant
- UDistributionVectorConstantCurve
- UDistributionVectorParameterBase
- UDistributionVectorUniform
- UDistributionVectorUniformCurve
- UDragDropOperation
- UDrawFrustumComponent
- UDynamicAtlasTexture2D
- UDynamicInputBindingComponent
- UEdGraph
- UEdGraphNode
- UEdGraphNode_Documentation
- UEdGraphPin_Deprecated
- UEditableGameplayTagQuery
- UEditableGameplayTagQueryExpression_AllExprMatch
- UEditableGameplayTagQueryExpression_AllTagsMatch
- UEditableGameplayTagQueryExpression_AnyExprMatch
- UEditableGameplayTagQueryExpression_AnyTagsMatch
- UEditableGameplayTagQueryExpression_NoExprMatch
- UEditableGameplayTagQueryExpression_NoTagsMatch
- UEditableText
- UEditableTextBox
- UEditableTextBoxWidgetStyle
- UEditableTextWidgetStyle
- UEndUserSettings
- UEngine
- UEngineMessage
- UEnvQuery
- UEnvQueryContext_BlueprintBase
- UEnvQueryGenerator
- UEnvQueryGenerator_ActorsOfClass
- UEnvQueryGenerator_BlueprintBase
- UEnvQueryGenerator_Composite
- UEnvQueryGenerator_Cone
- UEnvQueryGenerator_CurrentLocation
- UEnvQueryGenerator_Donut
- UEnvQueryGenerator_OnCircle
- UEnvQueryGenerator_PathingGrid
- UEnvQueryGenerator_ProjectedPoints
- UEnvQueryGenerator_SimpleGrid
- UEnvQueryInstanceBlueprintWrapper
- UEnvQueryManager
- UEnvQueryNode
- UEnvQueryOption
- UEnvQueryTest
- UEnvQueryTest_Distance
- UEnvQueryTest_Dot
- UEnvQueryTest_GameplayTags
- UEnvQueryTest_Overlap
- UEnvQueryTest_Pathfinding
- UEnvQueryTest_PathfindingBatch
- UEnvQueryTest_Project
- UEnvQueryTest_Trace
- UExpandableArea
- UExponentialHeightFogComponent
- UExporter
- UFileMediaSource
- UFloatBinding
- UFloatingPawnMovement
- UFoliageInstancedStaticMeshComponent
- UFoliageStatistics
- UFoliageType
- UFoliageType_Actor
- UFoliageType_InstancedStaticMesh
- UFont
- UFontFace
- UFontImportOptions
- UForceFeedbackAttenuation
- UForceFeedbackComponent
- UForceFeedbackEffect
- UGCAchievementSystem
- UGCActivitySystem
- UGCActorComponentUtility
- UGCAirAttachSystem
- UGCAirAttackManager
- UGCAirDropManagerSystem
- UGCAsyncUtility
- UGCAttributeSystem
- UGCBackPackSystem
- UGCBackpackSystemV2
- UGCBuffSystem
- UGCCameraManagerSystem
- UGCCampSystem
- UGCCharAvatarShowcaseActor
- UGCCircleManagerSystem
- UGCCommoditySystem
- UGCCommonDragDropItem
- UGCCommonUISystem
- UGCDebugSystem
- UGCDelegateUtility
- UGCDropSystem
- UGCEMPZoneManager
- UGCEMPZoneSystem
- UGCEntityTypeSystem
- UGCFakePlayerSystem
- UGCGamePartSystem
- UGCGameSettingSystem
- UGCGameSystem
- UGCGameplayTag
- UGCGameplayTagSystem
- UGCGameplayTaskSystem
- UGCGenericCharacterSystem
- UGCGenericMessageSystem
- UGCGunSystem
- UGCInputSystem
- UGCItemSystem
- UGCItemSystemV2
- UGCLevelFlowSystem
- UGCMailSystem
- UGCMapMarkManagerSystem
- UGCMathUtility
- UGCMessageSystem
- UGCMiscFunctionSystem
- UGCMobPawnSystem
- UGCMultiMode
- UGCNavigationSystem
- UGCObjectUtility
- UGCPawnAttrSystem
- UGCPawnSystem
- UGCPersistEffectSystem
- UGCPlayerControllerSystem
- UGCPlayerPawnSystem
- UGCPlayerStateSystem
- UGCPrivilegeSystem
- UGCProjectileSystem
- UGCProjectileSystemV2
- UGCRankSystem
- UGCSceneQueryUtility
- UGCSimpleCharacterSystem
- UGCSkillManagerSystem
- UGCSoundManagerSystem
- UGCStringTextUtility
- UGCTeamSystem
- UGCTimerUtility
- UGCVehicleCommonSystem
- UGCVehicleSeatSystem
- UGCVehicleSystem
- UGCVehicleSystemV2
- UGCVoiceManagerSystem
- UGCWeaponManagerSystem
- UGCWeatherSystem
- UGCWidgetManagerSystem
- UGC_Backpack_Item_UIBP
- UGC_SecondaryConfirmation_UIBP
- UGIBoxVolumeComponent
- UGIVolumesContainerComponent
- UGameEngine
- UGameInstance
- UGameMapsSettings
- UGameModeGeneralDataAsset
- UGameNetworkManagerSettings
- UGameSessionSettings
- UGameUserSettings
- UGameViewportClient
- UGameplayDataCollectHelperBase
- UGameplayStatics
- UGameplayTagsDeveloperSettings
- UGameplayTagsList
- UGameplayTagsManager
- UGameplayTagsSettings
- UGameplayTask
- UGameplayTaskResource
- UGameplayTask_ClaimResource
- UGameplayTask_SpawnActor
- UGameplayTask_TimeLimitedExecution
- UGameplayTask_WaitDelay
- UGameplayTasksComponent
- UGarbageCollectionSettings
- UGeneralProjectSettings
- UGridPanel
- UGridPathFollowingComponent
- UGridSlot
- UGridVisibilityCaptureComponent
- UHLODProxy
- UHapticFeedbackEffect_Buffer
- UHapticFeedbackEffect_Curve
- UHapticFeedbackEffect_SoundWave
- UHeadMountedDisplayFunctionLibrary
- UHierarchicalInstancedStaticMeshComponent
- UHierarchicalLODSetup
- UHorizontalBox
- UHorizontalBoxSlot
- UHudSettings
- UIdeaGrassFieldFunctionLibrary
- UImage
- UImageCaptureSettings
- UImportanceSamplingLibrary
- UInGameAdManager
- UInheritableComponentHandler
- UInputActionDelegateBinding
- UInputAxisDelegateBinding
- UInputAxisKeyDelegateBinding
- UInputComponent
- UInputKeyDelegateBinding
- UInputKeySelector
- UInputSettings
- UInputTouchDelegateBinding
- UInstancedStaticMeshComponent
- UInt32Binding
- UIntSerialization
- UInterpCurveEdSetup
- UInterpData
- UInterpFilter
- UInterpFilter_Classes
- UInterpFilter_Custom
- UInterpGroup
- UInterpGroupCamera
- UInterpGroupInst
- UInterpToMovementComponent
- UInterpTrack
- UInterpTrackAnimControl
- UInterpTrackBoolProp
- UInterpTrackColorProp
- UInterpTrackDirector
- UInterpTrackEvent
- UInterpTrackFade
- UInterpTrackFloatAnimBPParam
- UInterpTrackFloatBase
- UInterpTrackFloatMaterialParam
- UInterpTrackFloatParticleParam
- UInterpTrackFloatProp
- UInterpTrackInstAnimControl
- UInterpTrackInstBoolProp
- UInterpTrackInstColorProp
- UInterpTrackInstDirector
- UInterpTrackInstEvent
- UInterpTrackInstFloatAnimBPParam
- UInterpTrackInstFloatMaterialParam
- UInterpTrackInstFloatParticleParam
- UInterpTrackInstFloatProp
- UInterpTrackInstLinearColorProp
- UInterpTrackInstMove
- UInterpTrackInstParticleReplay
- UInterpTrackInstProperty
- UInterpTrackInstSlomo
- UInterpTrackInstSound
- UInterpTrackInstToggle
- UInterpTrackInstVectorMaterialParam
- UInterpTrackInstVectorProp
- UInterpTrackInstVisibility
- UInterpTrackLinearColorBase
- UInterpTrackLinearColorProp
- UInterpTrackMove
- UInterpTrackMoveAxis
- UInterpTrackParticleReplay
- UInterpTrackSound
- UInterpTrackToggle
- UInterpTrackVectorBase
- UInterpTrackVectorMaterialParam
- UInterpTrackVectorProp
- UInterpTrackVisibility
- UInvalidationBox
- UKismetAnimationLibrary
- UKismetArrayLibrary
- UKismetGuidLibrary
- UKismetInputLibrary
- UKismetInternationalizationLibrary
- UKismetMaterialLibrary
- UKismetMathLibrary
- UKismetMetaDataLibrary
- UKismetNodeHelperLibrary
- UKismetPackageNameLibrary
- UKismetRenderingLibrary
- UKismetStringLibrary
- UKismetStringTableLibrary
- UKismetSystemLibrary
- UKismetTextLibrary
- ULandscapeAOTextureDataAsset
- ULandscapeComponent
- ULandscapeGrassType
- ULandscapeHeightfieldCollisionComponent
- ULandscapeInfo
- ULandscapeLayerInfoObject
- ULandscapeMaterialInstanceConstant
- ULandscapeMeshCollisionComponent
- ULandscapeMeshProxyComponent
- ULandscapeSplineControlPoint
- ULandscapeSplineSegment
- ULandscapeSplinesComponent
- ULayer
- ULevel
- ULevelActorContainer
- ULevelBlocksFoliageDataContainer
- ULevelCapture
- ULevelScriptBlueprint
- ULevelSequence
- ULevelSequenceBurnIn
- ULevelSequenceBurnInOptions
- ULevelSequenceDirector
- ULevelSequencePlayer
- ULevelStreaming
- ULevelStreamingKismet
- ULightComponent
- ULightComponentBase
- ULightmappedSurfaceCollection
- ULightmassPortalComponent
- ULightmassPrimitiveSettingsObject
- UListView
- ULocalPlayer
- ULocalizedOverlays
- UManagementRuleSetting
- UMapBuildDataRegistry
- UMaterial
- UMaterialBillboardComponent
- UMaterialExpression
- UMaterialExpressionAbs
- UMaterialExpressionAdd
- UMaterialExpressionAntialiasedTextureMask
- UMaterialExpressionAppendVector
- UMaterialExpressionArccosine
- UMaterialExpressionArccosineFast
- UMaterialExpressionArcsine
- UMaterialExpressionArcsineFast
- UMaterialExpressionArctangent
- UMaterialExpressionArctangent2
- UMaterialExpressionArctangent2Fast
- UMaterialExpressionArctangentFast
- UMaterialExpressionAtmosphericFogColor
- UMaterialExpressionBentNormalCustomOutput
- UMaterialExpressionBlackBody
- UMaterialExpressionBlendMaterialAttributes
- UMaterialExpressionBreakMaterialAttributes
- UMaterialExpressionBumpOffset
- UMaterialExpressionCeil
- UMaterialExpressionChromaticAberrationCustomOutput
- UMaterialExpressionClamp
- UMaterialExpressionClearCoatNormalCustomOutput
- UMaterialExpressionCollectionParameter
- UMaterialExpressionComment
- UMaterialExpressionComponentMask
- UMaterialExpressionConstant
- UMaterialExpressionConstant2Vector
- UMaterialExpressionConstant3Vector
- UMaterialExpressionConstant4Vector
- UMaterialExpressionConstantBiasScale
- UMaterialExpressionCosine
- UMaterialExpressionCrossProduct
- UMaterialExpressionCustom
- UMaterialExpressionDDX
- UMaterialExpressionDDY
- UMaterialExpressionDecalMipmapLevel
- UMaterialExpressionDepthFade
- UMaterialExpressionDepthOfFieldFunction
- UMaterialExpressionDeriveNormalZ
- UMaterialExpressionDesaturation
- UMaterialExpressionDistance
- UMaterialExpressionDistanceFieldGradient
- UMaterialExpressionDistanceToNearestSurface
- UMaterialExpressionDivide
- UMaterialExpressionDotProduct
- UMaterialExpressionDynamicInstancingParameter
- UMaterialExpressionDynamicParameter
- UMaterialExpressionFeatureLevelSwitch
- UMaterialExpressionFloor
- UMaterialExpressionFmod
- UMaterialExpressionFontSample
- UMaterialExpressionFontSampleParameter
- UMaterialExpressionFrac
- UMaterialExpressionFresnel
- UMaterialExpressionFunctionInput
- UMaterialExpressionFunctionOutput
- UMaterialExpressionGIReplace
- UMaterialExpressionGetMaterialAttributes
- UMaterialExpressionIBLSwitch
- UMaterialExpressionIf
- UMaterialExpressionLandscapeBlendTA
- UMaterialExpressionLandscapeFlattenCoords
- UMaterialExpressionLandscapeFlattenTexture
- UMaterialExpressionLandscapeGrassOutput
- UMaterialExpressionLandscapeLayerBlend
- UMaterialExpressionLandscapeLayerCoords
- UMaterialExpressionLandscapeLayerSample
- UMaterialExpressionLandscapeLayerSwitch
- UMaterialExpressionLandscapeLayerWeight
- UMaterialExpressionLandscapeVisibilityMask
- UMaterialExpressionLightmassReplace
- UMaterialExpressionLinearInterpolate
- UMaterialExpressionLogarithm10
- UMaterialExpressionLogarithm2
- UMaterialExpressionMakeMaterialAttributes
- UMaterialExpressionMaterialFunctionCall
- UMaterialExpressionMaterialProxyReplace
- UMaterialExpressionMax
- UMaterialExpressionMin
- UMaterialExpressionMultiply
- UMaterialExpressionNoise
- UMaterialExpressionNormalize
- UMaterialExpressionOneMinus
- UMaterialExpressionPSCustomData
- UMaterialExpressionPanner
- UMaterialExpressionParameter
- UMaterialExpressionParticleSubUV
- UMaterialExpressionPerInstanceCustomData
- UMaterialExpressionPower
- UMaterialExpressionPreviousFrameSwitch
- UMaterialExpressionQualitySwitch
- UMaterialExpressionReflectionVectorWS
- UMaterialExpressionReroute
- UMaterialExpressionRotateAboutAxis
- UMaterialExpressionRotator
- UMaterialExpressionRound
- UMaterialExpressionSaturate
- UMaterialExpressionScalarParameter
- UMaterialExpressionSceneColor
- UMaterialExpressionSceneDepth
- UMaterialExpressionSceneDepthWithoutWater
- UMaterialExpressionSceneTexture
- UMaterialExpressionScreenPosition
- UMaterialExpressionSetMaterialAttributes
- UMaterialExpressionSign
- UMaterialExpressionSine
- UMaterialExpressionSingleLayerWaterMaterialOutput
- UMaterialExpressionSobol
- UMaterialExpressionSpeedTree
- UMaterialExpressionSphereMask
- UMaterialExpressionSphericalParticleOpacity
- UMaterialExpressionSquareRoot
- UMaterialExpressionStaticBool
- UMaterialExpressionStaticBoolParameter
- UMaterialExpressionStaticComponentMaskParameter
- UMaterialExpressionStaticSwitch
- UMaterialExpressionStaticSwitchParameter
- UMaterialExpressionSubtract
- UMaterialExpressionTangent
- UMaterialExpressionTangentOutput
- UMaterialExpressionTemporalSobol
- UMaterialExpressionTerrainBlend
- UMaterialExpressionTerrainBlendBase
- UMaterialExpressionTerrainBlendDesert
- UMaterialExpressionTerrainBlendHeight
- UMaterialExpressionTerrainBlendHeightBlend
- UMaterialExpressionTexcoordAddressing
- UMaterialExpressionTextureBase
- UMaterialExpressionTextureCoordinate
- UMaterialExpressionTextureProperty
- UMaterialExpressionTextureSample
- UMaterialExpressionTextureSampleParameter
- UMaterialExpressionTextureSampleParameterSubUV
- UMaterialExpressionTime
- UMaterialExpressionTransform
- UMaterialExpressionTransformPosition
- UMaterialExpressionTruncate
- UMaterialExpressionVectorNoise
- UMaterialExpressionVectorParameter
- UMaterialExpressionVertexInterpolator
- UMaterialExpressionViewProperty
- UMaterialExpressionWorldPosition
- UMaterialFunction
- UMaterialInstance
- UMaterialInstanceDynamic
- UMaterialInterface
- UMaterialParameterCollection
- UMaterialParameterCollectionInstance
- UMaterialShaderQualitySettings
- UMediaPlayer
- UMediaPlaylist
- UMediaSoundComponent
- UMediaSource
- UMediaTexture
- UMenuAnchor
- UMeshComponent
- UMeshSimplificationSettings
- UMeshVertexPainterKismetLibrary
- UMicroTransactionBase
- UModelComponent
- UMorphTarget
- UMouseCursorBinding
- UMovementComponent
- UMoviePlayerSettings
- UMovieScene
- UMovieScene2DTransformSection
- UMovieScene3DAttachSection
- UMovieScene3DConstraintSection
- UMovieScene3DConstraintTrack
- UMovieScene3DPathSection
- UMovieScene3DTransformSection
- UMovieSceneActorReferenceSection
- UMovieSceneAudioSection
- UMovieSceneAudioTrack
- UMovieSceneBindingOverrides
- UMovieSceneBoolSection
- UMovieSceneBuiltInEasingFunction
- UMovieSceneByteSection
- UMovieSceneByteTrack
- UMovieSceneCameraAnimSection
- UMovieSceneCameraAnimTrack
- UMovieSceneCameraCutSection
- UMovieSceneCameraCutTrack
- UMovieSceneCameraShakeSection
- UMovieSceneCameraShakeTrack
- UMovieSceneCapture
- UMovieSceneCaptureEnvironment
- UMovieSceneCinematicShotSection
- UMovieSceneColorSection
- UMovieSceneColorTrack
- UMovieSceneComponentMaterialTrack
- UMovieSceneEasingExternalCurve
- UMovieSceneEnumSection
- UMovieSceneEnumTrack
- UMovieSceneEventRepeaterSection
- UMovieSceneEventSection
- UMovieSceneEventTimelinessSection
- UMovieSceneEventTrack
- UMovieSceneEventTriggerSection
- UMovieSceneFadeSection
- UMovieSceneFloatSection
- UMovieSceneFolder
- UMovieSceneIntegerSection
- UMovieSceneLevelVisibilitySection
- UMovieSceneLevelVisibilityTrack
- UMovieSceneMarginSection
- UMovieSceneMaterialParameterCollectionTrack
- UMovieSceneMaterialTrack
- UMovieSceneNewEventTrack
- UMovieSceneParameterSection
- UMovieSceneParticleParameterTrack
- UMovieSceneParticleSection
- UMovieSceneParticleTrack
- UMovieScenePropertyTrack
- UMovieSceneSection
- UMovieSceneSequence
- UMovieSceneSequencePlayer
- UMovieSceneSignedObject
- UMovieSceneSkeletalAnimationSection
- UMovieSceneSkeletalAnimationTrack
- UMovieSceneSpawnTrack
- UMovieSceneSplineSection
- UMovieSceneStringSection
- UMovieSceneSubSection
- UMovieSceneSubTrack
- UMovieSceneSubtitleSection
- UMovieSceneSubtitleTrack
- UMovieSceneTrack
- UMovieSceneVectorSection
- UMovieSceneVectorTrack
- UMovieSceneWidgetMaterialTrack
- UMultiBillBoardComponent
- UMultiLineEditableText
- UMultiLineEditableTextBox
- UNavArea
- UNavAreaMeta_SwitchByAgent
- UNavCollision
- UNavLinkComponent
- UNavLinkCustomComponent
- UNavLinkDefinition
- UNavLocalGridManager
- UNavModifierComponent
- UNavMovementComponent
- UNavRelevantComponent
- UNavigationDataChunk
- UNavigationGraphNodeComponent
- UNavigationInvokerComponent
- UNavigationPath
- UNavigationQueryFilter
- UNavigationSystem
- UNetConnection
- UNetDriver
- UNetworkSettings
- UnrealNetwork
- UObject
- UObjectLibrary
- UObjectPoolUtility
- UObjectReferencer
- UOceanCDLODMeshComponent
- UOceanFFTComponent
- UOceanGerstnerComponent
- UOceanMeshComponent
- UOverlapCheckAreaComponent
- UOverlay
- UOverlaySlot
- UPESkillPassiveSkill
- UPESkillWidget
- UPESkillWithPredict
- UPanelSlot
- UPanelWidget
- UPaperFlipbook
- UPaperFlipbookComponent
- UPaperGroupedSpriteComponent
- UPaperRuntimeSettings
- UPaperSprite
- UPaperSpriteAtlas
- UPaperSpriteBlueprintLibrary
- UPaperSpriteComponent
- UPaperSpriteSheet
- UPaperTerrainComponent
- UPaperTerrainMaterial
- UPaperTileLayer
- UPaperTileMap
- UPaperTileMapComponent
- UPaperTileSet
- UPartTypeSocket
- UParticleEmitter
- UParticleLODLevel
- UParticleModule
- UParticleModuleAcceleration
- UParticleModuleAccelerationBase
- UParticleModuleAccelerationConstant
- UParticleModuleAccelerationDrag
- UParticleModuleAccelerationDragScaleOverLife
- UParticleModuleAccelerationOverLifetime
- UParticleModuleAttractorLine
- UParticleModuleAttractorParticle
- UParticleModuleAttractorPoint
- UParticleModuleAttractorPointGravity
- UParticleModuleBeamModifier
- UParticleModuleBeamNoise
- UParticleModuleBeamSource
- UParticleModuleBeamTarget
- UParticleModuleCameraOffset
- UParticleModuleCollision
- UParticleModuleCollisionGPU
- UParticleModuleCollisionHeight
- UParticleModuleColor
- UParticleModuleColorBase
- UParticleModuleColorOverLife
- UParticleModuleColorScaleOverLife
- UParticleModuleColor_Seeded
- UParticleModuleEventGenerator
- UParticleModuleEventReceiverBase
- UParticleModuleEventReceiverKillParticles
- UParticleModuleEventReceiverSpawn
- UParticleModuleKillBox
- UParticleModuleKillHeight
- UParticleModuleLifetime
- UParticleModuleLifetime_Seeded
- UParticleModuleLight
- UParticleModuleLight_Seeded
- UParticleModuleLocation
- UParticleModuleLocationBoneSocket
- UParticleModuleLocationDirect
- UParticleModuleLocationEmitter
- UParticleModuleLocationEmitterDirect
- UParticleModuleLocationPrimitiveBase
- UParticleModuleLocationPrimitiveCylinder
- UParticleModuleLocationPrimitiveCylinder_Seeded
- UParticleModuleLocationPrimitiveSphere
- UParticleModuleLocationPrimitiveSphere_Seeded
- UParticleModuleLocationPrimitiveTriangle
- UParticleModuleLocationSkelVertSurface
- UParticleModuleLocationStVertSurface
- UParticleModuleLocationWorldOffset_Seeded
- UParticleModuleLocation_Seeded
- UParticleModuleMeshMaterial
- UParticleModuleMeshRotation
- UParticleModuleMeshRotationRate
- UParticleModuleMeshRotationRateMultiplyLife
- UParticleModuleMeshRotationRateOverLife
- UParticleModuleMeshRotationRate_Seeded
- UParticleModuleMeshRotation_Seeded
- UParticleModuleOrbit
- UParticleModuleOrbitBase
- UParticleModuleOrientationAxisLock
- UParticleModuleParameterDynamic
- UParticleModuleParameterDynamic_Seeded
- UParticleModulePivotOffset
- UParticleModuleRequired
- UParticleModuleRotation
- UParticleModuleRotationOverLifetime
- UParticleModuleRotationRate
- UParticleModuleRotationRateMultiplyLife
- UParticleModuleRotationRate_Seeded
- UParticleModuleRotation_Seeded
- UParticleModuleSize
- UParticleModuleSizeMultiplyLife
- UParticleModuleSizeScale
- UParticleModuleSizeScaleBySpeed
- UParticleModuleSize_Seeded
- UParticleModuleSourceMovement
- UParticleModuleSpawn
- UParticleModuleSpawnBase
- UParticleModuleSpawnPerUnit
- UParticleModuleSubUV
- UParticleModuleSubUVMovie
- UParticleModuleTrailSource
- UParticleModuleTypeDataAnimTrail
- UParticleModuleTypeDataBeam2
- UParticleModuleTypeDataGpu
- UParticleModuleTypeDataMesh
- UParticleModuleTypeDataRibbon
- UParticleModuleVectorFieldGlobal
- UParticleModuleVectorFieldLocal
- UParticleModuleVectorFieldRotation
- UParticleModuleVectorFieldRotationRate
- UParticleModuleVectorFieldScale
- UParticleModuleVectorFieldScaleOverLife
- UParticleModuleVelocity
- UParticleModuleVelocityBase
- UParticleModuleVelocityCone
- UParticleModuleVelocityInheritParent
- UParticleModuleVelocityOverLifetime
- UParticleModuleVelocityRibbon
- UParticleModuleVelocity_Seeded
- UParticleSystem
- UParticleSystemComponent
- UParticleSystemReplay
- UPathFollowingComponent
- UPathNameMappingDataAsset
- UPathNameMappingManager
- UPawnAction
- UPawnAction_BlueprintBase
- UPawnAction_Move
- UPawnAction_Repeat
- UPawnAction_Sequence
- UPawnAction_Wait
- UPawnActionsComponent
- UPawnMovementComponent
- UPawnNoiseEmitterComponent
- UPawnSensingComponent
- UPendingNetGame
- UPersistBaseComponent
- UPersistEffectBase
- UPersistEffectBuff
- UPersistEffectSkill
- UPersistEffectWithState
- UPhysicalAnimationComponent
- UPhysicalMaterial
- UPhysicsAsset
- UPhysicsCollisionHandler
- UPhysicsConstraintComponent
- UPhysicsConstraintTemplate
- UPhysicsHandleComponent
- UPhysicsSettings
- UPhysicsSpringComponent
- UPhysicsThrusterComponent
- UPixelProjectedReflectionComponent
- UPlanarReflectionComponent
- UPlaneReflectionCaptureComponent
- UPlatformEventsComponent
- UPlatformGameInstance
- UPlatformInterfaceBase
- UPlatformInterfaceWebResponse
- UPlatformMediaSource
- UPlayMontageCallbackProxy
- UPlayer
- UPlayerInput
- UPointLightComponent
- UPoseAsset
- UPoseWatch
- UPoseableMeshComponent
- UPostProcessComponent
- UPreviewMeshCollection
- UPrimaryAssetLabel
- UPrimaryDataAsset
- UPrimitiveComponent
- UProceduralFoliageComponent
- UProceduralFoliageSpawner
- UProceduralFoliageTile
- UProgressBar
- UProgressWidgetStyle
- UProjectileActionEffectBase
- UProjectileMovementComponent
- UProjectileMovementPathBase
- UProxyLODMeshSimplificationSettings
- URadialForceComponent
- UReflectionCaptureComponent
- URendererOverrideSettings
- URendererSettings
- URetainerBox
- UReverbEffect
- URichTextBlock
- URichTextBlockDecorator
- URig
- URotatingMovementComponent
- USCS_Node
- USTBaseBuffSystemComponent
- USTExtraGameMagnitudeCalculation
- USafeZone
- USafeZoneSlot
- UScaleBox
- UScaleBoxSlot
- USceneCaptureComponent
- USceneCaptureComponent2D
- USceneCaptureComponentCube
- USceneComponent
- UScrollBar
- UScrollBarWidgetStyle
- UScrollBox
- UScrollBoxSlot
- UScrollBoxWidgetStyle
- UShaderPlatformQualitySettings
- UShadowMapTexture2D
- UShapeComponent
- USimpleConstructionScript
- USimpleMeshComponent
- USizeBox
- USizeBoxSlot
- USkeletalBodySetup
- USkeletalMesh
- USkeletalMeshComponent
- USkeletalMeshReductionSettings
- USkeletalMeshSocket
- USkeleton
- USkinnedMeshComponent
- USkyLightComponent
- USlateBlueprintLibrary
- USlateBrushAsset
- USlateDataSheet
- USlateSettings
- USlateThemeManager
- USlateVectorArtData
- USlateWidgetStyleAsset
- USlider
- USoundAttenuation
- USoundBase
- USoundClass
- USoundConcurrency
- USoundCue
- USoundEffectSourcePresetChain
- USoundGroups
- USoundMix
- USoundNode
- USoundNodeAttenuation
- USoundNodeBranch
- USoundNodeConcatenator
- USoundNodeDelay
- USoundNodeDialoguePlayer
- USoundNodeDistanceCrossFade
- USoundNodeDoppler
- USoundNodeEnveloper
- USoundNodeGroupControl
- USoundNodeLooping
- USoundNodeMixer
- USoundNodeModulator
- USoundNodeModulatorContinuous
- USoundNodeOscillator
- USoundNodeParamCrossFade
- USoundNodeRandom
- USoundNodeSoundClass
- USoundNodeSwitch
- USoundNodeWaveParam
- USoundNodeWavePlayer
- USoundSourceBus
- USoundSubmix
- USoundWave
- USpacer
- USpectatorPawnMovement
- USphereComponent
- USphereReflectionCaptureComponent
- USpinBox
- USpinBoxWidgetStyle
- USplineComponent
- USplineComponentEditorModifer
- USplineMeshComponent
- USpotLightComponent
- USpringArmComponent
- UStackBox
- UStackBoxSlot
- UStaticMesh
- UStaticMeshComponent
- UStaticMeshIndoorVolumeComponent
- UStaticMeshIndoorVolumeContainerComponent
- UStaticMeshSocket
- UStaticMeshWidget
- UStereoLayerComponent
- UStereoLayerFunctionLibrary
- UStreamMediaSource
- UStreamingSettings
- USubUVAnimation
- USubmixEffectDynamicsProcessorPreset
- USubmixEffectReverbPreset
- USubmixEffectSubmixEQPreset
- USubsurfaceProfile
- USynthComponent
- UTextBinding
- UTextBlock
- UTextBlockWidgetStyle
- UTextLayoutWidget
- UTextPropertyTestObject
- UTextRenderComponent
- UTextTextureAtlas
- UTexture
- UTexture2D
- UTexture2DArray
- UTexture2DDynamic
- UTextureLODSettings
- UTextureLightProfile
- UTextureProperty
- UTextureRenderTarget
- UTextureRenderTarget2D
- UTextureRenderTargetCube
- UThrobber
- UTileMapBlueprintLibrary
- UTileView
- UTimelineComponent
- UTimelineTemplate
- UTireType
- UTouchInterface
- UTwitterIntegrationBase
- UUGCBackpackAvatarHandle
- UUGCCommonProduceDropItemComponent
- UUGCGamePartConfig
- UUGCItemWarehouseBase
- UUGCMotionComponent
- UUMGSequencePlayer
- UUTSkillManagerComponent
- UUniformGridPanel
- UUniformGridSlot
- UUniversalProjectileFilter
- UUserDefinedEnum
- UUserDefinedStruct
- UUserInterfaceSettings
- UUserRefStyle
- UUserWidget
- UUserWidgetSkin
- UUserWidgetStyle
- UUserWidgetUI
- UVectorField
- UVectorFieldAnimated
- UVectorFieldComponent
- UVectorFieldStatic
- UVehicleCommonComponent
- UVehicleSeatComponent
- UVerticalBox
- UVerticalBoxSlot
- UVideoCaptureSettings
- UViewport
- UVirtualJoystickResource
- UVisibilityBinding
- UVisualLoggerKismetLibrary
- UVolumetricFogBoxComponent
- UVolumetricFogSphereComponent
- UWST_AnchorData
- UWST_Bool
- UWST_ButtonListenAction
- UWST_ButtonStyle
- UWST_CheckBoxStyle
- UWST_ComboBoxStyle
- UWST_EditableTextBoxStyle
- UWST_EditableTextStyle
- UWST_Float
- UWST_Int32
- UWST_LinearColor
- UWST_Margin
- UWST_Name
- UWST_Object
- UWST_ProgressBarStyle
- UWST_ScrollBarStyle
- UWST_ScrollBoxStyle
- UWST_SlateBrush
- UWST_SlateChildSize
- UWST_SlateColor
- UWST_SlateFontInfo
- UWST_SlateSound
- UWST_SliderStyle
- UWST_SpinBoxStyle
- UWST_String
- UWST_Text
- UWST_TextBlockStyle
- UWST_UInt8
- UWST_Vector
- UWST_Vector2D
- UWST_WidgetTransform
- UWeakRefImage
- UWidget
- UWidget3DInstancedComponent
- UWidgetAnimation
- UWidgetAnimationDelegateBinding
- UWidgetBinding
- UWidgetBlueprintGeneratedClass
- UWidgetBlueprintLibrary
- UWidgetComponent
- UWidgetInteractionComponent
- UWidgetLayoutLibrary
- UWidgetNavigation
- UWidgetSkin
- UWidgetSkinProxy
- UWidgetSwitcher
- UWidgetSwitcherSlot
- UWidgetTree
- UWindDirectionalSourceComponent
- UWindow
- UWindowTitleBarArea
- UWindowTitleBarAreaSlot
- UWorldComposition
- UWorldParallelismBlueprintUtils
- UWrapBox
- UWrapBoxSlot
- VirtualItemManager

### 全部枚举列表

- AIPathCompVisSelectOP
- AI_Phase
- AkAcousticPortalState
- AkChannelConfiguration
- AkMultiPositionType
- AnimPhysAngularConstraintType
- AnimPhysAngularConstraintType_UE5
- AnimPhysCollisionType
- AnimPhysLinearConstraintType
- AnimPhysLinearConstraintType_UE5
- AnimPhysSimSpaceType
- AnimPhysSimSpaceType_UE5
- AnimPhysTwistAxis
- AnimalAnimListType
- AnimationCompressionFormat
- AnimationKeyFormat
- ArrayLabelEnum
- AudioPlotterActionType
- AudioPlotterModes
- AudioRegionProcessorType
- AvatarPawnState
- Beam2SourceTargetMethod
- Beam2SourceTargetTangentMethod
- BeamModifierType
- BehaviorState
- BLOCKYLUA_AUTO_SCROLL_TYPE
- ButtonImageSelectType
- ChatFlagType
- CopyBoneDeltaMode
- CopyState
- CustomGameAttributeType
- CylinderHeightAxis
- DistributionParamMode
- DragonBoatMatchState
- DragonBoatPathNodeType
- EABF_AvatarExtraPartType
- EAIActionSkillActionType
- EAIActionSkillTargetType
- EAIAttrCompareType
- EAIAttributeTestType
- EAIAvoidPlayerPathDir
- EAIBotType
- EAICheckShootingPoseType
- EAIDirectionTestType
- EAIDisguisedStateBehaviorType
- EAIEquipSpawnItemType
- EAIEventType
- EAIFindActorOfTypeStrategy
- EAIFindPickupItemType
- EAIFindableActorType
- EAIFollowFormationType
- EAIFollowSpeedType
- EAIFollowStatus
- EAIGCCOSResourceErrorCode
- EAIGCCOSResourceStatus
- EAIGCCOSResourceType
- EAIGCDeleteState
- EAIGCScanState
- EAIInteractableStatus
- EAIInteractableTags
- EAIInteractableType
- EAILiveState
- EAILockSource
- EAILogicResuming
- EAILostTombDebuffCasterType
- EAILostTombDebuffType
- EAILostTombSkillType
- EAIMovePose
- EAIMoveToOcclusionFinishMovePoseType
- EAIMoveToOcclusionMovingPoseType
- EAIMoveToOcclusionPoseType
- EAIMoveToOcclusionSearchBestOcclusionMethod
- EAIMoveType
- EAINewFocusPriority
- EAINewThrowProjectilePhase
- EAIOBPlayerInfoSource
- EAIOBPlayerState
- EAIOptionFlag
- EAIOrderType
- EAIParamType
- EAIPatrolPointDebugLineShowType
- EAIPoseState
- EAIProjectileModeType
- EAIRequestPriority
- EAISenseGrenadeType
- EAISenseNotifyType
- EAIShootingPose
- EAISkillActUnlockType
- EAIStatAliveState
- EAIStatBodyState
- EAIStatLocationState
- EAIStatObstacleType
- EAIStatParachuteState
- EAIStatProgressType
- EAIStatTeamBehavior
- EAIStatThrownType
- EAIStatVehicleLocationState
- EAIStateItemStateType
- EAIStateOperation
- EAISwitchPathFollowType
- EAITargetPointTrackType
- EAITaskPriority
- EAIThrowProjectilePhase
- EAITriggerAttrType
- EAIVehicleMoveGiveWayType
- EAIWarDogBodyState
- EAIWarningNotifyCharType
- EAIWayPointDebugLineShowTeam
- EAIWayPointDebugLineShowType
- EAIWayPointEventResult
- EAIWayPointEventType
- EAIWeaponShootType
- EAI_BlockType
- EAKEventDisableType
- EAKEventTag
- EARKitTextureType
- EARTrackingQuality
- EATTEditorScriptingFilterType
- EATTEditorScriptingStringMatchType
- EATTaskGraphState
- EATTaskNodeExcuteResult
- EATTaskNodeState
- EAT_PCManagerType
- EAVRefMatchLogic
- EAVRefPathMatchPattern
- EAVRefReferenceType
- EAVRefRelationType
- EAVRefRuleMode
- EAVRefWhitelistType
- EAccumulateEnergyByHitStatus
- EActionNodeState
- EActionStateType
- EActionTriggerType
- EActiveMoveStuckFailedReason
- EActivityClientRecoverType
- EActivityEctypeQuitReason
- EActivityUIShowMode
- EActorCacheID
- EActorFilterType
- EActorHiddenMask
- EActorInputEvent
- EActorMetricsType
- EActorSequenceObjectReferenceType
- EActorSpawnType
- EActorSpawnWay
- EAdManagerDelegate
- EAddMarkFlag
- EAddPlayerResult
- EAddPlayerToSceneResult
- EAddSkillActionType
- EAddSkillEffectPositionType
- EAddWeaponActionType
- EAddiontionDisplayDataType
- EAdditionDamageSubType
- EAdditionPropertyType
- EAdditionalBackpackItemDropReason
- EAdditionalBackpackItemPickupReason
- EAdditiveAnimationType
- EAdditiveBasePoseType
- EAddonControlCharacterPolicyOnDeath
- EAddonGraphNodeAttributeStructType
- EAddonGraphNodeEventKillNodeType
- EAddtiveFOVState
- EAddtiveTransOffsetState
- EAerofoilType
- EAffectSightType
- EAiGMParamType
- EAiModelErrorType
- EAiModelEventType
- EAiModelLogicType
- EAirAbsorptionMethod
- EAirAttackGenerateType
- EAirAttackInfo
- EAirAttackMode
- EAirDropBoxReportType
- EAirDropBoxSimulateCloseType
- EAirDropType
- EAirWallShapeType
- EAirlineType
- EAllAttachmentSet
- EAllowEditsMode
- EAllowGiveUpType
- EAllowThrowMode
- EAlphaBlendOption
- EAlphaStateEnum
- EAmmoDisplayType
- EAndroidAntVerbosity
- EAndroidAudio
- EAndroidDepthBufferPreference
- EAndroidGraphicsDebugger
- EAndroidInstallLocation
- EAndroidScreenOrientation
- EAngleRotationDirectionType
- EAngledSightType
- EAngularConstraintMotion
- EAngularDriveMode
- EAnim3DTransformSource
- EAnim3DTransformType
- EAnim3DTransformWarpingTargetType
- EAnimAssetConfigType
- EAnimAssetCurveFlags
- EAnimBPType
- EAnimCurveType
- EAnimGroupRole
- EAnimHurtingTarget
- EAnimIKClassification
- EAnimInterpolationType
- EAnimKeepBoneRetargetFeatureConfigType
- EAnimLayerType
- EAnimLinkMethod
- EAnimNotifyEventType
- EAnimSeqCheckMode
- EAnimStateType
- EAnimToTextureAnimState
- EAnimToTextureBonePrecision
- EAnimToTextureMode
- EAnimToTextureNumBoneInfluences
- EAnimalDeliverStrategy
- EAnimalMovePose
- EAnimalState
- EAnimalType
- EAnimationMode
- EAnimationViewportCameraFollowMode
- EAntiAliasingMethod
- EAntiCheatShoot
- EAppChannelType
- EAppleARKitHitTestResultType
- EApplicationState
- EApplicationStrategy
- EApplyImpactPhysicsForcesDir
- EApplyStatus
- EAquariumLayerCategory
- EAquariumLayerType
- EArState
- EArcadeVehicleAdditionAccelerateType
- EArcadeVehicleDriftState
- EArchiveDataType
- EAreaCleanupActorType
- EAreaOverlapCheckState
- EAreaOverlapCheckType
- EAreaTagPossessorType
- EAreaTypeFlags
- EArithmeticKeyOperation
- EArithmeticOperationType
- EArmorLevel
- EArmorTypeEnum
- EArtPerfVisualizationMode
- EAsianGamesTeamColor
- EAskQPropertyVisibility
- EAspectRatioAxisConstraint
- EAssetEditorOpenLocation
- EAssetPathType
- EAssetReferenceRelation
- EAssetReferenceType
- EAssetSetManagerResult
- EAsyncIsPakDownloadedInPin
- EAttachLocation
- EAttachVehicleLeavePos
- EAttachVehicleShapeCollisionEnableType
- EAttachVehicleShapeControlType
- EAttachmentRule
- EAttenuationDistanceModel
- EAttenuationShape
- EAttrClientPlayerType
- EAttrClientShowMode
- EAttrIntConvertType
- EAttrOperator
- EAttrOperator_DoChange
- EAttrVariableType
- EAttractorParticleSelectionMethod
- EAttracttedTargetType
- EAudioOutputTarget
- EAudioRecordingMode
- EAudioRegionEventType
- EAutoAimType
- EAutoAimingTaskConfigType
- EAutoChangeMode
- EAutoColumnType
- EAutoEndTaskType
- EAutoExposureMethod
- EAutoExposureMethodUI
- EAutoLockSortMethord
- EAutoLockVisibilityLocation
- EAutoLockVisibilityType
- EAutoPossessAI
- EAutoReceiveInput
- EAutoSwitchDSState
- EAutomationArtifactType
- EAutomationEventType
- EAutomationState
- EAvailableForSale
- EAvatarAnimAdapt_WingType
- EAvatarAsyncLoadRequestState
- EAvatarAsyncLoadRequestType
- EAvatarCategories
- EAvatarComponentType
- EAvatarCustomAbilityType
- EAvatarDamagePosition
- EAvatarDetailMode
- EAvatarDisplayAnimType
- EAvatarDownloadActorType
- EAvatarDownloadSourceType
- EAvatarEmoteType
- EAvatarGender
- EAvatarHandleLODMatCheckPathType
- EAvatarIdleState
- EAvatarIntegrationDataTableType
- EAvatarLobbySettingType
- EAvatarMatCutCondition
- EAvatarMatDynamicParameterType
- EAvatarMaterialParamType
- EAvatarModule
- EAvatarNewFPPMatSetType
- EAvatarResIdType
- EAvatarResTeamRelationType
- EAvatarRole
- EAvatarSlotFeatureTag
- EAvatarSlotType
- EAvatarSlotVarType
- EAvatarStrategyType
- EAvatarStyle
- EAvatarSubSlot
- EAvatarSubSystemCreationMethod
- EAvatarTimeSliceMatInterruptInstruction
- EAvatarTimeSliceMatPlayMode
- EAvatarVehicleState
- EAvatarVehicleStatus
- EAvatarVisiblityType
- EAxis
- EAxisOption
- EAxisType
- eAnimState
- eAttackState
- EBGMStatus
- EBLEFunctionID
- EBPCTarget
- EBSSkillActionType
- EBTBlackboardRestart
- EBTChildIndex
- EBTDecoratorLogic
- EBTFlowAbortMode
- EBTNodeResult
- EBTParallelMode
- EBTTask_FindAIWorldVolumeActorType
- EBTTeleportFailedReason
- EBTUnsuitableDeliveryReason
- EBUIProperty
- EBUIStatusFlag
- EBackPackLevel
- EBackpackDragSlot
- EBackpackHandleVehicleType
- EBackpackItemCommonAttachTypeGlobal
- EBackpackItemCommonSocketTypeGlobal
- EBackpackItemOperateMsgType
- EBackpackItemState
- EBackpackItemType
- EBackpackType
- EBasicKeyOperation
- EBasicMoveAntiStrategy
- EBatchModeType
- EBatchModifySpace
- EBatchOprationType
- EBatchTaskControlType
- EBattleAvatarDisplayActionType
- EBattleFieldCamp
- EBattleFieldEnemyType
- EBattleFieldModeType
- EBattleItemClientPickupType
- EBattleItemDisuseReason
- EBattleItemDropReason
- EBattleItemIconType
- EBattleItemOperationFailedReason
- EBattleItemOperationType
- EBattleItemPickupReason
- EBattleItemRepType
- EBattleItemUseReason
- EBattleResultTeamNum
- EBattleSceneAvatarDisplayType
- EBattleTextType
- EBeaconConnectionState
- EBeam2Method
- EBeamTaperMethod
- EBeastKind
- EBeastType
- EBigAirShipMoveType
- EBigWorldItemType
- EBigWorldServerArea
- EBigWorldTaskInfoPropertyType
- EBigWorldTaskInitState
- EBigWorldTaskNodeState
- EBigWorldTaskOperType
- EBigWorldTaskType
- EBindingKind
- EBlackBoardEntryComparison
- EBlackboardFormationTestLogic
- EBlendListTransitionType
- EBlendMode
- EBlendSpaceAxis
- EBlendableLocation
- EBlockButtonType
- EBlockNestType
- EBlockObjType
- EBlockState
- EBlockyAccessType
- EBlockyBPToolButtonType
- EBlockyBinaryOperation
- EBlockyBlockTypeGroup
- EBlockyCurrentGraphBlockyNumberType
- EBlockyFunctionArgumentAttribute
- EBlockyListItemType
- EBlockyLogMsgMode
- EBlockyLuaAnyType
- EBlockyLuaCopyMode
- EBlockyLuaOperationState
- EBlockyLuaParamType
- EBlockyLuaStubArgType
- EBlockyLuaUndoRedo
- EBlockySelectionMode
- EBlockyToolButtonType
- EBlockyUnaryOperation
- EBlockyValueType
- EBlockyVarInitType
- EBlockyVariableType
- EBlockyVisitMode
- EBloomMethod
- EBlueprintBreakpointReloadMethod
- EBlueprintCompileMode
- EBlueprintNativizationFlag
- EBlueprintPinStyleType
- EBlueprintStatus
- EBlueprintType
- EBlueprintUsage
- EBlueprintWarningBehavior
- EBlurType
- EBodyCollisionResponse
- EBodyDamageType
- EBodyPartName
- EBodyPosition
- EBoneAxis
- EBoneControlSpace
- EBoneForwardAxis
- EBoneForwardAxis_UE5
- EBoneMirrorType
- EBoneModificationMode
- EBoneRotationSource
- EBoneShiftTolerencePolicy
- EBoneSpaces
- EBoneTranslationRetargetingMode
- EBoneVisibilityStatus
- EBossBattleFieldState
- EBotCategray
- EBotChannelCloseCode
- EBotChannelState
- EBotConnectionState
- EBountyBuyingResultType
- EBreakReloadType
- EBrushType
- EBuffApplierCondition
- EBuildingActionType
- EBuildingActorConstructingMode
- EBuildingDirection
- EBuildingMode
- EBuildingPositionType
- EBuildingStateType
- EBuildingType
- EBuildingViewType
- EBulletHitActionAddBuffTeamType
- EBulletImpactDir
- EBulletShootBlockVerifyRes
- EBulletTraceCriticalVerify
- EBulletTrackCriticalVerify
- EBurnTireDifferentialType
- EBusEffectSlotType
- EButtonClickMethod
- EButtonClickSoundTypes
- EButtonEventType
- EButtonInputActionEvent
- EButtonListenActionEvent
- EButtonPressMethod
- EButtonReleasedReason
- EButtonTouchMethod
- eBattleFieldMode
- ECAM_ActorState
- ECDCompare
- ECDType
- ECG36MusicGameHitLevel
- ECHPTMode
- ECJActorMovementCompensationMode
- ECJFootPlacementLockType
- ECJPelvisHeightMode
- ECNP_Operation_Type
- ECNP_Target_Type
- ECOSResourceErrorCode
- ECOSResourceStatus
- ECOSResourceType
- ECOSResourceUpdateType
- ECSVImportType
- ECVarType
- ECableCarRunningState
- ECableCarState
- ECableNoiseState
- ECacheType
- ECallServerMoveUseRelativeControlRotationType
- ECallStackType
- ECallingVehicleResult
- ECamShakeType
- ECameraAlphaBlendMode
- ECameraAnimPlaySpace
- ECameraBorderType
- ECameraCurveAnimType
- ECameraDataLerpFunction
- ECameraDataOperateType
- ECameraDataType
- ECameraFocusMethod
- ECameraModeSwitchResult
- ECameraPosType
- ECameraProjectionMode
- ECampRelation
- ECanBeCharacterBase
- ECanCreateConnectionResponse
- ECanShowKillThanksUIOperation
- ECancelHostingReason
- ECarRacingRoadManagerState
- ECarringState
- ECellPlacementStrategy
- EChainState
- EChangeWeaponEffectType
- EChangeWeatherReason
- ECharAnimAdditiveType
- ECharAnimEventType
- ECharLikeMonsterAnimType
- ECharLikeMonsterStateType
- ECharOperationType
- ECharWeaponAnimType
- ECharaAnimListType
- ECharaHorseAnimListType
- ECharacterAdditionalWeaponSwitchAnimType
- ECharacterAnimOverrideType
- ECharacterAnimType
- ECharacterAnimTypeAsynLoaded
- ECharacterAvatarState
- ECharacterAvatarVisibilityMaskType
- ECharacterBodyAnimHurtType
- ECharacterDyingWeaponAnimType
- ECharacterFollowProgress
- ECharacterGender
- ECharacterHealthStatus
- ECharacterHorseAnimGrenadeType
- ECharacterJumpPhase
- ECharacterJumpType
- ECharacterMeshClipType
- ECharacterModeType
- ECharacterMovementDisableTickMask
- ECharacterNewFPPAnimType
- ECharacterParachuteAnimType
- ECharacterParachuteMultiAnimType
- ECharacterParachuteQuadAnimType
- ECharacterPoseType
- ECharacterShieldAnimType
- ECharacterShovelAnimType
- ECharacterShowSceneType
- ECharacterVehicleAnimType
- ECharacterVehicleHorseAnimType
- ECharacterViewType
- EChartAggregationMode
- ECheatCommandAirDropType
- ECheatCommandResultType
- ECheatCommandType
- ECheckAreaCompStartCheckMethodInEventMode
- ECheckBoxState
- ECheckEscapeType
- ECheckImpartedMovementBaseVelocity
- ECheckInteractPhase
- ECheckJumpPointResult
- ECheckPakStateType
- ECheckPointType
- ECheckResult
- ECheckTagretResult
- EChooseEnemySearchMethod
- EChooseEnemyType
- ECircleStatus
- EClampMode
- EClassLoadBeginTime
- EClassLoadType
- EClassMemberQueryMode
- EClassViewerDeveloperType
- EClearDroppedActorCategory
- EClearSceneOptions
- EClickActorExcuteSide
- EClickDetectionType
- EClickInteractSortType
- EClickOverlapCheckType
- EClickUIInfoAnchorType
- EClientActionSetPersistentType
- EClientCheckType
- EClientCompleteReplayModeType
- EClientFatalDamageRecordCustomDataType
- EClientFatalItemType
- EClientReplayFeature
- EClientRequestType
- EClientTaskStatus
- EClimbResult
- EClimbState
- EClosure_RunSide
- EClothingWindMethod
- ECloudStorageDelegate
- EColdModeItemType
- ECollectedEventDataEventId
- ECollectionKeyPolicy
- ECollisionChannel
- ECollisionEnabled
- ECollisionLimitType
- ECollisionLimitType_UE5
- ECollisionResponse
- ECollisionShape
- ECollisionSourceType
- ECollisionTraceFlag
- ECollisionType
- EColorChannel
- EColorChannelType
- EColorPickerModes
- EColorSliderChannels
- EColorVisionDeficiency
- ECombatDroneRewardPointType
- ECombinationSharedPermissions
- ECombineMoveNotRestoreRotationMask
- ECommMiniMapItemLayerType
- ECommMiniMapItemType
- ECommMiniMapRefreshType
- ECommMiniMapScaleType
- ECommMiniMapType
- ECommandExecuteType
- ECommandFailureType
- ECommandOperationType
- ECommentBoxMode
- ECommonRevivalTriggerType
- ECommonTlogInterface
- ECommonTlogPos
- ECommonTlogValue
- ECompAttachType
- ECompareAngleType
- ECompareConditionResult
- ECompareLengthType
- ECompareLogicAndOr
- ECompareLogicType
- ECompareOperation
- ECompareOperationType
- ECompareRule
- ECompareType
- EComparisonMethod
- EComparisonTolerance
- ECompilerVersion
- EComponentCreationMethod
- EComponentDeferredMode
- EComponentListDataDiffLevel
- EComponentListDataItemType
- EComponentMobility
- EComponentSocketType
- EComponentType
- ECompositeTextureMode
- ECompositingSampleCount
- ECompressionLibraryFlags
- EComputeNTBsOptions
- EConcertActivityType
- EConcertEventType
- EConcertPlayerState
- EConditionHeathType
- EConditionNodeResult
- EConditionOperator
- EConditionType
- EConfigDefaultValueRestrictionMode
- EConfigFileSourceControlStatus
- EConfigSettingMode
- EConnectionCheckState
- EConnectionType
- EConsoleCommandPriority
- EConsoleForGamepadLabels
- EConsoleType
- EConstraintFrame
- EConstraintOffsetOption
- EConstraintTransform
- EConstraintType
- EConstructBuildingType
- EConstructGroupRuleType
- EConstructMode
- EConstructRuleType
- EConstructType
- EConstructionMode
- EConsumeItemCategory
- EConsumeItemType
- EConsumeMouseWheel
- EContainInType
- EContainerCollisionRotationAxisType
- EContentSourceCategory
- EContentType
- EContextTargetFlags
- EControlConstraint
- EControllerAnalogStick
- EControllerHand
- ECookMode
- ECookProgressDisplayMode
- ECookReason
- ECookRequestFlags
- ECookTickFlags
- ECookerStatsObjectSets
- ECopyMotion_Component
- ECopyType
- ECrossHairSpreadType
- ECsgOper
- ECullingStrategy
- ECurrencyType
- ECurveBlendOption
- ECurveEditorCurveVisibility
- ECurveEditorTangentVisibility
- ECurveMoveMotionWarpingType
- ECurvePlayerEndType
- ECurveSportLoopType
- ECurveType
- ECustomActorForwardDir
- ECustomBlackboardPropertyValueType
- ECustomBlockType
- ECustomCndEventType
- ECustomCullingBoxType
- ECustomDamageEventReactionType
- ECustomDamageEventTriggerType
- ECustomDataType
- ECustomDepthStencil
- ECustomEquipItemReason
- ECustomFastDrawInterruptType
- ECustomFbxExportCompatibility
- ECustomFlyingMoveFlag
- ECustomFlyingMoveMode
- ECustomMaterialOutputType
- ECustomMoveModeStartRole
- ECustomMovementMode
- ECustomMovmentMode
- ECustomMovmentModeCD
- ECustomParamType
- ECustomQueryMobilityType
- ECustomServerMoveResultFlags
- ECustomSimpleFlyingDirType
- ECustomSkillDelayType
- ECustomTableConfig_ValueType
- ECustomTickRoleType
- ECustomTickType
- ECustomUIType
- ECustomWalkingDirType
- ECustomizedToolMenuVisibility
- eCrowdMoveType
- EDDMCFindType
- EDOFMode
- EDPCompareType
- EDPSourceType
- EDVPCActivateType
- EDamageBoxDetectType
- EDamageEventFlags
- EDamageModifyMethodType
- EDamageModifyPhase
- EDamageNumberEvictionPolicy
- EDamageNumberStartPosition
- EDamageType
- EDamageableGameObjectType
- EDataReporterType
- EDataTableType
- EDataTableViewFilterCategory
- EDataValidationResult
- EDataValidationUsecase
- EDeadDropItemType
- EDeadZoneType
- EDealMethod
- EDeathMatchDamageResult
- EDeathMatchGameEndType
- EDeathMatchGlobalAudioType
- EDeathMatchGlobalNotifyReason
- EDeathMatchPersonalMedalType
- EDeathMatchPersonalNotifyReason
- EDeathMatchSubModeType
- EDeathMatchWWISENotifyReason
- EDeathReplayRecordEventType
- EDebugLineNetMode
- EDebugViewChannel
- EDecalBlendMode
- EDecompressionType
- EDecoratorLogicMode
- EDefaultBackBufferPixelFormat
- EDefaultLocationUnit
- EDeferredFlag
- EDefinitionValidityType
- EDeformEffectType
- EDelayRenderRequestState
- EDelegateProvider
- EDeleteDisplayeType
- EDeliverTargetLimitAreaType
- EDeltaRotationTest
- EDemoPlayFailure
- EDepositMLAIType
- EDepthOfFieldFunctionValue
- EDepthOfFieldMethod
- EDescendantScrollDestination
- EDesignPreviewSizeMode
- EDetachmentRule
- EDetailMode
- EDeviceQualityTier
- EDeviceVisibilityStrategy
- EDialogueSpeakerType
- EDialogueVoiceType
- EDifferentTeammateReportingType
- EDir
- EDirection
- EDirection8
- EDisplayQuality
- EDisplayWeaponType
- EDistanceWithNPC
- EDistributionMode
- EDistributionVectorLockFlags
- EDistributionVectorMirrorFlags
- EDolphinDancerPoseState
- EDolphinDancerState
- EDoorState
- EDoorSyncTriggerBoxType
- EDoubleVaultState
- EDragBackpackItemMsgType
- EDragDirectionMode
- EDragDropMode
- EDragIntent
- EDragPivot
- EDrawDebugItemType
- EDrawDebugTrace
- EDrawDyeingMode
- EDriftInputSerializeFlag
- EDriveCar
- EDrivenBoneModificationMode
- EDrivenDestinationMode
- EDrivingCheckPointState
- EDroneState
- EDropGroupType
- EDropItemAnimState
- EDropItemCategory
- EDropItemListGeneratorType
- EDropItemParitcleType
- EDropItemParitcleloadType
- EDropItemPerformanceMethod
- EDropItemPositionType
- EDropItemStrategyType
- EDropItemTraceMethod
- EDropItmeLimitType
- EDropPattern
- EDropRuleItemPackageMode
- EDropType
- EDropdownSchemeTypes
- EDualWeaponFireType
- EDuelingArenaType
- EDungeonSwitch
- EDuoActionPerformanceLocation
- EDupVerifyMethod
- EDuplicateModuleCheckMode
- EDyingFaceRotBlendType
- EDynaCanvasPanelAutoLoadType
- EDynaConfigEnum
- EDynaConfigNetExecutionPolicy
- EDynaConfigOwner
- EDynaConsoleVariableNetExecutionPolicy
- EDynamicActorScene
- EDynamicCompType
- EDynamicForceFeedbackAction
- EDynamicLoadingAnimType
- EDynamicNavAffectorUpdateMode
- EDynamicWeatherExMgrActivityStatus
- EditColor
- EEMPZoneGenerateType
- EEMPZoneState
- EEQCompareOp
- EEQSNormalizationType
- EESPlayerRstType
- EESPlayerSettleReason
- EESPlayerType
- EESplayerColorCampType
- EEarlyZPass
- EEaseType
- EEasingFunc
- EEasingType
- EEdGraphPinDirection
- EEdGraphSchemaAction_K2Graph
- EEditorArchiveDataType
- EEditorResToolRenameType
- EEditorScriptingFilterType
- EEditorScriptingStringMatchType
- EEditorToolColorChannel
- EEffectAdjustType
- EEffectModifierAutoReflectParamType
- EEffectModifierGenericParamType
- EEffectSpreadState
- EElecMusicState
- EElevatorOp
- EElevatorOrderSortMode
- EElevatorStatus
- EEmitterDynamicParameterValue
- EEmitterNormalsMode
- EEmitterRenderMode
- EEmitterRotationMode
- EEmitterSelfRotationMode
- EEmitterType
- EEmoteAIEvent
- EEmoteEndReason
- EEmoteMesh
- EEmoteType
- EEndPlayReason
- EEnemyType
- EEntitlementCacheLevelRequest
- EEntitlementCacheLevelRetrieved
- EEntityMemberAnimSharingState
- EEnvDirection
- EEnvOverlapShape
- EEnvQueryHightlightMode
- EEnvQueryParam
- EEnvQueryRunMode
- EEnvQueryStatus
- EEnvQueryTestClamping
- EEnvQueryTrace
- EEnvTestCost
- EEnvTestDistance
- EEnvTestDot
- EEnvTestFilterOperator
- EEnvTestFilterType
- EEnvTestPathfinding
- EEnvTestPurpose
- EEnvTestScoreEquation
- EEnvTestScoreOperator
- EEnvTestWeight
- EEnvTraceShape
- EEnvironmentType
- EEscalatorApplySpeedType
- EEscapeActorType
- EEscapeAttachmentSlotType
- EEscapeEquipReservedReason
- EEscapeFightingState
- EEscapeGalleryCrossHairType
- EEscapeGalleryExhibitType
- EEscapeGameDifficultyType
- EEscapeGameType
- EEscapeGoldRaceBattleType
- EEscapeModeElevatorStateType
- EEscapeModePlayerType
- EEscapeMonsterDoingState
- EEscapeSupplyBoxType
- EEscapeType
- EEvaluateCurveTableResult
- EEvaluationMethod
- EEvaluationRunSide
- EEvaluatorDataSource
- EEvaluatorMode
- EEventDataCollectionValues_CG008_QiXiFestival_Action
- EEventDataCollectionValues_MicSpeakerState_Mic
- EEventDataCollectionValues_MicSpeakerState_Speaker
- EEventDataCollectionValues_RankList_Type
- EExcavatorPoseType
- EExcavatorState
- EExcellentOperationPosType
- EExcellentOperationResultType
- EExcellentOperationStartResult
- EExecuteAirDropOrderResult
- EExecuteType
- EExitBehaviorReason
- EExitFollowReason
- EExplosionEnvironment
- EExplosionTrigger
- EExposedCompareType
- EExposedType
- EExtraAnimDataType_FastDraw
- EExtraAnimDataType_MoveAimExtend
- EExtraHatredConditionType
- EExtraInvalidCondition
- EExtraWeaponUIType
- eEntityMemberAnimationState
- eEntityState
- eEntityTpye
- EFBXAnimationLengthImportType
- EFBXExpectedResultPreset
- EFBXImportContentType
- EFBXImportType
- EFBXNormalGenerationMethod
- EFBXNormalImportMethod
- EFBXSceneNormalGenerationMethod
- EFBXSceneNormalImportMethod
- EFBXSceneOptionsCreateHierarchyType
- EFBXTestPlanActionType
- EFPCacheState
- EFPPCameraDataType
- EFRRSerializeFlag
- EFRR_Movetype
- EFRR_TYPE
- EFaceHiddenState
- EFaceRotCheckRetType
- EFacilityUniqueID
- EFacingDirectionMode
- EFadeCurveType
- EFakePlayerType
- EFarmOperationType
- EFarmPlantState
- EFastDestructibleState
- EFastDrawInterruptActionType
- EFastImpactType
- EFatalDamageMaxKillStatus
- EFatalDamageRelationShip
- EFbxExportCompatibility
- EFbxSceneReimportStatusFlags
- EFbxSceneVertexColorImportOption
- EFeaturePackDetailLevel
- EFeatureSetType
- EFeedbackDumpObjectType
- EFieldLogicApplyType
- EFieldLogicSerializationType
- EFieldLogicType
- EFieldOfViewNotificationStatus
- EFielddLogicFalloffType
- EFigmaActionMedia
- EFigmaActionNodeNavigation
- EFigmaActionType
- EFigmaAxisSizingMode
- EFigmaBlendMode
- EFigmaComponentPropertyType
- EFigmaCounterAxisAlignContent
- EFigmaCounterAxisAlignItems
- EFigmaEasingType
- EFigmaFileState
- EFigmaFileType
- EFigmaInputDevice
- EFigmaLayoutAlign
- EFigmaLayoutConstraintHorizontal
- EFigmaLayoutConstraintVertical
- EFigmaLayoutMode
- EFigmaLayoutPositioning
- EFigmaLayoutSizing
- EFigmaLayoutWrap
- EFigmaLineType
- EFigmaOverflowDirection
- EFigmaPrimaryAxisAlignItems
- EFigmaStrokeAlign
- EFigmaStrokeCap
- EFigmaStrokeJoin
- EFigmaStyleType
- EFigmaTextAlignHorizontal
- EFigmaTextAlignVertical
- EFigmaTextAutoResize
- EFigmaTextCase
- EFigmaTextDecoration
- EFigmaTextTruncation
- EFigmaTransitionType
- EFigmaTriggerType
- EFileArchiveMode
- EFilterConditionType
- EFilterEditorType
- EFilterInterpolationType
- EFilterSkillEditorPawnType
- EFindFormationMemberStrategy
- EFindPointOnNavmeshType
- EFindReachablePos_SearchDirection
- EFinderShape
- EFireEventsAtPosition
- EFireResetType
- EFishHiddenReason
- EFlattenMaterialProperties
- EFlipbookAniType
- EFlipbookCollisionMode
- EFlowLightEmoteType
- EFlowLightGenderType
- EFlowNodeType
- EFlyPatrolRelativeCenterType
- EFlyTargetLocHeightSetType
- EFocusCause
- EFocusTurnTargetResult
- EFoliageScaling
- EFollowEmoteErrorCode
- EFollowMethod
- EFollowState
- EFontCacheType
- EFontFallback
- EFontHinting
- EFontImportCharacterSet
- EFontLayoutMethod
- EFontLoadingPolicy
- EFootStepState
- EFootprintType
- EFormatArgumentType
- EFortressContainerState
- EFortressDoorCategory
- EFortressDoorState
- EFracturedAxis
- EFracturedClipType
- EFracturedEditorPreviewType
- EFracturedImpactEffType
- EFracturedMeshConnectionType
- EFracturedMeshDestructibleAction
- EFracturedUV
- EFreeCombinationVoicePlayConflictType
- EFreeCombinationVoiceWaitConflictType
- EFreshWeaponStateType
- EFresnelPlayState
- EFrictionCombineMode
- EFullyLoadPackageType
- EFunctionInputType
- EFunctionalTestResult
- EFusionOperator
- EFutureCarrierMoveType
- eFilterChannel
- eFollowWaypointType
- EGBufferFormat
- EGGameGalleryType
- EGIFPlayStrategy
- EGISActionChainFailAction
- EGISActionChainMode
- EGISActionStatus
- EGISActorActionType
- EGISConditionCheckMethod
- EGISOperatorType
- EGISRunSIde
- EGISUIActionType
- EGMDataType
- EGMPUnitTestEnum1
- EGMPUnitTestEnum2
- EGMPUnitTestEnum3
- EGMPUnitTestEnum4
- EGMPUnitTestScopedEnumInt16
- EGMPUnitTestScopedEnumInt32
- EGMPUnitTestScopedEnumInt64
- EGMPUnitTestScopedEnumInt8
- EGMPUnitTestScopedEnumUint16
- EGMPUnitTestScopedEnumUint32
- EGMPUnitTestScopedEnumUint64
- EGMPUnitTestScopedEnumUint8
- EGPCompareType
- EGPSourceType
- EGT_LockPPType
- EGT_TestActivityEvent
- EGT_TestPersistEffectEvent
- EGUCM_RETFUNC_TYPE
- EGalaxyFaceMaskType
- EGalaxyFaceSceneType
- EGalleryAvatarType
- EGameAttributeCategory
- EGameAttributeValueType
- EGameFeatureContainerModifyMethod
- EGameFeatureFileCellHandleType
- EGameFeatureFileCellValueRelation
- EGameFeatureFileRootType
- EGameMap
- EGameModeActorState
- EGameModeType
- EGameModeWeaponModuleSchemeType
- EGameMsgType
- EGamePawnEvent
- EGameplayCondition_OperatorType
- EGameplayCondition_SpeedType
- EGameplayContainerMatchType
- EGameplayDebuggerOverrideMode
- EGameplayFeaturePropertyType
- EGameplayFeatureRootType
- EGameplayStateOp
- EGameplayTagAnimListCompType
- EGameplayTagEventTypeNew
- EGameplayTagMatchType
- EGameplayTagQueryExprType
- EGameplayTagSourceType
- EGameplayTaskRunResult
- EGameplayTaskState
- EGender
- EGenerateItemEntityType
- EGenerateItemReason
- EGeneratedContentType
- EGeneratorState
- EGenericAICheck
- EGenericAbilityOperationType
- EGenericAbilityWorkSide
- EGenericAvatarDisplayOperation
- EGenericAvoidanceGroup
- EGenericCharacterAnimSharingState
- EGenericCharacterSubAnimParamType
- EGenericMoveState
- EGenericReportID
- EGenericSidesShiftSideWays
- EGenericStateOp
- EGetChargeTimeType
- EGitFileStatus
- EGizmoHandleTypes
- EGizmoPlacement
- EGlobaleTriggerVolumeSafety
- EGoogleVRCaps
- EGoogleVRMode
- EGradeScoreType
- EGradeType
- EGrammaticalGender
- EGrammaticalNumber
- EGraphAxisStyle
- EGraphDataStyle
- EGraphPanningMouseButton
- EGraphType
- EGraphViewType
- EGraphaQuality
- EGraphicsPreset
- EGrassScaling
- EGrenadeType
- EGridCompressFlag
- EGridIntervalType
- EGridRotateState
- EGridTransformAxis
- EGroundSprintMode
- EGroupBackpackScheme
- EGunKickType
- EGunLocIDToPointType
- EGunMasterEventID
- EGundamModelStatus
- eGroupType
- EHBAOBlurRadius
- EHDRCaptureGamut
- EHISMCullState
- EHLConstructionDataVersion
- EHLDecorationDataVersion
- EHLDecorationOperation
- EHLErrorCode
- EHLODBatchingPolicy
- EHMDTrackingOrigin
- EHMDWornState
- EHandlePickUpActionReplicatedDataActionType
- EHardPoinRegionType
- EHardPointManagerState
- EHardPointOccupyState
- EHardwareClass
- EHasCustomNavigableGeometry
- EHealthPredictShowType
- EHearSoundCharacterType
- EHelicopterHeightCorrectType
- EHelicopterState
- EHeroAISkillType
- EHeroGameModeType
- EHeroType
- EHideAndSeekCampType
- EHideAndSeekRespawnReason
- EHideAndSeekRoundStateType
- EHierarchicalLODActionType
- EHierarchyQueryMode
- EHintUIType
- EHitDir
- EHitFeedbackType
- EHitModeType
- EHitPartJugementType
- EHitTestAreaPolicyType
- EHomeAuditState
- EHomeAvatarDisplayOperation
- EHomeAvatarDisplaySlotType
- EHomeAvatarDisplayType
- EHomeBlueprintType
- EHomeCatAnimState
- EHomeConstructSnapType
- EHomeCrossHair
- EHomeFishGroupType
- EHomeFishMoveType
- EHomeInstanceType
- EHomeItemRepType
- EHomeItemType
- EHomeItemsSortType
- EHomeNpcOptionType
- EHomePawnState
- EHomePetGetHomeLocationType
- EHomeStoreGlobalEventType
- EHomeStoreItemType
- EHomelandActivityState
- EHomelandAddActorPositionPolicy
- EHomelandCommonAuthType
- EHomelandConstructRPCType
- EHomelandDataTag
- EHomelandMutexState
- EHoodState
- EHorizTextAligment
- EHorizontalAlignment
- EHorseAvatarType
- EHorseBehaviorType
- EHorseReinIKType
- EHorseWingMaxSpeedAnimationType
- EHuntBowVerifyResult
- EICreateBizClientType
- EICreateErrorCode
- EICreateUserLoginType
- EIDCardDestroyReasonType
- EIOSMetalShaderStandard
- EIOSVersion
- EIconState
- EIdeaBakingLayout
- EIdeaBakingMode
- EIdeaDecalParentType
- EIdeaFenceSelector
- EImageExSourceType
- EImmediateUIStyle
- EImpactDamageOverride
- EImportGeometryType
- EImportLODType
- EImportanceLevel
- EImportanceWeight
- EImportantMovelogShowType
- EInAppPurchaseState
- EInSafetyCircleType
- EIndirectLightingCacheQuality
- EIndoorOutdoorMask
- EInertializationBoneState
- EInertializationSpace
- EInertializationState
- EInfectionCampType
- EInfectionMeleeWeaponType
- EInfectionPlayerInfectType
- EInfectionRespawnReason
- EInfectionSupplyType
- EInitMLNetOnlineTime
- EInitialOscillatorOffset
- EInnerCircleType
- EInputActionAccumulationBehavior
- EInputActionType
- EInputActionValueType
- EInputConsumeOptions
- EInputEvent
- EInputTriggerState
- EInputTypes
- EInspectedOperation
- EIntegerArithmeticOperationType
- EInteractionDataOrigin
- EInteractionDataType
- EInteractiveObjectType
- EInteractorHand
- EInterp3Method
- EInterpCurveMode
- EInterpMoveAxis
- EInterpToBehaviourType
- EInterpTrackMoveRotMode
- EInterpolationBlend
- EInvalidLocType
- EInviteResponceType
- EItemBehaviorType
- EItemCurveAnimState
- EItemDataTypeStrs
- EItemExtensionType
- EItemFlowOperation
- EItemGAActiveCondition
- EItemInBackpackVersion
- EItemNumCheckType
- EItemOperationType
- EItemOperationTypeV2
- EItemReporterTime
- EItemStopReason
- EItemStoreArea
- EJoystickIsInside
- EJoystickOperatingMode
- EJsonType
- EJukeboxOperateType
- EJukeboxStatus
- EJumpJoyType
- EJumpType
- EKawaiiAnimNodeReferenceConversionResult
- EKawaiiPhysicsSimulationSpace
- EKawaiiSimulationSpace
- EKillOrPutDownMessageType
- EKinematicBonesUpdateToPhysics
- EKiteState
- ELabelAnchorMode
- ELadderClimbState
- ELandscapeConvertMode
- ELandscapeCullingPrecision
- ELandscapeCustomizedCoordType
- ELandscapeFoliageEditorControlType
- ELandscapeGizmoType
- ELandscapeImportAlphamapType
- ELandscapeImportHeightmapError
- ELandscapeImportLayerError
- ELandscapeImportResult
- ELandscapeLODFalloff
- ELandscapeLayerBlendType
- ELandscapeLayerDisplayMode
- ELandscapeLayerPaintingRestriction
- ELandscapeMaterialBakingType
- ELandscapeMirrorOperation
- ELandscapeObjectSets
- ELandscapeSetupErrors
- ELandscapeToolErosionMode
- ELandscapeToolFlattenMode
- ELandscapeToolHydroErosionMode
- ELandscapeToolNoiseMode
- ELandscapeToolPasteMode
- ELandscapeWeightmapUsage
- ELaserTraceUIStage
- ELaunchControlCharacterState
- ELaunchControlEffectState
- ELaunchControlState
- ELaunchModeType
- ELavaType
- ELeanOutStatus
- ELeftQueueItemStatus
- ELeftQueueItemType
- ELegendPosition
- ELerpInterpolationMode
- ELevelEditor2DAxis
- ELevelLoadType
- ELevelObjectSets
- ELevelReorganizationPlatform
- ELevelViewportType
- ELevelVisibility
- ELevelVisibilityDirtyMode
- ELevelsCheckObjectSets
- ELifetimeCondition
- ELightMapPaddingType
- ELightShadowAdventureActorStatus
- ELightingBuildInfoObjectSets
- ELightingBuildQuality
- ELightmapType
- ELightspeedPolyAnimationCheckKind
- ELightspeedPolyGeometryDataFieldType
- ELightspeedPolyLODRecipeCommandletSwitches
- ELightspeedPolyMeshReductionTarget
- ELightspeedPolyMetaTagType
- ELightspeedPolyOperationPreference
- ELightspeedPolyOutputColorSpace
- ELightspeedPolyQualityMetric
- ELightspeedPolyRecipeMeshState
- ELightspeedPolyRemeshingMethod
- ELightspeedPolyVisibilityCheckKind
- ELimitType
- ELimitedItemCase
- ELinearConstraintMotion
- EListItemAlignment
- EListenEscMethod
- ELiteInstancedStructUtilsResult
- ELoadLevelAtStartup
- ELoadMode
- ELobbyAircraftHatchLevelSequenceType
- ELobbyAircraftHatchPlayingStatus
- ELobbyBgMatType
- ELobbyBigPlaneLevelSequenceType
- ELobbyBoneType
- ELobbyCarPlateType
- ELobbyCharacterAnimType
- ELobbyCharacterPosIndex
- ELobbyGameType
- ELobbyItemMontageType
- ELobbyItemSlotType
- ELobbyMultiEmoteStatus
- ELobbyNPCAnimState
- ELobbyNPCAnimType
- ELobbyPawnState
- ELobbyPawnStateChangeType
- ELobbyPreviewer_AvatarGender
- ELobbyPreviewer_TaskViewTemplate
- ELobbyUseSWPState
- ELocalizationTargetConflictStatus
- ELocalizationTargetLoadingPolicy
- ELocalizedTextCollapseMode
- ELocationBoneSocketSelectionMethod
- ELocationBoneSocketSource
- ELocationEmitterSelectionMethod
- ELocationSkelVertSurfaceSource
- ELocationStVertBrustType
- ELocationStVertSurfaceSource
- ELockPPType
- ELockTPPReason
- ELockTargetState
- ELockedVehicleState
- ELogCategory
- ELogLevel
- ELogTimes
- ELogTypeID
- ELogTypes
- ELogVerbosity
- ELogicAreaType
- ELogicEffectOp
- ELogicImageIDType
- ELoginPlatform
- ELoopMoveMode
- ELostConnectionToDSReason
- ELostTombEquipSlotType
- ELostTombPlayerRole
- ELostTombPlayerSettleReason
- ELostTombWeaponSlotType
- ELowMemoryGCLevel
- ELuaExtendPushPropertyType
- ELuaNetworkRemoteContentType
- ELuaOrder
- ELuaTriggerType
- EMCPErrorCode
- EMLAISpecialZoneType
- EMPMatchOutcome
- EMVVMBindingMode
- EMVVMBindingSource
- EMVVMExecutionMode
- EMVVMFieldSelectorType
- EMVVMLoadBindingState
- EMYRIAPODFRR_TYPE
- EMacMetalShaderStandard
- EMachanicalAxisType
- EMachanicalRotType
- EMachineDogState
- EMagicFieldEventType
- EMagicFieldSpawnType
- EMagicMoveVehicleState
- EMainCharMontagePlayType
- EManifestFileHeader
- EManualVehicleSyncType
- EMapErrorCode
- EMapExOpenState
- EMapExUIType
- EMapRotateMode
- EMapSetBrushFlags
- EMapStatus
- EMapType
- EMapUpdateType
- EMapWidgetType
- EMarkDispatchActionType
- EMarkDispatchRange
- EMarkEditType
- EMarkFilterType
- EMarkGetAllType
- EMarkObjType
- EMarkParentWidget
- EMarkState
- EMarkStatus
- EMarkSyncDataType
- EMarkType
- EMaskTextureSize
- EMatSlotCutType
- EMatchLogic
- EMatchRuleLogic
- EMaterialAttributeBlend
- EMaterialBakeMethod
- EMaterialCookFeatureLevel
- EMaterialCookQualityLevel
- EMaterialDecalResponse
- EMaterialDomain
- EMaterialExposedTextureProperty
- EMaterialExposedViewProperty
- EMaterialExpressionScreenPositionMapping
- EMaterialHasParamType
- EMaterialLODType
- EMaterialMergeType
- EMaterialPositionTransformSource
- EMaterialProperty
- EMaterialProxySmaplingQuality
- EMaterialSamplerType
- EMaterialSceneAttributeInputMode
- EMaterialSearchLocation
- EMaterialShadingModel
- EMaterialShadingRate
- EMaterialShadowOverride
- EMaterialTessellationMode
- EMaterialUsage
- EMaterialVectorCoordTransform
- EMaterialVectorCoordTransformSource
- EMaterialsCheckObjectSets
- EMaxConcurrentResolutionRule
- EMaxFlyHeightType
- EMeasuringToolUnits
- EMechanicalArmType
- EMediaAudioCaptureDeviceFilter
- EMediaPlayerEditorScale
- EMediaPlayerTrack
- EMediaSoundChannels
- EMediaVideoCaptureDeviceFilter
- EMediaWebcamCaptureDeviceFilter
- EMediaplayStatus
- EMediaplayType
- EMeleeAttackAbsorbStopReason
- EMeleeAttackBoxType
- EMeleeAttackComboJumpType
- EMeleeAttackDamageCustomEvent
- EMeleeAttackMontagePointType
- EMeleeAttackType
- EMeleeDamageSubType
- EMeleeTraceInterpolationType
- EMenuPlacement
- EMenuType
- EMeshBufferAccess
- EMeshCameraFacingOptions
- EMeshCameraFacingUpAxis
- EMeshComponentUpdateFlag
- EMeshDeviceAdaptationType
- EMeshFeatureImportance
- EMeshInstancingReplacementMethod
- EMeshLODBiasTypeExt
- EMeshLODSelectionType
- EMeshMergeType
- EMeshPaintColorViewMode
- EMeshPaintMode
- EMeshPerLODBiasType
- EMeshScreenAlignment
- EMeshShiftCompensationType
- EMeshTexelCheckType
- EMeshType
- EMeshVertexPaintTarget
- EMessageAuthorityType
- EMessageContainerMatchType
- EMessageTagMatchType
- EMessageTagSelectionType
- EMessageTagSourceType
- EMicroTransactionDelegate
- EMicroTransactionResult
- EMikuRhythmGameActionType
- EMikuRhythmGameType
- EMiniMarkRange
- EMinimumSupportedOS
- EMixerEffectSlotType
- EMobNetRelevantType
- EMobStateType
- EMobWalkType
- EMobaFindStrategy
- EMobaHeroAISkillType
- EMobaHeroSubAreaType
- EMobaSpecificActorType
- EMobileCSMQuality
- EMobileMSAASampleCount
- EModeAvatarFeatureType
- EModeType
- EModelsCheckObjectSets
- EModifyBlackboardDataNewValueType
- EModifyBlackboardDataValueType
- EModifyCurveApplyMode
- EModifyHideCrossHairState
- EModuleCheckClassType
- EModuleType
- EMonsterBornType
- EMonsterClimbPhase
- EMonsterDurationType
- EMonsterJumpExPhase
- EMonsterPeekPose
- EMonsterPoseType
- EMonsterState
- EMonsterThrowItemType
- EMonsterTreasureBoxState
- EMonsterWeaponAttachmentSocketType
- EMonsterWeaponPose
- EMonsterWeaponType
- EMontageNotifyTickType
- EMontagePlayReturnType
- EMontagePreviewType
- EMontageSubStepResult
- EMouseCaptureMode
- EMouseCursor
- EMouseLockMode
- EMoveAntiCheatPauseFlag
- EMoveBaseSpeedType
- EMoveComponentAction
- EMoveCurveType
- EMoveDebugDrawFlag
- EMoveDirType
- EMoveFRROnRepMask
- EMoveFRRPropMask
- EMoveFRRSerializeMask
- EMoveHeadShowFlag
- EMoveInputRateLimitPriority
- EMoveState
- EMoveToEndAction
- EMovementDirection
- EMovementMode
- EMoviePlaybackType
- EMovieSceneBlendType
- EMovieSceneBuiltInEasing
- EMovieSceneCompletionMode
- EMovieSceneEventFirePCType
- EMovieSceneKeyInterpolation
- EMovieSceneObjectBindingSpace
- EMovieScenePESkillTaskLifeMode
- EMovieScenePlayerStatus
- EMsgType
- EMultiFunctionalShootModeType
- EMultipleKeyBindingIndex
- EMusicGameType
- EMusicGirlSearchRange
- EMuzzleLocType
- EMuzzleRotType
- EMyLandscapePlatfromConfiguration
- EMyriapodFRRSerializeFlag
- EMysteriousEscapePointState
- EmitterType
- eMEAnimationState
- eMEAttributeOperation
- eMEDamageType
- eMoveDrivenMode
- ENPCShowIdleType
- ENameMatchMode
- ENameType
- ENativeEventSwitch
- ENavCostDisplay
- ENavDataGatheringMode
- ENavDataGatheringModeConfig
- ENavLinkDirection
- ENavLinkExtendedFlag
- ENavLinkMoveDirection
- ENavLinkType
- ENavPathEvent
- ENavigationGenesis
- ENavigationOptionFlag
- ENavigationQueryResult
- ENavigationSource
- ENavigatorItemEdgeState
- ENetDormancy
- ENetEmoteType
- ENetRelevantType
- ENetRelevantZCompareMode
- ENetRole
- ENetRoleAndQualityCondition
- ENetSequenceType
- ENetworkFailure
- ENetworkLagState
- ENetworkSmoothingMode
- ENeverCookType
- ENewCookTickFlags
- ENewFPPMovePoseType
- ENewWorldTaskNodeControlType
- ENewYearActivityEventType
- ENewbieGuidePlayerCategory
- ENewbieGuideType
- ENewbieGuideUIType
- ENightVisionDisableType
- ENightVisionType
- ENodeAdvancedPins
- ENodeChangeState
- ENodeDataValueType
- ENodeEnabledState
- ENodeTitleType
- ENodeTypes
- ENoiseFunction
- ENormalMode
- ENoticeType
- ENotifyFilterType
- ENotifyTriggerMode
- EndTangentLengthType
- EnmSprintOptType
- EnumParticleParameterType
- EOBPlayerType
- EOBReportReason
- EOBReportReason_BP
- EOBUIUsingForType
- EODPakCheckResult
- EOHCompareType
- EOHGradeScoreType
- EOHSourceType
- EOITBlendMode
- EOPPathType
- EOPType
- EOasisGenDisplayMessageType
- EObjectImageApplyType
- EObjectImageType
- EObjectPropertyType
- EObjectTypeQuery
- EObserveFlowState
- EObserverOutlineType
- EObserverType
- EOcclusionCombineMode
- EOccupationChipSocketType
- EOceanTestPointState
- EOffsetDisCriticalVerifySubKey
- EOffsetDisVerifyRet
- EOnHitBackEndReason
- EOpacitySourceMode
- EOpenHarmonyScreenOrientation
- EOpenOrCloseHoodResult
- EOpenParachuteParticleType
- EOpenRateCheckType
- EOperationRunResult
- EOperatorType
- EOptimizationMetric
- EOptimizationType
- EOrbitChainMode
- EOrientPositionSelector
- EOrientation
- EOrientationByX
- EOrthoThumbnailDirection
- EOverlapCheckSide
- EOverlapFilterOption
- EOverlapObjectCheckType
- EOverlapObjectType
- EOverlookState
- EOverrideConditionCheck
- EOverrideMeshTarget
- EOverridePawnStateCheck
- EOverrideQueryMobilityType
- EOverrideWay
- EOwnerType
- eOperationTargetType
- EPBRecordCond
- EPCGActorFilter
- EPCGActorSelection
- EPCGAttachOptions
- EPCGAttributeAccessorFlags
- EPCGAttributeFilterOperation
- EPCGAttributeFilterOperator
- EPCGAttributeNoiseMode
- EPCGAttributePropertySelection
- EPCGAttributeReduceOperation
- EPCGAttributeSelectAxis
- EPCGAttributeSelectOperation
- EPCGBoundsModifierMode
- EPCGChangeType
- EPCGComponentDirtyFlag
- EPCGComponentGenerationTrigger
- EPCGComponentInput
- EPCGControlFlowSelectionMode
- EPCGCoordinateSpace
- EPCGCopyAttributesOperation
- EPCGCopyPointsInheritanceMode
- EPCGCopyPointsMetadataInheritanceMode
- EPCGCopyPointsTagInheritanceMode
- EPCGCreateSplineMode
- EPCGDataType
- EPCGDebugVisScaleMethod
- EPCGDifferenceDensityFunction
- EPCGDifferenceMode
- EPCGEditorDirtyMode
- EPCGEditorNewPCGGraphBehavior
- EPCGEditorNewSettingsBehavior
- EPCGElementType
- EPCGExclusiveDataType
- EPCGExecutionPhase
- EPCGExtraProperties
- EPCGFilterByTagOperation
- EPCGGetDataFromActorMode
- EPCGGridPivot
- EPCGHiGenGrid
- EPCGIntersectionDensityFunction
- EPCGLandscapeCacheSerializationContents
- EPCGLandscapeCacheSerializationMode
- EPCGLocalGridPivot
- EPCGMatchMaxDistanceMode
- EPCGMeshSelectorMaterialOverrideMode
- EPCGMetadataBitwiseOperation
- EPCGMetadataBooleanOperation
- EPCGMetadataCompareOperation
- EPCGMetadataFilterMode
- EPCGMetadataMakeRotatorOp
- EPCGMetadataMakeVector3
- EPCGMetadataMakeVector4
- EPCGMetadataMathsOperation
- EPCGMetadataOp
- EPCGMetadataRotatorOperation
- EPCGMetadataSettingsBaseMode
- EPCGMetadataSettingsBaseTypes
- EPCGMetadataStringOperation
- EPCGMetadataTransformOperation
- EPCGMetadataTrigOperation
- EPCGMetadataTypes
- EPCGMetadataTypesConstantStructStringMode
- EPCGMetadataVectorOperation
- EPCGNodeTitleType
- EPCGPinStatus
- EPCGPinUsage
- EPCGPointExtentsModifierMode
- EPCGPointNeighborhoodDensityMode
- EPCGPointPosition
- EPCGPointProperties
- EPCGPrintVerbosity
- EPCGProjectionColorBlendMode
- EPCGProjectionTagMergeMode
- EPCGProxyInterfaceMode
- EPCGReverseSplineOperation
- EPCGSelfPruningType
- EPCGSettingsExecutionMode
- EPCGSettingsType
- EPCGSortMethod
- EPCGSpawnActorGenerationTrigger
- EPCGSpawnActorOption
- EPCGSplineMeshForwardAxis
- EPCGSplineSamplingDimension
- EPCGSplineSamplingFill
- EPCGSplineSamplingInteriorOrientation
- EPCGSplineSamplingMode
- EPCGSplineSamplingSeedingMode
- EPCGSplitAxis
- EPCGTagFilterOperation
- EPCGTextureAddressMode
- EPCGTextureColorChannel
- EPCGTextureDensityFunction
- EPCGTextureFilter
- EPCGTextureMappingMethod
- EPCGTransformLerpMode
- EPCGTypeConversion
- EPCGUnionDensityFunction
- EPCGUnionType
- EPCGWorldQueryFilterByTag
- EPCInteractionMode
- EPDPoseDriverOutput
- EPDPoseDriverSource
- EPDPoseDriverType
- EPDRBFDistanceMethod
- EPDRBFFunctionType
- EPDRBFNormalizeMethod
- EPDRBFSolverType
- EPEActorAttachEndType
- EPEAddonCustomParamType
- EPEAttachScaleRule
- EPEBackpackMonitorType
- EPEBackpackOperationType
- EPEBuffAttrModifyType
- EPEBuffDurationType
- EPEBuffEffectNetworkMode
- EPEBuffEffectStackType
- EPEBuffEffectStopType
- EPEBuffEffectTriggerConditionOptType
- EPEBuffEffectTriggerConditionType
- EPEBuffMergeConditionType
- EPEBuffMergeType
- EPEBuffOcclusionHighlightType
- EPEBuffRemoveType
- EPEBuffTriggerType
- EPEBuffTriggerTypeDisplay
- EPEConditionCheckDirectionType
- EPEConditionCompareType
- EPEConditionResultType
- EPEGetterType
- EPEMagnitudeWrapperAttrSourceType
- EPEMeleeAttackRefAnimDataType
- EPEMeleeAttackTrackType
- EPEPassiveSkillDisplayType
- EPEPassiveSkillMergeType
- EPEPassiveSkillTagsMatchType
- EPEPersonPerspectiveType
- EPESkillActivatableReason
- EPESkillAnimSlotType
- EPESkillAttachType
- EPESkillCDChargeType
- EPESkillCDType
- EPESkillCameraShakeTargetType
- EPESkillCameraShakeType
- EPESkillCancelTaskAction
- EPESkillChargeState
- EPESkillConsumeTimeType
- EPESkillDeActivateReason
- EPESkillEventConditionMatchType
- EPESkillEventInputType
- EPESkillEventLongPressType
- EPESkillEventMonitorType
- EPESkillEventTimeIntervalType
- EPESkillGMPEventType
- EPESkillImpulseDir
- EPESkillIndicatorType
- EPESkillIndicatorVisiable
- EPESkillInputStateType
- EPESkillInputType
- EPESkillLaunchProjectileDir
- EPESkillMergeBehaviorType
- EPESkillPointPickerType
- EPESkillScreenParticleTargetType
- EPESkillSelectTarget
- EPESkillSpawnTargetType
- EPESkillSprintDir
- EPESkillSprintSpeedType
- EPESkillTargetConditionType
- EPESkillTargetsSortType
- EPESkillTaskBackpackOperateType
- EPESkillTaskDeactivateReason
- EPESkillTeamConditionType
- EPESkillTipType
- EPESkillTracetType
- EPESkillTransformConditionType
- EPESkillTransformSourceType
- EPESkillUISlotMapping
- EPESkillValueCalculatorType
- EPETransitionType
- EPIEPreviewDeviceType
- EPKRoomPlayerState
- EPKRoomState
- EPSkillEventAttributeConditionType
- EPSkillEventSkillStateEvent
- EPSkillEventStateType
- EPSkillEventWeaponHitCounterType
- EPSkillEventWeaponHitPartType
- EPSoundPlayType
- EPVEProjectileType
- EPVETeleportType
- EPVSMode
- EPackageNotifyState
- EPaintDecalTargetValidationType
- EPaintMode
- EPaintTypes
- EPaintableClothProperty
- EPakResState
- EPakResourceType
- EPakSplitState
- EPandoraEnv
- EPaperSpriteAtlasPadding
- EParachuteFollowStateForPet
- EParachuteInvitationType
- EParachuteMultiAnimSeatType
- EParachuteQuadAnimSeatType
- EParachuteState
- EParachutingCWMsgType
- EParagliderCharacterType
- EParamCompareType
- EParamType
- EParrotAttachReason
- EParrotBornReason
- EParrotDeathReason
- EParrotEffectType
- EParrotEmoteType
- EParrotEventType
- EParrotMoveToTargetState
- EParrotSkillType
- EParticleAxisLock
- EParticleBurstMethod
- EParticleCameraOffsetUpdateMethod
- EParticleCollisionComplete
- EParticleCollisionMode
- EParticleCollisionResponse
- EParticleConsistencyCheckMode
- EParticleCoutingMethod
- EParticleDirection
- EParticleDrawEffect
- EParticleEventType
- EParticleKey
- EParticleLODDistanceCheckMode
- EParticleLimitType
- EParticleModuleDuplicatedType
- EParticleRotateType
- EParticleScreenAlignment
- EParticleSignificanceLevel
- EParticleSortMode
- EParticleSourceSelectionMethod
- EParticleSubUVInterpMethod
- EParticleSysParamType
- EParticleSystemInsignificanceReaction
- EParticleSystemOcclusionBoundsMethod
- EParticleSystemUpdateMode
- EParticleTemplateBindingType
- EParticleUVFlipMode
- EPartyReservationResult
- EPasteTo
- EPatchToolCmdType
- EPatchToolPlatform
- EPathExistanceQueryType
- EPathFollowingAction
- EPathFollowingRequestResult
- EPathFollowingResult
- EPathFollowingStatus
- EPathInterpType
- EPathMatchMode
- EPathMatchPattern
- EPathMoveDir
- EPathMoveFindPathMode
- EPathMoveLoopMode
- EPathMoveState
- EPatrolCarBackDoorState
- EPatrolCarEventState
- EPawnActionAbortState
- EPawnActionEventType
- EPawnActionFailHandling
- EPawnActionMoveMode
- EPawnActionResult
- EPawnDetailInfoShowFlag
- EPawnDetailInfoShowType
- EPawnPoseSwitchType
- EPawnState
- EPawnStateForbiddenRelationReason
- EPawnStateSettingValueType
- EPawnSubActionTriggeringPolicy
- EPayloadOperation
- EPcConsolePreset
- EPeaceMemoryActorState
- EPeaceMemorySubType
- EPeekMark
- EPerfAlertLevel
- EPerfCollectionState
- EPerfDataDownloadStatus
- EPerfHeatmapDisplayMode
- EPerfReadyCondition
- EPerfSampleDirection
- EPerfSamplingEditType
- EPerfSamplingGenerationMethod
- EPerfSamplingTraceMethod
- EPerfStandardDataProviderType
- EPerfStandardOperator
- EPerfTaskState
- EPerfValueType
- EPerforceFileStatus
- EPerformJudgement
- EPerformLinkType
- EPerformanceLabDevicePlatform
- EPersistEffectClientEvent
- EPersistEffectUnApplyReason
- EPersistPlayMode
- EPersistRollState
- EPersonPriority
- EPersonalOperateType
- EPerspectiveMode
- EPerspectiveTypes
- EPhotonDestructibleSurfaceHitType
- EPhotonDestructibleVolumeType
- EPhysAssetFitGeomType
- EPhysAssetFitVertWeight
- EPhysBodyOp
- EPhysicalSurface
- EPhysicalSurfaceDescription
- EPhysicsAssetEditorConstraintViewMode
- EPhysicsAssetEditorRenderMode
- EPhysicsSceneType
- EPhysicsTransformUpdateMode
- EPhysicsType
- EPickUpBoxType
- EPickUpGenerationReason
- EPickUpItemFlowSourceType
- EPickerFromBlackboard_DataType
- EPickerMode
- EPickerPreviewType
- EPickupWrapperProtectType
- EPinContainerType
- EPinHidingMode
- EPixelFormat
- EPlaceBlueprintErrorCode
- EPlanarConstraint
- EPlanarConstraint_UE5
- EPlaneConstraintAxisSetting
- EPlaneDir
- EPlaneStateType
- EPlaneType
- EPlaneTypeForTlog
- EPlatformBoardActorType
- EPlatformInterfaceDataType
- EPlayCurveVehicleType
- EPlayDataReporterSwitchType
- EPlayModeLocations
- EPlayModeType
- EPlayNetMode
- EPlayOnBuildMode
- EPlayOnLaunchConfiguration
- EPlayShovelSoundType
- EPlaybackState
- EPlaybackType
- EPlayerAcceptHostResult
- EPlayerBodyPartType
- EPlayerBoundingBoxType
- EPlayerCameraMode
- EPlayerControllerMsgType
- EPlayerEnegyStage
- EPlayerEquipmentLevel
- EPlayerEquipmentSlotType
- EPlayerHeadType
- EPlayerHostingState
- EPlayerHurtAnimType
- EPlayerLadderState
- EPlayerMoveState
- EPlayerOBTransformState
- EPlayerOperation
- EPlayerPartyDanceState
- EPlayerPerspectiveType
- EPlayerRangeType
- EPlayerRequireHostResult
- EPlayerRestartReason
- EPlayerStateMsgType
- EPlayerSwitchDSPriority
- EPlayerSwitchDSState
- EPlotDialogueEndReason
- EPlotDialoguePerformType
- EPlotState
- EPointOnCircleSpacingMethod
- EPopKartMarkState
- EPopKartSeatState
- EPosUIShowType
- EPoseDriverOutput
- EPoseDriverSource
- EPoseDriverType
- EPoseStateType
- EPositionType
- EPossessClearState
- EPossessMode
- EPossessRejectEvent
- EPostCopyOperation
- EPostEffectBlendType
- EPostOperationType
- EPowerUsageFrameRateLock
- EPressType
- EPrewarmOperationReason
- EPrimaryAssetCookRule
- EPrimaryAssetPriorityRule
- EPrimitiveObjectSets
- EPriorityChooseTargetType
- EProcMeshSliceCapOption
- EProductType
- EProgressBarFillType
- EProjectPackagingBlueprintNativizationMethod
- EProjectPackagingBuild
- EProjectPackagingBuildConfigurations
- EProjectPackagingInternationalizationPresets
- EProjectileActionType
- EProjectileDeAttachType
- EProjectileEffectApplyCondition
- EProjectileEventType
- EProjectileMatchType
- EProjectileModifierType
- EProjectileMoveType
- EProjectilePassThroughType
- EProjectileShootIntervalVerifyFailedType
- EProjectileSplitDirectionType
- EProjectileSplitType
- EPropReplacePlatform
- EPropTypeForLua
- EPropertyBagContainerType
- EPropertyBagMissingEnum
- EPropertyBagPropertyType
- EPropertyBagResult
- EPropertyClass
- EPropertyCompareType
- EPropertyContainRule
- EPropertyDataType
- EPropertyLogicOperator
- EPropertyMatchRule
- EPropertyModifyRevertType
- EPropertyOwner
- EPropertySerializeType
- EPropertyTargetOwner
- EPropertyUpdateGroup
- EPropertyVisbility
- EProtocolTimeoutHandlingMethod
- EProxyLODCollisionType
- EProxyNormalComputationMethod
- EProxyTaskDataMark
- EPullSpeedType
- EPullTargetLocationType
- EPurchaseValidationResult
- EPushingCharacterShapeFlag
- EPxDebugInfo
- EPxDynamicTextureUpdateMode
- EPxFontFaceType
- EPxKeyEventType
- EPxKeyboardTypes
- EPxLogGroups
- EPxLogLevels
- EPxMouseType
- EPxTouchType
- EPxWidgetBatchType
- EPxWidgetTransformType
- EPyTestEnum
- EPythonProjectItemType
- EQSNode_ScoreEquationType
- EQSNode_TestFilterType
- EQSNode_TestPurposeType
- EQualityRenderBits
- EQuatumBallState
- EQueryType
- EQuickSignInputType
- EQuickSignType
- EQuitInteractionReason
- EQuitPreference
- ERBFDistanceMethod
- ERBFFunctionType
- ERCRBoxType
- ERCRCharacterState
- ERCRCheckGapType
- ERCRCheckTipsType
- ERCRCheckType
- ERCROcclusionType
- ERCRReportType
- EREOperationType
- ERETaskPlantType
- ERETaskType
- ERMAFoliageToolsFoliageSelectionMode
- ERSHCollisionMergeType
- ERTEActorBindRelationType
- ERTEActorNotDoFlag
- ERTEActorSelectMaterialType
- ERTEActorStateType
- ERTEBindActorResultType
- ERTECopyActorCheckResult
- ERTECopyActorResult
- ERTECopyMoveType
- ERTEFingerMotionType
- ERTEListener
- ERTEMViewTargetMoveType
- ERTERangeSelect
- ERTPCValueType
- ERadialImpulseFalloff
- ERailGunMatParamChangingType
- ERainbowSwingBuildType
- ERainbowSwingMeshHiddenType
- ERainbowSwingStateType
- ERandomLocType
- ERandomModifierValueType
- ERandomRocketExplosionType
- ERangeBoundTypes
- ERangeShape
- ERankListDisplayType
- ERankListEnableType
- ERankListPeriodType
- ERankListScoreFormatType
- ERankListSortType
- ERawCurveTrackTypes
- ERayTracingGroupCullingPriority
- EReadSpeciesData
- ERebuildMapFlags
- ERecastPartitioning
- ERecastWithoutLayerCachePartitioning
- ERecordAntiStrategyType
- ERecordType
- ERecoverOBType
- ERecoveryReasonType
- ERecoveryType
- ERefPoseType
- ERefereeClientState
- EReferenceRuleMode
- EReferenceType
- EReferenceWhitelistType
- EReflectionFilterBits
- EReflectionPlatform
- EReflectionSourceType
- ERefractionMode
- ERegionSizeIndex
- ERegionStatsObjectSets
- ERegionTriggerType
- ERegionType
- ERegionlMapActorPlusUIMountType
- ERegionlMapActorPlusUIShowType
- ERegistPossessValueType
- EReimportFolder
- EReimportSequenceType
- EReimportTaskType
- ERelationshipWithTarget
- ERelativeTransformSpace
- EReleaseToFireType
- ERenderAspectRatio
- ERenderDynamicStyle
- ERenderFocusRule
- ERenderQuality
- ERenderQualityEngine
- ERenderQualityEngine_PC
- ERenderStyle
- ERendererStencilMask
- EReplaceLevelCycleType
- EReplaceSlot
- EReplayCollectType
- EReplayEndReason
- EReplayError
- EReplayStatus
- EReplayUIGroupType
- EReplayWidgetLogoMode
- EReportEquipmentSlotType
- EReportPolicy
- EReportPolicyName
- EReporterLineStyle
- EReqType
- ERescueHelicopterState
- EResourceErrorCode
- EResourceStatus
- EResourceType
- EResourceUpdateType
- ERespawnPointType
- ERestrictedDamageType
- ERetargetAvatarAdaptSpace
- EReuseFallOverscrollState
- EReuseListDiffNotFullAlignStyle
- EReuseListDiffStyle
- EReuseListGridAlign
- EReuseListJumpStyle
- EReuseListNotFullAlignStyle
- EReuseListOverscrollState
- EReuseListSortZOrder
- EReuseListSpNotFullAlignStyle
- EReuseListSpOverscrollState
- EReuseListSpStyle
- EReuseListStyle
- EReuseListTrainGridAlign
- EReuseListTrainJumpStyle
- EReuseListTrainNotFullAlignStyle
- EReuseListTrainOverscrollState
- EReuseListTrainSortZOrder
- EReuseListTrainStyle
- EReuseMapContentType
- EReuseMapOverDragType
- EReverbSendMethod
- ERevivalAirlineType
- ERevivalCardTipsType
- ERevivalCheckerStatisticType
- ERevivalFailedReasonType
- ERevivalPointState
- ERiceGlueBallAreaState
- ERichCurveExtrapolation
- ERichCurveInterpMode
- ERichCurveInterpModeForKeyGroup
- ERichCurveTangentMode
- ERichCurveTangentWeightMode
- ERightJoystickDirectionType
- ERightJoystickInputState
- ERoleAndQualityCondition
- ERoleAndQualityLobbyCondition
- ERoleFrontAxis
- ERollState
- ERoomRangeType
- ERootMotionAccumulateMode
- ERootMotionFinishVelocityMode
- ERootMotionMode
- ERootMotionRootLock
- ERootMotionSourceSettingsFlags
- ERootMotionSourceStatusFlags
- ERotationGridMode
- ERotatorQuantization
- ERoundingMode
- ERouteSegmentMode
- ERulePriority
- ERuleSetType
- ERuntimeGenerationType
- ERuntimeMeshCollisionCookingMode
- ERuntimePlatform
- ERuntimeSettingFeatureLevel
- ERuntimeTexturesObjectSets
- ESGLuaTestEnum
- ESGLuaTestEnumUInt32
- ESGLuaTestEnumUInt8
- ESGLuaUnitTestEnum
- ESGLuaUnitTestFuncCallType
- ESGLuaUnitTestFuncImplType
- ESGLuaUnitTestFuncType
- ESLPCrossHair_WithValidation_Result
- ESLP_CrossHair_TraceType
- ESLanternRacingPerf
- ESOperateVehicle
- ESPCRJointSimSpaceType
- ESRAudioEngine
- ESRDirectOcclusionMethod
- ESRMaterial
- ESRRayTracerType
- ESRePairVehicle
- ESTEAnimalDealMethod
- ESTECharacterType
- ESTEDealMethod
- ESTEPoseState
- ESTEScopeState
- ESTEScopeType
- ESTEWeaponHoldType
- ESTEWeaponShootType
- ESTExtraBuffAction_PostAKEvent_AttachTo
- ESTExtraCharToVehiclePer
- ESTExtraDoorMachineCameraMode
- ESTExtraDoorMachineState
- ESTExtraDumpBoxState
- ESTExtraGlideCarGlideState
- ESTExtraHammerSharkInWaterState
- ESTExtraHammerSharkRepairCheckResult
- ESTExtraHammerSharkRepairState
- ESTExtraLockedVehicleStatus
- ESTExtraPenguinVehicleState
- ESTExtraTankControlMode
- ESTExtraTankMovementMode
- ESTExtraUAVVehicleOperateState
- ESTExtraUAVVehicleState
- ESTExtraVehicleAnimalType
- ESTExtraVehicleBaseType
- ESTExtraVehicleCruiseControlState
- ESTExtraVehicleDampingState
- ESTExtraVehicleEnjoyVoiceType
- ESTExtraVehicleHealthState
- ESTExtraVehicleSeatType
- ESTExtraVehicleShootWeaponHoldType
- ESTExtraVehicleShootWeaponTypeAtDriverSeat
- ESTExtraVehicleStates
- ESTExtraVehicleSyncState
- ESTExtraVehicleType
- ESTExtraVehicleUserState
- ESTExtraVehicleWheelIconType
- ESTExtraVehicleWindowState
- ESTExtraWheeledMovementType
- ESTExtraZiplineDirection
- ESTPopkartAreaTriggerType
- ESTQuadrupedCharacterPickableActorType
- ESTQuadrupedCharacterQueryItemType
- ESTQuadrupedCharacterScenePerceptionItemType
- ESTQuadrupedCharacterScenePerceptionMode
- ESTQuadrupedCharacterVehicleInteractStage
- ESTQuadrupedCharacterVehicleInteractState
- ESTRemoteControlPawnType
- ESTRemoteControlState
- ESTSpawnerVolume
- ESTVehicleSupply
- ESTVehicleWeaponControlMode
- ESVehAnimVehicleType
- ESWingManMovementMode
- ESaStateErrorType
- ESamplerSourceMode
- ESaveOnCompile
- ESavePropertyType
- EScaleChainInitialLength
- EScaleMode
- EScanMaterialQualityLevel
- EScanPropOperationType
- EScanRulesType
- EScanSamplerPlatform
- EScanTextureType
- EScannerBlueprintMemberType
- EScannerBoxCompareMode
- EScannerBranchType
- EScannerChannelSelectorType
- EScannerCheckStatus
- EScannerCollisionCheckType
- EScannerCollisionPreset
- EScannerCompareMode
- EScannerCookerSettingType
- EScannerDataRowType
- EScannerDataTableRowMode
- EScannerEditorNoticeMode
- EScannerEmitterCheckMode
- EScannerEmitterSelecterType
- EScannerGeneralOutType
- EScannerLODSelectorType
- EScannerLogType
- EScannerMatParamCheckMode
- EScannerMatParamType
- EScannerMatPropertyTag
- EScannerMeshLODSelecterType
- EScannerMeshSectionSelecterType
- EScannerMeshType
- EScannerModuleSelect
- EScannerModuleSelecterType
- EScannerParticleLODType
- EScannerPermissionGroupType
- EScannerProcMode
- EScannerRecordLevel
- EScannerResultOutType
- EScannerRuleCategory
- EScannerScreenSizeMode
- EScannerSectionSelectorType
- EScannerSerializeType
- EScannerSlotMaterialCheckType
- EScannerTimeUnit
- EScannerTriggerBy
- EScannerTriggerMode
- ESceneCaptureCompositeMode
- ESceneCapturePrimitiveRenderMode
- ESceneCaptureSource
- ESceneDepthPriorityGroup
- ESceneRenderActorType
- ESceneSubPayload
- ESceneTextureId
- EScopeMeshAnimType
- EScoreStatus
- EScratchDecalStartRegionType
- EScreenAppearanceTargetType
- EScreenDir
- EScreenOrientation
- EScreenParamType
- EScreenParticleEffectType
- EScreenParticleType
- EScriptingCollisionShapeType
- EScrollDirection
- EScrollGestureDirection
- ESearchCase
- ESearchDir
- ESearchPriority
- ESearchResultVisibleType
- ESearchUnitState
- ESeasonTaskUIPage
- ESecMarkType
- ESectionEvaluationFlags
- ESeekAndLockStage
- ESeekFlyPointCenterLocType
- ESeekFlyPointHorizontalAngleType
- ESegmentedSplineFindResult
- ESelectBuildingParts
- ESelectInfo
- ESelectStrategy
- ESelectionMode
- ESelectorConditionLobbyRole
- ESelectorConditionNetRole
- ESelectorConditionRole
- ESelfContextInfo
- ESensibilityCheckType
- ESequenceBindingType
- ESequenceEvalReinit
- ESequenceEvalTimeType
- ESequencerLoopMode
- ESequencerSectionResizeMode
- ESequencerSpawnPosition
- ESequencerTimeSnapInterval
- ESequencerZoomPosition
- EServer
- EServerErrorCode
- EServerTaskType
- EServerType
- ESetSkinWeightReason
- ESettingsDOF
- ESettingsLockedAxis
- ESettlementType
- EShaderPerfMetricType
- EShaderTypeCategory
- EShadowCacheInvalidationBehavior
- EShadowMapFlags
- ESheetAxis
- EShelterType
- EShootBodyType
- EShootDanceCurveType
- EShootIntervalVerifyFailedType
- EShootTimeDataTransType
- EShootVertifyRes
- EShootWeaponFX
- EShootWeaponShootMode
- EShootWeaponSound
- EShootWeaponState
- EShootWeaponType
- EShootingRoomStatus
- EShovelEnabledFlags
- EShow3DTrajectory
- EShowBindConfigData_BindingType
- EShowHPBarDamageType
- EShowMoveLogFlag
- EShowPCSkillPromptType
- EShrineActorType
- EShrineEvent
- EShrineState
- ESightScopeFunctionState
- ESightScopeSensibilityChangeType
- ESightType
- ESimpleFindEnemyType
- ESimplePawnState
- ESimpleSequenceStatus
- ESimpleTreasureChestStatus
- ESimpleVertexNormalSituation
- ESimplygonCasterType
- ESimplygonColorChannels
- ESimplygonDataCreationPreferce
- ESimplygonLODType
- ESimplygonMaterialChannel
- ESimplygonProcessingMode
- ESimplygonTextureResolution
- ESimplygonTextureSamplingQuality
- ESimplygonTextureStrech
- ESimulateAddBuffRole
- ESimulatePhysicsType
- ESimulationOverlap
- ESimulationQuery
- ESimulationSpace
- ESimulationSpace_UE5
- ESimulatorMovementConfigType
- ESkeletalMeshLODType
- ESkillActionFireType
- ESkillActionFlags
- ESkillActionParticleParamType
- ESkillActionsListType
- ESkillAddForceDirection
- ESkillAttrOperator
- ESkillCastType
- ESkillConditionCheckType
- ESkillConditionType
- ESkillDebugEventType
- ESkillEditorSperatorMode
- ESkillEndConditionType
- ESkillEventAllowdActiveType
- ESkillEventAttribueOperatingType
- ESkillEventDamageEventSelectType
- ESkillEventDamageListenTimer
- ESkillEventDamageOptimizeMethod
- ESkillEventPassiveType
- ESkillEventRecoverListenTimer
- ESkillEventTargetCampType
- ESkillEventTargetType
- ESkillEventWeaponOperatingType
- ESkillEventWeaponScopeType
- ESkillFlowNodeState
- ESkillFlowState
- ESkillGraphNodeType
- ESkillIconStatus
- ESkillNodeActionType
- ESkillValidCanCastType
- ESkillValidationType
- ESkipBulletNumVerifyMaskType
- ESkirtPoseType
- ESkyLightSourceType
- ESkyboxControlDeviceType
- ESlateBrushDrawType
- ESlateBrushImageType
- ESlateBrushMirrorType
- ESlateBrushTileType
- ESlateCheckBoxType
- ESlateColorStylingMode
- ESlateEventType
- ESlateGesture
- ESlateSizeRule
- ESlateVisibility
- ESledMarkState
- ESleepFamily
- ESlotClickType
- ESlotDisableShowType
- ESlotInstallResult
- ESlotVisibilityCondition
- ESlotVisibleMode
- ESmartNameContainerType
- ESmartPhotographerMode
- ESmartPhotographerModifierDevice
- ESnapedBuildingType
- ESnapedHiddenType
- ESnapshotSourceMode
- ESnowBoardAirStunt
- ESnowBoardState
- ESnowballLaunchState
- ESocketAnimCurveRefAnimType
- ESocketAnimCurveTransformType
- ESortStrategy
- ESortitionState
- ESoundDistanceCalc
- ESoundGroup
- ESoundSpatializationAlgorithm
- ESoundType
- ESourceBusChannels
- ESourceType
- ESpaceType
- ESpawnActorCollisionHandlingMethod
- ESpawnItemFunction
- ESpawnOwnership
- ESpawnProjectileType
- ESpawnSpotType
- ESpawnType
- ESpecialAreaVolume_AreaType
- ESpecialPakID
- ESpecialWatchType
- ESpeciesOrganization
- ESpecificFunctionType
- ESpectatorScreenMode
- ESpeedTreeGeometryType
- ESpeedTreeLODType
- ESpeedTreeWindType
- ESpeedType
- ESphericalLimitType
- ESphericalLimitType_UE5
- ESpikeDeploymentState
- ESpineWidgetAreaType
- ESplicedTrain
- ESplicedTrainLinkErrorCode
- ESplineBoneAxis
- ESplineCoordinateSpace
- ESplineMeshAxis
- ESplinePickerDirectionType
- ESplinePickerOffsetType
- ESplinePointType
- ESplineRouteType
- ESplineSnappingType
- ESpotGroupType
- ESpotType
- ESpriteCollisionMode
- ESpriteExtractMode
- ESpritePivotMode
- ESpritePolygonMode
- ESpriteShapeType
- ESsfNormalGenerationMethod
- ESsfNormalImportMethod
- ESsfSceneOptionsHierarchyType
- ESsfSceneReimportStatusFlags
- ESsfVertexColorImportOption
- EStandInsOutlinerActionType
- EStandbyType
- EStarTypeID
- EStateType
- EStaticMeshLODType
- EStaticMeshLightingInfoObjectSets
- ESteerDebugerDataType
- EStereoLayerShape
- EStereoLayerType
- EStoreId
- EStrategicApplyState
- EStrategicRunSide
- EStreamingVolumeUsage
- EStretch
- EStretchDirection
- EStructUtilsResult
- EStructViewerDeveloperType
- EStyleColor
- ESubAnimMapReplaceType
- ESubAnimType
- ESubSystemType
- ESubUVBoundingVertexCount
- ESubmixEffectDynamicsPeakMode
- ESubmixEffectDynamicsProcessorType
- ESubtitleKeyAnchorType
- ESubtitleKeyAnimationType
- ESubtitleKeyType
- ESubtitleRichTextType
- ESuggestProjVelocityTraceOption
- ESuperPeopleSkillActionType
- ESuperPeopleSkillType
- ESurfBoardState
- ESurfaceAlignMode
- ESurroundRotationType
- ESurroundState
- ESurroundTowardsType
- ESurvivePickUpCategory
- ESurvivePickUpGlobalCategory
- ESurvivePickUpType
- ESurviveWeaponPropSlot
- ESuspiciousInfoThresholdType
- ESwitchDSPrerequisiteType
- ESwitchTableType
- ESwitchWeaponFlag
- ESwordSniperShootMode
- ESyncOperation
- ESyncPropertyFlags
- eStopMoveReason
- ETGISMsgType
- ETLog_BackpackEquipmentSlotType
- ETWSTurnState
- ETableAssetCookRule
- ETableViewMode
- ETagLogParamType
- ETakeDamageDirByPhysics
- ETakeDamagePerform
- ETakeDamageRunState
- ETankTurnResult
- ETargetEnemyType
- ETargetLoopType
- ETargetPickerShapeType
- ETargetsSortType
- ETaskActionType
- ETaskBBOperType
- ETaskConbinationOperation
- ETaskConditionType
- ETaskDurationType
- ETaskEventType
- ETaskObjectCacheType
- ETaskParamSrcType
- ETaskParamType
- ETaskPlayerAchievementType
- ETaskPlayerConditionStateType
- ETaskPlayerPropCompType
- ETaskResourceOverlapPolicy
- ETaskResultTag
- ETaskSubType
- ETaskTableType
- ETaskTeamActionConditionType
- ETaskTriggerAreaType
- ETaskTriggerItemType
- ETaskType
- ETeamAttitude
- ETeamMatchCampType
- ETeamMatchStageType
- ETeamNumber
- ETeamTaskType
- ETeammateIconInvisibleReason
- ETelecontrolState
- ETemperatureSeverityType
- ETemplateCreateMethod
- ETerrainCoordMappingType
- ETestAvgPingDataType
- ETestBoneVertexType
- ETetrominoAttachType
- ETetrominoType
- ETexAlign
- ETexBias
- ETextCommit
- ETextFlowDirection
- ETextGender
- ETextHorzPos
- ETextJustify
- ETextKeyOperation
- ETextShapingMethod
- ETextVertPos
- ETextVerticalJustify
- ETextWrappingPolicy
- ETextureBasisSetting
- ETextureChannel
- ETextureColorChannel
- ETextureCompressionQuality
- ETextureCrunchSetting
- ETextureEditorBackgrounds
- ETextureMipCount
- ETextureMipValueMode
- ETextureObjectSets
- ETexturePaintIndex
- ETexturePowerOfTwoSetting
- ETextureRenderTargetFormat
- ETextureSamplerFilter
- ETextureSizingType
- ETextureSourceArtType
- ETextureSourceFormat
- ETextureType
- ETextureWeightTypes
- ETexturesCheckObjectSets
- EThreePlayerSplitScreenType
- EThrowGrenadeMode
- EThrowLimitation
- EThrowState
- EThumbnailPrimType
- EThumbnailQuality
- ETickingGroup
- ETileMapProjectionMode
- ETimeLimitStatus
- ETimeLimitType
- ETimeLineCheckResult
- ETimeStretchCurveMapping
- ETimelineDirection
- ETimelineLengthMode
- ETimelineSigType
- ETimerOperateType
- ETimezoneSetting
- ETipType
- EToMove
- EToPlainTextMode
- EToolMenuInsertType
- EToolMenuSectionAlign
- EToolMenuStringCommandType
- ETopMostUIPanelType
- ETouchEventStatus
- ETouchFingerFlag
- ETouchFireType
- ETouchIndex
- ETouchType
- ETraceType
- ETraceTypeQuery
- ETrackActiveCondition
- ETrackCheckNeedRunType
- ETrackSideType
- ETrackToggleAction
- ETrackingStatus
- ETrail2SourceMethod
- ETrailMarkType
- ETrailWidthMode
- ETrailerMovementMode
- ETrailsRenderAxisOption
- ETrainHeadingDir
- ETrainRouteMoveState
- ETrajectoryMoveState
- ETransformConstraintType
- ETransformationDomain
- ETransformationType
- ETransitionBlendMode
- ETransitionGetter
- ETransitionLogicType
- ETransitionType
- ETranslucencyLightingMode
- ETranslucentSortPolicy
- ETravelFailure
- ETravelType
- ETriangleSortAxis
- ETriangleSortOption
- ETriggerEvent
- ETriggerLevelCheckStatus
- ETriggerLevelLoadState
- ETriggerSkillCondition
- ETriggerType
- ETrueSightCameraDirectionType
- ETrueSightDataType
- ETrueSightTestActorType
- ETurnToAxis
- ETurretWeaponCrossHairTypes
- ETutorialAnchorIdentifier
- ETutorialContent
- ETweenDataType
- ETweenPlayMode
- ETweenState
- ETwitterIntegrationDelegate
- ETwitterRequestMethod
- ETwoPlayerSplitScreenType
- EType
- ETypeAdvanceAnim
- ETypeOfWalls
- eTeamSightMode
- EUAEBlackboardType
- EUAECharacterRegionSize
- EUAESkillCondition_BlackboardValueComparison
- EUAESkillEvent
- EUAESpotGroupType
- EUAESpotType
- EUAETriggerActionExecPolicy
- EUAETriggerActionState
- EUAETriggerRunType
- EUAETriggerVariableType
- EUAEUserWidgetInputActionEvent
- EUAVCharacterMsgType
- EUAVUseType
- EUEMeshReductionModuleType
- EUGCAIAmmoEnoughType
- EUGCAITakeMedicineType
- EUGCAIThrowProjectilePhase
- EUGCActivityTaskResetType
- EUGCActivityType
- EUGCAddItemReason
- EUGCAnimPlayType
- EUGCBattlePhase
- EUGCCampSpawnPointSelectionMethod
- EUGCChooseEnemyStrategy
- EUGCChooseEnemyType
- EUGCCommodityCommandType
- EUGCCommodityResponseType
- EUGCCommonItemReason
- EUGCCommonItemRepType
- EUGCCompareAngleType
- EUGCCrossHairPresetType
- EUGCCustomModeInputReason
- EUGCDeadDropType
- EUGCDropItemListGeneratorType
- EUGCDropItemPositionDirection
- EUGCEnemyHatredMaxDistanceType
- EUGCExceptionFlags
- EUGCExceptionVerbosity
- EUGCFoliageDistribution
- EUGCFoliageMode
- EUGCGenerateItemEntityType
- EUGCHPBarShowMode
- EUGCHatredType
- EUGCItemChangeType
- EUGCItemGAActiveCondition
- EUGCItemSpawnerConfigMode
- EUGCItemSpawnerManagerStartCondition
- EUGCMBindErrorCode
- EUGCMBrushType
- EUGCMCaptureMoveMode
- EUGCMDSWaitingExtraState
- EUGCMInstigatorType
- EUGCMItemDecoratorParticleAttachMode
- EUGCMItemDecoratorType
- EUGCMItemDecoratorVisualSwitchMode
- EUGCMItemDecoratorWorkerType
- EUGCMLoadingUIState
- EUGCMMapSerializeRst
- EUGCMMapStatus
- EUGCMPreviewSceneLoadState
- EUGCMPreviewSceneStage
- EUGCMPreviewSceneUpdateMode
- EUGCMSerializeType
- EUGCM_ActorSelectType
- EUGCM_MapSerMask
- EUGCMailOperationFailedReason
- EUGCMailStatus
- EUGCMapMarkShortcutActionType
- EUGCMobDynamicStateOp
- EUGCMobSidesShiftSideWays
- EUGCMobSpawnerConfigMode
- EUGCMobSpawnerContrMode
- EUGCMobSpawnerManagerStartCondition
- EUGCMobState
- EUGCMobileActorCategory
- EUGCMobileActorPoolingPolicy
- EUGCMobileArchiveCategory
- EUGCMobileArchiveReturnCode
- EUGCMobileArchiveType
- EUGCMobileBindLimit
- EUGCMobileCheckMapConstraintReason
- EUGCMobileConfigOverrideStatus
- EUGCMobileDataIOResult
- EUGCMobileDataOperationCode
- EUGCMobileDataOperationReason
- EUGCMobileDependencyPropertyHandleUpdateStrategy
- EUGCMobileEditSplinePointAddRes
- EUGCMobileEditorStatus
- EUGCMobileEndPreviewReason
- EUGCMobileEnvType
- EUGCMobileEventScopeType
- EUGCMobileFeatureScope
- EUGCMobileGamePhase
- EUGCMobileModeType
- EUGCMobileMotionCheckResult
- EUGCMobileMotionCompSpace
- EUGCMobileMotionCompType
- EUGCMobileMotionEventActionType
- EUGCMobileMotionPauseFlag
- EUGCMobileMotionSplinePathType
- EUGCMobileMotionStartType
- EUGCMobileMotionState
- EUGCMobileNonUniformMotionExerciseType
- EUGCMobileOperatorStatus
- EUGCMobilePendulumAxis
- EUGCMobilePreviewReason
- EUGCMobilePropertyChangedType
- EUGCMobileRebuildMapReason
- EUGCMobileRequestEndPreviewResult
- EUGCMobileRequestPreviewResult
- EUGCMobileSetRTEActorsHiddenReson
- EUGCMobileSpawnFlag
- EUGCMobileSplinePointMode
- EUGCMobileSplinePointPositionType
- EUGCMobileSplineStyleMode
- EUGCMobileTestMode
- EUGCMobileTransformModule
- EUGCMobile_RTEActorBindingCmdType
- EUGCMobile_RTEActorChildCmdType
- EUGCMobile_RTEActorCombinationCmdType
- EUGCMobile_RTEActorStateCmdType
- EUGCMobile_RTEBindEventCmdType
- EUGCMobile_RTECameraCommandType
- EUGCMobile_RTECommandType
- EUGCMobile_RTEEditableUICmdType
- EUGCMobile_RTESkyboxCmdType
- EUGCMobilityType
- EUGCMotionCompType
- EUGCObjectTemplateType
- EUGCPercentTaskResetType
- EUGCPlayerRespawnPointSelectionMethod
- EUGCPlayerSpawnPointSelectionMethod
- EUGCRemoveItemReason
- EUGCSpawnWaveStartCondition
- EUGCStateDealMethod
- EUGCTaskCustomWeekResetType
- EUGCTaskLineAwardState
- EUGCTaskLineType
- EUGCTaskState
- EUGCTaskTargetType
- EUGCToastPriorityType
- EUGCToastReceiverType
- EUGCToastSizeType
- EUGCWeaponCooperateType
- EUIActionType
- EUIMarkState
- EUINavigation
- EUINavigationRule
- EUIOperateType
- EUIParticlePropertyType
- EUIScalingRule
- EUMGSequencePlayMode
- EUTGetterType
- EUTGiftType
- EUTSkillEntry
- EUVOutput
- EUVParameterizerType
- EUVStrech
- EUnPossessReason
- EUnit
- EUnitDisplay
- EUniversalTaskBlackboardType
- EUniversalTaskEventParamType
- EUniversalTaskNodeState
- EUniversalTaskState
- EUniversalTaskTableParamType
- EUniversalTaskTestOBType
- EUpScaleMethod
- EUpdateAnimAssetEvent
- EUpdateFrequency
- EUpdateRateShiftBucket
- EUpdateTransformOption
- EUpdateUIInfoType
- EUpdateWaypointResult
- EUseRedemptionCodeResult
- EUseSWPState
- EUserDefinedStructureStatus
- EUserWidgetFadingStatus
- EUserWidgetNameEqualPolitics
- EVFXCameraAlignmentPolicy
- EVFXSamplingMode
- EVFXSimulationMode
- EVHFRRSerializeFlag
- EVHKFSerializeFlag
- EVHSeatDeferredMoveType
- EVHSeatGUIType
- EVHSeatSideType
- EVHSeatSpecialType
- EVHSeatWeaponHoldType
- EVLMOptimizeType
- EVREditorWidgetDrawingPolicy
- EValidatorType
- EValueCompareLogic
- EValueType
- EVariableMetaDataFlag
- EVaultDir
- EVaultFoot
- EVaultType
- EVectorArithmeticOperationType
- EVectorDBType
- EVectorFieldConstructionOp
- EVectorNoiseFunction
- EVectorPart
- EVectorQuantization
- EVectorVMBaseTypes
- EVectorVMOp
- EVectorVMOperandLocation
- EVehAnimAssetType
- EVehCameraDataType
- EVehicle2HPType
- EVehicleAIAvoidanceMode
- EVehicleAccelerateSkillState
- EVehicleAcclerateType
- EVehicleAdvancedConditionType
- EVehicleAnimType
- EVehicleAudioEffectiveState
- EVehicleAvatarSlot
- EVehicleBurnTireMode
- EVehicleConnectFailReason
- EVehicleControlPanelSubMode
- EVehicleControlType
- EVehicleCraftParachuteState
- EVehicleCreateType
- EVehicleDifferential4W
- EVehicleDriftState
- EVehicleDriftStopReason
- EVehicleEffectParamType
- EVehicleFailReason
- EVehicleForceTickAnimMask
- EVehicleInterruptType
- EVehicleMeshMode
- EVehicleMoveCompType
- EVehicleMultiMoveStateChangeFailReason
- EVehicleMultiMoveStateChangeReason
- EVehiclePCTipsUIType
- EVehicleParachuteState
- EVehicleParachutingState
- EVehiclePartDirection
- EVehiclePartName
- EVehiclePengState
- EVehicleSeatType
- EVehicleShootWeaponCalculatorType
- EVehicleSkillErrorCode
- EVehicleSkillState
- EVehicleSkillType
- EVehicleSpotRandomType
- EVehicleTeleportSkillState
- EVehicleTextureType
- EVehicleTireState
- EVehicleType
- EVehicleUpgradeDataType
- EVehicleWeaponBoardDataType
- EVelocityChangeType
- EVenomArmState
- EVerifyFunctionTag
- EVersionControlBehavior
- EVertexColorImportOption
- EVertexColorMaskChannel
- EVertexPaintAxis
- EVerticalAlignment
- EVerticalTextAligment
- EVibrateStrengthLevel
- EVibrateTriggerActionType
- EVibrateTriggerEventType
- EVibrateTriggerMainItemType
- EVibrateTriggerSubItemType
- EViedoRecorderAdaptorType
- EViewBindingMemberType
- EViewDirection
- EViewLimitType
- EViewModeIndex
- EViewTargetBlendFunction
- EViewportInteractionDraggingMode
- EViewportTransformType
- EVirtualItemAddItemSource
- EVirtualItemRepType
- EVirtualJoystickState
- EVirtualKeyboardType
- EVisibilityAggressiveness
- EVisibilityTrackAction
- EVisibilityTrackCondition
- EVoiceCheckResource
- EVoiceMicrophoneType
- EVoiceSignFailedReason
- EVoiceVisualizationFlag
- EVolumeLightingMethod
- EWASDType
- EWS_TimelineEventFuncType
- EWS_UnitType
- EWalkSTATE
- EWalkType
- EWalkableSlopeBehavior
- EWarDogCommandType
- EWarDogLocomotionType
- EWarDogLookAtTargetType
- EWarDogMoveToTargetState
- EWarDogSearchState
- EWarDogVehicleState
- EWarScoreChangeReason
- EWaterRangeType
- EWaveState
- EWaypointParamType
- EWeaponAbilityEnableType
- EWeaponAbilityKillCount
- EWeaponAbilityRepType
- EWeaponAction
- EWeaponAttachSocket
- EWeaponAttachState
- EWeaponAttachmentSocketType
- EWeaponAttrCheckConfigType
- EWeaponBaseNotifyCheckType
- EWeaponComponentType
- EWeaponCustomMeshType
- EWeaponDisplayMode
- EWeaponFireMode
- EWeaponGAActiveCondition
- EWeaponGAUnEquipState
- EWeaponGameplayStateStage
- EWeaponGraphNodeType
- EWeaponHoldType
- EWeaponMeshType
- EWeaponModuleModifyAttrType
- EWeaponOperationMode
- EWeaponPendantSocketType
- EWeaponReloadMethod
- EWeaponReloadState
- EWeaponReloadType
- EWeaponShootIntervalMode
- EWeaponSightType
- EWeaponSingleHandHoldType
- EWeaponSlot
- EWeaponSpecialSoundType
- EWeaponState
- EWeaponSubSlotType
- EWeaponSwitchWay
- EWeaponTriggerEvent
- EWeaponType
- EWeaponTypeNew
- EWeaponVeiryIgnore
- EWeaponWeightType
- EWeaponsCompanionRuleVoiceType
- EWeaponsCompanionVoiceEvent
- EWeatherChangeEvent
- EWeatherChangeStatus
- EWeatherSequencePlaybackStatus
- EWeatherSequenceType
- EWeatherStatusType
- EWeatherType
- EWheelSweepType
- EWidgetAnimationEvent
- EWidgetBlendMode
- EWidgetClipping
- EWidgetDesignFlags
- EWidgetGeometryMode
- EWidgetInteractionSource
- EWidgetLayoutSlotType
- EWidgetMatchMethod
- EWidgetMatchStatus
- EWidgetSpace
- EWidgetTestAppearLocation
- EWidgetTimingPolicy
- EWidgetUIBlueprintType
- EWindSourceType
- EWindowMode
- EWindowTitleBarMode
- EWonderfulCutCaptureType
- EWonderfulCutOutputType
- EWonderfulCutShootDamageType
- EWorldCellPartitionGrade
- EWorldPositionIncludedOffsets
- EWorldTileLodPlatform
- EWrapperMeshLoadType
- EWriteDisallowedWarningState
- EXPBDComplianceType
- EXPBDComplianceType_UE5
- ExtraPlayerLiveState
- EZoneType
- E_AnimNotifyState_AdaptType
- FAIDistanceType
- FAPTCDropOffLocationType
- FASTNodeType
- FAvatarManagermentMemoryCompareType
- FAvatarManagermentModClientMemoryType
- FAvatarManagermentModClientPaltformType
- FAvatarManagermentModLaunchOccasion
- FAvatarManagermentModLaunchOccasionConfigType
- FAvatarManagermentModRunModeType
- FDriverAttachmentType
- FDropOffLocationType
- FExtendTaskEventID
- FExtendTaskState
- FFixedDropOffLocationType
- FItemTypeEnum
- FNavigationSystemRunMode
- FoliageVertexColorMask
- FPESkillAttributeModifyMethod
- FQuestionAnswerStatusType
- FSeekingState
- FSkillType
- FSoundType
- FTeslaModelFxStatusType
- FTeslaModelStatusType
- FUGCMobileMotionStartStopState
- FUGCMobileMotionSyncState
- FUGCVehiclePhysicsShapeType
- FUGC_ACCharacterEnum
- FUIOperationType
- GuideConfig.RunMode
- GuideConfig.State
- GuideConfig.TriggerMode
- HomeLightType
- InputReason
- InputType
- IteratorType
- KilledReason
- LandscapeSplineMeshOrientation
- LevelExportType
- MammothVehicleSkill
- ManagerParticleType
- MaskTarget_PhysMesh
- MIDIEventType
- ModulationParamMode
- MovieScene3DPathSection_Axis
- NativeGameAttributeType
- ObjectMovingType
- ObsAvoidDir
- PanningRule
- ParticleFilterType
- ParticleReplayState
- ParticleSystemLODMethod
- PCGDistanceShape
- PCGNormalToDensityMode
- PCGSpatialNoiseMask2DMode
- PCGSpatialNoiseMode
- PerfStartEventType
- ProfileDemandType
- PropertEditorTestEnum
- QuickChatType
- RelevantToOwnerOwnerType
- ReverbPreset
- ShootWeaponAnimType
- SkeletalMeshOptimizationImportance
- SkeletalMeshOptimizationType
- SkillEditorPawnType
- SledFlyingStage
- SurfaceColliderType
- TargetEffectType
- TargetLeafState
- TextureAddress
- TextureCompressionSettings
- TextureFilter
- TextureGroup
- TextureMipGenSettings
- TrueSightTestType
- UAETParamType
- UBLEType
- UDeviceScreenType
- UDeviceSensorType
- UGetActorStrategy
- UPESkillTaskProgressUIType
- UTPickerTargetType
- UTSkillEventType
- UTSkillPhaseType
- UTSkillPickerType
- UTSkillStopReason
- UTSkill_SoundCue_ListenType
- WeatherUICountDownType
- WolfKind
- ZombieKind

### 全部结构体列表

- FA2CSPose
- FA2Pose
- FACESParameter
- FAIDamageEvent
- FAIDataProviderBoolValue
- FAIDataProviderFloatValue
- FAIDataProviderIntValue
- FAIDataProviderTypedValue
- FAIDataProviderValue
- FAIMoveRequest
- FAINoiseEvent
- FAIPredictionEvent
- FAIRequestID
- FAISenseAffiliationFilter
- FAISightEvent
- FAIStimulus
- FAITeamStimulusEvent
- FAITouchEvent
- FARFilter
- FActionBindingCluster
- FActionBindingInfo
- FActionCluster
- FActiveForceFeedbackEffect
- FActiveHapticFeedbackEffect
- FActorPerceptionBlueprintInfo
- FActorSet
- FAggregatedCollision
- FAmbientCube
- FAmbientCube2
- FAmbientCubeFace
- FAnchorData
- FAnchors
- FAngularDriveConstraint
- FAnimControlTrackKey
- FAnimGroupInfo
- FAnimGroupInstance
- FAnimLegIKDefinition
- FAnimLinkableElement
- FAnimMontageInstance
- FAnimNodeBoneShiftTolerenceChecker
- FAnimNode_AimOffsetLookAt
- FAnimNode_AnimDynamics
- FAnimNode_AnimDynamics_UE5
- FAnimNode_ApplyAdditive
- FAnimNode_ApplyMeshSpaceAdditive
- FAnimNode_AssetPlayerBase
- FAnimNode_Base
- FAnimNode_BlendBoneByChannel
- FAnimNode_BlendListBase
- FAnimNode_BlendListByBool
- FAnimNode_BlendListByEnum
- FAnimNode_BlendListByInt
- FAnimNode_BlendListBySlot
- FAnimNode_BlendListBySlots
- FAnimNode_BlendSpaceEvaluator
- FAnimNode_BlendSpacePlayer
- FAnimNode_BoneBlendFilter
- FAnimNode_BoneDrivenController
- FAnimNode_BoneFollowChain
- FAnimNode_BoneMirror
- FAnimNode_BoneRetarget
- FAnimNode_CCDIK
- FAnimNode_CachedBoneTransform
- FAnimNode_CompnentPoseBase
- FAnimNode_Constraint
- FAnimNode_ConvertComponentToLocalSpace
- FAnimNode_ConvertLocalToComponentSpace
- FAnimNode_CopyBone
- FAnimNode_CopyBoneDelta
- FAnimNode_CopyBonesFromPose
- FAnimNode_CopyBonesFromPose_Config
- FAnimNode_CopyMotion
- FAnimNode_CopyPoseFromMesh
- FAnimNode_CopyPoseFromRemapping
- FAnimNode_CurveSource
- FAnimNode_EmoteSwitchAdapt
- FAnimNode_Fabrik
- FAnimNode_HandIKRetargeting
- FAnimNode_HandIKRetargeting_UE5
- FAnimNode_HeadDodging
- FAnimNode_Inertialization
- FAnimNode_LayeredBoneBlend
- FAnimNode_LegIK
- FAnimNode_LookAt
- FAnimNode_MakeDynamicAdditive
- FAnimNode_ModifyBone
- FAnimNode_ModifyBoneList
- FAnimNode_ModifyBoneTransforms
- FAnimNode_ModifyBoneWithFunction
- FAnimNode_ModifyCurve
- FAnimNode_MoveAdditiveLayering
- FAnimNode_MultiWayBlend
- FAnimNode_ObserveBone
- FAnimNode_PoseBlendNode
- FAnimNode_PoseByName
- FAnimNode_PoseDriver
- FAnimNode_PoseHandler
- FAnimNode_PoseSnapshot
- FAnimNode_QuadrupedTerrainAdapting
- FAnimNode_RandomPlayer
- FAnimNode_RectificationBone
- FAnimNode_RefPose
- FAnimNode_ResetBoneTransform
- FAnimNode_RigidBody
- FAnimNode_RigidBody_UE5
- FAnimNode_Root
- FAnimNode_RotateRootBone
- FAnimNode_RotationMultiplier
- FAnimNode_RotationOffsetBlendSpace
- FAnimNode_SaveCachedPose
- FAnimNode_ScaleChainLength
- FAnimNode_SequenceEvaluator
- FAnimNode_SequencePlayer
- FAnimNode_SkeletalControlBase
- FAnimNode_Slot
- FAnimNode_SplineIK
- FAnimNode_SpringBone
- FAnimNode_StateMachine
- FAnimNode_SubInput
- FAnimNode_SubInstance
- FAnimNode_Trail
- FAnimNode_TransitionPoseEvaluator
- FAnimNode_TransitionResult
- FAnimNode_TwistCorrectiveNode
- FAnimNode_TwoBoneIK
- FAnimNode_TwoWayBlend
- FAnimNode_UseCachedBoneTransform
- FAnimNode_UseCachedPose
- FAnimNotifyStateBoneRetargetAdaptInfo
- FAnimParentNodeAssetOverride
- FAnimPhysBodyDefinition_UE5
- FAnimPhysConstraintSetup
- FAnimPhysConstraintSetup_UE5
- FAnimPhysPlanarLimit
- FAnimPhysPlanarLimit_UE5
- FAnimPhysSphericalLimit
- FAnimPhysSphericalLimit_UE5
- FAnimSegment
- FAnimSequenceTrackContainer
- FAnimSetMeshLinkup
- FAnimSlotDesc
- FAnimSlotGroup
- FAnimSlotInfo
- FAnimTrack
- FAnimUpdateRateParameters
- FAnimationActiveTransitionEntry
- FAnimationEventBinding
- FAnimationGroupReference
- FAnimationRecordingSettings
- FAnimationState
- FAnimationStateBase
- FAnimationTransitionBetweenStates
- FAnimationTransitionRule
- FAssetBundleData
- FAssetBundleEntry
- FAssetData
- FAssetEditorOrbitCameraPosition
- FAssetManagerRedirect
- FAssetMapping
- FAtlasTexList
- FAtlasTextures
- FAtmospherePrecomputeParameters
- FAudioComponentParam
- FAudioEQEffect
- FAudioQualitySettings
- FAutoCompleteCommand
- FAutoCompleteNode
- FAutomationEvent
- FAxisBindingCluster
- FAxisBindingInfo
- FBLEEnumInfo
- FBPInterfaceDescription
- FBPVariableDescription
- FBPVariableMetaDataEntry
- FBTCompositeChild
- FBTDecoratorLogic
- FBakedAnimationState
- FBakedAnimationStateMachine
- FBakedStateExitTransition
- FBaseAttenuationSettings
- FBasedMovementInfo
- FBasedPosition
- FBatchedLine
- FBatchedPoint
- FBeamModifierOptions
- FBeamTargetData
- FBehaviorTreeTemplateInfo
- FBillBoardMaterialSpriteElement
- FBillboardData
- FBlackListAssetData
- FBlackboardEntry
- FBlendBoneByChannelEntry
- FBlendParameter
- FBlendProfileBoneEntry
- FBlendSample
- FBlendSampleData
- FBlueprintComponentDelegateBinding
- FBlueprintEditorPromotionSettings
- FBlueprintInputActionDelegateBinding
- FBlueprintInputAxisDelegateBinding
- FBlueprintInputAxisKeyDelegateBinding
- FBlueprintInputDelegateBinding
- FBlueprintInputKeyDelegateBinding
- FBlueprintInputTouchDelegateBinding
- FBlueprintWarningSettings
- FBlueprintWidgetAnimationDelegateBinding
- FBodyInstance
- FBoneListTransforms
- FBoneMirrorConfig
- FBoneMirrorConfig_AutoLR
- FBoneMirrorConfig_GivenName
- FBoneMirrorExport
- FBoneMirrorInfo
- FBoneMirrorMapData
- FBoneNode
- FBoneOffset
- FBoneReductionSetting
- FBoneSocketTarget
- FBonesTransfroms
- FBonesTransfromsWithFPP
- FBoolTrackKey
- FBoundActorProxy
- FBox
- FBox2D
- FBoxSphereBounds
- FBranchFilter
- FBranchingPoint
- FBranchingPointMarker
- FBuildPromotionImportWorkflowSettings
- FBuildPromotionNewProjectSettings
- FBuildPromotionOpenAssetSettings
- FBuildPromotionTestSettings
- FBuilderPoly
- FButtonInputActionBinding
- FButtonInputActionBindings
- FButtonInputActionBindingsStruct
- FButtonInputActionSelector
- FButtonInputAxisSelector
- FButtonListenAction
- FButtonStyle
- FCDLODMeshNodeData
- FCacheCameraShakeData
- FCachedBoneParamInfo
- FCachedBoneTransformContainer
- FCachedBoneTransformInfo
- FCameraCacheEntry
- FCameraCutInfo
- FCameraExposureSettings
- FCameraFilmbackSettings
- FCameraFocusSettings
- FCameraLensSettings
- FCameraLookatTrackingSettings
- FCameraPreviewInfo
- FCameraTrackingFocusSettings
- FCampConfigInfo
- FCampReleation
- FCanvasIcon
- FCanvasUVTri
- FCaptureProtocolID
- FCaptureResolution
- FCheckBoxStyle
- FClassRedirect
- FClientReceiveData
- FClothCollisionData
- FClothCollisionPrim_Convex
- FClothCollisionPrim_Sphere
- FClothCollisionPrim_SphereConnection
- FClothConfig
- FClothConstraintSetup
- FClothLODData
- FClothParameterMask_PhysMesh
- FClothPhysicalMeshData
- FClothPhysicsProperties_Legacy
- FClothVertBoneData
- FClothingAssetData_Legacy
- FClusterNode
- FCollectionBoolParameter
- FCollectionIntParameter
- FCollectionParameterBase
- FCollectionReference
- FCollectionScalarParameter
- FCollectionStructParameter
- FCollectionVectorParameter
- FCollisionImpactData
- FCollisionProfileName
- FCollisionResponse
- FCollisionResponseContainer
- FCollisionResponseTemplate
- FColor
- FColorGradePerRangeSettings
- FColorGradingSettings
- FColorMaterialInput
- FColorParameterNameAndCurves
- FComboBoxStyle
- FComboButtonStyle
- FCompilerNativizationOptions
- FComponentKey
- FComponentOverrideRecord
- FComponentReference
- FComponentSpacePose
- FCompositeFallbackFont
- FCompositeFont
- FCompositeSection
- FCompositeSubFont
- FCompositionGraphCapturePasses
- FCompressedTrack
- FConeConstraint
- FConfigOverriderSetting
- FConstrainComponentPropName
- FConstraint
- FConstraintBaseParams
- FConstraintDrive
- FConstraintInstance
- FConstraintProfileProperties
- FConvolutionBloomSettings
- FCrowdAvoidanceConfig
- FCrowdAvoidanceSamplingPattern
- FCullDistanceSizePair
- FCurveEdEntry
- FCurveEdTab
- FCurveParams
- FCurveTableRowHandle
- FCurveTrack
- FCustomChannelSetup
- FCustomHeightFog
- FCustomInput
- FCustomMontageAnimInfo
- FCustomProfile
- FCustomSkeletonName
- FCustomizedToolMenu
- FCustomizedToolMenuEntry
- FCustomizedToolMenuNameArray
- FCustomizedToolMenuSection
- FDPProfileMatch
- FDPProfileMatchItem
- FDamageEvent
- FDataTableCategoryHandle
- FDataTableRowHandle
- FDebugDisplayProperty
- FDebugFloatHistory
- FDebugTextInfo
- FDecalBakingRequest
- FDecalParameter
- FDelayInitAnimTickParam
- FDelegateArray
- FDelegateRuntimeBinding
- FDepthFieldGlowInfo
- FDialogueContext
- FDialogueContextMapping
- FDialogueWaveParameter
- FDirectorTrackCut
- FDirectoryPath
- FDistanceDatum
- FDistributionLookupTable
- FDockTabStyle
- FDrawToRenderTargetContext
- FDropNoteInfo
- FDynamicBatchSectionInfo
- FDynamicGenerateTargetNavigation
- FDynamicPropertyPath
- FDynamicTextureInstance
- FEdGraphPinReference
- FEdGraphPinType
- FEdGraphSchemaAction
- FEdGraphSchemaAction_NewNode
- FEdGraphTerminalType
- FEditableTextBoxStyle
- FEditableTextStyle
- FEditedDocumentInfo
- FEditorElement
- FEditorImportExportTestDefinition
- FEditorImportWorkflowDefinition
- FEditorMapPerformanceTestDefinition
- FElementID
- FEmitterDynamicParameter
- FEmoteBoneAdaptConfig
- FEngineShowFlagsSetting
- FEnvQueryInstanceCache
- FEnvQueryRequest
- FEscRespondSetting
- FEventPayload
- FEventTrackKey
- FExpandableAreaStyle
- FExpectedQuality
- FExposedValueCopyRecord
- FExposedValueHandler
- FExposureSettings
- FExpressionInput
- FExpressionOutput
- FExternalToolDefinition
- FExtraPVSInfo
- FFOscillator
- FFastArraySerializerItem
- FFastRepRemoteContent
- FFilePath
- FFilmStockSettings
- FFindFloorResult
- FFixedDPIValueEntry
- FFixedDPIValueMap
- FFloatDistribution
- FFloatInterval
- FFloatRK4SpringInterpolator
- FFloatRange
- FFloatRangeBound
- FFoliageTypeLocation
- FFoliageTypeObject
- FFoliageVertexColorChannelMask
- FFontCharacter
- FFontData
- FFontImportOptionsData
- FFontOutlineSettings
- FFontParameterValue
- FFontRenderInfo
- FForceFeedbackChannelDetails
- FForeignControlPointData
- FForeignSplineSegmentData
- FForeignWorldSplineData
- FFormatArgumentData
- FFppTppShadowChangeRecord
- FFractureEffect
- FFullyLoadedPackagesInfo
- FFunctionBoneModifyData
- FFunctionExpressionInput
- FFunctionExpressionOutput
- FGPUSpriteEmitterInfo
- FGPUSpriteLocalVectorFieldInfo
- FGPUSpriteResourceData
- FGameMagnitudeWrapper
- FGameModeName
- FGameModePawnPool
- FGameNameRedirect
- FGameplayTag
- FGameplayTagCategoryRemap
- FGameplayTagContainer
- FGameplayTagQuery
- FGameplayTagRedirect
- FGameplayTagSource
- FGameplayTagTableRow
- FGaussianSumBloomSettings
- FGenericStruct
- FGenericTeamId
- FGeomSelection
- FGerstnerWaterWaveGeneratorSimple
- FGerstnerWave
- FGraphReference
- FGrassInput
- FGrassVariety
- FGridBlendSample
- FGridVisibilityCameraInfo
- FGroupedSkeletalOptimizationSettings
- FGroupedStaticMeshOptimizationSettings
- FGuid
- FHLODProxyMesh
- FHLODStreamTicker
- FHapticFeedbackDetails_Curve
- FHardwareCursorReference
- FHeaderRowStyle
- FHierarchicalSimplification
- FHitResult
- FHyperlinkStyle
- FIdeaBakingPrimitiveSettings
- FIdeaBakingWorldInfoSettings
- FIdeaGrassFieldData
- FImportFactorySettingValues
- FImportanceTexture
- FIndexedCurve
- FInlineEditableTextBlockStyle
- FInlineTextImageStyle
- FInputActionKeyMapping
- FInputAxisConfigEntry
- FInputAxisKeyMapping
- FInputAxisProperties
- FInputBindingInfo
- FInputBlendPose
- FInputChord
- FInputScaleBias
- FInputTouchCacheData
- FInstanceRecoverData
- FInstanceRun
- FInstanceVisibilityData
- FInstancedStaticMeshInstanceData
- FInstancedWidget3DInstanceData
- FInt32Interval
- FInt32Range
- FInt32RangeBound
- FIntMargin
- FIntPoint
- FIntVector
- FIntegralCurve
- FIntegralKey
- FInteriorSettings
- FInterpControlPoint
- FInterpCurveFloat
- FInterpCurveLinearColor
- FInterpCurvePointFloat
- FInterpCurvePointLinearColor
- FInterpCurvePointQuat
- FInterpCurvePointTwoVectors
- FInterpCurvePointVector
- FInterpCurvePointVector2D
- FInterpCurveQuat
- FInterpCurveTwoVectors
- FInterpCurveVector
- FInterpCurveVector2D
- FInterpEdSelKey
- FInterpGroupActorInfo
- FInterpLookupPoint
- FInterpLookupTrack
- FInterpolationParameter
- FItemDefineID
- FItemOperationInfoV2
- FJsonHaptic
- FJsonObjectWrapper
- FKAggregateGeom
- FKBoxElem
- FKConvexElem
- FKSphereElem
- FKSphylElem
- FKeyBind
- FLODSoloTrack
- FLODStealConfig
- FLandscapeColorMask
- FLandscapeColorMaskLayer
- FLandscapeEditToolRenderData
- FLandscapeEditorLayerSettings
- FLandscapeImportLayerInfo
- FLandscapeInfoLayerSettings
- FLandscapeLayerStruct
- FLandscapeSplineConnection
- FLandscapeSplineInterpPoint
- FLandscapeSplineMeshEntry
- FLandscapeSplineSegmentConnection
- FLandscapeWeightmapUsage
- FLatentActionInfo
- FLaunchOnTestSettings
- FLayerActorStats
- FLayerBlendInput
- FLensBloomSettings
- FLensImperfectionSettings
- FLensSettings
- FLevelBlockFoliageDstLocation
- FLevelBlockFoliageInfo
- FLevelCollection
- FLevelIndexVisibilityInfo
- FLevelNameAndTime
- FLevelSequenceBindingReference
- FLevelSequenceBindingReferenceArray
- FLevelSequenceBindingReferences
- FLevelSequenceObject
- FLevelSequencePlayerSnapshot
- FLevelSequenceSnapshotSettings
- FLevelSimplificationDetails
- FLevelStreamingStatus
- FLevelViewportInfo
- FLevelVisibilityInfo
- FLightingChannels
- FLightmassDebugOptions
- FLightmassDirectionalLightSettings
- FLightmassLightSettings
- FLightmassMaterialInterfaceSettings
- FLightmassPrecomputedVisibilitySettings
- FLightmassPrimitiveSettings
- FLightmassWorldInfoSettings
- FLinearColor
- FLinearConstraint
- FLinearDriveConstraint
- FLocalSpacePose
- FLocalizedSubtitle
- FLocationBoneSocketInfo
- FMTDResult
- FMainUILayoutData
- FManagementRule
- FManagementRuleBase
- FManagementRuleFNameArrayCheck
- FManagementRuleFNameCheck
- FManagementRuleFStringArrayCheck
- FManagementRuleFStringCheck
- FManagementRuleSwitch
- FMargin
- FMarkerSyncAnimPosition
- FMaterialAttributesInput
- FMaterialBatchInfo
- FMaterialEditorPromotionSettings
- FMaterialFunctionInfo
- FMaterialInput
- FMaterialInstanceBasePropertyOverrides
- FMaterialParameterCollectionInfo
- FMaterialParameterInfo
- FMaterialProxySettings
- FMaterialQualityOverrides
- FMaterialRemapIndex
- FMaterialSpriteElement
- FMaterialTextureInfo
- FMatrix
- FMemberReference
- FMergedAtlasList
- FMeshBuildSettings
- FMeshInstancingSettings
- FMeshLODBiasCondition
- FMeshMergingSettings
- FMeshPerLODBiasArray
- FMeshProxySettings
- FMeshReductionSettings
- FMeshSectionInfo
- FMeshSectionInfoMap
- FMeshShiftParam
- FMeshSocketSelector
- FMeshTriangle
- FMinimalViewInfo
- FModulatorContinuousParams
- FMontageSectionsPlayInfo
- FMoveAdditiveLayeringData
- FMovementProperties
- FMovieScene3DLocationKeyStruct
- FMovieScene3DRotationKeyStruct
- FMovieScene3DScaleKeyStruct
- FMovieScene3DTransformKeyStruct
- FMovieScene3DTransformTemplateData
- FMovieSceneBinding
- FMovieSceneBindingOverrideData
- FMovieSceneCameraAnimSectionData
- FMovieSceneCameraShakeSectionData
- FMovieSceneCaptureSettings
- FMovieSceneColorKeyStruct
- FMovieSceneComponentMaterialSectionTemplate
- FMovieSceneComponentTransformSectionTemplate
- FMovieSceneEasingSettings
- FMovieSceneEditorData
- FMovieSceneEvalTemplate
- FMovieSceneEvaluationField
- FMovieSceneEvaluationFieldSegmentPtr
- FMovieSceneEvaluationFieldTrackPtr
- FMovieSceneEvaluationGroup
- FMovieSceneEvaluationGroupLUTIndex
- FMovieSceneEvaluationKey
- FMovieSceneEvaluationMetaData
- FMovieSceneEvaluationTemplate
- FMovieSceneEvaluationTrack
- FMovieSceneEvent
- FMovieSceneEventPayloadVariable
- FMovieSceneEventPtrs
- FMovieSceneEventSectionData
- FMovieSceneEventWrapper
- FMovieSceneExpansionState
- FMovieSceneLegacyTrackInstanceTemplate
- FMovieSceneObjectBindingID
- FMovieSceneOrderedEvaluationKey
- FMovieSceneParameterSectionTemplate
- FMovieScenePossessable
- FMovieSceneRootEvaluationTemplateInstance
- FMovieSceneSectionEvalOptions
- FMovieSceneSectionParameters
- FMovieSceneSequenceCachedSignature
- FMovieSceneSequenceHierarchy
- FMovieSceneSequenceHierarchyNode
- FMovieSceneSequenceID
- FMovieSceneSequencePlaybackSettings
- FMovieSceneSequenceTransform
- FMovieSceneSkeletalAnimationParams
- FMovieSceneSkeletalAnimationSectionTemplate
- FMovieSceneSkeletalAnimationSectionTemplateParameters
- FMovieSceneSkeletalAnimation_MultipleDeviceGrade
- FMovieSceneSpawnSectionTemplate
- FMovieSceneSpawnable
- FMovieSceneSubSequenceData
- FMovieSceneSubtitleParams
- FMovieSceneSubtitleTagsKeyValue
- FMovieSceneTemplateGenerationLedger
- FMovieSceneTrackCompilationParams
- FMovieSceneTrackEvalOptions
- FMovieSceneTrackIdentifier
- FMovieSceneTrackIdentifiers
- FMovieSceneTrackLabels
- FMovieSceneTransformMask
- FMovieSceneVector2DKeyStruct
- FMovieSceneVector4KeyStruct
- FMovieSceneVectorKeyStruct
- FMovieSceneVectorKeyStructBase
- FMultiSubInstanceData
- FMyLandscapeConfigurationParams
- FNameCurve
- FNameCurveKey
- FNameMapping
- FNamedColor
- FNamedCurveValue
- FNamedEmitterMaterial
- FNamedFilmbackPreset
- FNamedFloat
- FNamedLensPreset
- FNamedNetDriver
- FNamedSlotBinding
- FNamedTransform
- FNamedVector
- FNavAgentProperties
- FNavAgentSelector
- FNavAvoidanceMask
- FNavCollisionBox
- FNavCollisionCylinder
- FNavDataConfig
- FNavGraphNode
- FNavigationFilterArea
- FNavigationFilterFlags
- FNavigationLink
- FNavigationLinkBase
- FNavigationSegmentLink
- FNetDriverDefinition
- FNetViewer
- FNewFPPPoseOffset
- FNode
- FObjectPoolConfig
- FOptionalMovieSceneBlendType
- FOrbitOptions
- FOrientedBox
- FOverlapResult
- FOverlayItem
- FOverrideBoneTranslationRetargetingModeConfig
- FOverridePhyxMaterial
- FPEBuffInfo
- FPEBuffUIInfo
- FPESkillAttributeItem
- FPESkillCDWapper
- FPESkillConsume
- FPESkillConsumeAttribute
- FPESkillConsumeItem
- FPESkillTargetData
- FPESkillUIInfo
- FPOV
- FPackedNormal
- FPackedRGB10A2N
- FPackedRGBA16N
- FPacketSimulationSettings
- FPaintedVertex
- FPairCachedBoneInfo
- FPaperFlipbookKeyFrame
- FPaperSpriteAtlasSlot
- FPaperSpriteSocket
- FPaperTerrainMaterialRule
- FPaperTileInfo
- FPaperTileMetadata
- FPaperTileSetTerrain
- FParallelWorldInfo
- FParallelWorldPlayerInfo
- FParameterGroupData
- FParticleBurst
- FParticleCurvePair
- FParticleEditorPromotionSettings
- FParticleEvent_GenerateInfo
- FParticleRandomSeedInfo
- FParticleReplayTrackKey
- FParticleSysParam
- FPassiveSoundMixModifier
- FPawnActionEvent
- FPawnActionStack
- FPerBoneInterpolation
- FPerConOwningObjectInfo
- FPhysicalAnimationData
- FPhysicalAnimationProfile
- FPhysicalSurfaceName
- FPhysicsConstraintProfileHandle
- FPlane
- FPlatformInterfaceData
- FPlatformInterfaceDelegateResult
- FPlayerMuteList
- FPluginRedirect
- FPointDamageEvent
- FPoseData
- FPoseDataContainer
- FPoseDriverTarget
- FPoseDriverTransform
- FPoseLinkBase
- FPostProcessSettings
- FPredictProjectilePathParams
- FPredictProjectilePathPointData
- FPredictProjectilePathResult
- FPreviewAssetAttachContainer
- FPreviewAttachedObjectPair
- FPreviewMeshCollectionEntry
- FPrimaryAssetId
- FPrimaryAssetRules
- FPrimaryAssetRulesOverride
- FPrimaryAssetType
- FPrimaryAssetTypeInfo
- FPrimitiveMaterialRef
- FProceduralFoliageInstance
- FProgressBarStyle
- FPropertyPathSegment
- FPurchaseInfo
- FQuat
- FRBFEntry
- FRBFParams
- FRBFTarget
- FROscillator
- FRadialDamageEvent
- FRadialDamageParams
- FRandomPlayerSequenceEntry
- FRandomStream
- FRankListAward
- FRawAnimSequenceTrack
- FRawDistribution
- FRawDistributionFloat
- FRawDistributionVector
- FRedirector
- FReferenceBoneFrame
- FReferencePose
- FReliableRPCTracker
- FRepAttachment
- FRepMovement
- FRepRootMotionMontage
- FResponseChannel
- FReverbSettings
- FRichCurve
- FRichCurveKey
- FRigConfiguration
- FRigTransformConstraint
- FRigidBodyContactInfo
- FRigidBodyErrorCorrection
- FRigidBodyErrorCorrectionNew
- FRigidBodyState
- FRollbackNetStartupActorInfo
- FRootMotionExtractionStep
- FRootMotionFinishVelocitySettings
- FRootMotionMovementParams
- FRootMotionSource
- FRootMotionSourceGroup
- FRootMotionSourceSettings
- FRootMotionSourceStatus
- FRootMotionSource_ConstantForce
- FRootMotionSource_JumpForce
- FRootMotionSource_MoveToDynamicForce
- FRootMotionSource_MoveToForce
- FRootMotionSource_RadialForce
- FRotationTrack
- FRotator
- FRuntimeCurveLinearColor
- FRuntimeFloatCurve
- FRuntimeFloatCurveHaptic
- FRuntimeMergingOverrideMaterial
- FRuntimeMergingSettings
- FRuntimeVectorCurve
- FScalabilityQuality
- FScalarMaterialInput
- FScalarParameterNameAndCurve
- FScalarParameterValue
- FScaleTrack
- FScreenMessageString
- FScriptNetworkRemoteContent
- FScrollBarStyle
- FScrollBorderStyle
- FScrollBoxStyle
- FSearchBoxStyle
- FSectionEvaluationData
- FSectionTexelDensity
- FSegmentedControlStyle
- FShapedTextOptions
- FSimSpaceSettings
- FSimpleMemberReference
- FSimpleMeshSection
- FSimpleMeshTangent
- FSimpleMeshVertex
- FSimplygonChannelCastingSettings
- FSimplygonMaterialLODSettings
- FSimplygonRemeshingSettings
- FSimulatedRootMotionReplicatedMove
- FSkelMeshComponentLODInfo
- FSkelMeshSkinWeightInfo
- FSkeletalMaterial
- FSkeletalMeshClothBuildParams
- FSkeletalMeshLODGroupSettings
- FSkeletalMeshLODInfo
- FSkeletalMeshOptimizationSettings
- FSkeletonToMeshLinkup
- FSkinDynamicElemKey
- FSkinMountInfo
- FSkinWeightInfoForFPP
- FSkippedActorTracker
- FSlateBrush
- FSlateChildSize
- FSlateColor
- FSlateFontInfo
- FSlateMeshVertex
- FSlateSound
- FSliderStyle
- FSlotAnimationTrack
- FSlotEvaluationPose
- FSmartName
- FSocketReference
- FSoftObjectPath
- FSoundAttenuationSettings
- FSoundClassAdjuster
- FSoundClassProperties
- FSoundConcurrencySettings
- FSoundGroup
- FSoundSourceBusSendInfo
- FSoundSubmixSendInfo
- FSoundTrackKey
- FSourceEffectChainEntry
- FSpinBoxStyle
- FSplineCurves
- FSplineIKCachedBoneData
- FSplineMeshParams
- FSplinePoint
- FSplitterStyle
- FSpriteCategoryInfo
- FSpriteDrawCallRecord
- FSpriteGeometryCollection
- FSpriteGeometryShape
- FSpriteInstanceData
- FStatColorMapEntry
- FStatColorMapping
- FStaticMaterial
- FStaticMeshComponentLODInfo
- FStaticMeshOptimizationSettings
- FStaticMeshPointLightVertexDataBuffer
- FStaticMeshSourceModel
- FStaticSimpleMaterial
- FStreamingSkeletalMeshPrimitiveInfo
- FStreamingStaticMeshPrimitiveInfo
- FStreamingTextureBuildInfo
- FStreamingTexturePrimitiveInfo
- FStringCurve
- FStringCurveKey
- FStructRedirect
- FStyleColorList
- FSubBoundsIncludedVertices
- FSubInstanceBlendData
- FSubTrackGroup
- FSubmixEffectDynamicsProcessorSettings
- FSubmixEffectEQBand
- FSubmixEffectReverbSettings
- FSubmixEffectSubmixEQSettings
- FSubsurfaceProfileStruct
- FSubtitleCue
- FSupportedAreaData
- FSupportedSubTrackInfo
- FSurfelRayTracingSettings
- FSwarmDebugOptions
- FTOD_Animation
- FTOD_AtmosphereParameters
- FTOD_CloudPBRParameters
- FTOD_CycleParameters
- FTOD_DayParameters
- FTOD_LightParameters
- FTOD_Moon
- FTOD_SpecialSky
- FTOD_Stars
- FTOD_Sun
- FTOD_SunAndMoon
- FTOD_Time
- FTOD_WorldParameters
- FTTEventTrack
- FTTFloatTrack
- FTTLinearColorTrack
- FTTTrackBase
- FTTVectorTrack
- FTViewTarget
- FTableColumnHeaderStyle
- FTableRowStyle
- FTableViewStyle
- FTagAndValue
- FTargetPickerFan
- FTargetPickerRectangle
- FTargetPickerSphere
- FTerrainLayer
- FTerrainLayerDesert
- FTerrainLayerHeight
- FTerrainLayerHeightBlend
- FTerrainLayerTA
- FTestFastRep
- FTestFastRep_Composite
- FTestFastRep_Custom
- FTextBlockStyle
- FTextureDensityInfo
- FTextureInfo
- FTextureLODGroup
- FTextureLODGroupFilterOverride
- FTextureParameterValue
- FTextureSource
- FTickFunction
- FTimeStretchCurve
- FTimeStretchCurveInstance
- FTimeStretchCurveMarker
- FTimeline
- FTimelineEventEntry
- FTimelineFloatTrack
- FTimelineLinearColorTrack
- FTimelineVectorTrack
- FTimerHandle
- FTireFrictionScalePair
- FToggleTrackKey
- FToolBarStyle
- FToolMenuProfile
- FTouchInputControl
- FTrackToSkeletonMap
- FTransform
- FTransformBase
- FTransformBaseConstraint
- FTranslationTrack
- FTriangleSortSettings
- FTwistConstraint
- FTwoVectors
- FTypeface
- FTypefaceEntry
- FUGCActivityTask
- FUGCCustomDamageNumberItemParams
- FUGCDamageNumberParams
- FUGCGamePartPlayerComponentConfig
- FUGCGenerateDropItemInfo
- FUGCItemSpawnerInfo
- FUGCItemSpawnerItemConfig
- FUGCItemTransferResult
- FUGCLevelTaskLineConfig
- FUGCMobBTBlackBoardInfo
- FUGCMobBTDebugInfo
- FUGCMobBTDebugTreeElemInfo
- FUGCMobBTDebugTreeInfo
- FUGCMobSpawnerMobConfig
- FUGCPercentTaskAward
- FUGCPercentTaskLineConfig
- FUGCPickupItemData
- FUGCRankingListAwardItem
- FUGCRankingListData
- FUGCSpawnActorNumLimitCfg
- FUGCTaskConfig
- FUGCTaskLineConfig
- FUserActivity
- FUserDetailSetting
- FUserRefStyleInfo
- FUserWidgetRefInfo
- FUserWidgetStyleInfo
- FVOscillator
- FVector
- FVector2D
- FVector2MaterialInput
- FVector4
- FVector4Distribution
- FVector4MaterialInput
- FVectorDistribution
- FVectorMaterialInput
- FVectorParameterNameAndCurves
- FVectorParameterValue
- FVectorRK4SpringInterpolator
- FViewTargetTransitionParams
- FVirtualBone
- FVisibilityData
- FVisibilityTrackKey
- FVolumeControlStyle
- FWSDynamicPropContext
- FWSPropContext
- FWSPropKey
- FWalkableSlopeOverride
- FWeightedBlendable
- FWeightedBlendables
- FWeightmapLayerAllocationInfo
- FWidgetAnimationBinding
- FWidgetInputAxisBindings
- FWidgetInputBinding
- FWidgetNavigationData
- FWidgetTransform
- FWindowStyle
- FWorldContext
- FWorldParallelismIDWrapper
- FWorldParallelismManager
- FWorldRegionManager
- FWorldTileExtraInfo
