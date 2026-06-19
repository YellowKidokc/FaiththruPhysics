#!/usr/bin/env python3
"""Move the TP pill-player bar from the very top to just below the header block
(before the first <main>, hero <header>, <section>, or <article>)."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")
BAR_RE = re.compile(
    r'(<!-- TP PILL PLAYER BAR .*? -->\s*<div class="tp-pill-bar" id="tpPillBar"[^>]*>.*?</div>\s*)',
    re.S
)
# Find first content-root tag after <body>: main, hero header, section, article,
# or a div whose class contains "main".
CONTENT_RE = re.compile(
    r'<((?:main|header|section|article)\b|div\b[^>]*\bclass=["\'][^"\']*\bmain\b)',
    re.I | re.S
)


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="tp-pill-bar"' not in text:
        return False

    m = BAR_RE.search(text)
    if not m:
        return False
    bar_block = m.group(1)

    body_start = text.lower().find('<body')
    if body_start == -1:
        return False

    # Search for first content marker after body
    cm = CONTENT_RE.search(text, body_start)
    if not cm:
        print(f"  [skip] no content marker: {path.name}")
        return False

    insert_pos = cm.start()

    # If bar is already right before this marker, skip
    # Check if the bar block is immediately preceding the content marker
    preceding = text[:insert_pos].strip()
    if preceding.endswith(bar_block.strip()):
        print(f"  [skip] already in place: {path.name}")
        return False

    # Remove bar block from current location
    text = text[:m.start()] + text[m.end():]

    # Recompute insert position after removal
    cm = CONTENT_RE.search(text, body_start)
    if not cm:
        print(f"  [skip] content marker lost after removal: {path.name}")
        return False
    insert_pos = cm.start()

    # Insert bar block before content marker, with blank lines for readability
    text = text[:insert_pos] + bar_block + "\n" + text[insert_pos:]
    path.write_text(text, encoding="utf-8")
    return True


if __name__ == "__main__":
    files = list((ROOT / "mda").glob("*/*.html"))
    files.extend([ROOT / "index.html", ROOT / "mda/index.html"])
    moved = 0
    skipped = 0
    for path in files:
        if "components" in path.parts:
            continue
        if process_file(path):
            moved += 1
            print(f"Moved bar below header: {path}")
        else:
            skipped += 1
    print(f"\nMoved: {moved}, Skipped: {skipped}")
