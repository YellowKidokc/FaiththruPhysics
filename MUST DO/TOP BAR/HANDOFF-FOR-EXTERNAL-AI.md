# Handoff — Revolution of Truth Page Shell + Math Translation Layer

**For:** an AI or collaborator with NO access to David's local file system — this document is meant to be self-contained.
**Site:** faiththruphysics.com | **Project:** POF 2828, Theophysics Research Initiative
**Written:** 2026-07-01

---

## 0. Read this first — the one mistake to not repeat

This project has **two folders that look canonical and aren't both current**:

- `MUST DO\TOP BAR\` (where this file lives) — **legacy**. Early prototype scripts and an old all-in-one `verification-bar.html`. Its own README says so.
- `MUST DO\PAGE-SHELL-GOLD-STANDARD\` — **canonical as of 2026-06-29**. This is the real spec and the real execution scripts. Ten numbered sections, `00_INDEX.md` is the map.

If you don't have access to the local drive at all (pure online AI), the canonical spec folder won't be visible to you — which is exactly why this document exists: it's a flattened, self-contained copy of what matters from that spec plus the working MTL system, so you don't need drive access to understand the architecture.

**The failure mode that already happened once in this project:** CSS for a component gets written into a page's `<style>` block, a `<!-- COMPONENT NAME -->` comment gets left as a placeholder, and the actual `<div>` markup never gets inserted. The page *looks* like it has the feature (styles are there, script tags are linked) but nothing renders because there's no element for the CSS/JS to attach to. **Always check for markup, not just for links.** A linked stylesheet is not evidence a feature works.

---

## 1. The page shell — ten sections, current status

Reference page: `revolution-of-truth/drv-00-the-argument.html`. Template: `revolution-of-truth/_TEMPLATE.html`.

| # | Section | What it is | Status (as of this handoff) |
|---|---|---|---|
| 1 | Top bar | Fixed header — brand, Home/MTL/Proof links, series lip toggle, HS/College/PhD tabs, search | Tabs render (`level-panel` markup present). **Search UI markup was not found in the live pages** — likely designed but not built. Treat as open. |
| 2 | Header lip | Dropdown under header — domain meter, classification tags, prev/next, series grid | Spec'd via `components/tp-header-lip.js`, domain data injected as `ARTICLE_PROFILE` by the builder script. Needs verification per-page. |
| 3 | Verified bar | Collapsible strip — axioms, laws, χ score, isomorphism bridges, domain chips, expand panel | **Fixed 2026-07-01.** Markup was missing (classic CSS-without-div bug above). Now inserted in `_TEMPLATE.html` and all 6 live `drv-*.html` pages. Auto-fetches its own JSON from the URL — no manual per-page wiring needed. Domain chips added as a new feature (weren't in the original spec). |
| 4 | Reading levels | High School / College / PhD content swap | **Content files confirmed present** for all 6 articles in 5 different location conventions (`site-data/revolution-of-truth/highschool/`, `/phd/`, `site-data/easy/revolution-of-truth/`, `site-data/academic/revolution-of-truth/`, `site-data/APIs/input/revolution-of-truth/`) — all fully populated `.canonical.md` files, nothing missing. If a page isn't showing the right level, the swap logic (`components/reading-levels.js`) is the thing to check, not the content. |
| 5 | Article body | College drop caps, equation cards, feature boxes, sections | Present, standard article CSS. |
| 6 | Bottom nav | Big prev/next, series home, chapter cards | Present per template. |
| 7 | Audit foot | Got right / overstated / got wrong covenant box | Present per template. |
| 8 | Math references | MathJax + `.tp-refs` bibliography | Present. Feeds into MTL (see below). |
| 9 | Evaluation pipeline | Excel workbook → JSON → verified bar | **Working but only 1 of 6 articles has data.** `Article_Evaluation_Workbook.xlsx` has rows filled in only for `drv-00-the-argument`. Run `python excel_to_site_json.py --apply` after filling in the other 5 articles' rows across all sheets (Identity, Verification Metrics, Domains, Claims, Axioms, Ten Laws, Audit Boxes, Kill Conditions, Physics Process, Narrative Flow, Citations). |
| 10 | Data layout | site-data paths, markdown tiers, frontmatter | Confirmed working per section 4 above. |

**One-command rebuild** (from the canonical scripts folder):
```
cd "D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\scripts"
python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-00-the-argument
python excel_to_site_json.py --apply
```
Dry-run is the default; `--apply` is required to write. A `--report` flag produces a structured JSON audit instead of writing.

---

## 2. Math Translation Layer (MTL) — full explanation

This is pulled directly from `MUST DO\math-translation-layer\MTL-HANDOFF-2026-06-30.md`, the most current source doc, condensed.

### There are two MTL systems — don't confuse them

**1. Current runtime path (canonical for new work):**
- Cloudflare Worker: `faith-mtl-worker`, live at `https://faith-mtl-worker.davidokc28.workers.dev`
- D1 database: `faiththruphysics-mtl` (binding name `DB`)
- Worker source: `D:\GitHub\faiththruphysics-site\workers\mtl-service`
- Site client (already loaded on many pages): `D:\GitHub\faiththruphysics-site\shared\js\mtl-worker-client.js`

What it does: collects MathJax-rendered equations off the page, batches them to the worker, gets back one translation string per equation, inserts a callout div right after each rendered equation. Behavior varies by reading mode — academic/proof mode shows the equation only; easy mode shows equation + plain-English translation; standard mode shows equation + term-by-term translation.

**2. Legacy overlay path (reference only, don't build on this unless there's a specific reason):**
- `shared/js/mtl-overlay.js`, `shared/js/mtl-overlay-loader.js`, `shared/data/mtl-overlay-translations.json`

### The actual worker-client code (in full, 181 lines)

```javascript
/**
 * MTL Worker Client
 * Auto-translates MathJax-rendered equations using faith-mtl-worker.
 *
 * Behavior:
 *   - Academic/Proof mode: equation only (no translation inserted).
 *   - Easy mode: equation + plain-English translation underneath.
 *   - Standard mode: equation + term-by-term/standard translation.
 *
 * Requires MathJax 3 and the MTL reader bar markup.
 */
(function () {
  const API_BASE = "https://faith-mtl-worker.davidokc28.workers.dev";
  const BATCH_LIMIT = 40;
  const WORKER_CALLOUT_SELECTOR = '.mtl-worker-callout[data-mtl-worker="true"]';

  function normalizeMode(mode) {
    if (!mode) return "easy";
    if (mode === "math") return "standard";
    if (mode === "readable") return "standard";
    if (mode === "scholarly") return "academic";
    if (mode === "simple") return "easy";
    return mode;
  }

  function getReaderMode() {
    const htmlMode = normalizeMode(document.documentElement?.dataset?.readerMode || "");
    if (htmlMode && ["easy", "standard", "academic", "proof"].includes(htmlMode)) return htmlMode;

    // 1. Check body class
    const body = document.body;
    for (const cls of body.classList) {
      const m = cls.match(/^(?:mtl|level)-(easy|standard|academic|proof)$/);
      if (m) return m[1];
    }

    // 2. Check active reader tab
    const active = document.querySelector('.mtl-reader-tab.active, .tp-level.active, [data-reader-mode].active');
    if (active) return normalizeMode(active.dataset.readerMode || active.dataset.level || "");

    // 3. Check persisted shell mode
    try {
      const stored = normalizeMode(localStorage.getItem("ftp-reader-mode") || "");
      if (stored && ["easy", "standard", "academic", "proof"].includes(stored)) return stored;
    } catch (_) {}

    // 4. Default
    return "easy";
  }

  function extractLatex(el) {
    if (el.dataset.latex) return el.dataset.latex;
    if (el.MathJax && el.MathJax.math) return el.MathJax.math;
    return "";
  }

  function annotateMathJaxSources() {
    if (typeof MathJax === "undefined" || !MathJax.startup || !MathJax.startup.document) return;
    const doc = MathJax.startup.document;
    if (!doc.math) return;
    doc.math.forEach((mathItem) => {
      const root = mathItem.typesetRoot;
      if (root && !root.dataset.latex) {
        root.dataset.latex = mathItem.math;
        root.dataset.display = mathItem.display ? "block" : "inline";
      }
    });
  }

  function collectEquations() {
    const containers = Array.from(document.querySelectorAll('mjx-container, .eq-block, [data-latex]'));
    const map = new Map(); // latex -> [elements]
    containers.forEach((el) => {
      const latex = extractLatex(el);
      if (!latex) return;
      if (!map.has(latex)) map.set(latex, []);
      map.get(latex).push(el);
    });
    return map;
  }

  async function fetchBatch(latexList, mode) {
    const resp = await fetch(`${API_BASE}/api/batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ latexList, mode }),
    });
    if (!resp.ok) throw new Error(`MTL worker returned ${resp.status}`);
    return resp.json();
  }

  function createCallout(translation, mode) {
    const div = document.createElement("div");
    div.className = `mtl-worker-callout mtl-mode-${mode}`;
    div.dataset.mtlWorker = "true";
    div.textContent = translation;
    return div;
  }

  function clearWorkerCallouts() {
    document.querySelectorAll(WORKER_CALLOUT_SELECTOR).forEach((node) => node.remove());
    document.querySelectorAll("mjx-container, .eq-block, [data-latex]").forEach((el) => {
      delete el.dataset.mtlAnnotated;
    });
  }

  function applyTranslations(map, results, mode) {
    if (mode === "academic" || mode === "proof") return; // equation only

    Object.entries(results).forEach(([latex, data]) => {
      const translation = data && data.translation;
      if (!translation) return;
      const elements = map.get(latex);
      if (!elements) return;

      elements.forEach((el) => {
        if (el.dataset.mtlAnnotated) return;
        el.dataset.mtlAnnotated = "true";
        const target = el.closest("mjx-container") || el;
        target.after(createCallout(translation, mode));
      });
    });
  }

  async function run() {
    annotateMathJaxSources();
    const mode = getReaderMode();
    clearWorkerCallouts();
    const map = collectEquations();
    if (map.size === 0) return;

    const latexList = Array.from(map.keys());
    const batches = [];
    for (let i = 0; i < latexList.length; i += BATCH_LIMIT) {
      batches.push(latexList.slice(i, i + BATCH_LIMIT));
    }

    for (const batch of batches) {
      try {
        const data = await fetchBatch(batch, mode);
        if (data && data.results) applyTranslations(map, data.results, mode);
      } catch (err) {
        console.warn("MTL worker batch failed:", err);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
        window.MathJax.startup.promise.then(run).catch(run);
      } else {
        setTimeout(run, 500);
      }
    });
  } else {
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      window.MathJax.startup.promise.then(run).catch(run);
    } else {
      setTimeout(run, 500);
    }
  }

  document.addEventListener("click", (e) => {
    const tab = e.target.closest("[data-reader-mode], [data-level]");
    if (!tab) return;
    setTimeout(run, 50);
  });

  document.addEventListener("ftp-layer-change", () => {
    setTimeout(run, 50);
  });
})();
```

### MTL current hard limitation

The worker returns **one translation string per equation**. That's enough for a first readable layer but not the fuller target model. The next real upgrade (per the source handoff) is moving from a single string to a structured payload per equation:

```
id, latex, canonical_reading, plain_english, symbol_map, why_it_matters, claim_hook, test_hook, mode_variants
```

### MTL coverage for revolution-of-truth specifically

From the same source doc — this series is **Tier 2** (next lane after `consciousness`, which is the flagship):
- 173 extracted equations total across the series
- `drv-00-the-argument.html`: 1 found / 57 missing translations
- `drv-02-the-lock.html`: 0 found / 48 missing translations

So even on the pages where the verified-bar and reading levels are working, **MTL coverage on revolution-of-truth is weak** — this is a known, pre-existing gap, not something the verified-bar fix touched or was supposed to touch.

### MTL scripts (operational backbone — use these, don't reinvent)

Folder: `D:\GitHub\faiththruphysics-site\MUST DO\math-translation-layer\scripts\`
- `extract_series_math.py` — pulls equations out of a series' HTML
- `run_series_math_scan.ps1` — wrapper to run the scan
- `summarize_active_math_surface.py` — produces the coverage summary
- `normalize_mtl_workbook.py` — cleans up extracted rows before import
- `export_safe_rows_to_d1.py` — pushes vetted rows into the D1 database
- `audit_mtl_site_coverage.py` — the coverage audit (found/missing per page)

**Operational rule from the source doc: only push "safe rows" to D1 on a first pass. Keep `needs_review` rows separate. Don't sweep ambiguous translations into production just to make a coverage number look better.**

---

## 3. The audit-first prompt (use this before fixing anything)

This is the prompt that should have been used from the start of this work, distilled from the mistake described in Section 0:

> Before touching any code, read `00_INDEX.md` and every README under `01-top-bar` through `10-data-layout` in the canonical PAGE-SHELL-GOLD-STANDARD spec (or this handoff document, if that's not accessible). Confirm which folder is currently authoritative before running anything — it moves.
>
> For [series name], audit `_TEMPLATE.html` and one live page against every section in the index. For each section: does the CSS/JS link exist, does a comment marker exist, and does actual markup exist between them? Don't assume a linked stylesheet means the feature works — check for orphaned markers (a comment placeholder with no HTML under it).
>
> Report every section as one of: present and wired, marker exists but markup missing, or absent entirely. Show the full gap list before fixing anything.
>
> Once confirmed, fix one page completely, verify it renders right, then apply the same fix to the rest — and ask explicitly before running anything that touches more than one file.

---

## 4. Open items (known, not yet fixed)

1. **Search UI** — no markup found in live revolution-of-truth pages despite being in the top-bar spec. Needs the same audit-then-fix treatment as the verified bar got.
2. **Evaluation workbook** — only `drv-00` has data; 5 articles need their rows filled in (`Article_Evaluation_Workbook.xlsx`, sheets `01_Article_Identity` through `11_Recommended_Citations`).
3. **MTL coverage on revolution-of-truth** — weak (see numbers above). Series is queued as Tier 2 behind `consciousness`.
4. **Header lip domain data** — spec'd, not yet independently verified live on revolution-of-truth pages (worth checking with the same rigor applied to the verified bar).
