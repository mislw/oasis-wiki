# 进阶内容/GamePlay系统/怪物系统/AI编辑器1.0/怪物制作

> 本分类共 7 篇文章

---


## 框架介绍

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 框架介绍

#  框架介绍

## 大致框架图

![企业微信截图_16868159265658.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868159265658.png)

## 几个主要模块

### 模型+动画

- 模型，动画蓝图，动画列表为配套配置
- 模型和动画蓝图必须配套对应，动画列表可以根据实际情况，配置不同状态下的动画

### 碰撞体积，被击体积

- CapsuleComponent决定了碰撞体积
- HitCapsuleComponent决定了被击体积

### 技能管理器

- 技能管理器上配置了所有怪物可以释放的技能

### Ai控制器，行为树

- 行为树控制怪物所有的ai逻辑，黑板提供了变量功能

### 移动代理，寻路网格

- 负责让怪物在场景中移动起来，寻路网格标识了哪些区域是可行走的，哪些区域不可行走



---


## 寻路网格烘焙以及组件配置

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 寻路网格烘焙以及组件配置

**涉及API:** `ComponentManager`, `DataManager`, `ESS_MonsterCrowdMove`, `ESS_Navigation`, `GameMode`, `Navigation`

# 寻路网格烘焙以及组件配置

此教程仅为流程操作教程，更详细的寻路网格教学参见对应的Wiki文档

## 配置地图烘焙区域

---

- 体积中找到寻路网格体边界Volume
  <br>

![企业微信截图_16868159433308.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868159433308.png)

- 场景中编辑Volume的大小，让其包含需要烘焙的地图区域<br>
![企业微信截图_16868159605038.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868159605038.png)
  
![企业微信截图_16868159791766.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868159791766.png)
- 点击构建按钮，等待片刻寻路网格烘焙完成，编辑器中会绘制出可行走区域<br>

![企业微信截图_16868159966974.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868159966974.png)

## 配置GameMode中NavMesh相关组件

---

- `GameMode`中`ComponentManager`中添加`ESS_Navigation`以及`ESS_MonsterCrowdMove`

![企业微信截图_16868160095979.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868160095979.png)

- `GameMode`中`DataManager`中添加`Navigation`
  <br>
![企业微信截图_16868160167153.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868160167153.png)



---


## 新建怪物蓝图并配置动画

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 新建怪物蓝图并配置动画

**涉及API:** `CapsuleHalfHeight`, `CapsuleRadius`, `MoveSpeed`, `UAEMonsterAnimList`

#  新建怪物蓝图并配置动画

## 新建怪物蓝图

---

- 继承STExtraSimpleCharacter创建怪物蓝图

![企业微信截图_16868160436337.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868160436337.png)

- 打开怪物蓝图，配置Mesh，配置碰撞体积，配置被击体积
- 以下图为例：
  - 需要配置CapsuleComponent的`CapsuleHalfHeight`，`CapsuleRadius`
  - 从原本男僵尸蓝图复制HitBox组件过来作为被击体积，配置`CapsuleHalfHeight`，`CapsuleRadius`
  - 配置Mesh，此处配置男僵尸的模型

<details open>
<summary> <font face="楷体">示例：以男僵尸为例</font> </summary>

![企业微信截图_16868160526141.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868160526141.png)
	
---

</details>

## 配置动画蓝图，增加动画列表组件

---

### 配置动画蓝图

- 动画蓝图和模型绑定，上面我们选择使用男僵尸模型，则我们需要找到对应男僵尸的动画蓝图，填入
- 哪种模型使用哪个动画蓝图可以参见和平提供的原生资源

![企业微信截图_16868160878289.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868160878289.png)

### 新建动画列表组件

- 新建`UAEMonsterAnimList`组件
- 根据男僵尸原蓝图上的组件配置，分别填入`动画数据`，`MoveSpeed`，`受击动画和受击距离曲线数据`
- <span style="color: #ff0000">其中，动画数据可以根据自己的实际使用，不同状态配置不同的动作动画</span>

![企业微信截图_16868160965680.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868160965680.png)



---


## 让怪物移动起来

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 让怪物移动起来

**涉及API:** `AIController`, `BaseClass`, `GetBehaviorTreeObjectPath`, `OnPossess`, `RunBehaviorTree`, `SuperClass.OnPossess`, `Target`, `UE.LoadObject`, `UGCMapInfoLib`, `UGCMapInfoLib.GetRootLongPackagePath`, `UGCPlayerPawn`

#  让怪物移动起来

## 创建AIController，行为树，黑板

---

### 创建AIController

- 继承Base AIController，创建我们的AIController
- 怪物蓝图中，AI Controller Class中引用我们创建的AIController
![企业微信截图_16868174471769.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868174471769.png)
![企业微信截图_16868174565388.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868174565388.png)

### 创建行为树，黑板

- 鼠标右键，新建行为树和黑板
  <br>
![企业微信截图_16868174807981.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868174807981.png)

### 配置引用关系

- `AIController`中`Behavior Tree Path`中新增一项，引用新建的行为树
- 打开行为树，`Blackboard Asset`中引用新建的黑板
![企业微信截图_16868174949862.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868174949862.png)
- `AIController`绑定Lua脚本中，添加逻辑，在游戏运行时加载运行行为树
- 在OnPossess中，加载并启动行为树
![企业微信截图_16868175045195.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868175045195.png)

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

## 行为树中添加移动逻辑

- 黑板中添加`Target`变量，`BaseClass`设置为`UGCPlayerPawn`
![企业微信截图_16868175232212.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868175232212.png)
- 行为树中添加寻敌节点，怪物移动节点
- 寻敌节点中，配置寻敌类型为`UGCPlayerPawn`，寻敌目标黑板变量为`Target`，其他设置暂时保持默认值
- 怪物移动节点中，移动目标设置为`Target`，其他设置暂时保持默认值
![企业微信截图_16868175333326.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868175333326.png)
![企业微信截图_16868175411854.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868175411854.png)
- 上述设置代表，行为树在运行过程中，寻敌节点持续寻找`UGCPlayerPawn`类型的对象，并且将寻找到的对象值赋值到`Target`变量上，运行到怪物移动节点时，移动节点会把移动目标设置为`Target`，也就是我们的玩家，怪物就会朝着玩家位置移动



---


## 让怪物释放技能进行攻击

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 让怪物释放技能进行攻击

**涉及API:** `Actor`, `SelfActor`

#  让怪物释放技能进行攻击

## 新建怪物攻击技能

---

- 复制男僵尸现有攻击技能，命名为MonsterAttack
- 技能复制操作，详见技能相关教学Wiki<br>
![企业微信截图_16868175622298.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868175622298.png)
- 给怪物蓝图上添加UAESkillManager，配置相关技能数据，详细配置参见技能相关教学Wiki
![企业微信截图_16868175749527.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868175749527.png)
- UGCGameState中配置MonsterAttack数据，详细配置参见技能相关教学Wiki
![企业微信截图_1686817582870.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686817582870.png)

## 编辑行为树，新增技能释放逻辑

---

- 黑板中添加`SelfActor`变量，类型设置为`Actor`，此处为既定规则，当配置这个变量后，此变量运行时会自动被设置为怪物本身
- 如图新增逻辑，增加`距离判断节点`，`释放技能节点`，`等待节点`
![企业微信截图_1686817590625.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686817590625.png)
- `距离判断节点`中配置了自己和目标的距离，满足配置才执行后续的`释放技能`
- 图中配置的意思是自己和目标小于3米时才释放技能
  <br>
![企业微信截图_1686817639255.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686817639255.png)
- 施放技能中，配置了技能的触发方式和技能id
- 配置技能数据时，我们的技能id为0，所以此处填0
![企业微信截图_16868176491472.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868176491472.png)
- `等待节点`代表释放技能后，执行一个等待，否则怪物会一个接一个的释放技能，中间没有停顿，显得不自然
- `等待节点`可以配一个基础等待实长，并配置时间的随机偏差
![企业微信截图_16868176592685.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868176592685.png)

## 运行测试

- 怪物会跟随玩家移动，并且释放攻击
![企业微信截图_168681766739.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_168681766739.png)



---


## 常用参数和接口详解

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 常用参数和接口详解

#  常用参数和接口详解

## SimpleCharacter下常用属性详解

---

参数|解释
--|--
僵尸之间无伤害|选中后，怪于怪之间不会互相造成伤害
爆炸冲量缩放|被手雷等爆炸物炸中后，击飞冲量权值，愈大飞的越远，建议正常表现填0.3左右 
爆炸冲量缩放Z|对应Z轴上的爆炸冲量缩放
SpeedValueFight|战斗状态下移动速度
SpeedValue|非战斗状态下移动速度
SpeedScale|移动速度缩放
Health|出生时生命值
HealthMax|最大生命值
StunHealthPercentageThreshold|血量低于多少可能出现硬直
StunProbability|低血量硬直概率
StunDuration|硬直状态时间
非战斗状态是否硬直|勾选后，非战斗也会硬直
Can be Pick by Picker|勾选后，可以被技能中的Picker选中
AIController Class|设置怪物使用的AIController

## Skeletal Mesh下常用设置

---

参数|解释
--|--
AnimationMode|一般选AnimationBlueprint，使用动画蓝图形式
AniClass|使用的动画蓝图
SkeletalMesh|模型
Materials|材质





---


## 附件工程

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 怪物制作 > 附件工程

#  附件工程



<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HelloWorld%20.7z">HelloWorld .7z</a>

---
