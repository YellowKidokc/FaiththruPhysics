#!/usr/bin/env python3
"""Inject dark-theme :root + body background into HTML pages missing them.

Usage:
  python white_fix.py FILE [FILE ...]
  python white_fix.py --dry-run FILE ...

Skips files that already have <style id="theme-restore-dark">.
Skips files that already define :root and body{background:var(--bg)}.
"""
import re
import sys
from pathlib import Path

THEME_BLOCK = """<style id="theme-restore-dark">
:root{
  --bg:#050505; --surface:#0a0a0a; --surface2:#111; --surface3:#1a1a1a;
  --border:#222; --border-2:#2a2a2a; --border-hi:#3a3a3a; --border-hover:#3a3a3a;
  --text:#e5e3df; --text-dim:#9a9a9a; --text-muted:#5a5a5a; --text-primary:#e5e3df; --text-secondary:#9a9a9a;
  --gold:#d4af37; --gold-dim:rgba(212,175,55,.1); --gold-glow:rgba(212,175,55,.3); --highlight:#d4af37; --accent-gold:#d4af37;
  --red:#c94040; --red-dim:rgba(201,64,64,.1); --teal:#3bb39a; --teal-dim:rgba(59,179,154,.1);
  --blue:#5b9bd5; --blue-dim:rgba(91,155,213,.1); --purple:#a78bfa; --purple-dim:rgba(167,139,250,.1); --green:#7fc77f;
  --serif:'Crimson Text',Georgia,serif; --mono:'JetBrains Mono',ui-monospace,monospace;
  --display:'Oswald','Inter',sans-serif; --sans:'Inter',system-ui,sans-serif;
  --max:1180px; --header-h:48px;
}
html{background:var(--bg)}
body{background:var(--bg);color:var(--text);font-family:var(--sans)}
</style>
"""

ROOT_DEF = re.compile(r":root\s*\{", re.I)
BODY_BG = re.compile(r"body\s*\{[^}]*background\s*:\s*var\(--bg\)", re.I)
RESTORE_TAG = re.compile(r'<style\s+id="theme-restore-dark"', re.I)


def read(p):
    b = p.read_bytes()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1")


def write(p, text):
    p.write_text(text, encoding="utf-8", newline="\n")


def needs_fix(text):
    if RESTORE_TAG.search(text):
        return False, "already has theme-restore-dark"
    has_root = bool(ROOT_DEF.search(text))
    has_body = bool(BODY_BG.search(text))
    if has_root and has_body:
        return False, "already has :root + body{background:var(--bg)}"
    if "</head>" not in text.lower():
        return False, "no </head> tag"
    return True, "missing theme"


def fix(text):
    return re.sub(r"</head>", THEME_BLOCK + "</head>", text, count=1, flags=re.I)


def main():
    args = sys.argv[1:]
    dry = False
    if args and args[0] == "--dry-run":
        dry = True
        args = args[1:]
    if not args:
        print("Usage: white_fix.py [--dry-run] FILE [FILE ...]")
        sys.exit(1)

    fixed = skipped = 0
    for raw in args:
        p = Path(raw)
        if not p.is_file():
            print(f"SKIP  {raw}  (not found)")
            skipped += 1
            continue
        text = read(p)
        do_fix, reason = needs_fix(text)
        if not do_fix:
            print(f"SKIP  {p}  ({reason})")
            skipped += 1
            continue
        if dry:
            print(f"DRY   {p}  (would inject theme-restore-dark)")
            fixed += 1
            continue
        write(p, fix(text))
        print(f"FIXED {p}")
        fixed += 1

    print(f"\nDone: {fixed} fixed, {skipped} skipped")


if __name__ == "__main__":
    main()
