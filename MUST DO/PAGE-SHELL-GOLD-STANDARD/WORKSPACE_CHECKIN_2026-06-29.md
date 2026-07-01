# Workspace Check-in: Top Bar Segmentation

Date: 2026-06-29
Folder: `D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD`

What I reviewed
- `scripts/top_bar_bottom_bar.py` in this folder for segment toggles, audience profile behavior, and report output.
- `scripts/README.md`, `skills/page-shell-builder.md`, `00_INDEX.md`, and `README.md` for canonical run instructions.

What I added
- Updated docs to treat this folder as the practical execution copy for shell work (instead of `Python-WEB`).
- Added explicit examples for:
  - `--segments`
  - `--disable-segments`
  - `--audience`
  - `--report`
- Added check-in report at `reports/top-bar-academic-drv00-20260629.json`.
- Added this check-in note file so the workspace state is recoverable.
- Added full-run dry-run reports:
  - `reports/top-bar-easy-fullsegments-20260629.json`
  - `reports/top-bar-academic-fullsegments-20260629.json`

What I changed
- `skills/page-shell-builder.md`: path table and script command examples now point to `MUST DO\\PAGE-SHELL-GOLD-STANDARD\\scripts` and include new segment/audience/report flags.
- `scripts/README.md`: replaced Python-WEB-centric guidance with local run guidance and new control flags.
- `00_INDEX.md` and `README.md`: updated workflow pointers and one-command notes for local script execution and report generation.

What still needs work
- `09-evaluation-pipeline/README.md`, `gold-standard/drv-00-checklist.md`, and theme READMEs still reference `D:\\GitHub\\Python-WEB` for command entry points.
- `top_bar_bottom_bar.py` currently writes a report and script output to `faiththruphysics-site-data/_inject_backups` with unchanged schema; if you want a standardized artifact format, we can add a small post-processing script.

Full report references
- `reports/top-bar-academic-drv00-20260629.json`
- `reports/top-bar-easy-fullsegments-20260629.json`
- `reports/top-bar-academic-fullsegments-20260629.json`
