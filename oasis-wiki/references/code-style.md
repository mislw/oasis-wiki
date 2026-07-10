# UGC Code Style

Use this reference whenever writing or reviewing Oasis/绿洲启元/和平精英 UGC Lua code, especially when adding config tables, member variables, methods, or `GlobalConfig` entries.

## Core Rules

1. New config tables must include Chinese comments for every column.
2. English words in config table column names and variable names should be spelled out completely. Only use very common abbreviations such as `ID` and `UI`.
3. Simple typed variables should use lightweight type prefixes:
   - `nLevel`: number
   - `szName`: string
   - `tbItemList`: table/list
4. Every member variable and every `GlobalConfig` config variable must have a Chinese comment.
5. Every method must have a Chinese comment explaining its purpose.
6. Do not add excessive defensive validity checks. Only guard real boundary risks such as user input, missing config, RPC/network payloads, async UI lifecycle, destroyed actors, or optional data. For internal code with trusted required values, keep the flow direct; if an impossible invalid value appears and there is no clear recovery path, let it error so the real bug is exposed instead of hiding it behind noisy `if` branches. In particular, do not repeatedly wrap each block with checks like `if CauserActor and UE.IsValid(CauserActor) then` when the same actor/context is required by the whole calculation flow.

## How To Apply

- Put comments close to the variable, table field, or method they explain.
- For config tables, comment the meaning of each column, not only the table itself.
- For methods, explain what the method is responsible for and which side it runs on when relevant, such as server, client, UI, GameState, GameMode, PlayerController, Pawn, or Action.
- Keep existing project naming when editing old code. Apply this style most strongly to new code, new config fields, new member variables, and newly added methods.
- Do not rename old fields only to satisfy style unless the user explicitly asks for cleanup, because renaming config keys, RPC names, event IDs, or save keys can break existing behavior.
- Avoid boilerplate nil/validity checks at every step when the value is a required invariant. Add a guard only when the code can make a useful decision after the guard, such as logging a clear config error, returning from a UI callback after a widget was closed, rejecting bad client input, or using a documented fallback.
- If a required object must be validated once for readability, validate it once near the boundary or function entry, then write the main logic without repeating the same `and UE.IsValid(...)` condition around every section. For calculations such as damage formulas, repeated checks around attack, tower, critical, and camp logic usually make the code harder to read without adding real recovery behavior.

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
