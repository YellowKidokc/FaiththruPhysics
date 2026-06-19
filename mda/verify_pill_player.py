#!/usr/bin/env python3
"""Static verification for TP pill-player injection."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")

article_files = []
for html in (ROOT / "mda").glob("*/*.html"):
    if "components" in html.parts:
        continue
    article_files.append(html)
article_files.extend([ROOT / "index.html", ROOT / "mda/index.html"])

issues = []
ok = 0

for path in article_files:
    text = path.read_text(encoding="utf-8")
    has_bar = "tp-pill-bar" in text
    has_css = "/mda/components/tp-pill-player.css" in text
    has_js = "/mda/components/tp-pill-player.js" in text
    bar_count = text.count('class="tp-pill-bar"')
    if not has_bar:
        issues.append(f"{path}: missing bar")
        continue
    if bar_count > 1:
        issues.append(f"{path}: {bar_count} bars (duplicate)")
    if not has_css:
        issues.append(f"{path}: missing CSS link")
    if not has_js:
        issues.append(f"{path}: missing JS link")
    if not re.search(r'data-audio-slug="[^"]+"', text):
        issues.append(f"{path}: missing data-audio-slug")
    # check bar is inside body
    body_open = text.find('<body')
    body_close = text.find('</body>')
    bar_pos = text.find('class="tp-pill-bar"')
    if body_open == -1 or body_close == -1 or not (body_open < bar_pos < body_close):
        issues.append(f"{path}: bar outside body")
    if not issues or (issues and not any(str(path) in i for i in issues[-5:])):
        ok += 1

print(f"Checked {len(article_files)} pages. OK: {ok}. Issues: {len(issues)}")
for issue in issues[:30]:
    print("  -", issue)
if issues:
    raise SystemExit(1)
