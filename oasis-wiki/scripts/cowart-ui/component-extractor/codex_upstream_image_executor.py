from __future__ import annotations

from collections import deque
import base64
import io
import json
import math
import os
import re
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

from image_reconstruction_executor import ImageReconstructionExecutor, ReconstructionUnavailable, UNAVAILABLE_CODE


CHROMA_KEY = (255, 0, 255)
GENERATED_ALPHA_ALIGNMENT_PADDING = 3
PARENT_DESCENDANT_ENVELOPE_PADDING = 3


def merge_masked_edit(original: Image.Image, edited: Image.Image, edit_mask: Image.Image) -> Image.Image:
    original_rgba = original.convert("RGBA")
    edited_rgba = edited.convert("RGBA").resize(original_rgba.size, Image.Resampling.LANCZOS)
    return Image.composite(edited_rgba, original_rgba, edit_mask.convert("L"))


def _is_chroma_background(pixel: tuple[int, int, int, int], key: tuple[int, int, int]) -> bool:
    red, green, blue, alpha = pixel
    if alpha == 0:
        return True
    distance = math.sqrt((red - key[0]) ** 2 + (green - key[1]) ** 2 + (blue - key[2]) ** 2)
    magenta_dominance = min(red, blue) - green
    return distance <= 112 or magenta_dominance >= 16 or (alpha < 224 and max(red, green, blue) < 96)


def chroma_key_to_alpha(image: Image.Image, key: tuple[int, int, int] = CHROMA_KEY) -> Image.Image:
    result = image.convert("RGBA")
    pixels = result.load()
    width, height = result.size
    total = width * height
    background = bytearray(total)
    queue: deque[int] = deque()

    def enqueue(x: int, y: int):
        index = y * width + x
        if not background[index] and _is_chroma_background(pixels[x, y], key):
            background[index] = 1
            queue.append(index)

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(1, height - 1):
        enqueue(0, y)
        enqueue(width - 1, y)
    while queue:
        index = queue.popleft()
        x = index % width
        y = index // width
        if x > 0:
            enqueue(x - 1, y)
        if x + 1 < width:
            enqueue(x + 1, y)
        if y > 0:
            enqueue(x, y - 1)
        if y + 1 < height:
            enqueue(x, y + 1)

    for index, is_background in enumerate(background):
        if is_background:
            pixels[index % width, index // width] = (0, 0, 0, 0)

    visited = bytearray(total)
    components: list[list[int]] = []
    for start in range(total):
        if visited[start] or background[start]:
            continue
        x = start % width
        y = start // width
        if pixels[x, y][3] == 0:
            visited[start] = 1
            continue
        component = []
        component_queue = deque([start])
        visited[start] = 1
        while component_queue:
            index = component_queue.popleft()
            component.append(index)
            x = index % width
            y = index // width
            for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if not (0 <= next_x < width and 0 <= next_y < height):
                    continue
                next_index = next_y * width + next_x
                if visited[next_index] or background[next_index] or pixels[next_x, next_y][3] == 0:
                    continue
                visited[next_index] = 1
                component_queue.append(next_index)
        components.append(component)

    if components:
        minimum_area = max(3, round(max(len(component) for component in components) * 0.01))
        for component in components:
            if len(component) >= minimum_area:
                continue
            noise_like = True
            for index in component:
                red, green, blue, _alpha = pixels[index % width, index // width]
                if max(red, green, blue) >= 96 and min(red, blue) - green < 12:
                    noise_like = False
                    break
            if not noise_like:
                continue
            for index in component:
                pixels[index % width, index // width] = (0, 0, 0, 0)
    return result


def _plan_instance_bounds(source_root: Path) -> dict[str, dict[str, float]]:
    plan_path = source_root / "extraction-plan.json"
    if not plan_path.is_file():
        return {}
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    return {
        instance["node_id"]: instance["bounds"]
        for component in plan.get("components", [])
        for instance in component.get("instances", [])
        if isinstance(instance.get("bounds"), dict)
    }


def _mask_from_asset(path: Path, bounds: dict[str, float], crop_bounds: dict[str, float]) -> Image.Image:
    with Image.open(path) as asset:
        if "A" in asset.getbands():
            alpha = asset.convert("RGBA").getchannel("A")
        else:
            alpha = asset.convert("L")
    width = max(1, round(bounds["width"]))
    height = max(1, round(bounds["height"]))
    alpha = alpha.resize((width, height), Image.Resampling.LANCZOS)
    layer = Image.new("L", (round(crop_bounds["width"]), round(crop_bounds["height"])), 0)
    layer.paste(alpha, (round(bounds["x"] - crop_bounds["x"]), round(bounds["y"] - crop_bounds["y"])))
    return layer


def build_union_mask(job: dict[str, Any], source_root: Path, crop_bounds: dict[str, float]) -> Image.Image:
    width = max(1, round(crop_bounds["width"]))
    height = max(1, round(crop_bounds["height"]))
    union = Image.new("L", (width, height), 0)
    instance_bounds = _plan_instance_bounds(source_root)
    for source in (job.get("mask") or {}).get("sources", []):
        bounds = source.get("bounds") or instance_bounds.get(source.get("node_id"))
        if not isinstance(bounds, dict):
            continue
        asset_value = source.get("path")
        asset_path = source_root / asset_value if isinstance(asset_value, str) else None
        if asset_path and asset_path.is_file():
            layer = _mask_from_asset(asset_path, bounds, crop_bounds)
            if source.get("source_type") == "clean_layer_alpha":
                padding = max(0, round(source.get("padding", GENERATED_ALPHA_ALIGNMENT_PADDING)))
                if padding:
                    layer = layer.filter(ImageFilter.MaxFilter(padding * 2 + 1))
        else:
            layer = Image.new("L", (width, height), 0)
            padding = max(0, round(source.get("padding", 0)))
            left = round(bounds["x"] - crop_bounds["x"]) - padding
            top = round(bounds["y"] - crop_bounds["y"]) - padding
            right = round(bounds["x"] + bounds["width"] - crop_bounds["x"]) + padding
            bottom = round(bounds["y"] + bounds["height"] - crop_bounds["y"]) + padding
            ImageDraw.Draw(layer).rectangle((left, top, right, bottom), fill=255)
        union = ImageChops.lighter(union, layer)
    if job.get("category") in {"panel", "background", "window"}:
        descendant_bounds = union.getbbox()
        if descendant_bounds:
            left, top, right, bottom = descendant_bounds
            padding = PARENT_DESCENDANT_ENVELOPE_PADDING
            envelope = Image.new("L", (width, height), 0)
            ImageDraw.Draw(envelope).rectangle(
                (
                    max(0, left - padding),
                    max(0, top - padding),
                    min(width - 1, right - 1 + padding),
                    min(height - 1, bottom - 1 + padding),
                ),
                fill=255,
            )
            union = ImageChops.lighter(union, envelope)
    return union


def _border_color(image: Image.Image) -> tuple[int, int, int, int]:
    rgba = image.convert("RGBA")
    samples = Image.new("RGBA", (4, 1))
    samples.putdata([
        rgba.getpixel((0, 0)),
        rgba.getpixel((rgba.width - 1, 0)),
        rgba.getpixel((0, rgba.height - 1)),
        rgba.getpixel((rgba.width - 1, rgba.height - 1)),
    ])
    return tuple(round(value) for value in ImageStat.Stat(samples).mean)


def _api_canvas(image: Image.Image, edit_mask: Image.Image | None = None, background: tuple[int, int, int] | None = None):
    width, height = image.size
    valid_native = width * height >= 655_360 and max(width, height) / min(width, height) <= 3
    if valid_native:
        canvas_size = (math.ceil(width / 16) * 16, math.ceil(height / 16) * 16)
        scale = 1.0
    else:
        canvas_size = (1024, 1024)
        scale = min(960 / width, 960 / height)
    rendered_size = (max(1, round(width * scale)), max(1, round(height * scale)))
    offset = ((canvas_size[0] - rendered_size[0]) // 2, (canvas_size[1] - rendered_size[1]) // 2)
    fill = (*background, 255) if background else _border_color(image)
    canvas = Image.new("RGBA", canvas_size, fill)
    canvas.paste(image.convert("RGBA").resize(rendered_size, Image.Resampling.LANCZOS), offset)
    api_mask = None
    if edit_mask is not None:
        scaled_mask = edit_mask.convert("L").resize(rendered_size, Image.Resampling.NEAREST)
        transparent_hole = Image.new("RGBA", rendered_size, (0, 0, 0, 0))
        rendered = canvas.crop((offset[0], offset[1], offset[0] + rendered_size[0], offset[1] + rendered_size[1]))
        rendered = Image.composite(transparent_hole, rendered, scaled_mask)
        canvas.paste(rendered, offset)
        alpha = Image.new("L", canvas_size, 255)
        alpha.paste(Image.eval(scaled_mask, lambda value: 255 - value), offset)
        api_mask = Image.new("RGBA", canvas_size, (255, 255, 255, 255))
        api_mask.putalpha(alpha)
    return canvas, api_mask, {"offset": offset, "rendered_size": rendered_size, "source_size": image.size}


def _restore_api_region(image: Image.Image, transform: dict[str, Any]) -> Image.Image:
    offset_x, offset_y = transform["offset"]
    width, height = transform["rendered_size"]
    restored = image.convert("RGBA").crop((offset_x, offset_y, offset_x + width, offset_y + height))
    return restored.resize(transform["source_size"], Image.Resampling.LANCZOS)


def _fit_transparent_subject(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    alpha = image.getchannel("A")
    bounds = alpha.getbbox()
    if not bounds:
        raise ValueError("image edit returned no foreground artwork")
    subject = image.crop(bounds)
    scale = min((size[0] - 4) / subject.width, (size[1] - 4) / subject.height)
    rendered = subject.resize((max(1, round(subject.width * scale)), max(1, round(subject.height * scale))), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.alpha_composite(rendered, ((size[0] - rendered.width) // 2, (size[1] - rendered.height) // 2))
    return output


class CodexUpstreamImageReconstructionExecutor(ImageReconstructionExecutor):
    executor_id = "codex-upstream-gpt-image-2"

    def __init__(self):
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        auth_path = codex_home / "auth.json"
        config_path = codex_home / "config.toml"
        if not auth_path.is_file() or not config_path.is_file():
            raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: Codex auth/config not found")
        auth = json.loads(auth_path.read_text(encoding="utf-8-sig"))
        self.api_key = os.environ.get("COWART_IMAGE_API_KEY") or auth.get("OPENAI_API_KEY")
        config = config_path.read_text(encoding="utf-8-sig", errors="replace")
        base_match = re.search(r'base_url\s*=\s*"([^"]+)"', config)
        self.base_url = (os.environ.get("COWART_IMAGE_BASE_URL") or (base_match.group(1) if base_match else "")).rstrip("/")
        self.model = os.environ.get("COWART_IMAGE_MODEL", "[l]gpt-image-2")
        self.quality = os.environ.get("COWART_IMAGE_QUALITY", "low")
        if not self.api_key or not self.base_url:
            raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: upstream credentials are incomplete")

    def capabilities(self) -> set[str]:
        return {"image_edit_inpainting"}

    def _multipart_edit(self, image: Image.Image, prompt: str, mask: Image.Image | None = None) -> Image.Image:
        boundary = "----CodexBoundary" + uuid.uuid4().hex
        parts: list[bytes] = []

        def field(name: str, value: str):
            parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode())

        def image_part(name: str, value: Image.Image):
            buffer = io.BytesIO()
            value.convert("RGBA").save(buffer, "PNG")
            parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{name}.png"\r\nContent-Type: image/png\r\n\r\n').encode() + buffer.getvalue() + b"\r\n")

        for name, value in (
            ("model", self.model),
            ("prompt", prompt),
            ("quality", self.quality),
            ("size", f"{image.width}x{image.height}"),
            ("output_format", "png"),
            ("n", "1"),
        ):
            field(name, value)
        image_part("image", image)
        if mask is not None:
            image_part("mask", mask)
        payload = b"".join(parts) + f"--{boundary}--\r\n".encode()
        request = urllib.request.Request(
            self.base_url + "/images/edits",
            data=payload,
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "multipart/form-data; boundary=" + boundary,
                "Accept": "application/json",
                "User-Agent": "Cowart-Layer-Reconstruction/1.0",
            },
            method="POST",
        )
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=360) as response:
                    result = json.loads(response.read())
                item = (result.get("data") or [{}])[0]
                if item.get("b64_json"):
                    return Image.open(io.BytesIO(base64.b64decode(item["b64_json"]))).convert("RGBA")
                if item.get("url"):
                    with urllib.request.urlopen(item["url"], timeout=180) as response:
                        return Image.open(io.BytesIO(response.read())).convert("RGBA")
                raise ValueError("image edit response has no image")
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as error:
                last_error = error
                if attempt < 2:
                    time.sleep(2 ** attempt)
        raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: upstream image edit failed: {last_error}")

    def _extract_transparent(self, image: Image.Image, target: str) -> Image.Image:
        canvas, _mask, transform = _api_canvas(image, background=CHROMA_KEY)
        edited = self._multipart_edit(
            canvas,
            f"Extract only {target} from the supplied game UI crop. Preserve its silhouette, materials, lighting, and complete edges. "
            "Remove all surrounding panel background, text, numbers, badges, and unrelated controls. Place the isolated asset on a perfectly flat solid #ff00ff background with no shadow outside the asset, no gradient, no texture, and no watermark.",
        )
        keyed = chroma_key_to_alpha(edited, CHROMA_KEY)
        restored = _restore_api_region(keyed, transform)
        return _fit_transparent_subject(restored, image.size)

    def reconstruct(self, job: dict[str, Any], source_root: Path, output_root: Path) -> dict[str, Any]:
        source_path = source_root / job["source_image"]
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        bounds = job["instances"][0]["bounds"]
        crop_box = (
            round(bounds["x"]),
            round(bounds["y"]),
            round(bounds["x"] + bounds["width"]),
            round(bounds["y"] + bounds["height"]),
        )
        with Image.open(source_path) as source:
            crop = source.convert("RGBA").crop(crop_box)
        if job["mode"] == "extract_artwork":
            clean = self._extract_transparent(crop, job["target_component_id"])
            edited_pixels = clean.getchannel("A").getbbox()
        else:
            edit_mask = build_union_mask(job, source_root, bounds)
            if not edit_mask.getbbox():
                raise ValueError(f"{job['target_component_id']} has no reconstruction mask")
            canvas, api_mask, transform = _api_canvas(crop, edit_mask)
            edited = self._multipart_edit(
                canvas,
                f"Reconstruct the clean {job['category']} layer {job['target_component_id']}. The transparent mask is a hole where descendant layers were removed. "
                "Continue only this layer's underlying material, texture, border, and lighting through the hole. Remove every child control, text, icon, value, badge, shadow, bevel, and outline in the masked area. "
                "For a parent panel or background, the repaired area must be uninterrupted panel or background substrate: do not recreate blank buttons, cards, tabs, frames, rounded rectangles, separators, or any other child-shaped structure. "
                "For a button, row, or card skin, restore only that component's own continuous skin without text or icons. Preserve unmasked context exactly. No new text, symbols, controls, or decoration.",
                api_mask,
            )
            restored = _restore_api_region(edited, transform)
            clean = merge_masked_edit(crop, restored, edit_mask)
            if job["category"] in {"button", "row", "card"}:
                clean = self._extract_transparent(clean, job["target_component_id"])
            edited_pixels = edit_mask.getbbox()
        output = output_root / job["output"]
        output.parent.mkdir(parents=True, exist_ok=True)
        clean.save(output, "PNG")
        return {
            "method": "masked_image_edit",
            "mask_strategy": "descendant_envelope_fallback" if job["category"] in {"panel", "background", "window"} else "union_priority_mask",
            "model": self.model,
            "quality": self.quality,
            "source_bounds": bounds,
            "edited_bounds": edited_pixels,
            "output_size": clean.size,
        }
