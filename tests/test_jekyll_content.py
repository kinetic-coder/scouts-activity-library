import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONT_MATTER = re.compile(r"\A---\n(?P<yaml>.*?)\n---(?:\n|\Z)", re.DOTALL)
DATE = re.compile(r"^date:\s*(?P<value>[^#]*?)(?:\s+#.*)?$", re.MULTILINE)


class JekyllContentTests(unittest.TestCase):
    def markdown_front_matter(self):
        for path in sorted(ROOT.rglob("*.md")):
            match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
            if match:
                yield path, match.group("yaml")

    def test_front_matter_is_valid_yaml(self):
        ruby = shutil.which("ruby")
        if not ruby:
            self.skipTest("Ruby is required to validate YAML with Jekyll's parser")

        for path, front_matter in self.markdown_front_matter():
            with self.subTest(path=path.relative_to(ROOT)):
                result = subprocess.run(
                    [ruby, "-ryaml", "-e", "YAML.parse(STDIN.read)"],
                    input=front_matter,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    def test_dates_are_real_or_null(self):
        for path, front_matter in self.markdown_front_matter():
            match = DATE.search(front_matter)
            if not match:
                continue
            value = match.group("value").strip().strip("'\"")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertRegex(value, r"^(?:null|\d{4}-\d{2}-\d{2})$")


if __name__ == "__main__":
    unittest.main()
