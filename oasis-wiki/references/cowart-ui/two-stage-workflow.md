# Two-stage UI workflow

## Stage 1: Visual review

The UI generator produces a complete page bitmap. Cowart is used to review and adjust the composition. This stage owns visual decisions: layout, art direction, proportion, decoration, and page readability.

Create the package with `create_visual_review.py`. The package remains `pending_visual_review` until the developer explicitly approves a final exported image with `approve_visual_review.py`.

## Stage 2: Componentization

The approved bitmap is reference evidence, not a layer source. Build the complete UI Tree and then supply either:

- A real layered export: independent transparent PNGs plus metadata, preferred for Canva Magic Layers.
- A reconstruction plan: each node is marked `reconstruction_candidate` until a replacement layer or native control is supplied.

Native UI should own text, values, progress, interaction hit areas, and state. Bitmap layers should own static skins, illustration, icons, and decoration.

## Acceptance checks

1. The visual-review checksum matches the bitmap used for componentization.
2. Every UI Tree node has one parent, numeric layer, and z-index.
3. Every movable component has a transparent asset or is still marked `candidate`.
4. Moving a child reveals its real parent/background layer, never the original flattened bitmap.
5. The reconstructed preview matches the approved visual before controls are promoted for reuse.
