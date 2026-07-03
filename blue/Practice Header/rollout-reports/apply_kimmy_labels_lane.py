#!/usr/bin/env python3
"""Kimmy lane: batch label manifest pages (Cursor, Gemini, Claude, or Kimmy)."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\GitHub\faiththruphysics-site-v2")
MANIFEST = ROOT / "blue" / "Practice Header" / "ai-article-rollout-split.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", choices=["Cursor", "Gemini", "Claude", "Kimmy"], default="Gemini")
    args = parser.parse_args()

    sys.path.insert(0, str(Path(r"D:\GitHub\Python-WEB")))
    import label_elements as le
    from label_elements import apply_one, load_rules

    le.SITE_ROOT = ROOT
    le.VISUAL_DIR = ROOT / "_visual"
    le.RULES_FILE = le.VISUAL_DIR / "label_rules.json"
    le.UNKNOWNS_FILE = ROOT / "_visual" / f"label-unknowns-{args.lane.lower()}-rollout.json"
    le.ARCHIVE_ROOT = ROOT / "_site_archives" / "labeling"

    paths = json.loads(MANIFEST.read_text(encoding="utf-8"))["folder_balanced_article_split"][args.lane]["paths"]
    rules = load_rules()
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report_dir = ROOT / "blue" / "Practice Header" / "rollout-reports" / args.lane.lower()
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "KIMMY-LABEL-BATCH.json"

    changed = unchanged = 0
    all_unknowns: Counter = Counter()

    for rel in paths:
        p = ROOT / Path(rel)
        if not p.exists():
            continue
        _status, _roles, unknowns, did_change = apply_one(p, rules, True, True, run_stamp)
        if did_change:
            changed += 1
        else:
            unchanged += 1
        all_unknowns.update(unknowns)

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "lane": f"Kimmy ({args.lane} manifest batch)",
        "pages": len(paths),
        "changed": changed,
        "unchanged": unchanged,
        "distinct_unknown_tokens": len(all_unknowns),
        "top_unknowns": [{"class": t, "count": n} for t, n in all_unknowns.most_common(40)],
    }
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    le.UNKNOWNS_FILE.write_text(
        json.dumps({"generated": payload["generated"], "unknown_count": len(all_unknowns), "unknowns": payload["top_unknowns"]}, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({k: payload[k] for k in ("pages", "changed", "unchanged", "distinct_unknown_tokens")}, indent=2))
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
