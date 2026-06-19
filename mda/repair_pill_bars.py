#!/usr/bin/env python3
"""Repair pill-player bars that were truncated by an over-greedy move script.
Rebuilds the full bar from the captured slug and podcast URL."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")

# Matches the truncated bar block from comment through the closing </div> of the pill strip.
TRUNCATED_BAR_RE = re.compile(
    r'(<!-- TP PILL PLAYER BAR .*? -->\s*)'
    r'<div class="tp-pill-bar" id="tpPillBar" data-audio-slug="([^"]*)">\s*'
    r'<div class="tp-pill-strip">\s*'
    r'<button class="tp-pill active" data-mode="deep" data-src="([^"]+)" data-label="Deep Dive"><span class="dot"></span>Deep Dive</button>\s*'
    r'<button class="tp-pill" data-mode="debate" data-src="[^"]+" data-label="Debate"><span class="dot"></span>Debate</button>\s*'
    r'<button class="tp-pill" data-mode="critique" data-src="[^"]+" data-label="Critique"><span class="dot"></span>Critique</button>\s*'
    r'<button class="tp-pill" data-mode="tts" data-src="[^"]+" data-label="TTS"><span class="dot"></span>TTS</button>\s*'
    r'<button class="tp-pill" data-mode="web" data-src="[^"]+" data-label="Web"><span class="dot"></span>Web</button>\s*'
    r'</div>\s*',
    re.S
)


def build_bar(comment: str, slug: str, url: str) -> str:
    return (
        f'{comment}'
        f'<div class="tp-pill-bar" id="tpPillBar" data-audio-slug="{slug}">\n'
        f'  <div class="tp-pill-strip">\n'
        f'    <button class="tp-pill active" data-mode="deep" data-src="{url}" data-label="Deep Dive"><span class="dot"></span>Deep Dive</button>\n'
        f'    <button class="tp-pill" data-mode="debate" data-src="{url}" data-label="Debate"><span class="dot"></span>Debate</button>\n'
        f'    <button class="tp-pill" data-mode="critique" data-src="{url}" data-label="Critique"><span class="dot"></span>Critique</button>\n'
        f'    <button class="tp-pill" data-mode="tts" data-src="{url}" data-label="TTS"><span class="dot"></span>TTS</button>\n'
        f'    <button class="tp-pill" data-mode="web" data-src="{url}" data-label="Web"><span class="dot"></span>Web</button>\n'
        f'  </div>\n'
        f'  <div class="tp-bar-controls">\n'
        f'    <button class="tp-bar-play"><i class="fas fa-play"></i></button>\n'
        f'    <div class="tp-bar-track"><div class="tp-bar-fill"></div></div>\n'
        f'    <span class="tp-bar-time">0:00 / 0:00</span>\n'
        f'    <select class="tp-bar-speed">\n'
        f'      <option value="0.5">0.5x</option>\n'
        f'      <option value="0.75">0.75x</option>\n'
        f'      <option value="1" selected>1x</option>\n'
        f'      <option value="1.25">1.25x</option>\n'
        f'      <option value="1.5">1.5x</option>\n'
        f'      <option value="1.75">1.75x</option>\n'
        f'      <option value="2">2x</option>\n'
        f'    </select>\n'
        f'  </div>\n'
        f'  <audio preload="metadata"></audio>\n'
        f'</div>\n'
    )


def repair_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="tp-pill-bar"' not in text:
        return False

    # Already full bar? Skip
    if re.search(r'<div class="tp-pill-bar" id="tpPillBar"[^>]*>.*?<audio[^>]*>.*?</audio>\s*</div>', text, re.S):
        print(f"  [skip] already full: {path.name}")
        return False

    m = TRUNCATED_BAR_RE.search(text)
    if not m:
        print(f"  [skip] pattern mismatch: {path.name}")
        return False

    comment, slug, url = m.group(1), m.group(2), m.group(3)
    full_bar = build_bar(comment, slug, url)
    text = text[:m.start()] + full_bar + text[m.end():]
    path.write_text(text, encoding="utf-8")
    return True


if __name__ == "__main__":
    files = list((ROOT / "mda").glob("*/*.html"))
    files.extend([ROOT / "index.html", ROOT / "mda/index.html"])
    repaired = 0
    skipped = 0
    for path in files:
        if "components" in path.parts:
            continue
        if repair_file(path):
            repaired += 1
            print(f"Repaired {path}")
        else:
            skipped += 1
    print(f"\nRepaired: {repaired}, Skipped: {skipped}")
