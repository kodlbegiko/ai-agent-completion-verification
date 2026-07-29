# Research Protocol v0.1.0

Protocol lock date: 2026-07-27

## Primary question

Can low-cost verification methods distinguish genuinely completed patches from false-completion patches with known ground truth?

## Pilot scope

This phase is a pipeline-feasibility study using 12 synthetic Python control tasks. It cannot support claims about real-world repositories, all coding agents, or all programming languages.

## Experimental unit

A task contains a candidate implementation, original public tests, agent-selected tests, hidden tests, an agent completion claim, static-risk expectations, and a locked ground-truth completion label.

## Methods

- V0 predicts completion from the agent claim alone.
- V1 predicts completion when agent-selected tests pass.
- V2 predicts completion when the original public suite passes.
- V3 rejects completion when predefined source/diff risk rules trigger.
- V4 predicts completion when hidden regression tests pass.

## Primary endpoint

False Completion Rate among ground-truth failed tasks.

## Secondary endpoints

Precision, recall, specificity, F1, false rejection rate, balanced accuracy, MCC, elapsed time, method error rate, and per-category recall.

## Inclusion

All generated tasks with valid schema, executable candidate code, public tests, hidden tests, and unambiguous machine-checkable ground truth.

## Exclusion

Schema failure, non-executable fixtures, missing test files, or ambiguous oracle. Exclusions are logged and never silently removed.

## Decision limits

With fewer than 60 tasks, the overall effectiveness conclusion remains INCONCLUSIVE. Pilot findings describe pipeline behavior only.

## Amendments

Any post-lock change to methods, thresholds, labels, or exclusions must be appended to `docs/protocol-amendments.md` with date and rationale.
