from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from completion_verification.metrics import metric_record


def fmt(value):
    return "NA" if value is None else f"{value:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    path = ROOT / args.input
    for output_dir in (ROOT / "results" / "tables", ROOT / "results" / "reports"):
        output_dir.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)
    metrics = {method: metric_record(method_rows) for method, method_rows in sorted(grouped.items())}
    table_json = ROOT / "results" / "tables" / f"{path.stem}-metrics.json"
    table_csv = ROOT / "results" / "tables" / f"{path.stem}-metrics.csv"
    table_json.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fields = ["method", "n_evaluable", "tp", "tn", "fp", "fn", "not_testable", "precision", "recall", "specificity", "f1", "false_completion_rate", "false_completion_rate_ci95_low", "false_completion_rate_ci95_high", "false_rejection_rate", "balanced_accuracy", "mcc"]
    with table_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for method, record in metrics.items():
            writer.writerow({"method": method, **record})
    report = ROOT / "results" / "reports" / f"{path.stem}-pilot-report.md"
    lines = [
        "# Pilot Results",
        "",
        f"Input: `{path.relative_to(ROOT)}`",
        "",
        "This is a 12-task synthetic pipeline pilot. It does not support general effectiveness claims.",
        "",
        "| Method | TP | TN | FP | FN | FCR | 95% Wilson CI | Balanced accuracy | MCC |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method, record in metrics.items():
        ci = f"{fmt(record['false_completion_rate_ci95_low'])}–{fmt(record['false_completion_rate_ci95_high'])}"
        lines.append(f"| {method} | {record['tp']} | {record['tn']} | {record['fp']} | {record['fn']} | {fmt(record['false_completion_rate'])} | {ci} | {fmt(record['balanced_accuracy'])} | {fmt(record['mcc'])} |")
    lines += [
        "",
        "## Pilot interpretation",
        "",
        "- V0 and V1 quantify the risk of trusting self-declaration or agent-selected tests.",
        "- V2 shows the residual risk when original public tests do not cover required behavior.",
        "- V3 is intentionally partial: static rules detect some suspicious patches but cannot prove behavioral correctness.",
        "- V4 is the strongest oracle in this synthetic corpus because hidden tests encode the withheld requirements.",
        "",
        "## Formal verdict",
        "",
        "**INCONCLUSIVE for real-world effectiveness.** The infrastructure pilot is operational, but the sample is synthetic and below the 60-task threshold.",
    ]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))
    print(f"wrote {table_csv}, {table_json}, {report}")


if __name__ == "__main__":
    main()
