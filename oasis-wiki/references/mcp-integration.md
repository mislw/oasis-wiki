# MCP Integration

Use this reference for UGCAskQ MCP, MCP Server, editor automation, `.mcp.json`, SSE connection, PRV, or MCP log debugging tasks.

## Boundary

- Keep `oasis-wiki` as the planning, safety, wiki lookup, project-pattern, and verification layer.
- Keep `ugcaskq` MCP as the editor execution channel for reading or mutating editor state and assets.
- Do not modify the official UGCAskQ MCP server unless the user explicitly asks to work on the server itself.
- Prefer a separate companion MCP for non-Codex clients that need access to this skill's wiki search or checklists.

## Standard Flow

1. Trigger this skill and load only the relevant references.
2. Confirm the MCP Server panel is running and the port matches `.mcp.json` or the client MCP config.
3. Confirm MCP call logging is enabled when debugging or mutating assets.
4. Inspect project code, data tables, selected actors, or editor context before choosing edits.
5. Make a small plan before MCP writes; use PRV planning when the editor requires it.
6. Back up assets before data table, blueprint, map, or bulk asset mutation. Put `.uasset` backups outside the UGC project tree.
7. Execute editor reads/writes through UGCAskQ MCP.
8. Verify the changed assets through MCP reads, project files, or editor-visible state.
9. Verify runtime behavior with `Saved/log/MCP/MCP_YYYYMMDD.log`, DSlog, Clientlog, PIE logs, or battle logs as appropriate.
10. Report exact evidence and any remaining risk.

## MCP Setup Checks

- `.mcp.json` should contain an SSE server whose URL matches the editor panel, for example `http://127.0.0.1:<port>/sse`.
- The editor MCP Server should show `Running` and the same port.
- If a direct MCP tool namespace is not exposed, use a small local JSON-RPC/SSE bridge only as an execution fallback.
- Treat UGCAskQ MCP as local-only and experimental; save or back up before mutation.

## Binary Asset Read Fallback

Use UGCAskQ MCP when project context depends on editor-only or binary assets that normal text search cannot inspect.

Common examples:

- `.uasset` DataTables.
- Blueprint assets.
- map actors or selected actors.
- skill editor assets.
- item, gem, monster, equipment, shop, task, or gameplay config tables stored as assets.
- asset references whose fields cannot be confirmed from Lua or text files.

Do not infer table fields from Lua code alone when the authoritative config is a `.uasset`. First use MCP to inspect table schema, row count, key fields, sample rows, and warnings. If MCP is unavailable, say the asset content is unverified and avoid claiming exact fields, rows, or values.

## Mutation Guardrails

- Do not use MCP writes as the first step. Read context and identify the smallest safe change first.
- Do not put backup `.uasset` files inside the UGC project tree. The editor can scan backup folders and reject backup names or paths, so use an external location such as `C:/Users/Administrator/Documents/CodexBackups/<ProjectName>/...`.
- Keep project-specific memories and caches outside the global skill and outside the team project unless explicitly requested.
- After table mutation, re-read row counts, key fields, missing rows, and unexpected warnings.
- After gameplay mutation, search DSlog and Clientlog for both success markers and error markers.

## Evidence Pattern

For a complete answer after MCP work, include:

- What was changed.
- Which MCP/editor verification succeeded.
- Which runtime log lines prove behavior, if runtime behavior matters.
- What was not verified, if any part could not be tested.
