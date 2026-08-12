# Reference-Driven Game UI Image Generation Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an auditable pipeline that carries original style and layout images into a real image-generation request, records only real generation results, and gates AI-generated Cowart reviews on those artifacts.

**Architecture:** Keep generation orchestration under `oasis-wiki/scripts/game-ui/`, with one shared module for JSON/image/hash validation and focused command-line scripts for package creation, prompt compilation, result recording, and style review. Extend the existing Cowart UI spec/tree contract with structured references, then make `create_visual_review.py` distinguish `ai_generated` from `external_source` inputs.

**Tech Stack:** Python 3, Pillow, JSON, SHA-256, `unittest`, Node.js `node:test`.

## Global Constraints

- Formal game UI generation must not fall back to HTML/CSS/Chromium screenshots.
- A valid AI generation request must contain at least one readable style image.
- Layout references must explicitly use `copy_visual_style: false`.
- Generation results may only be recorded for an existing real output image.
- User-provided reference screenshots stay outside the public repository.
- Precision Component Reconstruction and RedCliff UGC assets are out of scope.

---

### Task 1: Structured UI References

**Files:**
- Modify: `oasis-wiki/assets/cowart-ui/ui-spec-template.json`
- Modify: `oasis-wiki/scripts/cowart-ui/component-extractor/validate_ui_spec.py`
- Modify: `oasis-wiki/scripts/cowart-ui/component-extractor/build_ui_tree.py`
- Test: `oasis-wiki/tests/test_game_ui_generation.py`

**Interfaces:**
- Consumes: `visual.reference_images[]` objects with `source`, `role`, `priority`, optional `copy_visual_style`, and optional `source_kind`.
- Produces: validated references preserved in `ui-tree.json`, with layout style-copy defaulted to `false`.

- [ ] Write tests for missing source/role, invalid role/priority, and layout defaulting.
- [ ] Run the focused tests and verify they fail against the current string-array contract.
- [ ] Implement reference validation and canonicalization.
- [ ] Re-run focused tests and verify they pass.

### Task 2: Generation Package And Prompt Compiler

**Files:**
- Create: `oasis-wiki/scripts/game-ui/generation_pipeline.py`
- Create: `oasis-wiki/scripts/game-ui/build_generation_prompt.py`
- Create: `oasis-wiki/scripts/game-ui/build_generation_package.py`
- Create: `oasis-wiki/scripts/game-ui/validate_generation_package.py`
- Test: `oasis-wiki/tests/test_game_ui_generation.py`

**Interfaces:**
- Consumes: UI Tree, style profile, reference metadata, readable image files, page purpose, and reusable component IDs.
- Produces: copied reference images, `reference-manifest.json`, `generation-prompt.txt`, and `generation-request.json` with separated style/layout lists and `fallback_policy: forbid_html_screenshot`.

- [ ] Write tests for no style reference, profile-only input, valid style/layout input, image metadata, SHA-256, source-kind rejection, and request separation.
- [ ] Run focused tests and verify the new commands are missing.
- [ ] Implement minimal shared validation, prompt compilation, package construction, and package validation.
- [ ] Re-run focused tests and verify all package tests pass.

### Task 3: Generation Result And Style Review

**Files:**
- Create: `oasis-wiki/scripts/game-ui/record_generation_result.py`
- Create: `oasis-wiki/scripts/game-ui/create_style_review.py`
- Test: `oasis-wiki/tests/test_game_ui_generation.py`

**Interfaces:**
- Consumes: a validated package and a real generated bitmap.
- Produces: `generation-result.json` with output/prompt hashes and `style-review.json` with qualitative checks set to `pending_developer_review`.

- [ ] Write tests that reject absent output files and prevent fabricated results.
- [ ] Run focused tests and verify failure.
- [ ] Implement result recording and the auditable qualitative review template.
- [ ] Re-run focused tests and verify pass.

### Task 4: Cowart Generation Gate

**Files:**
- Modify: `oasis-wiki/scripts/cowart-ui/component-extractor/create_visual_review.py`
- Modify: `oasis-wiki/scripts/cowart-ui/component-extractor/launch_ui_workflow_console.py`
- Test: `oasis-wiki/tests/test_game_ui_generation.py`

**Interfaces:**
- Consumes: `--source-type ai_generated --generation-package <dir>` or `--source-type external_source`.
- Produces: a visual review only when AI artifacts validate, while retaining direct external-image review.

- [ ] Write tests for missing generation result, output hash mismatch, and allowed external source.
- [ ] Run focused tests and verify failure.
- [ ] Implement the source-type gate and pass package metadata into the review manifest.
- [ ] Re-run focused and existing Cowart tests.

### Task 5: Documentation, Stress Package, And Release Verification

**Files:**
- Modify: `oasis-wiki/references/cowart-ui-workflow.md`
- Modify: `oasis-wiki/references/cowart-ui/component-extractor.md`
- Modify: `oasis-wiki/references/game-ui/workflow.md`
- Modify: `oasis-wiki/references/game-ui-design-system.md`
- Modify: `oasis-wiki/tests/cowart-ui-category.test.mjs`

**Interfaces:**
- Produces: documented mandatory flow from original references through real image generation and Cowart, with `IMAGE_GENERATION_UNAVAILABLE` as the only accepted outcome when the active session lacks image-generation capability.

- [ ] Update documentation and bundled-resource assertions.
- [ ] Run all Python and Node tests.
- [ ] Build a repository-external exchange-shop package from three style images and one layout image.
- [ ] Attempt the real built-in image-generation call with all four images plus the compiled prompt; stop with `IMAGE_GENERATION_UNAVAILABLE` if the tool is absent.
- [ ] Inspect the final diff, commit with `Add reference-driven game UI image generation pipeline`, and push the feature branch.
