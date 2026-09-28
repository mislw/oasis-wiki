# UI Delivery Contract

Use this reference when an approved UI visual is moving through Workbench, WidgetBlueprint delivery, Lua rebinding, or final review. The contract joins evidence that was previously scattered across images, chat approvals, Workbench snapshots, MCP reads, and PIE logs.

## Purpose

A contract prevents these failure classes:

- an exact reusable background is silently redrawn;
- a stale Workbench layout or stale MCP snapshot is reused after another edit;
- a correct convenience texture field hides a missing `Brush.ResourceObject`;
- a window is visually compensated with negative coordinates or the wrong root space;
- `Auto Size`, render scaling, clipping, or scrollbar reservation changes final geometry;
- property readback is reported as visual or functional verification;
- prompts, audit scripts, manifests, or temporary files enter the UGC project and block validation.

## Artifact

Use `artifact_type: ui_delivery_contract` and `schema_version: 1`. Keep the contract and every audit output outside the UGC project.

Required sections:

```json
{
  "schema_version": 1,
  "artifact_type": "ui_delivery_contract",
  "project": {
    "slug": "project-slug",
    "root": "D:/path/to/UGCProject"
  },
  "outputs": {
    "root": "C:/Users/<user>/.codex/ui-audits/page-id"
  },
  "visual": {
    "status": "approved",
    "path": "D:/external/approved.png",
    "sha256": "...",
    "width": 1920,
    "height": 1080
  },
  "layout": {
    "page_id": "page-id",
    "revision": 3,
    "session_path": "D:/external/session.json",
    "session_sha256": "...",
    "layout_review_path": "D:/external/layout-review.json",
    "layout_review_sha256": "..."
  },
  "target": {
    "load_path": "/Project/Asset/UI/Page.Page",
    "snapshot_path": "D:/external/umg-snapshot.json",
    "snapshot_sha256": "...",
    "root": {
      "name": "CanvasPanel_0",
      "size": [1920, 1080],
      "coordinate_space": "full_viewport"
    },
    "required_controls": [
      {
        "name": "Image_Background",
        "class": "Image",
        "require_brush_resource": true
      },
      {
        "name": "Button_Close",
        "class": "Button"
      }
    ],
    "layout_rules": {
      "forbid_negative_positions": true,
      "forbid_auto_size": ["Image_Background"],
      "scrollbars": [
        {"name": "ScrollBox_Content", "visibility": "Collapsed"}
      ]
    }
  },
  "verification": {
    "property_readback": "pass",
    "designer_visual": "pass",
    "designer_screenshot": "D:/external/designer.png",
    "designer_screenshot_sha256": "...",
    "pie": "not_run"
  }
}
```

The MCP-created `umg-snapshot.json` contains the current root and a `widgets` array. Record each audited widget's class, parent, position, size, anchors, alignment, `auto_size`, render scale, visibility, brush image, `Brush.ResourceObject`, and scrollbar visibility when applicable.

## Visual Lock

When a background, frame, logo, or other project component must remain exact, create an editable mask whose nonzero pixels are the only pixels generation may change. Run:

```powershell
python scripts/game-ui/verify_ui_visual_lock.py `
  --baseline <approved-source.png> `
  --candidate <generated-candidate.png> `
  --editable-mask <editable-mask.png> `
  --report <external-output>/visual-lock.json `
  --diff-image <external-output>/visual-lock-diff.png
```

Any changed pixel outside the mask returns exit code `2`, status `fail`, and must be reported as `UI_VISUAL_LOCK_FAILED`. Do not continue to visual approval or slicing. A prompt saying "preserve the background" is not evidence of preservation.

## Contract Validation

After MCP readback and Designer review, run:

```powershell
python scripts/game-ui/validate_ui_delivery_contract.py `
  <external-output>/ui-delivery-contract.json `
  --report <external-output>/ui-delivery-validation.json
```

The validator checks current hashes, Workbench source freshness, exact target identity, root geometry, required controls, brush resources, negative-position policy, `Auto Size`, scrollbar policy, Designer evidence, and project-external output placement.

## Designer-first Verification

Keep the three evidence levels separate:

1. **属性回读**: MCP proves serialized values, names, types, hierarchy, references, and saved state.
2. **Designer 视觉**: the reopened WidgetBlueprint proves layout, clipping, Z-order, text proportion, texture rendering, and hit-region placement.
3. **PIE 功能**: mobile PIE proves creation, runtime data, button callbacks, state switching, refresh, and close behavior.

Designer-first means every layout or style iteration stops at Designer visual review. Run PIE after the Designer result is accepted, or earlier only when the symptom is runtime-only. Never report one level as proof of another.

## Staleness

Recompute the contract whenever any of these changes:

- approved visual bytes or editable mask;
- Workbench bounds, parent, Z-order, classification, revision, or session;
- target `load_path`, WidgetTree, brush, slot, anchor, visibility, or runtime-facing control;
- Designer screenshot;
- Lua binding plan or Switcher state contract.

An old successful report does not apply to changed bytes. Re-read, rebuild the snapshot, and rerun validation.

## Project Hygiene

Audit scripts, prompts, JSON manifests, screenshots, diff images, temporary source files, and backups must not be written into the UGC project directory. Use the UI library, `%CODEX_HOME%`, or another project-external audit root. Before PIE, inspect unexpected project artifacts and run the project's normal filename, suffix, and Lua validators.
