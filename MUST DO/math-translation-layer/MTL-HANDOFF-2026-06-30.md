# Math Translation Layer Handoff

**Date:** 2026-06-30  
**Purpose:** Give the next AI a clean operational picture of what the Math Translation Layer actually is, what is live, what is legacy, and how to attack it series by series.

## Executive read

The Math Translation Layer is not just an idea. It already has:

- a live **Cloudflare Worker** runtime path
- a live **D1 database** path
- a live **site client** already loaded by many pages
- a repeatable **audit + import** script set
- a local **workbook normalization** path

So the next serious work is **not** inventing MTL from scratch.

It is:

1. deciding which path is canonical
2. finishing coverage series by series
3. upgrading the payload from a single translation string to a richer structured explanation model

## The most important truth

There are **two MTL systems** in the repo.

### 1. Current runtime worker path

This is the living path for runtime equation translation.

- Worker folder: `D:\GitHub\faiththruphysics-site\workers\mtl-service`
- Worker name: `faith-mtl-worker`
- Live base URL: `https://faith-mtl-worker.davidokc28.workers.dev`
- D1 binding: `DB`
- D1 database: `faiththruphysics-mtl`
- Live site client: `D:\GitHub\faiththruphysics-site\shared\js\mtl-worker-client.js`

What it does:

- collects MathJax-rendered equations from the page
- batches them to the Cloudflare worker
- receives a translation string per equation
- inserts translation callouts after the rendered math

This is the path to prefer for **new runtime translation work**.

### 2. Legacy overlay / local uploader path

This is the older path.

- `shared/js/mtl-overlay.js`
- `shared/js/mtl-overlay-loader.js`
- `shared/data/mtl-overlay-translations.json`
- local uploader references under `mtl-admin`

This path still matters as reference material, but it should be treated as **legacy unless there is a specific reason to revive it**.

## Important doc tension

The docs are not perfectly aligned yet.

### One branch says:

The old generic overlay is deprecated and the future is **in-article callouts** using:

- `mtl-callout.css`
- `mtl-callout.js`

### Another branch says:

The **worker client** is live and already active on many pages:

- `shared/js/mtl-worker-client.js`
- D1-backed translation coverage audits

## Best interpretation

Both are true in different senses:

- the **worker path** is the active runtime translation infrastructure
- the **callout path** is the design direction for richer article-integrated presentation

So the next AI should not pick one and ignore the other. It should treat them like this:

- **runtime/data canon:** worker + D1
- **presentation/design target:** richer in-article callout model

That distinction matters.

## What is already true

From the current-state notes:

- the site already has an MTL Cloudflare worker project
- many live pages already load `shared/js/mtl-worker-client.js`
- `consciousness` is already a valid high-value MTL target
- a safe `consciousness` subset was uploaded into D1
- worker mode handling was recently patched so reader-mode changes rerender correctly

## Current hard limitation

The worker currently returns **one translation string per equation**.

That is enough for a first readable layer, but not enough for the fuller target model you want:

- canonical form
- structure-preserving reading
- key parts
- why it matters
- claim / test surface

So the next real upgrade is not “get the worker working.”  
The worker already works.

The upgrade is:

**move from single-string translations to a structured payload model**

## Repeatable script surface

Script folder:

- `D:\GitHub\faiththruphysics-site\MUST DO\math-translation-layer\scripts`

Primary scripts:

- `extract_series_math.py`
- `run_series_math_scan.ps1`
- `summarize_active_math_surface.py`
- `normalize_mtl_workbook.py`
- `export_safe_rows_to_d1.py`
- `audit_mtl_site_coverage.py`

This is the operational backbone. Use these instead of inventing new ad hoc scans first.

## Key reports already in play

- `D:\GitHub\faiththruphysics-site\reports\faiththruphysics-site-math-active\active_math_summary.md`
- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_coverage_summary.md`
- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_page_status.csv`
- `D:\GitHub\faiththruphysics-site\reports\mtl-site-coverage-audit\mtl_missing_equations.csv`

For the primary target lane:

- `D:\GitHub\faiththruphysics-site\reports\consciousness-math\series_math_summary.md`
- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-workbook-normalized\`
- `D:\GitHub\faiththruphysics-site\reports\consciousness-mtl-d1-import\`

## Series-by-series attack plan

## Tier 1 - flagship finish

### `consciousness`

Why first:

- already has substantial embedded math
- already has working MTL client wiring
- already has safe-row D1 import work
- strongest candidate for proving the full stack: math + translation + audio + shell + rigor

Known state:

- 22 HTML files
- 17 with extracted math
- 626 extracted equations
- 5 zero-math files

High-value pages:

- `consciousness-chi-field-action.html`
  - 141 equations
  - 120 found
  - 21 missing
- `consciousness-grace-source-term.html`
  - 101 equations
  - 81 found
  - 20 missing
- `consciousness-reality-assessment.html`
  - 98 equations
  - 41 found
  - 57 missing

Interpretation:

- `chi-field-action` is the best flagship page
- `grace-source-term` is the next near-finish page

## Tier 2 - next safe-row import lane

### `revolution-of-truth`

Why next:

- smaller surface
- already scanned
- clear math presence
- currently weak D1 coverage, so wins should be obvious

Known state:

- 173 extracted equations
- strongest pages:
  - `drv-00-the-argument.html`
  - `drv-02-the-lock.html`

Current coverage examples:

- `drv-00-the-argument.html` -> 1 found / 57 missing
- `drv-02-the-lock.html` -> 0 found / 48 missing

Interpretation:

- this should be the next clean import/audit lane after consciousness

## Tier 3 - large backlog lane

### `genesis-to-quantum`

Why later:

- largest remaining active backlog
- not the fastest proof of success

Known state:

- 415 uncovered equation instances in the active D1-backed coverage audit

Interpretation:

- do not start here if the goal is a visible fast win
- do start here once the workflow is stable and repeatable

## What the next AI should actually do

## Job 1: confirm the canonical path

Write down clearly:

- worker + D1 is runtime canon
- richer callout model is presentation target
- overlay-only path is legacy reference unless explicitly needed

## Job 2: finish one flagship page end-to-end

Best first page:

- `consciousness-chi-field-action.html`

Definition of done:

- page math extracted and audited
- missing equations identified
- safe rows normalized from workbook
- safe rows imported to D1
- runtime client verified on page
- translation coverage improved measurably

## Job 3: define the richer payload

The current worker returns one string.

The next target payload should probably carry, per equation:

- `id`
- `latex`
- `canonical_reading`
- `plain_english`
- `symbol_map`
- `why_it_matters`
- `claim_hook`
- `test_hook`
- `mode_variants`

That is the real bridge between the worker system and the deeper page experience.

## Job 4: build the series rollout plan

Do not just say “MTL is incomplete.”

Write the next rollout sequence clearly:

1. consciousness flagship pages
2. consciousness series finish
3. revolution-of-truth safe-row import
4. genesis-to-quantum bulk backlog

## Operational rule

Only move **safe rows** into D1 on first pass.

Keep `needs_review` separate.

Do not sweep ambiguous rows into the live translation layer just to make the coverage chart look better.

## Final recommendation

The next Opus / Cloudflare / worker push should probably not start with front-end polish.

It should start with:

1. one canonical runtime path
2. one flagship page
3. one structured payload upgrade plan
4. one series rollout order

That gives the whole MTL effort a spine instead of a pile of parts.
