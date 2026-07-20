# NotebookLM Asset Inventory

Generated: 2026-07-20  
Source of truth for names: `assets/media-manifest.json` (paths under `D:\GitHub\faiththruphysics-site-data`) plus existing Studio snapshots in-repo.

## Blockers for live capture / PDF redownload

| Need | Status |
| --- | --- |
| Log into [notebooklm.google.com](https://notebooklm.google.com) and screenshot every folder | **Blocked** — this cloud agent has no Google session; NotebookLM redirects to Sign in |
| Redownload slide-deck PDFs from R2 and capture first-page images | **Blocked** — all `documents/one-page-stories/.../*.pdf` and `.../pdf-pages/page-001.webp` URLs return **404**; manifest has `sizeBytes: 0` / `needsDerivative: true` |
| Read PDFs from `faiththruphysics-site-data` | **Not in this workspace** — originals lived on the Windows data root |

**To finish the visual inventory:** either (1) run a **Desktop** Cursor agent already signed into Google and ask it to walk NotebookLM folders, or (2) zip/upload `D:\GitHub\faiththruphysics-site-data\**\notebooklm\**\*__SD__*.pdf` into this repo / agent workspace so first pages can be rendered here.

---

## Slide deck ↔ notebook ↔ series map

Export filenames already encode the Studio slide-deck title after `__SD__`. Use this to line PDFs up with notebooks/series even without first-page images.

| Series folder | Notebook slug | Slide deck PDF (export title) | Deep Dive audio title | Video Overview title |
| --- | --- | --- | --- | --- |
| starting-point | `dictionary` | Theophysics | The Physics of Good and Evil | Theophysics Universal Dial |
| starting-point | `inversion` | THE GREAT INVERSION | Why Society Rebrands Entropy as Freedom | The Great Inversion |
| starting-point | `structural-isomorphism` | Structural Isomorphism | Physics and Theology Share One Architecture | Architectural Symmetry |
| starting-point | `the-floor-beneath-the-floor` | THEOPHYSICS | The quantum physics of the Trinity | The Floor Beneath the Floor |
| starting-point | `the-unavoidable-conclusion` | The Logos Signature | The Mathematical Case for a Creator | The Unavoidable Conclusion |
| breakdown-and-coherence | `terminus` | The Terminus | Five proofs the universe needs an anchor | Terminus Sui Five Proofs |
| measure-and-judgment | `the-93-year-floor` | The 93 Year Floor | The 93 Year Floor of Human Lifespan | The 93-Year Floor |
| Templeton | `templeton_briefing` | The Intelligence Isomorphism | The Mathematical Equation for Human Grace | *(no VO in manifest)* |
| Templeton | `test-death-1` | Jurisdiction Over Death | Why Death Had No Jurisdiction | The Death Test |
| Templeton | `the-bilateral-audit` | Bilateral Audit | The Bilateral Audit of Science and Theology | The Bilateral Audit |
| Templeton | `the-bilateral-audit-lean4` | THE BILATERAL AUDIT | Physics and Theology Share Identical Mathematical Logic | Lean 4 Evidence Layer |
| Templeton | `the-method-and-the-mystery` | THE DIVINE ISOMORPHISM | The Mathematical Architecture of Divine Grace | Theophysics Explainer |
| Templeton | `the-watcher` | Triadic Quantum Unity | How the Trinity solves quantum measurement | The Watcher Problem |
| truth-and-pushback | `the-logos-thesis-v3` | The Eternal Logos | Where math existed before humans | Pre-Human Math |
| truth-and-pushback | `irony` | *(no SD export)* | *(no DD)* | The Divine Irony |

Machine-readable: [`slide-deck-notebook-map.json`](./slide-deck-notebook-map.json)

---

## Extra NotebookLM folders (downloads / Math all)

### `notebooklm_downloads` (audio/video batches)

| Folder | Assets |
| --- | --- |
| Consciousness_15_paper | `Consciousness as a universal scalar field.mp3`, `Your Brain Is A Consciousness Receiver.mp3`, `A New Map of Reality_.mp4` |
| Convergence_Physics_Math_Theology | `Scientific Laws Mirroring Christian Theology.mp3`, `The Mathematical Architecture of the Cross.mp3` |
| Roster_of_Losers | `Why the Most Successful Movement Targeted Felons.mp3` |
| Structural_Taxonomy_Evil | `The Mathematical Impossibility of Evil.mp3`, `Why Evil is a Mathematical Failure.mp3`, `The 24 Anti-Properties.mp4` |
| Substrate_Fracture | `How the Fall Created Quantum Physics.mp3`, `Why Evil Fractured Physics.mp3`, `The Mathematics of Character.mp4` |
| Turtles_and_Floor | `The Master Equation of Physics and Theology.mp3` |
| blackout-pics | five blackout PNGs (names in full inventory) |

### Math all (studio snapshots only; no DD/VO/SD files)

| Notebook (UI title from snapshot) | Snapshot file |
| --- | --- |
| Convergence Series. Scientific method. | [`studio-snapshots/convergence-series-scientific-method-notebooklm-studio-snapshot-2026-06-22.png`](./studio-snapshots/convergence-series-scientific-method-notebooklm-studio-snapshot-2026-06-22.png) |
| Theophysics Research Initiative: The Lean 4 Corpus. | [`studio-snapshots/lean4-theophysics-corpus-notebooklm-studio-snapshot-2026-06-22.png`](./studio-snapshots/lean4-theophysics-corpus-notebooklm-studio-snapshot-2026-06-22.png) |

Lean 4 Studio assets visible in snapshot: *Lean 4 and the shape of God*, *Lean 4 proofs for theophysical models*, *Lean 4 Physics and Theology…*, *Machine Verified Proofs for…*, *Only one redemption is mathematicall…*

---

## MDA NotebookLM Studio snapshots (existing)

These already show notebook title + Studio asset names (including slide decks). First-page PDF images are still missing until PDFs are re-exported.

| Notebook UI title | Source(s) | Slide deck title(s) seen in Studio | Snapshot |
| --- | --- | --- | --- |
| MDA 2: Parts 03 + 04 + 05 | `mda-03-semantic-collapse.md`, `mda-04-cognitive-decline.md`, `mda-05-spiritual-collapse.md` | The 1962 Software Crash | [mda-03…](./studio-snapshots/mda-03-notebooklm-studio-snapshot-mda2-parts-03-04-05-2026-06-22.png) |
| MDA 3: Part 06 | `mda-06-signal-went-dark.md` | Signal Blackout | [mda-06…](./studio-snapshots/mda-06-notebooklm-studio-snapshot-2026-06-22.png) |
| MDA 4: Part 07 | `mda-07-phantom-money.md` | Phantom Money Phantom Morals; Phantom Wealth Terminal | [mda-07…](./studio-snapshots/mda-07-notebooklm-studio-snapshot-mda4-part-07-2026-06-22.png) |
| MDA 5: Part 08 | `mda-08-observer-collapsed.md` | The Observer Collapsed | [mda-08…](./studio-snapshots/mda-08-notebooklm-studio-snapshot-mda5-part-08-2026-06-22.png) |
| MDA 6: Part 09 | `mda-09-amish-proof.md` | The Amish Proof | [mda-09…](./studio-snapshots/mda-09-notebooklm-studio-snapshot-mda6-part-09-2026-06-22.png) |
| MDA 7: Part 10 | `mda-10-way-back.md` | RECOVERY PHYSICS | [mda-10…](./studio-snapshots/mda-10-notebooklm-studio-snapshot-mda7-part-10-2026-06-22.png) |

---

## Counts

- NotebookLM-tagged manifest assets: **249** (see [`full-asset-inventory.json`](./full-asset-inventory.json))
- Story notebooks with slide-deck PDF exports: **14**
- Story notebooks missing SD PDF: **irony** (Divine Irony)
- Local non-NotebookLM PDFs with first-page renders: [`local-pdf-first-pages/`](./local-pdf-first-pages/) (three-truths + quantum-fall only)

---

## Recommended next step

1. On the machine that has `D:\GitHub\faiththruphysics-site-data`, copy every `*__SD__*.pdf` (and optionally `*__SD__*.pptx`) into this repo under `docs/notebooklm-inventory/pdfs/`.
2. Re-run first-page rendering (PyMuPDF) so each notebook gets a cover image next to the name map above.
3. Optionally open NotebookLM in a signed-in Desktop agent and screenshot any folders not covered by the Jun 22 studio snapshots.
