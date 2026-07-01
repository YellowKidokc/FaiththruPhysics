---
name: revolution-of-truth-image-shell
description: "Single-pass workflow for adding Revolution of Truth page images and rebuilding shell layers with one script that supports segment toggles."
audience: web-page-authoring
scope:
  - D:\GitHub\faiththruphysics-site-data\revolution-of-truth
  - D:\GitHub\faiththruphysics-site\revolution-of-truth
  - D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts
---

# Revolution of Truth — Image + Shell Iteration

This skill keeps image placement and shell regeneration in the same lane:

- Put image blocks in source markdown variants first.
- Rebuild that slug through `top_bar_bottom_bar.py`.
- Use segment toggles to disable top bar or bottom bar when needed instead of changing page output logic.

## Scope

- Canonical source files:
  - `D:\GitHub\faiththruphysics-site-data\revolution-of-truth\*.canonical.md`
  - `D:\GitHub\faiththruphysics-site-data\revolution-of-truth\highschool\*.canonical.md`
  - `D:\GitHub\faiththruphysics-site-data\revolution-of-truth\phd\*.canonical.md`
- Rendered output:
  - `D:\GitHub\faiththruphysics-site\revolution-of-truth\*.html`
- Script:
  - `D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts\top_bar_bottom_bar.py`

## Standard image block

```md
<img src="/media/media/series-opener.webp" alt="Revolution of Truth visual map" style="display:block; width:100%; max-width:980px; margin:1.5rem auto; border-radius:8px; border:1px solid rgba(212,175,55,.25);" />
```

## Runbook

1. Edit one page slug across three levels:
   - `revolution-of-truth\drv-XX-canonical.md`
   - `revolution-of-truth\highschool\drv-XX-canonical.md`
   - `revolution-of-truth\phd\drv-XX-canonical.md`
2. Insert image block in a stable location (usually right after abstract/title block).
3. Validate markdown sources:
   - confirm `/media/media/` path exists in `faiththruphysics-site\media\media`.
4. Dry-run rebuild:

```powershell
python "D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts\top_bar_bottom_bar.py" --series revolution-of-truth --page drv-XX --audience full --dry-run --report "D:\GitHub\faiththruphysics-site\reports\top-bar-drvXX-image-dryrun.json"
```

5. Apply only after review:

```powershell
python "D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts\top_bar_bottom_bar.py" --series revolution-of-truth --page drv-XX --audience full --apply --report "D:\GitHub\faiththruphysics-site\reports\top-bar-drvXX-image-apply.json"
```

6. Use segment-level toggles if one script section should be bypassed:

```powershell
python "...\\top_bar_bottom_bar.py" --series revolution-of-truth --page drv-XX --disable-segments top-bar,bottom-bar --dry-run
```

## Notes

- Keep one image per page during pilot (max 2).
- Do not split to one-off scripts; evolve this script and document toggles here.
- If a page already has a conflicting image intent, place the new image only after explicit review.
