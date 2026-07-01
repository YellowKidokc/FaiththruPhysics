# Series shell themes

Reference copies of per-series `_TEMPLATE.html` shells. **Live source of truth** stays on the site:

| Theme | Accent | Live template |
|-------|--------|---------------|
| [revolution-of-truth-gold](revolution-of-truth-gold/README.md) | `#d4af37` gold | `revolution-of-truth/_TEMPLATE.html` |
| [consciousness-teal](consciousness-teal/README.md) | `#14b8a6` teal | `consciousness/_TEMPLATE.html` |

When you change a theme, edit the **live** `{series}/_TEMPLATE.html`, rebuild with `top_bar_bottom_bar.py`, then refresh the copy here so this folder stays a color/style museum.

## Excel vs API JSON (target workflow)

Ideal path for verified bar, domains, audit foot, and claims:

1. Structural API stations (or evaluation workbook) produce metrics
2. **Excel workbook** per article (`build_article_evaluation_workbook.py`)
3. `excel_to_site_json.py` → `data-viz/`, `rigor/`, `claims/`, `editorial/`
4. `top_bar_bottom_bar.py` injects shell + reading levels; verification bar loads JSON at runtime

Consciousness currently has API JSON in `faiththruphysics-site-data/{raw-metrics,framework-alignment,justice-mercy,knowledge-graph}/consciousness/`. That is valid staging data; Excel merge can come next when you want one workbook per paper instead of scattered station outputs.

## Adding a new series theme

1. Copy `revolution-of-truth-gold/_TEMPLATE.html` → `{series}/_TEMPLATE.html`
2. Swap `--gold` tokens and `body` class (`series-{slug}`)
3. Add scoped overrides in `components/top-bar-bottom-bar.css` if shared chrome still shows gold rgba
4. Extend `top_bar_bottom_bar.py` with `SERIES_PAGE_ORDER` + nav titles
5. Mirror the finished template into `themes/{series-name}/` with a README
