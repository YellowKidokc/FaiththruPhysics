#!/usr/bin/env python3
"""
Fix canonical URL mismatches across MDA HTML files.
Sets canonical to match actual file path under https://faiththruphysics.com/mda/
"""

import os
import re
from pathlib import Path

BASE_URL = "https://faiththruphysics.com"
MDA_DIR = Path("D:/GitHub/faiththruphysics-site/mda")

# Regex to find <link rel="canonical" href="...">
canonical_re = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']\s*/?>',
    re.IGNORECASE
)

changed = 0
unchanged = 0
errored = 0

for html_file in sorted(MDA_DIR.rglob("*.html")):
    try:
        # Read with errors='replace' to handle mixed encodings/line endings
        content = html_file.read_text(encoding="utf-8", errors="replace")
        
        # Compute expected canonical based on actual relative path
        rel_path = html_file.relative_to(MDA_DIR.parent).as_posix()
        expected_canonical = f"{BASE_URL}/{rel_path}"
        
        # Find existing canonical
        match = canonical_re.search(content)
        if not match:
            print(f"NO CANONICAL: {rel_path}")
            continue
        
        existing = match.group(1)
        
        if existing == expected_canonical:
            unchanged += 1
            continue
        
        # Replace
        new_content = canonical_re.sub(
            f'<link rel="canonical" href="{expected_canonical}"/>',
            content,
            count=1
        )
        
        html_file.write_text(new_content, encoding="utf-8")
        changed += 1
        print(f"FIXED: {rel_path}")
        print(f"   FROM: {existing}")
        print(f"   TO:   {expected_canonical}")
    except Exception as e:
        errored += 1
        print(f"ERROR: {html_file} — {e}")

print("\n" + "="*60)
print(f"Changed:   {changed}")
print(f"Unchanged: {unchanged}")
print(f"Errors:    {errored}")
print("="*60)
