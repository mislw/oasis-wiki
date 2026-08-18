# Upstream Image Model Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Discover image-capable models from the active managed provider without paid probes, list candidates for developer selection, and publish the synchronized `1.260818.2` Skill and Companion release.

**Architecture:** Extend the existing dependency-free provider script with model-record discovery and deterministic classification. Keep discovery read-only and separate from the existing authorized generation path. Encode the orchestration rule in the Skill references, then synchronize only the changed Skill files into Companion.

**Tech Stack:** Python 3 standard library, `unittest`, Node test runner, Rust/Tauri, GitHub Releases.

---

### Task 1: Add Failing Discovery Tests

**Files:**
- Modify: `oasis-wiki/tests/test_game_ui_generation.py`

- [ ] **Step 1: Add candidate classification tests**

Add tests that construct model records containing explicit image-generation metadata, image-family IDs, ambiguous image modality, and unrelated text models. Assert ordered candidate tuples equivalent to:

```python
[
    ('vendor-image-edit', 'confirmed'),
    ('[l]gpt-image-2', 'likely'),
    ('vision-model', 'uncertain'),
]
```

- [ ] **Step 2: Add configured-model merge test**

Assert that a configured `flux-pro` model absent from `/models` is returned once with `likely` confidence and `configured_model` evidence.

- [ ] **Step 3: Add read-only CLI test**

Patch provider loading and model listing, set `sys.argv` to `['generate_with_codex_provider.py', '--discover-image-models']`, make `create_image_edit` raise if called, then assert `main()` returns `0` and JSON contains:

```json
{
  "generation_attempted": false,
  "selection_required": true
}
```

- [ ] **Step 4: Run the focused tests and verify RED**

Run:

```powershell
python -m unittest oasis-wiki.tests.test_game_ui_generation.GameUiGenerationTests.test_provider_direct_discovers_image_model_candidates oasis-wiki.tests.test_game_ui_generation.GameUiGenerationTests.test_provider_direct_discovery_merges_configured_models oasis-wiki.tests.test_game_ui_generation.GameUiGenerationTests.test_provider_direct_discovery_cli_is_read_only
```

Expected: failures because `ImageModelCandidate`, `discover_image_model_candidates`, and `--discover-image-models` do not exist.

### Task 2: Implement Read-Only Model Discovery

**Files:**
- Modify: `oasis-wiki/scripts/game-ui/generate_with_codex_provider.py`
- Test: `oasis-wiki/tests/test_game_ui_generation.py`

- [ ] **Step 1: Add the candidate record**

```python
@dataclass(frozen=True)
class ImageModelCandidate:
    model_id: str
    confidence: str
    evidence: tuple[str, ...]
```

- [ ] **Step 2: Preserve provider model metadata**

Implement `list_provider_model_records()` to validate `/models` data and return copied mapping records. Keep `list_provider_models()` as:

```python
def list_provider_models(connection: ProviderConnection) -> list[str]:
    return [record['id'] for record in list_provider_model_records(connection)]
```

- [ ] **Step 3: Implement deterministic classification**

Flatten safe metadata strings, classify explicit output capabilities as `confirmed`, known image-family IDs as `likely`, and generic image modality as `uncertain`. Merge configured models, de-duplicate by ID, accumulate evidence, and sort with `confirmed` before `likely` before `uncertain`.

- [ ] **Step 4: Add discovery CLI mode**

Make `--package` optional at parser level. When `--discover-image-models` is present, load the managed provider, call only `/models`, and print JSON containing provider source, provider hostname, candidate dictionaries, `generation_attempted: false`, and `selection_required: true`. In generation mode, explicitly reject a missing package and retain `--user-authorized-provider-direct`.

- [ ] **Step 5: Run focused tests and verify GREEN**

Run the Task 1 command and expect all three tests to pass.

- [ ] **Step 6: Run the provider test group**

Run:

```powershell
python -m unittest oasis-wiki.tests.test_game_ui_generation
```

Expected: all provider and generation-pipeline tests pass.

### Task 3: Encode The Skill Rule And Version

**Files:**
- Modify: `oasis-wiki/SKILL.md`
- Modify: `oasis-wiki/references/cowart-ui-workflow.md`
- Modify: `oasis-wiki/references/game-ui-design-system.md`
- Modify: `oasis-wiki/tests/cowart-ui-category.test.mjs`
- Modify: `oasis-wiki/VERSION`
- Modify: `oasis-wiki/tests/test_companion_versioning.py`

- [ ] **Step 1: Add documentation regression assertions**

Assert the Skill route and Cowart workflow contain `--discover-image-models`, require developer model selection, forbid automatic paid probing, and do not immediately stop because an official environment key is absent.

- [ ] **Step 2: Run the documentation test and verify RED**

Run:

```powershell
node --test oasis-wiki/tests/cowart-ui-category.test.mjs
```

Expected: failure because the discovery rule is not documented.

- [ ] **Step 3: Update the three instruction files**

Document the trigger, discovery command, candidate table fields, no-cost policy, selection gate, and no-candidate wording. Keep built-in `image_gen` preferred and actual provider generation explicitly authorized.

- [ ] **Step 4: Advance upstream version**

Set `oasis-wiki/VERSION` and its regression test to `1.260818.2`.

- [ ] **Step 5: Run documentation and full upstream tests**

Run Node documentation tests, `python -m unittest discover -s oasis-wiki/tests -p 'test_*.py'`, and `git diff --check`.

### Task 4: Synchronize Companion And Release Metadata

**Files:**
- Modify matching files under `skills/oasis-wiki/`
- Modify matching files under `src-tauri/resources/skill/`
- Modify: `.codex-plugin/plugin.json`
- Modify: `package.json`
- Modify: `package-lock.json`
- Modify: `src-tauri/Cargo.toml`
- Modify: `src-tauri/Cargo.lock`
- Modify: `src-tauri/tauri.conf.json`
- Modify: `tauri.build.conf.json`
- Modify: `src-tauri/src/skill/mod.rs`
- Modify: `src/windows/Settings.tsx`
- Modify: `tests/companion-versioning.test.mjs`

- [ ] **Step 1: Apply the exact upstream Skill changes twice**

Apply the same patch to `skills/oasis-wiki` and `src-tauri/resources/skill`; verify packaged files remain byte-identical.

- [ ] **Step 2: Advance Companion versions**

Set canonical fields to `1.260818.2` and MSI mapping to `1.26.818+2`. Add an explicit August 18 release assertion to the Node version test.

- [ ] **Step 3: Run complete release checks**

Run all Node tests, both Skill Python suites, TypeScript/Vite build, Rust tests, packaging equality, and `git diff --check`.

- [ ] **Step 4: Build MSI**

Build `Oasis Companion_1.26.818+2_x64_zh-CN.msi` from the committed clean Companion worktree and record SHA-256.

### Task 5: Publish And Read Back

**Files:**
- No source changes.

- [ ] **Step 1: Commit and push both repositories**

Push both release commits to `main`, create annotated `v1.260818.2` tags, and push the tags without force.

- [ ] **Step 2: Publish both GitHub Releases**

Mark both releases Latest and upload `Oasis.Companion_1.26.818+2_x64_zh-CN.msi` to `mislw/oasis-wiki-comp`.

- [ ] **Step 3: Publicly verify release state**

Read back public main/tag refs, Latest release metadata, asset name, size, and downloaded SHA-256.

- [ ] **Step 4: Install and verify runtime**

Install the publicly downloaded MSI, restart Companion, synchronize the installed Skill, and run `check_companion_skill_versions.py` until it reports `status=match` for `1.260818.2`.
