import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join, relative } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const wikiRoot = fileURLToPath(new URL("../", import.meta.url));

const requiredFiles = [
  "references/cowart-ui-workflow.md",
  "references/cowart-ui/component-extractor.md",
  "references/cowart-ui/two-stage-workflow.md",
  "references/cowart-ui/layer-manifest.md",
  "references/cowart-ui/delivery.md",
  "references/cowart-ui/delivery-contract.md",
  "scripts/cowart-ui/component-extractor/validate_ui_spec.py",
  "scripts/cowart-ui/component-extractor/create_ui_workbench.py",
  "scripts/cowart-ui/component-extractor/open_ui_workflow.py",
  "scripts/cowart-ui/component-extractor/create_cowart_blank_snapshot.mjs",
  "scripts/cowart-ui/component-extractor/apply_component_decisions.py",
  "scripts/game-ui/generation_pipeline.py",
  "scripts/game-ui/build_generation_prompt.py",
  "scripts/game-ui/build_generation_package.py",
  "scripts/game-ui/validate_generation_package.py",
  "scripts/game-ui/prepare_image_generation.py",
  "scripts/game-ui/generate_with_codex_provider.py",
  "scripts/game-ui/record_generation_result.py",
  "scripts/game-ui/create_style_review.py",
  "scripts/game-ui/project_library.py",
  "scripts/game-ui/validate_project_library.py",
  "scripts/game-ui/initialize_project_library.py",
  "scripts/game-ui/index_project_assets.py",
  "scripts/game-ui/import_project_previews.py",
  "scripts/game-ui/build_item_icon_catalog.py",
  "scripts/game-ui/resolve_project_references.py",
  "scripts/cowart-ui/delivery/build_delivery_plan.py",
  "scripts/cowart-ui/delivery/validate_delivery_plan.py",
  "assets/cowart-ui/ui-spec-template.json",
  "assets/cowart-ui/component-decisions-template.json",
  "assets/cowart-ui/workflow-console/index.html",
  "assets/cowart-ui/workbench-template/index.html",
  "references/cowart-ui/precision-reconstruction.md",
  "assets/cowart-ui/extraction-plan-template.json",
  "scripts/cowart-ui/component-extractor/build_extraction_plan.py",
  "scripts/cowart-ui/component-extractor/validate_extraction_plan.py",
  "scripts/cowart-ui/component-extractor/build_reconstruction_jobs.py",
  "scripts/cowart-ui/component-extractor/recompose_ui.py",
  "scripts/cowart-ui/component-extractor/validate_reconstruction.py",
];

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = join(dir, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

test("Oasis Wiki exposes Cowart UI as a separate routed category", () => {
  for (const file of ["SKILL.md", "AGENTS.md", "references/task-router.md"]) {
    const content = readFileSync(join(wikiRoot, file), "utf8");
    assert.match(content, /references\/cowart-ui-workflow\.md/, `${file} must route to Cowart UI workflow`);
  }
});

test("Cowart UI category bundles all reusable workflow resources", () => {
  for (const file of requiredFiles) {
    assert.ok(existsSync(join(wikiRoot, file)), `missing ${file}`);
  }
});

test("Cowart UI category describes upstream design and automatic Cowart handoff", () => {
  const content = readFileSync(join(wikiRoot, "references/cowart-ui-workflow.md"), "utf8");
  assert.match(content, /Game UI Design System|游戏 UI 设计系统/);
  assert.match(content, /自动.*Cowart|Cowart.*自动/s);
  assert.match(content, /IMAGE_GENERATION_UNAVAILABLE/);
  assert.match(content, /Codex 内置.*image_gen|image_gen.*Codex 内置/s);
  assert.match(content, /codex_provider_direct/);
  assert.match(content, /明确授权|显式授权/);
  assert.match(content, /禁止使用 HTML\/CSS\/Chromium screenshot fallback/);
  assert.match(content, /build_generation_package\.py/);
  assert.doesNotMatch(content, /OPENAI_API_KEY/);
  assert.match(content, /scripts\/cowart-ui\/delivery/);
});

test("image generation discovers upstream candidates before failing closed", () => {
  for (const file of [
    "SKILL.md",
    "references/cowart-ui-workflow.md",
    "references/game-ui-design-system.md",
  ]) {
    const content = readFileSync(join(wikiRoot, file), "utf8");
    assert.match(content, /--discover-image-models/, `${file} must route upstream discovery`);
    assert.match(content, /selection_required:\s*true/, `${file} must require developer selection`);
    assert.match(content, /generation_attempted:\s*false/, `${file} must keep discovery read-only`);
    assert.match(content, /paid probe/i, `${file} must forbid automatic paid probing`);
    assert.match(content, /official environment Key/i, `${file} must not stop at missing official credentials`);
  }
});

test("Cowart UI bundle excludes environments, bytecode, and runtime outputs", () => {
  const roots = ["references/cowart-ui", "scripts/cowart-ui", "assets/cowart-ui"]
    .map((path) => join(wikiRoot, path))
    .filter(existsSync);
  const forbidden = roots.flatMap(walk).map((path) => relative(wikiRoot, path))
    .filter((path) => /(^|[\\/])(?:\.venv|__pycache__|sessions?)([\\/]|$)|\.pyc$/i.test(path));
  assert.deepEqual(forbidden, []);
});

test("bundled Skill includes the precision component reconstruction workflow", () => {
  const content = readFileSync(join(wikiRoot, "references/cowart-ui-workflow.md"), "utf8");
  assert.match(content, /Precision Component Reconstruction/);
  assert.match(content, /reconstruction_candidate/);
});

test("Game UI Design System documents project library generation references", () => {
  const files = [
    "references/game-ui-design-system.md",
    "references/game-ui/schemas.md",
    "references/game-ui/workflow.md",
    "references/game-ui/validation-rules.md",
    "references/game-ui/output-templates.md",
  ];
  const content = files.map((file) => readFileSync(join(wikiRoot, file), "utf8")).join("\n");
  assert.match(content, /project_library_asset/);
  assert.match(content, /classified[^\n]*(?:not|不是|不等于)[^\n]*active/i);
  assert.match(content, /local cache paths?[^\n]*(?:never|不得|不进入)[^\n]*committed manifests?/i);
});
