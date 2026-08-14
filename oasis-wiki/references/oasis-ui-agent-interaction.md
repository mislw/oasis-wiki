# Oasis UI Agent 交互编排

本参考只规定 Agent 如何围绕现有 Cowart/UI Workflow 与用户交互，不改变任何生产功能。

```text
INTERACTION_ONLY_NO_RUNTIME_CHANGE
```

## 能力边界

继续使用现有 Game UI Design System、图片生成、Layer Reconstruction、Workbench、MCP、WidgetBlueprint、Lua 和 PIE 流程。不要新增或假装已经存在：

- 持久化 UI Task 状态机；
- `current_ui_task` 或跨重启 pending decision；
- 新的 IPC、WebSocket、HTTP、文件监听或命令桥；
- Companion 当前任务面板、待验收徽标或自动打开当前任务；
- 自动跨越现有授权门禁的后台执行。

当前 Workflow Console 的 `console-state.json` 只证明单次工作目录状态；它不是通用 Agent Task Store。Companion 可以显示 Agent、MCP 和 Skill 状态，但在运行时代码真正支持以前，Agent 不得声称 Companion 已同步当前 UI 阶段。

如果没有持久化状态，恢复任务时应读取当前对话、实际产物、工作目录和编辑器状态进行只读重发现。无法确认时说明可能过期，并询问一个最关键的问题，不得假装自动恢复成功。

## 交互总协议

每个用户可理解的生产阶段遵循：

```text
Agent 读取与推断
-> 只询问真正缺失的信息
-> 用户确认关键决策
-> 执行一个阶段
-> 报告真实结果和绝对路径
-> 等待用户验收
-> 再进入下一阶段
```

固定规则：

1. 一次只处理一个最重要的待决策问题。
2. 能从项目、UI Tree、Lua、配置或已有产物读取到的内容不重复询问。
3. 一个阶段内部的低风险脚本动作可以连续执行，不要每一步都打断用户。
4. 视觉版本锁定、Layer Freeze、UMG 写入、Lua 逻辑写入和最终验收必须停住等待明确确认。
5. 用户未确认时不跨阶段；用户要求修改时保持当前阶段，修改、重验、再次等待确认。
6. 报告产物时使用实际绝对路径。没有路径就明确说未生成，不从聊天历史猜测。
7. 不把聊天中的“可以”脱离当前阶段解释，也不把修改请求当成批准。

## 对话阶段

这些名称是交互标签，不是新的运行时状态模型：

```text
SOURCE
VISUAL
LAYERING
WORKBENCH_REVIEW
UMG_REQUIREMENTS
UMG_BUILD
LOGIC_BINDING
FINAL_REVIEW
COMPLETE
```

不要把内部十几个脚本步骤全部暴露为阶段。阶段代表用户能理解和验收的生产结果。

## SOURCE

开始新 UI 时自然询问来源，不要求用户填写固定表格：

```text
准备开始这个 UI。

这次你是：
- 还没有 UI，需要我先生成
- 已经有 UI 图，直接使用
- 继续之前做到一半的 UI

直接用自然语言告诉我就行。
```

用户说“我已经有图了”“先帮我生成”“继续之前那个页面”时，按语义进入对应分支。

## VISUAL

如果需要生成，Agent 先读取项目 Design System、可复用控件、Style/Layout Reference 和 UI Tree，再只问缺失信息：

```text
我准备制作“<页面名称>”。

我会默认：
- 使用当前项目已有 UI 风格
- 优先复用现有 Panel、Button 和 Tab
- 动态文字、数值、进度和点击区保留为 Native

目前只需要确认：<真正缺失的一个问题>
```

图片生成后必须停住：

```text
UI 效果图已经生成。

图片：<absolute path>
版本：<version>
尺寸：<width> x <height>

请确认是否使用这张图进入正式分层。
你可以说：用这版 / 再生成一版 / 指定位置修改。
```

如果用户直接提供图片：

```text
已经收到 UI。

项目：<project>
尺寸：<width> x <height>

我准备执行：
UI Tree 推断 -> 控件分类 -> 分层重建 -> 工作台预览

是否开始？
```

没有视觉确认，不进入正式分层。`visual approval` 只批准当前图片版本进入 Layering，不批准后续 UMG 或 Lua 写入。

## LAYERING

控件识别、UI Tree inference、节点分类、Layer Reconstruction、Assembly Preview 和 Workbench package 可以作为一个阶段连续执行。只有失败或高风险歧义时暂停：

```text
发现 <count> 个控件无法确定父级：

<child> -> 建议归属 <parent>

是否按这个层级继续？
```

完成后必须报告真实统计和路径：

```text
UI 分层完成。

识别节点：<count>
Native：<count>
Skin：<count>
Artwork：<count>
Composite：<count>
Clean Layer：<count>
需要人工确认：<count>

UI 工作台：<absolute path or URL>
切图目录：<absolute path>
UI Tree：<absolute path>
Assembly Preview：<absolute path>
```

能力不可用时使用现有失败码，例如 `IMAGE_GENERATION_UNAVAILABLE` 或 `LAYER_RECONSTRUCTION_UNAVAILABLE`，说明已完成什么、缺少什么以及用户下一步能做什么。

## WORKBENCH_REVIEW

分层完成后必须停在工作台验收，不因脚本成功而自动进入 MCP：

```text
分层与 Assembly Preview 已完成。

请在 UI 工作台检查：
- 控件范围与父子归属
- Z-order 和遮挡
- clean layer 是否有子控件残影
- Native / Skin / Artwork / Composite 分类
- 移动 child 后原位置是否干净
- 移动 parent 后是否露出 clean background

工作台：<absolute path or URL>
Assembly Preview：<absolute path>

检查完成后可以说“切图确认”；发现问题就直接描述要改的位置。
```

没有当前阶段的 layer approval 时，任何 MCP 写入都必须停止并报告：

```text
USER_APPROVAL_REQUIRED
当前需要：确认工作台分层结果
尚未执行：WidgetBlueprint 写入
```

工作台修改 `bounds`、`parent`、`ZOrder`、节点分类、clean layer、拆分或合并以后，旧的 layer approval 立即失效。重新验证并再次等待用户确认。不要声称工作台会自动回传这些变化；没有运行时桥接时，应重新读取实际 manifest、文件时间和工作台产物。

## UMG_REQUIREMENTS

用户确认分层后，先读取真实 UI Tree、项目中已工作的 WidgetTree、Lua、UIManager、配置和 RPC，再生成交互需求草案。不得直接创建 WidgetBlueprint。

```text
我准备把“<页面名称>”制作成 WidgetBlueprint。

根据当前 UI Tree 和项目代码，我判断：
- <按钮> -> <推断的点击行为>
- <文本/数值> -> <推断的数据来源与刷新时机>
- <状态控件> -> <normal/selected/disabled/locked 等状态>

目前只需要确认：<无法从项目推断的一个问题>
```

优先确认真实点击控件、动态字段、状态变化、动画反馈、数据来源和本次交付范围。一次只问一个会改变实现计划的问题；不要让用户重新填写项目中已经存在的信息。

需求足够后，先报告 UMG 实施计划并等待批准：

```text
UMG 实施计划已整理。

目标资产：<absolute asset path>
参考 WidgetTree：<asset path>
语义父容器：<planned groups>
Native 控件：<planned widgets>
图片资源：<planned clean layers/artwork>
交互范围：<visual only/buttons/data binding/full integration>
验证：坐标、Z-order、按钮身份、资源引用、保存后回读

确认后我才会通过 MCP 写入 WidgetBlueprint。是否按这个计划执行？
```

这里的批准只授权当前 UMG 计划，不自动授权 Lua、DataTable 或其他资产修改。计划或上游分层发生变化时，本批准失效。

## UMG_BUILD

收到当前计划的明确批准后，继续遵守现有 MCP、PRV、事务、备份和 Git 安全规则。完成后报告真实写入与独立回读结果：

```text
WidgetBlueprint 构建完成。

资产：<asset path>
创建/复用控件：<summary>
图片绑定：<summary>
按钮身份：<summary>
保存后回读：<pass/fail>
坐标保持：POSITION_PRESERVATION=PASS|FAIL
编辑器视觉检查：<verified/not verified>

请先在编辑器中检查布局、图片、文字、层级和按钮区域。
确认 Widget 视觉结果后，我再进入 Lua / 交互绑定。
```

属性已保存或 MCP 返回成功，不等于视觉验收通过。没有真实编辑器渲染证据时写 `not verified`，不得猜测。

## LOGIC_BINDING

Widget 视觉验收通过后，先说明将复用的现有入口、事件、RPC、配置和刷新函数，再单独请求 Lua / 数据绑定授权：

```text
交互绑定计划：

- <ButtonName> -> <existing handler/event/RPC>
- <TextName> -> <existing data source and refresh function>
- 页面打开/关闭 -> <existing UIManager flow>
- 状态刷新 -> <existing event or callback>

计划修改：<absolute paths>
保持不变：<existing gameplay/RPC/save/config behavior>

是否授权执行这次 Lua / 数据绑定修改？
```

只有当前逻辑计划获得明确批准后才能写代码或数据。完成后报告修改文件、绑定链、静态检查，以及仍需 PIE 验证的项目。

## FINAL_REVIEW

最终验收报告必须分开陈述已经验证和仍未验证的内容：

```text
UI 已进入最终验收。

视觉：<pass/fail/not verified>
分层残影：child=<pass/fail> parent=<pass/fail>
UMG 结构与坐标：<pass/fail>
按钮绑定：<pass/fail/not verified>
动态数据刷新：<pass/fail/not verified>
PIE：<pass/fail/not run>
Git/Skill 沉淀：<done/not requested>

产物：
- Visual：<absolute path>
- UI Tree：<absolute path>
- Workbench：<absolute path>
- WidgetBlueprint：<asset path>
- Lua：<absolute paths>

请确认是否完成本次 UI。
```

只有用户确认最终结果后才使用 `COMPLETE`。测试未运行、编辑器不可见或 PIE 未执行时必须直说。

## Approval Interpretation

Approval 必须同时满足：

1. 有明确的当前阶段和当前待决策；
2. 用户回复在语义上表示接受该结果或计划；
3. 自请求确认后，相关上游产物没有发生变化。

“可以”“确认”“用这版”“切图确认”“UMG 没问题”可以按当前上下文批准对应阶段，但不能跨阶段复用。每次只允许 `one pending decision`。如果同时存在两个关键问题，先解决影响更大的一个。

下列内容不是批准：

- “按钮往右一点”等修改请求；
- “继续看看”“先检查一下”等调查请求；
- 对旧版本的确认；
- 无法确定指向哪个阶段的“可以”。

发生修改时保持当前阶段：执行修改 -> 重新验证 -> 报告新版本/新路径 -> 再次等待确认。Visual 改动会使下游 UI Tree、Layer、Assembly 和 UMG Plan 过期；Layer/Workbench 改动会使 layer approval 与 UMG Plan approval 失效；UMG 结构改动会使 Widget 视觉批准和 Logic Plan 失效。

## Backtracking

用户可以要求返回上一阶段、重新生成、重新分层或重新整理需求。Agent 先说明哪些下游产物会变为 stale，再执行当前已授权范围内的动作。

如果已经写入真实 `.uasset`、`.umap`、Lua 或 DataTable，不得用“回到上一阶段”暗示自动回滚。必须遵守现有快照、事务、备份与 Git 安全流程，并对实际回滚另行取得授权。

## Blocked And Failed

缺少用户决策时：

```text
WAITING_USER
当前阶段：<stage>
已完成：<verified result>
等待确认：<one decision>
未执行：<gated action>
```

能力或外部条件不满足时：

```text
BLOCKED
当前阶段：<stage>
原因：<specific capability/editor/input problem>
已保留：<real artifacts>
下一步：<one actionable recovery>
```

真正执行失败时：

```text
FAILED
当前阶段：<stage>
失败动作：<operation>
错误：<exact error or failure code>
资产状态：<saved/rolled back/unknown>
验证：<read-back result>
```

`waiting_user` 不是失败。MCP timeout 也不自动等于写入失败，必须先回读真实资产状态。

## Standard Stage Response

阶段性回复优先使用这个紧凑结构，不要求每次显示内部状态 JSON：

```text
当前阶段：<conversational stage>
已完成：<verified result>
产物：<absolute paths or asset paths>
验证：<pass/fail/not run>
等待你确认：<one pending decision>
确认后执行：<next gated action>
```

这是对话协议，不是持久化承诺。`do not claim persisted task state`：在真正增加并验证任务存储、通信桥和 Companion UI 前，不得声称重启后会自动恢复、自动显示当前任务或自动打开当前 Workbench。
