# 09 — Evaluation Pipeline

Turns analyzer + workbook data into site JSON.

## Folders

| Path | Role |
|------|------|
| `faiththruphysics-site-data/APIs/revolution-of-truth-pipeline/` | Excel template, schemas, input markdown |
| `faiththruphysics-site-data/revolution-of-truth/_evaluation/` | Writing-analyzer outputs per run |
| `X:\09_DATABASES\DRV_*_Vectorization_*` | ChromaDB corpora (college / PhD / HS) |

## drv-00 analyzer output (example)

```
revolution-of-truth/_evaluation/drv-00_eval_20260629_020038/
  01_01_find_variables_deepseek.md
  02_04_writing_analysis_deepseek.md
  ...
  manifest.json
```

## Workbook → JSON

```bash
cd D:\GitHub\Python-WEB
python build_article_evaluation_workbook.py
python excel_to_site_json.py --apply
```

Exports:

- `data-viz/verification-*.json` → verified bar
- `rigor/{series}/{slug}.json` → audit foot
- `claims/{series}/{slug}.json` → PhD proof layer
- `editorial/{series}/{slug}.json` → flow + physics + citations

## Writing-analyzer

```bash
python APIs/revolution-of-truth-pipeline/scripts/run_drv_eval.py
```

Prompts: `x:\06_ENGINES\writing-analyzer\prompts\01–13`

## fp-005 framework tabs (future on-page)

7Q, Decision Tree, Swap Test, CKG — schema: `schemas/framework-report.schema.json`

Reference page: `Templates David/fp-005-enhanced.html`
