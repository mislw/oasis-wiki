# 进阶内容/GamePlay系统

> 本分类共 1 篇文章

---


## Gameplay标签

> 文档路径: 进阶内容 > GamePlay系统 > Gameplay标签

**涉及API:** `Comment`, `Delete`, `EqualsTag`, `GameplayTags`, `HasTag`, `MatchesTag`, `Name`, `NewTest`, `UGCGameplayTagSystem`

# Gameplay标签

GameplayTag是具备分层含义的标签功能，通过“.”分隔的一串多层级标识符来表达游戏中的具体概念，开发者可以创建任意数量的标签用于对资源、状态、物品等对象进行分类和标记，这种轻量、灵活的方式可以应用在 [技能编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20091)、[Buff编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20087) 或者 [物品编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20101) 等各种系统功能中。

<br>

## GameplayTag概述

GameplayTag通过树状结构的字符串来表达层级关系，顶层的标识符代表某类概念，而层级之间的关系可以理解为对此概念的逐级具象化，层级越深概念越具体，例如 ``Item.Consumable`` 代表消耗类的物品，而 ``Item.Consumable.Drink`` 则代表消耗类物品下的饮料物品。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/irUlBimage.png)

GameplayTag对层级数量没有限制，开发者可根据需要灵活定义分层结构，但需要确保各标签名唯一。系统预置了一批标签，用于 ```物品```、```技能```、```玩家状态``` 等场景下的分类或标记信息，开发者可直接使用，但不可删除或编辑修改。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/mpGqHimage.png)

<br>

## 编辑GameplayTag

点击编辑器菜单栏 ```编辑 -> 工程设置``` ，在工程设置界面左侧选择 ```GameplayTags``` ，进入标签配置界面。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/ihj72image.png)

### 添加标签

**创建顶层标签**

点击展开 ```Add New Gameplay Tag``` 下拉项，在 ```Name``` 与 ```Comment``` 输入框内填入标签信息，点击```Add New Tag```按钮，即可成功添加一个顶层标签。
- Name：标签名，不支持单/双引号、换行符、制表符和空格
- Comment：标签注释

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/Fxiarimage.png)

---

**添加子级标签**

选择要添加子级标签的顶层标签名，点击其右侧 ```+``` ，系统会在 ```Add New Gameplay Tag``` 配置处自动填充顶层标签信息，在顶层标签名后添加一级标签名，用“.”分隔，填写规范与顶层标签一致。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UNmaPimage.png)

以 ```NewTest``` 添加子标签为例，点击```+```后，系统自动于 ```Name``` 处填充了顶层标签 ```NewTest.```，开发者在“.”后填写子标签名称，点击 ```Add New Tag``` 即可成功添加子标签。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/iWHnJimage.png)

---

### 删除标签

选中要删除的标签，点击右侧三角下拉框，选择 ```Delete``` 按钮即可删除标签。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/UV8Pjimage.png)

删除标签前需要确保该标签没有被其他系统功能的蓝图配置所引用，否则会提示无法删除。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/gDfc0image.png)

**注意：**
> 系统预置的标签不可删除

<br>

## 使用GameplayTag

### 引用标签

一些系统功能涉及标签的引用配置，例如 [Buff编辑器](https://developer.gp.qq.com/wikieditor/#/catalog/20087?autoJump=%E7%8A%B6%E6%80%81%E4%BA%92%E6%96%A5) 可以通过 ```Tag``` 过滤施放的对象或根据角色状态决定是否可获得Buff。

![image.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/J2N5eimage.png)

---

### 脚本中访问标签

[``UGCGameplayTagSystem``](https://developer.gp.qq.com/api/#/searchContent/UGCGameplayTagSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGameplayTagSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGameplayTagSystem) 库提供了校验标签相关的API，开发者可以在脚本中调用API以实现特定的玩法逻辑。

<br>

## GameplayTag匹配

GameplayTag系统支持基于层级结构的Tag匹配，目前提供了三种匹配方式：[``MatchesTag``](https://developer.gp.qq.com/api/#/searchContent/UGCGameplayTagSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGameplayTagSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGameplayTagSystem&autoJump=MatchesTag)、[``EqualsTag``](https://developer.gp.qq.com/api/#/searchContent/UGCGameplayTagSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGameplayTagSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGameplayTagSystem&autoJump=EqualsTag) 和 [``HasTag``](https://developer.gp.qq.com/api/#/searchContent/UGCGameplayTagSystem?classDetailShow=true&path=class%2Fdetail%2F%E5%92%8C%E5%B9%B3%E5%85%A8%E5%B1%80%E6%8E%A5%E5%8F%A3%2F%E5%B7%A5%E5%85%B7%E5%BA%93%2FUGCGameplayTagSystem.json&isSelect=1&apiEnc=%5B%22%E7%B1%BB%22%5D&apiLabel=UGCGameplayTagSystem&autoJump=HasTag)。

**MatchesTag**

`MatchesTag` 判断两个标签是否匹配，具体规则如下：
- 精确匹配：两个标签完全相同（如 `A.Test` 与 `A.Test`），则返回True
- 模糊匹配：
	- 左值标签最长前缀匹配：`A.Test` 会匹配 `A`
	- 右值标签最长前缀匹配：`A` 与 `A.Test` 不匹配

| **Source**     | **Function**    | **Target** | **Return Value** |
|----------------|-----------------|---------------------|------------------|
| A              | MatchesTag      | A                   | true             |
| A              | MatchesTag      | A.Test              | false            |
| A.Test         | MatchesTag      | A                   | true             |
| A.Test         | MatchesTag      | A.Test              | true             |
| A.Test         | MatchesTag      | B                   | false            |
| B              | MatchesTag      | A.Test              | false            |
| A.Test         | MatchesTag      | A.Other             | false            |

---

**EqualsTag**

`EqualsTag` 用于比较两个标签是否完全相同，效果等同于 ``MatchesTag``。

| **Source**     | **Function**    | **Target** | **Return Value** |
|----------------|-----------------|---------------------|------------------|
| A              | EqualsTag       | A                   | true             |
| A              | EqualsTag       | A.Test              | false            |
| A.Test         | EqualsTag       | A                   | false            |
| A.Test         | EqualsTag       | A.Test              | true             |
| A.Test         | EqualsTag       | B                   | false            |
| B              | EqualsTag       | A.Test              | false            |

---

**HasTag**

`HasTag` 检查一个标签集中是否包含某个特定标签。

| **Source**     | **Function**    | **Target** | **Return Value** |
|----------------|-----------------|---------------------|------------------|
| {A, A.Test}    | HasTag          | A                   | true             |
| {A, A.Test}    | HasTag          | A.Test              | true             |
| {A, A.Test}    | HasTag          | A.Other             | false            |
| {A}            | HasTag          | A.Test              | false            |
| {A, B}         | HasTag          | A.Test              | false            |
| {A, B}         | HasTag          | B                   | true             |

---
