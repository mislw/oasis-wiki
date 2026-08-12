#!/usr/bin/env python3
"""Place reconstructed transparent PNG assets back into their UI-tree positions."""

import argparse
import sys
from pathlib import Path

from validate_extraction_plan import load_json, validate_plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--assets-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--background", type=Path)
    args = parser.parse_args()
    try:
        from PIL import Image
    except ImportError:
        print("recompose_ui.py requires Pillow: install with python -m pip install Pillow", file=sys.stderr)
        return 1
    try:
        plan = validate_plan(load_json(args.plan))
        page_size = plan["source"]["page_size"]
        if args.background:
            canvas = Image.open(args.background).convert("RGBA")
            if canvas.size != (page_size["width"], page_size["height"]):
                raise ValueError("background dimensions must match source.page_size")
        else:
            canvas = Image.new("RGBA", (page_size["width"], page_size["height"]), (0, 0, 0, 0))
        for component in plan["components"]:
            if component["output"] is None:
                continue
            asset_path = args.assets_dir / component["output"]
            if not asset_path.is_file():
                raise ValueError(f"missing reconstructed asset: {asset_path}")
            asset = Image.open(asset_path).convert("RGBA")
            for instance in component["instances"]:
                bounds = instance["bounds"]
                rendered = asset.resize((bounds["width"], bounds["height"]), Image.Resampling.LANCZOS)
                canvas.alpha_composite(rendered, (bounds["x"], bounds["y"]))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(args.output, "PNG")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Wrote recomposed preview: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
