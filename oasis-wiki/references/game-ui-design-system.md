# Game UI Design System

Use this branch for UI screenshots, component extraction/correction, project style libraries, UI Tree planning, UI generation, hierarchy review, and visual consistency checks.

## Start

1. Run `scripts/game-ui/detect_project.py --cwd <current-directory>`.
2. Load the first available profile using `references/game-ui/project-routing.md`.
3. Read only the task reference:

| Task | Reference |
|---|---|
| Screenshot analysis, extraction, correction, new page | `references/game-ui/workflow.md` |
| Profile/component fields or file updates | `references/game-ui/schemas.md` |
| Hierarchy, occlusion, style review | `references/game-ui/validation-rules.md` |
| Required response order and report fields | `references/game-ui/output-templates.md` |

## Mandatory gates

- Search the resolved project library before creating a control or page.
- Build a complete UI Tree before prompts, images, Figma notes, UMG hierarchies, or code.
- Give every control one parent and one numeric layer.
- Store uncertain recognition as `candidate` with confidence and reason.
- Store new controls as `pending_review`; only explicit developer confirmation may set `active`.
- Preserve old versions and append history for every correction.
- Stop final generation when the UI Tree is missing, a parent is missing, serious layer/interaction conflicts exist, a deprecated/rejected control is used, or a known control was redesigned without approval.

## Oasis integration

- Use this branch for visual structure and reusable style decisions.
- Use `references/mcp-ui-widget.md` only when real WidgetBlueprint inspection or mutation is needed.
- Use `references/feature-development-flow.md` for Lua, RPC, events, data ownership, and runtime refresh.
- Read project files freely. Modify UGC code, `.uasset`, `.umap`, or project-local profiles only with explicit authorization.
- Keep writable component profiles under `%USERPROFILE%/.codex/game-ui-design-system/projects/<slug>/profile.json` by default.

## Save validation

Run:

```powershell
python scripts/game-ui/validate_library.py --profile <profile.json>
```

If `python` is unavailable, use the configured Codex workspace Python runtime. A failed validation must not replace the last valid profile.
