# 进阶内容/UI系统

> 官方知识库同步分类，共 16 篇文章

---

## Tips系统

> 文档路径: 进阶内容 > UI系统 > Tips系统

> 文档ID: 20445 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20445)

> 新增: 2026-09-02 13:56:10

**涉及API/标识符:** `BPDoActionsWhenNewTipBegin`, `BPDoActionsWhenNewTipEnd`, `PlayAnimation`, `UE.IsValid`, `UGCGameSystem.ClearTimer`, `UGCGameSystem.GameState`, `UGCGameSystem.SetTimer`, `UGCWidgetManagerSystem.ShowCustomTipsByID`, `UGCWidgetManagerSystem.ShowCustomTipsByIDWithPC`, `UUserWidget`

# Tips系统

可以基于该系统，配置游戏中常见的弹框消息提示，通常用于一些任务的提示、功能的引导。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VC5Vvimage.png)

<br>

## Tips表

点击【表格管理器】->【功能表格】->【Tips表】创建TIps表进行Tips的相关配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/evmMpimage.png)

参数说明：
+ TipsID：Tips的ID，在代码里用接口显示对应Tips时，依赖ID进行查询。
+ 优先级：当下一条Tips进行显示，而前一条Tips还未完全隐藏时，依赖该优先级确定是否顶替。若优先级更大，则会进行顶替。优先级最大支持到3。即该优先级配置只能配置为0，1，2，3。
+ 是否可以被同等级顶替：如果两条Tips优先级一样，勾选该选项时，可以被优先级一致的Tips顶替。
+ 持续时间：tips的持续时间，优先级低于`Tips调用接口`。
+ 默认文本：该Tips的默认文本，可以使用富文本。
+ TipsUI蓝图：显示Tips的UI蓝图。支持在工程内使用对应UI模板创建自定义的Tips覆盖默认Tips蓝图。

---

### Tips调用接口

**客户端调用**

```lua
---生效范围：客户端
-- @param ID Tips表ID
-- @param TipsContent Tips的覆盖文本。若有，则会用该文本覆盖原本表里配置的默认文本
-- @param ExtraParam 动态黑板参数，可以构造动态参数传入Tips蓝图。
function UGCWidgetManagerSystem.ShowCustomTipsByID(ID, TipsContent, ExtraParam)
```

在对应客户端，根据ID找Tips表里定义的Tips，显示对应Tips。

```lua
function test:Button_3_OnClicked()
	UGCWidgetManagerSystem.ShowCustomTipsByID(1, "击杀成功！")
	return nil;
end
```

**服务端调用**

```lua
---生效范围：服务端
-- @param ID Tips表ID
-- @param TipsContent Tips的覆盖文本。若有，则会用该文本覆盖原本表里配置的默认文本
-- @param PlayerController 对应显示该Tips的玩家的Controller
function UGCWidgetManagerSystem.ShowCustomTipsByIDWithPC(ID, TipsContent, PlayerController)
```
在服务端，根据对应PlayerController，给对应玩家显示相应Tips。


```lua
function UGCGameState:ReceiveTick(DeltaTime)
    self.Timer = (self.Timer or 0) + DeltaTime
    if self.Timer >= 5.0 then
        self.Timer = self.Timer - 5.0
        local GameState = UGCGameSystem.GameState
        if GameState and GameState.PlayerArray then
            for _, PlayerState in pairs(GameState.PlayerArray) do
                if UE.IsValid(PlayerState) then
                    local PlayerKey = PlayerState:GetPlayerKey()
                    if PlayerKey then
                        local PC = ScriptGameplayStatics.GetPlayerControllerByPlayerKey(GameState, PlayerKey)
                        if UE.IsValid(PC) then
                            UGCWidgetManagerSystem.ShowCustomTipsByIDWithPC(1, "Boss 即将出现！", PC)
                        end
                    end
                end
            end
        end
    end
end
```

<br>

## 自定义Tips扩展

### UI模板

点击【UI编辑器】->【元件】->【消息提示】创建自定义TipsUI蓝图。可基于该蓝图进行自定义扩展。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/usuppimage.png)

---

### 数据结构
`BPDoActionsWhenNewTipBegin`是TipsUI刚显示进行构造时调用的函数，会传入一个data数据。

```lua
function testTips2:BPDoActionsWhenNewTipBegin(data)
    self.TopTips_Content:SetText(tostring(data.FinalContext))
    if CheckObjectContainsField(self, 'FadeIn') then
        self:StopAnimation(self.FadeIn)
        self:PlayAnimation(self.FadeIn, 0, 1, EUMGSequencePlayMode.Forward, 1)
    end
    if self.Timer then
        UGCGameSystem.ClearTimer(self, self.Timer)
        self.Timer = nil
    end
    local SelfWeakObjectPtr = WeakObjectPtr(self)
    self.Timer = UGCGameSystem.SetTimer(self,
        function ()
            local self = SelfWeakObjectPtr:Get()
            if self == nil then return end
            if CheckObjectContainsField(self, 'FadeOut') then
                self:StopAnimation(self.FadeOut)
                self:PlayAnimation(self.FadeOut, 0, 1, EUMGSequencePlayMode.Forward, 1)
            end
        end,
    data.PlayLength - 0.5,
    false)
end
```

以下为data数据含义参考。

```lua
    data.FinalContext      -- FText 最终文本
    data.ExtraParam        -- UUAEBlackboard* 调用方传入的额外参数
    data.PlayLength        -- float 持续时间
    data.Priority          -- uint8 优先级
    data.bCanBeReplaced    -- bool 可否被顶替
    data.TopTipWidget      -- TSoftClassPtr 覆盖的 Widget 类引用
		data.Offset            -- FVector2D 偏移量
		data.AnimationName     -- string 播放动画名
```

`BPDoActionsWhenNewTipEnd`是TipsUI持续时间结束，被隐藏时调用的函数事件。

---

### 淡入淡出动画

可参考Tips模板里的用法，在UI编辑器里配置对应组件的动画效果。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YbhLUimage.png)

在TipsUI构造时，使用[`PlayAnimation`](https://developer.gp.qq.com/api/#/searchContent/UUserWidget?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUUserWidget.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UUserWidget&autoJump=PlayAnimation)进行淡入淡出动画的播放。
> 淡出动画的延迟播放时间=tips持续时间 - 淡出动画时间

```lua
function testTips2:BPDoActionsWhenNewTipBegin(data)
  if CheckObjectContainsField(self, 'FadeIn') then
          self:StopAnimation(self.FadeIn)
          self:PlayAnimation(self.FadeIn, 0, 1, EUMGSequencePlayMode.Forward, 1)
      end
      self.Timer = UGCGameSystem.SetTimer(self,
                  function ()
                      if CheckObjectContainsField(self, 'FadeOut') then
                      self:StopAnimation(self.FadeOut)
                      self:PlayAnimation(self.FadeOut, 0, 1, EUMGSequencePlayMode.Forward, 1)
                      end
                  end,
                  data.PlayLength - 0.5,
                  false)
end
```

---

### 使用动态黑板参数

可以利用黑板透传Tips的动态参数。
调用时构造黑板并传入。

```lua
local BlackBoardClass = LoadClass("/Script/UAESharedModule.UAEBlackboard")
local BlackBoard = ScriptGameplayStatics.NewObject(self, BlackBoardClass)
BlackBoard:SetValueAsInt({SelectedKeyName = "ImageIndex"}, 2, true)
UGCWidgetManagerSystem.ShowCustomTipsByID(1, nil, BlackBoard)
```

构造TipsUI时使用传入的黑板参数。

```lua
function testTips2:BPDoActionsWhenNewTipBegin(data)
    self.TopTips_Content:SetText(tostring(data.FinalContext))
    local ExtraParam = data.ExtraParam
    if ExtraParam then
        local ColorIndex = ExtraParam:GetValueAsInt({SelectedKeyName = "ImageIndex"})
        local Color = self.ImageIndexs[ColorIndex]
        self.Image_0:SetColorAndOpacity(Color)
    end
end
```

---

## UI自适应屏幕

> 文档路径: 进阶内容 > UI系统 > UI自适应屏幕

> 文档ID: 20269 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20269)

> 更新: 2025-12-30 18:05:48

# UI自适应屏幕

制作UI界面时，如果想要保证UI在不同分辨率的设备上以固定的比例正常显示，需要提前对UI进行自适应适配，否则可能出现缩放比例不正确或者非预期的控件间隔现象。

![UI自适应效果图.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/k1xhMUI%E8%87%AA%E9%80%82%E5%BA%94%E6%95%88%E6%9E%9C%E5%9B%BE.gif)

<br>

## 设置层次结构

创建并进入【控件蓝图】界面（具体操作可参考 [UI系统快速入门](https://developer.gp.qq.com/wikieditor/#/catalog/347)），将屏幕分辨率设定为1920*1080（16：9）或点击 ``设计师 -> 屏幕尺寸`` 设定为“Apple iPhone 6+(Landscape)”。

![image.5.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6JNVWimage.5.png)

右键 ``画布面板 -> 包裹 -> 尺寸框`` 在承载UI界面的“画布面板”外包裹一层“尺寸框”。

![image.21.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UMf5Kimage.21.png)

右键 ``尺寸框 -> 包裹 -> 缩放框`` 在“尺寸框”外包裹一层“缩放框”。

![image.22.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xyCp7image.22.png)

右键 ``缩放框 -> 包裹 -> 画布面板`` 在“缩放框”外包裹一层“画布面板”。

![image.23.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LZz6Pimage.23.png)

最终层次结构如图所示。

![image.18.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/N5boyimage.18.png)

<br>

## 相关参数设置

在 ``层次结构`` 中点击缩放框，在【详细信息】中将 ``锚点`` 更改为“四向拉伸”，并将“偏移左侧”、“偏移顶部”、“偏移右侧”和“偏移底部”数值均设置为0。

![image.24.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LuMPqimage.24.png)

点击尺寸框，在【详细信息】中对尺寸框的尺寸进行设置，``宽度重载`` 设定为1920，``高度重载`` 设定为1080。

![image.33.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Iepmhimage.33.png)

点击画布面板，在【详细信息】中将 ``水平对齐`` 设定为“水平对齐填充”，``垂直对齐`` 为“垂直居中填充”。

![image.27.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lIILuimage.27.png)

---

### 居中型控件

若属于道具弹窗这类无需贴边的UI，调整尺寸框的 ``水平对齐`` 为水平对齐居中，``垂直对齐`` 为垂直居中对齐。

![image.31.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vY1VPimage.31.png)
![image.29.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2uIxRimage.29.png)

---

### 贴边型控件

若按钮有贴边需求，则调整尺寸框的 ``水平对齐`` 为水平右对齐，``垂直对齐`` 为垂直居中对齐。

![ScreenShot_2025-12-22_155524_627.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/S8tGpScreenShot_2025-12-22_155524_627.png)
![image.28.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8znyIimage.28.png)

<br>

## 实现UI界面

完成以上层级结构设置后，开发者根据自身需要添加UI控件元素，该控件蓝图即带有自适应缩放效果。

![image.20.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ozmovimage.20.png)

---

## UMG Lua的结构

> 文档路径: 进阶内容 > UI系统 > UMG Lua的结构

> 文档ID: 199 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/199)

> 更新: 2025-06-19 11:33:40

**涉及API/标识符:** `ReceiveTick`, `WidgetBlueprintLibrary.Create`

#  UMG Lua的结构

UMG Lua 和 普通的蓝图Lua稍有不同，下面我们介绍一下UMG Lua的文件结构：

---

<br>

## 典型文件示例：

![企业微信截图_16868319977162.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868319977162.png)
<br>

## 自动注释：

- UMG Lua 会根据控件蓝图自动生成Class信息 和 变量信息
- Class信息在首行，会以格式 类型信息：“父类类型信息” 生成：
- 变量信息在后面，会以格式： “变量名字 变量类型” 生成，只有勾选了Is Variable 属性的控件才会生成蓝图变量：
![企业微信截图_16868320062056.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868320062056.png)
  <br>

## 常用事件：

和 普通的 Lua不同，UMG Lua主要有两个事件：

```
function SubUI:Construct()
end
-- 主要在创建控件蓝图的时候调用，比如在调用 `WidgetBlueprintLibrary.Create` 函数的时候会调用Construct事件。可以在该事件内初始化蓝图。


function SubUI:Tick(MyGeometry, InDeltaTime)
end
-- 会在每一帧调用该事件，相当于 普通蓝图Lua 中的 `ReceiveTick` 函数。
```

具体函数详情可以参考API文档。

---

## 创建3D UI

> 文档路径: 进阶内容 > UI系统 > 创建3D UI

> 文档ID: 201 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/201)

> 更新: 2025-06-19 11:33:40

#  创建3D UI

在游戏中，我们经常要显示怪物的血条，这时候3D UI就派上用场了，下面我们简单介绍一下3D UI的使用方法。

---

<br>

## 流程

![企业微信截图_16868321386789.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868321386789.png)

---

<br>

## 实战演练

1.制作你想要显示的3DUI，这里简单制作了一个想要显示的血条：

![企业微信截图_16868321537981.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868321537981.png)
2.在你想要显示的Actor上显增加widget组件，并引用你刚才制作的UI蓝图：

![企业微信截图_16868321624595.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868321624595.png)
3.在蓝图编辑视口中预览和调整UI的显示到合适位置：

![企业微信截图_1686832172729.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686832172729.png)
4.启动游戏，你会发现3D UI已经正常显示了：

![企业微信截图_16868321831865.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868321831865.png)

<br>

附件：



<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UI3D.zip">UI3D.zip</a>

---

## 和平主界面控件布局

> 文档路径: 进阶内容 > UI系统 > 和平主界面控件布局

> 文档ID: 20019 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20019)

> 新增: 2026-09-10 17:24:38 | 更新: 2026-09-11 14:41:28

**涉及API/标识符:** `AddToSlot`, `SetWidgetLayout`, `UGCGameSystem.GetLocalPlayerController`, `UGCGameSystem.GetUGCResourcesFullPath`, `UGCWidgetManagerSystem`, `UGCWidgetManagerSystem.SetWidgetLayout`, `WidgetLayout`

# 和平主界面控件布局

和平精英基于经典“大逃杀”与不断衍生的玩法模式，构建了一系列丰富的 [控件库](https://developer.gp.qq.com/wikieditor/#/catalog/250)，方便玩家根据操作习惯与喜好进行个性化设置；而绿洲启元因游戏特性与规则的多样化，开发者常常需要定制UI界面，以适配玩法的操作交互，为了方便开发者对和平控件的控制与布局设置，使用WidgetLayout中间件的方案来提供支持。

<br>

## WidgetLayout概述

和平控件的复杂性体现在因角色状态与动态加载的时机不同，各类控件被分散在不同的widget类中，不同widget类通过子控件的形式相互嵌套引用，且widget类之间的层级存在强制的绑定关系，所以不支持直接编辑和平控件蓝图，而通过脚本的方式修改widget类的属性无法保障可用性，也无法解决控件层级问题。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JAwR4image.png)

为此，提供了新的 ``WidgetLayout`` 蓝图类承载和平主界面的常用控件，通过将该蓝图中的控件与对应和平Widget类中的控件进行映射关联，可以更方便地对和平控件进行设置和管理。

从结构上看，``WidgetLayout`` 是开发者交互与和平原生widget之间的中间层：
- 开发者交互：开发者可以对和平控件进行属性设置，也可以将自定义控件按指定的层级挂载到界面上
- 原生widget：通过透传开发者设置的属性来决定和平控件的状态，以及自定义控件与和平控件的层级关系

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iB2vXimage.png)

玩法逻辑中只需调用 [``UGCWidgetManagerSystem``](https://developer.gp.qq.com/api/#/searchContent/UGCWidgetManagerSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2FUI%20%E7%95%8C%E9%9D%A2%2FUGCWidgetManagerSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCWidgetManagerSystem) 的API加载WidgetLayout蓝图类，UI系统会重载或覆盖和平的原生界面，从而按WidgetLayout的设置正确显示各控件的状态。

<div style="text-align: center;">
	<img src="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KeczD%E6%9C%AA%E5%91%BD%E5%90%8D%E7%BB%98%E5%9B%BE.png"/>
</div>

<br>

由于蓝图属性设置是静态编译的形式，如果玩法中需要对控件进行运行时的动态控制，可以创建多组WidgetLayout蓝图类，在运行时通过API对WidgetLayout蓝图进行加载与卸载，实现动态切换的效果。

目前已支持的和平控件如下：
|控件名|控件说明|
|:-:|:-:|
|MainUI_BackPack_C_0|背包|
|MainUI_FireLeft_C_0|左侧开火按键|
|MainUI_FirstAid_C_0|消耗品道具栏|
|MainUI_Joystick_C_0|移动摇杆|
|MainUI_Weapon1_C_0|主武器1|
|MainUI_Weapon2_C_0|主武器2|
|MainUI_Projectile_C_0|投掷物道具栏|
|MainUI_LookAround_C_0|环视|
|MainUI_Rush_C_0|自动冲刺|
|MainUI_Map_C_0|小地图|
|MainUI_FireRight_C_0|右侧开火按键|
|MainUI_Jump_C_0|跳跃按键|
|MainUI_Crawl_C_0|匍匐状态|
|MainUI_Crouch_C_0|蹲姿状态|
|MainUI_FriendsList_C_0|组队面板|
|MainUI_FPS_TPS_Switch_C_0|人称切换|
|MainUI_Pistol_C_0|手枪栏|
|MainUI_Setting_Btn_C_0|设置|
|MainUI_Voice_Btn_C_0|声音|
|MainUI_Microphone_Btn_C_0|麦克风|
|MainUI_SurviveInfo_Btn_C_0|局内存活状态|
|MainUI_PlayerInfo_Btn_C_0|人物状态栏|
|MainUI_Navigator_C_0|指南针罗盘|

<br>

## 使用WidgetLayout

### 创建WidgetLayout

在项目的内容浏览器中，右键 ``用户界面 -> 控件布局``，点击创建并命名，双击打开蓝图可看到内置的和平主界面控件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jopSaimage.png)
![企业微信截图_17420144956100.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/S3q0Q%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17420144956100.png)

---

### 设置和平控件

> 目前仅支持对和平控件的显隐控制

选择目标和平控件，在该控件的【详细】面板中设置 ``可视性`` 属性，然后编译并保存，其中有效的属性选项为“可视”、“已折叠”和“隐藏”。

- 可视（Visible）：控件可见，用户可以与控件进行交互，例如点击按钮或输入文本
- 已折叠（Collapsed）：控件不可见，不占用布局中的空间，用户无法交互
- 隐藏（Hidden）：控件不可见，但仍然占用布局中的空间，并保留了原本的位置和大小，用户无法交互

以下图为例，针对左侧开火按键，将其可视性设置为“已折叠”，则游戏中将不会出现该按钮。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QYT4simage.png)

---

### 自定义控件布局

WidgetLayout支持添加自定义的控件并设置控件挂载的 [UISlot锚点](https://developer.gp.qq.com/wikieditor/?timeStamp=1725589224096#/catalog/20097?autoJump=UISlot%E9%94%9A%E7%82%B9)，方便开发者以可视化的方式控制自定义控件的层级。

从控件面板选择目标控件添加至UI结构树下，在控件蓝图根节点的【详细】面板中设置 ``Custom User Widget Layout`` 属性，该属性关联了自定义控件与锚点的映射，以键值对的形式配置，Key为自定义控件的名称，Value为指定的层级锚点，运行时将参照层级和控件的布局数据进行挂载。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kgqEGimage.png)

蓝图配置控件UISlot的方式目前仅支持全局层级锚点类型，如果需要对特定和平控件挂载自定义的控件，可以调用 [``AddToSlot``](https://developer.gp.qq.com/api/#/searchContent/UGCWidgetManagerSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2FUI%20%E7%95%8C%E9%9D%A2%2FUGCWidgetManagerSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCWidgetManagerSystem&autoJump=AddToSlot) 来实现同类效果。

---

### 加载与卸载WidgetLayout

创建与设置完WidgetLayout蓝图后，开发者可以在需要的场景和合适的时机下（确保和平主UI已完成初始化及加载，建议PlayerController/Pawn的Beginplay或之后），于客户端调用 [``SetWidgetLayout``](https://developer.gp.qq.com/api/#/searchContent/UGCWidgetManagerSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2FUI%20%E7%95%8C%E9%9D%A2%2FUGCWidgetManagerSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCWidgetManagerSystem&autoJump=SetWidgetLayout) 完成WidgetLayout的加载或卸载（传参为“Default”为卸载WidgetLayout效果）。

<br>

## 案例演示

为了更直观的展示功能，在此使用widget控件蓝图 [新建一个用户界面](https://developer.gp.qq.com/wikieditor/#/catalog/347)，并添加两个按钮，一个按钮用于加载 ``WidgetLayout`` ，一个按钮用于卸载 ```WidgetLayout```：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Hp8UBimage.png)

创建两个按钮后，分别为其绑定对应的加载与卸载事件：

``` lua
function MainUI:Construct()
	  self.Button_0.OnClicked:Add(self.Load, self)
    self.Button_1.OnClicked:Add(self.UnLoad, self)
end

function MainUI:Load()
    local PlayerController = UGCGameSystem.GetLocalPlayerController()
    PlayerController:LeftFireLoad()
end

function MainUI:UnLoad()
    local PlayerController = UGCGameSystem.GetLocalPlayerController()
    PlayerController:LeftFireUnLoad()
end

--[[ 加载 ]]--
function UGCPlayerController:LeftFireLoad()
    local path = UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/Test/All.All_C')
    UGCWidgetManagerSystem.SetWidgetLayout(path)
end

--[[ 卸载 ]]--
function UGCPlayerController:LeftFireUnLoad()
    UGCWidgetManagerSystem.SetWidgetLayout("Default")
end
```

启动调试游戏，默认是和平原生界面状态（显示左侧拳击键）
- 点击”Load“按钮，加载创建好的WidgetLayout，原生界面被覆写，左侧拳击键被隐藏
- 再次点击”UnLoad“按钮，卸载WidgetLayout，恢复为和平原生界面状态，左侧开火键重新出现

![QQ录屏20240902104004.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wJ7VYQQ%E5%BD%95%E5%B1%8F20240902104004.gif)

<br>

## 注意事项

- 同一组WidgetLayout蓝图只可加载一次，不应该重复加载
- 不推荐同时加载多组WidgetLayout蓝图
- 当进行WidgetLayout蓝图切换时，应当遵循先卸载->加载的执行顺序

---

## 和平控件锚点

> 文档路径: 进阶内容 > UI系统 > 和平控件锚点

> 文档ID: 20097 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20097)

> 更新: 2026-02-12 10:20:18

**涉及API/标识符:** `AddToSlot`, `UGCGameSystem.GetUGCResourcesFullPath`, `UGCWidgetManagerSystem`, `UGCWidgetManagerSystem.AddToSlot`, `UGCWidgetManagerSystem.CreateWidgetAsync`, `UI.UISlot`

# 和平控件锚点

和平精英UI交互界面上的控件元素由不同的控件蓝图组成，各控件蓝图之间存在复杂的层级关系，且根据玩家角色处于不同状态或者接触可交互物时UI元素也会发生相应变化，导致玩法中难以控制自定义控件的层级和布局。

UISlot以锚点的形式提供了通用的和平控件层级接入点，开发者使用锚点可以将自定义的控件添加到指定层级，结合控件布局实现更精准的挂载效果，解决被和平控件遮挡的问题。

<br>

## UISlot锚点

UISlot为不同和平控件蓝图的基础上预设的一组锚点，各锚点所处层级不同，添加至锚点的控件具备对应的层级效果，例如SlotA与和平控件蓝图2处于同一层级，挂载至此处的控件与控件D具备有效的ZOrder顺序关系，而因低于控件蓝图1会被控件A、B、C遮挡。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8oxg4image.png)

目前提供了 ``全局层级`` 和 ``特定控件`` 两类锚点。

### 全局层级锚点

全局层级锚点覆盖范围为整个和平主界面，锚点起始位置为屏幕左上角原点。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3UYQEimage.png)

|锚点名|锚点说明|图例|
|:-:|:-:|:-:|
|UI.UISlot.MainUISlot_High|和平主界面高层级锚点|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/wW1fTimage.png)|
|UI.UISlot.MainUISlot_Middle|和平主界面中层级锚点|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6F6F5image.png)|
|UI.UISlot.MainUISlot_Low|和平主界面低层级锚点|![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Jij03image.png)|

---

### 特定控件锚点

特定控件锚点的起始位置为特定控件下的指定位置，适合针对单控件进行追加挂载。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aUn6Wimage.png)

#### 队伍面板锚点

| 锚点名 | 锚点说明 | 图例 |
| ------ | ------ | ------ |
| UI.UISlot.MainUISlot_TeamItem | 锚点位于队伍信息列表的右侧，层级和该队伍信息UI平级，位置会跟随该面板适配和移动 | ![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ueeTWimage.png) |

#### 大地图工具栏锚点

| 锚点名 | 锚点说明 | 图例 |
| ------ | ------ | ------ |
| UI.UISlot.MapExtendTools_TaskList | 手册任务挂点，锚点起始位置位于手册任务右侧 |![image.15.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9hcusimage.15.png) |
| UI.UISlot.MapExtendTools_CampList | 营地工具挂点，锚点起始位置位于营地工具右侧 |![image.16.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rjlV9image.16.png) |
| UI.UISlot.MapExtendTools_Action | 局内任务挂点，锚点起始位置位于局内任务右侧 |![image.17.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VPFwEimage.17.png) |
| UI.UISlot.MapExtendTools_EscapeTask |地铁任务挂点，锚点起始位置位于地铁任务右侧| ![image.18.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7Plvpimage.18.png) |

#### 全屏背包锚点

| 锚点名 | 锚点说明 | 图例 |
| ------ | ------ | ------ |
| UI.UISlot.BackpackUISlot.Full.BGSlot | 背包背景底图 |![ScreenShot_2026-01-16_111808_562.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/roiRnScreenShot_2026-01-16_111808_562.png) |
| UI.UISlot.BackpackUISlot.Full.BagSlot | 背包主界面 |![ScreenShot_2026-01-16_111850_813.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/u1tM9ScreenShot_2026-01-16_111850_813.png) |
| UI.UISlot.BackpackUISlot.Full.OptionSlot | 侧边栏 | ![ScreenShot_2026-01-16_111926_465.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QqeZtScreenShot_2026-01-16_111926_465.png)|
| UI.UISlot.BackpackUISlot.Full.EquipSlot | 装备面板 |![ScreenShot_2026-01-16_112001_552.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/aQN5SScreenShot_2026-01-16_112001_552.png) |
| UI.UISlot.BackpackUISlot.Full.GridsSlot | 背包格子面板 | ![ScreenShot_2026-01-16_112021_184.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/goX47ScreenShot_2026-01-16_112021_184.png)|
| UI.UISlot.BackpackUISlot.Full.InventorySlot | 仓库面板 |![ScreenShot_2026-01-16_115226_993.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eK8dpScreenShot_2026-01-16_115226_993.png)|
| UI.UISlot.BackpackUISlot.Full.DeleteItemSlot | 丢弃物品面板 | ![ScreenShot_2026-01-16_115717_176.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/upBcoScreenShot_2026-01-16_115717_176.png)|
| UI.UISlot.BackpackUISlot.Full.ItemDetailSlot | 物品详情面板 |![ScreenShot_2026-01-16_120254_093.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Dr5nzScreenShot_2026-01-16_120254_093.png) |

#### 半屏背包锚点

| 锚点名 | 锚点说明 | 图例 |
| ------ | ------ | ------ |
| UI.UISlot.BackpackUISlot.Half.BGSlot | 背包背景底图 |![ScreenShot_2026-01-16_112947_218.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/E9aVYScreenShot_2026-01-16_112947_218.png) |
| UI.UISlot.BackpackUISlot.Half.BagSlot | 背包主界面 | ![ScreenShot_2026-01-16_113036_169.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HS0HOScreenShot_2026-01-16_113036_169.png)|
| UI.UISlot.BackpackUISlot.Half.OptionSlot | 侧边栏 |![ScreenShot_2026-01-16_113315_196.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hhcwIScreenShot_2026-01-16_113315_196.png) |
| UI.UISlot.BackpackUISlot.Half.EquipSlot | 装备面板 |![ScreenShot_2026-01-16_113330_863.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/J02C5ScreenShot_2026-01-16_113330_863.png) |
| UI.UISlot.BackpackUISlot.Half.GridsSlot | 背包格子面板 | ![ScreenShot_2026-01-16_114523_168.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GZ1yMScreenShot_2026-01-16_114523_168.png)|
| UI.UISlot.BackpackUISlot.Half.InventorySlot | 仓库面板 |![ScreenShot_2026-01-16_112923_314.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ymQl8ScreenShot_2026-01-16_112923_314.png) |
| UI.UISlot.BackpackUISlot.Half.DeleteItemSlot | 丢弃物品面板 |![ScreenShot_2026-01-16_142732_433.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5PQguScreenShot_2026-01-16_142732_433.png) |
| UI.UISlot.BackpackUISlot.Half.ItemDetailSlot | 物品详情面板 |![ScreenShot_2026-01-16_142742_002.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fthJfScreenShot_2026-01-16_142742_002.png) |

#### 技能UI锚点

| 锚点名 | 锚点说明 | 图例 |
| ------ | ------ | ------ |
| UI.UISlot.MainUISlot_Skill.Slot0 |预设技能UI槽位0，位于普攻键位的左侧|![ScreenShot_2026-01-14_152141_451.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/W7bUNScreenShot_2026-01-14_152141_451.png) |
| UI.UISlot.MainUISlot_Skill.Slot1 |预设技能UI槽位1，位于普攻键位的左上侧|![微信图片_2026-01-14_152219_436.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nHEKM%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_2026-01-14_152219_436.png) |
| UI.UISlot.MainUISlot_Skill.Slot2 |预设技能UI槽位2，位于普攻键位的右上侧|![ScreenShot_2026-01-14_152821_437.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kEaTlScreenShot_2026-01-14_152821_437.png) |

<br>

## 自定义锚点

除了使用预设的UISlot锚点以外，开发者也可以创建自定义的锚点，点击编辑器菜单栏 ``编辑 -> 工程设置 -> GameplayTags``，在 ``UI.UISlot`` 层级下新建锚点标签名。

![UI挂点 (2).gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/etCGGUI%E6%8C%82%E7%82%B9%20(2).gif)

在WidgetLayout蓝图中，通过【控制板】搜索“UGCCustom UISlot Mount Point Widget”，并将该控件模板添加到层级树中，设置此子控件的位置布局。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rRgB0image.png)

将子控件的 ``Slot Name`` 属性设置为新建好的锚点标签，这样就可以使用此自定义锚点去添加挂载其他控件了。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/feZUSimage.png)

<br>

## 通过锚点添加控件

脚本中在合适的时机下（确保和平主UI已加载，建议时机为PlayerController/Pawn的Beginplay之后）调用 [``AddToSlot``](https://developer.gp.qq.com/api/#/searchContent/UGCWidgetManagerSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2FUI%20%E7%95%8C%E9%9D%A2%2FUGCWidgetManagerSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCWidgetManagerSystem) 即可将指定的控件挂载到对应锚点上，需要注意的是，同一层级内的各控件之间也存在ZOrder顺序关系，因此为了实现更精准的层级设置，还需要结合控件自身的布局数据进行精细调整，API中的AnchorData参数为布局数据结构体。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1drvximage.png)

代码示例：

``` lua
local WidgetPath = UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/MainUI.MainUI_C')
local UISlotName = 'UI.UISlot.MainUISlot_Middle'
local ZOrder = 0;

UGCWidgetManagerSystem.CreateWidgetAsync(WidgetPath, function(WidgetInstance)
		-- 构造控件的布局数据
		local AnchorData = CreateStruct("AnchorData")
		local OffsetsData = CreateStruct("Margin")
		OffsetsData.Left = 50
		OffsetsData.Top = 100
		OffsetsData.Right = 50
		OffsetsData.Bottom = 0
		local Anchors = CreateStruct("Anchors")
		Anchors.Minimum = Vector2D.New(0, 0)
		Anchors.Maximum = Vector2D.New(0, 0)
		AnchorData.Offsets = OffsetsData
		AnchorData.Anchors = Anchors
		AnchorData.Alignment = Vector2D.New(0, 0)

    UGCWidgetManagerSystem.AddToSlot(WidgetInstance, UISlotName, ZOrder, AnchorData)
end)
```

---

## 基础UI元件

> 文档路径: 进阶内容 > UI系统 > 基础UI元件

> 文档ID: 20149 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20149)

> 新增: 2026-05-19 20:13:51 | 更新: 2026-05-20 10:35:48

**涉及API/标识符:** `UGCGameSystem.GetUGCResourcesFullPath`, `UGCWidgetManagerSystem.LoadMainUIWidgetLayoutByPath`, `widgetLayout`

# 基础UI元件

UI元件是基于基础控件封装的一组实现特定显示效果的UI元素组件，UI元件具备易用性、可交互及复用性等特点，开发者可以通过配置实现对UI元件的显示及样式调整，目前提供了四种UI元件：主角血条、怪物血条、新手指引和队伍面板。

<br>

## 主角血条

主角血条元件支持配置血条的样式，包括血量值处于不同百分比的显示颜色、预扣除的样式等，也支持扩展额外的属性条。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/TKbN4image.png)

### 创建与配置血条

**1.创建主角血条组件**

右键新建蓝图
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EuVrmimage.png)

继承UGC_Player_HealthBar_UIBP，选择玩家血条组件进行创建

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uCDcsimage.png)

**2.配置主角血条组件**

在左侧Hierarchy栏中选择主角血条组件，即可在右侧的Details栏对其进行配置
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zJI1Gimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/6Y8XJimage.png)

**参数说明：**
|属性|属性说明|
|-|-|
|**Health Fill Image**|血量值百分比与颜色的映射，表示当血量值小于或等于这个百分比时血条所显示的颜色。<br>如：![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mZSI2image.png)表示血量低于或等于40%时血条颜色为紫色<br>展开一组映射后，可以进行更细致的配置，支持配置多组映射。<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pHAWaimage.png)|
|**Health Pre Deduct Fill Image**|血条预扣除颜色，表示当血量减少时血条变化量的颜色。<br>如：![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XXh38image.png)其中白色为血条预扣除的颜色|
| **Game Attribute Fill Image Map**|属性值配置，打开后如图所示<br>![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Myw7mimage.png)<br> **CurrentValue**：属性值，该属性条所配置属性的当前值<br>**TotalValue**：最大属性值，该属性条所配置属性的最大值<br>**FillImage**：属性值百分比/颜色映射，和血条的百分比/颜色映射类似，表示当这个属性值低于或等于这个百分比时属性条所显示的颜色<br>**AttrPreDeductFillImage**：属性值预扣除颜色，和血条与扣除颜色类似，表示该属性值减少时属性条变化量的颜色<br>**Scale**：属性条缩放比，相对于血条的宽高比，取值0~1<br>**HorizontalAlignment**：属性条相对于血条对齐方式<br>**Padding_Top**：属性条间距，此属性条相对于上一条属性条的距离 <br>**ShowText**：是否显示属性数值，此项仅对怪物血条有效<br>**注意：一条属性条的属性值与其最大值需要一一对应，如CurrentValue填的是信号值，TotalValue就应该是最大信号值**|

### 添加血条元件

#### 基于widgetLayout添加

**将创建好的主角血条组件加入主UI**

打开UGCPlayerController
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/G4gpiimage.png)

搜索Main UIClass，可以看到主UI配置
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZqzFXimage.png)

打开主UI
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DfHr5image.png)

在左侧搜索栏处输入创建的玩家血条组件的名字（由用户命名的名字）
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sVWCCimage.png)

将其拖入主UI中
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qpXq3image.png)

**调整主角血条组件位置，隐藏原血条组件**

选择主角血条组件，在Detials中搜索Layout即可调整其位置，也可以在画布中拖动调整

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Q5axCimage.png)

调整好后，在左侧Hierarchy栏中选择MainUI_PlayerInfo_C_0
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XEqGkimage.png)

在其Detials中搜索Behavior，在其可视性下拉框选择“已折叠”或者“隐藏”，即可把MainWidget原来的血条隐藏掉，只显示所配置的主角血条组件
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Mb9c6image.png)

**5.编译和保存**
配置完成后，编译并保存方可生效
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uQvglimage.png)

经过配置后可以达到如图效果，新加的属性条会出现在血条的上方
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Bwx4jimage.png)

#### 脚本动态添加
主角血条也可以动态添加，步骤如下：
1.创建一个```widgetLayout```
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SsUgUimage.png)
2.打开刚创建```widgetLayout```，在控制板处搜索创建好的血条蓝图，将其拖入画布
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EZPDpimage.png)
3.配置主角血条
调整好血条UI位置，配置完各项参数后需编译并保存，具体配置方法可参考[创建和配置主角血条](https://developer.gp.qq.com/wikieditor/#/catalog/20149?autoJump=%E5%88%9B%E5%BB%BA%E4%B8%8E%E9%85%8D%E7%BD%AE%E8%A1%80%E6%9D%A1)
4.动态加载```widgetLayout```
在有需要的时机可以动态加载出刚创建的```widgetLayout```，动态加载方法可参考[加载与卸载WidgetLayout](https://developer.gp.qq.com/wikieditor/#/catalog/20019?autoJump=%E5%8A%A0%E8%BD%BD%E4%B8%8E%E5%8D%B8%E8%BD%BDWidgetLayout)
以下为在UGCGameState中ReceiveBeginPlay时机调用主角血条UI的示例：
```
function UGCGameState:ReceiveBeginPlay()

    local path = UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/PlayerHealthBarUI.PlayerHealthBarUI_C')
    UGCWidgetManagerSystem.LoadMainUIWidgetLayoutByPath(path)

end
```

------------------------------------


## 新手引导

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Uud5pimage.png)
新手引导组件可配置大标题、小标题、内容和图片

### 前置依赖
新工程要使用新手引导组件，需要先找到以下路径：和平精英/资源/UI资源/UI模板/提示/新手教程，打开新手教程（需要先打开一遍，才可以搜索到）
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2qMxYimage.png)
### 添加新手引导元件
#### 基于WidgetLayout添加

这里展示的是在主UI加载时，显示新手引导组件的方法
**1.将新手引导组件加入主UI**

主UI可在UGCPlayerController中找到
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/dFkCNimage.png)

打开后细节中搜索Main UIClass，可以看到主UI配置
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eai00image.png)

打开主UI
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/C80qNimage.png)

左上角搜索UGC Modules Teaching Tips UIBP，将其拖入主UI
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XGMcrimage.png)

**2.配置其在主UI的位置**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7vMcRimage.png)

**3.主要内容配置**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sutn1image.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DvldQimage.png)
**参数说明**：
1.**Big Title**：**大标题**
2.**Small Titles**：**小标题**
3.**Content Text**：**内容文本**
4.**Images**：**图片**
**注意：每个下标一样的数组的【小标题-内容文本-图片】为一组展示在同一页中，如图所示**
5.**翻页按钮**
6.**不再提示勾选按钮**
**【不再提示】功能以Big Title为准，如果创建了多个新手引导，注意不要让Big Title一样**
**这里展示的是三页的新手引导，如有需求可以自行增加**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ezqYximage.png)
**4.编译并保存**
配置完成后，编译并保存方可生效
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/MhAFpimage.png)

#### 脚本动态添加

新手引导组件也可以在合适的时机动态添加，步骤如下：
1.创建一个```widgetLayout```
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SsUgUimage.png)
2.打开刚创建```widgetLayout```，在控制板处搜索```UGC Modules Teaching Tips```，将其拖入画布
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gm9MMimage.png)
3.调整新手引导组件大小和位置，配置好各项参数后编译并保存
4.动态加载```widgetLayout```
在有需要的时机可以动态加载出刚创建的```widgetLayout```，动态加载方法可参考[加载与卸载WidgetLayout](https://developer.gp.qq.com/wikieditor/#/catalog/20019?autoJump=%E5%8A%A0%E8%BD%BD%E4%B8%8E%E5%8D%B8%E8%BD%BDWidgetLayout)
以下为在UGCGameState中ReceiveBeginPlay时机调用新手引导UI的示例：
```
function UGCGameState:ReceiveBeginPlay()

    local path = UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/TeachUI.TeachUI_C')
    UGCWidgetManagerSystem.LoadMainUIWidgetLayoutByPath(path)

end
```



------------------------------------

## 队伍信息面板
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2lfRgimage.png)
队伍信息组件可以配置血量值或属性值百分比与颜色的映射、多条属性值、队伍排序方式

### 使用前置
**1.打开UGCPlayerController，确认主UI**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bhReFimage.png)
在细节搜索Main UIClass，可以看到主UI，推荐将队伍信息组件放入主UI使用
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IaDVDimage.png)

**2.打开UGCGameMode**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/VD3Taimage.png)
细节中搜索UIModule Prefab，在UI模块预制中填入UGCMainTeamModule
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cGqLLimage.png)
**注意：在世界设置中，选择的Game Mode要和打开的一致**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vlSeNimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xocsBimage.png)

**3.打开PlayerState需设置属性条要用到的属性**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RSHeKimage.png)
在细节中搜索Synced Attribute Pairs，添加需要用到的属性，需填写其当前值和最大值
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GiBDnimage.png)

### 使用方法
**1.打开主UI**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pdFf2image.png)
在左上角搜索UGC Ingame Team Panel New BP将其拖入主UI中
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/jN7r3image.png)

**2.配置组件**
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/marROimage.png)
	**参数说明：**
- **Max Display Count**：最大显示个数，即最大显示多少个队友的信息，小于0表示不限制，当前只能支持最多8人
- **Health Fill Image** ：血量值百分比与颜色的映射，配置方法参考[主角血条](https://developer.gp.qq.com/wikieditor/#/catalog/20149?autoJump=%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)组件
- **Game Attribute Fill Image Map**：属性值百分比/颜色映射，配置方法参考[主角血条](https://developer.gp.qq.com/wikieditor/#/catalog/20149?autoJump=%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)组件
**注意：这里要让额外的属性条显示生效，必须在PlayerState中设置好，具体在使用前置可见；额外属性条的多少开发者可自行决定，过多的属性条会占用更多的屏幕空间**
- **Sort Order**：队伍排序方式，这里提供了两种排序方式：
	DefaultSorting：和平默认规则
	PlayerNameSorting：玩家ID字符串排序，值越小越靠前
**队伍信息组件暂不支持调整位置和大小功能，在其Layout中如何更改都不会奏效**

**3.编译并保存**
配置完成后，编译并保存方可生效
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vLxAMimage.png)

---

## 头像框组件

> 文档路径: 进阶内容 > UI系统 > 头像框组件

> 文档ID: 20365 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20365)

> 新增: 2026-05-19 20:14:11 | 更新: 2026-05-20 10:17:21

# 头像框组件
## 头像框组件概述
头像框是身份与个性的视觉延伸，既能装饰头像、提升辨识度，也可彰显荣誉、传递专属氛围。头像框组件则可以满足此类需求。

## 头像框组件快速使用

### 1. 创建头像框组件
可在 UI 编辑器里的模板里找到头像框组件，选择其为模板并创建。
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RbbvDimage.png)

### 2. 配置头像内容和头像框
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HfBJ5image.png)
|属性名|说明|
|-|-|
|Head Image Path|头像路径，选择使用图片资产路径作为头像内容后生效
|Head Image Type|头像图片类型，有Asset和Playerkey两个选项，Asset为选用资产图片作为头像内容，Playerkey为以玩家QQ或微信头像作为头像内容
|Profile Frame Asset Path|头像框路径，可以填入图像、材质资产路径作为头像框
### 3. 将头像框配置到需要显示的位置
示例：将头像框放到战斗主界面中，打开 MainWidget，在控制板中搜索到创建好的头像框，添加到战斗主界面中。
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BWFxOimage.png)
最终效果如下
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PLkxOimage.png)
 > 当头像框组件有参数修改时，放置对应头像框组件的界面也需保存一下，否则修改可能不生效
## 头像框层级说明
头像框组件由头像内容和头像框组成，头像内容可以是图片资产也可以是玩家QQ或微信的头像
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kec5zimage.png)
|层名|说明|
|-|-|
|SizeBox_0|整体头像框尺寸，可在此调整体头像框的大小|
|HeadImage|头像内容层级，以图片资产作为头像内容时，在此处调整头像内容的大小缩放偏移等参数|
|Avatar|头像内容层级，以玩家QQ或微信头像作为头像内容时，在此处可调整头像内容的大小缩放偏移等参数|
|ProfileFrameImage|头像框层级，在此处可调整头像框的大小缩放偏移等参数|

---

## 富文本框

> 文档路径: 进阶内容 > UI系统 > 富文本框

> 文档ID: 202 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/202)

> 更新: 2025-06-19 11:33:40

# 富文本框

富文本框有三种功能：字体样式支持、图片支持和链接支持。

<br>

## 字体样式

支持在富文本框中使用font标签，改变字体样式。

### 内容文本参考

```
和平精英<font src="/Engine/EngineFonts/Roboto.Roboto" size="16" color="FFEA42FF" use_shadow="1" shadow_color="000000FF" shadow_offset="3;3">绿洲启元</>
```

### 字段含义

| 字段 | 是否必填 | 字段含义 |  默认值 | 参考值 |
| ------ | ------ | ------ | ------ | ------ |
| src | 否 | 字体族系路径 | 控件字体族系 | "/Engine/EngineFonts/Roboto.Roboto" |
| size | 否 | 字体尺寸 | 控件字体尺寸 | 16 |
| color | 否 | 字体颜色 | 控件字体颜色 | `"FFEA42FF"` |
| use_shadow | 否 | 是否开启阴影 | 不开启 | 1，表示开启阴影 |
| shadow_color | 否 | 字体阴影颜色 | 黑色 | `"FFEA42FF"` |
| shadow_offset | 否 | 字体阴影偏移 | 0;0 | 1.5;2.5 表示 X偏移1.5 Y偏移2.5 |

### 字体颜色格式

颜色支持 SRGB Hex写法， RGB, RRGGBB, RRGGBBAA, #RGB, #RRGGBB, #RRGGBBAA, 例如：2B272F 或 C85D1CFF

### 使用效果

![企业微信截图_16868322378799.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868322378799.png)

<br>

## 图片支持

支持在富文本框中嵌入图片,需要勾选SupportImage属性。

### 内容文本参考

```
和平精英<pic src="/Game/UGC/Textures/Icon/OasisEra/OasisEra_2.OasisEra_2" size="100;50" baseline="-10"/>
```

### 字段含义

| 字段 | 是否必填 | 字段含义 |  默认值 | 参考值 |
| ------ | ------ | ------ | ------ | ------ |
| src | 是 | 图片路径，支持和平资源和项目工程资源路径 | 无 | 和平资源："/Game/UGC/Textures/Icon/OasisEra/OasisEra_2.OasisEra_2"  项目资源："Asset/Blueprint/TestImg1.TestImg1" |
| size | 否 | 图片大小 | 32;32 | 100;50 表示 宽100 高50 |
| baseline | 否 | 文字基线高度 | 0 |  |

#### 使用效果

![企业微信截图_1686832252312.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686832252312.png)

<br>

## 链接支持

支持在富文本框中嵌入链接样式的图片。

### 内容文本参考

```
请点击<a2 src="/Engine/EngineFonts/Roboto.Roboto" size="30" color="A9FF00FF" under_line="1">这里</>
```

### 字段含义

| 字段 | 是否必填 | 字段含义 |  默认值 | 参考值 |
| ------ | ------ | ------ | ------ | ------ |
| src | 否 | 字体族系路径 | 控件字体族系 | "/Engine/EngineFonts/Roboto.Roboto" |
| size | 否 | 字体尺寸 | 控件字体尺寸 | 16 |
| color | 否 | 字体颜色 | 控件字体颜色 | `"FFEA42FF"` |
| under_line | 否 | 是否开启下划线 | 不开启,0 | 1,表示开启下划线 |

### 使用效果

![企业微信截图_16868322697756.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868322697756.png)

<br>

## 链接点击事件

新增链接点击事件: OnHyperlinkClicked，相关链接设置信息会放在事件参数中。需要勾选SupportHyLink属性

### 使用范例参考

```
function MainUI:Construct()
    self.UTRichTextBlock_0.OnHyperlinkClicked:Add(self.OnHyperlinkClicked, self)
end

function MainUI:OnHyperlinkClicked(meta)
	log_tree("OnHyperlinkClicked",meta);
end
```

---

## 异形屏适配

> 文档路径: 进阶内容 > UI系统 > 异形屏适配

> 文档ID: 357 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/357)

> 更新: 2025-06-19 11:33:40

#  异形屏适配

在绿洲启元编辑器完成UI制作后，如果想要适配异形屏，可以参考如下步骤调整UI。

<br>

## 异形屏介绍

什么是异形屏？如下图所示：

![7fe9-fzihnep5169152.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xlWze7fe9-fzihnep5169152.png)

异形屏的结构：

![c97c-hsccyrs7858029.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WQBlXc97c-hsccyrs7858029.png)

<br>

## 适配流程

调整UI层次结构，参考如下结构：

![企业微信截图_16868321042655.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868321042655.png)

 在适当时机调用函数适配UI，例如在Construct事件中调用（已设置AdaptionPanel 的 Is Variable属性）：

```
function MainUI:Construct()
   ...
   UICommonFunctionLibrary.SetAdaptation(self.AdaptionPanel, self);
end
```



<br>

## 注意事项

所有主UI都需要适配一遍。

---

## 强引导组件

> 文档路径: 进阶内容 > UI系统 > 强引导组件

> 文档ID: 20383 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20383)

> 新增: 2026-06-03 14:31:15

**涉及API/标识符:** `Border`, `Border_0`, `ButtonBP`, `CanvasPanel_0`, `GameState`, `Image_2`, `ItemBP`, `SelfHitTestInvisible`, `SizeBox_0`, `UE.LoadClass`, `UGCAPI.UGCGameSystem`, `UGCEventSystem.SetTimerOnce`, `UGCGameSystem.GetGameState`, `UGCGameSystem.GetLocalPlayerController`, `UGCGameSystem.UGCRequire`, `UGCMapInfoLib.GetRootLongPackagePath`, `UTRichTextBlock_Tips14_1`, `Visible`

# 强引导组件
在玩法引导中，有时会用到强制点击某个按钮的引导，编辑器提供了一个此类功能的组件，此组件的实现原理是将除此按钮外的其他区域用不可点击的遮罩进行阻挡，进而实现强制点击此按钮。

## 使用示例
1.打开UI编辑器，在元件-系统中找到强引导组件模板进行创建
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Vgorbimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/WGkL7image.png)
2.根据需要强引导的区域，调整好```CanvasPanel_0```的位置和大小，将其```SizeBox_0```框到需要引导的区域处，之后的调用都会固定将框到区域设置成可点击的高亮区
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pPU2Dimage.png)
3.游戏初始化时创建，需要时自行调用显示。为了保证可以顺利获取到镂空框的位置和大小，这里推荐游戏初始化时，将强引导UI创建出来（创建出来的UI是隐藏的），在需要调用时再显示即可。为方便演示，此处代码示例为在游戏初始化时创建并延迟0.5s后显示，在```GameState```的Lua中添加如下代码，其中```ItemBP```获取的路径请自行改为自己工程内的强引导UI路径，```ButtonBP```为之后会用到关闭强引导UI的按钮。
```
---@class UGCGameState_C:BP_UGCGameState_C
--Edit Below--
UGCGameSystem.UGCRequire('Script.Common.ue_enum_custom')
local UGCGameState = {};


--- 游戏开始时调用（仅客户端执行）
function UGCGameState:ReceiveBeginPlay()

    -- 服务端直接返回，不处理UI逻辑
    if self:HasAuthority() then
        return
    end

    -- 初始化提示强引导UI和按钮UI
    self:InitTipsUI()
    self:InitButtonUI()

    -- 延迟0.5秒后调用引导界面的OpenGuide方法，将原本隐藏的强引导UI显示出来
    UGCEventSystem.SetTimerOnce(self, function()
        if self.ItemBP then
            self.ItemBP:OpenGuide()
        end
    end, 0.5)

end

--- 初始化强引导UI
function UGCGameState:InitTipsUI()
    print ('UGCGameState:InitTipsUI')

    -- 仅客户端执行
    if self:HasAuthority() then
        return
    end

    -- 防止重复初始化
    if self.ItemBP then
        return
    end

    -- 加载强引导UI蓝图
    local ItemBP = UE.LoadClass(UGCMapInfoLib.GetRootLongPackagePath().. '/Asset/Blueprint/Prefabs/UI/test002.test002_C')

    -- 获取本地玩家控制器
    local PC = UGCGameSystem.GetLocalPlayerController()

    -- 创建Widget实例并保存到self.ItemBP
    self.ItemBP = UserWidget.NewWidgetObjectBP(PC, ItemBP)

    -- 添加到视口顶层显示（层级999999）以防止被遮挡
    if self.ItemBP then
        self.ItemBP:AddToViewport(999999)

    end

end


--- 初始化按钮UI (Button.Button_C)
function UGCGameState:InitButtonUI()
    print('UGCGameState:InitButtonUI')

    -- 仅客户端执行
    if self:HasAuthority() then
        return
    end

    -- 防止重复初始化
    if self.ButtonBP then
        return
    end

    -- 加载Button蓝图类
    local ButtonBP = UE.LoadClass(UGCMapInfoLib.GetRootLongPackagePath().. '/Asset/Blueprint/Prefabs/UI/Button.Button_C')

    -- 获取本地玩家控制器
    local PC = UGCGameSystem.GetLocalPlayerController()

    -- 创建Widget实例并保存到self.ButtonBP
    self.ButtonBP = UserWidget.NewWidgetObjectBP(PC, ButtonBP)

    -- 添加到视口显示（层级999997）
    if self.ButtonBP then
        self.ButtonBP:AddToViewport(999997)
    end

end

-- function UGCGameState:ReceiveTick(DeltaTime)

-- end
-- function UGCGameState:ReceiveEndPlay()

-- end
return UGCGameState;


```
4.为了隐藏掉这个强引导UI，这里需要再创建一个按钮用其点击事件来隐藏掉这个强引导UI。需要注意，这个按钮的锚点位置需要和前面设置的强引导区域一致，否则无法点击。
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8gwEdimage.png)
打开按钮的Lua，在其点击事件中隐藏引导UI
```
---@class Button_C:UUserWidget
---@field Button_0 UButton
--Edit Below--
require("ugc.UGCAPI.UGCGameSystem")

local Button = { bInitDoOnce = false }

function Button:Construct()
    self:LuaInit()
end

function Button:LuaInit()
    if self.bInitDoOnce then
        return
    end
    self.bInitDoOnce = true
    self.Button_0.OnClicked:Add(self.Button_0_OnClicked, self)
end

function Button:Button_0_OnClicked()
    print("Button_0_OnClicked")
    local GameState = UGCGameSystem.GetGameState()

    if GameState and GameState.ItemBP then
        GameState.ItemBP:HideGuide()
    end

    return nil
end

return Button
```
5.实机效果
![2026-05-2618-16-07-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/59eCf2026-05-2618-16-07-ezgif.com-video-to-gif-converter.gif)

## 关键控件介绍
- ```SizeBox_0```需要高亮（镂空）的目标区域，其位置大小决定镂空框的位置大小
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oB4iaimage.png)
- ```Image_2```中可以指定镂空边框材质
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AKnlrimage.png)
- ```UTRichTextBlock_Tips14_1```富文本控件中可以更改引导所显示的文字
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/nZeVYimage.png)
- ```Border_0```全屏遮罩Border，使用动态材质判断设置遮挡实现镂空效果
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gzxq0image.png)

## 关键函数及其功能
|函数|功能|
|-|-|
|```Construct()```|启动 0.5 秒定时器调用```RenderBox()```，保证用于镂空计算的UI缓存可获取，若需要动态创建强引导UI，则需要给一定的时间后再显示，否则镂空位置会出错|
|```RenderBox()```|计算 ```SizeBox_0```相对```Border_0```的位置比例，设置材质参数实现镂空，完成后移除定时器并默认隐藏|
|```OnPaint(Context)```|每帧检测鼠标位置，当鼠标在镂空区域内时将```Border```设为```SelfHitTestInvisible```（可穿透点击）；当鼠标在区域外时，将```Border```设为```Visible```（阻挡点击）|
|```OpenGuide()```/```HideGuide()```|打开/隐藏强引导控件|

**注意：**
- ```RenderBox()```在初始化时仅执行一次适配屏幕计算
- 设置UI默认可见属性为隐藏请在```RenderBox()```末尾调用```HideGuide()```隐藏，请勿直接通过蓝图设置以防缓存初始化失败
- 交互完成引导按钮请确保与镂空框位置重合，避免出现无法通过交互关闭强制引导的情况
- 请确保强制点击引导UI覆盖全屏

---

## 快速入门

> 文档路径: 进阶内容 > UI系统 > 快速入门

> 文档ID: 347 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/347)

> 更新: 2025-06-19 11:33:40

**涉及API/标识符:** `Asset`, `Blueprint`, `GameplayStatics.GetPlayerController`, `UE.LoadClass`, `UGCMapInfoLib.GetRootLongPackagePath`, `UI`

#  快速入门

在绿洲启元编辑器中可以使用UI编辑器自定义你的游戏UI，下面会逐步介绍如何制作游戏项目的UI。

<br>

## 流程

![企业微信截图_16868317197353.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868317197353.png)

<br>

## 实战演练

### 1. 创建蓝图，并调整UI样式

创建任意工程后，在`Asset`-`Blueprint`-`UI`找到【用户界面】，创建【控件蓝图】。

![企业微信截图_16868317289584.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868317289584.png)

双击【控件蓝图】  打开蓝图编辑器，并调整UI样式，这里我们新增了3个button控件 和 4个Text 控件。

![企业微信截图_16868317971945.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868317971945.png)

### 2. 绑定UI事件

点击，`菜单栏`-`UMG Lua`，打开蓝图绑定的Lua脚本。

![企业微信截图_16868318082268.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868318082268.png)

修改button控件和显示Text控件的 is Variable 属性为 True，使得Lua脚本中可以调用对应控件的函数。

![企业微信截图_16868318172097.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868318172097.png)

在Lua脚本中，MainUI的构造函数`Construct()`中初始化button控件的事件绑定，参考代码如下：

脚本的最上方是自动生成的，可以在Lua中调用的控件蓝图变量，下述代码在 button被点击的时候，修改了text的文字显示。

```
---@class MainUI_C:UserWidget
---@field Button_69 UButton
---@field Button_129 UButton
---@field Button_200 UButton
---@field TextBlock_117 UTextBlock
--Edit Below--
local MainUI = {};

function MainUI:Construct()
    self:InitBindEvent()
end

function MainUI:InitBindEvent()
    print("MainUI:InitBindEvent");

    self.Button_69.OnClicked:Add(self.Button_69_OnClicked, self);
    self.Button_129.OnClicked:Add(self.Button_129_OnClicked, self);
    self.Button_200.OnClicked:Add(self.Button_200_OnClicked, self);
end

function MainUI:Button_69_OnClicked()
    print("MainUI:Button_69_OnClicked");

    self.TextBlock_117:SetText("开始游戏");
end

function MainUI:Button_129_OnClicked()
    print("MainUI:Button_129_OnClicked");

    self.TextBlock_117:SetText("暂停游戏");
end

function MainUI:Button_200_OnClicked()
    print("MainUI:Button_200_OnClicked");

    self.TextBlock_117:SetText("结束游戏");
end

return MainUI;
```

### 3. 加载UI

加载UI，主要依靠下述API。

```
UUserWidget* UserWidget.NewWidgetObjectBP(Outer:UObject,UserWidgetClass:UClass)
```

推荐在 GameState 的`ReceiveBeginPlay()`中初始化UI，参考代码如下。

```
---@class UGCGameState_C:BP_UGCGameState_C
--Edit Below--
local UGCGameState = {};

function UGCGameState:ReceiveBeginPlay()
    self.SuperClass.ReceiveBeginPlay(self);

    if self:HasAuthority() == true then
        -- 只有客户端加载UI
    else
        local MainUI = UE.LoadClass( UGCMapInfoLib.GetRootLongPackagePath().. "Asset/Blueprint/UI/MainUI.MainUI_C");
        print("Load MainUI Class");
        -- 加载 MainUI 蓝图类

        local PlayerController = GameplayStatics.GetPlayerController(self, 0);
        print("Get Player Controller");
        -- 获得当前PlayerController

        local MainUI_BP = UserWidget.NewWidgetObjectBP(PlayerController,MainUI);
        print("Load MainUI_BP");
        -- 加载 MainUI

        MainUI_BP:AddToViewport();
        print("MainUI_BP AddToViewport");
        -- 将 MainUI 加入视口，显示UI
    end
end

return UGCGameState;
```

<br>

## 示例工程

示例工程见附件，点击附件启动游戏，我们发现在平时的UI上增加了3个按钮，点击按钮，对应的Text显示会发生变化。

![企业微信截图_16868318328224.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868318328224.png)

<br>

## 附件

<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UIQuickStart.zip">UIQuickStart.zip</a>

---

## 技能元件

> 文档路径: 进阶内容 > UI系统 > 技能元件

> 文档ID: 20325 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20325)

> 新增: 2026-05-06 10:30:55 | 更新: 2026-05-29 17:12:27

**涉及API/标识符:** `InitButton`, `OnSkillBound_BP`, `PersistClientStateComponent`, `PlayerPawn`, `UE.IsValid`, `UPESkillWidget`

# 技能元件

## 创建技能元件蓝图

点击绿洲启元编辑器菜单栏的【UI编辑器】按钮，打开UI编辑器的操作界面。

![ScreenShot_2026-02-28_155817_968.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mbSctScreenShot_2026-02-28_155817_968.png)

在【UI编辑器】中点击【元件】->【技能】->【技能按钮模板】创建技能元件蓝图

![ScreenShot_2026-02-28_155930_411.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/93yS7ScreenShot_2026-02-28_155930_411.png)

<br>

## 技能元件结构

![ScreenShot_2026-02-28_144602_706.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GDRprScreenShot_2026-02-28_144602_706.png)

| 组件名称| 组件功能 |
| :---: | :---:|
|Button_Skill|技能按钮，处理点击事件|
|Image_Icon|技能图标|
|Image_CDTime|CD蒙版组件|
|【Text_Time】"99"|CD文本组件|
|【Canvas Panel_FX】|UI动效组件|
|【Text_Name】"加速"|技能名称组件|
|CanvasPanel_Lock|技能锁定状态组件|
|CanvasPanel_Disable|技能禁用状态组件|
|CanvasPanel_Charging|技能充能模版组件|
 |CanvasPanel_Number|技能充能次数组件|

<br>

## 编辑技能元件

### 新增子控件

可通过新增UI组件实现模板里没有的相关功能。

![ScreenShot_2026-03-02_153503_476.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4mPAYScreenShot_2026-03-02_153503_476.png)

以新增图像为例，在`画布面板`下新增`图像组件`，将`图像`更改为所需图像，`可视性`更改为“非可命中测试”。

---

### 子控件显隐

为了保证模板能够正常运行，当需要对某个UI组件进行隐藏时，对该组件的可视性进行更改实现隐藏的效果，这里以技能名称文本“加速”为例。

![ScreenShot_2026-03-02_102342_017.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Qw35PScreenShot_2026-03-02_102342_017.png)

选中“加速”文本对应的组件后将`可见性`更改为“以折叠”。

---

### 自定义UI组件

**技能UI基类的绑定**

利用这种基类里已经预制好的绑定，可以将自己自定义的UI组件和技能Owner实例进行方便的关联，如自己实现了按钮、名称、图标组件，可调用InitButton 快速实现这些组件和技能Owner实例的关联（即读取技能上配置的图标、名称等信息）。
以“CD模块”为例。创建CD模块相关组件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yFenlimage.png)

将创建好的CD模块组件填入对应的基类进行绑定，即可实现组件和对应技能的关联。

```lua
function TestSkillUI:Construct()
	TestSkillUI.SuperClass.InitCDProgress(self, self.Text_Time, self.Image_CDTime, self.CanvasPanel_CDtime)
end
```

[技能UI基类](https://developer.gp.qq.com/api/#/searchContent/UPESkillWidget?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUPESkillWidget.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UPESkillWidget&autoJump=InitButton)

|绑定对象|函数|
| :---: | :---|
|技能按钮控件|InitButton(UImage* （图标控件）, UTextBlock* （名字控件）, UButton* （按钮控件））;|
|技能使用层数控件|InitLayer(UTextBlock* （技能层数）, UCanvasPanel* （技能层数的Panel控件，控制层数的显隐））|
|技能CD控件|InitCDProgress(UTextBlock* （技能CD时间）, UImage* （技能CD进度条）, UCanvasPanel* （整个CD的Panel控件，控制CD的显隐））|
|技能能量控件|InitEnergyProgress(UImage* (技能能量进度条), UCanvasPanel* (技能能量Panel控件，控制能量进度条的显隐))|
|显示TagDisable状态的控件|InitTagDisableState(UCanvasPanel* (技能TagDisable状态的Panel控件，控制TagDisable状态的显隐))|
|技能显示Enable状态的控件|InitEnableState(UCanvasPanel* （技能Enable状态的Panel控件，控制Enable状态的显隐））|

---

**技能UI基类的UI事件**

以`OnSkillBound_BP`为例，当控件绑定到新的技能时触发对应事件。

```lua
function TestSkillUI:OnSkillBound_BP(InOwnerSkill)
	TestSkillUI.SuperClass.OnSkillBound_BP(self, InOwnerSkill)

    if UE.IsValid(InOwnerSkill) then
        self.PreCDState = InOwnerSkill.SkillCD.MaxLayer ~= InOwnerSkill.SkillCD.CurLayer
        self.PreEnableState = InOwnerSkill:IsSkillEnable()
    end
end
```

[技能UI基类相关的UI事件](https://developer.gp.qq.com/api/#/searchContent/UPESkillWidget?classDetailShow=true&path=class%2Fdetail%2FOthers%2FUPESkillWidget.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UPESkillWidget&autoJump=InitButton)

|UI事件|触发时机|事件|
| :---: |:---| :---|
|控件绑定到新的技能|绑定时|OnSkillBound_BP(UPersistEffectSkill* (当前绑定的技能))|
|更新CD显示|帧触发|UpdateCD_BP(float （每帧的时间）)|
|判断技能是否处在CD状态|CD状态变化时|OnCDStateChange_BP(bool (技能是否处在CD状态))|
|控件绑定的技能的UI信息变化时触发|变化时|OnSkillUIInfoChange_BP()|
|控件绑定的技能Enable状态变化时触发|变化时|OnEnableChange_BP(bool (技能是否Enable))|
|绑定的技能被禁用Tag(PawnState.ActivatingSkill)时触发|无法激活时|OnTagDisableChange_BP(bool (技能是否被Tag禁用))|

<br>

## 技能与元件蓝图的绑定

参照[新建技能蓝图](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%96%B0%E5%BB%BA%E6%8A%80%E8%83%BD%E8%93%9D%E5%9B%BE)，进行技能的创建。
点击【技能编辑器】->`技能`->创建好的技能->`默认技能UI`，更改为创建好的“技能元件蓝图”。

![numbered-image-1772442661037.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fFWUdnumbered-image-1772442661037.png)

<br>

## 多个技能的添加

当需要给角色挂载三个以上技能时，可复用换弹，瞄准这类用不上的按钮的槽位，并通过平移满足布局的需要。以毒气手雷技能复用至下蹲槽位为例。
确保下蹲按钮为可见状态。

![ScreenShot_2026-04-13_110219_429.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/uVBOBScreenShot_2026-04-13_110219_429.png)


在【技能编辑器】中将毒气手雷技能挂载至下蹲的槽位。

![ScreenShot_2026-04-13_111720_095.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XKlmjScreenShot_2026-04-13_111720_095.png)

在【UI编辑器】选中与冲刺技能绑定的元件蓝图中的最上层的`画布面板`，对其进行平移处理。

![ScreenShot_2026-04-14_095200_746.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/CF5KwScreenShot_2026-04-14_095200_746.png)

若复用和平按钮槽不能满足需求，可参照[自定义控件布局](https://developer.gp.qq.com/wikieditor/#/catalog/20019?autoJump=%E8%87%AA%E5%AE%9A%E4%B9%89%E6%8E%A7%E4%BB%B6%E5%B8%83%E5%B1%80)和[贴边型控件](https://developer.gp.qq.com/wikieditor/#/catalog/20269?autoJump=%E8%B4%B4%E8%BE%B9%E5%9E%8B%E6%8E%A7%E4%BB%B6)创建自定义锚点并做好适配。
参照[添加技能](https://developer.gp.qq.com/wikieditor/#/catalog/20091?autoJump=%E6%B7%BB%E5%8A%A0%E6%8A%80%E8%83%BD)，在`PlayerPawn`蓝图中， 通过`PersistClientStateComponent `技能组件为角色蓝图默认挂载该技能组件。技能UI锚点位置可参照[和平控件锚点](https://developer.gp.qq.com/wikieditor/#/catalog/20097?autoJump=%E6%8A%80%E8%83%BDUI%E9%94%9A%E7%82%B9)。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ILloMimage.png)

 <br>

## 和平精英模拟器适配

如果你的玩法需要支持PC端,可以配置键盘操作的提示效果。
![image.22.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zgYK6image.22.png)
点击【UI编辑器】->【元件】->【技能按钮模板】进行模版的创建，在详细信息中进行相应配置。
![ScreenShot_2026-05-22_102159_710.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qiCkgScreenShot_2026-05-22_102159_710.png)
|技能按键提示配置|配置功能|
|-|-|
|挂接Panel名|指定提示角标挂接到哪个UI子控件上(使用子控件的蓝图变量名,非UMG显示名称)|
|Anchor|提示控件相对父控件的锚点位置|
|Margin|提示控件相对锚点的偏移量|
|Alignment|提示控件的轴点对齐方式|
|ZOrder|提示控件的显示优先级,用于控制与其他控件的叠放顺序|
|Size To Content|是否让提示控件自动铺满父控件|

---

## 背包Tips系统

> 文档路径: 进阶内容 > UI系统 > 背包Tips系统

> 文档ID: 20463 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20463)

> 新增: 2026-09-08 18:58:08

**涉及API/标识符:** `UGCBackpackSystemV2.GetBackpackTipsConfig`

# 背包Tips系统

可以基于该系统，配置与背包系统相关的弹框信息提示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/QuZkfimage.png)

<br>

## Tips表

点击【表格管理器】->【功能表格】->【Tips表】创建TIps表进行Tips的相关配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/evmMpimage.png)

参数说明：
+ TipsID：Tips的ID，在代码里用接口显示对应Tips时，依赖ID进行查询。
+ 优先级：当下一条Tips进行显示，而前一条Tips还未完全隐藏时，依赖该优先级确定是否顶替。若优先级更大，则会进行顶替。优先级最大支持到3。即该优先级配置只能配置为0，1，2，3。
+ 是否可以被同等级顶替：如果两条Tips优先级一样，勾选该选项时，可以被优先级一致的Tips顶替。
+ 持续时间：tips的持续时间，优先级低于Tips调用接口。
+ 默认文本：该Tips的默认文本，可以使用富文本。
+ TipsUI蓝图：显示Tips的UI蓝图。支持在工程内使用[TipsUI模板](https://developer.gp.qq.com/wikieditor/#/catalog/20463?autoJump=TipsUI%E6%A8%A1%E7%89%88)创建自定义的Tips覆盖默认Tips蓝图。

<br>

## TipsUI模版

点击【UI编辑器】->【元件】->【TipsUI模版】创建背包Tips系统蓝图。可基于该蓝图进行自定义扩展。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yajcTimage.png)

<br>

## 背包Tips系统的配置

点击【玩法通用设置】按钮，[启用背包系统](https://developer.gp.qq.com/wikieditor/#/catalog/20104?autoJump=%E5%90%AF%E7%94%A8%E8%83%8C%E5%8C%85%E7%B3%BB%E7%BB%9F)，添加“GP_BackpackV2”模块，创建并打开`背包组件（BP_BackpackComponentV2）`。

![ScreenShot_2026-08-17_151147_588.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IZEqtScreenShot_2026-08-17_151147_588.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zfXknimage.png)

在【细节】->【Backpack Tips】->【背包Tips配置】中将默认TipsID更改为Tips表中的TipsID。

|背包映射key|默认TipsID|默认文本|触发场景|
|-|-|-|-|
|BackpackSpaceNotEnough|81001|背包空间不足!|背包容量满，添加物品失败时|
|CannotAddToBackpack|81002|无法加入背包!|背包容量满，拾取物品失败时|
|CannotEquip|81003|无法装备!|装备不符合装备条件的装备时|
|AddToBackpackFailed|81004|加入背包失败!|添加物品失败时|
|EquipFailed|81005|装备失败!|装备物品失败时|
|EquipSuccess|81006|成功装备%s!|装备物品成功时|
|ItemPickedUp|81011|已拾取%s|拾取物品时|
|BackpackFullDropItem|81013|背包容量不足，自动丢弃%s|背包容量不足，自动丢弃物品时|
|CannotUseItemInCurren|81014|当前状态无法使用%s|使用当前状态无法使用的物品时|
|ItemCannotBeDropped|81016|该物品无法被丢弃|丢弃无法丢弃物品时|
|ItemDestroyed|81017|已销毁%s|物品被销毁时|


> %s 会被替换为对应的物品名称

+ 物品名称的文本颜色将以【玩法通用设置】->【物品品质配置】中的【品质文本颜色】显示。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AbCzHimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UP4khimage.png)

---

### Tips相关接口

获取背包Tips配置值

```lua
---通过Key查询BackpackTipsConfig TMap中对应的整型配置值
---生效范围：服务器&客户端
---@param Player PlayerPawn | PlayerController @玩家角色或者玩家控制器
---@param Key string @Tips配置Key
---@return number|nil @对应TipsID，未找到返回nil
function UGCBackpackSystemV2.GetBackpackTipsConfig(Player, Key) end
```

弹出背包Tips

```lua
---func 服务端/客户端调用
---@param TipKey string Tips配置Key（对应BackpackTipsConfig中的键）
---@param ItemDefineID userdata 物品DefineID
---@param Count number 物品数量，默认0
---@param Reason number EUGCCommonItemReason 通用操作原因，默认Default
 function BP_BackpackComponentV2_Custom:DisplayBackpackTipsV2(TipKey, ItemDefineID, Count, Reason)
    BP_BackpackComponentV2_Custom.SuperClass.DisplayBackpackTipsV2(self, TipKey, ItemDefineID, Count, Reason);
 end
```

<br>

---

## 通用屏幕指示器

> 文档路径: 进阶内容 > UI系统 > 通用屏幕指示器

> 文档ID: 20295 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20295)

> 更新: 2026-02-12 10:24:44

**涉及API/标识符:** `ActorMark`, `InDistanPanel`, `ObjectPositionWidget`

# 通用屏幕指示器

屏幕指示器是一种用于处理控件对象超出屏幕范围后显示效果的通用机制，适用于标记怪物、静态物件等场景。

![ScreenShot_2026-01-20_175045_914.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Wq61nScreenShot_2026-01-20_175045_914.png)

<br>

## ActorMark组件

ActorMark组件对蓝图进行引用实现提示场景中Actor位置的效果，对于实体编辑器中创建的怪物/场景可破坏物，其已经内置了这个组件，对于非实体实体编辑器创建的对象则需开发者手动添加ActorMark组件。

![ScreenShot_2026-01-19_164508_694.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/eP2TGScreenShot_2026-01-19_164508_694.png)

`ActorMark` 的配置项以及说明如下。

![image.4.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pdQzCimage.4.png)
+ 控件蓝图路径：怪物初始化时候会直接使用类默认值中配置的血条UI蓝图，在怪物中此选项无需配置
+ 出显示范围后是否显示箭头：怪物离开屏幕范围之后是否显示ui中配置的箭头（取消勾选“出显示范围是否隐藏”之后此选项才生效）
+ 出显示范围是否隐藏：怪物离开屏幕范围之后血条控件是否隐藏
+ 检查遮挡：检查怪物和角色之间是否有阻挡对怪物进行隐藏，若有则不会显示
+ 使用相机作为起点计算遮挡：若不勾选则会使用角色位置去计算遮挡
+ 最大显示距离：控件的最大显示距离，对怪物，此值无需配置，会自动使用怪物类默认值中的血条实时显示最大距离
+ 开始缩放距离：通用屏幕指示器开始缩放的最小距离
+ 结束缩放距离：通用屏幕指示器结束缩放的最大距离
+ 开始缩放值：距离为开始距离的时候，控件的整体缩放值
+ 结束缩放值：距离为结束距离的时候，控件的整体缩放值
+ 最小缩放粒度：每次缩放变化的最小单位
+ 开始Alpha距离：角色和目标透明度发生变化的最小距离
+ 结束Alpha距离：角色和目标透明度发生变化的最大距离
+ 开始Alpha值：在距离为开始距离的时候，控件的整体透明度
+ 结束Alpha值：在距离为结束距离的时候，控件的整体透明度，Alpha值越小，越透明
+ 最小Alpha粒度：每次透明度变化的最小单位
+ 开始偏移距离：开始偏移的最小距离
+ 结束偏移距离：结束偏移的最大距离
+ 开始偏移缩放值：距离为开始偏移距离的时候，控件的世界坐标偏移
+ 开始偏移缩放值：距离为结束偏移距离的时候，控件的世界坐标偏移
+ 最小偏移缩放粒度：每次偏移缩放值变化的最小单位
+ 从中间计算屏蔽限制
	+ 不勾选，表示从屏幕边缘开始计算屏幕限制
	+ 勾选，表示从屏幕中心开始计算屏幕限制
+ 屏幕限制为百分比：若不勾选则“屏幕限制”单位为像素否则为比率
+ 屏幕限制（左右上下）：表示指示光标会距离屏幕四个边缘多远的距离
+ 计算后的UI偏移：UI在使用最终世界坐标映射到世界后，还需再偏移才是最后的UI在屏幕的位置

<br>

## 创建指示器控件

为了展示屏幕指示器，开发者需要新建一个继承自`ObjectPositionWidget`的蓝图。

![ScreenShot_2026-01-16_155456_965.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7yNmEScreenShot_2026-01-16_155456_965.png)

在蓝图内新建``画布面板``并构建成如图所示层次结构，在各个画布面板中添加对应样式的控件。

![ScreenShot_2026-01-19_201900_035.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/qFxAKScreenShot_2026-01-19_201900_035.png)

+ InScreenPnl：Actor在屏幕中显示的控件
+ OutScreenPnl：Actor在屏幕外显示的控件
+ InArrowWidget：Actor在屏幕外的时候显示的箭头控件（“InArrowWidget”需放置在“OutScreenPnl”的层级下，否则无法正常运行）

“InScreenPnl”、“OutScreenPnl”和“InArrowWidget”的锚点均设置为点锚点靠左上对齐，并将组件置于画布面板的左上角。

![ScreenShot_2026-01-19_204347_257.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/GR9rWScreenShot_2026-01-19_204347_257.png)
![ScreenShot_2026-01-19_203630_280.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pBrJRScreenShot_2026-01-19_203630_280.png)


<br>

## 激活指示器

为了蓝图可以根据不同场景展示不同的组件，开发者需要对蓝图下的控件进行相关设置。
在此前创建的继承自`ObjectPositionWidget`的蓝图添加相关逻辑，示例如下：

```lua
function WBP_UGC_MonsterHealthBar:Event_InitParam()
    ---@field SetStateWidgetPanel:fun(InScreenPanel:UWidget,OutScreenPanel:UWidget,InArrowWidget:UWidget,InDistanPanel:UWidget,InDistanText:UTextBlock)
    self:SetStateWidgetPanel(self.InScreenPnl, self.OutScreenPnl, self.InArrowWidget, nil, nil)
end
```
各类参数及其含义如下。
```lua
-- @param InScreenPanel UWidget 对象在屏幕中显示的控件
-- @param OutScreenPanel UWidget 对象在屏幕外显示的控件
-- @param InArrowWidget UWidget 对象在屏幕外的时候需要显示的箭头控件，用来提示对象的方位，此控件会因对象的位置变化而产生一定的旋转
-- @param InDistanPanel UWidget 显示距离的控件
-- @param InDistanText UTextBlock 显示距离的文本控件，一般需要放在`InDistanPanel`里面
SetStateWidgetPanel:fun(InScreenPanel:UWidget,OutScreenPanel:UWidget,InArrowWidget:UWidget,InDistanPanel:UWidget,InDistanText:UTextBlock)
```

---

## 通用进度条UI

> 文档路径: 进阶内容 > UI系统 > 通用进度条UI

> 文档ID: 20392 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20392)

> 新增: 2026-06-02 16:50:29

**涉及API/标识符:** `duration`, `SetPercent`, `UGCGameSystem.GetUGCResourcesFullPath`, `UGCPlayerController`, `UGCPlayerController.SuperClass`, `UGCTimerUtility.CreateLuaTimer`, `UGCTimerUtility.RemoveLuaTimerByName`, `UGCWidgetManagerSystem.CreateWidgetAsync`

# 通用进度条UI
游戏中很多地方需要用到进度条，如角色技能蓄力、大招充能、道具耐久值等，编辑器提供了条形和环形两种样式的进度条供开发者选择，可以很方便的创建出来使用。
## 快速上手
### 1.创建进度条UI
进入UI编辑器，选择元件
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/poqVsimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/pi3cMimage.png)
从模板中创建条形或环形进度条
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EBjn3image.png)

### 2.使用进度条UI
这里举例两种使用方式
#### 2.1创建到界面中
将创建好的进度条元件配置到界面中
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hepCKimage.png)
打开```UGCPlayerController```的lua，游戏开始时进行调用
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/BRpfuimage.png)
``` local UGCPlayerController = {}

function UGCPlayerController:ReceiveBeginPlay()
    UGCPlayerController.SuperClass.ReceiveBeginPlay(self)
    self.Time = 10
    self.Duration = 0
    UGCWidgetManagerSystem.CreateWidgetAsync(UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/TestUI.TestUI_C'),
               function (Widget)
                   if Widget == nil then
                       print("UGCPlayerController:ReceiveBeginPlay(): Create failed")
                       return
                   end
                Widget:AddToViewPort()
                Widget.LineP:SetDuration(self.Time)
                Widget.CircleP:SetDuration(self.Time)

                UGCTimerUtility.CreateLuaTimer(0.1, function()
                    self.Duration = self.Duration + 0.1
                    KismetMathLibrary.FClamp(self.Duration, 0.0, 1.0)
                    if self.Duration / self.Time >= 1 then
                        UGCTimerUtility.RemoveLuaTimerByName("TestTimer")
                        return
                    end
                    Widget.LineP:SetText(self.Duration / self.Time)
                end, true, "TestTimer")
            end
           )
end

return UGCPlayerController
```
PIE即可看到实际效果
![企业微信截图_17794411892511.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/AdDgp%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17794411892511.png)
#### 2.2在蓄力技能中使用
这里用蓄力技能进行举例，将进度条应用到技能的蓄力中使用
在技能蓄力阶段的创建进度条UI任务，并点击它进行配置
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iU90Wimage.png)
进度条UI类型选择【自定义】，将创建好的进度条配置上，这里需要设置好锚点
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/X4kF2image.png)
PIE使用技能即可看到进度条效果
![2026-05-2211-40-58-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mudOY2026-05-2211-40-58-ezgif.com-video-to-gif-converter.gif)
## 进度条渐变色功能
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ebG2jimage.png)
条形进度条与环形进度条均支持进度条颜色渐变，配置项一样
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oSLrgimage.png)
|配置项|说明|
|-|-|
|StartPoint|进度条渐变色起点设置。如图，渐变色起点进度为0.2且颜色为蓝色，则20%之前的进度条充能为蓝色|
|EndPoint|进度条渐变色终点设置。如图，渐变色终点进度为0.8颜色为紫色，则80%之后的进度条充能为紫色，中间20%到80%则为蓝色到紫色的渐变过渡|
|Percent|百分比设置，取值0~1|
|Color|颜色设置|
## 可使用接口
``` function TestProgressBarUI:SetDuration(duration)
	self.duration = duration
	self.along_duration = 0.0
	self.frequence = 0.05
	self:SetPercent(self.along_duration)

	UGCTimerUtility.CreateLuaTimer(self.frequence, function()
		self.along_duration = self.along_duration + self.frequence
		if self.along_duration > self.duration then
			UGCTimerUtility.RemoveLuaTimerByName("Duration_Timer")
			print("TestProgressBarUI:SetDuration(duration):ClearDuration_Timer")
		end
		self:SetPercent(self.along_duration / self.duration)
	end, true, "Duration_Timer")
end
```
传入进度条充满所需要的时间```duration```，进度条将会在经过该时间后充满（环形进度条和条形进度条的API调用方式一样）,如不需要随时间充满，则使用```SetPercent```即可

```
function TestProgressBarUI:SetText(text)
    self.TextBlock_0:SetText(text)
end
```
进度条数显设置，在需要显示进度的时候将UI中的该组件的可见性设置为“可见”，调用即可修改数显（环形进度条数显随进度自动变化，可以不用设置）

---
