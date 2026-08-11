# Cowart 组件提取与可编辑化

Use a three-stage, layer-first workflow. A flattened screenshot is a visual-review artifact only; every component that enters the editable workbench must be either an independent PNG or explicitly marked as a reconstruction candidate.

Resolve a Python runtime before running scripts. When `python` is not on PATH, use the Python path returned by `codex_app__load_workspace_dependencies`.

For a visible local control surface, launch the workflow console. It orchestrates only local scripts and local session files; all AI image generation or edits remain Codex actions in the active conversation:

```powershell
python scripts/cowart-ui/component-extractor/launch_ui_workflow_console.py --name "<page name>"
```

## Stage 0: UI specification

1. Create `ui-spec.json` from `assets/cowart-ui/ui-spec-template.json`. It owns page purpose, operations, data ownership, page size, and every UI node before any final image is generated.
2. Validate it, then serialize the reviewable UI Tree:

```powershell
python scripts/cowart-ui/component-extractor/validate_ui_spec.py <ui-spec.json>
python scripts/cowart-ui/component-extractor/build_ui_tree.py --spec <ui-spec.json> --output <ui-tree.json>
```

3. Keep text, values, counters, progress, and interactive hit targets as `asset_policy: native`. Static skins, art, icons, and decoration may use `layer`.

## Stage 0.5: reference-driven image generation

1. Resolve every original image into `style` or `layout` metadata. At least one readable Style Image is mandatory; Style Profile and art direction do not satisfy this gate.
2. Build the self-contained package:

```powershell
python scripts/game-ui/build_generation_package.py --ui-tree <ui-tree.json> --style-profile <profile.json> --references <references.json> --output <generation-package>
python scripts/game-ui/validate_generation_package.py <generation-package>
```

3. Pass all files in `generation-request.json.style_references`, all files in `layout_references`, and `generation-prompt.txt` to the active session's real image-generation tool.
4. If that capability is absent, output `IMAGE_GENERATION_UNAVAILABLE` and stop. Do not generate final artwork with HTML/CSS/Chromium.
5. After a real output exists, record it and create the pending style review:

```powershell
python scripts/game-ui/record_generation_result.py --package <generation-package> --output-image <real-generated-image.png>
python scripts/game-ui/create_style_review.py --package <generation-package>
```

## Two-stage workflow

### Stage 1: Cowart visual review

1. Generate a complete UI preview and create a review package. Formal AI output must use `ai_generated`; a user-supplied existing image may use `external_source`:

```powershell
python scripts/cowart-ui/component-extractor/create_visual_review.py --image <ui-preview.png> --name "<page name>" --source-type ai_generated --generation-package <generation-package>
python scripts/cowart-ui/component-extractor/create_visual_review.py --image <external-ui.png> --name "<page name>" --source-type external_source
```

2. Read the active project with `get_cowart_canvas_state` before insertion.
3. If `snapshot` is missing, initialize it automatically:
   - Resolve the bundled Node.js runtime with `codex_app__load_workspace_dependencies` when `node` is unavailable.
   - Run `scripts/cowart-ui/component-extractor/create_cowart_blank_snapshot.mjs --output <review-session>/cowart-blank-snapshot.json`. The script discovers the installed Cowart plugin and derives a validated blank snapshot from that plugin's own `@tldraw/editor` runtime.
   - Read the emitted JSON and call `save_cowart_canvas_state` with the exact snapshot and `protectImageRecords: true`.
   - Re-read `get_cowart_canvas_state`; require a non-null snapshot and at least one page record before continuing.
   - If generation, validation, save, or readback fails, call `render_cowart_canvas_widget`, ask for the one-time blank-page save, and retry after the user confirms. This is the failure fallback, not the default path.
4. Hand the generated bitmap to native Cowart without asking the user to copy a path:
   - Call `insert_cowart_image` with the generated bitmap and `workflowStage: visual_review`, `reviewStatus: pending_visual_review`, and the review path in `shapeMeta`.
   - For a revision, anchor it to the preceding review image and place it to the right without replacing the original.
   - Run `scripts/cowart-ui/component-extractor/record_cowart_handoff.py` with the returned page and shape IDs.
   - Re-read the canvas and verify the inserted shape, asset URL, bounds, and review metadata.
   - Call `render_cowart_canvas_widget` after successful insertion so Cowart opens with the generated UI already present.
5. The localhost workflow console cannot call Codex MCP tools and must never pretend to embed Cowart. It displays handoff status; Codex performs initialization, insertion, and native opening.
6. Iterate on layout and art direction in Cowart. This stage may use a flattened bitmap; it must not create component crops.
7. When the developer explicitly confirms the visual result, export the final bitmap and lock it:

```powershell
python scripts/cowart-ui/component-extractor/approve_visual_review.py --review <visual-review.json> --final-image <ui-final.png>
```

The approval command records a SHA-256 checksum. A later componentization run rejects an unapproved or changed image.

### Stage 2: Componentization

1. Build the complete UI Tree from the approved image. It must include every movable or dynamic element, not only the outer containers.
2. Prefer a real layered package, such as Canva Magic Layers, for `panel`, `card`, `button`, `icon`, `badge`, and decorative art.
3. Keep text, values, counters, progress, and button labels as native controls in the UI Tree. Do not bake them into bitmap layers.
4. A bitmap-only UI can produce `reconstruction_candidate` entries for review, but must not be represented as true independent layers. Create or import replacement transparent assets before marking the entries ready.
5. Only then create the workbench, passing the locked visual review:

```powershell
python scripts/cowart-ui/component-extractor/create_ui_workbench.py --image <ui-final.png> --controls <ui-tree.json> --visual-review <visual-review.json> --name "<page name>"
```

The generated preview is a composition check. The independent layer files and `layer-manifest.json` are authoritative for editing.

### Stage 3: Component confirmation

1. Export the reviewed candidate atlas and JSON from the workbench.
2. Create explicit decisions from `assets/cowart-ui/component-decisions-template.json`. Only the named decisions may become `active`.
3. Apply decisions to the user-level project profile, optionally slicing the exported atlas into reusable transparent PNGs:

```powershell
python scripts/cowart-ui/component-extractor/apply_component_decisions.py --manifest <candidates.json> --atlas <candidates.png> --decisions <decisions.json> --profile <user-profile.json>
```

4. Run `scripts/game-ui/validate_library.py` against the resulting profile. Do not write project-local profiles or UGC assets here.

## Automatic UI Generation Handoff

Every newly generated or revised game UI bitmap must enter Cowart automatically before approval:

1. Validate `ui-spec.json` and serialize its complete UI Tree.
2. Create the visual-review package.
3. Read Cowart state. If it is empty, generate a validated blank snapshot with `scripts/cowart-ui/component-extractor/create_cowart_blank_snapshot.mjs`, save it through `save_cowart_canvas_state`, and verify readback.
4. Insert the candidate into native Cowart, record its handoff, verify persistence, and then open the Cowart widget. Never require manual path pasting for Codex-generated images.
5. Preserve every prior candidate. Place revisions beside their source image.
6. Record the returned Cowart page and shape IDs with `record_cowart_handoff.py` so the workflow console shows `宸茶繘鍏?Cowart`.
7. Keep the review at `pending_visual_review` until the developer explicitly confirms it.

After approval, do not stop at the image when the user expects editable controls:

1. Validate `ui-spec.json`, serialize its complete UI Tree, then run the visual-review stage and lock the approved image with `approve_visual_review.py`.
2. Include `component_id`, `category`, `parent_id`, `layer`, `z_index`, `bounds`, `asset_policy`, and `status` for every node.
3. Run:

```powershell
python scripts/cowart-ui/component-extractor/create_ui_workbench.py --image <ui-final.png> --controls <ui-tree.json> --visual-review <visual-review.json> --name "<page name>"
```

4. Return the printed local URL as a clickable link. The script also creates `Open UI Workbench.url` beside the session files.
5. Keep all generated controls at `pending_review` or `candidate`; never mark them `active` automatically.

If no UI Tree is supplied, the script creates only one `candidate` source-image node. This is a failure-safe fallback, not automatic component recognition. It is allowed only with `--allow-unreviewed` for diagnostics, never for a component handoff.

## Workflow

1. Inspect the export without changing the source. Prefer a directory containing metadata JSON plus element PNG files. Unpack ZIP files into a new working directory first.
2. Read [layer-manifest.md](references/cowart-ui/layer-manifest.md) before mapping a new exporter.
3. Normalize the export:

```powershell
python scripts/cowart-ui/component-extractor/normalize_canva_export.py --input <export-dir-or-json> --output <normalized-dir>
```

Use `--allow-png-fallback` only when metadata is absent. Fallback nodes are `candidate`, start at `(0, 0)`, and require manual placement.

4. Validate the package:

```powershell
python scripts/cowart-ui/component-extractor/validate_manifest.py <normalized-dir>/layer-manifest.json
```

Stop on any validation error. Do not silently repair cycles, missing files, duplicate IDs, invalid bounds, or `active` status.

5. Generate the import plan:

```powershell
python scripts/cowart-ui/component-extractor/build_cowart_shape_plan.py <normalized-dir>/layer-manifest.json --output <normalized-dir>/cowart-shape-plan.json
```

6. Review the UI Tree before Cowart import. Every node must have one parent, one numeric layer, one z-index, and `pending_review` or `candidate` status. Never auto-promote a node to `active`.
7. Read Cowart state for the user's active working directory. When the canvas has no saved snapshot, create one with `scripts/cowart-ui/component-extractor/create_cowart_blank_snapshot.mjs`, save it through Cowart MCP, and verify readback. Use manual blank-page saving only as the failure fallback.
8. Import each PNG with `insert_cowart_image`. Put `componentId`, `logicalParentId`, `layer`, `zIndex`, `sourceBounds`, and `reviewStatus` into `shapeMeta`. Keep the original reference image and all existing shapes. After a successful import, call `render_cowart_canvas_widget` so the user sees the result immediately.
9. Use `get_cowart_canvas_state`, then update only the newly inserted shape IDs to the plan coordinates and ordering through `save_cowart_canvas_state`. Preserve all unrelated records. Parent-child movement is represented by the plan's nested `move_groups`; apply grouping only when the Cowart snapshot schema validates it. If grouping cannot be validated, retain logical parent metadata and report the limitation instead of risking the canvas.
10. Re-read the canvas and confirm all expected layer shapes exist, have correct bounds, and do not cover unrelated content.

## Gates

- Prefer full-canvas transparent PNGs. Cropped PNGs are valid only when metadata includes exact page-space bounds.
- Preserve rotation, opacity, masks, text metadata, source element IDs, and page dimensions when available.
- Keep uncertain or incomplete imports as `candidate` with a reason.
- Keep complete new imports as `pending_review`.
- Never write UGC Lua, WidgetBlueprint, `.uasset`, or `.umap` files from this Skill.
- Never replace, delete, hide, or move the source image or pre-existing Cowart shapes.
- Never infer missing hierarchy from visual overlap alone. Use exporter group data or request review.

## Exporter Adapters

All Canva-specific aliases live in `scripts/cowart-ui/component-extractor/canva_adapter.py`. When a real plugin sample uses different field names, update only that adapter and its tests. Keep `layer-manifest.json` stable.

## Outputs

The normalized directory contains:

```text
layer-manifest.json
cowart-shape-plan.json
layers/<component-id>.png
```

The manifest is authoritative for UI Tree review. The shape plan is an intermediate import contract, not a replacement for the manifest.
