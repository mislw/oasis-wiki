# 进阶内容/GamePlay系统/属性与伤害

> 本分类共 8 篇文章

---


## 通用属性系统

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 通用属性系统

**涉及API:** `AttrModifyComp`, `AttributeOwnerActor`, `FGameMagnitudeContext`, `GetEndurance_Override`, `TestAttribute`, `UGCAttributeGroup_Character`, `UGCAttributeSystem`, `UGCAttributeSystem.GetGameAttributeValue`, `UGCGameSystem`, `UGCGameSystem.UGCRequire`, `UGCNativeGameAttributeType`, `UGCRequire`

# 通用属性系统
  
属性系统是一套通用的对象属性管理框架，旨在为开发者提供统一、灵活的访问或修改游戏对象（如角色、枪械等）属性的方式，支持创建属性、动态修改属性及构建属性推导逻辑等，属性可应用于 [技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091)、[Buff编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20087)、[物品编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20101) 等多类系统功能中。  

<br>

## 属性系统概述

所有自定义属性在 ``属性管理器`` 中创建及管理，各属性会被 ``属性修改组件`` 和其他涉及属性的系统功能引用，在 ``属性修改组件`` 中可以对指定属性进行初始值的覆盖修改，当对象挂载了该组件时将拥有这些属性，继而在运行时能够访问到属性、正常执行属性的动态计算。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VItSsimage.png)

<br>

## 属性管理器 

点击绿洲启元编辑器菜单栏的【属性管理器】按钮，将打开属性管理器的操作界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/c1aXSimage.png)

### 属性类别

属性管理器包含多个页签：基础属性、人物属性、武器属性、载具属性、伤害公式与治疗公式，其中 [伤害公式](https://developer.gp.qq.com/wikieditor/#/catalog/20099) 与 [治疗公式](https://developer.gp.qq.com/wikieditor/#/catalog/20216) 可以结合属性定制伤害与治疗的计算逻辑，其他四类属性页签功能用于管理不同的适用对象的属性。

- 基础属性：适用于创建通用型属性，挂载 ```属性修改组件``` 的实体对象（包括角色、怪物、载具等）都将拥有这些属性  
- 人物属性：此类属性对玩家角色与 [新怪物](https://developer.gp.qq.com/wikieditor/#/catalog/20144) 均生效，适合扩展独有的角色属性
- 武器属性：针对枪械武器的属性定义
- 载具属性：针对载具的属性定义

#### 固化属性

人物属性、武器属性和载具属性均预设了各类对象的部分通用属性，该类属性无法在属性管理器和属性蓝图中修改，但仍然受 ``属性修改组件`` 的覆盖影响，各属性具体的含义可参考 [角色固化属性](https://developer.gp.qq.com/wikieditor/#/catalog/20205?autoJump=%E8%A7%92%E8%89%B2%E5%9B%BA%E5%8C%96%E5%B1%9E%E6%80%A7)、[枪械固化属性](https://developer.gp.qq.com/wikieditor/#/catalog/20159) 与 [载具固化属性](https://developer.gp.qq.com/wikieditor/#/catalog/20246)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AKD0Gimage.png)

#### 自定义属性

在“自定义属性”类别下可以编辑自定义的属性，支持添加、修改、删除等操作，编辑后点击右上方“保存”按钮以保存编辑内容。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GQAygimage.png)

|字段名|字段说明|
|-|-|
|属性名|属性的唯一标识符，只支持英文字符和下划线_，不可重名<br>支持复合属性，用“\|”分隔，例如："Health\|MaxHealth"|  
|属性描述|属性的含义说明，涉及属性的蓝图配置中将以 ``「属性描述」-「属性名」`` 的格式展示|
|默认值|属性的初始值，可被 ``属性修改组件`` 覆盖修改，默认值必须位于最小值和最大值之间|
|最小值|属性值的下限，建议不小于-100000000|  
|最大值|属性值的上限，建议不大于100000000(最大值与另一自定义属性绑定，使其随该属性值动态变化)| 
|即时属性|当属性被标记为即时属性时，其仅支持``永久修改``修改| 

除了在属性管理器界面中编辑属性，也支持在属性蓝图中编辑，点击属性页签，将自动在 ``Asset/Blueprint/Attributes`` 路径下生成对应的属性蓝图，编辑方式和属性管理器界面保持一致。

- 基础属性蓝图：UGCAttributeGroup_Base
- 人物属性蓝图：UGCAttributeGroup_Character
- 枪械属性蓝图：UGCAttributeGroup_Weapon
- 载具属性蓝图：UGCAttributeGroup_Vehicle

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BbA6qimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/P8cx8image.png)

---

### 属性导出

属性管理器中的所有属性都会以键值对形式的table自动导出到工程的 ``Script/GameAttribute/game_attribute_type.lua`` 脚本中，按固化属性（Native）和自定义属性（Custom）类别各自生成两个表：属性名映射表 [``UGC{类别}GameAttributeType``] 和属性引用别名映射表 [``UGC{类别}GameAttributeTypeCommentMap``]。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/twfDzimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3LSGWimage.png)

**注意**
> 开发者的自定义属性名不可与系统预置的属性名相同，否则将出现非预期的功能问题

<br>

## 属性修改组件

属性修改组件 ``AttrModifyComp`` 是一类 [ActorComponent子组件](https://dev.epicgames.com/documentation/en-us/unreal-engine/components-in-unreal-engine?application_version=5.4)，可以挂载在任意Actor对象上，只有挂载了该组件的对象才能引用属性管理器里创建的属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kgaOqimage.png)   

选中 ```AttrModifyComp``` 组件，在【细节】面板中找到 ``Custom Game Attribute`` 属性组， 该组下提供了 `属性初始值配置` 项，开发者可以在此处设置属性的初始值，用以覆盖属性管理器中属性的默认值。
> 覆盖的属性值仅针对该对象生效

以下图为例，对玩家角色的固化属性 ```血量``` 、```最大血量``` 以及自定义属性 ```TestAttribute``` 重新覆写了初始值，游戏开始后玩家的这些属性初始值将为新值。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xnPzqimage.png)

> `自定义属性集列表` 与 `自定义属性列表` 已弃用，开发者无需配置此项

<br>

## 使用属性

### 属性绑定及修改

涉及属性的系统通常都通过蓝图配置的方式，提供 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 或基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的修改属性的功能，例如技能编辑器中的 [角色修改属性](https://developer.gp.qq.com/wikieditor/#/catalog/20117?autoJump=%E4%BF%AE%E6%94%B9%E5%B1%9E%E6%80%A7) Task支持修改技能施法者的指定属性值。

> [属性基础值](https://developer.gp.qq.com/wikieditor/#/catalog/20153?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E5%99%A8%E6%A6%82%E8%BF%B0) 会受 ``属性修改组件`` 的覆盖影响

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rcYZCimage.png)

通常属性修改支持基于常数、计算公式或者指定Lua函数的修改方式。


#### 即时属性

当一个属性被标记为即时属性时，这类属性涉及属性修改时，只能使用永久修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PmOmDimage.png)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7QTuDimage.png)

### 最大值属性

一个属性的最大值可以动态绑定到另一个属性上，此时其最大值将随目标属性的实际数值影响。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/INMl2image.png)

#### 计算公式

计算公式固定为 ``属性值 * A + B`` 的计算方法，计算变量支持常数或者float类型的属性绑定。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/a2KQ2image.png)

#### 指定Lua函数

属性修改支持将一个Lua函数注册为伤害计算的回调函数，从而允许在Lua侧通过自定义逻辑来决定伤害结果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dHQZoimage.png)

可在Lua中定义一个自定义方法，用于实现伤害计算逻辑。该方法接收一个 ``FGameMagnitudeContext`` 结构体类型的参数，依据其中的伤害信息进行计算，需返回一个 ``number`` 类型的结果。

**代码示例**

``` Lua
function DamageSkill:MyTureDamage(DamageContext)
    local TheDamage = 0
    if UGCGenericCharacterSystem.IsGenericCharacter(DamageContext.TargetActor) then
        TheDamage = UGCGenericCharacterSystem.GetHealth(DamageContext.TargetActor) / 2
    else
        TheDamage = 10
    end
		
		return TheDamage
end
```

**FGameMagnitudeContext**

| 字段               | 数据类型 | 说明                             |
|--------------------|----------|-------------------------------|
| SourceObject                 |             UObject             |伤害的源对象|
| Instigator          |               AController     |施加者的PlayerController|
| Causer         | AActor |施加者Actor，可能为角色或者枪|
| TargetActor         |     AActor               |被施加者Actor，作为伤害公式时可代表受击者|
| SrcMagnitude            |     float               |伤害的原数值|
| RestrictedDamageType   |        uint8              |伤害类型|
| DamageTypeTags           |  ULuaArrayHelper|伤害的额外Tags|
| AdditionalDamageData          |  FAdditionalDamageCalculationData|伤害的额外数据信息|
| ResultTags            |     ULuaArrayHelper               |伤害结果的额外数据信息，在造成伤害后有效|
| IsFatal         |  bool|伤害结果的额外数据信息，在造成伤害后有效|
| RecoverTags            |ULuaArrayHelper |伤害的额外Tags|

---

### 推导属性
  
对于某些属性，如果希望在获取属性值前执行特定逻辑的预处理或者基于其他属性推导计算而来，则需要使用到推导属性。

点击属性右侧的“推导”按钮，将跳转到对应属性蓝图的lua脚本中，生成一个以 `Get{属性名}_Override` 命名的函数，需要在该函数中实现推导逻辑，函数的返回值为推导后的属性值。

> 推导后的属性值对全局的取值场景均生效，包含脚本中调用API的获取和蓝图配置的引用，覆盖优先级最高

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GwdSsimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HdE22image.png)
   
代码示例：
  
```lua   
-- 获得的耐力值*3
function UGCAttributeGroup_Character:GetEndurance_Override(OriginalValue, AttributeOwnerActor)  
    return OriginalValue * 3  
end  

return UGCAttributeGroup_Character  
```  

---

### 动态设置属性

[``UGCAttributeSystem``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem) 提供了完善的操作属性的接口与委托，包括查询、修改以及监听属性数值变化的委托等，开发者可以在脚本中调用相关函数对属性值进行动态调整，使用属性前需要主动引用该脚本文件，并通过属性名映射表的key来访问对应属性。

> 目前 ```UGCAttributeSystem``` 库函数对挂载了属性修改组件的角色、枪械与怪物均适用

代码示例：

```lua   
UGCGameSystem.UGCRequire('Script.GameAttribute.game_attribute_type')

local Hp = UGCAttributeSystem.GetGameAttributeValue(CauserActor, UGCNativeGameAttributeType.Character_Health)
-- 获取血量后的其他逻辑处理 
```  

<br>

## 属性应用优先级

属性值的修改和传递在不同应用场景下有固定的优先级覆盖关系，开发者需要确保设置和覆盖时机符合优先级规则，避免出现最终输出值与预期不符的问题。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uiZSQimage.png)

**注意**
> 由于属性推导可基于其他属性推导计算，因此设计上需要避免出现属性依赖的嵌套而产生死循环



---


## 全局伤害公式

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 全局伤害公式

**涉及API:** `Add`, `Context`, `DamageContext`, `ExtraResult`, `GetCalculationResult`, `GetDamageTagsFromContext`, `GetDamageTypeFromContext`, `GetSourceMagnitudeFromContext`, `GetVictimFromContext`, `UGCAttributeSystem`, `UGCAttributeSystem.GetDamageTagsFromContext`, `UGCAttributeSystem.GetDamageTypeFromContext`, `UGCGameplayTagSystem`, `UGCGameplayTagSystem.RequestGameplayTag`, `UGCGenericMessageSystem`, `UGCGenericMessageSystem.ListenObjectMessage`, `UGCGenericMessageSystem.UnListenObjectMessage`, `UGCGlobalDamageCalculation`, `UnListenObjectMessage`

# 全局伤害公式

玩法中经常根据特定对象或者伤害源产生的角色/怪物伤害进行二次修改，例如放大对指定部位的伤害、增强特定玩家/物品造成的伤害等等，现有功能体系下实现 [伤害覆写](https://developer.gp.qq.com/api/#/searchContent/ASTExtraBaseCharacter?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E7%B1%BB%E4%BA%8B%E4%BB%B6%2F%E4%B8%BB%E8%A7%92%E7%B1%BB%EF%BC%88PlayerPawn%EF%BC%89%2FASTExtraBaseCharacter.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=ASTExtraBaseCharacter&autoJump=UGC_TakeDamageOverrideEvent) 的逻辑分散在各个类脚本中难以管理。

全局伤害公式提供了统一定制伤害计算逻辑的入口，以中心化的方式管理全局的伤害处理逻辑，支持接入 [属性系统](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20098) 的复杂伤害计算，且相比于伤害覆写，伤害公式的优先级更高，作为伤害结算的最终输出值。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sqjFsimage.png)

> 对于怪物伤害，伤害公式仅支持 [新怪物系统](https://developer.gp.qq.com/wikieditor/#/catalog/20144)

<br>

## 启用伤害公式

编辑器菜单栏中单击 ``属性管理器``，打开属性管理器面板后，选择 ``伤害公式`` 并点击【推导】按钮，将在工程目录 ``Blueprint/Attributes`` 下创建名为“UGCGlobalDamageCalculation”的蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0xmqbimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kXNvFimage.png)

同时，会在工程Script脚本目录的相同路径下生成全局伤害公式的类文件，核心的伤害处理逻辑在该类下实现。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LEQvkimage.png)

<br>

## 实现伤害计算

所有对角色触发的伤害都会进入 ``GetCalculationResult`` 回调函数中，该函数可实现伤害结算的覆写。

**回调参数**

|参数名|参数描述|数据类型|
|-|-|-|
|Context|伤害事件上下文数据|FGameMagnitudeContext|
|ExtraResult|伤害的额外信息，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 表示|FExtraDamageCalculationResult|

**返回值**

|数据类型|数据描述|
|-|-|
|number|覆写后的伤害，即最终的结算值|
|FExtraDamageCalculationResult|伤害的额外信息，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 表示|

### Context 

通过 [``UGCAttributeSystem``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem) 库提供的函数可以从 ``Context`` 中获取本次伤害的具体情境信息，例如 [``GetVictimFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetVictimFromContext) 获取受害者对象、[``GetSourceMagnitudeFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetSourceMagnitudeFromContext) 获取原始伤害值等，方便开发者基于特定的条件实现伤害逻辑。

此外部分系统功能支持触发伤害的行为配置，例如技能编辑器提供的 [技能Task-造成伤害](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3)，Buff编辑器提供的 [造成伤害](https://developer.gp.qq.com/wikieditor/#/catalog/20117?autoJump=%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3) 动作，UGCAttributeSystem库也提供了相应的获取方式 [``GetDamageTypeFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetDamageTypeFromContext) 和 [``GetDamageTagsFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetDamageTagsFromContext)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uXj7gimage.png)

代码示例：

```lua
local RestrictedDamageType = UGCAttributeSystem.GetDamageTypeFromContext(Context)
local DamageTypeTags = UGCAttributeSystem.GetDamageTagsFromContext(Context)
 
for _, Tag in pairs(DamageTypeTags) do
	if Tag then
		print("[UGCGlobalDamageCalculation] Context Tag: --->"..Tag)
	end
end
```

### ExtraResult

``ExtraResult`` 参数支持追加额外的伤害信息，并通过 ``GetCalculationResult`` 函数返回，当监听了伤害公式触发的相关事件时，能够通过事件回调的 ``DamageContext`` 参数获取到，方便更进一步的逻辑处理。

例如，监听了 [``UGCGenericMessageSystem.Messages.UGC.PlayerPawn.PostTakeDamage``](https://developer.gp.qq.com/api/#/searchContent/UGCGenericMessageSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGenericMessageSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGenericMessageSystem) 事件，触发伤害时判断当次伤害产生暴击，为 ``ExtraResult`` 添加暴击的Tag：

```lua
local CritTag = UGCGameplayTagSystem.RequestGameplayTag("UGC.Damage.Result.Critical")
if CritTag then
	ExtraResult.ResultTags:Add(CritTag)
end
```

在事件回调的函数中，通过 ``DamageContext.ResultTags`` 可以读取到暴击Tag。

<br>

## 过滤伤害修改范围

伤害公式默认会捕捉所有能触发伤害的场景，如果不希望和平原生的一些伤害加成/减伤机制受到影响，可以通过“内置通用伤害修改过滤选项”进行过滤，选中状态代表该类型的伤害不受伤害公式的影响，支持多选。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1TJY6image.png)

<br>

## 伤害事件

当角色受到伤害时，在回调伤害公式前后分别触发两个事件：[``UGCGenericMessageSystem.Messages.UGC.PlayerPawn.PreTakeDamage``](https://developer.gp.qq.com/api/#/searchContent/UGCGenericMessageSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGenericMessageSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGenericMessageSystem) 和 [``UGCGenericMessageSystem.Messages.UGC.PlayerPawn.PostTakeDamage``](https://developer.gp.qq.com/api/#/searchContent/UGCGenericMessageSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGenericMessageSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGenericMessageSystem)，开发者可以监听该事件实现自定义处理逻辑。

代码示例：

```lua
-- 定义回调函数
local Callback = function(PlayerPawn, DamageCauserActor, EventInstigator, Damage, DamageContext)
	if DamageContext then
		print("DamageContext exists")
		if DamageContext and DamageContext.ResultTags then
			print("ResultTags exists:" .. tostring(DamageContext.ResultTags))
    else
			print("ResultTags is nil")
		end
	end

	-- 反监听PostTakeDamage事件
	UGCGenericMessageSystem.UnListenObjectMessage(PlayerPawn, UGCGenericMessageSystem.Messages.UGC.PlayerPawn.PostTakeDamage)
end

-- 监听PostTakeDamage事件
UGCGenericMessageSystem.ListenObjectMessage(PlayerPawn, UGCGenericMessageSystem.Messages.UGC.PlayerPawn.PostTakeDamage, nil, Callback)
```

---


## 属性修改器

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 属性修改器

# 属性修改器

通常人物角色/怪物的属性在游戏对局过程中受装备、技能、环境等系统影响而发生动态变化，常规的属性修改方式基于各系统的基础运算操作独立修改属性值，由于修改/还原时机的因素难以管理，容易产生预期外的数据准确性问题。

属性修改器提供了一套属性计算流程和框架，通过统一的运算规则收敛各属性修改的执行过程，保证修改结果的准确与配置的灵活。

<br>

## 属性修改器概述

属性修改器引申了属性基础值、属性修改符及计算公式等概念，将属性修改的过程描述为：属性基础值在基于属性修改符的逻辑运算的计算下输出最终值，且根据修改类型的不同决定是否能被还原为原始基础值。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PwP9Cimage.png)

- 属性基础值：未受到任何属性修改效果影响下的原始值
- 属性修改类型：支持临时修改、永久修改与持续修改，对属性的临时修改或者持续修改都可以在效果结束后还原为原始基础值；而永久修改直接改变基础值，此后的修改及计算将基于新的基础值
- 属性修改符：参与计算的操作运算符，包含加法、乘法和值覆盖等，每一种运算符都会生成一个对应的修改器
- 属性计算公式：将属性基础值和所有的属性修改器代入指定的公式进行运算，得到最终的输出值

<br>

## 属性修改符

目前支持加法、乘法、值覆盖、独立乘法和独立加法五种运算符，不同运算符对修改类型的支持略有不同。

- 加法运算符（Plus）：对属性执行指定数值的加法运算，多个加法修改器将合并计算，支持临时修改与永久修改
- 乘法运算符（Multiply）：对属性执行指定数值的乘法运算，多个乘法修改器将合并计算，支持临时修改与永久修改
- 值覆盖（Set）：直接将属性赋值为指定数值，如果存在多个值覆盖修改器，则仅取时序上最后一个修改器生效，支持临时修改与永久修改
- 独立乘法运算符（Extra Multiply）：此类型乘法修改器不参与合并计算，而作为独立的乘法操作符，适用于输出值前的系数计算，仅支持临时修改
- 独立加法运算符（Extra Plus）：此类型加法修改器不参与合并计算，而作为独立的加法操作符，适用于输出值前的累加计算，仅支持临时修改

<br>

## 属性计算公式

**临时修改属性**

对属性临时修改的最终输出值基于以下公式进行计算，其中X代表属性基础值：

```lua
f(X) = 值覆盖修改器 ? 值覆盖修改器 : (X + 加法修改器1 + 加法修改器2...) * (乘法修改器1 + 乘法修改器2...) * 独立乘法修改器1 * 独立乘法修改器2... + 独立加法修改器1 + 独立加法修改器2...
```

由于计算公式有固定的四则运算优先级，最终的计算值不受属性还原时序的影响而产生错误的输出；且基础值未被修改，因此能够正确地被还原，保证计算结果的准确与稳定。

<br>

**永久修改属性**

对于永久修改，基于修改执行时序进行基础四则运算，例如：道具A和技能B均对血量属性有永久加成，其中道具A让血量提升50%，技能B让血量提升200点，当先拥有道具A后释放技能B时，``血量最终值 = 基础值 * 1.5 + 200``；但如果先释放技能B后获得道具A，则 ``血量最终值 = (基础值 + 200) * 1.5``。

<br>

**持续修改属性**

持续修改与临时修改类似，都是基于固定的四则运算，但差异点在于持续修改会以Tick的频率不断执行公式计算，且每次取修改器内各属性的最新值参与计算，例如：让伤害值持续提升20%，伤害基础值为100，第一次Tick的时候伤害值变为120，第二次Tick的时候以120作为基数计算伤害值为144，以此类推；但是不会变更基础值，当持续时间结束时，还原到100。


<br>

## 应用属性修改器

属性修改器的机制被应用在技能、Buff、装备等系统中，以蓝图的形式提供配置使用，例如Buff编辑器中的 [修改武器属性](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E6%AD%A6%E5%99%A8%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9) Action，底层即是通过属性计算公式将运算符生成的修改器代入运算。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZDPGEimage.png)

<br>

## 注意事项

- 涉及属性修改的功能设计需要前置规划好修改类型，过度泛用临时修改会带来较多的性能开销
- 值覆盖修改器不存在优先级的概念，当存在多个有效的值覆盖修改器时，只根据执行时序确定最后生效的值覆盖修改器，因此尽量在逻辑上保证同时只有一个值覆盖修改器会生效，或者尽量不使用临时修改类型的值覆盖修改器







---


## 枪械属性对照表

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 枪械属性对照表

**涉及API:** `UGC全自动射击间隔`, `UGC切枪时间影响因子`, `UGC后坐力影响因子`, `UGC后坐力影响因子RecoilFactorWrapper`, `UGC子弹基础伤害`, `UGC弹匣容量`, `UGC换弹时间影响因子`, `UGC连发子弹间隔`, `UGC连发射击间隔`, `UGC连发数量`

# 枪械属性对照表

| 属性名 | 属性含义 | 取值 | 示例取值 |效果|
| :------: | ------ | ------ | ------ |------ |
| `射击前处理时长-PreFireTime` | **狙击枪**拉栓后到射击的停留时间 | (0,+∞) | x5 |![PreFireTime.2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qu13mPreFireTime.2.gif)|
|`射击后处理时长-PostFireTime`| **狙击枪**射击后到拉栓的停留时间 | (0,+∞) | x5 | ![PreFireTime.2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oxgPGPreFireTime.2.gif)|
|`单发换弹拉栓时长-ReloadDurationStart`| **狙击枪**换弹时，拉栓的动画时长 | (0,+∞) | =5 | ![Start.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wepoOStart.gif)|
|`单发换弹填弹时长-ReloadDurationLoop`| **狙击枪**换弹时，填充一发子弹的时长 （第二颗子弹开始计算）| (0,+∞) | =5 |![Loop.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dNyZNLoop.gif)|
| `全弹夹换弹时长` | **所有枪械**子弹打完后的换弹时长 | （0,+∞） | =1 | ![全弹匣换弹时长.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/E6DNn%E5%85%A8%E5%BC%B9%E5%8C%A3%E6%8D%A2%E5%BC%B9%E6%97%B6%E9%95%BF.gif)|
| `全弹夹换弹时间修改参数` | **所有枪械**子弹打完后的换弹时长修改参数 | （0,+∞） | x5 | ![全换弹时长修改因素.2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iHJ6y%E5%85%A8%E6%8D%A2%E5%BC%B9%E6%97%B6%E9%95%BF%E4%BF%AE%E6%94%B9%E5%9B%A0%E7%B4%A0.2.gif)|
| `战术换弹时长` |**非狙击枪**子弹未打完后的换弹时长 | （0,+∞） | =5 | ![战术换弹时长.2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Rho3i%E6%88%98%E6%9C%AF%E6%8D%A2%E5%BC%B9%E6%97%B6%E9%95%BF.2.gif)|
| `战术换弹时间修改参数` |**非狙击枪**子弹未打完后的换弹时长修改参数 | （0,+∞） | =5 | ![战术换弹时长修改因素.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dNAtQ%E6%88%98%E6%9C%AF%E6%8D%A2%E5%BC%B9%E6%97%B6%E9%95%BF%E4%BF%AE%E6%94%B9%E5%9B%A0%E7%B4%A0.gif)|
| `单发战术换弹时间修改参数-ReloadTimeTacticalOneByOneModifier` | **狙击枪**子弹未打完后的换弹时长修改参数 | (0,+∞) | x5 | ![单发战术弹时长修改因素.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZfPMA%E5%8D%95%E5%8F%91%E6%88%98%E6%9C%AF%E5%BC%B9%E6%97%B6%E9%95%BF%E4%BF%AE%E6%94%B9%E5%9B%A0%E7%B4%A0.gif)|
| `所有换弹时间修改参数-AllReloadTimeModifier` | **所有枪械**战术/全弹夹换弹时间的修改参数 | （0,+∞） | =0.01 | ![AllReloadTime.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LpGqxAllReloadTime.gif)|
| `垂直后坐力修改系数` | 开枪时枪口抬高幅度的大小，取值越大，幅度越大 | (0,+∞) | x100 | ![垂直后坐力.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VSDZY%E5%9E%82%E7%9B%B4%E5%90%8E%E5%9D%90%E5%8A%9B.gif) |
| `水平后坐力修改系数` | 开枪时枪口左右抖动的大小，取值越大，幅度越大 | (0,+∞) | x100 | ![水平后坐力.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/m6EXu%E6%B0%B4%E5%B9%B3%E5%90%8E%E5%9D%90%E5%8A%9B.gif)|
| `霰弹枪垂直散布-ShotGunVerticalSpread` | 霰弹枪垂直方向的散布修改因子；取值越大，散布范围越大 | (0, 8) | / | - |
| `霰弹枪水平散布-ShotGunHorizontalSpread` | 霰弹枪水平方向的散布修改因子；取值越大，散布范围越大 | (0, 8) | / | - |
| `最终散布修改参数-DeviationFactorModifier` | 霰弹枪散布修改因子；取值越大，散布范围越大 | (0, 8) | =8 | ![最终散布.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pUguJ%E6%9C%80%E7%BB%88%E6%95%A3%E5%B8%83.gif) |
| `开镜速度` | 值越大，开镜速度越快 | （0, +∞） | x10 | ![开镜速度.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cW1bF%E5%BC%80%E9%95%9C%E9%80%9F%E5%BA%A6.gif)|
| ``倍镜类别`` | 倍镜的枚举值<br>- 0：全息/红点<br>- 1：2倍镜<br>- 2：4倍镜<br>- 3：8倍镜<br>- 4：默认无倍镜<br>- 5：3倍镜<br>- 6：6倍镜  | (0, 6) | / | - | 
| `开火动画抖动幅度` | 值越大，开火镜头抖动幅度越大 | (0, +∞) | x100  | ![开火抖动幅度.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IbAgr%E5%BC%80%E7%81%AB%E6%8A%96%E5%8A%A8%E5%B9%85%E5%BA%A6.gif)|
| `UGC换弹时间影响因子-ReloadTimeFactorWrapper` | 所有枪械换单时间影响因子（战术+全换弹）| (0. +∞) | =0.2 | ![UGC换弹时间.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eWf5yUGC%E6%8D%A2%E5%BC%B9%E6%97%B6%E9%97%B4.gif)|
| `UGC切枪时间影响因子-SwitchTimeFactorWrapper` | 切枪时间影响因子 | (0, +∞) | =3 | ![UGC切枪时间.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/W8g0YUGC%E5%88%87%E6%9E%AA%E6%97%B6%E9%97%B4.gif)|
| `UGC攻击间隔影响因子-ShootIntervalFactorWrapper` | 射击间隔时间的修改参数 |  (0, +∞) | =5 | ![UGC攻击间隔.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6g1O1UGC%E6%94%BB%E5%87%BB%E9%97%B4%E9%9A%94.gif)|
| `UGC后坐力影响因子RecoilFactorWrapper` | 后坐力整体影响因子 | (0, +∞) | =50 | ![UGC后坐力.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QohtBUGC%E5%90%8E%E5%9D%90%E5%8A%9B.gif)|
| `UGC散布影响因子-DeviationFactorWrapper` | 霰弹枪整体散布影响因子（垂直+水平） | （0,+∞） | 5 | ![UGC散布.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Ew2mxUGC%E6%95%A3%E5%B8%83.gif) |
| `UGC一次拉栓子弹装填数量-MaxBulletNumInBarrelWrapper` | 狙击枪 | / | / | - |
| `UGC弹匣容量-MaxBulletNumlnOneClipWrapper` | 所有枪械的弹匣容量修改 | (0, +∞) | =50 | ![UGC弹匣容量.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yHx94UGC%E5%BC%B9%E5%8C%A3%E5%AE%B9%E9%87%8F.gif) |
| `枪械所有射速修改系数` | 枪械当前伤害修改的系数 | (0,+∞) | / |  - |
|  `全弹夹换弹开始到拔出弹匣时间` | 全换弹前半段 | （0,+∞） | / | - |
|  `全弹夹换弹时插入到换弹结束时间` | 全换弹后半段 | （0,+∞） | / | - |
| `战术换弹开始到拔出弹匣时间` | 战术换弹前半段 | （0,+∞） | / | - |
| `战术换弹时插入到换弹结束时间` | 战术换弹后半段 | （0,+∞） | / | - |
| `UGC换弹时间影响因子` | 全换弹、战术换弹的统一影响因子（越大换弹速度越慢） | （0,+∞） | 0.1 | ![UGC换弹时间因子.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l2RpLUGC%E6%8D%A2%E5%BC%B9%E6%97%B6%E9%97%B4%E5%9B%A0%E5%AD%90.gif)|
| `UGC切枪时间影响因子` | 武器一、武器二切换时，当前枪械的切枪时间影响（越大切枪速度越慢） | （0,+∞） | 0.1 | ![UGC切枪时间因子.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XfoB6UGC%E5%88%87%E6%9E%AA%E6%97%B6%E9%97%B4%E5%9B%A0%E5%AD%90.gif) |
| `UGC后坐力影响因子` | 影响后坐力（越大，后坐力越强） | （0,+∞） | 100 | ![UGC后坐力因子.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FofpnUGC%E5%90%8E%E5%9D%90%E5%8A%9B%E5%9B%A0%E5%AD%90.gif) |
| `UGC全自动射击间隔` | 自动模式射击时间间隔（越大，射击间隔越长） | （0,+∞） | / | ![UGC全自动射击间隔.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KBODGUGC%E5%85%A8%E8%87%AA%E5%8A%A8%E5%B0%84%E5%87%BB%E9%97%B4%E9%9A%94.gif)|
| `UGC子弹基础伤害` | 子弹命中时的基础伤害值 | （0,+∞） | 100 | ![UGC基础伤害.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0vtkaUGC%E5%9F%BA%E7%A1%80%E4%BC%A4%E5%AE%B3.gif)|
| `UGC连发数量` | 连发模式下，一次爆发子弹的数量 | （0,+∞） | 10 | ![UGC连发数量.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5R2PjUGC%E8%BF%9E%E5%8F%91%E6%95%B0%E9%87%8F.gif)|
| `UGC连发子弹间隔` | 连发模式下，爆发多颗子弹每一颗之间的间隔 | （0,+∞） | 0.5 | ![UGC连发子弹间隔.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lbJwCUGC%E8%BF%9E%E5%8F%91%E5%AD%90%E5%BC%B9%E9%97%B4%E9%9A%94.gif)|
| `UGC连发射击间隔` | 连发模式下，爆发子弹的间隔 | （0,+∞） | 1 | ![UGC连发射击间隔 .gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WGOvmUGC%E8%BF%9E%E5%8F%91%E5%B0%84%E5%87%BB%E9%97%B4%E9%9A%94%20.gif) |
| `UGC弹匣容量` | 枪械本身的容量 | （0,+∞） | 50 | ![UGC枪械弹匣.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pTcdHUGC%E6%9E%AA%E6%A2%B0%E5%BC%B9%E5%8C%A3.gif) |

---


## 受击数据资产

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 受击数据资产

# 受击数据资产

受击是游戏中角色或物体受到攻击时产生的反馈，通常通过特效、音效、镜头抖动等多种效果组合的形式描述受击的程度，能够产生伤害的场景一般都伴随受击表现，因此通过数据资产蓝图的方式提供统一的受击表现数据配置，便于管理与复用。

<br>

## 创建数据资产蓝图

在编辑器内容浏览器窗口下，右键 ``各种各样 -> 数据资源``， 搜索“On Hurt Effects Data Asset”，基于该结构体创建数据资产蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XCEypimage.png)

<br>

## 配置受击数据

双击打开受击数据资产蓝图，进入编辑界面：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/f4Emnimage.png)

|属性名|属性说明|
|-|-|
|Particle System|受击时触发的粒子特效资源|
|Scale|受击粒子特效的缩放大小|
|Ak Event|命中非头部部位播放的音效|
|Head Shot Ak Event|命中头部播放的音效|
|Shake Class|播放的相机抖动蓝图资源|
|Scale|抖动强度|
|Horizontal Speed|击退的水平方向上的速度|
|Vertical Speed|击退的垂直方向上的速度|
|Horizontal Friction|击退的水平方向上的摩擦力|
|Duration|击退的持续时间|
|Priority|击退的执行优先级，当多个击退效果作用于同一个目标时，将根据该优先级决定最终生效的击退效果|

设置完成后，点击【保存】按钮完成配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hNT9zimage.png)

<br>

## 应用受击数据

所有支持配置受击数据资产蓝图的功能都可以应用受击数据，例如 [技能Task-近战攻击](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E8%BF%91%E6%88%98%E6%94%BB%E5%87%BB) 提供了受击效果的配置项，关联后即会读取受击数据进行对应的效果表现。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JZtNzimage.png)

---


## 角色属性与状态

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 角色属性与状态

**涉及API:** `AdditiveSpeedValueWrapper`

# 角色属性与状态

## 角色固化属性

[属性管理器](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E5%B1%9E%E6%80%A7%E7%AE%A1%E7%90%86%E5%99%A8) 中内置了部分角色的常用属性作为固化属性，开发者可以直接应用这类属性在玩法逻辑中，无需重复定义。

|属性名|属性含义|取值范围|
|-|-|-|
|Health|角色的当前血量|[0, +∞)|
|HealthMax|角色的最大血量|[0, +∞)|
|SkillCDRecoverRate|技能CD的恢复速率|[0, 3]|
|SignalHP|角色当前的信号量|[0, +∞)|
|SignalHPMax|角色的最大信号量|[0, +∞)|
|voiceCheckDis|角色检测周围声音的最大距离，影响 [小地图可视化音效](https://developer.gp.qq.com/wikieditor/#/catalog/20202) 的图标显示效果|[0, +∞)|
|Breath|角色的当前呼吸值|[0, +∞)|
|AdditiveSpeedValueWrapper|角色移动时额外叠加的移速倍率，影响走路、冲刺、游泳等所有移动行为<br>``角色最终移动速度 = 基础移动速度 * (UGC移速倍率 + 额外移速倍率)``|[0, +∞)|
|EnergyCurrent|角色的当前能量值|[0, +∞)|
|UGCGeneralMoveSpeedScale|UGC移速倍率，与 ``AdditiveSpeedValueWrapper`` 共同影响角色的移动速度|[0, +∞)|
|RescueOtherDurationRate|角色救援队友时，救援所需时间的倍率|[0, +∞)|
|JumpCountLimit|角色连续跳跃的次数上限|[0, +∞)|
|JumpZSpeed|角色进行跳跃时的初速度|[0, +∞)|
|FallingDamageRatio|角色受到跌落伤害的倍率系数|[0, +∞)|
|HitBackIntensity|角色对敌方造成的击退效果强度，值越大，击退效果越强|[0, 100000000]|
|HitBackResist|角色受到击退效果时的击退抗性，值越大，击退效果越弱，1代表无击退效果|[0, 1]|

<br>

## 角色状态标签

编辑器为角色预设了一批基于 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 的状态标签，用以表示角色当前身处的行为状态，按触发类型可分为被动状态标签与主动状态标签，其中主动状态标签带有功能逻辑，当为角色赋予该类标签时即会按照标签的含义生效其对应的功能；而被动状态标签仅为角色进入对应的行为模式或者状态后被赋予的标签。

| 状态名                           | 含义       |   标签类型  |
|-------------------------------------|--------------|----|
| PawnState.Action.HoldGrenade       | 持有手雷     |  被动状态标签 |
| PawnState.Action.HoldWeapon        | 持有武器     |  被动状态标签 |
| PawnState.Action.Jump              | 跳跃         |  被动状态标签 |
| PawnState.Action.MeleeAttack       | 近战攻击     |  被动状态标签 |
| PawnState.Action.Pick              | 拾取         |  被动状态标签 |
| PawnState.Action.Sprint            | 冲刺         |  被动状态标签 |
| PawnState.Action.SwitchWeapon      | 切换武器     |  被动状态标签 |
| PawnState.Action.UseConsumeables   | 使用消耗品   |  被动状态标签 |
| PawnState.Action.Vault             | 攀爬         |  被动状态标签 |
| PawnState.ActivatingSkill          | 技能激活     |  被动状态标签 |
| PawnState.Dead                     | 死亡         |  被动状态标签 |
| PawnState.Dying                    | 濒死         |  被动状态标签 |
| PawnState.Gun.GunADS               | 瞄准         |  被动状态标签 |
| PawnState.Gun.GunFire              | 开火         |  被动状态标签 |
| PawnState.Gun.GunRelod             | 换弹         |  被动状态标签 |
| PawnState.Movement.Flying          | 飞行         |  被动状态标签 |
| PawnState.Movement.Swimming        | 游泳         |  被动状态标签 |
| PawnState.Movement.Walking         | 行走         |  被动状态标签 |
| PawnState.Pose.Crouch              | 蹲          |  被动状态标签 |
| PawnState.Pose.Prone               | 趴          |  被动状态标签 |
| PawnState.Pose.Stand               | 站          |  被动状态标签 |
| PawnState.SwitchPP                 | 人称视角切换中     |  被动状态标签 |
| PawnState.Vehicle.DriveVehicle     | 驾驶载具         |  被动状态标签 |
| PawnState.Vehicle.InVehicle        | 乘坐载具         |  被动状态标签 |
| PawnState.Vehicle.LeanOutVehicle   | 载具探身         |  被动状态标签 |
| PawnState.Buff.Invincible   | 无敌（处于该状态下，无法被造成伤害、无法被击退）         |  被动状态标签 |
| PawnState.Buff.UnDetectable   | 不可追踪（角色获得该状态时，无法被抛体追踪）         |  主动状态标签 |
| PawnState.Buff.UnPerceptionable   | 不可感知（角色获得该状态时，无法被怪物感知到）        |  主动状态标签 |
| PawnState.Debuff.DisableHealing   | 禁疗（角色获得该状态时，无法被治疗）         |  主动状态标签 |
| PawnState.Debuff.Dizzy   | 眩晕（角色获得该状态时，无法移动、释放技能、使用武器）       |  主动状态标签 |


---


## 全局治疗公式

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 全局治疗公式

**涉及API:** `Add`, `Context`, `ExtraResult`, `GetCalculationResult`, `GetDamageTagsFromContext`, `GetSourceMagnitudeFromContext`, `GetVictimFromContext`, `RecoverGenericCharacterHealth`, `UGCAttributeSystem`, `UGCAttributeSystem.GetDamageTagsFromContext`, `UGCGameplayTagSystem`, `UGCGameplayTagSystem.RequestGameplayTag`, `UGCGlobalRecoveryCalculation`

# 全局治疗公式

类似于 [全局伤害公式](https://developer.gp.qq.com/wikieditor/#/catalog/20099) 的作用，属性管理器提供了统一定制治疗计算逻辑的入口，以中心化的方式管理全局的治疗处理逻辑，决定所有调用 [``RecoverGenericCharacterHealth``]() 的最终治疗值结果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gMdl4image.png)

> 对于怪物治疗，仅 [新怪物系统](https://developer.gp.qq.com/wikieditor/#/catalog/20144) 支持治疗公式

<br>

## 启用治疗公式

编辑器菜单栏中单击 ``属性管理器``，打开属性管理器面板后，选择 ``治疗公式`` 并点击【推导】按钮，将在工程目录 ``Blueprint/Attributes`` 下创建名为“UGCGlobalRecoveryCalculation”的蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/F2Biiimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BygBuimage.png)

同时，会在工程Script脚本目录的相同路径下生成全局治疗公式的类文件，核心的治疗处理逻辑在该类下实现。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AfaEvimage.png)

<br>

## 实现治疗计算

经由 [``RecoverGenericCharacterHealth``]() 对角色触发的治疗都会进入 ``GetCalculationResult`` 回调函数中，该函数可实现治疗结算的覆写。

**回调参数**

|参数名|参数描述|数据类型|
|-|-|-|
|Context|治疗事件上下文数据|FGameMagnitudeContext|
|ExtraResult|治疗的额外信息，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 表示|FExtraDamageCalculationResult|

**返回值**

|数据类型|数据描述|
|-|-|
|number|覆写后的最终治疗值|
|FExtraDamageCalculationResult|治疗附带的额外信息，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 表示|

### Context 

通过 [``UGCAttributeSystem``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem) 库提供的函数可以从 ``Context`` 中获取本次治疗的具体情境信息，例如 [``GetVictimFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetVictimFromContext) 获取治疗对象、[``GetSourceMagnitudeFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetSourceMagnitudeFromContext) 获取原始治疗值等，方便开发者基于特定的条件实现治疗逻辑。

此外部分系统功能支持触发治疗的行为配置，例如技能编辑器提供的 [技能Task-治疗](https://developer.gp.qq.com/wikieditor/#/catalog/20186?autoJump=%E6%8A%80%E8%83%BDTask-%E6%B2%BB%E7%96%97)，Buff编辑器提供的 [治疗恢复](https://developer.gp.qq.com/wikieditor/#/catalog/20123?autoJump=%E6%B2%BB%E7%96%97%E6%81%A2%E5%A4%8D) 动作，UGCAttributeSystem库也提供了相应的获取方式 [``GetDamageTagsFromContext``](https://developer.gp.qq.com/api/#/searchContent/UGCAttributeSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E8%A7%92%E8%89%B2%E7%B3%BB%E7%BB%9F%2FUGCAttributeSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCAttributeSystem&autoJump=GetDamageTagsFromContext)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/b1qjgimage.png)

代码示例：

```lua
local RecoverTypeTags = UGCAttributeSystem.GetDamageTagsFromContext(Context)
 
for _, Tag in pairs(RecoverTypeTags) do
	if Tag then
		print("[UGCGlobalRecoveryCalculation] Context Tag: --->"..Tag)
	end
end
```

### ExtraResult

``ExtraResult`` 参数支持追加额外的治疗信息，并通过 ``GetCalculationResult`` 函数返回，方便自定义特殊的治疗标记。

```lua
local CritTag = UGCGameplayTagSystem.RequestGameplayTag("UGC.Damage.Result.Critical")
if CritTag then
	ExtraResult.ResultTags:Add(CritTag)
end
```

---


## 载具属性对照表

> 文档路径: 进阶内容 > GamePlay系统 > 属性与伤害 > 载具属性对照表

# 载具属性对照表

|属性名|属性含义|取值范围|
|-|-|-|
|CurrentHP|载具当前的生命值|[-100000000, 100000000]|
|MaxHP|载具的最大生命值|[0, 100000000]|
|CurrentFuel|载具当前的油量|[-100000000, 100000000]|
|MaxFuel|载具的最大油量|[0, 100000000]|
|FuelConsumeFactor|载具移动时消耗的油量系数，数值越大，油耗越大|[0, 100000000]|
|ImpactAbsorption|载具受到撞击后，对载具自身造成伤害的衰减程度|[0, 100000000]|
|ImpactAbsorptionPassenger|载具受到撞击后，对乘客造成伤害的衰减程度|[0, 100000000]|
|HitDamagePassengerMaxHP|载具受到撞击后，最多可对乘客造成的伤害上限|[0, 100000000]|
|ExplosionBaseDamage|载具血量归0后产生爆炸，所造成的基础伤害值|[0, 100000000]|
|ExplosionMinimumDamage|载具血量归0后产生爆炸，所造成的最小伤害值，爆炸伤害概念可参见载具 [伤害配置](https://developer.gp.qq.com/wikieditor/#/catalog/20245?autoJump=%E4%BC%A4%E5%AE%B3%E9%85%8D%E7%BD%AE)|[0, 100000000]|
|FuelConsumptionModifierBoost|加速时额外增加的油耗系数，数值越大，加速时的油耗越大|[0, 100000000]|
|BoostModifier|加速动力系数，数值越大，加速时的动力越强|[0, 100000000]|
|LinearDamping|载具移动时的速度衰减系数，影响载具的滑停时间，值越大载具越“沉”，松油门后滑停的距离越短；如果值为0，则只依赖地面的摩擦力减速|[0, 100000000]|
|AngularDamping|载具移动转弯时的角速度衰减系数，影响“甩尾回正速度”与“空中翻转难度”，防止载具侧翻持续打转，值越大载具飘移回正速度越快|[0, 100000000]|
|MaxAcceleration|载具每秒加速度的上限，影响载具速度变化的快慢程度，仅针对水上载具生效|[0, 100000000]|
|StartAccelerationRate|载具每秒加速度的增加速率，影响载具加速度变化的快慢程度，仅针对水上载具生效|[0, 100000000]|
|BackwardForceScale|载具倒车时加速度的比例系数，``倒车加速度 = 前进加速度 * BackwardForceScale``，仅针对水上载具生效|[-100000000, 100000000]|
|MaxRotationYawAngle|载具转向时的角度上限，影响轮胎的转弯半径，仅针对水上载具生效|[0, 100000000]|
|MaxVelocity|载具速度上限，仅针对水上载具生效|[-100000000, 100000000]|
|HitDamageBase|载具对角色撞击造成的伤害值|[0, 100000000]|

---
