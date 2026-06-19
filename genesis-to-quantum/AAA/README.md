# AAA Templates — Reader Output Layer

This folder is the shared output contract used by GTQ/MDA pages.

What to use:
- `templates/reader-output.schema.json` → canonical JSON payload contract for each page
- `templates/reader-output.template.md` → markdown layout used by export and editorial review

Drop both into page generation so every article can emit:
- 8th-grade / easy paraphrase
- academic version
- lossless compression
- proof summary with falsification tests
- math translation notes (optional)
- machine-readable stats for downstream spreadsheets

Both `template-main.html` and `template-deepdive.html` now contain `reader-output` placeholders that match the same schema.

Expected behavior:
- `article_slug` + `article_title` are required identifiers
- the JSON block is inserted into `<script id="readerOutputPayload" type="application/json">...</script>`
- each page can copy/paste the markdown section for editorial or manual publishing
