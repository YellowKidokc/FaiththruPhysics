#!/usr/bin/env python3
"""Update existing TP pill-strip bars inside MDA articles.

- Moves the 'active' class from the Deep Dive pill to the TTS pill.
- Adds data-fallback-src to every pill so the player can fall back to the folder's
  known-good audio file if a mode-specific file is ever swapped in later.
"""
from pathlib import Path
import re

MDA_DIR = Path(__file__).resolve().parent

BAR_START = "<!-- TP PILL PLAYER BAR"
BAR_END = '  <audio preload="metadata"></audio>\n</div>'


def update_bar(bar_html: str) -> str:
    # Add data-fallback-src next to data-src if missing.
    def add_fallback(match: re.Match) -> str:
        full = match.group(0)
        if 'data-fallback-src' in full:
            return full
        src = match.group(1)
        return full.replace(f'data-src="{src}"', f'data-src="{src}" data-fallback-src="{src}"')

    bar_html = re.sub(r'<button class="tp-pill(?: active)?" data-mode="([^"]+)" data-src="([^"]+)"', add_fallback, bar_html)

    # Move active class from deep to tts.
    bar_html = bar_html.replace('class="tp-pill active" data-mode="deep"', 'class="tp-pill" data-mode="deep"')
    bar_html = bar_html.replace('class="tp-pill" data-mode="tts"', 'class="tp-pill active" data-mode="tts"')

    return bar_html


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if BAR_START not in text or BAR_END not in text:
        return False

    start = text.index(BAR_START)
    end = text.index(BAR_END, start) + len(BAR_END)
    original_bar = text[start:end]
    updated_bar = update_bar(original_bar)
    if updated_bar == original_bar:
        return False

    text = text[:start] + updated_bar + text[end:]
    path.write_text(text, encoding="utf-8")
    return True


changed = 0
for html_file in sorted(MDA_DIR.rglob("*.html")):
    rel = html_file.relative_to(MDA_DIR)
    if len(rel.parts) != 2:
        continue
    if process_file(html_file):
        changed += 1
        print(f"UPDATED: {rel}")

print(f"\nUpdated: {changed}")
