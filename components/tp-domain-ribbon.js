(function () {
  "use strict";

  const CLAIM_TYPES = {
    what: {
      key: "what",
      label: "What",
      color: "#185FA5",
      legend: "observations + evidence"
    },
    how: {
      key: "how",
      label: "How",
      color: "#0F6E56",
      legend: "mechanism + structure"
    },
    why: {
      key: "why",
      label: "Why",
      color: "#854F0B",
      legend: "interpretation + meaning"
    }
  };

  function normalizeClaimType(value) {
    const key = String(value || "").trim().toLowerCase();
    return CLAIM_TYPES[key] ? key : null;
  }

  function getClaims(meta) {
    const candidates = [];
    if (Array.isArray(window.MDA_CLAIMS)) candidates.push(...window.MDA_CLAIMS);
    if (Array.isArray(meta?.claims)) candidates.push(...meta.claims);
    return candidates.filter((claim) => claim && normalizeClaimType(claim.primary));
  }

  function computeCounts(claims) {
    const counts = { what: 0, how: 0, why: 0 };
    claims.forEach((claim) => {
      const key = normalizeClaimType(claim.primary);
      if (key) counts[key] += 1;
    });
    return counts;
  }

  function articleParagraphs() {
    const selectors = [
      "article p",
      "main article p",
      ".article-body p",
      ".prose p",
      "main p"
    ];
    for (const selector of selectors) {
      const nodes = Array.from(document.querySelectorAll(selector))
        .filter((node) => node.textContent && node.textContent.trim().length > 40);
      if (nodes.length) return nodes;
    }
    return [];
  }

  function ensureParagraphTargets(claims) {
    const paragraphs = articleParagraphs();
    claims.forEach((claim) => {
      const index = Number(claim.paragraph_index);
      if (Number.isInteger(index) && index >= 0 && index < paragraphs.length) {
        claim._target = paragraphs[index];
      }
    });
    return paragraphs;
  }

  function clearActiveState(root) {
    document.querySelectorAll(".tp-claim-highlight").forEach((node) => {
      node.classList.remove("tp-claim-highlight");
      node.style.removeProperty("--tp-claim-color");
      node.removeAttribute("data-claim-jurisdiction");
    });

    document.querySelectorAll(".tp-claim-note").forEach((node) => node.remove());

    root.querySelectorAll(".tp-jurisdiction-segment").forEach((segment) => {
      segment.setAttribute("aria-pressed", "false");
      segment.classList.remove("is-active");
    });
  }

  function explanationHtml(claim, type) {
    const evidenceMap = {
      what: "This kind of claim lives or dies on evidence, observation, and traceable sourcing.",
      how: "This kind of claim needs mechanism clarity: structure, causal pathway, and explanatory fit.",
      why: "This kind of claim needs interpretive honesty: scope, assumptions, and what bridges are being made."
    };
    const warnings = [];
    if (claim.overreach && String(claim.overreach).toLowerCase() !== "none") {
      warnings.push(`Overreach flag: ${claim.overreach}.`);
    }
    if (claim.pos_mismatch) {
      warnings.push("Grammar mismatch flagged by the claim scanner.");
    }
    const note = warnings.length ? `<p>${warnings.join(" ")}</p>` : "";
    return `
      <div class="tp-claim-note-header">
        <strong style="color:${type.color}">${type.label}</strong>
        <span>${type.legend}</span>
      </div>
      <p>${claim.text || "Claim detail unavailable."}</p>
      <p>${evidenceMap[type.key]}</p>
      ${note}
    `;
  }

  function showClaimNote(target, claim, type) {
    const note = document.createElement("div");
    note.className = "tp-claim-note";
    note.innerHTML = explanationHtml(claim, type);
    target.insertAdjacentElement("afterend", note);
  }

  function activateType(root, claims, typeKey) {
    clearActiveState(root);
    const type = CLAIM_TYPES[typeKey];
    const matching = claims.filter((claim) => normalizeClaimType(claim.primary) === typeKey && claim._target);
    if (!matching.length) return;

    const segment = root.querySelector(`.tp-jurisdiction-segment[data-type="${typeKey}"]`);
    if (segment) {
      segment.setAttribute("aria-pressed", "true");
      segment.classList.add("is-active");
    }

    matching.forEach((claim) => {
      const target = claim._target;
      if (!target || target.dataset.tpClaimBound === "true") return;
      target.dataset.tpClaimBound = "true";
      target.addEventListener("click", () => {
        const existingNext = target.nextElementSibling;
        if (existingNext && existingNext.classList.contains("tp-claim-note")) {
          existingNext.remove();
          return;
        }
        document.querySelectorAll(".tp-claim-note").forEach((node) => node.remove());
        showClaimNote(target, claim, type);
      });
    });

    const seen = new Set();
    matching.forEach((claim) => {
      const target = claim._target;
      if (!target || seen.has(target)) return;
      seen.add(target);
      target.classList.add("tp-claim-highlight");
      target.style.setProperty("--tp-claim-color", type.color);
      target.setAttribute("data-claim-jurisdiction", type.label);
    });
  }

  function render(target, meta) {
    const root = typeof target === "string" ? document.querySelector(target) : target;
    if (!root) return null;

    const claims = getClaims(meta);
    if (!claims.length) return null;

    ensureParagraphTargets(claims);
    const counts = computeCounts(claims);
    const total = Object.values(counts).reduce((sum, count) => sum + count, 0) || 1;

    const wrap = document.createElement("section");
    wrap.className = "tp-jurisdiction-bar";
    wrap.setAttribute("aria-label", "Claim jurisdiction");

    const title = document.createElement("div");
    title.className = "tp-jurisdiction-title";
    title.textContent = "Claim jurisdiction";

    const strip = document.createElement("div");
    strip.className = "tp-jurisdiction-strip";

    Object.values(CLAIM_TYPES).forEach((type) => {
      const count = counts[type.key];
      const pct = Math.round(count / total * 100);
      const button = document.createElement("button");
      button.type = "button";
      button.className = "tp-jurisdiction-segment";
      button.dataset.type = type.key;
      button.setAttribute("aria-pressed", "false");
      button.style.setProperty("--tp-claim-color", type.color);
      button.style.flex = `${Math.max(count, 1)} 1 0`;
      button.innerHTML = `<strong>${type.label}</strong><span>${pct}%</span>`;
      button.addEventListener("click", () => activateType(wrap, claims, type.key));
      strip.appendChild(button);
    });

    const legend = document.createElement("div");
    legend.className = "tp-jurisdiction-legend";
    legend.innerHTML = Object.values(CLAIM_TYPES)
      .map((type) => `<span><i style="background:${type.color}"></i>${type.legend}</span>`)
      .join("");

    wrap.append(title, strip, legend);
    root.appendChild(wrap);
    return wrap;
  }

  window.TPDomainRibbon = { render };
})();
