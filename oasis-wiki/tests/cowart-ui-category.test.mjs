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
  "scripts/cowart-ui/component-extractor/create_cowart_blank_snapshot.mjs",
  "scripts/cowart-ui/component-extractor/apply_component_decisions.py",
  "scripts/cowart-ui/delivery/build_delivery_plan.py",
  "scripts/cowart-ui/delivery/validate_delivery_plan.py",
  "assets/cowart-ui/ui-spec-template.json",
  "assets/cowart-ui/component-decisions-template.json",
  "assets/cowart-ui/workflow-console/index.html",
  "assets/cowart-ui/workbench-template/index.html",
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
  assert.match(content, /scripts\/cowart-ui\/delivery/);
});

test("Cowart UI bundle excludes environments, bytecode, and runtime outputs", () => {
  const roots = ["references/cowart-ui", "scripts/cowart-ui", "assets/cowart-ui"]
    .map((path) => join(wikiRoot, path))
    .filter(existsSync);
  const forbidden = roots.flatMap(walk).map((path) => relative(wikiRoot, path))
    .filter((path) => /(^|[\\/])(?:\.venv|__pycache__|sessions?)([\\/]|$)|\.pyc$/i.test(path));
  assert.deepEqual(forbidden, []);
});
