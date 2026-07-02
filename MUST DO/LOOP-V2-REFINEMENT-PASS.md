# LOOP V2 — SHELL REFINEMENT PASS (Handoff Spec)
**POF 2828 · July 1, 2026 · Status: ACTIVE — supersedes all prior broad-sweep loop instructions**
**Audience: any worker (Codex / Cursor / Kimi / Claude). Read fully before touching a file.**

> Loop v1 was a DISCOVERY loop — it was figuring out what the shell should be.
> Loop v2 is a REFINEMENT loop — it ENFORCES what the shell already is.
> If you find yourself redesigning the shell, stop. That is out of scope. File it as Needs Review.

## 0 · REQUIRED READING (in this order, before any edit)

1. `MUST DO/PAGE-SHELL-CLINICAL-TERMS.md` — the defect vocabulary. Use these exact terms in every report.
2. `MUST DO/PAGE-SHELL-GOLD-STANDARD/00_INDEX.md` — the frozen standard map.
3. `MUST DO/WHITE-PAGE-FIX-PROCESS.md` — the only approved white-page fix.
4. This document.

## 1 · THE FROZEN STANDARD (do not reinterpret)

| Layer | Gold standard | Authority file |
|---|---|---|
| Page-level reference | `revolution-of-truth/drv-00-the-argument.html` | rendered page itself |
| Top bar | brand + Home/MTL/Proof + series lip toggle + HS/College/PhD tabs + search | `PAGE-SHELL-GOLD-STANDARD/01-top-bar/` |
| Header lip | domain meter (sums to 100%) + tags + prev/next + series grid | `02-header-lip/` |
| Verified bar | axioms, laws, χ, bridges, domain chips, expand panel — loads real JSON, never em-dashes | `03-verified-bar/` |
| Reading levels | three panels (HS / College / PhD), all load | `04-reading-levels/` |
| Article body | College drop caps, equation cards, feature boxes, section rhythm | `05-article-body/` |
| Bottom nav | big prev/next cards + series home + sub-series strip | `06-bottom-nav/` |
| Audit foot | Right / Overstated / Wrong, rigor JSON when present | `07-audit-foot/` |
| Math | MathJax renders inline + display (never raw red `\(`) | `08-math-references/` |
| Dark theme | dark reset first in `<head>`: `html,body{background:#050505;color:#e0e0e0;}` | `WHITE-PAGE-FIX-PROCESS.md` |
| Shell loader | `/site-shell/frame.js` (local) — normalize remote→local unless page documented as exception | clinical terms §Local Shell Source |

**FROZEN means:** workers may not change the standard's structure, spacing, colors, or behavior.
Standard changes require David's explicit sign-off, recorded by updating the gold-standard folder FIRST, then rebuilding pages FROM it. Never patch the standard inside an individual article.

## 2 · THE PAGE-FIX CHECKLIST (run per page, in order)

Every check has: TEST (deterministic), FIX PATH, and CLASS (AUTO = safe-to-auto-fix, REVIEW = needs review).

| # | Check | TEST (pass condition) | Fix path | Class |
|---|---|---|---|---|
| C1 | ONE top bar only | exactly 1 shell header in DOM; zero legacy `header.tp-top` / `.tp-class` alongside new shell | strip legacy shell residue, keep canonical bar (migration pass) | AUTO if legacy pattern matches known markup; REVIEW if interleaved with content |
| C2 | ONE bottom/audio system only | ≤1 audio dock + ≤1 mini-player + 1 bottom nav; no stacked old docks | remove duplicate/legacy dock (bottom-dock regression) | AUTO |
| C3 | No white page | dark reset present as FIRST style in `<head>`; no inner container forcing white | `WHITE-PAGE-FIX-PROCESS.md`, minimal reset first, expanded block only if still white | AUTO |
| C4 | No broken JS/CSS links | every `<script src>` / `<link href>` resolves locally (file exists) or is a known CDN (MathJax, fonts) | rewrite path or flag; never delete a functional include | AUTO for path rewrites to existing files; REVIEW for missing assets |
| C5 | Headings styled | h1 present once; h1/h2/h3 inherit shell styles; no title merge regression (h1+subtitle collapsed) | restore split title/subtitle from source md/canonical | REVIEW (touches content boundary) |
| C6 | Reading layers present where expected | series flagged as leveled (see §3 table) → 3 panels present and switchable; single-level series exempt | rebuild page via `top_bar_bottom_bar.py` from canonical md | AUTO via builder only — never hand-write panels |
| C7 | Verification block present where expected | verified bar markup + `data-verification-slug` set; JSON loads or shows honest "pending" state, never em-dash garbage | wire slug; if JSON missing, mark pending in report (do NOT fabricate data) | AUTO for wiring; REVIEW for missing JSON |
| C8 | No duplicate shell artifacts | zero double-shell defect; zero legacy residue (live markup); dead CSS noted but not blocking | migration pass per clinical terms | AUTO |
| C9 | Readable, not overcrowded | body max-width respected; spacing rhythm matches drv-00; no component stacked on component | spacing normalization only; if judgment needed → REVIEW with screenshot | REVIEW default |

**HARD RULES (unchanged from Loop v1, non-negotiable):**
- NEVER rewrite article prose, theology, math content, dates, citations, claims, or χ/verification numbers.
- NEVER fabricate verification data. Missing JSON = "pending", reported.
- Backup every file before write (`_loop-v2-backups/<batch>/<series>/`).
- Idempotent: running the loop twice must change nothing the second time.
- Unknown situation = STOP + report (Needs Review). Guessing is a defect.

## 3 · SERIES ORDER (batches — never "the whole universe at once")

Root: `D:\GitHub\faiththruphysics-site\`

| Batch | Series folder | Leveled (C6)? | Notes |
|---|---|---|---|
| 1 | `revolution-of-truth/` | YES | gold standard lives here; should be nearly clean — this batch CALIBRATES the loop |
| 2 | `consciousness/` | YES (teal theme) | first real enforcement target |
| 3 | `genesis-to-quantum/` | YES | check prev/next chain naming before trusting auto-nav |
| 4 | `one-page-stories/` | NO (single-level) | C6 exempt; C1–C5, C7–C9 apply |
| 5 | the rest, one at a time: `moral-decline/` + `mda/`, `convergence/` (+`-deep`,`-series`), `logos-papers/`, `three-truths/`, `three-gates/`, `cross-domain/`, `duality-project/`, `Introduction to Theophysics/`, `formal-papers/` | per-series call | each gets its own batch + gate; NEVER combined |

Batch protocol: **audit pass (read-only) → report → David YES → repair pass → regression gate → next batch.**
No batch begins until the previous batch's gate is green. One series at a time. No exceptions.

## 4 · AUDIT GATE (after every batch — all four, every time)

| Gate | What | Pass condition |
|---|---|---|
| G1 Scanner | full checklist C1–C9 re-run on every page in batch | zero AUTO-class defects remaining; REVIEW items filed, not hidden |
| G2 White-page check | headless or manual load of every page | zero white-page regressions |
| G3 Shell-duplication check | grep for legacy `.tp-top`/`.tp-class` live markup + double dock | zero double-shell defects, zero live legacy residue |
| G4 Visual spot check | HUMAN (David or designate) opens ≥3 pages/batch: first, last, one random | matches drv-00 feel; no theme-integrity failure |

Gate output per batch → `reports/loop-v2/<batch>-<series>-gate.md` containing:
pages scanned · defects found by clinical term · defects fixed (AUTO) · defects filed (REVIEW) · files changed w/ backup paths · idempotence confirmation (second run = 0 changes) · G1–G4 verdicts.

**Regression gate definition (clinical terms):** prove (1) the intended defect class was fixed AND (2) unrelated page regions did not regress. Both, or the batch stays open.

## 5 · WORKER ASSIGNMENT TEMPLATE (copy-paste per batch)

> You are running LOOP V2 batch <N> on series `<folder>`. This is a REFINEMENT pass, not a discovery pass.
> Read `MUST DO/PAGE-SHELL-CLINICAL-TERMS.md`, `MUST DO/PAGE-SHELL-GOLD-STANDARD/00_INDEX.md`,
> `MUST DO/WHITE-PAGE-FIX-PROCESS.md`, and `MUST DO/LOOP-V2-REFINEMENT-PASS.md` first.
> Gold standard: `revolution-of-truth/drv-00-the-argument.html`. The standard is FROZEN — enforce it, never redesign it.
> Phase 1: AUDIT PASS only (read-only). Produce the gate report. STOP and wait for YES.
> Phase 2 (after YES): REPAIR PASS — fix AUTO-class defects only, per checklist fix paths, with backups, idempotently.
> File every REVIEW-class item; do not attempt it. Never touch prose, math, claims, or verification numbers.
> Finish with the regression gate (G1–G4) and the batch report. Do not start the next series.

## 6 · SCOPE FENCES

- Loop v2 covers the SHELL and page chrome only. Content passes (STT artifacts, ERR-4 vocabulary sweep, claims) are separate loops.
- The NAS repair repo (`theophysics-site-repair`) and its whole-site runner operate on the NAS deploy trees; Loop v2 operates on THIS git repo. Do not cross the streams in one batch.
- `subdomains/`, `site-shell/`, `components/`, `assets/`, `prototypes/`, `_link-fix-backups/`, `MUST DO/` itself: out of scope for page repair (infrastructure, not articles).
- If two standards appear to conflict, the gold-standard FOLDER wins over any individual page, and David's ruling wins over both. File the conflict; don't resolve it silently.

*Loop v1 asked what the shell should be. Loop v2 makes every page answer to it.*
