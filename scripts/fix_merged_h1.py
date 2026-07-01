#!/usr/bin/env python3
"""Split title+subtitle that were merged into a single <h1>.

Root cause: the shell pass concatenated the page title and its subtitle into
the <h1>, leaving <p class="subtitle"> empty. The clean title still lives in
the <title> tag, so we split <h1> at the title-stem boundary and move the
remainder into the empty subtitle paragraph.

Only acts when ALL of these hold (conservative, reversible via git):
  - <h1> inner is plain text (no nested tags)
  - inner starts with the <title> stem and has extra trailing text
  - the next <p class="subtitle"> after the <h1> is empty
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("one-page-stories")
DRY = "--apply" not in sys.argv

H1   = re.compile(r'(<h1[^>]*>)(.*?)(</h1>)', re.I | re.S)
TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
SUB  = re.compile(r'(<p[^>]*class="[^"]*\bsubtitle\b[^"]*"[^>]*>)(\s*)(</p>)', re.I)

def title_stem(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    # Only the title/site separator has whitespace around it; internal hyphens
    # (e.g. "93-Year", "Anti-Properties") must NOT split the title.
    return re.split(r"\s+[-|\u2013\u2014]\s+", t)[0].strip()

changed, skipped = [], []
for f in sorted(ROOT.rglob("*.html")):
    # Read as UTF-8 (correct stem parsing for em-dash separators); fall back to
    # latin-1 only for genuinely non-UTF-8 files. Write back in the SAME encoding
    # so untouched bytes are preserved exactly and our ASCII inserts are safe.
    data = f.read_bytes()
    try:
        raw = data.decode("utf-8"); enc = "utf-8"
    except UnicodeDecodeError:
        raw = data.decode("latin-1"); enc = "latin-1"
    tm, hm = TITLE.search(raw), H1.search(raw)
    if not tm or not hm:
        continue
    stem = title_stem(tm.group(1))
    inner_raw = hm.group(2)
    if "<" in inner_raw:           # nested markup in h1 -> skip
        continue
    inner = inner_raw.strip()
    if len(stem) < 4 or not inner.startswith(stem) or len(inner) <= len(stem) + 1:
        continue
    rest = inner[len(stem):].strip()
    if not rest:
        continue
    sub_m = SUB.search(raw, hm.end())
    if not sub_m:
        skipped.append((f, "no empty subtitle after h1"))
        continue

    new_h1 = hm.group(1) + stem + hm.group(3)
    new_sub = sub_m.group(1) + rest + sub_m.group(3)
    new_raw = raw[:hm.start()] + new_h1 + raw[hm.end():sub_m.start()] + new_sub + raw[sub_m.end():]
    changed.append((f, stem, rest))
    if not DRY:
        f.write_text(new_raw, encoding=enc)

mode = "DRY-RUN (use --apply to write)" if DRY else "APPLIED"
print(f"[{mode}] {len(changed)} files to fix, {len(skipped)} skipped\n")
for f, stem, rest in changed:
    print(f"  {f.relative_to(ROOT)}")
    print(f"      h1  -> {stem!r}")
    print(f"      sub -> {rest[:70]!r}")
for f, why in skipped:
    print(f"  SKIP {f.relative_to(ROOT)} ({why})")
