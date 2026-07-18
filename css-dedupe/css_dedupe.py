"""CSS dedupe lookup for migrate_canonical_shell.py — exact-match-or-keep.

Approved by David 2026-07-18: strip duplicated inline CSS from all in-scope
families (isomorphism excluded) by replacing style blocks that byte-match a
promoted shared file with a <link> to that file. Non-matching blocks are NEVER
stripped — they stay on the page, scoped by the migrator's existing scoper.

This module makes no decisions about scoping and contains no scoper: promotion
of the shared files through the migrator's scope_legacy_css() (single source of
truth) happens once at integration time. Do not write a second scoper.

Usage inside the migrator, while disassembling a page:

    from css_dedupe import load_table, match_block

    table = load_table(Path("css-dedupe/dedupe_table.json"))
    for block in inline_style_blocks:          # raw inner CSS text
        hit = match_block(table, block)
        if hit:
            emit_link(hit["deploy_path"])      # same cascade position
        else:
            keep_scoped(block)                 # existing behavior, unchanged
"""

import hashlib
import json
import re
from pathlib import Path


def normalize(css_text: str) -> str:
    """Whitespace-insensitive canonical form. Must stay in lockstep with the
    normalization used to build dedupe_table.json (collapse runs of whitespace
    to a single space, trim)."""
    return re.sub(r"\s+", " ", css_text).strip()


def block_hash(css_text: str) -> str:
    return hashlib.sha1(normalize(css_text).encode("utf-8")).hexdigest()[:12]


def load_table(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["blocks"]


def match_block(table: dict, css_text: str):
    """Return the table entry for an exactly-matching promoted block, else None.
    None means KEEP the block on the page (scoped) — never strip on a miss."""
    return table.get(block_hash(css_text))


def link_tag(entry: dict) -> str:
    return f'<link rel="stylesheet" href="{entry["deploy_path"]}">'
