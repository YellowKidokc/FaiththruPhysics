#!/usr/bin/env python3
"""
header_fix.py — Strip old headers, inject canonical tp-inject.js
POF 2828 | July 2026

Usage:
    python header_fix.py page.html              # fix one file
    python header_fix.py ./genesis-to-quantum/   # fix a folder
    python header_fix.py ./genesis-to-quantum/ --dry-run  # preview only
"""

import re, sys, os, glob, argparse
from pathlib import Path

# The canonical injection line
INJECT_LINE = '<script src="/components/tp-inject.js"></script>'

# The canonical CSS links needed
CANONICAL_CSS = [
    '<link rel="stylesheet" href="/components/tp-theme.css"/>',
]


# Patterns that indicate OLD/broken headers to remove
OLD_HEADER_PATTERNS = [
    # Old inline nav bars
    r'<nav[^>]*class="[^"]*(?:old-nav|site-nav|main-nav)[^"]*"[^>]*>.*?</nav>',
    # Old header blocks with white backgrounds
    r'<header[^>]*style="[^"]*background:\s*(?:#fff|#ffffff|white)[^"]*"[^>]*>.*?</header>',
    # Old standalone CSS link patterns that conflict
    r'<link[^>]*href="[^"]*(?:old-header|legacy-nav|white-header)[^"]*"[^>]*/?>', 
]

# Pattern to detect if tp-inject.js is already present
INJECT_PRESENT = re.compile(r'tp-inject\.js', re.IGNORECASE)

# Pattern to detect if tp-theme.css is already present
THEME_PRESENT = re.compile(r'tp-theme\.css', re.IGNORECASE)


def fix_page(filepath, dry_run=False):
    """Fix a single HTML page."""
    path = Path(filepath)
    if not path.exists() or path.suffix.lower() not in ('.html', '.htm'):
        return None

    original = path.read_text(encoding='utf-8', errors='replace')
    html = original
    changes = []

    # 1. Check and remove old header patterns
    for pattern in OLD_HEADER_PATTERNS:
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        if matches:
            html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
            changes.append(f"  REMOVED: old header pattern ({len(matches)} match(es))")

    # 2. Check if tp-theme.css is present in <head>
    if not THEME_PRESENT.search(html):
        # Insert theme CSS before </head>
        if '</head>' in html:
            css_block = '\n'.join(CANONICAL_CSS)
            html = html.replace('</head>', f'{css_block}\n</head>')
            changes.append(f"  ADDED: tp-theme.css to <head>")
        else:
            changes.append(f"  WARNING: no </head> found — cannot inject CSS")

    # 3. Check if tp-inject.js is present
    if not INJECT_PRESENT.search(html):
        # Insert before </body>
        if '</body>' in html:
            html = html.replace('</body>', f'{INJECT_LINE}\n</body>')
            changes.append(f"  ADDED: tp-inject.js before </body>")
        else:
            changes.append(f"  WARNING: no </body> found — cannot inject script")

    # 4. Fix white/light backgrounds on body
    white_bg = re.search(
        r'(<body[^>]*style="[^"]*)(background:\s*(?:#fff|#ffffff|white|rgb\(255))',
        html, re.IGNORECASE
    )
    if white_bg:
        html = re.sub(
            r'(background:\s*(?:#fff|#ffffff|white|rgb\(255[^)]*\)))',
            'background:#0a0b0f',
            html,
            flags=re.IGNORECASE
        )
        changes.append(f"  FIXED: white body background → #0a0b0f")

    # 5. Write if changed
    if changes and not dry_run:
        # Backup original
        backup = path.with_suffix('.html.pre-headerfix.bak')
        if not backup.exists():
            backup.write_text(original, encoding='utf-8')
        path.write_text(html, encoding='utf-8')

    return changes if changes else None


def main():
    parser = argparse.ArgumentParser(description="Fix article headers — strip old, inject canonical")
    parser.add_argument("target", help="HTML file or folder to fix")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--recursive", "-r", action="store_true", help="Process subfolders")
    args = parser.parse_args()

    target = Path(args.target)

    if target.is_file():
        files = [target]
    elif target.is_dir():
        pattern = '**/*.html' if args.recursive else '*.html'
        files = sorted(target.glob(pattern))
    else:
        print(f"ERROR: {target} not found")
        sys.exit(1)

    # Filter out backup files
    files = [f for f in files if '.bak' not in f.name and '.pre-' not in f.name]

    print(f"\n{'='*60}")
    print(f"  HEADER FIX {'(DRY RUN)' if args.dry_run else ''}")
    print(f"  Target: {target}")
    print(f"  Files: {len(files)}")
    print(f"{'='*60}\n")

    fixed = 0
    skipped = 0
    errors = 0

    for f in files:
        try:
            changes = fix_page(f, dry_run=args.dry_run)
            if changes:
                fixed += 1
                status = "WOULD FIX" if args.dry_run else "FIXED"
                print(f"[{status}] {f.name}")
                for c in changes:
                    print(c)
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"[ERROR] {f.name}: {e}")

    print(f"\n{'='*60}")
    print(f"  Results: {fixed} fixed, {skipped} already OK, {errors} errors")
    if args.dry_run:
        print(f"  (Dry run — no files were modified)")
    else:
        print(f"  (Backups saved as .pre-headerfix.bak)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
