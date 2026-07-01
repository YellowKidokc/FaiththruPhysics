# 08 — MathJax & References

## MathJax config (critical)

In `_TEMPLATE.html`, delimiters **must** use double backslashes in JS strings:

```javascript
tex: {
  inlineMath: [['$','$'], ['\\(','\\)']],
  displayMath: [['$$','$$'], ['\\[','\\]']]
},
```

Single `\(` in JS becomes `(` → inline math breaks (red raw TeX, squished text).

## References section

`article_html.py` detects References / Bibliography heading → wraps in `<section class="tp-refs">`.

CSS: compact numbered hanging-indent list — all reading levels.

## Math Translation Layer

Folder: `MUST DO/math-translation-layer/`

- **New:** `mtl-callout.css` + `mtl-callout.js` — equation → English → meaning
- **Deprecated:** `mtl-overlay.js` — do not use on new pages

## College equation cards

Standalone display math wrapped by `college_enrich.py` → `.tp-eqcard` (separate from MTL callouts).
