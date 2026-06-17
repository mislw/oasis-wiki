# 进阶内容/GamePlay系统/技能系统/Buff编辑器1.0

> 本分类共 2 篇文章

---


## Buff简介

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器1.0 > Buff简介

**涉及API:** `AActor`, `AController`, `AddBuff`, `FName`, `NeedSimulateToClient`, `PlayerPawn`

# Buff系统

## Buff简介

---

### Buff的主要特点

- 有持续时间，有完整的生命周期
- 可以叠加层数
- 单个Buff功能相对单一
- Buff功能基本只影响Buff宿主本身

### Buff的基本框架

整个项目中，可以包含多个BuffList，BuffList仅用方便Buff的分类管理，不参与逻辑
通常情况下同一个玩法下的Buff，或者归属同一个功能管理的Buff都放在一个BuffList下，方便后续管理

每个Buff可以添加多个BuffAction，单个BuffAction的功能单一，通常用于实现一个简单的功能
例如播放特效，或者播放一个角色动画
单个Buff的最终效果由所属的所有BuffAction组合而成，而BuffAction的生命周期也由Buff管理
![企业微信截图_16867094188854.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867094188854.png)

## 新建/删除Buff

---

### 添加一个Buff

- 继承UGCBuffList新建蓝图，命名为MyBuffList
- <span style="color: #ff0000">新建的BuffList需要将其放到Asset\Blueprint\UGCBuffs目录下才能被识别生效，若是没有该目录需要自己新建一个</span>
- 打开MyBuffList，在BuffList中新增一项，在Name中输入需要新建的Buff名，回车保存，对应的Buff蓝图会由编辑器自动新建
![企业微信截图_16867094317361.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867094317361.png)
![企业微信截图_16867094488625.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867094488625.png)
### 删除一个Buff

-<span style="color: #ff0000"> 先从BuffList中删除Buff数据后再手动删除Buff蓝图，否则会引起引用错误</span><br>
![企业微信截图_1686709463911.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686709463911.png)

- 删除BuffList中数据后，再找到对应目录，删除Buff蓝图<br>
![企业微信截图_16867094753692.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867094753692.png)

## Lua中使用Buff

---
### `PlayerPawn`上的3个常用函数，添加，删除，查找

```lua
--判断是否拥有此Buff
HasBuff:fun(BuffName:FName):bool

--移除Buff，可指定只移除层数
RemoveBuff:fun(BuffName:FName,RemoveLayerOnly:bool,BuffApplierActor:AActor):bool

--添加Buff，可指定来源以及添加层数
AddBuff:fun(BuffName:FName,BuffCauser:AController,LayerCount:int32,BuffApplierActor:AActor,CauserActor:AActor):int32
```
- 以我们上面新建的MyBuff为例，最简单的添加方式如下
<details open><summary> <font face="楷体">示例：给角色添加Buff</font> </summary>

```lua
	PlayerPawn:AddBuff("MyBuff", nil, 1, nil, nil)
```
</details>
	
## Buff设置介绍

- 其中，标红为最常用字段

	字段名称|解释
	--|--
	BuffName|Buff名称
	Icon|Buff图标
	Layerable|Buff是否可以叠加层数
	LyaerMax|Buff可叠加的最大层数
	<span style="color: #ff0000"> ValidityTime</span>|<span style="color: #ff0000"> Buff持续时间</span>
	ValidityTimeAccumulable|Buff持续时间是否可以累加
	<span style="color: #ff0000"> MaxValidityTime</span>|<span style="color: #ff0000"> Buff最大持续时间</span>
	BuffConditions|角色状态条件，如果角色不满足状态，Buff失效
	NeedSimulateToClient|是否需要同步到客户端，默认全体广播
	SimulateAddBuffRole|客户端模拟加Buff的规则
	MutexBuffs|Buff互斥，例如Buff_1的互斥中填了Buff_2，那有Buff_1时，无法添加Buff_2
	<span style="color: #ff0000"> BuffActions</span>|<span style="color: #ff0000"> Buff功能</span>
	EventBuffAction|特定事件下触发的Buff功能
	IsAlwaysExists|是否永久存在
	
- `NeedSimulateToClient`的说明

	选项|说明
	--|--
	AddBuffRole_None|无客户端模拟加载
	AddBuffRole_All|所有客户都安模拟加载
	AddBuffRole_Self|自己模拟加载
	AddBuffRole_Causer|施放者模拟加载
	AddBuffRole_Firend|Buff目标以及其队友模拟加载，即Buff目标敌人看不到
	AddBuffRole_Enermy|Buff目标的敌人模拟加载，即Buff目标及其队友看不到
	
	
	
	
	


---


## 自定义自己的BuffAction

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器1.0 > 自定义自己的BuffAction

**涉及API:** `LuaDoAction`, `LuaResetAction`, `LuaUndoAction`, `LuaUpdateAction`

#  自定义自己的BuffAction

### 使用Lua脚本Action

- 在BuffActions中添加新的Action,类型选择Lua脚本Action
- 在LuaFile中填入路径

![企业微信截图_16867095152247.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867095152247.png)

- 对应的脚本路径

![企业微信截图_16867095284718.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16867095284718.png)

- 脚本对应实现如下

```lua
local myBuffAction = {}; 

function myBuffAction:LuaDoAction()
    print("myBuffAction:LuaDoAction")
    return true
end

function myBuffAction:LuaUndoAction()
    print("myBuffAction:LuaUndoAction")
    return true
end

function myBuffAction:LuaResetAction()
    print("myBuffAction:LuaResetAction")
    return true
end

function myBuffAction:LuaUpdateAction(DeltaSeconds)
    print("myBuffAction:LuaUpdateAction:"..DeltaSeconds)
    return true
end


return myBuffAction;
```



---
