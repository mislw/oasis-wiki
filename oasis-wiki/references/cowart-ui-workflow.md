# Cowart UI 生产工作流

这是 Oasis Wiki 中独立的游戏 UI 生产分类。它连接现有的 Game UI Design System、AI UI 图生成、原生 Cowart 视觉评审、可编辑组件提取、Precision Reconstruction，以及 RedCliff 编辑器交付，但不会自动修改 UGC 工程文件。

## 何时进入此分类

- 用户要求按游戏风格生成或修改 UI 图，并希望生成后自动放入、打开 Cowart。
- 用户要求把扁平 UI 图拆成可移动组件、恢复层级、生成 `layer-manifest.json` 或 UI Tree。
- 用户提供 Canva Magic Layers 或其他带图层元数据的导出包。
- 用户要求把已审核 UI 转成 RedCliff 的 UMG/Lua/DataTable 交付计划。

## 标准流水线

1. **设计约束**：先读 `references/game-ui-design-system.md`，解析项目风格档案和已有组件，确定 UI Tree、原生文本/数值控件与位图资源边界。
2. **UI 规格**：从 `assets/cowart-ui/ui-spec-template.json` 创建并验证 `ui-spec.json`，再生成完整 `ui-tree.json`。
3. **生成 UI 图**：按已解析的游戏风格生成完整候选图。图像生成是当前 Codex 会话动作，本地控制台不伪装成图像生成器。
4. **自动交给 Cowart**：创建视觉评审包，读取 Cowart 状态；空画布时自动生成并保存有效空快照，插入候选图，回读验证后自动打开原生 Cowart。详见 `references/cowart-ui/component-extractor.md`。
5. **视觉确认**：保留旧候选，把修订图放在来源图旁边。只有开发者明确确认后才锁定最终图。
6. **组件化**：优先使用真实图层导出；验证图层清单、建立 Cowart shape plan 和可编辑工作台。扁平图推断只能标记为 `reconstruction_candidate`，不能冒充独立图层。
7. **精细重建**：位图源图使用 `cowart-ui/precision-reconstruction.md` 的 Stage 2A/2B。区分 source crop、重建输出、`pending_review` 和明确确认的 active component。
8. **组件确认**：只把明确批准的组件写入用户级项目风格档案，并运行 `scripts/game-ui/validate_library.py`。
9. **交付计划**：运行 `scripts/cowart-ui/delivery/build_delivery_plan.py` 与 `scripts/cowart-ui/delivery/validate_delivery_plan.py`，生成 UMG 层级、Lua 绑定、数据归属和验收要求。详见 `references/cowart-ui/delivery.md`。
10. **工程实施**：只有用户明确授权后，才返回 Oasis Wiki 的 MCP UI/功能开发分支修改 WidgetBlueprint、Lua、DataTable 或其他 UGC 资产。

## 快速入口

```powershell
python scripts/cowart-ui/component-extractor/launch_ui_workflow_console.py --name "<page name>"
```

控制台只编排本地脚本和会话文件。Codex 负责调用 Cowart 的画布读取、空快照保存、图片插入和原生画布打开能力。

## 分类资源

- `references/cowart-ui/component-extractor.md`：Stage 0-3、Cowart 自动交接、组件提取与工作台流程。
- `references/cowart-ui/precision-reconstruction.md`：Stage 2A/2B 识别、净化、重组与审核 Gate。
- `references/cowart-ui/two-stage-workflow.md`：视觉评审与组件化的阶段边界。
- `references/cowart-ui/layer-manifest.md`：图层清单和导入契约。
- `references/cowart-ui/delivery.md`：RedCliff UI 交付计划流程。
- `references/cowart-ui/delivery-contract.md`：UMG/Lua/DataTable 映射与验收契约。
- `scripts/cowart-ui/component-extractor/`：规格、评审、Cowart 交接、图层规范化、工作台和组件确认脚本。
- `scripts/cowart-ui/delivery/`：交付计划构建与验证脚本。
- `assets/cowart-ui/`：UI 规格、组件决策和本地工作台模板。

## 强制边界

- Cowart 视觉评审通过，不等于组件已确认；组件已确认，也不等于编辑器或 PIE 已验收。
- 文本、数值、倒计时、进度、交互热区和状态必须保留为原生控件，不烘焙进 PNG。
- 任意矩形 source crop 都不能自动作为 reusable component；Skin 必须完成重建并通过审核。
- 不覆盖或删除 Cowart 中既有图形；修订图保留版本关系。
- 未经用户明确授权，不写入 UGC Lua、WidgetBlueprint、`.uasset`、`.umap` 或项目内风格档案。
- 不打包 `.venv`、`__pycache__`、`.pyc`、临时 session、用户 profile 或 RedCliff 运行产物。
