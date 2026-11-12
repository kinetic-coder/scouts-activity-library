#!/usr/bin/env python3
"""Generate delivered-only activity usage history from session Markdown.

No third-party dependencies. Supports the repository's simple YAML front matter
and optional activity_outcomes mapping. This is deliberately not a general YAML parser.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FIELDS = {"delivered", "leader", "planned_minutes", "actual_minutes", "participants", "feedback", "improvements"}


def scalar(value):
    value = value.strip()
    if value.startswith(("'", '"')) and value.endswith(value[0]):
        return value[1:-1]
    return value


def parse_record(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: missing YAML front matter")
    fm = text[4:].split("\n---\n", 1)[0]
    record, section, current = {}, None, None
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
        if top:
            key, val = top.groups()
            section, current = key, None
            if key in ("activities", "badge_requirements_evidenced"):
                record[key] = [] if val in ("", "[]") else [scalar(x) for x in val.strip("[]").split(",")]
            elif key == "activity_outcomes":
                record[key] = {}
            else:
                record[key] = scalar(val)
            continue
        if section in ("activities", "badge_requirements_evidenced"):
            item = re.fullmatch(r"\s+-\s+([a-z0-9][a-z0-9-]*)\s*", line)
            if item:
                record[section].append(item.group(1))
            else:
                raise ValueError(f"{path}: unsupported list entry: {line}")
        elif section == "activity_outcomes":
            key = re.fullmatch(r"  ([a-z0-9][a-z0-9-]*):\s*", line)
            field = re.fullmatch(r"    ([a-z_]+):\s*(.*?)\s*", line)
            if key:
                current = key.group(1)
                record[section][current] = {}
            elif field and current and field.group(1) in FIELDS:
                record[section][current][field.group(1)] = scalar(field.group(2))
            else:
                raise ValueError(f"{path}: unsupported outcome entry: {line}")
        else:
            # Other nested metadata is not used by this report.
            continue
    return record


def collect(sessions):
    events = []
    for path in sorted(sessions):
        record = parse_record(path)
        if record.get("status") != "delivered":
            continue
        date = record.get("date", "")
        dt.date.fromisoformat(date)
        section = record.get("section", "")
        activities = record.get("activities", [])
        outcomes = record.get("activity_outcomes")
        if outcomes is not None and set(outcomes) - set(activities):
            raise ValueError(f"{path}: outcome references an unplanned activity")
        for activity in dict.fromkeys(activities):
            if not ID.fullmatch(activity):
                raise ValueError(f"{path}: invalid activity ID {activity!r}")
            outcome = (outcomes or {}).get(activity, {})
            if outcomes is not None and outcome.get("delivered", "").lower() != "true":
                continue
            event = {"date": date, "section": section, "activity_id": activity, "session": path.name}
            for field in sorted(FIELDS - {"delivered"}):
                event[field] = outcome.get(field, "")
            for field in ("planned_minutes", "actual_minutes", "participants"):
                if event[field] != "":
                    try:
                        value = int(event[field])
                    except ValueError as exc:
                        raise ValueError(f"{path}: {field} must be a nonnegative integer") from exc
                    if value < 0:
                        raise ValueError(f"{path}: {field} must be nonnegative")
                    event[field] = value
            events.append(event)
    return events


def report(events):
    groups = defaultdict(list)
    for event in events:
        groups[(event["section"], event["activity_id"])].append(event)
    return [
        {"section": section, "activity_id": activity, "uses": len(items),
         "last_used": max(x["date"] for x in items),
         "average_actual_minutes": round(sum(x["actual_minutes"] for x in items if isinstance(x["actual_minutes"], int)) /
             len([x for x in items if isinstance(x["actual_minutes"], int)]), 1)
             if any(isinstance(x["actual_minutes"], int) for x in items) else None}
        for (section, activity), items in sorted(groups.items())
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sessions", type=Path, default=ROOT / "sessions")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        events = collect(args.sessions.glob("*.md"))
        summary = report(events)
        result = json.dumps({"summary": summary, "events": events}, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(result, encoding="utf-8")
        else:
            print(result, end="")
    except (ValueError, OSError) as exc:
        print(f"Activity history error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
