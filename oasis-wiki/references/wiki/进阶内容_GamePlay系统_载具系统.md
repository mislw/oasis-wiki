# 进阶内容/GamePlay系统/载具系统

> 本分类共 3 篇文章

---


## 普通载具

> 文档路径: 进阶内容 > GamePlay系统 > 载具系统 > 普通载具

**涉及API:** `AlwaysSpawn`, `Arts_PlayerBluePrints`, `KismetMathLibrary.MakeRotator`, `ScriptGameplayStatics.SpawnActor`, `SpawnActor`, `UE.LoadClass`, `Vector.New`, `VehicleCommon`, `VehicleMovement4W`

#  普通载具

绿洲启元编辑器提供了一个功能强大且种类丰富的载具系统，覆盖了陆、海、空三大领域，能够满足各种复杂的游戏玩法需求，开发者可以根据需要灵活调整载具的速度、血量等关键参数，提升载具的可玩性和游戏乐趣。

> 该文档为旧载具蓝图操作指南，目前已统一迁移至 [载具编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20245)，请参考新文档创建载具蓝图

<br>

## 使用载具

在载具资源目录内，可以直接拖动载具蓝图到关卡内使用。

![企业微信截图_16868126838118.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868126838118.png)

也可以通过 ``SpawnActor`` 的方式动态生成载具实例至关卡内：

```lua
-- 加载指定载具的蓝图类
local DaciaCarClass = UE.LoadClass('/Game/Arts_PlayerBluePrints/Vehicle/Dacia/VH_Dacia_New.VH_Dacia_New_C');

-- 将载具生成至指定位置
local carActor = ScriptGameplayStatics.SpawnActor(self, DaciaCarClass, Vector.New(22040, 30400, 100), KismetMathLibrary.MakeRotator(0, 0, 70), { X = 1, Y = 1, Z = 1 }, nil, ESpawnActorCollisionHandlingMethod.AlwaysSpawn)
```

<br>

## 修改载具属性

如果希望调整载具的相关参数设置，需要基于目标载具创建子蓝图类，在子蓝图上进行修改与设置。

### 创建载具子蓝图 

在内容浏览器内右键“蓝图类”创建新蓝图，选择需要继承的载具父类。

![企业微信截图_16868126979405.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868126979405.png)

创建出的载具子蓝图可以修改蓝图属性及子组件属性：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wbQYLimage.png)

### 属性修改

**载具基础属性**

在组件栏中找到 ```VehicleCommon``` 组件，可以设置载具的基础属性：
- 修改载具血量上限：VehicleCommon-HpMax
- 修改轮胎血量：VehicleCommon-WheelsHp
- 修改油量：VehicleCommon-FuelMax
- 修改油耗：VehicleCommon-Fuel Consume Factor

![企业微信截图_1686812711902.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686812711902.png)

**载具速度**

车辆行驶速度在 ```VehicleMovement4W``` 组件上进行调整，载具的行驶参数主要通过扭力和RMP来控制：
- 扭力参数：Engin Setup 通过调整曲线参数控制扭力大小
- RMP：Max RPM 直接修改最大RMP数值大小

![企业微信截图_16868127204339.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868127204339.png)

车辆加速组件可以通过检索“载具加速带”来查找，可在工程内继承并创建新的蓝图来修改加速参数：
- 加速比率：Accelerate Percent

![企业微信截图_16868151732829.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868151732829.png)


---


## 载具编辑器

> 文档路径: 进阶内容 > GamePlay系统 > 载具系统 > 载具编辑器

**涉及API:** `BP_UGCVehicleRefresher_Base`, `ExplosionBaseDamage`, `ExplosionMinimumDamage`, `SetBoosting`, `SpawnVehicle`, `UGCVehicleSystemV2`, `UGCWheeledVehicleComponent`

# 载具编辑器

载具编辑器将和平精英常用的包含陆地载具、水上载具和武装载具模板化，简化了载具繁杂的属性配置方式，开发者可基于模板创建载具实体，修改载具的各项属性以调整载具的性能，也支持为载具添加武器构建具备战斗能力的攻击型载具。

<br>

## 载具概述

载具是具有物理模拟特性的可交互实体对象，依据应用场景的不同分为陆地载具、水上载具与飞行载具，载具编辑器将各类型载具拆解为载具模型、基础属性、动力组件和座椅组件的组合：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IOgESimage.png)

以下将以陆地载具为代表的轮式载具进行讲解，说明如何创建载具及调整载具的各项功能属性。

<br>

## 编辑器界面

点击编辑器菜单栏的【实体编辑器】按钮，打开实体编辑器的操作界面，点击【载具】页签切换至载具编辑器工作界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qjWWKimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/47V6oimage.png)

**A. 工程载具资源**

工程内通过载具编辑器创建的所有载具蓝图将显示在该资源列表中

**B. 载具模板**

预置的陆地载具/水上载具/武装载具模板，基于模板创建对应类型的载具实体蓝图

**C. 载具预览窗口**

展示所创建载具的模型效果

**D. 载具属性面板**

载具蓝图的组件及各组件的可配置属性

<br>

## 载具模板

载具编辑器预置了三种载具模板：陆地载具、水上载具和武装载具，涵盖了和平精英常用的载具款式，其中武装载具是默认挂载了武器的陆地载具，开发者可为任意陆地载具添加武器使之成为武装载具。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/r6NYlimage.png)

<br>

## 载具创建流程

### 新建载具蓝图

开发者可以基于指定的载具模板创建载具蓝图，以创建防弹吉普车为例：

1. 从“载具模板”窗口中选择防弹吉普车模板，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``防弹吉普车`` 为模板创建”

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iDHP5image.png)

2. 点击“以 ``防弹吉普车`` 为模板创建” 按钮，弹出输入名称弹窗，输入载具蓝图名称并点击确定

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tTYZzimage.png)

3. 新建的防弹吉普车蓝图将显示在“工程载具资源”窗口中，且载具蓝图创建于 ``Asset/Blueprint/Prefabs/Vehicles`` 路径下

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8Cefyimage.png)

---

### 载具模型配置

基于模板创建的载具模型不可变更，但可以在动力组件下添加额外的网格体组件来扩展模型外观，建议配合动力组件下的 ``物理碰撞`` 属性添加合适的碰撞体，以确保物理碰撞效果符合预期。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/k41DQimage.png)

---

### 基础属性配置

载具编辑器为各类型的载具抽象了一批通用的基础属性，例如血量、油耗、爆炸伤害等，并通过固化属性的形式内置在属性管理器中，可基于 [属性系统](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7) 使用这部分属性。

> 载具各项基础属性的说明可参见 [载具属性对照表](https://developer.gp.qq.com/wikieditor/#/catalog/20246)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cVc6Dimage.png)

载具蓝图上挂载了 [属性修改组件](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%BB%84%E4%BB%B6)，如果希望修改载具的初始属性值，可通过该组件的 ``属性初始值配置`` 进行设置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GOb9zimage.png)

---

### 动力组件配置

轮式载具的移动效果受控于动力引擎、传动链、差速器、轮胎等多方面综合因素的影响，载具编辑器将这些动力系统的专业属性封装在 ``UGCWheeledVehicleComponent`` 组件中，在该组件的 ``物理配置`` 属性组下可对相关属性进行修改调整。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/b0goHimage.png)

#### 载具加速

``是否可加速`` 属性决定玩家乘坐载具时是否显示加速的UI控件，如果不启用该开关，也可以通过调用 [``SetBoosting``](https://developer.gp.qq.com/api/#/searchContent/UGCVehicleSystemV2?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCVehicleSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCVehicleSystemV2&autoJump=SetBoosting) 动态为载具加速。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OM3LDimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7XgiRimage.png)

#### 载具质量

载具质量是载具物理模拟计算的基准权重，影响线性加速度、转动惯量、碰撞冲量等多种物理模拟的结果，是决定载具操控手感的重要因素之一，通常质量越大转弯越稳、冲撞力更强。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8VjZximage.png)

#### 物理碰撞

载具默认的物理碰撞范围由骨骼网格体配置的物理资产决定，通常由多个及多种简单碰撞体组件拼接组成的物理刚体，是载具一切物理模拟的基础。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TXJHtimage.png)

除了匹配模型的物理资产，载具编辑器支持为载具添加额外的碰撞体，通过 ``额外的物理形状`` 属性可以添加多个球体/长方体/胶囊体等碰撞体组件，每种碰撞体可以设置大小和位置偏移等参数。

> 碰撞体组件的原点为 ``UGCWheeledVehicleComponent`` 组件的位置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZVkl4image.png)

#### 发动机系统

发动机是载具的核心动力引擎，决定了载具的最高速、加速能力等动力性能，载具编辑器提供了多种发动机数据资产模板供开发者直接配置使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NSTuRimage.png)

|资产模板名称|适用场景|
|-|-|
|VehicleEngineConfig_ExtremeFast|跑车发动机|
|VehicleEngineConfig_ExtremeLow|家用发动机|
|VehicleEngineConfig_Level1|214匹发动机|
|VehicleEngineConfig_Level2|235匹发动机|
|VehicleEngineConfig_Level3|277匹发动机|
|VehicleEngineConfig_Level4|320匹发动机|
|VehicleEngineConfig_Level5|363匹发动机|

如需自定义发动机的配置参数，可以启用 ``是否使用高级发动机配置`` 属性，此时面板将显示发动机系统的相关属性项。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cMV9ximage.png)

|属性名|属性说明|
|-|-|
|力矩曲线|基于 [曲线工具](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/curve-editor?application_version=4.27#%E6%9B%B2%E7%BA%BF%E7%BC%96%E8%BE%91) 的扭矩-转速曲线，控制不同转速下的输出扭矩，X轴代表转速，Y轴代表输出扭矩，每个坐标点代表一个档位<br>扭矩决定引擎的推力大小，影响载具移动的难易程度|
|发动机最大转速|发动机每分钟的最大转速，不代表载具的真实移动速度，转速配合齿轮比、差速器、终传比等参数才决定车速|
|转动惯量|影响载具灵活性和稳定性表现，惯量越大，转速变化和转向的响应更慢，反之亦然|
|离合器各级齿轮比|``力矩曲线`` 上各档位的相关配置<br>- Ratio：齿轮比，各档位扭矩和转速的比值，值越大，性能强劲但极速低；反之亦然<br>- Down Ratio：降档比例，决定降档的转速阈值，必须小于升档比例<br>- Up Ratio：升档比例，决定升档的转速阈值，需考虑换挡时间因素，避免升档后落入扭矩谷|
|终传比|变速箱输出到车轮的最终放大倍数，相当于把所有档位齿轮比同比例缩放，决定载具整体性能|
|使用自动变速器|勾选后速度达到临界值则会自动换挡；默认勾选，否则会永远停留在1档|
|换挡时间|手动切换档位需要的时长，该属性暂未启用|
|自动变速器启动换挡的最短时间|完成一次换挡需要的时长，时间越短，加速越平滑；反之，动力中断明显，顿挫感强|

#### 转向系统

转向系统影响载具的转向响应、角度和平稳度等性能，载具编辑器提供了多种转向数据资产模板供开发者直接配置使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MpKR0image.png)

|资产模板名称|适用场景|
|-|-|
|VehicleTurnConfig_Normal|常规版转向|
|VehicleTurnConfig_Speed|专业版转向|

如需自定义转向系统的配置参数，可以启用 ``是否使用高级转向系统配置`` 属性，此时面板将显示转向系统的相关属性项。

|属性名|属性说明|
|-|-|
|角速度阻尼|影响载具转弯的平稳度，值越小，转弯越容易打滑漂移|
|转向输入速率|- Rise Rate：方向盘拧满的速率，值越大越灵敏<br>- Fall Rate：方向盘松开的速率，值越大越灵敏|
|转弯角度限制曲线|基于 [曲线工具](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/curve-editor?application_version=4.27#%E6%9B%B2%E7%BA%BF%E7%BC%96%E8%BE%91) 的速度-转弯角度曲线，限制不同速度下安全转弯的最大角度，X轴代表车速，Y周代表转向角0～1系数|

#### 差速器

差速器通过给载具左右轮分配不同动力以调控左右轮的转速差，尤其适合调整转弯时的性能表现，载具编辑器目前提供了一种通用的差速器数据资产模板供开发者直接配置使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SpC1uimage.png)

|资产模板名称|适用场景|
|-|-|
|VehicleDifferentialConfig|万能差速器|

如需自定义差速器的配置参数，可以启用 ``是否使用高级差速器配置`` 属性，此时面板将显示差速器的相关属性项。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cxthpimage.png)

|属性名|属性说明|
|-|-|
|Differential Type|差速器的类型，分为限滑式与开放式两大类，开放式允许车轮转速差但易空转，限滑式在转速差大时自动锁止<br>- Limited Slip 4W：限滑四驱<br>- Limited Slip Front Drive：限滑前驱<br>- Limited Slip Rear Drive：限滑后驱<br>- Open 4W：开放式四驱<br>- Open Front Drive：开放式前驱<br>- Open Rear Drive：开放式后驱|
|Front Rear Split|中央差速器，前后轴静态扭矩分配比例，0→纯后驱，1→纯前驱，范围：0~1，仅针对 ``开放式四驱`` 生效|
|Front Left Right Split|前轴左右轮间的锁止倍率（焊死力度），值越大力度越强，范围：1~+∞，针对 ``开放式四驱`` 和 ``限滑前驱`` 生效|
|Rear Left Right Split|后轴左右轮间的锁止倍率（焊死力度），值越大力度越强，范围：1~+∞，针对 ``开放式四驱`` 和 ``限滑后驱`` 生效|
|Centre Bias|限滑差速器的动态锁止倍率，出现轴间转速差时，抓地轴可获得的扭矩倍数，范围：1~+∞，仅针对 ``限滑四驱`` 生效|
|Front Bias|限滑差速器前轴左右轮间的锁止倍率，范围：1~+∞，针对 ``限滑四驱`` 和 ``限滑前驱`` 生效|
|Rear Bias|限滑差速器后轴左右轮间的锁止倍率，范围：1~+∞，针对 ``限滑四驱`` 和 ``限滑后驱`` 生效|

#### 轮胎

载具编辑器支持为轮胎设置不同材质的摩擦系数，以及纵向/横向软硬度等属性，默认提供了多种轮胎数据资产模板供开发者直接配置使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AsVArimage.png)

|资产模板名称|适用场景|
|-|-|
|VehicleTireConfig_Drift|漂移轮胎|
|VehicleTireConfig_Normal|普通轮胎|
|VehicleTireConfig_Speed|竞赛轮胎|

如需自定义轮胎的配置参数，可以启用 ``是否使用高级轮胎配置`` 属性，此时面板将显示轮胎的相关属性项。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Gj2DBimage.png)

|属性名|属性说明|
|-|-|
|默认摩擦系数|决定轮胎与地面的抓地力大小，系数越大，抓地力越强|
|在不同材质地面上的摩擦系数|- 地面材质：当前提供了多种包含草地、金属、水面等物理材质<br>- 摩擦系数：轮胎在对应材质下的摩擦系数|
|纵向软硬度|决定轮胎在加速/制动时产生力的硬度，影响起步或刹车时达到摩擦力峰值的响应效率|
|横向软硬度|决定轮胎在转向/侧滑时产生力的硬度，影响转向或漂移的灵敏程度|

#### 其他参数

支持影响载具驾驶响应、制动力和阻力等属性的设置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/azoKTimage.png)

|属性名|属性说明|
|-|-|
|风阻系数|载具在行驶过程中的空气阻力系数大小，值越小高速行驶的稳定性越强|
|刹车力量系数|脚刹踏板触发对四轮的力量系数，值越大刹车距离越短|
|手刹力量系数|手刹按钮触发对后轮的力量系数，值越大刹车距离越短，适合漂移甩尾|
|油门输入速率|每秒把油门补满/回落的次数，范围：1~10<br>- Rise Rate：每秒油门0→1的补满次数<br>- Fall Rate：每秒油门1→0的回落次数|
|刹车输入速率|每秒脚刹踏板触发刹车/松刹的次数，范围：1~10<br>- Rise Rate：每秒刹车0→1的完成次数<br>- Fall Rate：每秒松刹1→0的回弹次数|
|手刹输入速率|每秒手刹按钮触发刹车/松刹的次数，范围：1~10<br>- Rise Rate：每秒刹车0→1的完成次数<br>- Fall Rate：每秒松刹1→0的回弹次数|

---

### 座椅组件配置

载具的座位数由座椅组件的数量决定，在载具蓝图中搜索“UGCVehicleSeat”并添加至 ``UGCWheeledVehicleComponent`` 动力组件下。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7jxodimage.png)

每一个座椅组件代表一个座位，载具座位遵循以下规则：
- 座椅组件的名称不可变更
- 座椅组件的顺序决定了司机位与乘客位，第一个组件代表司机位
- 最多支持8个座椅组件

座椅组件的配置数据涉及驾驶/乘坐动画、座位类型、上下载具挂载点、探头等功能，为了简化配置方式，载具编辑器提供了一批座椅数据资产模板供开发者直接配置使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BTpL7image.png)

|属性名|属性说明|
|-|-|
|使用自定义座位方案|如不勾选，使用载具默认的座椅配置数据，详见 ``载具座椅模板表``|
|座位模板选择|可使用 ``载具座椅模板表`` 中提供的任意资产模板|
|隐藏座位Mesh|是否隐藏座位模型，可实现悬空坐的效果|
|下车点偏移|下车的位置相对于座位位置的偏移量|
|激活的武器|座位是否能启用武器，取决于座位模板的配置|

**载具座椅模板表**

|载具名称|座椅类型|资产模板名称|
|-|-|-|
|全地形车|驾驶位|ATVDriverSeatConfig|
|全地形车|乘客位|ATVPassengerSeat01Config|
|大脚车|驾驶位|BigfootDriverSeatConfig|
|大脚车|副驾驶位|BigfootPassengerSeat01Config|
|大脚车|后排左侧位|BigfootPassengerSeat02Config|
|大脚车|后排右侧位|BigfootPassengerSeat03Config|
|布朗轿车|驾驶位|BlancDriverSeatConfig|
|布朗轿车|副驾驶位|BlancPassengerSeat01Config|
|布朗轿车|后排左侧位|BlancPassengerSeat02Config|
|布朗轿车|后排右侧位|BlancPassengerSeat03Config|
|沙滩车|驾驶位|BuggyDriverSeatConfig|
|沙滩车|后排特殊乘客位|BuggyPassengerSeat01Config|
|跑车|驾驶位|CoupeRBDriverSeatConfig|
|跑车|副驾驶位|CoupeRBPassengerSeat01Config|
|轿车|驾驶位|DaciaDriverSeatConfig|
|轿车|副驾驶位|DaciaPassengerSeat01Config|
|轿车|后排左侧位|DaciaPassengerSeat02Config|
|轿车|后排右侧位|DaciaPassengerSeat03Config|
|雪地车|驾驶位|LadaNivaDriverSeatConfig|
|雪地车|副驾驶位|LadaNivaPassengerSeat01Config
|雪地车|后排左侧位|LadaNivaPassengerSeat02Config|
|雪地车|后排右侧位|LadaNivaPassengerSeat03Config|
|迷你巴士|驾驶位|MiniBusDriverSeatConfig|
|迷你巴士|副驾驶位|MiniBusPassengerSeat01Config|
|迷你巴士|中排左侧位|MiniBusPassengerSeat02Config|
|迷你巴士|中排右侧位|MiniBusPassengerSeat03Config|
|迷你巴士|后排左侧位|MiniBusPassengerSeat04Config|
|迷你巴士|后排右侧位|MiniBusPassengerSeat05Config|
|四座跑车|驾驶位|MiradoCloseDriverSeatConfig|
|四座跑车|副驾驶位|MiradoClosePassengerSeat01Config|
|四座跑车|后排左侧位|MiradoClosePassengerSeat02Config|
|四座跑车|后排右侧位|MiradoClosePassengerSeat03Config|
|敞篷四座跑车|驾驶位|MiradoOpenDriverSeatConfig|
|敞篷四座跑车|副驾驶位|MiradoOpenPassengerSeat01Config|
|敞篷四座跑车|后排左侧位|MiradoOpenPassengerSeat02Config|
|敞篷四座跑车|后排右侧位|MiradoOpenPassengerSeat03Config|
|三人摩托车|驾驶位|MotorcycleCarDriverSeatConfig|
|三人摩托车|后排乘客位|MotorcycleCarPassengerSeat01Config|
|三人摩托车|右侧单座乘客位|MotorcycleCarPassengerSeat02Config|
|双人摩托车|驾驶位|MotorcycleDriverSeatConfig|
|双人摩托车|后排乘客位|MotorcyclePassengerSeat01Config|
|无篷皮卡|驾驶位|PickUpWDriverSeatConfig|
|无篷皮卡|副驾驶位|PickUpWPassengerSeat01Config|
|无篷皮卡|后排左侧位|PickUpWPassengerSeat02Config|
|无篷皮卡|后排右侧位|PickUpWPassengerSeat03Config|
|有篷皮卡|驾驶位|PickupYDriverSeatConfig|
|有篷皮卡|副驾驶位|PickupYPassengerSeat01Config|
|有篷皮卡|后排左侧位|PickupYPassengerSeat02Config|
|有篷皮卡|后排右侧位|PickupYPassengerSeat03Config|
|电动巴士|驾驶位|PicoBusDriverSeatConfig|
|电动巴士|副驾驶位|PicoBusPassengerSeat01Config|
|电动巴士|中排左侧位|PicoBusPassengerSeat02Config|
|电动巴士|中排右侧位|PicoBusPassengerSeat03Config|
|电动巴士|后排左侧位|PicoBusPassengerSeat04Config|
|电动巴士|后排右侧位|PicoBusPassengerSeat05Config|
|尼罗皮卡|驾驶位|RonyDriverSeatConfig|
|尼罗皮卡|副驾驶位|RonyPassengerSeat01Config|
|尼罗皮卡|后排左侧位|RonyPassengerSeat02Config|
|尼罗皮卡|后排右侧位|RonyPassengerSeat03Config|
|小型摩托车|驾驶位|ScooterDriverSeatConfig|
|小型摩托车|后排乘客位|ScooterPassengerSeat01Config|
|轻型雪地摩托车|驾驶位|SnowbikeDriverSeatConfig|
|轻型雪地摩托车|后排乘客位|SnowbikePassengerSeat01Config|
|雨林三轮车|驾驶位|TukDriverSeatConfig|
|雨林三轮车|后排左侧位|TukPassengerSeat01Config|
|雨林三轮车|后排右侧位|TukPassengerSeat02Config|
|敞篷吉普车|驾驶位|UAZCDriverSeatConfig|
|敞篷吉普车|副驾驶位|UAZCPassengerSeat01Config|
|敞篷吉普车|后排左侧位|UAZCPassengerSeat02Config|
|敞篷吉普车|后排右侧位|UAZCPassengerSeat03Config|
|防弹吉普车|驾驶位|UAZFDriverSeatConfig|
|防弹吉普车|副驾驶位|UAZFPassengerSeat01Config|
|防弹吉普车|后排左侧位|UAZFPassengerSeat02Config|
|防弹吉普车|后排右侧位|UAZFPassengerSeat03Config|
|布篷吉普车|驾驶位|UAZPDriverSeatConfig|
|布篷吉普车|副驾驶位|UAZPPassengerSeat01Config|
|布篷吉普车|后排左侧位|UAZPPassengerSeat02Config|
|布篷吉普车|后排右侧位|UAZPPassengerSeat03Config|
|吉普车|驾驶位|UAZDriverSeatConfig|
|吉普车|副驾驶位|UAZPassengerSeat01Config|
|吉普车|后排左侧位|UAZPassengerSeat02Config|
|吉普车|后排右侧位|UAZPassengerSeat03Config|
|摩托艇|驾驶位|AquaRailDriverSeatConfig|
|摩托艇|后排乘客位|AquaRailPassengerSeat01Config|
|快艇|驾驶位|PG117DriverSeatConfig|
|快艇|副驾驶位|PG117PassengerSeat01Config|
|快艇|中排左侧位|PG117PassengerSeat02Config|
|快艇|中排右侧位|PG117PassengerSeat03Config|
|快艇|后排左侧位|PG117PassengerSeat02Config|
|快艇|后排右侧位|PG117PassengerSeat03Config|

---

### 伤害配置

开发者可对载具爆炸时的伤害范围与衰减程度进行调整。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PrLLAimage.png)

- 载具爆炸范围内径：与载具的距离<=内径值时，受到的伤害固定为 ``ExplosionBaseDamage`` 属性值大小
- 载具爆炸范围外径：与载具的距离=外径值时，受到的伤害为 ``ExplosionMinimumDamage`` 属性值大小；超过外径距离不受到伤害；否则，基于伤害衰减系数计算伤害值
- 载具爆炸伤害衰减：处于内外径之间时伤害基于系数计算，公式为 ``(((外径 - 距离) / (外径 - 内径)) ^ 衰减系数) * (基础伤害值 - 最小伤害值) + 最小伤害值``

---

### 添加载具武器

如果使用的座椅数据资产支持载具武器配置，则可以添加载具武器。点击实体编辑器【载具武器】页签，参考 [新建载具蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20245?autoJump=%E6%96%B0%E5%BB%BA%E8%BD%BD%E5%85%B7%E8%93%9D%E5%9B%BE) 的方式基于任一载具武器模板创建载具武器蓝图。

> 载具武器蓝图的属性配置与普通枪械蓝图相同，可参见 [自定义枪械](https://developer.gp.qq.com/wikieditor/#/catalog/20103)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sDGaLimage.png)

在需要添加武器的座椅组件上启用武器，将 ``武器Class`` 设置为刚才创建的武器蓝图，调整武器相对于座椅组件的偏移量，即可将普通载具升级为带有武器的武装载具。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UwfhWimage.png)

目前驾驶位的座椅模板支持同时激活多个武器，但共享同一个开火按键，即开火时触发所有武器的攻击行为。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NFkyuimage.png)

<br>

## 生成载具

配置好载具蓝图后，可以将蓝图放置在场景中或者脚本调用API动态生成载具供玩家使用。

### 场景中放置载具

载具蓝图需要通过 ``BP_UGCVehicleRefresher_Base`` 组件绑定放置在场景中，不建议直接拖放至场景，否则蓝图的属性配置可能不生效。

编辑器【模式】窗口中搜索“BP_UGCVehicleRefresher_Base”，将该Actor放置在场景中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XEjMlimage.png)

【世界大纲】中找到该Actor对象，将 ``Target Vehicle`` 属性设置为创建好的载具蓝图，载具将被实例化到场景中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hWZEoimage.png)

---

### 动态生成载具

调用 [``SpawnVehicle``](https://developer.gp.qq.com/api/#/searchContent/UGCVehicleSystemV2?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCVehicleSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCVehicleSystemV2&autoJump=SpawnVehicle) 可以动态生成载具，同时 ``UGCVehicleSystemV2`` 函数库提供了更多对载具的操作及数据查询类功能函数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/udincimage.png)

<br>

## API参考

> 载具编辑器创建的载具需要配合V2函数库使用，与旧版函数（UGCVehicleSystem/UGCVehicleSeatSystem/UGCVehicleCommonSystem）不兼容

|函数库/类名|函数类型|函数功能范围|
|-|-|-|
|[UGCVehicleSystemV2](https://developer.gp.qq.com/api/#/searchContent/UGCVehicleSystemV2?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUGCVehicleSystemV2.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCVehicleSystemV2)|静态函数|生成载具、上下载具、设置载具属性等各类功能函数|


---


## 载具刷新器

> 文档路径: 进阶内容 > GamePlay系统 > 载具系统 > 载具刷新器

**涉及API:** `AddVehicleDriveAwayEventListener`, `AddVehicleEventListener`, `BP_UGCVehicleRefresherTool`, `DestroyCurrentVehicle`, `GenerateCustomizeVehicle`, `GenerateVehicle`, `GetVehicleRespawnPointConfig`, `GetVehicleStatusConfig`, `RemoveVehicleDriveAwayEventListener`, `RemoveVehicleEventListener`, `ResetVehicleRespawnPoint`, `UGCActorComponentUtility`, `UGCActorComponentUtility.GetAllActorsOfClass`, `UGCGame`, `UGCObjectUtility`, `UGCObjectUtility.LoadClass`

# 载具刷新器

载具刷新器通过蓝图配置和API调用的方式提供载具刷新的功能，适用于关卡中指定位置按需刷出载具对象的场景。

<br>

## 添加刷新器蓝图

> 除开以下两种方式添加载具刷新器，其他方式均属于不规范操作

方式1：在内容浏览器下搜索 “载具刷新器2.0” ，将该蓝图直接拖放至关卡场景中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6xRKmimage.png)

方式2：在模式编辑窗口下搜索 "BP_UGCVehicleRefresherTool" ，将蓝图直接拖放至关卡场景中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9GZ7Pimage.png)

<br>

## 配置刷新参数

刷新器蓝图的配置参数比较简单，主要通过基于权重随机的方式刷出载具。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JcuBPimage.png)

- Vehicle List：一组载具刷新列表
	- SoftPath：通过 [载具编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20245) 创建的载具蓝图类
	- Weight：刷新权重值，``刷新概率 = 该载具权重 / 权重总和``
- Active Begin：游戏启动时是否自动激活刷新点，刷新器默认只会执行一次刷新，再次刷新需要脚本中调用 [``GenerateVehicle``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool) 等函数主动触发

<br>

## 动态刷新载具

当刷新器蓝图启用了 ``Active Begin`` 属性时，游戏启动后即会在刷新器对应位置刷出载具，如果希望动态控制刷新状态可以调用 ``BP_UGCVehicleRefresherTool`` 函数库提供的接口来实现，例如 ``GenerateVehicle`` 允许重新生成载具。

```lua
local ToolClass = UGCObjectUtility.LoadClass('/Game/UGC/UGCGame/Vehicle/Refresher/BP_UGCVehicleRefresherTool.BP_UGCVehicleRefresherTool_C')
local ToolActors = UGCActorComponentUtility.GetAllActorsOfClass(self, ToolClass)
if #ToolActors > 0 then
	ToolActors[1]:GenerateVehicle()
end
```

<br>

## API参考

|函数名/类名|函数类型|函数功能范围|
|-|-|-|
|[``AddVehicleEventListener``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=AddVehicleEventListener)|对象函数|载具生成事件监听器|
|[``AddVehicleDriveAwayEventListener``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=AddVehicleDriveAwayEventListener)|对象函数|载具离开刷新器事件监听器|
|[``RemoveVehicleEventListener``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=RemoveVehicleEventListener)|对象函数|移除载具生成事件监听器|
|[``RemoveVehicleDriveAwayEventListener``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=RemoveVehicleDriveAwayEventListener)|对象函数|移除载具离开刷新器事件监听器|
|[``GenerateVehicle``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=GenerateVehicle)|对象函数|随机生成载具|
|[``GenerateCustomizeVehicle``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=GenerateCustomizeVehicle)|对象函数|生成指定的载具蓝图|
|[``DestroyCurrentVehicle``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=DestroyCurrentVehicle)|对象函数|销毁当前刷新点管理的载具|
|[``ResetVehicleRespawnPoint``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=ResetVehicleRespawnPoint)|对象函数|重置载具刷新点，如果载具还在原地，先销毁再重新刷新|
|[``GetVehicleRespawnPointConfig``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=GetVehicleRespawnPointConfig)|对象函数|获取配置的载具列表信息|
|[``GetVehicleStatusConfig``](https://developer.gp.qq.com/api/#/searchContent/BP_UGCVehicleRefresherTool?classDetailShow=true&path=class%2Fdetail%2FOthers%2FBP_UGCVehicleRefresherTool.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=BP_UGCVehicleRefresherTool&autoJump=GetVehicleStatusConfig)|对象函数|获取当前车辆的实时状态信息|

---
