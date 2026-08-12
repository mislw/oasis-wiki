# Precision Component Reconstruction

Use this workflow only after a flattened UI image has been visually approved. A flat screenshot is evidence of appearance, not proof of the original editable layers.

## Stage 2A: Component Recognition

Create a UI Tree that records bounds, category, and extraction metadata for every candidate. Group visually equivalent instances under one `target_component_id`; a six-offer exchange screen should produce one `button.purchase.gold` skin with six instances, not six cropped buttons.

Choose one mode per node:

- `native`: text, numbers, prices, timers, counters, progress, labels, and hit targets. These never output PNG files.
- `extract_artwork`: artwork, hero portraits, equipment, resource icons, and other isolated visuals. Output is a transparent PNG.
- `reconstruct_skin`: panels, cards, buttons, frames, badges, headers, and scrollbars. Remove baked dynamic content, reconstruct the covered skin, record nine-slice suitability, and output a transparent PNG.
- `composite`: complex cards assembled from children and layout. Composite nodes do not export a flattened bitmap by default.

For each candidate, set `asset_policy: reconstruction_candidate`. That state cannot be treated as a library layer until the asset is reconstructed and reviewed.

The schema 2 representation separates three files throughout Stage 2:

- `source_crop`: raw evidence, allowed to contain children and native content.
- `clean_asset`: reconstructed or independently extracted reusable Skin/Artwork.
- `assembly_preview`: clean parent plus children and native placeholders, used only for comparison.

For a parent that contains independently controlled children, keep the parent as `node_kind: composite` and reconstruct a dedicated `*.background` Skin. Composite defaults to `render_mode: outline`; Native defaults to `outline` or `hidden`. Neither may become a bitmap library asset.

## Stage 2B: Precision Reconstruction

1. Run `build_extraction_plan.py` with `ui-tree.json`, approved `visual-review.json`, and the locked visual image.
2. Run `validate_extraction_plan.py`. It rejects active status, unsafe paths, bitmap output for native/composite nodes, and a skin with neither `remove_content` nor a clean source.
3. Run `build_reconstruction_jobs.py`. Each reusable target produces exactly one job, even when it has many instances.
4. Perform semantic masking, text and icon removal, alpha separation, and occlusion repair with an image-edit model or a developer. The local scripts do not pretend to perform those semantic edits.
5. Save transparent PNGs at each plan output path and run `recompose_ui.py` to place them back at every recorded position.
6. Run `validate_reconstruction.py`. It checks files, PNG type, alpha support, preview existence, and review state. Its visual similarity is deliberately `null` because a developer must compare the preview with the approved source.

The Workbench `净化母版` action may create or queue the reconstruction job and reflect status, but it must not perform browser-side pixel filling. A Skin remains `needs_cleanup` until a real `clean_asset` is loaded and validated.

## Review Gate

Every planned component remains `candidate` or `pending_review`. Reconstruction does not grant `active`. The activation Gate rejects Composite, Native, missing `clean_asset`, non-clean cleanup state, and source/assembly-only nodes. Only the existing Stage 3 Component Confirmation and a developer decision may add a clean Skin/Artwork component to the library.
