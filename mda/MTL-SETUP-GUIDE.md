# Math Translation Layer (MTL) — Self-Service Setup Guide

> The MTL overlay auto-translates equations on every MDA page. This guide explains how to add reviewed translations so the overlay shows your own plain-English meanings instead of its automatic guesses.

---

## 1. What the MTL overlay does

Every MDA page loads `mtl-overlay.js`. It scans the page for equations inside `<div class="equation-block">` blocks (and other math markup) and inserts a translation card under each one.

The card shows:
- a **word equation** (visual, symbol-by-symbol)
- an **everyday meaning**
- a structural breakdown

By default the overlay generates these automatically. If you upload reviewed translations, it uses those instead.

---

## 2. The dead-simple upload process

### Open the desktop uploader

Double-click:

```text
D:\GitHub\faiththruphysics-site\mtl-admin\Open MTL Uploader.bat
```

No installation. No command line. It uses Python's built-in Tkinter.

### Upload an article

1. Click **Choose HTML file** and pick any MDA article.
2. The tool finds every `.equation-block` and extracts the math.
3. For each equation, type:
   - **Meaning** — the everyday explanation
   - **Visual** — a readable word-equation / symbol-by-symbol version
4. Click **Save translations**.

The tool writes to:

```text
shared/data/mtl-overlay-translations.json
```

That's it. The overlay will now use your reviewed translations on every page load.

---

## 3. Files you actually touch

| File | Purpose |
|------|---------|
| `mtl-admin/Open MTL Uploader.bat` | Double-click launcher for the upload tool. |
| `mtl-admin/mtl_uploader.pyw` | The upload tool itself. |
| `shared/data/mtl-overlay-translations.json` | Reviewed translations the overlay reads. |
| `shared/js/mtl-overlay.js` | The built overlay from `D:\GitHub\Math-Translation-Layer`. |
| `shared/js/mtl-overlay-loader.js` | Loads the JSON and exposes it to the overlay. |

Files you **do not** need to edit by hand:
- Individual MDA HTML files — the bars and script links are injected automatically by `mda/cleanup_and_rebuild_bars.py`.

---

## 4. Manual JSON format

If you prefer to edit JSON directly, open `shared/data/mtl-overlay-translations.json`. It is an array of records:

```json
[
  {
    "key": "chiapproxpminuspcbeta",
    "equation": "\\chi \\approx |P - P_c|^{\\beta}",
    "meaning": "Near a critical point, coherence scales as a power law of how far the control parameter is from its threshold.",
    "visual": "coherence ≈ distance from critical point raised to the scaling exponent"
  }
]
```

- `key` — a normalized version of the equation used for lookup. The uploader computes this for you.
- `equation` — the original LaTeX.
- `meaning` — everyday explanation.
- `visual` — readable word equation.

The overlay matches equations by key, so the same translation appears wherever that exact equation is used.

---

## 5. How the key is generated

The key normalizes the LaTeX by:
- spelling out Greek letters (`\chi` → `chi`, `\pi` → `pi`, etc.)
- removing commands like `\text`, `\mathrm`, `\left`, `\right`, `\cdot`
- removing all non-alphanumeric characters
- lowercasing

Example:

```text
\chi \approx |P - P_c|^{\beta}
```

becomes:

```text
chiapproxpminuspcbeta
```

The uploader shows the key under each equation so you can verify it.

---

## 6. Rebuilding after structural changes

If you add or remove equations from an article, or if you move files around, run:

```bash
cd D:\GitHub\faiththruphysics-site
python mda\cleanup_and_rebuild_bars.py
```

This refreshes the shared top bars and makes sure every page has the overlay loader in the right order.

---

## 7. Claim highlighting

The MTL reader bar now has a **Claims** tab. Clicking it:

- Highlights claim sentences inside paragraphs (sentences containing words like *claim, argue, therefore, conclude, proves, shows*).
- Adds a small "Claims in this paragraph" list below each paragraph that contains one or more claims.
- Clicking a claim chip scrolls to and highlights the exact sentence.

This is automatic — no upload or JSON editing required. It runs client-side via `shared/js/mtl-claims.js`.

If you want different signal words or want to exclude certain paragraphs, edit the `CLAIM_RE` regex at the top of `shared/js/mtl-claims.js`.

---

## 8. Rebuilding the overlay itself

The overlay is built from the standalone TypeScript repo at `D:\GitHub\Math-Translation-Layer`.

To rebuild it after editing the source:

```bash
cd D:\GitHub\Math-Translation-Layer
npm install
npm run build
```

Then copy the built file into the site:

```bash
cp D:\GitHub\Math-Translation-Layer\dist\browser\math-translation-overlay.js \
   D:\GitHub\faiththruphysics-site\shared\js\mtl-overlay.js
```

Finally, refresh the MDA pages:

```bash
cd D:\GitHub\faiththruphysics-site
python mda\cleanup_and_rebuild_bars.py
```

---

## 9. Quick checklist

- [ ] Opened `mtl-admin/Open MTL Uploader.bat`
- [ ] Chose the MDA article HTML
- [ ] Filled Meaning and Visual for each equation
- [ ] Clicked Save translations
- [ ] Deployed `shared/data/mtl-overlay-translations.json`
- [ ] Deployed `shared/js/mtl-overlay-loader.js` and `shared/js/mtl-overlay.js`
- [ ] Deployed `shared/js/mtl-claims.js` and `shared/css/mtl-claims.css`
- [ ] Deployed the rebuilt MDA HTML files

---

**Tip:** If you delete a translation from `shared/data/mtl-overlay-translations.json`, the overlay falls back to its automatic guess for that equation.
