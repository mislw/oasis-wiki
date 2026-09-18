# Cowart UI 生产工作流

这是 Oasis Wiki 中独立的游戏 UI 生产分类。它连接现有的 Game UI Design System、AI UI 图生成、原生 Cowart 视觉评审、可编辑组件提取、Precision Reconstruction，以及 RedCliff 编辑器交付，但不会自动修改 UGC 工程文件。

## 何时进入此分类

- 用户要求按游戏风格生成或修改 UI 图，并希望生成后自动放入、打开 Cowart。
- 用户要求把扁平 UI 图拆成可移动组件、恢复层级、生成 `layer-manifest.json` 或 UI Tree。
- 用户提供 Canva Magic Layers 或其他带图层元数据的导出包。
- 用户提供真实 PSD，并要求保留图层组、父子关系和堆叠顺序导入 UI/UMG 控件树。
- 用户要求把已审核 UI 转成 RedCliff 的 UMG/Lua/DataTable 交付计划。

## 标准流水线

1. **设计约束**：先读 `references/game-ui-design-system.md`，解析项目风格档案和已有组件，确定 UI Tree、原生文本/数值控件与位图资源边界。
2. **UI 规格**：从 `assets/cowart-ui/ui-spec-template.json` 创建并验证 `ui-spec.json`，再生成完整 `ui-tree.json`。
3. **解析原始参考图**：把用户给出的独立原图分类为 `style` 或 `layout`。聊天截图、浏览器截图、Cowart 截图和多图 collage 默认拒绝，除非用户明确授权。
4. **构建 Generation Package**：运行 `scripts/game-ui/build_generation_package.py`，把原图复制进包内，并记录尺寸、SHA-256、角色和优先级。
5. **编译 Prompt**：同时编译项目 Style Profile、已有组件、UI Tree、原生/位图边界和负面约束；Style Profile 只作补充，不能替代 Style Image。
6. **真实图片生成**：优先把 Style Images、Layout Images 和 Compiled Prompt 一起传给 Codex 内置 `image_gen`。不要求用户配置外部 Key，也不使用通用 CLI fallback。内置工具、official environment Key 或默认图片模型不可用，或者当前凭据来自自定义 Provider 时，不得直接停止：先运行 `generate_with_codex_provider.py --discover-image-models`，只读查询当前 Provider 的 `/models`，按 `confirmed`、`likely`、`uncertain` 列出候选和证据。发现结果固定为 `generation_attempted: false`，禁止 automatic paid probe；即使只有一个候选也保持 `selection_required: true`，由开发者选择模型后，再请求明确授权并执行 `codex_provider_direct`。
7. **Style Validation**：运行 `scripts/game-ui/create_style_review.py`，建立定性对比记录，状态保持 `pending_developer_review`，不得伪造相似度百分比。
8. **自动交给 Cowart**：`ai_generated` 来源必须通过 Generation Result、输出 SHA 和候选图一致性检查；`external_source` 仍允许用户直接导入已有 UI 图。
9. **组件化**：优先使用真实图层导出；PSD 输入必须按 `references/cowart-ui/psd-to-umg.md` 结构化解析并保留源层级。扁平图推断只能标记为 `reconstruction_candidate`，不能冒充独立图层。
10. **组件确认**：只把明确批准的组件写入用户级项目风格档案，并运行 `scripts/game-ui/validate_library.py`。
11. **交付**：先生成并验证 RedCliff 交付计划；只有用户明确授权后，才修改 WidgetBlueprint、Lua、DataTable 或其他 UGC 资产。

## Generation Package

```powershell
python scripts/game-ui/build_generation_package.py `
  --ui-tree <ui-tree.json> `
  --style-profile <profile.json> `
  --references <references.json> `
  --output <generation-package> `
  --page-purpose "<page purpose>"

python scripts/game-ui/validate_generation_package.py <generation-package>
python scripts/game-ui/prepare_image_generation.py --package <generation-package> --available-tool image_gen

# Only after explicit user authorization when image_gen is unavailable:
python scripts/game-ui/generate_with_codex_provider.py --discover-image-models
python scripts/game-ui/prepare_image_generation.py --package <generation-package> --allow-provider-direct
python scripts/game-ui/generate_with_codex_provider.py --package <generation-package> --user-authorized-provider-direct
```

`prepare_image_generation.py` 默认只接受 Codex 当前工具清单中的内置 `image_gen`，并输出真实调用所需的 prompt/reference 路径。工具缺失时以退出码 `3` 输出 `IMAGE_GENERATION_UNAVAILABLE`，但编排层必须先完成只读上游发现，不能只因 official environment Key 缺失就结束。`--discover-image-models` 只读取当前 Provider 配置和托管认证并调用 `GET /models`，输出 Provider 主机名、候选模型、置信度和证据，不打印或写入凭据，也不调用图片生成接口。开发者选择候选且显式授权 `--allow-provider-direct` 后，`generate_with_codex_provider.py` 才解析实际模型名并生成图片。

## 原生入口

用户询问怎么启动、继续或验收这套流程时，先读 `references/cowart-ui/usage-guide.md`。其中的常用说法只负责选择或继续阶段；除非满足精确资产、冻结计划、项目外备份和本次明确授权，不得把“同步编辑器”等模糊说法当成写入许可。

```powershell
python scripts/cowart-ui/component-extractor/open_ui_workflow.py
python scripts/cowart-ui/component-extractor/launch_ui_workflow_console.py --name "<page name>"
```

原生 Companion 工作流已启用。用户明确要求启动或打开 UI 工具链时，可运行 `open_ui_workflow.py`；已有审核图和 UI Tree 时，优先用 `create_ui_workbench.py` 注册并打开精确会话。只有用户明确要求或当前任务需要展示刚生成的审核会话时才打开/聚焦 Companion，不因检测到 UI 任务就自动抢焦点。打开 Workbench 不等于编辑器写入授权。

## 分类资源

- `references/cowart-ui/component-extractor.md`：Stage 0-3、Cowart 自动交接、组件提取与工作台流程。
- `references/cowart-ui/psd-to-umg.md`：PSD 图层树解析、manifest 规范化、UMG 层级映射、编辑器写入门禁和可复用提示词。
- `references/cowart-ui/usage-guide.md`：用户如何启动、继续、审核和授权 UI 工具链，以及说明更新与编辑器写入的权限边界。
- `references/cowart-ui/precision-reconstruction.md`：Stage 2A/2B 识别、clean layer 重建、Assembly Preview 与审核 Gate。
- `references/cowart-ui/transparent-asset-extraction.md`：完整母底图、透明/半透明控件判定、固定美术字、子控件图标、父层残留和复拼验收规则。
- `references/cowart-ui/two-stage-workflow.md`：视觉评审与组件化的阶段边界。
- `references/cowart-ui/layer-manifest.md`：图层清单和导入契约。
- `references/cowart-ui/delivery.md`：RedCliff UI 交付计划流程。
- `references/cowart-ui/delivery-contract.md`：UMG/Lua/DataTable 映射与验收契约。
- `references/oasis-ui-agent-interaction.md`：围绕现有流程的 Agent 提问、Approval Gate、Workbench/UMG/Lua 验收、回退与失败话术；只增加交互编排，不改变运行时功能。
- `scripts/cowart-ui/component-extractor/`：规格、评审、Cowart 交接、图层规范化、工作台和组件确认脚本。
- `scripts/cowart-ui/delivery/`：交付计划构建与验证脚本。
- `assets/cowart-ui/`：UI 规格、组件决策和本地工作台模板。

## 强制边界

- 正式 AI Game UI 视觉稿禁止使用 HTML/CSS/Chromium screenshot fallback。HTML 仅可用于 debug、layout prototype、workbench 或失败诊断。
- 正式后端优先为 Codex 内置 `image_gen`，凭据模式固定为 `codex_managed`；不得要求用户提供 Key。缺少内置工具、official environment Key 或默认图片模型时，先执行无生成、无 automatic paid probe 的 `--discover-image-models`，列出候选并保持 `selection_required: true`。只有开发者选定模型并明确授权后，才允许 `codex_provider_direct`，并继续禁止通用 CLI 与 HTML/CSS/Chromium screenshot fallback。
- 用户给出视觉参考图时，最终图片生成调用必须实际接收这些原始文件。只传 Style Profile、art direction 或 prompt 属于门禁失败。
- 不得手写或伪造 `generation-result.json`；只能通过 `record_generation_result.py` 对真实存在且可读取的输出图片记录结果。
- Cowart 视觉评审通过，不等于组件已确认；组件已确认，也不等于编辑器或 PIE 已验收。
- 运行时动态文本、数值、倒计时、进度、交互热区和状态默认保留为原生控件。开发者明确点名确认的固定美术字可按 `references/cowart-ui/transparent-asset-extraction.md` 提取为仅含字形的透明 PNG；该提取本身不授权替换动态绑定、运行时刷新或本地化契约。
- 组件化前必须先解析 `reuse_of`、`texture_asset`、语义键和 Item ID：只有 `active` 且预览可读的组件库项可以直接复用；`candidate`、`pending_review` 或无法解析的条目不得冒充成品，也不得跳过必要重建。
- 原生项目图标必须保留 Unreal 资源引用，并用 `visual_assets.native_preview` 在 Workbench 中显示；该字段只用于编辑器预览，不能把 Native 节点改成 reusable bitmap。任何 Native 节点已有 `native_preview` 时，该预览是唯一视觉，不得再叠加 `display_text`、`content_hint`、计数器 fallback 或其他 glyph。纯交互/热区节点可以保留语义文字数据，但不得在可视父控件上重复绘字。关闭控件即使分类为 `hit_target` 也必须显示明确的关闭图形，禁止空白热区；只有未解析到任何可复用视觉时才允许 fallback glyph。
- Workbench 层级树面向开发者显示本地化 `name`，内部 `id` 必须保持稳定并继续用于布局保存、资源引用和编辑器映射。会话打包不得丢弃 `name`；自动派生的背景子层也必须使用本地化名称，搜索同时匹配显示名和内部 ID。
- 任意矩形 `source_crop` 都不能自动作为 reusable component；Skin 和父层必须生成 `clean_layer` 并通过审核。
- 从工作台交付到 UMG 时，不能把视觉图层全部平铺成同级 Widget。先参照项目中已工作的真实 WidgetTree，再按可独立移动的业务组件建立语义父容器；坐标保持、按钮身份、Z-order、事务回滚和验证规则见 `references/mcp-ui-widget.md` 的 `Refine An Existing Widget Hierarchy Without Moving The UI`。
- PSD 输入必须以结构化图层数据为层级证据。不得用扁平预览、视觉重叠或图层名称猜测父子关系；解析失败或不支持的效果必须进入问题清单并等待确认。
- 不覆盖或删除 Cowart 中既有图形；修订图保留版本关系。
- 未经用户明确授权，不写入 UGC Lua、WidgetBlueprint、`.uasset`、`.umap` 或项目内风格档案。
- 不打包 `.venv`、`__pycache__`、`.pyc`、临时 session、用户 profile 或 RedCliff 运行产物。

### Superseded Workbench cleanup

- After a replacement for the same interface is verified and selected, keep only the latest same-interface page in the Companion catalog.
- Move obsolete session directories to the Recycle Bin only after resolving and confirming every target is under the expected Workbench root.
- During cleanup, do not delete source visual, visual review, extraction-plan, reconstruction, or component-library assets.
- After catalog cleanup, restart or refresh Companion because an already-running process may rewrite stale in-memory pages.

## Oasis UI Agent 交互层

执行本流程时同时遵循 `references/oasis-ui-agent-interaction.md`：Agent 先读取和推断，只询问一个真正缺失的关键决策；获得当前阶段确认后执行一个生产阶段；报告真实产物与验证结果；等待验收后再继续。视觉锁定、分层确认、UMG 计划、Widget 视觉结果、Lua/数据绑定和最终结果分别设门禁。

这只是对话编排，不是新的持久化状态机。当前没有经过验证的通用任务存储、Companion 当前任务面板或跨重启自动恢复时，不得声称这些能力已经存在，也不得因此改动 Cowart、Workbench、MCP 或 Companion 运行时。

## Precision Component Reconstruction

当审核通过的 UI 只有扁平位图、没有可信源图层包时，进入 `references/cowart-ui/precision-reconstruction.md`：

1. 锁定审核图与 SHA-256，并建立包含原生控件、皮肤、图标、复合区域和候选控件的 UI Tree。
2. 执行 Stage 2A Component Recognition，生成并验证 `extraction-plan.json`。
3. 执行 Stage 2B Precision Reconstruction；共享皮肤必须综合等价实例重建，不得把任意矩形裁剪冒充可复用控件。
4. 使用真实位图合成生成 `reconstructed-preview.png`，再与审核图对比并记录重建报告。
5. 只有通过评审的候选项才能进入 Stage 3 Component Confirmation 和组件库。

工作台必须区分 `reconstruction_candidate`、重建输出、`pending_review` 与开发者明确确认的 `active` 组件。

### Layer Reconstruction 补充门禁

扁平 UI 图进入工作台后，必须依次执行 UI Tree 推断、人工校正、节点分类、从叶子到根的 Layer Reconstruction、Assembly Preview 验证和组件确认。正式资产字段统一为 `source_crop`、`clean_layer`、`assembly_preview`。

`background.root`、Panel、Button、Artwork 等所有需要独立移动的视觉层都必须拥有自己的重建目标。页面使用一张完整母底图，前景使用透明或有意半透明的 clean layer。Native 动态文本、数值和交互区不生成运行时位图；开发者确认的固定美术字可生成透明视觉资产或 Native 预览，但不得因此改变运行时契约。父节点 Mask 按真实 Alpha/Mask、clean layer Alpha、语义分割、Bounds fallback 的优先级计算，并对所有可见后代做像素并集去重。

没有实现 `image_edit_inpainting` 的 `ImageReconstructionExecutor` 时必须返回 `LAYER_RECONSTRUCTION_UNAVAILABLE`，保持 `clean_layer: null`，不得用裁切、透明挖洞、Canvas 填色、HTML/CSS 或浏览器截图代替。
