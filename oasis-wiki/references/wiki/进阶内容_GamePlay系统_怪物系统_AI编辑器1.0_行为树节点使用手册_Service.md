# 进阶内容/GamePlay系统/怪物系统/AI编辑器1.0/行为树节点使用手册/Service

> 本分类共 2 篇文章

---


## 引擎

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 行为树节点使用手册 > Service > 引擎

#  引擎

## Default Focus

**默认聚焦(Default Focus）** 通过设置控制器的聚焦来创建访问代码中Actor的快捷方式。将AI控制器的聚焦设置到Actor上后，您便能直接从AI控制器对其进行访问，而不需要访问黑板键。

---

## Run EQS

**运行EQS（Run EQS）** 服务节点可用于以指定的时间间隔定期执行场景查询系统（EQS）模板，并可对指定的黑板键进行更新。

| Run Mode | 描述 |
| :--- | :---: |
| **SingleResult** | 选择得分最高的第一个项目 |
| **RandomBest5Pct** | 从得分在总分95% 至 100% 的项目中随机选择 |
| **RandomBest25Pct** | 从得分在总分75% 至 100% 的项目中随机选择 |
| **AllMatching** | 获取所有符合条件的项目 |



---


## 和平

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 行为树节点使用手册 > Service > 和平

#  和平

# 通用

## 打印日志（UGC_OutputLog）

可以当前行为树相关信息到日志中

## SEQ

可以使用该节点组合多个Service节点

## 盯着（UGC_Focus）

可以使用该节点获得目标对象

---

# 角色

## 寻敌（UCG_ChooseEnemy）

搜索敌人

---

# 怪物

## 怪物强制更新旋转（UGC_MonsterForceUpdateRotation）

强制更新怪物的旋转



---
