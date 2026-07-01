#!/usr/bin/env python3
"""Export safe normalized MTL rows to D1-ready JSON and SQL packages."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sql_quote(value: str) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export safe MTL rows to D1 SQL/JSON.")
    parser.add_argument("--normalized-csv", required=True, help="Path to normalized_mtl_records.csv")
    parser.add_argument("--output-dir", required=True, help="Folder to write D1 import assets")
    parser.add_argument("--source-label", default="mtl_workbook_normalized_safe_rows", help="Source label stored in D1")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_csv(Path(args.normalized_csv).resolve())
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    safe_rows = []
    review_rows = []

    for row in rows:
        record = {
            "eq_id": row.get("eq_id", "").strip(),
            "latex_hash": row.get("latex_hash", "").strip(),
            "latex": row.get("latex", "").strip(),
            "easy": row.get("easy", "").strip(),
            "standard": row.get("standard", "").strip(),
            "academic": row.get("academic", "").strip(),
            "audio_safe": row.get("audio_safe", "").strip(),
            "source": args.source_label,
            "source_file": row.get("source_file", "").strip(),
            "difficulty": row.get("difficulty", "").strip(),
            "paper_ref": row.get("paper_ref", "").strip(),
            "updated_at": timestamp,
            "needs_review": row.get("needs_review", "").strip().lower() == "true",
        }
        if record["needs_review"]:
            review_rows.append(record)
        else:
            safe_rows.append(record)

    sql_lines = [
        "-- Safe D1 import for MTL rows",
        f"-- Generated: {timestamp}",
        f"-- Safe rows: {len(safe_rows)}",
        "",
    ]

    for row in safe_rows:
        sql_lines.extend(
            [
                "INSERT INTO mtl_equations (eq_id, latex_hash, latex, easy, standard, academic, audio_safe, source, source_file, difficulty, paper_ref, updated_at)",
                "VALUES ("
                + ", ".join(
                    [
                        sql_quote(row["eq_id"]),
                        sql_quote(row["latex_hash"]),
                        sql_quote(row["latex"]),
                        sql_quote(row["easy"]),
                        sql_quote(row["standard"]),
                        sql_quote(row["academic"]),
                        sql_quote(row["audio_safe"]),
                        sql_quote(row["source"]),
                        sql_quote(row["source_file"]),
                        sql_quote(row["difficulty"]),
                        sql_quote(row["paper_ref"]),
                        sql_quote(row["updated_at"]),
                    ]
                )
                + ")",
                "ON CONFLICT(latex_hash) DO UPDATE SET "
                + ", ".join(
                    [
                        "eq_id=excluded.eq_id",
                        "latex=excluded.latex",
                        "easy=excluded.easy",
                        "standard=excluded.standard",
                        "academic=excluded.academic",
                        "audio_safe=excluded.audio_safe",
                        "source=excluded.source",
                        "source_file=excluded.source_file",
                        "difficulty=excluded.difficulty",
                        "paper_ref=excluded.paper_ref",
                        "updated_at=excluded.updated_at",
                    ]
                )
                + ";",
                "",
            ]
        )
    summary = {
        "generated_at": timestamp,
        "safe_row_count": len(safe_rows),
        "needs_review_count": len(review_rows),
        "source_label": args.source_label,
    }

    (output_dir / "safe_d1_import_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output_dir / "safe_d1_rows.json").write_text(json.dumps(safe_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "safe_d1_needs_review_rows.json").write_text(json.dumps(review_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "safe_d1_import.sql").write_text("\n".join(sql_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
