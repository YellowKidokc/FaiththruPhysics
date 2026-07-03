#!/usr/bin/env python3
"""Inject topbar assets on all Cursor manifest paths."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"D:\GitHub\faiththruphysics-site-v2")
sys.path.insert(0, str(ROOT / "scripts"))
import inject_topbar as inj  # noqa: E402

MANIFEST = ROOT / "blue" / "Practice Header" / "ai-article-rollout-split.json"


def main() -> int:
    paths = json.loads(MANIFEST.read_text(encoding="utf-8"))["folder_balanced_article_split"]["Cursor"]["paths"]
    changed = skipped = missing = 0
    for rel in paths:
        path = ROOT / Path(rel)
        if not path.exists():
            print(f"[MISSING] {rel}")
            missing += 1
            continue
        original = inj.read_text(path)
        updated, actions = inj.inject_assets(original)
        if not actions or updated == original:
            skipped += 1
            continue
        inj.backup_file(path, ROOT)
        path.write_text(updated, encoding="utf-8", newline="")
        changed += 1
        safe = rel.encode("ascii", "backslashreplace").decode("ascii")
        print(f"[CHANGE] {safe}: {', '.join(actions)}")
    print(f"[DONE] changed={changed} skipped={skipped} missing={missing} total={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
