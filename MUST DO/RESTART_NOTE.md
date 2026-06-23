# Restart Note

Date: 2026-06-21

What is done:

- Added `MUST DO/build_article.py`
- Added `MUST DO/ARTICLE_PACKAGES/README.md`
- Updated `MUST DO/ARTICLE_PIPELINE_SPEC.md` to point at the real build path
- Built a sample package successfully:
  - `MUST DO/_built/the-question/index.html`

How the pipeline is supposed to work:

1. Create one folder per article under `MUST DO/ARTICLE_PACKAGES/`.
2. Include `meta.json`, `story.md`, `plain.md`, `test.md`, and `proof.md`.
3. Put optional local assets in `audio/` and `media/`.
4. Run:

```powershell
python "MUST DO/build_article.py" the-question
```

Output:

- `MUST DO/_built/<slug>/index.html`
- copied `meta.json`
- copied `source/` markdown files
- copied `audio/` and `media/` assets

Notes:

- The builder is dependency-light and uses the package folder as the single input.
- The sample output is valid, but the site still has existing unrelated workspace changes.
- If you want the next pass, the likely follow-up is to point the site navigation or series pages at the `_built` output.
