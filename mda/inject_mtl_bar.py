#!/usr/bin/env python3
"""Inject the Math Translation Layer (MTL) reader-mode bar into all MDA pages."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")
MTL_BAR_PATH = ROOT / "mda/components/mtl-reader-bar.html"

CSS_LINKS = """<link rel="stylesheet" href="/mda/components/mtl-reader-bar.css">
<link rel="stylesheet" href="/shared/css/mtl-equation.css">
"""
JS_LINK = '<script src="/shared/js/mtl-equation.js"></script>\n'

BAR_SNIPPET = MTL_BAR_PATH.read_text(encoding="utf-8")
# Normalize line endings and ensure trailing newline
BAR_SNIPPET = BAR_SNIPPET.strip() + "\n"


def add_head_links(text: str) -> str:
    if "/mda/components/mtl-reader-bar.css" not in text:
        text = text.replace("</head>", CSS_LINKS + "</head>", 1)
    if "/shared/css/mtl-equation.css" not in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="/shared/css/mtl-equation.css">\n' + "</head>", 1)
    return text


def add_body_js(text: str) -> str:
    if "/shared/js/mtl-equation.js" not in text:
        text = text.replace("</body>", JS_LINK + "</body>", 1)
    return text


def inject_bar(text: str) -> str:
    if 'id="mtlReaderBar"' in text:
        return text
    # Find the pill-player bar closing </audio>\n</div>\n (full bar)
    marker = '<audio preload="metadata"></audio>\n</div>\n'
    pos = text.find(marker)
    if pos == -1:
        return text
    insert_pos = pos + len(marker)
    return text[:insert_pos] + "\n" + BAR_SNIPPET + text[insert_pos:]


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="tp-pill-bar"' not in text:
        return False
    text = add_head_links(text)
    text = inject_bar(text)
    text = add_body_js(text)
    path.write_text(text, encoding="utf-8")
    return True


if __name__ == "__main__":
    files = list((ROOT / "mda").glob("*/*.html"))
    files.extend([ROOT / "index.html", ROOT / "mda/index.html"])
    updated = 0
    skipped = 0
    for path in files:
        if "components" in path.parts:
            continue
        if process_file(path):
            updated += 1
            print(f"Updated {path}")
        else:
            skipped += 1
    print(f"\nUpdated: {updated}, Skipped: {skipped}")
