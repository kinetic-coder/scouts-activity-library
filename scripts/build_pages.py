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


def wrap_tables(rendered):
    """Make wide Markdown tables keyboard-scrollable without changing semantics."""
    return re.sub(
        r"(<table>.*?</table>)",
        r'<div class="table-scroll" role="region" aria-label="Scrollable table" tabindex="0">\1</div>',
        rendered,
        flags=re.DOTALL,
    )


def add_document_heading(title, rendered, eyebrow=None, meta=None):
    """Give every generated document one consistent, descriptive H1."""
    first_h1 = re.search(r"<h1>(.*?)</h1>", rendered, flags=re.DOTALL)
    if first_h1:
        heading_text = html.unescape(re.sub(r"<[^>]+>", "", first_h1.group(1))).strip()
        if heading_text.casefold() == title.strip().casefold():
            rendered = rendered[:first_h1.start()] + rendered[first_h1.end():]
    rendered = rendered.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
    header = '<header class="document-heading">'
    if eyebrow:
        header += f'<p class="document-heading__eyebrow">{html.escape(eyebrow)}</p>'
    header += f"<h1>{html.escape(title)}</h1>"
    if meta:
        header += f'<p class="document-heading__meta">{html.escape(meta)}</p>'
    return header + "</header>" + rendered


def shell(title, body, home, stylesheet, show_back=True):
    navigation = f'<nav class="site-nav" aria-label="Library"><a href="{html.escape(home, quote=True)}">All sessions</a></nav>' if show_back else ""
    document_title = "Scouts Activity Library" if title == "Scout Activity Library" else f"{title} | Scouts Activity Library"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#7413dc">
  <title>{html.escape(document_title)}</title>
  <link rel="stylesheet" href="{html.escape(stylesheet, quote=True)}">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="site-brand" href="{html.escape(home, quote=True)}" aria-label="Scouts Activity Library home">
        <span class="site-brand__name">Scouts</span>
        <span class="site-brand__descriptor">Activity library</span>
      </a>
      {navigation}
    </div>
  </header>
  <main class="page-shell" id="main-content">
    <article class="document">{body}</article>
  </main>
  <footer class="site-footer">Skills for life · Leader resources</footer>
</body>
</html>
"""


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
        rendered = wrap_tables(rendered)
        if linked:
            rendered = '<h2>Activities in this session</h2><div class="activity-links">' + "".join(linked) + "</div>" + rendered
        session_meta = " · ".join(value for value in (fields.get("date", ""), fields.get("status", "").title()) if value)
        rendered = add_document_heading(title, rendered, eyebrow=f"{section} session plan", meta=session_meta)
        dest = DEST / path.relative_to(ROOT).with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        home = os.path.relpath(DEST / "index.html", dest.parent)
        stylesheet = os.path.relpath(DEST / "assets/styles/scouts-pages.css", dest.parent)
        dest.write_text(shell(title, rendered, home, stylesheet), encoding="utf-8")
        catalog[section].append((title, dest.relative_to(DEST).as_posix(), fields.get("date", ""), fields.get("status", "")))
    for path in activities:
        fields, body = metadata(path.read_text(encoding="utf-8"))
        title = fields.get("title", path.stem)
        rendered = convert_links(markdown.markdown(body, extensions=["tables", "fenced_code"]), path)
        rendered = highlight_presentations(rendered)
        rendered = wrap_tables(rendered)
        rendered = add_document_heading(title, rendered, eyebrow="Reusable activity")
        dest = DEST / path.relative_to(ROOT).with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        stylesheet = os.path.relpath(DEST / "assets/styles/scouts-pages.css", dest.parent)
        dest.write_text(shell(title, rendered, "../index.html", stylesheet), encoding="utf-8")
    listing = "<h1>Scout Activity Library</h1><p>Practical, leader-ready plans and activities. Choose a section, then open a session.</p>"
    for section, items in catalog.items():
        listing += f'<section aria-labelledby="section-{section.lower()}"><h2 id="section-{section.lower()}">{section}</h2>'
        if items:
            listing += '<div class="session-grid">'
            for title, url, date, status in items:
                meta = " · ".join(value for value in (date, status.title()) if value)
                listing += f'<a class="session-card" href="{html.escape(url)}">{html.escape(title)}'
                if meta:
                    listing += f'<span class="session-card__meta">{html.escape(meta)}</span>'
                listing += "</a>"
            listing += "</div>"
        else:
            listing += "<p>No sessions yet.</p>"
        listing += "</section>"
    (DEST / "index.html").write_text(
        shell("Scout Activity Library", listing, "index.html", "assets/styles/scouts-pages.css", show_back=False),
        encoding="utf-8",
    )
    (DEST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(sessions)} sessions and {len(activities)} activities")


if __name__ == "__main__":
    build()
