from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from completion_verification.methods import METHODS
from completion_verification.task_loader import load_tasks


def git_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "UNCOMMITTED"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    tasks = load_tasks(ROOT / "tasks" / "synthetic")
    out = ROOT / "results" / "raw" / f"{args.run_id}.jsonl"
    evidence_root = ROOT / "evidence" / "task-runs" / args.run_id
    evidence_root.mkdir(parents=True, exist_ok=True)
    rows = []
    commit_sha = git_commit()
    runtime_version = platform.python_version()
    lock_hash = hashlib.sha256(b"stdlib-only-python>=3.11").hexdigest()
    for task in tasks:
        for method in METHODS:
            result = method(task)
            evidence_dir = evidence_root / task.task_id
            evidence_dir.mkdir(parents=True, exist_ok=True)
            stdout_path = evidence_dir / f"{result.method}.stdout.txt"
            stderr_path = evidence_dir / f"{result.method}.stderr.txt"
            stdout_path.write_text(result.stdout, encoding="utf-8")
            stderr_path.write_text(result.stderr, encoding="utf-8")
            rows.append({
                "run_id": args.run_id,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "git_commit": commit_sha,
                "task_dataset_version": "pilot-v0.1.0",
                "method_version": "0.1.0",
                "runtime_version": runtime_version,
                "dependency_lock_hash": lock_hash,
                "random_seed": 20260727,
                "task_id": task.task_id,
                "failure_category": task.metadata["failure_category"],
                "method": result.method,
                "status": result.status,
                "reason": result.reason,
                "elapsed_ns": result.elapsed_ns,
                "result_label": result.predicted_label,
                "predicted_label": result.predicted_label,
                "ground_truth_label": task.ground_truth,
                "stdout_path": str(stdout_path.relative_to(ROOT)),
                "stderr_path": str(stderr_path.relative_to(ROOT)),
            })
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"wrote {len(rows)} results to {out}")


if __name__ == "__main__":
    main()
