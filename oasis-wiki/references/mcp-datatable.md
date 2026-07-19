# MCP DataTable And Config Workflow

Use this branch for MCP requests about viewing, reading, exporting, or changing config tables, `.uasset` DataTables, `UAEDataTable`, numerical tables, item/gem/equipment/skill config, or table-backed UI/gameplay.

## Trigger Phrases

- `用MCP查表`
- `用MCP查看配置表`
- `把这个表发给我`
- `绑定一个配置表`
- `点击之后配置表可以加`
- `DataTable`
- `UAEDataTable`
- `数值表`

## Required Reads

After the shared MCP setup in `mcp-integration.md`, read only table/config APIs:

```text
ctx:
py:index
py:workflow asset_browser
py:list datatable
py:guide datatable
py:list asset_browser
schema:DataTable?level=full
```

If a direct table-view helper exists in the MCP tool list, prefer it for read-only inspection before falling back to custom `ue_py`.

## Low-Token Config Table Read Protocol

Do not dump whole tables unless the user explicitly asks.

1. Resolve candidate assets first; return at most 20 candidates with only `name`, `asset_class`, `load_path`, and `package_path`.
2. Load exactly one target table by the returned `load_path`.
3. Return compact metadata: `load_path`, `row_count`, first 10 row names, row struct/class if available, and field names from one sample row.
4. If the user names an ID, row, keyword, feature, or target UI, filter row names first and read only matching rows.
5. If no target row is known, read at most 3 sample rows and at most 20 fields per row.
6. For writes, capture a before/after snapshot of only the target rows and target fields.
7. For Chinese text verification, return `unicode_escape` for changed strings instead of dumping large localized rows.

Use MCP for table contents and schema. Use local `rg` only to find table usage, table paths, enum names, field names, or Lua binding code.

Token limits unless explicitly asked for more:

- candidate assets: max 20;
- row names preview: max 10;
- sample rows: max 3;
- fields per sample row: max 20;
- mutation verification: only changed rows and fields.

## Find The Real Load Path

Use asset browser APIs and the returned `load_path`:

```python
assets = ue.list_assets('/RedCliff/Asset/Data/Table', True)
target = [a for a in assets if a['name'] == 'AttributeBonusTest'][0]
load_path = target['load_path']
```

Do not construct `load_path` from folder and asset name by hand when AssetPathRemapping may apply.

Compact lookup:

```python
search_dir = '/RedCliff/Asset/Data/Table'
keyword = 'AttributeBonusTest'
assets = []
for a in ue.list_assets(search_dir, True):
    name = a.get('name', '')
    path = a.get('load_path', '')
    if keyword.lower() in name.lower() or keyword.lower() in path.lower():
        assets.append({
            'name': name,
            'asset_class': a.get('asset_class'),
            'load_path': path,
            'package_path': a.get('package_path'),
        })
__askq_result = {'matches': assets[:20], 'truncated': len(assets) > 20}
```

## Inspect Rows And Fields

```python
table = ue.load_object(ue.find_class('DataTable'), load_path)
row_names = table.data_table_get_row_names()
sample_names = row_names[:min(3, len(row_names))]
sample_rows = {}
field_names = []

for rn in sample_names:
    row = table.data_table_find_row(rn).as_dict()
    if not field_names:
        field_names = list(row.keys())
    sample_rows[rn] = {k: row.get(k) for k in field_names[:20]}

__askq_result = {
    'load_path': load_path,
    'row_count': len(row_names),
    'row_names_head': row_names[:10],
    'field_names': field_names,
    'sample_rows': sample_rows,
}
```

Target row read:

```python
target_names = ['RowName1']
target_fields = ['ID', 'Name', 'Desc']
rows = {}

for rn in target_names:
    row = table.data_table_find_row(rn).as_dict()
    rows[rn] = {f: row.get(f) for f in target_fields if f in row}

__askq_result = {'rows': rows}
```

If target rows are unknown but the user gives a keyword:

```python
keyword = 'Critical'
matches = [rn for rn in row_names if keyword.lower() in str(rn).lower()]
__askq_result = {'matches': matches[:20], 'truncated': len(matches) > 20}
```

## Create A New Oasis DataTable

For a new config table, prefer direct creation and row insertion. Read `mcp-config-driven-ui.md` as well when the table drives a generated Widget.

1. Back up any existing target `.uasset` outside the project tree.
2. Resolve and load the exact `UserDefinedStruct` asset.
3. Create `UGCDataTableFactory` and assign `factory.Struct`.
4. Create a `UAEDataTable` with `ue.create_asset`.
5. For each row, call `data_table_empty_row`, set exact fields, then call `data_table_add_row`.
6. Save, reload, and verify rows and values.

```python
row_struct = ue.load_object(ue.find_class('UserDefinedStruct'), struct_load_path)
factory = ue.new_object(ue.find_class('UGCDataTableFactory'))
factory.Struct = row_struct

table = ue.create_asset(
    table_name,
    package_path,
    ue.find_class('UAEDataTable'),
    factory,
)

row = table.data_table_empty_row()
row.set_field('Level', 1)
row.set_field('Value', 45)
table.data_table_add_row('Level1', row)
table.save_package()
```

Important behavior in current Oasis editor builds:

- `ue.import_asset(csv_path, destination)` can block on the `DataTable Options` modal.
- Supplying `UGCDataTableFactory` to `ue.import_asset` can still return `None`; do not repeatedly retry it.
- `data_table_add_row` may serialize its successful return as `null`. The authoritative check is persisted row readback, not the return token.
- Documentation may describe `row_data` as a dict, while the runtime binding requires the `UScriptStruct` returned by `data_table_empty_row`. Follow the runtime error and use the struct instance.
- Confirm the row fields with `row.as_dict()` before inserting all rows.

For Chinese values, construct strings with Unicode escapes or `chr(...)`, save, then verify the changed fields with `unicode_escape`.

## UAEDataTable Fallback

Some Oasis tables are `UAEDataTable`, not ordinary Unreal `DataTable`.

Symptoms:

- `schema:DataTable` exists, but `data_table_get_row_names` or `data_table_find_row` is unavailable or returns nothing.
- MCP confirms `asset_type` or class is `UAEDataTable`.
- Reflection shows custom fields such as compressed row data, but no stable public row reader.

Use this order:

1. Use MCP to confirm current asset path, class/type, row struct name, and available query/tool APIs.
2. Try object-editor/table queries such as `qt:objed`, `query_type: objed`, `query_mode: assets`, and any direct DataTable viewer exposed by MCP.
3. Try `ue_py` reflection on the `UAEDataTable` object only to discover methods/properties; keep output capped.
4. If MCP can locate the asset and struct but cannot read rows, use a read-only local `.uasset` fallback only for the target table and only for needed fields.
5. Cross-check field names against Lua struct hints such as `ue_struct_custom.lua` or project table loading code.
6. In the final answer, separate evidence clearly:
   - "MCP confirmed asset path/type/struct/API state."
   - "Rows were recovered by read-only local parsing."

Do not phrase local binary recovery as if MCP directly returned every row.

Read-only binary fallback guardrails:

- Never write, move, or delete the `.uasset`.
- Do not scan all `.uasset` files; target the exact MCP-confirmed file.
- Print only matching ASCII/UTF-16 strings, row names, and target fields.
- Avoid large hex dumps. If needed, dump small offset windows only.
- Prefer bundled Codex Python if `python` is not on PATH.
- Treat binary parsing as best-effort and report uncertainty when row order, localized text, or numeric values cannot be proven.

## Mutate Rows

Use a PRV plan, modify a small number of rows, save, reload, and verify exact fields:

```python
table.data_table_modify_row('RowName', 'FieldName', value)
table.save_package()
row2 = table.data_table_find_row('RowName').as_dict()
```

For Chinese strings, use the Unicode-safe pattern in `mcp-integration.md`.

For config-driven UI or gameplay tasks, read only the config table rows that drive the requested feature, then search code for the binding path. Do not read every related table unless a row reference points to another table and the referenced row is required to complete or verify the task.

Use runtime Lua/code lookup only to explain how the table is consumed. For example, a table may define `FeatureKey` rows while values live in code-side config such as `GemFeatureValueConfig`; report that distinction instead of implying all gameplay values come from the table.

For table-driven UI, do not stop after row verification. Continue with `mcp-config-driven-ui.md` and prove the Lua load, authoritative state transition, Widget variable binding, and runtime refresh.
