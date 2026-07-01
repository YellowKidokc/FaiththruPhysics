#!/usr/bin/env python3
"""
Audit all HTML pages under the site for:
  1. White/blank pages (body is empty or near-empty)
  2. Missing top-bar / bottom-dock shell injection
  3. Missing page metadata (article-meta / page-profile)

Usage:
  python audit_shell.py > audit_report.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SITE = Path(r"D:\GitHub\faiththruphysics-site")

# File patterns to skip
SKIP_DIRS = {
    "_link-fix-backup", "Archive", "CODEX_BUILD", "work", ".git", "node_modules",
    "__pycache__", "_inject_backups", "MUST DO", "Python-WEB",
}
SKIP_FILES = {"_TEMPLATE.html", "template-main.html", "template-deepdive.html"}

SHELL_MARKERS = [
    r"site-shell/frame\.js",
    r"components/tp-inject\.js",
    r"components/top-bar-bottom-bar\.css",
    r"tp-top-bar\.js",
    r"tp-bottom-bar\.js",
    r"frame\.js",
]

META_MARKERS = [
    r'id\s*=\s*"article-meta"',
    r'id\s*=\s*"page-profile"',
]

WHITE_MARKERS = [
    r'<body[^>]*>\s*</body>',
    r'<body[^>]*>\s*(?:<!--[^>]*-->)?\s*</body>',
]


def is_skip(path: Path) -> bool:
    rel = path.relative_to(SITE)
    parts = set(rel.parts)
    if parts & SKIP_DIRS:
        return True
    if path.name in SKIP_FILES:
        return True
    return False


def has_marker(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def body_is_white(text: str) -> bool:
    m = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL | re.IGNORECASE)
    if not m:
        return True
    body = m.group(1)
    visible = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)
    visible = re.sub(r"<style[^>]*>.*?</style>", "", visible, flags=re.DOTALL | re.IGNORECASE)
    visible = re.sub(r"<!--.*?-->", "", visible, flags=re.DOTALL)
    visible = re.sub(r"<[^>]+>", "", visible)
    visible = visible.strip()
    return len(visible) < 50 or len(body.strip()) < 200


def main():
    pages = []
    for html in SITE.rglob("*.html"):
        if is_skip(html):
            continue
        try:
            text = html.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            pages.append({
                "path": str(html.relative_to(SITE)),
                "error": str(e),
            })
            continue

        has_shell = has_marker(text, SHELL_MARKERS)
        has_meta = has_marker(text, META_MARKERS)
        is_white = body_is_white(text)

        if not has_shell or not has_meta or is_white:
            pages.append({
                "path": str(html.relative_to(SITE)),
                "has_shell": has_shell,
                "has_meta": has_meta,
                "is_white": is_white,
            })

    report = {
        "total_checked": len(list(SITE.rglob("*.html"))),
        "problem_count": len(pages),
        "problems": pages,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
