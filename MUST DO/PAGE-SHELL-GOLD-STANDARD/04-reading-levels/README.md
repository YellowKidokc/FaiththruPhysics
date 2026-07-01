# 04 — Reading Levels (HS / College / PhD)

Three content panels behind the top-bar tabs.

## Data layout (site-data)

```
revolution-of-truth/
  drv-00-the-argument.canonical.md      ← College (default)
  highschool/drv-00-the-argument.canonical.md
  phd/drv-00-the-argument.canonical.md
```

Legacy fallbacks: `easy/`, `academic/`, `APIs/input/`

## Migrate legacy → series folder

```bash
python top_bar_bottom_bar.py --series revolution-of-truth --organize-data --apply
```

## Live files

| File | Role |
|------|------|
| `components/reading-levels.js` | Tab switch, `data-reading-level` on body |
| `top_bar_bottom_bar.py` | Loads all 3 markdown files, injects 3 `<div class="tp-panel">` |

## Frontmatter (HS file)

```yaml
---
claims: [...]
domains: { Information Theory: 25, ... }
---
```

→ Domain pills + future claims layer on PhD.

## Design rule

| Level | Visual treatment |
|-------|------------------|
| High School | Clean prose, minimal markup |
| College | Drop caps, eq cards, feature boxes, callouts (CSS + `college_enrich.py`) |
| PhD | Full academic; future click-to-expand claims |

## Lighter pass for new series

Shell + three levels + domains + basic college blocks only. Skip rigor JSON and proof layer until content is stable.
