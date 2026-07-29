# AI Coding Agent Completion Verification

Status: **PILOT PUBLICATION CANDIDATE — REAL-WORLD EFFECTIVENESS INCONCLUSIVE**

This repository is a standard-library-only pilot for testing whether completion-verification methods can distinguish genuinely completed coding tasks from patches that appear complete but retain hidden failures.

## Scope

The pilot contains 12 synthetic control tasks with locked ground truth and five verification methods:

- V0: agent self-declaration
- V1: agent-selected tests
- V2: original public test suite
- V3: static and diff-risk rules
- V4: hidden regression tests

The pilot validates the research pipeline. It does **not** establish general effectiveness across real-world repositories or commercial coding agents. With fewer than 60 tasks and no real-world task layer, the formal effectiveness verdict remains `INCONCLUSIVE`.

## One-command verification

```bash
make verify
```

## Reproduction

```bash
python3 scripts/verify_reproducibility.py
```

The reproduction script performs two independent evaluations and compares canonical result hashes after excluding expected-to-vary timing and run metadata.

## Outputs

- `results/raw/`: task-level method results
- `results/tables/`: metrics and confusion matrices
- `results/reports/`: pilot report
- `evidence/environment/`: environment preflight evidence
- `evidence/task-runs/`: per-task stdout/stderr records
- `artifacts/`: reproducibility and release bundles

## Publication gate

The `v0.1.0-pilot` release is created only by `.github/workflows/release.yml` after the public `CI` workflow succeeds on `main`. The workflow re-runs the locked pilot gates, rebuilds all release assets, verifies SHA-256 checksums, creates the public protocol snapshot tag `protocol-v0.1.0`, and then creates the pilot tag and GitHub Release.

The public protocol tag records the first GitHub publication of the locally locked protocol. It must not be represented as proof of an externally preregistered study.

## Research status

See [`RESEARCH-STATUS.md`](RESEARCH-STATUS.md), [`docs/research-protocol.md`](docs/research-protocol.md), [`docs/analysis-plan.md`](docs/analysis-plan.md), and [`docs/limitations.md`](docs/limitations.md).
