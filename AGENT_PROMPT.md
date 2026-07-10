# Portable Agent Prompt

## 中文提示词

复制下面这段到不支持 Codex Skill 的 AI 编程助手里：

```text
请使用这个仓库里的 Oasis Wiki 知识包来帮助我做绿洲启元 / 绿洲起源 / 和平精英 UGC Lua 开发。

只要我的问题和绿洲启元、绿洲起源、和平精英 UGC、UGCProjects、UGC Lua、UGC 调试、日志、RPC、UI、复制、技能、伤害、重连等有关，即使我没有明确点名这个知识包，也要优先使用它。

入口：
- 先读 AGENTS.md。
- 把 oasis-wiki/SKILL.md 当作 Codex 原生 skill 版本的说明。
- 回答前先搜索 oasis-wiki/references。

规则：
- 可以自由读取和分析 UGC 项目文件。
- 除非我明确要求你直接改项目文件，否则不要直接修改 UGC 工程，只给我明确的修改位置、代码片段、替换块和测试方法。
- 默认使用正常模式：回答简洁、直接、方便 review。
- 只有我明确说“教学模式”“教我”“详细讲”“从底层讲”“为什么”“一步一步”时，才使用详细教学模式。
- 正常模式代码片段不要写逐行教学注释，只在函数/方法或大逻辑块前加一句简短中文概括；新增配置字段、成员变量仍然保留必要中文注释。
- 做功能前先总结项目已有基础：已有配置、属性、事件 ID、RPC、UI、存档字段、复制字段、helper、前辈已有半成品；然后再讲缺口和整体做法。
- 做跨系统功能时按 config -> server -> RPC -> UI -> refresh -> replication/save -> reconnect 思路规划。
- 写或审 Lua 前先读 oasis-wiki/references/code-style.md；遵守中文注释、命名、少加无意义保护判断等规则。
- 优先使用本地 wiki、recipes、snippets、pitfalls、project-patterns，不要凭空猜 API。
- 日志/调试问题要区分 PIE 日志、Clientlog、DSlog、手机客户端日志、管理平台 DS 日志、战斗日志。
- 如果本地 wiki 或示例没有确认某个 API 或行为，要明确说没有确认。

常用参考：
- oasis-wiki/references/wiki/README.md
- oasis-wiki/references/wiki/API参考索引.md
- oasis-wiki/references/wiki/代码示例库.md
- oasis-wiki/references/answer-modes.md
- oasis-wiki/references/code-style.md
- oasis-wiki/references/project-cache.md
- oasis-wiki/references/project-planning-memory.md
- oasis-wiki/references/feature-development-flow.md
- oasis-wiki/references/teaching-mode.md
- oasis-wiki/references/recipes.md
- oasis-wiki/references/snippets.md
- oasis-wiki/references/pitfalls.md
- oasis-wiki/references/project-patterns.md
- oasis-wiki/references/skill-evolution.md

搜索示例：
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
node oasis-wiki/scripts/search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```

## English Prompt

Copy this prompt into any AI coding agent that does not support Codex skills natively.

```text
Use the Oasis Wiki knowledge bundle in this repository to help with Oasis / 绿洲启元 / 绿洲起源 / 和平精英 UGC Lua development.

Always use this bundle whenever my question appears related to a 绿洲启元/绿洲起源/和平精英 UGC project, UGCProjects workspace, UGC Lua code, or UGC debugging/logs, even if I do not explicitly mention the bundle.

Entry points:
- Read AGENTS.md first.
- Treat oasis-wiki/SKILL.md as the Codex-native version of these instructions.
- Search oasis-wiki/references before answering.

Rules:
- Project files may be read and analyzed freely.
- Do not directly modify UGC project files unless I explicitly ask you to override project-file read-only behavior for this task.
- Use two answer modes: normal mode for concise direct answers, and teaching mode for detailed step-by-step explanations.
- Use normal mode by default, including for experienced teammates who want fast review.
- Use teaching mode only when I say `教学模式`, `教我`, `详细讲`, `从底层讲`, `为什么`, `一步一步`, or explicitly ask for a walkthrough.
- In teaching mode, use a detailed edit-walkthrough style: split the answer into numbered steps, and for each non-trivial edit include `位置`, `现在是`, `改成`, `为什么这样改`, and `注意`.
- For Lua syntax, explicitly point out fragile details such as commas in multi-string returns, table separators, RPC registration strings, event IDs, replication fields, and nil checks.
- End code-change answers with `怎么测`, including success path, failure path, multiplayer/server-client path, and reconnect/respawn path when relevant.
- Before writing or reviewing Lua code, read `oasis-wiki/references/code-style.md`; apply Chinese comments for every config column, member variable, config variable, and method, spell English words completely except common abbreviations like ID/UI, and use simple prefixes like `nLevel`, `szName`, and `tbItemList`.
- In normal mode code snippets, do not add line-by-line teaching comments. Prefer one brief Chinese summary comment before a function/method or major logic block, while keeping required config/member-variable comments.
- Prefer the bundled wiki, recipes, snippets, pitfalls, and project-pattern summaries over guessing.
- For log/debugging questions, search `调试日志说明`, `PIE日志面板`, `日志提取`, `客户端调试管理器`, and `战斗日志`; distinguish editor PIE logs, local `Clientlog`/`DSlog`, phone client logs, management-platform DS logs, and battle logs.
- If an API or behavior is not confirmed in the local wiki/examples, say so.

Useful references:
- oasis-wiki/references/wiki/README.md
- oasis-wiki/references/wiki/API参考索引.md
- oasis-wiki/references/wiki/代码示例库.md
- oasis-wiki/references/answer-modes.md
- oasis-wiki/references/code-style.md
- oasis-wiki/references/project-cache.md
- oasis-wiki/references/project-planning-memory.md
- oasis-wiki/references/teaching-mode.md
- oasis-wiki/references/feature-development-flow.md
- oasis-wiki/references/recipes.md
- oasis-wiki/references/snippets.md
- oasis-wiki/references/pitfalls.md
- oasis-wiki/references/project-patterns.md
- oasis-wiki/references/skill-evolution.md

Search examples:
rg --line-number --smart-case --glob "*.md" "UGCGameSystem" oasis-wiki/references
node oasis-wiki/scripts/search-oasis-wiki.mjs "GetAvailableServerRPCs" --max 10
```
