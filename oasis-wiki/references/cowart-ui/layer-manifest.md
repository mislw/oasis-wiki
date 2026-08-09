# Layer Manifest Contract

## Package layout

```text
normalized-export/
  layer-manifest.json
  cowart-shape-plan.json
  layers/
    panel.shop.root.png
    button.purchase.primary.png
```

## Canonical manifest

```json
{
  "schema_version": 1,
  "batch_id": "20260808T120000Z",
  "source": {
    "kind": "canva_magic_layers",
    "manifest_file": "export.json",
    "page_size": {"width": 1280, "height": 720}
  },
  "components": [
    {
      "component_id": "button.purchase.primary",
      "element_id": "canva-element-42",
      "name": "Purchase button",
      "category": "button",
      "file": "layers/button.purchase.primary.png",
      "parent_id": "panel.shop.root",
      "layer": 60,
      "z_index": 42,
      "bounds": {"x": 900, "y": 590, "width": 230, "height": 72},
      "rotation": 0,
      "opacity": 1,
      "mask": null,
      "text": null,
      "status": "pending_review",
      "reason": null
    }
  ],
  "ui_tree": {
    "root_id": "root",
    "children": ["panel.shop.root"]
  },
  "warnings": []
}
```

## Required fields

- `source.page_size.width` and `height` must be positive.
- Each component needs a unique lowercase dot-separated `component_id`.
- `file` must resolve inside the normalized package.
- `parent_id` must be `root` or another component ID.
- `layer` and `z_index` must be numeric.
- `bounds` must be positive and remain within the page.
- `status` must be `pending_review` or `candidate`.
- Parent references must be acyclic.

## Canva adapter aliases

The first version accepts common aliases:

| Canonical | Accepted aliases |
|---|---|
| elements | `elements`, `layers`, `components`, `items` |
| element ID | `element_id`, `elementId`, `id`, `uuid` |
| file | `file`, `fileName`, `filename`, `asset`, `image` |
| parent | `parent_id`, `parentId`, `group_id`, `groupId`, `parent` |
| z-index | `z_index`, `zIndex`, `z`, `order`, `index` |
| bounds | `bounds`, `rect`, `frame`, or direct `x/y/width/height` |
| page size | `page_size`, `pageSize`, `canvas`, `page`, or direct `width/height` |

The existing component workbench format is also accepted: `source_size`, `source_rect`, `layout_rect`, and `atlas_rect`. Put `redcliff-component-candidates.json` beside `redcliff-component-candidates.png`; the normalizer splits the atlas into one PNG per component.

Unknown exporter fields stay under `source_fields` so no source evidence is lost.

## PNG-only fallback

PNG-only input cannot recover position, parent, rotation, or z-order reliably. The fallback mode therefore:

- assigns every file to `root`
- uses file order as `z_index`
- places every layer at `(0, 0)` using its bitmap dimensions
- sets `status: candidate`
- records a warning and a review reason

Do not treat fallback output as a completed UI Tree.

## Cowart shape plan

The plan contains one image node per component plus nested `move_groups`. Each node carries the canonical component ID and logical parent. An importer must preserve the original canvas records, insert new assets through Cowart MCP, then update only the returned new shape IDs.
