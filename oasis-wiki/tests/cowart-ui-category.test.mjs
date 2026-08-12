import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { test } from "node:test";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const skillRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const requiredFiles = [
  "references/cowart-ui/precision-reconstruction.md",
  "references/cowart-ui/component-extractor.md",
  "references/cowart-ui-workflow.md",
  "assets/cowart-ui/extraction-plan-template.json",
  "scripts/cowart-ui/component-extractor/build_extraction_plan.py",
  "scripts/cowart-ui/component-extractor/validate_extraction_plan.py",
  "scripts/cowart-ui/component-extractor/build_reconstruction_jobs.py",
  "scripts/cowart-ui/component-extractor/recompose_ui.py",
  "scripts/cowart-ui/component-extractor/validate_reconstruction.py",
];

test("bundled Skill includes the precision component reconstruction workflow", () => {
  for (const relativePath of requiredFiles) {
    assert.equal(existsSync(join(skillRoot, relativePath)), true, relativePath);
  }
});
