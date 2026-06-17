# 进阶内容/GamePlay系统/怪物系统/AI编辑器1.0/行为树节点使用手册/Decorator

> 本分类共 2 篇文章

---


## 引擎

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 行为树节点使用手册 > Decorator > 引擎

#  引擎

## 逻辑 AND NOT OR

**逻辑节点** 节点使您能够设置比内置节点更高级的逻辑。

---

## Blackboard

**黑板（Blackboard）** 节点将检查给定的 **黑板键（Blackboard Key）** 上是否设置了值。

| Notify Observer | 描述 |
| :--- | :---: |
| **On Result Change** | 仅在条件改变时进行重新计算 |
| **On Value Change** | 仅在观察到的黑板键改变时进行重新计算 |

| 观察者终止 | 描述 |
| :--- | :---: |
| **None** | 不中止执行 |
| **Self** | 中止此节点自身和在其下运行的所有子树 |
| **Lower Priority** | 中止此节点右侧的所有节点 |
| **Both** | 中止此节点自身和在其下运行的所有子树，以及此节点右侧的所有节点 |

---

## Check Gameplay Tag Condition

**检查Gameplay标签条件（Check Gameplay Tag Condition）** 节点将检查给定的Actor上是否匹配 **Gameplay标签（Gameplay Tags）**。

---

## Compare BBEntries

**比较黑板条目（Compare BBEntries）** 节点将比较两个 **黑板键** 的值，并根据结果（等于或不等）阻止或允许节点的执行。

---

## Conditional Loop

只要满足了 **键查询（Key Query）** 条件，该装饰器将使它所连接节点进行循环。

---

## Cone Check

**椎体检查（Cone Check）** 装饰器采用了三个矢量键：第一个确定椎体的起始位置，第二个用于定义锥体朝向的方向，第三个用于检查该位置是否在锥体内部。您可以使用 **锥体半角（Cone Half Angle）** 属性来定义锥体的角度。

---

## Cooldown

**冷却（Cooldown）** 将锁定节点或分支的执行，直到冷却时间结束。

---

## Does Path Exist

**路径是否存在（Does Path Exist）** 节点会检查是否可以在以下两个矢量之间创建路径：黑板键A（Blackboard Key A）和黑板键B（Blackboard Key B）

| Path Query Type | 描述 |
| :--- | :---: |
| **NavMesh Raycast 2D** | 寻路网格体光线投射2D |
| **Hierarchical Query** | 分层查询 |
| **Regular Path Finding** | 常规通道搜寻 |

---

## Force Success

**强制成功（Force Success）** 装饰器会将节点结果更改为成功。

---

## Is At Location

**在位置处（Is At Location）** 装饰器节点将检查AI控制的Pawn是否位于给定位置。

---

## Is BBEntry Of Class

**Is BBEntry Of Class** 装饰器节点用于确定所指定的黑板键是否属于指定的类。

---

## Keep in Cone

**保持于椎体内（Keep in Cone）** 装饰器节点会根据所观察到的位置是否仍位于锥体内部来确定其条件。当节点首次拥有相关性时，将计算锥体的方向。

---

## Loop

**循环（Loop）** 装饰器会对节点或分支进行多次循环或无限次循环。

---

## Set Tag Cooldown

通过 **设置标签冷却（Set Tag Cooldown）** 可以设置Gameplay标签的冷却时长。

---

## Tag Cooldown

一个装饰器节点，其条件基于Gameplay标签的冷却计时器是否过期。

---

## Time Limit

**时间限制（Time Limit）** 装饰器会为一个分支或节点设置在终止其运行并失败前，完成运行所需的一段时间。每当该节点被聚焦时，计时器都会重置。

---



---


## 和平

> 文档路径: 进阶内容 > GamePlay系统 > 怪物系统 > AI编辑器1.0 > 行为树节点使用手册 > Decorator > 和平

#  和平

# 通用

## 概率（UGC_Probability）

随机概率判断正确错误

## 朝向夹角判断（UGC_AngleCheck）

可以当前行为树相关信息到日志中

## 距离判断（UGC_DistanceCheck）

可以当前行为树相关信息到日志中

---

# 角色

## 是否有BUFF（UGC_IsHasBuff）

可以当前行为树相关信息到日志中

---

# 主角

## 属性监视（UGC_AttrObserver）

监视主角自身的属性



---
