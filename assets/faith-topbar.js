(function () {
  "use strict";

  if (window.__ftpFaithTopbarLoaded) {
    return;
  }
  window.__ftpFaithTopbarLoaded = true;

  const DEFAULT_CONFIG = {
    replaceLegacyNav: true,
    brandHref: "/index.html",
    seriesHref: "/series.html",
    homeHref: "/index.html",
    mtlHref: "/equation/",
    proofHref: "/proof-explorer/",
    activeLevel: "college",
    title: document.title || "Faith Thru Physics",
    seriesLabel: "Series",
    domains: [
      ["logic", "Logic/Mathematics"],
      ["physics", "Physics"],
      ["info", "Information Theory"],
      ["theology", "Theology"],
      ["psychology", "Developmental Psychology"],
      ["philosophy", "Philosophy"]
    ],
    metrics: {
      axiomsTested: "-/188",
      coverage: "-%",
      chiRaw: "-",
      chiNormalized: "-/10",
      fruits: "-/9",
      bridges: "-",
      physics: "-",
      trinity: "-",
      meqVars: "-/10",
      claimsTotal: "-",
      loadBearing: "-",
      killConditions: "-",
      contradictions: "-"
    },
    laws: [],
    proofExplorerHref: "/proof-explorer/"
  };

  function mergeConfig(base, override) {
    const out = { ...base, ...(override || {}) };
    out.metrics = { ...base.metrics, ...((override && override.metrics) || {}) };
    out.domains = (override && override.domains) || base.domains;
    out.laws = (override && override.laws) || base.laws;
    return out;
  }

  function getConfig() {
    return mergeConfig(DEFAULT_CONFIG, window.FTP_TOPBAR || {});
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function removeLegacyNavs() {
    const navs = Array.from(document.body.children).filter((el) => {
      if (el.tagName !== "NAV") return false;
      if (el.dataset.ftpTopbar === "true") return false;
      const style = (el.getAttribute("style") || "").toLowerCase();
      return style.includes("position:sticky") || style.includes("top:0");
    });

    navs.forEach((nav) => {
      nav.dataset.ftpLegacyRemoved = "true";
      nav.style.display = "none";
    });
  }

  function renderPills(config) {
    return config.domains
      .map(([key, label]) => `<span class="ftp-pill ${escapeHtml(key)}">${escapeHtml(label)}</span>`)
      .join("");
  }

  function renderLaws(activeLaws) {
    const active = new Set((activeLaws || []).map(String));
    let html = "";
    for (let i = 1; i <= 10; i += 1) {
      const label = `L${i}`;
      const activeClass = active.has(label) || active.has(String(i)) ? "active" : "";
      html += `<span class="ftp-law ${activeClass}">${label}</span>`;
    }
    return html;
  }

  function renderMetricLine(label, value) {
    return `
      <div class="ftp-proof-line">
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
      </div>
    `;
  }

  const NAV_ITEMS = [
    { key: "home", label: "Home", href: "/index.html" },
    { key: "series", label: "Series", href: "/series.html" },
    { key: "proof", label: "Proof", href: "/proof-explorer/" },
    { key: "equation", label: "Equation", href: "/equation/" },
    { key: "media", label: "Media", href: "/media/" },
    { key: "glossary", label: "Glossary", href: "/glossary/" },
    { key: "all-pages", label: "All Pages", href: "/site-index.html" }
  ];

  function renderNavLinks(mobile) {
    const cls = mobile ? "ftp-nav ftp-nav--mobile" : "ftp-nav";
    const items = NAV_ITEMS.map(
      (item) => `<a href="${escapeHtml(item.href)}" class="ftp-nav-link" data-nav-item="${escapeHtml(item.key)}">${escapeHtml(item.label)}</a>`
    ).join("");
    return `<nav class="${cls}" data-section="primary-navigation" aria-label="Primary">${items}</nav>`;
  }

  function renderTopbar(config) {
    const level = String(config.activeLevel || "college").toLowerCase();
    const topbar = document.createElement("header");
    topbar.className = "ftp-topbar";
    topbar.dataset.ftpTopbar = "true";
    topbar.dataset.component = "ftp-topbar";
    topbar.dataset.version = "1.1";
    topbar.dataset.purpose = "global-site-navigation";

    topbar.innerHTML = `
      <div class="ftp-main-row" data-section="topbar-main-row">
        <div class="ftp-brand" data-section="brand-block">
          <a href="${escapeHtml(config.brandHref)}" class="ftp-brand-mark" data-element="brand-link" aria-label="Faith Thru Physics Home">χ</a>
          <span class="ftp-brand-name" data-element="brand-name">Faith Thru Physics</span>
          <span class="ftp-divider ftp-divider--nav" data-element="divider" aria-hidden="true"></span>
          ${renderNavLinks(false)}
        </div>

        <nav class="ftp-levels" data-section="reading-level-selector" aria-label="Reading level">
          <a class="ftp-level ${level === "high-school" || level === "highschool" ? "active" : ""}" data-reading-level="high-school" href="?level=high-school">High School</a>
          <a class="ftp-level ${level === "college" ? "active" : ""}" data-reading-level="college" href="?level=college">College</a>
          <a class="ftp-level ${level === "phd" ? "active" : ""}" data-reading-level="phd" href="?level=phd">PhD</a>
        </nav>

        <div class="ftp-actions" data-section="right-actions">
          <button type="button" class="ftp-menu-toggle" data-action="toggle-mobile-menu" aria-label="Open menu" aria-expanded="false">
            <span class="ftp-menu-bar"></span>
            <span class="ftp-menu-bar"></span>
            <span class="ftp-menu-bar"></span>
          </button>
          <button type="button" class="ftp-proof-toggle" data-action="toggle-proof-panel" data-ftp-proof-toggle>Verified</button>
          <div class="ftp-search" data-action="open-search" aria-label="Search shortcut"><span>⌕</span> <span>Ctrl+K</span></div>
        </div>
      </div>

      <div class="ftp-mobile-menu" data-section="mobile-menu" aria-hidden="true">
        ${renderNavLinks(true)}
      </div>

      <div class="ftp-domain-row" data-section="domain-verification-row">
        <div class="ftp-verified" data-element="verified-label">Verified</div>
        <div class="ftp-pills" data-section="domain-pills">${renderPills(config)}</div>
      </div>

      <div class="ftp-progress" data-section="verification-stripe" aria-hidden="true">
        <span data-stripe-domain="logic-mathematics"></span><span data-stripe-domain="physics"></span><span data-stripe-domain="information-theory"></span><span data-stripe-domain="theology"></span><span data-stripe-domain="philosophy"></span>
      </div>
    `;

    return topbar;
  }

  function renderProofPanel(config) {
    const m = config.metrics;
    const panel = document.createElement("aside");
    panel.className = "ftp-proof-panel";
    panel.id = "ftpProofPanel";
    panel.dataset.component = "ftp-proof-panel";
    panel.setAttribute("aria-hidden", "true");

    panel.innerHTML = `
      <div class="ftp-proof-inner" data-section="proof-panel-inner">
        <div class="ftp-proof-grid">
          <section class="ftp-proof-card" data-proof-card="axiom-coverage">
            <h3>Axiom Coverage</h3>
            ${renderMetricLine("Axioms Tested", m.axiomsTested)}
            ${renderMetricLine("Coverage", m.coverage)}
          </section>

          <section class="ftp-proof-card" data-proof-card="ten-laws-mapping">
            <h3>Ten Laws Mapping</h3>
            <div class="ftp-laws">${renderLaws(config.laws)}</div>
          </section>

          <section class="ftp-proof-card" data-proof-card="chi-coherence-score">
            <h3>Chi Coherence Score</h3>
            ${renderMetricLine("Raw", m.chiRaw)}
            ${renderMetricLine("Normalized", m.chiNormalized)}
            ${renderMetricLine("Fruits", m.fruits)}
          </section>

          <section class="ftp-proof-card" data-proof-card="isomorphisms">
            <h3>Isomorphisms</h3>
            ${renderMetricLine("Bridges", m.bridges)}
            ${renderMetricLine("Physics", m.physics)}
            ${renderMetricLine("Trinity", m.trinity)}
            ${renderMetricLine("MEQ vars", m.meqVars)}
          </section>

          <section class="ftp-proof-card" data-proof-card="claims">
            <h3>Claims</h3>
            ${renderMetricLine("Total", m.claimsTotal)}
            ${renderMetricLine("Load-bearing", m.loadBearing)}
            ${renderMetricLine("Kill conditions", m.killConditions)}
            ${renderMetricLine("Contradictions", m.contradictions)}
            <a class="ftp-proof-link" data-action="open-full-proof-explorer" href="${escapeHtml(config.proofExplorerHref)}">${icon("flask")} Full Proof Explorer -></a>
          </section>

          <section class="ftp-proof-card" data-proof-card="domains">
            <h3>Domains</h3>
            <div class="ftp-pills" style="white-space:normal;overflow:visible;">${renderPills(config)}</div>
          </section>
        </div>
      </div>
    `;

    return panel;
  }

  function togglePanel(panel, force) {
    const shouldOpen = typeof force === "boolean" ? force : !panel.classList.contains("open");
    panel.classList.toggle("open", shouldOpen);
    panel.setAttribute("aria-hidden", shouldOpen ? "false" : "true");
  }

  function wireEvents(topbar, panel) {
    const toggle = topbar.querySelector("[data-ftp-proof-toggle]");
    if (toggle) {
      toggle.addEventListener("click", () => togglePanel(panel));
    }

    const menuToggle = topbar.querySelector("[data-action='toggle-mobile-menu']");
    const mobileMenu = topbar.querySelector("[data-section='mobile-menu']");
    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener("click", () => {
        const isOpen = topbar.classList.toggle("ftp-menu-open");
        mobileMenu.setAttribute("aria-hidden", String(!isOpen));
        menuToggle.setAttribute("aria-expanded", String(isOpen));
      });
    }

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        togglePanel(panel, false);
        if (topbar.classList.contains("ftp-menu-open") && mobileMenu) {
          topbar.classList.remove("ftp-menu-open");
          mobileMenu.setAttribute("aria-hidden", "true");
          if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
        }
      }

      const searchHotkey = event.key.toLowerCase() === "k" && (event.metaKey || event.ctrlKey);
      if (searchHotkey) {
        event.preventDefault();
        const searchEvent = new CustomEvent("ftp:search", { bubbles: true });
        document.dispatchEvent(searchEvent);
      }
    });

    document.addEventListener("click", (event) => {
      if (panel.classList.contains("open")) {
        const clickedInsidePanel = panel.contains(event.target);
        const clickedToggle = topbar.contains(event.target);
        if (!clickedInsidePanel && !clickedToggle) {
          togglePanel(panel, false);
        }
      }
      if (topbar.classList.contains("ftp-menu-open") && mobileMenu) {
        const clickedInsideMenu = mobileMenu.contains(event.target);
        const clickedToggle = menuToggle && menuToggle.contains(event.target);
        if (!clickedInsideMenu && !clickedToggle) {
          topbar.classList.remove("ftp-menu-open");
          mobileMenu.setAttribute("aria-hidden", "true");
          if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
        }
      }
    });
  }

  function init() {
    if (document.querySelector(".ftp-topbar")) {
      return;
    }

    const config = getConfig();
    document.body.classList.add("ftp-topbar-enabled");

    if (config.replaceLegacyNav) {
      removeLegacyNavs();
    }

    const topbar = renderTopbar(config);
    const panel = renderProofPanel(config);

    document.body.prepend(panel);
    document.body.prepend(topbar);
    wireEvents(topbar, panel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
