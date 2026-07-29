# Threat Model

Primary threats include oracle leakage, benchmark contamination, post-result threshold changes, task duplication, selective exclusion, malicious candidate code, resource exhaustion, nondeterminism, and accidental publication of secrets. The pilot mitigates these through frozen manifests, subprocess timeouts, output capture, deterministic canonical hashes, and explicit limitations. It is not a security sandbox.
