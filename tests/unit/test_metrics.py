import unittest
from completion_verification.metrics import metric_record, wilson_interval


class MetricsTest(unittest.TestCase):
    def test_wilson_bounds(self):
        low, high = wilson_interval(5, 10)
        self.assertLess(low, 0.5)
        self.assertGreater(high, 0.5)

    def test_confusion_metrics(self):
        rows = [
            {"ground_truth_label": "COMPLETE", "predicted_label": "COMPLETE", "status": "OK"},
            {"ground_truth_label": "FAILED", "predicted_label": "FAILED", "status": "OK"},
            {"ground_truth_label": "FAILED", "predicted_label": "COMPLETE", "status": "OK"},
        ]
        record = metric_record(rows)
        self.assertEqual(record["tp"], 1)
        self.assertEqual(record["tn"], 1)
        self.assertEqual(record["fp"], 1)
        self.assertAlmostEqual(record["false_completion_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
