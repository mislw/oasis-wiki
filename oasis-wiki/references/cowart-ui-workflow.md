# Cowart UI Workflow

1. Generate or receive a flattened UI visual.
2. Review and lock the approved visual and SHA-256.
3. Build a UI Tree with native controls, artwork candidates, skins, and composites.
4. Prefer source layer packages when they exist.
5. For bitmap-only UI, use Stage 2A Component Recognition and Stage 2B Precision Reconstruction in `cowart-ui/precision-reconstruction.md`.
6. Recompose reconstructed assets and compare the preview with the approved visual.
7. Send only reviewed candidates to the existing Stage 3 Component Confirmation flow and component library.

The workbench must preserve the distinction between `reconstruction_candidate`, reconstructed output, `pending_review`, and an explicitly confirmed active component.
