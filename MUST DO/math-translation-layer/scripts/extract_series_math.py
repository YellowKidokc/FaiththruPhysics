#!/usr/bin/env python3
"""Extract math expressions from a site series folder into JSON/CSV reports.

Primary use:
  sweep a series like one-page-stories once, inventory all equations, and
  hand the output to MTL translation or definition workflows.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


DEFAULT_EXCLUDES = {".git", "node_modules", ".wrangler", "__pycache__"}

MATH_PATTERNS = [
    ("display_brackets", re.compile(r"\\\[(.*?)\\\]", re.S)),
    ("display_dollars", re.compile(r"\$\$(.*?)\$\$", re.S)),
    ("inline_brackets", re.compile(r"\\\((.*?)\\\)", re.S)),
    ("inline_dollars", re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", re.S)),
]

REPLACEMENTS = [
    (re.compile(r"\\chi|\u03c7", re.I), "chi"),
    (re.compile(r"\\iiint|\u222d|\\iint|\u222b|\\int", re.I), "int"),
    (re.compile(r"\\cdot|·|⋅|\*"), ""),
    (re.compile(r"\\,|\\left|\\right|\\text|\\mathrm"), ""),
    (re.compile(r"\\geq|≥"), "ge"),
    (re.compile(r"\\leq|≤"), "le"),
    (re.compile(r"\\neq|≠"), "ne"),
    (re.compile(r"\\propto|∝"), "propto"),
    (re.compile(r"\\to|→"), "to"),
    (re.compile(r"\\Delta|Δ"), "delta"),
    (re.compile(r"\\Phi|Φ"), "phi"),
    (re.compile(r"\\Psi|Ψ"), "psi"),
    (re.compile(r"\\sigma|σ"), "sigma"),
    (re.compile(r"\\gamma|γ"), "gamma"),
    (re.compile(r"\\mu|μ"), "mu"),
    (re.compile(r"\\nu|ν"), "nu"),
    (re.compile(r"\\rho|ρ"), "rho"),
    (re.compile(r"\\Lambda|Λ"), "lambda"),
    (re.compile(r"\\Theta|Θ"), "theta"),
    (re.compile(r"\\hbar|ℏ"), "hbar"),
    (re.compile(r"\\pi|π"), "pi"),
]


def normalize_for_lookup(source: str) -> str:
    normalized = source
    for pattern, replacement in REPLACEMENTS:
        normalized = pattern.sub(replacement, normalized)
    normalized = re.sub(r"\\[A-Za-z]+", "", normalized)
    normalized = re.sub(r"[^A-Za-z0-9]+", "", normalized)
    return normalized.lower()


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def strip_non_content(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<noscript\b.*?</noscript>", " ", html, flags=re.S | re.I)
    return html


def find_math_matches(text: str, source_kind: str, article_slug: str, start_index: int = 1) -> list[dict]:
    found = []
    seen = set()
    eq_index = start_index
    for pattern_name, pattern in MATH_PATTERNS:
        for match in pattern.finditer(text):
            latex = match.group(1).strip()
            if len(latex) < 2:
                continue
            key = normalize_for_lookup(latex)
            if not key or key in seen:
                continue
            seen.add(key)
            snippet = re.sub(r"\s+", " ", match.group(0))[:180]
            found.append(
                {
                    "equation_id": f"{article_slug}-EQ-{eq_index:03d}",
                    "latex": latex,
                    "lookup_key": key,
                    "source_kind": source_kind,
                    "pattern_name": pattern_name,
                    "source_snippet": snippet,
                }
            )
            eq_index += 1
    return found


def extract_equation_blocks(html: str, article_slug: str) -> tuple[list[dict], set[str]]:
    found = []
    seen = set()
    eq_index = 1
    for block in re.finditer(r'<div class="equation-block"[^>]*>(.*?)</div>', html, re.S | re.I):
        matches = find_math_matches(block.group(1), "equation_block", article_slug, start_index=eq_index)
        for item in matches:
            if item["lookup_key"] in seen:
                continue
            seen.add(item["lookup_key"])
            found.append(item)
            eq_index += 1
    return found, seen


def extract_page_math(path: Path, series_root: Path) -> list[dict]:
    html = strip_non_content(read_text(path))
    rel = path.relative_to(series_root)
    lane = rel.parts[0] if len(rel.parts) > 1 else "(root)"
    article_slug = path.stem

    rows, seen = extract_equation_blocks(html, article_slug)

    fallback = find_math_matches(html, "page_scan", article_slug, start_index=len(rows) + 1)
    for item in fallback:
        if item["lookup_key"] in seen:
            continue
        seen.add(item["lookup_key"])
        rows.append(item)

    for item in rows:
        item["source_path"] = rel.as_posix()
        item["lane"] = lane
        item["article_slug"] = article_slug
    return rows


def iter_html(series_root: Path) -> list[Path]:
    html_files = []
    for path in series_root.rglob("*.html"):
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        html_files.append(path)
    return sorted(html_files)


def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract equations from a series folder.")
    parser.add_argument("--series-root", required=True, help="Path to the series folder to scan.")
    parser.add_argument("--output-dir", required=True, help="Folder for JSON/CSV/summary output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    series_root = Path(args.series_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    all_rows = []
    file_summaries = []
    for path in iter_html(series_root):
        rows = extract_page_math(path, series_root)
        all_rows.extend(rows)
        file_summaries.append(
            {
                "source_path": path.relative_to(series_root).as_posix(),
                "equation_count": len(rows),
            }
        )

    missing_math = [row for row in file_summaries if row["equation_count"] == 0]
    files_with_math = [row for row in file_summaries if row["equation_count"] > 0]
    high_density_files = sorted(files_with_math, key=lambda row: (-row["equation_count"], row["source_path"]))

    key_counts = Counter(row["lookup_key"] for row in all_rows)
    duplicates = []
    for key, count in key_counts.items():
        if count < 2:
            continue
        matches = [row for row in all_rows if row["lookup_key"] == key]
        duplicates.append(
            {
                "lookup_key": key,
                "count": count,
                "latex_samples": sorted({row["latex"] for row in matches})[:5],
                "paths": sorted({row["source_path"] for row in matches}),
            }
        )

    (output_dir / "series_math_inventory.json").write_text(json.dumps(all_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(all_rows, output_dir / "series_math_inventory.csv")
    (output_dir / "series_math_files.json").write_text(json.dumps(file_summaries, indent=2), encoding="utf-8")
    write_csv(file_summaries, output_dir / "series_math_files.csv")
    (output_dir / "series_math_missing_math.json").write_text(json.dumps(missing_math, indent=2), encoding="utf-8")
    write_csv(missing_math, output_dir / "series_math_missing_math.csv")
    (output_dir / "series_math_high_density_files.json").write_text(json.dumps(high_density_files, indent=2), encoding="utf-8")
    write_csv(high_density_files, output_dir / "series_math_high_density_files.csv")
    (output_dir / "series_math_duplicates.json").write_text(json.dumps(duplicates, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(duplicates, output_dir / "series_math_duplicates.csv")

    lanes = Counter(row["lane"] for row in all_rows)
    files_with_math_count = len(files_with_math)
    summary_md = [
        "# Series Math Inventory",
        "",
        f"- Series root: `{series_root}`",
        f"- HTML files scanned: `{len(file_summaries)}`",
        f"- Files with extracted math: `{files_with_math_count}`",
        f"- Files with no extracted math: `{len(missing_math)}`",
        f"- Total unique extracted equations: `{len(all_rows)}`",
        f"- Duplicate lookup-key groups across pages: `{len(duplicates)}`",
        "",
        "## Lane Counts",
        "",
    ]
    for lane, count in lanes.most_common():
        summary_md.append(f"- `{lane}`: `{count}` equations")
    summary_md.append("")
    summary_md.append("## Files With No Extracted Math")
    summary_md.append("")
    if missing_math:
        for row in missing_math[:20]:
            summary_md.append(f"- `{row['source_path']}`")
        if len(missing_math) > 20:
            summary_md.append(f"- ... plus `{len(missing_math) - 20}` more")
    else:
        summary_md.append("- None")
    summary_md.append("")
    summary_md.append("## Highest-Density Math Files")
    summary_md.append("")
    for row in high_density_files[:10]:
        summary_md.append(f"- `{row['source_path']}`: `{row['equation_count']}` equations")
    summary_md.append("")
    summary_md.append("## Outputs")
    summary_md.append("")
    summary_md.append("- `series_math_inventory.json` and `.csv`")
    summary_md.append("- `series_math_files.json` and `.csv`")
    summary_md.append("- `series_math_missing_math.json` and `.csv`")
    summary_md.append("- `series_math_high_density_files.json` and `.csv`")
    summary_md.append("- `series_math_duplicates.json` and `.csv`")
    (output_dir / "series_math_summary.md").write_text("\n".join(summary_md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
