# 进阶内容/GamePlay系统/技能系统/Buff编辑器2.0

> 本分类共 2 篇文章

---


## BuffAction查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器2.0 > BuffAction查询手册

**涉及API:** `None`

# BuffAction查询手册

## 添加Buff

向目标添加指定的Buff。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3BUUsimage.png)

- Buff类型：指定添加的Buff蓝图
- 添加的层数：指定需要添加的层数
- Overwrite Time：Buff持续时间，-1代表不覆盖该Buff蓝图配置的生效时长
- 设置为Buff的Causer：此选项已弃用，开发者无需配置

<br>

## 修改人物属性

修改Buff目标的指定角色属性，遵循 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的计算方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EBiK3image.png)

- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：预置血量、能量、信号等和平角色的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20176?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式或者指定Lua函数的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自Buff目标

> - ``是否同步客户端`` 保持默认勾选
> - 属性绑定数据类型：float

<br>

## 造成伤害

对Buff的对象给与指定伤害。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6aSoeimage.png)

- 伤害类型Tag列表：可以为伤害添加额外的 [Tag标签](https://developer.gp.qq.com/wikieditor/#/catalog/20102?autoJump=GameplayTag%E6%A6%82%E8%BF%B0)
- 伤害数值：支持绑定常数、基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式或者指定Lua函数的返回值
- 修改值属性来源：若 ``伤害数值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自Buff目标

<br>

## 调用Lua脚本

执行指定脚本里的可重载函数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ARntUimage.png)

- LuaFunction：指定的重载函数

<br>

## 生成特效

播放指定的特效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vdo4jimage.png)

- 特效：选择要播放的特效资源
- 是否是强引用：建议勾选，否则影响特效资源的引用
- Socket：特效挂载的位置槽位，例如角色的某个骨骼；为空时，挂载到当前对象的世界坐标点上
- Offset：特效挂载位置或旋转的偏移量及缩放比例
- 缩放规则：
	- 保持相对缩放：与挂接目标保持相对缩放比例
	- 保持原始缩放：维持自身的原始缩放比例
- 持续时间：特效的持续时间，<0不会定时清除，只有在Buff结束时才清除
- 允许同时存在多个特效：勾选后，当多次触发该效果且之前生成的特效还未结束，则可以生成新的特效；反之亦然

<br>

## 治疗恢复

为Buff目标恢复指定血量。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4gzNyimage.png)

- 恢复数值：支持绑定常数、基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式或者指定Lua函数的返回值
- 恢复血量Tags：支持为治疗行为添加Tag，通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102?autoJump=GameplayTag%E6%A6%82%E8%BF%B0) 创建

<br>

## 移除Buff

为目标移除指定的Buff。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sXgb5image.png)

- Buff类型：指定移除的Buff蓝图
- 移除的层数：指定需要移除的层数

> ``设置为Buff的Causer`` 属性已弃用

<br>

## 播放声音

播放指定的音效。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bHoELimage.png)

- Attach Sound：选择需要播放的音效资源
- 叠层时行为：
	- 叠层时重新创建：Buff叠加新一层时，对应的播放音效Action销毁旧的音效，重新创建播放新的音效
	- 叠层时叠加多个：Buff叠加新一层时，额外多创建一个新的音效
- 消声器类型：
	- 不自动停止：音效不会自动停止
	- 层数减少时停止：Buff层数减少时，自动停止
	- Buff结束时停止：Buff结束时，对应音效停止

<br>

## 下一次伤害属性修改

基于 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的属性修改行为，临时修改Buff目标的指定属性值，当下一次受到任意伤害时（触发 [伤害公式](https://developer.gp.qq.com/wikieditor/#/catalog/20099)），自动移除相关修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UjehBimage.png)

- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：支持和平角色与枪械的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20176?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式或者指定Lua函数的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自Buff目标

> - ``目标属性公式`` 为预留项，保持 ``None``
> - ``是否同步客户端`` 保持默认勾选
> - 属性绑定数据类型：float

<br>

## 修改武器属性

修改Buff目标的指定武器属性，遵循 [属性修改器](https://developer.gp.qq.com/wikieditor/#/catalog/20153) 的计算方式。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kUKsuimage.png)

- 修改方式：临时修改/永久修改/持续修改
- 要修改的属性：预置和平枪械的基础属性，也支持绑定 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7)
- 修改符：基于属性修改器的 [修改运算符](https://developer.gp.qq.com/wikieditor/#/catalog/20176?autoJump=%E5%B1%9E%E6%80%A7%E4%BF%AE%E6%94%B9%E7%AC%A6)
- 修改值：支持绑定常数、基于 [自定义属性](https://developer.gp.qq.com/wikieditor/#/catalog/20098?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B1%9E%E6%80%A7) 的计算公式或者指定Lua函数的返回值
- 修改值属性来源：若 ``修改值`` 设定为计算公式，则该项决定公式中所使用的属性的取值来源
	- Causer：属性取值源自施法者
	- Target：属性取值源自Buff目标

> - ``是否同步客户端`` 保持默认勾选
> - 属性绑定数据类型：float

<br>

## 屏幕特效

屏幕特效的设置与 [技能Task-屏幕特效](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E5%B1%8F%E5%B9%95%E7%89%B9%E6%95%88) 相同，可参考相关说明。

<br>

## 附加Actor

附加一个Actor到对应施法者身上。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/srYBOimage.png)

- 附加的Actor类：生成的Actor蓝图类
- Socket：支持按 ``部位类型`` 或者 ``插槽名称`` 附加
- Offset：挂载位置基于该Socket点的偏移
- 叠层时行为：
	- 叠层时重新创建：Buff叠加新一层时，销毁对应的旧Actor，重新创建新的Actor并附加
	- 叠层时叠加多个：Buff叠加新一层时，额外多创建一个新的Actor并附加
- 生成停止类型：
	- 不自动停止：Actor不会主动被Buff销毁
	- 层数减少时停止：Buff层数减少时，自动销毁
	- Buff结束时停止：Buff结束时，对应Actor销毁

---


## 变参Buff模板

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器2.0 > 变参Buff模板

**涉及API:** `ABP_TransformPreset_Chicken`

# 变参Buff模板

Buff编辑器提供了部分特化制作的功能型Buff模板，通过参数的形式提供效果设置，方便开发者直接配置应用。

<br>

## 隐身

获得持续6秒的隐身效果。

![QQ2025819-174824-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MfoQUQQ2025819-174824-HD-ezgif.com-video-to-gif-converter.gif)

|属性名|属性说明|
|-|-|
|Invisible Material|隐身的材质|
|Self Alpha|主控端视角下隐身效果的透明度，0~+∞|
|Enemy Alpha|敌方阵营视角下隐身效果的透明度，0~+∞|
|Friendly Apha|友方阵营视角下隐身效果的透明度，0~+∞|
|Invisible Color|隐身透明效果的颜色|
|Enemy Visible Distance|透明度变化阈值，与敌人距离小于该值时，透明效果将从 ``Enemy Alpha`` 变为 ``Friendly Alpha``|

<br>

## 被透视

透过障碍物揭露在指定目标的视野中，持续8秒。

![QQ2025819-175129-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5ieBwQQ2025819-175129-HD-ezgif.com-video-to-gif-converter.gif)

|属性名|属性说明|
|-|-|
|Occlusion Highlight Color|透视效果的颜色|
|Occlusion Highlight Type|透视效果生效的目标类型<br> - 仅Causer透视：透视效果仅对Buff的释放者生效<br>- Causer及其队友透视：透视效果对Buff的释放者及释放者的队友均生效<br>- 所有人：透视效果对所有人生效|

<br>

## 变身-静态模型

角色变身为指定的静态模型，该模型无动画，但可以正常移动。

![QQ20251113-2144-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mqWDyQQ20251113-2144-HD-ezgif.com-video-to-gif-converter.gif)

|属性名|属性说明|
|-|-|
|Extra Health|变身状态下获得的额外生命值，启用后生效|
|Enable Extra Health|是否启用额外生命值|
|进入变身时间|进入变身的过渡时间，该时间下人物无敌且无法操作|
|退出变身时间|退出变身的过渡时间，该时间下人物无敌且无法操作|
|变身技能模组|变身后角色获得的技能组，如果变身前角色装配了技能，则将强制替换为配置的技能组，且变身结束后还原|
|变身模型和动画类型|目前支持静态模型（Static）、主角骨骼模型（Pawn）和怪物骨骼（Preset）三种<br>变身为静态模型时，会自动隐藏携带在身上的头、包、甲、武器等外显模型|
|Mesh Relative Transform|静态模型基于角色坐标点的位置偏移/旋转偏移/缩放|
|Collision Type|静态模型的碰撞体类型，支持碰撞盒（Box）和胶囊体（Capsule）|
|Box Extend|静态模型碰撞盒的大小，针对 ``Collision Type`` 为“Box”时生效|
|Capsule Radius|胶囊体的半径，针对 ``Collision Type`` 为“Capsule”时生效|
|Capsule Height|胶囊体的半高，针对 ``Collision Type`` 为“Capsule”时生效|
|Hide Material|隐藏头、包、甲等外显模型时使用的材质，保持默认即可|
|Fade in Speed|变身过程中相机变化淡入淡出的速度|
|Offset|相机跟随目标点的偏移|
|Spring Arm Length Additive|角色弹簧臂的变化量|
|Sprint Arm Rotation|角色弹簧臂的旋转|
|Additive Offset Fov|相机FOV修改量|
|Transform Static Mesh|变身的目标静态模型|

<br>

## 变身-主角骨骼

角色变身为指定的带主角骨骼类型的怪物模型，具备角色完整的动画功能，可正常移动、攻击等。

![QQ20251113-213537-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sFUryQQ20251113-213537-HD-ezgif.com-video-to-gif-converter.gif)

|属性名|属性说明|
|-|-|
|Extra Health|变身状态下获得的额外生命值，启用后生效|
|Enable Extra Health|是否启用额外生命值|
|进入变身时间|进入变身的过渡时间，该时间下人物无敌且无法操作|
|退出变身时间|退出变身的过渡时间，该时间下人物无敌且无法操作|
|变身技能模组|变身后角色获得的技能组，如果变身前角色装配了技能，则将强制替换为配置的技能组，且变身结束后还原|
|变身模型和动画类型|目前支持静态模型（Static）、主角骨骼模型（Pawn）和怪物骨骼（Preset）三种<br>变身为静态模型时，会自动隐藏携带在身上的头、包、甲、武器等外显模型|
|骨骼模型|变身的目标骨骼模型，模型的骨骼必须为 ``主角骨骼``|
|Transform Scale|变身后骨骼模型的缩放大小，包括碰撞体和胶囊体等|
|主角动画列表|变身后需要替换的 [姿态动画](https://developer.gp.qq.com/wikieditor/#/catalog/20251) 列表|
|获取的武器ID|变身后获得的武器物品ID|
|Fade in Speed|变身过程中相机变化淡入淡出的速度|
|Offset|相机跟随目标点的偏移|
|Spring Arm Length Additive|角色弹簧臂的变化量|
|Sprint Arm Rotation|角色弹簧臂的旋转|
|Additive Offset Fov|相机FOV修改量|

<br>

## 变身-怪物骨骼

角色变身为非主角骨骼类型的怪物模型，具备角色完整的动画功能，可正常移动、攻击等。

> 目前仅支持变身为光子鸡模型，其他怪物模型存在动画与模型不匹配的问题

![QQ2026120-15433-HD-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rvPd9QQ2026120-15433-HD-ezgif.com-video-to-gif-converter.gif)

|属性名|属性说明|
|-|-|
|Extra Health|变身状态下获得的额外生命值，启用后生效|
|Enable Extra Health|是否启用额外生命值|
|进入变身时间|进入变身的过渡时间，该时间下人物无敌且无法操作|
|退出变身时间|退出变身的过渡时间，该时间下人物无敌且无法操作|
|变身技能模组|变身后角色获得的技能组，如果变身前角色装配了技能，则将强制替换为配置的技能组，且变身结束后还原|
|变身模型和动画类型|目前支持静态模型（Static）、主角骨骼模型（Pawn）和怪物骨骼（Preset）三种<br>变身为静态模型时，会自动隐藏携带在身上的头、包、甲、武器等外显模型|
|骨骼模型|变身的目标骨骼模型，模型的骨骼为非主角骨骼的其他任意怪物骨骼|
|Mesh Relative Transform|骨骼模型基于角色坐标点的位置偏移/旋转偏移/缩放|
|Collision Type|骨骼模型的碰撞体类型，支持碰撞盒（Box）和胶囊体（Capsule）|
|Preset Box Extend|骨骼模型碰撞盒的大小，针对 ``Collision Type`` 为“Box”时生效|
|Preset Capsule Radius|胶囊体的半径，针对 ``Collision Type`` 为“Capsule”时生效|
|Preset Capsule Height|胶囊体的半高，针对 ``Collision Type`` 为“Capsule”时生效|
|Preset Transform Anim|怪物模型对应的动画蓝图，目前仅光子鸡的动画蓝图 ``ABP_TransformPreset_Chicken`` 可生效|
|Fade in Speed|变身过程中相机变化淡入淡出的速度|
|Offset|相机跟随目标点的偏移|
|Spring Arm Length Additive|角色弹簧臂的变化量|
|Sprint Arm Rotation|角色弹簧臂的旋转|
|Additive Offset Fov|相机FOV修改量|

<br>

## 怪物变身

怪物变身为静态模型或者其他骨骼类型的怪物模型，具备怪物完整的动画功能，可正常寻路、攻击等。

![2026-04-0311-40-42-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lxQW72026-04-0311-40-42-ezgif.com-video-to-gif-converter.gif)

|属性名|属性说明|
|-|-|
|TransformMeshType|StaticMesh/SkeletalMesh，变身后的模型是静态模型还是骨骼模型|
|Mesh Relative Transform|骨骼模型基于角色坐标点的位置偏移/旋转偏移/缩放|
|Preset Capsule Radius|胶囊体的半径，针对 ``Collision Type`` 为“Capsule”时生效|
|Preset Capsule Height|胶囊体的半高，针对 ``Collision Type`` 为“Capsule”时生效|
|怪物动画替换列表|变身为新怪后，新怪每一对应的动画行为，对应需要被替换的动画|
|进入变身时间|进入变身的过渡时间，该时间下人物无敌且无法操作|
|退出变身时间|退出变身的过渡时间，该时间下人物无敌且无法操作|
|Extra Health|变身状态下获得的额外生命值，启用后生效|
|Enable Extra Health|是否启用额外生命值|
|变身技能模组|变身后怪物获得的技能组，如果变身前怪物装配了技能，则将强制替换为配置的技能组，且变身结束后还原|
|BehaviorTree Settings|变身后怪物的行为设置，可以替换怪物变身后的行为树，且配置行为树的参数，变身结束后，怪物的行为还原|


---
