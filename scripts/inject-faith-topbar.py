#!/usr/bin/env python3
"""
Inject the shared Faith Thru Physics topbar dependency into HTML pages.

Usage:
  python scripts/inject-faith-topbar.py D:\\GitHub\\faiththruphysics-site
  python scripts/inject-faith-topbar.py D:\\GitHub\\faiththruphysics-site --dry-run
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EXCLUDE_DIRS = {
    ".git",
    ".wrangler",
    "node_modules",
    "__pycache__",
    "_link-fix-backups",
    "_inject_backups",
    "_inject_preview",
    "backups",
    "reports",
    "work",
}

INJECT_BLOCK = """\
<link rel="stylesheet" href="/assets/faith-topbar.css">
<script defer src="/assets/faith-topbar.js"></script>
"""

HAS_TOPBAR = re.compile(r"faith-topbar\.(?:css|js)", re.IGNORECASE)
HEAD_CLOSE = re.compile(r"</head>", re.IGNORECASE)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return any(part in EXCLUDE_DIRS for part in rel.parts)


def print_safe(message: str) -> None:
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "backslashreplace").decode("ascii"))


def inject(text: str) -> tuple[str, str]:
    if HAS_TOPBAR.search(text):
        return text, "skip: already has topbar"

    if not HEAD_CLOSE.search(text):
        return text, "skip: no </head>"

    updated = HEAD_CLOSE.sub(INJECT_BLOCK + "\n</head>", text, count=1)
    return updated, "fixed"


def main() -> int:
    if len(sys.argv) < 2:
      print(__doc__)
      return 1

    root = Path(sys.argv[1]).resolve()
    dry_run = "--dry-run" in sys.argv

    if not root.exists():
        print(f"Root does not exist: {root}")
        return 1

    fixed = 0
    skipped = 0

    for path in sorted(root.rglob("*.html")):
        if should_skip(path, root):
            continue

        original = read_text(path)
        updated, status = inject(original)
        rel = path.relative_to(root)

        if status == "fixed":
            fixed += 1
            if dry_run:
                print_safe(f"DRY   {rel}")
            else:
                write_text(path, updated)
                print_safe(f"FIXED {rel}")
        else:
            skipped += 1
            print_safe(f"SKIP  {rel}  ({status})")

    print(f"\nDone. Fixed: {fixed}. Skipped: {skipped}. Dry run: {dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
