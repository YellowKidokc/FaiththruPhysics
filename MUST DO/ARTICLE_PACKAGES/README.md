# Article Package Contract

One folder per article. That is the only input another AI needs.

## Required structure

```text
ARTICLE_PACKAGES/
`-- article-slug/
    |-- meta.json
    |-- story.md
    |-- plain.md
    |-- test.md
    |-- proof.md
    |-- audio/
    `-- media/
```

## File roles

- `meta.json` drives the page title, subtitle, series, navigation, classification, audio links, and formal references.
- `story.md` is the human-first narrative version.
- `plain.md` is the clear, non-technical version.
- `test.md` holds claims, objections, evidence, and kill conditions.
- `proof.md` holds the formal layer: equations, Lean references, datasets, and rigor notes.
- `audio/` holds optional MP3s and `tts-source.txt`.
- `media/` holds the hero image and any figures.

## Build command

From the repo root:

```powershell
python "MUST DO/build_article.py" the-question
```

If no slug is passed, the script builds every package that has a `meta.json`.

## Output

The builder writes each article to:

```text
MUST DO/_built/<slug>/index.html
```

It also copies the package metadata and any local `audio/` or `media/` assets into the build folder so the HTML stays self-contained.

## Minimum viable `meta.json`

- `slug`
- `title`
- `status`
- `classification`

Everything else can be added as the pipeline matures.

## Recommended `meta.json` fields

- `subtitle`
- `author`
- `date`
- `series`
- `series_title`
- `series_order`
- `prev`
- `next`
- `audio`
- `options`
- `formal_refs`

## What the builder does

1. Reads the package.
2. Converts the Markdown files into HTML sections.
3. Renders the reading tabs.
4. Renders the classification bar.
5. Renders the audio dock when audio is available.
6. Copies assets into the output folder.
7. Writes the final `index.html`.

## What an AI collaborator should do

Create the folder, fill the Markdown files, write `meta.json`, and let the builder handle everything downstream.
