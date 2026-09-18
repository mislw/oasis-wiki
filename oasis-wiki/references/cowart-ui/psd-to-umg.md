# PSD Hierarchy To UMG

Use this workflow when a real `.psd` file must be converted into a reviewable UI Tree and then imported into an existing or explicitly approved new WidgetBlueprint. A PSD preview is useful for visual comparison, but it is not the hierarchy source.

## Trigger Phrases

- `从 PSD 对应层级导入到 UI 控件`
- `解析 PSD 图层并生成 UMG`
- `按 PSD 层级导入 WidgetBlueprint`
- `PSD 转 UI 控件树`

## Required Workflow

1. Inspect the PSD read-only with a structured PSD parser. Do not infer groups or parent-child relationships from pixels, layer overlap, or a flattened export.
2. Extract document size and every group/layer's stable source ID, original name, parent ID, stack position, absolute bounds, visibility, opacity, blend mode, clipping relationship, masks, text metadata, and source type.
3. Export visual layers without overwriting the PSD. Preserve alpha. Record unsupported adjustment layers, smart objects, effects, fonts, blend modes, or masks instead of silently flattening or discarding them.
4. Normalize the result into `layer-manifest.json`. Assign unique stable IDs even when PSD names repeat, and keep an explicit mapping from original PSD names to sanitized UMG names.
5. Validate the manifest before UI planning. Reject cycles, missing parents, duplicate IDs, invalid bounds, missing exported assets, ambiguous clipping ownership, and stack-order conflicts.
6. Build `ui-tree.json` and a visual recomposition preview. Require developer review before choosing semantic UMG containers or changing the target WidgetBlueprint.
7. Map the reviewed tree into UMG without flattening all layers into siblings:
   - PSD groups become semantic parent containers such as `CanvasPanel`, `Overlay`, `HorizontalBox`, `VerticalBox`, `GridPanel`, or a reusable UserWidget only when the reviewed layout and current project patterns support that choice.
   - Raster/art/shape layers become `Image` or `Border` controls using exported transparent assets.
   - Editable or runtime-dynamic text becomes native `TextBlock`/input controls. Do not bake counters, timers, prices, labels, localization text, progress, or runtime state into parent textures.
   - A confirmed interactive button group becomes `Button` plus its reviewed visual/text children. Visual grouping alone is not enough to invent interaction.
   - Hidden PSD layers remain manifest evidence and are excluded from runtime by default unless the developer explicitly maps them to a state.
8. Preserve visual geometry. Compute child-local positions from the reviewed parent origin, preserve PSD stack order as UMG Z-order, and record every intentional layout or naming deviation.
9. Before editor mutation, require the exact project-local WidgetBlueprint `load_path`, project match, frozen mapping plan, read-only MCP preflight, a backup outside the UGC project tree, and explicit authorization for this specific write.
10. After import, compile, save, reload, and read back the WidgetTree. Compare hierarchy, bounds, Z-order, visibility, text/image types, and assets with the manifest, then visually inspect the editor result and verify behavior in PIE.

## Outputs

```text
psd-source-report.json
layer-manifest.json
ui-tree.json
umg-mapping-plan.json
recomposition-preview.png
layers/<stable-layer-id>.png
```

The mapping plan is not proof of editor delivery. Only WidgetTree readback, visual inspection, and PIE verification prove the implementation.

## Reusable Prompt

```text
使用 $oasis-wiki，把我提供的 PSD 按原始图层层级导入到 UI 控件树。不要把 PSD 当成扁平图片，也不要根据视觉重叠猜测层级。请使用结构化 PSD 解析方式读取画布尺寸、图层组、父子关系、堆叠顺序、坐标尺寸、可见性、透明度、蒙版、裁剪关系、文本信息和稳定源 ID，先生成并校验 layer-manifest.json、ui-tree.json、UMG 映射计划和复拼预览，列出无法可靠转换的效果或资源，等待我确认。映射时保留语义父容器和 Z-order，不得把全部图层平铺为同级控件；动态文字、数值、计时器、进度和交互状态保留为原生 UMG 控件，确认的按钮组合映射为 Button 及其子控件。只有在我提供精确 WidgetBlueprint load_path、项目匹配、完成只读预检、建立项目外备份，并明确授权本次写入后，才通过 MCP 修改 WidgetBlueprint。写入后必须编译、保存、重载、回读层级并进行可视检查和 PIE 验证。
```
