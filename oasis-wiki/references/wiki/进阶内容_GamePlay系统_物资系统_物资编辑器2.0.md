# 进阶内容/GamePlay系统/物资系统/物资编辑器2.0

> 本分类共 8 篇文章

---


## 物品编辑器

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 物品编辑器

**涉及API:** `AddBuffByClass`, `AddItem`, `AddItemByDefineIDV2`, `AddItemV2`, `Asset`, `BP_UGC_MachineGun_P90`, `BP_UGC_MeleeWeap_Machete`, `CanUseItemV2`, `EquipItemV2`, `GetOwner`, `ItemCanEquipToSlot`, `OnMergeItemV2`, `OnUseItemV2`, `OnUseV2`, `SuperClass.OnUseV2`, `UGCConfig`, `UGCGameSystem`, `UGCGameSystem.GetPlayerPawnByPlayerController`, `UGCItemSystemV2`, `UGCItemSystemV2.GetOwnBackpackComponent`

# 物品编辑器

物品编辑器将和平精英的常用物资模板化，对各类物资的原始属性进行了精简与提炼，开发者可基于模板创建并调整物品的基础属性，同时也支持了对特定物品的扩展能力，例如自定义个性化枪械，为枪械赋予词条属性等等，结合 [背包系统](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104) 能够为玩法创作带来更强大的功能支持。

<br>

## 物品概述

游戏中的物品是指一类玩家可交互的对象，根据存在形态的不同分为 [虚拟物品](https://developer.gp.qq.com/wikieditor/#/catalog/20139) 和实体物品，物品编辑器中的物品特指实体物品，且具有以下特征：
- 在世界场景中能够具象化展示物品的形态，即物品可被看见
- 玩家可以直接与物品进行交互，例如使用或者装配物品
- 通过背包/仓库内是否存在物品来表达玩家是否拥有该物品

物品编辑器支持武器、消耗品、装备三种类型的物品，包含各种枪械、近战武器、投掷物、药品、护甲等物资。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MeSxXimage.png)

<br>

## 编辑器界面

点击绿洲启元编辑器菜单栏的【物品编辑器】按钮，将打开物品编辑器的操作界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mtyv5image.png)

物品编辑器主界面分为5个区域：模板页签、工程物品资源、物品模板、物品预览窗口及物品属性面板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5X4afimage.png)

**A. 模板页签**

目前提供了物品、枪械、近战武器和投掷物四类模板：
- 物品模板用于创建所有已支持类型的物品，该物品能够发放至背包内使用，但无法直接放置在场景中被拾取
- 枪械模板用于创建枪械实体蓝图，该实体无法进入背包装配使用，但可以关联至通过物品模板创建的枪械物品上，实现枪械的 [自定义改装](https://developer.gp.qq.com/wikieditor/#/catalog/20103)
- 近战武器模板用于创建近战武器的实体蓝图，该实体无法进入背包装配使用，但可以关联至通过物品模板创建的近战武器物品上，实现近战武器的 [自定义设置](https://developer.gp.qq.com/wikieditor/#/catalog/20158)
- 投掷物模板用于创建投掷物的实体蓝图，该实体无法进入背包使用，但可以关联至通过物品模板创建的投掷物物品上，实现投掷物的 [自定义设置](https://developer.gp.qq.com/wikieditor/#/catalog/20157)

**B. 工程物品资源**

工程内通过物品编辑器创建的所有物品蓝图将显示在该资源列表中，对蓝图右键的菜单支持删除、克隆、重命名、创建子蓝图和复制引用路径等操作

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Amvawimage.png)

**C. 物品模板**

预置的物品/枪械/近战武器/投掷物模板，基于模板创建对应类型的物品或实体蓝图

**D. 物品预览窗口**

在【物品】页签的物品模板中，展示所创建物品在拾取物状态的模型和角色手持装备的效果，目前支持枪械、近战武器和投掷物类型物品的手持/装备预览

**E. 物品属性面板**

物品的可配置属性，包含物品的通用属性、背包配置属性或者物品的特性配置

<br>

## 物品模板

物品编辑器预置了多种物品模板：枪械物品、配件物品、子弹物品、装备物品、投掷物品、药品、防具、近战武器和空白物品。

**枪械物品模板**

和平精英常用的各类型枪械均已模板化，包含突击步枪、射手步枪、狙击枪、冲锋枪、手枪、霰弹枪、机枪和特殊武器。
> 空白枪械物品模板用于创建空参数的枪械物品，方便开发者结合 [自定义枪械](https://developer.gp.qq.com/wikieditor/#/catalog/20103) 的功能从0到1配置一把全新枪械

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RACUHimage.png)

**配件物品模板**

提供和平精英枪械配套的配件物品模板，包含弹匣、握把、枪口、枪托和瞄准镜。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wlKyPimage.png)

**子弹物品模板**

提供和平精英各类枪械适配的子弹物品模板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mL5Viimage.png)

**装备物品模板**

配合背包系统 [装备栏](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A3%85%E5%A4%87%E6%A0%8F) 提供的装备物品模板，开发者可以创建类似RPG游戏中的自定义装备，目前暂不包含和平精英的头盔/护甲/背包模板。
> 空白装备物品模板用于创建空参数的装备物品，方便开发者从0到1配置一个全新的装备

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WS95jimage.png)

**投掷物品**

和平精英常用的投掷物均已模板化，支持两种类型：传统的和平投掷物（震爆弹、烟雾弹、燃烧瓶及破片手雷）、基于 [技能抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20075) 实现的投掷物（功能效果与和平投掷物一致）
> 空白投掷物模板用于创建空参数的投掷物物品，方便开发者结合 [自定义投掷物](https://developer.gp.qq.com/wikieditor/#/catalog/20157) 的功能从0到1配置一个投掷物

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Lw6Mnimage.png)

**药品模板**

提供能量饮料、急救包、肾上腺素等常用药品物资模板。
> 空白药品模板用于创建空参数的药品物品，方便开发者从0到1配置一个全新的药品

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gYU2Himage.png)

**防具模板**

提供和平精英经典的一/二/三级头盔、防弹衣和背包物品模板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/k9ZkNimage.png)

**近战武器模板**

提供和平精英常规的平底锅、大砍刀、镰刀和撬棍等近战武器物品模板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UCdm7image.png)

**空白物品模板**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zesYLimage.png)

- 空白物品：默认不具备特性属性和功能，可用于创建玩法中类似货币、兑换物等虚拟物品，也能够结合 [背包系统API](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2) 实现具有特定功能的物品
- 空白消耗品：默认不具备特性属性和功能，支持使用时添加和触发相应的技能，需自行 [动态添加技能](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E5%8A%A8%E6%80%81%E6%B7%BB%E5%8A%A0%E6%8A%80%E8%83%BD) 逻辑实现

<br>

## 物品创建流程

所有类型的物品均可通过新建物品蓝图并配置相应的物品属性来实现物品的创建。

### 新建物品蓝图

物品编辑器统一了各类物品的创建方式，以创建能量饮料为例：

1. 从“物品模板”窗口中选择能量饮料物品模板，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``能量饮料`` 为模板创建”
2. 点击“以 ``能量饮料`` 为模板创建” 按钮，弹出输入名称弹窗，输入物品蓝图名称并点击确定
3. 新建的能量饮料物品蓝图将显示在“工程物品资源”窗口中，且物品蓝图创建于 ``Asset/Blueprint/Prefabs/Items`` 路径下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mX7fUimage.png)

---

### 基础属性配置

基础配置为各种类型物品高度抽象后的通用属性，包括物品ID、物品名称、拾取物模型等等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3OQL0image.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kRUFmimage.png)

|属性名|属性说明|
|-|-|
|物品ID|创建物品时自动生成的唯一ID，不可修改|
|物品名称|可拾取物和背包内该物品显示的名称|
|最大堆叠数量|一个背包格子最大可容纳的物品数量|
|物品图标|可拾取物和背包内该物品显示的图片样式|
|物品描述|背包内该物品的描述说明|
|拾取描述|可拾取物的简要描述|
|自定义类型|物品如果希望能添加到角色的 [装备栏](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A3%85%E5%A4%87%E6%A0%8F) 或者其他装备物品的槽位中, 需要确保 ``自定义类型`` 属性与对应装备槽位允许装备的物品类型保持一致|
|拾取物模型|可拾取物在场景中的显示模型|
|拾取物模型偏移|可拾取物模型的偏移、旋转和缩放|

---

### 经典背包属性配置

通常物品编辑器需要配合新的 [背包系统](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104) 使用，但物品编辑器也兼容了经典的和平背包系统，物品在经典背包内也可以正常使用，目前对经典背包的物品属性配置仅有“物品重量”。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eSXiAimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Z2Uakimage.png)

---

### V2背包属性配置

该部分属性均为针对启动了 [新背包系统](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104) 的配置项。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7HX2Jimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4UIHCimage.png)

|属性名|属性说明|
|-|-|
|是否可使用|物品是否可以从背包内被使用，对消耗品或者空模板创建的物品有效|
|是否可丢弃|物品是否可以被丢出背包，丢弃后的物品将掉落地面|
|是否可销毁|物品是否可以从背包内被销毁，销毁后的物品将直接消失|
|物品标记(Tag)|通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20102) 创建的物品标记|
|物品品质|设定物品的品质，有效值0~6，根据品质不同，该物品会显示不同的底色效果<br>【背包格子品质色样式】<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lDpw7image.png)<br>【[武器槽位](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E6%AD%A6%E5%99%A8%E6%A7%BD%E4%BD%8D) 品质色样式】<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uzSg4image.png)|
|是否持久化|物品是否能带出局外，勾选后该物品可以跨对局存储|
|自动尝试装备|影响配件物品的自动装备或是直接进入背包|
|死亡物品掉落配置|- 留在背包：角色死亡时物品数据保留，不会掉落出去，复活后还原同等数量的物品<br>- 掉落：基于角色 [死亡掉落类型](https://developer.gp.qq.com/wikieditor/#/catalog/20148?autoJump=%E8%AE%BE%E7%BD%AE%E6%AD%BB%E4%BA%A1%E6%8E%89%E8%90%BD%E7%B1%BB%E5%9E%8B) 的设置决定该物品的掉落形式<br>- 直接删除：物品直接被销毁|

部分类型的物品提供了额外的槽位配置项，允许为该物品定义可装配的 [配件槽位](https://developer.gp.qq.com/wikieditor/#/catalog/20210)。

---

### 类型特性配置

不同类型的物品因用途和交互不同，存在部分差异化属性，例如枪械具备射击特性的属性，药品具备使用特性的属性等。

#### 枪械物品特性

【枪械实体蓝图】

枪械物品需要关联枪械实体才能拥有对应的枪械特性，不同的枪械引用的实体蓝图不同，例如P90默认的实体蓝图为 ``BP_UGC_MachineGun_P90``；如果 [自定义枪械](https://developer.gp.qq.com/wikieditor/#/catalog/20103) 则需要修改此处的蓝图引用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/y4CQNimage.png)

【基础配置】

相比于其他类型的物品，枪械物品额外有 ``武器剪影图标`` 和 ``装备栏图标`` 两个配置项。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yTMNCimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ydiQ0image.png)

【属性覆盖】

各类枪械的性能参数默认与和平精英保持一致，提供了部分常用属性供开发者自定义修改，勾选 ``是否启用属性覆盖`` 即可修改各参数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/90PrMimage.png)

|属性名|属性说明|
|-|-|
|攻击间隔影响因子|枪械射击间隔的时间倍率|
|后坐力影响因子|后坐力程度倍率|
|散布影响因子|子弹偏离准心的程度，针对多发子弹类型的枪械，例如霰弹枪|
|射击间隔|单发子弹的射击间隔，对单发类型枪械有效|
|连发射击间隔|连发射击的间隔，对连发类型枪械有效|
|连发数量|连发子弹的数量，对连发类型枪械有效|
|连发子弹间隔|一次连发的子弹射击间隔，对连发类型枪械有效|
|换弹时间影响因子|枪械换弹的时间倍率|
|切枪时间影响因子|背负枪械和手持枪械的切换时间倍率|
|子弹基础伤害|单颗子弹的基础伤害值|
|子弹最低伤害|子弹在距离衰减/穿透之后的伤害最低值|
|子弹飞行速度|子弹射出枪膛的飞行速度|
|最大射程|子弹的最远射击距离，超出距离子弹被销毁|
|弹匣容量|枪械弹匣内存储的最大子弹数|
|一次拉栓子弹装填数量|``one by one`` 换弹方式的枪械一次填弹的数量，例如狙击枪<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PhJJximage.png)|
|子弹ID|枪械配备的子弹物品ID，可基于子弹物品模板创建，默认为 [和平精英物品表](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/299?autoJump=4.+%E7%89%A9%E5%93%81) 中的预设ID|

【额外子弹配置】

找到枪械物品蓝图中 ``UGCConfig`` 属性组下的 ``额外子弹配置`` 属性，可通过添加元素为该枪械配置其他子弹。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PL6acimage.png)

额外子弹配置目前只支持基于新物品编辑器子弹模板创建的子弹ID，以及 ``【表格管理器】 -> 【内置表格】 -> 【物品表】`` 中带有"831"前缀的子弹物品ID。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KDsZGimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4gktRimage.png)

|属性名|属性说明|
|-|-|
|自动拾取子弹数|自动拾取该类型子弹的数量上限|
|额外子弹配置|支持配置多组额外子弹，且各类子弹均可单独配置属性修改和额外抛体<br>- 武器属性修改配置：枪械装载当前ID的子弹时，对武器属性的修改效果，配置方式可参见 [技能Task-武器属性修改](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E6%AD%A6%E5%99%A8%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9)<br>- 抛体配置：枪械射击使用当前ID的子弹时，可启用额外的抛体，配置方式可参见 [技能Task-发射抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E5%8F%91%E5%B0%84%E6%8A%9B%E4%BD%93:~:text=%E5%8A%A8%E6%80%81%E7%8A%B6%E6%80%81%E5%8F%98%E5%8C%96-,%E6%8A%80%E8%83%BDTask%2D%E5%8F%91%E5%B0%84%E6%8A%9B%E4%BD%93,-%E6%8A%80%E8%83%BDTask%2DLua)<br>- 权重优先级：如果背包中同时存在该枪械支持的多种子弹物品时，会按照该优先级消耗子弹|

---

#### 配件物品特性

【Attr Modify】

所有类型的配件均支持基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的角色及武器属性修改，其中“通过武器Tag特殊修改”支持针对指定武器的属性修改生效。

> 武器属性的说明及修改效果可参考 [枪械属性对照表](https://developer.gp.qq.com/wikieditor/#/catalog/20159)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/19MnNimage.png)

---

#### 装备物品特性

【装备属性】

装备物品可以影响角色属性的变化，也允许拥有独特的装备技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wn31ximage.png)

|属性名|属性说明|
|-|-|
|装备附加的技能列表|装备绑定的 [技能](https://developer.gp.qq.com/wikieditor/#/catalog/20091)，允许存在多种主动或者被动技能，[装配到装备栏](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A3%85%E5%A4%87%E6%A0%8F) 时生效|
|角色属性修改配置列表|基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的角色属性修改，[装配到装备栏](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A3%85%E5%A4%87%E6%A0%8F) 时生效|

---

#### 投掷物品特性

【Projectile】

投掷物品提供抛体实体蓝图、投掷指示器、投掷音效、拉栓倒计时等自定义属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9x9N7image.png)

|属性名|属性说明|
|-|-|
|投掷物|投掷物需要关联抛体实体才能拥有对应的抛体特性，如果 [自定义投掷物](https://developer.gp.qq.com/wikieditor/#/catalog/20157) 或将投掷物变更为 [技能抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20075)，则需要修改此处的蓝图引用|
|投掷物图标路径|手持投掷物状态下的icon图标|
|投掷物按下图标路径|进入投掷状态下的icon图标|
|准备投掷音效|拉栓的音效资源|
|是否启用拉栓倒计时|是否显示拉栓倒计时的UI|
|拉栓倒计时|触发拉栓时，开始倒计时的时长|

---

#### 药品特性

【基础设置】

基础设置为药品使用效果的基础属性，例如使用的时长、恢复的目标效果等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6eXBaimage.png)

|属性名|属性说明|
|-|-|
|使用时间|药品的使用时长，通常表现为动画播放的时长（注意，配置为0会导致药品使用不生效）<br>|
|恢复项|可设置多种恢复属性及恢复量，多属性同步执行恢复<br>- 回复属性类型：预置血量、能量、信号等和平角色的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)<br>- 回复值：使用该药品恢复属性的回复量（0~1：按百分比回复，>1：按字面值回复）<br>- 回复上限：属性回复的最大值上限（0~1：按属性满值的百分比计算，>1：字面值）<br> - 血量预回复条：显示预恢复条，实际不执行回复效果，仅针对血量属性生效|
|是否连续使用|未达到属性回复上限前，是否允许连续使用药品；如果存在多个回复属性，则任意一个属性未回满都能触发连续使用|
|后续增益/减益|使用药品时的额外效果，支持设置多个增益/减益效果，触发时机为“使用时间”计时结束后<br>- 后续增益：配置的 [Buff](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20087) 效果<br>- 附加层数：Buff叠加的层数<br>- 持续时间：Buff持续的时间（-1则永久生效）|

【进阶设置】

除了药品的使用效果，还支持设置药品的使用条件及约束。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7y3ENimage.png)

|属性名|属性说明|
|-|-|
|使用中减速|使用药品时是否降低角色移动速度，该属性为百分比的加法逻辑，取值范围0~1|
|使用条件|满足指定条件才触发使用效果，支持设置多种条件，各条件为逻辑与<br>- 进行比较的属性：预置血量、能量、信号等和平角色的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)<br>- 比较操作符：数值比较运算符<br>- 进行比较的数值：支持常数或基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式<br>- 是否是百分比：是否以百分比的方式执行比较运算|
|手上模型|使用药品时角色手持的物品模型|
|失败提示|不满足使用条件时的提示信息|

---

#### 穿戴装备物品特性

【UGCBackpack Avatar Handle】

防具物品可以影响角色属性的变化，也允许拥有独特的装备技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rwrHBimage.png)

|属性名|属性说明|
|-|-|
|角色属性修改配置列表|基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的角色属性修改，[装配到装备栏](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A3%85%E5%A4%87%E6%A0%8F) 时生效|
|附加技能列表|装备绑定的 [技能](https://developer.gp.qq.com/wikieditor/#/catalog/20091)，允许存在多种主动或者被动技能，可以配置技能激活的时机，包括：拾取时激活、使用时激活、装备时激活和不自动激活（自行控制激活时机）|

【属性配置】

不同的防具物品具备特有的防具属性，例如头盔和防弹衣有耐久和减伤，背包可对背包格子进行扩容。

**头盔**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Y2Gloimage.png)

**防弹衣**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zpjRpimage.png)

**背包**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/e9yQ8image.png)

【附加Actor】

穿戴类装备支持挂接Actor。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pgl15image.png)

- 附加的Actor类：生成的Actor蓝图类
- Socket：支持按 ``部位类型`` 或者 ``插槽名称`` 附加
- Offset：挂载位置基于该Socket点的偏移

在 ``附加Actor配置列表`` 属性中点击【+】添加元素，绑定附加Actor类，绑定后可在编辑器中预览效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jenZS%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17756508324032.png)

点击调试，给玩家穿戴该装备，即可看到效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Vh8jGimage.png)

---

#### 近战武器物品特性

【近战武器实体蓝图】

近战武器物品需要关联武器实体才能拥有对应的特性，不同的近战武器引用的实体蓝图不同，例如大砍刀默认的实体蓝图为 ``BP_UGC_MeleeWeap_Machete``；如果 [自定义近战武器](https://developer.gp.qq.com/wikieditor/#/catalog/20158) 则需要修改此处的蓝图引用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/18Sgkimage.png)

---

### 空白模板实现物品功能

基于空白物品/消耗品模板创建的物品，需要结合 [``OnUseItemV2``](https://developer.gp.qq.com/api/#/searchContent/UBackpackComponentV2?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUBackpackComponentV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UBackpackComponentV2&autoJump=OnUseItemV2)、[``OnMergeItemV2``](https://developer.gp.qq.com/api/#/searchContent/UBackpackComponentV2?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUBackpackComponentV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UBackpackComponentV2&autoJump=OnMergeItemV2) 等物品交互的函数实现相关具体功能效果，以空白消耗品模板为例，实现一个使用物品效果为将使用者变身成光子鸡的物品。

在技能编辑器中，基于Buff模板 [怪物骨骼-光子鸡](https://developer.gp.qq.com/wikieditor/#/catalog/20253?autoJump=%E5%8F%98%E8%BA%AB-%E6%80%AA%E7%89%A9%E9%AA%A8%E9%AA%BC) 创建一个Buff蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dZWCLimage.png)

在物品编辑器中，基于 ``空白消耗品`` 模板创建一个物品蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0DQpkimage.png)

创建并配置完物品基础信息后，点击物资编辑器菜单栏【Lua】按钮，会自动生成带有物品交互相关模板函数的类脚本文件，各交互函数供开发者重载并自定义，本例中只涉及使用后触发Buff，因此在 ``OnUseV2`` 物品被使用回调的事件中实现为玩家添加Buff的逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/i1xKYimage.png)

```lua
function LightSpeedChicken:OnUseV2()
    LightSpeedChiken.SuperClass.OnUseV2(self);

    local SkillPath = UGCMapInfoLib.GetRootLongPackagePath() .. "Asset/Blueprint/Prefabs/Buffs/LightSpeedChicken.LightSpeedChicken_C"
    local SkillClass = UGCObjectUtility.LoadClass(SkillPath)

    local OwnBackpackComponent = UGCItemSystemV2.GetOwnBackpackComponent(self) --获取背包组件
    local PlayerController = OwnBackpackComponent:GetOwner() --获取玩家自身PlayerController
    local PlayerPawn = UGCGameSystem.GetPlayerPawnByPlayerController(PlayerController)

    if PlayerPawn then
        UGCPersistEffectSystem.AddBuffByClass(PlayerPawn, SkillClass)
    end
end
```

完成以上步骤后，点击调试，为玩家添加该物品并点击使用即可观察效果。

![ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vXg58ezgif.com-video-to-gif-converter.gif)

<br>

## 获取物品

玩家获取物品的途径通常有两种：将物品放置在场景中供玩家拾取，或者借助某种交互形式将物品发放至玩家背包内，物品编辑器支持了这两种方式。

### 场景拾取物品

物品编辑器创建的物品无法直接放置在场景中，需要经由 ``UGCPickupWrapper_BP`` 蓝图处理可拾取物的实例化过程。

在 [模式编辑](https://developer.gp.qq.com/wikieditor/#/catalog/124?autoJump=%E6%A8%A1%E5%BC%8F%E7%BC%96%E8%BE%91) 窗口中搜索“UGCPickupWrapper”，将该蓝图拖放至场景中合适的位置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/i7LOHimage.png)

在 ``UGCPickupWrapper_BP`` 蓝图中查找 ``UGCPick Up Wrapper`` 属性分类，``物品ID`` 填写创建物品时生成的ID，``数量`` 为被拾取后进入背包的物品数量，拾取物蓝图将根据物品【基础配置】中设置的拾取物模型进行实例化。
> 当数量>1时不会生成多个拾取物模型，但拾取时物品会按照对应数量进入背包

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Prvvtimage.png)

---

### 动态添加物品

脚本中调用发放物品的API可以将物品直接添加到玩家的背包中：
- 对于和平经典背包调用 [``AddItem``](https://developer.gp.qq.com/api/#/searchContent/UGCBackPackSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackPackSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackPackSystem&autoJump=AddItem)
- 如果玩法 [启用了新背包系统](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E5%90%AF%E7%94%A8%E8%83%8C%E5%8C%85%E7%B3%BB%E7%BB%9F) 可以调用 [``AddItemV2``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=AddItemV2) 或者 [``AddItemByDefineIDV2``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=AddItemByDefineIDV2)

<br>

## 使用物品

不同类型的物品使用交互形式存在差异，例如枪械物品需要装配在 [武器槽位](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E6%AD%A6%E5%99%A8%E6%A7%BD%E4%BD%8D) 上使用，药品可以在背包内直接使用，装备物品需要装配在 [装备槽位](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104?autoJump=%E6%B7%BB%E5%8A%A0%E6%A7%BD%E4%BD%8D) 上使用，其他类型的物品需要自定义使用条件和使用过程。

开发者可以使用 [背包系统](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20104) 提供的丰富API扩展和实现物品的交互逻辑，例如通过 [``ItemCanEquipToSlot``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=ItemCanEquipToSlot) 和 [``EquipItemV2``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=EquipItemV2) 扩展物品的装配规则和逻辑；通过 [``CanUseItemV2``](https://developer.gp.qq.com/api/#/searchContent/UBackpackComponentV2?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUBackpackComponentV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UBackpackComponentV2&autoJump=CanUseItemV2) 和 [``UseItemV2``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=UseItemV2) 扩展物品的使用规则和逻辑等。

> 仅新背包系统提供自定义的拓展功能

---


## 自定义枪械

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 自定义枪械

**涉及API:** `BulletTemplate`, `Loop`, `M416`, `OverrideHitEffectDataAsset`, `ShootWeaponEntity`, `State`

# 自定义枪械

物品编辑器内置了和平精英常用枪械的实体蓝图模板，基于模板创建的枪械实体提供更丰富的参数供开发者自定义修改，包括开火特效、枪械性能、子弹属性等等，甚至可以为枪械赋予技能，实现个性化的改装效果。

<br>

## 创建枪械实体蓝图

以创建M416枪械实体蓝图为例：

1. 从“枪械模板”窗口中选择 ``M416``，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``M416`` 为模板创建”
2. 点击“以 ``M416`` 为模板创建” 按钮，弹出输入名称弹窗，输入枪械名称并点击确定
3. 新建的枪械将添加至“工程物品资源”窗口中，且枪械实体蓝图创建于 ``Asset/Blueprint/Prefabs/Weapons`` 路径下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/u3Ns1image.png)

<br>

## 修改枪械属性

### 开火特效

枪械实体蓝图的【美术表现】属性类别下可以设置枪械射击时枪口的火焰特效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4Ygwpimage.png)

---

### 命中特效和音效

命中特效与音效通过数据资产蓝图配置，内容浏览器右键 ``各种各样 -> 数据资源``，搜索 "Hit Effect Data Asset" 并创建资产蓝图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/J2M8Iimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KtcSpimage.png)

在 【FXConfig】 属性配置对应的命中特效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Z4H8qimage.png)

在 【SoundConfig】 属性配置对应的命中音效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0s0zYimage.png)

**属性名对照表**

|属性名|属性说明|
|-|-|
|Default|默认|
|Concrete|混凝土|
|Dirt|土|
|Water|水|
|Metal|金属|
|Wood|木|
|Grass|草|
|Glass|玻璃|
|Flesh|躯体|
|Steel|钢铁|
|Sandbag|沙袋|
|Sand|沙子|
|Cloth|布料|
|Plastic|塑料|
|Leather|皮料|
|Ceramics|陶器|
|Paper|纸|
|Stone|石头|
|Snow|雪|
|PopCan|易拉罐|
|Leaf|叶子|
|Car|车|
|Asphalt|柏油路|
|ConcreteTDM|TDM混凝土|
|Ice|冰|
|Food|食物|

在自定义武器的 ``ShootWeaponEntity`` 组件中，找到 【Bullet Config】，将上面配置好的命中效果数据资源配置到 ``OverrideHitEffectDataAsset`` 中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xmH6Dimage.png)

[绑定枪械物品](https://developer.gp.qq.com/wikieditor/#/catalog/20103?autoJump=%E7%BB%91%E5%AE%9A%E6%9E%AA%E6%A2%B0%E7%89%A9%E5%93%81:~:text=%E6%8A%80%E8%83%BD%E9%85%8D%E7%BD%AE-,%E7%BB%91%E5%AE%9A%E6%9E%AA%E6%A2%B0%E7%89%A9%E5%93%81,-%E5%BC%80%E5%8F%91%E5%8A%A9%E6%89%8B) 后，点击调试，给玩家添加该枪械，即可看到效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Jrxgmimage.png)

---

### 枪械性能

枪械性能相关参数涵盖射击模式、人机工效、伤害配置和子弹配置等部分的属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iEyGyimage.png)

|属性名|属性说明|
|-|-|
|准心预设|准心的UI效果，目前支持步枪、霰弹枪、手枪、榴弹枪四类<br>【步枪】<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PAceHimage.png)<br>【霰弹枪】<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/isXReimage.png)<br>【手枪】<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aW81bimage.png)<br>【榴弹枪】<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XE41vimage.png)|
|攻击间隔影响因子|枪械射击间隔的时间倍率|
|后坐力影响因子|后坐力程度倍率|
|散布影响因子|子弹偏离准心的程度，针对多发子弹类型的枪械，例如霰弹枪|
|射击间隔|单发子弹的射击间隔，对单发类型枪械有效|
|连发射击间隔|连发射击的间隔，对连发类型枪械有效|
|连发数量|连发子弹的数量，对连发类型枪械有效|
|连发子弹间隔|一次连发的子弹射击间隔，对连发类型枪械有效|
|换弹时间影响因子|枪械换弹的时间倍率|
|切枪时间影响因子|背负枪械和手持枪械的切换时间倍率|
|子弹基础伤害|单颗子弹的基础伤害值|
|子弹最低伤害|子弹在距离衰减/穿透之后的伤害最低值|
|伤害类型Tag列表|支持为子弹伤害设置多种Tag，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20102) 创建|

---

### 子弹属性

枪械实体蓝图的【子弹配置】属性类别下可以设置子弹的基础属性，如果想要枪械能够支持装填和发射更多不同类型的子弹或者抛体，详情见 [枪械物品特性](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=%E6%9E%AA%E6%A2%B0%E7%89%A9%E5%93%81%E7%89%B9%E6%80%A7:~:text=%E7%B1%BB%E5%9E%8B%E7%89%B9%E6%80%A7%E9%85%8D%E7%BD%AE-,%E6%9E%AA%E6%A2%B0%E7%89%A9%E5%93%81%E7%89%B9%E6%80%A7,-%E9%85%8D%E4%BB%B6%E7%89%A9%E5%93%81%E7%89%B9%E6%80%A7) 中的额外子弹配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IP9gOimage.png)

|属性名|属性说明|
|-|-|
|子弹飞行速度|子弹射出枪膛的飞行速度|
|最大射程|子弹的最远射击距离，超出距离子弹被销毁|
|弹匣容量|枪械弹匣内存储的最大子弹数|
|一次拉栓子弹装填数量|栓狙枪械一次填弹的数量，例如98K|
|启用自定义抛体|如果启用，则会按 [通用抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20165) 的设置额外发射抛体|
|自定义抛体|启用后，设置抛体的蓝图类|

枪械实体蓝图的 ``ShootWeaponEntity`` 组件属性集中，【BulletConfig】控制弹匣初始子弹数和无限弹药的设置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qhKAvimage.png)

- Has Infinite Bullets：开启后拥有无限弹药，但受制于弹匣的容量仍需换弹
- Clip Has Infinite Bullets：开启后弹匣无容量限制，拥有无限弹药且无需换弹
- Init Bullet in Clip：当玩家获得枪械时，弹匣内的初始子弹数

---

### 技能配置

开发者可以为枪械挂载特定的技能及设定技能的赋予条件和生效时间。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/W5E7aimage.png)

- 技能类：通过 [技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091) 创建的技能
- 技能赋予条件：何时为角色添加技能
	- 武器装备激活：当玩家手持该枪械时添加
	- 武器使用激活：当玩家装配该枪械时添加
	- 不自动激活：开发者自行实现添加技能的逻辑
- 绑定开火事件：启用后武器触发开火时才会触发技能，注意只有一个技能能绑定开火按键
- 技能生效时间：以 ``技能赋予条件`` 的时间点开始的有效时长，超过生效时间会自动卸载技能，-1为永久生效

<br>

## 绑定枪械物品

枪械实体蓝图无法直接进入背包或者实例化为可拾取物，需要绑定枪械物品才有效，通过物品编辑器 [创建枪械物品](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=%E6%96%B0%E5%BB%BA%E7%89%A9%E5%93%81%E8%93%9D%E5%9B%BE)，将 ``Weapon Class`` 属性设置为该实体蓝图，即得到一把改装后的全新枪械。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/z9kGtimage.png)

<br>

## 技能枪械制作

以AKM枪械改为电击步枪为例，开发者可以熟悉技能枪械的制作流程，实现不同功能和表现的自定义枪械。

### 1. 创建枪械物品

打开【物品编辑器】，在【物品】和【枪械】页签中创建一把AKM枪械物品和对应的武器蓝图，并进行绑定。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XzGFDimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QFYHcimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IC6Xrimage.png)

---

### 2. 创建技能蓝图

打开【技能编辑器】，创建一个空技能模板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/v5KLaimage.png)

---

### 3. 绑定枪械技能

回到【物品编辑器】AKM枪械的武器蓝图配置面板，将创建的技能赋予给枪械，勾选 ``绑定开火按键`` 使技能能够监听枪械开火的流程，配置详情可参考 [技能配置](https://developer.gp.qq.com/wikieditor/#/catalog/20103?autoJump=%E6%8A%80%E8%83%BD%E9%85%8D%E7%BD%AE:~:text=%E5%AD%90%E5%BC%B9%E5%B1%9E%E6%80%A7-,%E6%8A%80%E8%83%BD%E9%85%8D%E7%BD%AE,-%E7%BB%91%E5%AE%9A%E6%9E%AA%E6%A2%B0) 。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EWPEHimage.png)

打开枪械蓝图的 ``ShootWeaponEntity`` 组件，找到 ``BulletTemplate`` ，点击【X】清空原来的发射子弹配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zL2csimage.png)

---

### 4. 配置技能逻辑

回到【技能编辑器】中创建的空模板技能，切到【Skill Flow Graph】面板，创建一个 ``State`` 技能节点并命名为 "fire"，创建一个 ``Global Event`` 全局事件节点（暂时不要重命名这个节点，会导致节点功能失效），如图所示进行连接。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iTlYDimage.png)

点击 "fire" 技能节点，勾选 ``Loop``，保证按住攻击键时达到持续攻击的效果，再点击下方按钮创建开火技能轨道

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/05CGVimage.png)

点击 "NewEvent_0" 全局事件节点，选择监听 ``输入事件`` 并配置输入事件为 ``抬起``，详情配置可参考 [技能Event](https://developer.gp.qq.com/wikieditor/#/catalog/20112?autoJump=%E9%80%9A%E7%94%A8%E7%B1%BB%E4%BA%8B%E4%BB%B6)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SpkSkimage.png)

在【序列播放器】中添加 ``选择目标`` 和 ``造成伤害`` 的 [技能task](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20094)，详细配置可参考 [序列播放器配置](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E5%BA%8F%E5%88%97%E6%92%AD%E6%94%BE%E5%99%A8%E9%85%8D%E7%BD%AE:~:text=%E6%8A%80%E8%83%BD%E9%98%B6%E6%AE%B5%E9%85%8D%E7%BD%AE-,%E5%BA%8F%E5%88%97%E6%92%AD%E6%94%BE%E5%99%A8%E9%85%8D%E7%BD%AE,-Task%E5%8F%82%E6%95%B0%E8%AE%BE%E7%BD%AE)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xoSE9image.png)

配置两个技能task的参数，【选择器】选择 ``扇形目标选择器``，勾选 ``是否需要可见`` 方便调试，配置伤害轨道的伤害数值，其他配置参数可参考下图。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/msHUpimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FRY0uimage.png)

调整两个技能task的 ``开始时间`` 和 ``结束时间``，配置 ``开始时间`` 时间需要往后一点（目前 ``开始时间`` 为0时不能正常触发循环），配置 ``结束时间`` 时间为0.2s。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FErI9image.png)

以上配置完成后，点击【编译】和【保存】，返回【PriewPort】面板即可预览效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JxFclimage.png)

---

### 5. 调整枪械性能

回到【物品编辑器】枪械蓝图中，调整 [枪械性能](https://developer.gp.qq.com/wikieditor/#/catalog/20103?autoJump=%E6%9E%AA%E6%A2%B0%E6%80%A7%E8%83%BD:~:text=%E7%89%B9%E6%95%88%E5%92%8C%E9%9F%B3%E6%95%88-,%E6%9E%AA%E6%A2%B0%E6%80%A7%E8%83%BD,-%E5%AD%90%E5%BC%B9%E5%B1%9E%E6%80%A7) 参数，此技能枪械伤害是跟随技能传递的，子弹伤害需要配置为0。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cVbQmimage.png)

---

### 6. 脚本实现技能表现

技能的轨道逻辑主要在DS上运行，技能的表现逻辑需要通过lua来实现。

回到【技能编辑器】，在【我的蓝图】中添加技能表现所需的变量，此技能表现所需的变量和逻辑代码可以创建一个 ``电击步枪技能`` 模板作为参考。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yR8LYimage.png)

在创建的 ``电击步枪技能`` 模板中，点击【Lua】进入编辑，可见技能表现逻辑。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oYFNOimage.png)

---

### 7. 调试枪械效果

在场景中放置怪物，点击【调试】，给玩家添加这把技能枪械，攻击怪物即可看到效果。

![2026-03-0511-42-39-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/115e12026-03-0511-42-39-ezgif.com-video-to-gif-converter.gif)






---


## 背包系统

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 背包系统

**涉及API:** `AddCellCapacity`, `AddMaxCellCapacity`, `AsyncLoadObjectBySoftPath`, `BP_BackpackComponentV2`, `BP_BackpackComponentV2_Custom`, `BP_BackpackUIComponentV2`, `BP_BackpackUIComponentV2_Custom`, `BP_BackpackUIComponentV2_Custom.CompareQuantity`, `BP_Grid_Tag`, `BackpackUIComponent.CompareQuality`, `CheckCustomItem`, `CheckUseItem`, `ClickLockBackpackItem`, `DA_GameModeGeneral`, `EquipmentSlot`, `FItemDefineID`, `GP_BackpackV2`, `Get`, `GetOwner`, `InitData`

# 背包系统

配合 [物品编辑器](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20101) 构建的全新背包系统，区别于和平精英经典背包的单列布局结构，新背包采用网格布局的设计，加入了背包扩容的概念，在继承物品基础操作和可堆叠的功能上，支持持久化存储物品数据的能力，并扩展出装备栏和仓库的独立功能，使得新的背包系统更通用、扩展性更强，为开发者打造多元化的绿洲玩法提供能力支撑。

<br>

## 启用背包系统

为了兼容经典背包，新的背包系统通过 [GamePart](https://developer.gp.qq.com/wikieditor/#/catalog/20090) 提供模块化的启用方式，玩法默认使用经典背包，启用后被新背包替代。
> 旧 [物资编辑器](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/185) 的物资功能无法适配新背包，新背包需要与新 [物品编辑器](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20101) 配套使用

点击编辑器菜单栏的【玩法通用设置】按钮，在弹出的 ``DA_GameModeGeneral`` 数据资产蓝图中的 ``Active Game Part Configs`` 属性下添加“GP_BackpackV2”模块，保存并 [启动调试](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/307) 即可验证是否生效：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Jj4BDimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PdoN7image.png)

<br>

## 自定义背包系统

完整的背包系统包含物品背包、装备栏和仓库三部分功能，开发者可以对各功能进行自定义设置，包括但不限于设置背包容量、解锁格子、配置装备槽位、启用仓库等等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l0wWnimage.png)

### 创建背包组件

背包系统的可配置属性集中在 ``背包组件（BP_BackpackComponentV2）`` 和 ``背包UI组件（BP_BackpackUIComponentV2）`` 中，``GP_BackpackV2`` 模块内置引用了默认的组件，开发者可以创建新的组件蓝图以对背包系统的属性进行自定义设置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KCKsIimage.png)

``GP_BackpackV2`` 模块提供了快捷的创建方式，以背包组件为例，点击右侧的【创建】按钮，将在 ``Asset/GamePartCustom/BackpackV2`` 目录下自动生成新的组件蓝图 ``BP_BackpackComponentV2_Custom``，该蓝图继承自默认的背包组件 ``BP_BackpackComponentV2``。

> 创建的新背包UI组件为 ``Asset/GamePartCustom/BackpackV2/BP_BackpackUIComponentV2_Custom``

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Iu4PIimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FVB9Wimage.png)

该组件蓝图自动被引用，且创建按钮变更为【打开】按钮，点击将自动打开 ``BP_BackpackComponentV2_Custom`` 蓝图编辑器窗口。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vNDjCimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wERfdimage.png)

<br>

### 自定义物品背包

物品背包的功能区域分为：排序规则、背包网格、物品页签、物品整理和扩容代币。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/86eFAimage.png)

**A. 排序规则**

物品背包的默认排序规则为按品质由高到低排序，开发者可以扩展自定义的排序规则。

**B. 背包网格**

存储及操作物品的网格空间，可以设置网格的容量，支持代币解锁格子，每格可堆叠的物品数量受物品 [最大堆叠数量](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20101?autoJump=%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 的影响；若格子被锁定，会显示解锁需要的代币及数量。

**C. 物品页签**

通过标签的方式对物品进行筛选及分类。

**D. 物品整理**

物品整理功能固定将同类的物品按 [可堆叠数量上限](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20101?autoJump=%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 进行合并，减少对网格容量的占用。

**E. 扩容代币**

解锁格子的代币及余额展示，最多支持显示4种货币。

---

#### 背包按钮显隐

在编辑器顶部的 ``玩法通用设置`` 中可以设置是否显示背包按钮，也可以通过 [``SetBackpackButtonVisible``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=SetBackpackButtonVisible:~:text=GetCustomUIWidget-,SetBackpackButtonVisible,-%E7%BB%BF%E6%B4%B2%E5%90%AF%E5%85%83) 函数控制背包按钮的动态显隐。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UiSeLimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/M1wo4image.png)

---

#### 设置背包容量

背包网格具有两种基础状态：空闲和待解锁，网格初始的空闲和待解锁状态通过格子容量属性设置。

打开 ``BP_BackpackComponentV2_Custom`` 组件蓝图，在【细节】面板 ``Backpack Component V2`` 属性类别下设置容量属性：
- 默认格子容量：空闲状态的格子数量，对应可使用的格子数
- 最大格子容量：背包最大网格数，包含空闲状态和待解锁状态，也即 **``待解锁格子数 = 最大格子容量 - 默认格子容量``**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UyE0Himage.png)

---

#### 设置物品页签

打开 ``BP_BackpackUIComponentV2_Custom`` 组件蓝图，在【细节】面板 ``Tab Info`` 属性组下添加一个新的页签：
- TabName：页签的名称
- Tags：带有指定 [Tag标记](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=V2%E8%83%8C%E5%8C%85%E9%85%8D%E7%BD%AE) 的物品会被自动分类到该页签下，判定遵循 [GameplayTag匹配](https://developer.gp.qq.com/wikieditor/#/catalog/20102?autoJump=GameplayTag%E5%8C%B9%E9%85%8D) 规则；若留空则代表任意物品都允许进入该页签

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9NsToimage.png)

> 页签的设置对背包和仓库同时生效

---

#### 扩展排序规则

打开 ``BP_BackpackUIComponentV2_Custom`` 组件蓝图，在【细节】面板 ``Sort Info List`` 属性组下添加一个新的排序规则配置：
- SortName：排序规则的名称
- SortFunctionName：自定义的排序函数名

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BdXgEimage.png)

打开组件蓝图对应的lua脚本，声明并实现自定义的排序函数：

```lua
-- Data形参结构
Data = {
	idx, -- 当前位置索引 number
	InstanceID, -- 物品实例ID number
	DefineID, -- 物品数据 FItemDefineID
}

---@param Data1 table 前一个物品数据
---@param Data2 table 后一个物品数据
---@return bool 是否保持位置不变
function BP_BackpackUIComponentV2_Custom.CompareQuantity(Data1,Data2)
	-- TODO 实现按数量排序的逻辑
end
```

按品质排序的代码示例：

```lua
function BackpackUIComponent.CompareQuality(Data1,Data2)
    local ItemDefinID1 = Data1.DefineID;
    local ItemDefinID2 = Data2.DefineID;
    if ItemDefinID1 == nil or ItemDefinID2 == nil then
        print("BackpackUIComponent:CompareQuality error InstanceID1:"..tostring(InstanceID1)..",InstanceID2:"..tostring(InstanceID2))
        return
    end
    local quality1 = UGCItemSystemV2.GetItemQualityV2(ItemDefinID1.TypeSpecificID)
    local quality2 = UGCItemSystemV2.GetItemQualityV2(ItemDefinID2.TypeSpecificID)
    --品质排序
    if quality1 ~= quality2 then
        return quality1 > quality2 -- 物品1品质大于物品2品质，则保持位置不变
    end
    return Data1[1] < Data2[1] -- 品质相同，则物品1原始位置在前，则保持位置不变
end
```

---

#### 为网格增添自定义UI

背包中的物品默认展示物品图标、品质色及物品数量，支持为网格额外叠加UI特效或者自定义的icon图等效果，叠加配置会在仓库格子、背包格子、物品详情和装备栏同时生效。

打开 ``BP_BackpackUIComponentV2_Custom`` 组件蓝图，在【细节】面板 ``Custom Item UIWidgets`` 属性组下设置控件蓝图及筛选规则：
- ItemTag：UI效果影响带指定 [标记Tag](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=V2%E8%83%8C%E5%8C%85%E9%85%8D%E7%BD%AE) 的物品
- Customtypes：UI效果影响指定 [自定义类型](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=%E7%89%B9%E6%80%A7%E9%85%8D%E7%BD%AE) 的物品
- WidgetSoftClassPath：引用的控件蓝图（图例中 ``BP_Grid_Tag`` 蓝图为新建的控件蓝图）

> ItemTag和Customtypes为“逻辑或”的关系

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FJBNsimage.png)
![企业微信截图_174290448329.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UCsNX%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_174290448329.png)

通用的筛选规则使得同类型的物品拥有指定的UI效果，更进一步地可以在控件蓝图中声明一个名为 **``InitData``** 的函数，当物品图标被创建时会创建对应的控件蓝图并调用 **``InitData``**，在该函数中实现自定义的逻辑以达到更精准、个性化的叠加效果，下面是以 ``3DUI_Text`` 控件为例，用代码逻辑设置图片。

```lua
---@field 3DUI_Icon UImage
local 3DUI_Text = {}

-- 内部约定好的函数名称InitData
-- @param DataTable table @物品数据 {ItemDefineID:物品FItemDefineID, DataType:EItemDataTypeStrs背包物品类型, ItemID:物品ID}
function 3DUI_Text:InitData(DataTable)
    -- 异步加载物品图标纹理并设置到Image控件
    local weakSelf = WeakObjectPtr(self)
    UGCObjectUtility.AsyncLoadObjectBySoftPath(UGCItemSystemV2.GetItemIconTextureV2(DefineID.TypeSpecificID), function(LoadedTexture)
        if weakSelf:IsValid() then
            weakSelf:Get().3DUI_Icon:SetBrushFromTexture(LoadedTexture, true)
        end
    end)
end
```

---

#### 扩展物品详情

背包系统为进入背包的物品提供了扩展详情面板的能力，方便开发者为物品描述添加额外展示信息。

打开 ``BP_BackpackUIComponentV2_Custom`` 组件蓝图，在【细节】面板 ``Custom Details Wights`` 属性组下设置控件蓝图及筛选规则：
- ItemTag：面板效果影响带指定 [标记Tag](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=V2%E8%83%8C%E5%8C%85%E9%85%8D%E7%BD%AE) 的物品
- Customtypes：面板效果影响指定 [自定义类型](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=%E7%89%B9%E6%80%A7%E9%85%8D%E7%BD%AE) 的物品
- WidgetSoftClassPath：引用的控件蓝图

> ItemTag和Customtypes为“逻辑或”的关系

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/a7Ghgimage.png)

详情面板同样也支持通过控件蓝图的 **``InitData``** 函数扩展逻辑。

---

#### 配置扩容代币

扩容即为解锁背包网格，目前支持解锁的代币类型为物品，因此需要先通过 [物品编辑器](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20101?autoJump=%E5%88%9B%E5%BB%BA%E7%89%A9%E5%93%81) 创建货币物品，再配置到背包组件上。

> 货币物品同样具有 ``最大堆叠数`` 属性，超出堆叠数将在数据上产生分堆、影响性能，建议将该属性值设置为小于21亿的较大值，且玩法中严格控制代币的产出

1. 基于空白物品模板创建货币物品。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YB8moimage.png)

2. 打开 ``BP_BackpackComponentV2_Custom`` 组件蓝图，在【细节】面板中为 ``货币物品ID列表`` 属性添加货币的物品ID，该货币物品会被识别为代币类型，且不占用背包格子，代币以 ``物品图标 + 数量`` 的形式显示在代币栏。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8Wyqrimage.png)
	
3. 打开 ``BP_BackpackUIComponentV2_Custom`` 组件蓝图，在【细节】面板中设置解锁格子的代币及数量：
- Cost Coin Value：解锁格子花费的代币数量
- Cost Coin ID：代币的物品ID

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TJ94jimage.png)

点击待解锁的背包网格时，将弹出解锁网格的购买弹窗，解锁会消耗背包中代币的相应数量，解锁增加的容量是持久化的。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lMflAimage.png)

---

#### 自定义背包扩容条件

如果需要自定义解锁逻辑，可重写 ``BP_BackpackUIComponentV2`` 中的 [``ClickLockBackpackItem``](https://developer.gp.qq.com/api/#/searchContent/BackpackUIComponent?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBackpackUIComponent.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BackpackUIComponent&autoJump=ClickLockBackpackItem) 函数，通过接口 [``AddCellCapacity``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=AddCellCapacity:~:text=GetMaxCellCapacity-,AddCellCapacity,-AddMaxCellCapacity) 为背包解锁格子，解锁增加的容量是持久化的。

```lua
---点击上锁格子的响应函数
---生效范围：客户端
---@param DataType number @类型 [0:背包数据, 1:仓库数据]
function BP_BackpackUIComponentV2_Custom:ClickLockBackpackItem(DataType)
    local PlayerController = self:GetOwner()
    local itemCount = UGCBackpackSystemV2.GetItemCountV2(PlayerController, 8310001)
    -- 判断条件，例如背包内有指定数量的道具才能解锁背包格子
    if itemCount >= 10 then
        -- 满足则解锁1个背包格子
        UGCBackpackSystemV2.AddCellCapacity(PlayerController, 1)
    end
end
```

与之相对的，[``AddMaxCellCapacity``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=AddMaxCellCapacity:~:text=AddCellCapacity-,AddMaxCellCapacity,-RemoveMaxCellCapacity) 接口增加的容量不会持久化，与背包扩容不同。

---

#### 设置背包样式

背包支持全屏与半屏两种样式，且兼容装备栏、仓库与背包的组合场景，通过 ``BP_BackpackUIComponentV2`` 组件上的 ``背包样式`` 和者 ``背包模式`` 属性可设置背包的显示样式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DTk4Fimage.png)

- 背包样式（Style）：全屏/半屏
- 背包模式（Mode）：背包系统的样式，0默认代表显示装备栏+背包，等同于1的效果
	- 1：背包 + 装备
	- 2：背包 + 仓库
	- 3：背包 + 仓库 + 装备
	
可通过接口 [``OpenBackpackPanelStyle``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=OpenBackpackPanelStyle:~:text=IsCurrency-,OpenBackpackPanelStyle,-OpenBackpackPanel) 打开背包。

全屏样式：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/X1qaiimage.png)

半屏样式：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GxI6Timage.png)

---

#### 自定义物品操作按钮

物品操作按钮分为内置按钮列表和自定义按钮列表，通过 ``BP_BackpackUIComponentV2`` 组件上的 ``内置按钮列表`` 和 ``自定义按钮列表`` 可设置对背包内物品操作按钮的显示样式、显隐和按钮响应的对物品的操作（如使用、丢弃、销毁、装备等），两个列表共同起作用，配置使用一致。

**默认内置按钮效果**

消耗类物品：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BiqUaimage.png) 

装备类物品：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sravbimage.png) 

已存入仓库的物品：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8UFiuimage.png)

> ``存入仓库`` 和 ``存入背包`` 按钮需要启用仓库（设置带有仓库的背包模式）和启用 [是否持久化](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=V2%E8%83%8C%E5%8C%85%E5%B1%9E%E6%80%A7%E9%85%8D%E7%BD%AE:~:text=%E8%83%8C%E5%8C%85%E5%B1%9E%E6%80%A7%E9%85%8D%E7%BD%AE-,V2%E8%83%8C%E5%8C%85%E5%B1%9E%E6%80%A7%E9%85%8D%E7%BD%AE,-%E7%B1%BB%E5%9E%8B%E7%89%B9%E6%80%A7%E9%85%8D%E7%BD%AE) 的物品才会显示

**按钮列表属性**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kXnrKimage.png)

- DisplayName:（按钮名称）：按钮文字显示
- ConditionFuncName（条件函数名）：满足条件函数，按钮才会显示，至多同时显示8个按钮
- FuncName（响应函数名）：点击按钮响应的函数
- BtnStyle（按钮样式）：目前提供四种按钮预设

**扩展内置按钮逻辑**

内置按钮支持在内置规则上扩展叠加按钮显示条件等逻辑，以能量饮料类型的物品才显示使用按钮的场景为例，演示扩展逻辑的实现方法。

点击 ``BP_BackpackUIComponentV2`` 组件上的【Lua】编辑按钮，打开背包UI组件的脚本。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KN22iimage.png)

定义一个按钮显示条件函数命名为“CheckCustomItem”，内置使用按钮的条件判定函数为 ``CheckUseItem``，在判断物品的ID类型后调用此函数作为返回结果。

> 内置按钮的默认条件函数不支持覆写

```lua
--在内置规则上叠加条件
function BP_BackpackUIComponentV2_Custom:CheckCustomItem(DefineID, DataType)
  	-- 8310000为物编创建的能量饮料物品id
    if DefineID.TypeSpecificID == 8310000 then
				-- 获取内置条件结果
        local bCheckUse = self:CheckUseItem(DefineID, DataType)
        return bCheckUse    
    else
				return false
    end
end
```

保存Lua脚本后，修改按钮的条件函数名为脚本中所定义的条件函数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wrb0Zimage.png)

点击【编译】并【保存】对 ``BP_BackpackUIComponentV2`` 组件的修改，添加能量饮料以及其他对照物品，打开背包点击格子物品，即可观察效果。

![2026-01-1415-48-34-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fOb4T2026-01-1415-48-34-ezgif.com-video-to-gif-converter.gif)

**自定义额外按钮**

同理，开发者也可以自定义额外的物品操作按钮，在 ``BP_BackpackUIComponentV2`` 组件上的自定义按钮列表，点击【+】添加一个自定义按钮，在组件的Lua脚本中定义该按钮的条件函数和响应函数并编写逻辑，配置对应的函数名，即可实现除了内置按钮的物品操作外其他效果（比如通过物品召唤宠物等功能）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jQJYgimage.png)

添加的自定义按钮会在内置按钮后，按自定义列表的顺序进行排列展示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QqmmFimage.png)

---

#### 自定义物品品质效果

背包物品品质支持新增物品品质，自定义修改品质条、品质底图、品质图标。

点击编辑器菜单栏的【玩法通用设置】按钮，找到 ``Item Quality`` 属性进行配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/02j8zimage.png)

对应的品质编号，与【[物品编辑器2.0](https://developer.gp.qq.com/wikieditor/#/catalog/20101)】的 ``物品品质`` 属性配置相关联。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2ItWcimage.png)

---

### 自定义装备栏

装备栏的槽位分为武器槽位和装备槽位两部分，其中武器槽位包含2个固定预设的主副武器槽位，除此之外，开发者可以修改和扩展自定义的槽位。

> 有关背包系统所有预设槽位及扩展功能，可参见 [物品与背包槽位](https://developer.gp.qq.com/wikieditor/#/catalog/20210)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/k7bE7image.png)

#### 武器槽位

打开 ``BP_BackpackComponentV2_Custom`` 组件蓝图，在【细节】面板中找到 ``装备槽位配置`` ，该属性组预设了 ``EquipmentSlot.Core.MainSlot1``、``EquipmentSlot.Core.MainSlot2``、``EquipmentSlot.Core.SubSlot`` 和 ``EquipmentSlot.Core.MeleeSlot`` 4种武器槽位，其中“武器一”和“武器二”对应的两个槽位不可删除且不可变更槽位名称（允许修改槽位中文名及槽位类型约束）。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TWJs9image.png)

---

#### 装备槽位

背包预设了头盔、背包和防弹衣三种常用的槽位，可以在 ``装备槽位配置`` 属性组下添加新的元素以增加新槽位：

- 槽位名称：同属于 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102)，但必须为 ``EquipmentSlot`` 下的子级Tag
- 槽位中文名：槽位的名称
- 槽位类型约束：槽位允许装配的 [物品类型](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20101?autoJump=%E7%89%B9%E6%80%A7%E9%85%8D%E7%BD%AE)，支持多种类型

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TpxI0image.png)

若装备物品类型与槽位类型匹配，则物品可被装配到对应槽位上。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uCZWPimage.png) 

<br>

### 自定义仓库

仓库作为物品背包的扩展功能，支持物品在背包和仓库之间的转移，拥有独立的容量，适用于存储可持久化的物品。

#### 启用仓库

仓库默认为关闭状态，需要在脚本中适当的时机调用 [``OpenBackPackPanel``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=OpenBackpackPanel:~:text=OpenBackpackPanelStyle-,OpenBackpackPanel,-CloseBackpackPanel) 以启用。

代码示例：

```lua
function BP_Func_Button:OnClickOpenWareHouse()
    UGCBackpackSystemV2.OpenBackpackPanel(5)
end
```

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZnKsNimage.png)

仓库默认共享背包的 ``页签`` 与 ``网格自定义UI`` 设置，如果背包配置了 ``扩容代币``，则将在背包底部额外显示“存入代币”和“取出代币”按钮，允许玩家将代币在背包与仓库之间转移。

---

#### 设置仓库容量

仓库的网格机制与物品背包类似，支持物品的存取和删除，但无法直接使用，通过仓库格子的容量属性设置格子状态，同样支持扩容。

打开 ``BP_BackpackComponentV2_Custom`` 组件蓝图，在【细节】面板 ``Backpack Component V2`` 属性类别下设置容量属性：
- 默认仓库格子容量：空闲状态的格子数量，对应可使用的格子数
- 最大仓库格子容量：仓库最大网格数，包含空闲状态和待解锁状态，也即 **``待解锁格子数 = 最大格子容量 - 默认格子容量``**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KgQpXimage.png)

<br>

## API参考

|函数库/类名|函数类型|函数功能范围|
|-|-|-|
|[UGCBackpackSystemV2](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2)|对象函数|V2背包对物品和装备的操作、内置仓库、容量限制以及货币的查询|
|[UGCItemSystemV2](https://developer.gp.qq.com/api/#/searchContent/UGCItemSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCItemSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCItemSystemV2)|对象函数|读取和查询物品信息|



---


## 物资刷新器

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 物资刷新器

**涉及API:** `BP_UGCItemSpawner`, `CustomID`, `EventName`, `Lua脚本`, `M16A4`, `NewPointManager`, `TestSpawn`, `UGCDrop`

# 物资刷新器

物资刷新功能是编辑器提供的一个灵活配置工具，旨在帮助开发者在场景中轻松配置物资的刷新。此功能由 **物资刷新点** 和 **物资刷新管理器** 组成，能够实现自动和复杂的物资刷新流程。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UK76yimage.png)
<br>

## **功能概述**

物资刷新功能主要由 **物资刷新点** 和 **物资刷新管理器** 组成，二者密切配合，分别承担物资的生成位置、刷新间隔和刷新流程管理的功能。

### **物资刷新点**

物资刷新点是一个 **Actor**，用来指定物资的类别、刷新位置和单次刷新的数量。刷新点支持两种工作模式：

* **独立运作**：物资刷新点可以单独运行，在指定位置自动生成物资并在物资被拾取后自动补充。
* **与刷新管理器协作**：当物资刷新点与刷新管理器结合使用时，刷新点提供物资刷新位置和类别，由管理器控制刷新时机。

### **物资刷新管理器**

物资刷新管理器也是一个 **Actor**，用于实现更复杂的物资刷新流程。通过管理多个物资刷新点，管理器可以自定义刷新时机，并控制刷新点的刷新间隔及数量。多个管理器可以在同一场景中共存，相互独立，不会干扰彼此的操作。
<br>

## **功能详解**

### **物资刷新点**

#### **创建物资刷新点**

在内容浏览器中，`右键 -> 蓝图` 搜索 `BP_UGCItemSpawner` ，以 `物品刷新点` 为父类创建一个蓝图，如图所示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5JrJ5image.png)

创建完成后，将物资刷新点蓝图放置在场景中希望刷出物资的位置。

#### **配置物资刷新点**

在关卡界面中选中物资刷新点，配置其属性，如下所示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OkdXBimage.png)

**配置详情**

   * **物资配置模式**：

     * **物资ID**：通过物品编辑器中的物资ID指定要刷新的物资。
     * **掉落表**：使用 [通用掉落](https://developer.gp.qq.com/wikieditor/#/catalog/20058) 指定的 `掉落ID` 。
     * **掉落组表**：通过 [通用掉落](https://developer.gp.qq.com/wikieditor/#/catalog/20058) 选择 `掉落组ID` 。
     * **自定义**：允许玩家在 Lua 脚本中选择刷新的物资，并提供自定义ID供配置。
   * **是否需要管理器**：确定该刷新点是否可以独立运作，还是必须依赖物资刷新管理器。
   * **是否循环生成**：如果选中该选项，物资在被拾取后会自动刷新。
   * **刷新间隔（秒）**：物资被拾取后，需要等待多长时间才会刷新。

此处，`物资配置模式` 选用的是 `物资ID`，开发者可将具体的物品ID配置在 `物资ID` 处，作为需要刷新的物资，每次刷新的数量为1，物资在被拾取后将会间隔5s生成。

![企业微信截图_17494608353099.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/r379w%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17494608353099.png)

**掉落表/掉落组表**

使用 `掉落表` 和 `掉落组表` 可以配置更复杂的物资生成逻辑，如每次生成都根据概率从多个物品中随机生成，新建一个掉落表 `UGCDrop` ，做如下配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kdY9iimage.png)

如上所示，掉落表中配置了三个物品，分别为`AKM`、`M16A4` 以及 `SCAR-L` 三把步枪，将 `物资配置模式` 配置为 `掉落表`，`掉落ID` 配置为0，如此每次生成物资都会根据概率从这三把武器中随机生成。

>注：此处物品ID只支持 `经典物品ItemID` ，不支持 `虚拟物品ItemID` 。

**自定义**

除了以上三种固定的物资配置模式，开发者还可以通过覆写物资生成的事件，自定义物资生成的类型和数量。这样，开发者可以根据具体需求灵活地控制物资的生成方式，例如根据游戏逻辑动态选择生成的物资类型或调整生成物资的特性。

选中场景中的 `物资刷新点Actor` ，将物资配置模式修改为 `自定义` ，并添加两个模式参数，如图所示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mHeVtimage.png)

其中添加的两个模式参数将会作为 `Table<Table<KeyType, ValueType>>` 类型传递至覆写事件中，打开 `物资刷新点` 蓝图，点击 `Lua` 按钮进入脚本，脚本中已经预置了自定义物资生成的事件，如下所示。

``` lua
function NewPoint:CustomSpawnItem(CustomID)
end
```

其中 `CustomID` 为自定义参数列表，即在 `物资刷新点Actor` 上配置的自定义模式参数，该事件需使用 [**SpawnItem**](https://developer.gp.qq.com/api/#/searchContent/AUGCItemSpawner?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAUGCItemSpawner.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCItemSpawner&autoJump=SpawnItem) 方法生成具体的物资数据，合并成 `Table<Table<KeyType, ValueType>>` 类型数据返回。

``` lua
function NewPoint:CustomSpawnItem(CustomID)
    ugcprint("启动自定义物资刷出流程")

    local item = {}

    for k, v in pairs(CustomID) do
        ugcprint("k:" .. k .. " v: " .. v)
        table.insert(item, self:SpawnItem(k, v))
    end

    return item
end
```

>注：物资刷新器相关API可查询文档：[物资刷新器](https://developer.gp.qq.com/api/#/searchContent/AUGCItemSpawner?classDetailShow=true&path=class%2Fdetail%2FOthers%2FAUGCItemSpawner.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCItemSpawner)

---

### **物资刷新管理器**

#### **创建物资刷新管理器**

在内容浏览器中，`右键 -> 蓝图` 搜索 `BP_UGCItemSpawner` ，以 `物品刷新管理器` 为父类创建一个蓝图，如图所示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AUUxMimage.png)

创建完成后，将物资刷新管理器放置到地图中的任意位置。

#### **配置物资刷新管理器**

在关卡界面中选中物资刷新管理器，查看细节面板，配置属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LChzuimage.png)

**配置详情**

   * **物资刷新启动方式**：

     * **关卡加载**：管理器会在关卡加载后自动开始刷新物资。
     * **事件触发**：通过事件触发启动刷新，事件名由开发者在脚本中设置。
     * **手动调用**：开发者可以在脚本中手动调用 **StartSpawnerManager()** 接口来启动刷新。
   * **刷新点生效数量**：设置同时生效的刷新点数量，系统会从配置的点中随机选择刷新点。
   * **刷新间隔**：物资被拾取后，需要等待多长时间才会刷新。
   * **总刷新次数**：定义物资刷新的总次数。当设置为 **-1** 时，物资将会无限刷新。
   * **刷新点**：在场景中需使用该管理器管理的物资刷新点。

**刷新点**

场景中需要使用管理器统一管理的刷新点，可在此处配置，如下所示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MK3HYimage.png)

点击刷新点配置右侧的 `➕` 键，即可增加一个刷新点配置，每个刷新点配置需要开发者选择一个场景中的 `物资刷新点Actor` 作为配置对象。 

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YzcqFimage.png)

选择之后，开发者需确定是否勾选 `覆盖刷新点物资配置` ，此处决定刷新点是否使用管理器的配置，开启后还需将刷新点的 `是否需要管理器` 一并开启。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Nh1Pnimage.png)

**物资刷新启动方式**

物资刷新启动方式除了使用 `关卡加载` 自动启动外，还可使用 `事件触发` 与 `手动调用` 两种方式手动启用。

**事件触发**

在关卡中选中 `物资刷新管理器Actor` ，将物资刷新启动方式修改为 `事件触发` ，事件名为开发者自定义，此处作为示例，配置为：TestSpawn，如下所示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PreTMimage.png)

使用 [**GMP系统**](http://) 注册此事件名，打开 `物资刷新管理器` 蓝图，并进入 `Lua脚本` ，注册事件。

``` lua
function NewPointManager:ReceiveBeginPlay()
    NewPointManager.SuperClass.ReceiveBeginPlay(self)

    local Message = self.EventName
    local registeredMsg = UGCGenericMessageSystem.RegisterUserDefinedMessage(Message)
end
```

其中，`NewPointManager` 为物资刷新管理器蓝图，`EventName` 参数即为关卡实例中配置的事件名 `TestSpawn` ，用此事件名注册事件。

``` lua
function UGCPlayerController:TestRpc()
    local manangerClass = UE.LoadClass(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/NewPointManager.NewPointManager_C'))
    local allManager = GameplayStatics.GetAllActorsOfClass(self, manangerClass)
    if allManager and allManager[1] then
        UGCGenericMessageSystem.BroadcastUserDefinedObjectMessage(allManager[1], allManager[1].EventName)
    end
end
```

如上所示，使用 [**GMP系统**](http://) 启用该事件，激活物资刷新管理器，调试游戏，如下所示。

![20250610_183017-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0rjZn20250610_183017-ezgif.com-video-to-gif-converter.gif)

**手动触发**

除了使用自定义事件触发开启物资刷新，还可以直接调用 `物资刷新管理器` 类自身方法。

``` lua
function UGCPlayerController:TestRpc()
    local manangerClass = UE.LoadClass(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/NewPointManager.NewPointManager_C'))
    local allManager = GameplayStatics.GetAllActorsOfClass(self, manangerClass)
    if allManager and allManager[1] then
        allManager[1]:StartSpawnerManager()
    end
end
```

如上所示， [**StartSpawnerManager**](https://developer.gp.qq.com/api/#/searchContent/AUGCItemSpawnerManager?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FAUGCItemSpawnerManager.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCItemSpawnerManager&autoJump=StartSpawnerManager) 为 `物资刷新管理器` 自身开启物资刷新的方法。

>注：物资刷新管理器相关API可查询文档：[物资刷新管理器](https://developer.gp.qq.com/api/#/searchContent/AUGCItemSpawnerManager?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FAUGCItemSpawnerManager.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=AUGCItemSpawnerManager)



---


## 自定义投掷物

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 自定义投掷物

**涉及API:** `P_White_Smoke_02`, `Smoking`, `Spine`

# 自定义投掷物

物品编辑器内置了和平精英常用投掷物的实体蓝图模板，基于模板创建的投掷物实体提供更丰富的参数供开发者自定义修改，包括投掷基础属性、爆炸属性、不同投掷物的特性属性等等，实现自定义的投掷物效果。

<br>

## 创建投掷物实体蓝图

以创建燃烧瓶投掷物实体蓝图为例：

1. 从“投掷物模板”窗口中选择 ``燃烧瓶``，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``燃烧瓶`` 为模板创建”
2. 点击“以 ``燃烧瓶`` 为模板创建” 按钮，弹出输入名称弹窗，输入投掷物名称并点击确定
3. 新建的投掷物将添加至“工程物品资源”窗口中，且投掷物实体蓝图创建于 ``Asset/Blueprint/Prefabs/Throwables`` 路径下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xjGq3image.png)

<br>

## 修改投掷物属性

### 基础属性

投掷物基础属性包含初始速度、重力系数、命中的各类行为、伤害类型等属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zbOZPimage.png)

|属性名|属性说明|
|-|-|
|穿透次数|忽略碰撞的目标角色可被穿透的次数|
|击中Pawn生成的特效|击中角色对象时生成的特效资源，生成位置默认为角色的 ``Spine`` 骨骼|
|击中声效|击中角色对象时播放的音效资源|
|启用特效缩放|是否启用击中特效的缩放设置|
|击中特效大小缩放|当启用击中特效缩放时，缩放的比例|
|击中特效跟随击中物体|击中生成的特效是否跟随角色对象移动|
|击中添加的BuffClass|击中角色对象时添加的 [Buff蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20087)|
|击中生成的Actor|针对投掷物与地面的碰撞，是否在击中点生成指定Actor对象（注意：投掷物落地产生弹射时，每次弹射都会触发生成）|
|碰撞忽略的阵营|忽略指定 [阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%98%B5%E8%90%A5%E7%B3%BB%E7%BB%9F) 的碰撞，忽略后对象可被穿透|
|初始速度|投掷物的初始发射速度|
|重力系数|投掷物的重力加速度系数，如果设置为<=-1，则会向上抛射|
|伤害数值|对击中对象造成的伤害值，支持常数或者基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式|
|伤害类型Tag列表|支持为伤害添加Tag，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 创建|

---

### 爆炸属性

投掷物爆炸属性支持爆炸触发的方式、爆炸伤害、爆炸范围和特效等属性的配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JQc7iimage.png)

|属性名|属性说明|
|-|-|
|爆炸触发方式|- 不发生爆炸：碰撞后立即销毁（击中效果依然生效），没有爆炸效果<br>- 命中立即发生爆炸：碰撞后立即触发爆炸<br>- 停止后开始计时延迟爆炸：投掷物运动停止后，延迟指定时间爆炸<br>- 弹射后开始计时延迟爆炸：投掷物第一次发生弹射时，开始计时并延迟指定时间爆炸<br>- 命中Pawn后开始计时延迟爆炸：击中角色对象时，开始计时并延迟指定时间爆炸<br>- 自定义计时延迟爆炸：即拉栓倒计时，触发拉栓时开始计时并延迟指定时间爆炸|
|爆炸延迟计时|当 ``爆炸触发方式`` 选为延迟爆炸类型时生效，指定需要延迟的时间|
|爆炸伤害|爆炸产生的伤害值，支持常数或者基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式|
|爆炸添加的BuffClass|爆炸时额外添加的 [Buff蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20087)|
|爆炸半径|爆炸的圆形范围，该范围内的角色对象都会受到定值伤害|
|爆炸筛选器|支持 [过滤器](https://developer.gp.qq.com/wikieditor/#/catalog/20218) 的方式筛选允许受到伤害的对象|
|爆炸特效|发生爆炸时生成的特效资源|
|启用自定义爆炸特效缩放|是否启用爆炸特效的缩放设置|
|爆炸特效缩放|当启用爆炸特效缩放时，缩放的比例|
|爆炸音效|爆炸时播放的音效资源|
|爆炸后是否立即销毁|爆炸后是否直接销毁该投掷物，如果不勾选默认10秒后销毁|

---

### 弹跳属性

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EB878image.png)

- Bounce Sound：投掷物发生弹射时播放的音效资源

---

### 特性属性

除了投掷物的通用属性，不同类型投掷物还具备独有的特性属性，例如燃烧瓶有燃烧伤害和燃烧持续时间等属性，震爆弹有白屏持续时间等，这部分特性属性也提供给开发者自定义。

#### 震爆弹

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZPzakimage.png)

|属性名|属性说明|
|-|-|
|作用范围|指定范围内的角色对象都会受到白屏影响|
|白屏持续时间|白屏效果持续的时长|
|是否需要对友方生效|友方是否会受到白屏的影响|

#### 烟雾弹

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4JOnkimage.png)

|属性名|属性说明|
|-|-|
|Smoking Sound|烟雾弹喷射烟雾时的音效资源|
|Explode Ak Event|烟雾弹的爆炸音效资源|

烟雾弹实体蓝图的名为 ``Smoking`` 的粒子组件支持替换烟雾粒子特效，修改粒子模板即可实现自定义的烟雾效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sicNlimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9bMvzimage.png)

烟雾弹实体蓝图的名为 ``P_White_Smoke_02`` 的粒子组件支持替换投掷尾迹的特效，修改粒子模板即可实现自定义的尾迹效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ksPKcimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PfvuEimage.png)

#### 燃烧瓶

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aLGhaimage.png)

|属性名|属性说明|
|-|-|
|作用范围|燃烧瓶爆炸后产生的燃烧范围|
|火焰持续时间|火焰特效的持续时间|
|燃烧持续时间|被火焰附着燃烧的持续时间|
|燃烧伤害间隔|燃烧伤害的结算周期|
|燃烧伤害|每次燃烧结算的伤害值|
|是否需要对友方生效|友方是否会受到火焰燃烧的影响|

<br>

## 绑定投掷物物品

投掷物实体蓝图无法直接进入背包或者实例化为可拾取物，需要绑定投掷物物品才有效，通过物品编辑器 [创建投掷物物品](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=%E6%96%B0%E5%BB%BA%E7%89%A9%E5%93%81%E8%93%9D%E5%9B%BE)，将 ``投掷物`` 属性设置为该实体蓝图，即得到一个自定义的投掷物。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/l7Lk8image.png)


---


## 自定义近战武器

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 自定义近战武器

# 自定义近战武器

物品编辑器内置了和平精英常用近战武器的实体蓝图模板，基于模板创建的近战武器实体支持部分通用属性的修改及技能的赋予。

> 目前版本下近战武器不具备可投掷状态，仅保留了近战攻击特性

<br>

## 创建近战武器实体蓝图

以创建平底锅实体蓝图为例：

1. 从“近战武器模板”窗口中选择 ``平底锅``，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``平底锅`` 为模板创建”
2. 点击“以 ``平底锅`` 为模板创建” 按钮，弹出输入名称弹窗，输入近战武器名称并点击确定
3. 新建的近战武器将添加至“工程物品资源”窗口中，且近战武器实体蓝图创建于 ``Asset/Blueprint/Prefabs/MeleeWeapons`` 路径下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ptHlIimage.png)

<br>

## 修改近战武器属性

### 投掷属性

当玩家装备近战武器后，和平精英默认的 ``开火按钮`` 将替换为近战武器的攻击按钮，当前投掷属性仅支持该攻击按钮按下与抬起的icon样式设置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tuPvsimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/h7EKximage.png)

---

### 技能配置

和平精英近战武器的攻击行为通过技能实现，因此实体蓝图需要关联指定的技能蓝图才具备近战攻击能力，且支持为近战武器挂载多种不同的技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5Btcrimage.png)

- 技能类：通过 [技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091) 创建的技能，默认配置了基于 [近战攻击Task](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E8%BF%91%E6%88%98%E6%94%BB%E5%87%BB) 实现的经典近战技能模板
- 技能赋予条件：何时为角色添加技能
	- 武器装备激活：当玩家手持该枪械时添加
	- 武器使用激活：当玩家装配该枪械时添加
	- 不自动激活：开发者自行实现添加技能的逻辑
- 绑定开火按键：该技能是否通过和平精英默认的 ``开火按钮`` 触发，如果不勾选则通过配置的技能UI槽外显；若多个技能同时绑定，则按配置先后顺序覆盖生效，建议保证有一个技能绑定开火按钮
- 技能生效时间：以 ``技能赋予条件`` 的时间点开始的有效时长，超过生效时间会自动卸载技能，-1为永久生效

<br>

## 绑定近战武器物品

近战武器实体蓝图无法直接进入背包或者实例化为可拾取物，需要绑定近战武器物品才有效，通过物品编辑器 [创建近战武器物品](https://developer.gp.qq.com/wikieditor/#/catalog/20101?autoJump=%E6%96%B0%E5%BB%BA%E7%89%A9%E5%93%81%E8%93%9D%E5%9B%BE)，将 ``Weapon Class`` 属性设置为该实体蓝图，即得到一把自定义的全新近战武器。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jHJ0aimage.png)


---


## 物品与背包槽位

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 物品与背包槽位

**涉及API:** `EquipmentSlot`, `GetEquipSlotEnable`, `Lock`, `SetEquipSlotEnable`

# 物品与背包槽位

槽位是为物品赋予额外外观或者功能性的逻辑虚拟容器，通过独立的UI元素表现与物品之间的交互方式，通常槽位可用于扩展物品的附属物件，例如配件、专属宝石、符文等，物品编辑器为多种类型的物品与背包都提供了槽位的配置能力，且支持槽位的锁定与解锁功能。

<br>

## 物品槽位

部分类型物品模板于【V2背包配置】属性类目中提供了槽位的配置项，允许为该物品定义可装配的配件/附属物槽位。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/L4awZimage.png)

|属性名|属性说明|
|-|-|
|Slot Name|基于 [GameplayTag](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20102) 定义的槽位名，必须为 ``EquipmentSlot`` 下的子级Tag|
|Display Name|槽位的名称，显示在槽位中的文本|
|Allow Types|允许装配的物品类型，对应物品的 ``自定义类型`` 属性，与 ``Allow Tags`` 为或的关系|
|Allow Tags|允许装配带有指定标签的物品，对应物品的 ``物品标记`` 属性，与 ``Allow Types`` 为或的关系|
|默认启用|该槽位是否默认可用，若不勾选则可设置锁定或者隐藏状态，详细见 [槽位锁定与解锁](https://developer.gp.qq.com/wikieditor/#/catalog/20210?autoJump=%E6%A7%BD%E4%BD%8D%E9%94%81%E5%AE%9A%E4%B8%8E%E8%A7%A3%E9%94%81) 部分内容|

> 特别注意，如果 ``Allow Types`` 和 ``Allow Tags`` 都留空，代表允许装配任意物品，可能出现枪械作为头盔配件而装备上的效果

当槽位装配了匹配的配件时，将在物品的详情面板的下方扩展显示槽位及该配件的信息。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OJVe5image.png)

同时背包中物品的右上角会显示槽位的装配状态，装配了配件的槽位将显示蓝色。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7LlF0image.png)

目前支持添加槽位的物品类型如下：

|物品类型|是否支持槽位|
|:-:|:-:|
|枪械物品|✔|
|配件物品|✔|
|子弹物品|✖|
|装备物品|✔|
|投掷物品|✔|
|药品物品|✖|
|穿戴装备物品|✔|
|近战武器物品|✔|

<br>

**枪械物品槽位**

枪械物品槽位的显示规则与其他类型物品略有不同，枪械物品模板依据和平精英的枪械特性预设了6种配件槽位Tag，各槽位在装备栏的显示位置固定，而在背包详情面板的显示位置取决于槽位的配置顺序。

|槽位Tag|槽位说明|
|:-:|:-:|
|EquipmentSlot.Core.AngledOpticalSight|侧边瞄准镜槽位|
|EquipmentSlot.Core.Grip|握把槽位|
|EquipmentSlot.Core.GunPoint|枪口槽位|
|EquipmentSlot.Core.GunStock|枪托槽位|
|EquipmentSlot.Core.Magazine|弹匣槽位|
|EquipmentSlot.Core.OpticalSight|瞄准镜槽位|

装备栏只显示6种预设范围内的槽位，自定义的槽位Tag仅装配了配件才额外显示在详情面板中；否则，不显示空槽位。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0dPnWimage.png)

背包中的物品详情页会按照槽位的配置顺序依序显示各槽位及装配状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dqFZQimage.png)

<br>

## 背包槽位

不同于物品槽位的附属物概念，背包的槽位主要用于 [扩展装备栏](https://developer.gp.qq.com/wikieditor/#/catalog/20137?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A3%85%E5%A4%87%E6%A0%8F)，即为物品的装配提供容器空间。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/r94DYimage.png)

当前背包预设了7种槽位，涵盖和平精英的各类枪械武器、头包甲装备及近战武器的装配空间。

|槽位Tag|槽位说明|
|:-:|:-:|
|EquipmentSlot.Core.MainSlot1|主武器一|
|EquipmentSlot.Core.MainSlot2|主武器二|
|EquipmentSlot.AvataEquipmentSlot.AvatarHelmet|头盔|
|EquipmentSlot.AvataEquipmentSlot.AvatarBag|背包|
|EquipmentSlot.AvataEquipmentSlot.AvatarArmor|护甲|
|EquipmentSlot.Core.SubSlot|手枪|
|EquipmentSlot.Core.MeleeSlot|近战武器|

<br>

## 槽位锁定与解锁

物品与背包的槽位均支持锁定和解锁的功能，在槽位配置中通过取消 ``默认启用`` 属性以对默认的槽位状态进行设置。

**槽位锁定**

物品槽位的锁定配置：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1c8W4image.png)

背包槽位的锁定配置：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/e8wCgimage.png)

- 不启用显示：槽位的默认状态
	- Lock：锁定状态，需要主动触发解锁
	- Hidden：隐藏状态，需要主动触发显示
- 点锁提示：当 ``不启用显示`` 选为 ``Lock`` 时生效，可配置锁定状态下点击的提示tips

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Ccywfimage.png)

<br>

**槽位解锁**

槽位的解锁需要通过脚本侧调用相应的API实现，其中物品槽位的解锁调用 [``SetEquipSlotEnable``](https://developer.gp.qq.com/api/#/searchContent/UGCItemSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCItemSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCItemSystemV2&autoJump=SetEquipSlotEnable)，背包槽位的解锁调用 [``SetEquipSlotEnable``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=SetEquipSlotEnable)。

> API仅支持解锁槽位，锁定状态为蓝图配置下的初始状态，不支持动态锁定

![QQ2025827-201148-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/F09OKQQ2025827-201148-HD-ezgif.com-video-to-gif-converter.gif)

<br>

## API参考

|函数库/类名|函数类型|函数功能范围|
|-|-|-|
|[``SetEquipSlotEnable``](https://developer.gp.qq.com/api/#/searchContent/UGCItemSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCItemSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCItemSystemV2&autoJump=SetEquipSlotEnable)|静态函数|解锁物品槽位|
|[``GetEquipSlotEnable``](https://developer.gp.qq.com/api/#/searchContent/UGCItemSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCItemSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCItemSystemV2&autoJump=GetEquipSlotEnable)|静态函数|查询物品槽位状态|
|[``SetEquipSlotEnable``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=SetEquipSlotEnable)|静态函数|解锁背包槽位|
|[``GetEquipSlotEnable``](https://developer.gp.qq.com/api/#/searchContent/UGCBackpackSystemV2?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E7%89%A9%E5%93%81%E4%B8%8E%E8%83%8C%E5%8C%85%2FUGCBackpackSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCBackpackSystemV2&autoJump=GetEquipSlotEnable)|静态函数|查询背包槽位状态|
		









---


## 自定义物品模型

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器2.0 > 自定义物品模型

**涉及API:** `Root`, `WeaponSocket_01`

# 自定义物品模型
物品编辑器提供了给自定义物品更换模型的功能，开发者能够自定义修改自己创作的物品模型，其中包括枪械模型、近战武器模型、投掷物模型以及穿戴装备模型，枪械模型更加细化，枪械配件模型也可供开发者自定义修改，实现个性化的显示效果。

<br>

## 物品模型概念
物品模型包括拾取物模型、手持模型和投掷物模型。

**拾取物模型**

拾取物指的是玩家在游戏场景中可拾取的物品，比如放置在场景中的枪械、枪械配件、子弹、投掷物、药品、近战武器、穿戴装备等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Par3Himage.png)

打开物品编辑器，创建一个物品Handle，在右侧细节面板中可以对 "拾取物模型" 进行配置：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vPdupimage.png)

**手持模型**

手持模型指的是装备在玩家手中的物品模型，其中包括枪械、近战武器、药品、投掷物。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0yUi9image.png) ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vccetimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GVdegimage.png) ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LNJnOimage.png)

不同类型的物品配置方法略有不同，详情配置可以看后面的内容。

**投掷物模型**

投掷物模型指的是投掷物在被投掷状态下显示的模型，详情配置可以跳转到自定义投掷物模型。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AVy8Qimage.png)

<br>

## 自定义枪械模型

### 模型配置说明

推荐使用静态模型进行枪械自定义外观，建模时可以选择将枪械配件都做到一个整体的模型上，角色持枪时，将会显示一把完整的枪械：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/N8ZRrimage.png)

也可以对枪械按照配件部位分开建模，以便枪械模型配置时可以自定义搭配配件使用，并且能够自适应枪械相关的动画：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ie3Uhimage.png)

**注意事项**

1. 枪械模型的 <font color="red">`Root`</font> 位置会直接挂接到角色的 <font color="red">`WeaponSocket_01`</font> 上，因此建议在建模的时候，将 <font color="red">`Root`</font> 位置调整到角色手持的位置

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kfcp5image.png)

2. 模型的单位默认使用厘米，需要在DCC软件中，改成对应的单位
3. 枪口需要朝向X轴正前方

---

### Socket配置规范

通过Socket配置能够使枪械的配件正确的显示与生效，开发者想要枪械配件能够正确显示，这一步必不可少。

**Socket规范图表**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GwKQIimage.png)

|配件挂点|Socket名称|备注|是否支持更换模型|
|-|-|-|-|
|枪口配件槽位挂点|Muzzle|/|支持|
|握把配件槽位挂点|Grip|/|支持|
|弹匣配件槽位挂点|Mag|/|支持|
|枪托配件槽位挂点|Gunstock|/|支持|
|瞄准镜配件槽位挂点|Upper_Small|装备瞄准镜时的槽位|不支持|
|枪口火焰挂点|MuzzleEffect|开火时，枪口火焰特效挂接的槽位|/|
|默认机瞄挂点|ScopeAimCamera|默认的没有装备瞄准镜时，相机瞄准的槽位|/|
|弹药特效挂点|Shell_Socket|抛弹壳，子弹弹出特效的槽位|/|

**Socket配置过程**

在实现枪械能够搭配自定义配件使用之前，需要对自定义枪械模型进行Socket配置：

双击打开导入的枪械本体模型，进入模型编辑器：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mXo08image.png)

**Socket配置步骤：**
- 在右下角插槽管理器面板点击【创建插槽】，添加槽位，创建开发者这把自定义枪械需要的配件部位
- 根据上述Socket配置规范图表，对对应的槽位进行正确的命名（命名必须与规范中Socket名称一致，否则配件显示无法生效）
- 绑定合适的配件静态mesh
- 调整槽位偏移到合适的位置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6Y9Gbimage.png)

---

### 枪械模型配置

打开物品编辑器，在枪械中创建一把枪械对象，如：M416，勾选 "是否使用自定义换皮模型"。

在枪身模型上，替换成刚才Socket配置好的枪械模型，可以在窗口中预览：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uRgUwimage.png)

运行游戏，添加对应物品，就能获取到这把自定义模型的枪械：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/O1o7Kimage.png)

如果想要这个枪械带有默认的配件显示，在默认模型配置点击【 + 】添加需要显示的配件模型（注意，这里添加的配件模型只作预览显示）
这里给自定义枪械添加了默认的枪托和弹匣的显示模型：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BQpDximage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6DLp0image.png)

> 当添加了 "枪口配件位" 之后，想要再添加配件，就会出现上图所示情况。如果开发者想要配置枪口配件模型，建议把枪口配件留到最后配置

运行游戏，添加对应物品，就能获取到这把有默认配件显示的枪械：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TQ6Yaimage.png)

> 配置完如果不生效需要先检查一下前面的Socket配置是否正确

另外，枪械还支持修改模型的相对偏移，通过物品编辑器创建的枪械物品蓝图上，找到 "UGCBackPack Weapon Handle" 中的 ``装备模型相对偏移`` 属性，修改后收起和手持状态的相应物品模型都会发生偏移。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gsZkrimage.png)

>注意：枪械物品目前不支持修改位置偏移属性

修改后效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ghjc4image.png) ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/K4mzLimage.png)

---

### 配件模型配置

开发者希望自己自定义的枪械配件能够在枪械本体上自由拆卸和装备。物品编辑器提供了空白配件模板，支持更换配件模型。

创建一个空白配件，在模型配置中选择导入的配件模型，配置 "物品标记(Tag)"，如枪口：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tboDhimage.png)

这里的配件Tag配置是枪械槽位的绑定逻辑，详情见 [物品与背包槽位](https://developer.gp.qq.com/wikieditor/#/catalog/20210)

> - 由于瞄准镜有特殊的开镜材质，暂时不支持自定义外显模型
> - 开发者需要根据枪械物品上的槽位，配置配件的物品Tag，否则，该配件不能装配到枪械对应的配件槽位上

运行游戏，添加枪械物品和枪口配件物品，装备枪口配件，就可以看到自定义的配件装配到枪械上了：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0hdFyimage.png)

把枪口卸下的效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9sh9nimage.png)

<br>

## 自定义近战武器模型

同理，在近战武器类别中，也可以通过直接替换模型，达到修改近战武器模型的效果，比如这里把大砍刀模型替换成荧光棒：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/toQcMimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LXgOCimage.png)

近战武器也支持修改模型的相对偏移，通过物品编辑器创建的近战物品蓝图上，找到 "UGCBackPack Weapon Handle" 中的 ``装备模型相对偏移`` 属性，修改后收起和手持状态的相应物品模型都会发生偏移。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UMXeIimage.png)

修改后效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FzJkpimage.png) ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XrTfCimage.png)

<br>

## 自定义投掷物模型

投掷物的表现主要包括手持和投掷出的对象，如果想要创建自定义的投掷物，需要先创建一个投掷物的Handle，在静态模型上，配置想要的效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZAf5Fimage.png)

接下来，需要创建一个投掷物，并将静态模型更换成想要的模型：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/thyJmimage.png)

之后，将投掷物和物品handle关联：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qFvxsimage.png)

效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zK6b1image.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UDj0pimage.png)

<br>

## 自定义穿戴装备模型

在穿戴装备物品中（头、包、甲），我们也提供了自定义穿戴装备模型：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qLor6image.png)

在自定义穿戴装备模型中，开发者可以通过勾选 "支持模型编辑" 来配置开发者自己的模型：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ymIcIimage.png)

属性配置说明：

|属性|说明|
|-|-|
|**模型位置偏移**|头、包、甲挂接到对应槽位之后的偏移量|
|**强制显示**|勾选此选项之后，在大厅勾选隐藏头盔、背包之后，会再次在游戏中显示|
|**装备等级**|对应左下角装备等级的图标<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qljkmimage.png)|

效果：

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;自定义熊猫头头盔&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;自定义小熊背包&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;自定义水桶防弹衣
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TjlxQimage.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1pbJBimage.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/97nQzimage.png)

<br>

## 枪械换皮示例

**示例：M416换皮AK47**

先从物资编辑器创建一个UGC M416枪械Weapon：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vX1zaimage.png)

切换到物品再创建一个对应的物品Handle：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WMBL3image.png)

绑定物品和武器的关系：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FU4UWimage.png)

回到M416 枪械Weapon 物品蓝图，选中Actor和【类默认值】，找到细节面板中 "UGCConfig" 下的 "模型换皮" 一栏勾选 "是否使用自定义换皮模型"：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XpLjfimage.png)

先选择一个枪身模型，这里选择了AK47：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mjsreimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jxkhqimage.png)

再在默认模型配置中点击【 + 】新增一项，然后选择 "弹匣配件位"，选择AK47突击步枪模型，就可以在预览窗口里看到携带了默认弹匣的AK47模型：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2LEFGimage.png)

游戏运行时添加配置的武器对应的物品，可以看到效果，换皮成功：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cL6Ziimage.png)

---
