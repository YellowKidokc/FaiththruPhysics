---
name: page-shell-builder
description: >-
  Build and enrich faiththruphysics article pages — unified shell (top bar,
  verified bar, bottom nav, audit foot), three reading levels (High School /
  College / PhD), domain pills, and College visual blocks. Use when wiring
  revolution-of-truth or any series page, running top_bar_bottom_bar.py,
  college_enrich.py, organizing site-data reading levels, or templatizing
  article layout from the drv-00 gold standard.
---

# Page Shell Builder

Build faiththruphysics article pages from **shared shell + per-page data**. Fix once in template/CSS/scripts; rebuild all pages.

## Repos and paths

| What | Path |
|------|------|
| Site (HTML output) | `D:\GitHub\faiththruphysics-site` |
| Data (markdown, rigor, audio API) | `D:\GitHub\faiththruphysics-site-data` |
| Script workspace | `D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts` |
| Page template (per series) | `{site}/{series}/_TEMPLATE.html` |
| Shared shell CSS | `{site}/components/top-bar-bottom-bar.css` |
| Reading-level JS | `{site}/components/reading-levels.js` |

## Data hierarchy (reading levels)

Canonical layout under `faiththruphysics-site-data/{series}/`:

```
{series}/
  drv-00-the-argument.canonical.md     ← College (base article)
  highschool/
    drv-00-the-argument.canonical.md   ← High School
  phd/
    drv-00-the-argument.canonical.md   ← PhD / academic
```

**Legacy fallbacks** (still read if series folder missing):

| Level | Legacy path |
|-------|-------------|
| High School | `easy/{series}/` |
| College | `APIs/input/{series}/` |
| PhD | `academic/{series}/` |

**Migrate legacy → series folder:**

```bash
cd D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts
python top_bar_bottom_bar.py --series revolution-of-truth --organize-data --apply
``` 

Copies `easy/` → `{series}/highschool/` and `academic/` → `{series}/phd/`.

## Frontmatter (domains + claims)

High School canonical files use a YAML fence at the top:

```yaml
---
claims:
  - "Claim text..."
domains:
  Information Theory: 25
  Physics: 20
  Theology: 20
---
```

- **domains** → verified-bar pill chips + 100% meter (`ARTICLE_PROFILE` in template)
- **claims** → `ARTICLE_CLAIMS` (future proof layer on PhD)

Fallback if no frontmatter: `faiththruphysics-site-data/domain-scan/{series}/{slug}.json`

## Scripts (MUST DO workspace)

### 1. `top_bar_bottom_bar.py` — full page shell

Injects template + all three reading levels + nav + domains + audit placeholders.

```bash
cd D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts
python top_bar_bottom_bar.py --series revolution-of-truth --dry-run
python top_bar_bottom_bar.py --series revolution-of-truth --apply
python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-00-the-argument
python top_bar_bottom_bar.py --series revolution-of-truth --apply --segments top-bar,reading-panels,metadata
python top_bar_bottom_bar.py --series revolution-of-truth --apply --disable-segments audit-panels
python top_bar_bottom_bar.py --series revolution-of-truth --apply --audience academic
python top_bar_bottom_bar.py --series revolution-of-truth --apply --report "D:\GitHub\faiththruphysics-site\reports\top-bar-build.json"
``` 

**What it does:**
- Reads `{series}/_TEMPLATE.html`
- Loads HS / College / PhD markdown per slug
- Runs College enrichment (via `college_enrich.py`)
- Injects prev/next nav, domain profile, audit box slots
- Backs up to `faiththruphysics-site-data/_inject_backups/top-bar-bottom-bar-{timestamp}/`

### Segment and output controls

- `--segments`: whitelist by comma list (`top-bar,bottom-bar,reading-panels,audit-panels,metadata,asset-hooks`).  
  If omitted, defaults to all segments.
- `--disable-segments`: remove selected segments from the enabled set.
- `--audience`: reading mode (`full`, `easy`, `academic`) controls which content levels load.
- `--report`: optional JSON report path for per-page segment status and changed-file summary.

### 2. `college_enrich.py` — College visual blocks (standalone)

Markup pass for College panel only. CSS does drop caps, rotating headers, blockquotes, tables.

**Python adds:**
- `.tp-eqcard` — standalone `$$…$$` / `\[…\]` equations (+ optional caption label)
- `.tp-feature-1..5` — rotated creative boxes on punchy paragraphs (every other section)

```bash
python college_enrich.py --series revolution-of-truth --audit
python college_enrich.py --series revolution-of-truth --slug drv-00-the-argument
python college_enrich.py --markdown path/to/article.canonical.md --out enriched.html
```

### 3. `article_html.py` — shared markdown → HTML

- Strips YAML frontmatter
- `md_to_html()` with tables, fenced code
- Wraps each `##` block in `<section>`; tags References as `class="tp-refs"`

Imported by both scripts above. Do not duplicate this logic elsewhere.

## What is CSS-only vs Python markup

| Effect | Layer | Scoped to |
|--------|-------|-----------|
| Drop caps (big first letter) | CSS `::first-letter` | College |
| Rotating h2 styles (3 variants) | CSS `nth-of-type` | College |
| Blockquote callouts | CSS | College |
| Table cards | CSS | College |
| References numbered list | CSS on `.tp-refs` | All levels |
| Equation cards | Python → `.tp-eqcard` | College |
| Feature boxes (5 shapes) | Python → `.tp-feature-N` | College |
| Top bar / verified bar / footer | Template + CSS | All pages |
| Domain pills + meter | Template JS + frontmatter | All pages |

**Rule:** College richness = CSS base layer + `college_enrich.py` markup. HS and PhD stay clean unless explicitly extended.

## Gold standard workflow (drv-00)

Use `drv-00-the-argument` as the reference page. Polish end-to-end, then propagate.

1. **Data** — confirm all three levels exist under `{series}/highschool`, `{series}/`, `{series}/phd`
2. **College content** — edit `{series}/drv-00-the-argument.canonical.md`
3. **Audit enrichment** — `python college_enrich.py --series revolution-of-truth --slug drv-00-the-argument`
4. **Build page** — `python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-00-the-argument`
5. **Verify** — serve site locally, check College / PhD / HS tabs, math, references, nav, domains
6. **Propagate** — `python top_bar_bottom_bar.py --series revolution-of-truth --apply` (all pages inherit shell + CSS + enrichment rules)

## MathJax (template)

In `_TEMPLATE.html`, delimiters must use **double backslashes** in JS strings:

```javascript
tex: { inlineMath: [['$','$'], ['\\(','\\)']], displayMath: [['$$','$$'], ['\\[','\\]']] },
```

Single `\(` in a JS string collapses to `(` and breaks inline math (red raw TeX).

## Nav title injection

When replacing prev/next titles in regex, use **lambda replacement**, not `rf"\1{title}\3"`. Titles starting with digits (e.g. `01 The Architecture`) become octal escapes (`\101` → `A`) and corrupt HTML.

## Lighter pass for next series

For new series/articles, minimum viable build:

- `top_bar_bottom_bar.py` — shell + HS + College + PhD + domains
- `college_enrich.py` — blocks (automatic from college markdown)
- Skip for now: claims proof layer, rigor audit JSON, audio wiring

Copy `_TEMPLATE.html` from `revolution-of-truth/` into the new series folder; adjust series label and nav home link.

## Future layers (not automated yet)

| Layer | Data source | Status |
|-------|-------------|--------|
| Audit boxes (got right / overstated / wrong) | `faiththruphysics-site-data/rigor/{series}/{slug}.json` | Excel pipeline ready (`excel_to_site_json.py`) |
| Verified bar metrics | `faiththruphysics-site-data/data-viz/verification-{series}-{slug}.json` | Excel pipeline ready |
| Claims proof layer (PhD click-to-expand) | `faiththruphysics-site-data/claims/{series}/{slug}.json` | Excel pipeline ready |
| Audio | `upload-audio` / `wire-audio` skills | Separate pipeline |

## Article evaluation pipeline (Excel → JSON)

**Folder:** `faiththruphysics-site-data/APIs/revolution-of-truth-pipeline/`

```bash
cd D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts
python build_article_evaluation_workbook.py          # regenerate Excel template
python excel_to_site_json.py --slug drv-00-the-argument --apply
python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-00-the-argument
```

Workbook sheets map to verified bar (`02_Verification_Metrics`), domain pills (`01_Article_Identity` / `03_Domains`), audit foot (`07_Audit_Boxes`), and claims (`04_Claims`).

NAS reference (if on network): `\\192.168.2.50\h_hp\Desktop\fruits_coherence_engine_package\Theophysics_Definitive_Workbook.xlsx`

## Related skills

- `media-convert` — WebP images into site repo
- `wire-audio` / `upload-audio` — R2 + faith-audio-pipeline
- `build-section-hub` — section index pages (if present in project)
