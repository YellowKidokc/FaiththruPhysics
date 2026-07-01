# 03 — Verified Bar

Pinned strip under header; expands to full metrics panel.

## Collapsed badges

- Axioms tested/total
- Laws active (of 10)
- χ normalized
- Isomorphism bridge count

## Expanded panel

- Axiom meter, law tags L1–L10
- χ raw, fruits score, isomorphism breakdown
- Claims counts, domain distribution table
- Link to Proof Explorer

## Live files

| File | Role |
|------|------|
| `components/verification-bar.html` | Markup snippet |
| `components/verification-bar.css` | Styles |
| `components/verification-bar.js` | `loadVerification()`, auto-fetch JSON |

## JSON path

```
faiththruphysics-site-data/data-viz/verification-{series}-{slug}.json
```

Copied to site `data-viz/` for static hosting.

## Populate data

1. Fill `Article_Evaluation_Workbook.xlsx` sheet `02_Verification_Metrics`
2. `python excel_to_site_json.py --apply`
3. Or: `merge_verification.py` from 13-station API outboxes

## Early prototype

`MUST DO/TOP BAR/verification-bar.html` — reference only; live version is in `components/`.
