# MCP Config-Driven UI Workflow

Use this reference when one feature crosses all of these layers: `UserDefinedStruct`/`DataTable`, Lua config loading, RPC or replicated state, and a WidgetBlueprint that must refresh visible values.

## Contents

1. Non-Negotiable Order
2. Create The Table Directly
3. Bind The Runtime Data Flow
4. Make Widgets Reachable From Lua
5. Chinese, Color, Background, And Layout
6. Verification Gates
7. Failure Matrix

## Non-Negotiable Order

Execute and verify one layer at a time:

```text
read context and back up binary assets
-> create/verify row struct
-> create UAEDataTable
-> add rows and reload them
-> load rows into the runtime data owner
-> update authoritative level/state
-> notify the client
-> refresh the Widget
-> inspect Clientlog and DSlog
```

Do not style the final UI before the table and refresh chain pass. Do not call a feature complete because the editor preview looks correct.

## Create The Table Directly

Prefer direct MCP creation for a new Oasis table. Do not begin with the generic CSV import dialog.

```python
import unreal_engine as ue

row_struct = ue.load_object(
    ue.find_class('UserDefinedStruct'),
    '/Project/Asset/Data/Table/Rank/UGCTemplateRowStruct_Rank.UGCTemplateRowStruct_Rank'
)

factory = ue.new_object(ue.find_class('UGCDataTableFactory'))
factory.Struct = row_struct

table = ue.create_asset(
    'RankConfig',
    '/Project/Asset/Data/Table/Rank',
    ue.find_class('UAEDataTable'),
    factory
)
```

Populate each row through the table's row struct:

```python
row = table.data_table_empty_row()
row.set_field('Level', 1)
row.set_field('Name', '\u521d\u59cb\u7b49\u7ea7')
row.set_field('Value1', 45)
row.set_field('Value2', 45)
row.set_field('Value3', 45)
table.data_table_add_row('Level1', row)

table.save_package()
```

Rules:

- Use the exact field names and case returned by `row.as_dict()` or the row struct.
- For a new Oasis config table, use `UAEDataTable` with `UGCDataTableFactory` unless MCP inspection proves a different local pattern.
- Treat a serialized `null` return from `data_table_add_row` as inconclusive. Some builds return no Python value even when the row is added.
- Prove success by reloading the asset and checking `data_table_as_dict()` or `data_table_find_row(...).as_dict()`.
- Verify row count, row names, key numeric fields, and Unicode text before touching Lua.

### CSV Import Trap

`ue.import_asset(csv_path, destination)` can open the `DataTable Options` modal and block the MCP call while waiting for a row struct. Passing `UGCDataTableFactory` to `ue.import_asset(..., factory)` may still return `None` because that factory is suitable for creating the table but not necessarily for importing CSV in the current editor build.

After either symptom, stop retrying that route. Cancel the modal, create the table with `ue.create_asset`, and add rows directly.

## Bind The Runtime Data Flow

Load the table once in the established config owner, usually `GameState`, and copy rows into normal Lua tables:

```lua
self.tbRankConfig = {}

local rows = UGCGameSystem.GetTableData(
    UGCGameSystem.GetUGCResourcesFullPath(
        "Asset/Data/Table/Rank/RankConfig.RankConfig"
    )
)

for _, config in pairs(rows or {}) do
    local level = tonumber(config.Level) or 0
    if level > 0 then
        self.tbRankConfig[level] = {
            Level = level,
            Name = config.Name,
            Values = {
                config.Value1 or 0,
                config.Value2 or 0,
                config.Value3 or 0,
            },
        }
    end
end
```

Do not mutate returned DataTable row objects at runtime. Copy the fields needed by gameplay/UI.

For an upgrade UI, read current and next rows separately:

```lua
local current = configByLevel[level]
local nextConfig = configByLevel[level + 1]
```

The authoritative server flow should be:

```text
button click -> server RPC -> validate next row -> increment state
-> client RPC or replication callback -> UI.Refresh
```

An optimistic local refresh is optional; the authoritative callback must still refresh the UI.

## Make Widgets Reachable From Lua

Widget names visible in `ue.widget_inspect(bp)` are not proof that Lua can access `self.WidgetName`.

Every control referenced from Lua must have `bIsVariable = true`, especially generated `TextBlock` controls. A missing binding usually produces:

```text
attempt to index a nil value (field 'TextBlock_*')
```

For generated assets where `bp.WidgetTree.AllWidgets` is empty, traverse from `RootWidget`:

```python
widgets = []

def walk(widget):
    widgets.append(widget)
    if hasattr(widget, 'GetChildrenCount'):
        for index in range(widget.GetChildrenCount()):
            walk(widget.GetChildAt(index))

walk(bp.WidgetTree.RootWidget)

for widget in widgets:
    if widget.get_class().get_name() == 'TextBlock':
        widget.bIsVariable = True

ue.compile_blueprint(bp)
bp.save_package()
```

Verify both the persisted flag and generated class fields:

```python
variable_flags = {w.get_name(): bool(w.bIsVariable) for w in widgets}
generated_fields = [p for p in bp.GeneratedClass.properties()
                    if p in variable_flags]
```

Restart PIE after changing `bIsVariable` or recompiling a WidgetBlueprint. Existing Widget instances use the old generated class.

## Chinese, Color, Background, And Layout

Apply these in order:

1. Copy font settings from a known working Chinese TextBlock.
2. Write Chinese through Unicode code points if transport readback becomes `?` or mojibake.
3. Test color on three representative controls before bulk styling.
4. Use real setter functions such as `SetColorRGBStr` and `SetBackgroundColor` when struct-style property writes do not persist.
5. Replace unbrushed decorative `Image` panels with disabled tinted `Button` controls when PIE renders white blocks.
6. Center the popup against the designer's dashed screen frame by moving all top-level children by one common delta.
7. Move major groups before local controls; then fix text/icon gaps and enlarge row backgrounds to cover every grouped row.
8. Compile, save, reopen the asset, and rerun PIE.

## Verification Gates

Do not proceed past a failed gate:

| Gate | Required evidence |
|---|---|
| Table asset | Correct `load_path`, `UAEDataTable`, expected row struct |
| Rows | Reloaded row count/names and exact current/next values |
| Chinese | `unicode_escape` readback matches intended code points |
| Lua load | Runtime config map contains every expected numeric level |
| State | DSlog shows server RPC and new authoritative level |
| Client | Clientlog shows callback/replication with the same level |
| Widget binding | `bIsVariable=true` and generated class contains every Lua field |
| Refresh | Clientlog shows `Refresh level/current/next` with no following Lua exception |
| Visual | New PIE instance shows the expected before/after values and final max state |

## Failure Matrix

| Symptom | Likely cause | Required check/fix |
|---|---|---|
| Import call hangs | CSV row-struct modal opened | Cancel it; use direct table creation and row insertion |
| Import returns `None` | Factory does not support CSV import in this build | Use `ue.create_asset` with `UGCDataTableFactory` |
| `data_table_add_row` returns `null` | Binding exposes no return value | Reload and inspect rows; do not assume failure |
| Table has correct values but UI stays static | Lua refresh aborted or TextBlocks are not variables | Search Clientlog for `nil TextBlock`; set `bIsVariable`, compile, restart PIE |
| Server says upgrade succeeded but UI is unchanged | State path works; client/widget path is broken | Compare DSlog level, client callback level, and first exception after `Refresh` |
| Designer text is correct but PIE shows boxes | Runtime font/fallback mismatch | Copy the full font configuration from a working TextBlock |
| MCP readback shows `?` | Chinese was corrupted in transport | Use ASCII-only Unicode construction and verify with `unicode_escape` |
| UI is white or colors reset | Unsupported style property write or unbrushed Image | Use widget setter functions; use disabled tinted Buttons for passive panels |
| Popup is visually offset | Centered against guessed coordinates | Center against the dashed screen frame and move top-level children together |
| New bindings still appear missing | PIE is using an old generated class | Stop PIE, compile/save, then start a fresh PIE session |
