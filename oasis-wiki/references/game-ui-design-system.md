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
- Store user references as structured objects with `source`, `role`, and numeric `priority`; `role` is only `style` or `layout`.
- When the user supplies visual references, copy the original files into a Generation Package and pass them to the final image-generation call. The Style Profile is supplementary and must not replace them.
- Require at least one readable Style Image with recorded dimensions and SHA-256. Layout references must set `copy_visual_style: false`.
- Prefer the Codex built-in `image_gen` backend with `codex_managed` credentials. Never request a user Key or use a generic CLI fallback.
- When the active session has no built-in `image_gen`, stop with `IMAGE_GENERATION_UNAVAILABLE` unless the user explicitly authorizes the `codex_provider_direct` fallback. That fallback resolves the current Codex provider's channel-prefixed `gpt-image-2` model and uses Codex-managed authentication without printing or persisting credentials. Never fall back to HTML/CSS/Chromium screenshots.
- Give every control one parent and one numeric layer.
- Store uncertain recognition as `candidate` with confidence and reason.
- Store new controls as `pending_review`; only explicit developer confirmation may set `active`.
- Preserve old versions and append history for every correction.
- Stop final generation when the UI Tree is missing, a parent is missing, serious layer/interaction conflicts exist, a deprecated/rejected control is used, or a known control was redesigned without approval.

## Project libraries

A project library combines project-owned manifests under `.game-ui-system/` with a derived user-local preview cache. Run `initialize_project_library.py`, `index_project_assets.py`, `import_project_previews.py`, `build_item_icon_catalog.py`, and `resolve_project_references.py` in that order before building a page that depends on existing project assets.

An asset with `catalog_status: classified` is not an `active` component. Only explicit developer confirmation may promote a component to `active`. Local cache paths never enter committed manifests; catalogs store `sha256:` preview keys, and generated reference metadata uses `source_kind: project_library_asset` when resolving the corresponding local file.

## Oasis integration

- Use this branch for visual structure and reusable style decisions.
- Use `references/mcp-ui-widget.md` only when real WidgetBlueprint inspection or mutation is needed.
- Use `references/feature-development-flow.md` for Lua, RPC, events, data ownership, and runtime refresh.
- Read project files freely. Modify UGC code, `.uasset`, `.umap`, or project-local profiles only with explicit authorization.
- Keep writable component profiles under `%USERPROFILE%/.codex/game-ui-design-system/projects/<slug>/profile.json` by default.
- Use `scripts/game-ui/build_generation_package.py` and `scripts/game-ui/validate_generation_package.py` before formal bitmap generation. Use `record_generation_result.py` and `create_style_review.py` before an `ai_generated` Cowart handoff.
- Pass resolved project assets with `--library-references`; only explicit `--references` participate in UI Tree reference alignment.

## Save validation

Run:

```powershell
python scripts/game-ui/validate_library.py --profile <profile.json>
```

If `python` is unavailable, use the configured Codex workspace Python runtime. A failed validation must not replace the last valid profile.
