#!/usr/bin/env python3
"""
register_series_default.py - register one shared "series default" audio track
against every page in a folder, so pages without dedicated media inherit it.

How it works
------------
The site pill player / audio dock asks the worker:  /api/audio?slug=<page-slug>
The worker falls back to the row with is_default=1 for that slug. This script
creates that default row for EVERY page in a folder, all pointing at the SAME
already-hosted URL (one file in R2, many catalog rows -- names stay canonical).

USAGE
-----
  # Dry run: show which slugs would get the default (no writes)
  python register_series_default.py --folder "D:\\GitHub\\faiththruphysics-site\\one-page-stories\\Templeton" \
      --series one-page-stories \
      --mode tts --url https://faith-audio-pipeline.davidokc28.workers.dev/audio/generated/one-page-stories/templeton-default/tts.mp3 \
      --title "Templeton Series Overview"

  # Apply
  ... same ... --apply

  # Several modes at once (repeat --mode/--url/--title triplets via --track)
  python register_series_default.py --folder ... --series ... \
      --track tts=https://.../tts.mp3 --track deep-dive=https://.../deep-dive.mp3 --apply

Slug resolution per page: data-audio-slug attribute if present, else the
file name stem lowercased (matching the worker's cleanSlug convention).
Pages that already have a NON-default track for that mode are left alone
(the worker prefers exact slug+mode matches anyway; is_default row is only
the fallback). Existing default rows for a slug+mode are overwritten by the
worker's upsert.

Token: reads admin-token.local.secret next to this script, or
FAITH_AUDIO_ADMIN_TOKEN env var.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

WORKER_BASE = "https://faith-audio-pipeline.davidokc28.workers.dev"
SCRIPT_DIR = Path(__file__).parent

AUDIO_SLUG_RE = re.compile(r'data-audio-slug="([^"]+)"')
SKIP_NAMES = {"index.html", "_template.html"}


def admin_token() -> str:
    env = os.environ.get("FAITH_AUDIO_ADMIN_TOKEN")
    if env:
        return env.strip()
    secret = SCRIPT_DIR / "admin-token.local.secret"
    if secret.exists():
        return secret.read_text(encoding="utf-8").strip()
    sys.exit("No admin token: set FAITH_AUDIO_ADMIN_TOKEN or create admin-token.local.secret")


def page_slug(path: Path) -> str:
    try:
        html = path.read_text(encoding="utf-8", errors="replace")
        m = AUDIO_SLUG_RE.search(html)
        if m:
            return m.group(1).strip().lower()
    except OSError:
        pass
    return re.sub(r"[^a-z0-9._-]+", "-", path.stem.lower()).strip("-")


def collect_slugs(folder: Path) -> list[tuple[Path, str]]:
    pages = []
    for f in sorted(folder.rglob("*.html")):
        if f.name.lower() in SKIP_NAMES or ".bak" in f.name:
            continue
        pages.append((f, page_slug(f)))
    return pages


def existing_tracks(slug: str) -> list[dict]:
    url = f"{WORKER_BASE}/api/audio?slug={urllib.parse.quote(slug)}"
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("tracks") or []
    except Exception:  # noqa: BLE001
        return []


def register(token: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{WORKER_BASE}/api/register",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    p = argparse.ArgumentParser(description="Bulk-register a series default audio track.")
    p.add_argument("--folder", required=True, help="Folder of HTML pages")
    p.add_argument("--series", required=True, help="Canonical series slug")
    p.add_argument("--mode", default=None, help="Track mode (tts, debate, deep-dive, critique)")
    p.add_argument("--url", default=None, help="Already-hosted audio URL (single-track form)")
    p.add_argument("--title", default=None, help="Track title shown in the player")
    p.add_argument("--track", action="append", default=[],
                   help="mode=url pair; repeatable for multiple modes")
    p.add_argument("--all-pages", action="store_true",
                   help="Register default for every page, even ones that "
                        "already have their own tracks (default: skip covered)")
    p.add_argument("--report", action="store_true",
                   help="Coverage report only: list pages with/without audio")
    p.add_argument("--apply", action="store_true", help="Write (default dry-run)")
    args = p.parse_args()

    tracks: list[tuple[str, str]] = []
    if args.mode and args.url:
        tracks.append((args.mode, args.url))
    for t in args.track:
        mode, _, url = t.partition("=")
        if not url:
            sys.exit(f"Bad --track (expected mode=url): {t}")
        tracks.append((mode.strip(), url.strip()))
    if not tracks and not args.report:
        sys.exit("No tracks given: use --mode/--url or --track mode=url (or --report)")

    folder = Path(args.folder)
    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")

    pages = collect_slugs(folder)

    if args.report:
        covered = uncovered = 0
        print(f"[REPORT] {len(pages)} pages in {folder.name}\n")
        for path, slug in pages:
            tr = existing_tracks(slug)
            if tr:
                covered += 1
                modes = ",".join(sorted({t.get("mode", "?") for t in tr}))
                print(f"  + {slug}  ({modes})")
            else:
                uncovered += 1
                print(f"  x {slug}  NO AUDIO")
        print(f"\nCovered: {covered}   Uncovered: {uncovered}")
        return

    mode_str = ", ".join(m for m, _ in tracks)
    print(f"[{'APPLY' if args.apply else 'DRY-RUN'}] {len(pages)} pages in {folder.name} "
          f"-> default modes: {mode_str}\n")

    token = admin_token() if args.apply else ""
    ok = failed = skipped = 0
    for path, slug in pages:
        if not args.all_pages and existing_tracks(slug):
            skipped += 1
            print(f"  = {slug}  has own audio, skipped")
            continue
        for mode, url in tracks:
            line = f"  {slug}  [{mode}]"
            if not args.apply:
                print(f"{line}  would register default")
                continue
            payload = {
                "slug": slug,
                "series": args.series,
                "mode": mode,
                "url": url,
                "title": args.title or f"{args.series} overview",
                "isDefault": True,
            }
            try:
                register(token, payload)
                ok += 1
                print(f"{line}  registered")
            except Exception as e:  # noqa: BLE001
                failed += 1
                print(f"{line}  FAILED: {e}")

    if args.apply:
        print(f"\nDone: {ok} registered, {failed} failed, {skipped} skipped (own audio)")
    else:
        print(f"\nDry-run only ({skipped} skipped with own audio). Add --apply to write.")


if __name__ == "__main__":
    main()
