"""Tests for delivered-only usage and per-activity outcomes."""
import tempfile
import unittest
from pathlib import Path
from scripts.activity_history import collect, report, session_files


class HistoryTests(unittest.TestCase):
    def make_session(self, directory, name, status, outcomes=""):
        path = Path(directory) / name
        path.write_text(
            "---\ndate: 2026-11-09\nsection: Beavers\nstatus: " + status +
            "\nactivities:\n  - rocket-building\n  - space-station-charades\n" +
            outcomes + "---\n# Session\n", encoding="utf-8")
        return path

    def test_planned_not_counted(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.make_session(d, "planned.md", "planned")
            self.assertEqual(collect([path]), [])

    def test_legacy_delivered_counts_both(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.make_session(d, "legacy.md", "delivered")
            self.assertEqual(len(collect([path])), 2)

    def test_partial_delivery_and_feedback(self):
        with tempfile.TemporaryDirectory() as d:
            outcomes = ('activity_outcomes:\n'
                        '  rocket-building:\n'
                        '    delivered: true\n'
                        '    leader: "Station leader"\n'
                        '    planned_minutes: 11\n'
                        '    actual_minutes: 15\n'
                        '    participants: 6\n'
                        '    feedback: "Great fun"\n'
                        '  space-station-charades:\n'
                        '    delivered: false\n')
            path = self.make_session(d, "partial.md", "delivered", outcomes)
            events = collect([path])
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["actual_minutes"], 15)
            self.assertEqual(events[0]["feedback"], "Great fun")
            self.assertEqual(report(events)[0]["uses"], 1)

    def test_invalid_outcome_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.make_session(d, "invalid.md", "delivered",
                "activity_outcomes:\n  unknown-activity:\n    delivered: true\n")
            with self.assertRaises(ValueError):
                collect([path])

    def test_session_discovery_ignores_readme(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "README.md").write_text("# Session plans\n", encoding="utf-8")
            session = self.make_session(d, "delivered.md", "delivered")
            self.assertEqual(list(session_files(root)), [session])


if __name__ == "__main__":
    unittest.main()
