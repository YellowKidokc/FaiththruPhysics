#!/usr/bin/env python3
"""Kimmy lane: batch label Cursor manifest pages."""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\GitHub\faiththruphysics-site-v2")
MANIFEST = ROOT / "blue" / "Practice Header" / "ai-article-rollout-split.json"
UNKNOWNS = ROOT / "_visual" / "label-unknowns-cursor-rollout.json"
REPORT = ROOT / "blue" / "Practice Header" / "rollout-reports" / "cursor" / "KIMMY-LABEL-BATCH.json"

sys.path.insert(0, str(Path(r"D:\GitHub\Python-WEB")))
from label_elements import (  # noqa: E402
    ARCHIVE_ROOT,
    SITE_ROOT,
    VISUAL_DIR,
    apply_one,
    detect_page_role,
    label_text,
    load_rules,
)


def main() -> int:
    # Point label_elements at site-v2 for this run
    import label_elements as le

    le.SITE_ROOT = ROOT
    le.VISUAL_DIR = ROOT / "_visual"
    le.RULES_FILE = le.VISUAL_DIR / "label_rules.json"
    le.UNKNOWNS_FILE = UNKNOWNS
    le.ARCHIVE_ROOT = ROOT / "_site_archives" / "labeling"

    paths = json.loads(MANIFEST.read_text(encoding="utf-8"))["folder_balanced_article_split"]["Cursor"]["paths"]
    rules = load_rules()
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    changed = blocked = unchanged = 0
    all_unknowns: Counter = Counter()
    touched: list[str] = []

    for rel in paths:
        p = ROOT / Path(rel)
        if not p.exists():
            continue
        status, roles, unknowns, did_change = apply_one(p, rules, True, True, run_stamp)
        if did_change:
            changed += 1
            touched.append(rel)
        elif unknowns:
            blocked += 1
        else:
            unchanged += 1
        all_unknowns.update(unknowns)

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "lane": "Kimmy (Cursor manifest batch)",
        "pages": len(paths),
        "changed": changed,
        "unchanged": unchanged,
        "had_unknowns": blocked,
        "distinct_unknown_tokens": len(all_unknowns),
        "top_unknowns": [{"class": t, "count": n} for t, n in all_unknowns.most_common(40)],
        "touched_sample": touched[:20],
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    UNKNOWNS.parent.mkdir(parents=True, exist_ok=True)
    UNKNOWNS.write_text(
        json.dumps(
            {
                "generated": payload["generated"],
                "unknown_count": len(all_unknowns),
                "unknowns": payload["top_unknowns"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps({k: payload[k] for k in ("pages", "changed", "unchanged", "had_unknowns", "distinct_unknown_tokens")}, indent=2))
    print(f"report: {REPORT}")
    print(f"unknowns: {UNKNOWNS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
