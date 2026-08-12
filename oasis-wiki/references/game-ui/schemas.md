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
