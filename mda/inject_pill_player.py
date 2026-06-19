#!/usr/bin/env python3
"""
Inject the TP pill-strip player bar into every MDA article.
Adds shared CSS/JS links and a folder-level podcast bar.
"""

from pathlib import Path
import re

MDA_DIR = Path(__file__).resolve().parent
SNIPPET = (MDA_DIR / "components" / "tp-pill-player-bar-snippet.html").read_text(encoding="utf-8")

CSS_LINK = '<link rel="stylesheet" href="/mda/components/tp-pill-player.css">'
JS_SCRIPT = '<script src="/mda/components/tp-pill-player.js" defer></script>'

# Folder -> shared podcast URL
FOLDER_PODCAST = {
    "00-entry-and-series-map": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-of-america.m4a",
    "01-story-thread": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-01-introduction.m4a",
    "02-method-and-metrics": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-facts-paper.m4a",
    "03-evidence-chronology": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-01-introduction.m4a",
    "04-collapse-mechanisms": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-02-phase-transition.m4a",
    "05-amish-and-case-studies": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-09-amish-proof.m4a",
    "06-recovery-and-synthesis": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-10-way-back.m4a",
    "90-appendices-and-source-packets": "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/moral-decline-of-america.m4a",
}

body_re = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
head_close_re = re.compile(r'(</head>)', re.IGNORECASE)
body_close_re = re.compile(r'(</body>)', re.IGNORECASE)

changed = 0
skipped = []

for html_file in sorted(MDA_DIR.rglob("*.html")):
    rel = html_file.relative_to(MDA_DIR)
    if len(rel.parts) != 2:
        continue  # only articles inside immediate subfolders
    folder = rel.parts[0]
    if folder not in FOLDER_PODCAST:
        continue

    content = html_file.read_text(encoding="utf-8", errors="replace")

    # Skip if already injected
    if 'tp-pill-bar' in content:
        skipped.append(str(rel))
        continue

    podcast_url = FOLDER_PODCAST[folder]
    bar_html = SNIPPET.replace("PODCAST-URL.m4a", podcast_url)

    # Inject CSS in <head>
    content = head_close_re.sub(CSS_LINK + "\n" + r"\1", content, count=1)

    # Inject bar after <body>
    content = body_re.sub(r"\1\n" + bar_html, content, count=1)

    # Inject JS before </body>
    content = body_close_re.sub(JS_SCRIPT + "\n" + r"\1", content, count=1)

    html_file.write_text(content, encoding="utf-8")
    changed += 1
    print(f"INJECTED: {rel}")

print(f"\nInjected: {changed}")
print(f"Already had bar (skipped): {len(skipped)}")
if skipped:
    for s in skipped[:10]:
        print(f"  {s}")
    if len(skipped) > 10:
        print(f"  ... and {len(skipped)-10} more")
