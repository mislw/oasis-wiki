# AI工具

> 本分类共 2 篇文章

---


## 视频生成3D动画

> 文档路径: AI工具 > 视频生成3D动画

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


## AI生成图片

> 文档路径: AI工具 > AI生成图片

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
