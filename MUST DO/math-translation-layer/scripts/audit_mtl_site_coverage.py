#!/usr/bin/env python3
"""Audit site MTL coverage against the live D1 database.

This script:
- scans HTML pages under a site root
- detects whether each page loads the worker client
- extracts unique equations from each page
- pulls all known equation hashes from D1 via Wrangler
- reports pages with full coverage, partial coverage, or missing coverage
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    ".wrangler",
    "node_modules",
    "__pycache__",
    "_link-fix-backups",
    "_link-fix-backup-2026-05-05-2124",
    "isomorphism_backup_20260624_163104",
    "work",
    "subdomains",
    "MUST DO",
    "reports",
    "components",
    "shared",
    "workers",
    "mtl-admin",
    "Templates David",
}

MATH_PATTERNS = [
    re.compile(r"\\\[(.*?)\\\]", re.S),
    re.compile(r"\$\$(.*?)\$\$", re.S),
    re.compile(r"\\\((.*?)\\\)", re.S),
    re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", re.S),
]

WORKER_SCRIPT_MARKER = "/shared/js/mtl-worker-client.js"


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


def normalize_latex(value: str) -> str:
    text = (value or "").strip()
    text = re.sub(r"^\$+", "", text)
    text = re.sub(r"\$+$", "", text)
    text = re.sub(r"^\\\(|\\\)$", "", text)
    text = re.sub(r"^\\\[|\\\]$", "", text)
    return text.strip()


def latex_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_equations(html: str) -> list[str]:
    cleaned = strip_non_content(html)
    found: list[str] = []
    seen: set[str] = set()
    for pattern in MATH_PATTERNS:
        for match in pattern.finditer(cleaned):
            latex = normalize_latex(match.group(1))
            if len(latex) < 2:
                continue
            if latex in seen:
                continue
            seen.add(latex)
            found.append(latex)
    return found


def iter_html(site_root: Path) -> list[Path]:
    files = []
    for path in site_root.rglob("*.html"):
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def extract_json_tail(text: str):
    start = text.find("[")
    if start == -1:
        raise ValueError("Could not find JSON payload in wrangler output")
    return json.loads(text[start:])


def fetch_d1_index() -> dict[str, dict]:
    cmd = [
        "wrangler.cmd",
        "d1",
        "execute",
        "faiththruphysics-mtl",
        "--remote",
        "--json",
        "--command",
        "SELECT latex_hash, eq_id, source_file, source FROM mtl_equations;",
    ]
    result = subprocess.run(
        cmd,
        cwd=r"D:\GitHub\faiththruphysics-site\workers\mtl-service",
        capture_output=True,
        text=True,
        check=True,
    )
    payload = extract_json_tail(result.stdout)
    rows = payload[0]["results"]
    return {row["latex_hash"]: row for row in rows}


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit site MTL coverage against live D1 rows.")
    parser.add_argument("--site-root", required=True, help="Root folder to scan")
    parser.add_argument("--output-dir", required=True, help="Folder for reports")
    parser.add_argument("--worker-base", default="https://faith-mtl-worker.davidokc28.workers.dev", help="Worker base URL for reference only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    site_root = Path(args.site_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    d1_index = fetch_d1_index()

    page_rows = []
    missing_rows = []
    status_counts = Counter()

    for path in iter_html(site_root):
        rel = path.relative_to(site_root).as_posix()
        html = read_text(path)
        has_worker_client = WORKER_SCRIPT_MARKER in html
        equations = extract_equations(html)
        found_count = 0
        missing_count = 0
        status = "no_equations"
        missing_sample = []

        if equations:
            missing = []
            for latex in equations:
                digest = latex_hash(latex)
                record = d1_index.get(digest, {})
                if record:
                    found_count += 1
                else:
                    missing_count += 1
                    missing.append((latex, digest))

            missing_sample = [item[0] for item in missing[:5]]
            if has_worker_client:
                if missing_count == 0:
                    status = "full_coverage"
                elif found_count == 0:
                    status = "worker_client_but_zero_matches"
                else:
                    status = "partial_coverage"
            else:
                if found_count > 0:
                    status = "db_ready_but_page_not_wired"
                else:
                    status = "page_not_wired_and_no_matches"

            for latex, digest in missing:
                missing_rows.append(
                    {
                        "source_path": rel,
                        "latex": latex,
                        "latex_hash": digest,
                        "has_worker_client": has_worker_client,
                    }
                )
        else:
            if has_worker_client:
                status = "worker_client_but_no_equations"

        status_counts[status] += 1
        page_rows.append(
            {
                "source_path": rel,
                "has_worker_client": has_worker_client,
                "equation_count": len(equations),
                "found_count": found_count,
                "missing_count": missing_count,
                "status": status,
                "missing_sample": " | ".join(missing_sample),
            }
        )

    page_rows.sort(key=lambda row: (-row["missing_count"], -row["equation_count"], row["source_path"]))
    missing_rows.sort(key=lambda row: (row["source_path"], row["latex"]))

    summary = {
        "site_root": str(site_root),
        "worker_base": args.worker_base,
        "d1_rows_checked": len(d1_index),
        "pages_scanned": len(page_rows),
        "status_counts": dict(status_counts),
        "pages_with_worker_client": sum(1 for row in page_rows if row["has_worker_client"]),
        "pages_with_equations": sum(1 for row in page_rows if row["equation_count"] > 0),
        "pages_with_missing_translations": sum(1 for row in page_rows if row["missing_count"] > 0),
        "total_missing_equations": len(missing_rows),
    }

    (output_dir / "mtl_coverage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output_dir / "mtl_page_status.json").write_text(json.dumps(page_rows, indent=2), encoding="utf-8")
    (output_dir / "mtl_missing_equations.json").write_text(json.dumps(missing_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(page_rows, output_dir / "mtl_page_status.csv")
    write_csv(missing_rows, output_dir / "mtl_missing_equations.csv")

    lines = [
        "# MTL Site Coverage Audit",
        "",
        f"- Site root: `{site_root}`",
        f"- Worker base: `{args.worker_base}`",
        f"- D1 rows checked: `{len(d1_index)}`",
        f"- Pages scanned: `{len(page_rows)}`",
        f"- Pages with worker client: `{summary['pages_with_worker_client']}`",
        f"- Pages with equations: `{summary['pages_with_equations']}`",
        f"- Pages with missing translations: `{summary['pages_with_missing_translations']}`",
        f"- Total missing equations: `{summary['total_missing_equations']}`",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(status_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{status}`: `{count}`")
    lines.extend(["", "## Worst Pages", ""])
    for row in page_rows[:25]:
        if row["equation_count"] == 0 and row["missing_count"] == 0:
            continue
        lines.append(
            f"- `{row['source_path']}` | status=`{row['status']}` | equations=`{row['equation_count']}` | found=`{row['found_count']}` | missing=`{row['missing_count']}`"
        )
    (output_dir / "mtl_coverage_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
