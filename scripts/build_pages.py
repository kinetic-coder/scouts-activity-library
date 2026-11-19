#!/usr/bin/env python3
"""Build browsable GitHub Pages from Markdown session plans and activities."""
from pathlib import Path
from urllib.parse import urlsplit
import html
import re
import shutil

try:
    import markdown
except ImportError as exc:
    raise SystemExit("Install pinned dependencies: pip install -r requirements-pages.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "site"
LINK = re.compile(r'(?P<attr>href|src)="(?P<url>[^"]+)"')
SECTION_NAMES = ("Beavers", "Cubs", "Scouts")


def metadata(text):
    if not text.startswith("---\n"):
        return {}, text
    match = re.search(r"\n---\n", text[4:])
    if not match:
        raise ValueError("Unclosed front matter")
    fm = text[4:4 + match.start()]
    body = text[4 + match.end():]
    fields = {}
    for line in fm.splitlines():
        if re.match(r"^[a-z_]+:", line):
            key, value = line.split(":", 1)
            fields[key] = value.strip().strip("'\"")
    return fields, body


def convert_links(rendered, source):
    def replace(match):
        url = html.unescape(match.group("url"))
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or url.startswith(("#", "/", "mailto:")):
            return match.group(0)
        target = (source.parent / parsed.path).resolve()
        if not target.is_relative_to(ROOT):
            raise ValueError(f"Link escapes repository: {source}: {url}")
        if not target.exists():
            raise FileNotFoundError(f"Broken link in {source.relative_to(ROOT)}: {url}")
        if target.suffix.lower() == ".md":
            target = target.with_suffix(".html")
        suffix = ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
        relative = target.relative_to(ROOT).as_posix()
        import os
        new_url = os.path.relpath(DEST / relative, (DEST / source.relative_to(ROOT)).parent).replace("\\", "/")
        return f'{match.group("attr")}="{html.escape(new_url + suffix, quote=True)}"'
    return LINK.sub(replace, rendered)


def shell(title, body, home):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>body{{margin:0;background:#f6f8fc;color:#1b263b;font:18px/1.6 system-ui,sans-serif}}main{{max-width:960px;margin:auto;padding:24px}}article{{background:white;padding:clamp(20px,4vw,48px);border-radius:16px;overflow-wrap:anywhere}}a{{color:#0757a8}}nav{{margin-bottom:24px}}h1,h2{{line-height:1.25}}table{{border-collapse:collapse;display:block;overflow-x:auto}}td,th{{border:1px solid #bdc8d7;padding:8px}}img{{max-width:100%}}.pill{{display:inline-block;margin:6px 8px 6px 0;padding:10px 14px;border:1px solid #aabbd2;border-radius:12px;background:white}}.present{{background:#174c8c;color:white;padding:12px 16px;border-radius:8px;display:inline-block;margin:8px 8px 8px 0}}@media print{{nav{{display:none}}article{{padding:0}}}}</style></head><body><main><nav><a href="{home}">← All sessions</a></nav><article>{body}</article></main></body></html>"""


def highlight_presentations(rendered):
    return re.sub(
        r'<a href="([^"]*/(?:slides|presentation)\.html)"',
        r'<a class="present" target="_blank" rel="noopener" href="\1"',
        rendered,
    )


def build():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    shutil.copytree(ROOT / "assets", DEST / "assets")
    for assets_dir in sorted((ROOT / "sessions").rglob("assets")):
        if not assets_dir.is_dir():
            continue
        dest = DEST / assets_dir.relative_to(ROOT)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(assets_dir, dest)
    sessions = []
    for path in sorted((ROOT / "sessions").rglob("*.md")):
        rel = path.relative_to(ROOT / "sessions")
        if not rel.parts or rel.parts[0] not in SECTION_NAMES:
            continue
        if path.name.lower() == "readme.md":
            continue
        sessions.append(path)
    activities = sorted((ROOT / "activities").glob("*.md"))
    activity_by_id = {}
    for path in activities:
        fields, _ = metadata(path.read_text(encoding="utf-8"))
        activity_by_id[fields.get("id", path.stem)] = path
    catalog = {section: [] for section in SECTION_NAMES}
    for path in sessions:
        fields, body = metadata(path.read_text(encoding="utf-8"))
        section = path.relative_to(ROOT / "sessions").parts[0]
        if fields.get("section") and fields["section"] != section:
            raise ValueError(f"Section mismatch: {path}")
        title = fields.get("title", path.stem)
        activity_ids = []
        in_list = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip() == "activities:":
                in_list = True
                continue
            if in_list and re.match(r"^[^\s#-].*:", line):
                in_list = False
            if in_list:
                match = re.match(r"^\s+-\s+([a-z0-9-]+)\s*$", line)
                if match:
                    activity_ids.append(match.group(1))
        for match in re.finditer(r"activities/([a-z0-9-]+)\.md", body):
            activity_ids.append(match.group(1))
        activity_ids = list(dict.fromkeys(activity_ids))
        import os
        linked = []
        for activity_id in activity_ids:
            activity = activity_by_id.get(activity_id)
            if not activity:
                raise FileNotFoundError(f"Unknown activity {activity_id} in {path}")
            target = DEST / activity.relative_to(ROOT).with_suffix(".html")
            url = os.path.relpath(target, (DEST / path.relative_to(ROOT)).parent)
            linked.append(f'<a class="pill" href="{html.escape(url)}">{html.escape(activity_id.replace("-", " ").title())}</a>')
        rendered = markdown.markdown(body, extensions=["tables", "fenced_code"])
        rendered = convert_links(rendered, path)
        rendered = highlight_presentations(rendered)
        if linked:
            rendered = "<h2>Activities in this session</h2>" + "".join(linked) + rendered
        dest = DEST / path.relative_to(ROOT).with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        home = os.path.relpath(DEST / "index.html", dest.parent)
        dest.write_text(shell(title, rendered, home), encoding="utf-8")
        catalog[section].append((title, dest.relative_to(DEST).as_posix(), fields.get("date", "")))
    for path in activities:
        fields, body = metadata(path.read_text(encoding="utf-8"))
        title = fields.get("title", path.stem)
        rendered = convert_links(markdown.markdown(body, extensions=["tables", "fenced_code"]), path)
        rendered = highlight_presentations(rendered)
        dest = DEST / path.relative_to(ROOT).with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(shell(title, rendered, "../index.html"), encoding="utf-8")
    listing = "<h1>Scout Activity Library</h1><p>Select a section and session. Activities link to instructions and presentations, which open in a new tab for projecting.</p>"
    for section, items in catalog.items():
        listing += f"<h2>{section}</h2>"
        listing += "".join(f'<p><a class="pill" href="{html.escape(url)}">{html.escape(title)}</a> {html.escape(date)}</p>' for title, url, date in items) if items else "<p>No sessions yet.</p>"
    (DEST / "index.html").write_text(shell("Scout Activity Library", listing, "index.html"), encoding="utf-8")
    (DEST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(sessions)} sessions and {len(activities)} activities")


if __name__ == "__main__":
    build()
