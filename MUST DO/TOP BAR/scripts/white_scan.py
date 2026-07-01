#!/usr/bin/env python3
"""Detect HTML pages likely to render white (broken/undefined dark theme).

Usage:
  python white_scan.py [ROOT]

ROOT defaults to D:\\GitHub\\faiththruphysics-site.
A page is flagged when it uses a theme var for background without defining
:root, declares an explicit white background, or has no stylesheet at all.
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\GitHub\faiththruphysics-site")
EXCLUDE = {".git", ".wrangler", "node_modules", "__pycache__", "_link-fix-backups",
           "_inject_backups", "_inject_preview", "backups", "reports", "work"}


def read(p):
    b = p.read_bytes()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1")


VAR_USE = re.compile(r"var\(--(bg|background|surface|pane|card)\b", re.I)
ROOT_DEF = re.compile(r":root\s*\{", re.I)
WHITE_BG = re.compile(r"(?:html|body)\s*\{[^}]*background[^;}]*(?:#fff(?:fff)?|white)\b", re.I)
HAS_STYLE = re.compile(r"<style|stylesheet", re.I)

flagged = []
for p in ROOT.rglob("*.html"):
    if any(part in EXCLUDE for part in p.parts):
        continue
    t = read(p)
    reasons = []
    if VAR_USE.search(t) and not ROOT_DEF.search(t):
        reasons.append("uses theme var, no :root")
    if WHITE_BG.search(t):
        reasons.append("explicit white background")
    if not HAS_STYLE.search(t):
        reasons.append("no <style> or stylesheet")
    if reasons:
        flagged.append((str(p.relative_to(ROOT)), reasons))

print(f"Scanned root: {ROOT}")
print(f"Flagged {len(flagged)} likely-white pages:\n")
for rel, reasons in sorted(flagged):
    print(f"  {rel}\n      -> {', '.join(reasons)}")
