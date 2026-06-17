# 进阶内容/GamePlay系统/怪物系统

> 本分类共 17 篇文章

---


## 怪物动画蓝图复用功能

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物动画蓝图复用功能

**涉及API:** `BP_Magic_Master`

# 怪物动画蓝图复用功能

怪物动画基于骨骼网格体（Skeletal Mesh，即骨骼模型）创建，一个动画资源定义一组帧动画序列，为了表现更丰富和控制更复杂的交互动画行为，需要将不同的动画序列进行关联混合，这通常由 [动画蓝图](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-blueprints-in-unreal-engine) 中的状态与逻辑控制来共同驱动动画姿态的输出，因此最终的动画表现依赖于动画蓝图的实现。

由于怪物的类型与配套的动画资源繁多，为每一种怪物实现一套动画蓝图带来的制作成本和管理维护成本很高，为了解决怪物动画播放的问题，对此提供了怪物动画蓝图复用的功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/beRFuimage.png)

<br>

## 使用步骤

复用动画蓝图的过程主要分为三个步骤：
1. **创建基准怪物蓝图：** 找到具备动画蓝图且各项动画表现正常的怪物，基于该怪物基类创建子类蓝图
2. **替换骨骼网格体：** 替换基准怪物蓝图的Mesh为目标怪物的骨骼网格体（骨骼模型）
3. **配置动画资源：** 将基准怪物蓝图AnimList中的动画资源替换为目标怪物的匹配动画资源（包含动画序列、蒙太奇或者混合空间）

下面将结合 *砍刀怪复用法师怪动画蓝图* 的场景作为案例讲解具体的使用方式。

### 创建基准怪物蓝图

首先，基于法师怪蓝图基类（UGC_Master_BP）创建法师怪的子类蓝图，命名为 ``BP_Magic_Master``。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7WgHtimage.png)

---

### 替换骨骼网格体

打开创建出的法师怪子类蓝图BP_Magic_Master，将法师怪的Mesh替换为砍刀怪的骨骼网格体（SK_UGC_Machete_B）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/f8pX7image.png)

---

### 配置动画资源

在法师怪蓝图中找到动画列表组件（UAEMonsterAnimList），组件的属性 ``UAEMonsterAnimListComponentBase > 动画数据（MosterAnimDatas）`` 下配置了法师怪在不同行为状态下使用的动画资源，需要将各动画资源替换为砍刀怪的匹配动画资源。
> 不同怪物使用的动画列表组件类型可能不同，以实际蓝图配置为准

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/W0EGNimage.png)

以替换“原地待机”状态的动画为例，查找砍刀怪的待机动画资源有两种方式：
- 双击砍刀怪的骨骼网格体会进入骨骼网格体编辑窗口，此处右上角自动关联了动画编辑窗口的入口<br>
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rRbFfimage.png)

	点击进入动画编辑窗口，在资源浏览器内会筛选出适合砍刀怪的所有动画资源<br>
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pLB3nimage.png)
- 使用 ``浏览到内容浏览器资源`` 跳转到砍刀怪骨骼网格体所在的资源目录，在动画子目录下即为砍刀怪的配套动画资源<br>
	> 不同怪物的目录结构可能不同，且部分同骨骼的通用动画资源可能不在怪物自身目录内

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ssVAzimage.png)

将砍刀怪待机动画序列替换为 ``【待机】原地待机(UAnimSequence)`` 类型的引用资源，这样砍刀怪在待机的状态下即会播放对应的动画效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ERzPMimage.png)

其他类型的动画资源替换方式同理，但需要注意：<span style="color:red">不同姿态类型所引用的资源类型可能不同，要确保资源类型的一致性</span>

> 建议将砍刀怪的AnimList直接复制给法师怪，避免资源配置的失误和遗漏

---

### 测试效果

将法师怪放置在场景中，[启动PIE调试](https://developer.gp.qq.com/wikieditor/?timeStamp=1718884727319#/catalog/307)，可以看到待机动画已关联至砍刀怪的动画表现，意味着动画蓝图复用成功。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KOgVximage.png)

<br>

## 注意事项

**1. 替换骨骼网格体后检查物理资产**

	怪物的碰撞检测及受击判定依赖于物理资产，因此需要检查骨骼网格体是否配备了有效的物理资产，可以通过以下方式进行检查：
- 骨骼网格体资产详情处是否配置了物理资产<br>
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JN1jEimage.png)
	
- 如果没有物理资产，可以在怪物蓝图Mesh组件的 ``物理资产覆盖（PhysicsAssetOverride）`` 处进行覆盖配置；如果已配置，则可置空<br>
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qcbIiimage.png)

**2. 动画资源的替换需要保证引用资源类型的一致性**

	动画数据中各姿态类型明确定义了所使用的资源类型，如果资源类型不匹配会导致无动画表现或者动画异常的现象。	

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fFHP1image.png)

- UAnimSequenc：动画序列资源
- UAnimMontage：动画蒙太奇资源
- UBlendSpace：混合空间资源

如果怪物没有配备对应的 [动画蒙太奇资源](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/creating-an-animation-montage?application_version=4.27) 或者 [混合空间资源](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/creating-blend-spaces?application_version=4.27)，可以用相关的动画序列资源进行创建和配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/a0O6cimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HCRBKimage.png)

> 如果缺少怪物本体的动画序列资源，可以使用相近骨骼的动画序列替代，但骨骼的类型跨度不要太大，例如：仿生体骨骼的怪物不适合使用动物骨骼的动画序列资源

另外，对于蒙太奇资源来说，需要额外检查蒙太奇引用的动画插槽，保证目标怪的插槽与基准怪一致，否则无法正确播放动画；如果没有对应的插槽，可以自行 [创建同名插槽](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/editing-an-animation-montage?application_version=4.27)：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MPI8Yimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wHN7jimage.png)

---


## 怪物快速配置指南

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物快速配置指南

**涉及API:** `AIWorldVolume`, `AttrModifyComp`, `BehaviorControlComp`, `Filter`, `GetEntityTypeTag`, `LogicPartManagerComp`, `PESkill_Monster_Claw`, `PersistBaseComponent`, `SetEntityTypeTag`, `TakeDamageLogicComp`, `UGCGameState`, `UGCGameplayTagSystem`, `UGCGameplayTagSystem.RequestGameplayTag`, `UGCPresetCommonDropItemComponent`, `UGC怪物行为树`

# 怪物快速配置指南

怪物是具备属性和状态的游戏对象，拥有独特的外观、行为模式和能力，是丰富游戏场景和强调互动性与游戏体验的重要元素，以下将以简单的怪物示例介绍如何快速创建与配置一个怪物。

<br>

## 配置依赖

怪物的移动行为依赖寻路系统，通过导航网格生成可移动区域，同时 ``AIWorldVolume`` 赋予识别交互对象的能力等，因此需要完成前置的配置事项，可参考 [导航网格配置](https://developer.gp.qq.com/wikieditor/#/catalog/20266)。

<br>

## 创建怪物蓝图

编辑器菜单栏点击【实体编辑器】按钮，打开实体编辑器操作界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LtxN6image.png)

1. 从“怪物模板”窗口中选择近战小怪模板，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``近战小怪模板`` 为模板创建”

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YG6AAimage.png)
2. 点击“以 ``近战小怪模板`` 为模板创建” 按钮，弹出输入名称弹窗，输入怪物蓝图名称并点击确定
3. 新建的怪物蓝图将显示在“工程实体资源”窗口中，且怪物蓝图创建于 ``Asset/Blueprint/Prefabs/Monsters`` 路径下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nkWhyimage.png)

<br>

## 配置怪物能力

怪物具有属性、阵营、技能和行为逻辑等基础能力，也可以为怪物添加伤害飘字、死亡掉落等其他功能。

### 基础信息

怪物蓝图中的【细节】面板可以设置 [怪物血条](https://developer.gp.qq.com/wikieditor/#/catalog/20145)、怪物名称和阵营等基础信息。

在怪物蓝图中将 ``Character Name`` 属性改为“弓箭手”，血条保持默认显示效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dxrk6image.png)

> 如果调试时怪物无法被攻击，需要确认怪物与玩家的阵营关系是否正确，可以参考 [配置阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%85%8D%E7%BD%AE%E9%98%B5%E8%90%A5)

---

### 实体类型

可以为各类怪物设置自定义的实体类型标签，例如精灵、机械兽、龙族等，实体类型标签也是一类基于 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 定义的概念性标签，怪物基类提供了 ``SetEntityTypeTag`` 与 ``GetEntityTypeTag`` 函数用于运行时动态设置/查询实体类型标签。

示例代码：

```lua
-- 设置实体类型标签
local EntityTypeTag = UGCGameplayTagSystem.RequestGameplayTag("LogicPart.Filter.EntityType.Melee")
MonsterObject:SetEntityTypeTag(EntityTypeTag)

-- 查询实体类型标签
local TagInfo = MonsterObject:GetEntityTypeTag()
ugcprint(string.format("Monster Entity Type: %s", TagInfo.TagName))
```

---

### 怪物行为

怪物的行为逻辑通过 [行为树](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/behavior-tree-in-unreal-engine---overview?application_version=5.5) 进行驱动，怪物系统已经为模板怪物默认添加了 ``UGC怪物行为树`` 模板，涵盖了常用的寻敌、巡逻、攻击等行为，且经由行为控制组件 ``BehaviorControlComp`` 反射行为树部分黑板变量，可以直接在蓝图中修改行为属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qn5aZimage.png)

---

### 逻辑管理组件

[逻辑管理组件](https://developer.gp.qq.com/wikieditor/#/catalog/20162) ``LogicPartManagerComp`` 在行为树模板的基础上抽象封装了一套逻辑模块组件，在不修改行为树的前提下仅通过蓝图配置实现不同行为模式的怪物。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l4v1Aimage.png)

---

### 怪物动画

怪物蓝图的动画列表组件支持自定义修改怪物动画，默认提供了受击、死亡、休闲移动、战斗移动、休闲Idle和战斗Idle等六种状态动画，同时也支持 [怪物动画蓝图复用功能](https://developer.gp.qq.com/wikieditor/#/catalog/20017) 用于怪物“换皮”。

> 需要确保替换的动画资源的骨骼与怪物骨骼类型一致

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QJ47Yimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eHizWimage.png)

---

### 修改初始属性
 
怪物蓝图的属性修改组件提供基于 [属性管理器](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E5%B1%9E%E6%80%A7%E7%AE%A1%E7%90%86%E5%99%A8) 的属性初始值修改能力。

在怪物蓝图的 ``AttrModifyComp`` 组件中为“属性初始值配置”添加 ``血量`` 和 ``最大血量`` 两项修改，初始值均设置为300。

> 如果待修改属性具备相应最大值属性，通常需要同步修改

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DMrCRimage.png)
 
---

### 添加怪物技能

怪物释放技能的行为由行为树的逻辑驱动，[释放技能](https://developer.gp.qq.com/wikieditor/#/catalog/20179?autoJump=[Generic]%E6%96%BD%E6%94%BE%E6%8A%80%E8%83%BD) 任务节点提供 [虚拟技能槽](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 的参数配置，该节点的执行将触发对应槽位的技能。

怪物蓝图的 ```PersistBaseComponent``` 组件关联虚拟技能槽与技能蓝图，将 ``Skill.Slot.Main`` 槽位绑定的技能改为 ``PESkill_Monster_Claw``。

> 行为树模板默认使用的释放技能槽位是 ``Skill.Slot.Main``

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5SLLLimage.png)

---

### 添加死亡掉落

怪物的死亡固定会触发掉落行为，通过 [掉落组件](https://developer.gp.qq.com/wikieditor/#/catalog/20142) 可以配置需要掉落的物品信息。

在怪物蓝图的 ```UGCPresetCommonDropItemComponent``` 组件中通过 ``蓝图配置`` 的方式掉落 ``Item ID`` 为831101003的物品，数量为1，掉落物类型选择为“Wrapper”，掉落效果为立即掉出1份该物品。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/g8JcZimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/L5WRJimage.png)

---

### 添加伤害飘字

为怪物添加伤害飘字的效果，在怪物蓝图的 ``TakeDamageLogicComp`` 组件中确认 ``伤害冒字`` 属性处于勾选状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8juouimage.png)

同时打开 ``UGCGameState`` 蓝图，确保 ``Enable Damage Number Pack for Generic Character`` 属性也处于勾选状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hXLmAimage.png)

> 如果调试时没有正确显示飘字效果，可参考 [通用伤害飘字](https://developer.gp.qq.com/wikieditor/#/catalog/20160) 的属性说明进行检查

<br>

## 怪物调试

点击怪物蓝图菜单栏的【浏览】按钮，内容浏览器将自动跳转到该怪物蓝图所处的目录下。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ei7TQimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/57SUlimage.png)

选中怪物蓝图放置到关卡场景的可移动区域范围内，启动 [Debug调试](https://developer.gp.qq.com/wikieditor/#/catalog/307) 观察怪物的行为。

![QQ202571-16030-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KS69pQQ202571-16030-HD-ezgif.com-video-to-gif-converter.gif)。

怪物默认处于巡逻状态，玩家靠近且在视野范围内时开始追击，当到达 ``追击距离`` 且处于 ``攻击距离`` 范围内时触发攻击行为，由于将怪物的技能替换为近战怪的攻击技能，因此怪物在进入远程攻击范围内时即开始攻击。

如果希望观察怪物实时的行为数据，可以通过 [怪物调试工具](https://developer.gp.qq.com/wikieditor/#/catalog/20161) 进行进一步的调试。

> ``追击距离`` 执行优先级高于 ``攻击距离``，如果未到达 ``追击距离`` 但满足 ``攻击距离`` 条件，此时并不会打断追击行为，仍会继续移动

---


## 怪物血条

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物血条

**涉及API:** `BP_CharacterHPChange`, `BP_CharacterNameChange`, `DA_GameModeGeneral`, `Event_InitParamEnd`, `FName`, `UGCGenericCharacterPositionWidget`, `UGC_BOSS_Generic_HealthBar_UIBP`, `UGC_NPC_Generic_HealthBar_UIBP`

# 怪物血条

怪物血条通过UI元件的形式提供组件化的使用方式，开发者可以设置血条的样式，同时怪物实体蓝图支持更加自定义的血条显示效果。

<br>

## 给怪物配置血条

###  创建怪物血条

编辑器内容浏览器中右键 ``蓝图类``，继承自 ``UGC_NPC_Generic_HealthBar_UIBP`` 或者 ``UGC_BOSS_Generic_HealthBar_UIBP`` 创建子蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ivirVimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tHIU3image.png)

``UGC_NPC_Generic_HealthBar_UIBP`` 是普通小怪的血条样式，``UGC_BOSS_Generic_HealthBar_UIBP`` 是BOSS怪的血条样式，两者配置项一样仅在样式上有些许差异。

普通小怪血条样式：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EE5ZMimage.png)

Boss怪血条样式：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BGS7Eimage.png)

<br>

### 配置血条样式

打开创建好的血条元件蓝图，选中结构树根节点，右侧【详细信息】面板中展示所有可配置的属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MA13gimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/in7aximage.png)

|属性名|属性说明|
|-|-|
|Is Show Name|是否显示怪物的名字，怪物的名字文本由 [怪物蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20144?autoJump=%E5%88%9B%E5%BB%BA%E6%80%AA%E7%89%A9%E8%93%9D%E5%9B%BE) 配置的 ``Character Name`` 属性决定<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0nc7Timage.png)|
|Is Show Blood Num|是否显示血条数值，样式为“当前值/最大值”<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CNmk9image.png)|
|Blood Fill Image|一组血量百分比及显示颜色的映射关系，表示当前血量<=此百分比时血条显示的颜色，例如血量低于或等于50%时血条颜色为鲜红色：<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NM4qjimage.png)|
|Background Image|血条背景图样式<br> ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yfpNzimage.png) <br> ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Qj36Aimage.png)
|Health Pre Deduct Fill Image|血条预扣除的颜色样式，即血量实际变化前的预显示颜色，例如预扣除颜色为白色的效果：<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4cFXEimage.png)|
|Game Attribute Fill Image Map|支持追加显示额外的属性条，需要绑定属性及配置颜色样式，配置内容等同于血条<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PyUwoimage.png)|

配置完成后需要编译并保存才能生效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pkRLPimage.png)

<br>

### 为怪物添加血条

通过实体编辑器 [创建一个怪物蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20144?autoJump=%E5%88%9B%E5%BB%BA%E6%80%AA%E7%89%A9%E8%93%9D%E5%9B%BE)，在怪物蓝图【细节】面板的“Health Bar”类别下，将血条组件配置到 ``控件蓝图路径`` 属性上即为怪物赋予了血条功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SdqWgimage.png)

效果如图所示：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rkWekimage.png)

<br>


## 设置显示效果

怪物蓝图中除了关联血条元件，还集成了对血条功能的配置项，可以自定义血条的挂载位置、显示距离等多种规则。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mp8nlimage.png)

|属性名|属性说明|
|-|-|
|控件蓝图路径|血条元件的蓝图类|
|被遮挡后是否显示|若勾选，则当怪物被障碍物阻挡时仍会显示血条|
|实时显示最大距离CM|当玩家与怪物的距离小于该值时，血条会一直显示（单位：厘米）<br>![2025-06-1015-39-09-ezgif.com-cut.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/alYT72025-06-1015-39-09-ezgif.com-cut.gif)<br>目前最多支持同时显示20组怪物血条，超过时优先显示距离玩家最近的怪物血条<br>如果设置为0，就会关闭玩家靠近实时显示血条的功能，但不会影响其他显示血条的方式|
|是否绑定到特定部位|默认使用怪物Actor的坐标为基础位置，若勾选则将绑定到怪物的指定部位上|
|部位名|绑定部分的名称，默认为head头部，可以参考怪物骨骼进行配置，怪物骨骼上的挂点均可使用<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/B61Baimage.png)|
|位置偏移|血条显示位置相对于特定部位（绑定了特定部位）或Actor的坐标（未绑定特定部位）的位置偏移|
|受击后显示|若勾选，怪物受到攻击后就会显示血条<br>![ezgif.com-crop (1).gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9o5Saezgif.com-crop%20(1).gif)<br>若不勾选，则怪物受击后不会因此显示血条，不影响到其他的显示规则|
|锁定玩家时显示|若勾选，玩家被怪物锁定或玩家身上有怪物仇恨时，怪物就会显示血条<br>![2025-06-1016-02-25-ezgif.com-crop.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0sydm2025-06-1016-02-25-ezgif.com-crop.gif)<br>若不勾选，怪物锁定玩家后不会因此显示血条，不影响其他显示规则|
|被瞄准时显示|若勾选，怪物被玩家瞄准时会显示血条，若不勾选，怪物被瞄准后不会因此显示血条，不影响其他显示规则|
|条件显示最大距离CM|勾选了 ``被瞄准时显示`` 时生效，触发被瞄准显示的最大距离（单位：厘米），超过这个距离后玩家瞄准怪物不会显示怪物血条<br>![ezgif.com-crop.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FH3qJezgif.com-crop.gif)|
|显示时间|不满足血条显示的条件时，多长时间内血条消失（单位：秒），包括：怪物未受击、怪物不再锁定玩家、怪物不再被瞄准（包括超出被瞄准时最大显示距离）|
|CampFilter|基于 [阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%98%B5%E8%90%A5%E7%B3%BB%E7%BB%9F) 的过滤器，怪物与玩家之间的阵营关系匹配该条件时才会显示血条|
|受伤显示类型|血条可见性目标的范围<br>- 仅伤害来源显示：血条只会对伤害来源的目标显示<br>- 伤害来源同阵营均显示：血条会对伤害来源的同阵营中的所有目标显示|

血条显示的逻辑流程图如下：

<div style="text-align: center;">
	<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gnGOF%E8%A1%80%E6%9D%A1%E9%80%BB%E8%BE%91%E6%B5%81%E7%A8%8B%E5%9B%BE.png">
</div>
	
<br>

## 全局血条数量限制

怪物系统支持设置全局可见的血条数量，点击编辑器菜单栏的【玩法通用设置】按钮，在 ``DA_GameModeGeneral`` 数据资产蓝图中找到 ``血条显示最大数量`` 属性，设置并保存后即可生效，当血条显示逻辑流程图判定可显示的血条数量超过该设置值时，将按照距离由远至近逐一剔除血条。

> 全局血条数量设为0代表不显示血条，基于性能考虑，建议开发者设置一个合理值

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yKjiQimage.png)

<br>

## 自定义血条控件

基于UI元件的性质，怪物血条控件蓝图的扩展灵活性有限，如果希望自定义血条，可以通过派生自 ``UGCGenericCharacterPositionWidget`` 蓝图新建血条控件来实现。

右键 ``蓝图类``，继承自 ``UGCGenericCharacterPositionWidget`` 创建子蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nszGGimage.png)

按需求添加所需的控件元素，例如通过子控件的方式引用血条控件（拖动血条控件时需拖进层次结构中），并在其下方添加一行包含文本与图片的水平框控件，新增控件行与血条控件通过垂直框进行上下布局。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dQtisimage.png)

点击 【UMG Lua】按钮，设置血条组件的逻辑实现血条名字，血量的变化。
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
将此控件蓝图绑定至怪物蓝图的 ``控件蓝图路径``，启动调试运行即可观察自定义的控件效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l7gtMimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/h7UsPimage.png)

<br>

## 注意事项

1. 单客户端触发怪物的血条显示后，将同步至其他满足条件的客户端可见
2. 怪物血条显示方式可以使用多种搭配，只要满足任意一个配置方式就可以显示怪物血条，不会因为某个方式没激活或反激活使得别的显示方式不生效

---


## 怪物刷新器

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物刷新器

**涉及API:** `Attr`, `AttrItem`, `AttributeName`, `Attributes`, `BP_UGCMobSpawner`, `BP_UGCMobSpawnerManager`, `CustomSpawnMob`, `FinallyMonsterID`, `GetFollowWayPointPartInterface`, `GetLogicPartManagerInterface`, `GetMonsterAttributes`, `GetMonsterClass`, `InitMonsterAttr`, `K2_GetActorLocation`, `SetValueAsBool`, `SetWaypoints`, `SpawnMob`, `StartSpawnerManager`, `UGCAttributeSystem`, `UGCAttributeSystem.SetGameAttributeValue`

# 怪物刷新器

怪物刷新器提供蓝图配置化的方式帮助开发者管理怪物的生成和刷新规则，支持单刷新点及按波次刷怪两种形式，开发者能够更方便、灵活地实现怪物刷新机制。

<br>

## 怪物刷新器概述 

怪物刷新器由刷怪策略、刷新点和刷怪管理器三部分组成，刷怪策略决定生成什么样的怪物，刷新点指定怪物刷新的位置，刷怪管理器负责调度和管理刷新流程，其中刷新点可以不依赖于刷怪管理器而独立实现怪物的刷新。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/j4j2fimage.png)

- 刷怪策略：通过 ``UGCMobGroup`` 怪物组表提供刷怪策略的配置，每一组配置即是一套怪物生成规则，刷新点和刷怪管理器都基于该表来决定如何生成怪物
- 刷新点：刷新点是一个蓝图类对象，放置在关卡场景中使用，用来指定怪物的刷新位置和刷新数量。设置刷怪策略后刷新点可以单独刷怪，也可以结合刷怪管理器使用，由刷怪管理器控制刷怪流程，刷新点只提供坐标和生成规则
- 刷怪管理器：刷怪管理器是一个蓝图类对象，负责管理整个刷怪流程，以波次的形式触发刷新点的执行，因此刷怪管理器必须配合刷新点使用；场景中允许存在多个刷怪管理器，各管理器之间互不干扰，独立管理各自的刷怪流程

<br>

## 怪物组表

在编辑器主界面的工具栏，点击进入【表格管理器】。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EpXkkimage.png)

在【表格类型区】选择“功能表格”，然后在【表格浏览区】的【Template】单击选择“怪物组表”，点击“选择模板创建”后，成功创建 ``UGCMobGroup`` 怪物组表。

![怪物组表.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fbOFe%E6%80%AA%E7%89%A9%E7%BB%84%E8%A1%A8.drawio.png)

双击打开 ``UGCMobGroup`` 怪物组表，可配置多组生成规则，每组包含怪物的种类、阵营、生成权重和初始属性值等属性。

![image.14.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gl5Joimage.14.png)

|属性名|属性说明|
|-|-|
|怪物组ID|每组生成规则的唯一ID，被刷新点引用|
|怪物阵营|怪物所属的 [阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%98%B5%E8%90%A5%E7%B3%BB%E7%BB%9F)|
|怪物类型|基于实体编辑器创建的 [怪物蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20144?autoJump=%E5%88%9B%E5%BB%BA%E6%80%AA%E7%89%A9%E8%93%9D%E5%9B%BE)|
|怪物权重|该怪物的生成权重，当列表配置了多种怪物时，该怪物的刷出概率为其 ``怪物权重/权重之和``，权重的形式保证每次必定有一个怪物能被生成|
|出生属性|支持为怪物设置初始属性值|

<br>

## 怪物刷新点

编辑器内容浏览器右键 ``蓝图类``，继承自 ``BP_UGCMobSpawner`` 创建子蓝图类。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5skdJimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2xPBYimage.png)

### 配置刷新点

怪物生成的位置取决于刷新点的坐标位置，因此需要把刷新点蓝图放置在关卡中期望刷出怪物的目标位置，此时将生成实例化对象。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5cRN6image.png)

选中关卡中的刷新点实例对象，在实例对象【细节】面板编辑刷新点属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vVgN9image.png)


|属性名|属性说明|
|-|-|
|刷出的怪物阵营|默认为-1表示使用 [怪物蓝图中配置的阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E8%AE%BE%E7%BD%AE%E6%80%AA%E7%89%A9%E9%98%B5%E8%90%A5) ，若大于-1则会将此数据覆盖到刷出的怪物上|
|刷怪器控制模式|- 管理器控制：需要使用**刷怪管理器**引用这个刷怪点才可以让其刷怪<br>- 最大数量控制：刷怪点自动刷怪，仅当场上怪物数量 < ``最大存活数量`` 时才继续刷怪，同时刷怪总量仍然受最大/最小生成数量约束<br>- 无控制：刷怪点自动刷怪，且不受其他条件控制|
|最大存活数量|仅对 ``刷怪器控制模式`` 为“最大数量控制”时生效，通常该设定值建议小于最小生成数量；例如设置为1，则代表怪物死亡一个再补充一个，直到刷出怪物的总量为最大刷怪数量为止|
|怪物配置模式|支持蓝图配置，怪物组表，自定义三种模式<br>- 蓝图配置：``怪物蓝图`` 属性可配，指定怪物蓝图类，刷固定种类的怪物<br>- 怪物组表：``怪物组ID`` 属性可配，指定使用的刷怪策略<br>- 自定义参数：``自定义参数`` 属性可配，可添加任意组KV结构的元素，通过 ``自定义刷新规则`` 实现怪物的生成|
|使用NavMesh找随机点|是否优先在被 [导航网格](https://developer.gp.qq.com/wikieditor/#/catalog/20151) 覆盖的范围内刷怪|
|随机朝向|怪物生成后的初始朝向，默认使用刷新点蓝图箭头组件的方向，否则随机朝向|
|生成范围|刷新器以自身为中心的圆柱范围内寻找合适位置，生成范围为圆柱的半径（单位：厘米）|
|生成高度范围|刷新器以自身为中心的圆柱范围内寻找合适位置，生成高度范围为圆柱的高度（单位：厘米）|
|最小生成数量|- 当刷新器独立刷怪时，为可生成怪物总数量的最小值<br>- 当配合刷怪管理器使用时，为每波次生成怪物数量的最小值|
|最大生成数量|- 当刷新器独立刷怪时，为可生成怪物总数量的最大值<br>- 当配合刷怪管理器使用时，为每波次生成怪物数量的最大值|
|刷怪间隔(秒)|每次刷怪的时间间隔，仅对刷新器独立刷怪有效|
|单次刷怪数量|每次刷怪的固定数量，直到刷出怪物的总数达到最大值则停止刷怪，仅对刷新器独立刷怪有效|
|刷在地面上|勾选后，会尽量将怪物贴近地面，防止生成在半空中|

>如果只需要简单的刷怪功能，则可以选择无控制，刷怪点在游戏开始后便会自行按照配置的属性开始刷怪。
若要实现更为复杂的刷怪流程，则要搭配刷怪管理器使用。
> 当刷新器独立刷怪时，总刷怪数量为 ``最小生成数量 ~ 最大生成数量`` 之间的随机值

---

### 自定义刷新规则

当使用刷新器独立刷怪，且 ``怪物配置模式`` 设置为“自定义”时，可以扩展刷新规则实现自定义的怪物生成效果。

刷新器提供了 [``CustomSpawnMob``](https://developer.gp.qq.com/api/#/searchContent/AUGCMobSpawner?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAUGCMobSpawner.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCMobSpawner&autoJump=CustomSpawnMob) 函数用于覆写生成怪物的逻辑，该函数的入参是配置在 ``自定义参数`` 中的参数组，开发者可以通过该属性透传任意参数用于实现特定逻辑，在函数体中调用刷新器提供的 [``SpawnMob``](https://developer.gp.qq.com/api/#/searchContent/AUGCMobSpawner?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAUGCMobSpawner.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCMobSpawner&autoJump=SpawnMob) 函数进行怪物的生成。

以下示例中配置了 “MonsterType”和“MonsterID”两个参数，于 ``CustomSpawnMob`` 中查找怪物蓝图路径生成怪物，同时设置怪物的初始属性。

刷新点自定义参数：

![企业微信截图_17503144356318.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kRT9f%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17503144356318.png)

怪物蓝图配置表：

![企业微信截图_17503144975179.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0KUql%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17503144975179.png)

怪物属性配置表：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GA8vaimage.png)

**示例代码**

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

<br>

## 刷怪管理器

使用刷怪管理器生成怪物时，需要创建刷怪管理器蓝图，编辑器内容浏览器右键 ``蓝图类``，继承自 ``BP_UGCMobSpawnerManager`` 创建子蓝图类，同样需要将刷怪管理器蓝图放置到关卡中实例化才能生效。

![1111.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oSotF1111.png)

在关卡中选中刷怪管理器实例对象，在实例对象【细节】面板编辑配置属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8WiV7image.png)

刷怪管理器会按照 ``刷怪波次`` 列表中的设置依次执行，波次列表中的元素数量代表刷怪的总批次，当波次触发后所属的所有刷新点会同时开始刷怪。

|属性名|属性说明|
|-|-|
|刷怪管理器启动方式|支持关卡加载、事件触发和手动调用三种方式<br>- 关卡加载：当管理器所属的关卡加载后自动启动刷怪流程<br>- 事件触发：当接收到 ``事件名`` 属性中填写的指定GMP事件时触发启动刷怪流程<br>- 手动调用：管理器无法自动启动，需要在脚本中调用 [``StartSpawnerManager``](https://developer.gp.qq.com/api/#/searchContent/AUGCItemSpawnerManager?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FAUGCItemSpawnerManager.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCItemSpawnerManager&autoJump=StartSpawnerManager) 触发|
|事件名|启动方式为“事件触发”时，绑定的指定 [GMP事件](https://developer.gp.qq.com/wikieditor/#/catalog/20163)|
|每帧刷怪上限|每一帧执行怪物生成的数量限制，防止游戏卡顿|
|存活怪物检查间隔|检查怪物存活状态的时间间隔，``波次开始条件``设置为“All Mob Die”时会实时检测刷出的怪物是否已死亡，理论上间隔越大性能消耗越小，但时间误差也相对越大|
|刷怪点|该波次执行的刷新点，可手动选择蓝图类，也可以通过吸管工具吸取关卡中的刷新点实例对象<br>![QQ202571-12644-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7MWv7QQ202571-12644-HD-ezgif.com-video-to-gif-converter.gif)|
|覆盖怪物类型配置|是否覆盖刷新点上的刷怪策略配置|
|怪物类型配置|勾选了 ``覆盖怪物类型配置`` 时可配，配置项与刷新点蓝图对应属性一致|
|波次开始条件|波次触发的条件（该条件不影响第一波次的执行），支持 ``All Mob Die`` 和 ``Last Wave End`` 两种：<br>- All Mob Die：上一波次刷出的所有怪物全部死亡后才开始<br>- Last Wave End：上一波次刷怪结束后开始|
|延迟开始时间|波次开始后，延迟多长时间开始刷怪|

<br>

## API参考

|函数库/类名|函数类型|函数功能范围|
|-|-|-|
|[AUGCMobSpawner](https://developer.gp.qq.com/api/#/searchContent/AUGCMobSpawner?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAUGCMobSpawner.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCMobSpawner)|对象函数|修改刷新点配置、生成怪物及相应的刷新事件|
|[AUGCMobSpawnerManager](https://developer.gp.qq.com/api/#/searchContent/AUGCMobSpawnerManager?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%80%AA%E7%89%A9%E7%B3%BB%E7%BB%9F%2FAUGCMobSpawnerManager.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCMobSpawnerManager)|对象函数|刷怪管理器的启动、暂停、重置等运行时管理及配置修改和刷新事件|

---


## 怪物调试工具

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物调试工具

# 怪物调试工具

游戏中怪物的行为依赖于 [行为树](https://developer.gp.qq.com/wikieditor/#/catalog/20147) 和 [怪物逻辑组件]() 的运行，怪物的状态也在动态发生变化，为了方便开发者调试和优化怪物的行为，提供了适用于运行时的怪物调试工具。该工具允许开发者直观地查看游戏运行时怪物行为树的执行状态，包括节点信息、黑板变量值、装饰器打断判定等，帮助开发者快速定位问题并调整AI行为。

![企业微信截图_17496351338454.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mka7l%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17496351338454.png)

<br>

## 启用调试工具

怪物调试工具功能通过 [通用GM面板](https://developer.gp.qq.com/wikieditor/#/catalog/20109) 提供，启动编辑器 [Debug调试](https://developer.gp.qq.com/wikieditor/#/catalog/307)，找到右上角GM入口并点击。

![企业微信截图_17496325493795.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yUhTg%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17496325493795.png)

展开GM面板后，点击右侧【调试】页签，切换到调试面板，点击 ``怪物调试面板`` 的确定按钮即可打开怪物调试工具。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SQPr2image.png)

<br>

## 调试功能说明

怪物调试工具提供了多种调试功能，能够实时查看怪物的属性值、行为树的运行状态、黑板数据等核心信息。

### 选择调试目标

要查看怪物的信息，首先需要选择调试的目标，调试工具会将以玩家自身为中心的球形范围内的怪物对象纳入可选列表，因此需要确保目标怪物处于绿色范围内，从下拉列表选择目标实例对象。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZdFG9image.png)

当怪物对象选择成功后，会通过绿色箭头形式的UI标识当前调试目标。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PRQSmimage.png)

---

### 基础信息

怪物基础信息面板主要显示当前选择的目标怪物的运行时属性，包含怪物移动速度、和玩家距离、位于玩家的方向角度等。

> 基础信息为只读，不可运行时修改
 
![企业微信截图_17496329639062.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1kO22%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17496329639062.png)

- 和玩家的距离：当前怪物与玩家之间的直线距离（单位：米）
- 怪物在玩家方位的角度：怪物相对于玩家的方向角度，这个角度表示怪物面朝玩家的位置，可用于计算视线范围或攻击角度
- 玩家在怪物方位的角度：玩家相对于怪物的方向角度，这个角度帮助计算玩家是否位于怪物的视野范围内
- 怪物的蓝图路径：显示当前怪物的蓝图资源路径
- 怪物的速度：显示怪物当前的移动速度（单位：米/秒）

---

### 行为树状态

行为树面板可以查看当前怪物行为树中执行的各个节点的状态，包括任务节点、服务节点、装饰器节点等。

> 行为树信息为只读，不可运行时修改

![企业微信截图_17496333031356.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sxJ7i%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17496333031356.png)
	 
- 当前运行行为树：当前怪物正在执行的行为树，行为树决定了怪物的决策逻辑和执行的任务
- 当前运行节点：当前怪物在行为树中执行的任务节点
- 当前生效打断：当前是否有装饰器或其他条件打断了行为树的节点执行，如果有则显示所有装饰器节点信息
- 当前生效服务节点：当前正在运行的服务节点，服务节点通常用于持续性环境检测或者黑板数据更新，如果有则显示该服务节点信息
- 平行节点：当前是否有平行节点在执行，如果有则显示所有正在执行的任务节点信息

---

### 黑板数据

黑板面板显示怪物黑板中的实时变量值，并且支持动态修改布尔、浮点、整形及向量类型的变量值。

![企业微信截图_1749634499784.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WXMVG%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1749634499784.png)

---

### 添加怪物

怪物调试工具支持快速将指定怪物添加到场景中，便于进一步调试怪物行为。

点击调试工具界面右下角 `调试怪物` 按钮，弹出添加怪物面板，开发者需要选择生成的目标怪物蓝图类、怪物数量以及生成范围。

![企业微信截图_17496347383359.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/e6yyK%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17496347383359.png)
![TODO换图.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FRRUcTODO%E6%8D%A2%E5%9B%BE.png)

点击【确定】按钮，即可在场景中生成该怪物。

![添加怪物.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Rn8j3%E6%B7%BB%E5%8A%A0%E6%80%AA%E7%89%A9.gif)


---


## 怪物逻辑管理组件

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物逻辑管理组件

**涉及API:** `AIWorldVolume`, `BP_UGCTargetProducer_EnemyHatred`, `BT_UGC_GenericMob_MainTree`, `CalculateHatredValueOfBasic`, `CalculateHatredValueOfDamage`, `LogicPartManagerComp`, `TargetProducer`, `TargetProducer_AllyForHelp`, `TargetProducer_EnemyDistance`, `TargetProducer_EnemyHatred`

# 怪物逻辑管理组件

怪物逻辑管理组件是一个特化的通用行为参数化配置组件，它将怪物常见的行为抽象并封装成不同的逻辑模块，在复用基础行为树的前提下，仅需为怪物蓝图添加逻辑模块并调整参数，即可高效实现不同行为模式的怪物。

<br>

## 逻辑管理组件概述

怪物的行为动作依赖于行为树的编排逻辑，通常一种怪物需要实现一份行为树，当怪物的行为设计复杂时，会将复杂行为拆解为子树的形式实现和引用，这样的实现方式对单个怪物来说结构清晰可读，但是一旦怪物的种类愈多，将带来庞大的行为树维护和管理成本。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/U9TGdimage.png)

怪物系统为怪物蓝图默认配备基础行为树 ``BT_UGC_GenericMob_MainTree``，该行为树涵盖了寻敌、巡逻、攻击、追踪等通用行为，为了在保证最小维护成本的前提下方便扩展怪物种类，将这些通用行为的属性提炼组合成逻辑模块，将其作为组件的形式赋予怪物蓝图，如此即可通过配组件属性的方式扩展怪物的种类，无需创建和维护过多的行为树。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aYkpWimage.png)

<br>

## 添加逻辑管理组件

基于怪物模板创建的怪物蓝图默认都添加了逻辑管理组件 ``LogicPartManagerComp``，如果需要手动添加，可以点击【添加组件】按钮，搜索“Logic Part Manager”并添加即可。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZV1s0image.png)

> 逻辑管理组件主要为配套 ``BT_UGC_GenericMob_MainTree`` 行为树使用，对怪物蓝图来说是非必需组件，如果开发者希望制作有别于通用行为模式的自定义怪物，可不添加该组件，完全由行为树逻辑驱动怪物行为。

<br>

## 配置逻辑管理组件

逻辑管理组件支持四种逻辑模块：寻找目标、呼叫支援、路点跟随和地图网格控制，各逻辑模块以插件化的形式提供启用与配置。

> 每种逻辑模块都有一个 ``Tick Intervel in Seconds`` 属性，为性能优化使用，不建议低于默认值

### 寻找目标逻辑模块

寻找目标逻辑模块 ``Choose Enemy Part`` 用于按指定的任务寻找敌方目标，模块支持多任务组合，各任务之间为 ``或`` 的逻辑关系，即只要其中一个任务执行成功则结束并返回目标结果，类似复合节点中的 [选择器](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-composites?application_version=5.4#%E9%80%89%E6%8B%A9%E5%99%A8)。

该模块依赖 [[Generic]寻敌](https://developer.gp.qq.com/wikieditor/#/catalog/20174?autoJump=[Generic]%E5%AF%BB%E6%95%8C) 服务节点的运行，每次执行寻敌服务节点时，按照配置的子任务顺序 ``从上至下`` 逐一执行，任意子任务查找到有效目标则终止执行，返回该目标，寻敌服务节点执行结束。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8yZvTimage.png)

每个子任务被定义为一个TargetProducer查找器实例，目前提供了多种类型的查找器，寻找目标逻辑模块默认启用了 ``BP_UGCTargetProducer_EnemyHatred`` 和 ``TargetProducer_AllyForHelp`` 两种查找器，分别对应按仇恨值查找与响应呼叫支援。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wCWd6image.png)

#### 查找器通用属性

所有类型的查找器都具有目标筛选的通用属性组：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ODftJimage.png)

|属性名|属性说明|
|-|-|
|Filter Camp Relations|查找所属指定 [阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%98%B5%E8%90%A5%E5%85%B3%E7%B3%BB%E9%85%8D%E7%BD%AE) 的目标|
|Filter Entity Type Tags|查找带有指定 [实体类型标签](https://developer.gp.qq.com/wikieditor/#/catalog/20144?autoJump=%E5%AE%9E%E4%BD%93%E7%B1%BB%E5%9E%8B) 的目标|
|Filter Include Tags|查找带有指定状态标签的目标|
|Filter Exclude Tags|带有指定状态标签的目标不会被查找到|

---

#### 查找器基类

``TargetProducer`` 是查找器基类，其他查找器都是此基类的派生类，该基类本身没有实际的逻辑，因此请勿配置使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xcaoZimage.png)

---

#### 距离查找器

```TargetProducer_EnemyDistance``` 是基于距离的查找器，优先选择距离自身最近的目标，当多个目标都处于最近位置时，随机选择一个目标。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Dm5qiimage.png)

|属性名|属性说明|
|-|-|
|Lock Target Range|锁定目标距离，目标与自身的距离如果小于此值，则锁定该目标且不发生切换，锁定效果仅在该查找器及派生类查找器中生效|
|Range Limit|查找距离阈值，超过该距离的目标将不会被查找，已选中的目标若超过该距离也会被丢失|

---

#### 基于类型优先级的距离查找器

```Target Producer EnemyDistance ClassPriority``` 是距离查找器的派生类，在距离查找的基础上增加了按类型决定目标选取优先级的功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TFARUimage.png)

|属性名|属性说明|
|-|-|
|Enemy Class to Priority|类型优先级配置，为 ``蓝图类：优先级`` 的键值对形式，值越大优先级越高|

> 如果一个怪物未配置在这个优先级中，则在检测到此怪物时，默认会给一个极小数作为优先级值参与比对

如果有锁定中的敌人且处于 ``Lock Target Range`` 范围内时，怪物仍会攻击锁定目标，此查找器的完整执行流程如下：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4JHM3image.png)

---

#### 仇恨值查找器

怪物系统构建了一套仇恨值机制，将感知仇恨及伤害仇恨进行加权计算得出总仇恨值，该仇恨值用于选择最佳目标的评判基准，计算公式为 ``总仇恨值 = f(感知仇恨值) + f(伤害仇恨值)``。

- 感知仇恨：基于敌人与自身距离计算，距离越近仇恨值越高，感知仇恨值每次刷新，默认实现为 ``感知仇恨值 = (1 - 当前距离 / Max(感知半径, 视野半径)) * 100``
- 伤害仇恨：基于伤害值与距离的加权计算，距离越近、伤害越高，此次累加的仇恨值越高，伤害仇恨值可累加，默认实现为 ``伤害仇恨值 = (伤害值 > 100 ? 100 : 伤害值) / 100 * 40``

```BP_UGCTargetProducer_EnemyHatred``` 是基于仇恨值的查找器，每次执行选取仇恨值最高或者随机一个有仇恨值的目标结果，提供了一些细化参数配置决定如何查找目标以及目标仇恨值的更新方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eKLHbimage.png)

|属性名|属性说明|
|-|-|
|仇恨随机转移概率|在仇恨列表中随机选择目标的概率，范围0~1<br>- 0：每次必定选择仇恨值最高的那个目标<br>- 1：每次都是随机选择一个有仇恨值的目标<br>- 其他值：代表有多大概率采用随机选择的方式，例如0.1代表10%的概率随机选仇恨目标，90%概率选仇恨值最高目标|
|寻敌感知半径|以怪物为中心，此半径的球形范围内的目标会被选择为仇恨值目标（单位：厘米）|
|寻敌视野半径|以怪物为中心，此半径的球形范围内，若有目标进入球体则将其坐标投影至XY平面，并与 ``寻敌视野角度`` 进行匹配，若匹配成功则被选择为仇恨值目标（单位：厘米）|
|寻敌视野角度|寻敌视野的扇形范围角度大小，范围0~360度|
|寻敌视野会被障碍物阻挡|勾选之后怪物不会感知在障碍物后的敌人|
|仇恨转移最小间隔|每隔随机的一段时间后，进行一次仇恨值排序并选择新的有效目标，该随机时间的最小值|
|仇恨转移最大间隔|每隔随机的一段时间后，进行一次仇恨值排序并选择新的有效目标，该随机时间的最大值|
|仇恨消失时间|仇恨列表中的目标，多长时间未被感知到或者未对自身造成伤害，从仇恨列表中移除（单位：秒）|
|仇恨消失距离|仇恨列表中的目标，超过多远距离会被强制从仇恨列表中移除（单位：厘米）
|仇恨消失距离适配|用于处理 ``仇恨消失距离`` 小于感知和视野半径的情况（默认情况下无需处理，保持初始选项 ``不处理`` ）<br>- 不处理：保持默认逻辑，即目标到自身的距离只要大于这个仇恨消失距离就会清空这个目标的仇恨<br>-  固定增大：仇恨距离会自动增加到 ``max (感知半径，视野半径) + 固定增大参数`` <br>- 比例增大：仇恨距离会自动增加到 ``max (感知半径，视野半径) * 比例增大参数`` |
|Update Hatred Enemies Interval|更新仇恨列表的频率|
|Line Trace Self Offset|检测可视性时候，射线起点的相对偏移，默认为自身坐标点|
|Line Trace Target Offest|检测可视性时候，射线终点的相对偏移，默认为目标坐标点|

该查找器维护了一个仇恨列表，记录多组 ``{实体对象，总仇恨值}`` 结构的元素，每个实体对象的总仇恨值按配置的规则进行周期性更新：

- 感知仇恨值：寻敌感知半径或者寻敌视野半径内的目标会计算感知仇恨值，即进入仇恨列表，每隔 ``Update Hatred Enemies Interval`` 时间间隔更新一次感知仇恨值，默认为0.2秒的频率
- 伤害仇恨值：一旦对象对自身造成了伤害即计算伤害仇恨值，进入仇恨列表，每次攻击都会进行伤害仇恨值的累计

仇恨列表的完整执行流程如下：

<div style="text-align: center;">
	<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Qk476image.png">
</div>

---

#### 自定义仇恨值查找器

除了属性配置影响仇恨值计算结果，仇恨值查找器还支持自定义仇恨值计算公式，提供 ``CalculateHatredValueOfBasic`` 和 ``CalculateHatredValueOfDamage`` 覆写函数扩展仇恨值的计算实现。

内容浏览器右键 ``蓝图类``，搜索“BP_UGCTargetProducer_EnemyHatred”并基于该类创建查找器蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lHUN5image.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/P8HiWimage.png)

双击打开蓝图，可设置查找器的属性，点击【Lua】按钮进入脚本，可以自定义覆写函数的实现逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ktDQPimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wnqNgimage.png)

自定义的查找器蓝图需要重新配置到逻辑模块中才可生效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/c7DBHimage.png)

---

#### 仇恨值查找器基类

``TargetProducer_EnemyHatred`` 是仇恨值查找器 ``BP_UGCTargetProducer_EnemyHatred`` 的基类，该查找器不具备复杂的参数配置，但也支持通过 ``CalculateHatredValueOfBasic`` 和 ``CalculateHatredValueOfDamage`` 覆写函数扩展仇恨值的计算实现，该基类的默认仇恨值计算公式如下：

- 感知仇恨：``感知仇恨值 = (1 - 当前距离 / RangeLimit) * 100 + (可见 ? 30 : 10)``
- 伤害仇恨：``伤害仇恨值 = (伤害值 > 100 ? 100 : 伤害值) / 100 * 40``

> 可见性结果由射线检测判断

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JEc5jimage.png)

---

#### 响应呼叫支援查找器

```TargetProducer_AllyForHelp``` 是一个响应其他实体呼叫支援的查找器，在收到了其他实体通过 ``呼叫支援逻辑模块`` 发出的支援消息之后，该查找器会将攻击呼叫支援者的对象缓存到组件中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wkf3Eimage.png)

|属性名|属性说明|
|-|-|
|Help Ally Lock Time|收到一个请求支援消息之后，多长时间之内不响应其他的请求支援，此属性可防止自身目标频繁变化|
|Help Ally Elapse Time|收到一个请求支援消息之后，多久之后会移除缓存的目标|

<br>

### 呼叫支援逻辑模块

呼叫支援逻辑模块 ``Call For Help Part`` 用于在怪物受到攻击时自动呼叫周围同阵营怪物进行支援，能够实现“摇人”的效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bKqffimage.png)

|属性名|属性说明|
|-|-|
|Call for Help Intervel|每隔多久进行一次呼叫支援，从第一次受到伤害开始以固定的频率执行前置伤害判定，周期内接收过伤害才会触发呼叫支援<br>受伤害的频率可能比较高，此属性主要用来限制呼叫频率（单位：秒）|
|Call for Help Range|能接收到呼叫支援消息的半径范围（单位：厘米）|
|Ally Entity Type Tags|拥有指定 [实体类型标签](https://developer.gp.qq.com/wikieditor/#/catalog/20144?autoJump=%E5%AE%9E%E4%BD%93%E7%B1%BB%E5%9E%8B) 的怪物能接收到呼叫支援消息|
|Call for Help from Damage Causer|是否以伤害来源为中心进行呼叫，否则以怪物自身为中心|

该逻辑模块的执行流程如下：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Jo6rQimage.png)

> 仅与呼叫者 **属于同阵营** 的怪物才能响应支援，忽略盟友阵营

<br>

### 路点跟随逻辑模块

路点跟随逻辑模块 ```Follow Waypoint Part``` 提供了怪物按路点移动的功能，即怪物在设定好的路线上移动，例如Moba中的兵线，潜入类游戏中的怪物路点巡逻等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FDlh2image.png)

> 功能尚在开发中，开发者暂勿使用

<br>

### 地图网格控制逻辑模块

地图网格控制逻辑模块 ```Map Cell Control Part``` 的作用是将怪物放置到 ``AIWorldVolume`` 体积空间中，所有放置在该体积空间中的游戏对象都能被怪物识别到。

> 理论上所有怪物都需要添加该逻辑模块，否则影响部分功能

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VPbROimage.png)

- Update Map Cell Interval：更新MapCell的时间间隔，保持默认即可


---


## 移动与避障

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 移动与避障

**涉及API:** `CrowdMove`, `DynamicObstacleAvoidance`, `MoveControlComponent`, `SetAvoidanceGroup`

# 移动与避障

新怪物系统优化统一了怪物的移动逻辑，不再需要依怪物类型区分使用的移动任务节点，只需通过移动策略的配置即可实现不同怪物的移动，且支持了怪物的动态避障功能。

<br>

## 移动控制组件

类似玩家角色的移动机制，怪物的移动也都依赖于 [角色移动组件](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/understanding-networked-movement-in-the-character-movement-component-for-unreal-engine?application_version=5.5) ，考虑到移动底层涉及大量的网络同步及Gameplay功能的处理，为了方便开发者配置与使用，额外封装了移动控制组件 ``MoveControlComponent``，该组件只提供最精简的移动策略、避障规则、移动速度和怪物转向等配置项，行为树的移动任务节点会读取组件的配置并最终决定怪物的移动行为。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YVGDGimage.png)

<br>

## 移动策略

移动控制组件提供了4种移动策略：基础移动、飞行移动、群体移动、静止不动，各移动策略适用于不同的应用场景。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tgh2bimage.png)

- Move Tag：当怪物移动时添加的Tag，基于 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 定义的状态标签
- Move Strategy：使用的移动策略 
- Smooth Class Type：移动组件类，默认值不建议修改

### 基础移动

基础移动是最通用的移动行为，它基于导航网格计算出可达的移动路径以支持移动位置，支持怪物之间及动态物件的避障功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hq9Rfimage.png)

---

### 飞行移动

飞行移动有个独有的 ``飞行移动`` 属性，该属性决定当移动方向前方存在障碍物时，选择绕行还是从其上方飞过去。

> 当前飞行移动暂不支持主动避障

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UTuQdimage.png)

- 飞行移动：可飞跃障碍物的高度（单位：厘米），该高度仅作为怪物避障的参考，并不会让怪物保持此高度漂浮移动
- 重新寻路阈值：寻路底层使用的属性，默认值不建议修改
- 出生时保持飞行高度：勾选后，怪物出生时的Z轴将直接设定为飞行高度；否则，将以出生点的实际Z轴位置生成怪物
- 死亡后是否落地：勾选后，怪物死亡时会进入下落状态直到落地；否则，会以死亡动画状态停留在空中

---

### 群体移动

群体移动是自带怪物间避障的移动策略，相比于 ``基础移动`` 的避障能力，群体移动采用了更加高效的群体怪物移动算法，性能更加优越，因此更适合海量怪物的移动场景，但是不支持动态物件的避障。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JINjGimage.png)

- 重新寻路阈值：寻路底层使用的属性，默认值不建议修改

---

### 静止不动

静止不动是一种特殊的移动策略，它能确保怪物保持绝对静止状态，包括不受任何冲击技能（如击飞、击退等）的影响，因此适合防御塔这类不需要移动功能的场景。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eQuduimage.png)

<br>

## 怪物避障

避障是怪物在移动过程中识别障碍物并调整移动行为以规避障碍的能力，根据避障目标的类型不同可分为静态物件避障和动态目标避障。

- 静态物件避障：针对场景中的静态物体的避障，例如各类建筑物、高低地形等
- 动态目标避障：目标对象的坐标位置动态发生变化，需要达到实时识别并规避碰撞的效果，包括对其他移动中的怪物避障、动态生成的阻挡物避障等，不同的移动策略支持的避障场景不同

|移动策略|支持的避障场景|支持的避障策略|
|-|:-:|:-:|
|基础移动|群体避障、动态障碍物避障|RVO、CrowdMove|
|飞行移动|-|-|
|群体移动|群体避障|CrowdMove|
|静止不动|-|-|

### 静态物件避障

对于场景中的静态物体，当 [构建导航网格](https://developer.gp.qq.com/wikieditor/#/catalog/20144?autoJump=%E7%94%9F%E6%88%90%E5%8F%AF%E7%A7%BB%E5%8A%A8%E5%8C%BA%E5%9F%9F) 时会将静态物体的形状和范围参与寻路路径计算，构建结果会自动避开障碍物的区域，怪物的移动范围也将排除这些区域。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/z2DZuimage.png)

---

### 动态目标避障

动态目标避障有两种不同的策略，分别适用于单目标的避障和多目标的群体避障场景，两种策略都依赖于避障组的设置，即避障组决定了怪物可避障的目标范围，避障策略决定怪物的避障效率。

#### 避障组

任意实体对象都可以设置自身所属的避障组及避障目标的避障组，例如隶属0号避障组，避障目标组号0~10，则代表该对象能够主动避让组号属于0~10号范围内的所有对象目标，而自身将被避障目标为0号的对象所避让。

> 系统预设了0~31号避障组供选择使用

所属避障组：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/weJAaimage.png)

目标避障组：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vLlXqimage.png)

具备 ``移动控制组件`` 的实体对象与动态障碍物对象配置方式与隶属避障组的规则不同，动态障碍物依赖于 ``DynamicObstacleAvoidance`` 组件的设置，一个动态障碍物可以隶属于多个避障组；而可移动的实体对象在 ``移动控制组件`` 中设置避障组，且一个实体对象只能隶属一个避障组。

---

#### 避障策略

避障策略分为 [RVO（相对速度障碍物）](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/using-avoidance-with-the-navigation-system?application_version=4.27#4-%E5%90%91%E4%BB%A3%E7%90%86%E6%B7%BB%E5%8A%A0%E7%9B%B8%E5%AF%B9%E9%80%9F%E5%BA%A6%E9%9A%9C%E7%A2%8D%E7%89%A9%E7%AE%97%E6%B3%95) 和 [CrowdMove（群体移动避障）](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/using-avoidance-with-the-navigation-system?application_version=4.27#5-%E5%90%91%E4%BB%A3%E7%90%86%E5%BA%94%E7%94%A8%E7%BE%A4%E7%BB%84%E7%BB%95%E8%A1%8C%E9%81%BF%E9%9A%9C) 两种，两者都能实现避障效果但功能启用上为互斥关系，对于不同的避障场景需要选择合适的策略。

|策略|功能说明|适用场景|
|-|-|-|
|RVO|基于特定半径内的速度向量计算及调整以规避障碍物，但不参考寻路网格体的路径范围|避障效果更精确，但是性能消耗更大，适用于精英怪或者Boss这类单个或者少数怪物的移动场景|
|CrowdMove|通过自适应RVO采样计算及路径优化提升碰撞规避效果|性能更优，适合大量怪物移动的避障场景|

---

#### 怪物间避障

怪物实体之间的避障效果在移动策略组件下配置避障相关属性实现，支持 ``基础移动`` 和 ``群体移动``。

打开怪物蓝图，在 ``Move Strategy`` 属性组下设置使用的避障策略，例如启用 ``CrowdMove`` 策略；于 ``Crowd Move`` 属性组下设置该怪物所属避障组和目标避障组，``默认避障组号`` 对应所属避障组，``组间避障关系`` 对应目标避障组，例如隶属避障组号为0，对组号为1~3的怪物对象进行避障。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/23NIGimage.png)

为了验证避障效果，创建另一个怪物蓝图，并将此怪物的移动策略同样设置为 ``基础移动``，开启 ``CrowdMove`` 且 ``默认避障组号`` 设置为1，运行调试游戏可观察怪物的移动避障行为。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/80yVOimage.png)
![QQ2025715-172544-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/z3dvlQQ2025715-172544-HD-ezgif.com-video-to-gif-converter.gif)

怪物所属的避障组除了蓝图配置外，也支持脚本中调用 [``SetAvoidanceGroup``](https://developer.gp.qq.com/api/#/searchContent/UGCGenericCharacterSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%80%AA%E7%89%A9%E7%B3%BB%E7%BB%9F%2FUGCGenericCharacterSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGenericCharacterSystem&autoJump=SetAvoidanceGroup) 动态修改，建议根据怪物所属阵营设置好对应的避障组号。

**注意事项**

> - 避障关系为单向，即怪物A会避让怪物B，反之未必成立，取决于两者的所属避障组和目标避障组是否双向匹配
> - 移动策略和避障策略组合的一致性是避障关系生效的充分必要条件，例如A为基础移动并开启RVO避障，B也必须是基础移动并开启RVO避障，避障功能才能生效

---

#### 动态障碍物避障

``DynamicObstacleAvoidance`` 动态避障组件是怪物避让障碍物对象的前置依赖，该组件需要添加至障碍物上并设置避障相关属性，仅使用 ``基础移动`` 策略的怪物具备对动态障碍物避让的能力，且只支持 ``CrowdMove`` 的避障策略。

1. 制作一个带有静态网格体的简易障碍物蓝图，并为其添加 ``DynamicObstacleAvoidance`` 组件。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TuEWEimage.png)

2. 设置动态避障组件的避障相关属性，包含避障策略、避障参考范围、所属避障组和目标避障组等。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OVEh4image.png)

	|属性名|属性说明|
	|-|-|
	|Use RVO|目前仅支持 ``CrowdMove`` 避障策略，固定不勾选|
	|Avoidance Weight|避障权重，数值越大的对象在移动的时候避障路线变化幅度更小，由于动态障碍物自身并不存在移动逻辑，故此数值保持默认即可|
	|Custom Origin Relative Location|是否启用碰撞偏移，若勾选，则障碍物实际的碰撞位置将会产生偏移，影响检测碰撞的结果和避障效果|
	|Origin Relative Location|碰撞偏移量，启用 ``碰撞偏移`` 后有效|
	|Custom Avoidance Capsule|是否使用自定义的碰撞胶囊体，避障固定使用胶囊体作为碰撞检测目标，如果不启用，则使用Actor下的 ``Capsule Collision（胶囊体碰撞）组件`` 作为检测碰撞体；若Actor下不存在该组件，避障功能会失效|
	|Avoidance Radius|碰撞胶囊体的半径，启用 ``自定义碰撞胶囊体`` 后有效|
	|Avoidance Half Height|碰撞胶囊体的半高，启用 ``自定义碰撞胶囊体`` 后有效|
	|Avoidance Group|胶囊体隶属的碰撞组，动态障碍物可以隶属多个避障组|
	|Groups to Avoid / Groups to Ignore|由于动态障碍物自身不存在移动逻辑，故无需关注这两个属性|
	|Auto Regist|勾选将使用 ``CrowdMove`` 避障策略，必须勾选，且需要确保怪物也同样使用该策略才能生效|

	例如为障碍物添加动态避障组件，设置该障碍物隶属于1~3号避障组。
	
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4lGxUimage.png)

3. 创建一个怪物蓝图，将该怪物设置 ``基础移动`` 策略并启用 ``CrowdMove`` 避障策略，且目标避障组号设为2。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/z4exXimage.png)

运行调试游戏，在怪物移动过程中动态生成此障碍物，观察怪物的移动避障行为。

![ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uYj6Mezgif.com-video-to-gif-converter.gif)

<br>

## 移动速度

``默认最大移动速度`` 表示怪物移动时可达的最大速度值，移动功能会根据当前移动状态、释放转向、是否避障等动态调整移动速度。

> - ``最大移动属性名`` 默认为预设名称，关联其他系统功能，不建议修改
> - ``是否根据状态切换速度`` 功能尚在开发中，开发者暂勿使用

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3hwz4image.png)

<br>

## 怪物转向

[[Generic]转向](https://developer.gp.qq.com/wikieditor/#/catalog/20179?autoJump=[Generic]%E8%BD%AC%E5%90%91) 任务节点能够让怪物执行转向动作以面对指定方向或者目标，通常转向属性在任务节点中配置，移动控制组件中该部分属性为默认初始值。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bHHvgimage.png)

|属性名|属性说明|
|-|-|
|Turning Tag|当怪物转向时，进入指定的Tag状态|
|启动平滑转向的角度阈值|当怪物前向向量与朝向目标的向量夹角大于此值时，会执行平滑转向；否则瞬间面向对象|
|平滑转向的默认时间|保持默认值即可|


---


## 服务节点查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 服务节点查询手册

**涉及API:** `Actor`

# 服务节点查询手册

服务节点以指定的频率周期性执行，通常用于定期检查执行节点的条件以及更新黑板值，可以依附于 [复合节点](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-composites?application_version=5.5) 或者 [任务节点](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-tasks?application_version=5.5)。

> 名称前缀带有“[Generic]”的节点为新怪物系统的适配节点，其他节点为不兼容的老旧节点，请开发者谨慎使用

<br>

## 通用属性

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZgacBimage.png)

- 间隔：定义该节点每次执行的时间间隔
- 随机偏差：为时间间隔添加随机的+/-偏差值，修正执行频率
- 节点名称：定义节点的名称

<br>

## [Generic]寻敌

寻敌是怪物最基础的行为之一，通常基于距离、仇恨值、感知系统等多维度综合选择出最终目标，由于寻敌模式的通用性，实体编辑器将各要素抽象成不同的逻辑组件，并通过 [怪物逻辑管理组件](https://developer.gp.qq.com/wikieditor/#/catalog/20162) 提供参数化配置，开发者无需关注此服务节点的 ``寻敌策略`` 配置。

> 行为树如果使用了该节点，则必须配套为怪物蓝图 [添加逻辑管理组件](https://developer.gp.qq.com/wikieditor/#/catalog/20162?autoJump=%E6%B7%BB%E5%8A%A0%E9%80%BB%E8%BE%91%E7%AE%A1%E7%90%86%E7%BB%84%E4%BB%B6)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JbJdzimage.png)

- 最优敌人目标：寻敌结果绑定的 ``Actor`` 类型的黑板变量

<br>

## [Generic]修改最大速度

此节点执行效果为修改怪物的最大移动速度，支持定值与黑板变量两种传值方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DTUHEimage.png)

- 新最大速度：覆盖怪物蓝图的移动管理组件下的最大移动速度
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LWh6Mimage.png)
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 退出节点是否还原最大速度：当该节点不再执行的时候，是否恢复最大速度值
	- 原始值：布尔值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``bool`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值


---


## 装饰器节点查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 装饰器节点查询手册

**涉及API:** `Actor`, `FVector`, `HasTag`, `Vector`

# 装饰器节点查询手册

装饰器节点用于判断分支或者子节点的执行条件，作为条件判断语句使用，可以依附于 [复合节点](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-composites?application_version=5.5) 或者 [任务节点](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-tasks?application_version=5.5)。

> 名称前缀带有“[Generic]”的节点为新怪物系统的适配节点，其他节点为不兼容的老旧节点，请开发者谨慎使用

<br>

## 通用属性

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fwba8image.png)

- 观察者终止：当此节点 **判定结果** 发生变化时，终止执行子树，支持三种类型的终止
	- None：不终止
	- Self：终止此节点自身和在其下运行的所有子树
	- Lower Priority：终止此节点右侧的所有节点（包括右侧全部节点子树）
	- Both：终止此节点自身和在其下运行的所有子树，以及此节点右侧的所有节点（包括右侧全部节点子树）
- 翻转条件：是否对节点的执行结果取反
- 节点名称：定义节点的名称

<br>

## [Generic]概率

进行一次随机概率决定节点的真值结果，例如20%的概率为true，则代表该节点20%的概率是条件通过。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4urj6image.png)

- 原始值：固定值，0代表必定false，``取值方式`` 选为“原始值”时生效
- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
- 取值方式：原始值/黑板值

<br>

## [Generic]角度判断

比较指定对象的中心位置前向向量，与该对象中心位置到目标位置方向向量的夹角大小是否满足指定条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/k5FOFimage.png)

- 中心位置：指定的Actor，绑定 ``Actor`` 类型的黑板变量
- 目标位置：支持指定坐标位置或者目标Actor的位置
	- 原始值：固定世界坐标位置，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``Actor`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 操作：比较运算符
- 设定角度：比较的目标角度值
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]距离判断

判断指定对象和目标位置的距离是否满足指定条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DHXpeimage.png)

- 起点Actor：指定的Actor，绑定 ``Actor`` 类型的黑板变量
- 目标Actor/目标位置：指定的Actor或者位置坐标，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 操作：比较运算符
- 距离：比较的目标距离
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 是否考虑胶囊体大小：如果考虑胶囊体大小，则判断标准为 ``距离 + 胶囊体大小``
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``bool`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>


## [Generic]距离判断EX

判断指定对象和目标位置的距离是否满足指定条件。与 ```[Generic]距离判断``` 功能类似，区别在于距离值可以取一个属性值

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4rp6iimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wXQYcimage.png)

- 起点Actor：指定的Actor，绑定 ``Actor`` 类型的黑板变量
- 目标Actor/目标位置：指定的Actor或者位置坐标，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 操作：比较运算符
- 距离：比较的目标距离
	-	使用属性值：布尔值，勾选后将取值变为属性值选择
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 是否考虑胶囊体大小：如果考虑胶囊体大小，则判断标准为 ``距离 + 胶囊体大小``
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``bool`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]时间

判断当前游戏运行时间与目标时间的差值，是否符合指定范围的判断条件，计算公式为 ``|当前运行时间 - 目标时间| [OP] {范围最小值，范围最大值}``。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bs6wJimage.png)

- 检测时间：目标时间
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 操作：比较运算符
- 检测值-最小：比较范围最小值
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 检测值-最大：比较范围最大值
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]状态检查

判断目标对象是否具备指定状态的匹配条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/R5wZnimage.png)

- BBKey Target Actor：指定的Actor，绑定 ``Actor`` 类型的黑板变量
- Target Dynamic State：目标状态，基于 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 定义
- OP：匹配条件
	- 允许：指定的状态是否可以和目标对象身上的所有状态共存，即不能和任何一个状态存在 [互斥关系](https://developer.gp.qq.com/wikieditor/#/catalog/20106?autoJump=%E7%8A%B6%E6%80%81%E4%BA%92%E6%96%A5%E5%AE%9A%E4%B9%89) 
	- 含有：目标对象是否存在指定的状态，即 [``HasTag``](https://developer.gp.qq.com/api/#/searchContent/UGCGameplayTagSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGameplayTagSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGameplayTagSystem&autoJump=HasTag) 的匹配方式

<br>


## [Generic]黑板值比较

将对象上的一个指定名称的属性与一个值进行比较，若满足给出的条件则通过，否则不通过。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PD3odimage.png)

- 观察对象：目标Actor，绑定 ``Actor`` 类型的黑板变量
- 属性名称：目标对象要比对的属性名称
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``name`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 操作：比较运算符
- 比较值：比对的条件值
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

 
<br>


## [Generic]属性比较

与[Generic]黑板值比较功能一致，区别点在于优化了属性名称的绑定方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QXIsNimage.png)

- 观察对象：目标Actor，绑定 ``Actor`` 类型的黑板变量
- 属性：目标对象要比对的属性，支持 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 操作：比较运算符
- 比较值：比对的条件值
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值


<br>


## [Generic]可见性检查

检查自身（或者自定义）和一个目标之间是否有阻挡，可以选择使用射线或者扫掠检测。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qM3gSimage.png)

- 检测目标：目标Actor，绑定 ``Actor`` 类型的黑板变量
- 使用扫掠检测：使用扫掠检测两者之间的可见性，扫掠的对象是一个球，其半径为自身胶囊体的半径 * 0.8（注意，若自身比较大，可能会导致扫掠球碰撞到地面）从一个起点沿着某个路径“拖动”或“扫过”，并检测它在这个过程中是否与其他物体发生碰撞，只关心第一次碰撞的物体；不勾选，则使用射线进行检测
- 检测起点偏移：检测的起点会加上这个偏移量
- 检测终点偏移：检测的终点会加上这个偏移量
- 查询移动类型：检测的对象是何种移动类型，取决于对象的 ``移动性`` 设置
	- Static：静态类型
	- DynamicAndStationary：可移动和静态对象类型
	- Any：任意类型
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/H3RSfimage.png)
- 追踪通道：射线或者扫掠使用的通道，默认为可视性
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uHjGWimage.png)
- 是否忽略Pawn：是否不检测Pawn类型的阻挡
- 自定义检测起点：勾选之后使用下面这个自定义的检测起点，否则就是使用自身
	- 检测起点：绑定 ``Actor`` 或者 ``FVector`` 类型的黑板变量


---


## 任务节点查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 任务节点查询手册

**涉及API:** `Actor`, `OnBehaviorNotify_BP`, `Vector`

# 任务节点查询手册

任务节点为具体执行的动作或者逻辑行为，在行为树的结构上属于叶子节点，可以添加 [装饰器节点](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-decorators?application_version=5.5) 或者 [服务节点](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-behavior-tree-node-reference-services?application_version=5.5)。

> 名称前缀带有“[Generic]”的节点为新怪物系统的适配节点，其他节点为不兼容的老旧节点，请开发者谨慎使用

<br>

## 通用属性

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/o6MNIimage.png)

- 忽略重启自身：当启用忽略时，如果此节点正处于执行状态，且下一个要执行的任务节点还是此节点，则不会重新执行，保持当前执行状态
- 节点名称：定义节点的名称

<br>

## 移动类节点

### [Generic]导航移动到

怪物对象以最大移动速度进行移动，移动到指定的目标位置或者目标对象的位置，可以设置目标位置前的停止距离。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/J2Ajhimage.png)

- 停止距离：距离目标位置前多远距离停止移动（值过小可能会导致一直无法完成此任务节点）
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 黑板键：指定的目标位置或者目标对象，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量

---

### [Generic]多方向移动

忽略导航网格，强制怪物对象以后/左/右等方向移动，也支持随机方向的移动。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/d1OSKimage.png)

- 移动方向：指定左/右/后的移动方向，此方向基于中心点参照物，即左代表参照物的左方向，与 ``随机移动`` 互斥
- 随机移动：每次执行都从左/右/后中随机一个方向，与 ``移动方向`` 互斥
- 移动中心对象：即参照物，怪物围绕该参照物进行移动，绑定 ``Actor`` 类型的黑板变量
- 移动速度：指定移动的速度
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 移动距离：本次移动的总距离
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 步数：本次移动的总步数，每走一步会参考中心点的位置调整下一步的方向，当步数足够多时会趋近于围绕中心点的圆形轨迹
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

![企业微信截图_17514271209409.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5OkW0%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17514271209409.png)

> 移动速度、移动距离和步数三个参数需要配套调整，当数值不合理时，可能出现移动拉扯的异常现象，开发者可参考 ``移动距离 / 步数 > 移动速度`` 的简单公式对数值合理性进行评估优化

---

### [Generic]沿路点移动

让怪物对象沿着设定好的路径点进行移动，需要配合 [路点移动]() 功能使用。

> 该Task执行时通常不会返回失败，若所有的路点全部走完，则会结束任务并且返回成功；特别的，若一条路线是环形的，则此Task会一直执行下去

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oFAHzimage.png)

- Stop Radius Scale：保持默认值即可

---

### [Generic]指定速度移动到

让怪物对象以指定的速度进行移动，移动到指定的目标位置或者目标对象的位置，可以设置目标位置前的停止距离。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l8o3Limage.png)

- 最大速度：指定的速度，覆盖怪物对象的最大移动速度
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 停止距离：距离目标位置前多远距离停止移动（值过小可能会导致一直无法完成此任务节点）
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 黑板键：指定的目标位置或者目标对象，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量

<br>

## [Generic]等待

使行为树处于等待状态，节点执行后开始计时，在达到指定时间之后结束运行并返回成功，等待时长为 ``{等待时间 - 随机时间， 等待时间 + 随机时间}``。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/B1nQfimage.png)

- 等待时间：基础等待时间
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 随机时间：为 ``等待时间`` 添加随机+/-偏差值
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

> Wait属性暂无实际作用，无需配置和使用

<br>

## [Generic]发送通知

向怪物对象发送一条消息通知，可以通过实体对象的 [``OnBehaviorNotify_BP``](https://developer.gp.qq.com/api/#/searchContent/AUGCGenericCharacter?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAUGCGenericCharacter.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCGenericCharacter&autoJump=OnBehaviorNotify_BP) 函数来监听行为树发送的消息并执行相应的逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CpZNHimage.png)

- 消息：发送的消息字符串
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``string`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]记录时间

将当前的游戏运行时长记录到指定的黑板键中，通常配合 [[Generic]时间](https://developer.gp.qq.com/wikieditor/#/catalog/20178?autoJump=[Generic]%E6%97%B6%E9%97%B4) 装饰器节点一起使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jEceCimage.png)

- 输出时间：游戏运行时长（单位：秒），绑定 ``float`` 类型的黑板变量

<br>

## [Generic]设置AI状态

让怪物对象进入或退出指定的状态，默认情况下如果不存在特殊的互斥关系，怪物会进入 ``PawnState.Movement.Idle`` 待机状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xcfIWimage.png)

- 处理方式：指定进入/退出状态行为
- 状态：指定的状态，默认已经为怪物预设了多种状态
	- PawnState.Movement.Idle：待机状态
	- PawnState.Movement.Walking：移动状态
	- PawnState.Action.Battle：战斗状态
	- PawnState.Action.Turning：转向状态
	- PawnState.Dead：死亡状态
	- PawnState.AddtiveState.HitFly：击飞状态
	- PawnState.AddtiveState.OnStun：眩晕状态

<br>

## [Generic]施放技能

向指定目标或者位置施放怪物对象指定的技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sNt7mimage.png)

- 技能GameplayTag：[虚拟技能槽](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E9%80%9A%E8%BF%87%E8%93%9D%E5%9B%BE%E9%85%8D%E7%BD%AE%E6%8A%80%E8%83%BD) 对应绑定的技能
- 技能目标：指定的Actor对象或者目标位置，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 无目标是否能释放技能：如果没有有效的目标对象，是否允许施放技能

<br>

## [Generic]寻找可达位置

以一个位置为中心点，查找其圆环区域内可以到达的位置，此节点依赖 [导航网格](https://developer.gp.qq.com/wikieditor/#/catalog/20151)，且从导航网格范围内进行查找。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0NpjWimage.png)

- 查找中心：指定的Actor对象或者坐标位置，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 输出位置：查找到的可达点坐标位置记录到指定的黑板键上，绑定 ``Vector`` 类型的黑板变量
- 最大查找次数：若查找次数超过这个值仍未找到可达点，则任务执行失败
- 查找范围-最小：圆环的内径大小
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 查找范围-最大：圆环的外径大小
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 最小巡逻距离：查找到的可达点与自身之间的最小距离，小于此距离会重新查找
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]转向

将怪物对象在世界坐标系的Z轴上进行旋转，直到面向了转向目标后执行完成并返回成功。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kRZyYimage.png)

- 转向目标：要面对的Actor对象或者坐标位置，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 是否瞬时转向：勾选后会立刻将自身面向目标，否则平滑缓慢地转向目标，与 ``启动平滑转向的角度阈值`` 互斥
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``bool`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 启动平滑转向的角度阈值：当自身前向向量与朝向目标的向量夹角小于此值时，会瞬间面向对象，与 ``是否瞬时转向`` 互斥
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]修改技能

将怪物绑定的指定虚拟技能槽上的技能替换为目标技能，支持批量替换。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ropUSimage.png)

- 技能GameplayTag：指定的 [虚拟技能槽位](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) Tag
- 技能：替换的目标技能蓝图，若不配置则代表清空该槽位的技能

<br>

## [Generic]释放技能组

从配置的一组技能组中依据权重随机选取可释放的技能，向指定目标或者位置进行施放。

执行该节点时，首先会筛选当前不处于CD状态的技能，并按距离范围选取有效的技能，然后根据权重随机取得一个技能进行释放。

> 只有成功释放技能之后此节点才会返回成功，否则执行结果为失败

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Op2Y0image.png)

- GameplayTag：[虚拟技能槽位](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) Tag
- 技能目标：技能的释放目标，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 权重：该技能在技能组中的权重
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``int`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 最小/大CD：该技能成功释放后，会从 ``[最小CD, 最大CD]`` 范围内随机一个值赋予该技能作为CD时间，并进入CD状态
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 无目标是否能释放技能：若勾选，则不做距离判断；否则，目标在距离范围内才允许释放技能
- 最小/大距离：约束可释放技能的距离范围
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

<br>

## [Generic]寻找指定方向上的可达位置

以指定的位置或者对象目标为原点，朝特定方向上指定的一个距离范围内寻找一个可以到达的位置。

> 该Task执行必定返回成功，但可能未找到有效的位置点，因此建议对此节点的输出位置做有效值判断

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ajWDeimage.png)

- 查找中心：查找的目标原点，绑定 ``Actor`` 或者 ``Vector`` 类型的黑板变量
- 查找方向：以查找中心的坐标系为参考，前为X正方向，后为X负方向，左为Y负方向，右为Y正方向
- 查找距离：以查找中心和查找方向为基准，按指定的直线距离进行查找，是明确的位置点
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 范围误差：以查找的位置点为中心，该参数值为半径划定可达位置的范围
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值
- 最大查找次数：使用导航网格进行查找的次数上限，未查找到则返回nil
- 输出位置：查找的结果通过黑板变量输出，绑定 ``Vector`` 类型的黑板变量
- 目标对象：用于过滤查找结果，保证可达位置与一个指定对象的距离处于有效范围内（小于指定值），绑定 ``Actor`` 类型的黑板变量
- 范围：有效的距离范围，若配置小于等于0的值，则忽略这个目标对象
	- 原始值：固定值，``取值方式`` 选为“原始值”时生效
	- 黑板值：读取指定的 ``float`` 类型的黑板变量，``取值方式`` 选为“黑板值”时生效
	- 取值方式：原始值/黑板值

---


## 怪物动画

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 怪物动画

**涉及API:** `AnimListComp`, `Death`, `SK_CH_UGC_Elements_Skeleton`, `UGCSimpleMobAnimConfig`, `UGCSimpleMobSharingAnimConfig`

# 怪物动画

怪物动画是基于骨骼网格体的动作表现资源，怪物系统将 [动画蓝图](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-blueprints?application_version=4.27)、[状态机](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/state-machines?application_version=4.27) 等动画相关的复杂概念与制作工具简化，基于怪物行为抽象出一系列姿态动画配置，开发者仅需替换姿态对应的动画资源即可实现不同的动画效果。

<br>

## 动画资源类型

怪物系统目前支持动画序列、动画蒙太奇与混合空间三种动画资源。

### 动画序列

[动画序列](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-sequences?application_version=4.27) 是在骨骼网格体上播放的单个关键帧动画资源，每一帧存储了各骨骼的变换数据（平移、旋转与缩放）以驱动骨骼网格体的变换，通过播放关键帧实现平滑的动画效果，是最基础的动画资源。

编辑器为不同的怪物类型提供了相应的动画序列资源，双击打开动画序列可预览动画效果，需要注意的是，每个动画序列资源只针对当前怪物或者同骨骼的怪物有效，不同骨骼的怪物复用动画序列会因骨骼的变换数据差异而导致播放效果异常。

![QQ2025119-18415-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ihVUiQQ2025119-18415-HD-ezgif.com-video-to-gif-converter.gif)

> 由于绿洲启元动画美术制作规范复杂，不建议开发者导入外部软件制作的动画资源，容易因参数不一致导致播放异常的问题

---

### 动画蒙太奇

[动画蒙太奇](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-montage-overview?application_version=4.27) 是将同骨骼怪物的动画序列资源剪辑分成若干片段，并对这些片段进行拼接组合以实现特定的播放效果，类似电影蒙太奇，例如怪物的死亡动画蒙太奇就是将死亡动画序列的片段与循环播放的倒地动画组合，以达到怪物死亡后保持倒地状态的效果。

![QQ2025119-181816-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/219WqQQ2025119-181816-HD-ezgif.com-video-to-gif-converter.gif)

---

### 混合空间

[混合空间](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/blend-spaces-overview?application_version=4.27) 是基于指定混合轴的输入值将离散的动画序列资源进行平滑插值以实现连贯的动画效果，在怪物移动的场景下比较常用，例如怪物从待机->普通移动->奔跑移动就是通过混合对应的动画序列资源实现。

![QQ20251110-15461-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Jy0z9QQ20251110-15461-HD-ezgif.com-video-to-gif-converter.gif)

<br>

## 创建动画蒙太奇

与动画序列资源一样，编辑器内置了部分怪物的动画蒙太奇资源，开发者也可以基于已有的动画序列自行制作动画蒙太奇，下面以元素之心的死亡动画蒙太奇为例，介绍创建的步骤。

工程目录下右键 ``动画 -> 动画蒙太奇``，选择目标怪物的骨骼，元素之心的骨骼为 ``SK_CH_UGC_Elements_Skeleton``，选中后将创建出动画蒙太奇资源。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VoLoNimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PDyjqimage.png)

双击打开动画蒙太奇，在预览区下方的面板中包含蒙太奇编辑、插槽组和片段编辑三部分，蒙太奇编辑用于拼接动画序列资源和创建新片段，默认有“Default”片段，插槽组设置该动画蒙太奇播放时使用的插槽，片段编辑定义不同片段之间播放的衔接方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zdx5Limage.png)

通常每个怪物都默认使用名为“DefaultGroup.DefaultSlot”的插槽，死亡动画蒙太奇必须使用 ``Death`` 插槽播放，将插槽组切换为“DefaultGroup.Death”。

> - 切换后建议关闭重新打开蒙太奇，否则预览区可能停止播放
> - 插槽组与怪物动画蓝图的 [动画图表](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animgraph?application_version=4.27) 逻辑相关，只能使用已定义的插槽，新建插槽无法生效

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pPxKjimage.png)

将死亡动画序列拖放至Default槽位下，会自动把动画序列填充到Default片段中，预览动画会发现动画编辑器重复播放该动画片段。

![QQ2025119-192322-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/K6lIsQQ2025119-192322-HD-ezgif.com-video-to-gif-converter.gif)

为了使死亡动画的播放能卡到最后一帧，还需要添加一个循环片段，在Default片段上右键“新建蒙太奇片段”，输入片段的名称“Loop”将创建新的片段区域，并自动将该片段拼接到Default片段之后，绿色的游标尺代表该片段的起始位置，移动游标尺到动画的末尾表示循环片段将从末尾开始播放。

![QQ2025119-193616-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lehfaQQ2025119-193616-HD-ezgif.com-video-to-gif-converter.gif)

在片段编辑区的【预览】轨道处点击选中Loop片段，再次点击上方生成的Loop片段将在后面出现 ``X`` 标记，表示该片段播放完成后继续播放同片段，实现了循环播放Loop片段的效果，元素之心的死亡动画蒙太奇即配置完成。

![QQ2025119-195051-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bOxdtQQ2025119-195051-HD-ezgif.com-video-to-gif-converter.gif)

<br>

## 创建混合空间

编辑器内置了部分怪物的混合空间资源，开发者也可以基于已有的动画序列自行制作混合空间，下面以元素之心的移动混合空间为例，介绍创建的步骤。

工程目录下右键 ``动画 -> 混合空间1D``，选择目标怪物的骨骼，元素之心的骨骼为 ``SK_CH_UGC_Elements_Skeleton``，选中后将创建出混合空间资源。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1aCLjimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LZJpiimage.png)

双击打开混合空间，混合空间1D代表单一维度的混合，移动场景下以移动速度作为输入值，因此混合面板中只有水平轴单轴。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FLJokimage.png)

水平轴分为3个分区，分别对应速度为0、50和100时要播放的动画，将对应的动画序列资源拖拽到相应的采样点上，元素之心的移动混合空间即配置完成。

![QQ20251110-191816-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hRWVoQQ20251110-191816-HD-ezgif.com-video-to-gif-converter.gif)

绿色菱形点代表预览值，按住Shift键移动该点可以预览混合的效果，左上角的网格选项提供了显示动画名称的设置功能。

<br>

## 配置怪物动画

怪物动画的配置功能封装在 ``AnimListComp`` 组件中，组件预置了多种姿态的动画标签，每种姿态引用需要播放的动画资源，例如休闲姿态的标签为 ``GenericCharacterAnim.General.Idle.Relax``，引用的是“岩石巨怪待机”动画，则当怪物处于待机状态时播放此动画效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mx2Zfimage.png)

怪物模板默认都已配置了初始的动画资源，如有需要开发者仅需替换姿态对应的动画资源即可，目前根据应用场景的不同提供了两种怪物动画模式，各模式支持的姿态动画范围与所需的动画资源类型不同。

### 普通动画模式

普通动画模式属于默认的配置方案，适用于所有的怪物类型，此模式实现了较复杂的动画逻辑表现，因此支持的姿态动画更丰富，该模式的配置项通过 ``UGCSimpleMobAnimConfig`` 数据资产定义。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NENwyimage.png)

|姿态名称|姿态标签|动画资源类型|
|-|-|-|
|休闲移动|GenericCharacterAnim.General.Move.Relax|混合空间|
|战斗移动|GenericCharacterAnim.General.Move.Battle|混合空间|
|休闲待机|GenericCharacterAnim.General.Idle.Relax|动画序列|
|战斗待机|GenericCharacterAnim.General.Idle.Relax|动画序列|
|受击|GenericCharacterAnim.General.Hurt|动画序列|
|打断动画（击退）|GenericCharacterAnim.General.HitBack|动画蒙太奇<br>插槽：DefaultGroup.HitBack|
|死亡|GenericCharacterAnim.General.Die|动画蒙太奇<br>插槽：DefaultGroup.Death|
|左转135度|GenericCharacterAnim.General.Turn.135L|动画序列|
|右转135度|GenericCharacterAnim.General.Turn.135R|动画序列|
|空中动画|GenericCharacterAnim.General.Air.Falling|动画序列|
|落地动画|GenericCharacterAnim.General.Air.Landing|动画序列|

> - 击退动画的触发，取决于对怪物造成的伤害是否配置了 [受击数据](https://developer.gp.qq.com/wikieditor/#/catalog/20169)，且具备击退的水平/垂直方向上的速度
> - 落地动画播放时，怪物会被强制在原地不动以避免出现滑步问题
> - 由于怪物的攻击行为由技能触发，因此攻击动画需要通过技能编辑器的 [动画轨道](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E5%8A%A8%E7%94%BB%E8%A1%A8%E7%8E%B0) 配置

此外该模式提供了部分特化的动画参数供自定义调整：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/V4l0Rimage.png)

- 移动XY坐标：针对二维混合空间的移动设置，不建议修改
- 受击动画单次播放时长：表示受击动画播放的时间长度，建议根据动画的真实播放时长填写
- 受击动画连续播放CD：完整播放一次受击动画之后，隔多长时间才能再次播放

---

### 共享动画模式

共享动画是基于 [动画共享插件](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-sharing-plugin?application_version=4.27) 实现的一套动画优化方案，通过将同一骨骼、同一动画蓝图的怪物对象合并使用一份动画实例计算变换数据，节省大量CPU与内存的性能消耗，适用于海量同骨骼怪物播放同一套动画资源的场景。

共享动画模式的配置项由 ``UGCSimpleMobSharingAnimConfig`` 数据资产定义，配置形式上与普通动画模式一致，区别在于仅支持五种姿态动画，且只允许配置动画序列资源。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3ENxeimage.png)

|姿态名称|姿态标签|动画资源类型|
|-|-|-|
|休闲|GenericCharacterAnim.General.SharingStateAnim.Idle|动画序列|
|移动|GenericCharacterAnim.General.SharingStateAnim.Run|动画序列|
|攻击|GenericCharacterAnim.General.SharingStateAnim.Attack|动画序列|
|受击|GenericCharacterAnim.SubAnimType.Hurt|动画序列|
|死亡|GenericCharacterAnim.SubAnimType.Dead|动画序列|

> 共享动画模式提供了攻击姿态动画配置，技能编辑器中通过 [技能Task-播放预设动画](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E6%92%AD%E6%94%BE%E9%A2%84%E8%AE%BE%E5%8A%A8%E7%94%BB) 进行关联引用

<br>

## 注意事项

- 所有动画资源的骨骼必须与怪物骨骼网格体使用的骨骼一致才能正常播放
- 各模式中引用的动画资源类型必须与姿态对应的 ``动画类型`` 匹配
- 动画蒙太奇的插槽必须与姿态对应的 ``动画类型`` 中标注的Slot保持一致
- 如果怪物附带的动画资源不包含动画蒙太奇或者混合空间，可以使用动画序列自行创建相应的动画资源
- 部分老旧怪物资源的受击动画因配置问题可能存在播放异常现象，如遇到相关问题请联系绿洲官方人员处理






---


## 路点移动

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 路点移动

**涉及API:** `FollowWaypointPart`, `LogicPartManagerComp`, `STSpawnerWayPoint`, `SpawnConfig`, `StopRadiusScale`, `UGC怪物MOBA小怪巡逻行为树`, `UGC怪物行为树`, `WayPointArr`

# 路点移动

本文档介绍了怪物基于路点的寻路功能逻辑与操作方法，可以实现类似MOBA游戏中怪物沿指定路径寻路到达目标点的功能。

![2025-11-1411-55-19-ezgif.com-crop.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/c5LQ32025-11-1411-55-19-ezgif.com-crop.gif)
<br>

## 创建路点对象

编辑器菜单栏点击 ``窗口 -> 模式`` 打开模式编辑窗口，搜索 "AIWayPointActor" 找到路点对象Actor，将该Actor拖放到关卡场景中，可以看到其胶囊体。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JHcvkimage.png) ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oF9R0image.png)

<br>

## 配置怪物寻路路线

怪物寻路路线在 [怪物刷新点](https://developer.gp.qq.com/wikieditor/#/catalog/20156?autoJump=%E6%80%AA%E7%89%A9%E5%88%B7%E6%96%B0%E7%82%B9:~:text=%E6%80%AA%E7%89%A9%E7%BB%84%E8%A1%A8-,%E6%80%AA%E7%89%A9%E5%88%B7%E6%96%B0%E7%82%B9,-%E9%85%8D%E7%BD%AE%E5%88%B7%E6%96%B0%E7%82%B9) 中配置，在模式窗口中，搜索 "BP_UGCMobSpawner"，将怪物刷新点拖放到场景中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DvClUimage.png)

将创建的路点对象都拖放到怪物刷新点下，选中刷怪点对象中的 ``STSpawnerWayPoint`` 组件，属性 ``WayPointArr`` 数组 表示此路线的所有路点，将创建的所有路点配置到这个数组中（注意：数组的元素顺序就是路点的顺序）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Y4dhVimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QTU4Uimage.png)

<br>

## 怪物刷新点配置

完成路线配置之后，选中怪物刷新点根组件，在细节面板中，有下图几个关键的配置项：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gBjZDimage.png)

- 刷出的怪物阵营：若填写大于-1的值，其会覆盖怪物原本的阵营设置
- 使用路点寻路：勾选之后，此刷怪点出生的怪物才会使用配置的路点进行寻路
- 路点寻路方式：
	- CircleLoop表示成环循环，即到达终点后直接前往起点，一直循环
	- OneWay表示单向，即到达终点后停止 
	- OneWayReturn表示单次往复，即到达终点后原路返回起点，然后停止 
	- OneWayLoop表示往复循环，即到达终点后原路返回起点，一直循环下去

打开【实体编辑器】，创建一个模板小怪（实体编辑器怪物模板的行为树已经自带沿路点寻路功能）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6CXmNimage.png)

在场景中按照上述配置，然后找到 "怪物刷新点" 中 ``SpawnConfig`` 的 ``怪物蓝图`` 属性，配置刚才创建的模板小怪，运行调试，刷新出来的怪物即可实现沿路点移动。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hzHvmimage.png)

如果怪物没有移动，需要检查一下行为树中是否启用 ``巡逻`` 属性，以及是否配置导航网格，详情参见[怪物快速配置指南](https://developer.gp.qq.com/wikieditor/#/catalog/20144:~:text=%E6%80%AA%E7%89%A9%E7%B3%BB%E7%BB%9F-,%E6%80%AA%E7%89%A9%E5%BF%AB%E9%80%9F%E9%85%8D%E7%BD%AE%E6%8C%87%E5%8D%97,-%E6%80%AA%E7%89%A9%E8%A1%80%E6%9D%A1)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BWeNkimage.png)

<br>

## 逻辑管理组件配置

若想让怪物拥有沿路点移动的能力，找到怪物的 ``LogicPartManagerComp`` 组件，添加加 ``FollowWaypointPart`` 组件（此组件表示实体拥有了沿路点移动的能力，实体编辑器中的怪物模板都已经默认增加了这个组件）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2BHFhimage.png)

- CheckWayPointRadius：表示实体和当前目标的路点相隔多远就认为其已经到达了此路点
- FindWayType：表示实体寻路被打断之后，恢复寻路遵循的规则
	- FindPointInOrder：寻找已走过路点的下一个路点开始，按路点顺序继续寻路
	- FindNearestPoint：寻找距离实体最近路点，按路点顺序继续寻路
	- FindForwardPoint：寻找实体与距离路径垂线最短距离的路径，前往这条路径的终点，按路点顺序继续寻路（如下图所示：怪物原本寻路打断被拉到所在位置，重新开始寻路后，发现B路径的垂线F最短，怪物就会前往B路径的终点3，继续按路点顺序寻路）

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/n0fyAimage.png)

<br>

## 添加路点移动Task

行为树中添加 "[Generic]沿路点移动" 的任务节点，实现让实体沿配置的路点移动。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qPAWUimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eboZ3image.png)

> 此节点上只有一个参数 ``StopRadiusScale``，是Unreal底层的一个属性，不建议开发者进行修改

当前实体编辑器模板怪物内置的 ``UGC怪物行为树`` 已支持路点寻路，可在其子树 ``UGC怪物MOBA小怪巡逻行为树`` 中找到配置的沿路点移动任务节点，当实体进入巡逻状态时，如果有上述路点配置，则会执行沿路点移动的行为树。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RW5O5image.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xQtGMimage.png)


---


## 修改怪物模型

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 修改怪物模型

**涉及API:** `ColorTint`, `M_UGC_Character`, `Master_UGC_Mask_Base`, `Material`, `Parent`, `Texture`

# 修改怪物模型

编辑器内置了包含人形怪物、兽型怪物、机械怪物等多种类型与风格的怪物资源，由于怪物美术资源制作规范的复杂性与性能因素，暂未支持怪物骨骼与模型的自定义制作与导入，目前提供了基于已有怪物资源的换皮与附加模型的功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lycq4image.png)

<br>

## 怪物换皮

实体编辑器中各类怪物模板的材质均继承自 ``M_UGC_Character`` 或者 ``Master_UGC_Mask_Base`` 制作，开发者可以基于这两个材质创建新的材质实例，通过调整材质实例的颜色参数来达到换皮的效果。

1. 右键 ``材料和纹理 -> 材质实例``，创建新的材质实例资源

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BaP1aimage.png)
	
2. 打开材质实例，将 ``Parent`` 母材质设置为 ``Master_UGC_Mask_Base``

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kw6j6image.png)
	
3. 打开目标怪物的原始材质实例，将 ``Texture`` 下的原始色、法线和金属粗糙度等贴图资源复制到新建的材质实例中

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RTTBOimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ketrHimage.png)
	
4. 在新材质实例中启用 ``ColorTint`` 参数并调整为合适的颜色

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oWtnFimage.png)

5. 将新材质实例替换至目标怪物Mesh骨骼网格体组件下即完成换皮效果

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dLLbuimage.png)


<br>

## 部位换色

编辑器对于一些怪物模型使用的材质支持按照部位进行换色，开发者在实体编辑器面板上可以直接查看到当前模型是否支持换色。打开实体编辑器，对于可以换色的怪物模型，细节面板中 ``Material`` 属性下会出现四种颜色。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/m5lgSimage.png)

若不支持换色，细节面板中 ``Material`` 属性下则会显示不支持换色。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uP2primage.png)


目前支持的换色骨骼有“机器蝎模型”、“后排刺客模型”、“快枪手模型”。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3KTWIimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VOtHCimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Pr4Ngimage.png)

以下是实体编辑器中怪物模板的“后排刺客”为例演示部位换色。对于需要换色的区域，在细节面板中 ``Material`` 属性下点击区域后的按钮即可打开颜色选择器修改部位颜色。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/E8BkHimage.png)

|选定区域|效果图|
|-|-|
|原色|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mx3whimage.png)|
|区域一|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BLd6Nimage.png)|
|区域二|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bwgm8image.png)|
|区域四|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/f6fxWimage.png)|

<br>

## 附加模型

怪物蓝图提供了为怪物添加附加模型的功能，可以基于指定部位或者插槽挂载额外的静态模型。

打开怪物蓝图，在 ``挂载配置列表`` 属性下可以添加多组模型配置，每组模型需要指定挂载的部位或者骨骼的插槽名，且可以设置挂载点的偏移量，例如对近战僵尸怪的左手部位添加一个硬币模型。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TJTIpimage.png)

添加成功的模型将作为静态网格体组件追加到怪物的Mesh骨骼网格体组件下。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XYihvimage.png)

---


## 导航网格

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 导航网格

**涉及API:** `DataManager`, `ESS_MonsterCrowdMove`, `ESS_Navigation`, `NavMeshVolume`, `UGCGameMode`

# 导航网格
怪物的移动行为依赖寻路系统，通过导航网格生成可移动区域，同时AIWorldVolume赋予识别交互对象的能力，以下将以简单示例介绍如何快速创建与配置导航网格。

<br>

## 导航网格体

导航网格体(Nav Mesh Bounds Volume)可计算整个关卡区域的导航路径，寻路网格体用于控制在关卡中构建寻路网格体的位置，它用于为人工智能AI提供导航功能。

在该体积中，会在所有角度适合行走的表面上构建寻路网格体，可以根据生成所需寻路网格体的需要，重叠任意数量的此类体积。要使用寻路网格体边界体积，请创建一个或多个体积，将关卡的可寻路区域围住，再进行构建。

### 创建导航网格体

首先向场景中加入导航网格体 ```Nav Mesh Bounds Volume``` 组件，可以在模式选项卡的放置菜单栏下体积中找到对应组件或通过搜索 “Nav Mesh Bounds Volume” 找到该组件，然后将该组件拖入场景中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yq6bNimage.png)

调整缩放大小，保证可以完全覆盖需要生成的区域，可以在细节菜单栏中调整缩放大小。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RJQgPimage.png)

或者在视口中选中组件按R键进行缩放调整。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/faKxBimage.png)

---

### 导航网格烘焙

在顶部工具栏中可以找到 ``构建`` 按钮，如果已经创建并设置好缩放，点击即可生成Navmesh数据。等待片刻导航网格烘焙完成，可移动区域将以浅蓝色高亮显示，导航网格会自动识别障碍物并通过算法避开该区域。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/j88pPimage.png)

构建完成后即可看到生成的导航网格（按P可开关查看）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Inj9wimage.png)

Navmesh数据会生成在和在一个和关卡同一个目录，并且和关卡同名的文件夹中。开发者可以在内容浏览器中Asset文件夹下找到Navmesh文件夹，右击选择在浏览器中显示打开文件夹找到navmesh数据文件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1uvDlimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/G3o0simage.png)

<br>

## 添加AI World Volume

AIWorldVolume体积组件用于识别场景中的游戏对象，筛选怪物行为的目标，因此通常需要覆盖整个游戏场景。在模式编辑窗口中搜索 "AI World Volume" ，并将其放置在场景中，调整缩放大小使其覆盖整个关卡图的大小。
>一个关卡图中仅能放置一个 ``AI World Volume`` 体积组件

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Od8t8image.png)

``AI World Volume`` 同样需要调整缩放，操作方法和 ``NavMeshVolume`` 相同。

<br>

## 配置GameMode组件

打开 ``UGCGameMode`` 蓝图，该蓝图默认位于工程的 ``Asset/Blueprint`` 目录下。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oTQDdimage.png)

在细节面板中搜索 ``Component Manager`` 配置组，添加 ``ESS_Navigation`` 以及 ``ESS_MonsterCrowdMove`` 子系统，并按照下图配置好对应的子系统类组件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3A2nbimage.png)

在细节面板中搜索 ``DataManager`` 配置组，添加 ``GMData Source Navigation``，将会读取本关卡图的导航网格数据。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VDrPqimage.png)

配置完成后在工具栏中 ``编译`` 并 ``保存`` 配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5N53Timage.png)

此外，需要保证 ``世界设置`` 面板中的“游戏模式重载”蓝图类与当前工程的 ``UGCGameMode`` 蓝图类一致，点击 ``菜单栏 窗口 -> 世界设置`` 进行确认。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mXQx4image.png)

>若经过上述步骤后，怪物仍不能正常移动，则需要重新加载一下 ``UGCGameMode``，避免某些特定情况下，可能会出现引擎底层bug导致的游戏模式未能正确生效的问题；重载后还需要再确认下 ``UGCGameMode`` 的组件配置是否完整。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Cjq54image.png)


---


## 动态更新导航网格

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 动态更新导航网格

**涉及API:** `Add`, `AddDynamicNavAffect`, `AgentName`, `AsyncBuildNavmesh`, `AsyncIncrementalBuild`, `FName`, `Fbox`, `FinishedDelegate`, `Generation`, `GetNavigationGenerationFinishedDelegate`, `NavMeshBoundsVolume`, `UGCMathUtility`, `UGCMathUtility.MakeBox`, `UGCMathUtility.MakeVector`, `UGCNavigationSystem`, `UGCNavigationSystem.AddDynamicNavAffect`, `UGCNavigationSystem.AsyncIncrementalBuild`, `UGCNavigationSystem.GetNavigationGenerationFinishedDelegate`, `UObject`

# 动态更新导航网格

怪物的移动范围取决于 [导航网格](https://developer.gp.qq.com/wikieditor/#/catalog/20266) 的覆盖面积，通常是在编辑器视口中静态构建，如果希望在游戏运行时能够动态改变怪物的可移动范围，需要遵循指定的配置并调用相应的API来改变导航网格数据。

<br>

## 添加导航网格体

更新导航网格数据的前置条件是场景中存在导航网格体组件，可以参考 [创建导航网格体](https://developer.gp.qq.com/wikieditor/#/catalog/20266?autoJump=%E5%88%9B%E5%BB%BA%E5%AF%BC%E8%88%AA%E7%BD%91%E6%A0%BC%E4%BD%93) 的方式在关卡场景中添加 ``Nav Mesh Bounds Volume`` 组件。

> 导航网格体的覆盖范围需要包含待动态更新的区域，否则无法正常生成

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Sy7y3image.png)

<br>

## 配置更新规则

导航网格体添加到场景中后，会在【世界大纲】中自动生成一个名为“UAERecastNavMesh-Mannequin”的对象，它用来承载此地图中所有的导航网格数据对象，需要对该对象的属性进行调整才可开启动态导航网格更新。

选中 ``UAERecastNavMesh-Mannequin`` 对象，在【细节】面板中查找并勾选 ``UGCDyn Nav Data`` 属性，表示允许动态更新导航网格数据。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GdObYimage.png)

在 ``Generation`` 属性组下点击【显示高级项】按钮扩展详细列表。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qZrTYimage.png)

- Allowed Dynamic Nav Affectors：是否允许运行时局部更新导航网格，必选项，勾选后以下两个属性才能生效
- Dynamic Affector Update Interval：导航网格数据更新的检测频率，当检测到存在待更新的缓存区域时，则触发更新，仅针对 ``Dynamic Affector Update Mode`` 模式选为“Timed Trigger”时生效
- Dynamic Affector Update Mode：导航网格的更新模式
	- Timed Trigger：自动更新，依赖 ``Dynamic Affector Update Interval`` 的检测触发
	- Manual Trigger：手动更新，需要自行调用 [``AsyncIncrementalBuild``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AsyncIncrementalBuild) 触发更新

此外，提供了三种更新导航网格数据的算法策略，根据游戏地图设计的规模，需要选择合适的算法策略来加速运行时的生成效率。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rrenXimage.png)

- 单音调：快速划分区域，精确度低但是耗时少
- 转折：分水岭算法，更加精确但是比较耗时
- 厚实单音调：针对小型区域的单音调算法
	
建议开发者对大型地图（1KM * 1KM以上），在编辑器视口中静态构建导航网格的时候，使用 ``转折（分水岭算法）``；构建完成之后，若想实现动态构建再将此属性更改为``单音调`` 算法，以加快运行时更新导航网格的速度。

<br>

## 更新导航网格数据

### 全局更新

[``AsyncBuildNavmesh``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AsyncBuildNavmesh) 会对场景中所有寻路体积覆盖的区域进行一次性导航网格数据更新，在服务器端调用此接口即可进行导航网格的动态刷新。

首先在编辑器中【工具栏】点击【构建】按钮完成导航网格数据生成，接着在 ```NavMeshBoundsVolume``` 区域内创建一个平台,可以看到平台没有导航网格数据，然后在运行时全局更新导航网格后，平台生成新的导航网格数据。

|全局更新前的导航网格范围|全局更新后的导航网格范围|
|-|-|
|对于编辑器构建导航网格数据之后创建的平台，运行时未使用全局更新时没有导航网格数据。<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rI84Eimage.png) |对于编辑器构建导航网格数据之后创建的平台，运行时使用全局更新后生成了导航网格数据。<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/A4NEVimage.png)|


全局更新之前，在未被构建可运行区域的地方怪物无法进行寻路。

![2026-01-2015-39-40-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SRIN62026-01-2015-39-40-ezgif.com-video-to-gif-converter.gif)

调用接口进行导航网格的更新后，怪物可以进行正常寻路。

![2026-01-2015-39-51-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UAK3g2026-01-2015-39-51-ezgif.com-video-to-gif-converter.gif)


---

### 局部更新

要想触发导航网格数据的局部更新，需要先调用 [``AddDynamicNavAffect``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AddDynamicNavAffect) 标记待更新的区域，该区域将被缓存直到被更新模式触发为止：

- 手动更新模式：在合适的时机下脚本中调用 [``AsyncIncrementalBuild``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AsyncIncrementalBuild) 主动触发更新
- 自动更新模式：系统将在 ``Dynamic Affector Update Interval`` 间隔时间后自动调用 [``AsyncIncrementalBuild``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AsyncIncrementalBuild)

>对于需要局部更新的区域，必须要在 ```NavMeshBoundsVolume``` 区域范围内
寻路图烘焙区域Tile划分是100m x 100m，局部更新的是选定区域所在的一个Tile<br>

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hg6FLimage.png)

在局部更新时，先标记待更新区域,为了更好地演示，在这里对于标记的区域进行绘制以便观察。点击按钮"局部更新区域标记"调用接口 [``AddDynamicNavAffect``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AddDynamicNavAffect) 标记待更新的区域，即可发现红色线框区域为标记区域。

```lua
 local min  = UGCMathUtility.MakeVector(18610.0,21590.0,0)
 local max  = UGCMathUtility.MakeVector(20660.0,22530.0,520.0)
 local Fbox = UGCMathUtility.MakeBox(min,max)
 UGCNavigationSystem.AddDynamicNavAffect(self, "Mannequin", Fbox)
```

![企业微信截图_1770868009131.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wAdBc%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1770868009131.png)

标记完成后，如果选择手动更新模式，则需要手动调用更新，点击按钮"局部更新手动调用"手动调用接口 [``AsyncIncrementalBuild``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=AsyncIncrementalBuild) 触发更新。更新完成后即可发现标记区域导航网格数据已被更新。

```lua
---生效范围：服务器
---@param WorldContext UObject 当前世界上下文
---@param AgentName FName 作用Agent的寻路图名称一般为"Mannequin"
UGCNavigationSystem.AsyncIncrementalBuild(self, "Mannequin")
```

![企业微信截图_17708681194311.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/G4DMJ%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17708681194311.png)

[``GetNavigationGenerationFinishedDelegate``](https://developer.gp.qq.com/api/#/searchContent/UGCNavigationSystem?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCNavigationSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCNavigationSystem&autoJump=GetNavigationGenerationFinishedDelegate) 可以获取到更新结束的委托，进而绑定回调函数以执行特定处理逻辑。


![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dJktfimage.png)

```lua
local FinishedDelegate = UGCNavigationSystem.GetNavigationGenerationFinishedDelegate(self)
FinishedDelegate:Add(self.OnFinishGeneration, self)
```

当成功执行了局部更新后，标记的缓存区域将被移除，下一次更新需要重复执行标记与触发更新的操作。






---


## 无骨骼怪物模板

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 无骨骼怪物模板

**涉及API:** `CustomRotatingMovement`, `SpawnGenericCharacter`, `StaticMesh`

# 无骨骼怪物模板

玩法中可能存在海量刷怪的需求，例如弹幕游戏，如果使用带有骨骼动画的怪物模型，可能因大量动画数据解算导致出现性能问题，为此实体编辑器提供了基于静态模型的怪物配置方案，并且预置了几个怪物模板供开发者使用。并且对于同类型怪物还分别预设了三种等级模型。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/J4pgEimage.png)
<br>

## 创建无骨骼怪物蓝图

在编辑器上方工具栏中打开【实体编辑器】，在【怪物】页签的“怪物模板”类目下找到 **割草怪**，点击打开下拉栏可以看到预置的静态模型怪物模板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/c6XTWimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gOZoIimage.png)

选择其中任意一个模板创建怪物蓝图并打开该蓝图，可以发现在组件列表中没有动画相关的配置内容，并且新增了一个 ```StaticMesh``` 静态网格体组件来作为怪物的模型配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2o356image.png)

<br>

## 替换怪物模型

开发者若有替换怪物模型的需求，可以修改 ```StaticMesh``` 上的静态网格体资产。

> 因为无骨骼怪物是纯静态类模型，自身没有动画，所以如果开发者希望动画表现可以通过添加 ```CustomRotatingMovement``` 组件或通过代码逻辑实现基础的摆动或旋转效果

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Az6iEimage.png)

<br>

## 生成怪物对象

开发者可以使用 [```SpawnGenericCharacter```](https://developer.gp.qq.com/api/#/searchContent/UGCGenericCharacterSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%80%AA%E7%89%A9%E7%B3%BB%E7%BB%9F%2FUGCGenericCharacterSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGenericCharacterSystem&autoJump=SpawnGenericCharacter) 函数在服务端手动调用生成怪物对象，与普通骨骼怪物相同，由行为树的逻辑驱动怪物的状态行为，开发者可以自行扩展怪物行为。

```Lua
local MonsterClass = UGCObjectUtility.LoadClass(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Prefabs/Monsters/TestMonster.TestMonster_C'))
UGCGenericCharacterSystem.SpawnGenericCharacter(self, MonsterClass, {X = 1000, Y = 1000, Z = 0}, {Pitch = 0, Yaw = 0 , Roll = 0})
```

![2026-01-2015-26-13-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3SGdQ2026-01-2015-26-13-ezgif.com-video-to-gif-converter.gif)

---


## 丧尸法师案例

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > 丧尸法师案例

**涉及API:** `BehaviorControlComp`, `CastSkill`, `K2_SetActorLocation`, `LogicPartManagerComp`, `MoveControlComp`, `OverlapCheckArea`, `PESkillTargetPickerBase`, `PersistClientStateComponent`, `PreviewSetting`

# 丧尸法师案例

## 怪物机制描述
丧尸法师定位是一个远程Boss，感知范围，攻击范围都比较大。Boss有转阶段机制，一阶段和二阶段的技能有所不同，在行为树中通过血量来判断当前是否需要转阶段，两个阶段的怪物行为接近，但是二阶段的Boss会更加强大。

怪物每隔一定时间会释放一个技能，释放技能的间隙会根据当前距离或者其他因素来决定是移动还是传送还是其他行为。

<br>

## 创建丧尸法师
打开【实体编辑器】，在【怪物】页签的“怪物模板”类目下的 **首领** 栏中找到丧尸法师，并以丧尸法师为模板创建怪物蓝图。此处创建的怪物蓝图模板不是案例说明中的完全形式，是一个简易版本的丧尸法师。完整版的丧尸法师怪物模板在 ```功能演示模板``` 中可以找到。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FvEjtimage.png)

<br>

## 技能

### 基础技能

#### 火球术

丧尸法师向自身正前方发射三个火球，火球在发射出去一定距离之后会追踪玩家直到命中，造成少量伤害。对应的技能槽位为"Skill.Slot.Main"，怪物初始拥有。命中玩家之后有概率（0.33）给玩家施加一个持续2秒的燃烧BUFF。

![火球术.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wLEjI%E7%81%AB%E7%90%83%E6%9C%AF.gif)

1. 打开【技能编辑器】，在【技能】页签的“主动技能”的“模板”中找到 **直接释放技能模板** 并创建技能模板，命名为“BossSkill_FireBall"

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Wsnffimage.png)

2. 在刚才创建好的技能蓝图的 `PreviewSetting` 中，修改 `SPreview Actor Setting` 中 Actor类型为 **怪物**，并替换怪物蒙皮为“丧尸法师模型”。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dG9RVimage.png)

3. 在细节面板中修改技能外显信息，修改名字、描述与图标。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/okBrBimage.png)


4. 点击下方【状态列表】中的 `CastSkill` 将动画时间调整为1.4秒并为技能添加 **动画表现轨道** 和 **角色技能轨道** 。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZuaiZimage.png)

5. 点击动画表现轨道右侧的“+”打开下拉栏选中 `PESkill Animation` 搜索“僵尸法师释放技能”，添加动画表现。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MtLs7image.png)

6. 点击动画表现轨道右侧的“+”打开下拉栏选中 `New PESkill Task` 找到“发射抛体” 添加技能轨道。在刚才创建的Task下继续添加两个 **发射抛体** 以及 **追踪目标** 和 **选择目标** ，并将轨道Task修改到合适的开始与结束时间。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/F0Ullimage.png)

7. 选中 **选择目标** 在右上角详细设置中，设置选择器为 `扇形目标选择器` ，并修改选择器半径扇形张开角度以及选择器高度分别为3000、75、200；并修改 `PESkillTargetPickerBase` 最大数量为1。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0Xqniimage.png)

8. 选中 **追踪目标** 并修改最大吸附角度、角度吸附速度为180、90。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/r1nJEimage.png)

9. 在【抛体】页签中找到 **导弹** 并创建蓝图模板，修改特效为“火焰爆炸”，修改Buff为燃烧并添加 **播放声音** 动作播放火球爆炸事件并设置静态网格体为空。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hMtXsimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6kI5Himage.png)

10. 在刚才创建的火球术技能中的技能轨道选中 **发射抛体** ，设置抛体类为刚才创建好的抛体，并分别设置发射点与角度。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rM7Nwimage.png)

---

#### 强化火球术

和普通火球术类似，但是命中玩家之后不会施加BUFF，而回在命中的位置生成一个法术场，效果是一片燃烧的区域，玩家在其中会被持续施加燃烧BUFF。对应的技能槽位也是"Skill.Slot.Main"，是在行为树中动态修改的。

命中玩家产生的法术场持续3秒，每隔0.1秒给玩家施加燃烧buff，相当于是必定会收到燃烧buff影响，buff蓝图和上面一样。

1. 创建方式与火球术大致一致，只是在动作添加 **范围Buff** 时改为生成法术场。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TcLqAimage.png)

2. 在【区域】页签中找到 **空模板** 并创建蓝图模板，在默认场景根组件下添加Box盒体碰撞组件修改为合适大小以及若干粒子组件系统（ParicleSystem）并设置模板为地板燃烧。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hLuhOimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ysh4Bimage.png)

3. 修改 `OverlapCheckArea` 组件的细节属性。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qAsYAimage.png)

---

#### 传送

怪物原地起飞，一定延迟之后传送到指定的目标位置，传送的时候有特效生成。传送中核心的逻辑是在技能Lua代码中实现的。此技能默认挂在怪物"Skill.Slot.Slot4"槽位上。

![传送.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kZp7F%E4%BC%A0%E9%80%81.gif)

1. 创建方式与火球术类似，通过创建 **直接释放技能模板** 进行创建
2. 添加两个动画表现轨道分别为“跃起浮空”和“落地”并设置时间
3. 添加角色技能轨道—— `调用Lua脚本` 并设置Task细节绑定函数，在函数中调用 [`K2_SetActorLocation`](https://developer.gp.qq.com/api/#/searchContent/AActor?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAActor.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AActor&autoJump=K2_SetActorLocation) 实现位移。
	``` Lua
	function BossSkill_Teleport:TPToSelectTransform()
			local TargetPos = self:GetSelectTransform().Translation
			self:GetOwnerActor():K2_SetActorLocation(Vector.New(TargetPos.X, TargetPos.Y, TargetPos.Z + 88.0))
	end
	```
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BZTGEimage.png)
	
4. 添加角色技能轨道 `生成粒子` 并修改细节面板中 `粒子模板` 为“传送”，添加角色技能轨道 `播放音效` 并修改细节面板中 `音效` 为“传送发动事件”，角色技能轨道 `播放音效` 并修改细节面板中 `音效` 为“传送落地事件”。为他们设置合理的开始于完成时间。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/V73RPimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gzsYuimage.png)
	
---
	
#### 强化传送

机制和普通传送一致，区别在于技能开始时怪物进入无敌状态，技能结束时怪物离开无敌状态。因此他的创建方法和普通传送是一样的。

无敌逻辑也是在技能Lua代码中实现的。此技能是在行为树中动态修改的。

``` Lua
	--技能被触发事件调用
	function BossSkill_Teleport:OnActivateSkill_BP()
			print("BossSkill_Dash:OnActivateSkill_BP -- 技能触发")
			if self:HasAuthority() then
					print("BossSkill_Dash:OnActivateSkill_BP -- 设置无敌状态")
					--self.Owner.Owner:SetInvincible(true) 
					self:GetOwnerActor():SetGenericCharacterIsInvincible(true)
			end
			BossSkill_Teleport.SuperClass.OnActivateSkill_BP(self)
	end

	--技能结束发事件调用
	function BossSkill_Teleport:OnDeActivateSkill_BP()
			print("BossSkill_Dash:OnDeActivateSkill_BP -- 退出技能")
			if self:HasAuthority() then
					--关闭无敌状态
					print("BossSkill_Dash:OnDeActivateSkill_BP -- 关闭无敌状态")
					--self.Owner.Owner:SetInvincible(false)
					self:GetOwnerActor():SetGenericCharacterIsInvincible(false)
			end
			BossSkill_Teleport.SuperClass.OnDeActivateSkill_BP(self)
	end
```

<br>

### 特殊技能

##### 火焰冲刺

释放的时候怪物会向目标方向发起冲锋，最多对目标造成三次击退，并造成一次固定的伤害。冲刺持续过程中自身处于无敌状态并且隐藏自身模型。技能中的无敌和隐藏模型逻辑在对应的Lua代码中实现。

![火焰冲刺.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BeoIA%E7%81%AB%E7%84%B0%E5%86%B2%E5%88%BA.gif)

1. 打开【技能编辑器】，在【技能】页签的“主动技能”的“直接释放型技能”中找到 **冲刺** 并创建技能模板。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/shmMpimage.png)
	
2. 修改添加 **角色技能轨道** 为：冲刺、生成例子、调用Lua脚本、动态状态变化、追踪目标、选择目标、添加冲量、造成伤害以及若干添加冲量。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1ezprimage.png)

3. 编辑这个技能蓝图的Lua脚本，选中“调用Lua脚本”修改细节配置。
 
	```Lua
		function BossSkill_Dash:OnActivateSkill_BP()
				print("BossSkill_Dash:OnActivateSkill_BP -- 技能触发")
				if self:HasAuthority() then
						print("BossSkill_Dash:OnActivateSkill_BP -- 设置无敌状态")
						--self.Owner.Owner:SetInvincible(true) 
						self:GetOwnerActor():SetGenericCharacterIsInvincible(true)
				end

				BossSkill_Dash.SuperClass.OnActivateSkill_BP(self);
		end

		function BossSkill_Dash:OnDeActivateSkill_BP()
				print("BossSkill_Dash:OnDeActivateSkill_BP -- 退出技能")
				if self:HasAuthority() then
						--关闭无敌状态
						print("BossSkill_Dash:OnDeActivateSkill_BP -- 关闭无敌状态")
						--self.Owner.Owner:SetInvincible(false)
						self:GetOwnerActor():SetGenericCharacterIsInvincible(false)
				end
				BossSkill_Dash.SuperClass.OnDeActivateSkill_BP(self);
		end
	```
	 ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/92ekuimage.png)
	 
4. 设置“添加冲量”轨道Task细节。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lZSlLimage.png)
	
---

#### 火焰强化

怪物转阶段时刻释放的主动技能，全程无敌，释放的时候上浮到空中，在空中会向下持续发射火球，结束时候会落到地面并对周围一定范围内的玩家造成伤害。技能中的无敌和特殊逻辑在Lua代码中实现。

![火焰强化.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Esa5K%E7%81%AB%E7%84%B0%E5%BC%BA%E5%8C%96.gif)

1. 创建技能模板，添加多个技能阶段，分别为上浮，浮空，落地。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bSMbJimage.png)
	
2. 分别为三个阶段设置状态轨道。在上浮阶段添加上浮动画轨道，并添加角色技能轨道调用lua脚本实现无敌和上浮。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8O4Pkimage.png)
	``` Lua
		---设置无敌
		function BossSkill_TransSection:SetInvincibleEnable()
			ugcprint('设置无敌')
			self:GetOwnerActor():SetGenericCharacterIsInvincible(true)
		end
		
		---设置技能方向
		function BossSkill_TransSection:SetSelectDir()
    		self:SetSelectDirection(Vector.New(0.0, 0.0, 1.0))
		end
		
		---浮空
		function BossSkill_TransSection:SetGrivatyZero()
			ugcprint('设置重力系数...................')
			local MoveComp = self:GetOwnerActor():GetMovementComponent()
			if MoveComp then
					self.OriginGravityScale = MoveComp.GravityScale
					MoveComp.GravityScale = 0
					ugcprint('怪物重力系数设置为0')
    		end  
		end
	```
	浮空阶段主要在空中会向下持续发射火球，添加下浮空的动画轨道并且在技能轨道需要添加若干发射抛体，该抛体与强化火球术抛体大致一致。设置不同的发射角度和时机。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Fjs0Simage.png)
	
	下落阶段除了下落动画之外需要添加一个冲刺Task来实现下落的效果，在下落完成时向四周发射火球抛体，同时需要结束无敌状态。
	
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LWnMtimage.png)
	
	``` Lua
		function BossSkill_TransSection:SetInvincibleDisabled()
    		ugcprint('解除无敌')
    		self:GetOwnerActor():SetGenericCharacterIsInvincible(false)
		end
	```
	
---

#### 火球强化

二阶段持续存在的被动技能，怪物头顶会持续存在一个大火球，每隔一定时间会向前发射一个小火球，落地或者命中角色发生爆炸并造成伤害。此技能所有逻辑全部都是配置完成的。

![火球强化.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jyYEa%E7%81%AB%E7%90%83%E5%BC%BA%E5%8C%96.gif)

在【被动技能】页签下找到“空模板技能”，创建技能模板，修改技能配置。所使用的抛体与火焰强化二阶段抛体一致。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/w4DGXimage.png)

---

#### 陨石坠落

释放的时候会在玩家周围生成七个随机分布的陨石并下落，每个下落的陨石都有一个预警圈，被陨石命中的玩家受到伤害的同时会被施加一个持续1.25秒的眩晕buff，强制收回武器并无法操作角色。

![火球召唤.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KDh3R%E7%81%AB%E7%90%83%E5%8F%AC%E5%94%A4.gif)

创建技能模板并添加相应的动画与“选择点”和“发射抛体”等技能轨道，所发射的抛体创建方式与火球抛体类似，仅修改特效音效为陨石爆炸；修改粒子发射器为陨石(红)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8pyjTimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vOFSAimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xD0ieimage.png)

---

#### 强化陨石坠落

机制和普通的陨石坠落类似，区别在于，其落地之后还会在地面生成一个法术场，在区域中的玩家会被持续施加一个毒buff，持续流血。

![强化火球召唤.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ciiY6%E5%BC%BA%E5%8C%96%E7%81%AB%E7%90%83%E5%8F%AC%E5%94%A4.gif)

技能创建方式与陨石坠落一致，只是在创建技能轨道——发射抛体Task时替换抛体蓝图。强化陨石坠落的抛体陨石与普通陨石抛体类似，修改特效和粒子发射器为陨石(绿)，此外还需要添加一个生成法术场。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/833kaimage.png)

毒雾法术场的创建与之前火焰的类似。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JDcqDimage.png)

---

#### 召唤仆从

技能释放的时候会在怪物周围召唤四只近战僵尸小怪和两只远程僵尸小怪，小怪会响应boss的召集，即boss受击之后小怪会攻击玩家。每个小怪出生15秒之后会自杀，此逻辑使用一个被动技能实现。

![召唤小怪.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l6OMc%E5%8F%AC%E5%94%A4%E5%B0%8F%E6%80%AA.gif)
![怪物自杀.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/O23DZ%E6%80%AA%E7%89%A9%E8%87%AA%E6%9D%80.gif)

1. 创建主动技能模板。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RLECfimage.png)
	
2. 修改技能配置，添加动画轨道和技能轨道。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uqMvTimage.png)
	
3. 创建小怪模板，使用“近战僵尸”和“远程僵尸”作为小怪模板蓝图。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/b1uqCimage.png)
	
4. 为刚才创建的小怪添加额外的被动技能，来实现让小怪出生十五秒之后自杀。该技能通过怪物通用被动技能——“亡语-毒谭”作为模板实现。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MvRyDimage.png)

5. 修改技能配置。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XsHT5image.png)
	
6. 分别为创建的小怪添加被动技能。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7gm6limage.png)
	
7. 修改技能的角色技能轨道中“生成怪物”的细节面板，将Monster类设为刚才创建的小怪。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BOPdfimage.png)
	
---

#### 召唤强化仆从

召唤强化仆从和召唤仆从技能逻辑一致，区别在于强化仆从自杀时候会在其位置生成一个法术场，在法术场中的玩家会被持续施加一个中毒buff。

![怪物自杀2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3vWip%E6%80%AA%E7%89%A9%E8%87%AA%E6%9D%802.gif)

因此只需要在召唤仆从的基础上修改小怪技能，为小怪额外添加一个法术场技能，并且为该法术场技能配置“流血Buff”作为中毒效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jQOKmimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/c1fXSimage.png)
### 添加技能
打开刚刚创建的丧尸法师的技能组件 `PersistClientStateComponent` ，可以发现模板预设了两个技能，分别是“火球术”和“传送”，点击加号可以添加更多的技能，并将刚才创建的技能添加上去。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/H7HPmimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9hyx7image.png)

槽位Slot0，Slot1，Slot2是用来给技能组使用的，Main为普通技能火球术，Slot3是召唤仆从，Slot4是传送，Slot5是转阶段技能，在二阶段时候Slot5中的技能会替换为二阶段特有的被动技能。开发者可以根据自身需求 [创建技能](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%88%9B%E5%BB%BA%E6%B5%81%E7%A8%8B) 并添加技能 。

>开发者可以自行添加技能slot和tag，但必须遵循特定格式如"Skill.Slot.xxx"。

<br>

## 行为

### 仇恨

丧尸法师使用的仇恨系统和模板使用的相同，区别在于参数，为了突出丧尸法师这个远程Boss的特点，将寻敌感知半径调整为10m，视野半径调整为40m，并且视野角度为180°并且可以穿墙看到角色，同步的也将仇恨消失距离调整到了60m。

开发者可以在实体编辑器中打开创建好的怪物模板，在组件 `LogicPartManagerComp` 中设置仇恨参数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/INDajimage.png)

另外，其自身受击呼叫支援的范围也有所扩大，变为15m。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SGmTWimage.png)

其他的配置保持普通近战怪物的数据。

<br>

### 行为树

行为树中相关的配置暴露在 `BehaviorControlComp` 组件中，通过配置可以调整怪物施法技能的频率，距离，权重，巡逻相关的内容等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GOBGcimage.png)

#### 转阶段行为

行为树中实现了转阶段逻辑，主要是释放特定的技能和替换一些技能。如果血量少于阈值则会转阶。打开行为树，我们在根节点下面的selector节点中，添加了下面的逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1pRfeimage.png)

在执行一次行为树时候，会先判断当前血量是否低于了配置的数值。此数值在怪物的行为组件中配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eh1CXimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aLIVTimage.png)

注意，在判断转阶段的条件中有比对黑板中bHasChangeStage这个值是否为true，若不为true且血量低于设置值就需要执行下面的这个转阶段逻辑，执行的时候会先将bHasChangeStage这个键设置为true，这样保证了转阶段逻辑只会执行一次。

在转阶段中，首先执行释放转阶段技能的逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wBSQ3image.png)

然后执行一个修改技能的任务，此任务会修改怪物当前指定槽位上的技能，这样在二阶段时候，怪物释放一个slot中的技能时候，就会释放新的技能了。最后会执行一个通知脚本的任务节点，此节点执行之后会触发怪物脚本中的一个特定名称的方法。

``` Lua
function MagicMonster:OnBehaviorNotify_BP(NotifyMsg)
    ugcprint('OnBehaviorNotify_BP' .. NotifyMsg)
    if NotifyMsg == 'ChangeStage' then
        -- 转阶段
        self.CurrentStage = 2
        for k, v in pairs(self.CharactersHit) do
            UnrealNetwork.CallUnrealRPC_Multicast(self, "PlaySound", self.CurrentStage, v)
        end
    elseif NotifyMsg == 'Battle' then
        -- 战斗中
        
    end
end
```

---

#### 寻敌服务

在完成转阶段之后会一直执行寻敌服务，此服务的执行间隔为0.3S左右，表示每个0.3S左右的时间就会执行一次寻敌的操作，若寻敌成功，则将目标写入Target这个黑板键中，若寻敌失败则这个黑板键中的值将会是无效的。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6mOCrimage.png)

---

#### 进战状态

怪物在感知到敌人之后，若自身状态中没有战斗标签，则我们需要给怪物添加这个战斗状态，并且通知脚本，我们添加这几个行为树节点。装饰器节点是判断当前若已经存在了这个状态标签，则不会执行这个逻辑，保证进战斗时候这个逻辑不会重复执行。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kIvotimage.png)

---

#### 移动逻辑

当处理完成进战逻辑之后，需要先执行战斗中的移动机制，具体如下。

+ **过远处理机制** ：按照设计，在怪物距离目标大于配置的传送距离之后，需要执行传送逻辑，我们在进战右侧增加了一个选择节点，然后在这个选择节点下编写这个逻辑。首先需要判断距离，若通过了之后则会寻找目标的前方向上的一个点，然后传送到这个位置。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bhDdoimage.png)

+  **超过追击距离** ：若上面的判断未通过，则会去判断怪物和目标的距离是否超过了追击距离，若超过了则执行追击移动的行为此任务节点会控制怪物使用追击速度移动到目标附近，移动的时候若怪物和目标距离小于了这个追击距离则会中断移动，之后后续的逻辑。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JnMStimage.png)
	
+ **超过绕行距离** ：前两个判断都未通过后，会执行绕行检查，当距离大于配置的绕行距离之后开始执行。在此行为下，有几率执行绕行，若几率不满足则会执行一个选点传送的机制。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kPfzhimage.png)
	
	红色框中的内容，是先进行概率判断，通过之后会选择调用下面两个节点中的一个，实现随机左右移动的机制。若不绕行，则红框中的行为执行失败，会去执行Selector节点下右侧的子树。
	
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/s0SqNimage.png)
	
	这个子树中，会先选取敌人面前的一个可以到达的点，然后执行传送；若点未找到则会执行一次等待，这样可以保证这个行为最终必定成功。
	
+  **近距离传送机制** ：若前面的判断都未通过，则会执行距离检查，若此时距离小于配置的近身传送距离则执行传送逻辑。这样可以实现若玩家很靠近自身，则会自动传送到一个比较远的位置。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GBCVQimage.png)
	
+ **保底机制** : 若前面的检查均失败或者行为未成功执行，则会执行一个保底行为,有30%的几率传送到目标前面的一个较远的范围中，有70%的几率等待一定时间。这样保证了顶端的移动逻辑选择节点一定会返回成功。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lMSWkimage.png)

---

#### 攻击逻辑

当怪物执行完一次行为逻辑之后，会执行攻击逻辑。因为攻击行为需要有一定的冷却时间，所以在此行为的序列节点上增加了一个装饰器，判断上次执行的攻击时间到现在是否满足配置的冷却时长。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2BLlIimage.png)

若判断通过了，则按照顺序执行下属行为:
1. 转向，最终朝向目标
2. 等待一定时间
3. 执行释放技能组机制
4. 若技能组中没有技能可以释放，则释放基础技能火球术
5. 完成释放技能之后记录此时的时刻
6. 转向到朝向目标

---

#### 巡逻机制

若当前没有感知到敌人，则会执行巡逻机制。

+ 修改状态：和上文中进战类似，首次执行巡逻的时候我们需要将状态修改为脱战，直接将战斗Tag清除。注意，只有当怪物还存在战斗Tag的时候才执行清除操作，需要增加一个装饰器来判断。
	
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jjxsIimage.png)

+ 脱离范围返回：因为上面的修改状态逻辑在没有目标时候只会在首次执行，后续装饰器判断不通过会直接执行这个脱离范围返回的检查。若检测到怪物当前坐标距离出生点超过了指定的距离，会从巡逻范围中选择一个随机点前往。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7Jk1himage.png)
	
+ 正常巡逻：在正常情况下，即自身在巡逻范围内时候，会执行巡逻行为，每次都是等待一定时间之后在巡逻范围中随机选择一个点然后移动过去。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pm8XZimage.png)
	
---

#### 传送机制
因为传送是一个独立的行为，并且内部有多个节点组合形成，故我们可以使用一个单独的行为树进行封装，以方便复用逻辑。

在执行传送的时候首先需要确认如下几个条件是否满足：
+ 目标点是否有效
+ 传送是否处在冷却中
+ 目标位置到自身的距离是否大于最小传送距离

若条件判断通过了，才会最终执行传送行为，按照下列顺序执行：
1. 转向以面朝目标位置
2. 释放传送技能，将目标点作为参数传入
3. 记录传送时间
4. 转向以面朝目标位置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/knaJdimage.png)

<br>

### 动画 

和模板怪物不同的是，丧尸法师增加了左转和右转动画配置，并且只有转向角度大于135°才会播放动画，这个参数体现在行为树中的转向节点上。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jU2Pkimage.png)

注意，这个数值是在怪物移动中发生转向时候调用的，比如当前怪物朝向玩家A移动，玩家A下一刻传送到另一个位置，此位置在怪物身后，则此时怪物将会先执行平滑转向然后再执行移动。这个配置和行为树中的转向节点中的角度配置尽量保持一致，这样才可以将怪物表现调好。

<br>

### 移动

#### 避障

因为丧尸法师会召唤小怪，其在移动的时候需要避开这些怪，在 `MoveControlComp` 组件中开启引擎CrowdMove，并将避障组设置为0

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QdjvXimage.png)

同时，Boss召唤出的小怪也需要这样设置，小怪也是在实体编辑器中的，默认情况下创建的小怪模板已经设置好了这些小怪的避障逻辑了，无需再次修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dWLw2image.png)


---
