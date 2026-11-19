#!/usr/bin/env python3
"""Assemble a self-contained Markdown leader pack from a meeting plan and linked activities.

Python standard library only. Usage:
  python scripts/build_leader_pack.py sessions/Beavers/2026-11-09-beavers-space-night.md
  python scripts/build_leader_pack.py path/to/plan.md --output build/leader-pack.md
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_RE = re.compile(r"(?<![\w])activities/([a-z0-9][a-z0-9-]*)\.md\b")
LINK_RE = re.compile(r"\[([^]]+)\]\(([^)]+)\)")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return "", text
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("Unclosed YAML front matter")
    return text[4:marker], text[marker + 5:]


def parse_activity_ids(frontmatter, body):
    # Accept a simple YAML list of activity IDs and/or relative Markdown links.
    ids = []
    inside = False
    for line in frontmatter.splitlines():
        if re.match(r"^activities:\s*$", line):
            inside = True
            continue
        if inside and re.match(r"^[^\s#-][^:]*:", line):
            inside = False
        if inside:
            m = re.match(r"^\s+-\s+([a-z0-9][a-z0-9-]*)\s*$", line)
            if m:
                ids.append(m.group(1))
    for match in ACTIVITY_RE.finditer(body):
        ids.append(match.group(1))
    return list(dict.fromkeys(ids))


def rewrite_links(body, source_file, output_file):
    """Rewrite local relative Markdown links for the generated file location."""
    import os
    def replace(match):
        label, target = match.groups()
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group(0)
        path, sep, fragment = target.partition("#")
        if not path:
            return match.group(0)
        absolute = (source_file.parent / path).resolve()
        relative = Path(os.path.relpath(absolute, output_file.parent)).as_posix()
        return f"[{label}]({relative}{sep}{fragment})"
    return LINK_RE.sub(replace, body)


def build(plan, output):
    plan = plan.resolve()
    output = output.resolve()
    if not plan.is_file():
        raise FileNotFoundError(f"Plan not found: {plan}")
    if not plan.is_relative_to(ROOT):
        raise ValueError("Meeting plan must be inside the repository")
    frontmatter, body = split_frontmatter(plan.read_text(encoding="utf-8"))
    activity_ids = parse_activity_ids(frontmatter, body)
    if not activity_ids:
        raise ValueError("No activity IDs found. Add an activities: YAML list or Markdown links to activities/<id>.md")
    parts = ["# Leader pack", f"Source meeting plan: `{plan.relative_to(ROOT)}`", "",
             "## Meeting plan", rewrite_links(body.strip(), plan, output), "",
             "## Detailed activity instructions", ""]
    for activity_id in activity_ids:
        source = ROOT / "activities" / f"{activity_id}.md"
        if not source.is_file():
            raise FileNotFoundError(f"Activity '{activity_id}' is missing: {source.relative_to(ROOT)}")
        _, activity_body = split_frontmatter(source.read_text(encoding="utf-8"))
        parts.extend([f"### Activity: {activity_id}", "",
                      rewrite_links(activity_body.strip(), source, output), ""])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Created {output} with {len(activity_ids)} activities")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    plan = args.plan if args.plan.is_absolute() else ROOT / args.plan
    output = args.output if args.output is not None else Path("build") / f"{plan.stem}-leader-pack.md"
    if not output.is_absolute():
        output = ROOT / output
    build(plan, output)


if __name__ == "__main__":
    main()
