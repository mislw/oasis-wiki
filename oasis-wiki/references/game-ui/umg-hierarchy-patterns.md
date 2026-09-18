# UMG Hierarchy Patterns

Use this reference when comparing two existing WidgetBlueprints, learning from a stronger hierarchy, planning reusable Item/List controls, or deciding whether a visually similar asset can replace a live UI. This is a structure and runtime-contract audit, not permission to mutate project assets.

## Core Principle

A better tree is not simply the tree with fewer widgets, more nesting, or newer artwork. Prefer the hierarchy that makes ownership, repeated content, runtime state, layout behavior, and input boundaries explicit while preserving the complete live UI contract.

Evaluate four things separately:

1. Visual composition: what the player sees.
2. Structural ownership: which component owns each movable bundle.
3. Runtime contract: which controls Lua, Blueprint, animation, config, and refresh code require.
4. Layout and input behavior: anchors, slots, clipping, Z-order, visibility, and hit regions.

Do not infer one category from another. A clean-looking tree can be unbound; a dense legacy tree can still be the only functional implementation.

## Read-Only Audit Workflow

### 1. Freeze the comparison targets

Record the exact object paths, classes, package dirty state, source revision when known, and whether each asset is live, experimental, or historical. Inspect both assets without saving them.

When the worktree is dirty, distinguish current unsaved/editor changes from the committed reference. Do not restore, delete, or replace binary assets during an audit.

### 2. Inventory the runtime contract first

Before grading the candidate hierarchy, search the live UI loader and associated Lua/Blueprint code. Record:

- the asset path loaded by the UI manager or factory;
- every named `Button`, `TextBlock`, `ProgressBar`, `WidgetSwitcher`, list, item widget, and custom child accessed at runtime;
- button/event bindings and their teardown;
- refresh functions and their data owners;
- dynamic texture, text, progress, quality, lock, quantity, and visibility updates;
- any animation, RPC, config, save, replication, or reconnect dependency that reaches the UI;
- initial visibility states that are intentionally `Collapsed`, `Hidden`, `HitTestInvisible`, or `SelfHitTestInvisible`.

Treat this inventory as the replacement contract. A candidate is not a drop-in replacement until every required surface is present or has an explicit, minimal compatibility mapping.

### 3. Capture both trees at the same resolution

For every widget, collect:

- name, class, parent, depth, and child order;
- slot class;
- anchors, offsets, alignment, auto-size, padding, size rule, and Z-order;
- visibility, enabled state, clipping, render opacity, and render transform;
- class-specific constraints such as `SizeBox` overrides, `WidgetSwitcher` index, list Item class/size/gap/cache, and Button style;
- `Image.Brush.ResourceObject`, not only a convenience texture field.

Useful summary metrics include widget count, maximum depth, generic-name count, repeated manual children, reusable Item classes, and missing runtime controls. Metrics describe the tree; they do not decide quality by themselves.

### 4. Compare by responsibility

Build a component map instead of comparing only same-named nodes:

```text
viewport/root
window/frame
header/title/close
content section A
content section B
progress/status
primary action
secondary action and non-clickable cost
reusable item
state presentation
```

For each responsibility, mark the candidate pattern as:

- `keep`: structurally and behaviorally sound;
- `adapt`: good ownership, but naming, sizing, binding, or lifecycle must change;
- `reject`: visual-only, broken, redundant, or incompatible with the live contract.

## Semantic Ownership

Give each independently movable or replaceable unit one semantic parent. A component owns its full visual and interactive bundle, including its plate, icon, native text, progress, badge, state decoration, and hit target.

Recommended page shape:

```text
CanvasPanel_Root
  modal mask or outside-click layer
  ScaleBox_Window
    CanvasPanel_Window
      CanvasPanel_Header
      CanvasPanel_ContentSectionA
      CanvasPanel_ContentSectionB
      CanvasPanel_Status
      CanvasPanel_Actions
```

Rules:

- Keep the viewport root full-screen; center or scale a fixed-size child window as one unit.
- Group by business responsibility, not by accidental overlap or shared color.
- A background `Image` is a child of a region, never the region's container.
- Keep window-local coordinates inside the window rather than positioning every child in viewport space.
- Put decorative siblings below content and input in Z-order.
- Use semantic names for regions and all runtime-facing controls. Generic names are tolerable only for truly private decorative leaves, and even then should be minimized.
- Do not add wrapper depth without ownership, layout, clipping, state, or reuse value.

## Container Choice

| Container | Prefer it for | Avoid it for |
|---|---|---|
| `CanvasPanel` | Anchored page regions, intentional overlap, absolute local composition, independent Z-order | Rows or columns that should naturally reflow |
| `Overlay` | Several layers sharing the same bounds, such as frame + icon + badge | Arbitrary page positioning |
| `SizeBox` | A real width/height, min/max, or aspect constraint | Decorative nesting with no constraint |
| `Border` | One child needing background, padding, clipping, or a styled text surface | Multi-child layout |
| `HorizontalBox` | Cost icon + amount, button groups, aligned metadata rows | Overlapping children |
| `VerticalBox` | Label/content/action stacks and vertically spaced sections | Independent absolute placement |
| `WrapBox` | A small, genuinely fixed or naturally wrapping set of uniform children | Runtime-sized data, pooling, or item virtualization |
| `UGC_ReuseList2` | Runtime-sized repeated data with a stable Item contract | A one-off visual group with no data/lifecycle owner |
| `WidgetSwitcher` | Mutually exclusive quality, lock, selection, or mode states | Independent layers that must appear together |

Choose the simplest container that expresses actual behavior. Do not convert fixed content to a list merely to reduce node count, and do not duplicate runtime-sized items manually because the current sample count happens to be small.

## Reusable Item Contract

A reusable item should be a self-contained visual state renderer with stable dimensions and a small data-facing surface.

Recommended ownership:

```text
Item root with cell-sized bounds
  quality/state switcher
  icon constraint
  quantity/background group
  native item name
  optional lock/selection layer
  optional Button covering the intended hit area
```

Verify:

- the list `ItemWidth` and `ItemHeight` agree with the Item root's intended bounds;
- icon, frame, quantity, and name remain within the cell unless overflow is deliberate;
- list gap/padding is represented once, not partly in the list and partly in each Item;
- dynamic text and icons remain native controls;
- mutually exclusive states use a stable `WidgetSwitcher` mapping;
- display-only children do not intercept input;
- clickable Items have a Button or precise-click configuration whose hit area matches the visible cell;
- runtime-facing child names are semantic even when the Item class itself is reused in several lists.

Prefer an Item method such as `InitUI(data)` when the Item owns presentation logic. Direct child assignment from the parent callback is acceptable for very small items, but keep the data-to-visual mapping in one place.

## ReuseList Runtime Contract

`UGC_ReuseList2` is not complete when it only previews the correct Item in the editor. The owning UI must provide data, callbacks, refresh, and teardown.

Use this lifecycle:

1. Configure `ItemClass`, `ItemWidth`, `ItemHeight`, spacing, preview count, cache, scrolling, and alignment in the WidgetBlueprint.
2. Store the current data array on the owning UI.
3. Bind `OnUpdateItem` during construction for pooled Item data refresh.
4. Call `Reload(count)` after the data array is ready or changes.
5. Treat the callback index as 0-based and convert to Lua's 1-based table index deliberately.
6. In the callback, initialize the Item from the matching data entry.
7. Clear the list listener during `Destruct` or the project's equivalent teardown path.

Use `OnAfterNewItem` only for work that belongs to newly created Item instances. Do not rely on creation-only callbacks to refresh recycled Items whose data can change.

For draggable lists whose Items are also clickable, enable the engine's precise scrolling on the outer list and precise click behavior on the Item. Verify both drag and tap on the target device.

## WidgetSwitcher State Pattern

Use a switcher when exactly one visual state should be active, such as quality, locked/unlocked, selected/unselected, or mode A/B.

- Define one explicit data-to-index mapping beside the runtime binding code.
- Keep child order stable; reordering children silently changes runtime meaning.
- Use one switcher per independent state axis. Do not combine unrelated states into a large Cartesian-product switcher.
- Set the active index whenever Item data is refreshed, including recycled list Items.
- Keep shared icon, name, and quantity controls outside the switcher when only the frame/state artwork changes.

## Button Ownership And Hit Regions

The `Button` is the input owner. Its visible plate, icon, and native label should normally be children of that same Button.

Recommended structure:

```text
Button_Action
  CanvasPanel_ButtonContent
    Image_ActionPlate
    TextBlock_ActionLabel
```

For image-driven buttons:

- use a transparent/no-resource Button style when the child Image supplies the plate;
- keep Button content padding at zero and the child content slot set to Fill;
- make decorative children non-blocking for hit tests;
- preserve the original Button identity and binding during reparenting;
- require the Button hit bounds to cover the full visible plate;
- if a visual intentionally overflows, document the reason and test edge taps on mobile;
- keep non-clickable cost, requirement, cooldown, or warning content outside the Button unless clicking it is intended to trigger the action.

Do not grade a button by appearance alone. Compare the Button slot, child visual bounds, padding, style brushes, visibility, and parent clipping together.

## Native Text And Styled Content

Prefer native text for titles, costs, warnings, quantities, names, progress values, and any localized or runtime-dynamic content.

Useful patterns include:

- `SizeBox > Border > UTRichTextBlock` for a constrained warning or explanatory surface;
- `HorizontalBox > SizeBox(icon) + RichText/TextBlock(value)` for a cost row;
- `VerticalBox > cost row + SizeBox > Button` for an action with non-clickable metadata above it.

Do not bake dynamic text into button or panel images. Preserve intentionally collapsed legacy text controls only when they remain part of the runtime or compatibility contract; otherwise classify them explicitly instead of leaving unexplained dead fields.

## Asset Move And Brush Integrity

Texture reorganization is a dependency migration, not a filesystem cleanup.

- Move or rename Unreal assets through editor-aware operations so redirectors and references can be updated.
- Before deleting an old location, enumerate dependent WidgetBlueprints and Item widgets.
- After the move, verify the new asset exists and each dependent `Image.Brush.ResourceObject` points to a live object.
- Check Button `WidgetStyle` brushes separately from child Image brushes.
- Compile, save, reload, and re-read the dependent WidgetBlueprints.
- Visually inspect the frame/background, title, close control, primary and secondary buttons, progress styling, list Items, and every switcher state.

A non-empty convenience texture property, successful import, or correct tree is not proof that Slate can render the image. Use the `UMG_IMAGE_BRUSH_RESOURCE_UNBOUND` diagnosis and repair workflow in `../mcp-ui-widget.md` when `Brush.ResourceObject` is null.

## Migration Rules

When adapting the stronger hierarchy into the live UI:

- preserve the live asset load path unless the caller is deliberately migrated;
- preserve every Lua-facing control name and class where compatible;
- preserve callbacks, RPCs, config rules, refresh order, visibility semantics, and gameplay behavior;
- replace manual repeated children with a list only when the runtime data and callback lifecycle are implemented in the same change;
- keep old specialized child widgets when they carry behavior that the new generic Item does not yet reproduce;
- migrate one responsibility at a time and verify it before removing the old owner;
- never call the candidate complete while required controls or Item scripts are missing.

Hierarchy improvement does not authorize gameplay or Lua-rule changes. Any compatibility edit should be the smallest local mapping needed to preserve the old behavior.

## Validation Checklist

Before accepting a hierarchy or migration:

- root and adaptation container cover the intended viewport;
- every independently movable bundle has one clear owner;
- all runtime-required controls exist with expected classes and names;
- slot type, anchors, offsets, alignment, auto-size, padding, and render transforms are intentional;
- child bounds and overflow are reviewed at desktop and mobile aspect ratios;
- Z-order is correct across sibling components, not only within each component;
- decorative widgets do not block input;
- Button hit regions cover their visible plates;
- fixed repeated content and runtime-sized repeated content use the appropriate ownership model;
- Item root bounds match list cell configuration;
- list callbacks bind, use the correct index base, reload from current data, and clear on teardown;
- switcher child order matches the runtime state mapping;
- dynamic text, icons, progress, lock, quality, quantity, and visibility all refresh;
- every required brush resource is non-null after reload;
- compile/save succeeds and `package_is_dirty() == False` after the intended save;
- PIE or device testing verifies rendering, list population, edge taps, refresh, reopen, and teardown.

`widget_inspect` proves hierarchy and slot layout only. It does not prove rendering, data binding, button interaction, or lifecycle cleanup.

## Comparison Report

Use this compact report shape:

```text
source_asset:
candidate_asset:
source_role: live | experimental | historical
candidate_role: live | experimental | historical

tree_metrics:
  widget_count:
  max_depth:
  generic_names:
  reusable_item_classes:
  fixed_repeated_children:

runtime_contract:
  required_controls:
  present:
  missing:
  callbacks_and_refresh:

structure_decisions:
  keep:
  adapt:
  reject:

layout_and_input:
  anchors_and_slots:
  overflow:
  z_order:
  button_hit_regions:

asset_integrity:
  moved_dependencies:
  null_brush_resources:

replacement_readiness: ready | compatible_after_mapping | not_ready
verification_remaining:
```

State confirmed facts separately from inference. A useful conclusion explains both what to learn from the stronger tree and what must not be copied without repair.
