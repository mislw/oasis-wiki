# Layer Manifest Contract

## Package layout

```text
normalized-export/
  layer-manifest.json
  cowart-shape-plan.json
  source/
  layers/
  preview/
```

## Schema 3 node

```json
{
  "schema_version": 3,
  "source": {
    "page_size": {"width": 1280, "height": 720}
  },
  "components": [
    {
      "component_id": "panel.main",
      "parent_id": "root",
      "children": ["button.draw.single", "artwork.pool"],
      "node_kind": "composite",
      "render_mode": "outline",
      "asset_policy": "reconstruction_candidate",
      "layer": 20,
      "z_index": 10,
      "bounds": {"x": 100, "y": 80, "width": 900, "height": 520},
      "status": "candidate",
      "visual_assets": {
        "source_crop": "source/panel.main.png",
        "clean_layer": null,
        "assembly_preview": null
      },
      "layer_reconstruction": {
        "status": "pending",
        "remove_nodes": ["button.draw.single", "text.draw.single", "artwork.pool"],
        "direct_children": ["button.draw.single", "artwork.pool"],
        "visible_descendants": ["button.draw.single", "text.draw.single", "artwork.pool"],
        "native_descendants": ["text.draw.single"],
        "artwork_descendants": ["artwork.pool"],
        "mask": {
          "operation": "union",
          "deduplicate_pixels": true,
          "priority": ["alpha_mask", "clean_layer_alpha", "semantic_mask", "bounds_fallback"],
          "sources": []
        },
        "method": "image_reconstruction",
        "transparent": true,
        "error": null
      },
      "review": {
        "status": "candidate",
        "cleanup_status": "pending"
      },
      "reusable_bitmap": false
    }
  ]
}
```

## Required behavior

- New manifests use `schema_version: 3`.
- `visual_assets` contains exactly `source_crop`, `clean_layer`, and `assembly_preview`.
- `source_crop` and `assembly_preview` cannot satisfy a clean-layer or component activation gate.
- Every independently movable non-Native visual node may own a `clean_layer`, including Composite parents and `background.root`.
- Native nodes keep `clean_layer: null` and `layer_reconstruction.status: not_applicable`.
- A reusable Skin/Artwork additionally requires `clean_layer`, `layer_reconstruction.status: ready`, and developer confirmation.
- Composite clean layers may render in Cowart and Assembly Preview but do not automatically become reusable library components.
- All paths stay inside the package; bounds stay inside the page; parent references are acyclic.

## Reconstruction states

Valid states are:

`not_applicable`, `pending`, `requested`, `job_created`, `waiting_executor`, `reconstructing`, `reconstructed`, `validation`, `ready`, `failed`.

`failed` must include an error reason. Missing image-edit capability uses `LAYER_RECONSTRUCTION_UNAVAILABLE`.

## Root background

Every flattened-UI reconstruction plan includes `background.root`. It covers the full page, removes every visible foreground node through a deduplicated union mask, and is reconstructed last.

## Cowart shape plan

The shape plan imports only nodes that have a validated `clean_layer` and `layer_reconstruction.status: ready`. This includes clean Composite visual layers for editing, while the component-library activation gate remains limited to approved Skin/Artwork nodes. Nested `move_groups` retain the complete logical hierarchy so moving a parent also moves its descendants.

Schema 1 and schema 2 may be read for migration, but new normalization and Workbench exports emit schema 3.
