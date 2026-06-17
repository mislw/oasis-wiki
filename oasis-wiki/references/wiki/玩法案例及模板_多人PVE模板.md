# 玩法案例及模板/多人PVE模板

> 本分类共 12 篇文章

---


## 概览

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 概览

# 概览

该模板是PVE类射击玩法模板，提供该类型玩法的基础结构、系统和部分模块的详细配置样例。

基于此模板可实现单人或多人PVE玩法，涵盖玩家等级属性配置、游戏流程配置、局内商店刷新、英雄制作、怪物制作、关卡副本制作、局内外物品互通等功能。

该模板包含以下系统模块：

**角色相关系统**

- 角色属性
- 元素属性
- 等级系统
- 英雄制作

**二次匹配大厅系统**

- 英雄选择系统
- 模式选择系统
- 商城
- 仓库
- 天赋系统
- 3D大厅

**战斗内系统**

- 关卡控制器
- 物品刷新
- 怪物刷新
- 怪物制作
- 战斗内商店
- 随机词条装备系统

<br>

## 游戏流程

枪火大厅中选择模式开始游戏
![17756994611407.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XAzHh17756994611407.png)

进入游戏
![_17757010098718.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RWuz5_17757010098718.png)

达成目标后进入商店购买物品或走进传送门进入下一关
![_17757011557630.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KqotF_17757011557630.png)

完成所有关卡或复活次数用光则结束比赛
![_17757019945618.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QBZsQ_17757019945618.png)

## 注意事项

1.PIE运行工程时，需要指定调试的子模式ID，默认大厅子模式ID为：1001。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bGkiNimage.png)

2.PIE调试中匹配时会有匹配失败弹窗，可以忽略，不影响正常调试

![企业微信截图_17784880299754.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VE401%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17784880299754.png)

---


## 模式配置（单人PVE模式）

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 模式配置（单人PVE模式）

# 模式配置（单人PVE模式）

目前的单人PVE模式下，单次匹配进入模式后，玩家可以逐个挑战解锁下一副本，直至结算；

同时也支持同一模式不同难度的配置和解锁

模式配置分为两大块内容：

- 该模式战斗内容的配置（包括副本，怪物，刷新道具，关底商店）,对应配置表格：Asset\Data\Table\UGCGameModeConfig.uasset
- 该模式在大厅的显示配置（显示名称，图片说明等）,对应配置表格：Asset\Data\Table\UGCGameModeDetail.uasset

<br>

## UGCGameModeConfig

这个表格是一个模式下战斗内容的汇总表，也是一个模式衔接各个模块的中枢表格。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YjQ32image.png)

参数说明：

- ModeId：模式表的唯一ID,从二次大厅选择的每个玩法模式和难度，就对应这里唯一的模式ID
- ModeName：供有需要读取关卡名称的地方读取显示
- Difficulty：难度信息读取
- LevelCount：这一模式总共包含的小副本数量，纯查看用
- UnlockDesc：模式解锁条件信息读取处

> 初始解锁关卡需在UGCPlayerState.lua文件下，修改PlayerData.GameCompletionRecord = PlayerData.GameCompletionRecord or下的Modeid，则可设定初始解锁关卡。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kICt1image.png)

- UnlockMode：通关该模式后对应可解锁的模式ID
- EnemyRefresh：刷怪方案表的ID，读取：Asset\Data\Table\DT_MonsterSpawnScheme.uasset 中的ID
- ItemRefresh：道具刷新方案表的ID，读取：Asset\Data\Table\DT_ItemSpawnScheme.uasset中的ID
- ShopAfterLevel：每个副本关底解锁的局内商店刷新方案，依次是从第一关到最后一关，ID读取的是Asset\Data\Table\UGCDropGroup.uasset中的ID
- TrapRefresh：机关方案表的ID（目前没做这方面的功能设计，未接入lua）
- SettlementExpCount：通过每一副本后获取的经验数量
- SettlementTalentCount：通过每一副本后获取的天赋点数量
- GameModeActorMgr： 模式管理器路径，通过模式管理器可管理模式内的副本通关分数，游戏总时长，结算规则，副本关卡资源及其刷新数量、顺序等几乎全部战斗内所需的逻辑配置
- FreeReviveCount：当前模式战斗内免费复活总次数
- PaidReviveCount：当前模式战斗内付费复活总次数
- Price： 
	- 0：复活使用的货币物品ID，读取：Asset\Data\Table\UGCObject.uasset中的ID
	- 1: 单次复活消耗的货币数量

<br>

## UGCGameModeDetail

模式图片表是一个模式在大厅的各个显示内容的配置，是大厅里展示模式信息所需的关键表。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PqczAimage.png)

参数说明：

- ID：模式图片表的唯一ID,从二次大厅看到的每个玩法模式，就对应这里唯一的模式ID
- ModeName：供大厅读取关卡名称的地方读取显示
- ModeDesc：模式描述信息读取处
- ModeBanner：二次大厅主页展示区域，当前模式小图读取处
- ModePost：模式选择界面，当前模式大图读取处
- ModeIDs：在这个模式展示图占位下，不同难度对应的模式ID，读取：Asset\Data\Table\UGCGameModeConfig.uasset中的ID，难度依次为：简单、困难、梦魇
- Hide ：是否隐藏本模式显示，勾选即隐藏

<br>

## 工程设置

单人闯关模式工程设置，UGCGameModeConfig表中新增模式ModeID需要在工程设置中的多模式配置处同步配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HDGz2image.png)

在多模式配置数组中添加元素，模式ID对应UGCGameModeConfig.uasset中的ModeID，如”单人闯关简单难度”ModeID为1002，此处模式ID应为1002.添加模式后，其他配置保持默认即可。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hqFGPimage.png)

> 新增多人模式配置略有区别，详情见模式配置（多人PVE模式）表

调试时修改PlayNum为1，启动单人闯关调试。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6ISKximage.png)

---


## 模式配置（多人PVE模式）

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 模式配置（多人PVE模式）

# 模式配置（多人PVE模式）

## 队伍关系的的建立改变

### 队伍关系建立流程

玩家需先在和平大厅组队进入枪火大厅完成队伍关系的建立。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hQIRDimage.png)

1. 进入枪火大厅后可进行模式/难度/是否自动匹配队友的选择。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cJjSZimage.png)

2. 需队友完成准备后，队长才可开始游戏，每次切换模式将自动重置准备状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xJ0JVimage.png)

3. 若勾选自动匹配队友，则会补充对应模式人数的队友进入战斗DS（阶段匹配功能生效除外），新增队友为临时队友，不加入枪火大厅的队伍关系。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7A4w3image.png)

4. 对局结束后返回枪火大厅，仍保留原和平大厅队伍关系。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NWVOkimage.png)

<br>

### 队伍关系规则

- 枪火多人模式的队伍关系继承于和平大厅，通过读取和平大厅的人数来确定枪火大厅的人数
- 枪火大厅内的队伍大厅关系不可改变，不允许进行离队，转让队长等操作
- 若玩家从枪火大厅退出，则提示有玩家从枪火大厅退出，需返回和平大厅重新进行匹配才可开始游戏，退出的玩家需退出队伍才可进行其他游戏，显示未退出队伍玩家状态为游戏中
- 退出玩家位于和平大厅中进行转让队长/退出队伍等队伍操作，此时队伍状态不同步到枪火大厅中，直到所有玩家退出枪火大厅再次进行本模式的匹配
- 玩家开启”自动匹配队友“功能时，进入战斗DS会自动匹配相应队友，本队伍关系仅存在战斗DS中，完成结算后依旧保留原和平大厅队伍
- 若玩家在游玩过程中强行退出，则在结算后在枪火大厅显示该玩家掉线，需重新退出至和平大厅重新匹配

<br>

## 多人模式的模式配置

枪火多人PVE模式配置与枪火单人PVE模式配置相似，玩家可在配表文件与Lua文件进行修改，以完成所需模式的配置。

同时也支持同一模式不同难度的配置和解锁。

模式配置分为两大块内容：

- 战斗内容的配置（包括副本，怪物，刷新道具，关底商店，解锁关卡，模式人数）,对应配置表格：Asset\Data\Table\UGCGameModeConfig.uasset
- 该模式在大厅的显示配置（显示名称，图片说明等）,对应配置表格：Asset\Data\Table\UGCGameModeDetail.uasset

### 战斗内容的配置

#### UGCGameModeConfig

这个表格是一个模式下战斗内容的汇总表，也是一个模式衔接各个模块的中枢表格。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2LG3Iimage.png)

参数说明：

- ModeId：模式表的唯一ID,从二次大厅选择的每个玩法模式和难度，就对应这里唯一的模式ID
- ModeName：供有需要读取关卡名称的地方读取显示
- Difficulty：难度信息读取
- LevelCount：这一模式总共包含的小副本数量，纯查看用
- UnlockDesc：模式解锁条件信息读取处
- UnlockMode：通关该模式后对应可解锁的模式ID
- EnemyRefresh：刷怪方案表的ID，读取：Asset\Data\Table\DT_MonsterSpawnScheme.uasset中的ID
- ItemRefresh：道具刷新方案表的ID，读取：Asset\Data\Table\DT_ItemSpawnScheme.uasset中的ID
- ShopAfterLevel：每个副本关底解锁的局内商店刷新方案，依次是从第一关到最后一关，ID读取的是Asset\Data\Table\UGCDropGroup.uasset中的ID
- TrapRefresh：机关方案表的ID
- SettlementExpCount：通过每一副本后获取的经验数量
- （暂未生效）SettlementTalentCount：通过每一副本后获取的天赋点数量
- GameModeActorMgr： 模式管理器路径，通过模式管理器可管理模式内的副本通关分数，游戏总时长，结算规则，副本关卡资源及其刷新数量、顺序等几乎全部战斗内所需的逻辑配置
- FreeReviveCount：当前模式战斗内免费复活总次数
- PaidReviveCount：当前模式战斗内付费复活总次数
- Price： 
	- 0：复活使用的货币物品ID，读取：Asset\Data\Table\UGCObject.uasset中的ID
	- 1: 单次复活消耗的货币数量

---

#### 工程设置

1. 多人模式需在工程设置中调整所需人数，才可进行多人模式的适配。

以“多人闯关（四人）简单”示例，打开工程设置-UGC项目-Multi-mode Game

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RhpGnimage.png)

在多模式配置中在数组中添加元素，模式ID对应UGCGameModeConfig.uasset中的ModeID，如”多人闯关（四人）简单”ModeID为1008，此处模式ID应为1008.

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Rpjw5image.png)

打开元素下MatchSetting，以”多人闯关（四人）简单”举例，队伍数量为1，小队玩家数量为4，其他建议依照默认。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hFvbKimage.png)

2. 多人模式若需在PIE（编辑器）进行调试，需在调试面板中，选择子模式调试，输入大厅ModeID（1001），并在队伍玩家的数组中选择对应的小队人数再进行调试。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/u0KRkimage.png)

---

#### 模式解锁设置

1. 解锁目标关卡功能位于UGCGameModeConfig.uasset中的UnlockDesc词条，在关卡下填写需解锁目标关卡的ModeID，完成此关卡便可以解锁目标关卡。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9HRUiimage.png)

2. 初始解锁关卡需在UGCPlayerState.lua文件下，修改PlayerData.GameCompletionRecord = PlayerData.GameCompletionRecord or下的Modeid，则可设定初始解锁关卡

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sqpoYimage.png)

<br>

### 大厅的显示配置

#### UGCGameModeDetail

添加新增关卡在大厅的显示的重要配置文件，是大厅里展示模式信息所需的关键表。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5FEx7image.png)

参数说明：

- ID：模式图片表的唯一ID,从二次大厅看到的每个玩法模式，就对应这里唯一的模式ID
- ModeName：供大厅读取关卡名称的地方读取显示
- ModeDesc：模式描述信息读取处
- ModeBanner：二次大厅主页展示区域，当前模式小图读取处
- ModePost：模式选择界面，当前模式大图读取处
- ModeIDs：在这个模式展示图占位下，不同难度对应的模式ID，读取：Asset\Data\Table\UGCGameModeConfig.uasset中的ID，根据输入顺序决定战火大厅的关卡难度选择的顺序
- Hide：是否隐藏本模式显示，勾选即隐藏

---


## 怪物刷新

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 怪物刷新

# 怪物刷新

游戏内怪物生成，核心由MonsterSpawner（单体生成器逻辑）与MonsterSpawnerManager（生成集群管理组件）协同运作，配合数据表驱动的刷新规则库实现动态调控。

<br>

## MonsterSpawner

刷怪点蓝图，关卡里的怪物从这个点刷新。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Jbzb0image.png)

- Spawner Type：刷怪类型，与DT_ItemSpawnScheme.uasset表中的刷怪类型对应，决定该刷怪点触发时刷新什么怪物
- 刷出的怪物阵营：调整怪物阵营
- 是否需要刷怪管理器：勾选此选项与刷怪管理器MonsterSpawnerManager.uasset配合控制怪物刷新时间，波次等
- 生成范围：控制怪物在刷怪点周围以输入值为半径的圆形区域内的随机一点刷新怪物
- 生成高度范围：检测刷怪点z轴方向上输入值范围内是否有地面，如果有就在地面刷新，如果没有就不刷新。控制怪物刷新在有天花板的地面时会用到，单位：厘米
- 随机朝向：勾选后生成怪物朝向随机，若要精确控制怪物朝向可通过刷怪点上的蓝色箭头控制
- 最小生成数量： 该刷怪点同一波次最小刷新的怪物数量
- 最大生成数量：该刷怪点同一波次最大刷新的怪物数量
- 刷怪间隔： 每次刷新怪物间隔时间
- 单次刷怪数量：单次刷怪只数
- 刷到地面上：勾选则直接刷到地面

<br>

## MonsterSpawnerManager

刷怪管理器蓝图，用来控制怪物刷新时间、波次。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FXZKKimage.png)

- score：击杀当前刷怪管理器控制刷新的全部怪物后，获得的分数，当此分数累计之和大于等于模式管理器SingleModeMgr中设置的通关数值时，即算作完成当前关卡
- 刷怪管理器启动方式：包括事件触发、关卡加载和手动调用三种方式，常用事件触发和关卡加载
- 事件名：当刷怪管理器启动方式选择事件触发时监听的事件名
- 刷怪波次：将关卡内刷怪点分组管理，以不同刷怪波次按数组顺序依次触发各组刷怪点
- 刷怪点：在刷怪点蓝图中勾选了是否需要刷怪管理器属性的刷怪点，就会出现在这里的下拉列表中，可将该刷怪点配置在刷怪管理器的单个或多个波次中
- 覆盖怪物刷怪类型配置：勾选后将会以下方的怪物类型配置覆盖刷怪点自带的怪物类型配置，通常勾选
- 波次开始条件：当前波次的开始条件，包括All Mob Die和Last Wave End两个选项，分别表示上一波怪物全部死亡和上一波怪物刷新完毕。
- 延迟开始时间：当满足当前波次开始条件时开始计时，在延迟时间后开始刷新这波次的怪物，单位：秒

<br>

## 怪物生成逻辑

怪物生成逻辑由DT_MonsterSpawnScheme（怪物刷新规则表）与DT_MonsterDetails（怪物属性配置表）协同驱动。

### DT_MonsterSpawnScheme

怪物刷新表，配置刷怪类型对应不同的具体怪物，是决定刷怪点具体刷新什么怪物，配置各模式具体刷怪方案的重要表格。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Bg33iimage.png)

- SchemeID: 怪物刷新表的唯一ID,UGCGameModeConfig模式配置表里的EnemyRefresh的值，就对应这里唯一的怪物刷新ID
- SpawnerType： 怪物类型，与刷怪点上配置的刷怪类型对应
- MonsterID： 怪物ID，对应DT_MonsterDetails.uasset唯一的怪物ID
- Weight：权重，表示怪物刷新组中当前怪物的刷新权重


---


## 物品刷新

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 物品刷新

# 物品刷新

游戏内物品生成系统通过双蓝图架构（ItemSpawner执行物理生成+ItemSpawnerManager动态调控）与多层数据表驱动的动态规则库协同运作，实现高效可控的自适应物品刷新机制。物品刷新机制与怪物刷新原理基本相同，但是数据表配置较怪物刷新更为复杂。

<br>

## ItemSpawner

物品刷新点，关卡内物品在这个点刷新。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8kn5Simage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QwIC2image.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nDyODimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lJunTimage.png)

- Spawner Type ：物品刷新类型，与DT_ItemSpawnScheme.uasset表中的物品类型对应，决定该刷新点触发时刷新什么怪物。
- 物资配置模式 ：物品刷新的配置模式，有四种不同的模式可配置，分别为物资ID，掉落表，掉落组表，自定义。通常选择自定义
- 物资ID ：选择物资ID配置模式时，需配置的物品ID，与物品编辑器中的物品ID对应
- 物资数量 ：选择物资ID配置模式时，需配置的物品刷新数量
- 掉落ID ：选择掉落表配置模式时，需配置的掉落ID，与掉落表UGCDrop.uasset中的掉落ID对应
- 掉落组ID ：选择掉落组表配置模式时，需配置的掉落组ID，与掉落组表UGCDropGroup.uasset中的掉落组ID对应
- 自定义ID ：选择自定义配置模式时，需配置的自定义ID，默认-1
- 是否需要管理器：勾选此选项与物品刷新管理器ItemSpawnerManager.uasset配合控制物品刷新时间，数量，间隔等。通常勾选此选项
- 是否需要循环生成 ：勾选是否需要管理器时，此选项无效，控制刷新点是否循环生成
- 刷新间隔（秒） ： 勾选是否需要管理器时，此选项无效，控制刷新点循环生成间隔时间
- 是否生成在地面上 ： 默认勾选，控制物品刷新在地面上

<br>

## ItemSpawnerManager

物品刷新管理器，与刷新点配合控制物品刷新的时间，数量，循环间隔等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Y2TbHimage.png)

- 物资刷新启动方式 ：同刷怪管理器包括关卡加载、事件触发、手动调用三种启动方式，通常选择关卡加载
- 事件名 ：物资刷新启动方式选择事件触发时监测的事件名
- 刷新点 ：勾选了是否需要管理器的刷新点会出现在这里的下拉列表中
- 覆盖刷新点物资配置 ： 勾选后以下方物资配置覆盖刷新点物资配置，通常不勾选，勾选会导致部分刷新bug
- 最大刷新间隔 ：刷新点刷新物品时最大刷新间隔
- 最小刷新间隔 ：刷新点刷新物品时最小刷新间隔
- 刷新点生效最大数量 ： 上面的刷新点中最大的生效数量，从上到下依次生效
- 刷新点生效最小数量 ： 上面的刷新点中最小的生效数量，从上到下依次生效
- 总刷新次数 ：刷新管理器中的刷新点的总刷新次数，设置为-1时为循环刷新
- 覆盖刷新点物资配置 ：同上

<br>

## 物品刷新逻辑

物品刷新逻辑由DT_ItemSpawnScheme.uasset（物品刷新表）、UGCDropGroup.uasset（掉落组表）、UGCDrop.uasset（掉落表）三张表协同驱动。

### DT_ItemSpawnScheme

物品刷新表，配置物品类型对应不同种类的具体物品，是决定刷新点具体刷新什么物品，配置各模式具体刷物品方案的重要数据表。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/X2DK0image.png)

- SchemeID : 物品刷新表的唯一ID，UGCGameModeConfig模式配置表里的ItemRefresh的值与此唯一ID对应
- SpawnerTypes：物品类型数组
- SpawnerType ：物品类型，与刷新点上配置的SpawnerType对应
- DropGroupID ：掉落组ID，与掉落组表UGCDropGroup.uasset中的唯一ID对应

---

### UGCDropGroup

掉落组表，通过不同掉落组配置不同触发条件的刷新方案，如关底商店刷新方案，丧尸掉落物方案，不同模式的物品刷新方案等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7M9aJimage.png)

- 掉落组ID ：掉落组表的唯一ID，也是当前掉落组方案的唯一标识
- 描述 ：对当前掉落组方案的描述
- 掉落类型 ：分为权重和概率两种类型，区分内含掉落方案的具体概率
- 掉落组信息：
	- 权重/概率 ：当前掉落id对应的物品组出现的概率/权重
	- 掉落ID ：与掉落表中的唯一ID对应

---

### UGCDrop

控制掉落方案的最后一节，与物品编辑器中的各物品ID对应决定实际刷新出什么物品。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eA8VWimage.png)

- 掉落ID ：掉落表的唯一ID，也是当前掉落物品组的唯一标识
- 描述 ： 对当前掉落物品组的描述信息
- 掉落类型 ：分为权重和概率，提供两种不同的随机条件
- 随机次数 ：最终决定刷新物品的刷新随机次数
- 物品信息：物品组内全部物品的物品信息
- 权重/概率 ： 当前掉落id对应的物品组出现的概率/权重
- 物品ID ： 与物资编辑器中的物品ID对应，是标识当前物品的唯一ID
- 物品数量Min ：物品刷新最小数量
- 物品数量Max ：物品刷新最大数量

---


## 战斗内商店

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 战斗内商店

# 战斗内商店

战斗内关底商店的刷新规则，由多张数据表协同控制，UGCGameModeConfig.uasset，UGCDropGroup.uasset，UGCDrop.uasset这三张表控制商品生成逻辑，UGCShop.uasset，UGCObject.uasset，UGCObjectMapping.uasset定义商品经济属性与显示交互，两组数据表通过物品ID串联形成逻辑解耦的动态刷新体系。

<br>

## UGCGameModeConfig

模式配置表，决定了战斗内每一各副本的关底商店的商品刷新方案。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EgKw7image.png)

ShopAfterLevel ：关底商店刷新方案数组，图中表示前三关的刷新方案为9000，后三关的刷新方案为9001，与UGCDropGroup.uasset掉落组表中的唯一ID对应

<br>

## UGCDropGroup

掉落组表，决定了商品刷新方案中具体刷出哪些商品组。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VagOcimage.png)

- 掉落组ID ：掉落组表的唯一ID，也是当前掉落组方案的唯一标识
- 描述 ： 当前掉落组信息的用途简述
- 掉落类型 ： 分为概率和权重两种随机规则，这里选择的是概率
- 掉落组信息 ：当前掉落组具体包含的物品组信息
- 概率/权重 ： 当前物品组刷新的概率，如果是概率的话则是万分底，这里表示有80%的概率刷新这个物品组
- 掉落ID ： 当前物品组的ID，与掉落表中的唯一ID对应

<br>

## UGCDrop

掉落表，决定物品组中具体包含哪些物品。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mkqn7image.png)

- 掉落ID ：掉落表的唯一ID，也是当前物品组的唯一标识
- 物品信息下的物品ID ： 与物品刷新规则不同，这里填写的是该物品对应的商品ID，与UGCShop.uasset中唯一的商品ID对应

<br>

## UGCShop

商品表，这张表包含了商品的各种售卖相关属性配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9OEi7image.png)

- 商品ID ： 当前商品的唯一ID
- 商品类型 ： 分为物品和货币两种商品，物品包含枪甲药等不同物品，货币如金币
- 商品名称 ： 当前商品的名称信息读取处
- 物品ID ： 当前商品的唯一物品ID，与UGCObject.uasset 虚拟物品表中的唯一ID对应
- 是否售卖 ：包含永久售卖、限时售卖、不售卖三种售卖类型
- 货币类型 ： 包含绿洲币、启元币、其他货币三种类型，设置为游戏货币时选择其他货币
- 售卖价格 ： 商品使用当前货币的出售价格
- 限购类型 ： 包括不限购，每日限购，每周限购，永久限购四种类型
- 限购数量 ： 限购出售商品的限购数量
- 上/下架时间 ： 商品的上架、下架时间
- 商城ID ： 包含战斗内和玩法详情页两个选项，通常选择战斗内
- 商品排序 ： 商品的排序方式
- 商品包含物品数量 ： 当前商品包含的物品数量，如：金币×1000
- 消耗道具ID ： 当前商品购买消耗的道具ID，与UGCObject.uasset表中的项目itemID对应
- 折扣：当前商品的折扣
- 商城页签ID ： 标识当前商品出现的大厅商城页签，0表示道具，1表示武器

<br>

## UGCObject

虚拟物品表，包含当前商品的展示信息

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aIfKfimage.png)

- 项目itemID ： UGCObject.uasset 虚拟物品表的唯一ID，在UGCObjectMapping.uasset虚拟物品映射表中通过这个ID与物资编辑器里的物品ID对应
- 物品名称 ： 商品名读取处
- 物品描述 ： 当前商品简述
- 小icon ： 当前商品的展示icon

<br>

## UGCObjectMapping

虚拟物品映射表，决定商品对应的真正物品。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zZlVPimage.png)

- 虚拟物品ItemID ：UGCObject.uasset 虚拟物品表中的项目虚拟物品ID
- 经典物品ItemID ：标识物资编辑器里的物品的唯一ID


---


## 关卡管理

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 关卡管理

**涉及API:** `Actor`, `Add`, `AllPlayer`, `Asset`, `Beginplay`, `CallReset`, `CallSettle`, `CallShop`, `InitDoor`, `LuaExecute`, `LuaExecuteWithFinish`, `OnAllMobDie`, `OnBeginOverlap`, `OnFinish`, `ReceiveBeginPlay`, `ReceiveEndPlay`, `Remove`, `SuperClass.ReceiveBeginPlay`, `UCapsuleComponent`, `UGCGameMode`

# 关卡管理

LevelFlowSystem是绿洲启元团队为了便利外部开发者快速产出需要关卡切换的玩法（如PVE玩法）而做的一套关卡流管理系统。这套系统总共有四个概念：**关卡实例**，**关卡控制器**，**关卡流管理器，UGCLevelFlowSystem**。

本wiki总共分为三个部分：背景介绍，详细配置项解释以及制作流程演示。看完背景介绍后可以先看制作流程演示，再看详细配置项解释，会更加清晰明了，详细配置项会写一些注意事项。

<br>

## 相关概念

### 关卡实例 - 子关卡

关卡实例就是子关卡，也就是我们配置的可用于动态切换的关卡。我们正常进行PIE的时候，通常只会加载主关卡，并不会加载子关卡。

---

### 关卡控制器 - UGCLevelActor

关卡控制器是用于控制关卡的切换逻辑的Actor，DS和客户端都会生成该Actor。一个关卡控制器与一个子关卡绑定，成为一个关卡元素，被关卡管理器控制。关卡控制器可以控制如下的一些逻辑：
- 当前关卡的通关分数是多少
- 当前关卡胜利后，传送到下个关卡的方式是自动传送还是传送点传送
- 当前关卡是否需要关卡结算
- 等等等等

即关卡实例，是配置关卡里面的场景，而关卡管理器用于管理关卡的运行逻辑。这样一组关卡元素，就是玩家在真正游玩时体验到的一个关卡。

---

### 关卡流管理器 - UGCLevelActorMgr

关卡流管理器是控制整局游戏（副本）的逻辑的一个管理器，仅DS生成该管理器。关卡流管理器可以控制如下的一些逻辑：
- 一局游戏里有几个关卡
- 关卡更换的顺序是什么
- 这局游戏的通关条件是什么
- 这局游戏的总时长是多久
- 等等等等

---

### UGCLevelFlowSystem

UGCLevelFlowSystem是一个Lua API库，我们将不便在蓝图中配置的以及更灵活的一些处理逻辑整合到了这里。里面有如下方法：
- `EnableLevelFlow(string InMgrPath)` 启用关卡流程
- `bool GoToNextLevelForAllPlayers()` 当前关卡所有玩家直接跳转到下个关卡
- `bool GoToNextLevelForOnePlayer(ASTExtraPlayerController PlayerController)` 单个玩家直接跳转到下个关卡
- `LevelAddScore(int32 TeamID, int32 Score)` 给指定队伍关卡加分
- `LevelSettle(int32 TeamID, bool IsFinish)` 队伍所在关卡立即结算
- `int32 GetCurrentLevelStage(ASTExtraPlayerController PlayerController)` 获取当前玩家处于第几关
- `int GetTotalLevelCount()` 获取总关卡数
- `GameAddScore(int32 TeamID, int32 Score)` 给指定队伍游戏加分
- `GameSettle(bool IsFinish)` 游戏立即结算
- `GetAllPlayerControllerInCurrentLevel()` 获取关卡里的所有玩家
- `UGCLevelActorGetCurrentLevelActor()` 获取当前副本

<br>

## 关卡流系统驱动游戏运行的流程

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9sskiimage.png)

<br>

## 关卡控制器

共有10个配置项

**关卡通关分数**

这一项是用于统计当前关卡的胜利条件。如果当前关卡得分超过关卡通关分数，则进入重置数据 - 关底奖励 - 关卡结算 - 跳转关卡的流程。
    
**关卡传送类型**

这里可以选两种选项：**传送点传送** 和 **自动传送**

- 传送点传送：达到通关分数后，有teleport的ActorTag的传送点会显示出来。并需要在传送点的碰撞检测盒中调用 `UGCLevelFlowSystem.GoToNextLevelForOnePlayer` ，跳转到下一个关卡的出生点
- 自动传送：达到通关分数后，自动跳转到下一个关卡的出生点
  
**关卡通关得分条件蓝图配置**

该配置项有待优化，我们已将功能嵌入到UGCLevelFlowSystem中

**关卡通关分数统计类型**

这里可以选两种选项：**队伍分数结算** 和 **全部队伍分数结算**，由于目前不支持多个队伍在同一局游戏中竞争，所以目前默认都选择队伍分数结算。
  
**是否需要关底奖励**

**关底奖励**与**关卡结算**相似，是在跳转到下个关卡前插入两个时间点，默认是进行**关底奖励**和**关卡结算**的逻辑处理。实际上开发者可以根据自己的需求在这里插入自己的逻辑，不一定是进行**关底奖励**和**关卡结算**。

> 勾选了这个选项后，必须要配置相应的蓝图，否则会一直卡在当前阶段无法进入后面的流程

关底奖励配置需要创建关底奖励蓝图 `UGCLevelReward`，如下图所示

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BEKXFimage.png)

蓝图里没有需要配置的选项，具体逻辑需要在lua中编写。当关卡到达通关分数后，则会检索是否有关底奖励蓝图配置，如果有，则会调用里面的 `LuaExecute` 函数。如下面代码所示，我们在 `LuaExecute` 函数中自定义逻辑，当我们认为关底奖励的内容执行完后，调用 `UGCLevelReward:OnFinish()` ，即可进行下一步操作，否则会被一直阻断在**关底奖励**这一阶段。

```lua
-- UGCLevelReward.lua

local UGCLevelReward = {}

function UGCLevelReward:LuaExecute()
	-- 获取当前关卡内的所有玩家
   	 local AllPlayer = UGCLevelFlowSystem.GetAllPlayerControllerInCurrentLevel()
    
	-- 每个玩家进行关底商店
	if AllPlayer and #AllPlayer > 0 then
		for k, v in pairs(AllPlayer) do
			v:CallShop()
		end
	else
		print("UGCLevelReward:LuaExecute AllPlayer is nil")
	end
	
	-- 关底奖励完成，进入结算
	self:OnFinish()
end

return UGCLevelReward
```

**是否需要关卡结算**

> 勾选了这个选项后，必须要配置相应的蓝图，否则会一直卡在当前阶段无法进入后面的流程。

首先需要创建结算蓝图 `UGCSettlement`

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MkUBIimage.png)

与关底奖励相似，在Lua中编写逻辑，唯一不同的是 `LuaExecute` 变成了 `LuaExecuteWithFinish`，且函数里传入了两个参数，第一个为无用参数，第二个参数为

```lua
-- UGCSettlement.lua

local UGCSettlement = {}

function UGCSettlement:LuaExecuteWithFinish(_, IsFinish)
	-- 获取当前关卡内的所有玩家
   	 local AllPlayer = UGCLevelFlowSystem.GetAllPlayerControllerInCurrentLevel()
    
	-- 每个玩家进行结算
	if AllPlayer and #AllPlayer > 0 then
		for k, v in pairs(AllPlayer) do
			v:CallSettle()
		end
	else
		print("UGCSettlement:LuaExecuteWithFinish AllPlayer is nil")
	end
	
	-- 关底结算完成，跳转到下个关卡
	self:OnFinish()
end

return UGCSettlement
```

**离开关卡是否需要重置数据**

> 勾选了这个选项后，必须要配置相应的蓝图，否则会一直卡在当前阶段无法进入后面的流程

首先需要创建重置蓝图 `UGCResetData`

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8XWpqimage.png)

与关卡奖励和关卡结算相似，在跳转关卡前提供一个不阻断的时间点，重置关卡数据。开发者可以在这里编写自己的逻辑，重置不能带出关卡的一些数据。

```lua
-- UGCResetData.lua

local UGCResetData = {}

function UGCResetData:LuaExecute()
	-- 获取当前关卡内的所有玩家
   	 local AllPlayer = UGCLevelFlowSystem.GetAllPlayerControllerInCurrentLevel()
    
	-- 每个玩家进行重置数据
	if AllPlayer and #AllPlayer > 0 then
		for k, v in pairs(AllPlayer) do
			v:CallReset()
		end
	else
		print("UGCSettlement:LuaExecuteWithFinish AllPlayer is nil")
	end
end

return UGCResetData
```

**小地图配置**  

小地图配置项是提供一个位置保存不同关卡的小地图，从而在更换关卡的时候，可以读取关卡的小地图配置进行更换。  
  
**关卡实例列表**

这里默认只有一个元素，这个元素里填写子关卡的名字，实现子关卡与关卡控制器的绑定

<br>

## 关卡管理器 -UGCLevelActorMgr

共有8个配置项:

**GameModeActor蓝图路径**

在管理器中加入需要的关卡控制器，路径填写以Asset开始的路径，例如：`Asset/Blueprint/GameModeActor/SingleMode/SingleMode_1/SingleMode_1_Actor.SingleMode_1_Actor_C`
这个配置项的前面还有对应控制器的序号，用于后面副本顺序的填写
  
  
**是否副本创建位置固定**

- 不固定：副本会在随机位置创建
- 固定：副本会在固定位置创建

建议选择固定，并设置所有副本位置为0，这样可以保证子关卡的坐标与在持久化关卡中显示的坐标相同，配置参考如下：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Uukpnimage.png)
	  
**副本通关分数**

与关卡通关分数相似，如果当前副本得分超过副本通关分数，则进入副本胜利结算的流程
  
**副本切换模式**

副本切换模式有三种： 固定切换，随机切换以及自定义切换

- 固定切换：逐一填入每个关卡的序号（同一关卡可重复填入），该序号为**GameModeActor蓝图路径**配置项中填写的关卡控制器序号
- 随机切换：填写需要生成的副本数，每一关都会在**GameModeActor蓝图路径**配置项中选取一个，且可以设置最后副本的index
- 自定义切换：暂时不支持
	
**副本通关得分条件蓝图配置**

该配置项有待优化，我们已将功能嵌入到UGCLevelFlowSystem中

**是否有PVE游戏总时长**

可以设置单局游戏时长限制，如果超时，则会走 超时处理 - 失败结算处理 逻辑。同时可以设置游戏超时处理蓝图，在蓝图中执行我们想要的超时处理逻辑。

> 勾选了这个选项后，必须要配置相应的蓝图，否则会报错

首先创建超时处理蓝图 UGCTimeOut

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BtLx7image.png)

接着在对应lua中的LuaExecute函数里编写超时处理逻辑，当游戏触发超时时，会自动调用该lua的LuaExecute方法

```lua
-- UGCTimeOut.lua

local UGCTimeOut = {}

function UGCTimeOut:LuaExecute()
    -- 获取当前游戏内的所有玩家
    local AllPlayer = UGCLevelFlowSystem.GetAllPlayerControllerInCurrentLevel()

    if AllPlayer and #AllPlayer > 0 then
        for k, Player in pairs(AllPlayer) do
            -- 如果超时，逐个玩家调用失败结算，设置下面变量后会自动弹出超时失败结算界面
            if not Player.SettleParams.bIsSettled then
                Player.SettleParams.bIsSettled = true
                Player.SettleParams.bIsFinished = false
                DOREPONCE(Player, "SettleParams")
            end
        end
    else
        print("UGCTimeOut:LuaExecute AllPlayer is nil")
    end

end

return UGCTimeOut
```

**游戏结算类型**

首先创建游戏结算蓝图 UGCSettlement

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hIXf1image.png)

接着在结算蓝图中编写逻辑：

```lua
-- UGCSettlement.lua

local UGCSettlement = {}

function UGCSettlement:LuaExecuteWithFinish(_, IsFinish)

    -- 获取当前游戏内的所有玩家
    local AllPlayer = UGCLevelFlowSystem.GetAllPlayerControllerInCurrentLevel()
    if AllPlayer and #AllPlayer > 0 then
        for k, Player in pairs(AllPlayer) do
            
            -- 在玩家结算的时候更新游戏时间
            Player.PlayerState:UpdateGameTime()

            -- 通知玩家调出结算UI
            Player.SettleParams.bIsSettled = true
            Player.SettleParams.bIsFinished = true
            DOREPONCE(Player, "SettleParams")
        end
    else
        print("UGCSettlement:LuaExecuteWithFinish AllPlayer is nil")
    end

end

return UGCSettlement
```

**NumPlayersPerInstanceForPIE**

请默认设置一个较大的数字，否则死亡后玩家会无法复活。（必选）

<br>

## 制作流程演示

1. 首先创建工程，然后新增子关卡，并补充关卡内容：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pggOlimage.png)

2. 创建关卡控制器LevelActor，关卡管理器LevelActorMgr，并填充内容

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZNa9rimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7EiMBimage.png)

3. 在一个时序比较早的地方启用关卡流程（Lua），例如在 `UGCGameMode` 的 `Beginplay` 中

```lua
-- UGCGameMode.lua

local UGCGameMode = {}

function UGCGameMode:ReceiveBeginPlay()

	-- 启用关卡流程
	local MgrPath = "Asset/Blueprint/GameModeActor/SingleMode/SingleModeMgr.SingleModeMgr_C"
	UGCLevelFlowSystem.EnableLevelFlow(UGCGameSystem.GetUGCResourcesFullPath(MgrPath))
end

return UGCGameMode;
```

4. 加入加分逻辑。例如：杀怪加分，当触发到所有怪物死亡事件（自定义事件，自定义触发）时，调用 `UGCLevelFlowSystem.LevelAddScore` 进行关卡加分

```lua
-- MonsterSpawnerManager.lua

local MonsterSpawnerManager = {}

function MonsterSpawnerManager:OnAllMobDie()
    local PlayerControllers = UGCGameSystem.GetAllPlayerController(true)
        for k, v in pairs(PlayerControllers) do
            local TeamID = v.TeamID
            local Score = self.Score
            UGCLevelFlowSystem.LevelAddScore(TeamID, Score)
        end
end

return MonsterSpawnerManager
```

5. 加入跳转逻辑。例如：与传送门重叠后调用 `UGCLevelFlowSystem.GoToNextLevelForOnePlayer` 使该玩家跳转

```lua
-- PortalDoor.lua

---@field Trigger UCapsuleComponent
local PortalDoor = { };

function PortalDoor:ReceiveBeginPlay()

    PortalDoor.SuperClass.ReceiveBeginPlay(self)
    if UGCGameSystem.IsServer() then 
        self:InitDoor()
    end

end

function PortalDoor:InitDoor()
    self.Trigger.OnComponentBeginOverlap:Add(self.OnBeginOverlap, self)
end

function PortalDoor:ReceiveEndPlay()
    print(string.format("[PortalDoor:ReceiveEndPlay]"))
    self.Trigger.OnComponentBeginOverlap:Remove(self.OnBeginOverlap, self)
end

function PortalDoor:OnBeginOverlap(OverlappedComp, Actor, OtherComp, OtherBodyIndex, bFromSweep, SweepResult)

    -- 当玩家的Pawn和传送门折叠后，触发传送玩家
    UGCLevelFlowSystem.GoToNextLevelForOnePlayer(UGCGameSystem.GetPlayerControllerByPlayerKey(Actor.PlayerKey))
    
end

return PortalDoor
```

6. 启动PIE调试验证关卡流程效果

---


## 游戏大厅系统

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 游戏大厅系统

# 游戏大厅系统

游戏大厅作为玩家主界面，整合英雄选择、模式选择、商城、仓库、天赋系统、玩家信息以及3D大厅展示功能模块，提供游戏的核心功能入口。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vAGzhimage.png)

<br>

## 英雄选择系统

提供英雄列表展示、解锁验证及角色选择功能，支持技能详情查阅与背景故事展示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4EOwGimage.png)

<br>

## 模式选择系统

配置多模式入口与难度梯度规则，支持难度选择动态切换，自定义难度解锁逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MCOXnimage.png)

<br>

## 商城系统

自定义商品内容，实现商品分类展示（道具/武器），包含购买数量调节、异常提示及背包同步机制。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ekmPWimage.png)

<br>

## 仓库系统

管理仓库与背包的物品流转，支持转移、销毁、代币存取及战斗携带物品持久化规则。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CSlK7image.png)

<br>

## 天赋系统

构建通用与英雄专属双天赋体系，提供加点逻辑、层级解锁、异常提示及英雄天赋重置功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/F7Cagimage.png)

### 天赋类配置表

路径：Asset\Data\Table\TalentTree\UGCTalentCategory

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ygKDKimage.png)

|属性名|属性说明|
|-|-|
|ID|序列号，无需关注，没有重复即可，默认的天赋类别上下顺序是按照ID从小到大的|
|Name|该类别的名称|
|IsGeneral|用于区分该类别是否为通用类别，即对所有英雄都生效|
|HeroID|仅仅在上面的IsGeneral配置为false时才生效，用于配置该类别对那个英雄生效<br>比如：3类别的天赋，升级后只有玩家在使用101英雄进入游戏时才生效|
|CanReset|是否支持该类别的天赋树重置，重置后会清除所有升级的天赋然后返还所有消耗的天赋点|
|LimitType|用于配置每层与下一层的解锁方式，目前只支持了在上一层消耗多少天赋点才会解锁到下一层|
|Description|用于填写每层的描述，每存在一层就需要配置描述，否则会显示为空|
|UnlockDescription|用于填写每层的解锁描述，每存在一层就需要配置描述（第一层可以不填，除非需要解锁），否则会显示为空|

---

### 天赋树配置表

路径：Asset\Data\Table\TalentTree\UGCTalent

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/x4aBqimage.png)

|属性名|属性说明|
|-|-|
|ID|序列号，无需关注，没有重复即可|
|Name|填写该天赋的名称|
|Desc|配置打开后的天赋描述|
|CategoryID|用于配置该天赋属于哪一个类别，比如配置为1，则分配在 天赋类别-攻击 里面显示|
|MaxLevel|该天赋书的最高等级，目前默认为1等级消耗1个天赋点|
|LimitParameter|用于配置该天赋的解锁需求。程序在读取该列时会按照该类别一共有多少种限制分成N层（N为多少种限制，比如111到124都是类别1但只有两种就会生成2层）。每个天赋会根据排序分配在对应层级里面|
|Skills|用于配置获得技能。这里是一个组，每一组对应一等级，不要超过配置的等级|
|Buffs|用于配置获得buff。这里是一个组，每一组对应一等级，不要超过配置的等级|
|Attributes|用于配置获得属性修改。这里是一个组，每一组对应一等级，不要超过配置的等级|
|SortPriority|排序权重，用于配置该天赋在这一层的先后顺序|
|Icon|用于配置该天赋在天赋页面中的图标显示。升级到满级之后会自动高亮，所以图标的产出需要参考目前已有的|

---

### 天赋点获取

每升一等级获得配置的天赋点数，可参考角色 [等级系统](https://developer.gp.qq.com/wikieditor/#/catalog/20198?autoJump=%E7%AD%89%E7%BA%A7%E7%B3%BB%E7%BB%9F) 的配置说明。

<br>

## 玩家信息展示

集成基础数据（等级/头像/性别等）面板与自定义游戏币展示，实时更新核心统计信息（如经验条、等级提升）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fEBvHimage.png)

<br>

## 3D大厅系统

整合功能入口，触发待机动作等次要功能，常驻核心信息于屏幕边缘显示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/r0ZXjimage.png)

### 建立场景关卡

1.打开窗口中的"子关卡"

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7bdxpimage.png)

2. 确认玩法主关卡路径：'UGCmap.UGCmap'

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BUHO9image.png)

3. 建立大厅场景子关卡路径：'Asset/Maps/Lobby.Lobby'（右键后选择"关卡"即可创建新的子关卡）

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uW86gimage.png)

4. 加载主关卡，左键点击子关卡将其拖入关卡窗口中的主关卡附属下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZVgw3image.png)

5. 将子关卡加载方式改为蓝图

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RrkEBimage.png)

6. 双击子关卡（出现蓝色字符为正确，意为后续添加的所有actor都归类与该关卡）

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BHI5iimage.png)

---

### 角色Pawn位置校准

单人角色坐标：(X=5879.791992,Y=3046.190674,Z=1328.808350)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tpNI8image.png)

---

### 配置大厅相机Pawn

1. 创建pawn添加相机

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5nBIaimage.png)

2. 相机pawn蓝图路径：'/Asset/Maps/Lobby/Blueprint/Lobby_Camerapawn.Lobby_Camerapawn'

3. 将相机pawn拖入场景中，调试好坐标参数，当前大厅相机坐标参数为：

位置：(X=6109.808594,Y=3138.059570,Z=1417.380859)
旋转：(Pitch=1.730237,Yaw=-158.344101,Roll=0.000002)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tMsKYimage.png)

4. 为了防止不同设备分辨率下出现黑边，需要关闭相机的（约束宽高比）选项

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MylnUimage.png)

---

### 场景物件Mesh制作与摆放

1. 模型资产可以选择自制3D模型或引用项目其他现成模型
2. 模型资产路径：StaticMesh'/Asset/Maps/Lobby/Mesh/UGC_Lobby031_01.UGC_Lobby031_01'
3. 模型材质路径：MaterialInstanceConstant'/Asset/Maps/Lobby/Material/M_UGC_Lobby031_01.M_UGC_Lobby031_01'
4. 模型贴图路径：Texture2D'/Asset/Maps/Lobby/Texture/T_UGC_Lobby031_03D.T_UGC_Lobby031_03D'
5. 将模型在关卡中进行搭建

---

### 灯光组件调整

1. 根据场景模型表现需求布置打灯

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jaZVzimage.png)

2. 场景灯光属性设置为静态

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8TrKIimage.png)

3. 角色灯光由平行光和天光组件共同照明，平行光有灯光通道可调节，天光则无（平行光属性需要开可移动）

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YCvVPimage.png)

4. 因为引擎的灯光逻辑问题，光照通道智能识别单一的最高优先级的通道，所以场景内的所有角色和物件网格都需要把灯光通道统一改成通道0

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kHiV0image.png)

---

### 端手效果同步

1. 由于端游和手游对于性能调用逻辑不同，需要为手游效果同步新增一些配置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZbrBbimage.png)

2. 新增一个天空盒关卡（需要和开发沟通）将大厅的天空盒复制进来

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TmOh6image.png)

3. 将复制的天空盒组件内的平行光关闭

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5obePimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gcbQzimage.png)







---


## 角色系统

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 角色系统

# 角色系统

RPG射击模板支持市面上常见的RPG类型的角色制作，通过此文档可以了解在RPG射击模板中角色制作的关键系统，包括角色属性、元素系统、等级系统和英雄制作。

- 角色属性：详细列出了各种属性集及其配置方法，如魔法值、防御穿透比例、暴击几率等，并提供了伤害计算公式和技能冷却公式
- 元素系统：主要演示了火元素属性的触发效果和伤害计算方式
- 等级系统：说明了经验获取和等级提升的配置方法
- 英雄制作：介绍了英雄的美术资源和能力制作，包括3D模型、头像、技能设计和属性修改等配置方法

<br>

## 角色属性

### 属性集

目前已支持属性编辑器功能。所有的属性初始值、默认值等配置可以在属性编辑器中进行配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bfxUPimage.png)

---

### 伤害计算公式

由于不同rpg的实际需求，每个rpg模式中针对伤害的计算方式也是不同。本模板同样支持公式修改和替换。

伤害的公式修改lua地址：Script\Blueprint\Attributes\UGCGlobalDamageCalculation.lua
伤害公式中，对于HasTag的判断，是会判断伤害来源是否带有相关tag。tag的增加在UGCGameplayTags.ini，需要进行修改的话在 编辑-工程设置 中如图操作

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FdX3simage.png)

技能冷却百分比lua地址：Script\Blueprint\Attributes\UGCDerivedAttributes.lua
 
这里针对模板中的公式进行展示：

**玩家对怪物造成的技能伤害**

实际造成伤害=技能面板伤害*(1+攻击力加成1+攻击力加成2)*(1+伤害加成1+伤害加成2....)*(1-被命中者防御带来的减伤)*(1+命中者暴击伤害加成)*(1-被命中者暴击伤害抗性)*(1-被命中者火属性减伤)*(1+命中者火属性伤害加成)

**玩家对怪物造成的武器伤害**

实际造成伤害=枪械面板伤害*(1+攻击力加成1+攻击力加成2)*(1+伤害加成1+伤害加成2....)*(1-被命中者防御带来的减伤)*(1+命中者暴击伤害加成)*(1-被命中者暴击伤害抗性)*(1+命中者弱点伤害加成)*(1-被命中者暴击伤害抗性)*(1-被命中者火属性减伤)*(1+命中者火属性伤害加成)

若此次攻击不带火元素属性或者没有暴击，没命中弱点，则对应的乘区不存在。

**防御公式**

防御减伤=(基础防御力+装备提供防御力)*(1+防御力加成1+防御力加成2....)*(1-攻击方的防御力穿透)/((基础防御力+装备提供防御力)*(1+防御力加成1+防御力加成2....)+K*自身等级+C) (在本模板中，该公式内的K设置为0，c为100，即 技能冷却时间减少百分比=10/技能冷却+10 )

实际的防御减伤为： (基础防御力+装备提供防御力)*(1+防御力加成1+防御力加成2....)*(1-防御力穿透)/((基础防御力+装备提供防御力)*(1+防御力加成1+防御力加成2....)+100)

> 基础防御为10，装备防御为50，防御总加成为35%，攻击方防御力穿透为10%。受到伤害时的减伤为： 60*（1+0.35）*（1-0.1）/(60*（1+0.35）+100)=0.402762431

**吸血公式**

吸血量=实际造成的伤害 * 吸血倍率(1 +治疗加成1+治疗加成2…..))

**反伤公式**

反伤伤害=即将收到的伤害 * 反伤比例 * (1+伤害加成1+伤害加成2.....)

**技能冷却**

技能冷却时间减少百分比=(K*lv+c)/(技能冷却+K*lv+c) (在本模板中，该公式内的K设置为0，c为100，即 技能冷却时间减少百分比=100/(技能冷却+100) )
实际技能的冷却时间为： T*技能冷却时间减少百分比 (T为技能的初始冷却时间)

> 技能冷却当前为300，技能冷却时间为12秒，则技能冷却时间减少百分比=100/（100+300）=0.25 ，则该技能在战斗中的冷却时间为3秒

<br>

## 元素系统

### 元素触发效果

作为功能演示的元素属性系统只制作了火元素属性。

整体功能需求：
- 枪械每次命中叠加一定层数（每种枪械不同），叠加层数后重置持续时间。
- 当层数达到一定层数之后，触发额外的效果（不同的元素配置不同效果，火元素定为百分比减少目标防御值），持续期间内不可再叠加层数，持续时间结束之后需要重新叠加层数来触发。

配置方法：

1. 先制作一个被动技能，配置效果为造成伤害后叠加buff。 模板中名称为：FireElement、FireElement_DMR（针对射手步枪的，增加了每枪命中获得的层数）、FireElement_shotgun（针对霰弹枪的）

使用tag的方式来限制该被动技能的伤害触发是由 枪械+火焰 来触发。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dcsSAimage.png)

2. 创建两个buff FireElementCount（用于火元素命中计数，计数达到后触发FireEffect） FireEffect（用于配置火元素的效果和持续时间）

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2as6Eimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/inpM0image.png)

3. 使得被动技能在命中敌人时能给敌人挂接 FireElementCount buff层数。即完成配置。

对于需要挂接火元素被动的枪械，在物品编辑器中将被动技能挂接在物品上即完成配置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EIpYVimage.png)

### 元素伤害

目前对元素伤害的计算，则使用伤害tag的方式进行配置。

在枪械配置编辑器中，以tag的方式添加到伤害配置里面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LqhYkimage.png)

<br>

## 等级系统

等级系统的经验由每局游戏配置，完成后获取经验。根据经验提升玩家等级，根据玩家等级修改玩家属性或者向玩家发放奖励。

路径：Asset\Data\Level

UGCLevelConfig 是等级的详细配置，用于配置每级升级到下一级需要的经验量，每级获得的技能，被动技能，属性修改，天赋点数获取等等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sJjutimage.png)

UGCLevelGlobal 用于配置每级的生命成长，防御成长，蓝量成长（用于减轻配置工作量）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gnkwdimage.png)

<br>

## 英雄制作

### 英雄的美术资源

先说明英雄基础资源，即3d模型和头像。其中英雄选择页面使用的是角色3d模型。天赋树这里由于时间问题，目前采取了2d图片显示。

**3D模型**

英雄选择：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/a4bpzimage.png)

配置在：Asset\Data\Table\Hero\UGCHero

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uURQ0image.png)

UGC资源库提供了17个模型用于使用，如果需要自行添加，需要满足骨骼需求。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VK0nzimage.png)

**2D图片**

天赋树：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5AK76image.png)

其中全身资源比例为：880 * 2048，保证比例即可，会自动拉大。
头像资源比例为：423 * 588，保证比例即可，会自动拉大。

配置在：Asset\Data\Table\Hero\UGCHero

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/92wIaimage.png)

---

### 英雄技能

英雄的制作，除开美术面的形象外，在游戏中涉及到技能设计，初始拥有的buff，属性修改等等。

以上都可以在Asset\Data\Table\Hero\UGCHero.uasset 中进行配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/10vEtimage.png)





---


## 天赋系统

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 天赋系统

# 天赋系统

主要用于提供玩家在局外自由养成自己的角色。
关键配置由两张表进行配置：

## UGCTalentCategory

天赋类配置表

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/98BEcimage.png)

- ID：序列号，无需关注，没有重复即可，默认的天赋类别上下顺序是按照ID从小到大的。
- Name：该类别的名称
- IsGeneral：用于区分该类别是否为通用类别，即对所有英雄都生效。
- HeroID：仅仅在上面的IsGeneral配置为false时才生效，用于配置该类别对那个英雄生效。比如：3类别的天赋，升级后只有玩家在使用101英雄进入游戏时才生效。
- CanReset：是否支持该类别的天赋树重置，重置后会清除所有升级的天赋然后返还所有消耗的天赋点。
- LimitType：用于配置每层与下一层的解锁方式，目前只支持了在上一层消耗多少天赋点才会解锁到下一层。
- Description：用于填写每层的描述，每存在一层就需要配置描述，否则会显示为空。
- UnlockDescription：用于填写每层的解锁描述，每存在一层就需要配置描述（第一层可以不填，除非需要解锁），否则会显示为空。

## UGCTalent

天赋树配置表

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/M4Xn2image.png)

- ID：序列号，无需关注，没有重复即可。
- Name：填写该天赋的名称。
- Desc：配置打开后的天赋描述。
- CategoryID：用于配置该天赋属于哪一个类别，比如配置为1，则分配在 天赋类别-攻击 里面显示
- MaxLevel：该天赋书的最高等级，目前默认为1等级消耗1个天赋点。
- LimitParameter：用于配置该天赋的解锁需求。程序在读取该列时会按照该类别一共有多少种限制分成N层（N为多少种限制，比如111到124都是类别1但只有两种就会生成2层）。每个天赋会根据排序分配在对应层级里面。
- Skills：用于配置获得技能。这里是一个组，每一组对应一等级，不要超过配置的等级。
- Buffs：用于配置获得buff。这里是一个组，每一组对应一等级，不要超过配置的等级。
- Attributes：用于配置获得属性修改。这里是一个组，每一组对应一等级，不要超过配置的等级。
- SortPriority：排序权重，用于配置该天赋在这一层的先后顺序。
- Icon：用于配置该天赋在天赋页面中的图标显示。升级到满级之后会自动高亮，所以图标的产出需要参考目前已有的。

## UGCLevelConfig

人物等级经验对照表中可以设置每级获取的天赋点：TalentPoints

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yhFZQimage.png)






---


## 装备随机词条

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 装备随机词条

**涉及API:** `UGCAffixDetails`, `UGCEquippmentRandomAffix`, `UGCItemMapAffixId`

# 装备随机词条

## 功能概述

可以在任意物品上设置随机品质的固定词条数，且每个品质存在最高限制和最低限制的词条随机方式。
>比如一个紫色物品，产出4个词条，需要限制最差能出1个紫色词条，1个蓝色词条，2个白色词条(不会产出1紫3白)，最好能产出3个紫色词条和1个蓝色词条

## 配置方式

### 词条属性表

在``UGCAffixDetails``中配置所有会进行随机的词条

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/V4vxoimage.png)

- ID：序列号，无需关注，没有重复即可。
- MutexExclusion：互驳类型，支持中文。后文随机配置的时候会说明该功能。这里只需要保证在使用了相同属性时这里配置一样的就行了。
- IsPassiveSkill：用于判断是属性修改，还是被动技能
- AffixesLevel：用于配置该词条的品质等级。同时会影响词条在显示时的颜色。
- TargetAttrType：只有在非被动技能，即为属性修改时生效。用于配置是对那个属性的修改。
- Description：该词条的描述，会在词条显示的时候使用该描述。
- RandomModifier：只有在非被动技能，即为属性修改时生效。用于配置该词条的数值随机上下限。（如果装备最终出现未随机到词条，很有可能是这里上下弄反导致的）
- SkillId：用于配置该词条在获得后玩家会获得的技能。玩家只会获得该组内的1个技能。
- DecimalPlaces：需要显示多少小数点（针对原始数据，不受百分比选择的影响。即如果为4，则换成百分比就是XX.XX%）
- DisplayPercentage：是否按照百分比的方式显示

### 词条随机表

在``UGCEquippmentRandomAffix``配置随机词条组

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pGrrHimage.png)

- RandomModifier：配置该随机词条组需要随机多少个词条
- RandomAffixes：随机词条的配置，这里采取的配置方式是嵌套数组。
- IsRepeat：即随机过程中是否允许重复属性的随机，即假如随机到了橙色词条的攻击力加成，则后续不再出现紫蓝绿白等其他品质的攻击力词条。
- EquipSlot：用于后续判断该随机用于装备还是配件（暂时无用）

直接已目前已配置完成的随机词条组103为例进行介绍：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NoJs0image.png)

RandomAffixes中存在4个数组，随机顺序为从上往下按顺序进行随机，0随机完了到1，然后到2最终到3。在103中，0代表紫色品质的词条随机，1代表蓝色品质的词条随机，2代表绿色品质的词条随机，3代表白色的词条随机。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/90211image.png)

在数组0中，AffixIds为配置该数组内会进行随机的词条，NumberRange为随机的词条数，可以填写上下限

如果该随机词条组IsRepeat为false，则在0中随机到的词条，后续在1中就不随机到相同 互驳类型 的词条。

>假设随机到的数量为1，随机到的词条为1014。因为1013,1012,1011与1014在 词条属性表-MutexExclusion 中配置的是相同互驳类型。后续在其他数组中就不会再随机到1013.1012.1011 词条。从而实现了假如随机到了橙色词条的攻击力加成，则后续不再出现紫蓝绿白等其他品质的攻击力词条。

### 词条随机组与装备挂联表

在``UGCItemMapAffixId``中配置装备使用那个随机词条组。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0ZDVdimage.png)



---


## 怪物配置

> 文档路径: 玩法案例及模板 > 多人PVE模板 > 怪物配置

# 怪物配置

### DT_MonsterDetails

怪物表，这个表包含各个怪物的详细属性配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AOcKFimage.png)

- MonsterID：怪物数据表的唯一ID，也是标识当前怪物的唯一ID
- MonsterName： 当前怪物名称信息读取处
- MonsterClass：当前怪物对应的蓝图路径
- MonsterType：怪物类型区分，包括Monster普通怪物、EliteMonster精英怪、Boss
- Level：怪物等级信息读取处
- KillExp：击杀怪物获取的经验值
- DropGroupID： 掉落物的掉落组ID，对应UGCDropGroup表中的掉落组ID
- Health：怪物最大生命值
- Defence： 怪物防御
- CritDamageResist：怪物暴击伤害减免
- HeadDamageResist：怪物弱点伤害减免
- FireDamageResist：怪物火元素伤害减免
- CounterAttackRatio：怪物反伤倍率
- HealthStealRatio：怪物吸血倍率
- DropGroupID_wrapper：掉落组ID
- DropGroupID_Backpack：背包掉落组ID

### UGCDropGroup

掉落组表，对应上面的DropGroupID

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dhG7Uimage.png)

### UGCDrop

掉落表，对应上面的掉落表ID

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CIVdaimage.png)

---
