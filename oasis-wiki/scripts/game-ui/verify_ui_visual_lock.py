#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def difference_bounds(points: list[tuple[int, int]]) -> list[int] | None:
    if not points:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return [min(xs), min(ys), max(xs) + 1, max(ys) + 1]


def verify_visual_lock(
    baseline_path: Path,
    candidate_path: Path,
    editable_mask_path: Path | None,
    diff_image_path: Path | None,
) -> dict:
    baseline_path = baseline_path.resolve()
    candidate_path = candidate_path.resolve()
    baseline = Image.open(baseline_path).convert("RGBA")
    candidate = Image.open(candidate_path).convert("RGBA")
    if baseline.size != candidate.size:
        raise ValueError(
            f"baseline and candidate dimensions differ: {baseline.size} != {candidate.size}"
        )

    if editable_mask_path is None:
        mask = Image.new("L", baseline.size, 0)
        mask_sha256 = None
    else:
        editable_mask_path = editable_mask_path.resolve()
        mask = Image.open(editable_mask_path).convert("L")
        if mask.size != baseline.size:
            raise ValueError(
                f"editable mask dimensions differ: {mask.size} != {baseline.size}"
            )
        mask_sha256 = sha256_file(editable_mask_path)

    baseline_pixels = baseline.load()
    candidate_pixels = candidate.load()
    mask_pixels = mask.load()
    diff = Image.new("RGBA", baseline.size, (0, 0, 0, 0))
    diff_pixels = diff.load()
    changed_total: list[tuple[int, int]] = []
    changed_locked: list[tuple[int, int]] = []
    changed_editable: list[tuple[int, int]] = []

    for y in range(baseline.height):
        for x in range(baseline.width):
            if baseline_pixels[x, y] == candidate_pixels[x, y]:
                continue
            changed_total.append((x, y))
            if mask_pixels[x, y] > 0:
                changed_editable.append((x, y))
                diff_pixels[x, y] = (255, 196, 0, 255)
            else:
                changed_locked.append((x, y))
                diff_pixels[x, y] = (255, 0, 0, 255)

    if diff_image_path is not None:
        diff_image_path = diff_image_path.resolve()
        diff_image_path.parent.mkdir(parents=True, exist_ok=True)
        diff.save(diff_image_path)

    return {
        "schema_version": 1,
        "artifact_type": "ui_visual_lock_report",
        "status": "pass" if not changed_locked else "fail",
        "baseline": {
            "path": str(baseline_path),
            "sha256": sha256_file(baseline_path),
        },
        "candidate": {
            "path": str(candidate_path),
            "sha256": sha256_file(candidate_path),
        },
        "editable_mask": (
            {"path": str(editable_mask_path), "sha256": mask_sha256}
            if editable_mask_path is not None
            else None
        ),
        "dimensions": [baseline.width, baseline.height],
        "changed_pixels_total": len(changed_total),
        "changed_pixels_editable": len(changed_editable),
        "changed_pixels_locked": len(changed_locked),
        "locked_difference_bounds": difference_bounds(changed_locked),
        "diff_image": str(diff_image_path) if diff_image_path is not None else None,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify that a UI candidate changed only inside an editable mask."
    )
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--editable-mask", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--diff-image", type=Path)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    report = verify_visual_lock(
        args.baseline,
        args.candidate,
        args.editable_mask,
        args.diff_image,
    )
    args.report = args.report.resolve()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
