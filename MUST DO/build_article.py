#!/usr/bin/env python3
"""
Build standardized article packages into standalone HTML pages.

Input contract:
  MUST DO/ARTICLE_PACKAGES/<slug>/
    meta.json
    story.md
    plain.md
    test.md
    proof.md
    audio/
    media/

Output:
  MUST DO/_built/<slug>/index.html
  MUST DO/_built/<slug>/meta.json
  MUST DO/_built/<slug>/source/
  MUST DO/_built/<slug>/audio/
  MUST DO/_built/<slug>/media/

The builder keeps the package structure simple for AI authors and handles the
rendering, navigation, classification, and asset wiring downstream.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from typing import Any

try:
    import markdown as md_lib
except Exception:  # pragma: no cover - dependency fallback
    md_lib = None


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGES_ROOT = REPO_ROOT / "MUST DO" / "ARTICLE_PACKAGES"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "MUST DO" / "_built"
CONTENT_ORDER = ["story", "plain", "test", "proof"]
LOCAL_AUDIO_FILES = {
    "podcast": "podcast.mp3",
    "read_aloud": "read-aloud.mp3",
    "debate": "debate.mp3",
    "critique": "critique.mp3",
}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__PAGE_TITLE__</title>
<style>
:root{
  --bg:#050505;
  --panel:#0f0f0f;
  --card:#131313;
  --line:#232323;
  --text:#e7e2d7;
  --muted:#9c9688;
  --gold:#d4af37;
  --gold-soft:rgba(212,175,55,.12);
  --gold-line:rgba(212,175,55,.28);
  --ok:#59c56d;
  --warn:#e2b93b;
  --bad:#d06a5f;
  --radius:18px;
  --radius-sm:12px;
  --shadow:0 24px 60px rgba(0,0,0,.32);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:
  radial-gradient(circle at top, rgba(212,175,55,.08), transparent 38%),
  linear-gradient(180deg,#080808 0%,#040404 100%);
  color:var(--text);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
body{min-height:100vh;line-height:1.65}
a{color:inherit}
.shell-top{
  position:sticky;top:0;z-index:50;
  background:rgba(5,5,5,.96);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--gold-line);
}
.shell-top-inner,.shell-bar-inner,.shell-footer-inner,.shell-bottom-inner{
  max-width:1180px;margin:0 auto;padding:0 1rem;
}
.shell-top-inner{
  min-height:58px;display:flex;align-items:center;justify-content:space-between;gap:1rem;
}
.brand{
  display:flex;align-items:center;gap:.6rem;text-decoration:none;
  font-family:Cinzel,Georgia,serif;font-size:.84rem;letter-spacing:.06em;color:var(--gold);
}
.brand-badge{
  width:11px;height:11px;border-radius:50%;background:var(--gold);
  box-shadow:0 0 12px rgba(212,175,55,.4);
}
.path-tabs{display:flex;flex-wrap:wrap;gap:.35rem;justify-content:center}
.path-tab{
  border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.03);
  color:rgba(255,255,255,.52);border-radius:999px;padding:.4rem .7rem;
  font:600 .62rem/1 JetBrains Mono,ui-monospace,monospace;
  letter-spacing:.06em;text-transform:uppercase;cursor:pointer;
}
.path-tab.active{color:var(--gold);background:var(--gold-soft);border-color:var(--gold-line)}
.path-tab.disabled{opacity:.38;cursor:not-allowed;text-decoration:line-through}
.nav-arrows{display:flex;gap:.5rem;align-items:center}
.nav-arrows a,.nav-arrows span{
  font:600 .62rem/1 Oswald,system-ui,sans-serif;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted);text-decoration:none;padding:.35rem .55rem;border-radius:999px;
}
.nav-arrows a:hover{color:var(--gold);background:var(--gold-soft)}
.bar{
  border-bottom:1px solid rgba(255,255,255,.05);background:rgba(255,255,255,.015);
}
.bar-inner{padding:.8rem 1rem}
.bar-label{
  font:500 .52rem/1 JetBrains Mono,ui-monospace,monospace;letter-spacing:.12em;
  text-transform:uppercase;color:#777;margin-bottom:.45rem
}
.segments{display:flex;overflow:hidden;border-radius:999px;height:8px;background:rgba(255,255,255,.05)}
.seg{height:100%}
.tags{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.45rem}
.tag{
  display:inline-flex;align-items:center;gap:.35rem;
  border:1px solid rgba(255,255,255,.06);background:rgba(255,255,255,.03);
  border-radius:999px;padding:.18rem .5rem;font:400 .56rem/1 JetBrains Mono,ui-monospace,monospace;
  color:#888
}
.dot{width:7px;height:7px;border-radius:50%}
.article{
  max-width:880px;margin:0 auto;padding:2.2rem 1.1rem 1rem;
}
.eyebrow{
  font:600 .62rem/1 JetBrains Mono,ui-monospace,monospace;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gold);margin-bottom:.7rem
}
h1{
  margin:0;font-family:Cinzel,Georgia,serif;font-size:clamp(2.1rem,5vw,3.8rem);
  line-height:1.06;font-weight:600;color:#f4e9c6;
}
.subtitle{
  margin:.8rem 0 1.6rem;font-family:"Crimson Text",Georgia,serif;font-size:1.15rem;
  font-style:italic;color:var(--muted)
}
.meta-row{
  display:flex;flex-wrap:wrap;gap:.5rem .8rem;align-items:center;margin-bottom:1.4rem;
  font:400 .72rem/1.2 JetBrains Mono,ui-monospace,monospace;color:#8b8678
}
.meta-pill{
  display:inline-flex;align-items:center;gap:.35rem;padding:.28rem .55rem;border-radius:999px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.05)
}
.reader-panes{margin-top:1.7rem}
.reader-pane{display:none}
.reader-pane.active{display:block}
.path-head{
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  margin:0 0 1rem;padding-bottom:.55rem;border-bottom:1px solid rgba(212,175,55,.18)
}
.path-name{
  font:600 .74rem/1 JetBrains Mono,ui-monospace,monospace;letter-spacing:.12em;
  text-transform:uppercase;color:var(--gold)
}
.path-desc{font-size:.86rem;color:var(--muted)}
.content{
  background:rgba(255,255,255,.015);border:1px solid rgba(255,255,255,.05);
  border-radius:var(--radius);padding:1.2rem 1.1rem;box-shadow:var(--shadow)
}
.content :is(p,li){font-size:1rem;color:#d4cec1}
.content h1,.content h2,.content h3,.content h4{color:#f2e8ca}
.content h2{
  margin-top:1.5rem;padding-bottom:.35rem;border-bottom:1px solid rgba(212,175,55,.14);
  font:600 1.05rem/1.2 Oswald,system-ui,sans-serif;text-transform:uppercase;letter-spacing:.06em
}
.content blockquote{
  margin:1rem 0;padding:.85rem 1rem;border-left:3px solid var(--gold);
  background:var(--gold-soft);border-radius:0 var(--radius-sm) var(--radius-sm) 0;color:#f2e8ca
}
.content code{background:rgba(255,255,255,.05);padding:.1rem .25rem;border-radius:5px}
.content pre{
  overflow:auto;padding:1rem;background:#0b0b0b;border:1px solid rgba(255,255,255,.08);
  border-radius:var(--radius-sm)
}
.media-card,.rigor-card,.note-card{
  margin-top:1.1rem;background:rgba(255,255,255,.015);border:1px solid rgba(255,255,255,.05);
  border-radius:var(--radius);padding:1rem 1.05rem
}
.card-label{
  font:600 .62rem/1 JetBrains Mono,ui-monospace,monospace;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gold);margin-bottom:.65rem
}
.grid-2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.9rem}
.kv{display:flex;flex-direction:column;gap:.2rem}
.kv span:first-child{font:500 .58rem/1 JetBrains Mono,ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:#8b846f}
.kv span:last-child{color:#ddd6c4;font-size:.92rem}
.list{margin:.45rem 0 0;padding-left:1.2rem}
.list li{margin:.25rem 0;color:#d4cec1}
.audio-dock{
  position:fixed;left:0;right:0;bottom:0;z-index:60;background:rgba(8,8,8,.98);
  border-top:1px solid var(--gold-line);backdrop-filter:blur(12px)
}
.audio-inner{
  max-width:1180px;margin:0 auto;padding:.55rem 1rem;display:flex;flex-wrap:wrap;
  align-items:center;gap:.6rem
}
.audio-tabs{display:flex;flex-wrap:wrap;gap:.25rem}
.audio-tab{
  border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.03);color:#aaa;
  border-radius:999px;padding:.34rem .6rem;font:600 .58rem/1 JetBrains Mono,ui-monospace,monospace;
  text-transform:uppercase;letter-spacing:.08em;cursor:pointer
}
.audio-tab.active{color:var(--gold);background:var(--gold-soft);border-color:var(--gold-line)}
.audio-play,.audio-min{
  border:1px solid var(--gold-line);background:transparent;color:var(--gold);
  width:32px;height:32px;border-radius:999px;cursor:pointer
}
.audio-play:hover,.audio-min:hover{background:var(--gold-soft)}
.audio-track{flex:1;min-width:160px;height:4px;border-radius:999px;background:#242424;overflow:hidden}
.audio-fill{width:0;height:100%;background:var(--gold)}
.audio-time{font:400 .56rem/1 JetBrains Mono,ui-monospace,monospace;color:#7d7769;white-space:nowrap}
.audio-link{
  font:600 .62rem/1 JetBrains Mono,ui-monospace,monospace;letter-spacing:.08em;
  text-transform:uppercase;color:#8f8a7b;text-decoration:none;padding:.2rem .35rem;border-radius:6px
}
.audio-link:hover{color:var(--gold);background:var(--gold-soft)}
.audio-dock.minimized{transform:translateY(calc(100% - 42px))}
.audio-mini{
  position:fixed;right:14px;bottom:14px;z-index:61;display:none;align-items:center;justify-content:center;
  width:42px;height:42px;border-radius:999px;background:#090909;border:1px solid var(--gold-line);
  color:var(--gold);box-shadow:var(--shadow);cursor:pointer
}
.audio-mini.visible{display:flex}
.bottom-shell{
  margin:1.25rem auto 0;padding:0 1rem 1.1rem;max-width:1180px
}
.subdomains{
  display:flex;flex-wrap:wrap;justify-content:center;gap:.35rem .65rem;padding:0 0 .7rem;
  border-top:1px solid rgba(255,255,255,.05);margin-top:1rem
}
.subdomains a{
  font:400 .56rem/1 JetBrains Mono,ui-monospace,monospace;text-transform:uppercase;letter-spacing:.08em;
  color:rgba(255,255,255,.38);text-decoration:none;padding:.28rem .38rem;border-radius:6px
}
.subdomains a:hover{color:var(--gold);background:var(--gold-soft)}
.footer{
  padding:.35rem 0 4.5rem;text-align:center;font:400 .52rem/1.5 JetBrains Mono,ui-monospace,monospace;
  color:rgba(255,255,255,.2)
}
@media (max-width:760px){
  .shell-top-inner{flex-wrap:wrap;justify-content:center;padding:.75rem 1rem}
  .nav-arrows{width:100%;justify-content:center}
  .grid-2{grid-template-columns:1fr}
  .article{padding-top:1.4rem}
}
</style>
</head>
<body>
<header class="shell-top">
  <div class="shell-top-inner">
    <a class="brand" href="/">
      <span class="brand-badge" aria-hidden="true"></span>
      Faith Through Physics
    </a>
    <div class="path-tabs" role="tablist" aria-label="Reading levels">
      __PATH_TABS__
    </div>
    <div class="nav-arrows">
      __PREV_LINK__
      <a href="__HOME_HREF__">Series Home</a>
      __NEXT_LINK__
    </div>
  </div>
</header>

<section class="bar">
  <div class="shell-bar-inner bar-inner">
    <div class="bar-label">Article Classification</div>
    <div class="segments">__CLASS_SEGMENTS__</div>
    <div class="tags">__CLASS_TAGS__</div>
  </div>
</section>

<main class="article">
  <div class="eyebrow">__SERIES_LABEL__</div>
  <h1>__TITLE__</h1>
  <div class="subtitle">__SUBTITLE__</div>
  <div class="meta-row">
    <span class="meta-pill">__AUTHOR__</span>
    <span class="meta-pill">__DATE__</span>
    <span class="meta-pill">__STATUS__</span>
    <span class="meta-pill">__SLUG__</span>
  </div>

  <section class="media-card" __MEDIA_HIDDEN__>
    <div class="card-label">Media</div>
    <div class="grid-2">
      <div class="kv">
        <span>Hero</span>
        <span>__HERO_NOTE__</span>
      </div>
      <div class="kv">
        <span>Figures</span>
        <span>__FIGURE_NOTE__</span>
      </div>
    </div>
  </section>

  <div class="reader-panes">
    __READER_PANES__
  </div>

  <section class="rigor-card" __RIGOR_HIDDEN__>
    <div class="card-label">Rigor Card</div>
    <div class="grid-2">
      <div class="kv">
        <span>Formal refs</span>
        <span>__FORMAL_REF_SUMMARY__</span>
      </div>
      <div class="kv">
        <span>Reading levels</span>
        <span>__READING_LEVELS_SUMMARY__</span>
      </div>
    </div>
    <ul class="list">
      __KILL_CONDITIONS__
    </ul>
  </section>

  <section class="note-card" __NOTE_HIDDEN__>
    <div class="card-label">Build Notes</div>
    <div class="kv">
      <span>Package source</span>
      <span>__PACKAGE_PATH__</span>
    </div>
    <div class="kv" style="margin-top:.65rem">
      <span>Build output</span>
      <span>__OUTPUT_PATH__</span>
    </div>
  </section>
</main>

<div class="bottom-shell">
  <nav class="subdomains">
    <a href="/">Home</a>
    <a href="/one-page-stories/">One-Page Stories</a>
    <a href="/master-equation/">Master Equation</a>
    <a href="/Axiom%20Layer/">Axiom Layer</a>
    <a href="/proof-explorer/">Proof Explorer</a>
    <a href="/the-bilateral-audit/">Bilateral Audit</a>
    <a href="/isomorphism/">Isomorphisms</a>
    <a href="/lean4/">Lean 4</a>
  </nav>
  <div class="footer">Copyright 2024-2026 David Lowe - Faith Through Physics</div>
</div>

<div class="audio-dock __AUDIO_DOCK_MINIMIZED__" id="audioDock" __AUDIO_HIDDEN__>
  <div class="audio-inner">
    <div class="audio-tabs">
      __AUDIO_TABS__
    </div>
    <button class="audio-play" id="audioPlay" type="button" aria-label="Play audio">Play</button>
    <div class="audio-track" id="audioTrack" aria-label="Audio progress track">
      <div class="audio-fill" id="audioFill"></div>
    </div>
    <span class="audio-time" id="audioTime">0:00 / 0:00</span>
    <a class="audio-link" id="audioOpen" href="#" target="_blank" rel="noreferrer">Open</a>
    <button class="audio-min" id="audioMin" type="button" aria-label="Minimize player">-</button>
  </div>
</div>
<button class="audio-mini" id="audioMiniBtn" type="button" aria-label="Show player">Play</button>

<script id="article-meta" type="application/json">__META_JSON__</script>
<script>
(function(){
  const meta = JSON.parse(document.getElementById('article-meta').textContent);
  const availablePanes = Array.from(document.querySelectorAll('.reader-pane'));
  const tabs = Array.from(document.querySelectorAll('[data-reader-path]'));
  const audioMeta = meta.audio || {};
  const audioMap = Array.from(document.querySelectorAll('[data-audio-mode]')).reduce((acc, btn) => {
    acc[btn.dataset.audioMode] = btn.dataset.audioSrc || '';
    return acc;
  }, {});
  const dock = document.getElementById('audioDock');
  const playBtn = document.getElementById('audioPlay');
  const audioMiniBtn = document.getElementById('audioMiniBtn');
  const audioMin = document.getElementById('audioMin');
  const audioTrack = document.getElementById('audioTrack');
  const audioFill = document.getElementById('audioFill');
  const audioTime = document.getElementById('audioTime');
  const audioOpen = document.getElementById('audioOpen');
  const audio = new Audio();
  audio.preload = 'metadata';
  let currentMode = audioMap.podcast ? 'podcast' : (audioMap.read_aloud ? 'read_aloud' : (audioMap.debate ? 'debate' : (audioMap.critique ? 'critique' : '')));

  function formatTime(value){
    if (!isFinite(value) || value < 0) return '0:00';
    const mins = Math.floor(value / 60);
    const secs = Math.floor(value % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
  }

  function setTab(path){
    const available = tabs.find(btn => btn.dataset.readerPath === path && !btn.classList.contains('disabled'));
    if (!available) return;
    tabs.forEach(btn => btn.classList.toggle('active', btn === available));
    availablePanes.forEach(pane => pane.classList.toggle('active', pane.dataset.readerPane === path));
    localStorage.setItem('ftp-reader-mode', path);
  }

  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      if (btn.classList.contains('disabled')) return;
      setTab(btn.dataset.readerPath);
    });
  });

  const storedPane = localStorage.getItem('ftp-reader-mode');
  if (storedPane && tabs.some(btn => btn.dataset.readerPath === storedPane && !btn.classList.contains('disabled'))) {
    setTab(storedPane);
  } else {
    const firstPane = tabs.find(btn => !btn.classList.contains('disabled'));
    if (firstPane) setTab(firstPane.dataset.readerPath);
  }

  function setAudioMode(mode){
    currentMode = mode;
    document.querySelectorAll('[data-audio-mode]').forEach(btn => btn.classList.toggle('active', btn.dataset.audioMode === mode));
    const src = audioMap[mode];
    if (!src) return;
    audio.src = src;
    audioOpen.href = src;
    audio.load();
  }

  document.querySelectorAll('[data-audio-mode]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (btn.dataset.audioSrc) setAudioMode(btn.dataset.audioMode);
    });
  });

  if (currentMode) setAudioMode(currentMode);
  if (!currentMode) {
    dock.style.display = 'none';
    audioMiniBtn.style.display = 'none';
  }

  playBtn.addEventListener('click', () => {
    if (!audio.src) return;
    if (audio.paused) audio.play();
    else audio.pause();
  });

  audio.addEventListener('play', () => playBtn.textContent = 'Pause');
  audio.addEventListener('pause', () => playBtn.textContent = 'Play');
  audio.addEventListener('timeupdate', () => {
    if (audio.duration && isFinite(audio.duration)) {
      audioFill.style.width = `${Math.min(100, (audio.currentTime / audio.duration) * 100)}%`;
      audioTime.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
    }
  });
  audio.addEventListener('loadedmetadata', () => {
    audioTime.textContent = `0:00 / ${formatTime(audio.duration)}`;
  });
  audio.addEventListener('ended', () => {
    audio.pause();
    audio.currentTime = 0;
  });

  audioTrack.addEventListener('click', (event) => {
    if (!audio.duration || !isFinite(audio.duration)) return;
    const rect = audioTrack.getBoundingClientRect();
    const pct = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    audio.currentTime = audio.duration * pct;
  });

  audioMin.addEventListener('click', () => {
    dock.classList.add('minimized');
    audioMiniBtn.classList.add('visible');
  });
  audioMiniBtn.addEventListener('click', () => {
    dock.classList.remove('minimized');
    audioMiniBtn.classList.remove('visible');
  });
})();
</script>
</body>
</html>
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def pretty(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return html.escape(text)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def markdown_to_html(text: str) -> str:
    if not text.strip():
        return "<p class=\"empty-note\">No content provided.</p>"
    if md_lib is None:
        paragraphs = [segment.strip() for segment in re.split(r"\n\s*\n", text.strip()) if segment.strip()]
        rendered = []
        for paragraph in paragraphs:
            if paragraph.startswith("#"):
                level = len(paragraph) - len(paragraph.lstrip("#"))
                heading = paragraph[level:].strip()
                rendered.append(f"<h{level}>{html.escape(heading)}</h{level}>")
            else:
                rendered.append(f"<p>{html.escape(paragraph).replace(chr(10), '<br>')}</p>")
        return "\n".join(rendered)
    return md_lib.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists", "footnotes"],
        output_format="html5",
    )


def resolve_article_path(value: Any, output_root: Path) -> str:
    if value in (None, "", False):
        return "#"
    text = str(value).strip()
    if text.startswith(("http://", "https://", "/")) or text.endswith(".html"):
        return text
    return f"../{text}/index.html"


def resolve_audio_source(meta_audio: dict[str, Any], package_dir: Path, name: str) -> str:
    remote = meta_audio.get(name)
    if remote:
        return str(remote).strip()
    local_name = LOCAL_AUDIO_FILES[name]
    local_path = package_dir / "audio" / local_name
    if local_path.exists():
        return f"audio/{local_name}"
    return ""


def copy_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    for item in source.rglob("*"):
        if item.is_dir():
            continue
        target = destination / item.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)


def build_classification(meta: dict[str, Any]) -> tuple[str, str]:
    raw = meta.get("classification") or []
    items = [item for item in raw if isinstance(item, dict)]
    if not items:
        return "", ""
    segments: list[str] = []
    tags: list[str] = []
    for item in items:
        tag = pretty(item.get("tag", ""))
        pct = item.get("pct", 0)
        color = item.get("color", "#666")
        segments.append(f'<div class="seg" style="width:{float(pct):.2f}%;background:{html.escape(str(color))}" title="{tag} {pct}%"></div>')
        tags.append(
            f'<span class="tag"><span class="dot" style="background:{html.escape(str(color))}"></span>{tag} {pct}%</span>'
        )
    return "".join(segments), "".join(tags)


def build_reader_tabs(levels: list[str], available: set[str], active: str) -> str:
    label_map = {
        "story": "Story Path",
        "plain": "Plain Path",
        "test": "Test Path",
        "proof": "Proof Path",
    }
    buttons: list[str] = []
    for level in levels:
        label = label_map.get(level, level.title())
        classes = ["path-tab"]
        attrs = [f'data-reader-path="{html.escape(level)}"']
        if level == active:
            classes.append("active")
        if level not in available:
            classes.append("disabled")
            attrs.append("disabled")
            attrs.append('aria-disabled="true"')
        buttons.append(f'<button type="button" class="{" ".join(classes)}" {" ".join(attrs)}>{html.escape(label)}</button>')
    return "".join(buttons)


def build_audio_tabs(audio_sources: dict[str, str], active_mode: str) -> str:
    labels = {
        "podcast": "Podcast",
        "read_aloud": "Read Aloud",
        "debate": "Debate",
        "critique": "Critique",
    }
    buttons: list[str] = []
    for name, label in labels.items():
        source = audio_sources.get(name, "")
        classes = ["audio-tab"]
        attrs = [f'data-audio-mode="{name}"', f'data-audio-src="{html.escape(source)}"']
        if source and name == active_mode:
            classes.append("active")
        else:
            classes.append("disabled")
            attrs.append("disabled")
        buttons.append(
            f'<button type="button" class="{" ".join(classes)}" {" ".join(attrs)}>{html.escape(label)}</button>'
        )
    return "".join(buttons)


def build_panes(package_dir: Path, levels: list[str]) -> tuple[str, set[str], str]:
    available: set[str] = set()
    panes: list[str] = []
    active = ""
    desc_map = {
        "story": "Narrative, human-first, image-rich.",
        "plain": "Clear explanation without the technical load.",
        "test": "Claims, objections, evidence, kill conditions.",
        "proof": "Formal references, equations, and rigor artifacts.",
    }
    label_map = {
        "story": "Story Path",
        "plain": "Plain Path",
        "test": "Test Path",
        "proof": "Proof Path",
    }
    for level in levels:
        md_path = package_dir / f"{level}.md"
        if md_path.exists():
            available.add(level)
            if not active:
                active = level
            body_html = markdown_to_html(read_text(md_path))
            content = f'<div class="content">{body_html}</div>'
        else:
            content = '<div class="content"><p class="empty-note">Not provided in this package.</p></div>'
        panes.append(
            "".join(
                [
                    f'<section class="reader-pane{" active" if level == active else ""}" data-reader-pane="{html.escape(level)}">',
                    '<div class="path-head">',
                    f'<div class="path-name">{html.escape(label_map.get(level, level.title()))}</div>',
                    f'<div class="path-desc">{html.escape(desc_map.get(level, ""))}</div>',
                    "</div>",
                    content,
                    "</section>",
                ]
            )
        )
    if not active and levels:
        active = levels[0]
    return "".join(panes), available, active


def build_kill_conditions(items: list[Any]) -> str:
    if not items:
        return '<li>None specified.</li>'
    return "".join(f"<li>{html.escape(str(item))}</li>" for item in items)


def copy_package_assets(package_dir: Path, output_dir: Path) -> None:
    for folder_name in ("audio", "media"):
        copy_tree(package_dir / folder_name, output_dir / folder_name)
    for name in ("meta.json", "story.md", "plain.md", "test.md", "proof.md", "tts-source.txt"):
        source = package_dir / name
        if source.exists():
            target = output_dir / "source" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def build_article(package_dir: Path, output_root: Path) -> Path:
    meta_path = package_dir / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing meta.json in {package_dir}")

    meta = load_json(meta_path)
    levels = meta.get("options", {}).get("reading_levels") or CONTENT_ORDER
    levels = [level for level in levels if level in CONTENT_ORDER]
    if not levels:
        levels = CONTENT_ORDER[:]

    title = str(meta.get("title") or package_dir.name)
    subtitle = str(meta.get("subtitle") or "").strip()
    author = str(meta.get("author") or "").strip() or "Unknown author"
    date = str(meta.get("date") or "").strip()
    series_title = str(meta.get("series_title") or meta.get("series") or "").strip()
    status = str(meta.get("status") or "draft").strip()
    slug = str(meta.get("slug") or package_dir.name).strip()
    prev_href = resolve_article_path(meta.get("prev"), output_root)
    next_href = resolve_article_path(meta.get("next"), output_root)
    home_href = resolve_article_path(meta.get("series_home") or "/one-page-stories/", output_root)

    classification_segments, classification_tags = build_classification(meta)
    panes_html, available_levels, active_level = build_panes(package_dir, levels)
    tabs_html = build_reader_tabs(levels, available_levels, active_level)

    audio = meta.get("audio") or {}
    audio_sources = {
        "podcast": resolve_audio_source(audio, package_dir, "podcast"),
        "read_aloud": resolve_audio_source(audio, package_dir, "read_aloud"),
        "debate": resolve_audio_source(audio, package_dir, "debate"),
        "critique": resolve_audio_source(audio, package_dir, "critique"),
    }
    active_audio_mode = next((name for name, source in audio_sources.items() if source), "")
    audio_tabs_html = build_audio_tabs(audio_sources, active_audio_mode)
    any_audio = any(audio_sources.values())

    formal = meta.get("formal_refs") or {}
    axioms = formal.get("axioms") or []
    theorems = formal.get("theorems") or []
    iso = formal.get("isomorphisms") or []
    kill_conditions = formal.get("kill_conditions") or []
    formal_summary = (
        f"{len(axioms)} axioms - {len(theorems)} theorems - {len(iso)} isomorphisms"
        if any([axioms, theorems, iso])
        else "No formal refs supplied."
    )
    reading_levels_summary = " / ".join(levels).title()

    media_dir = package_dir / "media"
    hero_exists = any((media_dir / candidate).exists() for candidate in ("hero.jpg", "hero.jpeg", "hero.png", "hero.webp"))
    figure_count = len([p for p in media_dir.glob("*") if p.is_file()]) - (1 if hero_exists else 0)
    hero_note = "Hero image available." if hero_exists else "No hero image supplied."
    figure_note = f"{max(figure_count, 0)} additional figure file(s)." if figure_count > 0 else "No figures supplied."
    media_hidden = "" if hero_exists or figure_count > 0 else "hidden"
    rigor_hidden = "" if any([axioms, theorems, iso, kill_conditions]) else "hidden"
    note_hidden = "" if package_dir.exists() else "hidden"
    audio_hidden = "" if any_audio else "hidden"

    page = HTML_TEMPLATE
    replacements = {
        "__PAGE_TITLE__": html.escape(f"{title} - Faith Through Physics"),
        "__PATH_TABS__": tabs_html,
        "__PREV_LINK__": f'<a href="{html.escape(prev_href)}">Prev</a>' if prev_href != "#" else '<span>Prev</span>',
        "__NEXT_LINK__": f'<a href="{html.escape(next_href)}">Next</a>' if next_href != "#" else '<span>Next</span>',
        "__HOME_HREF__": html.escape(home_href),
        "__CLASS_SEGMENTS__": classification_segments or '<div class="seg" style="width:100%;background:#333"></div>',
        "__CLASS_TAGS__": classification_tags or '<span class="tag">No classification data</span>',
        "__SERIES_LABEL__": html.escape(series_title or "Article"),
        "__TITLE__": html.escape(title),
        "__SUBTITLE__": html.escape(subtitle or ""),
        "__AUTHOR__": html.escape(author),
        "__DATE__": html.escape(date or "Undated"),
        "__STATUS__": html.escape(status),
        "__SLUG__": html.escape(slug),
        "__MEDIA_HIDDEN__": media_hidden,
        "__HERO_NOTE__": html.escape(hero_note),
        "__FIGURE_NOTE__": html.escape(figure_note),
        "__READER_PANES__": panes_html,
        "__RIGOR_HIDDEN__": rigor_hidden,
        "__FORMAL_REF_SUMMARY__": html.escape(formal_summary),
        "__READING_LEVELS_SUMMARY__": html.escape(reading_levels_summary),
        "__KILL_CONDITIONS__": build_kill_conditions(kill_conditions),
        "__NOTE_HIDDEN__": note_hidden,
        "__PACKAGE_PATH__": html.escape(str(package_dir)),
        "__OUTPUT_PATH__": html.escape(str(output_root / slug / "index.html")),
        "__AUDIO_DOCK_MINIMIZED__": "",
        "__AUDIO_HIDDEN__": audio_hidden,
        "__AUDIO_TABS__": audio_tabs_html,
        "__META_JSON__": html.escape(json.dumps(meta, ensure_ascii=False)),
    }
    for key, value in replacements.items():
        page = page.replace(key, value)

    # If the page has no audio, remove the audio dock entirely to avoid empty chrome.
    if audio_hidden:
        page = re.sub(r'<div class="audio-dock .*?</div>\s*<button class="audio-mini".*?</button>\s*', "", page, flags=re.S)

    output_dir = output_root / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    write_text(output_dir / "index.html", page)
    write_text(output_dir / "meta.json", json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    copy_package_assets(package_dir, output_dir)
    return output_dir / "index.html"


def find_packages(root: Path) -> list[Path]:
    packages: list[Path] = []
    for candidate in root.iterdir():
        if candidate.is_dir() and (candidate / "meta.json").exists():
            packages.append(candidate)
    return sorted(packages, key=lambda item: item.name.lower())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build standardized article packages into HTML.")
    parser.add_argument("package", nargs="?", help="Slug or path to an article package. Omit to build all packages.")
    parser.add_argument("--packages-root", default=str(PACKAGES_ROOT), help="Root folder that contains article packages.")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Where built HTML should go.")
    return parser.parse_args()


def resolve_package(arg: str, packages_root: Path) -> Path:
    direct = Path(arg)
    if direct.exists():
        return direct.resolve()
    candidate = packages_root / arg
    if candidate.exists():
        return candidate.resolve()
    raise FileNotFoundError(f"Could not find article package '{arg}' in {packages_root}")


def main() -> int:
    args = parse_args()
    packages_root = Path(args.packages_root).resolve()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    if args.package:
        package_dirs = [resolve_package(args.package, packages_root)]
    else:
        package_dirs = find_packages(packages_root)

    if not package_dirs:
        raise SystemExit(f"No article packages found under {packages_root}")

    built: list[Path] = []
    for package_dir in package_dirs:
        built.append(build_article(package_dir, output_root))

    print(f"Built {len(built)} article(s) into {output_root}")
    for path in built:
        print(f" - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
