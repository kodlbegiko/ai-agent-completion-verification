import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class GroundTruthRegressionTest(unittest.TestCase):
    def test_locked_labels_match_oracle(self):
        for task_json in sorted((ROOT / "tasks" / "synthetic").glob("*/task.json")):
            root = task_json.parent
            meta = json.loads(task_json.read_text())
            public = subprocess.run([sys.executable, "public_tests.py"], cwd=root, capture_output=True, text=True)
            hidden = subprocess.run([sys.executable, "hidden_tests.py"], cwd=root, capture_output=True, text=True)
            observed = "COMPLETE" if public.returncode == 0 and hidden.returncode == 0 else "FAILED"
            self.assertEqual(observed, meta["ground_truth_label"], meta["task_id"])


if __name__ == "__main__":
    unittest.main()
