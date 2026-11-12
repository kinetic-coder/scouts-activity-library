"""Regression tests for the existing Markdown leader-pack assembler."""
import tempfile
import unittest
from pathlib import Path
from scripts.build_leader_pack import ROOT, build, parse_activity_ids, split_frontmatter


class LeaderPackTests(unittest.TestCase):
    def test_existing_space_night(self):
        plan = ROOT / "sessions/2026-11-09-beavers-space-night.md"
        self.assertTrue(plan.exists(), "Expected existing session fixture is missing")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "space-night-pack.md"
            build(plan, output)
            text = output.read_text(encoding="utf-8")
            self.assertIn("## Meeting plan", text)
            self.assertIn("## Detailed activity instructions", text)
            for activity in (
                "earth-solar-system-mission",
                "robotic-arm-mission-control",
                "rocket-building",
                "space-station-charades",
            ):
                self.assertEqual(text.count("### Activity: " + activity), 1)

    def test_missing_activity_fails(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            plan = Path(temp) / "missing.md"
            plan.write_text("---\nactivities:\n  - missing-activity-for-test\n---\n# Plan\n")
            with self.assertRaises(FileNotFoundError):
                build(plan, Path(temp) / "output.md")

    def test_relative_link_without_yaml_activity_list(self):
        body = "[Rocket](../activities/rocket-building.md)"
        self.assertEqual(parse_activity_ids("", body), ["rocket-building"])

    def test_deduplicates_frontmatter_and_links(self):
        frontmatter = "activities:\n  - rocket-building\n"
        body = "[Rocket](../activities/rocket-building.md)"
        self.assertEqual(parse_activity_ids(frontmatter, body), ["rocket-building"])


if __name__ == "__main__":
    unittest.main()
