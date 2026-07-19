# MCP Integration

Use this reference first for UGCAskQ MCP, MCP Server, editor automation, `.mcp.json`, SSE connection, PRV, or MCP log debugging tasks. Keep this file as the shared connection and routing layer, then load only the needed branch reference:

- UI/Widget/UMG/Blueprint work: `references/mcp-ui-widget.md`
- Config table/DataTable/UAEDataTable work: `references/mcp-datatable.md`

## Boundary

- Keep `oasis-wiki` as the planning, safety, wiki lookup, project-pattern, and verification layer.
- Keep `ugcaskq` MCP as the editor execution channel for reading or mutating editor state and assets.
- Do not modify the official UGCAskQ MCP server unless the user explicitly asks to work on the server itself.
- Prefer branch references over this file for task-specific detail.

## Standard Flow

1. Trigger this skill and load only the relevant references.
2. Confirm the MCP Server panel is running and the port matches `.mcp.json` or the client MCP config.
3. Confirm MCP call logging is enabled when debugging or mutating assets.
4. Inspect editor context before choosing edits.
5. Branch:
   - UI/Widget/UMG/Blueprint: read `references/mcp-ui-widget.md`.
   - Config/DataTable/UAEDataTable: read `references/mcp-datatable.md`.
   - Map/actor/other asset work: continue with shared MCP docs and focused wiki search.
6. Make a small plan before MCP writes; use PRV planning when the editor requires it.
7. Back up assets before data table, blueprint, map, or bulk asset mutation. Put `.uasset` backups outside the UGC project tree.
8. Execute editor reads/writes through UGCAskQ MCP.
9. Verify changed assets through MCP reads, project files, editor-visible state, or logs.
10. Report exact evidence and any remaining risk.

## Branch Selection

Use the UI branch for:

- `用MCP生成蓝图/UI`
- `用MCP查看这个UI`
- `补Widget蓝图`
- `这个UI在哪里`
- Widget tree, UMG controls, layout, colors, buttons, click interaction, UI Lua binding.

Use the DataTable branch for:

- `用MCP查表`
- `用MCP查看配置表`
- `绑定一个配置表`
- `DataTable`
- `UAEDataTable`
- numerical tables, item/gem/equipment/skill configs, table-backed UI/gameplay.

If a task touches both, read this file first, then `mcp-datatable.md` for config shape and `mcp-ui-widget.md` for UI creation/binding. Keep reads narrow: identify config rows first, then inspect only UI widgets that use those rows.

## MCP Setup Checks

- `.mcp.json` should contain an SSE server whose URL matches the editor panel, for example `http://127.0.0.1:<port>/sse`.
- The editor MCP Server should show `Running` and the same port.
- If a direct MCP tool namespace is not exposed, use a small local JSON-RPC/SSE bridge only as execution plumbing.
- Treat UGCAskQ MCP as local-only and experimental; save or back up before mutation.

### Missing `.mcp.json` Bootstrap

If the user asks to use MCP but no direct `mcp__ugcaskq__...` namespace is exposed, first search for an existing connection file:

```powershell
Get-ChildItem -Force -Path . -Filter .mcp.json
Get-ChildItem -Force -Path <ProjectRoot> -Filter .mcp.json -Recurse
```

If no `.mcp.json` exists in the current UGC project, create one at the project root instead of stopping. Use the editor MCP Server panel port when visible or provided by the user. If the port is not visible, try the official/default UGCAskQ port from the wiki first, then clearly report the chosen port and verify connectivity.

Minimal file:

```json
{
  "mcpServers": {
    "ugcaskq": {
      "type": "sse",
      "url": "http://127.0.0.1:<port>/sse"
    }
  }
}
```

Bootstrap rules:

- Do not overwrite an existing `.mcp.json`; read and reuse it.
- Create the file only in the current UGC project root, not in parent engine folders.
- After creating the file, connect to the SSE URL and call `initialize`, `notifications/initialized`, and `tools/list`.
- Treat the connection as usable only after `tools/list` returns `ue_read`, `ue_py`, and `ue_plan_submit`.
- If connection fails, tell the user the exact URL tried and ask them to start the editor MCP Server or provide the panel port. Do not guess multiple ports in a long loop.
- Once connected through a manual SSE bridge, keep using the same read-plan-write-verify workflow as a direct MCP namespace.

## MCP Tool Roles

Use these UGCAskQ tools in this order:

- `ue_read`: read editor context, API docs, schemas, asset registry, widget tree, DataTable structure, selected actors.
- `ue_plan_submit`: submit a PRV mutation plan when doing CDO, WidgetTree, DataTable, map, or asset writes.
- `ue_py`: execute editor Python. For reads, no plan is needed. For writes, include `transaction_name` and a YAML `plan`.

If no direct `mcp__ugcaskq__...` namespace is exposed, connect to the SSE URL from `.mcp.json` and call JSON-RPC methods:

1. `initialize`
2. `notifications/initialized`
3. `tools/list`
4. `tools/call` with `name: ue_read | ue_py | ue_plan_submit`

## Required First Reads

At the start of any MCP editor task, read:

```text
ctx:
py:index
py:workflow asset_browser
```

Then branch:

- UI branch adds `py:workflow blueprint`, `py:workflow lua`, and widget APIs from `mcp-ui-widget.md`.
- DataTable branch adds `py:list datatable`, `py:guide datatable`, and table schema reads from `mcp-datatable.md`.
- Config-driven UI branch reads `mcp-config-driven-ui.md` first, then loads only the UI/DataTable API details required by the current layer.

Use the first reads to identify:

- current UGC project root and mount path, such as `/RedCliff`;
- current asset open in editor;
- selected actors;
- available UGCAskQ APIs;
- which branch reference to load.

Do not infer editor asset paths from disk paths. Prefer `ue.list_assets(...)` and returned `load_path`.

## Asset Cleanup And Path Collision Checks

If asset creation failed once, or editor reports:

```text
AssetRegistry.GetAssetByObjectPath(/RedCliff/Asset/UI/MilitaryRank) failed
```

check for a file/folder collision:

```text
Asset/UI/MilitaryRank.uasset
Asset/UI/MilitaryRank/
```

The nested Widget asset should be:

```text
/RedCliff/Asset/UI/MilitaryRank/MilitaryRank.MilitaryRank
```

not:

```text
/RedCliff/Asset/UI/MilitaryRank
```

Cleanup rules:

- Delete only assets created or confirmed wrong in the current task.
- Prefer `ue.delete_asset('/Project/Asset/...')` to clean AssetRegistry.
- If a broken tiny `.uasset` remains on disk after registry cleanup, delete only that exact file path.
- Never recursively delete an asset directory unless the user explicitly asks.
- Re-run `ue.list_assets(target_dir, True)` after cleanup.

## PRV Plan Template

For `ue_py` writes, include a task-specific plan:

```yaml
intent: "Create or modify WidgetBlueprint/DataTable/Blueprint"
asset_path: /RedCliff/Asset/UI/MilitaryRank/MilitaryRank
pre_write_snapshot: true
apis_to_call:
  - py:load_object
  - py:compile_blueprint
  - py:save_package
mutations:
  - property: WidgetTree or DataTable row
    value: "Describe the smallest requested change"
```

Match `apis_to_call` and `mutations` to the real task. Do not use a generic plan for unrelated writes.

## Binary Asset Read Fallback

Use UGCAskQ MCP when project context depends on editor-only or binary assets that normal text search cannot inspect.

Common examples:

- `.uasset` DataTables.
- Blueprint assets.
- map actors or selected actors.
- skill editor assets.
- item, gem, monster, equipment, shop, task, or gameplay config tables stored as assets.

Do not infer table fields from Lua code alone when the authoritative config is a `.uasset`. First use MCP to inspect table schema, row count, key fields, sample rows, and warnings. If MCP is unavailable, say the asset content is unverified and avoid claiming exact fields, rows, or values.

## Mutation Guardrails

- Do not use MCP writes as the first step. Read context and identify the smallest safe change first.
- Do not put backup `.uasset` files inside the UGC project tree. The editor can scan backup folders and reject backup names or paths, so use an external location such as `C:/Users/Administrator/Documents/CodexBackups/<ProjectName>/...`.
- Keep project-specific memories and caches outside the global skill and outside the team project unless explicitly requested.
- After table mutation, re-read row counts, key fields, missing rows, and unexpected warnings.
- For a new Oasis table, prefer `ue.create_asset` with `UAEDataTable` plus `UGCDataTableFactory`, then `data_table_empty_row`/`data_table_add_row`; do not repeatedly retry a blocking CSV import modal.
- For Lua-driven Widgets, verify every referenced control has `bIsVariable=true` and appears in the generated class before debugging the table or RPC again.
- After gameplay mutation, search DSlog and Clientlog for both success markers and error markers.

## Chinese Text Encoding

UGCAskQ MCP logs or JSON-RPC wrappers may display Chinese text as mojibake or `?`, especially when `ue_py` requests pass literal Chinese through PowerShell, JSON, or the editor log. Treat the log display as unreliable until the asset is re-read.

When writing Chinese text to DataTable rows or Widget text through MCP:

1. Prefer an ASCII-only `ue_py` script that constructs Chinese strings from Unicode code points with `chr(...)`.
2. For DataTable rows, write fields with DataTable APIs such as `data_table_modify_row(row_name, field_name, value)`.
3. For Widget TextBlocks, call `TextBlock.SetText(text)` from the codepoint-built string. Do not pass literal Chinese through PowerShell or JSON when the previous readback showed `?`.
4. Save the asset package.
5. Re-read the same rows or TextBlocks and verify the real string using `value.encode('unicode_escape').decode('ascii')`.

## Evidence Pattern

For a complete answer after MCP work, include:

- What was changed or read.
- Which branch reference was used: UI/Widget or DataTable/config.
- Which MCP/editor verification succeeded.
- Which runtime log lines prove behavior, if runtime behavior matters.
- What was not verified, if any part could not be tested.
