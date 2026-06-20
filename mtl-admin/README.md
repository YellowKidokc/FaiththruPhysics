# MTL Admin — Desktop Uploader

## Open the tool

Double-click:

```text
mtl-admin/Open MTL Uploader.bat
```

No installation needed. It uses Python's built-in Tkinter.

## What it does

1. You pick an MDA article HTML file.
2. It finds every `.equation-block` and extracts the math inside.
3. For each equation you type:
   - **Meaning** — the everyday explanation
   - **Visual** — a readable word-equation / symbol-by-symbol version
4. Click **Save translations**.

The tool writes to:

```text
shared/data/mtl-overlay-translations.json
```

The MTL overlay (`mtl-overlay.js`) fetches that file and shows your reviewed translations instead of its automatic guess.

## Why this is dead simple

- You do **not** edit any HTML by hand.
- You do **not** pick reading levels.
- You upload once per article, and the overlay handles the rest on every page load.

## No equations found?

Make sure the article uses `<div class="equation-block">...</div>` with math inside `\[ ... \]`, `$$ ... $$`, or `\( ... \)`.

## Full guide

See `../MTL-SETUP-GUIDE.md`.
