#!/usr/bin/env python3
"""Move the MTL reader bar from wherever it is to immediately after the pill-player bar."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")

MTL_BAR_RE = re.compile(
    r'<!-- MTL READER MODE BAR .*? -->\s*<div class="mtl-reader-bar" id="mtlReaderBar"[^>]*>.*?</div>\s*',
    re.S
)
PILL_BAR_END = '<audio preload="metadata"></audio>\n</div>\n'


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'id="mtlReaderBar"' not in text:
        return False

    # Extract MTL bar
    m = MTL_BAR_RE.search(text)
    if not m:
        return False
    mtl_bar = m.group(0)

    # Remove MTL bar from current location
    text = text[:m.start()] + text[m.end():]

    # Find pill bar end and insert after it
    pos = text.find(PILL_BAR_END)
    if pos == -1:
        # restore MTL bar if no pill bar found
        print(f"  [skip] no pill bar end: {path.name}")
        return False
    insert_pos = pos + len(PILL_BAR_END)
    text = text[:insert_pos] + mtl_bar + "\n" + text[insert_pos:]

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
            print(f"Repositioned MTL bar: {path}")
        else:
            skipped += 1
    print(f"\nMoved: {moved}, Skipped: {skipped}")
