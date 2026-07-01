# Scripts (MUST DO workspace)

These are the practical execution copies used in the site/data pipeline.

Primary path:

`D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts`

### Shared command patterns

```bash
cd "D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts"
python top_bar_bottom_bar.py --series revolution-of-truth --dry-run
python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-00-the-argument
python top_bar_bottom_bar.py --series revolution-of-truth --apply --segments top-bar,reading-panels,metadata
python top_bar_bottom_bar.py --series revolution-of-truth --apply --disable-segments top-bar
python top_bar_bottom_bar.py --series revolution-of-truth --apply --audience academic
python top_bar_bottom_bar.py --series revolution-of-truth --apply --audience easy --segments reading-panels,metadata --report "D:\GitHub\faiththruphysics-site\reports\top-bar-build-academic.json"
```

### Scripts

| Script | Command |
|--------|---------|
| `top_bar_bottom_bar.py` | `python top_bar_bottom_bar.py ...` |
| `college_enrich.py` | `python college_enrich.py --series revolution-of-truth --audit` |
| `article_html.py` | Imported module — not run standalone |
| `build_article_evaluation_workbook.py` | Regenerates Excel template |
| `excel_to_site_json.py` | `python excel_to_site_json.py --apply` |
| `merge_verification.py` | `python merge_verification.py drv-00-the-argument` |

### New behavior notes

- `top_bar_bottom_bar.py` now supports:
  - `--segments` to enable only selected sections (top-bar, bottom-bar, reading-panels, audit-panels, metadata, asset-hooks).
  - `--disable-segments` to explicitly skip sections without deleting code.
  - `--audience` to select reading set (`full`, `easy`, `academic`).
  - `--report <path>` to write a JSON run report.
- This workflow defaults to script-level backups in:
  - `D:\GitHub\faiththruphysics-site-data\_inject_backups\top-bar-bottom-bar-<timestamp>/`
- Dependencies: `openpyxl`, stdlib.
