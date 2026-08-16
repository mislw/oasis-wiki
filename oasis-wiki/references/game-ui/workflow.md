# Workflow

## 0. Project library preparation

Use this order for a project-backed page:

```text
detect project
-> load project profile
-> validate/index assets
-> import external editor exports into local cache
-> synchronize UGCObject read-only export
-> review state families
-> confirm components active
-> resolve project references
-> build UI Tree
-> build and validate Generation Package
-> ImageGen
-> Cowart review
```

The editor export step is read-only: export PNG/TGA/JPEG files to a user-local staging directory, normalize them with `import_project_previews.py`, and review the generated contact sheets. Duplicate export stems require an explicit asset-to-file mapping. Synchronize item names, descriptions, and icons from a normalized `UGCObject` export with `build_item_icon_catalog.py`; do not parse `.uasset` binary strings.

Review state families before mapping assets to components. A classified raw asset is not an active component. After explicit confirmation, use `resolve_project_references.py --library-root <project>/.game-ui-system` and pass its output to `build_generation_package.py --library-references`.

## 1. Reference image analysis

1. Identify page type, purpose, and main operations.
2. Divide background, header, navigation, content, detail, action, popup, hint, and mask regions.
3. Build the complete UI Tree with parent and layer for every node.
4. Extract controls and match them against the resolved project library.
5. Record name, ID, category, purpose, page, parent, layer, states, reuse, similarity, confidence, and status.
6. Put uncertain results in `candidate` and explain why.
7. Validate hierarchy before proposing library changes.

## 2. Component extraction

- Use lowercase dot-separated IDs in the form `type.purpose.state`.
- Reuse confirmed definitions without changing core shape, palette, border, highlight, shadow, material, interaction meaning, or states.
- Use instance numbers only for identical repeated controls inside a page.
- Store a high-confidence but unconfirmed extraction as `pending_review`, not `active`.

## 3. New page generation

1. Parse page name, purpose, scene, operations, information, ratio, references, and requested deliverables.
2. Resolve each original image as a structured `style` or `layout` reference. Layout references default to `copy_visual_style: false`.
3. Classify controls as direct reuse, state extension, or new candidate.
4. Create new controls as `pending_review` and state why existing controls cannot satisfy the need.
5. Build the complete UI Tree.
6. Resolve approved project-library assets, then build and validate a Generation Package containing explicit references, supplemental `project_library_asset` references, their dimensions and SHA-256, the UI Tree, Style Profile, compiled prompt, and generation request.
7. Invoke the Codex built-in `image_gen` tool with every listed Style Image, every listed Layout Image, and the compiled prompt. Codex manages credentials; do not request a user Key. If the tool is unavailable, stop with `IMAGE_GENERATION_UNAVAILABLE` unless the user explicitly authorizes `codex_provider_direct`; the authorized runner resolves the current provider's channel-prefixed `gpt-image-2` model and uses Codex-managed authentication. Never use HTML/CSS/Chromium as a final-image fallback.
8. Record only a real output with `record_generation_result.py`, then create a qualitative style review.
9. Send the validated result to Cowart as `ai_generated`; use `external_source` only for an existing image supplied directly by the user.
10. Finish with the automatic check report.

Hard rules:

- Style Profile is supplementary. It MUST NOT replace real Style Reference images when the user supplied them.
- Layout references control information hierarchy and approximate placement only. They MUST NOT provide visual styling.
- HTML/CSS/Chromium screenshots are not Final Game UI Visual Generation.
- No valid Style Image means generation must fail even when `art_direction`, a prompt, or a project profile exists.

## 4. Developer commands

### `控件修正：`

Locate the control, show the old summary, apply the correction, check conflicts, increment the version, append history, deprecate or reject the wrong version, list affected pages, and report revalidation work.

### `确认控件：`

Require an exact component ID. Set it to `active`, record `confirmed_by: developer`, append history, and validate the profile.

### `拒绝控件：`

Require an exact component ID and reason. Set it to `rejected`, append history, find affected pages, and prohibit future reuse.
