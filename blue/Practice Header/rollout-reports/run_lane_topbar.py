#!/usr/bin/env python3
"""Prep or inject topbar for manifest lane(s)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(r"D:\GitHub\faiththruphysics-site-v2")
MANIFEST = ROOT / "blue" / "Practice Header" / "ai-article-rollout-split.json"
sys.path.insert(0, str(ROOT / "scripts"))


def paths_for_lanes(lanes: list[str]) -> list[str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))["folder_balanced_article_split"]
    out: list[str] = []
    for lane in lanes:
        out.extend(data[lane]["paths"])
    return out


def run_prep(lanes: list[str], apply: bool) -> None:
    import prepare_topbar_pages as prep

    changed = skipped = missing = 0
    for rel in paths_for_lanes(lanes):
        path = ROOT / Path(rel)
        if not path.exists():
            missing += 1
            continue
        original = prep.read_text(path)
        if "FTP_TOPBAR_PREP:START" in original:
            skipped += 1
            continue
        updated, actions = prep.prepare_html(original)
        if not actions or updated == original:
            skipped += 1
            continue
        changed += 1
        if apply:
            prep.backup_file(path, ROOT)
            path.write_text(updated, encoding="utf-8", newline="")
        safe = rel.encode("ascii", "backslashreplace").decode("ascii")
        print(f"[PREP{'-APPLY' if apply else ''}] {safe}: {', '.join(actions)}")
    print(f"[PREP DONE] lanes={lanes} changed={changed} skipped={skipped} missing={missing}")


def run_inject(lanes: list[str], apply: bool) -> None:
    import inject_topbar as inj

    changed = skipped = missing = 0
    for rel in paths_for_lanes(lanes):
        path = ROOT / Path(rel)
        if not path.exists():
            missing += 1
            continue
        original = inj.read_text(path)
        if "FTP_TOPBAR_ASSETS:START" in original:
            skipped += 1
            continue
        updated, actions = inj.inject_assets(original)
        if not actions or updated == original:
            skipped += 1
            continue
        changed += 1
        if apply:
            inj.backup_file(path, ROOT)
            path.write_text(updated, encoding="utf-8", newline="")
        safe = rel.encode("ascii", "backslashreplace").decode("ascii")
        print(f"[INJECT{'-APPLY' if apply else ''}] {safe}: {', '.join(actions)}")
    print(f"[INJECT DONE] lanes={lanes} changed={changed} skipped={skipped} missing={missing}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prep", "inject"])
    parser.add_argument("--lanes", default="Claude,Kimmy", help="Comma-separated lane names")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    lanes = [x.strip() for x in args.lanes.split(",") if x.strip()]
    if args.action == "prep":
        run_prep(lanes, args.apply)
    else:
        run_inject(lanes, args.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
