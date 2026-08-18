# Upstream Image Model Discovery Design

## Problem

The Oasis UI generation workflow can currently stop after observing that the process environment does not contain an official `OPENAI_API_KEY` or that a hard-coded image model is unavailable. That is incorrect when Codex or DSH is configured with a managed custom provider: the provider key and base URL may already exist, and its upstream `/models` endpoint may expose another image-capable model.

## Goals

- Before reporting image generation as unavailable, inspect the active Codex or DSH managed provider.
- Perform a read-only `/models` lookup without generating an image or creating billable output.
- Classify upstream models as `confirmed`, `likely`, or `uncertain` image candidates.
- List candidates with evidence and require the developer to choose a model before generation.
- Never print, persist, or return the provider API key.
- Keep actual provider-direct image generation behind the existing explicit authorization gate.

## Non-Goals

- Do not send an automatic image generation or image edit probe.
- Do not silently choose a discovered model, even when only one candidate exists.
- Do not add a generic external CLI fallback or HTML screenshot fallback.
- Do not change the built-in `image_gen` preference when that tool is available.

## Current Flow

`scripts/game-ui/generate_with_codex_provider.py` already:

1. Reads the active Codex provider from `config.toml` and managed authentication from `auth.json`.
2. Falls back to the configured DSH provider and managed credentials.
3. Calls `/models` and resolves a requested model suffix.
4. Requires `--user-authorized-provider-direct` before posting to `/images/edits`.

The missing behavior is a non-generating discovery mode plus Skill instructions that route missing-official-key situations through it.

## Discovery API

Add an immutable `ImageModelCandidate` record:

```python
@dataclass(frozen=True)
class ImageModelCandidate:
    model_id: str
    confidence: str
    evidence: tuple[str, ...]
```

Add these functions to `generate_with_codex_provider.py`:

```python
def list_provider_model_records(connection: ProviderConnection) -> list[dict[str, object]]: ...

def discover_image_model_candidates(
    records: Iterable[Mapping[str, object]],
    configured_models: Iterable[str] = (),
) -> list[ImageModelCandidate]: ...
```

`list_provider_models()` remains as a compatibility wrapper returning model IDs.

## Classification

Classification is metadata-first and does not make paid requests:

- `confirmed`: model metadata explicitly names image generation/edit output or image endpoints such as `image_generation`, `text_to_image`, `image_edit`, `/images/generations`, or `/images/edits`.
- `likely`: the model ID matches a known image-family token such as `gpt-image`, `dall-e`, `flux`, `imagen`, `seedream`, `recraft`, `ideogram`, or `stable-diffusion`.
- `uncertain`: metadata mentions image modality but does not distinguish image input from image output.

Configured DSH model IDs are merged into discovery even when the upstream response omits them. Results are de-duplicated and sorted by confidence, then model ID.

## CLI Contract

Add `--discover-image-models` to `generate_with_codex_provider.py`.

Discovery mode:

- Does not require `--package`.
- Does not require `--user-authorized-provider-direct` because it performs only `GET /models`.
- Never calls `/images/edits`.
- Returns JSON containing the provider source, provider hostname, model count, candidates, `generation_attempted: false`, and `selection_required: true`.
- Returns an empty candidate list when no image-capable model can be inferred.
- Keeps bounded, key-redacted provider errors.

Generation mode keeps the current authorization and package requirements unchanged.

## Skill Behavior

Update `SKILL.md`, `references/cowart-ui-workflow.md`, and `references/game-ui-design-system.md` with this rule:

1. Do not stop only because the process environment lacks an official OpenAI key or a hard-coded image model.
2. If the built-in `image_gen` tool is unavailable, or the configured image model cannot be resolved, run provider discovery first.
3. Present `model ID`, `confidence`, `evidence`, and `provider source` to the developer.
4. Require a model selection before provider-direct generation.
5. If discovery returns no candidates, report that the configured upstream exposed no identifiable image model; do not falsely claim that no key exists.

## Security

- Authorization headers remain internal to `urllib.request`.
- Output includes only the normalized provider hostname, never the complete key or credential file contents.
- HTTP error bodies remain bounded to 512 bytes and replace the active key with `<redacted>`.
- Discovery makes no POST request and writes no generated files.

## Verification And Release

- Add unit tests for metadata, name, ambiguous modality, configured-model fallback, sorting, and secret-safe output.
- Add a CLI test proving discovery makes only `GET /models` and does not require package or generation authorization.
- Add documentation regressions preventing immediate failure on missing official `OPENAI_API_KEY`.
- Synchronize upstream, plugin, bundled, and installed Skill copies.
- Advance the release to `1.260818.2`, run all Node/Python/Rust/build checks, publish both GitHub Releases, upload the matching MSI, install it, and require `status=match`.
