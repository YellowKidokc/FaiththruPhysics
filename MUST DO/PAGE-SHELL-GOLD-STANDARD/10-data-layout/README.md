# 10 — Data Layout

Where content and metrics live.

## Site repo (`faiththruphysics-site`)

```
revolution-of-truth/
  _TEMPLATE.html          ← per-series shell template
  drv-00-the-argument.html
  ...
components/
  top-bar-bottom-bar.css
  reading-levels.js
  verification-bar.js
  tp-header-lip.js
data-viz/                 ← copy verification JSON here for deploy
```

## Data repo (`faiththruphysics-site-data`)

```
revolution-of-truth/
  *.canonical.md          ← College
  highschool/
  phd/
  _evaluation/            ← analyzer runs (not source markdown)
data-viz/
rigor/
claims/
editorial/
APIs/revolution-of-truth-pipeline/
```

## Do not overwrite

Canonical `.canonical.md` files are **source**. Analyzer outputs go in `_evaluation/` or pipeline `outbox/`.

## Reading level rule

| Tier | Folder | Audience |
|------|--------|----------|
| High School | `highschool/` | Accessible |
| College | series root | Default / main |
| PhD | `phd/` | Formal + claims |
