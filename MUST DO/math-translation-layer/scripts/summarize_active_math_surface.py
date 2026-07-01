#!/usr/bin/env python3
"""Summarize the likely active MTL surface from a full-site math scan.

This filters out obvious backup, mirror, and workspace surfaces so the
remaining counts better reflect live/public pages that matter for rollout.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


DEFAULT_EXCLUDES = [
    "_link-fix-backup",
    "_link-fix-backups/",
    "isomorphism_backup_",
    "work/",
    "subdomains/",
    "Templates David/",
    "MUST DO/",
    "mtl-admin/",
    "reports/",
    "components/",
    "shared/",
    "workers/",
    ".wrangler/",
]


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def is_excluded(source_path: str, patterns: list[str]) -> bool:
    normalized = source_path.replace("\\", "/")
    return any(pattern in normalized for pattern in patterns)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize likely active math pages from a full-site scan.")
    parser.add_argument("--site-root-report", required=True, help="Path to the full-site math report folder.")
    parser.add_argument("--output-dir", required=True, help="Output folder for active-only summary.")
    parser.add_argument("--exclude", action="append", default=[], help="Extra exclusion substring. Can be repeated.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report_dir = Path(args.site_root_report).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    files_rows = read_csv(report_dir / "series_math_files.csv")
    inventory_rows = read_csv(report_dir / "series_math_inventory.csv")
    duplicate_rows = read_csv(report_dir / "series_math_duplicates.csv")

    exclude_patterns = DEFAULT_EXCLUDES + args.exclude

    active_files = [row for row in files_rows if not is_excluded(row["source_path"], exclude_patterns)]
    active_inventory = [row for row in inventory_rows if not is_excluded(row["source_path"], exclude_patterns)]

    active_lookup_keys = {row["lookup_key"] for row in active_inventory}
    active_duplicates = []
    for row in duplicate_rows:
        if row.get("lookup_key") in active_lookup_keys:
            active_duplicates.append(row)

    lane_counts = Counter()
    for row in active_inventory:
        lane = row["lane"] or "(root)"
        lane_counts[lane] += 1

    active_files_with_math = []
    active_missing_math = []
    for row in active_files:
        eq_count = int(row["equation_count"])
        record = {"source_path": row["source_path"], "equation_count": eq_count}
        if eq_count > 0:
            active_files_with_math.append(record)
        else:
            active_missing_math.append(record)

    active_files_with_math.sort(key=lambda row: (-row["equation_count"], row["source_path"]))
    active_missing_math.sort(key=lambda row: row["source_path"])

    lane_rows = [{"lane": lane, "equation_count": count} for lane, count in lane_counts.most_common()]
    summary = {
        "site_root_report": str(report_dir),
        "excluded_patterns": exclude_patterns,
        "html_files_scanned_after_filter": len(active_files),
        "files_with_math_after_filter": len(active_files_with_math),
        "files_with_no_math_after_filter": len(active_missing_math),
        "total_equations_after_filter": len(active_inventory),
        "duplicate_groups_after_filter": len(active_duplicates),
        "top_lanes": lane_rows[:20],
        "top_files": active_files_with_math[:20],
    }

    (output_dir / "active_math_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output_dir / "active_lane_counts.json").write_text(json.dumps(lane_rows, indent=2), encoding="utf-8")
    write_csv(lane_rows, output_dir / "active_lane_counts.csv")
    write_csv(active_files_with_math, output_dir / "active_files_with_math.csv")
    write_csv(active_missing_math, output_dir / "active_files_missing_math.csv")

    summary_md = [
        "# Active Math Surface",
        "",
        f"- Source report: `{report_dir}`",
        f"- HTML files after filter: `{len(active_files)}`",
        f"- Files with extracted math: `{len(active_files_with_math)}`",
        f"- Files with no extracted math: `{len(active_missing_math)}`",
        f"- Total extracted equations: `{len(active_inventory)}`",
        f"- Duplicate lookup-key groups: `{len(active_duplicates)}`",
        "",
        "## Excluded Patterns",
        "",
    ]
    for pattern in exclude_patterns:
        summary_md.append(f"- `{pattern}`")
    summary_md.extend(["", "## Top Lanes", ""])
    for row in lane_rows[:20]:
        summary_md.append(f"- `{row['lane']}`: `{row['equation_count']}` equations")
    summary_md.extend(["", "## Top Files", ""])
    for row in active_files_with_math[:20]:
        summary_md.append(f"- `{row['source_path']}`: `{row['equation_count']}` equations")

    (output_dir / "active_math_summary.md").write_text("\n".join(summary_md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
