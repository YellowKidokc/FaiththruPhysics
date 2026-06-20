# One-Page Stories Interlude First Batch

This is the reviewable vertical slice for the Kimmy interlude/template migration.

## Prototype Pages

| Room | Theme | Prototype | Original / Full Page |
|---|---|---|---|
| Start Here / Equation / Architecture | Gold | `the-floor-beneath-the-floor-interlude.html` | `the-floor-beneath-the-floor.html` |
| God / Logos / Ground | Crimson | `character-of-god-interlude.html` | `character-of-god-from-physics.html` |
| Salvation / Grace / Judgment | Emerald | `salvation-algorithm-interlude.html` | `salvation-algorithm.html` |
| Adversary / Testing / Broken World | Azure | `character-of-adversary-interlude.html` | `character-of-adversary-from-physics.html` |
| Audit / Bilateral / Lean / Method | Paper | `the-seven-questions-interlude.html` | `7q_explained.html` |

## Implementation Notes

- Originals are untouched.
- New pages are short interludes that link to full/original pages.
- The four new pages share `interlude-prototype.css`; the existing Salvation Test is still self-contained from the prior pass.
- Each page keeps `../components/site-shell.js` and a unique `data-audio-slug`.
- These are intentionally not mass-converted. Use them as design/content examples before scaling.

## Next Prompt For Other Workers

Use these five pages as the pattern. Do not replace original full pages. For each future story, create a `*-interlude.html` page, keep the full derivation linked, preserve site-shell/audio hooks, and validate all local links before handoff.
