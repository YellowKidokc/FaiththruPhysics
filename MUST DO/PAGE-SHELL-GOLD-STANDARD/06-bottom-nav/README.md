# 06 — Bottom Navigation

Big prev/next cards + series home + sub-series strip.

## What it contains

- **Prev card** — prior chapter title + teaser
- **Next card** — next chapter
- **Series home** — link to series index
- **Sub-series strip** — related hubs (Proof, Logos Papers, etc.)

## Builder

`top_bar_bottom_bar.py` sets prev/next from series order in canonical index or workbook `01_Article_Identity`.

## Styles

`components/top-bar-bottom-bar.css` — `.tp-bignav-*`, `.tp-sub-card`, hover glow

## Bug fixed

Nav title regex octal escape — see `01-top-bar/README.md`.
