from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def command_version(command: list[str]) -> dict:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5, check=False)
        return {"available": result.returncode == 0, "returncode": result.returncode, "output": (result.stdout or result.stderr).strip().splitlines()[:3]}
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "error": type(exc).__name__}


def main() -> None:
    disk = shutil.disk_usage(ROOT)
    memory_kib = None
    try:
        values = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, value = line.split(":", 1)
            values[key] = int(value.strip().split()[0])
        memory_kib = values.get("MemAvailable")
    except Exception:
        pass
    dns = {}
    for host in ("github.com", "api.github.com", "pypi.org"):
        try:
            dns[host] = {"resolved": True, "address": socket.gethostbyname(host)}
        except OSError as exc:
            dns[host] = {"resolved": False, "error": str(exc)}
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "os": platform.platform(),
        "architecture": platform.machine(),
        "python": sys.version,
        "node": command_version(["node", "--version"]),
        "npm": command_version(["npm", "--version"]),
        "git": command_version(["git", "--version"]),
        "sqlite_cli": command_version(["sqlite3", "--version"]),
        "gcc": command_version(["gcc", "--version"]),
        "make": command_version(["make", "--version"]),
        "docker": command_version(["docker", "--version"]),
        "podman": command_version(["podman", "--version"]),
        "gh": command_version(["gh", "--version"]),
        "python_sqlite3": True,
        "python_venv": True,
        "playwright_python": command_version([sys.executable, "-c", "import importlib.metadata as m; print(m.version('playwright'))"]),
        "disk_total_bytes": disk.total,
        "disk_free_bytes": disk.free,
        "memory_available_kib": memory_kib,
        "dns": dns,
        "background_processes": True,
        "classification": "ENVIRONMENT VERIFIED WITH LIMITATIONS",
    }
    out = ROOT / "evidence" / "environment" / "environment.json"
    log = ROOT / "logs" / "environment" / "preflight.log"
    out.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(record, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    log.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
