# 07 — Audit Foot

Three-column audit at page bottom.

## Columns

- **Got right** — what the article nails
- **Overstated** — confidence too high for evidence
- **Got wrong** — factual or structural errors (often empty)

## Data source

```
faiththruphysics-site-data/rigor/{series}/{slug}.json
```

```json
{
  "got_right": ["..."],
  "overstated": ["..."],
  "got_wrong": []
}
```

Populated from workbook sheet `07_Audit_Boxes` via `excel_to_site_json.py`, or writing-analyzer prompt `04_writing_analysis`.

## Builder

`top_bar_bottom_bar.py` → `audit_lists()` reads rigor JSON when present; otherwise placeholder covenant text.

## Reference UI

`MUST DO/audit-gradient.html` — visual reference for audit box styling.
