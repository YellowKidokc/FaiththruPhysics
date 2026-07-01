# Page Shell Clinical Terms

This file is the shared vocabulary for page-shell work. Use these terms in prompts, audits, reports, and handoffs so every worker means the same thing.

Read this after you receive an assignment and before you choose a fix path.

## Core Rule

Do not describe a page issue loosely if a defined term exists here.

Good:

- "white-page regression"
- "double-shell defect"
- "header-lip drift"
- "title merge regression"

Bad:

- "that weird white thing"
- "header looks off"
- "bar is broken somehow"

## System Terms

### Page Shell

The full reusable article frame:

- top bar
- header lip / dropdown
- verified bar
- reading-level controls
- article chrome
- bottom nav / bottom dock
- audit foot

If a task says "page shell," assume it refers to the full frame, not only the top bar.

### Universal Shell

The JS-driven shared shell loaded by `frame.js`.

This is the canonical structural system unless a page is explicitly documented as an exception.

### Gold Standard

The reference implementation used for comparison and rebuild decisions.

Current page-level gold standard:

- `revolution-of-truth/drv-00-the-argument.html`

Current process-level gold standard:

- `MUST DO/PAGE-SHELL-GOLD-STANDARD/`

### Local Shell Source

The local shell loader path:

- `/site-shell/frame.js`

### Remote Shell Source

The fully qualified shell loader path:

- `https://faiththruphysics.com/site-shell/frame.js`

If a task mentions shell-source consistency, it means normalize local-vs-remote shell loading.

## Defect Terms

### White-Page Regression

A page that renders with a white or mostly white viewport when it should render in the site dark theme.

Typical causes:

- dark reset missing
- root theme variables stripped
- inner layout container forcing white background

First reference:

- `MUST DO/WHITE-PAGE-FIX-PROCESS.md`

### Double-Shell Defect

A page that renders more than one header shell, more than one dock shell, or a mixed old/new shell combination.

Typical causes:

- legacy `.tp-top` / `.tp-class` elements left in page body
- `frame.js` injected without stripping legacy shell

### Legacy Shell Residue

Old shell markup still present in live DOM or source markup after migration.

Examples:

- old `header.tp-top`
- old `.tp-class`
- old manual nav shell

Note:
Dead CSS alone is not the same as live residue. Record whether the issue is markup residue, live render residue, or harmless dead CSS.

### Top-Bar Drift

The top bar exists, but differs from the canonical shell in structure, spacing, scale, or behavior.

Examples:

- bar too tall
- misaligned brand area
- malformed controls
- wrong spacing around reading-level controls

### Header-Lip Drift

The dropdown / under-header layer exists, but its contents, spacing, or behavior differ from the expected pattern.

Examples:

- missing domain meter
- wrong tag layout
- broken prev/next cluster
- poor mobile collapse behavior

### Bottom-Dock Regression

The bottom audio / media dock is missing, duplicated, malformed, or wired incorrectly.

### Title Merge Regression

The page `h1` and subtitle have been accidentally merged into a single heading or the subtitle has been emptied.

### Theme-Integrity Failure

Any page where dark-theme colors, contrast, or shell theming are no longer coherent even if the page is technically not white.

Use this term when the page is dark but visually off.

## Work-Type Terms

### Audit Pass

Read-only inspection plus report generation. No page mutation.

### Repair Pass

A targeted fix pass against a defined defect type.

Examples:

- white-page repair pass
- title-merge repair pass
- shell-source normalization pass

### Migration Pass

A structural conversion from one shell system or component pattern to another.

Example:

- strip legacy shell and inject universal shell

### Regression Gate

The check that proves:

1. the intended defect was fixed
2. unrelated page regions did not regress

### Archive Placement

Copying or moving repair artifacts, zips, reports, and backups to the direct corresponding content root in `site-data`.

## Decision Terms

### Canonical

Preferred, approved, or source-of-truth implementation.

### Preferred Workflow

The documented first-choice process for a defect or task type.

If a worker hits a known issue, they should check the preferred workflow before inventing a new one.

### Exception

A documented deviation from the canonical pattern. Exceptions should be explicit, not assumed.

### Safe-to-Auto-Fix

A defect class that can be repaired with a documented script or deterministic rule without changing article meaning.

### Needs Review

A defect or ambiguity that should be reported upward rather than guessed at.

## Assignment Language

Use this pattern in future prompts:

1. identify the defect class
2. identify the workflow document
3. identify the gold standard
4. specify audit vs repair vs migration
5. require regression gate output

Example:

"You are doing a white-page repair pass. Before editing, check `MUST DO/WHITE-PAGE-FIX-PROCESS.md` and the page-shell clinical terms. Use `revolution-of-truth/drv-00-the-argument.html` as the gold standard for shell behavior. Fix only white-page regressions, then run a regression gate for shell integrity."

## Fast Lookup

| Term | Meaning |
|---|---|
| white-page regression | dark theme failed and page renders white |
| double-shell defect | old and new shell render together |
| legacy shell residue | old shell still present after migration |
| top-bar drift | header exists but no longer matches canonical structure |
| header-lip drift | dropdown / subheader layer differs from standard |
| bottom-dock regression | media dock missing, duplicated, or malformed |
| title merge regression | `h1` and subtitle collapsed together |
| theme-integrity failure | page is dark but visually inconsistent |
| audit pass | inspect only |
| repair pass | targeted fix |
| migration pass | structural conversion |
| regression gate | prove fix + no collateral damage |
| archive placement | put reports/backups with direct content counterpart |

