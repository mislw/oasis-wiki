# 进阶内容/GamePlay系统/技能系统/Buff编辑器2.0

> 官方知识库同步分类，共 4 篇文章

---

## BuffAction查询手册

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器2.0 > BuffAction查询手册

> 文档ID: 20117 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20117)

> 新增: 2026-04-20 16:22:19

**涉及API/标识符:** `None`

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

## BuffListUI

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器2.0 > BuffListUI

> 文档ID: 20444 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20444)

> 新增: 2026-08-12 10:15:59

**涉及API/标识符:** `ActivePassives`, `AlwaysShow`, `ArrangeEffects`, `Button_Expand`, `DisplayEffects`, `groupBox.OnUpdateItem`, `IsExpanded`, `PersistEffectBuff`, `ShowEffectList`, `UE.LoadClass`, `UGCGameSystem.GetLocalPlayerController`, `UPESkillPassiveSkill`, `Widget`, `WrapGroupBox`

# BuffListUI

## 功能概述

支持玩家屏幕的 [Buff](https://developer.gp.qq.com/wikieditor/#/catalog/20087) 和 [被动技能](https://developer.gp.qq.com/wikieditor/#/catalog/20110) 列表 UI，支持展开/收起、动态增删、多行自动排版。

|功能|说明|
|-|-|
|Buff 显示|显示玩家身上的 ``PersistEffectBuff`` 类型效果（需 ``bShowUI = true`` ）|
|被动技能显示|显示已激活且类型为 ``AlwaysShow`` 的被动技能 ( ``UPESkillPassiveSkill`` )|
|展开/收起|点击按钮切换两种模式，收起时显示 11 个 【+】 箭头按钮，展开时最多显示 23 个|
|动态增删|监听 Buff 增删和被动技能状态变化，实时更新 UI|
|多行自动排版|4 个 ``WrapGroupBox`` 容器，按需显隐和分配子项，支持自动换行|
|显示顺序保证|通过 ``SelectSkill()`` 统一排序，确保显示顺序与效果添加顺序一致|

<br>

## 快速配置

### 创建BuffListUI

在UI编辑器中，选择 【元件】 → 【系统】 → 【BuffList】 进行创建

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9MF82image.png)

<br>

### 加入到战斗主UI界面显示

BuffList基本没有可手动配置的参数，创建出来后直接使用即可实现对应功能

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8Mq6uimage.png)

<br>

## UI 结构说明

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IlGw5image.png)

## 核心数据结构

```lua
-- 内部状态表（定义在文件顶部）
{
    bInitDoOnce = false,          -- 防重复初始化标记
    BuffList = {},                -- Buff 原始列表
    ActivePassives = {},          -- 已激活的被动技能（AlwaysShow 类型）
    DisplayEffects = {},          -- 合并后的待显示效果列表（Buff + 被动技能）
    WrapGroupBoxes = {},          -- 4个容器的引用数组
    IsExpanded = false,           -- 当前是否展开
    ListenComp = nil,             -- 消息监听组件引用
    ShowEffectList = {},          -- 最终实际渲染的效果列表（截取后）
}
```

<br>

### 关键数组关系

```lua
角色身上的 Effect 数据
        │
        ▼
  GetAllEffects() ──────────► 原始全量数据
        │
        ▼
  SelectSkill() ─────────────► 过滤+排序
        │                      - Buff: 仅保留 bShowUI=true
        │                      - 被动: 仅保留 ActivePassives 中存在的
        ▼
  DisplayEffects[] ──────────► 合并后待显示列表
        │
        ▼
  UpdateEffectList() ────────► 按模式截取
        │                      - 收起: 最多11个（或12个特殊处理）
        │                      - 展开: 最多23个
        ▼
  ShowEffectList[] ──────────► 最终渲染列表
        │
        ▼
  ArrangeEffects() ──────────► 分配到4个 WrapGroupBox 并刷新UI
```

<br>

### 生命周期

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/02jVXimage.png)

## 显示规则与容量

**模式对比**

|状态|显示数量|特殊条件|
|-|-|-|
|收起 (``IsExpanded=false``)|≤ 11 个|当 ``DisplayEffects == 12`` 时临时改为显示 23 个|
|展开 (``IsExpanded=true``)|≤ 23 个|正常满容量展示|
|≤ 12 个总效果|全部显示|不显示展开按钮|

**展开按钮显隐逻辑**

- DisplayEffects 数量 > 12  →  Button_Expand 可见
- DisplayEffects 数量 ≤ 12  →  Button_Expand 隐藏

**UI 自动分配策略（ArrangeEffects）**

当需要 增加 UI 时：
- 如果 WrapGroupBox_01 未满（<5）→ 直接添加
- 如果 WrapGroupBox_01 已满且有隐藏的 WrapBox → 将01的内容迁移到新WrapBox，再添加新项
- 收起模式下从 WrapGroupBox_04 向前查找空位；特殊情况 DisplayEffects==12 时从01开始

当需要 减少 UI 时：
- 如果 WrapGroupBox_01 有内容 → 从末尾移除
- 如果 WrapGroupBox_01 为空 → 从 WrapGroupBox_02~04 中找到有内容的，将其前5个迁移回01并隐藏该WrapBox

<br>

## 使用示例

### 基础使用（自动运行）

BuffList_0 是一个自包含组件，一旦被创建并 AddToViewport 即可自动运行：

```lua
-- 在 UGCGameState 或 HUD 的 Lua 脚本中
function MyHUD:ReceiveBeginPlay()
    local BuffListClass = UE.LoadClass("/Game/.../BuffList_0.BuffList_0_C")
    local PC = UGCGameSystem.GetLocalPlayerController()

    self.BuffListWidget = UserWidget.NewWidgetObjectBP(PC, BuffListClass)
    if self.BuffListWidget then
        -- 添加到视口即可，内部会自动完成初始化
        self.BuffListWidget:AddToViewport(100)
    end
end
```

组件会自动获取：
1. 获取本地 PlayerController 和 Pawn
2. 绑定 Buff/被动技能的事件监听
3. 首次扫描已有的效果并显示

<br>

### 手动触发刷新

```lua
-- 强制刷新所有效果显示
if self.BuffListWidget then
    self.BuffListWidget.DisplayEffects = self.BuffListWidget:SelectSkill()
    self.BuffListWidget:UpdateEffectList()
end
```

<br>

### 程序化展开/收起

```lua
-- 代码中控制展开收起（等同于点击按钮）
if self.BuffListWidget then
    self.BuffListWidget.IsExpanded = true  -- 或 false
    self.BuffListWidget.WidgetSwitcher_Expand:SetActiveWidgetIndex(
        self.BuffListWidget.IsExpanded and 0 or 1
    )
    self.BuffListWidget:UpdateEffectList()
end
```

<br>

### 查询当前显示状态

```lua
-- 获取当前正在显示的效果数量
local count = self.BuffListWidget:GetCurrentUICount()

-- 获取所有Buff子Widget
local allWidgets = self.BuffListWidget:GetAllWidgetInWrapBox()
for i, widget in ipairs(allWidgets) do
    print(string.format("Slot %d: %s", i, tostring(widget)))
end
```

<br>

### 自定义 Buff 过滤

如果需要在 ``SelectSkill()`` 基础上追加额外过滤逻辑：

```lua
-- 可以覆写 SelectSkill 或在其之后做二次过滤
local originalSelect = self.BuffListWidget.SelectSkill
self.BuffListWidget.SelectSkill = function(self)
    local effects = originalSelect(self)
    -- 自定义过滤：例如排除特定ID的Buff
    local filtered = {}
    for _, eff in ipairs(effects) do
        if not self:IsHiddenBuff(eff) then
            table.insert(filtered, eff)
        end
    end
    return filtered
end
```

<br>

## 核心 API 参考

### 效果获取函数

|函数名|说明|
|-|-|
|GetAllBuffList|获取玩家身上所有 ``PersistEffectBuff`` 类型的效果|
|GetAllPassiveSkillList|获取玩家所有被动技能|
|GetAllEffects|获取合并的全部效果数据（供 ``SelectSkill()`` 使用）|

<br>

### 显示筛选

|函数名|说明|
|-|-|
|SelectSkill|从全部 Effect 中按顺序筛选出需要显示的|

规则：
- 遍历 GetAllEffects() 返回的所有效果
- 如果是 Buff 类型：仅保留 bShowUI == true 的
- 如果是 被动技能类型：仅在 ActivePassives 列表中存在的才保留
- 保持原始顺序（即添加顺序）

<br>

### UI 刷新链路

**UpdateEffectList**

截取 DisplayEffects 生成 ShowEffectList，触发重新排版：
1. 根据 ``IsExpanded`` 确定显示上限（11 或 23）
2. 特殊处理：``DisplayEffects`` == 12 时强制上限为 23
3. 控制 ``Button_Expand`` 的显隐
4. 若总数 ≤ 上限：取全部
5. 若总数 > 上限：取最后 N 个（最新添加的优先显示）
6. 调用 ``ArrangeEffects``() 排版

**ArrangeEffects**

根据 ``ShowEffectList`` 长度与当前 UI 数量对比，执行增删操作，然后调用 ``RefreshByShowEffectList()``

**RefreshByShowEffectList**

遍历所有 WrapGroupBox 中的已有子项，逐个设置数据：
- Buff 类型 → 调用 ``SetBuffinfo(buffData)``
- 被动技能类型 → 调用 ``SetPassiveSkillInfo(skillData)``

<br>

### 事件回调

|事件函数名|说明|
|-|-|
|OnEffectApplied|新效果添加时的回调|
|OnEffectUnapplied|获取玩家所有被动技能|
|OnExpandButtonClicked|获取合并的全部效果数据（供 ``SelectSkill()`` 使用）|
|OnUpdateItemEffect|WrapGroupBox 创建/更新子项时的回调（通过 ``groupBox.OnUpdateItem`` 绑定）|

<br>

### 辅助函数

|函数名|说明|
|-|-|
|CreateOneWrapGroupBoxChildUI|创建单个 ``030_Buff_Item_UIBP`` 子项 Widget 实例|
|GetCurrentUICount|统计4个 ``WrapGroupBox`` 中所有子项的总数|
|GetAllWidgetInWrapBox|获取所有 ``WrapGroupBox`` 中的全部子 ``Widget`` 引用|
|RemoveActivePassive|从 ``ActivePassives`` 数组中移除指定被动技能|

---

## Buff编辑器

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器2.0 > Buff编辑器

> 文档ID: 20087 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20087)

> 更新: 2026-02-12 10:47:02

**涉及API/标识符:** `AddBuffByClass`, `AddBuffByClass:~:text=UPersistEffectBuff-,AddBuffByClass,-(AActorTargetActor`, `Buff`, `UGCGameSystem.GetUGCResourcesFullPath`, `UGCObjectUtility.LoadClass`, `UGCPersistEffectSystem`, `UGCPersistEffectSystem.AddBuffByClass`, `UGCPlayerController`, `UPersistEffectBuff`

# Buff编辑器

Buff是针对特定对象附加临时或永久属性、能力或者特殊效果的机制，根据效果归属强化或者负面限制的不同分为增益型Buff和减益型Debuff，同时Buff存在可堆叠的特性，例如叠加2层的流血Buff可以让角色受到的伤害加倍，通过引入Buff机制能够提升玩法的长线养成能力、增强战斗的策略竞技性、促进环境的可互动性。

Buff编辑器将常规的Buff生命周期抽象为一系列逻辑判定与执行节点，允许开发者通过蓝图配置的方式填充各节点的执行动作，高效地实现Buff效果，也支持重写Lua函数以实现定制化的Buff构建需求。

<br>

## Buff生命周期

Buff编辑器将Buff从赋予对象至生效并结束的完整生命周期拆解为 ``添加阶段`` 、`合并阶段` 和 ``执行阶段``，各配置参数项即围绕这两个阶段的条件与执行节点进行设定。

**添加阶段**

为对象初次添加Buff和重复添加Buff时，实际的添加效果因设定的合并方式不同而存在差异，具体的添加流程遵循以下规则：

![添加.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FaxgN%E6%B7%BB%E5%8A%A0.png)

1. 在尝试将Buff添加到目标实体前，首先检查目标实体是否可以接收该Buff，如果无法添加Buff（例如处于异常状态下），则流程终止；否则进入步骤2
2. 允许添加，继续判断目标实体是否已经拥有该类型的Buff，如果不存在则直接为实体对象添加新的Buff实例，流程结束；否则进入步骤3
3. 目标实体已经拥有此类型的Buff，继续判断Buff自身的合并类型，若无法合并或者非同一施加来源的Buff，则直接为实体对象添加新的Buff实例，流程结束；否则进入合并阶段

---

**合并阶段**

依据合并行为（刷新时间/追加持续时间/堆叠层数）决定实体对象最终的Buff状态：

![合并.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vbLBr%E5%90%88%E5%B9%B6.png)

1. 进入合并阶段后，首先判断Buff的合并方式：如果是非堆叠类型，则进入步骤2；如果是堆叠类型，则进入步骤3。
2. 对于非堆叠类型的合并处理：刷新操作会将已有Buff的持续时间重置为初始值重新计时；追加操作则会将新Buff的持续时间累加到已有Buff的剩余时间上。
3. 对于堆叠类型的处理：首先为已有Buff增加一层，当总层数超过1时，需要根据堆叠规则调整持续时间。若采用 `结束` ，当第一层Buff结束时所有层数同时失效。若采用 `每层结束刷新` ，当每层结束时去掉此层并将Buff的持续时间刷新至初始值。若采用 `每层独立计时` ，则每层单独计算持续时间，移除某一层时不影响其他层。

---

**执行阶段**

Buff的执行过程由生命周期计时器和效果触发计时器共同管理，生命周期计时器用于追踪Buff的持续时间，管理Buff的有效周期；效果触发计时器负责定时调度触发Buff的效果执行动作，具体的执行流程遵循以下规则：

![执行.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0i9l5%E6%89%A7%E8%A1%8C.png)

1. 首先触发 ``Buff开始事件``，设定触发时机为设Buff开始时的动作将在此时被执行，同时分别启动生命周期计时器和效果触发计时器
2. 生命周期计时器开始计时，若Buff持续时间已经结束，触发 ``Buff结束事件``，触发时机设为Buff结束时的动作将在此时被执行，随即移除Buff实例；否则重置计时器并重新计时
3. 效果触发计时器开始计时，在Buff有效生命周期内循环定时触发 ``Buff触发事件``，触发时机设为Buff触发时的动作将在此时被执行；当Buff生命周期结束时，将强行中断效果触发计时器，所有Buff效果不再生效

<br>

## 编辑器界面

点击绿洲启元编辑器菜单栏的【技能编辑器】按钮，打开技能编辑器的操作界面，在左侧类型栏中选择 ```Buff``` 将切换到Buff编辑界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HkO19image.png)

**A. 工程Buff资源**

工程内通过Buff编辑器创建的所有Buff蓝图将显示在该资源列表中，双击可打开已创建过的Buff蓝图。

**B. Buff模板**

编辑器已经预置了一批Buff模板供使用，开发者基于模板创建Buff蓝图并配置Buff效果。

**C. Buff蓝图配置面板**

Buff的核心属性配置区域，包括Buff的UI展示信息、合并行为、触发效果等。

<br>

## Buff模板

Buff编辑器预置了伤害型、异常状态、增益效果三大类型的Buff模板，各类型下提供了具体的Buff蓝图示例，开发者可以基于示例模板创建Buff蓝图进行二次定制；另外，提供了部分特化的 [功能型Buff](https://developer.gp.qq.com/wikieditor/#/catalog/20253) 供开发者直接使用，开发者也能够使用空模板制作全新的Buff效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZUaJ9image.png)

**空模板**

不带有任何预设属性配置的Buff蓝图，需要开发者从0开始配置。

---

**伤害型模板**

【流血】

每0.5秒失去10生命值，持续2秒；每叠加一层Buff时，会延长一层Buff的持续时间

![流血.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vx3Jn%E6%B5%81%E8%A1%80.gif)

【燃烧】

每秒受到25点伤害；Buff可叠加，最多叠加3层。

![燃烧.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QXpzc%E7%87%83%E7%83%A7.gif)

【定时炸弹】

给予角色一枚定时炸弹，炸弹3秒后爆炸，造成30伤害

![QQ20250408172311-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/FOznNQQ20250408172311-ezgif.com-video-to-gif-converter.gif)

---

**异常状态模板**

【冰冻】

使移动速度减少20%，持续3秒；Buff可叠加，最多叠加5层。

![冰冻.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/E84aj%E5%86%B0%E5%86%BB.gif)

【荆棘束缚】

每秒受到15点伤害且无法移动，持续3秒。

![荆棘束缚.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VXeBS%E8%8D%86%E6%A3%98%E6%9D%9F%E7%BC%9A.gif)

【眩晕】

造成3秒的眩晕，无法移动且无法使用技能。

![晕眩.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WN3PO%E6%99%95%E7%9C%A9.gif)

---

**增益效果模板**

【战意】

在角色移速增幅大于30%时增加20%的技能冷却效率，持续5秒。

【生命之赐】

在buff持续时间内，当生命值低于60%时，每0.1秒恢复最大生命值的2%

![生命.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZOOUE%E7%94%9F%E5%91%BD.gif)

<br>

## Buff创建流程

### 新建Buff蓝图

以基于 ``定时炸弹`` 模板创建Buff蓝图为例：

1. 从“Buff模板”窗口中选择定时炸弹模板，下方“选择模板创建”按钮将高亮显示，并更名为“以 ``定时炸弹`` 为模板创建”
2. 点击“以 ``定时炸弹`` 为模板创建” 按钮，弹出输入名称弹窗，输入Buff名称并点击确定
3. 新建的Buff蓝图将显示在“工程Buff资源”窗口中，且Buff蓝图创建于 ``Asset/Blueprint/Prefabs/Buffs`` 路径下

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WXtWkimage.png)

<br>

### 配置Buff蓝图

#### 启用Buff栏控件

Buff编辑器为主界面额外提供了Buff栏控件，当Buff生效时将在Buff栏处显示Buff的图标及层数，长按对应Buff出现详情面板。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dhlsLimage.png)

在资源目录中搜索“UGC_DefaultMainUI”，或者在路径 ```和平精英/资源/UI资源/UI模板/战斗界面``` 下找到该控件蓝图，右键 ```复制引用路径```。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/guxahimage.png)

打开 ```UGCPlayerController``` 蓝图，在属性栏中搜索“Main UIClass”，右键 ```粘贴``` 将控件蓝图赋予该属性。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/36uvsimage.png)

---

#### Buff基础信息

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ukvl1image.png)

- 生效时长：单层Buff的默认持续时间，设置<0的值代表永久生效，Buff实际时长受合并效果影响
- 类型Tags：通过 [GameplayTag](https://developer.gp.qq.com/wikieditor/#/catalog/20102) 标记的Buff类型，适用于筛选和分类场景，遵循 [GameplayTag匹配规则](https://developer.gp.qq.com/wikieditor/#/catalog/20102?autoJump=GameplayTag%E5%8C%B9%E9%85%8D)

---

#### Buff UI信息

启用Buff栏控件后，开发者可选择是否将Buff状态的UI显示在Buff栏，相关配置在 ``Buff Info`` 属性组下。

![Buff UI.jpg](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GT4HkBuff%20UI.jpg)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/R8sB4image.png)

- 名字：Buff的名称
- 描述：Buff的描述说明，只显示在Buff详情面板
- 图标：Buff的icon图标
- 是否显示UI：是否将UI信息显示在Buff栏中

> 开发者也可以利用 [``UPersistEffectBuff``](https://developer.gp.qq.com/api/#/searchContent/UPersistEffectBuff?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUPersistEffectBuff.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UPersistEffectBuff) 提供的查询类API自行实现Buff的UI外显效果

---

#### 状态互斥

通常为对象添加Buff前，需要考虑对象所处的状态，以及添加Buff后为对象带来的额外状态效果，例如：
- 角色在移动状态下无法获得此Buff
- 角色获得Buff时进入无敌/免疫特定伤害的状态
- ……

Buff编辑器通过状态组的配置形式，将预设的互斥关系应用在添加Buff阶段，当满足添加条件时Buff才能挂载成功。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VTNuAimage.png)

- 阻碍Tag：如果对象身上携带该项配置的任一状态Tag，则无法被添加Buff
- 拥有Tag：获得该Buff时，将会给对象添加的状态Tag
- 打断Tag：当Buff添加到对象身上时，如果对象拥有这些状态Tag，则这些Tag及其关联的技能或Buff都将被移除
- 禁用Tag：当Buff添加到对象身上时，如果对象拥有这些状态Tag，则这些Tag及其关联的技能或Buff都将被移除，且拥有这些Tag的技能或Buff无法再次施加给对象

> 更多关于角色状态的概念及互斥逻辑关系可参考 [状态互斥](https://developer.gp.qq.com/wikieditor/#/catalog/20106) 文档

---

#### 合并Buff

Buff编辑器将堆叠特性分解为 ``合并条件`` 与 ``合并行为`` 的组合，并提供了相应的可配置属性，满足复合的堆叠配置需求。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cagOfimage.png)

|属性名|属性说明|
|-|-|
|合并条件|当一个新的Buff实例被添加时，是否与已拥有的Buff进行合并<br>- 无法合并：不发生合并，按新的Buff实例添加<br>- 同类型合并：如果已拥有的Buff类型和新添加的Buff类型相同，则允许合并<br>- 同施放者且同类型合并：如果已拥有的Buff类型和新添加的Buff类型相同，且施放的来源相同才允许合并|
|合并行为|当触发Buff合并时，决定合并的处理效果，该属性为可复选项<br>- 追加时长：追加已拥有Buff的持续时间<br>- 刷新Buff：以Buff的初始生效时长为准刷新已拥有Buff的剩余持续时间，并触发行为的刷新效果<br>- 堆叠：为已拥有的Buff堆叠一层，即增加一层Buff的层数<br>- 重置时长：仅以Buff的初始生效时长为准重置已拥有Buff的剩余持续时间<br>- 无合并行为：如果未选择以上任何选项，则不执行任何操作，新添加的Buff实例会被“吞掉”，等同于没有发生实际添加效果|

> 1. 在条件优先级关系上， 合并条件 > 合并行为 > 最大堆叠次数
> 2. 如果同时选择了“追加时长”与“刷新时长”，则两个效果同时生效，例如：一个持续10秒的Buff已生效5秒（即剩余5秒），此时再次添加同类buff，则当前Buff时长刷新回10秒且额外追加10秒，即该Buff还会持续20秒

---

#### Buff堆叠

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KwIaGimage.png)

堆叠允许多个相同类型的效果叠加，以增强角色的能力或状态，Buff编辑器提供了 ``最大堆叠次数`` 和 ``堆叠持续时长`` 来控制Buff的堆叠效果。

- 最大堆叠次数：同类型的Buff允许堆叠的前提下，能够叠加的最大层数
- 堆叠持续时长：当最大堆叠次数>1时，需要设置堆叠后Buff的持续时间的计算方式
	- 结束：所有层数的Buff共享同一个持续时长，只有第一层Buff的持续时间被计算，当第一层Buff结束时其他所有层的Buff也都被移除，例如：第一层Buff的生效时长是5秒，其他层数的Buff到了第5秒也都结束，buff的总持续时长为5秒
	- 每层结束刷新时间：当一层Buff的时间结束时，堆叠层数-1并重新刷新buff的时间，例如：玩家堆叠了3层Buff，每层的持续时间是5秒，第1层结束后，剩下两层将重新开始计时，直至最后一层buff结束，buff的总持续时长为15秒
	- 每层独立计算时间：每一层Buff的持续时间完全独立计算，各自计算该层的持续时间，例如：第一层Buff的生效时长是5秒，第二层Buff也是5秒，第三层Buff是8秒，则第8秒时该Buff结束，buff的总持续时长为8秒

---

#### 触发效果

在Buff生命周期内的特定时机或者周期性触发的具体动作，这些动作决定了对象受到的Buff效果影响，Buff编辑器通过数组的形式配置效果集合，且允许为各动作设置不同的触发时机。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PPXVYimage.png)

【触发时机】

支持Buff的开始/结束、间隔、堆叠时触发，支持复选时机条件，即同一动作可以在多种时机下被触发。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7FC3Jimage.png)

- 开始：随 ``Buff开始事件`` 时触发，根据当前层数触发所有层的效果
- 结束：随 ``Buff结束事件`` 时触发，根据当前层数触发所有层的效果
- 间隔：按指定间隔时间周期性触发，根据当前层数触发所有层的效果
	- 触发间隔：触发的间隔时间，仅 ``触发效果时机`` 选择“间隔”时设置
- 堆叠：Buff堆叠层数发生变化时触发对应层数的效果
	- 触发条件：指定触发需要满足的层数关系，通过“关系运算符”和“条件数值”组合，例如可以设置条件为 ``>3`` 或 ``=2``；如果选为“无条件”，则只要发生了堆叠即触发，仅 ``触发效果时机`` 选择“堆叠”时设置
- 效果触发延迟：效果真正触发的延迟时间，例如配置为1秒，则代表触发该效果时，实际会在延迟1秒后才真正执行，对所有时机类型均生效

【触发动作】

Buff编辑器预置了一批动作Action，各动作配置属性不同，可参考 [BuffAction查询手册](https://developer.gp.qq.com/wikieditor/#/catalog/20117) 部分内容。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zfM5Timage.png)

<br>

## 使用Buff

Buff可以随技能触发激活，也可以在脚本中调用API动态给对象添加/移除Buff。

### 通过技能激活Buff

技能编辑器提供了 [``添加Buff``](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E6%B7%BB%E5%8A%A0Buff) 和 [``移除Buff``](https://developer.gp.qq.com/wikieditor/#/catalog/20094?autoJump=%E6%8A%80%E8%83%BDTask-%E7%A7%BB%E9%99%A4Buff) 的技能节点，配置在时间轴上，施放该技能时将在指定的时间点执行添加/移除Buff。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/B4WFvimage.png)

---

### 脚本动态添加Buff

[UGCPersistEffectSystem](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem) 库提供了添加和移除Buff的API，例如 [``AddBuffByClass``](https://developer.gp.qq.com/api/#/searchContent/UGCPersistEffectSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E6%8A%80%E8%83%BD%E7%B3%BB%E7%BB%9F%2FUGCPersistEffectSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCPersistEffectSystem&autoJump=AddBuffByClass:~:text=UPersistEffectBuff-,AddBuffByClass,-(AActorTargetActor)) 可以给目标对象添加Buff。

代码示例：

```lua
local BuffTarget = self:GetPlayerCharacterSafety()
local BuffClass = UGCObjectUtility.LoadClass(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Prefabs/Buffs/TickBomb.TickBomb_C'));
UGCPersistEffectSystem.AddBuffByClass(BuffTarget, BuffClass)
```

---

## 变参Buff模板

> 文档路径: 进阶内容 > GamePlay系统 > 技能系统 > Buff编辑器2.0 > 变参Buff模板

> 文档ID: 20253 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20253)

> 新增: 2026-04-20 16:22:28 | 更新: 2026-09-08 18:58:51

**涉及API/标识符:** `ABP_TransformPreset_Chicken`

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
|Preset Transform Anim|怪物模型对应的动画蓝图，参考设置光子鸡 ``ABP_TransformPreset_Chicken`` |
|Fade in Speed|变身过程中相机变化淡入淡出的速度|
|Offset|相机跟随目标点的偏移|
|Spring Arm Length Additive|角色弹簧臂的变化量|
|Sprint Arm Rotation|角色弹簧臂的旋转|
|Additive Offset Fov|相机FOV修改量|

<br>

### 动画蓝图ABP使用说明

对上述Preset Transform Anim动画蓝图进行说明

首先创建动画蓝图

<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YuDKtimage.png" width = "700">

<br>

动画蓝图创建时，选择

<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/O7SVKimage.png" width = "700">

<br>

创建后动画蓝图后，需配置动画蓝图的默认参数进行动画列表的替换——即控制变身的模型在执行对应行为时播放什么动画。

<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/v7GgSimage.png" width = "1200">

<br>

（注意，建议只修改动画蓝图这里的动画列表相关参数，不用轻易修改其余配置项，否则可能出现配置项不正确的情况。）

MoveBlendSpace：代表变身模型移动时使用的移动动画资产。是一个BlendSpace资产。

<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/tD0ylimage.png" width = "1200">

<br>

该移动BlendSpace的创建需要遵守一定的规范

|参数名|参数说明|
|-|-|
|水平坐标名称|需要配置为WalkRight，且取值范围需要配置为真实速度的取值范围，运行时，实际会将真实速度在角色右朝向的分量传进来（比如此时角色朝左运动，则此时传进来的值为-[移动速度]，朝右运动，则此时传进来的值为[移动速度]）|
|垂直坐标名称|需要配置为WalkForward，且取值范围需要配置为真实速度的取值范围，运行时，实际会将真实速度在角色前朝向的分量传进来（比如此时角色朝前运动，则此时传进来的值为[移动速度]，朝后运动，则此时传进来的值为-[移动速度]）|
|Blend Samples|根据实际的需要，将左走、右走、前走、后走等不同动画配置到不同的位置即可|
|InPlaceJumpAnim|原地起跳使用的动作|
|ForwardJumpAnim|向前起跳使用的动作|
|FallingAnim|在空中滞空的Loop动作|
|LandingLightAnim|轻落地动作|
|LandingHardAnim|重落地动作|
|HurtAnim|被攻击时播放的动画。该动作需要是一个叠加类型的动作资产|
|DeathMontage|死亡时播放的蒙太奇。该资产需要为一个蒙太奇。且该蒙太奇的最后一个阶段需要为循环且卡在死亡动画的最后一帧（这是为了保证死亡过程中死亡动画播完且目标还未销毁时，目标最后可以保留在一个静止的死亡Pose）|

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
