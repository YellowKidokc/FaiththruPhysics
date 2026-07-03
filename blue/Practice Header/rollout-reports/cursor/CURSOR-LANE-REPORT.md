# Cursor Lane Report — Topbar Prep + Inject Complete

**Manifest:** `ai-article-rollout-split.json`  
**Lanes completed:** Prep (Step 3a) + Inject (Step 3b, advanced on user go-ahead)  
**Verifier:** Gemini (prep/inject), Kimmy (labeling next)  
**Date:** 2026-07-02

## Status: **90 / 90 ready for Kimmy labeling**

| Check | Count |
|--------|-------|
| `FTP_TOPBAR_PREP` + config | 90/90 |
| `FTP_TOPBAR_ASSETS` (marked inject) | 90/90 |
| `faith-topbar.css/js` present | 90/90 |
| Article body rewritten | 0 |

**Backups:** `backups/topbar_prep/`, `backups/topbar_inject/`

**Inject run:** 83 newly injected, 7 already had assets (normalized to marked block where needed).

**After-inject audit (first 10):** `rollout-reports/cursor/after-inject-sample.json` — 10 keep, 0 exclude.

## Next step → **Kimmy**
Label `data-tp-*` / `data-slot` on touched structure for Cursor's 90 pages. Claude verifies Kimmy.

## Next step → **Gemini (parallel)**
Gemini's own 90 (`moral-decline`, `blue`, etc.) — prep + inject on **Gemini manifest paths only**.

---

## Step 1 — Candidate list (full assignment)

| Field | Value |
|--------|--------|
| **Total candidate pages** | 90 |
| **AI** | Cursor |
| **Folders included** | `duality-project` (32), `proof-architecture` (14), `cross-domain` (12), `Logos_Papers` (12), `socratic-axioms` (9), `convergence-deep` (6), `isomorphism` (5) |

**First 10 paths:**
1. `duality-project/alpha-prime-canonical.html`
2. `duality-project/dc-waveparticleduality.html`
3. `duality-project/dp-00-the-null-hypothesis.html`
4. `duality-project/dp-000-the-assignment.html`
5. `duality-project/dp-01-candle-in-the-void.html`
6. `duality-project/dp-02-the-blinding-mirror.html`
7. `duality-project/dp-03-the-gray-stagnation.html`
8. `duality-project/dp-04-the-birth-of-a-devil.html`
9. `duality-project/dp-05-the-generational-rust.html`
10. `duality-project/dp-06-the-chorus-appears.html`

**Excluded (by manifest, not in Cursor list):** all `index.html`, media/audio/podcast, proof-explorer, subdomains, archives, Double Check, Practice Header demos, site-index/series, etc.

**Sample pass (7 pages, one per folder):** applied prep only — awaiting approval before remaining 83 pages.

**UPDATE 2026-07-02:** All **90/90** Cursor manifest pages now have `FTP_TOPBAR_PREP` + `FTP_TOPBAR_CONFIG`. No `faith-topbar` injection (Gemini lane). Backups under `backups/topbar_prep/`.

---

## Step 2 — Before audit

```text
python D:\GitHub\Python-WEB\web_quality_audit.py ^
  --json "...\rollout-reports\cursor\before-sample.json" ^
  --path <7 sample files>
```

**Output:** `rollout-reports/cursor/before-sample.json`  
**Summary:** 7 sources, 7 keep, 0 exclude, 0 optimize  
**Notes:** pre-existing issues only (missing meta description, multi-H1 on one page) — not introduced by prep.

---

## Step 3 — Lane changes applied (sample only)

**Script:** `scripts/prepare_topbar_pages.py --apply`  
**Did NOT run:** `inject_topbar.py` (Gemini lane)

**Per file:** inserted marked blocks before `</head>`:
- `<!-- FTP_TOPBAR_PREP:START/END -->` — scoped prep CSS (`--ftp-header-h`, `body.ftp-topbar-enabled` padding, ribbon offset, scroll-margin, mobile table guard)
- `<!-- FTP_TOPBAR_CONFIG:START/END -->` — `window.FTP_TOPBAR` with `replaceLegacyNav: false`

**Backups:** `backups/topbar_prep/20260702_181824/`

---

## Step 4 — Labeling

Prep lane does not add `data-slot` / `data-tp-*` (Kimmy lane). No article body content changed.

---

## Step 5 — After audit

**Output:** `rollout-reports/cursor/after-sample.json`  
**Summary:** 7 sources, 7 keep — **unchanged vs before** (quality scores stable).

---

## Step 6 — Files touched / skipped

### Touched (7)
- `convergence-deep/cdt-01-math-is-moral.html`
- `cross-domain/cd-01-an-introduction-to-theophysics.html`
- `duality-project/alpha-prime-canonical.html`
- `isomorphism/emergent_theological_structures_master_equation.html`
- `Logos_Papers/lgs-01-the-universe-is-a-language.html`
- `proof-architecture/pa-00-bundle-viewer.html`
- `socratic-axioms/sa-01-information-persistence.html`

### Skipped (0)
- None — full Cursor manifest complete.

### Concerns
- None from prep: no topbar injected, no duplicate header, CSS scoped inside marked prep block only
- Pre-existing: missing meta descriptions on several articles (not fixed in this lane)

---

## Step 7 — Recommendation

**PASS — Cursor prep lane complete (90/90)** → Gemini may inject topbar on **Cursor's 90** when ready. Gemini's own 90 (`moral-decline`, `blue`, etc.) need **their own prep** (Gemini runs `prepare_topbar_pages.py` on Gemini manifest paths, or explicit cross-lane handoff).

---

## Next commands (after approval)

```powershell
# Remaining 83 pages — dry-run first
python scripts\prepare_topbar_pages.py --root D:\GitHub\faiththruphysics-site-v2 --apply <paths-from-manifest>

# Or batch by folder with manifest path list export
```
