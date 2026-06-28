#!/usr/bin/env python3
"""
Apply components/universal-shell-v5.html to article pages.

Best-effort extraction of:
  - <title>
  - first <h1>
  - subtitle / byline (heuristic)
  - main body content
  - existing audio player block
  - canonical URL

Usage:
  python scripts/apply_universal_shell.py --dry-run path/to/file.html
  python scripts/apply_universal_shell.py --batch mda/ moral-decline/ genesis-to-quantum/
"""

import argparse
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin

try:
    from bs4 import BeautifulSoup, NavigableString
except ImportError as exc:
    raise SystemExit("beautifulsoup4 is required: pip install beautifulsoup4 lxml") from exc

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / "components" / "universal-shell-v5.html"

SERIES_MAP = {
    "mda": ("/moral-decline/", "MDA Series Home"),
    "moral-decline": ("/moral-decline/", "MDA Series Home"),
    "genesis-to-quantum": ("/genesis-to-quantum/", "GTQ Series Home"),
    "cross-domain": ("/cross-domain/", "Cross-Domain Series Home"),
    "one-page-stories": ("/one-page-stories/", "One-Page Stories Home"),
    "blue": ("/blue/", "Blue Papers Home"),
    "consciousness": ("/consciousness/", "Consciousness Home"),
    "convergence-series": ("/convergence-series/", "Convergence Home"),
    "proof-architecture": ("/proof-architecture/", "Proof Architecture Home"),
    "the-bidirectional-audit": ("/the-bidirectional-audit/", "Bidirectional Audit Home"),
    "three-truths": ("/three-truths/", "Three Truths Home"),
    "three-gates": ("/three-gates/", "Three Gates Home"),
    "revolution-of-truth": ("/revolution-of-truth/", "Revolution of Truth Home"),
    "rigor": ("/rigor/", "Rigor Home"),
}


def load_shell():
    return SHELL.read_text(encoding="utf-8")


def guess_series(rel_path: Path):
    parts = rel_path.parts
    for part in parts:
        if part in SERIES_MAP:
            return SERIES_MAP[part]
    return ("/", "faiththruphysics.com")


def extract_metadata(soup: BeautifulSoup):
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Faith thru Physics"

    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else title

    subtitle = ""
    byline = ""

    # Try explicit subtitle/byline classes
    for p in soup.find_all("p"):
        cls = " ".join(p.get("class", [])).lower()
        text = p.get_text(strip=True)
        if not subtitle and ("subtitle" in cls or "deck" in cls):
            subtitle = text
        elif not byline and ("byline" in cls or "meta" in cls or "author" in cls):
            byline = text
        if subtitle and byline:
            break

    # Fallback byline from title text after em-dash or pipe
    if not byline and "—" in title:
        byline = title.split("—", 1)[1].strip()

    return {
        "title": title,
        "h1": h1_text,
        "subtitle": subtitle,
        "byline": byline,
    }


def is_likely_wrapper(node):
    """Heuristic: is this node a nav/header/footer/sidebar rather than main content?"""
    if isinstance(node, NavigableString):
        return False
    if node.name in {"header", "nav", "footer", "aside", "script", "style", "noscript"}:
        return True
    cls = " ".join(node.get("class", [])).lower()
    bad = {"nav", "header", "footer", "sidebar", "topbar", "bottombar", "player", "audio", "toolbar", "banner"}
    for b in bad:
        if b in cls:
            return True
    return False


def content_score(el):
    """Score an element by how likely it is to be the main content container."""
    if isinstance(el, NavigableString):
        return -1
    if is_likely_wrapper(el):
        return -1
    cls = " ".join(el.get("class", [])).lower()
    score = len(el.find_all("p")) * 2 + len(el.find_all("section"))
    if el.find("h1"):
        score += 20
    if "content" in cls or "article" in cls or "prose" in cls or "main" in cls:
        score += 30
    if "max-w" in cls:
        score += 10
    # Penalize very shallow / body-level wrappers
    depth = 0
    parent = el.parent
    while parent and parent.name not in {"body", "html"}:
        depth += 1
        parent = parent.parent
    score += depth
    return score


def find_main_content(soup: BeautifulSoup):
    """Return HTML string of the main article body, excluding nav/headers/footers."""
    # Prefer <article> or <main> explicitly.
    preferred = soup.find("article") or soup.find("main")

    candidates = []
    body = soup.find("body")
    if body:
        for el in body.find_all(True):
            score = content_score(el)
            if score > 0:
                candidates.append((score, el))

    # If we have a preferred container, force it to the top of the list.
    if preferred:
        candidates = [(9999, preferred)] + candidates

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best = candidates[0][1]
        # Parse the container HTML into a new tree so decompose works cleanly.
        container_soup = BeautifulSoup(str(best), "html.parser")
        root = container_soup.find()

        # Collect elements to remove first (don't mutate while iterating deep lists).
        to_remove = []
        for el in root.find_all(True):
            if not getattr(el, "name", None):
                continue
            if el.name in {"header", "nav", "footer"}:
                to_remove.append(el)
                continue
            cls = " ".join(el.get("class", []) or [])
            if "tp-player-block" in cls or "tp-read-aloud" in cls:
                to_remove.append(el)
                continue
            # Remove duplicate h1 inside the content (we extracted the first as article h1)
            if el.name == "h1":
                to_remove.append(el)

        for el in to_remove:
            if el and el.parent:
                el.decompose()

        # Return innerHTML of cleaned container
        return "".join(str(c) for c in root.children)

    return ""


def is_excluded_node(node):
    if isinstance(node, NavigableString):
        return False
    if node.name in {"script", "style", "noscript"}:
        return True
    excluded = {"tp-top", "tp-class", "tp-bignav", "tp-audit", "tp-bottom", "mtl-reader-bar"}
    if set(node.get("class", [])) & excluded:
        return True
    return False


def is_excluded_node(node):
    if isinstance(node, NavigableString):
        return False
    if node.name in {"script", "style", "noscript", "header"}:
        return True
    excluded = {"tp-top", "tp-class", "tp-bignav", "tp-audit", "tp-bottom", "mtl-reader-bar", "tp-player-block"}
    if set(node.get("class", [])) & excluded:
        return True
    return False


def extract_audio_player(soup: BeautifulSoup):
    block = soup.find("div", class_="tp-player-block")
    if block:
        return str(block)
    return ""


def extract_canonical(soup: BeautifulSoup, rel_path: Path):
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        return link["href"]
    return f"https://faiththruphysics.com/{rel_path.as_posix()}"


def apply_to_file(html_path: Path, dry_run: bool = False):
    rel = html_path.relative_to(ROOT)
    print(f"Processing {rel}...")

    shell = load_shell()
    original = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(original, "html.parser")

    # Skip if already wrapped in v5 shell
    if soup.find(class_="tp-top"):
        print(f"  SKIP: already has v5 shell")
        return False

    meta = extract_metadata(soup)
    body_content = find_main_content(soup)
    audio_player = extract_audio_player(soup)
    canonical = extract_canonical(soup, rel)

    series_href, series_label = guess_series(rel)

    # Build placeholders
    placeholders = {
        "{{PAGE_TITLE}}": meta["title"],
        "{{PAGE_CANONICAL}}": canonical,
        "{{ARTICLE_H1}}": meta["h1"],
        "{{ARTICLE_SUBTITLE}}": meta["subtitle"],
        "{{ARTICLE_BYLINE}}": meta["byline"] or "Faith thru Physics",
        "{{ARTICLE_BODY}}": body_content,
        "{{AUDIO_PLAYER_BLOCK}}": audio_player,
        "{{PREV_HREF}}": "#",
        "{{PREV_TITLE}}": "Previous",
        "{{NEXT_HREF}}": "#",
        "{{NEXT_TITLE}}": "Next",
        "{{SERIES_HOME_HREF}}": series_href,
        "{{SERIES_HOME_LABEL}}": series_label,
        "{{AUDIT_RIGHT}}": "<li>Load-bearing claims, clear definitions, and the parts that clearly survived the check.</li>",
        "{{AUDIT_OVER}}": "<li>Strong direction, but the language ran ahead of the evidence or the proof.</li>",
        "{{AUDIT_WRONG}}": "<li>Claims that need correction, tightening, or weaker formulation.</li>",
    }

    new_html = shell
    for key, val in placeholders.items():
        new_html = new_html.replace(key, val)

    # Preserve original head-only elements that are not already in shell (e.g. analytics, meta)
    # For simplicity, just keep the original <head> extra tags by inserting them before </head>.
    # This is a best-effort; full head merging is complex.

    if dry_run:
        preview = new_html[:600]
        print(f"  DRY-RUN preview:\n{preview}\n...")
        return True

    # Backup
    backup = html_path.with_suffix(html_path.suffix + ".bak")
    shutil.copy2(html_path, backup)

    html_path.write_text(new_html, encoding="utf-8")
    print(f"  DONE (backup: {backup.name})")
    return True


def collect_article_files(paths, skip_index=True):
    files = []
    for p in paths:
        target = ROOT / p
        if target.is_file() and target.suffix == ".html":
            files.append(target)
        elif target.is_dir():
            files.extend(target.rglob("*.html"))
    if skip_index:
        files = [f for f in files if f.name.lower() != "index.html"]
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Files or directories to process")
    parser.add_argument("--dry-run", action="store_true", help="Show preview without writing")
    parser.add_argument("--include-index", action="store_true", help="Also process index.html landing pages")
    args = parser.parse_args()

    files = collect_article_files(args.paths, skip_index=not args.include_index)
    files = [f for f in files if f.is_relative_to(ROOT)]

    print(f"Found {len(files)} HTML files")
    processed = 0
    for f in files:
        if apply_to_file(f, dry_run=args.dry_run):
            processed += 1
    print(f"Processed {processed} files")


if __name__ == "__main__":
    main()
