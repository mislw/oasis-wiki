# Task Router

Use this reference immediately after `SKILL.md` for Oasis / UGC project work. Its job is to route the request by user intent, then load only the needed detailed references.

Default rule: choose one primary task branch and at most one secondary branch. Do not load every related reference just because the task mentions UGC.

## Primary Branches

### Project Analysis

Use when the user asks to understand, take over, inspect, compare with a planning document, or identify a project.

Trigger examples:

- `解析一下这个项目`
- `这是哪个工程`
- `策划案对应哪个项目`
- `我接手这个项目`
- `通读项目`
- `项目结构/主流程/核心系统`

Read:

- `references/project-cache.md`
- `references/project-planning-memory.md`
- `references/project-patterns.md` only if architecture patterns are needed

Output should identify project entry points, lifecycle, core systems, data owners, important config/table sources, likely search keywords, risks, and an onboarding path.

### Feature Development

Use when the user asks to add or change gameplay, rewards, buttons, UI actions, upgrades, attributes, tasks, shop behavior, respawn behavior, skills, items, or cross-client/server flows.

Trigger examples:

- `做一个功能`
- `加个按钮`
- `点击后可以升级/领取/购买/抽奖`
- `做军衔/跃升/属性加成`
- `接到配置表`
- `GM 测试`

Read:

- `references/feature-development-flow.md`
- `references/code-style.md` when editing or reviewing Lua
- Secondary branch: `UI And Interaction`, `Config And Balancing`, or `MCP Operation` only when needed

Keep the main pipeline unchanged:

```text
existing foundation
-> config
-> authoritative server logic
-> Server RPC
-> UI/input binding
-> UI refresh
-> replication/save
-> reconnect/recovery
-> GM/log verification
```

Start from the authoritative data owner, not from the button.

### Debugging And Errors

Use when the user reports errors, no effect, crashes, white UI, failed asset load, button does nothing, log output, or editor/MCP failures.

Trigger examples:

- `报错`
- `没生效`
- `点了没反应`
- `怎么都是白色的`
- `AssetRegistry.GetAssetByObjectPath failed`
- `Can not assign table data`
- `日志`

Read:

- `references/pitfalls.md`
- `references/feature-development-flow.md` only if the failure is in a cross-layer feature path
- Secondary branch: `MCP UI`, `MCP DataTable`, or `Config And Balancing` according to the symptom

First inspect available logs when possible. Distinguish root cause from secondary UI symptoms. Prefer fixing the smallest broken link in the existing chain.

### MCP Operation

Use when the user explicitly asks Codex to use MCP / UGCAskQ / editor automation, or asks to generate/view WidgetBlueprints, inspect DataTables, or operate editor assets.

Trigger examples:

- `用 MCP 帮我`
- `生成蓝图/UI`
- `补 Widget 蓝图`
- `查表`
- `操作编辑器`
- `连接 MCP`

Always read:

- `references/mcp-integration.md`

Then branch:

- UI / Widget / UMG / Blueprint viewing or generation: read `references/mcp-ui-widget.md`
- Config tables / DataTable / UAEDataTable: read `references/mcp-datatable.md`
- Mixed feature: read the smallest feature/config/UI branch needed after MCP routing

Do not use both MCP UI and MCP DataTable branches unless the task truly needs both.

### Config And Balancing

Use when the user asks about tables, numerical fields, rewards, probability, item IDs, attributes, row meanings, or how a DataTable/Lua config drives gameplay.

Trigger examples:

- `配置表`
- `数值表`
- `这个字段怎么填`
- `宝石特性表`
- `权重/概率/奖励/属性`
- `FeatureKey`

Read:

- `references/mcp-datatable.md` when the table is an editor asset or the user asks to use MCP
- `references/project-cache.md` for known local table usage
- Search project code for the table consumer before giving design conclusions

Rule: DataTable/UAEDataTable rows are treated as source data. Runtime logic must not mutate returned row objects directly; copy the row into a normal Lua table before changing derived values.

### UI And Interaction

Use when the user asks where a UI lives, how a button opens a panel, how a Widget should be named/bound, or how UI refresh should happen.

Trigger examples:

- `主要 UI 在哪里`
- `按钮怎么接`
- `点击可以交互`
- `UIManager`
- `MainUI`
- `Widget 控件名`
- `刷新 UI`

Read:

- `references/feature-development-flow.md` for server/client data flow
- `references/mcp-ui-widget.md` only for MCP-generated or inspected WidgetBlueprints
- Search `Script/UI`, UIManager registration, and existing button binding patterns

Final answers should name the Widget asset path, Lua script path, entry button, event/RPC chain, and refresh source when known.

### Project Safety

Use as a secondary branch when a task touches editor assets, teammate code, binary assets, dirty worktrees, backup behavior, or release/upload risk.

Trigger examples:

- `.uasset`
- `.umap`
- `脏文件`
- `上传`
- `备份`
- `别影响别的功能`
- `队友代码`

Read:

- `references/pitfalls.md`
- `references/code-style.md`
- MCP branch docs when editor assets are involved

Separate active edits from editor-auto-dirtied assets. Back up binary assets outside the UGC project tree when MCP/editor operations need backups.

## Secondary Branch Selection

Use these pairings for common mixed tasks:

- `MCP 生成 UI + 点击升级`: MCP Operation + Feature Development + UI And Interaction.
- `MCP 查表并解释字段`: MCP Operation + Config And Balancing.
- `报错 Can not assign table data`: Debugging And Errors + Config And Balancing.
- `UI 白色/样式没生效`: Debugging And Errors + MCP Operation UI branch.
- `接手新项目并准备开发`: Project Analysis + Feature Development.

If a secondary branch would only restate obvious engineering knowledge, skip it.

