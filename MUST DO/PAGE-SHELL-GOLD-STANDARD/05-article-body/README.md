# 05 — Article Body (College Enrichment)

Main content area between verified bar and bottom nav.

## CSS-only (College scoped)

Scoped with `[data-reading-level="college"]` in `top-bar-bottom-bar.css`:

- Drop caps on first paragraph
- Rotating h2 styles (3 variants)
- Blockquote callouts
- Table cards
- References `.tp-refs` hanging indent (all levels)

## Python markup (`college_enrich.py`)

| Class | What |
|-------|------|
| `.tp-eqcard` | Standalone `$$…$$` equations + optional label |
| `.tp-feature-1` … `.tp-feature-5` | Creative boxes on punchy paragraphs (every other section) |

## Shared HTML (`article_html.py`)

- Strip YAML frontmatter
- Markdown → HTML (tables, fenced code)
- Wrap each `##` in `<section>`
- Tag References section as `class="tp-refs"`

## Commands

```bash
python college_enrich.py --series revolution-of-truth --audit
python college_enrich.py --series revolution-of-truth --slug drv-00-the-argument
```

## Math Translation Layer (optional per equation)

See `MUST DO/math-translation-layer/` — in-article `.mtl-callout` blocks, not the deprecated overlay.
