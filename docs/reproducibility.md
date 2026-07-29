# Reproducibility

Run `make verify`. The repository uses only Python's standard library. `scripts/verify_reproducibility.py` runs the evaluation twice and compares canonical task/method decisions while excluding timestamps, run identifiers, and elapsed-time fields that are expected to vary.
