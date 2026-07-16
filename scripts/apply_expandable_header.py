#!/usr/bin/env python3
"""
Apply the canonical expandable header (ftp-top + Verification & Proof panel)
throughout the site.

Source of truth:
  site-shell/expandable-header.html  — Layer 1 topbar + Layer 2 expandable panel
  site-shell/shell.css               — styles extracted from ftp-shell-v2.5.1
  site-shell/shell.js                — runtime (togglePanel, tabs, shell-data)

This matches the expandable header pattern from:
  Python-WEB/topbar/canonical-page-shell/ (ftp-panel-toggle / ftpPanel)

Usage:
  python scripts/apply_expandable_header.py --path revolution-of-truth
  python scripts/apply_expandable_header.py --path revolution-of-truth --apply
  python scripts/apply_expandable_header.py --path . --apply
  python scripts/apply_expandable_header.py --file revolution-of-truth/drv-00-the-argument.html --apply

Safety:
  - Dry-run by default
  - Idempotent: skips pages that already have id="ftpPanelToggle"
  - Does not rewrite article prose
  - Writes .bak-ftp-header beside each changed file (unless --no-backup)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL_DIR = ROOT / "site-shell"
HEADER_FILE = SHELL_DIR / "expandable-header.html"
CSS_FILE = SHELL_DIR / "shell.css"
JS_FILE = SHELL_DIR / "shell.js"

MARKER = 'id="ftpPanelToggle"'
SHELL_DATA_RE = re.compile(
    r'\s*<script[^>]*id=["\']shell-data["\'][^>]*>.*?</script>\s*',
    re.I | re.S,
)
TP_TOP_RE = re.compile(r'\s*<header class="tp-top"[^>]*>[\s\S]*?</header>\s*', re.I)
TP_CLASS_RE = re.compile(
    r'\s*<!--[^\n]*CLASSIFICATION[^\n]*-->\s*<div class="tp-class"[^>]*>[\s\S]*?</div>\s*',
    re.I,
)
TP_LIP_RE = re.compile(
    r'\s*<div class="tp-header-lip"[^>]*>[\s\S]*?</div>\s*',
    re.I,
)
BODY_OPEN_RE = re.compile(r"<body([^>]*)>", re.I)
FA_RE = re.compile(r"font-awesome|fontawesome", re.I)

EXCLUDE_DIRS = {
    ".git", "site-shell", "prototypes", "workers", ".wrangler",
    "node_modules", "__pycache__", ".venv", "venv",
    "_archive", "backups", "MUST DO", "components",
    "reports", "docs", "work", "CODEX_BUILD", "subdomains",
    "production-vault", "_link-fix-backups", "Kimi_Agent_ONEPAGE_GLOWINGBALL",
}

SERIES_LABELS = {
    "revolution-of-truth": ("DRV", "Revolution of Truth", "/revolution-of-truth/"),
    "genesis-to-quantum": ("GTQ", "Genesis to Quantum", "/genesis-to-quantum/"),
    "moral-decline": ("MDA", "Moral Decline of America", "/moral-decline/"),
    "mda": ("MDA", "Moral Decline of America", "/moral-decline/"),
    "consciousness": ("CON", "Consciousness", "/consciousness/"),
    "convergence-series": ("CNV", "Convergence", "/convergence-series/"),
    "cross-domain": ("XD", "Cross-Domain", "/cross-domain/"),
    "one-page-stories": ("OPS", "One-Page Stories", "/one-page-stories/"),
    "blue": ("BLUE", "Logos Papers", "/blue/"),
    "three-truths": ("3T", "Three Truths", "/three-truths/"),
    "three-gates": ("3G", "Three Gates", "/three-gates/"),
    "proof-architecture": ("PA", "Proof Architecture", "/proof-architecture/"),
    "rigor": ("RIGOR", "Rigor", "/rigor/"),
}


def rel_prefix(page: Path) -> str:
    depth = len(page.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else "./"


def series_meta(page: Path) -> tuple[str, str, str]:
    parts = page.relative_to(ROOT).parts
    for part in parts:
        if part in SERIES_LABELS:
            return SERIES_LABELS[part]
    return ("FTP", "Faith thru Physics", "/")


def page_title(html: str, fallback: str) -> str:
    for pat in (r"<title[^>]*>(.*?)</title>", r"<h1[^>]*>(.*?)</h1>"):
        m = re.search(pat, html, re.I | re.S)
        if m:
            t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            t = re.sub(r"\s+", " ", t)
            if t:
                return t[:200]
    return fallback


def build_shell_data(html: str, page: Path, siblings: list[Path]) -> dict:
    code, name, home = series_meta(page)
    data = {
        "page": {
            "title": page_title(html, page.stem),
            "series": code,
            "series_name": name,
            "series_home": home,
            "slug": page.stem,
            "author": "David Lowe",
        },
        "domains": [
            {"id": "theology", "name": "Theology", "pct": 34},
            {"id": "physics", "name": "Physics", "pct": 33},
            {"id": "mathematics", "name": "Math", "pct": 33},
        ],
        "verification": {
            "chi": {"raw": None, "normalized": None, "fruits": None},
            "axioms": {"tested": None, "total": 188, "pct": None},
            "laws": [],
            "isomorphisms": {},
            "claims": {},
            "badge_text": "Verification & Proof",
        },
        "claims": [],
        "proofs": [],
        "mtl": [],
        "audio": [],
    }
    if page in siblings:
        idx = siblings.index(page)
        if idx > 0:
            prev = siblings[idx - 1]
            data["page"]["prev"] = {"title": prev.stem, "url": prev.name}
        if idx + 1 < len(siblings):
            nxt = siblings[idx + 1]
            data["page"]["next"] = {"title": nxt.stem, "url": nxt.name}
    return data


def ensure_font_awesome(html: str) -> str:
    if FA_RE.search(html):
        return html
    tag = (
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" '
        'rel="stylesheet"/>\n'
    )
    if "</head>" in html:
        return html.replace("</head>", tag + "</head>", 1)
    return html


def _balanced_div_at(html: str, start: int) -> str | None:
    """Return the full <div>...</div> starting at start, or None."""
    if not html[start:].lower().startswith("<div"):
        return None
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div>", html[start:], flags=re.I):
        token = m.group(0).lower()
        if token.startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return html[start : start + m.end()]
    return None


def remove_verification_bars(html: str) -> str:
    """Remove legacy .verification-bar blocks (balanced), plus nearby comments."""
    while True:
        m = re.search(r'<div\b[^>]*class="[^"]*verification-bar[^"]*"[^>]*>', html, re.I)
        if not m:
            break
        block = _balanced_div_at(html, m.start())
        if not block:
            break
        start = m.start()
        # Also drop a preceding VERIFIED/VERIFICATION comment if present
        prefix = html[max(0, start - 220) : start]
        cm = re.search(r"(?:<!--[^\n]*VERIF(?:IED|ICATION)[^\n]*-->\s*)+$", prefix, re.I)
        if cm:
            start = max(0, start - 220) + cm.start()
        html = html[:start] + "\n" + html[m.start() + len(block) :]
    return html


def strip_legacy_chrome(html: str) -> str:
    """Remove old fixed topbar / verification chrome that would double up."""
    html = TP_TOP_RE.sub("\n", html, count=1)
    html = TP_LIP_RE.sub("\n", html, count=1)
    html = TP_CLASS_RE.sub("\n", html, count=1)
    html = remove_verification_bars(html)
    # Clean leftover TOP BAR stub comments (keep one marker for readability)
    html = re.sub(
        r"(?:<!--[^\n]*TOP BAR[^\n]*-->\s*)+",
        "<!-- TOP BAR replaced by FTP expandable header -->\n",
        html,
        count=1,
        flags=re.I,
    )
    return html


def inject(html: str, page: Path, siblings: list[Path], header_html: str) -> str | None:
    if MARKER in html:
        return None

    prefix = rel_prefix(page)
    css_href = f"{prefix}site-shell/shell.css"
    js_src = f"{prefix}site-shell/shell.js"
    data = build_shell_data(html, page, siblings)
    data_block = (
        '<script id="shell-data" type="application/json">'
        + json.dumps(data, ensure_ascii=False)
        + "</script>"
    )
    head_bits = (
        f'\n<link rel="stylesheet" href="{css_href}"/>\n'
        f"{data_block}\n"
        '<style id="ftp-expandable-header-pagefit">\n'
        "  body.ftp-expandable-header-enabled {\n"
        "    padding-top: calc(var(--header-h, 46px) + var(--panel-h, 34px)) !important;\n"
        "  }\n"
        "</style>\n"
    )

    html = ensure_font_awesome(html)
    html = SHELL_DATA_RE.sub("\n", html)
    if "</head>" not in html:
        raise RuntimeError("no </head>")
    html = html.replace("</head>", head_bits + "</head>", 1)

    m_body = BODY_OPEN_RE.search(html)
    if not m_body:
        raise RuntimeError("no <body>")
    attrs = m_body.group(1) or ""
    if "ftp-expandable-header-enabled" not in attrs:
        if "class=" in attrs:
            attrs = re.sub(
                r'class=(["\'])(.*?)\1',
                lambda m: f'class={m.group(1)}{m.group(2)} ftp-expandable-header-enabled{m.group(1)}',
                attrs,
                count=1,
            )
        else:
            attrs += ' class="ftp-expandable-header-enabled"'
    body_tag = f"<body{attrs}>"
    html = html[: m_body.start()] + body_tag + html[m_body.end() :]

    html = strip_legacy_chrome(html)

    # Re-find body open after edits
    m_body = BODY_OPEN_RE.search(html)
    if not m_body:
        raise RuntimeError("body lost after strip")
    insert = (
        "\n<!-- FTP EXPANDABLE HEADER (auto-injected) -->\n"
        + header_html
        + "\n"
    )
    html = html[: m_body.end()] + insert + html[m_body.end() :]

    js_tag = f'\n<script src="{js_src}"></script>\n'
    if "site-shell/shell.js" not in html:
        idx = html.rfind("</body>")
        if idx == -1:
            raise RuntimeError("no </body>")
        html = html[:idx] + js_tag + html[idx:]

    return html


def iter_html(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".html" else []
    files: list[Path] = []
    for f in sorted(target.rglob("*.html")):
        if any(part in EXCLUDE_DIRS for part in f.relative_to(ROOT).parts):
            continue
        if ".bak" in f.name or f.name.startswith("_"):
            continue
        files.append(f)
    return files


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--path", type=Path, help="Folder under site root")
    ap.add_argument("--file", type=Path, help="Single HTML file")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()

    for required in (HEADER_FILE, CSS_FILE, JS_FILE):
        if not required.exists():
            raise SystemExit(f"Missing required asset: {required}")

    header_html = HEADER_FILE.read_text(encoding="utf-8")
    if MARKER not in header_html:
        raise SystemExit("expandable-header.html missing ftpPanelToggle")

    if args.file:
        target = (args.root / args.file).resolve() if not args.file.is_absolute() else args.file
    elif args.path:
        target = (args.root / args.path).resolve() if not args.path.is_absolute() else args.path
    else:
        target = args.root / "revolution-of-truth"

    files = iter_html(target)
    if not files:
        raise SystemExit(f"No HTML files under {target}")

    # siblings for prev/next within the scanned folder
    siblings = [f for f in files if f.parent == files[0].parent] if files else []

    updated = skipped = failed = 0
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] target={target} files={len(files)}")

    for f in files:
        try:
            html = f.read_text(encoding="utf-8", errors="replace")
            local_siblings = sorted(
                p for p in f.parent.glob("*.html")
                if ".bak" not in p.name and not p.name.startswith("_")
            )
            new = inject(html, f, local_siblings, header_html)
            if new is None:
                skipped += 1
                print(f"  skip (already has expandable header): {f.relative_to(ROOT)}")
                continue
            if args.apply:
                if not args.no_backup:
                    bak = f.with_suffix(f.suffix + ".bak-ftp-header")
                    if not bak.exists():
                        shutil.copy2(f, bak)
                f.write_text(new, encoding="utf-8")
            updated += 1
            print(f"  {'wrote' if args.apply else 'would update'}: {f.relative_to(ROOT)}")
        except Exception as exc:
            failed += 1
            print(f"  FAIL {f.relative_to(ROOT)}: {exc}")

    print(f"[{mode}] updated={updated} skipped={skipped} failed={failed}")
    if not args.apply and updated:
        print("Re-run with --apply to write changes.")


if __name__ == "__main__":
    main()
