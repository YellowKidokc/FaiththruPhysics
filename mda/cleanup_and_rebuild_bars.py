#!/usr/bin/env python3
"""
Clean up corrupted/truncated pill-player and MTL-reader-bar fragments,
then rebuild and insert one clean pill bar + one MTL bar below the header.
"""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")

# Matches the full pill bar (including controls and audio)
FULL_PILL_RE = re.compile(
    r'<!-- TP PILL PLAYER BAR .*? -->\s*'
    r'<div class="tp-pill-bar" id="tpPillBar" data-audio-slug="([^"]*)">\s*'
    r'<div class="tp-pill-strip">\s*'
    r'(<button class="tp-pill[^>]*data-src="([^"]+)"[^>]*>.*?</button>\s*){5}'
    r'</div>\s*'
    r'<div class="tp-bar-controls">.*?</div>\s*'
    r'<audio[^>]*>.*?</audio>\s*'
    r'</div>\s*',
    re.S
)

# Matches a truncated pill-bar opening + strip
TRUNC_PILL_RE = re.compile(
    r'<!-- TP PILL PLAYER BAR .*? -->\s*'
    r'<div class="tp-pill-bar" id="tpPillBar" data-audio-slug="([^"]*)">\s*'
    r'<div class="tp-pill-strip">\s*'
    r'(<button class="tp-pill[^>]*data-src="([^"]+)"[^>]*>.*?</button>\s*){1,5}'
    r'</div>\s*',
    re.S
)

# Orphaned controls/audio from a truncated bar
ORPHAN_RE = re.compile(
    r'<div class="tp-bar-controls">.*?<audio[^>]*>.*?</audio>\s*</div>\s*',
    re.S
)

# MTL bar
MTL_BAR_RE = re.compile(
    r'<!-- MTL READER MODE BAR .*? -->\s*<div class="mtl-reader-bar" id="mtlReaderBar"[^>]*>.*?</div>\s*',
    re.S
)

CONTENT_RE = re.compile(
    r'<((?:main|header|section|article)\b|div\b[^>]*\bclass=["\'][^"\']*\bmain\b)',
    re.I | re.S
)


def extract_slug_and_url(text: str):
    """Return (slug, url) from any pill-bar fragment."""
    for regex in (FULL_PILL_RE, TRUNC_PILL_RE):
        m = regex.search(text)
        if m:
            slug = m.group(1)
            # Find first deep-mode data-src in the captured buttons
            url_m = re.search(r'data-mode="deep" data-src="([^"]+)"', m.group(0))
            url = url_m.group(1) if url_m else ""
            return slug, url
    return "", ""


def build_pill_bar(slug: str, url: str) -> str:
    return (
        f'<!-- TP PILL PLAYER BAR — inject after <body>; requires /mda/components/tp-pill-player.css and /mda/components/tp-pill-player.js -->\n'
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


def build_mtl_bar() -> str:
    return (
        f'<!-- MTL READER MODE BAR — requires /shared/css/mtl-equation.css and /shared/js/mtl-equation.js -->\n'
        f'<div class="mtl-reader-bar" id="mtlReaderBar" aria-label="Math reading level">\n'
        f'  <span class="mtl-reader-label">Math layer</span>\n'
        f'  <div class="mtl-reader-tabs" role="tablist" aria-label="Reading levels">\n'
        f'    <button class="mtl-reader-tab" type="button" data-reader-mode="easy" aria-selected="false">Easy</button>\n'
        f'    <button class="mtl-reader-tab active" type="button" data-reader-mode="standard" aria-selected="true">Standard</button>\n'
        f'    <button class="mtl-reader-tab" type="button" data-reader-mode="academic" aria-selected="false">Academic</button>\n'
        f'    <button class="mtl-reader-tab" type="button" data-reader-mode="proof" aria-selected="false">Proof</button>\n'
        f'  </div>\n'
        f'</div>\n'
    )


def insert_location(text: str) -> int:
    """Return position just before the first content-root element after <body>."""
    body_start = text.lower().find('<body')
    if body_start == -1:
        return -1
    cm = CONTENT_RE.search(text, body_start)
    if not cm:
        return -1
    return cm.start()


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    # Extract data before removing fragments
    slug, url = extract_slug_and_url(text)
    if not slug or not url:
        print(f"  [skip] cannot extract pill data: {path.name}")
        return False

    # Remove all fragments
    text = FULL_PILL_RE.sub('', text)
    text = TRUNC_PILL_RE.sub('', text)
    text = ORPHAN_RE.sub('', text)
    text = MTL_BAR_RE.sub('', text)

    # Normalize excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Build clean bars
    pill_bar = build_pill_bar(slug, url)
    mtl_bar = build_mtl_bar()
    bars = pill_bar + "\n" + mtl_bar + "\n"

    # Insert before first content element
    pos = insert_location(text)
    if pos == -1:
        print(f"  [skip] no content marker: {path.name}")
        return False

    text = text[:pos] + bars + text[pos:]

    # Ensure MTL CSS/JS and pill CSS/JS links
    if "/mda/components/tp-pill-player.css" not in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="/mda/components/tp-pill-player.css">\n</head>', 1)
    if "/mda/components/tp-pill-player.js" not in text:
        text = text.replace("</body>", '<script src="/mda/components/tp-pill-player.js"></script>\n</body>', 1)
    if "/mda/components/mtl-reader-bar.css" not in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="/mda/components/mtl-reader-bar.css">\n</head>', 1)
    if "/shared/css/mtl-equation.css" not in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="/shared/css/mtl-equation.css">\n</head>', 1)
    if "/shared/css/mtl-claims.css" not in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="/shared/css/mtl-claims.css">\n</head>', 1)
    if "/shared/js/mtl-equation.js" not in text:
        text = text.replace("</body>", '<script src="/shared/js/mtl-equation.js"></script>\n</body>', 1)
    if "/shared/js/mtl-claims.js" not in text:
        text = text.replace("</body>", '<script src="/shared/js/mtl-claims.js"></script>\n</body>', 1)
    # Load the MTL overlay on every page so it is always ready.
    # The loader must run before the overlay so reviewed translations are available.
    # Remove any existing overlay script lines first, then re-insert in the right order.
    text = re.sub(r'<script src="/shared/js/mtl-overlay(?:-loader)?\.js"></script>\n', '', text)
    overlay_scripts = (
        '<script src="/shared/js/mtl-overlay-loader.js"></script>\n'
        '<script src="/shared/js/mtl-overlay.js"></script>\n'
    )
    text = text.replace("</body>", overlay_scripts + "</body>", 1)

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
            print(f"Cleaned/rebuilt bars: {path}")
        else:
            skipped += 1
    print(f"\nUpdated: {updated}, Skipped: {skipped}")
