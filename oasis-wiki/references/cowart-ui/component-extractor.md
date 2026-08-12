# Cowart UI Component Extractor

## Inputs

- `visual-final.png`: visually approved flattened UI image.
- `visual-review.json`: `artifact_type: visual_review`, `status: approved`, and the locked source SHA-256.
- `ui-tree.json`: `artifact_type: ui_tree` with `page_size`, nodes, bounds, categories, and optional extraction metadata.

## Commands

```powershell
python scripts/cowart-ui/component-extractor/build_extraction_plan.py `
  --ui-tree ui-tree.json --visual-review visual-review.json `
  --image visual-final.png --output extraction-plan.json

python scripts/cowart-ui/component-extractor/validate_extraction_plan.py --plan extraction-plan.json

python scripts/cowart-ui/component-extractor/build_reconstruction_jobs.py `
  --plan extraction-plan.json --output-dir reconstruction-jobs

python scripts/cowart-ui/component-extractor/recompose_ui.py `
  --plan extraction-plan.json --assets-dir . --background visual-final.png `
  --output reconstructed-preview.png

python scripts/cowart-ui/component-extractor/validate_reconstruction.py `
  --plan extraction-plan.json --assets-dir . --preview reconstructed-preview.png `
  --output reconstruction-report.json
```

`recompose_ui.py` requires Pillow because it performs real raster composition. The planning and validation scripts use only the Python standard library.

## Extraction Metadata

```json
{
  "mode": "reconstruct_skin",
  "target_component_id": "button.purchase.gold",
  "remove_content": ["cost_text", "currency_icon"],
  "transparent": true,
  "evaluate_nine_slice": true,
  "confidence": 0.96,
  "reason": "Repeated purchase controls share one reusable skin."
}
```

Use all equivalent instances when reconstructing a shared skin. Never use an arbitrary rectangular crop as a reusable component.
