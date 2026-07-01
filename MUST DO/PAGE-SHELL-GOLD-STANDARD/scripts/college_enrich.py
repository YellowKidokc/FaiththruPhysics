#!/usr/bin/env python3
"""
college_enrich.py — automatic College-level visual enrichment for article HTML.

Turns plain markdown/HTML bodies into College-panel markup the CSS can style:
  - Equation cards (.tp-eqcard) for standalone $$…$$ / \\[…\\] blocks
  - Feature boxes (.tp-feature-1..5) — rotated shapes/highlights on punchy lines
  - Section wrappers + References tagging (via article_html.md_to_html)

CSS in faiththruphysics-site/components/top-bar-bottom-bar.css handles the rest
(drop caps, rotating h2 styles, blockquote callouts, table cards) — no markup needed.

Standalone usage:
  python college_enrich.py --series revolution-of-truth --slug drv-00-the-argument
  python college_enrich.py --series revolution-of-truth --audit
  python college_enrich.py --markdown path/to/article.canonical.md --out enriched.html

Called automatically by top_bar_bottom_bar.py when building pages.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from article_html import md_to_html

DATA = Path(r"D:\GitHub\faiththruphysics-site-data")
LEGACY_COLLEGE = DATA / "APIs" / "input"

EQ_PARA_RE = re.compile(
    r"<p>\s*((?:\$\$.*?\$\$)|(?:\\\[.*?\\\]))\s*</p>", re.DOTALL
)
LABEL_EQ_RE = re.compile(
    r"<p>([^<]{3,70})</p>\s*<div class=\"tp-eqcard\">(.*?)</div>", re.DOTALL
)

FEATURE_VARIANTS = 5
_P_RE = re.compile(r"<p>(.*?)</p>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_SECTION_RE = re.compile(r"(<section[^>]*>.*?</section>)", re.DOTALL)


def _is_feature_candidate(inner_html: str) -> bool:
    if "$$" in inner_html or "\\[" in inner_html or "\\(" in inner_html:
        return False
    text = _TAG_RE.sub("", inner_html).strip()
    if not (60 <= len(text) <= 230):
        return False
    if text.count(". ") > 2:
        return False
    return True


def _inside_blockquote(chunk: str, pos: int) -> bool:
    before = chunk[:pos]
    return before.rfind("<blockquote") > before.rfind("</blockquote>")


def wrap_equation_cards(html: str) -> str:
    """Standalone block equations → .tp-eqcard; fold short caption paragraphs into label."""
    html = EQ_PARA_RE.sub(
        lambda m: f'<div class="tp-eqcard">{m.group(1).strip()}</div>', html
    )

    def fold(m: re.Match) -> str:
        label = m.group(1).strip()
        eq = m.group(2).strip()
        if label.endswith(".") or label.endswith(":") or (" " not in label and len(label) < 3):
            return m.group(0)
        if len(label) > 70 or label.count(".") > 1:
            return m.group(0)
        return f'<div class="tp-eqcard"><div class="tp-eqcard-label">{label}</div>{eq}</div>'

    return LABEL_EQ_RE.sub(fold, html)


def wrap_feature_boxes(html: str, max_boxes: int = 6) -> str:
    """Pull one punchy paragraph from every other section into a rotated feature box."""
    parts = _SECTION_RE.split(html)
    feat = 0
    sec_idx = -1
    out: list[str] = []
    for chunk in parts:
        if chunk.startswith("<section"):
            sec_idx += 1
            if "tp-refs" in chunk:
                out.append(chunk)
                continue
            if sec_idx % 2 == 1 and feat < max_boxes:
                target = None
                for j, m in enumerate(_P_RE.finditer(chunk)):
                    if j == 0 or _inside_blockquote(chunk, m.start()):
                        continue
                    if _is_feature_candidate(m.group(1)):
                        target = m
                        break
                if target is not None:
                    variant = (feat % FEATURE_VARIANTS) + 1
                    feat += 1
                    inner = target.group(1).strip()
                    box = (
                        f'<aside class="tp-feature tp-feature-{variant}">'
                        f"<p>{inner}</p></aside>"
                    )
                    chunk = chunk[: target.start()] + box + chunk[target.end():]
            out.append(chunk)
        else:
            out.append(chunk)
    return "".join(out)


def enrich_college_html(html: str) -> str:
    """Full College markup enrichment pass (equation cards + feature boxes)."""
    if not html:
        return html
    html = wrap_equation_cards(html)
    html = wrap_feature_boxes(html)
    return html


def enrich_college_markdown(md: str) -> str:
    """Markdown → HTML → College enrichment."""
    return enrich_college_html(md_to_html(md))


def enrichment_stats(html: str) -> dict:
    """Counts for audit / dry-run reports."""
    features = re.findall(r'tp-feature tp-feature-(\d+)', html)
    return {
        "sections": len(re.findall(r"<section", html)),
        "eq_cards": html.count('class="tp-eqcard"'),
        "feature_boxes": len(features),
        "feature_variants": features,
        "blockquotes": html.count("<blockquote"),
        "tables": html.count("<table"),
        "has_refs_section": 'class="tp-refs"' in html,
    }


def college_md_path(series: str, slug: str) -> Path | None:
    filename = f"{slug}.canonical.md"
    for path in (DATA / series / filename, LEGACY_COLLEGE / series / filename):
        if path.is_file():
            return path
    return None


def audit_series(series: str, slugs: list[str] | None = None) -> list[dict]:
    series_dir = DATA / series
    if slugs is None:
        slugs = sorted(
            p.name.replace(".canonical.md", "")
            for p in series_dir.glob("*.canonical.md")
        )
    rows = []
    for slug in slugs:
        path = college_md_path(series, slug)
        if not path:
            rows.append({"slug": slug, "status": "missing", "path": None})
            continue
        md = path.read_text(encoding="utf-8", errors="replace")
        html = enrich_college_markdown(md)
        row = {"slug": slug, "status": "ok", "path": str(path), **enrichment_stats(html)}
        rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="College-level article HTML enrichment")
    parser.add_argument("--series", default="revolution-of-truth")
    parser.add_argument("--slug", help="Single page slug (without .html)")
    parser.add_argument("--audit", action="store_true", help="Report enrichment stats for series")
    parser.add_argument("--markdown", type=Path, help="Enrich a single markdown file")
    parser.add_argument("--out", type=Path, help="Write enriched HTML here")
    parser.add_argument("--json", action="store_true", help="Emit audit as JSON")
    args = parser.parse_args()

    if args.audit:
        rows = audit_series(args.series, [args.slug] if args.slug else None)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print(f"College enrichment audit — {args.series}")
            for row in rows:
                if row["status"] == "missing":
                    print(f"  MISSING: {row['slug']}")
                    continue
                print(
                    f"  {row['slug']}: "
                    f"{row['eq_cards']} eq-cards, "
                    f"{row['feature_boxes']} features {row.get('feature_variants', [])}, "
                    f"{row['sections']} sections, "
                    f"{row['tables']} tables"
                )
        return 0

    if args.markdown:
        md = args.markdown.read_text(encoding="utf-8", errors="replace")
        html = enrich_college_markdown(md)
        stats = enrichment_stats(html)
        if args.out:
            args.out.write_text(html, encoding="utf-8", newline="\n")
            print(f"Wrote {args.out} — {stats}")
        else:
            print(html)
        return 0

    if not args.slug:
        parser.error("Provide --slug, --audit, or --markdown")
        return 1

    path = college_md_path(args.series, args.slug)
    if not path:
        print(f"No college markdown for {args.series}/{args.slug}", file=sys.stderr)
        return 1
    md = path.read_text(encoding="utf-8", errors="replace")
    html = enrich_college_markdown(md)
    stats = enrichment_stats(html)
    print(f"Source: {path}")
    print(f"Stats: {json.dumps(stats)}")
    if args.out:
        args.out.write_text(html, encoding="utf-8", newline="\n")
        print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
