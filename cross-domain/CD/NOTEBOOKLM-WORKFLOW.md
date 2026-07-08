# Cross-Domain (CD) — NotebookLM Workflow

Source project on desktop:

`\\192.168.2.50\h_hp\Desktop\[TX_A5.1] Cross-Domain Coherence Project`

This repo folder mirrors that project under `cross-domain/CD/` with short human labels.

---

## Domain Map

| Desktop folder | CD folder |
|---|---|
| `00_CANONICAL_THEOPHYSICS_SYNTHESIS` | `Canonical Synthesis` |
| `01_Federal_Reserve` | `Federal Reserve` |
| `02_Psychology_Crisis` | `Psychology Crisis` |
| `03_Education` | `Education` |
| `04_Scientific_Method` | `Scientific Method` |
| `05_Theological_Engineering` | `Theological Engineering` |
| `07_Semantic_Entropy` | `Semantic Entropy` |
| `08_Coherence_Tools` | `Coherence Tools` |
| `12_Demographics` | `Demographics` |
| `13_Architecture` | `Architecture` |
| `14_AI_Synthesis_Final` | `AI Synthesis Final` |

Each domain folder has:

- `sources/` — good markdown only (canonical article text)
- `notebooklm/` — generated outputs + rename manifest

---

## Per-Domain Pipeline

For each domain, run this order in NotebookLM:

1. **Drop sources** — copy vetted `.md` files into `sources/`
2. **Slideshow** — use the **Black It Out** prompt (no filename prefix)
3. **Deep Dive** — long audio; prefix rename with `DD `
4. **Debate** — prefix rename with `D `
5. **Critique** — prefix rename with `AC `
6. **Video** — one explainer only; no prefix
7. **Reading level check** — flag words above 8th grade; add definitions; move on

---

## NotebookLM Rename Rules (Audio)

These prefixes go on the **NotebookLM output title**, not on source markdown.

| Output type | Prefix | Example |
|---|---|---|
| Debate audio | `D ` | `D How the Federal Reserve Devalues Your Dollar` |
| Deep Dive audio | `DD ` | `DD Where Your Missing Sixty Four Percent Went` |
| Critique audio | `AC ` | `AC The Physics of the Cantillon Effect` |
| Explainer video | *(none)* | `The Chain of Paper` |
| Slideshow | *(none)* | `MONETARY DECOHERENCE` |

Rules:

- One leading `D` for debate — not `DD`, not `Debate`
- Two Ds with a space for deep dive — `DD Title Here`
- `AC` with a space for critique — `AC Title Here`
- Video and slideshow keep clean titles — no prefix

---

## NotebookLM Prompts

### Slideshow — Black It Out

Use NotebookLM's slideshow generator with the blackout instruction:

> Black it out. Minimal text per slide. One claim per slide. No paragraph blocks. High contrast. Let the spoken audio carry the explanation.

### Deep Dive (long audio)

Pick the **middle-length long-form** deep dive prompt from the project instructions. This is the main teaching pass.

Rename output: `DD [title]`

### Debate

Steel-man both sides. Adversarial but fair.

Rename output: `D [title]`

### Critique

Audit claims, evidence gaps, kill conditions.

Rename output: `AC [title]`

### Video

One explainer per domain. No prefix on the title.

---

## 8th Grade Reading Level Pass

After audio generation, ask NotebookLM (or run locally):

> List every word or phrase in this material above an 8th-grade reading level. For each, give a one-sentence plain-English definition a 14-year-old would understand. Do not remove claims — only define terms.

Save definitions in `notebooklm/vocabulary.md` for that domain.

---

## Source Markdown Rules

Only drop markdown into `sources/` when:

- Claims are stated clearly
- Evidence is cited
- Voice matches Theophysics (direct, no hedging)
- No duplicate/conflicting drafts

Do **not** prefix source files with `D`, `DD`, or `AC`. Prefixes are for NotebookLM outputs only.

---

## Federal Reserve Pilot (current)

See `Federal Reserve/notebooklm/manifest.json` for the live rename map from the first completed notebook.
