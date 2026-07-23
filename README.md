# Oasis Wiki Codex Skill

这是一个给 **绿洲启元 / 绿洲起源 / 和平精英 UGC Lua 开发** 使用的 Codex Skill / AI Agent 知识包。

它会让 Codex 或其他 AI Agent 在处理 UGC Lua、RPC、UI、复制、日志、编辑器流程、项目结构、功能开发、配置表和 MCP 自动化问题时，优先搜索本地官方 wiki、官方 API 手册、1.37 增量内容、官方论坛经验帖和项目规则，而不是凭记忆猜。

## 适合什么场景

- 接手或解析一个 UGC 项目。
- 开发功能，例如按钮、奖励、升级、属性、抽奖、关卡、商店、技能、任务、存档、重连。
- 排查报错，例如按钮没反应、RPC 没触发、UI 白色、DataTable 只读报错、资源加载失败、日志异常。
- 查询配置表、数值表、DataTable、UAEDataTable、奖励表、属性表。
- 使用 UGCAskQ MCP 操作编辑器、生成 Widget 蓝图、查看 UI、查表。
- 当 Codex 直连 MCP 因 Responses tool streaming 兼容问题断流时，通过本地长连接 HTTP 代理继续使用 UGCAskQ 读写编辑器。
- 在多个 Codex 对话里持续开发同一个项目，复用本地项目索引和功能记忆。

## 安装到 Codex

把仓库里的 `oasis-wiki` 文件夹复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

然后重启 Codex，或刷新 skills。

## 更新本地安装

```powershell
git pull
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

## 触发方式

一般情况下，只要问题和下面内容相关，Codex 就应该自动使用这个 skill：

- `UGCProjects`
- `绿洲启元` / `绿洲起源` / `和平精英UGC`
- `UGCGameMode` / `UGCGameState` / `UGCPlayerController` / `UGCPlayerState` / `UGCPlayerPawn`
- `UIManager` / `EventDefine` / `GlobalConfig`
- `UnrealNetwork` / `GetAvailableServerRPCs` / `CallUnrealRPC`
- `DSlog` / `Clientlog` / `PIE日志`
- `MCP` / `UGCAskQ` / `.mcp.json`

也可以显式写：

```text
用 oasis-wiki 看一下这个 UGC 功能怎么接。
用 oasis-wiki 帮我查这个报错。
用 oasis-wiki 走教学模式讲一下这个 RPC 流程。
```

## 任务分类

Skill 现在先按任务意图分类，再读对应 reference，避免每次加载太多无关内容。

主要分类在 `oasis-wiki/references/task-router.md`：

- **项目解析**：接手项目、读项目结构、策划案对应工程、生命周期、核心系统。
- **功能开发**：配置 -> 服务端权威逻辑 -> RPC -> UI -> 刷新 -> 复制/存档 -> 重连 -> GM/日志验证。
- **报错处理**：日志优先，定位最小断点，例如 UI 构建失败、RPC 未注册、DataTable 只读、资产路径错误。
- **MCP 操作**：连接 UGCAskQ MCP、读工具清单、做 PRV 计划、执行和验证。
- **配置表/数值**：查表、解释字段、追踪代码消费链路、处理权重/奖励/属性。
- **UI/交互**：MainUI 入口、UIManager 注册、Widget 控件命名、按钮绑定、刷新链路。
- **项目保护**：二进制资产、`.uasset` / `.umap` 脏文件、备份、队友代码保护。

默认一次任务只选一个主分支，最多再选一个辅助分支。

## 常规模式和教学模式

默认是 **常规模式**：回答直接、简洁、方便 review。

常规模式通常会给：

```text
结论
依据
改哪里
最小改动
影响范围
风险
怎么测
回滚点
```

只有当用户明确说下面这些词时，才进入 **教学模式**：

```text
教学模式
详细讲
教我
一步一步
拆一下
从底层讲
```

教学模式是强制只读模式：

- 可以读项目文件、日志、配置、资源路径和 wiki。
- 不允许直接修改 UGC 项目代码、资产或配置。
- 即使用户在教学模式里说“你直接改”，也要先让用户切回常规/直接执行模式。
- 每个代码改动都必须说明文件路径、行号、函数/表名。
- 如果精确行号无法确定，必须先查文件；仍不能确定时给最近的稳定锚点并说明原因。

## 多对话项目开发

为了避免每次新开对话都重新扫完整项目，这个 skill 支持本地项目索引和功能记忆。

项目缓存位置：

```text
%USERPROFILE%\.codex\oasis-project-cache\<project-name>-<path-hash>\
```

缓存不会写进 UGC 项目目录，也不应该提交到 GitHub。

建立或刷新项目索引：

```powershell
powershell -ExecutionPolicy Bypass -File ".\oasis-wiki\scripts\index-oasis-project.ps1" -ProjectRoot "<UGC project root>" -Force
```

新对话可以这样提示：

```text
这是 RedCliff 项目，先按 oasis-wiki 走。
先读本地项目缓存，不要重新全项目扫描。
我要继续做/排查：<功能名>
```

功能完成后，如果希望后续对话复用这次功能背景，可以说：

```text
记住这个功能
```

然后 agent 应该调用：

```powershell
powershell -ExecutionPolicy Bypass -File ".\oasis-wiki\scripts\remember-oasis-feature.ps1" -ProjectRoot "<UGC project root>" -Title "<feature title>" -Summary "<short summary>"
```

## MCP / UGCAskQ

如果 Codex 直连 UGCAskQ MCP 出现 `stream disconnected before completion: stream closed before response.completed`，优先使用本仓库提供的本地长连接 HTTP 代理，而不是反复重试 native MCP 注册。

默认文件：

```text
oasis-wiki/scripts/ugcaskq-proxy-server.js
oasis-wiki/scripts/ugcaskq-cli.js
```

启动代理：

```powershell
$node = "C:\Users\ASUS\.workbuddy\binaries\node\versions\22.22.2\node.exe"
& $node ".\oasis-wiki\scripts\ugcaskq-proxy-server.js"
```

默认代理地址是 `http://127.0.0.1:18763`，上游编辑器 SSE 地址是 `http://127.0.0.1:12463/sse`。常用接口：

```text
GET  /health
GET  /tools
GET  /read?uri=ctx:
POST /call
POST /py
POST /plan
```

这个代理不是新的 MCP Server，而是长期连接编辑器 UGCAskQ MCP，再把 `ue_read`、`ue_py`、`ue_plan_submit` 等工具转成普通 HTTP 调用，方便 Codex 或其他本地工具绕过 Responses tool streaming 兼容问题。

MCP 相关规则分为三层：

- `references/mcp-integration.md`：连接、`.mcp.json`、SSE、工具发现、PRV、备份、安全和证据规则。
- `references/mcp-ui-widget.md`：查看或生成 WidgetBlueprint / UMG / UI 层级、布局、颜色、按钮交互。
- `references/mcp-datatable.md`：查 DataTable / UAEDataTable、低 token 读表、只读 fallback、表行修改规则。

常见触发：

```text
用 MCP 帮我生成这个 UI。
用 MCP 查一下这个配置表。
补一下 Widget 蓝图。
这个 UI 怎么都是白色的？
AssetRegistry.GetAssetByObjectPath failed。
```

注意：

- UI 和表格是两个分支，不要无脑两个都读。
- Widget 样式不要只靠 `widget_set_property`，需要用可靠函数写颜色并验证。
- DataTable / UAEDataTable 行对象默认视为只读。运行时代码要复制成普通 Lua table 后再改派生值。
- 二进制资产备份要放在 UGC 项目目录外，避免编辑器扫描备份资产。

## 代码风格

写或审 UGC Lua 前读 `references/code-style.md`。

核心规则：

- 新配置表字段要有中文注释。
- 新成员变量、`GlobalConfig` 变量、方法要有中文注释。
- 变量名尽量写完整英文，保留常见缩写如 `ID` / `UI`。
- 简单变量用轻量前缀，如 `nLevel`、`szName`、`tbItemList`。
- 保留旧代码命名、顺序、RPC 名、事件 ID、存档 key，不为了规范强行重命名。
- 不要堆无意义的 `nil` / `UE.IsValid` 防御检查，只在真实边界做保护。

## 常用问法

```text
帮我解析一下这个 UGC 项目的主流程。
帮我做一个点击按钮升级的功能，按现有项目结构来。
这个按钮点了没反应，帮我看日志和 RPC 链路。
用 MCP 查一下 GemFeature 表。
教学模式，带我一步一步看这个 UI -> ServerRPC -> 刷新流程。
正常模式，直接给最小改动和怎么测。
```

## 仓库内容

- `AGENTS.md`：给通用 AI coding agent 的仓库级说明。
- `AGENT_PROMPT.md`：给不支持自动读取 skill 的 agent 使用的复制版提示词。
- `oasis-wiki/SKILL.md`：Codex skill 入口和触发说明。
- `oasis-wiki/AGENTS.md`：放在 skill 内部的通用 agent 说明。
- `oasis-wiki/agents/openai.yaml`：Codex UI 元数据。
- `oasis-wiki/references/wiki`：本地官方 wiki markdown 导出。
- `oasis-wiki/references/task-router.md`：任务意图分类路由。
- `oasis-wiki/references/answer-modes.md`：常规模式 / 教学模式规则。
- `oasis-wiki/references/teaching-mode.md`：教学模式细则和强制只读规则。
- `oasis-wiki/references/feature-development-flow.md`：功能开发主流程。
- `oasis-wiki/references/code-style.md`：Lua 代码风格。
- `oasis-wiki/references/mcp-integration.md`：MCP 通用连接、长连接 HTTP 代理和安全规则。
- `oasis-wiki/references/mcp-ui-widget.md`：MCP UI / Widget 工作流。
- `oasis-wiki/references/mcp-datatable.md`：MCP 配置表 / DataTable 工作流。
- `oasis-wiki/references/project-cache.md`：本地项目索引工作流。
- `oasis-wiki/references/project-planning-memory.md`：项目规划记忆工作流。
- `oasis-wiki/references/pitfalls.md`：常见坑和验证提醒。
- `oasis-wiki/references/recipes.md`：常见实现配方。
- `oasis-wiki/references/snippets.md`：常用 Lua 模板片段。
- `oasis-wiki/references/skill-evolution.md`：如何判断是否更新 skill。
- `oasis-wiki/scripts`：搜索、项目索引、功能记忆、UGCAskQ MCP 长连接代理脚本。

## 注意事项

- 不要把 `%USERPROFILE%\.codex\oasis-project-cache` 提交到 GitHub。
- 不要把私有项目策划案、Excel、截图原件、完整源码复制进这个公开 skill 仓库。
- 项目缓存只放本机；通用经验才沉淀回这个仓库。
- UGC 项目源文件是最终事实来源。缓存和规划记忆只用来缩小搜索范围。

---

## English Overview

This repository packages a portable AI-agent knowledge bundle for Oasis / Peace Elite UGC Lua development.

It is Codex-native through `oasis-wiki/SKILL.md`, and also includes generic instructions for other AI coding agents through `AGENTS.md` and `AGENT_PROMPT.md`.

The skill bundles a local Markdown export of the Oasis wiki, official API reference, 1.37 updates, official forum tutorials, and distilled workflow references. It is designed to help agents search official/local references before answering questions about Lua APIs, gameplay systems, UI, editor workflows, MCP/UGCAskQ, debugging, logs, performance, project analysis, and feature development.

Project-specific caches and planning notes should stay outside this public repository, under `%USERPROFILE%\.codex\oasis-project-cache`.
