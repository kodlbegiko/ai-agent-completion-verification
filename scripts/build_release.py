from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def included_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in {".git", "__pycache__"} or "__pycache__" in rel.parts:
            continue
        if path.suffix in {".pyc", ".zip"}:
            continue
        files.append(path)
    return sorted(files)


def main() -> None:
    report_md = ROOT / "results" / "reports" / "pilot-primary-pilot-report.md"
    report_pdf = ROOT / "results" / "reports" / "research-report.pdf"
    subprocess.run([sys.executable, "scripts/render_report_pdf.py", str(report_md), str(report_pdf)], cwd=ROOT, check=True)
    required = [
        report_pdf,
        report_md,
        ROOT / "results" / "tables" / "pilot-primary-metrics.csv",
        ROOT / "data" / "manifests" / "pilot-task-manifest.csv",
        ROOT / "evidence" / "environment" / "environment.json",
        ROOT / "evidence" / "environment" / "github-connector-preflight.json",
        ROOT / "artifacts" / "reproducibility-pilot.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"missing release inputs: {missing}")
    evidence_manifest = {
        "status": "PILOT PUBLICATION CANDIDATE - REAL-WORLD EFFECTIVENESS INCONCLUSIVE",
        "protocol_snapshot_tag": "protocol-v0.1.0",
        "task_count": 12,
        "valid_tasks": 12,
        "excluded_tasks": 0,
        "methods": ["V0", "V1", "V2", "V3", "V4"],
        "formal_verdict": "INCONCLUSIVE",
        "files": {str(path.relative_to(ROOT)): sha(path) for path in required},
    }
    evidence_path = ROOT / "evidence" / "publication" / "evidence-manifest.json"
    evidence_path.write_text(json.dumps(evidence_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    archive = ARTIFACTS / "reproduction-bundle.zip"
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in included_files():
            if path == archive:
                continue
            zf.write(path, path.relative_to(ROOT))
    release_files = required + [evidence_path, archive]
    sums = {str(path.relative_to(ROOT)): sha(path) for path in release_files}
    (ROOT / "SHA256SUMS").write_text("\n".join(f"{digest}  {name}" for name, digest in sorted(sums.items())) + "\n", encoding="utf-8")
    manifest = {
        "release_gate": "successful public CI on main and release-workflow completion",
        "formal_verdict": "INCONCLUSIVE",
        "assets": sums,
    }
    (ARTIFACTS / "local-release-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
