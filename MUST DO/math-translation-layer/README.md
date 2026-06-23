# Math Translation Layer (MTL) — Article-Integrated Equation Callouts

## Status

The old generic overlay (`mtl-overlay.js`, `mtl-overlay-loader.js`, `mtl-equation.js/css`, `mtl-reader-bar.html/css`) is **deprecated**. It translated equations in isolation and did not feel like part of the article chrome.

The new approach is an **in-article equation callout**: formal equation → physics↔spiritual mapping → “Read it in English” → “What this means” → optional derived claim/test condition.

## New files

| File | Purpose |
|------|---------|
| `mtl-callout.css` | Styles for `.mtl-callout` blocks. Scoped to the article body; respects host theme variables. |
| `mtl-callout.js` | Progressive enhancement: toggles translation panels, tracks `aria-expanded`, supports `data-default="open"`. |
| `mtl-callout-template.html` | Copy-paste template for Master Equation and standard equation variants. |

## Deprecated files (kept for reference only)

- `mtl-overlay.js`
- `mtl-overlay-loader.js`
- `mtl-equation.js`
- `mtl-equation.css`
- `mtl-reader-bar.html`
- `mtl-reader-bar.css`
- `mtl-claims.js`
- `mtl-claims.css`

## How to use

1. Make sure the page already loads the shared shell:
   ```html
   <script id="article-meta" type="application/json">{ ... }</script>
   <script src="/components/tp-inject.js" data-theme="dark"></script>
   ```
2. Load the MTL assets in the article `<head>`:
   ```html
   <link rel="stylesheet" href="/MUST%20DO/math-translation-layer/mtl-callout.css">
   ```
3. Load the MTL script near `</body>`:
   ```html
   <script src="/MUST%20DO/math-translation-layer/mtl-callout.js"></script>
   ```
4. Replace each generic `.equation-block` with the markup from `mtl-callout-template.html`.
5. Fill in the mapping, English reading, meaning, and optional derived claim/test condition from canon. **Do not rewrite canon.** If a claim is stale or unsupported, flag it with `.mtl-callout__flag` instead of silently fixing it.

## Canonical rules

- Do not renumber laws or change claims during presentation cleanup.
- Flag stale/unsupported math claims with `.mtl-callout__flag`.
- Keep the translation tied to the specific equation on the page; do not paste generic text.

## Pages already converted

- `convergence-deep/cdt-01-math-is-moral.html` — Master Equation + Coherence Evolution
- `MUST DO/article-template.html` — template with example callout and `tp-inject.js`
- `MUST DO/MDA-010-pre-modern-baseline-reading-ladder-v2.html` — assets loaded; shell migration pending
