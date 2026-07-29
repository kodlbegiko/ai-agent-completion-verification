from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    failures = []
    for task_json in sorted((ROOT / "tasks" / "synthetic").glob("*/task.json")):
        root = task_json.parent
        meta = json.loads(task_json.read_text(encoding="utf-8"))
        public = subprocess.run([sys.executable, "public_tests.py"], cwd=root, capture_output=True, text=True)
        hidden = subprocess.run([sys.executable, "hidden_tests.py"], cwd=root, capture_output=True, text=True)
        observed = "COMPLETE" if public.returncode == 0 and hidden.returncode == 0 else "FAILED"
        if observed != meta["ground_truth_label"]:
            failures.append({"task_id": meta["task_id"], "expected": meta["ground_truth_label"], "observed": observed})
    print(json.dumps({"valid": not failures, "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
