from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import tomllib
import urllib.error
import urllib.request
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from generation_pipeline import (
    GenerationPipelineError,
    read_json,
    record_generation_result,
    validate_generation_package,
)


@dataclass(frozen=True)
class ProviderConnection:
    base_url: str
    api_key: str
    configured_models: tuple[str, ...]
    source: str


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


def yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise GenerationPipelineError("invalid double-quoted YAML scalar") from exc
        return parsed if isinstance(parsed, str) else str(parsed)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value.split(" #", 1)[0].strip()


def yaml_mapping_value(text: str, path: tuple[str, ...]) -> str | None:
    stack: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if stripped.startswith("-"):
            continue
        match = re.fullmatch(r"([^:#][^:]*):(?:\s*(.*))?", stripped)
        if match is None:
            continue
        key = match.group(1).strip()
        raw_value = match.group(2) or ""
        while stack and stack[-1][0] >= indent:
            stack.pop()
        current_path = tuple(item[1] for item in stack) + (key,)
        if raw_value and current_path == path:
            return yaml_scalar(raw_value)
        if not raw_value:
            stack.append((indent, key))
    return None


def yaml_list_field(text: str, section_path: tuple[str, ...], field: str) -> tuple[str, ...]:
    stack: list[tuple[int, str]] = []
    values: list[str] = []
    item_pattern = re.compile(rf"-\s+{re.escape(field)}:\s*(.+)")
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        item_match = item_pattern.fullmatch(stripped)
        if item_match is not None:
            current_path = tuple(item[1] for item in stack)
            if current_path == section_path:
                values.append(yaml_scalar(item_match.group(1)))
            continue
        match = re.fullmatch(r"([^:#][^:]*):(?:\s*(.*))?", stripped)
        if match is None:
            continue
        key = match.group(1).strip()
        raw_value = match.group(2) or ""
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if not raw_value:
            stack.append((indent, key))
    return tuple(values)


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


def load_dsh_provider(dsh_home: Path) -> ProviderConnection:
    settings_path = dsh_home / "settings.yaml"
    credentials_path = dsh_home / ".credentials.yaml"
    try:
        settings = settings_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GenerationPipelineError(f"cannot read DSH provider config: {settings_path}: {exc}") from exc
    provider_name = yaml_mapping_value(settings, ("agent-default-model", "provider"))
    if not provider_name:
        raise GenerationPipelineError("DSH default provider is unavailable")
    provider_path = ("llm-pi-ai", "providers", provider_name)
    base_url = yaml_mapping_value(settings, (*provider_path, "baseURL"))
    api_key_env = yaml_mapping_value(settings, (*provider_path, "apiKeyEnv"))
    models = yaml_list_field(settings, (*provider_path, "models"), "id")
    if not base_url:
        raise GenerationPipelineError(f'DSH provider "{provider_name}" has no baseURL')
    if not api_key_env:
        raise GenerationPipelineError(f'DSH provider "{provider_name}" has no apiKeyEnv')
    try:
        credentials = credentials_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GenerationPipelineError(f"cannot read DSH managed credentials: {credentials_path}: {exc}") from exc
    api_key = yaml_mapping_value(credentials, (api_key_env,))
    if not api_key:
        raise GenerationPipelineError(f'DSH managed credential "{api_key_env}" is unavailable')
    return ProviderConnection(
        base_url=base_url.rstrip("/"),
        api_key=api_key,
        configured_models=models,
        source="dsh",
    )


def load_configured_provider(codex_home: Path, dsh_home: Path) -> ProviderConnection:
    try:
        base_url, api_key = load_codex_provider(codex_home)
    except GenerationPipelineError as codex_error:
        try:
            return load_dsh_provider(dsh_home)
        except GenerationPipelineError as dsh_error:
            raise GenerationPipelineError(
                f"no usable managed image provider; Codex: {codex_error}; DSH: {dsh_error}"
            ) from dsh_error
    return ProviderConnection(
        base_url=base_url,
        api_key=api_key,
        configured_models=(),
        source="codex",
    )


def provider_json_request(
    connection: ProviderConnection,
    path: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    content_type: str | None = None,
) -> dict[str, object]:
    headers = {
        "Authorization": f"Bearer {connection.api_key}",
        "Accept": "application/json",
    }
    if content_type is not None:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(
        f"{connection.base_url}{path}",
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read(512).decode("utf-8", errors="replace").replace(connection.api_key, "<redacted>")
        finally:
            exc.close()
        raise GenerationPipelineError(f"provider request {path} failed with HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        detail = str(exc.reason).replace(connection.api_key, "<redacted>")
        raise GenerationPipelineError(f"provider request {path} failed: {detail}") from exc
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise GenerationPipelineError(f"provider request {path} returned invalid JSON") from exc
    if not isinstance(parsed, dict):
        raise GenerationPipelineError(f"provider request {path} returned a non-object response")
    return parsed


def list_provider_models(connection: ProviderConnection) -> list[str]:
    response = provider_json_request(connection, "/models")
    data = response.get("data")
    if not isinstance(data, list):
        raise GenerationPipelineError("provider model discovery returned no data list")
    return [item["id"] for item in data if isinstance(item, dict) and isinstance(item.get("id"), str)]


def multipart_image_edit_body(
    model: str,
    prompt: str,
    reference_paths: Iterable[Path],
    size: str,
    quality: str,
) -> tuple[bytes, str]:
    boundary = f"dsh-image-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    def add_field(name: str, value: str) -> None:
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("ascii"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )

    for name, value in (
        ("model", model),
        ("prompt", prompt),
        ("size", size),
        ("quality", quality),
        ("output_format", "png"),
    ):
        add_field(name, value)
    for path in reference_paths:
        filename = path.name.replace('"', "_")
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="image[]"; filename="{filename}"\r\n'.encode("utf-8"),
                f"Content-Type: {content_type}\r\n\r\n".encode("ascii"),
                path.read_bytes(),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def create_image_edit(
    connection: ProviderConnection,
    model: str,
    prompt: str,
    reference_paths: Iterable[Path],
    size: str,
    quality: str,
) -> dict[str, object]:
    body, content_type = multipart_image_edit_body(model, prompt, reference_paths, size, quality)
    return provider_json_request(
        connection,
        "/images/edits",
        method="POST",
        body=body,
        content_type=content_type,
    )


def save_image_response(item: object, output: Path) -> None:
    b64_json = item.get("b64_json") if isinstance(item, Mapping) else getattr(item, "b64_json", None)
    url = item.get("url") if isinstance(item, Mapping) else getattr(item, "url", None)
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
    parser.add_argument("--dsh-home", type=Path)
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
        dsh_home = (args.dsh_home or Path(os.environ.get("DSH_HOME", Path.home() / ".dsh"))).resolve()
        connection = load_configured_provider(codex_home, dsh_home)
        model_ids = list_provider_models(connection)
        model = resolve_provider_model(model_ids, args.model_suffix)
        prompt = (package / request["prompt_file"]).read_text(encoding="utf-8")
        reference_paths = [
            package / path
            for path in [*request["style_references"], *request["layout_references"]]
        ]
        response = create_image_edit(connection, model, prompt, reference_paths, args.size, args.quality)
        response_data = response.get("data")
        if not isinstance(response_data, list) or not response_data:
            raise GenerationPipelineError("Codex provider returned no generated images")
        scratch = package / ".provider-generated.png"
        save_image_response(response_data[0], scratch)
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
                "provider_source": connection.source,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
