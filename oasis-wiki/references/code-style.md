# UGC Code Style

Use this reference whenever writing or reviewing Oasis/绿洲启元/和平精英 UGC Lua code, especially when adding config tables, member variables, methods, or `GlobalConfig` entries.

## Core Rules

0. Existing teammate/predecessor code is protected. Do not directly rewrite, restructure, wrap, rename, reorder, or refactor existing blocks for cleanliness. Keep the original structure intact and add the narrowest compatible new logic beside or after it. If an existing block truly must change, explain why it is unavoidable before editing and limit the edit to the exact affected lines.
1. New config tables must include Chinese comments for every column.
2. English words in config table column names and variable names should be spelled out completely. Only use very common abbreviations such as `ID` and `UI`.
3. Simple typed variables should use lightweight type prefixes:
   - `nLevel`: number
   - `szName`: string
   - `tbItemList`: table/list
4. Every member variable and every `GlobalConfig` config variable must have a Chinese comment.
5. Every method must have a Chinese comment explaining its purpose.
6. Keep defensive code narrow. Only guard real boundary risks such as user input, missing config, RPC/network payloads, async UI lifecycle, destroyed actors, or optional data. For internal code with trusted required values, keep the flow direct; if an impossible invalid value appears and there is no clear recovery path, let it error so the real bug is exposed instead of hiding it behind noisy `if` branches. In particular, do not repeatedly wrap each block with checks like `if CauserActor and UE.IsValid(CauserActor) then` when the same actor/context is required by the whole calculation flow.
7. Match HeQirui-style change size for RedCliff-like code: bug fixes should usually be a few changed lines, ordinary feature hooks should stay close to the existing entry point, and larger diffs need a real feature reason rather than extra protection layers. Prefer direct project-style code over generic guard/wrapper scaffolding.
8. A Lua table literal is not automatically a config table. Classify it by what it owns and how it is used: business/config data needs config-table rules; a short ordered list of homogeneous runtime widgets may be local and looped; unrelated fixed-semantic UI attributes should usually bind their explicit config fields directly to their explicit widgets instead of introducing a metadata-driven mapping layer.

## How To Apply

- Put comments close to the variable, table field, or method they explain.
- For config tables, comment the meaning of each column, not only the table itself.
- For methods, explain what the method is responsible for and which side it runs on when relevant, such as server, client, UI, GameState, GameMode, PlayerController, Pawn, or Action.
- When adding behavior to an existing file, prefer a new helper, a new config entry, a new event/RPC hook, or a small appended branch over replacing the original function body.
- Add helpers only when they remove real repeated code or match an existing project pattern. Do not create helper layers just to make one small change look more systematic.
- Keep existing project naming when editing old code. Apply this style most strongly to new code, new config fields, new member variables, and newly added methods.
- Do not rename old fields only to satisfy style unless the user explicitly asks for cleanup, because renaming config keys, RPC names, event IDs, or save keys can break existing behavior.
- Avoid boilerplate nil/validity checks at every step when the value is a required invariant. Add a guard only when the code can make a useful decision after the guard, such as logging a clear config error, returning from a UI callback after a widget was closed, rejecting bad client input, or using a documented fallback.
- If a required object must be validated once for readability, validate it once near the boundary or function entry, then write the main logic without repeating the same `and UE.IsValid(...)` condition around every section. For calculations such as damage formulas, repeated checks around attack, tower, critical, and camp logic usually make the code harder to read without adding real recovery behavior.

## UI Tables: Config, Mapping, Or Widget List

Use the table's responsibility, not the `{}` syntax, to classify it:

- **Business/config table:** contains tunable values, IDs, labels, field names, rules, costs, or balance data that drive behavior. Prefer the project's DataTable/`GlobalConfig`/`GameState` config owner and follow config comments and naming rules.
- **Homogeneous widget list:** contains runtime references or names for repeated controls that receive the same operation by index, such as inventory cells, tower slots, or feature rows. A small local `tb...WidgetList` plus a loop is appropriate, especially when Blueprint-generated names are irregular.
- **Fixed-semantic binding:** health, defense, attack, critical chance, and other distinct fields each have a stable meaning and a stable target widget. Bind `currentLevelConfig.Health` to the health widgets and `currentLevelConfig.Attack` to the attack widgets directly. Do not create entries such as `{ FieldName, Label, PrefixWidget, ArrowWidget, NumberWidget }` merely to replace a few explicit assignments.

Decision checks:

1. If every entry has the same shape, receives the same operation, and the index has real slot/row meaning, use a list and loop.
2. If entries represent different fixed meanings and the table exists mainly to enable dynamic field lookup, prefer direct binding.
3. If designers may tune the values or rules independently of the widget instances, keep them in the authoritative config source rather than a local UI table.
4. When reviewing "predecessor style," verify authorship with `git blame`/`git show`. A new block inside an older function is not predecessor code merely because the surrounding loop is.

```lua
-- Good: repeated homogeneous slots with irregular Blueprint widget names.
local tbTowerSlotWidgetList = {
    self.TowerSlot,
    self.TowerSlot_C_0,
    self.TowerSlot_C_1,
}

for nSlotIndex = 1, #tbTowerSlotWidgetList do
    local slotImage = tbTowerSlotWidgetList[nSlotIndex].Image_Icon
    -- Refresh every slot with the same operation.
end
```

```lua
-- Avoid: fixed-semantic attributes converted into a second configuration layer.
local tbAttributeBindingList = {
    { FieldName = "Health", Label = "Health", Widget = self.Text_Health },
    { FieldName = "Attack", Label = "Attack", Widget = self.Text_Attack },
}

-- Prefer explicit bindings from the authoritative config row.
self.Text_Health:SetText(tostring(currentLevelConfig.Health))
self.Text_Attack:SetText(tostring(currentLevelConfig.Attack))
```

## Examples

```lua
GlobalConfig.SkillConfig = {
    [1] = {
        SkillID = 1001, -- 技能配置ID，用于和技能系统或技能表中的配置对应
        szSkillName = "疾跑", -- 技能显示名称，用于UI展示
        nCooldownSeconds = 10, -- 技能冷却时间，单位：秒
        tbRewardItemList = { -- 技能触发后发放的奖励道具列表
            { ItemID = 101, nCount = 1 }, -- 奖励道具ID和数量
        },
    },
}
```

```lua
-- 初始化玩家本局技能数据，只在服务端创建权威数据
function UGCPlayerController:InitPlayerSkillData()
    -- tbPlayerSkillData 保存玩家本局技能状态，重连时可以基于它重新下发UI
    self.tbPlayerSkillData = {}

    -- nSelectedSkillID 记录玩家当前选择的技能ID，0表示还没有选择
    self.nSelectedSkillID = 0
end
```
