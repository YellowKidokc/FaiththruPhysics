# Consciousness — teal shell theme

**Accent:** `#14b8a6` (mapped onto `--gold` in CSS so shared shell components keep working)

**Body class:** `series-consciousness` — triggers teal overrides in `components/top-bar-bottom-bar.css` (verified bar border, audio dock accent).

**Bottom equation:** `L = χ[Φ, g, C]` (field Lagrangian, not full MTL string)

**Series home:** `/consciousness/`

## Live vs reference

| | Path |
|---|------|
| **Deploy / rebuild from** | `faiththruphysics-site/consciousness/_TEMPLATE.html` |
| **This folder** | Museum copy + color notes — paths in `_TEMPLATE.html` assume `{series}/` on the live site (`../components/…`) |

Rebuild all 10 articles:

```powershell
cd D:\GitHub\Python-WEB
python top_bar_bottom_bar.py --series consciousness --apply
```

## Why this series is harder

Consciousness papers are long, dense, and not written with clean `##` section breaks like drv. That affects:

| Layer | Impact |
|-------|--------|
| **College feature boxes** | `college_enrich.py` keys off `##` sections — uneven breaks → uneven boxes. OK to run lighter or skip feature rotation on first pass. |
| **HS / PhD tabs** | No `consciousness/highschool/` or `consciousness/phd/` yet — both tabs may duplicate College or stay hidden until easy/academic markdown exists. |
| **Domain pills** | Use frontmatter on HS canonical **or** `domain-scan/consciousness/{slug}.json` **or** Excel → `excel_to_site_json` when workbook is filled. |
| **Verified bar** | Needs `data-viz/verification-consciousness-{slug}.json` on the site (from Excel merge or manual copy from framework-alignment / knowledge-graph JSON). |

Do not force drv-style section rhythm onto consciousness — polish one gold page (`consciousness-chi-field-action` or `consciousness-constraint-argument`), then propagate shell-only changes.

## Color tokens (search-replace from gold)

```
--gold:#d4af37          →  --gold:#14b8a6
--gold-dim              →  rgba(20,184,166,.08)
--gold-glow             →  rgba(20,184,166,.35)
rgba(212,175,55,…)      →  rgba(20,184,166,…)
```

`DOMAIN_COLORS["consciousness"]` in `top_bar_bottom_bar.py`: `#14b8a6`

## Data already staged (API path)

```
faiththruphysics-site-data/
  consciousness/*.canonical.md          ← College base
  raw-metrics/consciousness/*.json      ← station 01
  framework-alignment/consciousness/*.json
  justice-mercy/consciousness/*.json
  knowledge-graph/consciousness/*.json
```

Next optional step: one Excel workbook per article → `excel_to_site_json.py --series consciousness` so verified bar + audit foot match drv workflow.
