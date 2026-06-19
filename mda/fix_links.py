#!/usr/bin/env python3
"""
Fix relative internal links between MDA HTML files.
- Bare MDA-*.html links that point to files in other folders get the correct ../folder/ path.
- Bare index.html links in subfolders are rewritten to ../index.html (MDA series home).
"""

from pathlib import Path
import re
from urllib.parse import unquote

html_dir = Path(__file__).resolve().parent

file_map = {}
for p in sorted(html_dir.rglob('*.html')):
    if p.name in file_map:
        print(f'WARNING: duplicate filename {p.name}')
    file_map[p.name] = p.parent.relative_to(html_dir).as_posix()

href_re = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

changes = []

for html_file in sorted(html_dir.rglob('*.html')):
    rel_dir = html_file.parent.relative_to(html_dir)
    content = html_file.read_text(encoding='utf-8', errors='replace')
    new_content = content

    for match in href_re.finditer(content):
        url = match.group(1)
        if url.startswith('#') or url.startswith('mailto:') or url.startswith('javascript:') or url.startswith('data:'):
            continue
        if url.startswith('http://') or url.startswith('https://') or url.startswith('//'):
            continue
        if url.startswith('/'):
            continue

        if url == 'index.html':
            if rel_dir == Path('.'):
                continue
            new_url = '../index.html'
            new_content = re.sub(r'href="index.html"', f'href="{new_url}"', new_content, count=1)
            changes.append((html_file, url, new_url))
            continue

        basename = Path(unquote(url)).name
        has_path = '/' in url or chr(92) in url
        if basename.startswith('MDA-') and basename.endswith('.html') and not has_path:
            if basename not in file_map:
                continue
            target_dir = Path(file_map[basename])
            if target_dir == rel_dir:
                continue

            current_parts = rel_dir.parts if rel_dir != Path('.') else ()
            target_parts = target_dir.parts

            common = 0
            for a, b in zip(current_parts, target_parts):
                if a == b:
                    common += 1
                else:
                    break

            up = ['..'] * (len(current_parts) - common)
            down = list(target_parts[common:])
            new_url = '/'.join(up + down + [basename])

            new_content = new_content.replace(f'href="{url}"', f'href="{new_url}"', 1)
            changes.append((html_file, url, new_url))

    if new_content != content:
        html_file.write_text(new_content, encoding='utf-8')

print(f'Total changes: {len(changes)}')
for src, old, new in changes[:30]:
    print(f'  {src}: {old} -> {new}')
if len(changes) > 30:
    print(f'  ... and {len(changes) - 30} more')
