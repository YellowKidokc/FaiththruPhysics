# Current State

## What is already true

- The site already has an MTL Cloudflare worker project.
- Many live pages already load `shared/js/mtl-worker-client.js`.
- `consciousness` has heavy embedded math and is a valid MTL target now.
- `one-page-stories` mostly has MathJax wiring but very little real embedded math markup.

## Recent fix

`shared/js/mtl-worker-client.js` was patched so that:

- shell mode `math` maps to MTL mode `standard`
- global reader-mode changes rerender equations
- old worker callouts are cleared before rerender
- `academic` and `proof` stop showing worker callout translations

## D1 deployment state

- The live D1 database `faiththruphysics-mtl` is reachable through Wrangler.
- A safe `consciousness` subset was uploaded from the normalized workbook.
- The upload updated `EQ-001` through `EQ-010` in place and tagged them with:
  - `source = mtl_workbook_normalized_safe_rows`

Import artifacts:

- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-d1-import\safe_d1_import.sql`
- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-d1-import\safe_d1_rows.json`
- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-d1-import\safe_d1_needs_review_rows.json`

## Current limitation

The worker still returns one translation string per equation. That is enough for a first-pass readable layer, but not enough for the richer target model:

- canonical form
- structure-preserving reading
- key parts
- why it matters

That richer model will require a structured payload and a better renderer.

## Coverage reality

The worker path is live, but coverage is still incomplete.

Active-site audit summary:

- `820` active-ish pages scanned
- `413` pages load the worker client
- `128` pages contain equations
- `122` equation pages still have at least one missing translation
- `1319` equation instances are still uncovered in D1

Coverage report:

- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_coverage_summary.md`
