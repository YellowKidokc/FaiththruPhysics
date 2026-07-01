# Page Shell Image Workflow (Hands-On)

## Why this exists

This note keeps the image + page-shell workflow in one place so edits stay reusable and can be expanded through a single script.

## Current practice

- Use the `revolution-of-truth` markdown sources in `faiththruphysics-site-data`.
- Put image markup in source markdown so the same image renders in all output levels that reference that source file.
- Keep `faiththruphysics-site-data` as content source; keep rendered pages in `faiththruphysics-site`.

## What to edit first (single-page pilot)

1. Edit one page in small pieces.
2. Add image blocks in:
   - `faiththruphysics-site-data\\revolution-of-truth\\drv-00-the-argument.canonical.md` (college/pivot)
   - `faiththruphysics-site-data\\revolution-of-truth\\highschool\\drv-00-the-argument.canonical.md` (easy)
   - `faiththruphysics-site-data\\revolution-of-truth\\phd\\drv-00-the-argument.canonical.md` (academic)
3. Run `--dry-run` first, then `--apply` on the same page to confirm.

## Example image tag used in markdown

```md
<img src="/media/media/series-opener.webp" alt="Revolution of Truth visual map" style="display:block; width:100%; max-width:980px; margin:1.5rem auto; border-radius:8px; border:1px solid rgba(212,175,55,.25);" />
```

## Rebuild commands for one page

```bash
cd "D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts"
python top_bar_bottom_bar.py --series revolution-of-truth --page drv-00-the-argument --audience full --dry-run --report "D:\GitHub\faiththruphysics-site\reports\top-bar-drv00-image-dryrun.json"
python top_bar_bottom_bar.py --series revolution-of-truth --page drv-00-the-argument --audience full --apply --report "D:\GitHub\faiththruphysics-site\reports\top-bar-drv00-image-apply.json"
```

## Keep improving, don’t fork

- Keep edits to `top_bar_bottom_bar.py` and shared markdown sources.
- Avoid one-off scripts for the same task unless it becomes a stable new capability.
