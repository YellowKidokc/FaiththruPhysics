# 01 — Top Bar

Fixed header on every article page.

## What it contains

- **Brand** — χ + Faith thru Physics → faiththruphysics.com
- **Nav links** — Home, MTL (equation), Proof Explorer
- **Series lip toggle** — opens header lip (classification + series grid)
- **Reading levels** — High School | College | PhD tabs
- **Search** — placeholder (⌘K)

## Live files

| File | Role |
|------|------|
| `revolution-of-truth/_TEMPLATE.html` | HTML structure (`.tp-top`, `.tp-levels`) |
| `components/top-bar-bottom-bar.css` | Top bar + lip + article + bottom nav styles |
| `components/tp-header-lip.css` | Lip dropdown styling |
| `components/tp-header-lip.js` | Series grid cards in lip |

## Builder injection

`top_bar_bottom_bar.py` reads `_TEMPLATE.html` and injects:

- Series name, page title, prev/next slugs
- `data-verification-slug` on verified bar
- Per-page audio block attributes

## Bugs fixed (drv-00)

| Bug | Fix |
|-----|-----|
| Nav title `A The Architecture` | Lambda `re.sub` — avoid `\101` octal in replacement |

## Verify

Local: `http://127.0.0.1:8765/revolution-of-truth/drv-00-the-argument.html`  
Check: lip opens, level tabs switch panels, brand link works.
