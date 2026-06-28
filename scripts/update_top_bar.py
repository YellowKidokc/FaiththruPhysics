#!/usr/bin/env python3
"""
Update the top bar in all v5-shelled pages to the latest version.

Usage:
  python scripts/update_top_bar.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / "components" / "universal-shell-v5.html"

SERIES = [
    "mda", "moral-decline", "genesis-to-quantum", "cross-domain", "blue",
    "consciousness", "convergence-series", "proof-architecture",
    "the-bidirectional-audit", "three-truths", "three-gates",
    "revolution-of-truth", "rigor", "one-page-stories"
]


def extract_top_bar(html: str):
    start = html.find("<!-- ═══════ TOP BAR ═══════ -->")
    end = html.find("</header>", start)
    if start == -1 or end == -1:
        return None
    return html[start:end + len("</header>")]


def main():
    shell_html = SHELL.read_text(encoding="utf-8")
    new_top_bar = extract_top_bar(shell_html)
    if not new_top_bar:
        raise SystemExit("Could not extract top bar from shell template")

    updated = 0
    skipped = 0
    for s in SERIES:
        series_dir = ROOT / s
        if not series_dir.exists():
            continue
        for html_path in series_dir.rglob("*.html"):
            if "components" in html_path.parts or "_link-fix-backup" in str(html_path):
                continue
            if html_path.name.lower() == "index.html":
                continue
            text = html_path.read_text(encoding="utf-8", errors="ignore")
            if "tp-top" not in text:
                skipped += 1
                continue
            old_top_bar = extract_top_bar(text)
            if not old_top_bar:
                skipped += 1
                continue
            if old_top_bar == new_top_bar:
                skipped += 1
                continue
            new_text = text.replace(old_top_bar, new_top_bar, 1)
            html_path.write_text(new_text, encoding="utf-8")
            updated += 1

    print(f"Updated {updated} pages")
    print(f"Skipped {skipped} pages")


if __name__ == "__main__":
    main()
