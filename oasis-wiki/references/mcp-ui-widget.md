# MCP UI And Widget Workflow

Use this branch for MCP requests about viewing UI, generating UI, modifying WidgetBlueprints, UMG layout, interactive buttons, or errors in generated Widget assets.

## Trigger Phrases

- `用MCP生成蓝图/UI`
- `用MCP查看这个UI`
- `用MCP操作Widget`
- `补Widget蓝图`
- `这个UI在哪里`
- `怎么都是白色的`
- `点击按钮要能交互`

## Required Reads

After the shared MCP setup in `mcp-integration.md`, read only UI/widget APIs:

```text
ctx:
py:index
py:workflow blueprint
py:workflow lua
py:workflow asset_browser
py:list widget_edit
py:widget_add
py:widget_remove
py:widget_inspect
py:widget_move
py:widget_wrap
py:widget_unwrap
py:widget_set_property
py:widget_slot
schema:UGCWidgetBlueprintFactory?level=full
schema:CanvasPanelSlot?level=full
schema:TextBlock
schema:Button
schema:Image
```

For viewing an existing UI, prefer `widget_inspect`, current editor context, and nearby Lua binding files. Do not read DataTable workflows unless the UI content is explicitly config-driven.

## Inspect Existing UI

Load nearby working UI assets and inspect their trees:

```python
from unreal_engine.classes import Blueprint
bp = ue.load_object(Blueprint, '/Project/Asset/UI/MainUI.MainUI')
tree = ue.widget_inspect(bp)
```

Check:

- asset class is a WidgetBlueprint/UGCWidgetBlueprint;
- root panel and named controls exist;
- button names match Lua fields;
- slots show expected position/size;
- Lua creates the UI through the existing UIManager or project pattern.

## Create WidgetBlueprint Correctly

Do not assume `ue.create_blueprint(UserWidget, path)` creates editable UMG. It can create a plain `Blueprint`, then `widget_add` fails with:

```text
widget_add: arg1 must be a UWidgetBlueprint
```

Use `create_asset` with `UGCWidgetBlueprintFactory`:

```python
from unreal_engine.classes import UserWidget, Blueprint

factory_cls = ue.find_class('UGCWidgetBlueprintFactory')
asset_cls = ue.find_class('UGCWidgetBlueprint')
factory = ue.new_object(factory_cls)
factory.ParentClass = UserWidget

bp = ue.create_asset('MilitaryRank', '/RedCliff/Asset/UI/MilitaryRank', asset_cls, factory)
bp = ue.load_object(Blueprint, '/RedCliff/Asset/UI/MilitaryRank/MilitaryRank.MilitaryRank')
assert bp.get_class().get_name() == 'UGCWidgetBlueprint'
```

## Add Controls

Use `widget_add` for hierarchy:

```python
ue.widget_add(bp, 'Image', 'Image_Backdrop', 'CanvasPanel_0')
ue.widget_add(bp, 'TextBlock', 'TextBlock_Title', 'CanvasPanel_0')
ue.widget_add(bp, 'Button', 'Button_Upgrade', 'CanvasPanel_0')
ue.widget_add(bp, 'TextBlock', 'TextBlock_UpgradeButton', 'Button_Upgrade')
```

Keep widget names aligned with Lua fields, such as `Button_Upgrade`, `TextBlock_Cost`, and `TextBlock_CurrentRank`.

## Layout

First try `ue.widget_slot`. If it fails or `widget_inspect` still shows default `Pos: 0,0, Size: 100,30`, write the `CanvasPanelSlot` directly:

```python
from unreal_engine import FVector2D

widgets = {w.get_name(): w for w in bp.WidgetTree.AllWidgets}
btn = widgets['Button_Upgrade']
btn.Slot.SetPosition(FVector2D(800.0, 516.0))
btn.Slot.SetSize(FVector2D(290.0, 58.0))
btn.Slot.ZOrder = 4
```

## Window-mode root layout

Most project pages are centered window-mode UIs, but the root viewport must remain full-screen. Use a full-screen `CanvasPanel` or anchored `ScaleBox` for resolution adaptation, then place the visible panel in a fixed-size centered child window. Do not use the Workbench image bounds or visible window bounds as the root canvas size.

Recommended ownership:

```text
CanvasPanel_0                 # full viewport, for example 1920x1080
  MaskOrOutsideClickLayer    # optional full-screen modal layer
  ScaleBox_Window
    CanvasPanel_Window       # fixed-size centered child window
      panel/header/content/buttons
```

- In the UMG designer, the selected root boundary must cover the entire preview; a half-size `640x360` root with `1920x1080` children is a layout failure even when overflow remains visible.
- Keep window children in window-local coordinates. Center or scale the window as one unit instead of scaling every child independently.
- Define an explicit outside-click policy: use `SelfHitTestInvisible` on a non-modal full-screen root, or a full-screen mask/`Button` when clicks outside the window must be blocked or close the page.
- Before Lua binding, verify root size/anchors, centered window bounds, child containment, DPI scaling, and button hit regions in the editor.

## Refine An Existing Widget Hierarchy Without Moving The UI

Use this branch when a Cowart/workbench page looks correct but its WidgetTree is visually grouped and structurally flat. Report:

```text
UMG_HIERARCHY_VISUALLY_GROUPED_BUT_FLAT
```

### Ownership

- Inspect the real predecessor WidgetTree and Lua bindings first. Group by business responsibility, not visual overlap alone.
- Give every independently movable unit a semantic parent `CanvasPanel`: portrait, header/tags, progress, stats, one effect row, plan tabs, stage path, or one resource item.
- A component owns its complete movable bundle: skin/artwork, icon, native text, progress, badge, and interaction hot zone. A background `Image` is a child, not a container.
- Preserve existing `Button` identity. Reparent the same Lua-facing Button and keep its name, text child, `WidgetStyle`, `RenderOpacity`, and binding.
- Opacity `0` may be an intentional click hot zone. Group that Button with the visible arrow/icon.

### Coordinate-Preserving Reparent

Capture parent, position, size, Z-order, and page-space position before writes. Validate current ownership, then create groups inside one PRV transaction. For children sharing one parent, use their union bounds and convert to group-local coordinates:

```python
from unreal_engine import FVector2D

ue.widget_add(bp, 'CanvasPanel', group_name, parent_name)
group = ue.find_object(bp.get_path_name() + ':WidgetTree.' + group_name)
group.Visibility = 4  # SelfHitTestInvisible
group.Slot.SetPosition(FVector2D(group_x, group_y))
group.Slot.SetSize(FVector2D(group_width, group_height))
group.Slot.ZOrder = group_z

old_position = child.Slot.GetPosition()
old_size = child.Slot.GetSize()
old_z = child.Slot.ZOrder
child.GetParent().RemoveChild(child)
new_slot = group.AddChildToCanvas(child)
new_slot.SetPosition(FVector2D(
    old_position.x - group_x,
    old_position.y - group_y,
))
new_slot.SetSize(old_size)
new_slot.ZOrder = old_z
```

For different source parents, convert page-space coordinates into the new parent's local space first. Never subtract unrelated local coordinates.

Use `CanvasPanelSlot.SetPosition()` and `SetSize()`. Do not assign `CanvasPanelSlot.LayoutData`, `Offsets`, or a rebuilt layout struct in this UE4 wrapper; that can silently zero slots.

After grouping, parent Z-order controls sibling-component ordering; child Z-order applies only inside the component. Keep backgrounds low, content above them, and navigation/hot zones above overlapping rows.

### UE4 Cache And Rollback Traps

- `ue.widget_add()` can create a widget before `bp.WidgetTree.AllWidgets` refreshes. Resolve it with `ue.find_object(bp.get_path_name() + ':WidgetTree.' + group_name)` until compile/reload.
- A cancelled transaction can remove the widget from `AllWidgets` while transiently reserving its UObject name. The next add then fails with `widget_add: widget '<name>' already exists`.
- On that conflict, do not delete the asset or blindly rerun. Prefer an editor restart; otherwise use a fresh semantic name and verify after reload that no orphan serialized.
- Send planned writes through native MCP or `POST /call` with `plan_id`; do not use a shortcut endpoint that drops PRV metadata.
- If the bridge disconnects after a long write, inspect editor logs, the saved tree, and `package_is_dirty()` before retrying. A transport timeout is not proof that the editor mutation failed.

### Verification

1. Back up the `.uasset` outside the project and confirm PIE is stopped.
2. Compile/save, then reload every new parent, child count, `Visibility`, and Button owner.
3. Compare all moved widgets' page-space positions; require `POSITION_PRESERVATION=PASS` with zero errors.
4. Read back Button child names, opacity, and normal brush `ResourceObject` paths.
5. Require `package_is_dirty() == False`.
6. Reopen the WidgetBlueprint and visually check occlusion, Z-order, text, icons, progress bars, and click hot zones.

`widget_inspect` and coordinate tests prove structure and layout, not final rendering or interaction. Keep changes uncommitted unless the user asks for a commit.

## Text And Styling

`widget_set_property` may fail for struct/style properties such as `ColorAndOpacity`, `Font.Size`, `BackgroundColor`, or slate brushes. The symptom is a correct widget tree with default white or pale gray visuals.

Do not keep retrying `widget_set_property` for visual style after this symptom appears. Discover real widget functions and call them directly:

```python
for name in ['Image_Backdrop', 'TextBlock_Title', 'Button_Upgrade']:
    widget = widgets[name]
    funcs = [f for f in widget.functions()
             if 'Color' in f or 'Brush' in f or 'Text' in f or 'Font' in f or 'Style' in f]
```

Reliable choices:

- `Image.SetColorRGBStr('#RRGGBBAA')` for tinting simple generated Image blocks.
- `TextBlock.SetText(text)` and `TextBlock.SetColorRGBStr('#RRGGBBAA')` for labels.
- `Button.SetBackgroundColor(FLinearColor(r, g, b, a))` for button background tint.
- `Button.SetColorAndOpacity(FLinearColor(1, 1, 1, 1))` if button content appears dimmed.

Minimal style write test before styling the whole UI:

```python
widgets['Image_Backdrop'].SetColorRGBStr('#050506FF')
widgets['Image_TitlePlate'].SetColorRGBStr('#F2F0E8FF')
widgets['TextBlock_Title'].SetColorRGBStr('#111111FF')
ue.compile_blueprint(bp)
bp.save_package()
```

Refresh or reopen the WidgetBlueprint. If the three controls changed color, apply the full palette. If not, inspect functions/properties again before bulk styling.

## Imported PNG Is Blank Or White

Use this branch when imported PNG assets exist and native text renders, but Image layers, icons, buttons, or artwork remain blank. A common UE4 UGC failure is:

```text
Image.BrushImage = Texture2D
Image.Brush.ResourceObject = None
```

`BrushImage` is not proof that UMG can render the texture. `widget_set_property(bp, name, 'BrushImage', path)` may succeed and read back correctly while the real `FSlateBrush` still has no resource. Report this diagnosis as:

```text
UMG_IMAGE_BRUSH_RESOURCE_UNBOUND
```

Read both properties before changing texture import settings:

```python
image = ue.find_object(bp.get_path_name() + ':WidgetTree.Image_Layer')
brush_image = image.get_property('BrushImage')
brush = image.get_property('Brush')
resource = brush.get_field('ResourceObject')

assert brush_image is not None
assert resource is None  # confirmed failure
```

Repair the real brush through a referenced struct. The `.ref()` call is required in this editor build; mutating a copied struct or assigning it back may appear successful but reload with `ResourceObject = None`:

```python
texture = ue.load_object(
    ue.find_class('Texture2D'),
    '/Project/Asset/UI/Textures/panel_main.panel_main',
)
image = ue.find_object(bp.get_path_name() + ':WidgetTree.Image_Layer')

brush = image.get_property('Brush').ref()
brush.set_field('ResourceObject', texture)
brush.set_field('DrawAs', 3)  # Image in the current UE4 build

ue.compile_blueprint(bp)
bp.save_package()
```

For batch assembly, verify every Image after save:

```python
missing = []
for name in image_names:
    image = ue.find_object(bp.get_path_name() + ':WidgetTree.' + name)
    resource = image.get_property('Brush').get_field('ResourceObject')
    if not resource:
        missing.append(name)

assert missing == []
```

Also check for a second failure mode:

```text
UMG_IMAGE_LAYER_CONFLICT
```

Legacy background/title Images can remain visible above or below the reconstructed layer, producing a white board, duplicate title, or mixed old/new UI. Inspect the actual WidgetTree and slot order, then collapse only verified legacy visual widgets. Do not collapse a parent that still owns required Buttons, native text, dynamic child widgets, or Lua-facing controls.

Required validation order:

1. Back up or duplicate the WidgetBlueprint; use PRV before mutation.
2. Confirm source PNG dimensions and alpha are valid.
3. Confirm `BrushImage` and `Brush.ResourceObject` separately.
4. Repair the referenced `FSlateBrush` with `.ref()`.
5. Compile and save.
6. Reload and assert every expected `ResourceObject` is non-null.
7. Reopen the WidgetBlueprint and visually verify the rendered editor result.

`widget_inspect` proves hierarchy and slot layout only. It does not prove that a bitmap rendered.
## Interaction Binding

For a clickable UI, verify both layers:

- WidgetBlueprint has named `Button_*` controls.
- Lua binds `OnClicked` or the project UI event pattern and calls the intended RPC/config update.

Prefer existing project UIManager and RPC patterns over one-off binding style.

## Save And Verify

Always compile, save, reload, and inspect:

```python
ue.compile_blueprint(bp)
bp.save_package()

bp2 = ue.load_object(Blueprint, '/RedCliff/Asset/UI/MilitaryRank/MilitaryRank.MilitaryRank')
result = {
    'class': bp2.get_class().get_name(),
    'tree': ue.widget_inspect(bp2),
    'upgrade': ue.widget_inspect(bp2, 'Button_Upgrade'),
}
```

Verification must confirm:

- class is `UGCWidgetBlueprint`;
- required widget names exist;
- important slots show expected position/size;
- entry buttons in existing UI have matching Lua bindings;
- no wrong top-level asset path was created.

Do not treat `widget_inspect` as proof of color. Use it for hierarchy/layout, then use editor-visible refresh or direct property/function readback for style confidence.

