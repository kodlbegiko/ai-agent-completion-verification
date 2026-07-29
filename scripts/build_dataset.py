from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks" / "synthetic"
MANIFEST = ROOT / "data" / "manifests" / "pilot-task-manifest.json"
MANIFEST_CSV = ROOT / "data" / "manifests" / "pilot-task-manifest.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    records = []
    for task_json in sorted(TASKS.glob("*/task.json")):
        task_root = task_json.parent
        meta = json.loads(task_json.read_text(encoding="utf-8"))
        files = {}
        for path in sorted(task_root.iterdir()):
            if path.is_file():
                files[path.name] = sha256(path)
        records.append({"task_id": meta["task_id"], "ground_truth_label": meta["ground_truth_label"], "failure_category": meta["failure_category"], "files": files})
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"dataset_version": "pilot-v0.1.0", "task_count": len(records), "tasks": records}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["task_id", "ground_truth_label", "failure_category", "task_json_sha256", "candidate_sha256", "public_tests_sha256", "agent_tests_sha256", "hidden_tests_sha256"])
        writer.writeheader()
        for record in records:
            files = record["files"]
            writer.writerow({
                "task_id": record["task_id"],
                "ground_truth_label": record["ground_truth_label"],
                "failure_category": record["failure_category"],
                "task_json_sha256": files["task.json"],
                "candidate_sha256": files["candidate.py"],
                "public_tests_sha256": files["public_tests.py"],
                "agent_tests_sha256": files["agent_tests.py"],
                "hidden_tests_sha256": files["hidden_tests.py"],
            })
    print(f"built manifest for {len(records)} tasks: {MANIFEST} and {MANIFEST_CSV}")


if __name__ == "__main__":
    main()
