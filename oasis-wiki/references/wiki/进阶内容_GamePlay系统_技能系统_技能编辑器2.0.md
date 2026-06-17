# 进阶内容/GamePlay系统/技能系统/技能编辑器2.0

> 本分类共 7 篇文章

---


## 技能抛体

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 技能抛体

**涉及API:** `CastSkill`, `NewProj`, `NewSkill`

# 技能抛体

> 此抛体基类为旧版本过渡使用，建议统一切换至 [通用抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20165) 实现功能

抛体是指通过物理模拟的方式实现带有飞行轨迹的动态对象，通常应用于投掷物、远程攻击等场景，例如手雷、远程导弹甚至法术飞弹等都可以通过抛体的形式来表现。[技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091) 内置了抛体模块，允许开发者通过蓝图的方式配置抛体并经由 ``发射抛体`` 节点挂载至任意技能上。

> 当前抛体只适用于技能中，通过 [技能Task-发射抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E5%8F%91%E5%B0%84%E6%8A%9B%E4%BD%93) 关联引用，暂不支持作为 [投掷物物资](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/188) 的抛体类使用

![ezgif.com-video-to-gif-converter (1).gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vwVBPezgif.com-video-to-gif-converter%20(1).gif)

<br>

## 抛体模板

抛体模块内置了命中型与爆炸型两类模板，开发者可以根据需求基于模板创建抛体蓝图，也能在创建后的蓝图上通过自定义组合不同的抛体属性来实现更加个性化的效果。

**【命中型抛体】**

以毒液模板为例，命中型抛体会对击中的对象触发伤害/治疗或者指定的特殊效果。

![duye-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HaS6fduye-ezgif.com-video-to-gif-converter.gif)

**【爆炸型抛体】**

以毒气手雷模板为例，爆炸型抛体除了能触发命中效果外，还具备额外的爆炸效果。

![show3-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Lpa8cshow3-ezgif.com-video-to-gif-converter.gif)

<br>

## 抛体蓝图结构

打开编辑器菜单栏中的 [技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091)，选中 ``抛体`` 类目，【Template】窗口显示预设的抛体模板，以任意模板创建的抛体蓝图将自动添加到 ```Asset/Blueprint/Prefabs/Projectiles``` 目录下。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CBRoMimage.png)

【Asset Tree】窗口下双击创建的抛体，打开抛体蓝图界面，抛体主要由 ``ProjectileMovement（抛射物）组件``、``Collision（碰撞体）组件`` 和其他粒子特效或静态网格体组成。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wB6iHimage.png)

[抛射物组件]((https://blog.csdn.net/zxh1592000/article/details/127092319)) 模拟物体抛掷在世界场景中的运动状态，是抛体的核心组件。
> 此组件下的属性无需单独设置，可配置的相关属性集中在蓝图的 ``Universal Projectile Base`` 组下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DARk3image.png)

[碰撞体组件](https://zhuanlan.zhihu.com/p/546113152) 用于检测物体是否发生碰撞以及触发特定的碰撞事件/委托，根据检测范围的不同分为 ``BoxCollision（立方体碰撞体）``、``CapsuleCollision（胶囊体碰撞体）`` 和 ``SphereCollision（球体碰撞体）`` 三种简单碰撞体，在抛体中必须将碰撞体组件作为与抛射物组件平级的根组件，否则在高速飞行的抛射物场景下可能出现碰撞检测失效的情况。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GzK6eimage.png)

在碰撞体组件下可以挂载静态网格体组件或者粒子组件，用于表现抛体的具体形态，例如导弹类型的抛体除了导弹的模型，可能还会包含飞行尾迹等特效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/seEWwimage.png)

<br>

## 抛体配置属性

抛体的核心属性分布在 ``Universal Projectile Base``、``Track Config``、``Explosion Config`` 和 ``Bounce Config`` 属性组下。

### 基础属性

``Universal Projectile Base`` 组为抛体的基础属性，允许开发者设置抛体的飞行速度/朝向、碰撞规则、命中特效等等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FxccHimage.png)

- 客户端禁用模拟：对于简单的运动轨迹抛体，开启此选项可以禁用模拟以提升性能
- 最大销毁距离：抛体的最大飞行距离，超出该距离后抛体会被销毁，小于0无效
- 最大存活时长：抛体的最大存活时间，超过时间后抛体会自动销毁，小于0无效
- 是否忽略自己：抛体在飞行过程中是否会与自己发生碰撞
- 抛体前向与速度一致：是否保持抛体始终朝向其速度方向
- 穿透次数：抛体能造成多少次碰撞伤害
- 击中Pawn生成的特效：击中Pawn时候的命中特效
- 击中声效：击中时播放的音效
- 启用特效缩放：是否启用击中特效的缩放设置
	- 击中特效大小缩放：特效的缩放系数
- 击中特效跟随击中物体：命中特效跟随击中目标，且跟随目标根节点；如果命中对象为Pawn，则跟随位置为骨盆
- 击中添加的BuffClass：可为命中对象添加指定 [Buff](https://developer.gp.qq.com/wikieditor/#/catalog/20087)
- 击中生成的Actor：可为命中点生成指定的Actor类对象，生成位置为命中点的贴地位置
- 碰撞忽略的阵营：抛体不会与指定 [阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%98%B5%E8%90%A5%E7%B3%BB%E7%BB%9F) 的对象发生碰撞，默认忽略Same阵营

---

### 目标追踪

``Track Config`` 配置抛体追踪目标的方式，当启用追踪后，抛体将以指定的速度按朝向直线追踪目标，目标受 [技能Task-选择目标](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E9%80%89%E6%8B%A9%E7%9B%AE%E6%A0%87) 配置效果影响。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tDKwcimage.png)

- 启用目标追踪：是否开启目标追踪功能
- 追踪速度：设置抛体在追踪目标时的速度

---

### 爆炸属性

``Explosion Config`` 定义抛体的爆炸行为，包括爆炸的触发方式、伤害、特效等。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QPMm6image.png)

- 爆炸触发方式：设置爆炸发生的条件
	- 不发生爆炸：抛体不执行爆炸
	- 命中立即爆炸：抛体命中后立即执行爆炸
	- 停止后开始计时延迟爆炸：抛体命中后开始计时并延迟执行爆炸
	- 弹射后开始计时延迟爆炸：抛体命中触发弹射后开始计时并延迟执行爆炸
	- 命中Pawn后开始计时延迟爆炸：抛体命中Pawn后开始计时并延迟执行爆炸 
- 爆炸延迟：爆炸的延迟时间，选择带有“计时延迟”类型的触发方式时才生效
- 爆炸伤害：爆炸造成的伤害，常数数值或者基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的公式化配置
- 爆炸添加的BuffClass：为爆炸范围内影响的目标添加指定 [Buff](https://developer.gp.qq.com/wikieditor/#/catalog/20087)
- 爆炸半径：爆炸的影响范围，涉及伤害计算
- 爆炸筛选器：指定的对象将不受爆炸伤害影响，可以指定类对象，也可以按 [阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095?autoJump=%E9%98%B5%E8%90%A5%E7%B3%BB%E7%BB%9F) /队友身份过滤
- 爆炸特效：发生爆炸时的效果
- 启用自定义爆炸特效缩放：是否启用爆炸特效的缩放设置
	- 爆炸特效缩放：特效的缩放系数
- 爆炸音效：爆炸发生时播放的音效

---

### 弹跳属性

``Bounce Config`` 目前只支持设置抛体弹跳时播放的音效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HmDKBimage.png)

---

### 震屏属性

在“默认”分组下设有一组震屏属性，当技能抛体命中时即对命中目标触发相应的震屏效果，震屏形式为相机XY轴上的随机震动，开发者可以自定义设置震屏强度、范围等属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9tWqNimage.png)

- Camera Shake Range：以技能抛体为中心影响的震屏范围
- Player Pawn：受到震屏影响的角色类型
- Camera Shake Time：震动持续时间
- Camera Shake Scale：震动强度

<br>

## 案例演示

以 ```精确制导``` 技能模板为例，通过修改抛体的模型和特效等属性，实现一个“斩妖飞刀”的技能效果。

1. 创建导弹技能

基于 ```精确制导``` 模板创建一个新的技能，取名为```NewSkill```，双击打开 ```NewSkill``` 技能编辑面板，选中 ```CastSkill``` 阶段，该阶段技能轨道上已内置一个名为 ```发射抛体``` 的技能Task。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/b4YkQimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BSdbGimage.png)

在角色技能轨道上选中 ```发射抛体```，该Task【任务配置】面板的 ```Projectile Class``` 属性关联抛体类，创建出的技能抛体将在此处配置替换。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mbrFQimage.png)

2. 创建并修改抛体

技能编辑器切换至 ``抛体`` 类目，以 ```导弹``` 为模板创建一个新的抛体，取名为 ```NewProj``` 。

![企业微信截图_17407290708518.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bedKW%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17407290708518.png)

选择抛体蓝图的静态网格体组件，将静态网格体替换为其他模型，此处替换为大砍刀模型并调整缩放。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oRX5Zimage.png)

替换抛体蓝图的 ```击中Pawn生成的特效``` 以及 ```爆炸特效```。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HvDLWimage.png)

设置 ``Explosion Config`` 组下的【爆炸伤害】为常数80，【爆炸半径】为300。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UQX19image.png)

3. 替换抛体验证效果

将新建的抛体 ```NewProj``` 配置到技能 ```NewSkill``` 的 ```发射抛体``` 技能Task上：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MvAjLimage.png)

将 ```NewSkill``` [技能赋予角色](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E9%80%9A%E8%BF%87%E8%93%9D%E5%9B%BE%E9%85%8D%E7%BD%AE%E6%8A%80%E8%83%BD)，启动Debug调试验证技能释放效果。

![ezgif.com-video-to-gif-converter (2).gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2FXSiezgif.com-video-to-gif-converter%20(2).gif)


---


## 技能Task查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 技能Task查询手册

**涉及API:** `AUniversalProjectileCore`, `Anim3DTransformWarpingTargetType_Custom`, `Anim3DTransformWarpingTargetType_SelectTarget`, `Anim3DTransformWarpingTargetType_SelectTransform`, `AnimListComp`, `InitTask_BP`, `Interval`, `None`, `OnActivate_BP`, `OnDeactivate_BP`, `OnTrigger_BP`, `PESkillPickerBase`, `Slot0`, `SortFunction`, `TaskSupportRPC_BP`, `Task已执行时间`, `Task总时间`

# 技能Task查询手册

## 通用属性

所有类型的技能Task都具备一些通用属性：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dkq41image.png)

- Interval：Task的执行时间间隔，>0的值表示隔多久执行一次该Task，执行时间点以白色分隔线显示在该Task上，-1代表只执行一次，此属性仅对周期性Task有影响
	![QQ2025620-211434-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uFAenQQ2025620-211434-HD-ezgif.com-video-to-gif-converter.gif)
- LifeMode：技能Task的生命周期，具有三种类型
	- Task结束时还原：到技能Task在时间轴上配置的结束时间点，技能Task的效果结束并还原
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mtSFJimage.png)
	- 技能结束时还原：技能Task生效后会直到整个技能结束才结束技能效果
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gpokIimage.png)
	- Task不还原：技能Task效果不会自动还原（使用该选项是要注意技能效果的残留问题。比如生成了一个Loop类型的特效，如果自身代码没有清理逻辑，又使用了该选项的话，那么该特效就会残留在游戏内）
> 不同技能Task根据设计的不同，可以使用的生命周期类型不同，并非所有的节点都会支持还原，比如造成伤害、治疗等这类节点是一次性的效果，不允许进行还原，不提供相应的选项。
- Name：Task的自定义显示名称
- Section Color：Task的自定义显示颜色，需要勾选 ``Use Custom Color`` 时有效
- Use Custom Color：当勾选时，可通过 ``Section Color`` 设置Task显示颜色；否则更改了颜色但编译后会被还原
- 完成时：该Task执行完成时是否需要重置动画的状态，通常用于动画卡帧场景使用
- 开始时间：Task相对于时间轴开始执行的时间
- 结束时间：Task相对于时间轴结束的时间
- 为激活：该Task是否处于激活状态，未激活的Task将置灰且不执行效果
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/m06Ykimage.png)
- 为锁定：该Task是否被锁定，锁定中的Task无法拖动时间轴上的位置
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hmvPgimage.png)
- 为无限：该Task片段是否无限长，不建议勾选

<br>

## 动画表现

### 基础动画Task

使用 [基础动画轨道](https://developer.gp.qq.com/wikieditor/#/catalog/20170?autoJump=%E5%BA%8F%E5%88%97%E6%92%AD%E6%94%BE%E5%99%A8%E9%85%8D%E7%BD%AE) 配置的动画Task的属性。

> 当前已弃用，请转用 ``技能动画Task``，已存在的配置功能不受影响

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QJ7moimage.png)

- 动画：需要播放的动画资源
- 播放速率：动画的播放速率，速率约大播放速度越快
- SlotName：播放所使用的 [动画插槽](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-slots-in-unreal-engine)，支持 ``全身`` 与 ``上半身``
- Blend Out Time：动画的混出时间

---

### 技能动画Task

使用 [技能动画轨道](https://developer.gp.qq.com/wikieditor/#/catalog/20170?autoJump=%E5%BA%8F%E5%88%97%E6%92%AD%E6%94%BE%E5%99%A8%E9%85%8D%E7%BD%AE) 配置的动画Task的属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EUPeCimage.png)

- 动画播放起始偏移：于时间轴上的开始时段
- 动画播放结束偏移：于时间轴上的时段结束
- 动画：需要播放的动画资源
- 播放速率：动画的播放速率，速率约大播放速度越快
- 动画Slot类型：播放所使用的 [动画插槽](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/animation-slots-in-unreal-engine)，相比于基础动画Task支持的类型更多
	- 全身（不叠加瞄准）：覆盖全身动作，但不会叠加 [瞄准偏移](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/aim-offset-in-unreal-engine)
	- 全身（叠加瞄准）：覆盖全身动作，但会叠加 [瞄准偏移](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/aim-offset-in-unreal-engine)
	- 上半身（不叠加瞄准）：覆盖上半身以上动作，但不会叠加 [瞄准偏移](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/aim-offset-in-unreal-engine)
	- 上半身（叠加瞄准）：覆盖上半身以上动作，但会叠加 [瞄准偏移](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/aim-offset-in-unreal-engine)
	- 胸部（不叠加瞄准）：覆盖胸部以上动作，但不会叠加 [瞄准偏移](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/aim-offset-in-unreal-engine)
	- 胸部（叠加瞄准）：覆盖胸部以上动作，但会叠加 [瞄准偏移](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/aim-offset-in-unreal-engine)
	- 手臂：仅覆盖手臂动作
	- 近战：静止时为覆盖全身动作，移动时为覆盖上半身动作
- 混出时间：动画的混出时间
- 混入时间：动画的混入时间

---

### AnimTransform轨道

该轨道通过提取动画序列或者为动画添加额外的 [根运动](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/root-motion?application_version=4.27) 数据，确保角色包含碰撞体的位移效果与实际动画保持同步。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/v6laYimage.png)

- Transform Source：读取位移数据类型
	- Anim3DTransformSource_Manual：通过编辑关键帧来自定义动画的位移数据
	![ezgif-5b84b570305ae0c8.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HVcriezgif-5b84b570305ae0c8.gif)
	- Anim3DTransformSource_Animation：读取动画序列自带的RootMotion位移数据
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BD1KHimage.png)
- Transform Type：位移的类型
	- Anim3DTransformType_Absolute：绝对位移，以播放动画时角色的世界坐标为基准点，加上所设定的偏移量，计算出最终到达的世界坐标位置，不会因镜头转动而发生偏移
	- Anim3DTransformType_Delta：累加位移，累加位移是在角色当前的实时位置和朝向上，执行偏移量总长度的位移，方向会随镜头旋转而实时改变，直至预设的位移总量全部完成
- Enable Slide：启用后，遇到障碍物时将发生碰撞挤压的侧滑效果；否则停止位移
- Keep Floor：位移过程中是否保持贴近地面
- Translation Scale：位移距离的总体缩放比例
- Warping Target Configs：支持基于时间轴配置多段位移效果
	- start Time：位移效果在时间轴上所对应的起始时间点
	- End Time: 位移效果在时间轴上所对应的结束时间点
	- Target Type：位移的目标位置类型
		- Anim3DTransformWarpingTargetType_SelectTarget：取决于技能编辑器中 [选择目标Task](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E9%80%89%E6%8B%A9%E7%9B%AE%E6%A0%87:~:text=%E7%9A%84%E6%9C%80%E8%BF%9C%E8%B7%9D%E7%A6%BB%E3%80%82-,%E6%8A%80%E8%83%BDTask%2D%E9%80%89%E6%8B%A9%E7%9B%AE%E6%A0%87,-%E4%BB%A5%E6%8C%87%E5%AE%9A%E5%BD%A2%E7%8A%B6) 所选取对象的位置
		- Anim3DTransformWarpingTargetType_SelectTransform：取决于技能编辑器中 [选择点Task](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E9%80%89%E6%8B%A9%E7%82%B9:~:text=%E9%80%89%E5%8F%96-,%E6%8A%80%E8%83%BDTask%2D%E9%80%89%E6%8B%A9%E7%82%B9,-%E8%BF%90%E8%A1%8C%E6%97%B6%E6%A0%B9%E6%8D%AE) 选取的选点位置
		- Anim3DTransformWarpingTargetType_Custom：自定义位置
	- Target Offset：目标位置的偏移量，仅针对 ``Anim3DTransformWarpingTargetType_SelectTarget`` 和 ``Anim3DTransformWarpingTargetType_SelectTransform`` 生效
	- Transform Getter：基于 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 变量值决定目标位置，仅针对 ``Anim3DTransformWarpingTargetType_Custom`` 生效
		- Value：目标位置偏移量
		- PropertyName：变量名称，属性绑定数据类型：FTransform
	- Max Translation：最大位移位置上限，达到这个上限将停止位移
	- Max Rotation Angle：向目标旋转时，旋转的最大角度上限
- Max Warping Distance：允许发生位移的最大距离限制，动画位移仅在移动距离<=该距离时生效
- Max Warping Angles：允许旋转的最大角度限制，动画位移仅在旋转角度<=该角度时生效

<br>

## Buff

### 技能Task-添加Buff

为目标添加指定的Buff效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GIGanimage.png)

- Buff类型：需要添加的 [Buff蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20087)
- 添加的层数：要添加几层Buff
   - Property：常量
   - Attribute：具体参考[属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20098) 
- 覆写生效时长：Buff持续时间，-1代表不覆盖该Buff蓝图配置的生效时长
   - Property：常量
   - Attribute：具体参考[属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20098) 
- 目标类型：
	- 技能施法者：给施法者加Buff
	- 全部技能Target：给技能选中的目标添加Buff，依赖前置 **``目标选择``** 类型Task的选取结果

---

### 技能Task-移除Buff

从目标身上移除对应Buff

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jPtdSimage.png)

- 移除方式：
	- 指定类型：根据配置的Buff基类移除匹配的Buff
	- 拥有任意Tag：当移除目标身上的Buff实例携带的类型Tag拥有配置的任一tag时，则移除对应的Buff实例
- Buff类型：要移除的 [Buff蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20087)
- 移除的层数：移除的Buff层数，如果移除后为0将销毁Buff
   - Property：常量
   - Attribute：具体参考[属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20098) 
- 目标类型：
	- 技能施法者：施法者自身
	- 全部技能Target：给技能选中的目标添加Buff，依赖前置 **``目标选择``** 类型Task的选取结果  

<br>

## 角色

### 技能Task-添加冲量

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kNccNimage.png)

- 冲量方向：
	- 选中位置方向：沿技能Task选点位置与目标的连线向量，取其反方向单位向量并施加物理冲量，技能目标与选中位置依赖前置 **``目标选择``** 类型Task的选取结果
	- 施法者方向：沿施法单位到目标单位的连线向量，取其反方向单位向量并施加物理冲量，技能目标依赖前置 **``目标选择``** 类型Task的选取结果
	- 选中方向：沿选中方向施加物理冲量，技能目标依赖前置 **``目标选择``** 类型Task以及 **``选择方向``** 的选取结果
- Horizontal Speed：冲力的水平运动速度
- Vertical Speed：冲力的垂直运动速度
- Horizontal Friction：水平运动速度的摩擦力
- Duration：冲力效果的持续时间
- Priority：优先级，当多个冲力效果作用在同一个目标上时，以该值判断执行哪个冲力效果

---

### 技能Task-冲刺

在技能执行期间，施法者将沿预设方向持续位移，该位移行为将与Task生命周期同步。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kQLubimage.png)

- 冲刺速度类型：
  - 常数：整段位移速度不变
  - 曲线：冲刺速度是一条随时间变化的曲线
  	- 冲刺速度曲线：配置曲线资产
- 冲刺速度：位移速度的常数值，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)
- 冲刺方向：非“瞄准方向/角色前向”类型依赖前置 **``目标选择``** 类型Task的选取结果
  - 瞄准方向：沿当前瞄准方向进行冲刺
  - 选取方向：沿技能选定的方向进行冲刺
  - 选取点位：朝向技能指定的坐标位置进行冲刺
  - 选取目标：朝向技能选中的目标单位进行冲刺
  - 角色前向：沿角色当前朝向的正前方进行冲刺
- 冲刺转向类型：
   - View Direction：使用摄像机视角方向控制冲刺转向
   - JoyStick Direction：使用摇杆输入方向控制冲刺转向
   - Custom Direction：暂不支持
- 角色朝向：
   - Dash Direction：冲刺过程中角色会朝向冲刺速度方向。
   - View Direction：冲刺过程中角色会始终面向视角方向。
- 转向速度：每秒能够旋转的角度（°/s），若目标位置距离较远，角色将以恒定转向速度持续调整朝向，直至对准转向方向，针对 ``View Direction`` 或者 ``JoyStick Direction`` 模式有效，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)
- 冲刺过程重力系数：冲刺过程中施法者受到的重力系数是多少
- 冲刺过程碰撞检测阵营：勾选将忽略阵营对象的碰撞检测，释放者能够穿透该实体单位，阵营的说明可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)
- 位移是否忽略Pawn：无论是否勾选此选项，碰撞事件都会正常触发。勾选后，在冲刺时将可以穿过其他玩家角色
- Clear Velocity on Exit：冲刺结束是否清除速度

> 属性绑定数据类型：float

---

### 技能Task-造成伤害

对目标造成固定伤害值。
> 【周期性Task】每隔 ``Interval`` 触发一次伤害

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RbNf9image.png)

- TargetType：接收伤害的目标类型
	- 技能施法者：对施法者自身造成伤害
	- 全部技能Target：对技能选中的全部目标造成伤害，依赖前置 **``目标选择``** 类型Task的选取结果
- 伤害类型Tag列表：支持为伤害添加Tag，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20102) 创建
- 伤害数值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 伤害数值属性来源：若 ``伤害数值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自选取的技能目标，若选中多个目标，则分别取各目标的属性独立计算，依赖前置 **``目标选择``** 类型Task的选取结果
- On Hurt Effect Asset：可配置 [受击资产](https://developer.gp.qq.com/wikieditor/#/catalog/20169)，启用后伤害目标具备受击效果

---

### 技能Task-追踪目标

以选取的技能目标的第一个Actor为锚点，让技能施法者向该Actor进行吸附，吸附效果分为 ``位移吸附`` 和 ``朝向吸附`` 两部分，其中位移吸附使施法者的位置向目标位置进行吸附；朝向吸附使施法者的朝向向目标所在位置方向进行吸附，依赖前置 **``目标选择``** 类型Task的选取结果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kxBWRimage.png)

- TraceType：吸附类型
   - 选中目标：施法者会朝选中目标执行吸附行为。仅该情况下吸附功能同时支持方向吸附和位移吸附
   - 选中方向：施法者的朝向向选中方向进行吸附，依赖前置 **``选择方向``** 类型Task的选取结果
   - 选中点方向：施法者会向选中点方向进行，依赖前置 **``选点``** 类型Task的选取结果
- 最大吸附角度：能够进行吸附的最大角度，当目标所在位置的方向与当前施法者朝向的角度小于该角度时，才会发生吸附，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)
- 角度吸附速度：朝向吸附的追踪修正速度，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)
- 最小吸附距离：能够进行吸附的最小距离范围，只有当目标所在位置和当前施法者位置的距离大于该距离时，才会发生吸附，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)
- 最大吸附距离：能够进行吸附的最大距离范围，只有当目标所在位置和当前施法者位置的距离小于该距离时，才会发生吸附，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)
- Trace Distance Ignore ZAxis：吸附是否忽略Z轴
- 位移吸附速度：位移吸附的追踪修正速度，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A)

> 属性绑定数据类型：float

---

### 技能Task-切换姿势

切换施法者的Pose姿态至目标Pose，仅对主角生效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TafUDimage.png)

- 要切换到的姿势：目标Pose，支持站立、蹲伏和匍匐

---

### 技能Task-治疗

对指定目标执行生命值的治疗效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/w0nb5image.png)

- 目标类型：治疗的目标类型
	- 技能施法者：对施法者自身造成伤害
	- 全部技能Target：对技能选中的全部目标造成伤害，依赖前置 **``目标选择``** 类型Task的选取结果
- 修改值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 恢复血量Tags：支持为治疗行为添加Tag，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20102) 创建

---

### 技能Task-拉取

将选择的第一个目标拉取并吸附至指定位置，到达后立即停止位移。

> 拉取的目标取决于技能编辑器中 ``选择目标类型Task`` 的选取结果

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WKNi0image.png)

- 拉取目标位置类型：
    - 施法者位置:向施法者位置进行拉取。
    - 选中的第一个位置:向选中的第一个位置进行拉取。
- 目标位置偏移：拉取最终落地相较原本的偏移
- 拉取速度类型：
   - PullSpeedType_Scalar：常速
   - PullSpeedType_Curve:速度曲线
- 拉取速度：拉取的速度大小，支持属性绑定
- 是否强制面向拉取目标位置：在拉取过程中，是否强制目标始终面向目标位置。
- 阵营碰撞关系：勾选将忽略阵营对象的碰撞检测，释放者能够穿透该实体单位，阵营的说明可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)

> 属性绑定数据类型：float

<br>

## 表现

### 技能Task-附加Actor

生成一个Actor，并将该Actor挂载到自身的一个Socket上，让该Actor跟随施法者。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yazxyimage.png)

- EndType：选择该Actor在客户端或者服务端生成
- 附加的Actor类：生成的Actor蓝图类
- Socket：支持按 ``部位类型`` 或者 ``插槽名称`` 附加
- Offset：挂载位置基于该Socket点的偏移
- 任务结束时销毁：当该Task结束时是否销毁Actor

> 插槽名称对应的骨骼Socket位置可参考Pawn骨骼树的结构：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ES7Jximage.png)

---

### 技能Task-控制相机

执行该Task时，将根据配置的值，修改相机的参数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tDIsYimage.png)

- Socket Offset：相机摇臂的Socket点相较原本的偏移
- Target Offset：相机摇臂的Target点相较原本的偏移
- Target Arm Length：覆盖的摇臂长度大小
- Additive Offset Fov：Fov相较原本的变化值
- Use Pawn Control Rotation Modify：使用Control Rotation模式是否需要变化
- Use Pawn Control Rotation：是否使用Pawn Control Rotation（否则会根据Spring Arm Rotation的配置，限制相机轴的旋转）
- Spring Arm Rotation：如果希望在技能Task生效过程中，固定相机某轴的旋转——则需要把将该轴数值配置为定值。比如希望技能Task执行期间，始终俯视角看施法者，则应该配置为（0，90，0）
- Camera Lag Speed Modify：是否需要修改相机的Lag速度
- Camera Lag Speed：修改后的Lag速度
- Camera Rotation Lag Speed Modify：是否需要修改相机的旋转Lag速度
- Camera Rotation Lag Speed：修改后的旋转Lag速度
- 淡入时间：从执行Task开始将以设定的过渡时间，从初始状态平滑切换至目标配置参数，单位为秒，持续时间不得超过Task总时长
- 淡出时间：Task结束前，从配置参数平滑切换至初始状态，单位为秒，持续时间不得超过Task总时长

---

### 技能Task-镜头抖动

播放一个震屏效果，Task结束时震屏结束。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Rlaglimage.png)

- 抖动类型：
   - Y轴方向震动：屏幕仅沿垂直方向上下震动
   - X轴方向震动：屏幕仅沿水平方向左右震动
   - 随机方向：随机抖动
- 抖动幅度：影响震屏强度大小
- 目标类型：
   - 释放者自身：以释放者自身播放震屏。
   - 选中目标：在技能Task选中的目标位置播放震屏，依赖前置 **``目标选择``** 类型Task的选取结果
   - 选中点周围：根据 ``生效距离`` 判断，决定主控端是否播放震屏
   ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oDJfmimage.png)
	 - 生效距离：选点位置为中心的半径范围，依赖前置 **``目标选择``** 类型Task的选取结果

---

### 技能Task-播放预设动画

为怪物共享动画功能预留的功能Task，通常怪物的攻击行为通过技能表示，为了优化怪物攻击时的表现性能，允许 [共享动画](https://developer.gp.qq.com/wikieditor/#/catalog/20251?autoJump=%E5%85%B1%E4%BA%AB%E5%8A%A8%E7%94%BB%E6%A8%A1%E5%BC%8F) 实例以进行合批提升性能，此Task即是播放指定的共享攻击动画。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/smZ33image.png)

- 动画标签：默认使用 ``GenericCharacterAnim.General.SharingStateAnim.Attack``，需要确保怪物蓝图的 ``AnimListComp`` 组件中配置了该标签的动画资源
- 播放速率：动画播放速率
- 起始Section名：指定动画播放的起始片段，``None`` 默认从头开始播放

> 该Task为预留功能，当前版本作用有限

---

### 技能Task-播放音效

在指定目标位置处播放一个音效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4q7IQimage.png)

- 播放类型：控制该音效播放端，仅模拟端播放/仅主控端播放/模拟端和主控端均播放
- 生成目标：该音效的生成及播放位置
	- 技能施法者：在施法者位置生成音效
	- 全部技能Target：在选中的全部目标上生成音效，依赖前置 **``目标选择``** 类型Task的选取结果
	- 全部技能位置：在选中的全部目标点上生成音效，依赖前置 **``目标选择``** 类型Task的选取结果
- 音效：需要播放的音效资源
	
---
	
### 技能Task-屏幕特效

仅在客户端执行，用于玩家屏幕上播放特殊效果，支持三种类型的屏幕特效：呼吸渐变、呼吸旋转和线性渐变。

**呼吸渐变**

该特效呈现中心衰减式径向扩散效果，即以实心区域为中心，向四周进行透明度/强度的非线性渐变过渡。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AswZGimage.png)
	
材质半径越大，中间透明圆扩散越大，左边是半径为0的效果，右边是半径为10的效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IxivTimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dO6ijimage.png)

- 噪声图：将所选的噪声图形状以透明玻璃的形式叠加于屏幕并赋予动态效果
- 颜色：改变噪声图的颜色
- 渐变倍率：由选择方向滚动噪声图的速度，若为反方向则与选择方向反方向滚动，范围：-∞~∞
- 持续时间：不勾选任务结束时销毁时生效，单位是秒，范围：0~∞
- 材质半径：材质半径越大，噪声图显示越少，范围：0~∞
- 透明度：噪声图的透明程度，范围：0~1
- 目标类型：
     - 释放者自身：在释放者主控端播放屏幕特效
     - 选中目标：在技能Task选中的目标的主控端播放屏幕特效，依赖前置 **``目标选择``** 类型Task的选取结果

---

**呼吸旋转**

呼吸旋转的半径影响和呼吸渐变一样，多了一个底图旋转，用于表现速度线条之类的效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OyG1jimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IPbLYimage.png)

- 噪声图：将所选的噪声图形状以透明玻璃的形式叠加于屏幕并赋予动态效果
- 颜色：改变噪声图的颜色
- 渐变倍率：由选择方向滚动噪声图的速度，若为反方向则与选择方向反方向滚动，范围：-∞~∞
- 持续时间：不勾选任务结束时销毁时生效，单位是秒，范围：0~∞
- 材质半径：材质半径越大，噪声图显示越少，范围：0~∞
- 透明度：噪声图的透明程度，范围：0-1
- 目标类型：
     - 释放者自身：在释放者主控端播放屏幕特效
     - 选中目标：在技能Task选中的目标的主控端播放屏幕特效，依赖前置 **``目标选择``** 类型Task的选取结果


---

**线性渐变**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pD3ZTimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0HoGUimage.png)

- 噪声图：将所选的噪声图形状以透明玻璃的形式叠加于屏幕并赋予动态效果
- 颜色：改变噪声图的颜色
- 渐变倍率：由选择方向滚动噪声图的速度，若为反方向则与选择方向反方向滚动，范围：-∞~∞、
- 持续时间：屏幕特效持续的时间，单位是秒，范围：0~∞
- 方向：
   - 由下向上：特效在屏幕下方生成向由上至下滚动
   - 由上向下：特效在屏幕上方生效由上至下滚动
- 材质半径：材质半径越大，噪声图显示越少，范围：0~∞
- 透明度：噪声图的透明程度，范围：0-1
- 目标类型：
     - 释放者自身：在释放者主控端播放屏幕特效
     - 选中目标：在技能Task选中的目标的主控端播放屏幕特效，依赖前置 **``目标选择``** 类型Task的选取结果

---

**垂直流动**

实现垂直UV流动效果，通过在屏幕空间叠加底图层，支持双向流动方向配置（自上而下/自下而上）

自下向上：

![ezgif-214e1aec8a16ca.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AfUv1ezgif-214e1aec8a16ca.gif)

自上向下：

![ezgif-228b72c8ad1bb2.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ozeyxezgif-228b72c8ad1bb2.gif)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/W4R5Wimage.png)

- 噪声图：将所选的噪声图形状以透明玻璃的形式叠加于屏幕并赋予动态效果
- 颜色：改变噪声图的颜色
- 方向：
   - 由下向上：特效在屏幕下方生成向由上至下滚动
   - 由上向下：特效在屏幕上方生效由上至下滚动
- 渐变倍率：噪声图滚动的速度
- 持续时间：屏幕特效持续的时间，单位是秒，范围：0~∞
- 目标类型：
     - 释放者自身：在释放者主控端播放屏幕特效
     - 选中目标：在技能Task选中的目标的主控端播放屏幕特效，依赖前置 **``目标选择``** 类型Task的选取结果

---

**自定义屏幕特效**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nMOI7image.png)

- 持续时间：屏幕特效持续的时间，设置为0则跟随Task的生命周期
- 特效材质：屏幕特效材质
- 自定义参数列表（对应材质内的参数）：
	- 标量：对应材质的Alpha数值（用于修改透明度）
	- 颜色：对应材质中color的RGBA通道（用于修改颜色）
	- 纹理：对应材质的纹理贴图

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rwAb0image.png)

此示例在风暴特效材质的基础上添加了标量、颜色、纹理自定义参数：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hwgqeimage.png)

自定义参数后的效果：

![2026-01-1616-33-33-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vBjHE2026-01-1616-33-33-ezgif.com-video-to-gif-converter.gif)

---

### 技能Task-生成Actor

在指定的位置生成一个actor。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oIma2image.png)

- Actor类：生成的Actor蓝图类
- 生成目标：
  - 技能施法者：以施法者为中心位置生成
  - 全部技能Target：以技能选中的全部目标为中心生成，依赖前置 **``目标选择``** 类型Task的选取结果
  - 全部技能位置：以技能选中的全部位置点为中心生成，依赖前置 **``目标选择``** 类型Task的选取结果
- 偏移量：生成Actor基于中心位置的偏移

---

### 技能Task-生成法术场

生成一个指定类型的法术场对象。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hLl03image.png)

- 法术场类：目标 [法术场](https://developer.gp.qq.com/wikieditor/#/catalog/20217) 蓝图类
- 生成目标：法术场生成位置的类型
	- 技能施法者：以施法者为中心位置生成
 	- 全部技能Target：以技能选中的全部目标为中心生成，依赖前置 **``目标选择``** 类型Task的选取结果
 	- 全部技能位置：以技能选中的全部位置点为中心生成，依赖前置 **``目标选择``** 类型Task的选取结果
- 偏移量：生成位置的偏移量
- 执行间隔覆盖：法术场的执行间隔覆盖值，若为-1则不覆盖
- 持续时间覆盖：法术场的持续时间覆盖值，若为-1则不覆盖

---

### 技能Task-生成怪物

在指定的位置生成一个怪物。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mnZEXimage.png)

- Monster类：生成怪物的蓝图类
- 生成目标：生成怪物的基准位置
	- 技能施法者：以施法者为中心位置生成
  - 全部技能Target：以技能选中的全部目标为中心生成，依赖前置 **``目标选择``** 类型Task的选取结果
  - 全部技能位置：以技能选中的全部位置点为中心生成，依赖前置 **``目标选择``** 类型Task的选取结果
- 偏移量：怪物生成位置的偏移量
- 是否将施法者仇恨目标设置为初始目标：仅施法者为怪物时生效，若勾选，会将施法者当前的仇恨目标同步给生成的怪物

---

### 技能Task-生成粒子

生成一个特效，并挂载到对应目标的指定位置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3fpXwimage.png)

- 粒子模板：引用的特效资源
- 是否强引用资源：特效资源的引用方式，建议勾选
- 生成目标：
	- 技能施法者：在施法者身上生成特效
	- 全部技能Target：在选中的全部目标上生成特效，依赖前置 **``目标选择``** 类型Task的选取结果
	- 全部技能位置：在选中的全部目标点上生成特效，依赖前置 **``目标选择``** 类型Task的选取结果
- Socket：基于该挂点的位置生成且挂载在该挂点上跟随运动，支持按 ``部位类型`` 或者 ``插槽名称`` 挂点
- Offset：生成的特效基于生成目标的挂点的偏移
- 缩放规则：
  - 保持相对缩放：继承挂接目标的缩放比例
  - 保持绝对缩放：维持自身的原始缩放比例，不受目标影响

---

### 技能Task-切换人称

切换施法者的视角至目标视角，仅对主角生效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/80FdRimage.png)

- 要切换到的人称：目标人称视角，第一/三人称
- 强制切换：勾选了强制切换后，在禁用了 ``PawnState.SwitchPP`` 状态的情况下也依然生效

<br>

## 武器

### 技能Task-自动瞄准

当玩家手持枪械武器时，激活该Task将自动锁定 **人形骨骼** 目标并瞄准距离最近的敌方角色。

![dd.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/f2lnCdd.gif)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/R6p2iimage.png)

- Can Aim NPC：是否能自动瞄准怪物，否则只会自瞄角色Pawn
- 自瞄速度倍率：生效自瞄时，自动瞄准到目标的吸附速度倍率。
- 自瞄范围倍率：自瞄功能有效作用范围的倍率。

<br>

## 背包

### 技能Task-背包操作

执行一次指定的背包操作。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TYdeWimage.png)

- Operator Type：背包操作类型。支持添加、销毁、使用、丢弃。
- 物品ID：进行操作的物品ID，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- 数量：进行操作的物品数量，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- 是否弹Tips：进行该背包操作时，是否会弹tips
- 是否强制操作：进行该背包操作时，是否强制执行，可能会中断当前的常规背包操作行为

<br>

## 技能

### 技能Task-释放技能

释放指定技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5Jh4Bimage.png)

- 技能槽位：[虚拟技能槽](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE)，将触发该槽位上绑定的技能

---

### 技能Task-返还CD

执行一次性的CD/能量返回（不超过上限），例如返回比率0.5，则一次性返回50%的能量。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/y9ePsimage.png)

- 返回数额：要返回多少数值的CD/能量
- 返还类型：
    - 比例：该数值表示一个相对比例，取值范围0~1
    - 绝对值：该值对应一个绝对值，取值范围0~+∞
- 返回CD的技能槽位：指定需要刷新返回时间的技能槽位，若不指定则默认为当前技能

---

### 技能Task-消耗

执行一次自定义的消耗，在Task开始时执行技能消耗，在Task结束时执行技能CD。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cnZMcimage.png)

- 执行CD：是否执行技能CD
- 每次/每秒消耗能量百分比：配置小于0的值时，依据 [技能基础属性](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 中配置的CD/能量消耗执行；否则按覆盖的百分比进行消耗
- 能量类型CDTask执行期间持续消耗：仅对能量CD类型的技能有效，勾选后，在该Task执行期间持续进行消耗；否则为一次性消耗
- 执行消耗：是否执行属性消耗和物品消耗
- 消耗属性列表：如果不配置，则以 [技能基础属性](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 中配置的消耗属性进行消耗；否则以覆盖的配置消耗
- 消耗物品列表：如果不配置，则以 [技能基础属性](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 中配置的消耗物品进行消耗；否则以覆盖的配置消耗

---

### 技能Task-近战攻击

执行该Task时，进行一次近战攻击行为的攻击盒检测，若检测到目标，则对目标造成伤害以及受击效果。不同于普通的选取类Task，该Task的选取区域绑定指定盒体且跟随动画运动，适用于需要精确表现的技能检测。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Ob8J1image.png)

- 阵营过滤：攻击允许命中目标的阵营筛选
- 攻击盒类型：支持自定义攻击盒与绑定武器攻击盒组件
	- 无效：不进行攻击检测
	- 读取角色Socket位置的攻击盒参数：自定义配置攻击盒的位置与大小，需要绑定指定的骨骼插槽，可以通过多组盒子拼接出异形的检测区域
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mRX1oimage.png)
		- 攻击盒挂接的Socket：攻击盒被挂接的角色骨骼Socket位置，攻击盒将基于该插槽随动画运动，骨骼Socket位置可参考Pawn骨骼树的结构
		![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RZRNNimage.png)
		- 攻击盒挂接的位置偏移：攻击盒基于Socket的位置偏移
		- 攻击盒挂接的旋转偏移：攻击盒基于Socket的旋转偏移
		- 攻击盒的尺寸：攻击盒的大小
	- 读取武器上的攻击盒组件：攻击盒将通过自动读取武器上配置的带有特殊Tag的Box组件决定，这种情况下该Task必须作为武器的攻击技能配合使用
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eQjsRimage.png)
- Melee Attack Track Type：近战攻击的检测方式
	- 离线曲线：采用动画离线曲线导出，最终的检测盒轨迹是稳定不变的，默认推荐使用此方式
	- 实时检测：近战攻击的检测轨迹基于绑定插槽（socket）的实时位置进行检测，因此检测盒的轨迹是动态变化的，适用于单阶段多种攻击类型动画的场景
- 伤害类型Tag列表：当检测到当前攻击能够造成伤害时，为该伤害添加指定的 [GameplayTag标签](https://developer.gp.qq.com/wikieditor/#/catalog/20102)
- DamageValue：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 伤害校验配置：用于作为反外挂作用的服务器校验相关配置项，如无特定需求，保持默认即可
	- 是否进行敌我双方的障碍物检测：是否需要校验敌我双方不被障碍物阻挡才合法
	- 每次伤害的距离校验偏移值：伤害检测判定到位置和实际位置的有效容差值
	- 每次伤害的有效期：每次伤害实际发生和检测发生时间的有效容差值
- 是否启用受击效果：是否启用受击效果，如果启用需要配置 [受击数据](https://developer.gp.qq.com/wikieditor/#/catalog/20169)，造成伤害时会对目标执行对应的受击效果
- 受击效果资产：受击效果的数据资产蓝图
- 顿帧：近战攻击命中生效的顿帧效果，即命中后将使得自身的技能动画速率变慢持续一段时间以模拟命中的卡肉效果
	- PlayRate：顿帧的动画播放速率
	- Duration：顿帧效果的持续时间

> 顿帧效果为客户端模拟效果，不会实际影响服务器实际Sequence的执行时间，所以如果服务器上Sequence提前结束，会打断相应的顿帧效果和动画，故而不建议使用太长时间的顿帧效果，避免出现动画后摇的表现异常问题

---

### 技能Task-阶段跳转

在task执行的过程中，持续监听事件，一旦检测到符合条件，跳转至预定义的对应阶段。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fszjnimage.png)

- 事件：要监听的 [事件](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20112)，多组事件之间为“或”的关系
- 条件：如果监听事件触发，跳转还需满足的 [条件](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20111)，事件与条件之间为“且”的关系
- StateName：跳转的目标 [阶段](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E9%98%B6%E6%AE%B5%E9%85%8D%E7%BD%AE)

<br>

## 自定义

### 技能Task-Lua自定义

该Task将绑定一个Lua脚本，Task执行时会调用该脚本的各模板函数，以支持扩展实现Task的功能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ovqZVimage.png)

- Lua脚本路径：以Script为根目录的脚本路径，路径形式如 ``Script.Blueprint.NewLua``

脚本默认生成的模板函数如下：

```lua
local TestCustomLua = {}

-- 该Task初始化时调用,即Task获取到SkillOwner,即该Task所属Section触发时调用
function TestCustomLua:InitTask_BP()
end

-- 该Task是否支持RPC
function TestCustomLua:TaskSupportRPC_BP()
  return false
end

-- 当该Task被激活时调用
function TestCustomLua:OnActivate_BP()
end

-- 当该Task被反激活时调用
function TestCustomLua:OnDeactivate_BP()
end

-- 当该Task被Trigger时调用，Trigger的间隔由Task配置的间隔决定
function TestCustomLua:OnTrigger_BP(Delta)
end
```

<br>

## 通用

### 技能Task-动态状态变化

执行该Task时，将为施法者附加基于 [状态互斥](https://developer.gp.qq.com/wikieditor/#/catalog/20106) 规则的约束效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fL6Y8image.png)

- 阻碍Tag：当目标身上携带该Tag时，此技能将被中断
- 拥有Tag：激活技能Task后，自动为目标添加Tag，如果存在禁用该Tag的设定，则此技能将被中断
- 打断Tag：激活技能Task后，会执行打断的Tag，如果目标拥有这些Tag，则Tag关联的技能/Buff都将被打断/移除
- 禁用Tag：激活技能Task后，会执行禁用的Tag，如果目标拥有这些Tag，则Tag关联的技能/Buff都将被打断/移除，且拥有这些Tag的技能或Buff无法被再次添加给目标

---

### 技能Task-调用Lua脚本

在指定的时机执行自定义的Lua脚本函数逻辑。

>【周期性Task】每隔 ``Interval`` 触发一次Trigger函数

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/55rLHimage.png)

- ActivateFunction：该技能Task激活时，执行的lua函数
- DeactivateFunction：该技能Task结束时，执行的lua函数
- TriggerFunction：每隔 ``Interval`` 执行的lua函数

<br>

## 输入

### 技能Task-缓存输入

执行该Task期间，阻挡并缓存指定的输入指令；并在Task结束时，触发还未过期且优先级最高的输入指令，支持同时缓存多种指令。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GJ5rUimage.png)

- 输入映射：要缓存的输入指令，基于 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20099) 表示，例如 ``Input.Skill.Slot0`` 代表触发 ``Slot0`` 虚拟技能槽位的输入指令
- 优先级：缓存指令的执行优先级，值越大优先级越高
- 缓存有效时间：输入指令的有效缓存时间

缓存输入功能适合应用在技能释放过程中需要响应输入，并对技能结果执行相应变更的场景中。以连段型技能举例，通常在技能中的某个时间窗口监听玩家输入，以此决定是否触发下一阶段的技能效果，即Combo时间窗口，但是玩家的输入操作一般不精确，从而容易导致触发结果不符合预期。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9FSbRimage.png)

为了给与一定的时间补偿上的宽容度，可以使用缓存输入的方式来解决，提前缓存技能的输入指令，就能够在阶段跳转前进行输入的精准判定。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/h0FQUimage.png)

<br>

## 抛体

### 技能Task-发射抛体

根据指定方向发射抛射物，例如魔法飞弹。
> 【周期性Task】每隔 ``Interval`` 发射一次抛体

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YSQI2image.png)

- 抛体类：指定的 [技能抛体](https://developer.gp.qq.com/wikieditor/#/catalog/20093) 蓝图
- 发射方向类型：非“角色前向”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 角色前向：抛体沿角色当前朝向的正前方发射
	- 技能选中方向/目标/位置：抛体朝向选取的方向/目标/位置结果
- Socket：发射抛体的位置可以额外基于施法者身上的一个挂点位置进行计算（仅当该发射抛体的位置来源类型为技能施法者自身时生效）
- 位置来源类型：该抛体发射的起点位置类型，非“技能施法者”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 技能选择目标：以技能选取的全部目标位置作为抛体发射起点
	- 技能选取点位：以技能选取的全部坐标位置作为抛体发射起点
	- 技能施法者：以技能施法者自身位置作为抛体发射起点
	- 客户端枪口位置：以主控端枪口的位置作为抛体发射起点
- 偏移量：最终发射位置相对起点位置的偏移
- 覆写抛体速度及重力系数：若勾选，可设置速度与重力系数的覆盖值；否则，使用抛体蓝图的属性值
	- Speed：技能发射抛体的初速度，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
	- 抛体重力系数：技能发射抛体的重力系数，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- 覆写抛体伤害：若勾选，可设置伤害相关的覆盖值；否则，使用抛体蓝图的属性值
	- 伤害值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
	- 伤害类型Tag列表：支持为抛体命中伤害设置多种Tag，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20102) 创建
- 发射数量：发射抛体的数量，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- 随机发射角度限制：发射抛体允许随机偏移的最大角度
- 随机发射位置偏移范围：发射抛体的随机起点偏移角度

> 属性绑定数据类型：float

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/knaVyimage.png)

> 属性绑定数据类型：AUniversalProjectileCore

当 ``发射方向类型`` 为 ``选中目标`` 发射抛体的时候，还需要配置两个额外参数：

该配置对应了一组最终发射方向分别可以和人物形成的横滚角、俯仰角、偏航角的最大限制，如果超过了该限制，只会修正到朝最大限制的方向发射抛体，避免出现比如玩家几乎在怪物垂直下方，怪物做了一个向前的动作，抛体却在垂直向下打得情况。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/B5zNEimage.png)

---
	
### 技能Task-修改抛体
	
针对 ``抛体列表`` 中绑定的抛体实例执行一组抛体修改器的效果。
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HDRjKimage.png)
	
- 抛体列表：通过 [属性求值器](https://developer.gp.qq.com/wikieditor/#/catalog/20108?autoJump=%E4%BD%BF%E7%94%A8%E5%B1%9E%E6%80%A7%E6%B1%82%E5%80%BC%E5%99%A8) 绑定的抛体蓝图变量，数据类型为 ``AUniversalProjectileCore``
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QGb9Limage.png)
- 修改器列表：等效于一组 [抛体修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20165?autoJump=%E6%8A%9B%E4%BD%93%E4%BF%AE%E6%94%B9%E5%99%A8)

<br>

## 属性

### 技能Task-角色修改属性

修改施法者自身的指定属性值，遵循 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的计算方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PLwp8image.png)

- 目标类型：
	- 技能施法者：施法者自身
	- 全部技能Target：给技能选中的目标修改属性，依赖前置 **``目标选择``** 类型Task的选取结果
- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：预置血量、能量、信号等和平角色的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20153?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自选取的技能目标，若选中多个目标，则分别取各目标的属性独立计算，依赖前置 ``目标选择`` 类型Task的选取结果

> - ``是否同步客户端`` 保持默认勾选
> - 属性绑定数据类型：float

---

### 技能Task-下一次<伤害>属性修改

基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的属性修改行为，临时修改施法者自身的指定属性值，当下一次受到任意伤害时（触发 [伤害公式](https://developer.gp.qq.com/wikieditor/#/catalog/20099)），自动移除相关修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VAgKIimage.png)

- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：支持和平角色与枪械的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20153?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自选取的技能目标，若选中多个目标，则分别取各目标的属性独立计算，依赖前置 ``目标选择`` 类型Task的选取结果

> - ``目标属性公式`` 为预留项，保持 ``None``
> - ``是否同步客户端`` 保持默认勾选
> - 该Task为临时修改含义，因此 ``永久修改`` 不适用
> - 属性绑定数据类型：float

---

### 技能Task-下一次<治疗>属性修改

基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的属性修改行为，临时修改施法者自身的指定属性值，当下一次受到治疗时（触发 [治疗公式]()），自动移除相关修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0NhBrimage.png)

- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：支持和平角色与枪械的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20153?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自选取的技能目标，若选中多个目标，则分别取各目标的属性独立计算，依赖前置 ``目标选择`` 类型Task的选取结果

> - ``目标属性公式`` 为预留项，保持 ``None``
> - ``是否同步客户端`` 保持默认勾选
> - 该Task为临时修改含义，因此 ``永久修改`` 不适用
> - 属性绑定数据类型：float

---

### 技能Task-武器属性修改

修改施法者自身武器的指定属性值，遵循 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的计算方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SmFqLimage.png)

- 目标类型：
	- 技能施法者：施法者自身
	- 全部技能Target：给技能选中的目标修改属性，依赖前置 **``目标选择``** 类型Task的选取结果
- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：预置和平枪械的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20153?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于自定义属性的 [计算公式](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%AE%A1%E7%AE%97%E5%85%AC%E5%BC%8F) 或者 [指定Lua函数](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E6%8C%87%E5%AE%9ALua%E5%87%BD%E6%95%B0) 的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自选取的技能目标，若选中多个目标，则分别取各目标的属性独立计算，依赖前置 ``目标选择`` 类型Task的选取结果

> - ``是否同步客户端`` 保持默认勾选
> - 属性绑定数据类型：float

<br>

## UI

### 技能Task-修改技能UI信息

覆盖技能UI上的指定参数和外显效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JOIwVimage.png)

- 图标：覆盖的技能图标
- 技能名称：覆盖的技能名称
- 技能描述：覆盖的技能描述

---

### 技能Task-显示取消按钮

执行该Task时，将显示技能的取消按钮，点击取消按钮，则可以主动取消该技能。
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UZnpjimage.png)
	
- 取消按钮自定义描述：未配置时显示默认值“取消释放”，若已配置时则使用该配置字符串进行显示
- Cancel Action：
   - 直接取消技能：结束技能流程，跳转End阶段
   - 仅发送取消事件： 不直接结束技能，触发状态图中的技能取消状态和事件
- 取消按钮UI：支持自定义取消按钮控件的样式
 
---

### 技能Task-显示UI

执行该Task时，将按配置显示一个UI效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pbYgIimage.png)

- UISlot Name：按 [和平控件锚点](https://developer.gp.qq.com/wikieditor/#/catalog/20097) 挂载UI的位置
- ZOrder：渲染所选控件时的顺序优先级，值越大，渲染越晚，最晚的显示在顶部；反之亦然
- Anchor Data：控件的 [布局数据](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/umg-slots-in-unreal-engine?application_version=5.5)
- UI类：指定的控件蓝图

---

### 技能Task-进度条UI

执行该Task时，将按配置显示一个进度条UI的效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/B6mK6image.png)

- PESkill Task Progress UIType：进度条的样式，目前支持 ``进度条`` 和 ``倒计时`` 两种
	- 倒计时样式：居于中心的倒计时圈，类似使用和平药品的效果
	- 进度条样式：位于屏幕中心下方的长条，类似蓄力进度条效果
	![ezgif-80f63eb8efda51.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SXf3Mezgif-80f63eb8efda51.gif)
- Duration：进度条的持续总时长
- 描述文本：当选择 ``倒计时样式`` 时生效，为倒计时圈中心的描述文本
- UISlot：该进度条UI的挂点位置配置
	- UISlot Name：按 [和平控件锚点](https://developer.gp.qq.com/wikieditor/#/catalog/20097) 挂载UI的位置
	- ZOrder：渲染所选控件时的顺序优先级，值越大，渲染越晚，最晚的显示在顶部；反之亦然
	- Anchor Data：控件的 [布局数据](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/umg-slots-in-unreal-engine?application_version=5.5) 
- CustomUserWidgetPath：在显示对应的UI实例时，会使用该控件蓝图进行创建（当启用自定义样式时，需要额外配置一个UI控件蓝图）
- PESkill Task Progress Config：进度条百分比及显示颜色的映射关系配置，例如下图效果为20%进度以内显示蓝色，超过50%时显示红色
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PsJKeimage.png)

---

### 技能Task-显示Tips

执行该Task时，屏幕中间显示指定的Tips字符效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xBEZKimage.png)

> 目前仅支持字符串类型的文本

<br>

## 选取

### 技能Task-选择点

运行时根据摄像机瞄准方向动态选择一个目标位置。
> 【周期性Task】每隔 ``Interval`` 执行一次选取点位

**单点选取器**

以摄像机命中位置进行一次点位选取，只会选取到一个位置。
> ``PESkillPickerBase`` 的属性对该类型选择器不适用，即单点选取器不支持变更颜色

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oVqw3image.png)

- 最大选取距离：选到的点位和施法者的最大距离
- 是否忽略重叠：若选取的点位位于阻挡物上，则被视为非法点，无法选择，若启用忽略重叠选项后，系统将忽略重叠类型的碰撞；否则，指定过滤器的方式决定可阻挡目标
- 目标区域类型：绘制的指示器区域类型
	- 圆形区域：默认以圆形绘制
   		- 选取器半径：圆形半径 
 	- 骨骼Mesh/静态Mesh：使用选取的骨骼/静态Mesh为区域选择形状
   		- MeshScale：Mesh的缩放比例
- Overlap检测实体类型：指定允许重叠检测的 [实体类型](https://developer.gp.qq.com/wikieditor/#/catalog/20298)，当不忽略重叠时生效
- 碰撞检测Actor过滤器：支持 [过滤器](https://developer.gp.qq.com/wikieditor/#/catalog/20218) 的方式筛选重叠阻挡目标，当不忽略重叠时生效
- 最大坡度限制：若目标位置坡度超过设定值，则点位选取无效

---

**多点目标选择器**

以选取点为圆心，在周围圆环区域内生成多个点位。系统会进行多次尝试，直到达到所需数量；若尝试次数用尽仍未满足条件，实际生成的点位数量可能少于预期。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qXmOQimage.png)

- 位置来源类型：
   - 技能选择的目标：以技能选择的第一个目标为中心，生成点位
   - 技能选择的位置：以技能选取的第一个点位为中心，生成点位
   - 技能施法者自身：以技能施法者自身为中心，生成点位
   - 客户端枪口位置：以主控端枪口的位置为中心，生成点位
- Offset：选取中心的偏移
- 最小距离：选取圆环区域的最小半径
- 最大距离：选取圆环区域的最大半径
- 最小选取数量：随机选取点位数量的最小值
- 最大选取数量：随机选取点位数量的最大值
- 是否忽略重叠：若选取的点位位于阻挡物上，则被视为非法点，无法选择，若启用忽略重叠选项后，系统将忽略重叠类型的碰撞；否则，指定过滤器的方式决定可阻挡目标
- 碰撞检测Actor过滤器：支持 [过滤器](https://developer.gp.qq.com/wikieditor/#/catalog/20218) 的方式筛选重叠阻挡目标，当不忽略重叠时生效
- 是否显示选取范围：仅PIE生效。是否需要在PIE下看到选取范围的指示器框
- 胶囊半径：用于选点时检测碰撞判定的范围，同时也是圆形指示器的绘制半径
- 是否检查和中心阻挡性：若启用，选取的点位必须与中心点之间无遮挡，才会被视为合法点
- 目标点平面的最大检测高度：选到点所处平面的最大坡度限制，超出则被认为是非法点
- 目标点平面的最大倾斜角度：该命中点位所处位置的最大坡度限制，超过该坡度时，选取点位非法
- 是否自动吸附至Navmesh：选点将根据配置的目标点位吸附至最近的NavMesh表面。若目标点位超出预设吸附半径范围，系统将保持原始坐标位置，但仍可正常完成点位选取操作。
>若勾选，则必须配置 [导航网格](https://developer.gp.qq.com/wikieditor/#/catalog/177?autoJump=%E5%AE%9E%E6%88%98)，否则将无法进行选点
- 吸附Navmesh半径：吸附Navmesh的检查半径
- 选取最大尝试次数：选点进行尝试选取的最大尝试次数
- 颜色：该选点指示器的颜色，指示器将绘制在最终选出的点位上，例如若选出5个点位，则会在每个点位上分别绘制一个圆形指示器
- 反向：绘制指示器特效的进度提示的方向，是否中心点向外扩展或由外向中心点汇聚
- 可见性：
	- 仅自己可见：指示器仅对当前玩家可见
	- 全局可见：指示器对所有玩家可见
	- 不可见：不绘制指示器
- 指示器类型：
	- 瞬时型：点位在初始阶段选取，绘制的指示器特效不显示进度提示
	- 进度型：点位在初始阶段选取，绘制的指示器特效显示进度提示，进度值为Task已执行时间与总时间的比值
	
---
	
**右摇杆选点**
	
执行时，点击技能UI的触控位置会额外显示一个右摇杆用于位置选取，右摇杆的轴位置最终会映射到实际场景里的3D位置，并作为最终的选取位置。
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/a2BKdimage.png)
	
- JoyStickRangeRadius：摇杆选取区域大小，选到的点位和施法者的最大距离，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- Rotate to Joystick：在选取过程中，角色的朝向是否始终朝向摇杆所选位置
- IgnoreOverlap：若选取的点位位于阻挡物上，则被视为非法点，无法选择，若启用忽略重叠选项后，系统将忽略重叠类型的碰撞；否则，指定过滤器的方式决定可阻挡目标  
- Target Area Type：绘制的指示器区域类型
	- 圆形区域：默认以圆形绘制
   		- Radius：选取目标位置半径区域大小。对应摇杆选取位置特效的半径大小，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 
 	- 骨骼Mesh/静态Mesh：使用选取的骨骼/静态Mesh为区域选择形状
   		- MeshScale：Mesh的缩放比例
- MaxSlopeAngle：若目标位置坡度超过设定值，则点位选取无效

<br>

### 技能Task-选择方向

运行时根据摄像机瞄准方向动态选择一个目标方向。
> 【周期性Task】每隔 ``Interval`` 执行一次选取方向

**摇杆方向选取器**

将施法者当前的摇杆输入换算成世界坐标方向后，将该方向归一化后的向量作为选取方向。
> ``PESkillPickerBase`` 的属性对该类型选择器不适用

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jrz1rimage.png)

---
 
 **矩形方向选取器**
 
以技能施法者的角色前向为选取方向，并沿此方向生成对应的矩形指示器特效。
> 矩形相关参数仅作用于指示器的效果绘制，不会对实际的选取结果产生任何影响
 
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dSFSximage.png)
 
- offset：绘制的指示器特效相对技能施法者的偏移
- 宽度：矩形指示器特效的宽度
- 长度：矩形指示器特效的长度
- 颜色：绘制的指示器特效的颜色。
- 反向：绘制的指示器特效的进度提示的方向，是否中心点向外扩展或由外向中心点汇聚
- 可见性：
  - 仅自己可见：指示器仅对施法者自身可见
  - 全局可见：指示器对所有玩家可见
  - 不可见：不绘制任何指示器效果
- 指示器类型：
   - 瞬时型：指示器的目标点位在初始时刻即完成选取，绘制的指示器特效不包含进度提示
   - 进度型：指示器的目标点位在初始时刻完成选取，绘制的指示器特效包含进度提示，其进度值为 ``Task已执行时间`` / ``Task总时间``

---

**抛物线方向选择器**
 
以玩家当前视角的方向为基准，确定目标选取方向，并沿此方向生成对应的抛物线轨迹指示器特效。
> - 抛物线相关参数仅作用于指示器的效果绘制，不会对实际的选取结果产生任何影响
> - ``PESkillPickerBase`` 属性组对该类型选择器不适用

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MMoMqimage.png)

- DirectionType：该抛物线方向选取器的选取方向类型
    - 相机方向：以摄像机朝向方向为基准进行选取
    - 准星方向：以选择器起点指向准星命中位置的向量作为其方向
- 位置偏移类型：
   - 角色位置：以角色为中心作为偏移起点
   - 枪口位置：选取器以枪口位置作为偏移起点
- 偏移：指示器特效相对施法者的偏移量 
- 重力系数：该抛物线的重力系数。
- 抛射速度：该抛物线发射的初速度，和 ``重力系数`` 共同影响抛物线的最远距离

---
	
**右摇杆方向选择器**

执行时，点击技能UI的触控位置会额外显示一个右摇杆用于方向选取，右摇杆的轴位置最终会映射到实际场景里的3D位置，并用该位置减去玩家位置最终得出选取的方向向量。
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cjw4Rimage.png)
	
- JoyStickRangeRadius：摇杆选取区域大小，选到的点位和施法者的最大距离，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- DirectionType：指示器样式
	- 箭头方向：以箭头形状绘制选取区域
		- Width：箭头指示器的宽度，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
	- 扇形方向：以扇形形状绘制选取区域
		- Half Angle：扇形指示器的半角角度，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- Rotate to Joystick：在选取过程中，角色的朝向是否始终朝向摇杆所选位置

<br>

### 技能Task-选择目标

以指定形状的指示器对选择区域内的所有游戏实例进行扫描，并筛选出符合条件的合法目标作为选取对象。
> 【周期性Task】每隔 ``Interval`` 执行一次选择目标

**扇形目标选取器**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SjYFJimage.png)

- Radius：扇形区域的半径
- Angle：扇形区域的角度
- 高度：该扇形区域的检查高度，限制可检查的游戏实例与检查中心点之间的最大高度差
- 最大数量：至多能选取到多少个目标，-1代表无限制
- 排序类型:
	- 随机排序：对选取到的目标进行随机排序
	- 距离排序：根据目标与施法者之间的距离排序，距离越近的目标越靠前
	- 角度排序：根据目标与施法者之间的角度排序，角度越小的目标越靠前
- 阵营过滤：选中指定阵营关系的目标，支持多选，阵营的概念可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)
	- Same：友方
	- Enemy：敌方
	- Neutral：中立
- 选取目标需要是否可见：如果勾选，目标需要可见才会被选取
- Transform Source Type：该选取区域的起点位置类型，非“释放者自身”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 技能释放者自身：扇形区域以施法者为中心
	- 技能选择的位置：扇形区域以选中的目标位置为中心
	- 技能选择的目标：扇形区域以选择的第一个目标为中心
- Offset：选取区域相对起点位置的偏移
- 颜色：绘制的指示器特效的颜色。
- 反向：绘制的指示器特效的进度提示的方向，是否中心点向外扩展或由外向中心点汇聚
- 可见性：
  - 仅自己可见：指示器仅对施法者自身可见
  - 全局可见：指示器对所有玩家可见
  - 不可见：不绘制任何指示器效果
- 指示器类型：
   - 瞬时型：指示器的目标点位在初始时刻即完成选取，绘制的指示器特效不包含进度提示
   - 进度型：指示器的目标点位在初始时刻完成选取，绘制的指示器特效包含进度提示，其进度值为 ``Task已执行时间`` / ``Task总时间``

---

**矩形目标选取器**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wdKzeimage.png)

- 选取器宽度：选取矩形区域的宽度
- 选取器长度：选取矩形区域的长度
- 选取器高度：选取到的游戏实例和选取起点的最大高度差
- 最大数量：至多能选取到多少个目标，-1代表无限制
- 选取目标排序类型:
	- 随机排序：对选取到的目标进行随机排序
	- 距离排序：根据目标与施法者之间的距离排序，距离越近的目标越靠前。
	- 角度排序：根据目标与施法者之间的角度排序，角度越小的目标越靠前。
- 阵营过滤：选中指定阵营关系的目标，支持多选，阵营的概念可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)
	- Same：友方
	- Enemy：敌方
	- Neutral：中立
- 是否需要可见：如果勾选，目标需要可见，才会被选取。
- 位置来源类型：该选取区域的起点位置类型，非“释放者自身”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 技能释放者自身：扇形区域以施法者为中心
	- 技能选择的位置：扇形区域以选中的目标位置为中心
	- 技能选择的目标：扇形区域以选择的第一个目标为中心
- 偏移量：选取区域相对起点位置的偏移
- 颜色：绘制的指示器特效的颜色。
- 反向：绘制的指示器特效的进度提示的方向，是否中心点向外扩展或由外向中心点汇聚
- 可见性：
  - 仅自己可见：指示器仅对施法者自身可见
  - 全局可见：指示器对所有玩家可见
  - 不可见：不绘制任何指示器效果
- 指示器类型：
   - 瞬时型：指示器的目标点位在初始时刻即完成选取，绘制的指示器特效不包含进度提示
   - 进度型：指示器的目标点位在初始时刻完成选取，绘制的指示器特效包含进度提示，其进度值为 ``Task已执行时间`` / ``Task总时间``
- Custom Picker Preview Actor Class：在选取器激活时，为其指定一个用于视觉预览的Actor
  
---
	
**球形目标选择器**
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Q7lMhimage.png)
	
- 球形选取半径：球形范围的半径。
- 最大数量：至多能选取到多少个目标，-1代表无限制
- 选取目标排列类型:
	- 随机排序：对选取到的目标进行随机排序
	- 距离排序：根据目标与施法者之间的距离排序，距离越近的目标越靠前。
	- 角度排序：根据目标与施法者之间的角度排序，角度越小的目标越靠前。
- 阵营过滤：选中指定阵营关系的目标，支持多选，阵营的概念可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)
	- Same：友方
	- Enemy：敌方
	- Neutral：中立
- 是否需要可见：如果勾选，目标需要可见，才会被选取。
- 位置来源类型：该选取区域的起点位置类型，非“释放者自身”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 技能释放者自身：球形区域以施法者为中心
	- 技能选择的位置：球形区域以选中的目标位置为中心
	- 技能选择的目标：球形区域以选择的第一个目标为中心
	- 客户端枪口位置：球形区域以角色枪口位置作为起点。
- 偏移量：选取区域相对起点位置的偏移
- 颜色：绘制的指示器特效的颜色。
- 反向：绘制的指示器特效的进度提示的方向，是否中心点向外扩展或由外向中心点汇聚
- 可见性：
  - 仅自己可见：指示器仅对施法者自身可见
  - 全局可见：指示器对所有玩家可见
  - 不可见：不绘制任何指示器效果
- 指示器类型：
   - 瞬时型：指示器的目标点位在初始时刻即完成选取，绘制的指示器特效不包含进度提示
   - 进度型：指示器的目标点位在初始时刻完成选取，绘制的指示器特效包含进度提示，其进度值为 ``Task已执行时间`` / ``Task总时间``

---

**右摇杆目标选择器**

执行时，点击技能UI的触控位置会额外显示一个右摇杆用于目标选取，右摇杆的轴位置最终会映射到实际场景里的3D位置，并基于该位置为中心进行目标的选取。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YOm5nimage.png)
	
- JoyStickRangeRadius：摇杆选取区域大小，选到的点位和施法者的最大距离，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- Range Radius：选取目标位置半径区域大小，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- Range Height：选取到的游戏实例和最终落点的最大高度差，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- Rotate to Joystick：在选取过程中，角色的朝向是否始终朝向摇杆所选位置
- 最大数量：至多能选取到多少个目标，-1代表无限制
- 选取目标排列类型:
	- 随机排序：对选取到的目标进行随机排序
	- 距离排序：根据目标与施法者之间的距离排序，距离越近的目标越靠前
	- 角度排序：根据目标与施法者之间的角度排序，角度越小的目标越靠前
	- 自定义： 在技能蓝图lua中写入自定义函数并替换到``SortFunction``选项上，自定义函数中只有两个回调参数，结果取决于 ``目标选择``的结果
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bNSqXimage.png)

按距离排序选敌代码示例：
``` lua
function MySkill:MyCustomFunction(FirstGoal, SecondGoal)
    local Owner = self:GetNetOwnerActor()
    local FirstGoalDist = STExtraBlueprintFunctionLibrary.Dist(Owner:K2_GetActorLocation(),
        FirstGoal:K2_GetActorLocation())   --判断第一个目标与技能释放者的距离
    local SecondGoalDist = STExtraBlueprintFunctionLibrary.Dist(Owner:K2_GetActorLocation(),
        SecondGoal:K2_GetActorLocation())  --判断第二个目标与技能释放者的距离
    if FirstGoalDist > SecondGoalDist then --第一个目标与释放者的距离大于第二个目标与释放者的距离优先级不变
        return true
    end
		
    return false --如果小于则让第二个目标优先被选中
end
```
- 阵营过滤：选中指定阵营关系的目标，支持多选，阵营的概念可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)
	- Same：友方
	- Enemy：敌方
	- Neutral：中立
- 是否需要可见：如果勾选，目标需要可见才会被选取
- 位置来源类型：该选取区域的起点位置类型，非“释放者自身”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 技能释放者自身：摇杆出发点以施法者为中心
	- 技能选择的位置：摇杆出发点以选中的目标位置为中心
	- 技能选择的目标：摇杆出发点以选择的第一个目标为中心
	- 客户端枪口位置：摇杆出发点以角色枪口位置作为起点
- 偏移量：选取区域相对起点位置的偏移

---

**瞄准目标选择器**
	
以屏幕中心发射射线进行检测，将命中的目标作为最终选取的目标。
	
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/G1mJhimage.png)
	
- Trace Distance：射线检测的最大有效距离，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- Sweep Sphere Radius：检测射线的体积半径大小，射线路径上在此半径范围内的所有物体均会被视为命中
- 最大数量：至多能选取到多少个目标，-1代表无限制
- 选取目标排列类型:
	- 随机排序：对选取到的目标进行随机排序
	- 距离排序：根据目标与施法者之间的距离排序，距离越近的目标越靠前
	- 角度排序：根据目标与施法者之间的角度排序，角度越小的目标越靠前
	- 自定义： 在技能蓝图lua中写入自定义函数并替换到``SortFunction``选项上，自定义函数中只有两个回调参数，结果取决于 ``目标选择``的结果
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kfTfCimage.png)

按距离排序选敌代码示例：
``` lua
function MySkill:MyCustomFunction(FirstGoal, SecondGoal)
    local Owner = self:GetNetOwnerActor()
    local FirstGoalDist = STExtraBlueprintFunctionLibrary.Dist(Owner:K2_GetActorLocation(),
        FirstGoal:K2_GetActorLocation())   --判断第一个目标与技能释放者的距离
    local SecondGoalDist = STExtraBlueprintFunctionLibrary.Dist(Owner:K2_GetActorLocation(),
        SecondGoal:K2_GetActorLocation())  --判断第二个目标与技能释放者的距离
    if FirstGoalDist > SecondGoalDist then --第一个目标与释放者的距离大于第二个目标与释放者的距离优先级不变
        return true
    end

    return false --如果小于则让第二个目标优先被选中
end
```

- 阵营过滤：选中指定阵营关系的目标，支持多选，阵营的概念可参考 [队伍与阵营](https://developer.gp.qq.com/wikieditor/#/catalog/20095)
	- Same：友方
	- Enemy：敌方
	- Neutral：中立
- 是否需要可见：如果勾选，目标需要可见才会被选取
- 位置来源类型：该选取区域的起点位置类型，非“释放者自身”类型依赖前置 **``目标选择``** 类型Task的选取结果
	- 技能释放者自身：射线出发点以施法者为中心
	- 技能选择的位置：射线出发点以选中的目标位置为中心
	- 技能选择的目标：射线出发点以选择的第一个目标为中心
	- 客户端枪口位置：射线出发点以角色枪口位置作为起点
- 偏移量：选取区域相对起点位置的偏移

<br>

## 注意事项

绝大多数技能Task提供了选取目标的参数项，选取结果取决于 **``目标选择``** 类型的前置Task的执行结果，执行逻辑上应该遵循 ``选择目标 -> 执行对该目标的逻辑`` 的顺序，因此逻辑Task对选取Task具有时序依赖，在使用 ``目标选择`` 类型的技能Task时，一定要注意时间轴上执行的时机比逻辑Task更早，否则会出现逻辑已经开始执行但还没有目标的情况。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6sYRiimage.png)






---


## 被动技能

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 被动技能

**涉及API:** `BP_PoisonGas`, `ECA配置`, `OnMerge_BP`

# 被动技能

不同于依靠释放行为的主动技能，被动技能需要在特定的时机或者符合特定的条件时才能自动触发，因此无法通过时间轴的形式编排行为逻辑，技能编辑器针对被动技能设计了一套独立的框架，让开发者也能通过蓝图配置的方式实现完整的被动技能效果。

<br>

## 被动技能概述

### 实现机制

通常被动技能的执行时机基于事件驱动或者状态触发，前者属于主动通知，后者强调条件的成立。

- 事件驱动：通过监听特定事件来触发技能效果，具有明确的触发条件，例如：每次普通攻击减少某技能的1秒冷却时间，此时“普攻命中事件”即是触发条件。
- 状态触发：当目标对象处于特定状态下或者状态满足指定条件时触发技能效果，与事件触发的主动通知不同，状态触发依赖对状态的持续监测，例如：当玩家生命值低于20%时提升100%的攻击力，此时需要对玩家的生命值进行持续检测，一旦符合20%的条件即触发技能。

技能编辑器将被动技能的触发到执行的过程拆解为事件（Event）、条件（Condition）和行为（Action）三部分的组合结果。

**事件（Event）**

各类系统功能（如技能、Buff、武器等）在运行过程中产生的特定逻辑触发点，对应以“事件驱动”被动技能的触发，通常以事件作为触发前提。

**条件（Condition）**

条件是动作发生、事物存在或变化的充分必要因素，通常用来描述因果关系或推导关系，例如“状态触发”中玩家生命值低于20%即是触发条件。条件既可以单独作为被动技能触发的直接依据，也可以结合事件以确保触发的时机更加精确，例如：当玩家受到伤害且为暴击伤害时，触发血量恢复，此时“玩家受到伤害”为事件，“本次伤害为暴击伤害”为条件。

**行为（Action）**

行为即当被动技能触发时应该执行的动作，例如“恢复血量”即是一种行为，行为决定了被动技能的具体效果，可以是单一的动作也可以是一系列动作序列。

因此，通过事件、条件和行为的组合就能实现被动技能的触发机制和执行效果。

---

### 结构框架

技能编辑器提供了两种配置被动技能的结构框架：事件触发和状态触发。

#### 事件触发

事件触发类型的被动技能基于事件驱动，首先注册监听指定的事件，当事件触发后即执行对应的动作；也支持在事件下嵌套条件，此时事件的发生作为先决条件，要同时满足指定的条件才会执行后续的动作。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9dk9kimage.png)

---

#### 状态触发 

状态触发类型的被动技能通过Tick机制轮询判断条件是否成立，一旦满足条件则执行动作。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/m3zloimage.png)

技能编辑器内置了 [技能Event](https://developer.gp.qq.com/wikieditor/#/catalog/20112) 和 [技能Condition](https://developer.gp.qq.com/wikieditor/#/catalog/20111) 组件供开发者通过蓝图配置被动技能的触发机制，行为复用 [技能Task](https://developer.gp.qq.com/wikieditor/#/catalog/20094) 实现具体的被动效果。

<br>

## 被动技能模板

技能编辑器预置了被动技能模板和多个被动技能示例，供开发者参考使用。

**增长**

进入对局即生效，当前血量和最大血量永久增加200点。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FaDSFimage.png)

**伤害光环**

对5m内的敌人周期性造成20点伤害。

![ezgif-54c86aa88140b8.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/93mGhezgif-54c86aa88140b8.gif)

**大还丹**

当生命值低于最大生命值25%时触发，恢复全部生命值，此技能150s内最多触发一次。（为了方便演示将血量修改为75的限额，CD修改为0）

![ezgif-5924023b8cf428.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jXheNezgif-5924023b8cf428.gif)

**英勇勋章**

击败一名敌人后，增加5点最大血量和0.5%移动速度倍率，最多增加300最大血量和30%移动速度倍率。

![ezgif-582432cf0e008e.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VSQupezgif-582432cf0e008e.gif)

**灵魂燃烧**

击败一名敌人后，有20%的概率在敌人被击败处产生一道持续3s的火龙卷，火龙卷周围半径3m内的敌人被持续吸引至中心，并且每秒受到来自火龙卷的90点伤害。

![ezgif-5135cb7729b3dc.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/v3ATOezgif-5135cb7729b3dc.gif)

**治疗法球**

击败一名敌人后，有20%的概率掉落一个治疗法球（治疗法球存在15s），拾取后恢复20生命值。

![ezgif-52bd80ddb5e518.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/r3mOKezgif-52bd80ddb5e518.gif)

<br>

## 被动技能创建流程

### 新建被动技能蓝图

创建被动技能蓝图的步骤与主动技能一致，可参考 [新建技能蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%96%B0%E5%BB%BA%E6%8A%80%E8%83%BD%E8%93%9D%E5%9B%BE) 相关指引。

---

### 配置被动技能蓝图

被动技能通过 [技能Event](https://developer.gp.qq.com/wikieditor/#/catalog/20112) 和 [技能Condition](https://developer.gp.qq.com/wikieditor/#/catalog/20111) 决定触发时机，因此配置形式上不具有 [技能阶段](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E9%98%B6%E6%AE%B5%E9%85%8D%E7%BD%AE) 和 [序列播放器](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E5%BA%8F%E5%88%97%E6%92%AD%E6%94%BE%E5%99%A8%E9%85%8D%E7%BD%AE) 的概念，但是与主动技能一样需要通过 [技能Task](https://developer.gp.qq.com/wikieditor/#/catalog/20094) 实现行为逻辑。 

被动技能的配置项主要包含 ``ECA配置`` 和 ``技能基础配置``。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GkgOHimage.png)

#### ECA配置

ECA的核心配置包含 ``被动类型``、``行为列表``、``合并条件``、``最大激活次数`` 和 ``状态栏显示类型``。

**被动类型**

``被动类型`` 属性的选择分为 ``事件触发被动`` 或者 ``状态触发被动``。

【事件触发被动】

当选择以事件触发时，将出现 ``触发列表`` 配置项，每个元素对应可触发被动技能的事件，多个触发事件为“或”的关系，即每个事件触发时都将执行一次被动技能。

点击右上角【+】按钮出现可选的预置事件，选择事件将添加到触发列表中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MOiSBimage.png)

添加后选中该事件，在【配置细节】面板出现事件的参数项，用于指定精确的事件触发时机，部分属性支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/w7dfIimage.png)

事件配置下允许嵌套条件，支持添加多组条件，且各条件之间允许设置“与或”逻辑关系，事件与条件为“且”的关系，此时当事件触发并且满足所有条件时才会触发被动技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wmYBwimage.png)

各类型事件的说明及参数详细信息可参见 [技能Event查询手册](https://developer.gp.qq.com/wikieditor/#/catalog/20112)。

【状态触发被动】

选择状态触发将出现 ``状态条件`` 配置项，开发者可以添加多个条件，并且指定条件的判定规则：
- 全部满足：所有的条件全部判定成功才允许触发被动技能
- 满足任意一个：任意一个条件判定成功即可触发被动技能

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Es9dZimage.png)

各类型条件的说明及参数详细信息可参见 [技能Condition查询手册](https://developer.gp.qq.com/wikieditor/#/catalog/20112)。

---

**行为列表**

点击右上角【+】按钮出现可选的预置技能Task，选择Task将添加到行为列表中，添加后选中Task可以在【配置细节】面板设置Task的详细参数。

当被动技能处于激活状态或是触发后，将按技能Task的配置顺序依次执行各行为逻辑，以此实现被动技能的完整效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/X2XTwimage.png)

各类型Task的说明及参数详细信息可参见 [技能Task查询手册](https://developer.gp.qq.com/wikieditor/#/catalog/20094)。

---

**合并条件**

当角色触发多个同类型的被动技能时，是否需要合并技能效果，合并效果由开发者通过触发的 [``OnMerge_BP``](https://developer.gp.qq.com/api/#/searchContent/UPersistEffectBase?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUPersistEffectBase.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UPersistEffectBase&autoJump=OnMerge_BP) 覆写函数自行实现逻辑。

- 唯一：后续的被动技能会被合并到第一个被动技能效果上，即同时只能存在一个
- 共存：角色身上可同时存在多个被动技能，且影响状态栏的显示效果

---

**最大激活次数**

针对状态触发类型的属性，通常用于限制被动效果的叠加上限，例如被动技能效果为“每次触发暴击伤害后恢复5%的血量，最多恢复3次”，此时即可通过该属性控制恢复上限；若设置为-1则代表没有限制。

---

**开启客户端模拟**

是否同步被动技能的相关参数到客户端，用于客户端独立模拟技能表现，常用于优化性能使用。

---

**状态栏显示类型**

决定被动技能是否在状态栏显示以及如何显示，状态栏UI位置固定。

> 仅支持 [状态触发](https://developer.gp.qq.com/wikieditor/#/catalog/20110?autoJump=%E7%8A%B6%E6%80%81%E8%A7%A6%E5%8F%91) 类型被动技能

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qELM3image.png)

- 不显示：该被动不会出现在状态栏上
- 生效时显示：角色一旦获得该被动技能就会显示在状态栏上
- 激活时显示：被动技能生效时才会显示在状态栏上
- 激活时显示层数：被动技能触发时会在状态栏显示，且每多触发一次，其状态栏下角标+1

<br>

#### 技能基础配置

被动技能也能够设置 ``技能预设槽位``、``CD/能量消耗`` 等属性，与 [主动技能基础配置](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE) 完全一致，可参考相关文档进行配置。

<br>

## 添加被动技能

被动技能也需要主动添加给角色Pawn才能触发生效，同样支持蓝图配置和脚本动态添加的方式，可参见 [添加技能](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%B7%BB%E5%8A%A0%E6%8A%80%E8%83%BD) 部分内容进行配置。

<br>

## 实现简易被动技能

下面以一个被动技能为例，从空模板创建被动技能蓝图开始，逐步完成各效果的配置，帮助开发者更好地理解被动技能的创建过程。

目标效果：当玩家受到伤害时，触发加速并且生成逃跑毒气。

1. 打开技能编辑器，选择以 ``空技能模板`` 创建被动技能蓝图。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OzfGoimage.png)

2. 由于被动技能为受到伤害时触发，因此被动类型选择“事件触发被动”，并添加一个 ``受到伤害事件``，将该伤害事件的伤害来源默认为全部。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/w4DUXimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oywWCimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mJBygimage.png)

3. 在行为列表中添加一个 ``修改属性`` 的行为，为角色血量回复999点生命值，同时根据当前血量动态调整移动速度：``10 - (当前生命值 × 0.085)``，实现血量越低、移速越快的效果。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NngX4image.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hIfwHimage.png)

4. 在行为列表中额外添加一个 ``生成Actor`` 行为，选择Actor类为 ``BP_PoisonGas``，这样当受伤时将放出一圈毒气。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4W9Fcimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EIBHmimage.png)

5. 最后配置被动技能的CD、技能名称及图标等基础属性，并将技能添加到角色的技能组件中。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1P0WGimage.png)
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sOrZEimage.png)

技能效果演示：

![ezgif-56c6bcf47717f6.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kmKMGezgif-56c6bcf47717f6.gif)






---


## 技能Condition查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 技能Condition查询手册

**涉及API:** `LuaFunction`

# 技能Condition查询手册

## 通用属性

各条件组件都具有逻辑运算符的通用配置：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1UnfJimage.png)

- 逻辑运算：``AND`` 或者 ``OR`` 的设置决定该条件以何种操作符参与条件结果运算，运算方式为 ``最终条件结果 = (AND条件1 && AND条件2 && AND条件3……) || OR条件1 || OR条件2 || OR条件3…``
- 取值运算：``正常`` 或者 ``取反`` 决定该条件的判定结果

<br>

## 状态比较器

检查角色身上是否带有指定状态，状态判定遵循 [Tag匹配规则](https://developer.gp.qq.com/wikieditor/#/catalog/20102?autoJump=GameplayTag%E5%8C%B9%E9%85%8D)，若携带则结果为True，反之为False。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wkQPximage.png)

<br>

## 属性比较器

针对角色属性的数值验证器。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DRXzUimage.png)

数值比较公式：``左值属性 【比较符】 右值系数 * 右值属性``，右值系数支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)。
> 属性绑定数据类型：float

<br>

## 背包物品条件

检测背包内指定的物品数量是否符合条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WCpr5image.png)

- 物品ID：需要检测的物品ID，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
> 属性绑定数据类型：int
- 操作符：常用的比较运算符
- 比较值：比对的目标值，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
> 属性绑定数据类型：int

<br>

## 自定义条件

使用指定函数的返回值作为判定结果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/s4we3image.png)

``LuaFunction`` 属性对应脚本里的函数，返回值必须是布尔类型。

代码示例：

``` Lua
function UGCPlayerPawn:CheckHPIsReachMinimum(CurrentHP)
    return HP <= 20  
end
```

<br>

## 事件计数器

针对事件的条件组件，对目标事件的触发次数进行计数，当触发次数达到累计目标时，条件判断成立，该条件适合作为事件的嵌套条件使用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/37ewMimage.png)

- 激活计数：决定条件成立的目标累计值(该属性类型为浮点型)
- 步进值：每次事件触发的计数增量值(该属性类型为浮点型)
- 时效：允许在多长的时间内执行计数，超过该时效后计数会被重置(该属性类型为浮点型)
- 激活后重置：达到激活计数后，是否重置并重新计数
- 启用调试日志：启用后DS日志里会打印调试log，关键词可搜“UPESkillCondition_EventCounter”

<br>

## 队伍存活人数

检测队伍当前存活的人数是否符合条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/McsD6image.png)

- 操作符：常用的比较运算符
- 存活人数：比对的目标值

<br>

## 人称检查

检查当前角色的视角是否符合指定的人称视角条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/B7P7nimage.png)

- Target Person Perspective：第一/三人称

<br>

## 概率比较器

系统将进行一次随机并判断是否符合设定的概率。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zDWUYimage.png)

- 生效概率：检测通过的概率（0~1），该数值采用百分比制表示，0.2即代表20%
> 属性绑定数据类型：float

<br>

## 是否有合法目标

仅适用于主动技能，且需配合 [技能Task-阶段跳转](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-PESkillTask_StateBranch) 使用的条件组件，判断当前技能是否具有合法的释放目标。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mk5knimage.png)

<br>

## 是否有合法选点

仅适用于主动技能，且需配合 [技能Task-阶段跳转](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-PESkillTask_StateBranch) 使用的条件组件，判断当前技能是否具有合法的释放点位。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MoX5Rimage.png)

<br>

## 方向检测

将技能指定维度的方向与以角色朝向为坐标系的方向进行比较，判断角度差异是否符合指定的检测条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/S37OXimage.png)

- 比较方向俯仰角：比较方向基于角色前向的俯仰角
- 比较方向偏航角：比较方向基于角色前向的偏航角
- 检测方向类型：
	- 选中方向：用技能的选中方向进行比较
	- 选中位置：用技能选中的第一个位置减去施法者位置得到的向量方向进行比较
	- 选中目标：用技能选中目标的位置减去施法者位置得到的向量方向进行比较
- 最小检测角度：比较角度范围的最小值，取值范围-180~180
- 最大检测角度：比较角度范围的最大值，取值范围-180~180

<br>

## 事件时间间隔条件

判断指定事件自上一次触发至今的间隔时间是否满足条件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gXJWsimage.png)

- 事件类型：进行比较的 [Event事件](https://developer.gp.qq.com/wikieditor/#/catalog/20112)
- 累计判断时间：进行比较的数值
- 比较操作符：比较运算符

<br>

## 输入检查

检测和该技能绑定的按钮当前的按钮状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RPvhEimage.png)

- 输入状态：检测该按钮是否处在按下/抬起/长按状态





---


## 技能Event查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 技能Event查询手册

# 技能Event查询手册

目前所有的事件只针对玩家角色生效。

<br>

## 通用类事件

### 延迟触发事件

当角色获得技能时，延迟若干秒后触发一次该事件，再次触发需要重新添加技能，延迟时间支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/d1pRRimage.png)

- 延迟事件：延迟多久触发，单位为秒
> 属性绑定数据类型：float

---

### 输入事件

该事件只针对主动技能，通过 [技能Task-阶段跳转](https://developer.gp.qq.com/wikieditor/#/catalog/20094:~:text=%E8%A1%A8%E7%8E%B0%E5%BC%82%E5%B8%B8%E9%97%AE%E9%A2%98-,%E6%8A%80%E8%83%BDTask%2D%E9%98%B6%E6%AE%B5%E8%B7%B3%E8%BD%AC,-%E5%9C%A8task%E6%89%A7%E8%A1%8C) 配置监听，当该Task开始的时候，才开始监听按下事件，检测技能按钮的交互输入以决定事件的触发，仅检测当前技能绑定的按钮。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uVZNlimage.png)

- 输入事件：
	- 点击：点按输入，按钮抬起后且按住时间小于0.2s触发
	- 按下：非点击情况下，按钮按下时触发
	- 抬起：非点击情况下，按钮抬起时触发
	- 长按：非点击/按下情况下，按钮按住时间大于长按时间时触发
		- Long Press Type：支持 ``持续检测`` 和 ``抬起时检测``，``持续检测`` 代表按住时间满足 ``长按时间`` 要求时立即触发该事件；``抬起时检测`` 只在按钮抬起时才检测是否满足 ``长按时间`` 要求
		- 长按时间：长按的时间阈值
- 按键时长：事件触发时通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出按钮按住的累计时间
> 属性绑定数据类型：float

---

### 周期触发事件

根据设定的时间间隔持续触发事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oIYaMimage.png)

- 间隔时间：事件触发的间隔时间

<br>

## 角色类事件

### 累计受到伤害事件

拥有此技能的角色累计受到多少伤害时触发该事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YUMKjimage.png)

- 清空时间：伤害值在多少时间内未达成累计量自动清空累计值，当<=0时不进行自动清空
- 触发阈值：需要达成的累计量，当累计受到伤害值超过该值时，触发该事件并执行清空
- 累计伤害值：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出当前累计受到的伤害值
> 属性绑定数据类型：float

---

### 累计造成伤害事件

拥有此技能的角色累计对敌方产生多少伤害时触发该事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/j2vjrimage.png)

- 清空时间：伤害值在多少时间内未达成累计量自动清空累计值，当<=0时不进行自动清空
- 触发阈值：需要达成的累计量，当累计产生伤害值超过该值时，触发该事件并执行清空
- 累计伤害值：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出当前累计产生的伤害值
> 属性绑定数据类型：float

---

### 助攻事件

当施法者在目标被队友击杀前60秒内曾造成伤害，则触发此事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/e8Kliimage.png)

---

### 跳跃事件

仅当玩家角色使用跳跃时，此事件才会被触发。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gWongimage.png)

- 比较符：当玩家的当前跳跃次数满足比较条件时与比较符的表达式时，才会触发该事件。
- 跳跃次数：将使用触发当次跳跃时的跳跃次数和配置值比较，满足表达式时，才会触发该事件。

### 属性变化事件

当角色身上某个属性发生变化时触发事件，此变化不包含值大小的比较。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jPWZdimage.png)

- 监听的属性：具体监听的角色属性，支持 [自定义角色属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 变化量：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出属性的变化量
> 属性绑定数据类型：float

---

### 背包事件

当背包内某物品或某类物品产生预置的操作时触发该事件。
> 该事件仅支持 [新背包系统](https://developer.gp.qq.com/wikieditor/#/catalog/20104)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wRJcfimage.png)

- 监控类型：支持指定物品或者通过标签筛选一类物品
	- 物品ID：目标物品ID，适用于单类物品，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
	- 物品Tags：[物品标记Tag](https://developer.gp.qq.com/wikieditor/#/catalog/20124?autoJump=V2%E8%83%8C%E5%8C%85%E5%B1%9E%E6%80%A7%E9%85%8D%E7%BD%AE)，适用于同类型的多个物品
- 操作：需要监听的背包操作行为，包含拾取、丢弃、使用和销毁，支持多选
> 属性绑定数据类型：int

---

### 死亡事件

挂载技能的角色死亡时触发事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fAWfOimage.png)

- 伤害类型：配置一个具体的伤害类型，只有这种伤害类型造成的死亡，才能触发事件，支持枪械、近战、技能和载具类型的伤害
- 伤害Tag：配置一组具体的伤害Tag，只有致死伤害携带了这些Tag，才能触发事件
- 伤害部位：只有对指定部位造成的伤害导致的死亡，才能触发事件，支持头部和身体的部位伤害
- 伤害阵营选择：只有该阵营造成的伤害导致的死亡，才能触发事件
- 击杀来源：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出击杀者
> 属性绑定数据类型：Actor
- 击中部位：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出命中的部位
> 属性绑定数据类型：float

---

### 角色落地事件

当角色落地时触发该事件，无特殊参数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rRH7dimage.png)

---

### 受到伤害事件

挂载技能的角色受到伤害时触发事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6jpbJimage.png)

- 监听方式：
	- 监听伤害前：在执行伤害结算前触发，如果为此监听方式，则可利用事件修改最终执行的伤害结算值
	- 监听伤害后：在执行伤害结算后触发
- 伤害类型：配置一个具体的伤害类型，只有这种伤害类型才能触发事件，支持枪械、近战、技能和载具类型的伤害
- 伤害Tags条件：所有Tags必须满足/任一Tag满足即可
- 伤害Tag：配置一组具体的伤害Tag，基于Tags条件决定是否允许触发事件
- 伤害部位：只有对指定部位造成的伤害，才能触发事件，支持头部和身体的部位伤害
- 伤害来源阵营选择：只有该阵营造成的伤害才能触发事件
- 伤害：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次受到的伤害值
> 属性绑定数据类型：float

---

### 造成伤害事件

挂载技能的角色对其他目标造成伤害时触发事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5SCMnimage.png)

- 监听方式：
	- 监听伤害前：在执行伤害结算前触发，如果为此监听方式，则可利用事件修改最终执行的伤害结算值
	- 监听伤害后：在执行伤害结算后触发
- 伤害类型：配置一个具体的伤害类型，只有这种伤害类型才能触发事件，支持枪械、近战、技能和载具类型的伤害
- 伤害Tags条件：所有Tags必须满足/任一Tag满足即可
- 伤害Tag：配置一组具体的伤害Tag，基于Tags条件决定是否允许触发事件
- 伤害部位：只有对指定部位造成的伤害，才能触发事件，支持头部和身体的部位伤害
- 伤害来源阵营选择：只有对指定的阵营对象造成的伤害才能触发事件
- 伤害：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次受到的伤害值
> 属性绑定数据类型：float

---

### 碰撞事件

角色发生碰撞时触发该事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3cXmUimage.png)

- 碰撞检测Actor过滤器：当碰撞到的Actor满足指定要求时，才会触发该碰撞事件
	- 过滤要求：触发条件的判定规则
		- 全部满足：所有的过滤器条件均符合才允许触发事件
		- 满足任意一个：任意一个过滤器条件符合即可触发事件
	- 过滤器：[命中过滤器](https://developer.gp.qq.com/wikieditor/#/catalog/20165?autoJump=%E6%8A%9B%E4%BD%93%E5%91%BD%E4%B8%AD%E8%BF%87%E6%BB%A4%E5%99%A8) 组件，可配置多组过滤器
- Nav地面检测：是否碰撞地面时触发该事件
- 碰撞到的：碰撞事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次检测到的碰撞Actor列表
> 属性绑定数据类型：Actor

---

### 击杀事件

挂载技能的角色产生击杀时触发事件，当击杀对象为其他玩家角色时才生效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VeCb4image.png)

- 伤害类型：配置一个具体的伤害类型，只有这种伤害类型导致的击杀才能触发事件，支持枪械、近战、技能和载具类型的伤害
- 伤害Tag：配置一组具体的伤害Tag，只有伤害携带了这些Tag导致的击杀，才能触发事件
- 伤害部位：只有对指定部位造成的伤害导致的击杀，才能触发事件，支持头部和身体的部位伤害
- 击杀目标阵营选择：只有击杀指定的阵营对象才能触发事件
- 击杀目标：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出击杀的目标
> 属性绑定数据类型：Actor
- 击中部位：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出击中的部位
> 属性绑定数据类型：float

---

### 受到治疗事件

当角色受到一次治疗时触发该事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TrjMYimage.png)

- 监听方式：监听到治疗前或者治疗后触发该事件
- 治疗Tags条件：决定触发事件的治疗Tag判定规则
	- 所有Tags必须满足：全部Tag同时匹配时才允许触发事件
	- 任一Tag满足即可：匹配任意一个Tag即可触发事件
- 治疗Tag：要求治疗行为携带的Tag标签
- 治疗值：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗值
> 属性绑定数据类型：float
- 治疗发起者Actor：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗来源Owner
> 属性绑定数据类型：Actor
- 治疗来源Actor：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗来源
> 属性绑定数据类型：Actor
- 治疗目标Actor：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗目标
> 属性绑定数据类型：Actor

---

### 造成治疗事件

角色主动触发一次治疗行为时触发该事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OPdajimage.png)

- 监听方式：监听到治疗前或者治疗后触发该事件
- 治疗Tags条件：决定触发事件的治疗Tag判定规则
	- 所有Tags必须满足：全部Tag同时匹配时才允许触发事件
	- 任一Tag满足即可：匹配任意一个Tag即可触发事件
- 治疗Tag：要求治疗行为携带的Tag标签
- 治疗值：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗值
> 属性绑定数据类型：float
- 治疗发起者Actor：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗来源Owner
> 属性绑定数据类型：Actor
- 治疗来源Actor：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗来源
> 属性绑定数据类型：Actor
- 治疗目标Actor：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出本次的治疗目标
> 属性绑定数据类型：Actor

---

### 状态改变事件

角色的某个状态发生改变时触发事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Lc6y8image.png)

- 监听Tag：具体监听的 [角色状态Tag](https://developer.gp.qq.com/wikieditor/#/catalog/20106?autoJump=%E5%92%8C%E5%B9%B3%E8%A7%92%E8%89%B2%E7%8A%B6%E6%80%81)

<br>

## 技能类事件

### 阶段Sequence事件

该事件只针对主动技能，通过 [技能Task-阶段跳转](https://developer.gp.qq.com/wikieditor/#/catalog/20094:~:text=%E8%A1%A8%E7%8E%B0%E5%BC%82%E5%B8%B8%E9%97%AE%E9%A2%98-,%E6%8A%80%E8%83%BDTask%2D%E9%98%B6%E6%AE%B5%E8%B7%B3%E8%BD%AC,-%E5%9C%A8task%E6%89%A7%E8%A1%8C) 配置监听，当阶段的Sequence执行完毕后才会触发该事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8z1UQimage.png)

- 仅完整播放结束：若勾选，如果技能阶段被打断则不触发

---

### 技能事件

该事件监听游戏中所有角色对象的技能的释放状态。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sw7Fmimage.png)

- 只监听所属技能：当有对象释放所监听技能槽位/Tag的技能时，触发该事件
- 只监听自己：当且仅当绑定该监听事件的角色，触发所监听技能槽位/Tag的技能时，触发该事件
- 监听类型：通过技能槽位监听还是技能Tag监听
	- 不监控槽位或技能：任何技能的释放均能监听到
	- 监听技能槽位：只有该槽位的技能状态发生改变时，事件才会触发
	- 监听技能Tag：只有该Tag类型的技能状态发生改变时，事件才会触发
- 监听技能状态：
	- 任意：所有技能状态变化时均触发
	- 取消：技能被中断时触发
	- 应用：技能效果成功附加时触发
	- 卸载：技能移除时触发
	- 完成：完成整个技能流程时触发
	- 中断：技能被外部强制打断时触发
	- 激活：技能开始释放时触发
- 技能对象：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出触发的对应技能实例
> 属性绑定数据类型：Actor

---

### 抛体发射事件

施法者发射抛体时触发的事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/croifimage.png)

- 抛体Tag：带有该Tag的抛体被发射时才触发；否则，所有抛体发射时都会触发该事件
- 发射的抛体：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出对应的抛体实例
> 属性绑定数据类型：AUniversalProjectileCore

<br>

## 枪械类事件

### 枪械开火

角色武器开火时触发的事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nibUQimage.png)

- 武器Tag：指定Tag类型的武器开火时才触发事件
- 最新武器：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出该武器实例
> 属性绑定数据类型：Actor

---

### 武器命中事件

角色武器命中目标的时候触发事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KxMbtimage.png)

- 计数器类型：
	- 重复执行：计数器达标后自动重置，可循环触发。
	- 执行一次：计数器达标后即停止计数，仅生效一次。
- 目标值：需要累计命中的次数，支持 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108)
- 武器Tag：指定Tag类型的武器开火命中时才计数
- 伤害部位：仅命中对应部位时才会进行计数
- 命中目标阵营过滤：命中对应阵营目标才会进行计数
- 命中来源：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出命中的角色实例
> 属性绑定数据类型：Actor
- 命中部位：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出命中的部位类型输出击中的部位
> 属性绑定数据类型：float

---

### 武器事件（换弹）

角色武器换弹时触发的事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PpsVWimage.png)

- 武器Tag：指定Tag类型的武器换弹时才触发事件
- 最新武器：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出该武器实例
> 属性绑定数据类型：Actor

---

### 武器事件（开关镜）

角色武器开关倍镜时触发的事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9fNzPimage.png)

- 监听开镜：True为监听开镜事件，False监听关镜事件
- 武器Tag：指定Tag类型的武器开/关镜时才触发事件
- 最新武器：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出该武器实例
> 属性绑定数据类型：Actor

---

### 武器事件（停火）

角色武器停火时触发的事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4JjVZimage.png)

- 武器Tag：指定Tag类型的武器停火时才触发事件
- 最新武器：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出该武器实例
> 属性绑定数据类型：Actor

---

### 武器事件（切枪）

角色切换武器的时候触发的事件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UlRRTimage.png)

- 触发方式：指定武器装备或者卸下时触发事件
- 武器Tag：指定Tag类型的武器切枪时才触发事件
- 最新武器：该事件触发时，通过 [属性绑定](https://developer.gp.qq.com/wikieditor/#/catalog/20108) 输出该武器实例
> 属性绑定数据类型：Actor




---


## 技能调试工具

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 技能调试工具

**涉及API:** `RemoveBuffByClass`, `RemoveSkillInstance`

# 技能调试工具

技能调试工具提供运行时查看技能、Buff和角色属性状态的功能，为新技能/Buff编辑器框架而设计，帮助开发者在技能开发过程中快速进行数值和表现的调试和迭代优化。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LmwN5image.png)

<br>

## 启用调试工具

技能调试工具功能通过 [通用GM面板](https://developer.gp.qq.com/wikieditor/#/catalog/20109) 提供，启动编辑器 [Debug调试](https://developer.gp.qq.com/wikieditor/#/catalog/307)，找到右上角GM入口并点击。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/clc4Simage.png)

展开GM面板后，点击右侧【调试】页签，切换到调试面板，点击 ``角色调试面板`` 的确定按钮即可打开技能调试工具。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/P0KIQimage.png)

<br>

## 调试功能说明
   
技能调试工具提供了三类调试功能：技能调试、Buff调试与属性调试。

### 技能调试

技能调试面板支持为指定目标添加/移除/释放指定技能、查看技能的运行时数据，甚至可以修改技能配置以调试技能效果。

调试技能前需要先选择调试目标，调试工具会将以玩家自身为中心的球形范围内的Pawn对象纳入可选列表，从【选择目标对象】的下拉列表中选择目标实例对象。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IqKH4image.png)

当Pawn对象选择成功后，会通过绿色箭头形式的UI标识当前调试目标。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Z4Jerimage.png)

#### 添加技能

点击【添加技能】按钮，在弹出窗口中需要填写要添加的技能和绑定的技能槽位。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ipS64image.png)

通过 [技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%96%B0%E5%BB%BA%E6%8A%80%E8%83%BD%E8%93%9D%E5%9B%BE) 创建的技能蓝图将出现在下拉列表中，“挂载Slot”为 [预设技能UI槽位](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%8A%80%E8%83%BD%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6sW6Aimage.png)

点击【确定】后该技能将添加给目标对象，【编辑】面板将显示该技能的CD消耗与技能消耗配置信息，同时【调试】面板也会显示技能槽位、技能阶段状态、上一次施法结果等更详细的运行时数据。

![QQ2025619-21540-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/b7qeDQQ2025619-21540-HD-ezgif.com-video-to-gif-converter.gif)

---

#### 释放技能

添加技能时如果绑定的是预设技能UI槽位，则会在界面上显示该技能，此时可以直接点击触发技能。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uJySQimage.png)

调试工具也提供了添加多种技能下的更便捷的释放方式，在【编辑】面板选中目标技能，点击下方【释放当前技能】按钮即可触发技能。

![QQ2025619-21155-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FMDlRQQ2025619-21155-HD-ezgif.com-video-to-gif-converter.gif)

---

#### 修改技能配置

除了释放技能，调试工具还支持修改CD消耗与技能消耗的参数配置，修改后点击【应用】按钮即可生效。

![QQ2025619-213111-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Yhn5mQQ2025619-213111-HD-ezgif.com-video-to-gif-converter.gif)

---

#### 移除技能

在选中技能的情况下，点击【移除技能】按钮可以移除该技能，效果等同于 [``RemoveSkillInstance``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=RemoveSkillInstance)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Oyikpimage.png)

<br>

### Buff调试

Buff调试面板默认显示当前玩家角色的Buff状态，如果需要调试其他对象，也需要先选择调试目标，操作与添加技能调试目标相同。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/je3Cuimage.png)

#### 添加Buff

点击【添加Buff】按钮，在弹出窗口中需要填写要添加的目标Buff、Buff来源（Causer）、Buff层数和持续时间，通过 [Buff编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20087?autoJump=%E6%96%B0%E5%BB%BABuff%E8%93%9D%E5%9B%BE) 创建的Buff蓝图会出现在可选列表中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1TGjPimage.png)

成功添加Buff后将在对应的目标对象的Buff栏实时显示Buff状态信息。

![QQ2025619-221052-HD-ezgif.com-effects.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xdCbkQQ2025619-221052-HD-ezgif.com-effects.gif)

---

#### 移除Buff

在目标对象的Buff栏，选中Buff并点击【移除Buff】按钮即可移除该Buff，效果等同于 [``RemoveBuffByClass``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=RemoveBuffByClass)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NHDNcimage.png)

<br>

### 属性调试

属性调试面板提供角色基础属性（[固化属性](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E5%9B%BA%E5%8C%96%E5%B1%9E%E6%80%A7)）和 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20135?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的调试功能，选择调试的目标对象后即显示各项属性信息，开发者可以直接在面板上修改属性值并验证修改效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Rakg0image.png)

#### 修改属性

以 ``移动速度倍率`` 属性为例，修改属性值后，点击【应用】按钮即可生效。

![QQ2025619-22362-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Iu9TkQQ2025619-22362-HD-ezgif.com-video-to-gif-converter.gif)

---

#### 还原属性

选中要还原的目标属性，点击【还原】按钮即可将属性值还原为默认值。

![QQ2025619-223724-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7oxgUQQ2025619-223724-HD-ezgif.com-video-to-gif-converter.gif)

如果修改了多个属性，可以通过【一键还原】按钮进行批量属性的还原。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/NuK4zimage.png)



---


## 技能状态图

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > 技能编辑器2.0 > 技能状态图

# 技能状态图

技能阶段图是基于节点连接的可视化状态图，用于定义技能各阶段的执行逻辑关系，开发者可通过节点连线快速定义技能阶段跳转逻辑，无需手写状态转换代码，显著提升复杂技能的开发效率，同时降低策划与程序间的协作成本。

<br>

## 状态图概念

在技能系统中，技能阶段是构成技能的基本，每个阶段代表技能执行过程中的一个特定状态，所有技能阶段连接起来构造成一个完整的技能。

### 状态图节点

技能状态图由入口节点、阶段节点、全局事件节点、动作列表节点和终止节点构成。

**Entry节点**
 
Entry入口节点是技能状态机中的单向起点，通过技能初始化进入，并且只能基于 ``技能激活事件`` 和跳转条件触发后续的阶段流程。

>注意：Entry节点的跳转默认不经由事件触发，但部分旧技能模板为保持功能可用而保留了事件触发的配置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eJRq0image.png)

**End节点**

End阶段是技能状态机的终止节点，当执行至该节点时，整个技能流程结束并自动重置为Entry状态，该节点仅保留进入引脚。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CJW7Timage.png)

**技能阶段节点**

自定义技能节点是由系统或玩家创建的技能单元，该节点既可以由Entry节点进入作为技能的起始阶段，也可输出至End节点作为技能最后阶段，因此同时具备进入和离开的引脚。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mBL3Iimage.png)

**全局事件节点**

全局事件节点是技能生命周期内独立监听的事件机制。当事件触发且条件满足时，会根据其执行行为产生两种结果：若执行对象是动作列表，则会完全独立运行，不影响当前正在执行的其他时间轴动作；若执行行为是跳转阶段，则会立即打断其他执行中的阶段，直接跳转到目标阶段，从而确保同一时间仅有一个阶段处于激活状态，仅保留输出引脚。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Ps4Zuimage.png)

- Event Name：节点名称
- 事件：需要监听的 [技能事件](https://developer.gp.qq.com/wikieditor/#/catalog/20112)
- 条件：如果触发监听事件，跳转还需满足的 [技能条件](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20111)，事件与条件之间为“且”的关系
- 是否技能激活前生效：
    - 勾选：获得技能后即开始监听事件，若事件触发且条件满足，则执行后续跳转；仅可连接 ``动作列表节点``
    - 不勾选：激活技能后即开始监听事件，若事件触发且条件满足，则执行后续跳转；可连接 ``动作列表节点`` 和 ``技能阶段节点``

全局事件的跳转仅能通过跳转条件触发。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PtDoTimage.png)

**动作列表节点**

动作列表节点仅用于定义并执行一个行为集合，在条件满足或事件触发时执行列表内全部动作，而无法控制流程的阶段跳转，因此仅具备进入引脚。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vZF5cimage.png)

- 动作组名称：节点名称
- 动作列表：可配置多个 [技能Task](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20094)，在节点激活时依次触发

>该节点不可作为技能的End节点使用。如需在某一阶段后立即执行其动作，则前一节点必须在跳转至该动作节点的同时，额外连接一个后续节点，以便动作执行完毕后能反激活进行跳转，否则将导致技能流程阻塞。

---

### 状态跳转流程图

技能阶段跳转流程始终从Entry节点开始到End节点结束，执行过程中当多个跳转条件同时满足时，系统将根据预设优先级选择唯一路径进行状态跳转。

![状态图可视化.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DA5Nq%E7%8A%B6%E6%80%81%E5%9B%BE%E5%8F%AF%E8%A7%86%E5%8C%96.png)

**节点连接/跳转规则**

|To/From|全局事件|状态|动作列表|
|-|-|-|-|
|全局事件|✖|✖|✖|
|状态|规则A|规则B|✖|
|动作列表|规则C|规则D|✖|

- 规则A：全局事件连接状态，仅允许在技能激活后生效的全局事件连接至状态。连线仅用于配置条件，事件触发后若条件满足，则执行状态跳转
- 规则B：状态连接状态，可配置的事件或条件将触发状态跳转，当事件触发或条件满足时，技能的状态由起始状态跳转到目标状态
- 规则C：全局事件连接动作列表，仅可配置跳转条件。事件触发后，若条件满足，则随即执行一次动作列表中的所有动作
- 规则D：状态连接列表，代表当技能处于该状态时，若满足配置的跳转条件，则激活对应动作列表里的所有动作，条件不满足时则反激活，此效果仅在本状态作用域内生效；若满足配置的跳转事件，则触发一次对应动作列表的所有动作

<br>

## 创建状态图

技能状态图是基于技能逻辑阶段的可视化状态机，访问技能状态图需先在技能编辑器中创建技能，参考[技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091)创建冲刺技能，在技能预览窗口中选中目标技能后，点击``Skill Flow Graph``选项即可进入技能状态图编辑界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QJj3Uimage.png)

> 该功能仅限主动技能

### 添加节点

在编辑器空白处右键点击或拖拽节点引脚至空白处释放，均可触发相同的上下文菜单，提供可操作选项：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5zvCtimage.png)

- Auto Arrange ：自动重新排布
- Focus Entry Node ：跳转到入口节点
- Fresh SkillData：刷新技能数据
- Add New Action List：新建动作列表
- Add New State ： 添加新的技能阶段
- Add New Global Event ： 添加全局事件节点

当用户将鼠标悬停在任意节点上时，可通过评论气泡功能为该节点添加自定义备注信息：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZR3Primage.png)

---

### 设置节点属性

在状态图中选中任意节点后，右侧属性面板将显示该节点的可配置参数：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YSfD7image.png)

- State Name：技能阶段名称
- Loop：该阶段是否无线循环
- PalyRate:该阶段的播放速度

---

### 定义跳转条件 

状态图中选择任意跳转节点，右侧【细节】面板将显示跳转的配置参数，不同类型的节点之间跳转参数不同。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AXCFbimage.png)

**Entry节点跳转**

Entry节点仅支持按条件跳转，当技能被激活且满足指定的条件时，触发跳转，多个条件之间为“且”的逻辑关系。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/n1lm3image.png)

**全局事件跳转**

全局事件仅支持按条件跳转，当事件被触发且满足指定的条件时，触发跳转，多个条件之间为“且”的逻辑关系。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/az3Xdimage.png)

**技能阶段跳转**

技能阶段之间的跳转支持事件触发跳转或者按条件跳转，若同时配置了两种跳转模式，则为“或”的逻辑关系。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VXy3simage.png)

- 优先级：跳转的优先级，若同一帧内某阶段存在多个满足条件的跳转路径，则优先执行优先级最高的跳转
- 事件型跳转：当指定的事件触发时可执行跳转操作，多个事件之间为“或”的逻辑关系
	- Event Name：跳转名称
	- 事件：指定的 [技能Event](https://developer.gp.qq.com/wikieditor/#/catalog/20112?autoJump=%E9%80%9A%E7%94%A8%E7%B1%BB%E4%BA%8B%E4%BB%B6) 事件类型
	- 条件：可为事件触发添加额外的约束条件，指定 [技能Condition](https://developer.gp.qq.com/wikieditor/#/catalog/20111?autoJump=%E6%A6%82%E7%8E%87%E6%AF%94%E8%BE%83%E5%99%A8) 条件组件
- 条件型跳转：定义 [技能Condition](https://developer.gp.qq.com/wikieditor/#/catalog/20111?autoJump=%E6%A6%82%E7%8E%87%E6%AF%94%E8%BE%83%E5%99%A8) 条件规则，系统将在每帧Tick时持续监测该条件，一旦条件符合则触发跳转行为，多个条件之间为“或”的逻辑关系


<br>

## 技能状态图拆解

蓄力机制通过多条件筛选与优先级判定，实现精准的跳转控制。我们将以技能践踏模板践为例，讲解践踏技能阶段实现的总体思路。

继承蓄力创建一个技能,创建技能具体可以参考[技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091)点击在技能预览窗口中选中目标技能后，点击``Skill Flow Graph``选项进入状态图页面：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kotkbimage.png)

>注意：若未出现该编辑窗口则需点击重置布局

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CIcnPimage.png)

Entry跳转至下一阶段时，默认由技能激活事件触发，因此无需进行额外的事件配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vRa8Mimage.png)



当玩家抬起按键时，触发事件满足，系统会按照优先级顺序依次检测各蓄力阶段（Charge）的跳转条件；若所有高阶条件均未满足，则执行最低优先级的跳转至End阶段，保证即使任何阶段条件均不满足技能流程也能正常结束。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Xapy4image.png)

效果演示：

![ezgif-73f22fd1219292.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RdPaoezgif-73f22fd1219292.gif)

当进入Charge阶段且满足输入触发事件时，系统检测长按输入事件按下并在抬起时计算持续时间，符合阈值则跳转至Action阶段。虽然该跳转与Charge至End的跳转条件相同，但Action跳转优先级更高（1>0），因此在条件同时满足时优先执行Action跳转。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XqOWlimage.png)

在触发条件达成后，系统会优先执行高优先级阶段：

![ezgif-7047218cc020ae.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pXaksezgif-7047218cc020ae.gif)

当长按≥2.2秒时，系统执行满足条件的最高优先级跳转；若未达时长，则自动切换至其他符合条件的跳转判定流程。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cd4V7image.png)

当两个技能阶段完成后，进入技能End阶段。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5ynEOimage.png)

<br>

## 状态图实战案例

通过继承技能模板创建的本地实例支持节点编辑功能，开发者可通过拖拽节点引脚对技能状态图进行逻辑调整与流程优化，下面将基于空白模板，逐步构建一个切换形态技能的完整实现流程。

**创建技能阶段**

以空技能为模板创建一个技能：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WjxcTimage.png)

进入状态图后，可以看到空技能模板只提供了技能的Entry和End阶段：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/D3FLdimage.png)

技能阶段的构建需要开发者手动创建。当技能触发时，执行流程始终从Entry初始状态开始顺序执行。创建新阶段的操作方法：右键状态图空白处，在弹出菜单中选择``Add New State``命令来建立首个技能阶段：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HTzRrimage.png)

选中新建的状态节点，通过添加Task来实现该技能阶段的核心功能逻辑，在空技能模板中没有提供角色技能轨道，需要我们手动创建，Task不能放在动画轨道上，否则将不生效，具体创建方法[技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WUzxoimage.png)

首先实现基础光环效果，创建生成粒子Task并绑定预设粒子模板，完成第一个光环效果的实现，Task可参考[技能Task查询手册](https://developer.gp.qq.com/wikieditor/#/catalog/20094)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zeQP8image.png)

按照如上方法，创建切换后的光环效果，需新增技能阶段节点并配置相应的属性：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/u2LSzimage.png)

---

**实现阶段跳转逻辑**



该技能采用状态切换机制：若在释放过程中未主动触发光环切换条件，则技能阶段执行完毕后进入End结束技能流程，跳转必须命名，若未命名则不会执行跳转：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bi0lJimage.png)

将第一阶段出口优先连接至第二阶段入口，并设置其优先级高于结束阶段跳转，确保在第一技能阶段满足条件时必定进入下一阶段而非进入End，添加一个输入事件，设置触发事件的方法为按下，优先级设置为1：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/T8LXSimage.png)

在第二阶段技能动作及特效播放完毕后，需将其状态节点出口与End终态节点相连，确保正常结束技能流程：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wXgZAimage.png)

技能效果演示：

![ezgif-2e0a430d242075.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CkWkoezgif-2e0a430d242075.gif)


---
