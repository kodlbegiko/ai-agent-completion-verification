from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    root: Path
    metadata: dict

    @property
    def task_id(self) -> str:
        return str(self.metadata["task_id"])

    @property
    def ground_truth(self) -> str:
        return str(self.metadata["ground_truth_label"])


def load_tasks(tasks_root: Path) -> list[Task]:
    tasks: list[Task] = []
    for metadata_path in sorted(tasks_root.glob("*/task.json")):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        required = {"task_id", "ground_truth_label", "failure_category", "expected_behavior", "agent_claim"}
        missing = sorted(required - metadata.keys())
        if missing:
            raise ValueError(f"{metadata_path}: missing {missing}")
        tasks.append(Task(metadata_path.parent, metadata))
    return tasks
