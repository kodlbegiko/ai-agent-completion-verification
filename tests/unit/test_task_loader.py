import unittest
from pathlib import Path
from completion_verification.task_loader import load_tasks

ROOT = Path(__file__).resolve().parents[2]


class TaskLoaderTest(unittest.TestCase):
    def test_loads_twelve_tasks(self):
        tasks = load_tasks(ROOT / "tasks" / "synthetic")
        self.assertEqual(len(tasks), 12)
        self.assertEqual(sum(t.ground_truth == "COMPLETE" for t in tasks), 6)
        self.assertEqual(sum(t.ground_truth == "FAILED" for t in tasks), 6)


if __name__ == "__main__":
    unittest.main()
