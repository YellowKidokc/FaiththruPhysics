# MTL Worker And Audit Map

## Runtime path

- Worker folder: `D:\GitHub\faiththruphysics-site\workers\mtl-service`
- Config: `workers\mtl-service\wrangler.jsonc`
- Entry: `workers\mtl-service\src\index.js`
- Worker base URL: `https://faith-mtl-worker.davidokc28.workers.dev`
- D1 binding: `DB`
- D1 database: `faiththruphysics-mtl`

## Runtime API

- `GET /health`
- `GET /api/translate?latex=...&mode=easy|standard|academic|audio_safe`
- `POST /api/batch`

## Live site client

- Site client file: `D:\GitHub\faiththruphysics-site\shared\js\mtl-worker-client.js`
- The client collects MathJax-rendered equations, batches them to the worker, and inserts translation callouts after rendered math.

## Important split

There are two MTL systems in the repo.

### Current worker path

- `workers/mtl-service`
- `shared/js/mtl-worker-client.js`

Use this path for new runtime translation work.

### Legacy overlay path

- `shared/js/mtl-overlay.js`
- `shared/js/mtl-overlay-loader.js`
- `shared/data/mtl-overlay-translations.json`
- `faiththruphysics-site-data\\mtl-admin\\mtl_uploader.pyw`

Treat this as legacy unless there is a specific reason to revive it.

## Repeatable audit scripts

Working script folder:

- `D:\GitHub\faiththruphysics-site\MUST DO\math-translation-layer\scripts`

Primary scripts:

- `extract_series_math.py`
- `run_series_math_scan.ps1`
- `summarize_active_math_surface.py`
- `normalize_mtl_workbook.py`
- `export_safe_rows_to_d1.py`
- `audit_mtl_site_coverage.py`

## Key report outputs

- `D:\GitHub\faiththruphysics-site\reports\faiththruphysics-site-math-active\active_math_summary.md`
- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_coverage_summary.md`
- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_page_status.csv`
- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_missing_equations.csv`
- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-workbook-normalized\`
- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-d1-import\`

## Safe operating rule

Only move safe rows into D1 on the first pass. Keep `needs_review` fully separate. Do not let ambiguous rows get swept into the live translation surface.
