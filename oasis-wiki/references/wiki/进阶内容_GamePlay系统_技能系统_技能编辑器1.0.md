# 进阶内容/GamePlay系统/技能系统/技能编辑器1.0

> 本分类共 5 篇文章

---


## 快速入门

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器1.0 > 快速入门

**涉及API:** `GameState`, `GetSkillManagerComponent`, `SkillArchetypes`, `SkillEntry_CommonDown`, `SkillIndex`, `TriggerEvent`, `UGCSkillPaths`, `UTSkillEventType`

#  快速入门

## 技能框架简介
-  <span style="color: #ff0000">技能为模板，不同角色共用一份技能实例</span>
- 一个技能包含多个SkillPhase（阶段）
- 默认情况下，每个阶段是顺序执行的，但可以指定条件跳转
- 每个阶段中包含多个SkillAction（行为）
- 行为组合成一个技能最终的效果<br>
![企业微信截图_168681894065.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_168681894065.png)

<br>

## 技能编辑器简介

### 主界面介绍

- 上方区域：基础操作按钮，保存，编译，设置，复制，新建等
- 中间区域：状态机区域，显示整个技能的状态流程和逻辑
- 右边区域：细节面板，根据选中节点显示不同的细节内容以提供编辑<br>
![企业微信截图_16868189524280.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868189524280.png)
![企业微信截图_16868189599477.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868189599477.png)

<br>

## 创建新技能

 **直接新建**：打开技能编辑器，点击新建,选择保存的目录已经输入文件名。

 ![企业微信截图_16868189837719.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868189837719.png)
 
**基于现有技能复制**：打开技能编辑器，选择要复制的技能打开（以绷带技能为例），点击复制，编辑器自动创建蓝图，基于现有技能复制也是需要手动保存到指定目录下Asset/Blueprint 。

![企业微信截图_16868189987298.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868189987298.png)
![企业微信截图_16868190138210.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868190138210.png)

**快速打开技能**：选中技能蓝图，鼠标右键点击打开技能编辑器
 
![企业微信截图_16868190251913.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868190251913.png)

<br>

## 给角色配置技能

在UGCPlayerPawn蓝图，找到下面的UAESkillManager，分别在Skill Entry Configs中，以及SkillArchetypes中增加配置。

<span style="color: #ff0000"> 注意：技能关联PlayerPawn后，如果技能改名或者转移目录，需要手动在PlayerPawn中重新关联一次，不然会导致技能加载失败。</span>

### 配置玩家技能数据

`SkillArchetypes`中新增配置，引用新建技能。

 ![企业微信截图_16868194693749.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868194693749.png)
 
`Skill Entry Configs`中新增配置，Entry填入`SkillEntry_CommonDown`,`SkillIndex`填`SkillArchetypes`对应的id。

![企业微信截图_16868194859607.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868194859607.png)

### 配置玩法技能数据

`GameState`中`UGCSkillPaths`中新建项，引用新建技能。

![企业微信截图_16868194948700.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868194948700.png)

<br>

## 在代码中释放技能

调用函数释放技能。

<details open>
<summary> <font face="楷体">示例：在PlayerPawn中调用技能</font> </summary>

```lua
--获取技能管理器
local SkillManager = self:GetSkillManagerComponent()
if SkillManager ~= nil then
	--释放120号技能
	SkillManager:TriggerEvent(120, UTSkillEventType.SET_KEY_DOWN)
end
```

</details>



---


## 技能设置，技能阶段设置详解

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器1.0 > 技能设置，技能阶段设置详解

# 技能设置，技能阶段设置详解

## 技能设置详情

---

![企业微信截图_16868198226306.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868198226306.png)
<br>

- <span style="color: #ff0000"> 重要的常用参数会标红显示，一般情况下大部分参数采用默认值即可，没在Wiki中的参数不建议修改</span><br>

参数|说明
| ------ | ------ |
NeedSync|是否会同步技能和CD激活状态, 动态添加的或者实时显示技能cd的技能，需要勾选此选项
SkillName|技能名称
SkillTypes|可设置技能是药品型还是伤害型
只同步最新阶段|见下文详解
释放方式|见下文详解
是否为独占技能|独占技能之间会相互打断
是否能打断自己|技能释放过程中可以再次释放此技能中断正在释放的自己
是否为近战攻击|近战攻击可以一直释放
是否检查第一个Phase的条件|技能释放前会检查第一个阶段的条件，条件不通过则技能不释放
主控端同步阶段后才表现|勾上了，技能的执行会等待服务器控制，否则会直接在客户都安释放表现，一般普通攻击不勾选
断线时保持技能释放|断线时维持技能的状态，技能暂停执行

- 只同步最新阶段<br>
  目前技能有两种同步方案：
  
  - 1.第一种是只同步最新阶段，即只同步当前正在执行的SkillPhase。当某阶段时间过短或阶段连续跳转时会出现客户端漏掉Phase不执行的情况。
  - 2.第二种是用一个int32编码技能执行的过程<br>
    如：1111表示执行了1,2,3,4，四个SkillPhase。这种方式不会漏Phase，但不能进行Phase回跳。
- 释放方式

参数|说明
| ------ | ------ |
Noraml|主动释放，需要代码调用或者其他地方主动调用触发
Passive|被动释放，一般用于被动技能，自动释放

- BaseData中参数说明

参数|说明
| ------ | ------ |
初始激活技能|技能未激活时不能使用
Interval|技能CD
IntervalSincePrevFinish|上次技能结束到下次释放技能的时间间隔
IgnoreDamage|是否忽略受伤动画，勾选时释放技能期间忽略受伤动画

## 技能阶段详解

---

### 技能阶段详解

![企业微信截图_16868198328700.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868198328700.png)

- <span style="color: #ff0000"> 重要的常用参数会标红显示，一般情况下大部分参数采用默认值即可，没在Wiki中的参数不建议修改</span>

参数|说明
| ------ | ------ |
PhaseName|阶段名称，显示用

- BaseData中设置

参数|说明
| ------ | ------ |
PhaseDuration| 阶段持续时间，一定要认真设置，每个阶段依赖这个值执行完成
PhaseConditions|阶段执行前置条件，不满足条件时，阶段不会执行
PhaseConditionFailAction|阶段执行前置条件判断不通过时，在此处配置执行的Action
PhaseType|详见下文

- PhaseType说明

参数|说明
| ------ | ------ |
SPT_SEQUENCE|顺序执行



---


## 新建技能阶段，新建技能Action

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器1.0 > 新建技能阶段，新建技能Action

**涉及API:** `EventEffectMapForEditor`, `GetCurSkillIndex`, `GetSkillManagerComponent`, `TriggerCurSkillEvent`, `TriggerEvent`, `TriggerStringEvent`, `UTSkillEventType`

#  新建技能阶段，新建技能Action

## 新建技能阶段

- 点击鼠标拖出，弹出菜单，选择Add New Phase，新建技能阶段
![企业微信截图_1686819887384.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686819887384.png)

## 新建技能Action

- 双击进入技能Phase编辑界面，弹出菜单，选择New Action，新建一个技能Action
![企业微信截图_16868198947992.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868198947992.png)

### <span style="color: #ff0000"> 重要提醒</span>

- <span style="color: #ff0000"> Action的执行顺序并非严格按连线顺序执行</span>
- <span style="color: #ff0000"> DelayTime不同则DelayTime小的先执行，DelayTime相同则按连线顺序执行</span>
- <span style="color: #ff0000"> 技能Phase中的Action，DelayTime不要大于Phase的执行时间，否则Action会不执行或者执行失败</span>

<span style="color: #ff0000"> 例：</span>

- <span style="color: #ff0000"> 技能阶段持续1秒，播放动画的Action Delay设置0.5秒，但动画播放持续时间为1秒</span>
- <span style="color: #ff0000"> 则动画播放到0.5秒时，动画将中断</span>
- <span style="color: #ff0000">正确应该把技能Action的DelayTime和技能Action执行的内容的持续时间考虑进技能Phase的持续时间中</span>

## 新建技能阶段Condition

- 新增一项Condition，选择要判断的类型
![企业微信截图_16868199039681.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868199039681.png)

## 新建技能响应事件

- 双击进入技能Phase编辑界面，弹出菜单，选择New Event，新建一个技能事件响应
![企业微信截图_16868200763136.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868200763136.png)
- 事件类型中可以选以下几种
![企业微信截图_16868200854380.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868200854380.png)

事件类型|解释
| ------ | ------ |
EventEffectMapForEditor|可以选择SkillEventType中的事件
UAESkill String Event Map for Editor|可以自定义事件的名称
UAESkill Event Effect Map for Editor|可以选择游戏中常用的一些时机事件

- `EventEffectMapForEditor`使用范例<br>

<details open>
<summary> <font face="楷体">示例：设置事件为SET_SKILL_CANCEL</font> </summary>

![企业微信截图_16868200998252.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868200998252.png)

- 在PlayerPawn中可以调用如下代码触发

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

</details>

- `UAESkill String Event Map for Editor`使用范例<br>

<details open>
<summary> <font face="楷体">示例：设置事件为MySkillEvent</font> </summary>

![企业微信截图_16868201112796.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868201112796.png)

- 在PlayerPawn中可以调用如下代码触发

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

</details>

- `UAESkill Event Effect Map for Editorr`使用范例<br>

<details open>
<summary> <font face="楷体">示例：设置事件为PickItem</font> </summary>

![企业微信截图_16868201362339.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868201362339.png)

- 在PlayerPawn中可以调用如下代码触发

```lua
--获取技能管理器
local SkillManager = self:GetSkillManagerComponent()
if SkillManager ~= nil then
	--获得当前正在运行的技能的Index
	local SkillIndex = SkillManager:GetCurSkillIndex()
	--向此技能发送PickItem事件
	SkillManager:TriggerCurSkillEvent(EUAESkillEvent.PickItem, SkillIndex)
end
```

</details>



---


## 自定义自己的技能Action节点

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器1.0 > 自定义自己的技能Action节点

**涉及API:** `Action开始执行调用`, `Action每一帧调用`, `GetOwnerPawn`, `OnRealDoAction`, `OnReset`, `OnUpdateAction`

#  自定义自己的技能Action节点

### 新建蓝图

- 新建蓝图，继承`UAESkill Action BP`
- 注意，是`UAESkill Action BP`不是`UAESkill Action`

![企业微信截图_16868202063113.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868202063113.png)

- 可以在技能中添加自己新建的SkillAction

![企业微信截图_16868202251666.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868202251666.png)

### 绑定Lua脚本

- 实现3个函数

![企业微信截图_16868202334426.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868202334426.png)

<details open>
<summary> <font face="楷体">示例：</font> </summary>

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

### 如何获取技能释放者

在自定义Action的绑定脚本中，获取到技能释放者是很重要的逻辑

可以直接通过GetOwnerPawn()方法获取到技能的释放者

```lua
--获取技能释放者Pawn
--进而获取PlayerKey
--其他定义在Pawn的属性也可以获取
local SkillPawn = self:GetOwnerPawn()
print(SkillPawn.PlayerKey)
```

</details>



---


## 技能编辑器节点查询

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器1.0 > 技能编辑器节点查询

# 技能编辑器节点查询

## Event

### Switch Weapon

- 切换武器
<div class="emptySeat"></div>

### GrenadeModeChange

- 投掷模式改变，高抛/低抛
<div class="emptySeat"></div>

### ReadyToThrowGrenade

- 准备投掷手榴弹
<div class="emptySeat"></div>

### ThrowGrenade

- 投掷手榴弹
<div class="emptySeat"></div>

### Skill Cancel

- 技能取消
<div class="emptySeat"></div>

### GrenadeTimeOut

- 手榴弹超时
<div class="emptySeat"></div>

### SwitchWeaponInterrupt

- 切换武器被中断
<div class="emptySeat"></div>

### SwitchWeaponFinish

- 切换武器结束
<div class="emptySeat"></div>

### UnEquipWeapon

- 卸载武器
<div class="emptySeat"></div>

### UnEquipWeaponFinish

- 卸载武器结束
<div class="emptySeat"></div>

### SkillInterrupt

- 技能中断
<div class="emptySeat"></div>

### SkillPlayerDieInterrupt

- 释放技能角色死亡造成中断
<div class="emptySeat"></div>


### PickItem

- 拾取物品
<div class="emptySeat"></div>

### CanGiveInterrupt

- 可以被赠与时被中断
<div class="emptySeat"></div>

### BeginAccept

- 开始接受
<div class="emptySeat"></div>

### GivingInterrupt

- 赠与过程被中断
<div class="emptySeat"></div>

### ReceivingInterrupt

- 接受过程被中断
<div class="emptySeat"></div>

### Hurt

- 伤害
<div class="emptySeat"></div>

### Door Operation

- 门操作
<div class="emptySeat"></div>

### MovementActive

- 移动行为激活，可以开始移动
<div class="emptySeat"></div>

### MovementInactive

- 移动行为不激活，禁止移动
<div class="emptySeat"></div>

### MovementBounce

- 弹跳移动
<div class="emptySeat"></div>

### MovementStop
- 移动停止
<div class="emptySeat"></div>


### Change Pose

- 改变姿势

---	

## Condition

### And 和条件

- 配置条件全部满足才能触发相应事件

	| 配置项 | 解释 |
	| ------ | ------ |
	| Conditions | 条件配置 |
	| 是否提示 | true时表示满足时显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>	
	
	
### Not 否条件

- 配置条件不满足才能触发相应事件

	| 配置项 | 解释 |
	| ------ | ------ |
	| Conditions | 条件配置 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### OR 或条件

- 配置条件任一满足才能触发相应事件

	| 配置项 | 解释 |
	| ------ | ------ |
	| Conditions | 条件配置 |
	| 是否提示 | true时表示满足时显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### 是否可以翻墙

- 判断玩家角色当前能否翻墙

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否忽略状态检查 | true时表示忽略状态检查 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>

### CurrentWeapon 是否是当前武器

- 检查是否与玩家角色当前的武器一致

	| 配置项 | 解释 |
	| ------ | ------ |
	| Weapon IDs | 武器ID表，将想要检查的武器ID放在此处 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### 是否面朝目标点

- 检查是否朝向目标点

	| 配置项 | 解释 |
	| ------ | ------ |
	| 目标位置拾取 | 选择目标点类型，在其下进行相应的目标点配置 |
	| 偏差的角度Cos | 偏差角度的Cos值 |
	| 是否包含Z轴 | true时表示判断时包含Z轴 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### FallingMode 降落模式

- 检查玩家角色当前是否为降落模式

	| 配置项 | 解释 |
	| ------ | ------ |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### 投掷物模式

- 判断当前投掷物的投掷模式，高抛或低抛

	| 配置项 | 解释 |
	| ------ | ------ |
	| Grenade Mode | 投掷物模式选择 |
	| Target Conditions | 目标条件 |


- HasBuff 拥有Buff

	- 检查当前玩家角色是否拥有buff
	
	| 配置项 | 解释 |
	| ------ | ------ |
	| Buff Name Array | 检查的Buff名称列表 |
	| Target Conditions | 目标条件 |

<div class="emptySeat"></div>

### InFightModePlayerNum 战斗模式玩家数量满足限制

- 检查当前处于战斗模式的玩家是否满足数量限制

	| 配置项 | 解释 |
	| ------ | ------ |
	| 比较方式| 数值比较的方式 |
	| 比较数值 | 比较的数值 |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### IsAnyPlayerAttached 有玩家连接

- 检查是否有玩家连接

	| 配置项 | 解释 |
	| ------ | ------ |
	| Range| 范围 |
	| Actor Tag | Actor的标签 |
	| Actor Class | Actor类 |
	| 是否有特定人数挂接 | 检查连接人数 |
	| Target Conditions | 目标条件 |

<div class="emptySeat"></div>

### IsCDOK 技能CD就位

- 检查技能CD是否结束

<div class="emptySeat"></div>

### IsDifferentSex 是否性别不同

- 检查两个角色性别是否相同

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |

<div class="emptySeat"></div>

### IsFirstAttachedPlayer是首个挂接的玩家

- 检查是否是第一个挂接的玩家

<div class="emptySeat"></div>

### IsHaveGiver 是否有赠送者

- 检查是否有赠送者

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### IsHaveReceiver 是否有接收者

- 检查是否有接收者

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### 是男人吗？

- 检查角色是否为男性角色


<div class="emptySeat"></div>

### IsOnVehicle 在载具上

- 检测是否在载具上

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### IsSkillActive 技能是否激活

- 检查技能是否激活

	| 配置项 | 解释 |
	| ------ | ------ |
	| Skill Class Name | 技能类名称 |
	| Equal Skill Active | 相同的技能是否激活 |
	| Target Conditions | 目标条件 |

<div class="emptySeat"></div>	
	
### IsSkillRunning 技能是否正在运行

- 检查技能是否正在运行

	| 配置项 | 解释 |
	| ------ | ------ |
	| Skill Names | 技能名称表，要检测的技能配置 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>	
	
	
### NotIsInWater 不在水里

- 检查角色是否在水里

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### AllowPawnState 允许的玩家状态

- 检查玩家状态是否为允许的状态列表中的状态

	| 配置项 | 解释 |
	| ------ | ------ |
	| Arr Allow Pawn State | 允许的玩家状态列表 |
	| Check Both Side | 双端检测 |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### 是否正在创建武器

- 检查当前是否正在创建武器

<div class="emptySeat"></div>

###  Conditiion Lua

- 以Lua文件作为判断条件

	| 配置项 | 解释 |
	| ------ | ------ |
	| Lua File | Lua文件 |
	| Params | 参数 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>

### VelocityChange 速度变化

- 检查速度变化

	| 配置项 | 解释 |
	| ------ | ------ |
	| Check Type | 检查方式 |
	| Speed Change Value | 速度改变值，改变值须达到该值 |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### HandleItemLimit 满足道具限制

- 检查道具是否满足使用显示

	| 配置项 | 解释 |
	| ------ | ------ |
	| 是否只用黑板中的ItemID | true时表示使用黑板中的值|
	| Selected Key Name | 选择的字段名称 |
	| Operate Type | 操作类型 |
	| Need Item Num | 需要的物品数量 |
	| Item ID | 需要检测的物品ID |
	| Type | 物品类型 |
	| Check Both Side | 双端检测 |
	| 是否显示提示 | true时表示显示提示 |
	| 提示ID | 提示文本ID |
	| Target Conditions | 目标条件 |
	
<div class="emptySeat"></div>
	
### IsMoveHitLandScape碰撞到地面

- 检查Actor是否撞击到地面

	| 配置项 | 解释 |
	| ------ | ------ |
	| Move Hit Actor Key | 碰到Actor的事件 |
	| Move Hit Normal Key | 碰到地面的事件 |
	| Target Conditions | 目标条件 |

<div class="emptySeat"></div>
	
### Custom Condition Is FPP

- 检查是否时第一人称

<div class="emptySeat"></div>

### Custom Condition Holding Weapon

- 检查某个槽位是否持有武器

	| 配置项 | 解释 |
	| ------ | ------ |
	| Check Slot | 检查的槽位|
	| Target Conditions | 目标条件 |

<div class="emptySeat"></div>	
	
### BP_SkillCondition_IsMyTeammate

- 检查是否是己方队友
	
<div class="emptySeat"></div>

---

## SkillAction

### AI

#### 怪物移动/撞击

| 配置项 | 解释 | 
| ------ | ------ |
| Damage Picker | sampleText |
| Speed | 移动速度（CM/S） | 
| Acceleration | 加速度（CM/S2） |
| MaxSpeed | 最大移动速度（CM/S） |
| 追踪目标 | true时追踪目标 |
| Overlap Object Types | 碰撞物体类型 |
| 是否检查碰撞 | true时检查碰撞 |
| 与目标的最短允许距离 | 与目标间允许的最短距离 |
| Skill Target Picker| 技能目标选择 |


#### 技能移动怪物
| 配置项 | 解释 | 
| ------ | ------ |
| Velocity | 移动速度 |
| Is Stop Movement | true时停止移动 |
| Damage Picker |移动目标选择器|
| Check Pawn Collision | 检查角色碰撞 |
| Predict Factor |预测权值 |
| Forward Only Mode | 仅向前 |
| Self Move Only | 仅自身移动 |
| Self Move Direction | 自身移动方向 |
| Debug Object Class | 用于调试路径的物品类|
| Debug Object Class2 | 用于调试路径的物品类2 |


#### 扑向目标（AI）
| 配置项 | 解释 | 
| ------ | ------ |
| Damage Picker |移动目标选择器|
| Location Picker| 选择目标类型 |
| 投射目标点偏移 | 飞扑目标点座标偏移|
| 重力系数 | 重力大小 |
| 投射速度 | true时使用飞扑 |
| Z-重力曲线 | 位移过程中重力改变曲线 |
| 是否使用缓存的初始目标位置 | true时使用缓存的初始目标位置 |


#### 召集僵尸
| 配置项 | 解释 |
| ------ | ------ |
| Summon Count Per Player | 每个玩家召唤的数量 |
| Summon Time Interval | 召唤时间间隔 |
| Summon Function | 召唤时用的函数 |
| Target Picker | 目标选择 |
#### AI旋转至朝向目标
| 配置项 | 解释 |
| ------ | ------ |
| RotateTarget Picker | 朝向目标选择 |
| RotateTime | 转向时间 |
| bOnlyServer | true时仅在服务器使用 |
| bPrintDebugInfo | true时输出调试信息 |
#### 改变僵尸状态
| 配置项 | 解释 |
| ------ | ------ |
| Target Pawn State | 目标状态 |

### Buff
#### 添加/移除buff
| 配置项 | 解释 |
| ------ | ------ |
| Is Add Buff | true时增加Buff，false时移除Buff |
| Buff Name | Buff名称 |
| Add Layer Count | 施加Buff的层数 |
| Target Picker | 目标选取 |
| Ignored Actor Classes | 不会被施加Buff的Actor类型 |
| Whether Stop Buff After Stop Phase | true时在阶段停止后结束Buff |
| Whether Stop Buff After Stop Skill | true时在技能停止后结束Buff |
| Whether Stop Buff Before Close Skill | true时在技能关闭前结束Buff |
#### 添加buff，并动态设置持续时间
| 配置项 | 解释 |
| ------ | ------ |
| Buff Name | Buff名称 |
| Add Layer Count | 施加的buff层数 |
| Same Buff Name List | 同名Buff列表 |
| Target Picker | 目标选择 |
### UI
#### 动态创建UI
| 配置项 | 解释 |
| ------ | ------ |
| UIConfig | UI配置 |
| 重置UI状态Msg | 重置UI的信息 |
| 关闭UI状态Msg | 关闭UI的信息 |
| 禁用UI时是否移除 | true时禁用UI时将移除 |
| 是否排除观战端 | true时排除观战端 |
#### 显示技能按键
| 配置项 | 解释 |
| ------ | ------ |
| Skill Target Picker| 技能目标选择 |

#### 显示技能提示
| 配置项 | 解释 |
| ------ | ------ |
| Prompt Text | 提示文本 |

#### 隐藏技能按键
| 配置项 | 解释 |
| ------ | ------ |
| Skill Target Picker| 技能目标选择 |

#### 设置预恢复提示条
| 配置项 | 解释 |
| ------ | ------ |
| Show Data Key | ------ |
| Show Type | 显示类型 |
| Value | 恢复值 |
| Limit Value | 限定恢复值 |
| Remove by Add Buff | true时添加Buff时移除 |
| Is Predict for Signal HP | true时表示提示信号预恢复 |
| Can be Ignored by GM | true时可以被GM忽略 |
### 人物声音
#### 播放声音
| 配置项 | 解释 |
| ------ | ------ |
| AK Audio Event | 音频资源 |
| Only Simulation | true时仅模拟 |

### 人物动画

#### 播放Montage

| 配置项 | 解释 |
| ------ | ------ |
| Anim Montage | 配置蒙太奇动画 |
| Stop Prev Montage | true时停止上一个蒙太奇 |
| Reset Stop Anim | true时重置时停止动画 |
| Undo Stop Anim | true时无操作时停止动画 |
| Only Simulation | true时仅模拟 |
| Start Section Name | 开始部分名称 |

#### 根据空手/持枪PlayMontagePose

| 配置项 | 解释 |
| ------ | ------ |
| Pose Montage Data Armed | 持枪蒙太奇姿势数据 |
| FPPPose Motage Data Armed | 第一人称下的持枪蒙太奇姿势数据 |
| Pose Montage Data | 空手蒙太奇姿势数据 |
| FPPPose Motage Data | 第一人称下的空手蒙太奇姿势数据 |
| Check Duration Config | 持续时间检查 |

#### 根据武器类型播放动画

| 配置项 | 解释 |
| ------ | ------ |
| Stop Prev Montage | true时停止上一蒙太奇动画 |
| 是否使用固定值比率 | true时使用固定值比率 |
| 固定值比率 | 固定值比率配置 |
| 播放速率_比率误差 | 比率误差值 |
| 播放速率_速度误差 | 速度误差值 |
| EmptyHand_Pose Montage Data | 空手蒙太奇姿势数据 |
| EmptyHand_FPPPose Motage Data | 第一人称下的空手蒙太奇姿势数据 |
| HandWeapon_Pose Montage Data | 持枪蒙太奇姿势数据 |
| HandWeapon_FPPPose Motage Data | 第一人称下的持枪蒙太奇姿势数据 |
| Weapon Types | 武器类型列表 |
| Stop Anim After Action | true时Action结束时停止动画 |
| Update Anim After Change | true时改变后更新动画 |

#### 速率可调播放Montage

| 配置项 | 解释 |
| ------ | ------ |
| 是否使用固定值比率 | true时使用固定值比率 |
| 固定值比率 | 固定值比率配置 |
| 播放速率_比率误差 | 比率误差值 |
| 播放速率_速度误差 | 速度误差值 |
| Anim Montage | 蒙太奇动画配置 |
| Stop Prev Montage | true时停止上一蒙太奇动画 |
| Stop Prev Montage | true时停止上一个蒙太奇 |
| Reset Stop Anim | true时重置时停止动画 |
| Undo Stop Anim | true时为撤销时停止动画 |
| Only Simulation | true时仅模拟 |
| Start Section Name | 开始部分名称 |
#### 暂停动画
| 配置项 | 解释 |
| ------ | ------ |
| Duration | 持续时间配置 |

#### PlayMontage根据Watering决定动画起始点

| 配置项 | 解释 |
| ------ | ------ |
| Anim Montage | 蒙太奇动画配置 |
| Stop Prev Montage | true时停止上一个蒙太奇 |
| Keep Animation | true时保持动画 |

#### PlayMontagewithPose播放姿势蒙太奇

| 配置项 | 解释 |
| ------ | ------ |
| Pose Montage Data | 蒙太奇姿势数据 |
| FPPPose Motage Data | 第一人称下蒙太奇姿势数据 |
| Play Speed Rate | 播放速率 |
| Start Position | 起始位置|
| Mutex Montage Group Name | 互斥蒙太奇组名 |
| Stop Prev Montage | true时停止上一蒙太奇动画 |
| Stop Prev Montage | true时停止上一个蒙太奇 |
| Reset Stop Anim | true时重置时停止动画 |
| Undo Stop Anim | true时无操作时停止动画 |
| Only Simulation | true时仅模拟 |
| Start Section Name | 开始部分名称 |

#### PlayMontagewithPoseJump播放跳跃蒙太奇

| 配置项 | 解释 |
| ------ | ------ |
| Anim Montage Jump | 跳跃蒙太奇动画配置 |
| Pose Montage Data | 蒙太奇姿势数据 |
| FPPPose Motage Data | 第一人称下蒙太奇姿势数据 |
| Play Speed Rate | 播放速率 |
| Start Position | 起始位置|
| Mutex Montage Group Name | 互斥蒙太奇组名 |
| Stop Prev Montage | true时停止上一蒙太奇动画 |
| Stop Prev Montage | true时停止上一个蒙太奇 |
| Reset Stop Anim | true时重置时停止动画 |
| Undo Stop Anim | true时无操作时停止动画 |
| Only Simulation | true时仅模拟 |
| Start Section Name | 开始部分名称 |

#### StopMontage停止播放蒙太奇

| 配置项 | 解释 |
| ------ | ------ |
| Anim Montage | 蒙太奇动画配置 |

### 人物状态

#### 改变姿势（PoseState）

| 配置项 | 解释 |
| ------ | ------ |
| Target Pose State | 目标姿势 |
| Should Show Prompt | true时显示提示 |

#### 关闭自动拾取

| 配置项 | 解释 |
| ------ | ------ |
| Act Name | 动作名称 |

#### 恢复（药品，能量，救援）

| 配置项 | 解释 |
| ------ | ------ |
| 属性名称 | 更改的属性名称 |
| 恢复类型 | 恢复类型选择 |
| 恢复数值 | 恢复数值配置 |
| 属性恢复上限 | 属性恢复上限，高于该上限无法恢复 |
| 是否在服务端执行 | true时只能在服务端执行 |
| 恢复数值 | 恢复的原因类型 |
| Can be Ignored by GM | true时可被GM忽略 |
| Has Effect when Near Death | true时即接近死亡时有效 |

#### 禁用/解禁移动

| 配置项 | 解释 |
| ------ | ------ |
| Set Is Moveable | true时为可移动，false时为不可移动 |

#### 禁止某个/一系列状态（PawnState）

| 配置项 | 解释 |
| ------ | ------ |
| Pawn Picker | 角色目标选取 |
| Pending Disable Pawn States | 禁用状态列表 |
| State | 状态配置 |
| New Disable | true时表示新增的不可用 |
| Reset on Enable | true时表示可用时重置 |
| Reverse Altered States on Undo | true时无操作时撤销已改变的状态 |
| Reverse Altered States on Reset | true时表示重置时撤销已改变的状态 |

#### 切换MovementMode

| 配置项 | 解释 |
| ------ | ------ |
| Movement Mode  | 移动模式配置 |

#### 设置角色状态

| 配置项 | 解释 |
| ------ | ------ |
| Pawn State | 角色状态 |
| Set Enter | true时表示进入状态，false表示离开状态 |
| Destroy After Phase | true时在阶段结束后销毁 |
| Destroy After Skill | true时在技能结束后销毁 |

#### 设置是否使用ControlRotation

| 配置项 | 解释 |
| ------ | ------ |
| 是否用Controller的Pitch | true时为使用Controller的Pitch |
| 是否用Controller的Yaw | true时为使用Controller的Yaw |
| 是否用Controller的Roll | true时为使用Controller的Roll |
| 是否在阶段结束时停止 | true时为在阶段结束时停止 |
| 人物腰部是否跟随Controller旋转 |  true时为人物腰部跟随Controller旋转 |
| Yaw值最大误差 | Yaw值最大误差配置 |

#### 修改碰撞通道

| 配置项 | 解释 |
| ------ | ------ |
| Channel to Change | 目标碰撞配置 |
| Response | 回应类型配置 |

#### 修改最大移动速度

| 配置项 | 解释 |
| ------ | ------ |
| 修改速度 | 配置为原有速度的百分比 |


### 人物行动

#### 触发一次人物跳跃

| 配置项 | 解释 |
| ------ | ------ |
| 是否使用黑板变量 | true时为使用黑板变量 |
| Add Velocity | 加速度 |
|往角色面朝方向增加 | true时为向角色面朝方向增加|
| 往视角方向增加 | true时为向视角方向增加 |

#### 翻墙

| 配置项 | 解释 |
| ------ | ------ |
| 是否需要翻越检测 | true时为翻越检测 |

#### 主角Launch

| 配置项 | 解释 |
| ------ | ------ |
| Launch角色 | 角色配置 |
| 目标位置拾取 | 选取目标位置 |
| Launch期间是否禁止人物移动 | true时禁止移动 |
| 是否使用自己配置的目标点 | true时为使用自己配置的目标点 |
| 自定义的目标方向 | 目标方向配置 |
| 自定义的移动距离 | 移动距离配置 |
| 启用重力 | true时为启用重力 |
| 重力缩放倍数 | 重力缩放倍数配置 |
| 是否使用固定值速度 | true时为使用固定值速度 |
| 固定值速度 | 固定值速度配置 |
| 速度曲线 | 速度曲线配置 |
| 允许停止范围 | 允许停止范围配置 |
| 移动距离够了就停止 | true时为一定距离够了就停止 |
| 到达目标点一定范围内就停止 | true时为进入目标点一定范围内时就停止 |
| 是否实时更新位置信息 | true时为实时更新位置信息 |
| 计算与终点的距离时是否包含Z轴 | true时为计算时包含Z轴 |
| 是否包含Z轴 | true时为包含Z轴 |
| 包含Z轴时恢复的MovementMode | 包含Z轴时的恢复MovementMode选择|
| 添加地面移动保护 | true时为地面移动保护 |
| 地面最大倾角 | 地面最大倾角配置 |
| StopLaunch时减缓当前速度 | true时为停止时减缓当前速度 |
| DebugLine | true时为开启调试辅助线 |
| 沿着角色朝向的方向飞 | true时为朝着角色朝向的方向飞 |
| Z轴速度曲线 | Z轴速度曲线配置 |
| XY速度 | XY轴速度曲线配置 |
| 使用黑板的里的速度曲线 | true时为使用黑板里的速度曲线 |

### 武器

#### 激光瞄准

| 配置项 | 解释 |
| ------ | ------ |
| Damage Picker | 终点目标选取 |
| Laser Template | 激光模板 |
| Attach Socket Name | 激光起点挂点 |
| Debug Line | true时为开启调试辅助线|
| Target Offset | 目标偏移配置|
| Source Offset | 源偏移配置 |
| Attach Target Socket Name | 激光终点挂点 |

#### 切换到某个手雷的武器槽位
| 配置项 | 解释 |
| ------ | ------ |
| Weapon Slot Name | 武器槽位名 |
| Tyoe | 物品类型 |
| Type Specific ID | 类型特殊ID |

#### 切换指定槽位武器
| 配置项 | 解释 |
| ------ | ------ |
| 武器槽位 | 武器槽位选择 |
| 技能结束是否切回 | true时在技能结束后将切回原武器 |
| 播放切枪动画 | true时执行切枪时将播放切枪动画 |
| 强制完成上次切枪 | true时若执行时存在切枪动作，则强制完成切枪动作 |
| 忽略状态检测 | true时将忽略状态检测 |
#### 切换至上一把武器

| 配置项 | 解释 |
| ------ | ------ |
| Use Animation | true是播放切枪动画 |
| Force Finish Previous Switc | true时若执行时存在切枪动作，则强制完成切枪动作  |
| 播放切枪动画 | true时执行切枪时将播放切枪动画 |

#### 武器射击

| 配置项 | 解释 |
| ------ | ------ |
| 射击类型 | 射击类型选择（STOP，START） |

#### 显示/隐藏枪械准心

| 配置项 | 解释 |
| ------ | ------ |
| Cross Hair Vis | 武器准心可视化，true时为显示准心 |
| Reset to Vis | 重新设置可视化 |

#### 显示武器

| 配置项 | 解释 |
| ------ | ------ |
| bShowWeapon | true时显示武器 |
| bUbdoReset | true时为无操作时重置 |
| bPhaseFinishClear | true时当阶段结束时清除武器显示 |
| WeaponName | 武器名称 |

### 活动

#### 触发GIS逻辑

| 配置项 | 解释 |
| ------ | ------ |
| GISActor | 触发GIS的Actor选择 |
| Indexes | 序列 |
| Send Custom Message | true时发送自定义信息 |
| Trigger All | true时为触发所有 |
| Parameters | 自定义信息的参数列表 |
| Name | 参数名称 |
| Type | 参数类型 |
| Default Value | 默认值配置 |
| When to Call | 触发时机配置 |

### 通用物品

#### 添加/移除物品

| 配置项 | 解释 |
| ------ | ------ |
| ItemID | 物品ID |
| Count | 数量 |

#### 消耗某个Item

| 配置项 | 解释 |
| ------ | ------ |
| 是否使用黑板中的ItemID | true时将使用配置在黑板中的ItemID |
| Selected Key Name |  |
| ItemID | 消耗的物品ID |
| Type | 物品类型 |
| Count | 数量 |
| Is Grenade | true时表示物品为手雷 |
| Is Need Notify Lobby Server | true时表示通知大厅服务器 |

### 相机

#### 播放镜头动画

| 配置项 | 解释 |
| ------ | ------ |
| 仅客服端 | true时表示仅在客户端播放 |
| 相机动画模板 | 相机动画文件配置 |
| 是否重置镜头 | true时表示重置镜头 |
| 强制转换第三人称 | true时表示在播放时将强制转换成第三人称 |
| 是否锁住镜头旋转 | true时表示在播放时禁止镜头旋转 |
| 恢复镜头旋转延迟时间 | 恢复镜头旋转时间配置 |

#### 播放镜头抖动效果

| 配置项 | 解释 |
| ------ | ------ |
| 相机抖动模板 | 相机抖动模板配置 |
| 抖动幅度 | 相机抖动幅度配置 |
| 最远距离 | 距离配置，在此距离内的玩家才会抖动相机 |

#### 改变相机摇臂长度

| 配置项 | 解释 |
| ------ | ------ |
| New Spring Arm | 新的相机摇臂长度 |
| Socket Offset | 挂点偏移 |
| Target Offset | 目标偏移配置 |
| Override Socket | 重载挂点 |
| Override Target | 重载目标 |
| Camera Data_Camera Data Name | 相机数据文件配置 |
| Camera Data_Data Name | 相机数据名称 |
| Camera Data_Exclusion Data Name | 除外的相机数据名称列表 |
| Camera Data_Relative Location Offset | 相对位置偏移 |
| Camera Data_Socket Offset| 相机数据挂点偏移 |
| Camera Data_Target Offset | 相机目标偏移 |
| Camera Data_Target Arm Length| 相机目标摇臂长度 |
| Camera Data_Spring Arm Length| 相机摇臂长度 |
| Camera Data_Target Arm Length Additive Offset | 相机目标摇臂长度叠加偏移 |
| Camera Data_Additive Offset Fov | 相机FOV叠加偏移 |
| Camera Data_Arm Length Interp Speed | 相机摇臂长度变化平滑速度 |
| Camera Data_Operate Type| 操作类型 |
| Force Undo | true时强制不执行 |
| Show Log | true时表示输出日志 |

#### 禁用镜头旋转和小眼睛

| 配置项 | 解释 |
| ------ | ------ |
| 仅客服端 | true时表示仅在客户端播放 |
| 是否重置镜头 | true时表示重置镜头 |
| 恢复镜头旋转延迟时间 | 恢复镜头旋转时间配置 |

#### 禁止动画瞄准

| 配置项 | 解释 |
| ------ | ------ |
| Force Disable Aim | true时为强制禁止镜头瞄准 |
#### 切换相机观察目标

| 配置项 | 解释 |
| ------ | ------ |
| Range | 相机观察范围 | 
| Actor Tag | Actor标签 | 
| Actor Class | Actor类 | 
| Target Transition Params_Blend Time| 目标转换参数_混合时间配置 | 
| Target Transition Params_Blend Function| 目标转换参数_混合函数配置  | 
| End Target Transition Params_Bland Time| 结束目标转换参数_混合时间配置  | 
| End Target Transition Params_Blend Function| 结束目标转换参数_混合函数配置 | 
| Force TPP | true时表示观察时强制第三人称 | 
| Reset时还原镜头 | true时为重置时还原镜头 | 
| Undo 时还原镜头 |  true时为撤销时还原镜头 | 

#### 锁定视角（第一/三人称）

| 配置项 | 解释 |
| ------ | ------ |
| 锁定类型 | 视角锁定类型配置（FPP,TPP） | 
| 技能结束后恢复原先视角 | true时表示技能结束后解除视角锁定恢复原先视角 | 
| 锁定视角切换按钮 | true时表示锁定视角切换按钮 | 
| Force Undo | true时表示强制撤销 | 
| 载具中锁定 | true时b表示在载具中锁定视角 | 

#### 限制相机旋转角

| 配置项 | 解释 |
| ------ | ------ |
| Min Rotator | 最小旋转角配置 | 
| Max Rotator | 最大旋转角配置 | 
| Disable Controller Yaw Rotation | true时表示关闭控制器的Yaw轴的旋转 | 
| Set Min Max Enable | true时表示打开最大最小值配置 | 
| Force Follow Camera | true时为强制跟随相机 | 
| Do Un Do on Reset | true时为重置时撤销操作 | 
| Need Set Free Camera on Un Do | true时为在撤销时设置成自由相机 | 
| Reset to Rotation | 重置时的相机旋转配置 | 

#### SetEyeRotationMode解锁视角控制

| 配置项 | 解释 |
| ------ | ------ |
| Free Camera | true时为设置成自由相机 | 
| Auto Revert on Undo | true时为撤销时自动还原 | 
| Spring Inhert Rotation | true时表示启用旋转平滑 | 

### 表现

#### AddParticle添加粒子特效

| 配置项 | 解释 |
| ------ | ------ |
| Template Particle Effect | 粒子特效配置 | 
| Attach Socket Name | 挂点名称 | 
| Location Position | 位置配置 | 
| Location Rotation | 旋转配置 | 
| Location Scale | 大小配置 |
| FPPScale | 第一人称下的大小缩放 |
| FPPLocation Position | 第一人称下的位置 |
| Phase Finish Remove | true时为在阶段结束时移除 |
| Undo Remove | true时表示撤销时移除 |

#### AnimHurtingState播放受伤动画

| 配置项 | 解释 |
| ------ | ------ |
| Target | 播放目标配置 | 

#### CreateParticleontheGround相对于地面生成特效

| 配置项 | 解释 |
| ------ | ------ |
| Template Effet | 特效配置 | 
| Offset Relative Owner | true时表示相对于拥有者偏移 | 
| Offset Loc | 位置偏移 | 
| Relative Scale | 相对大小配置 | 
| Need Attach to the Ground | true时附着在地面上 | 
| Trace Extent | 痕迹程度 | 
| Trace Channel | 射线通道 | 
| Auto Destroy | true时自动销毁 | 
| Destroy Particle on Undo Action  | true时为撤销时销毁特效 | 
| Only Spawn On Autonomous Client | true时表示仅生成在独立的客户端 | 

#### RemoveParticle移除粒子特效

| 配置项 | 解释 |
| ------ | ------ |
| Particle Comp Tag Name | 特效标签名称 | 
| Phase Finish Remove | true时为在阶段结束时移除 |
| Undo Remove | true时表示撤销时移除 |

### 载具

#### 加油

| 配置项 | 解释 |
| ------ | ------ |
| RunOnServer | true时表示在服务端运行 | 
| GasValue | 汽油值配置 | 
| Report Skill Cast Info | true时表示反馈技能信息 | 
| Hero ID | 角色ID | 
| Skill ID | 技能ID | 
| Record Name | 记录名 | 

#### 设置载具武器黑板数据

| 配置项 | 解释 |
| ------ | ------ |
| 载具黑板数据配置 | 黑板数据列表 | 
| 武器所在座位ID | 武器所在座位ID | 
| 该座位上武器列表ID | ID配置 | 
| 该座位上武器列表ID | 武器类型配置 | 

#### 载具维修

| 配置项 | 解释 |
| ------ | ------ | 
| RunOnServer | true时表示在服务端运行 | 
| PercentValue | 维修后百分比 | 
| GasValue | 汽油值配置 | 
| Report Skill Cast Info | true时表示反馈技能信息 | 
| Hero ID | 角色ID | 
| Skill ID | 技能ID | 
| HPRecover Record Name | 生命值恢复记录名 | 
| Tire Repair Record Name | 轮胎维修记录名 | 

### 技能

#### 触发技能

| 配置项 | 解释 |
| ------ | ------ |
| Skill Class | 技能蓝图配置 | 
| Trigger on Server | true时表示在服务器触发该技能 | 

#### 对当前技能触发EUAESkillEvent事件

| 配置项 | 解释 |
| ------ | ------ |
| Custom Event | 事件类型 | 
| UTCustom Event | 事件触发方式 | 

#### 对当前技能触发自定义字符事件

| 配置项 | 解释 |
| ------ | ------ |
| Trigger to All Skill | 触发所有类型事件 | 
| Custom String Event | 事件名称 |
 
#### 技能阶段跳转

| 配置项 | 解释 |
| ------ | ------ |
| New Phase ID | 跳转的阶段ID | 
| Jump Condition | 跳转条件 |
 
#### 捆绑Action的行为

| 配置项 | 解释 |
| ------ | ------ |
| Effect | 效果配置 | 
| Exe Reset | true时执行重置 | 
| Exe Undo | true时执行撤销 | 

#### 随机跳转至某一技能阶段

| 配置项 | 解释 |
| ------ | ------ |
| Start Index | 开始的技能阶段序号 | 
| End Index | 结束时的技能阶段序号 | 
| Is Can be Cur Index | true时表示可以跳转到当前的技能阶段 | 
| Jump Condition | 跳转条件 | 

#### 随机执行某个action

| 配置项 | 解释 |
| ------ | ------ |
| Skill Candidates | 随机的Action列表 | 

#### 在范围内给Actor发送自定义事件

| 配置项 | 解释 |
| ------ | ------ |
| Range | 发送自定事件的范围 |
| Actor Tag | 接收事件的Actor标记 | 
| Actor Calss | Actor蓝图|
| Event Type | 事件类型 | 
| End Event Type | 结束事件类型 | 
| Stops at First Encounters | true时表示第一次接收事件后停止 | 
| Local Only | true时为仅在本地执行 | 
| DSOnly | true时表示仅在DS运行 | 
| Send End Event | true时表示发送结束事件 | 
| Trigger Activity | true时表示Trigger激活 | 
| Trigger Activity Event  | 激活时的事件名称 | 

#### ActionwithConditions条件Action

| 配置项 | 解释 |
| ------ | ------ |
| Condition | 条件列表 | 
| Action | 成功时的Action | 
| False Action | 失败时的Action | 

#### StopSkill停止技能

| 配置项 | 解释 |
| ------ | ------ |
| Is Stop All Skill | true时表示停止所有技能 | 
| Is Stop Self | true时表示停止本技能 | 
| Other Skill Class Name | 停止其他技能的名称 | 
| Stop Reason | 停止原因 | 

#### 设置黑板的值

| 配置项 | 解释 |
| ------ | ------ |
| Type | 类型 | 
| Ecpected Object | 预设的Object | 
| Ecpected Class | 预设的蓝图 | 
| Ecpected Enum | 预设的枚举值 | 
| Ecpected Int | 预设的整数 | 
| Ecpected Float | 预设的浮点数 | 
| Ecpected Bool | 预设的布尔值 | 
| Ecpected String | 预设的字符 | 
| Ecpected Name | 预设的名称 | 
| Ecpected Vector | 预设的向量 | 

### 其他

#### 怪物跳跃

| 配置项 | 解释 | 
| ------ | ------ |
| Damage Picker | sampleText |
| Speed | 移动速度（CM/S） | 
| 追踪目标 | true时追踪目标 |
| 跳跃起始点Z值偏移 | 跳跃起始点Z值偏移 |
| 高跳阈值 | Z值偏移大于此值才会高跳 |
| 是否检查碰撞 | true时检查碰撞 |
| 与目标的最短允许距离 | 与目标间允许的最短距离 |
| Override Gravity ZScale | 覆盖Z轴的重力系数 |
| 跳跃速度区间 | X为最小值，Y为最大值 |
| Jump Speed Interval | 跳跃速度变化间隔 |
| Offset Of Target Dir | 目标方向偏移 |
| Max Percent Offset Of Target Dir |目标方向偏移的最大百分比  |

#### 投掷动作

| 配置项 | 解释 | 
| ------ | ------ |
| 只在服务器生成 | true时表示只在服务器执行 |
| 服务器触发发射/主端触发发射 | true时表示只能在服务器或主端触发 |
| Projectile Actor Template | 投掷物蓝图/模板|
| Damage Picker | 伤害选择配置 |
| 是否使用头部位置 | true时表示使用头部位置 |
| 是否使用精确位置 | true时表示使用精确位置 |
| 投射起点偏移 | 投射时的起点偏移配置 |
| 投射目标点偏移 | 投射目标点偏移配置 |
| 贴附目标中心点 | true时表示贴附在目标的中心点 |
| 重力系数 | 投掷物的重力系数 |
| 投射速度 | 投掷物投出时的速度(CM/S) |
| 最远投射距离 | 投掷物能达到的最远距离 |
| 挂在的槽位 | 投掷物放置的槽位 |
| 延迟投出时间 | 延迟投出时间 |
| 延迟投出时隐藏 | true时表示延迟投出时隐藏 |
| 最长存活时间 | 投掷物的最大存活时间 |
| 是否使用高抛 | true时表示投掷时使用高抛 |
| 高抛重力系数 | 高抛下的重力系数 |
| Gravity Scale | 重力系数 |
| 是否追踪目标 | true时追踪目标 |
| 追踪加速度大小 | 若选择追踪目标，则使用此配置 |
| 是否是射线 | true时表示是射线 |
| 是否是水平的 | true时表示是水平的射线 |



## BuffAction

#### AttrModify动态属性修改器

| 配置项 | 解释 |
| ------ | ------ |
| Authority Only | true时为仅运行在ds |
| Attr Modify Item Name | 属性修改物品名称 |
| Attr Name | 属性名称 |
| Modifier Op | 修改操作（Set，Plus，Mult） |
| 是否为资源类型 | true时为资源类型 |
| Modifier Value | 修改数值配置 |

#### （Buff）if...Else...

| 配置项 | 解释 |
| ------ | ------ |
| If Condition | 判断条件 | 
| If Action | true时的Action| 
| Else Action | false时的Action | 

#### （Buff）SequenceActions顺序的Action

| 配置项 | 解释 |
| ------ | ------ |
| Sequence | Action序列 | 

#### 播放动画

| 配置项 | 解释 |
| ------ | ------ |
| Animation Assert to Play | 播放的动画 | 
| Animation Assert to Play FPP | 第一人称播放的动画 | 
| Animation Montage to Play | 播放的蒙太奇动画 | 
| Animation Montage to Play FPP | 第一人称播放的蒙太奇动画 | 
| Need Replay by Change First View | true时表示切换到第一人称时重新播放动画 | 
| Animation Assert Tag | 播放动画的标记 |
|Animation Assert Tag FPP | 第一人称播放动画的标记 |
| Animation Montage tag | 播放的蒙太奇动画的标记 | 
| Animation Montage to Play FPP | 第一人称播放的蒙太奇动画的标记 | 

#### 播放屏幕效果

| 配置项 | 解释 |
| ------ | ------ |
| Need Check View Self | true时表示需要检查自身的视角 |
| Need Check Device Quality | true时表示需要检查设备画面质量设置 |
| Not Allow Device Quality Level | 不支持播放的设备画质设置 |
| Appearance Material | 屏幕效果材质 |
| Life Span |时间长度 |

#### 日志

| 配置项 | 解释 | 
| ------ | ------ |
| Log String | 日志内容 |

#### 使角色进入某个状态

| 配置项 | 解释 | 
| ------ | ------ |
| Target State | 目标状态 |

#### 向某个Buff（可以是自己的）FireEvent

| 配置项 | 解释 | 
| ------ | ------ |
| Buff Evnet Class | Buff事件 |
| Buff Name  | Buff名称 |
| Parameters | 参数列表 |
| Name | 名称 |
| Type | 类型 |
| Default Value | 默认值配置 |

#### 向所有Buffs（包括自己）FireEvent

| 配置项 | 解释 | 
| ------ | ------ |
| Buff Evnet Class | Buff事件 |
| Parameters | 参数列表 |
| Name | 名称 |
| Type | 类型 |
| Default Value | 默认值配置 |

#### 向自己（Buff）FireEvent

| 配置项 | 解释 | 
| ------ | ------ |
| Buff Evnet Class | Buff事件 |
| Parameters | 参数列表 |
| Name | 名称 |
| Type | 类型 |
| Default Value | 默认值配置 |

#### 淹在水里受伤

| 配置项 | 解释 | 
| ------ | ------ |
| Interval Time | 扣血间隔时间 |
| Dot Value | 伤害值 |
| Breath Amount Threhold  | 呼吸值零界点 |
| Damage Type Class | 伤害类型 |

#### 周期行为

| 配置项 | 解释 | 
| ------ | ------ |
| Action | 行为配置 |
| Iterval | 执行间隔 |
| Current Tick Delta Time | Tick 起始时间，用于控制第一次触发Action的时间点 |

#### Buff附加特效

| 配置项 | 解释 | 
| ------ | ------ |
| Component  | 组件 |
| Socket Name | 挂点名称 |
| Show Only First Person View | true时表示仅在第一人称下可见 |


---
