#!/usr/bin/env python3
"""Count site-v2 HTML pages and split across 4 AIs."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"D:\GitHub\faiththruphysics-site-v2")
OUT = ROOT / "blue" / "Practice Header" / "ai-page-split.json"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".wrangler", "backups", "trash_review", "_trash_review", "work"}
EXCLUDE_TOP = {"Double Check", "_archive", "prototypes", "redirects", "_site_archives"}
AIS = ["Claude", "Gemini", "Cursor", "Kimmy"]


def collect(exclude_review: bool) -> list[Path]:
    pages: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".html", ".htm"}:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        rel = p.relative_to(ROOT)
        if exclude_review and rel.parts and rel.parts[0] in EXCLUDE_TOP:
            continue
        pages.append(p)
    pages.sort(key=lambda x: str(x).lower())
    return pages


def alpha_split(pages: list[Path]) -> dict[str, list[str]]:
    n = len(pages)
    q, r = divmod(n, 4)
    out: dict[str, list[str]] = {}
    i = 0
    for idx, name in enumerate(AIS):
        size = q + (1 if idx < r else 0)
        chunk = pages[i : i + size]
        out[name] = [str(p.relative_to(ROOT)).replace("\\", "/") for p in chunk]
        i += size
    return out


def folder_split(pages: list[Path]) -> dict[str, dict]:
    by_folder: dict[str, list[Path]] = defaultdict(list)
    for p in pages:
        rel = p.relative_to(ROOT)
        top = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        by_folder[top].append(p)

    bins = [{"name": name, "folders": [], "count": 0, "paths": []} for name in AIS]
    for fname, flist in sorted(by_folder.items(), key=lambda x: (-len(x[1]), x[0])):
        target = min(bins, key=lambda b: b["count"])
        target["folders"].append({"folder": fname, "pages": len(flist)})
        target["count"] += len(flist)
        target["paths"].extend(str(p.relative_to(ROOT)).replace("\\", "/") for p in sorted(flist))

    return {b["name"]: {"page_count": b["count"], "folders": b["folders"], "paths": b["paths"]} for b in bins}


def main() -> None:
    all_pages = collect(exclude_review=False)
    live_pages = collect(exclude_review=True)

    payload = {
        "site_root": str(ROOT),
        "totals": {
            "all_html_in_repo": len(all_pages),
            "live_site_excludes": sorted(EXCLUDE_TOP),
            "live_site_pages": len(live_pages),
            "per_ai_if_even_split_live": len(live_pages) // 4,
            "remainder_live": len(live_pages) % 4,
        },
        "notes": {
            "double_check": "4475+ pages — review/duplicate corpus; excluded from live_site split",
            "recommended_split": "folder_balanced for live site; alpha_split for full repo inventory",
        },
        "alpha_split_full_repo": {k: {"page_count": len(v), "first": v[0] if v else None, "last": v[-1] if v else None} for k, v in alpha_split(all_pages).items()},
        "folder_balanced_live_site": folder_split(live_pages),
        "alpha_split_live_site": {k: {"page_count": len(v), "first": v[0] if v else None, "last": v[-1] if v else None} for k, v in alpha_split(live_pages).items()},
    }

    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["totals"], indent=2))
    print("\nFOLDER-BALANCED LIVE SITE:")
    for name, block in payload["folder_balanced_live_site"].items():
        folders = ", ".join(f"{f['folder']}({f['pages']})" for f in block["folders"])
        print(f"  {name}: {block['page_count']} — {folders}")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
