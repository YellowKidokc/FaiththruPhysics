# Math Translation Layer Current State

## Purpose

This knowledge note is the durable operating snapshot for the Math Translation Layer (MTL) effort across the live site and the supporting Cloudflare/D1 path.

## Current architecture

- Live site repo: `D:\GitHub\faiththruphysics-site`
- Working MTL folder: `D:\GitHub\faiththruphysics-site\MUST DO\math-translation-layer`
- Runtime worker project: `D:\GitHub\faiththruphysics-site\workers\mtl-service`
- Canonical worker name: `faith-mtl-worker`
- Canonical D1 database: `faiththruphysics-mtl`

## What is already live

- The site already has an MTL Cloudflare worker path.
- Many live pages already load `shared/js/mtl-worker-client.js`.
- `shared/js/mtl-worker-client.js` was patched so shell mode `math` maps to MTL mode `standard`.
- Reader mode changes now trigger equation rerendering.
- Old worker callouts are cleared before rerender.
- `academic` and `proof` no longer show worker callout translations.

## D1 status

- Live D1 is reachable through Wrangler.
- A safe `consciousness` subset was normalized and uploaded.
- `EQ-001` through `EQ-010` were updated in place.
- Current safe import source tag: `mtl_workbook_normalized_safe_rows`

## Coverage reality

Latest D1-backed site audit:

- `820` active-ish pages scanned
- `413` pages load the worker client
- `128` pages contain equations
- `122` equation pages still have at least one missing translation
- `1319` equation instances are still uncovered in D1

Status counts:

- `full_coverage`: `5`
- `partial_coverage`: `33`
- `worker_client_but_zero_matches`: `57`
- `db_ready_but_page_not_wired`: `14`
- `worker_client_but_no_equations`: `318`
- `no_equations`: `374`

## Best current series targets

### Consciousness

- `22` HTML files
- `17` files with extracted math
- `626` extracted equations

Best near-finish pages:

- `consciousness-chi-field-action.html`: `141` equations, `120` found, `21` missing
- `consciousness-grace-source-term.html`: `101` equations, `81` found, `20` missing
- `consciousness-reality-assessment.html`: `98` equations, `41` found, `57` missing

### Revolution of Truth

- `8` HTML files
- `173` extracted equations
- coverage is still weak

Most obvious backlog pages:

- `drv-00-the-argument.html`: `58` equations, `1` found, `57` missing
- `drv-02-the-lock.html`: `48` equations, `0` found, `48` missing
- `drv-01-the-architecture.html`: `17` equations, `0` found, `17` missing

### Genesis to Quantum

- `415` uncovered equation instances in the current active-surface audit
- largest remaining active backlog lane

## Current limitation

The current worker response is still a single translation string per equation. That is enough for first-pass readability, but it is not yet the richer target model.

Target rendering still needs:

- canonical form
- structure-preserving reading
- key-part breakdown
- relevance statement

## Canonical source files

- `references/current-state.md`
- `references/cloudflare-worker-map.md`
- `references/targets.md`
- `reports/mtl-site-coverage-audit/mtl_coverage_summary.md`
- `reports/consciousness-mtl-d1-import/safe_d1_import_summary.json`
