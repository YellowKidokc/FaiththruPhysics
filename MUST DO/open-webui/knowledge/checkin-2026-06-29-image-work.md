# Check-in: 2026-06-29

## Reviewed

- `MUST DO/open-webui/knowledge/page-shell-image-workflow.md`
- `MUST DO/open-webui/prompts/image-placement-feedback-loop.md`
- `MUST DO/PAGE-SHELL-GOLD-STANDARD/scripts/top_bar_bottom_bar.py`
- `D:\GitHub\faiththruphysics-site-data\revolution-of-truth` source markdown targets (`drv-00` and `drv-01`)
- Rebuild output for `D:\GitHub\faiththruphysics-site\revolution-of-truth`

## Added

- `MUST DO/open-webui/skills/revolution-of-truth-image-shell-skill.md`
- Page image blocks for:
  - `D:\GitHub\faiththruphysics-site-data\revolution-of-truth\drv-01-the-architecture.canonical.md`
  - `D:\GitHub\faiththruphysics-site-data\revolution-of-truth\highschool\drv-01-the-architecture.canonical.md`
  - `D:\GitHub\faiththruphysics-site-data\revolution-of-truth\phd\drv-01-the-architecture.canonical.md`

## Changed

- Ran `top_bar_bottom_bar.py` dry-run and apply for `drv-01-the-architecture`:
  - `reports/top-bar-drv01-image-dryrun.json`
  - `reports/top-bar-drv01-image-apply.json`
- Rebuilt `D:\GitHub\faiththruphysics-site\revolution-of-truth\drv-01-the-architecture.html` from the updated markdown with all segments enabled.
- Kept `page-shell` and top/bottom logic in the single script path (no one-off ad hoc scripts).

## Still Needs Work

- Decide next page(s) to add images to (single-page increments still recommended).
- Confirm placement preference for each slug (before intro, between sections, etc.).
- If desired, start a small "disable segment" rehearsal with `--disable-segments` once placement stability is confirmed.
