# 进阶内容/UI系统

> 本分类共 12 篇文章

---


## UMG Lua的结构

> 文档路径: 进阶内容 > UI系统 > UMG Lua的结构

**涉及API:** `ReceiveTick`

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


## 富文本框

> 文档路径: 进阶内容 > UI系统 > 富文本框

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


## 快速入门

> 文档路径: 进阶内容 > UI系统 > 快速入门

**涉及API:** `Asset`, `Blueprint`

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


## 异形屏适配

> 文档路径: 进阶内容 > UI系统 > 异形屏适配

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


## 和平主界面控件布局

> 文档路径: 进阶内容 > UI系统 > 和平主界面控件布局

**涉及API:** `AddToSlot`, `SetWidgetLayout`, `UGCWidgetManagerSystem`, `WidgetLayout`

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

<br>

## 使用WidgetLayout

### 创建WidgetLayout

在项目的内容浏览器中，右键 ``用户界面 -> WidgetLayout``，点击创建并命名，双击打开蓝图可看到内置的和平主界面控件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xJvoTimage.png)
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

**涉及API:** `AddToSlot`

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


## 通用屏幕指示器

> 文档路径: 进阶内容 > UI系统 > 通用屏幕指示器

**涉及API:** `ActorMark`, `Event_InitParam`, `InDistanPanel`, `ObjectPositionWidget`, `SetStateWidgetPanel`, `UTextBlock`, `UWidget`

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


## 技能元件

> 文档路径: 进阶内容 > UI系统 > 技能元件

**涉及API:** `Construct`, `IsSkillEnable`, `OnSkillBound_BP`, `PlayerPawn`, `SuperClass.InitCDProgress`, `SuperClass.OnSkillBound_BP`, `UE.IsValid`

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


## 头像框组件

> 文档路径: 进阶内容 > UI系统 > 头像框组件

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


## 强引导组件

> 文档路径: 进阶内容 > UI系统 > 强引导组件

**涉及API:** `Border`, `Border_0`, `ButtonBP`, `CanvasPanel_0`, `GameState`, `Image_2`, `ItemBP`, `SelfHitTestInvisible`, `SizeBox_0`, `UTRichTextBlock_Tips14_1`, `Visible`

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


## 通用进度条UI

> 文档路径: 进阶内容 > UI系统 > 通用进度条UI

**涉及API:** `SetPercent`, `UGCPlayerController`

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
