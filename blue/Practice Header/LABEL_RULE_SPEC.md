# Faith Thru Physics Topbar Label Rule Spec

Purpose: one canonical labeling contract for the shared topbar rollout.

Use this for article/content pages receiving the shared header. Do not use it as permission to rewrite article content.

## Core Rules

1. Every topbar/header control must have a stable `data-slot`.
2. Every page structure touched by the rollout should keep or receive the appropriate `data-tp-*` label used by the existing labeler.
3. If a page includes a standalone header entry or prototype, it must include `#header-entry-labels` JSON.
4. Labels describe role, not styling. Do not name labels after colors, sizes, or visual experiments.
5. Do not rename existing meaningful labels unless they are broken or duplicated.
6. Do not add labels to article prose just because it exists. Label structural containers and controls, not every paragraph.
7. JSON must parse. No comments inside JSON.

## Required Header Slots

These slots should exist anywhere the shared topbar/header is installed or evaluated:

```text
top-frame
top-frame-main-row
brand-home
brand-mark
brand-name
brand-nav-divider
primary-nav
nav-home
nav-mtl
nav-proof
nav-series
top-frame-actions
reading-level-control
reading-level-high-school
reading-level-college
reading-level-phd
search-command
proof-dashboard-toggle
domain-pill-row
domain-row-metric-numbers
metric-domains-number
metric-laws-number
metric-coherence-number
metric-claims-number
domain-pills
domain-logic-mathematics
domain-physics
domain-information-theory
domain-theology
domain-developmental-psychology
domain-philosophy
domain-color-strip
series-panel
proof-dashboard-panel
search-panel
```

Optional but recommended:

```text
series-blue
series-moral-decline
series-genesis-to-quantum
series-formal-papers
search-site-index
search-glossary
proof-card-grid
proof-card-domains
proof-card-laws
proof-card-coherence
proof-card-claims
```

## Header JSON Contract

Prototype/header contest pages must include:

```html
<script type="application/json" id="header-entry-labels">
{
  "entry": "claude",
  "author": "Claude",
  "version": "2026-07-02",
  "slots": {
    "top-frame": "Fixed shared topbar frame",
    "brand-home": "Home link and brand identity",
    "primary-nav": "Primary site navigation",
    "reading-level-control": "Reading-level selector",
    "domain-pill-row": "Domain and metric row",
    "proof-dashboard-panel": "Expandable proof metrics panel"
  }
}
</script>
```

Production article pages do not need per-page `header-entry-labels` unless the header is embedded directly in that file. If the page only links shared `/assets/faith-topbar.js`, the shared asset owns the topbar slot map.

## `data-tp-*` Guidance

Use existing site conventions first. If a page already has `data-tp-*`, preserve it.

Recommended structural labels:

```text
data-tp-page="article"
data-tp-shell="article-shell"
data-tp-region="article-header"
data-tp-region="article-body"
data-tp-region="article-footer"
data-tp-section="proof-dashboard"
data-tp-section="domain-map"
data-tp-section="reading-controls"
data-tp-component="shared-topbar"
data-tp-component="legacy-header"
data-tp-component="proof-card"
data-tp-component="domain-pill"
```

Use `data-slot` for exact controls and `data-tp-*` for broader page regions/components.

Example:

```html
<header data-tp-component="shared-topbar" data-slot="top-frame">
  <nav data-slot="primary-nav">
    <a data-slot="nav-home" href="/index.html">Home</a>
  </nav>
</header>
```

## Labeling Existing Article Pages

When labeling a rollout page:

1. Confirm the page is in `ai-article-rollout-split.json`.
2. Confirm it is not an index/doorway/media/app/archive page.
3. Label only touched structural wrappers and injected/hidden header areas.
4. Do not label every content paragraph.
5. Preserve page-specific classes and IDs.
6. If a legacy header is hidden, label it before hiding where practical:

```html
<header class="old-header" data-tp-component="legacy-header" data-slot="legacy-page-header">
```

## Unknown Class Queue

When the labeler finds unknown class tokens:

1. Do not guess aggressively.
2. Group unknowns by folder and page.
3. Record count and sample element.
4. Propose rule only if the role is obvious from repeated context.
5. Leave uncertain tokens in the queue.

Unknown report should include:

```text
folder
file
unknown class/token
count
sample element
recommended mapping or "hold"
```

## Required Verification

For every labeled batch, report:

```text
files_checked
files_changed
required_header_slots_missing
json_parse_status
data_tp_labels_added_or_verified
unknown_tokens_count
unknown_tokens_report_path
article_content_changed: yes/no
pass_or_revise
```

JSON verification:

```powershell
python -m json.tool PATH_TO_EXTRACTED_HEADER_JSON
```

HTML label search:

```powershell
rg -n "data-slot=|data-tp-|header-entry-labels" "D:\GitHub\faiththruphysics-site-v2\ASSIGNED_FOLDER"
```

## Stop Conditions

Stop and report instead of editing if:

- The page is not in `ai-article-rollout-split.json`.
- The page appears to be an index, app, media, archive, or generated duplicate.
- The same file is being edited by another lane.
- Required topbar assets are not injected yet and the task depends on them.
- Labeler output suggests article prose would be rewritten.
- JSON cannot be made valid without changing the header structure.

