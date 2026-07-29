import unittest
from pathlib import Path
from completion_verification.methods import METHODS
from completion_verification.task_loader import load_tasks

ROOT = Path(__file__).resolve().parents[2]


class MethodsIntegrationTest(unittest.TestCase):
    def test_all_methods_return_labels(self):
        for task in load_tasks(ROOT / "tasks" / "synthetic")[:2]:
            for method in METHODS:
                result = method(task)
                self.assertIn(result.predicted_label, {"COMPLETE", "FAILED"})
                self.assertIn(result.status, {"OK", "NOT_TESTABLE"})


if __name__ == "__main__":
    unittest.main()
