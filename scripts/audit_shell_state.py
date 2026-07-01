#!/usr/bin/env python3
"""Audit shell migration state with optional runtime evidence.

Static audit (default):
  - has_old_header : the OLD shell ELEMENT <header class="tp-top"> is present
  - has_frame_js   : the global /site-shell/frame.js loader is present
  - DOUBLE_SHELL   : old element AND frame.js (genuine duplicate-chrome risk)
  - mangled_h1     : <h1> looks like title+subtitle were concatenated
  - empty_subtitle : <p class="subtitle"></p> with no text

Runtime audit (--runtime):
  - white_page_risk : rendered html/body backgrounds are bright or missing
  - topbar_height   : rendered top bar height in pixels
  - topbar_size     : normal / big / missing

Element detection is regex-on-markup, NOT a substring match, so leftover CSS
rules like `.tp-top{...}` inside <style> do NOT count as the element.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


OLD_HEADER = re.compile(r'<header[^>]*class="[^"]*\btp-top\b', re.I)
OLD_CLASS = re.compile(r'<(?:div|section|nav)[^>]*class="[^"]*\btp-class\b', re.I)
FRAME_JS = re.compile(r'site-shell/frame\.js', re.I)
H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
SUB_EMPTY = re.compile(r'<p[^>]*class="[^"]*\bsubtitle\b[^"]*"[^>]*>\s*</p>', re.I)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default="one-page-stories")
    parser.add_argument("--runtime", action="store_true", help="also open pages in Playwright and inspect rendered shell/background state")
    parser.add_argument("--base-url", default="http://127.0.0.1:8792", help="base URL used for runtime page loads")
    parser.add_argument("--limit", type=int, default=None, help="only runtime-check the first N html files after sorting")
    parser.add_argument("--viewport-width", type=int, default=1440)
    parser.add_argument("--viewport-height", type=int, default=900)
    parser.add_argument("--timeout-ms", type=int, default=12000)
    return parser.parse_args()


def text(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def title_stem(t: str) -> str:
    # strip trailing " - Faith Through Physics", " | Theophysics", etc.
    return re.split(r"\s*[-|–—]\s*", t.strip())[0].strip()


def is_mangled(h1: str, ttl: str) -> bool:
    if not h1:
        return False
    stem = title_stem(ttl)
    if not stem or len(stem) < 4:
        return False
    if not h1.startswith(stem):
        return False
    rest = h1[len(stem):]
    # title immediately followed by more text with no separator => merged
    return len(rest) > 5 and (rest[0].isupper() or rest[0].islower())


def classify_topbar(height: float | None, width: int) -> str:
    if height is None or height <= 0:
        return "missing"
    # frame.js currently expects roughly 150 desktop / 190 tablet / 230 mobile
    if width <= 720:
        return "big" if height > 255 else "normal"
    if width <= 1100:
        return "big" if height > 215 else "normal"
    return "big" if height > 175 else "normal"


def luminance_from_css_rgb(css_value: str | None) -> float | None:
    if not css_value:
        return None
    m = re.search(r"rgba?\(([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)", css_value)
    if not m:
        return None
    r, g, b = (float(m.group(i)) for i in range(1, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def runtime_probe(rows: list[dict], root: Path, args: argparse.Namespace) -> None:
    subset = rows[: args.limit] if args.limit else rows
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.viewport_width, "height": args.viewport_height})
        for row in subset:
            rel = row["file"].relative_to(root).as_posix()
            url = f"{args.base_url.rstrip('/')}/{quote(rel)}"
            row["runtime_url"] = url
            try:
                page.goto(url, wait_until="networkidle", timeout=args.timeout_ms)
                probe = page.evaluate(
                    """
                    () => {
                      const htmlStyle = getComputedStyle(document.documentElement);
                      const bodyStyle = getComputedStyle(document.body);
                      const topbar = document.querySelector('#siteShellTopbar, .site-shell-topbar');
                      const dock = document.querySelector('#siteShellDock, .site-shell-dock');
                      return {
                        title: document.title,
                        htmlBg: htmlStyle.backgroundColor,
                        bodyBg: bodyStyle.backgroundColor,
                        bodyColor: bodyStyle.color,
                        topbarHeight: topbar ? topbar.getBoundingClientRect().height : 0,
                        dockHeight: dock ? dock.getBoundingClientRect().height : 0,
                        topbarExists: !!topbar,
                        dockExists: !!dock,
                      };
                    }
                    """
                )
                html_lum = luminance_from_css_rgb(probe.get("htmlBg"))
                body_lum = luminance_from_css_rgb(probe.get("bodyBg"))
                white_risk = False
                if html_lum is not None and body_lum is not None:
                    white_risk = html_lum > 220 and body_lum > 220
                row.update(
                    {
                        "runtime_ok": True,
                        "render_title": probe.get("title", ""),
                        "html_bg": probe.get("htmlBg"),
                        "body_bg": probe.get("bodyBg"),
                        "body_color": probe.get("bodyColor"),
                        "white_page_risk": white_risk,
                        "topbar_exists": bool(probe.get("topbarExists")),
                        "dock_exists": bool(probe.get("dockExists")),
                        "topbar_height": round(float(probe.get("topbarHeight", 0)), 1),
                        "dock_height": round(float(probe.get("dockHeight", 0)), 1),
                        "topbar_size": classify_topbar(float(probe.get("topbarHeight", 0)), args.viewport_width),
                    }
                )
            except PlaywrightTimeoutError:
                row.update(
                    {
                        "runtime_ok": False,
                        "runtime_error": f"timeout>{args.timeout_ms}ms",
                        "white_page_risk": None,
                        "topbar_exists": None,
                        "dock_exists": None,
                        "topbar_height": None,
                        "dock_height": None,
                        "topbar_size": "unknown",
                    }
                )
            except Exception as exc:  # noqa: BLE001
                row.update(
                    {
                        "runtime_ok": False,
                        "runtime_error": f"{type(exc).__name__}: {exc}",
                        "white_page_risk": None,
                        "topbar_exists": None,
                        "dock_exists": None,
                        "topbar_height": None,
                        "dock_height": None,
                        "topbar_size": "unknown",
                    }
                )
        browser.close()


def show(rows: list[dict], root: Path, label: str, pred) -> list[dict]:
    hits = [r for r in rows if pred(r)]
    print(f"\n=== {label}: {len(hits)} ===")
    for r in hits:
        rel = r["file"].relative_to(root)
        extra_parts = []
        if r.get("mangled_h1"):
            extra_parts.append(f"h1={r['h1'][:80]!r}")
        if "topbar_height" in r and r.get("topbar_height") is not None:
            extra_parts.append(f"topbar={r['topbar_height']}px/{r.get('topbar_size')}")
        if "body_bg" in r and r.get("body_bg"):
            extra_parts.append(f"body_bg={r['body_bg']}")
        if r.get("runtime_error"):
            extra_parts.append(f"runtime_error={r['runtime_error']}")
        extra = ("  " + " | ".join(extra_parts)) if extra_parts else ""
        print(f"  {rel}{extra}")
    return hits


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    if not root.exists():
        print(f"Root does not exist: {root}", file=sys.stderr)
        return 1

    rows: list[dict] = []
    for f in sorted(root.rglob("*.html")):
        raw = f.read_text(encoding="utf-8", errors="ignore")
        h1m = H1.search(raw)
        ttlm = TITLE.search(raw)
        h1 = text(h1m.group(1)) if h1m else ""
        ttl = text(ttlm.group(1)) if ttlm else ""
        has_header = bool(OLD_HEADER.search(raw))
        has_frame = bool(FRAME_JS.search(raw))
        rows.append(
            {
                "file": f,
                "old_header": has_header,
                "old_class": bool(OLD_CLASS.search(raw)),
                "frame_js": has_frame,
                "double": has_header and has_frame,
                "mangled_h1": is_mangled(h1, ttl),
                "empty_sub": bool(SUB_EMPTY.search(raw)),
                "h1": h1,
            }
        )

    if args.runtime:
        runtime_probe(rows, root, args)

    print(f"Scanned {len(rows)} html files under {root}")
    if args.runtime:
        print(
            f"Runtime mode: {args.base_url} @ {args.viewport_width}x{args.viewport_height}"
            + (f" (limit {args.limit})" if args.limit else "")
        )

    show(rows, root, "DOUBLE_SHELL (old element + frame.js)", lambda r: r["double"])
    show(rows, root, "Old element present, NOT migrated (no frame.js)", lambda r: r["old_header"] and not r["frame_js"])
    show(rows, root, "Framed pages with MANGLED h1", lambda r: r["frame_js"] and r["mangled_h1"])

    if args.runtime:
        show(rows, root, "WHITE_PAGE_RISK", lambda r: r.get("white_page_risk") is True)
        show(rows, root, "TOPBAR_BIG", lambda r: r.get("topbar_size") == "big")
        show(rows, root, "TOPBAR_MISSING", lambda r: r.get("topbar_size") == "missing")
        show(rows, root, "RUNTIME_LOAD_ERRORS", lambda r: not r.get("runtime_ok", True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
