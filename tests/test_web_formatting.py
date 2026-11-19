import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WebFormattingTests(unittest.TestCase):
    def html_artifacts(self):
        paths = list((ROOT / "assets").rglob("*.html"))
        paths.extend((ROOT / "sessions").rglob("assets/*.html"))
        return sorted(set(paths))

    def test_artifacts_have_responsive_document_metadata(self):
        for path in self.html_artifacts():
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertRegex(text, r'<html\s+lang="[^"]+"')
                self.assertRegex(text, r'<meta\s+name="viewport"[^>]+width=device-width')
                self.assertRegex(text, r"<title>[^<]+</title>")

    def test_artifacts_use_shared_scouts_styles(self):
        for path in self.html_artifacts():
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertRegex(text, r'<link\s+rel="stylesheet"\s+href="[^"]*scouts-(?:presentation|printables)\.css"')

    def test_every_artifact_loads_the_shared_theme_selector(self):
        for path in self.html_artifacts():
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertRegex(text, r'<script\s+src="[^"]*scripts/theme\.js"></script>')

        script = (ROOT / "assets/scripts/theme.js").read_text(encoding="utf-8")
        self.assertIn('dataset.themeChoice', script)
        self.assertIn('setAttribute("aria-pressed"', script)
        self.assertIn("localStorage.setItem", script)
        self.assertNotRegex(script, re.compile(r"https?://", re.IGNORECASE))

    def test_interactive_decks_expose_named_controls(self):
        decks = sorted((ROOT / "assets").glob("*/slides.html"))
        decks.extend((ROOT / "sessions").rglob("assets/presentation.html"))
        for path in decks:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("scouts-presentation.css", text)
                if "id=\"slide\"" in text:
                    self.assertIn("aria-live=\"polite\"", text)
                self.assertNotRegex(text, r">\s*[←→◀▶]")

    def test_shared_styles_are_offline_only(self):
        for path in sorted((ROOT / "assets/styles").glob("*.css")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotRegex(text, re.compile(r"https?://", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
