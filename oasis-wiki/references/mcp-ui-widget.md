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

