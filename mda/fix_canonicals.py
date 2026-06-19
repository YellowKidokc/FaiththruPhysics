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
# Regex to find a <head> tag so we can insert a canonical if one is missing
head_re = re.compile(r'(<head[^>]*>)', re.IGNORECASE)

changed = 0
unchanged = 0
added = 0
errored = 0

for html_file in sorted(MDA_DIR.rglob("*.html")):
    try:
        # Read with errors='replace' to handle mixed encodings/line endings
        content = html_file.read_text(encoding="utf-8", errors="replace")

        # Compute expected canonical based on actual relative path
        rel_path = html_file.relative_to(MDA_DIR.parent).as_posix()
        # Directory indexes should canonicalize to the directory URL, not /index.html
        if rel_path.endswith("/index.html"):
            dir_path = rel_path[:-len("/index.html")]
            expected_canonical = f"{BASE_URL}/{dir_path}/"
        else:
            expected_canonical = f"{BASE_URL}/{rel_path}"

        # Find existing canonical
        match = canonical_re.search(content)
        if not match:
            head_match = head_re.search(content)
            if not head_match:
                print(f"NO HEAD TAG: {rel_path}")
                errored += 1
                continue
            new_content = head_re.sub(
                rf'\1\n<link rel="canonical" href="{expected_canonical}"/>',
                content,
                count=1
            )
            html_file.write_text(new_content, encoding="utf-8")
            added += 1
            print(f"ADDED: {rel_path}")
            print(f"   CANONICAL: {expected_canonical}")
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
print(f"Added:     {added}")
print(f"Unchanged: {unchanged}")
print(f"Errors:    {errored}")
print("="*60)
