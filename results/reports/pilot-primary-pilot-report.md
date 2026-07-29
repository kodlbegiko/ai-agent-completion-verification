# Pilot Results

Input: `results/raw/pilot-primary.jsonl`

This is a 12-task synthetic pipeline pilot. It does not support general effectiveness claims.

| Method | TP | TN | FP | FN | FCR | 95% Wilson CI | Balanced accuracy | MCC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| V0 | 6 | 0 | 6 | 0 | 1.000 | 0.610–1.000 | 0.500 | NA |
| V1 | 6 | 0 | 6 | 0 | 1.000 | 0.610–1.000 | 0.500 | NA |
| V2 | 6 | 1 | 5 | 0 | 0.833 | 0.436–0.970 | 0.583 | 0.302 |
| V3 | 6 | 5 | 1 | 0 | 0.167 | 0.030–0.564 | 0.917 | 0.845 |
| V4 | 6 | 6 | 0 | 0 | 0.000 | 0.000–0.390 | 1.000 | 1.000 |

## Pilot interpretation

- V0 and V1 quantify the risk of trusting self-declaration or agent-selected tests.
- V2 shows the residual risk when original public tests do not cover required behavior.
- V3 is intentionally partial: static rules detect some suspicious patches but cannot prove behavioral correctness.
- V4 is the strongest oracle in this synthetic corpus because hidden tests encode the withheld requirements.

## Formal verdict

**INCONCLUSIVE for real-world effectiveness.** The infrastructure pilot is operational, but the sample is synthetic and below the 60-task threshold.
