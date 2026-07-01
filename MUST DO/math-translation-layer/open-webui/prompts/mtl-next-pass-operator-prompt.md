# MTL Next Pass Operator Prompt

Use the existing Math Translation Layer workspace and continue from current state without changing auth, admin, or unrelated site settings.

## Goal

Improve live Math Translation Layer coverage in small safe batches while keeping ambiguous rows isolated.

## Rules

- Treat `D:\GitHub\faiththruphysics-site` as the live site/output repo.
- Treat `D:\GitHub\faiththruphysics-site\MUST DO\math-translation-layer` as the current operator workspace.
- Use the worker path, not the legacy overlay path, unless a clear blocker forces otherwise.
- Do not delete anything on the first pass.
- Do not move `needs_review` rows into live D1.
- Verify small batches before widening scope.

## Existing assets

- Worker project: `workers/mtl-service`
- Live worker client: `shared/js/mtl-worker-client.js`
- D1 database: `faiththruphysics-mtl`
- Coverage audit script: `scripts/audit_mtl_site_coverage.py`
- Safe D1 export script: `scripts/export_safe_rows_to_d1.py`
- Workbook normalizer: `scripts/normalize_mtl_workbook.py`

## Current known status

- `EQ-001` through `EQ-010` were already uploaded from the safe consciousness subset.
- Site coverage audit still shows `1319` missing equation instances.
- Highest-value near-finish lane is `consciousness`.
- Next series lane is `revolution-of-truth`.
- Largest active backlog lane is `genesis-to-quantum`.

## What to do

1. Read:
   - `references/current-state.md`
   - `references/cloudflare-worker-map.md`
   - `references/targets.md`
   - `reports/mtl-site-coverage-audit/mtl_coverage_summary.md`
2. Confirm which series is being advanced this pass.
3. Run or reuse the math extraction and coverage audit.
4. Prepare only safe rows for D1 import.
5. Keep `needs_review` rows in a separate output.
6. Verify page wiring vs D1 coverage.
7. Leave a concise report:
   - what was reviewed
   - what was imported
   - what changed
   - what still blocks full coverage

## Preferred batch order

1. `consciousness`
2. `revolution-of-truth`
3. `genesis-to-quantum`
