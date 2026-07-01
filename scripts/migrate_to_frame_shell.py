#!/usr/bin/env python3
"""
Migrate old embedded shell pages to the universal frame.js shell.

Targets only pages that:
  - have the OLD shell ELEMENT (<header class="tp-top"> or .tp-class)
  - do NOT already load /site-shell/frame.js

Actions (matches already-migrated one-page-stories pages):
  - strip legacy chrome elements (top bar, class bar, inline player, big nav)
  - inject <script src="/site-shell/frame.js" defer></script> before </body>
  - preserve <h1>, <p class="subtitle">, and article body untouched

Usage:
  python scripts/migrate_to_frame_shell.py --dry-run one-page-stories
  python scripts/migrate_to_frame_shell.py --apply one-page-stories
"""
import argparse
import json
import re
import shutil
import time
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Comment
except ImportError as exc:
    raise SystemExit("beautifulsoup4 required: pip install beautifulsoup4 lxml") from exc

ROOT = Path(__file__).resolve().parent.parent
FRAME_TAG = '<script src="/site-shell/frame.js" defer></script>'
LOG_PATH = ROOT.parent / "faiththruphysics-site-data" / "debug-68d22e.log"

# Classes whose root elements are removed (not CSS-only leftovers).
LEGACY_CLASSES = {
    "tp-top", "tp-class", "tp-player-block", "tp-bignav",
    "tp-header-lip", "tp-verify-top", "dock-mini",
}
LEGACY_TAGS = {"header"}  # only when also carries a legacy class


def _log(run_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    # region agent log
    try:
        entry = {
            "sessionId": "68d22e",
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
    except OSError:
        pass
    # endregion


def has_old_shell(soup: BeautifulSoup) -> bool:
    if soup.find("header", class_=lambda c: c and "tp-top" in c):
        return True
    if soup.find(class_=lambda c: c and "tp-class" in c):
        return True
    return False


def has_frame_js(soup: BeautifulSoup) -> bool:
    for s in soup.find_all("script", src=True):
        src = s.get("src", "")
        if "site-shell/frame.js" in src:
            return True
    return False


def classes_of(el) -> set:
    try:
        return set(el.get("class") or [])
    except AttributeError:
        return set()


def is_legacy_element(el) -> bool:
    if not getattr(el, "name", None):
        return False
    cls = classes_of(el)
    if cls & LEGACY_CLASSES:
        return True
    if el.name in LEGACY_TAGS and cls & {"tp-top"}:
        return True
    if el.name == "div" and "verification-bar" in cls:
        return True
    return False


def strip_legacy_shell(soup: BeautifulSoup) -> list:
    removed = []
    # Collect first — don't mutate while walking.
    targets = [el for el in soup.find_all(True) if is_legacy_element(el)]
    for el in targets:
        # Skip if already decomposed (parent is None)
        if el.parent is None:
            continue
        removed.append(el.name + ("." + ".".join(classes_of(el)) if classes_of(el) else ""))
        el.decompose()
    return removed


def inject_frame_js(soup: BeautifulSoup):
    if has_frame_js(soup):
        return False
    tag = soup.new_tag("script", src="/site-shell/frame.js", defer="")
    body = soup.find("body")
    if not body:
        return False
    body.append(tag)
    return True


def title_stem(title: str) -> str:
    t = re.sub(r"\s+", " ", title).strip()
    return re.split(r"\s+[-|\u2013\u2014]\s+", t)[0].strip()


def is_mangled_h1(soup: BeautifulSoup) -> bool:
    h1 = soup.find("h1")
    title_tag = soup.find("title")
    if not h1 or not title_tag:
        return False
    full_title = re.sub(r"\s+", " ", title_tag.get_text(strip=True)).strip()
    inner = re.sub(r"\s+", " ", h1.get_text(strip=True)).strip()
    stem = title_stem(full_title)
    if len(stem) < 4 or not inner.startswith(stem):
        return False
    if len(inner) <= len(stem) + 1:
        return False
    rest = inner[len(stem):].strip()
    if not rest:
        return False
    # Not mangled if the h1 exactly matches the full <title> text (em-dash title pages)
    if inner == full_title or inner == re.sub(r"\s*[-\u2013\u2014]\s*.*$", "", full_title).strip():
        return False
    return True


def read_html(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    try:
        return data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return data.decode("latin-1"), "latin-1"


def migrate_file(path: Path, dry_run: bool, run_id: str) -> str:
    rel = path.relative_to(ROOT)
    raw, enc = read_html(path)
    soup = BeautifulSoup(raw, "html.parser")

    if has_frame_js(soup):
        _log(run_id, "H-skip-framed", str(rel), "skip already framed", {})
        return "skip-framed"

    if not has_old_shell(soup):
        _log(run_id, "H-skip-no-old", str(rel), "skip no old shell", {})
        return "skip-no-old"

    h1_before = (soup.find("h1").get_text(strip=True) if soup.find("h1") else "")
    sub_before = ""
    sub_el = soup.find("p", class_=lambda c: c and "subtitle" in c)
    if sub_el:
        sub_before = sub_el.get_text(strip=True)

    removed = strip_legacy_shell(soup)
    injected = inject_frame_js(soup)

    h1_after = (soup.find("h1").get_text(strip=True) if soup.find("h1") else "")
    sub_after = ""
    sub_el = soup.find("p", class_=lambda c: c and "subtitle" in c)
    if sub_el:
        sub_after = sub_el.get_text(strip=True)

    mangled = is_mangled_h1(soup)
    title_changed = h1_before != h1_after or sub_before != sub_after

    _log(run_id, "H-migrate", str(rel), "migrated", {
        "removed": removed,
        "injected": injected,
        "h1_before": h1_before[:120],
        "h1_after": h1_after[:120],
        "sub_before": sub_before[:120],
        "sub_after": sub_after[:120],
        "title_changed": title_changed,
        "mangled_h1": mangled,
    })

    if title_changed:
        return "error-title-changed"

    if mangled:
        return "error-mangled"

    if dry_run:
        return "dry-run"

    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(path, backup)
    soup_str = str(soup)
    if not has_frame_js(BeautifulSoup(soup_str, "html.parser")):
        return "error-no-frame"
    path.write_text(soup_str, encoding=enc)
    return "applied"


def collect_files(targets: list[Path], include_index: bool) -> list[Path]:
    files = []
    for t in targets:
        p = ROOT / t if not t.is_absolute() else t
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.html")))
    if not include_index:
        files = [f for f in files if f.name.lower() != "index.html"]
    return [f for f in files if f.is_relative_to(ROOT)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Files or directories")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--include-index", action="store_true", default=True)
    parser.add_argument("--exclude-index", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        args.dry_run = True

    run_id = "migrate-apply" if args.apply else "migrate-dry"
    include_index = args.include_index and not args.exclude_index
    files = collect_files([Path(p) for p in args.paths], include_index)

    counts = {}
    for f in files:
        status = migrate_file(f, dry_run=not args.apply, run_id=run_id)
        counts[status] = counts.get(status, 0) + 1
        if status not in ("skip-framed", "skip-no-old"):
            print(f"  {status:20} {f.relative_to(ROOT)}")

    print(f"\nSummary ({'APPLY' if args.apply else 'DRY-RUN'}):")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
