# Analysis Plan

## Hypotheses

- H1: V4 hidden regression testing will have a lower false-completion rate than V0 and V1 in the synthetic control corpus.
- H2: V3 static rules will detect some but not all false-completion categories.
- H3: V2 original public tests will miss cases deliberately constructed outside public coverage.

## Primary endpoint

False Completion Rate = false completions / all ground-truth failures.

## Estimation

Report point estimates and 95% Wilson confidence intervals for bounded proportions. Report paired task-level confusion matrices, absolute differences, and MCC. Because this is a 12-task pilot, p-values are not used for effectiveness claims.

## Missing data

Method infrastructure failure is recorded as `NOT_TESTABLE` and excluded from that method's confusion-matrix denominator, while the count and reason remain visible.

## Multiple comparisons

No confirmatory significance claims are made in the pilot. Method comparisons are descriptive and pre-specified.

## Sensitivity analysis

Recalculate metrics treating `NOT_TESTABLE` as failure-to-verify and separately excluding it. No `NOT_TESTABLE` outcomes are expected in the frozen synthetic corpus.

## Ground-truth disputes

Synthetic labels require executable oracle agreement. Disputed cases become `AMBIGUOUS` and are excluded from primary metrics.
