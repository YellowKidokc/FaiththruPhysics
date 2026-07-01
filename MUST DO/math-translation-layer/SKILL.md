---
name: math-translation-layer
description: "Audit, wire, and extend the Faith Through Physics Math Translation Layer. Use when working on equation extraction, MTL reader behavior, Cloudflare worker translation flow, series-by-series math inventory, or page-level equation callouts in faiththruphysics-site. This skill is for the current live stack: site HTML, shared/js/mtl-worker-client.js, shared/js/mtl-equation.js, the workers/mtl-service Cloudflare Worker, and series sweeps such as consciousness, one-page-stories, or revolution-of-truth."
---

# Math Translation Layer

Use this folder as the active MTL workspace inside the site repo.

## Core model

- Keep the canonical equation visible.
- Put the translation block immediately after the equation or sentence it belongs to.
- Preserve equation structure in words instead of paraphrasing loosely.
- Scale the explanation by equation complexity.
- Keep `definition`, `equation`, and `claim` as separate layers even when they touch the same content.

## Current live stack

- Worker project: `D:\GitHub\faiththruphysics-site\workers\mtl-service`
- Worker client in pages: `D:\GitHub\faiththruphysics-site\shared\js\mtl-worker-client.js`
- Reader/callout system: `D:\GitHub\faiththruphysics-site\shared\js\mtl-equation.js`
- Old overlay path still exists: `D:\GitHub\faiththruphysics-site\shared\js\mtl-overlay.js`
- Local uploader app: `D:\GitHub\faiththruphysics-site-data\mtl-admin\mtl_uploader.pyw`

Read [references/cloudflare-worker-map.md](references/cloudflare-worker-map.md) before changing the worker flow.
Read [references/current-state.md](references/current-state.md) before changing page behavior.

## Working rules

- Treat the worker path as the current runtime translation path unless a page is still hard-wired to the old overlay.
- Do not assume a series has usable equations; sweep it first with `scripts/extract_series_math.py`.
- Prefer one canonical page per article. Wrapped/unwrapped duplicates need explicit review.
- For first-pass audits, do not delete or flatten anything.

## Fast workflow

### 1. Sweep a series

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_series_math_scan.ps1 -SeriesRoot "D:\GitHub\faiththruphysics-site\consciousness"
```

Outputs go under:

```text
D:\GitHub\faiththruphysics-site\reports\<series-name>-math
```

Read:

- `series_math_summary.md`
- `series_math_missing_math.csv`
- `series_math_high_density_files.csv`
- `series_math_duplicates.csv`

### 2. Decide what kind of problem it is

- `0 equations` in a page: missing markup or nonstandard equation structure
- `many duplicates`: likely wrapped/unwrapped copies or repeated formula reuse
- `worker present but weak output`: renderer/schema problem, not extraction problem

### 3. Change the right layer

- Extraction/inventory problem: use `scripts/extract_series_math.py`
- Reader mode or page rerender problem: edit `shared/js/mtl-worker-client.js`
- Static callout rendering problem: edit `shared/js/mtl-equation.js` or related CSS
- Cloudflare translation/API problem: edit `workers/mtl-service/src/index.js`

## Bundled scripts

- `scripts/extract_series_math.py`
  Batch equation extractor with JSON/CSV/summary output.
- `scripts/run_series_math_scan.ps1`
  Wrapper that runs the extractor and writes reports into the site repo.
- `scripts/summarize_active_math_surface.py`
  Filters full-site scan output down to the likely live/public math surface.
- `scripts/normalize_mtl_workbook.py`
  Converts an MTL workbook into normalized records plus separate `needs_review` rows.
- `scripts/export_safe_rows_to_d1.py`
  Builds a D1-ready SQL/JSON import package from safe normalized rows only.
- `scripts/audit_mtl_site_coverage.py`
  Compares live site equations against the D1 hash set and reports full/partial/missing coverage.

## References

- `references/cloudflare-worker-map.md`
  Cloudflare worker name, API, D1 binding, and how runtime translation currently works.
- `references/current-state.md`
  What is already working, what is mixed/legacy, and what was recently patched.
- `references/targets.md`
  Current high-value series and what to do next.

## High-value next moves

- Build one flagship MTL page in `consciousness`.
- Sweep `revolution-of-truth` and classify its equation density.
- Move toward structured MTL output for `small`, `medium`, and `large` equations instead of one flat translation string.

## Current operational state

- Safe `consciousness` subset uploaded to live D1:
  - `10` rows tagged as `mtl_workbook_normalized_safe_rows`
- Current remote D1 size observed during audit:
  - `705` rows in `mtl_equations`
- Full-site active coverage audit exists:
  - `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit`

## What the latest audit says

- `consciousness` is the strongest live series right now.
- `revolution-of-truth` has substantial math but weak D1 coverage and needs an import pass.
- `genesis-to-quantum` is still the largest remaining equation backlog after excluding obvious backup/mirror surfaces.
- Some pages already have equations present in D1 but do not load the worker client. Those are low-hanging wiring fixes.

Read `references/current-state.md` and `references/targets.md` before choosing the next move.
