# Oasis Wiki Codex Skill

这是一个给 **绿洲启元 / 绿洲起源 / 和平精英 UGC Lua 开发** 用的 Codex Skill / AI Agent 知识包。

这个仓库主要面向国内小团队自用：默认使用中文语境，默认教学模式，回答会更偏步骤、原因和整体流程；只有明确要求“正常模式 / 简短点 / 直接说 / 给我代码 / 方便 review”时才切换到简洁正常模式。

它会让 Codex 或其他 AI Agent 在回答 UGC Lua、RPC、UI、复制、日志、编辑器流程、项目结构、功能规划等问题前，优先搜索官方 wiki 教学文档、官方 API 手册、1.37 增量内容、官方论坛经验帖和整理过的参考资料，而不是凭记忆猜。

## 中文快速说明

### 这个仓库解决什么

- 把绿洲启元相关官方 wiki 教学文档、Lua API、代码例子、术语、日志说明、官方论坛经验帖打包成一个本地知识包。
- 帮 AI 在回答前先查资料，减少胡编 API、乱改项目、漏注册 RPC、漏复制字段这类问题。
- 问功能、API、系统、模板、编辑器能力时，先查官方文档包：基础官方 wiki 教学文档、`官方API参考手册.md`、`新增内容_1.37版本.md`、`论坛经验帖_绿洲启妹.md`。
- 默认让 AI **只读项目文件并给修改建议**，不直接改 UGC 工程，除非你明确说可以直接改。
- 支持本机项目缓存和策划案记忆：项目级资料会放到 `%USERPROFILE%\.codex\oasis-project-cache`，不会写进 UGC 项目目录，也不会提交到团队仓库。

### 默认回答习惯

- 默认教学模式：先讲已有基础、资料依据、整体流程，再分步骤说明怎么接。
- 正常模式只在明确要求时使用：`正常模式`、`简短点`、`直接说`、`给我代码`、`方便 review`。
- 正常模式代码注释不要太密：只在函数/方法或大逻辑块前加一句中文概括，不逐行写教学注释。
- 做功能前先总结项目已有基础：已有配置、属性、RPC、事件、UI、存档、复制字段、helper、前辈已有代码，再规划整体怎么接。
- 代码习惯：尊重旧命名；新配置/成员变量/方法要有中文注释；不要加一堆无意义保护判断。

### 安装到 Codex

把 `oasis-wiki` 文件夹复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

然后重启 Codex 或刷新 skills。

### 安装到 Claude Code（VS Code 插件）

Claude Code 的 VS Code 插件也可以读取用户级 skill。安装后不需要在 UGC 项目根目录额外放 `CLAUDE.md`，后续打开 UGC 项目时让 Claude Code 自动识别，或者手动输入 `/oasis-wiki` 调用一次。

第一次安装：

```powershell
# 1. 把这个仓库克隆到一个稳定位置。
git clone https://github.com/mislw/oasis-wiki.git "$env:USERPROFILE\oasis-wiki"

# 2. 创建 Claude Code 的用户级 skills 目录。
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null

# 3. 复制 oasis-wiki skill 到 Claude Code。
Copy-Item -Recurse -Force "$env:USERPROFILE\oasis-wiki\oasis-wiki" "$env:USERPROFILE\.claude\skills\"
```

装完后重启 VS Code，或在命令面板执行 `Developer: Reload Window`。然后在 UGC 工程里打开 Claude Code；如果它没有自动触发，就先发一句 `/oasis-wiki`，后面继续正常提问。

更新 Claude Code 里的本地 skill：

```powershell
git -C "$env:USERPROFILE\oasis-wiki" pull
Copy-Item -Recurse -Force "$env:USERPROFILE\oasis-wiki\oasis-wiki" "$env:USERPROFILE\.claude\skills\"
```

如果某个 Claude Code 环境没有加载用户级 skill，就保留这个仓库，并让 Claude Code 能访问仓库目录；然后把 `AGENTS.md` 或 `AGENT_PROMPT.md` 当作临时启动说明使用。

### 更新本地安装

```powershell
git pull
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

### 常用问法

```text
用 oasis-wiki 看一下这个 UGCPlayerController 里的 RPC 怎么接。
帮我按当前项目已有基础规划一下某个养成功能。
看一下这个报错，先查 DSlog / Clientlog 相关说明。
正常模式，给我最小改动代码。
教学模式，带我一步一步做这个 UI -> ServerRPC -> 刷新流程。
```

### 注意

- 不要把 `%USERPROFILE%\.codex\oasis-project-cache` 里的内容提交到 GitHub。
- 不要把具体项目策划案、Excel、截图原件直接塞进这个 skill 仓库。
- 如果要沉淀项目资料，只写入本机项目缓存；如果要沉淀通用经验，再更新这个仓库。

---

## English Overview

This repository packages a portable AI-agent knowledge bundle for Oasis / 绿洲启元 / 和平精英 UGC Lua development.

It is Codex-native through `oasis-wiki/SKILL.md`, and also includes generic instructions for other AI coding agents through `AGENTS.md` and `AGENT_PROMPT.md`.

The skill bundles a local Markdown export of the Oasis wiki, official API reference, 1.37 incremental updates, and official forum tutorials. It instructs Codex to search official documentation before answering questions about Lua APIs, gameplay systems, UI systems, editor workflows, templates, debugging, logs, performance, release notes, and terminology.

It also includes generic project-architecture notes for common UGC Lua workflows. Project-specific planning notes, local caches, and private docs should stay outside this public repository.

The skill is designed for teaching-mode project help by default: Codex can read project files to understand them, but should explain edits instead of directly modifying UGC project files unless explicitly overridden. Concise normal mode is available when explicitly requested.

## Install

Copy the `oasis-wiki` folder into your Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\oasis-wiki "$env:USERPROFILE\.codex\skills\oasis-wiki"
```

Restart Codex or refresh skills after copying.

## Use With Other AI Agents

For agents that do not support Codex skills directly:

1. Open `AGENTS.md` as the repository-level instruction file.
2. If the agent accepts a setup prompt, paste `AGENT_PROMPT.md`.
3. Point the agent at the `oasis-wiki/references` folder for search and citation.

The important behavior is the same across agents: search the official local wiki docs and distilled references first, use teaching mode by default, and do not directly modify UGC project files unless explicitly allowed for that task.

Trigger expectation: if a question looks related to a 绿洲启元 / 绿洲起源 / 和平精英 UGC project, UGCProjects workspace, or UGC Lua code, the agent should use this bundle by default.

### Claude Code

Claude Code can use this bundle as a user-level skill, so you do not need to add `CLAUDE.md` or any other helper file to a UGC project root.

Install once:

```powershell
# 1. Clone the bundle somewhere stable.
git clone https://github.com/mislw/oasis-wiki.git "$env:USERPROFILE\oasis-wiki"

# 2. Create Claude Code's user skills directory.
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null

# 3. Copy the skill folder into Claude Code's user skills directory.
Copy-Item -Recurse -Force "$env:USERPROFILE\oasis-wiki\oasis-wiki" "$env:USERPROFILE\.claude\skills\"
```

After installing, restart VS Code or run `Developer: Reload Window`, then open Claude Code from your UGC project as usual. In most cases, questions about Oasis / 绿洲启元 / 和平精英 UGC, `UGCProjects`, UGC Lua, RPC, replication, UI, logs, `DSlog`, or `Clientlog` should trigger the skill from the conversation context. If Claude Code does not pick it up automatically, call it explicitly once with `/oasis-wiki`, then continue the conversation normally.

Update the installed skill:

```powershell
git -C "$env:USERPROFILE\oasis-wiki" pull
Copy-Item -Recurse -Force "$env:USERPROFILE\oasis-wiki\oasis-wiki" "$env:USERPROFILE\.claude\skills\"
```

Temporary fallback: if a Claude Code environment does not load user skills, keep the repository cloned and start Claude Code with access to the bundle directory:

```powershell
Set-Location "$env:USERPROFILE\UGCProjects\YourProject"
claude --add-dir "$env:USERPROFILE\oasis-wiki" "Use the Oasis Wiki bundle at $env:USERPROFILE\oasis-wiki. Read AGENTS.md first. For Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua, debugging, or log questions, search oasis-wiki/references before answering. For feature/API/system questions, search the official documentation bundle first: base wiki teaching docs, 官方API参考手册.md, 新增内容_1.37版本.md, and 论坛经验帖_绿洲启妹.md. For logs, distinguish PIE logs, Clientlog, DSlog, phone client logs, management-platform DS logs, and battle logs. Before writing Lua, read oasis-wiki/references/code-style.md. Use teaching mode by default. Use concise normal mode only when I explicitly ask for 正常模式, brevity, direct code, or review-friendly output. Keep UGC project files read-only unless I explicitly ask you to directly modify them. In normal mode code snippets, use only brief summary comments before functions/methods or major blocks; do not add line-by-line teaching comments. Prefer the smallest additive change."
```

## Use

Ask Codex questions such as:

```text
Use $oasis-wiki to explain how to revive a player in Oasis.
Use $oasis-wiki to find UGCGameSystem examples.
Use $oasis-wiki to write Lua code for toggling damage.
```

## Search The Bundled Wiki

From inside the `oasis-wiki` folder:

```powershell
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" .\references\wiki
powershell -ExecutionPolicy Bypass -File .\scripts\search-oasis-wiki.ps1 -Query "角色复活" -MaxResults 10
node .\scripts\search-oasis-wiki.mjs "角色复活" --max 10
```

## Contents

- `AGENTS.md`: Generic instructions for AI coding agents.
- `AGENT_PROMPT.md`: Copy-paste prompt for agents that do not auto-read repository instructions.
- `oasis-wiki/AGENTS.md`: Generic instructions kept inside the portable skill folder.
- `oasis-wiki/SKILL.md`: Codex skill instructions and trigger metadata.
- `oasis-wiki/agents/openai.yaml`: UI metadata.
- `oasis-wiki/references/wiki`: Markdown wiki export.
- `oasis-wiki/references/wiki/官方API参考手册.md`: Official API reference for classes, enums, functions, and parameters.
- `oasis-wiki/references/wiki/新增内容_1.37版本.md`: Official 1.37 incremental feature and behavior updates.
- `oasis-wiki/references/wiki/论坛经验帖_绿洲启妹.md`: Official forum tutorials and practical implementation examples.
- `oasis-wiki/references/project-patterns.md`: Generic UGC project architecture and Lua patterns without private project names or local paths.
- `oasis-wiki/references/project-cache.md`: Local computer cache workflow for reusing parsed knowledge from a specific UGC project without writing cache files into the project workspace.
- `oasis-wiki/references/project-planning-memory.md`: Project-name/path routing workflow for uploaded planning docs, requirements, system details, and whole-project design memory.
- `oasis-wiki/references/answer-modes.md`: Rules for default teaching mode and explicit concise normal mode.
- `oasis-wiki/references/code-style.md`: Lightweight project code style for comments, config tables, variable names, member variables, and methods.
- `oasis-wiki/references/teaching-mode.md`: Code teaching workflow and read-only project-file constraint.
- `oasis-wiki/references/feature-development-flow.md`: End-to-end UGC feature pipeline from config through server, RPC, UI, replication, and reconnect.
- `oasis-wiki/references/recipes.md`: Common implementation recipes for UGC coding tasks.
- `oasis-wiki/references/snippets.md`: Small Lua templates for RPCs, UI, replication, actions, resources, and loadouts.
- `oasis-wiki/references/pitfalls.md`: Gotchas and verification reminders for UGC Lua work.
- `oasis-wiki/references/skill-evolution.md`: Controlled protocol for deciding when and how to update the skill.
- `oasis-wiki/scripts`: Search helpers.

The bundled wiki export was generated on 2026-06-16 and contains 58 base Markdown files, plus official 2026-07-10 updates: `新增内容_1.37版本.md`, `论坛经验帖_绿洲启妹.md`, and `官方API参考手册.md`.
