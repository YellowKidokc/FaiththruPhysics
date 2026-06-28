#!/usr/bin/env python3
"""
Export MTL_CONSCIOUSNESS_COMBINED.xlsx to:
  - shared/data/mtl-equations-canonical.json
  - work/register-mtl-equations.sql

Usage:
  python scripts/build_mtl_sql.py
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone

try:
    import pandas as pd
except ImportError as exc:
    raise SystemExit("pandas is required: pip install pandas openpyxl") from exc

ROOT = Path(__file__).resolve().parent.parent
EXCEL = ROOT / "MTL_CONSCIOUSNESS_COMBINED.xlsx"
OUT_JSON = ROOT / "shared" / "data" / "mtl-equations-canonical.json"
OUT_SQL = ROOT / "work" / "register-mtl-equations.sql"

ALLOWED_MODES = {"easy", "standard", "academic", "audio_safe"}


def normalize_latex(value: str) -> str:
    if not isinstance(value, str):
        value = str(value) if value is not None else ""
    text = value.strip()
    text = re.sub(r"^\$+", "", text)
    text = re.sub(r"\$+$", "", text)
    text = re.sub(r"^\\\(|\\\)$", "", text)
    text = re.sub(r"^\\\[|\\\]$", "", text)
    return text.strip()


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe(value):
    if value is None:
        return ""
    text = str(value).strip()
    # collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text


def clean_for_sql(value: str) -> str:
    return value.replace("'", "''")


def row_to_record(row: dict, source: str, idx: int) -> dict:
    """Map a row from one of the three sheets to a canonical record."""
    record = {
        "eq_id": None,
        "latex": "",
        "easy": "",
        "standard": "",
        "academic": "",
        "audio_safe": "",
        "source": source,
        "source_file": "",
        "difficulty": "",
        "paper_ref": "",
    }

    if source == "Consciousness_Equations":
        record["eq_id"] = safe(row.get("ID")) or f"CON-{idx:04d}"
        record["latex"] = normalize_latex(row.get("Equation_Raw", ""))
        record["easy"] = safe(row.get("English_Translation"))
        record["standard"] = safe(row.get("Term_By_Term"))
        academic_parts = [
            safe(row.get("Physics_Side")),
            safe(row.get("Theology_Side")),
            safe(row.get("Shared_Structure")),
        ]
        record["academic"] = "\n\n".join([p for p in academic_parts if p])
        record["audio_safe"] = safe(row.get("English_Translation"))
        record["source_file"] = safe(row.get("Source_File"))
        record["difficulty"] = safe(row.get("Difficulty"))
        record["paper_ref"] = safe(row.get("Law_Reference"))

    elif source == "Existing_458_Translations":
        eq_id = safe(row.get("id"))
        record["eq_id"] = f"EXT-{eq_id}" if eq_id else f"EXT-{idx:04d}"
        record["latex"] = normalize_latex(row.get("latex", ""))
        record["easy"] = safe(row.get("medium_form")) or safe(row.get("short_form"))
        record["standard"] = safe(row.get("medium_form"))
        record["academic"] = safe(row.get("conceptual_meaning"))
        record["audio_safe"] = safe(row.get("tts_audio"))
        record["source_file"] = safe(row.get("source_file"))
        record["paper_ref"] = safe(row.get("paper_ref"))

    elif source == "Core_16_Equations":
        record["eq_id"] = safe(row.get("paper_ref")) or f"CORE-{idx:04d}"
        record["latex"] = normalize_latex(row.get("latex", ""))
        record["easy"] = safe(row.get("plain_english"))
        record["standard"] = safe(row.get("conceptual_meaning"))
        record["academic"] = safe(row.get("conceptual_meaning"))
        record["audio_safe"] = safe(row.get("tts_audio"))
        record["source_file"] = safe(row.get("paper_ref"))
        record["paper_ref"] = safe(row.get("paper_ref"))

    return record


def merge_records(records: list) -> dict:
    """Deduplicate by normalized latex hash; keep the richest translation per field."""
    by_hash = {}
    for rec in records:
        latex = rec["latex"]
        if not latex:
            continue
        h = sha256_hex(latex)
        if h not in by_hash:
            by_hash[h] = rec.copy()
            by_hash[h]["latex_hash"] = h
            continue

        existing = by_hash[h]
        # Prefer non-empty fields; for academic, take longest
        for mode in ALLOWED_MODES:
            if len(rec.get(mode, "")) > len(existing.get(mode, "")):
                existing[mode] = rec[mode]
        if not existing.get("eq_id") and rec.get("eq_id"):
            existing["eq_id"] = rec["eq_id"]
        if not existing.get("source_file") and rec.get("source_file"):
            existing["source_file"] = rec["source_file"]
        if not existing.get("paper_ref") and rec.get("paper_ref"):
            existing["paper_ref"] = rec["paper_ref"]
        if not existing.get("difficulty") and rec.get("difficulty"):
            existing["difficulty"] = rec["difficulty"]
        # Track all sources that contributed
        if rec["source"] not in existing["source"]:
            existing["source"] += f",{rec['source']}"

    return by_hash


def build_sql(by_hash: dict) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "-- Generated by scripts/build_mtl_sql.py",
        "-- Register MTL equations for the faith-mtl-worker.",
        "-- D1 remote execute does not support BEGIN TRANSACTION; statements are applied sequentially.",
    ]

    for h, rec in sorted(by_hash.items(), key=lambda x: x[1].get("eq_id") or x[0]):
        cols = [
            "eq_id", "latex_hash", "latex", "easy", "standard", "academic",
            "audio_safe", "source", "source_file", "difficulty", "paper_ref", "updated_at"
        ]
        values = [
            clean_for_sql(rec.get("eq_id", "")),
            clean_for_sql(rec.get("latex_hash", "")),
            clean_for_sql(rec.get("latex", "")),
            clean_for_sql(rec.get("easy", "")),
            clean_for_sql(rec.get("standard", "")),
            clean_for_sql(rec.get("academic", "")),
            clean_for_sql(rec.get("audio_safe", "")),
            clean_for_sql(rec.get("source", "")),
            clean_for_sql(rec.get("source_file", "")),
            clean_for_sql(rec.get("difficulty", "")),
            clean_for_sql(rec.get("paper_ref", "")),
            now,
        ]
        col_str = ", ".join(cols)
        val_str = ", ".join(f"'{v}'" for v in values)
        sql = (
            f"INSERT INTO mtl_equations ({col_str}) VALUES ({val_str}) "
            "ON CONFLICT(latex_hash) DO UPDATE SET "
            "eq_id = excluded.eq_id, "
            "latex = excluded.latex, "
            "easy = excluded.easy, "
            "standard = excluded.standard, "
            "academic = excluded.academic, "
            "audio_safe = excluded.audio_safe, "
            "source = excluded.source, "
            "source_file = excluded.source_file, "
            "difficulty = excluded.difficulty, "
            "paper_ref = excluded.paper_ref, "
            "updated_at = excluded.updated_at;"
        )
        lines.append(sql)

    return "\n".join(lines)


def main():
    if not EXCEL.exists():
        raise SystemExit(f"Excel file not found: {EXCEL}")

    print(f"Reading {EXCEL.name}...")
    xl = pd.ExcelFile(EXCEL)
    records = []

    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        print(f"  {sheet}: {len(df)} rows")
        for idx, row in df.iterrows():
            rec = row_to_record(row.to_dict(), sheet, idx + 1)
            if rec["latex"]:
                records.append(rec)

    print(f"Total raw records: {len(records)}")
    by_hash = merge_records(records)
    print(f"Unique equations: {len(by_hash)}")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_SQL.parent.mkdir(parents=True, exist_ok=True)

    canonical = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "total": len(by_hash),
        "items": sorted(by_hash.values(), key=lambda r: r.get("eq_id") or r["latex_hash"]),
    }
    OUT_JSON.write_text(json.dumps(canonical, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")

    OUT_SQL.write_text(build_sql(by_hash), encoding="utf-8")
    print(f"Wrote {OUT_SQL}")


if __name__ == "__main__":
    main()
