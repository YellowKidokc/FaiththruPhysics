# Page Shell Gold Standard — Index

**Reference page:** `revolution-of-truth/drv-00-the-argument.html`  
**Strategy:** Perfect drv-00 → bake into shared parts → regenerate all series pages.

## Folder map

| # | Section | What it does |
|---|---------|--------------|
| [01-top-bar](01-top-bar/README.md) | Fixed header | Brand, Home/MTL/Proof links, Series lip toggle, HS/College/PhD tabs, search |
| [02-header-lip](02-header-lip/README.md) | Dropdown under header | Domain meter, classification tags, prev/next, series grid |
| [03-verified-bar](03-verified-bar/README.md) | Verified strip | Axioms, laws, χ, bridges, domain chips, expand panel |
| [04-reading-levels](04-reading-levels/README.md) | Three panels | High School / College / PhD content swap |
| [05-article-body](05-article-body/README.md) | Article chrome | College drop caps, eq cards, feature boxes, sections |
| [06-bottom-nav](06-bottom-nav/README.md) | Big prev/next | Series home, chapter cards, sub-series strip |
| [07-audit-foot](07-audit-foot/README.md) | Audit covenant | Got right / overstated / got wrong |
| [08-math-references](08-math-references/README.md) | MathJax + refs | Delimiter fix, `.tp-refs` bibliography |
| [09-evaluation-pipeline](09-evaluation-pipeline/README.md) | Excel → JSON | Workbook, writing-analyzer, verified bar data |
| [10-data-layout](10-data-layout/README.md) | site-data paths | Markdown tiers, frontmatter, rigor JSON |

## Scripts (local execution copies)

| Script | Role |
|--------|------|
| [scripts/top_bar_bottom_bar.py](scripts/top_bar_bottom_bar.py) | **Main builder** — template + 3 levels + nav + domains + audit |
| [scripts/article_html.py](scripts/article_html.py) | Markdown → HTML, sections, references |
| [scripts/college_enrich.py](scripts/college_enrich.py) | College equation cards + feature boxes |
| [scripts/build_article_evaluation_workbook.py](scripts/build_article_evaluation_workbook.py) | Generate Excel evaluation template |
| [scripts/excel_to_site_json.py](scripts/excel_to_site_json.py) | Workbook → verification / rigor / claims / editorial JSON |
| [scripts/merge_verification.py](scripts/merge_verification.py) | 13-station pipeline → single verification JSON |

## Shared site components (live — do not fork)

See [components/MANIFEST.md](components/MANIFEST.md).

## Skills

| Skill | Path |
|-------|------|
| Page Shell Builder | [skills/page-shell-builder.md](skills/page-shell-builder.md) |
| Wire Audio | `C:\Users\David\.claude\skills\wire-audio\SKILL.md` |
| Upload Audio | `C:\Users\David\.claude\skills\upload-audio\SKILL.md` |
| Media Convert | `C:\Users\David\.claude\skills\media-convert\SKILL.md` |

## Related MUST DO folders (already existed)

| Folder | Topic |
|--------|-------|
| [../TOP BAR](../TOP BAR/README.md) | Early verification-bar prototype + merge script |
| [../PAGE-SHELL-CLINICAL-TERMS.md](../PAGE-SHELL-CLINICAL-TERMS.md) | Shared defect language, workflow terms, and handoff vocabulary |
| [../math-translation-layer](../math-translation-layer/README.md) | MTL equation callouts (in-article, not overlay) |
| [../ARTICLE_PIPELINE_SPEC.md](../ARTICLE_PIPELINE_SPEC.md) | Broader article pipeline spec |

## One-command rebuild (revolution-of-truth)

```bash
cd "D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts"
python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-00-the-argument
python top_bar_bottom_bar.py --series revolution-of-truth --apply --audience academic
python top_bar_bottom_bar.py --series revolution-of-truth --apply --segments top-bar,reading-panels,metadata --report "D:\GitHub\faiththruphysics-site\reports\top-bar-audit.json"
python college_enrich.py --series revolution-of-truth --audit
python excel_to_site_json.py --apply
```

## Series themes (color shells)

[themes/README.md](themes/README.md) — reference `_TEMPLATE.html` copies (gold drv, teal consciousness).

## Gold-standard checklist

[gold-standard/drv-00-checklist.md](gold-standard/drv-00-checklist.md)
