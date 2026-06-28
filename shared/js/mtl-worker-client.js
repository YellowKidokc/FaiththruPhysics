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

  function getReaderMode() {
    // 1. Check body class (e.g. body.mtl-easy)
    const body = document.body;
    for (const cls of body.classList) {
      const m = cls.match(/^mtl-(easy|standard|academic|proof)$/);
      if (m) return m[1];
    }
    // 2. Check active reader tab
    const active = document.querySelector('.mtl-reader-tab.active, .tp-level.active, [data-reader-mode].active');
    if (active) return active.dataset.readerMode || active.dataset.level;
    // 3. Default
    return "easy";
  }

  function extractLatex(el) {
    // If we already annotated the container, use it.
    if (el.dataset.latex) return el.dataset.latex;
    // MathJax 3 exposes the math item via the element property.
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
    div.textContent = translation;
    return div;
  }

  function applyTranslations(map, results, mode) {
    if (mode === "academic" || mode === "proof") return; // equation only

    Object.entries(results).forEach(([latex, data]) => {
      const translation = data && data.translation;
      if (!translation) return;
      const elements = map.get(latex);
      if (!elements) return;

      elements.forEach((el) => {
        // Skip if already annotated
        if (el.dataset.mtlAnnotated) return;
        el.dataset.mtlAnnotated = "true";

        // For inline math, insert after the outer container.
        const target = el.closest("mjx-container") || el;
        target.after(createCallout(translation, mode));
      });
    });
  }

  async function run() {
    annotateMathJaxSources();
    const mode = getReaderMode();
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

  // Run after MathJax finishes rendering.
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

  // Re-run when reader mode changes.
  document.addEventListener("click", (e) => {
    const tab = e.target.closest("[data-reader-mode], [data-level]");
    if (!tab) return;
    // Small delay so the active class updates first.
    setTimeout(run, 50);
  });
})();
