# Layer Manifest Contract

## Package layout

```text
normalized-export/
  layer-manifest.json
  cowart-shape-plan.json
  source/
    panel.shop.root.png
  layers/
    button.purchase.primary.png
  preview/
    panel.shop.root.png
```

## Canonical manifest

```json
{
  "schema_version": 2,
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
      "node_kind": "skin",
      "render_mode": "bitmap",
      "parent_id": "panel.shop.root",
      "children": ["text.purchase.price"],
      "layer": 60,
      "z_index": 42,
      "bounds": {"x": 900, "y": 590, "width": 230, "height": 72},
      "rotation": 0,
      "opacity": 1,
      "mask": null,
      "text": null,
      "status": "pending_review",
      "reason": null,
      "visual_assets": {
        "source_crop": "source/button.purchase.primary.png",
        "clean_asset": "layers/button.purchase.primary.png",
        "assembly_preview": null
      },
      "review": {
        "status": "pending_review",
        "cleanup_status": "clean"
      },
      "reusable_bitmap": true
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
- `node_kind` must be `composite`, `skin`, `artwork`, or `native`.
- `render_mode` must be `bitmap`, `outline`, `ghost`, `assembly`, or `hidden`.
- `visual_assets` always distinguishes `source_crop`, `clean_asset`, and `assembly_preview`; every non-null path must resolve inside the normalized package.
- `composite` and `native` do not require bitmap files. Their source crops are trace/debug evidence only.
- `skin` and `artwork` are reusable only when `clean_asset` exists and `review.cleanup_status` is `clean`.
- `parent_id` must be `root` or another component ID.
- `layer` and `z_index` must be numeric.
- `bounds` must be positive and remain within the page.
- `status` and `review.status` must remain `pending_review` or `candidate`.
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

Schema 1 remains readable for older packages. New normalizations emit schema 2. Unknown exporter fields stay under `source_fields` so no source evidence is lost.

## Node and asset semantics

- `composite` defaults to `outline` and belongs in the Workbench Structure view. A parent source crop may contain children, so it must never be used as a reusable bitmap.
- `skin` and `artwork` default to `bitmap`, but the canvas and Cowart shape plan use only `clean_asset`.
- `native` defaults to `outline` or `hidden` and remains an editor/UMG control.
- `source_crop` is provenance, `clean_asset` is the reusable file, and `assembly_preview` is a recomposition check. Neither source nor assembly can satisfy the activation gate.
- When a reconstructable node also has children, keep the original node as `composite` and create a sibling child such as `panel.main.background` or `button.draw.single.background` as `skin`.

## PNG-only fallback

PNG-only input cannot recover position, parent, rotation, or z-order reliably. The fallback mode therefore:

- assigns every file to `root`
- uses file order as `z_index`
- places every layer at `(0, 0)` using its bitmap dimensions
- sets `status: candidate`
- records a warning and a review reason

Do not treat fallback output as a completed UI Tree.

## Cowart shape plan

The plan contains image nodes only for clean `skin` and `artwork` assets, while nested `move_groups` retain every Composite/Native/Skin/Artwork node. Each image carries the canonical component ID and logical parent. An importer must preserve the original canvas records, insert new assets through Cowart MCP, then update only the returned new shape IDs.
