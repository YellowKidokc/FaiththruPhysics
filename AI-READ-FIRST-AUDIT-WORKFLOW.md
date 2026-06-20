# AI Read First: Audit Workflow

This repo contains live site pages, staging material, component snippets, examples, and backup-like folders mixed together.

Do not start editing blind.

## Core Rule

Before any HTML work:

1. Audit first.
2. Read the audit report.
3. Identify what the target file actually is:
   - production page
   - staging page
   - snippet/component
   - example/build artifact
   - archive/backup-like material
4. Record page context:
   - series
   - page type
   - dominant theme/topic
   - whether math is present
   - whether equation blocks are visibly labeled
   - whether equation blocks are explained in plain English nearby
5. If intent or labeling is ambiguous, stop and ask instead of guessing.

## Default Audit Command

From `D:\GitHub\Python-WEB\theophysics-site-repair`:

```powershell
python run_site_repair.py --series mda --target D:\GitHub\faiththruphysics-site --modules inventory,audit_html,verify_final --dry-run
```

## What The Audit Should Catch

At minimum:

- structure problems
- metadata problems
- broken links
- MathJax missing when math markers exist
- math presentation problems
- footer app integrity problems

As the workflow grows, the audit should also become the gate for:

- page classification problems
- component/snippet pages being mistaken for production pages
- claim drift and equation drift
- truth-status/category drift
- regression outside allowed edit regions

Math presentation means:

- display math should live in reusable equation containers where possible
- equation blocks should have a visible label
- equation blocks should have an explanatory note, caption, or nearby paragraph

Target pattern:

1. label
2. equation
3. explanation

## Current Reference Pattern

For readable equation presentation, use the GTQ article style as the reference pattern, especially pages that already pass the math presentation audit cleanly.

## Gold Nuggets Pulled From The Toolbox

These came from folders in `D:\GitHub\Python-WEB` that are easy to ignore but contain real workflow value.

### 1. Nothing Becomes Canonical By Generation

From the workflow factory notes:

- generated files are not automatically canonical
- candidates should land in a run/staging area
- canonical files should be replaced only by promotion
- every promotion should leave a report trail

Operational meaning:

- do not treat a generated HTML page as truth just because it exists
- audit first, then promote intentionally

### 2. Reusable Components Are Inputs, Not Page Truth

From `02_TEMPLATES`:

- headers
- footers
- equation blocks
- proof cards
- reader bars

should be treated as reusable inputs, not as canonical page instances.

Operational meaning:

- change templates carefully
- test on staging/candidates first
- do not assume a template edit is safe just because it is reusable

### 3. Canonical Pages Need A Protected Write Path

From `05_CANONICAL_SITE`:

- canonical folders should not be casually rewritten
- generated output should not be written directly to canonical
- replacements should happen through a promotion path

Operational meaning:

- the workflow should distinguish clearly between:
  - candidate
  - canonical
  - archive
  - snippet

### 4. Claim Preservation Must Be Explicit

From `docs/CLAIM_PRESERVATION_RULES.md`:

Protected items include:

- core claims
- supporting claims
- definitions
- equations
- Scripture references
- citations
- dates
- falsification language
- theological meaning
- mathematical meaning

Operational meaning:

- any workflow that rewrites or translates prose needs drift checks
- uncertainty must be marked `needs_review`, not silently passed

### 5. Paragraph Roles Are Useful

Also from claim preservation:

- hook
- define
- explain
- prove
- example
- objection
- reply
- transition
- application
- warning
- source
- conclusion
- unknown

Operational meaning:

- future audits can label paragraph role
- this will help detect pages with equations but no explanation
- it will also help detect where proof language and devotional language are blending badly

### 6. Structured Exports Beat Prose Scraping

From `series-assets/PROOF_LAYER_PACKET_FIELD_MAP.md` and `series-assets/shared-outputs/README.md`:

- pages should consume structured proof/audit/claim outputs where they exist
- shared JSON/CSV/graph artifacts should live in shared outputs
- pages should link to structured artifacts rather than scraping loose prose

Operational meaning:

- proof-heavy pages should eventually pull from structured packets
- audits should know when structured support exists for a page

### 7. Truth-Status Blocks Are A Good House Rule

From `series-assets/TRUTH_STATUS_COMPONENTS.html`:

Claims can be marked as:

- belief / conviction
- evidence-supported but not closed
- formally defended

Operational meaning:

- strong sections should announce their status before the reader has to infer it
- this is a strong future audit check for category honesty

### 8. Edit Safety Labels Already Exist

From `theophysics-site-repair/labels/edit_safety_labels.json`:

- some files are already effectively marked audit-only / manual-review-required

Operational meaning:

- edit safety should expand beyond the repair repo
- eventually the site repo itself should have clearer safety labeling for:
  - components
  - canonical pages
  - examples
  - backups

### 9. Workflow Factory Pattern Is Strong

From `_bootstrap`:

Good workflow structure is:

- `canonical/`
- `runs/`
- `comms/`
- `config/`
- `templates/`
- `scripts/`
- `prompts/`
- `archive/`

Operational meaning:

- even if the current site repo is not reorganized immediately, the workflow should imitate this logic conceptually

## Workflow Buildout Queue

These are the next useful expansions.

### Priority 1

- production vs snippet/example detection
- better exclusion of backup/archive/build folders during audit
- equation-block consistency audit by series
- detection of math-heavy pages with no plain-English explanation

### Priority 2

- page theme manifest
- paragraph role labeling
- truth-status block recommendations
- structured page classification report

### Priority 3

- allowed-region regression gate
- component marker-bound replacement audit
- promotion manifest for canonical replacements
- shared proof-packet awareness in page audits

## Suggested Operating Model

For now, use this sequence:

1. classify the target
2. run audit
3. decide whether this is:
   - audit only
   - safe mechanical repair
   - manual page patch
   - template/component work
4. preserve claims/equations/citations/dates
5. re-audit after edits
6. only then consider promotion/canonical replacement

## Unsure Means Ask

If the system cannot safely infer:

- the correct equation label
- the intended page theme
- whether a block is decorative or load-bearing
- whether a file is canonical production or only an example/snippet

it should not invent the answer.

It should:

1. report the issue
2. preserve the page
3. ask for the missing label or classification

## Good Workflow

1. Audit target
2. Read report
3. Narrow scope to real production pages
4. Patch only what the task requires
5. Re-audit after edits
6. Verify that presentation improved without moving article meaning

## Important Guardrail

Do not automatically rewrite article prose, theology, math claims, citations, dates, or historical claims as part of a mechanical cleanup pass.
