# 进阶内容/GamePlay系统/物资系统/物资编辑器1.0

> 本分类共 6 篇文章

---


## 概述

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器1.0 > 概述

**涉及API:** `SkillConfig`, `SkillTriggerEvent`

#  物资编辑器

物资特指在游戏内可以被拾取，装备，放入背包以及被使用的物品，物资编辑器用于创建新的物资，也可编辑已有的物资的相关属性设置。基于物资编辑器内提供的物资基础模板，可以快速创建新的物资，通过为物资绑定`Lua`脚本，可深度定制物资的功能和用途。

物资编辑器提供三方面的配置：属性配置，ItemHandle，PickupWrapper。

> 编辑器默认启用物品编辑器（物资编辑器2.0），如需使用旧物资编辑器，可参考 [旧物编入口开启方式](https://developer.gp.qq.com/wikieditor/#/catalog/20175?autoJump=%E5%85%B6%E4%BB%96) 说明

<br>

## 主界面

点击主界面顶栏**物资编辑**按钮进入物资编辑器主界面：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iliSVimage.png)
![企业微信截图_16868307946006.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868307946006.png)

物资编辑器主界面主要分为四个功能区域：文件操作区、模型预览、调试信息和属性配置区。

**文件操作区**

主要对文件进行相关操作，包括**新建物资**，**打开已有物资**，保存当前内容，打开ItemHandle及PickupWrapper配置窗口

**模型预览**

显示当前编辑中的物资模型和特效

**调试信息**

显示编辑过程中物资相关的日志信息

**属性配置区**

显示当前物资的**基础属性参数**，包括，堆叠数量，物资重量，物资类型，描述等

<br>

## 基础操作

### 新建物资

点击物资编辑器主界面顶栏**新建按钮**，在物资模板选择窗口选择自己需要的物资模板，并命名自定义物资，选择物资的存储位置

![企业微信截图_16868308309455.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868308309455.png)
![企业微信截图_1686830840727.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686830840727.png)
![企业微信截图_1686830848801.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686830848801.png)
<span style="color: #EE0000"> **强烈建议将自定义物品放在统一的文件夹中，命名方式遵循一定的规范和规律，方便后期对物资的查找** </span>

### 打开/删除物资

点击**打开按钮**打开已有物资列表，列表会将所有自定义物资展示出来，并可进行打开，删除快捷操作

![企业微信截图_16868308583239.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868308583239.png)
点击**打开按钮**打开已有自定义物资进行编辑，点击**删除按钮**即可删除已有自定义物资

![企业微信截图_16868308693005.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868308693005.png)

### 编辑物资属性

新建或打开物资后，在右边的**属性配置**面板中配置物资的基础属性

![企业微信截图_16868308769592.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868308769592.png)

<br>

## ItemHandle

ItemHandle用于管理物资在背包中被使用时需要处理的事情，包括使用物资，丢弃物资等。

通过物资编辑主界面顶栏**ItemHandle按钮**即可进入ItemHandle管理界面

![企业微信截图_16868308915761.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868308915761.png)
![企业微信截图_16868309071371.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868309071371.png)

文件操作主要是对当前物资进行**编译**，保存，或是绑定Lua脚本**定制化**功能的功能操作。

在细节面板中可以设置物资相关的一些参数，其中比较重要的是：
- `SkillTriggerEvent`，用于设置收到什么事件后执行物资绑定的技能
- `SkillConfig`，配置物资绑定的技能蓝图

<br>

## PickupWrapper

PickupWrapper用于配置物资在场景中可拾取时的参数和表现，可配置更改物资的模型，特效等表现。

点击物资编辑主界面顶栏**PickupWrapper**按钮打开PickupWrapper管理界面

![企业微信截图_16868309319611.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868309319611.png)
![企业微信截图_16868309385943.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868309385943.png)

在组件面板下，可以对物资的模型进行更改，或是添加新的组件。

---


## 创建新的药品

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器1.0 > 创建新的药品

**涉及API:** `ActionWithConditions条件Action`, `Equippable`, `SkillArchetypes`, `SkillEntryConfigs`, `StaticMesh`, `UAESkillManager`

#  创建新的药品

该部分将以 <span style="color: #EE0000">能量饮料</span> 作为模板，展示从创建物资，更改配置到放置到场景中并进行使用的整个过程

---

## 使用模板创建新的自定义物资

打开物资编辑器主界面后，点击顶栏**新建按钮**，打开模板创建窗口
![企业微信截图_16868206873073.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868206873073.png)
在**模板列表**里选择药品--能量饮料，选择**存储位置并为新建物资命名**后点击保存即可<br>
![企业微信截图_16868207039115.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868207039115.png)
![企业微信截图_16868207163832.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868207163832.png)
<span style="color: #EE0000">**强烈建议在Asset文件夹下新建一个Item文件夹用来存放自定义物资；物资命名也应遵从一定命名规律，以便之后查找**</span><br>
创建结束后，物资编辑器主界面将展示基础配置信息
![企业微信截图_16868207259686.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868207259686.png)

<details open>
<summary> <font face="楷体">主要配置说明</font> </summary><br>

`Max Count`                         物品在背包中的最大堆叠数量<br>
`Item Type`                           物品类型<br>
`Item Sub Type`                    物品子类型<br>
`Unit Weight F`                     物品重量<br>
`Equippable`                        可否装备<br>
`Pickup Dsc`                        拾取描述<br>
`Skill Config`                        物品技能配置<br>
`Item Big Icon N`                 物品Icon(大)<br>
`Item Big Icon N`                 物品Icon(小)<br>
`Auto Equip and Drop`         拾取时自动装备/替换<br>

</details>

可以根据自己对物资的需求，更改堆叠数量，拾取时的描述等；物品ID <span style="color: #EE0000">**无法更改**</span>，因为它是自动生成的，后续需要用到

---

## 配置物资技能蓝图

在使用模板创建药品（能量饮料）后，并不能直接使用，需要对物品绑定的**技能蓝图**进行编辑<br>
在物资编辑器主界面的**属性配置--Skill Config--0**中`Skill Template Class`选项就是需要更改的技能蓝图配置
![企业微信截图_1686820737721.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1686820737721.png)
这里**不能直接使用**模板中引用的技能蓝图，我们需要将其**复制**一份放在本地后再引用

### 复制技能蓝图

记住这里引用的技能蓝图名称，回到编辑器主界面，在顶栏打开**技能编辑器**
![企业微信截图_16868207508703.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868207508703.png)
在**详情--技能资源**处搜索相应的技能蓝图名称，并打开它
![企业微信截图_168682076076.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_168682076076.png)
打开对应的技能蓝图后，点击顶栏的**复制**按钮，将自动复制一份保存到**Asset/Blueprint**路径下
![企业微信截图_16868207696156.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868207696156.png)
![企业微信截图_16868207809228.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868207809228.png)
<span style="color: #EE0000"> **建议将复制的技能蓝图重命名，且按照一定命名规则** </span>

---

### 修改技能蓝图

再次重新打开技能编辑器，打开**刚刚复制的技能蓝图**，我们需要在技能蓝图里添加一个节点<br>
双击**恢复**打开
![企业微信截图_16868213195795.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868213195795.png)
![企业微信截图_16868213292531.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868213292531.png)
需要添加一个**消耗节点**，在空白处右键，搜索消耗，选择**消耗某个Item**，后将它连接起来<br>
如果不加这个节点，那么玩家使用道具将不会消耗道具数量<br>
<span style="color: #EE0000"> **如果要制作可无限消耗的物品，无需添加该节点**</span>
![企业微信截图_16868213398810.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868213398810.png)
点击该节点，将节点的`Item ID`改成之前创建物资时**自动生成的ID**，点击**Save**后退出技能编辑器
![企业微信截图_16868213569417.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868213569417.png)
回到物资编辑器主界面，在`Skill Template Class`中选择**刚刚修改过**的技能蓝图
![企业微信截图_16868213781246.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868213781246.png)

### 注册技能蓝图

复制并重新配置好技能蓝图后，我们需要在**PlayerPawn**蓝图中将技能蓝图注册后才能保证物品的正常拾取和使用
在**PlayerPawn**的`UAESkillManager`的`SkillEntryConfigs`和`SkillArchetypes`中新增一个配置项，并将新建的技能蓝图填入即可

---

## 修改物资模型&Icon

点击物资编辑器主界面顶栏**PickupWrapper按钮**打开拾取管理界面
![企业微信截图_16868214153927.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214153927.png)
在组件栏选择**StaticMesh**组件，在`StaticMesh`选择自己想要的模型，预览窗口可以预览选择的模型
![企业微信截图_16868214247359.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214247359.png)
![企业微信截图_16868214409646.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214409646.png)
修改完成后，依次点击顶栏**编译按钮**，**Save按钮**后关闭PickupWrapper管理界面<br>
回到物资编辑界面，在属性配置中将Icon项修改成相应的Icon配置，点击顶栏**保存按钮**后关闭物资编辑器主界面
![企业微信截图_16868214589060.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214589060.png)

---

## 更改玩家手中的物品模型

点击编辑器主界面顶栏**技能编辑器**并打开物资的技能蓝图，然后双击**前摇**节点
![企业微信截图_16868214725356.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214725356.png)
打开后，在蓝图中找到`ActionWithConditions条件Action`节点，点击它后将在**详情**中看到很多配置项
![企业微信截图_16868214819283.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214819283.png)
只需要关注`False Action`，打开它的子项，`Attach Actor Data`中的`Actor Template`配置，这里就是玩家手中物资的模型配置
![企业微信截图_16868214965161.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868214965161.png)
因为这里的蓝图还是模板中的蓝图配置，**不能直接使用**，所以需要**新建**一个蓝图来代替它<br>
使用**蓝图继承**来新建一个与其一样的蓝图（新建蓝图可看编辑器基础操作教学）<br>
新建好蓝图后，打开并修改`StaticMesh`下的模型
![企业微信截图_16868215092465.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868215092465.png)
修改好后，**编译**并**保存**后退出<br>
回到技能编辑器并打开技能蓝图，找到之前的`Actor Template`配置，将这里的配置修改成**刚刚新建的蓝图**
![企业微信截图_16868215204926.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868215204926.png)
**至此，成功修改了玩家手中的物资模型**

---

## 进阶--更改恢复数值

可以通过修改配置调整物资的回血数值<br>
进入**技能编辑器**并打开物资技能蓝图，进入**恢复**，可以看到两个恢复节点<br>
![企业微信截图_16868216639977.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868216639977.png)
第一个恢复节点恢复的是**能量值**，第二个恢复节点恢复的是**信号值**<br>
进入任一恢复节点，修改**恢复数值**即可<br>
![企业微信截图_16868216711453.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868216711453.png)

---

## 进阶--改变物资使用时间

通过修改技能蓝图的前摇时间可以延长物资的使用时间<br>
进入技能编辑器，打开物资的技能蓝图，进入**前摇**

---

### 修改技能提示

使用药品类物资时，会出现文字提示和倒计时<br>
选择**显示技能提示**节点，修改`Last Time`和`Prompt Text`配置，前者表示倒计时时间，后者表示使用物资时的文字提示
![企业微信截图_16868216967920.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868216967920.png)

---

### 修改技能时长

选择**前摇**节点，修改`Phase Duration`配置，表示技能从开始到结束的时间，应与`Last Time`相同
![企业微信截图_16868217135602.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868217135602.png)

---

### 匹配动作速度

更改了技能时长后，还需要按比例更改**技能释放动作的时长**，编辑器主要是通过设置动画的**播放速度**来调整<br>
选择**PlayMontageWithPose播放姿势蒙太奇**节点，修改`Play Speed Rate`配置<br>
<span style="color: #EE0000"> **Play Speed Rate配置的是动画的播放速度，该值越小，播放越慢，动画的时长也越长** </span>
![企业微信截图_16868217223256.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868217223256.png)
**至此，一个全新的，类似能量饮料的新物资就制作完成了**



---


## 枪械物资

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器1.0 > 枪械物资

**涉及API:** `BP_Rifle_M416`, `CrossHair`, `CrossHairData`, `HUDOwner`, `IsSpreadEnable`, `OnWeaponDrawHUDDelegate`, `PartDamage`, `ShootWeaponEntity`, `WeaponClass`, `WeaponHudWidget`

#  枪械物资

该部分将以 <span style="color: #EE0000"> M416 </span>为模板创建新的枪械武器。

<br>

## 创建枪械物资

在物资编辑器内选择M416对应的枪械模板，创建过程不再赘述。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/sPay5image.png)

观察可以发现，枪械物资的基础配置与药品物资基本相同，只是枪械Icon多了两个配置，在配置的时候注意。

<br>

## 自定义配置

<span style="color: #EE0000">由于和平精英武器框架的复杂性，不建议修改枪械的模型，</span>以下仅介绍如何修改枪械常用的配置。

### 创建枪械武器蓝图

在使用模板创建了新的枪械物资后，我们进入ItemHandle，找到 ``WeaponClass`` 配置项，这里就是枪械武器蓝图的配置。

通过继承自模板内配置的枪械武器蓝图 ``BP_Rifle_M416`` 以创建新的蓝图类（蓝图创建及继承，在此不赘述），创建后，将我们新建的枪械武器蓝图配置到``WeaponClass``配置项即可。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HvHdUimage.png)

---

### 子弹飞行速度

子弹飞行速度指的是子弹在**空中飞行**的速度，影响从开枪到击中的时间。

在枪械武器蓝图中的 ``ShootWeaponEntity`` 组件 ``Shoot Config`` 配置项下，``Bullet Fire Speed`` 属性即为子弹飞行速度配置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zmup6image.png)

初始值为默认值，该值越大，子弹飞行速度越快，反之则越慢。

---

### 子弹拖尾特效

子弹拖尾特效是指在子弹飞行过程中，为了增强视觉效果而产生的尾迹效果，增加拖尾可以给玩家提供更直观的射击反馈，提升游戏的真实感。

![QQ202409-ezgif.com-video-to-gif-converter.gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/0T0rKQQ202409-ezgif.com-video-to-gif-converter.gif)

在枪械武器蓝图中的 ``ShootWeaponEntity`` 组件下的 ```Visual Bullet Track Config``` 配置项中，可配置相关属性的参数。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ql26kimage.png)

- FPPSetting：第一人称视角
- TPPSetting：第三人称视角
- Gun ADSSetting：瞄准射击视角，即开镜状态

开发者可以根据需要配置以上三个视角状态下的每把枪的子弹拖尾效果。

在完成蓝图相关配置后，开发者还需调用以下API以启用拖尾效果。

``` lua
-- 启用子弹尾迹特效
-- 生效范围：服务器
-- @param PlayerController PlayerController* @玩家控制器
function UGCPlayerControllerSystem.EnableBulletTrackEffect(PlayerController)
end
```

---

### 枪械准心

枪械准心是指在游戏中，显示在屏幕中心用于辅助瞄准的视觉元素。它通常由多种形状和颜色的组成部分构成，以提供清晰的瞄准指示，开发者可以根据配置要求修改自己想要的准心效果。

目前提供了两种自定义准心的方式：设置准心组件与画布绘制准心。

#### 设置准心组件

和平原生的枪械准心是通过读取枪械武器蓝图中的 ```CrossHair``` 组件下的 ```CrossHairData``` 配置来实现，枪械准心由五部分组成：
- 中心点：准心的核心部分，通常是一个小点或十字，用于精确瞄准目标。
- 横向线条（2部分）：两条水平线，帮助玩家判断左右方向，增强瞄准的准确性，会随着玩家移动而缩放。
- 纵向线条（2部分）：两条垂直线，帮助玩家在上下方向上进行瞄准，会随着玩家移动而缩放。

在 ```CrossHairData``` 数组中，索引0-3配置项为横向线条和纵向线条，索引4配置项为中心点，其中索引0-3配置项使用同一张贴图，主要修改了位置偏移和旋转角度，索引4配置项使用的是中心点贴图，位置和旋转均为默认。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/LWWBMimage.png)

各配置项具体的属性说明如下：

|参数|名称|描述|
|-|-|-|
|Icon|图标|Icon下的主要配置为Texture；UV为图片的起始坐标默认为0就好；UL为图标的宽，VL为图标的高|
|Offset|偏移|图标根据屏幕中心点的偏移|
|IconOffset|图标偏移|图标整体往屏幕的哪个方向偏移|
|bIconOffsetNotUseUIScale|图标是否根据屏幕比例缩放|勾选图标会根据屏幕的比例进行缩放|
|Alpha|透明度|图标的透明度|
|Scale|缩放|缩放默认为1|
|IconRotate|旋转值|图标的旋转角度，例如十字准心就是相同的1个图片旋转组成了一个“十”字|
|LogicRotate|逻辑旋转值|和上述旋转值保持一致即可|
|IsSpreadEnable|启用动态准心|启用之后准心会动态缩放|
|SpreadScale|动态缩放系数|动态缩放的幅度|

以设置准心贴图为例，在枪械武器蓝图中清空 ``CrossHair`` 组件的默认数据配置项，重新添加一个元素，此处设置了一张名为“2X_Reticle”的贴图，并根据贴图大小修改了 ```UL``` 值与 ```VL``` 值，具体贴图大小可双击贴图查看。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/311mDimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/cp8qPimage.png)

取消勾选 ```IsSpreadEnable```，即禁用动态准心。

配置完成后，启动调试游戏，装配上对应的枪械，发现设置的准心贴图已生效。

![QQ202409-ezgif.com-video-to-gif-converter (1).gif](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/d5kCLQQ202409-ezgif.com-video-to-gif-converter%20(1).gif)

#### 画布绘制准心

画布绘制是基于屏幕HUD界面通过调用API逻辑绘制出准心效果，这种方式与准心组件不兼容，需要清空 ``CrossHair`` 组件的配置，且不具备复杂的动态效果能力。

首先在枪械武器蓝图脚本中绑定 ``OnWeaponDrawHUDDelegate`` 委托，委托触发的回调函数中通过 ``WeaponHudWidget`` 参数可以获取到HUD实例对象 ``HUDOwner``，进而可以在回调函数中实现绘制逻辑。

``` lua
---@class NewM416_C:BP_Rifle_M416_C
--Edit Below--
local NewM416 = {}
 
function NewM416:ReceiveBeginPlay()
    NewM416.SuperClass.ReceiveBeginPlay(self)

    if self:HasAuthority() then
        return
    end

		-- 绑定委托，回调函数为DrawHUD
    self.OnWeaponDrawHUDDelegate:Add(self.DrawHUD, self)
end

function NewM416:DrawHUD(WeaponHudWidget, Canvas)
    -- 绘制逻辑
end
```

**DrawLine**

DrawLine可以绘制线段，例如绘制两条横向线条和纵向线条作为枪械的十字准心：

``` lua
WeaponHudWidget.HUDOwner:DrawLine(0, Canvas.ClipY / 2, Canvas.ClipX, Canvas.ClipY / 2, {1.0, 1.0, 0}, 1.0)
WeaponHudWidget.HUDOwner:DrawLine(Canvas.ClipX / 2, 0, Canvas.ClipX / 2, Canvas.ClipY, {1.0, 1.0, 0}, 1.0)
```

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Ggrbiimage.png)

**DrawTextureSimple**

DrawTextureSimple可以绘制指定的贴图：

``` lua
self.TextureDraw = UE.LoadObject('/Game/Arts/UI/TableIcons/ItemIcon/Inkjet/2021newyear_128.2021newyear_128')
WeaponHudWidget.HUDOwner:DrawTextureSimple(self.TextureDraw, Canvas.ClipX / 2 - 64, Canvas.ClipY / 2 - 64, 1)
```

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/m3qpRimage.png)

---

### 枪械伤害

在枪械武器蓝图中的 ``ShootWeaponEntity ``组件下的 ``Bullet Config`` 配置项下，``Base Impact Damage`` 属性即为枪械基础伤害配置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3pmHdimage.png)

还可以根据不同的命中部位单独设置伤害比例，``ShootWeaponEntity`` 组件下的 ``PartDamage`` 配置项内即为命中人物不同部位的伤害百分比

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ybokbimage.png)

---

### 弹夹容量

枪械的弹夹容量由两部分配置：
1. 弹夹初始容量：当玩家将枪械拾取时，弹夹内的容量即为初始容量
2. 最大弹夹容量：当玩家备弹量足够时，按照最大弹夹容量进行装填

> 此处不包含枪械扩容弹夹带来的额外容量

枪械武器蓝图中的 ``ShootWeaponEntity`` 组件下的 ``Bullet Config`` 配置项下的 ``Init Bullet in Clip`` 属性即为弹夹初始容量，更改此配置的数值就可以修改弹夹的初始容量。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/OszdXimage.png)

枪械武器蓝图中的 ``ShootWeaponEntity`` 组件下的 ``Shoot Config`` 配置项下的 ``Max Bullet Num in One Clip`` 属性即为最大弹匣容量。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/JNBtsimage.png)

---

### 无限弹药

在某些情况下，会需要枪械带有无限的弹药，我们提供了两种配置项达到不同的配置效果。

1. 拥有无限弹药但仍有弹夹容量，仍需换弹
 
	枪械武器蓝图中的 ``ShootWeaponEntity`` 组件下的 ``Bullet Config`` 配置项下的 ``Has Infinite Bullets`` 属性即为无限弹药配置，将其勾选后即可拥有无限弹药且具有弹夹容量。
	
	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KvtMiimage.png)

2. 拥有无限弹药且无需换弹

	枪械武器蓝图中的 ``ShootWeaponEntity`` 组件下的 ``Bullet Config`` 配置项下的 ``Clip Has Infinite Bullets`` 属性即为无限弹药配置，将其勾选后即可拥有无限弹药且无弹夹容量。

	![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/50MIyimage.png)

---


## 投掷物物资

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器1.0 > 投掷物物资

**涉及API:** `BP_Grenade_Shoulei_Weapon`, `BP_ThrowComponent`, `EffectScale`, `EliteProjectile`, `ItemHandle`, `PickupWrapper`, `ProjGrenade_BP`, `ProjectileMesh`, `RangeScale`, `ReceiveProjectileExplodedEvent`, `Sphere`, `StaticMesh`, `WeaponClass`

#  投掷物物资

该部分将以<span style="color: #EE0000">破片手榴弹</span>为模板创建新的投掷物物资

<br>

## 创建手雷物资

在物资编辑器中选择 ``投掷物 -> 破片手榴弹`` 创建，新建过程可参考其他类型物资，不再赘述。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gwiQqimage.png)

<br>

## 自定义配置

如果想要改变手雷的一些属性，例如爆炸延迟时间、瞄准时间等，需要修改手雷物资关联的手雷武器蓝图及手雷抛体蓝图。

### 创建手雷武器蓝图

在手雷的ItemHandle中找到手雷武器蓝图配置项，``WeaponClass``即为手雷武器蓝图类：

![企业微信截图_16873298909368.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873298909368.png)

继承自 ``BP_Grenade_Shoulei_Weapon`` 创建新的蓝图类，创建好后，将新的武器蓝图路径配置到 ``Weapon Class`` 属性中引用。

![企业微信截图_16873299013871.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873299013871.png)

---

### 创建手雷抛体蓝图

```EliteProjectile``` 是手雷抛出时的蓝图类，该蓝图类配置在 ``BP_ThrowComponent`` 组件的 ``Projectile Class`` 属性中。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YEjBBimage.png)

继承自 ``ProjGrenade_BP`` 创建新的抛体蓝图类，将新的抛体蓝图路径配置到``Projectile Class`` 属性中引用。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/YSiCzimage.png)

---

### 手雷模型

手雷模型分为三类：手持模型、拾取物模型及抛体模型。

**手持模型**

点击物资编辑器，选择新建的手雷，点击并打开 ```ItemHandle```，属性面板中搜索 ```UBackpack Weapon Handle```，修改 ``St Mesh`` 和 ``St Mesh Lod``：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/DHLPYimage.png)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ojTqIimage.png)

修改完成重新编译并保存，启动调试游戏，装备手雷查看效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/emHmjimage.png)

**拾取物模型**

点击物资编辑器，选择新建的手雷，点击并打开 ```PickupWrapper```，找到 ```StaticMesh``` 组件，修改静态网格体与材质：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bGviwimage.png)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bQlt0image.png)

修改完成重新编译并保存，将wrapper蓝图放置在场景中，启动调试游戏，查看模型替换效果：

![企业微信截图_17284406205122.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PtGCC%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17284406205122.png)

**抛体模型**

双击打开手雷抛体蓝图，找到 ```ProjectileMesh``` 组件，修改静态网格体与材质：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IECnIimage.png)

修改完成重新编译并保存，启动调试游戏，将手雷投掷出去查看效果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/f5Zcrimage.png)

---

### 爆炸延迟时间

确认投掷（拉环）后到爆炸的时间

手雷武器蓝图中 ``BP_ThrowComponent`` 组件的 ``Explosion Delay Oerride`` 属性为爆炸延迟时间参数：

![企业微信截图_16873299094392.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873299094392.png)

---

### 投掷冷却时间

投掷两枚手雷之间的间隔

手雷武器蓝图中 ``BP_ThrowComponent`` 组件的 ``Throw Cooldown Duration`` 属性为投掷冷却时间参数：

![企业微信截图_16873299191492.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873299191492.png)

---

### 爆炸范围与伤害

自定义设置手雷的爆炸范围和伤害数值

**修改爆炸范围**

双击打开手雷抛体蓝图，找到 ``Sphere`` 属性配置项，该配置项即代表手雷爆炸时的伤害范围（单位：厘米）

![企业微信截图_16873299373722.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873299373722.png)

**修改手雷伤害**

手雷的伤害根据距离判定、有衰减，因此一般使用曲线进行配置，在抛体蓝图中找到 ``Damage Curve`` 属性配置项，新建一个曲线，替换该配置

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Ml3WKimage.png)
![企业微信截图_16873299438299.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16873299438299.png)

> 横轴为距离，竖轴为伤害

**动态修改爆炸范围与伤害**

打开抛体蓝图关联的lua类文件，脚本中已经内置了可以使用的函数和事件：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3LHrUimage.png)

在 ```ReceiveProjectileExplodedEvent``` 事件中可以通过调整 ```RangeScale``` 和 ```EffectScale``` 两个属性值，实现动态修改爆炸范围与伤害的效果。

``` lua
function ProNew:ReceiveProjectileExplodedEvent(HitResult)
    local HitActor = HitResult.Actor
    self.RangeScale = 2 -- 修改爆炸范围
    self.EffectScale = 5 -- 修改伤害效果
    ProNew.SuperClass.ReceiveProjectileExplodedEvent(self,HitResult)
end
```

> 此方式只在C4/烟雾弹/破片手雷/铝热弹/震爆弹中生效








---


## 为玩家添加初始道具

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器1.0 > 为玩家添加初始道具

**涉及API:** `AddItem`, `GetPlayerCharacterSafety`, `HasAuthority`, `KismetSystemLibrary.K2_SetTimerDelegateForLua`, `ObjectExtend.CreateDelegate`, `ReceiveBeginPlay`, `ReceiveEndPlay`, `ReceiveTick`, `SuperClass.ReceiveBeginPlay`, `UGCBackPackSystem`, `UGCBackPackSystem.AddItem`, `UGCPlayerController`, `UGCPlayerController_C`, `UGCPlayerController蓝图`

# 为玩家添加初始道具

在实际制作过程中，我们会在玩家进入游戏时就为他们配备一定的物资，即为角色增加初始道具
我们以最简单的场景为例，在玩家出生后，为角色装备一把枪

---

我们打开**Asset/Blueprint**路径下的`UGCPlayerController蓝图`绑定的Lua脚本 <span style="color: #EE0000">（若是没能找到其绑定的脚本，直接打开UGCPlayerController蓝图，点击顶栏的**Lua按钮**即可自动绑定一个与其同名的Lua脚本）</span>
![企业微信截图_16868309603538.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868309603538.png)
![企业微信截图_16868309685920.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868309685920.png)
第一次打开脚本时，我们会发现这个脚本里是没有任何逻辑的，三个自带函数都被注释掉

```lua
---@class UGCPlayerController_C:BP_STExtraPlayerController_C
--Edit Below--
local UGCPlayerController = {}; 

-- function UGCPlayerController:ReceiveBeginPlay()

-- end
-- function UGCPlayerController:ReceiveTick(DeltaTime)

-- end
-- function UGCPlayerController:ReceiveEndPlay()
 
-- end
return UGCPlayerController;
```

其中，我们只需要关注第一个函数`UGCPlayerController:ReceiveBeginPlay`，它会在玩家角色**初始化**时自动执行，在我们开始游戏时就会执行，所以我们将为角色装备武器的逻辑写在这里

```lua
local UGCPlayerController = {}; 

    function UGCPlayerController:ReceiveBeginPlay()
		-- 执行父类的ReceiveBeginPlay函数
        self.SuperClass.ReceiveBeginPlay(self)
		-- 创建一个延时执行函数体
        local OBTimerDelegate = ObjectExtend.CreateDelegate(self, 
        function()
        if self:HasAuthority() == true then -- 判断是否在服务端执行
            local PlayerPawn = self:GetPlayerCharacterSafety()  -- 获取玩家角色Pawn
            UGCBackPackSystem.AddItem(PlayerPawn, 102005, 1)  -- 为角色增加物品
        end
        end
        )
		-- 执行延时函数体
        KismetSystemLibrary.K2_SetTimerDelegateForLua(OBTimerDelegate, self, 2, false)
    end
-- function UGCPlayerController:ReceiveTick(DeltaTime)

-- end
-- function UGCPlayerController:ReceiveEndPlay()
 
-- end
return UGCPlayerController;
```

`self.SuperClass.ReceiveBeginPlay(self)`这句表示执行父类的`ReceiveBeginPlay`函数，因为某些设置的初始化是在`UGCPlayerController`的父类执行的，如果不执行的话会导致报错<br>
创建一个延时函数体为了等待玩家角色初始化完成后再执行物品添加操作，否则会报错<br>
为玩家角色添加物品**只能在服务端执行**，因为游戏框架的原因，在客户端直接添加物品会导致服务端报错，因此使用`self:HasAuthority()`来限定逻辑只在服务端运行

```lua
-- 为玩家添加物品
-- @param PlayerPawn  玩家Pawn
-- @param ItemID  物品ID
-- @param Num  物品数量
UGCBackPackSystem.AddItem(PlayerPawn, ItemID, Num)
```

至此，我们就为玩家在游戏开始时装备了初始物品

---

我们知道了这个给玩家增加物品的逻辑之后，我们可以在游戏中的任意阶段给玩家增加物品，并非一定要开始游戏时，注意逻辑执行的时机即可<br>
**可下载附件中的示例工程进行体验**

<br>

附件：



<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SetWeaponTest.7z">SetWeaponTest.7z</a>

---


## 物资刷新示例

> 文档路径: 进阶内容 > GamePlay系统 > 物资系统 > 物资编辑器1.0 > 物资刷新示例

**涉及API:** `AddConcomitants`, `AddItem`, `AddItemGroup`, `DropItemConfig`, `DropItemConfig.GetDropItems`, `DropItemGroup`, `HasAuthority`, `K2_DestroyActor`, `K2_GetActorLocation`, `K2_GetActorRotation`, `Monster`, `RandomItem`, `ReceiveBeginPlay`, `RewardBox`, `TableHelper.DeepCopy`, `UGCDropItemMgr`, `UGCDropItemMgr.SpawnItems`

#  物资刷新示例

在某些游戏中，我们会需要在场景中的某些位置刷出物资，类似于和平精英中的在地上刷出物资的功能。<br>
这里就会介绍如何在绿洲启元编辑器中实现上述的物资刷新功能<br>
<span style="color: #EE0000"> 注：该功能并非绿洲启元编辑器中的工具功能，完全由脚本实现 </span>

## 物资刷新功能介绍

我们实现的物资刷新功能具有几个特点：**刷新点配置，刷新类型配置，刷新概率配置，物资权重配置**

### 刷新点配置

我们通过创建SpawnActor的子类型蓝图，直接拖放在游戏场景中完成刷新点的配置，直观且高效

### 刷新类型配置

我们提供了三个配置的物资类型：<br>
``RewardBox``：宝箱类物资，类似于和平精英内的空投，在一个箱子内刷新多个物资<br>
``RandomItem``：随机物品类物资，即在某个刷新点根据配置随机刷出若干件物资<br>
``Monster``：怪物掉落物资，用于刷出怪物死亡时掉落的物资<br>
根据实际的物资刷新需要选择想要的刷新物资类型，<span style="color: #EE0000"> 也可以根据自己的定制化需求新增新的物资类型 </span>

### 刷新概率配置

我们可能并不希望在一个刷新点每次都能刷出物资，这种刷新概率是能配置的，根据配置，在实际刷新时会根据配置判断当前刷新点是否刷新

### 物资权重配置

我们可以通过配置不同物资的权重控制刷新点刷出的物资，权重就是物资刷出的概率

---

## 实现过程

我们下面就会介绍如何在绿洲启元编辑器中实现具有上述特点的物资刷新功能

### 创建物资Actor

**物资Actor**是我们直观配置刷新点的蓝图类，通过它可以配置刷新点和刷新物品组<br>
在实际的游戏中，我们可能会根据刷新点的刷新时间不同，刷新点所在区域不同等等区别，创建使用不同的物资Actor<br>
首先，我们需要创建一个**SpawnActor**蓝图作为我们所有物资Actor的父类
![企业微信截图_16868310082236.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16868310082236.png)
SpawnActor创建时继承**Actor类**，然后在SpawnActor中增加一个名为``DropItemGroup``的**整形变量**，它用来标识该刷新点刷新的物品组ID<br>
最重要的一步就是，为SpawnActor绑定一个Lua脚本，实现物资的生成逻辑。在其绑定的脚本中写上以下脚本代码

```lua
DropItemConfig = require("Script.DropItemConfig")
UGCDropItemMgr = require("Script.UGCDropItemMgr")
local SpawnActor = {}; 
function SpawnActor:ReceiveBeginPlay()
---检测是否在服务端执行
    if not self:HasAuthority() then
        self:K2_DestroyActor()
        return
    end
---生成物资
    local ItemList = DropItemConfig.GetDropItems(DropItemConfig.ItemKey.RandomItem, self.DropItemGroup)
    UGCDropItemMgr.SpawnItems(ItemList, self:K2_GetActorLocation(), self:K2_GetActorRotation(), 0)
end
return SpawnActor;
```

该代码主要是两部分逻辑：检测，生成<br>
检测该物资生成操作是否在服务端运行。因为刷新物品的操作**只能在服务端运行**，在客户端运行会被检测为非法行为；在确认该行为是在服务端运行之后，执行之后的物资生成逻辑。<br>
完成以上操作后，SpawnActor就已经创建完成<br>
我们创建一个物资Actor，它继承的是SpawnActor，因此我们可以在物资Actor的``DropItemGroup``变量处配置我们想要刷新的物品组，然后将物资Actor拖入场景中我们想要刷新物资的位置即可<br>
<span style="color: #EE0000"> 由于物资Actor继承的是SpawnActor，所以它也会执行SpawnActor绑定的脚本。但是为了保证物资生成逻辑的执行，我们为物资Actor也绑定一个Lua脚本</span>

```lua
---@class ItemActor_C:SpawnActor_C
--Edit Below--
require("Script.TableHelper")
local ItemActor = TableHelper.DeepCopy(require("Script.Blueprint.SpawnActor"))
return ItemActor
```

---

### 配置刷新物品

为了简化物品的配置流程，我们使用一个``DropItemConfig``的配置脚本，它主要通过4个配置函数来完成物品组的配置

```lua
---初始化物品类型组
local function InitGroup(GroupName, GroupId)
    DropItemConfig.ItemsGroup[GroupName][GroupId] = {}
    return DropItemConfig.ItemsGroup[GroupName][GroupId]
end

---增加一个物品组
local function AddItemGroup(Data, Pro, Count)
    local Tmp = {Pro = Pro, Count = Count,Items = {}}
    table.insert(Data, Tmp)
    return Tmp
end

---增加附加子表
local function AddConcomitants(Data, ItemID, StackCount, CountMin, CountMax)
    local Tmp = {ItemID = ItemID; StackCount = StackCount; CountMin = CountMin; CountMax = CountMax}
    table.insert(Data.Concomitants, Tmp)
    return Tmp
end

--增加物品
local function AddItem(Data, ItemID , Count, Weigth, ...)
    local Tmp = {ItemID = ItemID; Count = Count; Weigth = Weigth; Concomitants = {}}

    --初始化附加子表物品
    local Concomitants = {...}
    for k,v in pairs(Concomitants) do
        local ItemID = v[1]
        local StackCount = v[2]
        local CountMin = v[3]
        local CountMax = v[4]
        AddConcomitants(Tmp, ItemID, StackCount, CountMin, CountMax)
    end
    table.insert(Data.Items, Tmp)
    return Tmp
end
```

通过这4个配置函数，我们可以快速地配置我们想要的物品组

```lua
---RandomItem类型物品组配置示例
local Data = InitGroup(DropItemConfig.ItemKey.RandomItem, 25)
local ItemGroup = AddItemGroup(Data, 100 ,1)
AddItem(ItemGroup, 102001, 1, 10, {301001, 30, 1, 2})
AddItem(ItemGroup, 102005, 1, 10, {301001, 30, 1, 2})
AddItem(ItemGroup, 102003, 1, 10, {301001, 30, 1, 2})
AddItem(ItemGroup, 102002, 1, 10, {305001, 30, 1, 2})
```

<span style="color: #EE0000"> 这里仅举例RandomItem类型的物品组配置，另外两种类型的物品组配置可查看示例工程中的DropItemConfig</span><br>
至此，我们的物品组配置也就完成了

---

关于物品如何根据配置确定刷新物品并将其生成的过程，这里不做赘述<br>
**大家可以下载附件中的示例工程体验**

<br>

附件：



<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/SpawnItemProject.7z">SpawnItemProject.7z</a>

---
