from __future__ import annotations

import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str
    elapsed_ns: int
    timed_out: bool


def run_python(script: Path, cwd: Path, timeout_seconds: float = 5.0) -> CommandResult:
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    started = time.perf_counter_ns()
    try:
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return CommandResult(
            completed.returncode,
            completed.stdout,
            completed.stderr,
            time.perf_counter_ns() - started,
            False,
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            124,
            exc.stdout or "",
            exc.stderr or "timeout",
            time.perf_counter_ns() - started,
            True,
        )
