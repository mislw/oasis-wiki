# Profile Schema

Store each project in one UTF-8 JSON profile with these top-level fields:

```json
{
  "schema_version": 1,
  "project": {"name": "ProjectName", "slug": "projectname", "aliases": []},
  "style_guide": {},
  "components": [],
  "pages": [],
  "history": []
}
```

Each component requires:

```yaml
component_id: button.primary.gold
name: 金色主操作按钮
category: button
description: 页面核心确认操作
usage: [保存, 确认, 升级]
states: [default, pressed, disabled, highlighted]
parent_types: [panel, popup]
layer: 60
reusable: true
visual_style: {}
interaction: {}
source: {}
confidence: 0.94
status: pending_review
version: 1
confirmed_by: null
```

History records are append-only and require timestamp, component ID, old version, new version, action, reason, and affected pages. Pages store their page ID, type, source, components, and review status.

## Project library manifests

Project-shared data lives under `.game-ui-system/`:

```text
profile.json
catalogs/assets.json
catalogs/item-icons.json
catalogs/component-assets.json
history/catalog-history.jsonl
```

`assets.json` stores project-relative source files, normalized Unreal object paths, source fingerprints, category, `catalog_status`, and an optional `sha256:` `preview_key`. It never stores an absolute cache path. `item-icons.json` maps `semantic_key` and `item_id` to the authoritative `UGCObject` icon relationship. Candidate items require `resolution_reason`. `component-assets.json` maps a component ID and each visual state to asset IDs; this mapping does not change the component status in `profile.json`.

Resolved Generation Package inputs use:

```json
{
  "source": "<runtime cache file>",
  "role": "style",
  "priority": 1,
  "copy_visual_style": true,
  "source_kind": "project_library_asset",
  "library": {
    "asset_id": "project.uiresources.common.button_confirm",
    "preview_key": "sha256:<preview-hash>",
    "component_ids": ["button.primary.gold"],
    "semantic_keys": [],
    "states": ["default"],
    "source_asset": "/Project/Asset/UIresources/Common/Button_Confirm.Button_Confirm"
  }
}
```

The runtime `source` is excluded from committed manifests and from the compiled prompt. The copied package manifest preserves the `library` provenance fields.
