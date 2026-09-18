# AI工具

> 官方知识库同步分类，共 4 篇文章

---

## AI生成图片

> 文档路径: AI工具 > AI生成图片

> 文档ID: 20395 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20395)

> 新增: 2026-05-21 14:29:14

# AI生成图片
为了帮助开发者拓展更多玩法内容和提高玩法美术品质，现在编辑器内置AI工具-AI生成图片。

## 操作步骤
1、通过【AI助手】进入AI工具界面，选择【AI生成图片】
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/rSM4cimage.png)

2、选择参考图片并配置提示词，点击生成预览，则会提示你前往历史记录查看
ps：若找不到合适的参考图，纯文字提示词也是能生成的
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/yI3Vximage.png)

3、切换到历史记录页签，选中刚刚提交的生成数据，并等待3min即可查看到生成的图片
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/g4Lm3image.png)

## 功能使用规范
为了保证功能正常使用且符合转换预期，进行转换前请遵循下述使用规范：

- 上传的参考图片格式应为JPG,大小应控制在10M以内;
- 目标生成图输入尺寸需满足:宽高维度均在[512,2048]范围内;宽高乘积(即图像面积)不超过1024×1024像素;
- 单次生成不论失败或成功都会消耗次数
- 提示词长度输入不超过150字
- 参考图及提示词不得涉及政治,色情等其他违规恶意内容;若存在恶意违规情况,将被限制或禁止使用该功能

---

## AI生成角色

> 文档路径: AI工具 > AI生成角色

> 文档ID: 20453 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20453)

> 新增: 2026-09-10 17:23:58

**涉及API/标识符:** `UGCGameSystem.GetUGCResourcesFullPath`, `UGCPlayerPawn.lua`, `UGCPlayerPawn.SuperClass`, `UGCPlayerPawnSystem.ChangeAvatarMesh`

# AI生成角色

AI生成角色功能允许开发者通过输入关键词并导入风格图片，帮助开发者快速生成可供直接使用的角色模型与外观贴图。

> 目前仅支持生成骨架类型为“主角骨架”的角色，暂不支持其他骨架类型

<br>

## 操作步骤

### 生成角色模型

在编辑器主界面的工具栏，点击打开【AI协作】窗口，选择【AI生成角色】进入角色生成界面。

![ai生成角色.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lwubiai%E7%94%9F%E6%88%90%E8%A7%92%E8%89%B2.drawio.png)

上传风格图并输入提示词后，点击“生成预览”。

![ai生成角色-第 2 页.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/EqsXPai%E7%94%9F%E6%88%90%E8%A7%92%E8%89%B2-%E7%AC%AC%202%20%E9%A1%B5.drawio.png)

角色模型的生成需要一定时间，可从历史记录查看生成进度，尚未完成的任务会显示“生成模型中”。

![企业微信截图_17875630988791.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/oKhEn%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17875630988791.png)

已生成完毕的模型会提示“已生成模型”，选择对应历史记录后点击“下载”即可将角色模型资源保存至本地。

![ai生成角色-第 3 页.drawio.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/RNji0ai%E7%94%9F%E6%88%90%E8%A7%92%E8%89%B2-%E7%AC%AC%203%20%E9%A1%B5.drawio.png)

---

### 配置角色模型

首先将先将模型Lod0以及所有纹理贴图导入工程。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8QpSjimage.png)
![企业微信截图_1787567049659.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/I9l0Z%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1787567049659.png)

导入模型期间，骨架选择“主角骨架”，勾选【导入动画】，最后点击“导入所有”。

![企业微信截图_1787641854713.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/vUh2F%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_1787641854713.png)

创建一个材质实例，父级选择“通用物件（Spline）”，按下图所示，在对应属性引用对应纹理贴图并保存。

|属性|引用贴图名称|
|:-:|:-:|
|Albedo|base_color_out|
|Normal|normal_out|
|RoughnessMetallicAoEmissive|Baltic_Erangel_road2V_RMA|

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PkMHhimage.png)

打开模型Lod0并挂载材质实例。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/PB2mIimage.png)

最后从属性【LOD导入】中选择“导入LOD层级 X ”，分别导入模型 Lod1 和 Lod2，完成角色模型的配置。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/bOPyPimage.png)

---

### 使用角色模型

以下以替换玩家模型为例，相关代码如下：

``` lua
-- UGCPlayerPawn.lua部分代码

function UGCPlayerPawn:ReceiveBeginPlay()
    UGCPlayerPawn.SuperClass.ReceiveBeginPlay(self)
    -- 设置玩家的LOD模型
    self.timer = Timer.InsertTimer(1, function ()
        UGCPlayerPawnSystem.ChangeAvatarMesh(self, UGCGameSystem.GetUGCResourcesFullPath('Asset/Blueprint/NewFolder/lod0.lod0'),true)
    end)
end
```

最终画面效果如下：

![企业微信截图_17875766392005.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/IisJC%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_17875766392005.png)

---

## AI资源检索

> 文档路径: AI工具 > AI资源检索

> 文档ID: 20292 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20292)

> 新增: 2026-07-10 15:11:31

# AI资源检索

AI检索功能允许开发者通过输入关键词，快速查找相关联的资源，提高资源检索效率。
>当前版本仅支持静态网格类型的内容检索

<br>

## 功能入口

编辑器内容浏览器和【AI开发助手】都内置了AI检索的功能，两种入口的操作方式一致。

**内容浏览器**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/hTAkEimage.png)

**AI开发助手**

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HC1SAimage.png)

<br>

## 操作步骤

以【AI开发助手】为例说明检索功能的使用步骤。

1. 编辑器菜单栏点击打开【AI开发助手】。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/xYowPimage.png)

2. 选择【AI检索】页签。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/fcwnAimage.png)

3. 在输入框中输入检索内容，如：“枪械”，按回车即可出现搜索结果：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/k1E6Qimage.png)

4. 在搜索的同时，下方菜单会出现自动联想的扩展关键词：
>当前搜索暂不支持以单个字母或单个数字作为关键词进行联想

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ckUz3image.png)

点击右侧按钮，可以展开、收起联想菜单：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/zJnQZimage.png)

选择需要的联想内容，按回车即可触发搜索：

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4Io35image.png)

5. 每次搜索都会生成历史，历史保留的数量上限为10，点击历史记录会将关键词填入搜索框，需按回车键确认搜索。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8y6fpimage.png)


## 收藏夹

可以选择需要的资源拖进收藏夹

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ysMjLimage.png)

新建和删除文件夹

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4qQXqimage.png)

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UMxxlimage.png)


## 过滤器

可根据所需的资产类型进行筛选，以便更快找到目标资源

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/kSZwNimage.png)


## 图像识别

选择一张图片作为参考，系统将基于图片内容智能检索相似资产
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/XVFnhimage.png)

---

## 视频生成3D动画

> 文档路径: AI工具 > 视频生成3D动画

> 文档ID: 20207 | [官网原文](https://developer.gp.qq.com/wikieditor/#/catalog/20207)

> 更新: 2025-10-13 15:06:23

# 视频生成3D动画

为了帮助开发者拓展更多玩法内容和提高玩法美术品质，现在编辑器内置AI工具-视频转3D动画。

<br>

## 操作步骤

1. 通过【AI助手】进入AI工具界面选择【AI动作转换】

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KlN1Gimage.png)

点击视频上传，选择符合规范的视频进行上传后，在目标角色处选择需要的骨骼目标（角儿模型仅作示例，不代表真实角色）。

选中目标骨骼后，点击转换，等待5-10mins后，即可生成对应的动作。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/lqGXQimage.png)

2. 点击【下载】按钮会通过外部浏览器下载该动作FBX文件。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3LD4Bimage.png)

3. 将FBX文件拖拽到编辑器工程窗口， 选择对应的骨骼类型，勾选“Import Animations”，点击【导入】按钮即完成动画资源的导入

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2AX0uimage.png)
![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ZKmPaimage.png)

<br>

## 功能使用规范

为了保证功能正常使用且符合转换预期，进行转换前请遵循下述使用规范：

- 视频分辨率应控制在480p-2K内，视频时长应控制在5s-15s内；视频格式需MP4；视频大小不得超过100M
- 视频应保证正常光照，避免出现过暗或过曝，且镜头应尽量保持稳定
- 视频内容需单人，人物四肢需完整出现在视频内，避免被其他物体遮挡，且人物占据画面比例需在60%-80%
- 视频人物应避免全身纯色衣物，长裙，长袍等会遮盖四肢及动作细节的衣物
- 视频镜头需水平拍摄，避免俯拍或仰拍；且要求一镜到底不存在镜头切换和剪辑
- 视频动作应避免恶意非法，色情，不雅的动作

**注意**
> 工具全方面接入安全审核，若上传或转换非法内容，将被拦截；若成功上传且转换出非法内容并使用到工程中，官方有权对玩法进行下架及后续处理

---
