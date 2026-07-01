# drv-00 Gold Standard Checklist

Use before propagating shell to other series.

## Shell

- [x] Top bar: brand, nav, lip, level tabs
- [x] Scroll chrome: compact to levels + score badges on scroll
- [x] Domain meter sums to 100%
- [x] Verified bar loads JSON on drv-00 (not em dashes)
- [x] Prev/next nav titles correct (no `A The Architecture` bug)

## Reading levels

- [x] High School panel loads
- [x] College panel loads with enrichment
- [x] PhD panel loads

## College visuals

- [x] Drop caps visible
- [x] Equation cards on standalone math
- [x] Feature boxes on alternate sections
- [x] References compact numbered list

## Math

- [x] Inline math renders (not red raw `\(` text)
- [x] Display math renders

## Bottom

- [x] Big prev/next cards
- [x] Audit foot shows rigor JSON when present (drv-00)

## Series home

- [x] Framework Snapshot (4 boxes: Axioms, Laws, Bridges, Claims)

## Data

- [x] Three `.canonical.md` files exist (college, hs, phd)
- [x] `verification-revolution-of-truth-drv-00-the-argument.json` in site `data-viz/`
- [ ] `excel_to_site_json.py --apply` for drv-01 … drv-06 when workbook filled
- [ ] Analyzer outputs reviewed in `_evaluation/` for remaining pages

## Propagate (revolution-of-truth — done 2026-06-29)

```bash
cd D:\GitHub\Python-WEB
python top_bar_bottom_bar.py --series revolution-of-truth --apply
```

All 6 pages rebuilt with `tp-scroll-chrome.js`.

## Next series

Copy `_TEMPLATE.html` + run same build pipeline. Point `data-verification-slug` per page.
