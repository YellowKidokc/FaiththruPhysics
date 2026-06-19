#!/usr/bin/env python3
"""Add data-audio-slug attributes to every TP pill bar so D1 lookup is ready."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")

FILES = list((ROOT / "mda").glob("*/*.html"))
FILES.append(ROOT / "index.html")
FILES.append(ROOT / "mda/index.html")

PATTERN = re.compile(r'<div class="tp-pill-bar" id="tpPillBar">')


def slug_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.as_posix() == "index.html":
        return "site-home"
    if rel.as_posix() == "mda/index.html":
        return "mda-series-home"
    return path.stem


for path in FILES:
    if "components" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    if "tp-pill-bar" not in text:
        continue
    slug = slug_for(path)
    new_text, n = PATTERN.subn(
        f'<div class="tp-pill-bar" id="tpPillBar" data-audio-slug="{slug}">',
        text
    )
    if n:
        path.write_text(new_text, encoding="utf-8")
        print(f"Tagged {path} -> {slug}")
