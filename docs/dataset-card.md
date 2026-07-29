# Dataset Card

## Name

Synthetic Completion Verification Pilot v0.1.0

## Size

12 tasks: 6 complete and 6 false-completion controls.

## Purpose

Validate evaluation plumbing and characterize obvious differences among V0–V4 before acquiring real-world tasks.

## Failure categories

Boundary condition, wrong return type, exception handling, state pollution, hardcoded example, and weakened tests.

## Limitations

The tasks are synthetic, small, Python-only, standard-library-only, and intentionally diagnostic. Results cannot be generalized to real software maintenance without a real-world corpus.
