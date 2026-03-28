import datetime as dt
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from profile_dashboard.scripts.metrics import health_score


class TestMetrics(unittest.TestCase):
    def test_health_score_bounds(self):
        today = dt.date(2026, 3, 28)
        project = {
            "priority": "high",
            "stage": "mvp",
            "last_updated": "2026-03-28",
        }
        score = health_score(project, today)
        self.assertGreaterEqual(score, 1)
        self.assertLessEqual(score, 10)

    def test_stale_project_penalty(self):
        today = dt.date(2026, 3, 28)
        fresh = health_score({"priority": "medium", "stage": "poc", "last_updated": "2026-03-25"}, today)
        stale = health_score({"priority": "medium", "stage": "poc", "last_updated": "2026-01-01"}, today)
        self.assertGreater(fresh, stale)


if __name__ == "__main__":
    unittest.main()
