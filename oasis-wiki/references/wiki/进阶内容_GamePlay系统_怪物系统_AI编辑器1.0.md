# 进阶内容/GamePlay系统/怪物系统/AI编辑器1.0

> 本分类共 4 篇文章

---


## 行为树基本概念

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 行为树基本概念

#  行为树基本概念

如果想要制作一个有挑战的怪物，AI必不可少，下面我们简单介绍一下行为树相关的基本概念。

---

<br>

## AI框架：

![企业微信截图_16868177558214.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868177558214.png)

---

<br>

## 基本概念

<br>

#### 行为树

行为树和蓝图类似，是可视化编程的一种方式。

- 行为树在执行逻辑时，会将信息存储在 黑板 内。
- 行为树按照 从左到右，从上到下的顺序执行逻辑。右上角会有操作的数字顺序
- 行为树由节点组成，不同类型的节点有不同的功能
  <br>

#### 节点

行为树节点执行行为树的主要工作，包括任务执行，逻辑控制，黑板数据更新。
行为树主要分成如下四种类型的节点：

| Node Tyep | 节点类型 | 备注 |
| :--- | :---: | ---: |
| Composite Nodes | 组合节点 | 此类节点定义分支的根以及执行该分支的基本规则。 |
| Task Nodes | 任务节点 | 此类节点是行为树的叶。它们是可执行的操作，没有输出连接。 |
| Service Nodes | 服务节点 | 此类节点附接至合成节点，而且只要其分支正在执行，它们就会按照定义的频率执行。它们通常用于检查和更新黑板。它们取代了其他行为树系统中的传统并行节点。 |
| Conditionals | 条件节点 | 此类节点连接到另一节点，并决定树中的分支、甚至单个节点能否被执行。 |

<br>

#### 条件节点

条件有一个特殊的属性，观察者终止(打断类型)，该属性的含义如下：

| 观察者终止类型 | 效果 |
| :--- | :---: |
| None | 不打断 |
| Self | 打断自身节点和自身节点的子树 |
| Lower Priority | 打断优先级比自身节点低的所有子树 |
| Both | 打断自身节点，自身节点的子树和优先级比自身节点低的所有子树 |

<br>

#### 组合节点

组合节点定义了行为树的根，主要有三种：选择器，序列，简单平行节点。

| Node Type | 节点类型 | 备注 |
| :--- | :---: | ---: |
| Selector | 选择器 | 按从左到右的顺序执行其子节点。当其中一个子节点执行成功时，选择器节点将停止执行。如果选择器的一个子节点成功运行，则选择器运行成功。如果选择器的所有子节点运行失败，则选择器运行失败。  |
| Sequence | 序列 | 从左到右的顺序执行其子节点。当其中一个子节点失败时，序列节点也将停止执行。如果有子节点失败，那么序列就会失败。如果该序列的所有子节点运行都成功执行，则序列节点成功。 |
| Simple Parallel | 简单平行 | “同时”运行多个子节点，但节点的结束由主节点控制，主节点只能是任务节点 |



---


## 使用导航网格NavMesh

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 使用导航网格NavMesh

# 使用导航网格(NavMesh)

想让游戏中的动态物体能够自动寻路，就少不了使用导航网格(NavMesh)技术，下面会逐步介绍如何使用导航网格技术让你的怪物“动起来”。

---

<br>

## 流程

![企业微信截图_16868177879723.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868177879723.png)

---

<br>

## 实战演练

<br>

#### 准备工作

1.以系统模板 Template_demolition 创建工程。
<br>
2.由于该工程下demolition地图的navmesh已经烘焙完成，我们删除Asset/Map/demolition文件夹中的demolition.navmesh：
<br>
![企业微信截图_16868177972290.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868177972290.png)
![企业微信截图_1686817808858.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686817808858.png)

3.调试游戏，会发现在游戏中，NPC已经无法移动。
<br>
4.在世界大纲视图中删除导航网格体积，构建项目后，启动游戏，会发现在游戏中，NPC依然无法移动。这是因为我们删除导航网格体积间接调整了地图生成的导航网格数据。
<br>
![企业微信截图_16868178304836.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868178304836.png)

#### 实战

1.拖动 放置Actor面板 中的 体积 -> 寻路网格体边界Volume 到 视口中，生成对应的Actor。
<br>
![企业微信截图_1686818377394.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686818377394.png)

2.调整寻路网格体积大小，使得覆盖整个场景的可移动区域。
<br>
![企业微信截图_16868184008953.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868184008953.png)

3.点击构建，生成Navmesh数据。其中Navmesh数据会生成在和在一个和关卡同一个目录，并且和关卡同名的文件夹中。
<br>
例如Asset/Map/demolition.umap会生成Asset/Map/demolition/demolition.navmesh 的数据
<br>
![企业微信截图_16868184181439.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868184181439.png)

4.打开Asset/Blueprint/BurstGameMode，并设置开启Navigation功能，设置对应的参数：
<br>
![企业微信截图_16868184337876.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868184337876.png)

其中Nava Data Path就是刚才生成的Navmesh数据的位置
5.现在你已经可以在AI中使用相关的移动节点了(比如使用 主角移动 节点）
<br>
![企业微信截图_16868187545803.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868187545803.png)

6.启动游戏，你会发现NPC已经可以移动了。



---


## 利用和平的角色拓展玩法内容

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 利用和平的角色拓展玩法内容

**涉及API:** `AIPlayerKey`, `UGCFakePlayerSystem`, `UGCFakePlayerSystem.GetRandomAIPlayerKey`, `UGCFakePlayerSystem.SpawnFakePlayer`

# 利用和平的角色拓展玩法内容

## 简介

在绿洲启元编辑器中，我们可以复用和平精英已经制作好的角色丰富自己的玩法。

## 角色框架

在和平精英中，角色分成 玩家，怪物和动物三大类，怪物有狼，僵尸，动物里面还有鹿，狍子等，可参考：

<br>

![企业微信截图_16868187749302.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868187749302.png)

## 制作规范

根据角色框架，Pawn，AIController，会影响BT能够生效的节点，一般说来，角色类型决定了Pawn,AIController的基类，和能够使用的BT节点，参考：

| 类型 | Pawn父类(间接) | AIController父类 | 支持的和平BT节点 |
| ------ | ------ | ------ | ------ |
| 玩家(机器人) | STExtraPlayerCharacter | New Fake Player AIController | 通用，角色，玩家 |
| 怪物 | STExtraSimpleCharacter | Mob AIController | 通用，角色，怪物 |
| 动物 | STAnimalCharacter | Animal AIController | 通用，角色，动物 |

注：

<br>

1.复用和平的角色，尽量直接继承已经配置好的pawn蓝图类(例如： 和平精英/怪物/狼/Wolf/SC_WereWolf/BPPawn_Escape_WereWolf1.BPPawn_Escape_WereWolf1_C)，没有额外需求，尽量少的直接继承STExtraPlayerCharacter，STExtraSimpleCharacter，STAnimalCharacter这些类。

<br>

2.制作机器人的时候，可以直接复用UGCPlayerPawn

<br>

## 机器人

#### 配置规范

1.在GameMode中 配置GMComponentManager 和 GMDataManager，并在GMData Source AIProbe中配置AIController

<br>

![企业微信截图_16868187931774.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868187931774.png)

2.在AIController中 配置 BT 和 Character

<br>

![企业微信截图_16868188081531.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868188081531.png)

<br>

#### 使用方法

参考：

```lua
local AIPlayerKey = UGCFakePlayerSystem.GetRandomAIPlayerKey()
UGCFakePlayerSystem.SpawnFakePlayer(AIPlayerKey)
```

## 怪物和动物

#### 配置规范

1.在pawn中配置controller

<br>

![企业微信截图_16868188193517.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868188193517.png)

<br>

2.在controller中配置BehaviorTree

<br>

![企业微信截图_16868188391992.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868188391992.png)

<br>

## 注意事项

1.使用和平的AIController不需要在脚本中runBT，和平的AIController会自动的运行BehaviorTree

<br>

2.如果不使用和平的AIController，有些BT节点不能保证有效

<br>

3.部分节点生效还需要有其他正确的配置，比如移动相关节点，还需要正确配置Navigation

<br>

## 附件




<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FakePlayerDemo.zip">FakePlayerDemo.zip</a>
<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AnimalAndMonster.zip">AnimalAndMonster.zip</a>

---


## 自定义节点

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 自定义节点

#  自定义节点

在使用AI编辑器的过程中，也可以创建自定义节点，并用蓝图Lua来编写自定义节点的逻辑。

<br>

## 使用流程

1. 可以在行为树编辑器选择自定义节点的父类，并创建自定义节点

![企业微信截图_16873298173096.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873298173096.png)

>创建节点后，将在BT同名文件夹下创建对应的蓝图类。建议更换自定义节点蓝图的名字，使其更加符合需求逻辑。

2. 双击打开创建的自定义节点，可以使用蓝图Lua编写自定义节点的逻辑

![企业微信截图_16873298326585.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873298326585.png)

3. 编写完自定义节点的逻辑，便可以在行为树编辑器使用该节点

![企业微信截图_16967520885570.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3EKZo%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16967520885570.png)

<br>

## 常用节点Lua事件

和普通蓝图不一样，自定义行为树节点有自己独有的Lua事件。

### 任务节点

```
-- 执行节点的时候触发，只有调用FinishExecute(),才会改变节点运行状态
-- 需要调用self.bNotifyTick = true，ReceiveTickAI才会生效
function BTTask_LuaBase_New:ReceiveExecuteAI(OwnerController, ControlledPawn)
--    self:FinishExecute(true)
end

-- tick function
function BTTask_LuaBase_New:ReceiveTickAI(OwnerController, ControlledPawn, DeltaSeconds)

end
```

### 条件节点

```
-- "所属的节点"可以执行时，检查条件调用的事件
-- 需要调用self.bNotifyTick = true，ReceiveTickAI才会生效
function BTCondition_LuaBase_New:PerformConditionCheckAI(OwnerController, ControlledPawn)
    return false
end

-- tick function
function BTCondition_LuaBase_New:ReceiveTickAI(OwnerController, ControlledPawn, DeltaSeconds)

end

-- "所属的节点"执行前,执行
function BTCondition_LuaBase_New:ReceiveExecutionStartAI(OwnerController, ControlledPawn)

end

-- "所属的节点"执行结束后，执行
function BTCondition_LuaBase_New:ReceiveExecutionFinishAI(OwnerController, ControlledPawn, NodeResult)

end
```

### 服务节点

```
-- tick function
function BTAttachment_LuaBase_New:ReceiveTickAI(OwnerController, ControlledPawn, DeltaSeconds)

end

-- "所属节点"被激活后
function BTAttachment_LuaBase_New:ReceiveActivationAI(OwnerController, ControlledPawn)

end

-- "所属节点"结束执行后
function BTAttachment_LuaBase_New:ReceiveDeactivationAI(OwnerController, ControlledPawn)

end
```



---
