#!/usr/bin/env python3
"""
Inject the Faith Thru Physics topbar into every existing HTML file.

Usage from repo root:

  python tools/inject-topbar.py --dry-run
  python tools/inject-topbar.py

What it does:
- Scans all .html files.
- Skips backup/build/system folders.
- Adds the shared topbar CSS/JS before </head>.
- Does not inject twice.
- Creates a backup copy before modifying each file.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDE_DIRS = {
    ".git",
    ".github",
    ".wrangler",
    "node_modules",
    "__pycache__",
    "_link-fix-backups",
    "_inject_backups",
    "_inject_preview",
    "backups",
    "reports",
    "work",
    "dist",
    "build",
}

INJECT_BLOCK = """\
<!-- FAITH TOPBAR -->
<link rel="stylesheet" href="/assets/faith-topbar.css">
<script defer src="/assets/faith-topbar.js"></script>
<!-- /FAITH TOPBAR -->
"""

BACKUP_DIR = ROOT / "_topbar_backups"


def read_file(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def write_file(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def already_has_topbar(text: str) -> bool:
    return (
        "faith-topbar.css" in text
        or "faith-topbar.js" in text
        or "<!-- FAITH TOPBAR -->" in text
    )


def inject_topbar(text: str) -> tuple[str, str]:
    if already_has_topbar(text):
        return text, "already has topbar"

    lower = text.lower()
    head_close_index = lower.find("</head>")

    if head_close_index == -1:
        return text, "missing </head>"

    updated = text[:head_close_index] + INJECT_BLOCK + "\n" + text[head_close_index:]
    return updated, "fixed"


def backup_file(path: Path) -> None:
    relative = path.relative_to(ROOT)
    backup_path = BACKUP_DIR / relative
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    args = parser.parse_args()

    html_files = [path for path in ROOT.rglob("*.html") if not is_excluded(path)]

    fixed = 0
    skipped = 0
    missing_head = 0

    print(f"Repo root: {ROOT}")
    print(f"HTML files found: {len(html_files)}")
    print()

    for path in sorted(html_files):
        text = read_file(path)
        updated, status = inject_topbar(text)
        relative = path.relative_to(ROOT)

        if status == "fixed":
            fixed += 1

            if args.dry_run:
                print(f"DRY   {relative}")
            else:
                backup_file(path)
                write_file(path, updated)
                print(f"FIXED {relative}")

        elif status == "missing </head>":
            missing_head += 1
            print(f"SKIP  {relative}  ({status})")

        else:
            skipped += 1
            print(f"SKIP  {relative}  ({status})")

    print()
    print("Done.")
    print(f"Fixed: {fixed}")
    print(f"Already had topbar: {skipped}")
    print(f"Missing </head>: {missing_head}")

    if not args.dry_run and fixed:
        print(f"Backups saved to: {BACKUP_DIR}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
