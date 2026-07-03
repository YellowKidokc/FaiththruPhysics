#!/usr/bin/env python3
"""Prepare HTML pages for the shared Faith Through Physics topbar.

This script adds a small, marked adapter block to each selected HTML page.
It does not install the topbar assets. Run inject_topbar.py after this.

Default mode is dry-run. Use --apply to write files.
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


STYLE_START = "<!-- FTP_TOPBAR_PREP:START -->"
STYLE_END = "<!-- FTP_TOPBAR_PREP:END -->"
CONFIG_START = "<!-- FTP_TOPBAR_CONFIG:START -->"
CONFIG_END = "<!-- FTP_TOPBAR_CONFIG:END -->"

PREP_BLOCK = f"""{STYLE_START}
<style id="ftp-topbar-page-prep">
  :root {{
    --ftp-header-h: 52px;
  }}

  html {{
    scroll-padding-top: calc(var(--ftp-header-h, 52px) + 16px);
  }}

  body.ftp-topbar-enabled {{
    padding-top: var(--ftp-header-h, 52px);
  }}

  body.ftp-topbar-enabled .tp-ribbon,
  body.ftp-topbar-enabled .site-ribbon,
  body.ftp-topbar-enabled .page-ribbon {{
    top: var(--ftp-header-h, 52px) !important;
    z-index: 2147482000 !important;
  }}

  body.ftp-topbar-enabled main,
  body.ftp-topbar-enabled .page,
  body.ftp-topbar-enabled .content,
  body.ftp-topbar-enabled article {{
    scroll-margin-top: calc(var(--ftp-header-h, 52px) + 16px);
  }}

  @media (max-width: 768px) {{
    body.ftp-topbar-enabled table {{
      max-width: 100%;
    }}

    body.ftp-topbar-enabled .dtbl {{
      display: block;
      max-width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }}

    body.ftp-topbar-enabled .dtbl th,
    body.ftp-topbar-enabled .dtbl td {{
      white-space: nowrap;
    }}
  }}
</style>
{STYLE_END}"""

CONFIG_BLOCK = f"""{CONFIG_START}
<script id="ftp-topbar-config">
  window.FTP_TOPBAR = {{
    replaceLegacyNav: false,
    compact: true,
    equationHref: "/master-equation/"
  }};
</script>
{CONFIG_END}"""

SKIP_DIRS = {
    ".git",
    ".wrangler",
    "node_modules",
    "backups",
    "reports",
    "trash_review",
    "_trash_review",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def backup_file(path: Path, root: Path) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = root / "backups" / "topbar_prep" / stamp
    destination = backup_root / path.relative_to(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    return destination


def html_files(targets: list[Path], recursive: bool) -> list[Path]:
    found: list[Path] = []
    for target in targets:
        if target.is_file() and target.suffix.lower() in {".html", ".htm"}:
            found.append(target)
            continue
        if not target.is_dir():
            continue
        pattern = "**/*.htm*" if recursive else "*.htm*"
        for path in target.glob(pattern):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() in {".html", ".htm"}:
                found.append(path)
    return sorted(set(found))


def replace_marked_block(text: str, start: str, end: str, block: str) -> tuple[str, bool]:
    start_at = text.find(start)
    end_at = text.find(end)
    if start_at >= 0 and end_at >= start_at:
        end_at += len(end)
        new_text = text[:start_at] + block + text[end_at:]
        return new_text, new_text != text
    return text, False


def insert_before_head_close(text: str, block: str) -> tuple[str, bool]:
    lower = text.lower()
    head_close = lower.find("</head>")
    if head_close < 0:
        return text, False
    insert = block.rstrip() + "\n"
    return text[:head_close] + insert + text[head_close:], True


def prepare_html(text: str) -> tuple[str, list[str]]:
    actions: list[str] = []

    text, changed = replace_marked_block(text, STYLE_START, STYLE_END, PREP_BLOCK)
    if changed:
        actions.append("updated prep CSS")
    elif STYLE_START not in text:
        text, inserted = insert_before_head_close(text, PREP_BLOCK)
        if inserted:
            actions.append("added prep CSS")

    text, changed = replace_marked_block(text, CONFIG_START, CONFIG_END, CONFIG_BLOCK)
    if changed:
        actions.append("updated config")
    elif CONFIG_START not in text:
        text, inserted = insert_before_head_close(text, CONFIG_BLOCK)
        if inserted:
            actions.append("added config")

    return text, actions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", type=Path, help="HTML files or folders to prepare")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repo root for backups")
    parser.add_argument("--recursive", action="store_true", help="Scan folders recursively")
    parser.add_argument("--apply", action="store_true", help="Write changes. Default is dry-run")
    args = parser.parse_args()

    root = args.root.resolve()
    targets = [path.resolve() for path in args.targets]
    files = html_files(targets, args.recursive)

    changed_count = 0
    skipped_count = 0
    for path in files:
        original = read_text(path)
        updated, actions = prepare_html(original)
        if not actions or updated == original:
            skipped_count += 1
            continue
        changed_count += 1
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        print(f"[CHANGE] {rel}: {', '.join(actions)}")
        if args.apply:
            backup = backup_file(path, root)
            path.write_text(updated, encoding="utf-8", newline="")
            print(f"         backup: {backup}")

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"[{mode}] scanned={len(files)} changed={changed_count} unchanged={skipped_count}")
    if not args.apply and changed_count:
        print("Run again with --apply to write these changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
