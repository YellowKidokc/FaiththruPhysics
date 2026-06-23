# Math Translation Layer Workflow

## Goal

Every equation in an article should be readable without leaving the article flow. The callout answers four questions in order:

1. What is the physics↔spiritual mapping of the symbols?
2. What does it say in plain English?
3. What does it mean for the argument?
4. What claim does it generate, and how could it be tested?

## Step-by-step

### 1. Pick a representative article

Prefer articles that already load `components/tp-inject.js` and contain `.equation-block` elements. Good starting examples:

- `convergence-deep/cdt-01-math-is-moral.html`
- `convergence-deep/cdt-02-the-maxwell-moment.html`
- `convergence-deep/cdt-03-the-energy-that-doesnt-run-out.html`

### 2. Load assets

In the `<head>`:
```html
<link rel="stylesheet" href="/MUST%20DO/math-translation-layer/mtl-callout.css">
```

Near `</body>`, after any MathJax script and before `tp-inject.js`:
```html
<script src="/MUST%20DO/math-translation-layer/mtl-callout.js"></script>
<script src="/components/tp-inject.js" data-theme="dark"></script>
```

### 3. Replace each `.equation-block`

Copy the structure from `mtl-callout-template.html`. At minimum include:

- `.mtl-callout__header` with label and toggle
- `.mtl-callout__formula` with the math
- `.mtl-callout__mapping`
- `.mtl-callout__english`
- `.mtl-callout__meaning`

Optional but encouraged:

- `.mtl-callout__claim`
- `.mtl-callout__test`

### 4. Fill content from canon

- Mapping entries must match the symbols actually used in the equation.
- “Read it in English” should be a full sentence a non-specialist can follow.
- “What this means” connects the equation to the surrounding argument.
- Derived claims must be traceable to the text. If they aren't, flag them.

### 5. Flag stale claims

If you encounter a claim that the equation no longer supports, add:

```html
<div class="mtl-callout__flag">⚠︎ This mapping is under canonical review.</div>
```

Do not silently rewrite the underlying claim.

### 6. Verify

- Open the page and confirm the shared shell renders (top bar, classification bar, bottom audio dock, subdomain strip).
- Confirm the equation callout toggles open and closed.
- Confirm MathJax renders the formula inside `.mtl-callout__formula`.
- Check mobile: the callout should not overflow horizontally.

## Batch migration

After the representative articles are verified, extend the conversion to other articles with `.equation-block` elements. Use the file list from:

```bash
rg "class=\"equation-block\"" --files-with-matches
```

For pages with older shells (`mda-topbar-v2`, `site-shell.js`, `tp-pill-player.js`), either migrate the shell first or ensure `tp-inject.js` skips injection to avoid duplicate chrome.
