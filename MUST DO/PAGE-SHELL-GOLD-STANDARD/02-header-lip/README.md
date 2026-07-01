# 02 — Header Lip (Classification Row)

Dropdown panel attached to the top bar.

## What it contains

1. **Article classification row** — colored domain meter (100% bar) + tag dots
2. **Prev / Next** — chapter navigation in lip
3. **Series grid** — cards to other series (Genesis to Quantum, MDA, etc.)

## Data source

Domain meter and pills come from **frontmatter** on High School canonical (or domain-scan JSON):

```yaml
domains:
  Information Theory: 25
  Physics: 20
  Theology: 20
```

Injected as `ARTICLE_PROFILE` in page HTML by `top_bar_bottom_bar.py`.

## Live files

- `components/tp-header-lip.js` — `SERIES_CARDS` list + lip open/close
- `components/top-bar-bottom-bar.css` — `.tp-class-*`, `.tp-subdomain-grid`

## Future

- **Graph** link (Site | Classifier | Papers | Graph) — series knowledge graph from evaluation pipeline
- Classifier link → proof-explorer / fp-005 tabs
