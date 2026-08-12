from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tomllib
import urllib.request
from pathlib import Path
from typing import Iterable

from generation_pipeline import (
    GenerationPipelineError,
    read_json,
    record_generation_result,
    validate_generation_package,
)


def resolve_provider_model(model_ids: Iterable[str], requested_suffix: str) -> str:
    candidates = [model_id for model_id in model_ids if isinstance(model_id, str)]
    if requested_suffix in candidates:
        return requested_suffix
    suffix_matches = [model_id for model_id in candidates if model_id.endswith(requested_suffix)]
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if len(suffix_matches) > 1:
        raise ValueError(f"ambiguous provider models for suffix {requested_suffix}: {suffix_matches}")
    raise ValueError(f"provider does not expose a model ending with {requested_suffix}")


def load_codex_provider(codex_home: Path) -> tuple[str, str]:
    config_path = codex_home / "config.toml"
    auth_path = codex_home / "auth.json"
    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise GenerationPipelineError(f"cannot read Codex provider config: {config_path}: {exc}") from exc
    provider_name = config.get("model_provider")
    providers = config.get("model_providers", {})
    provider = providers.get(provider_name, {}) if isinstance(providers, dict) else {}
    base_url = provider.get("base_url") if isinstance(provider, dict) else None
    base_url = base_url or config.get("base_url")
    if not isinstance(base_url, str) or not base_url.strip():
        raise GenerationPipelineError("Codex configured provider has no base_url")
    auth = read_json(auth_path)
    api_key = auth.get("OPENAI_API_KEY")
    if not isinstance(api_key, str) or not api_key:
        raise GenerationPipelineError("Codex managed provider authentication is unavailable")
    return base_url.rstrip("/"), api_key


def save_image_response(item: object, output: Path) -> None:
    b64_json = getattr(item, "b64_json", None)
    url = getattr(item, "url", None)
    output.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(b64_json, str) and b64_json:
        output.write_bytes(base64.b64decode(b64_json))
        return
    if isinstance(url, str) and url:
        urllib.request.urlretrieve(url, output)
        return
    raise GenerationPipelineError("provider returned neither b64_json nor url")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a game UI through the current Codex configured provider without requesting a user Key."
    )
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--user-authorized-provider-direct", action="store_true")
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--model-suffix", default="gpt-image-2")
    parser.add_argument("--size", default="auto")
    parser.add_argument("--quality", choices=("low", "medium", "high", "auto"), default="high")
    args = parser.parse_args()
    if not args.user_authorized_provider_direct:
        print("ERROR: provider-direct generation requires explicit user authorization", file=sys.stderr)
        return 2
    try:
        context = validate_generation_package(args.package)
        package = context["package"]
        request = context["request"]
        codex_home = (args.codex_home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))).resolve()
        base_url, api_key = load_codex_provider(codex_home)
        try:
            from openai import OpenAI, OpenAIError
        except ImportError as exc:
            raise GenerationPipelineError("the Codex Python runtime must provide the openai package") from exc
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            model_ids = [item.id for item in client.models.list().data]
        except OpenAIError as exc:
            raise GenerationPipelineError(f"Codex provider model discovery failed: {exc}") from exc
        model = resolve_provider_model(model_ids, args.model_suffix)
        prompt = (package / request["prompt_file"]).read_text(encoding="utf-8")
        reference_paths = [
            package / path
            for path in [*request["style_references"], *request["layout_references"]]
        ]
        opened = [path.open("rb") for path in reference_paths]
        try:
            try:
                response = client.images.edit(
                    model=model,
                    image=opened,
                    prompt=prompt,
                    size=args.size,
                    quality=args.quality,
                    output_format="png",
                )
            except OpenAIError as exc:
                raise GenerationPipelineError(f"Codex provider image generation failed: {exc}") from exc
        finally:
            for handle in opened:
                handle.close()
        if not response.data:
            raise GenerationPipelineError("Codex provider returned no generated images")
        scratch = package / ".provider-generated.png"
        save_image_response(response.data[0], scratch)
        try:
            result_path = record_generation_result(
                package,
                scratch,
                generation_backend="codex_provider_direct",
                model=model,
            )
        finally:
            scratch.unlink(missing_ok=True)
        result = read_json(result_path)
    except (GenerationPipelineError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "generation_result": str(result_path),
                "output_image": str(package / result["output_image"]),
                "generation_backend": "codex_provider_direct",
                "model": model,
                "credential_mode": "codex_managed",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
