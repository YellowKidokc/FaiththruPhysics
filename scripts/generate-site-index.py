#!/usr/bin/env python3
"""Generate a lightweight index of section landing pages."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site-index.html"
EXCLUDE_PARTS = {
    ".git",
    ".wrangler",
    "node_modules",
    "reports",
    "work",
    "_trash_review",
    "_link-fix-backups",
    "_inject_backups",
    "MUST DO",
    "Templates David",
}


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDE_PARTS for part in rel.parts):
        return False
    return path.name.lower() == "index.html"


def title_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.parts == ("index.html",):
        return "Home"
    parts = list(rel.parts[:-1])
    return " / ".join(part.replace("-", " ").replace("_", " ").title() for part in parts)


def href_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    return "/" + rel.removesuffix("index.html")


def main() -> int:
    pages = sorted((p for p in ROOT.rglob("index.html") if should_include(p)), key=lambda p: href_for(p))
    cards = "\n".join(
        f'<a class="card" href="{html.escape(href_for(page))}"><span>{html.escape(href_for(page))}</span><strong>{html.escape(title_for(page))}</strong></a>'
        for page in pages
    )
    OUT.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Full Site Index - Faith Through Physics</title>
<meta name="description" content="Generated index of Faith Through Physics section landing pages.">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/assets/faith-topbar.css">
<script defer src="/assets/faith-topbar.js"></script>
<style>
body{{margin:0;background:#050505;color:#e5e3df;font-family:Inter,system-ui,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:4rem 1.25rem 5rem}}
h1{{font-family:Georgia,serif;font-weight:400;font-size:clamp(2.2rem,5vw,4rem);margin:0 0 .7rem;color:#fff}}
p{{max-width:760px;color:#aaa;line-height:1.7}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.75rem;margin-top:2rem}}
.card{{display:flex;flex-direction:column;gap:.35rem;min-height:92px;padding:1rem;border:1px solid #242424;border-radius:8px;background:#101010;color:inherit;text-decoration:none}}
.card:hover{{border-color:#d4af37;background:rgba(212,175,55,.06)}}
.card span{{font:600 .68rem ui-monospace,monospace;color:#d4af37;word-break:break-word}}
.card strong{{font-family:Georgia,serif;font-size:1.15rem;font-weight:400;color:#fff}}
</style>
</head>
<body>
<main>
<h1>Full Site Index</h1>
<p>Generated doorway to the section landing pages currently present in the site repository.</p>
<section class="grid" aria-label="Generated site index">
{cards}
</section>
</main>
</body>
</html>
""",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {OUT} with {len(pages)} section links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
