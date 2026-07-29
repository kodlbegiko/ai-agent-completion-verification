from __future__ import annotations

import math
from typing import Iterable


def safe_div(num: float, den: float) -> float | None:
    return None if den == 0 else num / den


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float | None, float | None]:
    if total == 0:
        return None, None
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


def confusion(rows: Iterable[dict]) -> dict[str, int]:
    counts = {"tp": 0, "tn": 0, "fp": 0, "fn": 0, "not_testable": 0}
    for row in rows:
        if row["status"] == "NOT_TESTABLE":
            counts["not_testable"] += 1
            continue
        truth = row["ground_truth_label"]
        pred = row["predicted_label"]
        if truth == "COMPLETE" and pred == "COMPLETE": counts["tp"] += 1
        elif truth == "FAILED" and pred == "FAILED": counts["tn"] += 1
        elif truth == "FAILED" and pred == "COMPLETE": counts["fp"] += 1
        elif truth == "COMPLETE" and pred == "FAILED": counts["fn"] += 1
        else: raise ValueError((truth, pred))
    return counts


def metric_record(rows: list[dict]) -> dict:
    c = confusion(rows)
    tp, tn, fp, fn = c["tp"], c["tn"], c["fp"], c["fn"]
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    f1 = None if precision is None or recall is None or precision + recall == 0 else 2 * precision * recall / (precision + recall)
    fcr = safe_div(fp, fp + tn)
    frr = safe_div(fn, fn + tp)
    balanced = None if recall is None or specificity is None else (recall + specificity) / 2
    mcc_den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = None if mcc_den == 0 else (tp * tn - fp * fn) / mcc_den
    fcr_ci = wilson_interval(fp, fp + tn)
    return {
        **c,
        "n_evaluable": tp + tn + fp + fn,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": f1,
        "false_completion_rate": fcr,
        "false_completion_rate_ci95_low": fcr_ci[0],
        "false_completion_rate_ci95_high": fcr_ci[1],
        "false_rejection_rate": frr,
        "balanced_accuracy": balanced,
        "mcc": mcc,
    }
