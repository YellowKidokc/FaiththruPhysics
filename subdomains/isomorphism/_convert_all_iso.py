#!/usr/bin/env python3
"""
_convert_all_iso.py — Batch-convert all isomorphism pages to registry theme.

Usage:
    python _convert_all_iso.py          # Preview (dry run)
    python _convert_all_iso.py --apply  # Actually convert
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ISO_DIR = Path(r"\\dlowenas\HPWorkstation\Desktop\Master HTMl\_____ KIMI WORKFLOW\subdomains\ISO")
THEME_CSS = "iso-registry-theme.css"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    parser.add_argument("--test", help="Test on one file, e.g. iso-038")
    return parser.parse_args()


def extract_title(html: str) -> str:
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    return m.group(1).strip() if m else "Isomorphism Record"


def extract_meta_description(html: str) -> str:
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', html, re.IGNORECASE)
    return m.group(1) if m else ""


def extract_body_content(html: str) -> str:
    """Extract content from body, stripping nav/header/footer if present."""
    # Try to find the main content area
    for pattern in [
        r'<main[^>]*>(.*?)</main>',
        r'<article[^>]*>(.*?)</article>',
        r'<div[^>]*class=["\'][^"\']*content[^"\']*["\'][^>]*>(.*?)</div>',
    ]:
        m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
    
    # Fallback: everything inside <body>
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if m:
        body = m.group(1)
        # Strip nav/header/footer/script/style
        for tag in ['nav', 'header', 'footer', 'script', 'style']:
            body = re.sub(rf'<{tag}[^>]*>.*?</{tag}>', '', body, flags=re.DOTALL | re.IGNORECASE)
        return body.strip()
    
    return html


def build_registry_shell(title: str, description: str, body_content: str, filename: str) -> str:
    """Wrap content in the registry theme shell."""
    # Derive ID and name from filename
    stem = Path(filename).stem
    iso_id = stem.split('_')[0].upper() if '_' in stem else "ISO-???"
    iso_name = ' '.join(stem.split('_')[1:]).replace('-', ' ').title() if '_' in stem else "Unknown"
    
    # Try to extract a subtitle/claim from the first <p> or heading
    subtitle_match = re.search(r'<p[^>]*class=["\']subtitle["\'][^>]*>(.*?)</p>', body_content, re.DOTALL | re.IGNORECASE)
    subtitle = subtitle_match.group(1) if subtitle_match else f"Structural isomorphism record for {iso_name}"
    subtitle = re.sub(r'<[^>]+>', '', subtitle)  # strip tags
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Theophysics Registry</title>
<meta name="description" content="{description or title}">
<link rel="stylesheet" href="{THEME_CSS}">
</head>
<body>
<div class="ambient-glow"></div>

<div class="iso-container">

  <!-- Registry Header -->
  <header class="registry-header">
    <div class="header-top">
      <div class="registry-brand">
        <div class="registry-logo">Φ</div>
        <div>
          <div class="registry-title">Theophysics Registry</div>
          <div class="registry-subtitle">{title}</div>
        </div>
      </div>
      <div class="header-meta">
        <div class="meta-row">
          <span class="meta-label">Classification</span>
          <span class="status-badge status-candidate">
            <span class="status-dot"></span>
            Candidate Isomorphism
          </span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Record</span>
          <span class="meta-value">{iso_id}</span>
        </div>
      </div>
    </div>
    <nav class="breadcrumb">
      <a href="/">Registry Home</a>
      <span class="breadcrumb-sep">›</span>
      <a href="/isomorphisms">Isomorphisms</a>
      <span class="breadcrumb-sep">›</span>
      <span class="breadcrumb-current">{iso_id}</span>
    </nav>
  </header>

  <!-- Hero Banner -->
  <div class="hero-banner">
    <div class="hero-grid">
      <div class="hero-left">
        <div class="iso-badge">
          <span class="icon">⚛</span>
          <span>{iso_id} — Isomorphism Record</span>
        </div>
        <h1 class="hero-title">{iso_name}</h1>
        <p class="hero-subtitle">{subtitle}</p>
      </div>
      <div class="hero-right">
        <div class="equation-card">
          <div class="eq-label">Isomorphic Domain</div>
          <div class="equation">
            {iso_name.replace(' ', ' <span class="op">↔</span> ')}
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Content -->
  <main>
{body_content}
  </main>

  <!-- Footer -->
  <footer class="registry-footer">
    <div class="footer-brand">Theophysics Registry</div>
    <div class="footer-meta">Isomorphism Classification System v2.1</div>
  </footer>

</div>
</body>
</html>
'''


def convert_file(filepath: Path, apply: bool) -> dict:
    html = filepath.read_text(encoding='utf-8', errors='replace')
    
    # Skip if already converted (has registry-header)
    if 'registry-header' in html:
        return {'file': filepath.name, 'status': 'already-converted'}
    
    title = extract_title(html)
    description = extract_meta_description(html)
    body = extract_body_content(html)
    
    new_html = build_registry_shell(title, description, body, filepath.name)
    
    if apply:
        # Backup
        backup = filepath.with_suffix('.html.bak')
        filepath.rename(backup)
        filepath.write_text(new_html, encoding='utf-8')
        return {'file': filepath.name, 'status': 'converted', 'backup': backup.name}
    else:
        # Preview
        return {'file': filepath.name, 'status': 'preview', 'title': title}


def main():
    args = parse_args()
    
    if args.test:
        files = list(ISO_DIR.glob(f"{args.test}*.html"))
    else:
        files = sorted(ISO_DIR.glob("iso-*.html"))
    
    print(f"{'[DRY RUN] ' if not args.apply else ''}Converting {len(files)} isomorphism pages...")
    print()
    
    for f in files:
        result = convert_file(f, args.apply)
        status = result['status']
        tag = '[OK]' if status == 'converted' else '[DRY]' if status == 'preview' else '[SKIP]'
        print(f"  {tag} {result['file']} — {status}")
    
    print()
    if not args.apply:
        print("Add --apply to actually convert.")
    else:
        print("Done. Backups saved as .html.bak")


if __name__ == '__main__':
    main()
