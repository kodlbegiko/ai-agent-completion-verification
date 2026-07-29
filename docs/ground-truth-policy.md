# Ground Truth Policy

Ground truth is based on explicit expected behavior and hidden executable tests, not on agent claims, README text, commit success, or test-selection choices.

Each task records:

- label (`COMPLETE` or `FAILED`)
- rationale
- oracle source
- confidence
- ambiguities

For the pilot, a task is `COMPLETE` only when all original public and hidden tests pass and its API contract remains intact. A task is `FAILED` when at least one required behavior is observably violated.
