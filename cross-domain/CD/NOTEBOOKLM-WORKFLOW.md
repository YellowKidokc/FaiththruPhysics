# Cross-Domain (CD) — NotebookLM Workflow

Source project on desktop:

`\\192.168.2.50\h_hp\Desktop\[TX_A5.1] Cross-Domain Coherence Project`

This repo mirrors that project under `cross-domain/CD/` using the **CD package code** system.

---

## Naming System

Every package in this series uses:

1. **Series prefix:** `CD` = Cross Domain
2. **Package code:** 4-letter code (example: `CDCS` = Canonical Synthesis)
3. **Folder name:** `CD-{CODE}-{Domain-Name}`
4. **Display name:** `CD {Domain Name}`

Example:

- Code: `CDCS`
- Folder: `CD-CDCS-Canonical-Synthesis/`
- Display: `CD Canonical Synthesis`

---

## Package Map

| Code | CD folder | Desktop source |
|---|---|---|
| `CDCS` | Canonical Synthesis | `00_CANONICAL_THEOPHYSICS_SYNTHESIS` |
| `CDFR` | Federal Reserve | `01_Federal_Reserve` |
| `CDPC` | Psychology Crisis | `02_Psychology_Crisis` |
| `CDED` | Education | `03_Education` |
| `CDSM` | Scientific Method | `04_Scientific_Method` |
| `CDTE` | Theological Engineering | `05_Theological_Engineering` |
| `CDSE` | Semantic Entropy | `07_Semantic_Entropy` |
| `CDCT` | Coherence Tools | `08_Coherence_Tools` |
| `CDDM` | Demographics | `12_Demographics` |
| `CDAR` | Architecture | `13_Architecture` |
| `CDAI` | AI Synthesis Final | `14_AI_Synthesis_Final` |

Each package folder contains:

- `sources/` — 3 vetted markdown files
- `notebooklm/manifest.json` — output plan + rename rules
- `README.md` — quick reference

---

## Standard Pipeline (Every CD Package)

Run in this order for **every** domain in the series:

1. **Sources** — upload the 3 files from `sources/`
2. **Slideshow** — type **Black it out** (no title prefix)
3. **Deep Dive** — long audio; rename with `DD `
4. **Debate** — rename with `D `
5. **Video** — one long-form explainer; no prefix
6. **Vocabulary pass** — list words above 8th-grade reading level

---

## NotebookLM Rename Rules

Prefixes apply to **NotebookLM output titles**, not source markdown filenames.

| Output | Prefix | Example |
|---|---|---|
| Deep Dive | `DD ` | `DD The Master Equation Across Every Domain` |
| Debate | `D ` | `D Is Cross Domain Coherence Real or Retrofit` |
| Slideshow | *(none)* | `THEOPHYSICS SYNTHESIS` |
| Video (long form) | *(none)* | `One Framework, Seven Colors` |

---

## Slideshow Prompt — Black It Out

> Black it out. Minimal text per slide. One claim per slide. No paragraph blocks. High contrast. Let the spoken audio carry the explanation.

---

## Production Order

Start with **CDCS** (Canonical Synthesis), then continue through the list in code order:

`CDCS → CDFR → CDPC → CDED → CDSM → CDTE → CDSE → CDCT → CDDM → CDAR → CDAI`

---

## 8th Grade Reading Level Pass

After outputs are generated:

> List every word or phrase above an 8th-grade reading level. For each, give a one-sentence plain-English definition a 14-year-old would understand. Do not remove claims — only define terms.

Save to `notebooklm/vocabulary.md` inside that package folder.
