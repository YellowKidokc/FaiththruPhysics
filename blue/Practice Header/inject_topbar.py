#!/usr/bin/env python3
"""Inject shared topbar CSS/JS includes into selected HTML pages.

Run prepare_topbar_pages.py first when a page needs physical spacing or
legacy-ribbon stacking. This injector only adds the asset includes.

Default mode is dry-run. Use --apply to write files.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


INJECT_START = "<!-- FTP_TOPBAR_ASSETS:START -->"
INJECT_END = "<!-- FTP_TOPBAR_ASSETS:END -->"
ASSET_BLOCK = f"""{INJECT_START}
<link rel="stylesheet" href="/assets/faith-topbar.css">
<script defer src="/assets/faith-topbar.js"></script>
{INJECT_END}"""

SKIP_DIRS = {
    ".git",
    ".wrangler",
    "node_modules",
    "backups",
    "reports",
    "trash_review",
    "_trash_review",
}

ALLOWED_GLOBAL_SELECTORS = {
    ":root",
    "body.ftp-topbar-enabled",
    "body.ftp-topbar-enabled.ftp-topbar-compact",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def backup_file(path: Path, root: Path) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = root / "backups" / "topbar_inject" / stamp
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


def strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def selector_is_scoped(selector: str) -> bool:
    selector = selector.strip()
    if not selector:
        return True
    if selector.startswith("@"):
        return True
    if selector in ALLOWED_GLOBAL_SELECTORS:
        return True
    if selector.startswith(".ftp-"):
        return True
    if selector.startswith("body.ftp-topbar-enabled "):
        return True
    if selector.startswith("body.ftp-topbar-enabled."):
        return True
    return False


def check_css_scope(css_path: Path) -> list[str]:
    css = strip_css_comments(read_text(css_path))
    warnings: list[str] = []
    for match in re.finditer(r"([^{}]+)\{", css):
        selector_text = match.group(1).strip()
        if selector_text.startswith("@"):
            continue
        selectors = [part.strip() for part in selector_text.split(",")]
        unsafe = [selector for selector in selectors if not selector_is_scoped(selector)]
        if unsafe:
            warnings.extend(unsafe)
    return warnings


def remove_old_unmarked_assets(text: str) -> str:
    text = re.sub(
        r'\s*<link\s+rel=["\']stylesheet["\']\s+href=["\']/assets/faith-topbar\.css["\']\s*/?>',
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\s*<script\s+defer\s+src=["\']/assets/faith-topbar\.js["\']\s*>\s*</script>',
        "",
        text,
        flags=re.I,
    )
    return text


def replace_marked_block(text: str) -> tuple[str, bool]:
    start_at = text.find(INJECT_START)
    end_at = text.find(INJECT_END)
    if start_at >= 0 and end_at >= start_at:
        end_at += len(INJECT_END)
        new_text = text[:start_at] + ASSET_BLOCK + text[end_at:]
        return new_text, new_text != text
    return text, False


def insert_before_head_close(text: str) -> tuple[str, bool]:
    lower = text.lower()
    head_close = lower.find("</head>")
    if head_close < 0:
        return text, False
    insert = ASSET_BLOCK.rstrip() + "\n"
    return text[:head_close] + insert + text[head_close:], True


def inject_assets(text: str) -> tuple[str, list[str]]:
    actions: list[str] = []
    text, changed = replace_marked_block(text)
    if changed:
        actions.append("updated topbar asset block")
        return text, actions
    if INJECT_START in text:
        return text, actions

    cleaned = remove_old_unmarked_assets(text)
    if cleaned != text:
        actions.append("normalized existing topbar includes")
    text, inserted = insert_before_head_close(cleaned)
    if inserted:
        actions.append("added topbar asset block")
    return text, actions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", type=Path, help="HTML files or folders to inject")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repo root for backups")
    parser.add_argument("--recursive", action="store_true", help="Scan folders recursively")
    parser.add_argument("--apply", action="store_true", help="Write changes. Default is dry-run")
    parser.add_argument(
        "--skip-css-scope-check",
        action="store_true",
        help="Do not check faith-topbar.css for unsafe broad selectors",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    css_path = root / "assets" / "faith-topbar.css"
    js_path = root / "assets" / "faith-topbar.js"
    missing = [path for path in (css_path, js_path) if not path.exists()]
    if missing:
        for path in missing:
            print(f"[ERROR] Missing asset: {path}")
        return 2

    if not args.skip_css_scope_check:
        warnings = check_css_scope(css_path)
        if warnings:
            print("[ERROR] Topbar CSS contains unscoped selectors:")
            for selector in warnings[:40]:
                print(f"  - {selector}")
            if len(warnings) > 40:
                print(f"  ... {len(warnings) - 40} more")
            print("Fix CSS scoping or rerun with --skip-css-scope-check.")
            return 3

    targets = [path.resolve() for path in args.targets]
    files = html_files(targets, args.recursive)
    changed_count = 0
    skipped_count = 0
    for path in files:
        original = read_text(path)
        updated, actions = inject_assets(original)
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
