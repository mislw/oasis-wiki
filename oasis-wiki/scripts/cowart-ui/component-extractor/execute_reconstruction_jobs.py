#!/usr/bin/env python3
"""Execute provider-neutral reconstruction jobs or fail closed."""

import argparse
import json
import sys
from pathlib import Path

from image_reconstruction_executor import ReconstructionUnavailable, UNAVAILABLE_CODE, load_executor


def load_jobs(directory: Path):
    jobs = []
    for path in sorted(directory.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("artifact_type") == "layer_reconstruction_job":
            jobs.append((path, payload))
    return sorted(jobs, key=lambda item: (item[1].get("sequence", 0), item[1].get("target_component_id", "")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs-dir", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--executor", help="Provider plugin as module:Class.")
    args = parser.parse_args()
    jobs = load_jobs(args.jobs_dir)
    try:
        executor = load_executor(args.executor)
    except ReconstructionUnavailable as error:
        for path, job in jobs:
            job["status"] = "failed"
            job["error"] = str(error)
            job.setdefault("executor", {"required_capability": "image_edit_inpainting", "provider": None})
            job["executor"]["provider"] = None
            path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(str(error) or UNAVAILABLE_CODE, file=sys.stderr)
        return 2

    completed = set()
    results = []
    source_root = args.source_root or args.jobs_dir.parent
    for path, job in jobs:
        missing = [dependency for dependency in job.get("depends_on", []) if dependency not in completed]
        if missing:
            job["status"] = "failed"
            job["error"] = f"dependencies not reconstructed: {', '.join(missing)}"
            path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(job["error"], file=sys.stderr)
            return 1
        output = args.output_root / job["output"]
        if job.get("status") == "reconstructed" and output.is_file():
            completed.add(job["target_component_id"])
            results.append({
                "target_component_id": job["target_component_id"],
                "status": "reconstructed",
                "executor_id": job.get("executor", {}).get("provider") or executor.executor_id,
                "capability": "image_edit_inpainting",
                "output": job["output"],
                "reused": True,
            })
            continue
        job["status"] = "reconstructing"
        job["executor"]["provider"] = executor.executor_id
        path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = executor.reconstruct(job, source_root, args.output_root)
        if not output.is_file():
            job["status"] = "failed"
            job["error"] = f"executor did not create clean layer: {output}"
            path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(job["error"], file=sys.stderr)
            return 1
        job["status"] = "reconstructed"
        job["error"] = None
        path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        completed.add(job["target_component_id"])
        results.append({
            "target_component_id": job["target_component_id"],
            "status": "reconstructed",
            "executor_id": executor.executor_id,
            "capability": "image_edit_inpainting",
            "output": job["output"],
            "provider_result": result,
        })
    report = {
        "artifact_type": "layer_reconstruction_execution",
        "status": "completed",
        "executor_id": executor.executor_id,
        "capability": "image_edit_inpainting",
        "results": results,
    }
    report_path = args.output_root / "layer-reconstruction-execution.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
