# 进阶内容/GamePlay系统/技能系统

> 本分类共 3 篇文章

---


## 状态互斥

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 状态互斥

**涉及API:** `Action`, `Add`, `AllowDynamicState`, `DA_UGCTagMappingTemplate`, `DynamicStateInterruptedHandle`, `DynamicStateTagRelationshipMapping`, `EnterDynamicState`, `GetOwnerActor`, `HasDynamicState`, `InterruptDynamicState`, `LeaveDynamicState`, `OnFlyInterrupt`, `PersistClientStateComponent`, `ReceiveBeginPlay`, `SetDynamicStateDisabled`, `SuperClass.ReceiveBeginPlay`, `UGCGameplayTagSystem`, `UGCGameplayTagSystem.EqualsTag`, `UGCGameplayTagSystem.RequestGameplayTag`, `UGCPersistEffectSystem`

# 状态互斥

游戏中的角色在不同行为下处于不同的状态，当同一时间内不允许同时生效多种状态时，这类状态间的冲突称为状态互斥，需要通过优先级或者覆盖规则来管理状态互斥关系。

<br>

## 状态概述

角色持续执行一段时间的行为都可以用状态来描述，例如基础的走路、奔跑、蹲下等状态，此外施放技能、执行攻击等交互行为也是一种状态，因此游戏中通常存在大量的角色状态。

### 状态表示

和平精英通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 的方式表示角色状态，每一种状态都是独立的标签，相较于传统的枚举类型，标签化的优势在于方便动态拓展且能实现树状的查找和父节点匹配，尤其在技能和Buff的复杂状态逻辑判定中更加灵活高效。

例如：禁用角色移动的场景，移动通常包括行走、游泳、飞行等多种状态，如果使用枚举类型需要实现很多条件判定分支逻辑；而采用GameplayTag，将各种状态定义成具体标签名：Movement.Walk、Movement.Swim、Movement.Fly，只需禁用Movement父节点，根据树形关系所有子节点标签将会自动被禁用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DpmWKimage.png)

---

### 状态切换

玩法中可以通过进入状态与退出状态来表示角色特定状态的切换，[UGCPersistEffectSystem](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem) 库提供了 [``EnterDynamicState``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=EnterDynamicState) 和 [``LeaveDynamicState``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=LeaveDynamicState) 两个函数分别用于实现状态的进入与退出。同一种状态允许多次进入，且每次进入状态都会累积计数，开发者可以通过 [``HasDynamicState``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=HasDynamicState) 判断当前角色是否存在该状态。


以飞行功能为例，当角色开始飞行时进入飞行状态，直至飞行结束时退出飞行状态，代码示例如下：

``` lua
-- 开始飞行
function UGCPlayerPawn:BeginFly()
	--不存在飞行状态再进入
	if not UGCPersistEffectSystem.HasDynamicState(self, "PawnState.Movement.Fly") then
		-- 进入飞行状态
		UGCPersistEffectSystem.EnterDynamicState(self, "PawnState.Movement.Fly")
		
		-- 具体飞行逻辑
  end
end

-- 结束飞行
function UGCPlayerPawn:EndFly()
	-- 退出飞行状态
	UGCPersistEffectSystem.LeaveDynamicState(self, "PawnState.Movement.Fly")
	
	-- 其他逻辑处理
end
```

---

### 和平角色状态

[GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 已经预设了和平精英人物角色所有的状态标签和部分功能系统扩展的特殊状态标签，开发者可以直接应用于角色执行特定行为前的状态判定，各类状态标签说明可参见 [角色状态标签](https://developer.gp.qq.com/wikieditor/#/catalog/20205?autoJump=%E8%A7%92%E8%89%B2%E7%8A%B6%E6%80%81%E6%A0%87%E7%AD%BE)。

<br>

## 状态互斥定义

状态中的互斥关系指状态的排他性，例如角色在走路时不能同时在跳跃，奔跑时不能同时趴着等，互斥的方式通常用 **打断** 和 **禁用** 来表示。如果两个状态之间没有任何互斥关系，则允许共存，例如：角色可以一边走路一边施放技能，因此施放技能状态和走路状态是非互斥的。

**打断状态**

当角色激活A状态时，如果当前正处于B状态，则会立即终止状态B的行为，此时角色不再拥有B状态，同时执行状态A相应的行为。

例如：角色处于蹲下状态时，此时开始施放技能，则蹲下状态将被打断，角色切换至施放技能状态并执行技能效果。

**禁用状态**

当角色激活A状态时，如果当前正处于B状态，则立即打断B状态且状态B将被禁用，无法再次被激活，同时执行状态A相应的行为，也即 ``禁用状态 = 打断 + 禁用`` 的复合效果。

例如：角色获得无敌状态时，将不受眩晕、中毒状态的影响，则无敌状态对眩晕和中毒属于禁用关系

<br>

## 创建互斥关系

### 实现状态互斥

如果开发者构建了新的 [状态Tag](https://developer.gp.qq.com/wikieditor/#/catalog/20102?autoJump=%E6%B7%BB%E5%8A%A0%E6%A0%87%E7%AD%BE)，并且希望为该状态赋予互斥关系，或者在预设的和平角色状态互斥规则基础上新增互斥关系，需要在业务逻辑中实现状态被打断的逻辑处理、是否被禁用的前置判定以及主动打断/禁用其他状态。

**状态是否被禁用**

脚本中可以通过是否能进入某个Tag标识的状态，来判断该状态是否已被禁用，如果被禁用则不允许进入该状态，开发者调用 [``AllowDynamicState``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=AllowDynamicState) 可获取判定结果。

代码示例：

```lua
-- 判断角色是否允许跳跃
local JumpTag = UGCGameplayTagSystem.RequestGameplayTag("PawnState.Action.Jump")
local CheckResult = UGCPersistEffectSystem.AllowDynamicState(self:GetOwnerActor(), JumpTag)

-- 支持Tag以字符型传参
local CheckResult = UGCPersistEffectSystem.AllowDynamicState(self:GetOwnerActor(), "PawnState.Action.Jump")
```

**状态被打断**

当被其他状态打断时，会触发 ``DynamicStateInterruptedHandle`` 委托，开发者需要绑定该委托并实现回调函数的逻辑。

```lua
function UGCPlayerPawn:ReceiveBeginPlay()
	UGCPlayerPawn.SuperClass.ReceiveBeginPlay(self)
	
	-- 绑定委托
	local PEComponent = UGCPersistEffectSystem.GetPersistBaseComponentByContent(self)
	PEComponent.DynamicStateInterruptedHandle:Add(self.OnFlyInterrupt, self);
end

-- 委托回调函数
function UGCPlayerPawn:OnFlyInterrupt(InterruptTag)
	if UGCGameplayTagSystem.EqualsTag(InterruptTag, "PawnState.Movement.Fly") then
		-- 实现被打断后的处理逻辑
	end
end

```

**打断/禁用其他状态**

脚本中调用 [``InterruptDynamicState``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=InterruptDynamicState) 和 [``SetDynamicStateDisabled``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=SetDynamicStateDisabled) 可实现主动打断/禁用其他状态的效果。

代码示例：

```lua
-- 打断交互状态
UGCPersistEffectSystem.InterruptDynamicState(self, "PawnState.Interacting")

-- 禁用持有武器
UGCPersistEffectSystem.SetDynamicStateDisabled(self, "PawnState.Action.HoldWeapon")
```

此外，在互斥规则表中配置打断和禁用的规则也能实现同等效果。

---

### 配置互斥规则

#### 互斥规则表

在不考虑技能、Buff等系统功能引入的额外互斥规则情况下，每个角色（如玩家、怪物）都可以拥有默认的状态互斥规则，这些规则由 **互斥规则表** 管理。

打开 ```UGCPlayerPawn``` 蓝图，找到 ```PersistClientStateComponent``` 子组件，在【细节】面板中找到 ```Tag Relationship Mapping``` 属性，该配置关联的即是互斥规则表。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/i6sOjimage.png)

编辑器预设了一套通用的状态互斥关系规则，双击打开互斥规则表 ```DA_UGCTagMappingTemplate``` 即可查看具体的配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tektWimage.png)

- Tag：角色状态标签
- Tag to Interrupt：该状态可以打断的目标状态
- Tag to Disable：该状态可以禁用的目标状态

> 系统预设的 ``和平角色状态`` 的互斥关系为固有规则，不允许删除或修改，但可以新增互斥规则

---

#### 覆写互斥规则

互斥规则表为内置资产资源，为只读属性无法直接修改，可以通过 ``PersistClientStateComponent`` 组件提供的 ``Tag Relationship Override`` 属性进行覆写修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5XqL8image.png)

---

#### 新建互斥规则表

如果编辑器预设的互斥规则绝大多数都无法满足玩法需求，可以创建新的状态互斥规则表以替换默认规则。

1. 于内容浏览器右键 ``各种各样 -> 数据资源``，基于 ``DynamicStateTagRelationshipMapping`` 类创建新的数据资产表。
	
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/q9DWSimage.png)

2. 在资产表中从0开始配置新的互斥规则。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/N6Z1uimage.png)

3. 将 ``PersistClientStateComponent`` 组件的 ```Tag Relationship Mapping``` 属性设置为新的数据资产表。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7sIMMimage.png)

<br>

## 技能系统中的状态互斥

类似技能编辑器与Buff编辑器等系统功能也涉及状态的判定，例如是否允许给角色添加Buff、角色当前状态是否能施放技能等，为了方便开发者配置和应用互斥规则，系统功能通过状态组的概念提供一组包含阻碍Tag、拥有Tag、打断Tag和禁用Tag的配置项，并对应实现了阻碍、打断及禁用等互斥行为对技能的影响结果逻辑，开发者无需关注实现细节。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NQDVvimage.png)

以 ``践踏`` 技能蓝图为例，查看蓄力（Charge）阶段配置，此阶段技能轨道上添加了一个 [技能Task-状态变化](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E7%8A%B6%E6%80%81%E5%8F%98%E5%8C%96) 用于设置需要打断和禁用的状态，效果为玩家在施放技能的蓄力阶段无法移动。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xEKh2image.png)

更多关于技能中的 [技能Task-状态变化](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E7%8A%B6%E6%80%81%E5%8F%98%E5%8C%96) 和Buff中的 [状态互斥](https://developer.gp.qq.com/wikieditor/#/catalog/20087?autoJump=%E7%8A%B6%E6%80%81%E4%BA%92%E6%96%A5) 设置说明可参阅相应的文档。


---


## 技能属性绑定

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能属性绑定

**涉及API:** `CastSkill`, `Getter`, `Indicator`, `PESkillTask_StateBranch`, `Radius`, `Setter`

# 技能属性绑定

属性绑定将蓝图属性与蓝图变量进行关联绑定，当变量值发生变化时，绑定的属性值将自动更新，从而实现技能蓝图的运行时动态配置效果。

<br>

## 属性绑定概述

属性绑定提供了一种动态调整技能蓝图属性的途径，可以根据外部脚本逻辑计算得到的结果来更新属性值，让属性不再局限于初始值的设置，变得更加灵活。

例如 [技能Task-发射抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E5%8F%91%E5%B0%84%E6%8A%9B%E4%BD%93) 具有一个 ``发射数量`` 属性，随着角色成长需要提升可发射的抛体数量，按常规做法需要配置多个技能蓝图，各蓝图设置不同的发射数量；当成长体系越发复杂时，需要配置的技能蓝图数量变得越来越多且不可控。如果使用属性绑定，只需将此属性与一个蓝图变量关联，角色成长时修改变量值则相对应发射数量也随之更新，这样在复用同一个技能蓝图的前提下，角色拥有了一个“新的技能”。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DXL1aimage.png)

<br>

## 使用属性绑定

要使用属性绑定的功能，首先需要创建蓝图变量，之后通过 ``属性设置器`` 将输出的结果保存到蓝图变量上，或者通过 ``属性求值器`` 将指定属性值与变量关联。

通常 ```属性求值器``` 和 ```属性设置器``` 可以配合使用。例如，实现 **狂暴技能** 时，可以用一个变量存储玩家的当前血量（Getter），另一个变量绑定技能的伤害（Setter），技能释放时根据血量动态调整伤害，血量越低、伤害越高。这样，技能的伤害值就会随着玩家血量的变化自动调整，无需每次手动修改，提高了游戏逻辑的灵活性。
> 蓝图变量的数据类型必须与属性值的类型严格保持一致，例如整形数值的属性，创建的蓝图变量的数据类型也应设置为整形

### 创建蓝图变量

在编辑器菜单栏中选择并打开技能编辑器，双击打开技能蓝图，找到 [```我的蓝图```](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%93%9D%E5%9B%BE%E5%8F%98%E9%87%8F) 页签。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5fCIHimage.png)

点击右侧【➕】按钮 ，将创建一个新的蓝图变量，点击变量名左侧的引脚按钮可以设置变量的数据类型，或者选中变量后在【细节】面板中修改变量相关属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/30ZeIimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4Joi8image.png)

新建的蓝图变量无法直接设置默认值，需主动点击【编译】按钮，编译后才能设置。

---

### **使用属性求值器**

属性求值器 ``Getter`` 可以将技能的属性值绑定到蓝图变量或者动态的计算值上，如此经过脚本逻辑计算产生的变化会反馈到属性值上，实现属性值的动态修改。

属性求值器目前支持两种使用方式：变量绑定与公式计算。

|类型|使用方式|示意图|
|:-:|-|-|
|变量绑定|将属性与相同数据类型的蓝图变量进行绑定，针对“Property”类型生效|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ql8SNimage.png)<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CNnM4image.png)|
|公式计算|基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 固定为 ``属性值 * A + B`` 的计算公式，计算变量支持常数，针对“Attribute”类型生效|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0HWmZimage.png)|

以 ```精确制导``` 技能为例，选中技能的 ``Indicator`` 阶段，在 [序列播放器时间轴](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E5%BA%8F%E5%88%97%E6%92%AD%E6%94%BE%E5%99%A8%E9%85%8D%E7%BD%AE) 上找到并点击打开 ``选择点`` 技能Task的参数面板，找到 ``选取器半径`` 属性，通过输入框右侧的下拉列表将新建的名为“Radius”的蓝图变量与该属性绑定，此时输入框被置灰即完成变量绑定。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jxsnpimage.png)

绑定完成后，开发者可以在脚本里动态修改变量 ``Radius`` 的值，而 ```选取器半径``` 的属性值也被同步更新。

---

### **使用属性设置器**

属性设置器 ```Setter``` 能够将事件的输出参数通过蓝图变量存储及传递数据，脚本中可以访问这个变量值，进一步处理业务逻辑或更新属性值。

以 ```精确制导``` 技能为例，在 ```CastSkill``` 阶段添加一个技能Task，类型选择 [PESkillTask_StateBranch](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-PESkillTask_StateBranch)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RJpJpimage.png)

打开 ```PESkillTask_StateBranch``` 的 [Task参数面板](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=Task%E5%8F%82%E6%95%B0%E8%AE%BE%E7%BD%AE)，添加一个 [```受到伤害事件```](https://developer.gp.qq.com/wikieditor/#/catalog/20112?autoJump=%E5%8F%97%E5%88%B0%E4%BC%A4%E5%AE%B3%E4%BA%8B%E4%BB%B6)，该事件拥有一个浮点型且名为“伤害”的参数输出类属性。新建一个浮点型蓝图变量Damage，通过“伤害”属性的下拉列表选择并绑定该变量，当受到伤害时，Damage变量将接收并存储伤害值。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fGfolimage.png)

开发者可以在技能释放结束时打印该变量值，验证属性设置器的输出效果。

代码示例：

``` lua
function MissileSkill:OnDeActivateSkill_BP()
    MissileSkill.SuperClass.OnDeActivateSkill_BP(self)
    ugcprint("触发")
    ugcprint(self.Damage)
end
```

打印结果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DxGCRimage.png)



---


## 法术场

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 法术场

**涉及API:** `Actor类型`, `CheckType`, `OverlapAllDynamic`, `OverlapCheckArea`

# 法术场

法术场是基于区域检测机制的持续性技能效果对象，通常适用于场景类技能效果的表现，例如毒雾陷阱、火龙卷、治疗泉水等等，技能编辑器封装了一套可配置化的法术场技能框架，并提供了多种蓝图模板帮助开发者快速实现法术场功能。

<br>

## 法术场概述

法术场作为一种特殊的技能效果，具有以下特征：

- 区域范围：范围通常是一个固定的区域（例如圆形或矩形），且效果作用于区域内的所有有效目标上，而非特定的单体目标
- 持续存在：法术场生成后不会立即消失，而是持续存在一段时间
- 周期性触发：以固定的频率周期性检测区域内的有效目标并执行效果的触发

### 基础框架

基于法术场的特征，以事件驱动的架构模式实现了法术场的框架，一个完整的配置框架由基础属性、区域检测、触发事件与执行动作等核心模块组成。

**基础属性**

法术场包含持续时间和检测间隔等基础属性，用以决定法术场的生命周期和效果触发频率。

**区域检测**

通过碰撞体组件决定法术场的区域范围，区域重叠检测组件对区域内的目标按指定的过滤条件进行筛选，选取结果即为法术场效果的作用目标。

**触发事件**

法术场提供了一批特定的事件，当事件触发时执行指定的动作行为以实现目标效果，即触发事件决定了动作的执行时机。

**执行动作**

当特定事件触发时需要执行的具体动作行为，目前法术场可执行的动作为释放技能或者添加Buff。

---

### 蓝图结构

法术场蓝图主要由 ``Collision（碰撞体）组件``、粒子特效、技能组件和区域重叠检测组件组成。

[碰撞体组件](https://dev.epicgames.com/documentation/unreal-engine/collision-overview?application_version=4.27&lang=zh-CN) 用于定义碰撞的检测范围，根据检测范围形状的不同分为 ``BoxCollision（立方体碰撞体）``、``CapsuleCollision（胶囊体碰撞体）`` 和 ``SphereCollision（球体碰撞体）`` 三种简单碰撞体。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/U5Whnimage.png)

法术场根组件下可以挂载粒子特效组件，用于体现法术场的具体形态或者特效表现。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Nwtmjimage.png)

由于法术场可执行技能或者Buff效果，因此需要添加技能组件以保证技能逻辑的执行和同步。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fSeb9image.png)

区域重叠检测组件基于碰撞体组件的范围进行目标检测，决定法术场效果的作用目标结果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VXDmjimage.png)

<br>

## 法术场模板

根据法术场效果的特性，提供了伤害场、治疗场、陷阱及发射抛体等四类模板，开发者可以基于特定模板或者空模板创建法术场蓝图并配置需要的功能效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JZpPnimage.png)

【伤害场】

以毒气为例，会在指定地点生成一团毒气，并对进入毒气范围内的敌人造成持续伤害。

![法术场毒烟.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/52PA1%E6%B3%95%E6%9C%AF%E5%9C%BA%E6%AF%92%E7%83%9F.gif)

【治疗场】

对进入治疗场范围内的同伴进行持续治疗。

![法术场治疗.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5lYlE%E6%B3%95%E6%9C%AF%E5%9C%BA%E6%B2%BB%E7%96%97.gif)

【陷阱】

对进入陷阱范围内的目标造成伤害和眩晕效果。

![QQ20251030-171853-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TDB7tQQ20251030-171853-HD-ezgif.com-video-to-gif-converter.gif)

<br>

## 创建法术场蓝图

开发者可以基于法术场模板创建法术场蓝图，以创建火龙卷类型的法术场为例：

1. 打开技能编辑器，切换至【区域】页签，从“法术场模板”窗口中选择 ``火龙卷``，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``火龙卷`` 为模板创建”

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/80k6vimage.png)

2. 点击“以 ``火龙卷`` 为模板创建” 按钮，弹出输入名称弹窗，输入法术场名称并点击确定

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UoEECimage.png)

3. 新建的法术场将显示在“工程法术场资源”窗口中，且法术场蓝图创建于 ``Asset/Blueprint/Prefabs/Regions`` 路径下

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OC4aBimage.png)

<br>

## 法术场配置详解

### 基础属性

法术场的基础属性决定存在的时长及效果的触发频率。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/q5jAtimage.png)

- 执行间隔：法术场的检测间隔时间，决定目标选取的频次和持续事件的触发频率
- 持续时间：法术场存在的时间，超过该时间后，法术场将被直接销毁
- 无目标激活：若勾选，则未选取到目标也可以触发事件对应的动作
- 创建类型：定义此法术场的创建方式
	- 由技能创建：通过技能/抛体释放法术场
	- 由自身创建：放置在关卡场景中生成，该方式生成的法术场无Owner
- 默认阵营ID：``创建类型`` 选择“由自身创建”时生效，为法术场分配一个阵营ID，此ID将作为后续 ``释放技能`` 动作时执行选取或者相关逻辑处理的的阵营值

<br>

### 区域检测

法术场支持自定义添加碰撞体组件，可以通过点击【添加组件】自行添加合适形状的碰撞体，调整碰撞体的大小以适配法术场的范围。

> 若无特殊需求，建议将碰撞通道预设置为 ``OverlapAllDynamic``

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/po3Tsimage.png)

确保法术场配置了区域重叠检测组件并关联碰撞体组件，模板默认配置了区域重叠检测组件，如有需要可以通过点击【添加组件】自行添加。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QcoB6image.png)

- BeginPlay自动开始检测：是否该组件启动BeginPlay时就进行检测
- CheckType：基于碰撞事件回调做检测还是Tick每帧检测，不推荐使用Tick，会有额外的性能消耗
- ObjectTypes：检测的Actor类型，不填代表所有Dynamic对象
- ChannelTypes：检测的碰撞通道类型，若有特殊需要可自行配置
- Overlap组件：选择需要用于区域检测的碰撞体组件
- Event模式下第一次主动检测的方式：``CheckType`` 为“Event”时第一次主动检测使用的组件，建议与模板的默认配置保持一致
- Check间隔：基于Tick检测模式下的检测时间间隔，仅针对 ``CheckType`` 为“Tick”时生效

<br>

### 碰撞过滤器

法术场应用了 [过滤器](https://developer.gp.qq.com/wikieditor/#/catalog/20218) 实现碰撞结果的筛选，符合过滤要求的碰撞单位才会受到法术场的效果影响。

<br>

### 触发事件

法术场提供了一批事件，以支持事件驱动动作的执行。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hXQgcimage.png)

- 进入事件：当目标进入法术场的检测区域时触发
- 退出事件：当目标退出法术场的检测区域时触发
- 持续事件：当目标持续在法术场检测区域内时，周期性被触发，触发间隔由 ``执行间隔`` 属性决定
- 开始事件：当法术场生成时触发
- 结束事件：当法术场销毁时触发

<br>

### 执行动作

当指定事件触发时，执行特定动作，该动作对检测到的所有目标均生效。

#### 释放技能

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VtKFZimage.png)

- 技能Class列表：要执行的目标技能蓝图

> 法术场作为该技能的施法者，由于法术场通过区域检测的方式选取目标，因此执行的技能无需再额外配置选取目标相关的Task

---

#### 添加Buff

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EqdCSimage.png)

- Buff类型：需要添加的Buff蓝图
- 添加的层数：覆盖Buff的添加层数参数，-1代表不覆盖
- 覆写生效时长：覆盖Buff的持续时间参数，-1代表不覆盖

---

#### 调用Lua脚本

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/b3l8Oimage.png)

- ExecuteFunction：执行的lua函数

<br>

### 基于事件触发的多技能使用

当法术场满足在事件时支持释放多个技能

#### 法术场事件


![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qkqCBimage.png)

- 技能Class列表：需要触发的技能
- 事件类型：
  - 进入事件：当目标进入法术场的检测区域时触发
  - 退出事件：当目标退出法术场的检测区域时触发
  - 持续事件：当目标持续在法术场检测区域内时，周期性被触发，触发间隔由 ``执行间隔`` 属性决定
  - 开始事件：当法术场生成时触发
  - 结束事件：当法术场销毁时触发
- 执行动作：
  - 释放技能：触发技能列表中已配置的技能,具体可参考[释放技能](https://developer.gp.qq.com/wikieditor/#/catalog/20217?autoJump=%E9%87%8A%E6%94%BE%E6%8A%80%E8%83%BD:~:text=%E7%9B%AE%E6%A0%87%E9%83%BD%E7%94%9F%E6%95%88%E3%80%82-,%E9%87%8A%E6%94%BE%E6%8A%80%E8%83%BD,-%E6%8A%80%E8%83%BDClass%E5%88%97%E8%A1%A8)
  -  添加buff：添加的buff，具体可参考[添加Buff
](https://developer.gp.qq.com/wikieditor/#/catalog/20217?autoJump=%E6%B7%BB%E5%8A%A0Buff:~:text=%E7%9B%B8%E5%85%B3%E7%9A%84Task-,%E6%B7%BB%E5%8A%A0Buff,-Buff%E7%B1%BB%E5%9E%8B%EF%BC%9A%E9%9C%80%E8%A6%81)
  -  调用Lua脚本：触发已配置的Lua脚本，具体可参考[调用Lua脚本](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E8%B0%83%E7%94%A8Lua%E8%84%9A%E6%9C%AC:~:text=%E6%B7%BB%E5%8A%A0%E7%BB%99%E7%9B%AE%E6%A0%87-,%E6%8A%80%E8%83%BDTask%2D%E8%B0%83%E7%94%A8Lua%E8%84%9A%E6%9C%AC,-%E5%9C%A8%E6%8C%87%E5%AE%9A%E7%9A%84)
  - 无目标激活：是否需要拥有目标才会激活法术场
  - 创建类型：
    - 由技能创建：法术场持有其施法者的信息，可用于追溯施法者
    - 由自身创建：法术场不携带施法者信息，但需额外配置[阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)


#### 碰撞事件

若要通过碰撞事件触发技能，必须先在目标的``OverlapCheckArea``组件中，正确配置所需碰撞盒的名称，仅当事件类型配置为``进入事件``和``退出事件``时该配置才可生效

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LdE6Nimage.png)

- Check Type：检测方式
  - Event：事件触发
  - Tick：根据Check间隔进行触发
- ObjectTypes：需要检测的碰撞对象类型，若为空则检测所有类型
- ChannerlTypes：需要检测的碰撞对象类型，若为空则检测所有类型
- ComponentName：需要触发事件的碰撞盒名称
- Event模式下第一次主动检测的方式：该配置选项忽略，不用改动
- Check间隔：当选择Tick模式下时，可以配置检测的间隔


碰撞事件也支持多个碰撞盒组合触发，但前提是必须为目标对象添加并**配置相应的 `` OverlapCheckArea ``组件**，并正确配置 ``ComponentName ``，才能确保事件正常触发

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3oJxyimage.png)


## 应用法术场

目前支持在关卡场景中放置和主动释放两种应用法术场的方式。

### 场景放置生成

当法术场蓝图的 ``创建类型`` 属性设置为“由自身创建”时，可将法术场蓝图拖放至场景中，游戏运行时即生成该法术场对象。

> 法术场的生命周期取决于法术场技能的持续时间

![1-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/g4ffs1-ezgif.com-video-to-gif-converter%20(1).gif)

---

### 主动释放法术场

可通过技能或者抛体的蓝图配置法术场功能，通过动作触发释放法术场。以技能释放场景为例，提供了 [生成法术场](https://developer.gp.qq.com/wikieditor/#/catalog/20186?autoJump=%E6%8A%80%E8%83%BDTask-%E7%94%9F%E6%88%90%E6%B3%95%E6%9C%AF%E5%9C%BA) 的技能Task。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XUbYsimage.png)

配置好法术场的参数后，当释放该技能时，即会在场景中生成一个火龙卷法术场，对进入火龙卷范围内的敌人造成伤害。

![法术场龙卷风.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jv7PO%E6%B3%95%E6%9C%AF%E5%9C%BA%E9%BE%99%E5%8D%B7%E9%A3%8E.gif)

<br>

## 注意事项

当法术场的动作为释放技能时，需要注意以下两点：

1. 法术场为技能的施法者，因此部分技能Task并不适用法术场的技能配置，例如 [自动瞄准](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E8%87%AA%E5%8A%A8%E7%9E%84%E5%87%86) Task，推荐配置技能蓝图时，将 [技能预览设置](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E9%A2%84%E8%A7%88%E8%AE%BE%E7%BD%AE) 中的 ``Actor类型`` 选为“法术场”，技能轨道会自动过滤不可用的Task。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZNA2Zimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EaZKPimage.png)

2. 部分技能Task涉及对Owner对象的依赖，例如 [造成伤害](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3) Task，当 ``伤害数值`` 设为“公式计算”且 ``伤害数值属性来源`` 设为“Causer”时，依赖于施法者的属性进行伤害计算。此时，如果法术场是由场景放置生成的，则会因为无Owner而导致逻辑异常，因此使用场景放置生成法术场的时候，需要确保技能的逻辑没有对Owner相关的依赖。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Cqz1Wimage.png)



---
