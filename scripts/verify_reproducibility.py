from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_pair() -> tuple[Path, Path]:
    commands = [
        [sys.executable, "scripts/run_evaluation.py", "--run-id", "repro-a"],
        [sys.executable, "scripts/run_evaluation.py", "--run-id", "repro-b"],
    ]
    processes = [subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) for command in commands]
    outputs = []
    for process in processes:
        output, _ = process.communicate()
        outputs.append(output)
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args, output=output)
    for output in outputs:
        print(output, end="")
    return ROOT / "results" / "raw" / "repro-a.jsonl", ROOT / "results" / "raw" / "repro-b.jsonl"


def canonical(path: Path) -> bytes:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        rows.append({
            "task_id": row["task_id"],
            "failure_category": row["failure_category"],
            "method": row["method"],
            "status": row["status"],
            "reason": row["reason"],
            "predicted_label": row["predicted_label"],
            "ground_truth_label": row["ground_truth_label"],
        })
    return (json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main() -> None:
    first, second = run_pair()
    hash_a = hashlib.sha256(canonical(first)).hexdigest()
    hash_b = hashlib.sha256(canonical(second)).hexdigest()
    record = {
        "canonical_sha256_a": hash_a,
        "canonical_sha256_b": hash_b,
        "match": hash_a == hash_b,
        "excluded_expected_variation": ["run_id", "timestamp_utc", "elapsed_ns", "stdout_path", "stderr_path"],
    }
    out = ROOT / "artifacts" / "reproducibility-pilot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, sort_keys=True))
    if not record["match"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
