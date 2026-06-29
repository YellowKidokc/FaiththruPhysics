#!/usr/bin/env python3
"""
inject_verification.py — Inject the verification bar below the top bar on article pages.

Usage:
    python scripts/inject_verification.py --dry-run
    python scripts/inject_verification.py --apply
    python scripts/inject_verification.py --apply --single genesis-to-quantum
"""

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
COMPONENT = ROOT / "components" / "verification-bar.html"
DATA_DIR = ROOT / "data-viz"
BACKUP_SUFFIX = "_vb_backup"

SERIES = [
    "genesis-to-quantum", "moral-decline", "cross-domain", "convergence-series",
    "convergence-deep", "one-page-stories", "blue", "consciousness",
    "proof-architecture", "three-truths", "revolution-of-truth", "rigor", "mda",
    "subdomains",
]


def load_component():
    if not COMPONENT.exists():
        raise SystemExit(f"Component not found: {COMPONENT}")
    return COMPONENT.read_text(encoding="utf-8")


def normalize_stem(stem: str) -> list[str]:
    """Generate likely JSON slug variants from an HTML filename stem."""
    base = stem
    no_interlude = base.replace("-interlude", "")
    hyphen = base.replace(" ", "-")
    hyphen_no_interlude = no_interlude.replace(" ", "-")
    seen = []
    for v in (base, no_interlude, hyphen, hyphen_no_interlude):
        if v not in seen:
            seen.append(v)
    return seen


def find_verification_slug(path: Path) -> str | None:
    """Return the verification JSON slug that matches this HTML page, or None."""
    for variant in normalize_stem(path.stem):
        exact = DATA_DIR / f"{variant}.verification.json"
        if exact.exists():
            return variant
        canonical = DATA_DIR / f"{variant}.canonical.verification.json"
        if canonical.exists():
            return f"{variant}.canonical"
    return None


def make_loader(slug: str) -> str:
    safe_slug = quote(slug, safe="")
    return f"""<script>
(function() {{
  function initVerification() {{
    fetch('/data-viz/{safe_slug}.verification.json')
      .then(r => {{ if (!r.ok) throw new Error('status ' + r.status); return r.json(); }})
      .then(data => {{ if (typeof loadVerification === 'function') loadVerification(data); }})
      .catch(err => {{ console.warn('Verification data unavailable for {safe_slug}:', err); }});
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', initVerification);
  }} else {{
    initVerification();
  }}
}})();
</script>"""


def inject_into_page(html: str, component_html: str, slug: str) -> tuple[str, str]:
    if 'id="verificationBar"' in html:
        return html, "already has verification bar"

    if "<header class=\"tp-top\"" not in html:
        return html, "no tp-top header"

    start = html.find("<header class=\"tp-top\"")
    end = html.find("</header>", start)
    if end == -1:
        return html, "no closing </header> for tp-top"
    insert_at = end + len("</header>")

    loader = make_loader(slug)
    injection = f"\n<!-- ═══════ VERIFICATION BAR ═══════ -->\n{component_html}\n{loader}\n<!-- ═══════ END VERIFICATION BAR ═══════ -->\n"
    html = html[:insert_at] + injection + html[insert_at:]
    return html, "injected verification bar"


def process_file(path: Path, component_html: str, apply: bool) -> str:
    html = path.read_text(encoding="utf-8", errors="ignore")
    slug = find_verification_slug(path)

    if not slug:
        return f"  SKIP {path.relative_to(ROOT)} (no verification JSON for {path.stem})"

    updated, action = inject_into_page(html, component_html, slug)
    if "ERROR" in action or "already" in action or "no " in action:
        return f"  SKIP {path.relative_to(ROOT)} - {action}"

    if apply:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = path.parent / f"{path.stem}{BACKUP_SUFFIX}_{ts}"
        backup_dir.mkdir(exist_ok=True)
        shutil.copy2(path, backup_dir / path.name)
        path.write_text(updated, encoding="utf-8")
        return f"  APPLY {path.relative_to(ROOT)} - {action}"
    return f"  DRY {path.relative_to(ROOT)} - {action}"


def process_series(series_dir: Path, component_html: str, apply: bool) -> list[str]:
    results = []
    if not series_dir.exists():
        return [f"  SKIP {series_dir.name}/ (not found)"]
    for html_path in series_dir.rglob("*.html"):
        parts = html_path.parts
        if any(p in ("components", "NLP") for p in parts):
            continue
        if any(BACKUP_SUFFIX in p or "backup" in p.lower() for p in parts):
            continue
        if html_path.name.lower() == "index.html":
            continue
        results.append(process_file(html_path, component_html, apply))
    return results


def main():
    parser = argparse.ArgumentParser(description="Inject verification bar into article pages")
    parser.add_argument("--single", help="Process only this series folder")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--apply", action="store_true", help="Write changes")
    args = parser.parse_args()

    component_html = load_component()
    apply = args.apply

    targets = [args.single] if args.single else SERIES
    total = 0
    for name in targets:
        print(f"\n[{name}]")
        results = process_series(ROOT / name, component_html, apply)
        for r in results:
            print(r)
        total += sum(1 for r in results if ("APPLY" if apply else "DRY") in r)

    print(f"\n{'APPLY' if apply else 'DRY'} {total} file(s) {'updated' if apply else 'would be updated'}")
    if not apply:
        print("  Add --apply to write.")


if __name__ == "__main__":
    main()
