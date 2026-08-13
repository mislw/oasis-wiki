# Layer Reconstruction / Clean Layer Extraction

Use this workflow only after the flattened UI bitmap has been visually approved. The bitmap proves appearance, but it is not an editable layer package.

## Required pipeline

```text
Flattened UI
-> UI Tree Inference
-> Manual Correction
-> Node Classification
-> Layer Reconstruction
-> Assembly Validation
-> Component Library / Export
```

Layer Reconstruction covers every independently movable visual level, including `background.root`, panels, cards, buttons, and artwork. Native text, values, timers, progress, labels, and hit targets remain native and never produce bitmap layers.

## Visual asset contract

Every node uses exactly these visual asset fields:

- `source_crop`: provenance and comparison input. It may contain children, text, icons, shadows, or other baked content. It is never a reusable layer.
- `clean_layer`: the reconstructed visual owned by this node. Descendant visuals and native content are removed, and all removed regions are repaired with coherent background, edges, material, and texture.
- `assembly_preview`: validation output assembled from clean layers, artwork, and native placeholders. It is never a component asset.

A rectangular crop, transparent hole, flat fill, browser paint, HTML/CSS render, Canvas fill, or Chromium screenshot is not a `clean_layer`.

## Node behavior

- `background.root`: remove every visible foreground node and reconstruct the complete root background.
- `composite`: may own a `clean_layer` for its background while retaining children as independently movable nodes. It is not automatically reusable as a component-library bitmap.
- `skin`: reconstruct the clean button, panel, frame, badge, header, card, or slot skin.
- `artwork`: extract a complete transparent artwork layer and repair occluded edges.
- `native`: keep `clean_layer: null` and `layer_reconstruction.status: not_applicable`.

Do not create a derived `panel.main.background` source crop to hide the problem. The owning parent node carries its own `clean_layer`.

## Hierarchy order

Reconstruction is post-order: leaves are confirmed first, then their parents, and `background.root` is last.

```text
Text -> Native
Button -> clean button layer
Artwork -> transparent artwork layer
Panel -> remove Button + Artwork + visible descendants -> clean panel layer
Root -> remove Panel + all foreground descendants -> clean root background
```

Each parent records direct children, visible descendants, native descendants, and artwork descendants. The final removal mask is a deduplicating pixel union; the same pixel must not be applied twice.

## Mask priority

Use the highest available source for each removed node:

1. Explicit child alpha or mask.
2. Reconstructed child `clean_layer` alpha.
3. Semantic segmentation mask.
4. Bounds plus padding fallback.

Bounds are planning and fallback metadata only. They are never proof of precise extraction.

## Planning and execution

The existing scripts remain the pipeline entry points:

```text
build_extraction_plan.py          # emits schema 3 layer_reconstruction_plan
build_reconstruction_jobs.py      # provider-neutral jobs in leaf-to-root order
execute_reconstruction_jobs.py    # pluggable ImageReconstructionExecutor
recompose_ui.py                   # clean layers + native placeholders only
validate_reconstruction.py        # executor, PNG, assembly provenance, movement evidence
```

`ImageReconstructionExecutor` is defined in `image_reconstruction_executor.py`. Providers must implement the `image_edit_inpainting` capability. Codex ImageGen, OpenAI Images, or another provider can be connected without changing the plan/job schema.

No executor is bundled by default. When no capable executor is configured, execution fails closed with:

`LAYER_RECONSTRUCTION_UNAVAILABLE`

No output file is created and `clean_layer` remains null in the node/session data.

## Workbench status

The Workbench uses this state sequence:

```text
requested
-> job_created
-> waiting_executor
-> reconstructing
-> reconstructed
-> validation
-> ready
```

Any error transitions to `failed` with a visible reason. The browser may request an external executor through `window.cowartReconstructionExecutor`; it must never reconstruct pixels locally.

## Assembly and residual validation

Assembly Preview may use only:

- clean root background
- clean parent layers
- clean child layers
- artwork layers
- native placeholders

It must never use `source_crop` as an assembly layer.

Acceptance requires both movement checks:

1. Move a child from A to B. A must show only the expected parent clean layer, with no button, text, icon, shadow, or badge residue.
2. Move a parent panel. Its original location must show only `background.root.clean_layer`, and all descendants must move with the parent.

The Python tests provide deterministic pixel fixtures for both checks. Real UI output still requires executor evidence and developer visual review before component confirmation.
