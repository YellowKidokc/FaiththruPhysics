#!/usr/bin/env python3
"""Inject the TP pill-player bar into the site root homepage and the MDA landing page.

The player exposes five modes (Deep Dive, Debate, Critique, TTS, Web). Each pill tries
to load its mode-specific audio file first; if that file is missing, the player falls
back to the known-good overview file. TTS is the default/active pill because it is the
primary "good version" of the audio.
"""
import re
from pathlib import Path

ROOT = Path("D:/GitHub/faiththruphysics-site")

BUCKET = "https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio"
FALLBACK_URL = f"{BUCKET}/moral-decline-of-america.m4a"

# Mode-specific "proper" audio files. Replace these URLs when distinct deep-dive,
# debate, critique, tts, or web renderings are uploaded to R2.
MODE_URLS = {
    "deep":     f"{BUCKET}/moral-decline-of-america-deep-dive.m4a",
    "debate":   f"{BUCKET}/moral-decline-of-america-debate.m4a",
    "critique": f"{BUCKET}/moral-decline-of-america-critique.m4a",
    "tts":      f"{BUCKET}/moral-decline-of-america-tts.m4a",
    "web":      f"{BUCKET}/moral-decline-of-america-web.m4a",
}

CSS_LINK = '<link rel="stylesheet" href="/mda/components/tp-pill-player.css">\n'
JS_LINK = '<script defer src="/mda/components/tp-pill-player.js"></script>\n'

PILL_TEMPLATE = '    <button class="tp-pill{active}" data-mode="{mode}" data-src="{src}" data-fallback-src="{fallback}" data-label="{label}"><span class="dot"></span>{label}</button>'


def build_bar(slug: str = "site-home"):
    pills = []
    for mode, label in [
        ("deep", "Deep Dive"),
        ("debate", "Debate"),
        ("critique", "Critique"),
        ("tts", "TTS"),
        ("web", "Web"),
    ]:
        active = " active" if mode == "tts" else ""
        pills.append(PILL_TEMPLATE.format(
            active=active,
            mode=mode,
            src=MODE_URLS[mode],
            fallback=FALLBACK_URL,
            label=label,
        ))

    return f'''<!-- TP PILL PLAYER BAR — inject after <body>; requires /mda/components/tp-pill-player.css and /mda/components/tp-pill-player.js -->
<div class="tp-pill-bar" id="tpPillBar" data-audio-slug="{slug}">
  <div class="tp-pill-strip">
{'\n'.join(pills)}
  </div>
  <div class="tp-bar-controls">
    <button class="tp-bar-play"><i class="fas fa-play"></i></button>
    <div class="tp-bar-track"><div class="tp-bar-fill"></div></div>
    <span class="tp-bar-time">0:00 / 0:00</span>
    <select class="tp-bar-speed">
      <option value="0.5">0.5x</option>
      <option value="0.75">0.75x</option>
      <option value="1" selected>1x</option>
      <option value="1.25">1.25x</option>
      <option value="1.5">1.5x</option>
      <option value="1.75">1.75x</option>
      <option value="2">2x</option>
    </select>
  </div>
  <audio preload="metadata"></audio>
</div>
'''


def ensure_links(head_text: str) -> str:
    if "/mda/components/tp-pill-player.css" not in head_text:
        head_text = head_text.replace("</head>", CSS_LINK + "</head>", 1)
    if "/mda/components/tp-pill-player.js" not in head_text:
        head_text = head_text.replace("</head>", JS_LINK + "</head>", 1)
    return head_text


BAR_START = "<!-- TP PILL PLAYER BAR"
BAR_END = '  <audio preload="metadata"></audio>\n</div>'


def inject_bar(body_text: str, slug: str = "site-home") -> str:
    # If a bar already exists, replace it in place so updates are idempotent.
    if BAR_START in body_text and BAR_END in body_text:
        start = body_text.index(BAR_START)
        end = body_text.index(BAR_END, start) + len(BAR_END)
        return body_text[:start] + build_bar(slug) + body_text[end:]
    # Insert after the opening <body ...> tag
    return re.sub(r"(<body[^>]*>\n?)", r"\1\n" + build_bar(slug) + "\n", body_text, count=1)


def process_file(path: Path, slug: str = "site-home") -> None:
    text = path.read_text(encoding="utf-8")
    text = ensure_links(text)
    text = inject_bar(text, slug)
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path}")


def fix_mda001_title() -> None:
    path = ROOT / "mda/01-story-thread/MDA-001-story-introduction.html"
    text = path.read_text(encoding="utf-8")
    old = "<title>Introduction () -- The Moral Decline of America</title>"
    new = "<title>Introduction — The Moral Decline of America</title>"
    if old in text:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        print(f"Fixed title in {path}")


if __name__ == "__main__":
    process_file(ROOT / "index.html", slug="site-home")
    process_file(ROOT / "mda/index.html", slug="mda-series-home")
    fix_mda001_title()
