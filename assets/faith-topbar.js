(function () {
  "use strict";

  /**
   * Faith Through Physics shared topbar (final labeled shell).
   *
   * Include on pages:
   *   <link rel="stylesheet" href="/assets/faith-topbar.css">
   *   <script defer src="/assets/faith-topbar.js"></script>
   *
   * Optional page override:
   *   window.FTP_TOPBAR = { equationHref: "/master-equation/", compact: true };
   */

  if (window.__ftpFaithTopbarLoaded) {
    return;
  }
  window.__ftpFaithTopbarLoaded = true;

  const DEFAULT_CONFIG = {
    replaceLegacyNav: true,
    brandHref: "/index.html",
    equationHref: "auto",
    activeLevel: "college",
    metrics: {
      domains: 6,
      laws: 10,
      coherence: 8,
      claims: 9
    }
  };

  const LEGACY_SELECTORS = [
    "header.ftp-top",
    ".ftp-panel-toggle",
    ".ftp-panel",
    ".topbar",
    ".top-bar",
    ".top-nav",
    "header.pe-header",
    "nav.tp-ribbon"
  ];

  const NAV_ITEMS = [
    { key: "home", label: "Home", href: "/index.html", slot: "nav-home" },
    { key: "mtl", label: "MTL", href: "/master-equation/", slot: "nav-mtl" },
    { key: "proof", label: "Proof", href: "/proof-explorer/", slot: "nav-proof" }
  ];

  const SERIES_ITEMS = [
    { label: "Blue Series", href: "/blue/", hint: "physics + truth", slot: "series-blue" },
    { label: "Moral Decline", href: "/moral-decline/", hint: "MDA", slot: "series-moral-decline" },
    { label: "Genesis to Quantum", href: "/genesis-to-quantum/", hint: "GTQ", slot: "series-genesis-to-quantum" },
    { label: "Cross Domain", href: "/cross-domain/", hint: "coherence", slot: "series-cross-domain" },
    { label: "Formal Papers", href: "/formal-papers/", hint: "proof layer", slot: "series-formal-papers" },
    { label: "All Pages", href: "/site-index.html", hint: "index", slot: "series-all-pages" }
  ];

  const DOMAIN_ITEMS = [
    { key: "logic", label: "Logic/Mathematics", short: "Logic/Math", slot: "domain-logic-mathematics" },
    { key: "physics", label: "Physics", short: "Physics", slot: "domain-physics" },
    { key: "info", label: "Information Theory", short: "Info Theory", slot: "domain-information-theory" },
    { key: "theology", label: "Theology", short: "Theology", slot: "domain-theology" },
    { key: "psych", label: "Developmental Psychology", short: "Dev Psych", slot: "domain-developmental-psychology" },
    { key: "phil", label: "Philosophy", short: "Philosophy", slot: "domain-philosophy" }
  ];

  function getConfig() {
    return { ...DEFAULT_CONFIG, ...(window.FTP_TOPBAR || {}) };
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function normalizePath(pathname) {
    let path = pathname || "/";
    if (path.endsWith("/index.html")) {
      path = path.slice(0, -"/index.html".length) || "/";
    }
    if (path.length > 1 && path.endsWith("/")) {
      path = path.slice(0, -1);
    }
    return path;
  }

  function getEquationHref(config) {
    return config.equationHref && config.equationHref !== "auto" ? config.equationHref : "/master-equation/";
  }

  function removeLegacyNavs() {
    LEGACY_SELECTORS.forEach((selector) => {
      document.querySelectorAll(selector).forEach((el) => {
        if (el.closest('[data-ftp-topbar="true"]')) {
          return;
        }
        el.dataset.ftpLegacyRemoved = "true";
        el.style.display = "none";
      });
    });

    Array.from(document.body.children).forEach((el) => {
      if (el.tagName !== "NAV" || el.dataset.ftpTopbar === "true") {
        return;
      }
      const style = (el.getAttribute("style") || "").toLowerCase();
      if (style.includes("position:sticky") || style.includes("position: sticky")) {
        el.dataset.ftpLegacyRemoved = "true";
        el.style.display = "none";
      }
    });
  }

  function renderNav(config) {
    const items = NAV_ITEMS.map((item) => {
      const href = item.key === "mtl" ? getEquationHref(config) : item.href;
      return `<a href="${escapeHtml(href)}" class="ftp-nav-link" data-nav-item="${escapeHtml(item.key)}" data-slot="${escapeHtml(item.slot)}">${escapeHtml(item.label)}</a>`;
    }).join("");
    return `
      <nav class="ftp-nav" aria-label="Primary navigation" data-slot="primary-nav">
        ${items}
        <button type="button" class="ftp-nav-link ftp-nav-button" data-panel="series" data-slot="nav-series" aria-expanded="false">Series</button>
      </nav>
    `;
  }

  function renderMetric(className, slot, value, label, title) {
    return `
      <span class="ftp-metric ${className}" data-slot="${slot}" title="${escapeHtml(title)}">
        <b>${escapeHtml(value)}</b><span>${escapeHtml(label)}</span>
      </span>
    `;
  }

  function renderDomains() {
    return DOMAIN_ITEMS.map((item) => `
      <button type="button" class="ftp-domain-pill ftp-domain-${item.key}" data-domain="${item.key}" data-slot="${item.slot}" title="${escapeHtml(item.label)}">
        <span>${escapeHtml(item.short)}</span>
      </button>
    `).join("");
  }

  function renderSeriesPanel() {
    const links = SERIES_ITEMS.map((item) => `
      <a href="${escapeHtml(item.href)}" data-slot="${escapeHtml(item.slot)}">
        <span>${escapeHtml(item.label)}</span>
        <small>${escapeHtml(item.hint)}</small>
      </a>
    `).join("");
    return `
      <section class="ftp-drop-panel" id="ftpSeriesPanel" data-slot="series-panel" aria-label="Series panel">
        <h2>Series</h2>
        <div class="ftp-panel-list">${links}</div>
      </section>
    `;
  }

  function renderSearchPanel() {
    return `
      <section class="ftp-drop-panel" id="ftpSearchPanel" data-slot="search-panel" aria-label="Search panel">
        <h2>Search</h2>
        <div class="ftp-panel-list">
          <a href="/site-index.html" data-slot="search-site-index"><span>Site Index</span><small>all pages</small></a>
          <a href="/glossary/" data-slot="search-glossary"><span>Glossary</span><small>terms</small></a>
          <a href="/media/" data-slot="search-media"><span>Media</span><small>audio + video</small></a>
          <a href="/podcast/" data-slot="search-podcast"><span>Podcast</span><small>episodes</small></a>
        </div>
      </section>
    `;
  }

  function renderProofPanel(config) {
    const m = config.metrics;
    return `
      <section class="ftp-drop-panel ftp-proof-panel" id="ftpProofPanel" data-slot="proof-dashboard-panel" aria-label="Proof metrics panel">
        <h2>Proof Dashboard</h2>
        <div class="ftp-proof-grid" data-slot="proof-card-grid">
          <div class="ftp-proof-card ftp-card-domains" data-slot="proof-card-domains"><b>${escapeHtml(m.domains)}</b><span>Domains bridged on this page.</span></div>
          <div class="ftp-proof-card ftp-card-laws" data-slot="proof-card-laws"><b>${escapeHtml(m.laws)}</b><span>Ten Laws mapping target.</span></div>
          <div class="ftp-proof-card ftp-card-coherence" data-slot="proof-card-coherence"><b>${escapeHtml(m.coherence)}</b><span>Coherence score.</span></div>
          <div class="ftp-proof-card ftp-card-claims" data-slot="proof-card-claims"><b>${escapeHtml(m.claims)}</b><span>Claims surfaced for audit.</span></div>
        </div>
      </section>
    `;
  }

  function renderLabelMap() {
    const labels = {
      entry: "shared-final",
      author: "Faith Thru Physics",
      topFrame: "top-frame",
      brand: { home: "brand-home", mark: "brand-mark", name: "brand-name" },
      nav: { home: "nav-home", mtl: "nav-mtl", proof: "nav-proof", series: "nav-series" },
      readingLevels: {
        control: "reading-level-control",
        highSchool: "reading-level-high-school",
        college: "reading-level-college",
        phd: "reading-level-phd"
      },
      domains: {
        pillRow: "domain-pill-row",
        pillGroup: "domain-pills",
        logicMathematics: "domain-logic-mathematics",
        physics: "domain-physics",
        informationTheory: "domain-information-theory",
        theology: "domain-theology",
        developmentalPsychology: "domain-developmental-psychology",
        philosophy: "domain-philosophy",
        colorStrip: "domain-color-strip"
      },
      metrics: {
        numbers: "domain-row-metric-numbers",
        domains: "metric-domains-number",
        tenLaws: "metric-laws-number",
        coherence: "metric-coherence-number",
        claims: "metric-claims-number"
      },
      actions: {
        search: "search-command",
        proofDashboard: "proof-dashboard-toggle"
      }
    };
    const script = document.createElement("script");
    script.type = "application/json";
    script.id = "header-entry-labels";
    script.textContent = JSON.stringify(labels, null, 2);
    return script;
  }

  function renderTopbar(config) {
    const m = config.metrics;
    const topbar = document.createElement("header");
    topbar.className = "ftp-topbar ftp-topbar-final";
    topbar.dataset.ftpTopbar = "true";
    topbar.dataset.component = "ftp-topbar";
    topbar.dataset.version = "3.0-final";
    topbar.dataset.slot = "top-frame";
    topbar.setAttribute("data-header-entry", "shared-final");
    topbar.setAttribute("data-header-author", "Faith Thru Physics");

    topbar.innerHTML = `
      <div class="ftp-main-row" data-slot="top-frame-main-row">
        <a class="ftp-brand" href="${escapeHtml(config.brandHref)}" data-slot="brand-home" aria-label="Faith Thru Physics home">
          <span class="ftp-brand-mark" data-slot="brand-mark">X</span>
          <span class="ftp-brand-name" data-slot="brand-name">Faith<span>Thru</span>Physics</span>
        </a>
        <span class="ftp-divider" data-slot="brand-nav-divider" aria-hidden="true"></span>
        ${renderNav(config)}
        <div class="ftp-actions" data-slot="top-frame-actions">
          <div class="ftp-levels" role="group" aria-label="Reading level" data-slot="reading-level-control">
            <button type="button" data-level="high-school" data-slot="reading-level-high-school">High School</button>
            <button type="button" class="active" data-level="college" data-slot="reading-level-college">College</button>
            <button type="button" data-level="phd" data-slot="reading-level-phd">PhD</button>
          </div>
          <button type="button" class="ftp-action" data-panel="search" data-slot="search-command" aria-label="Search">Ctrl K</button>
          <button type="button" class="ftp-action ftp-proof-toggle" data-panel="proof" data-slot="proof-dashboard-toggle" aria-label="Proof dashboard">Grid</button>
          <button type="button" class="ftp-menu-toggle" data-panel="series" data-slot="mobile-menu-toggle" aria-label="Open menu" aria-expanded="false">
            <span class="ftp-menu-bar"></span><span class="ftp-menu-bar"></span><span class="ftp-menu-bar"></span>
          </button>
        </div>
      </div>
      <div class="ftp-domain-row" aria-label="Domains and page metrics" data-slot="domain-pill-row">
        <div class="ftp-metric-row" data-slot="domain-row-metric-numbers">
          ${renderMetric("ftp-metric-domains", "metric-domains-number", m.domains, "dom", "Domains bridged")}
          ${renderMetric("ftp-metric-laws", "metric-laws-number", m.laws, "Ten Laws", "Ten Laws mapped")}
          ${renderMetric("ftp-metric-coherence", "metric-coherence-number", m.coherence, "score", "Coherence score")}
          ${renderMetric("ftp-metric-claims", "metric-claims-number", m.claims, "claims", "Claims surfaced")}
        </div>
        <div class="ftp-domain-pills" data-slot="domain-pills">
          ${renderDomains()}
        </div>
      </div>
      <div class="ftp-color-strip" data-slot="domain-color-strip" aria-hidden="true">
        <span></span><span></span><span></span><span></span><span></span><span></span>
      </div>
    `;
    return topbar;
  }

  function markActiveNav(topbar) {
    const path = normalizePath(window.location.pathname);
    const rules = [
      ["home", ["/", "/index.html"]],
      ["mtl", ["/master-equation", "/equation"]],
      ["proof", ["/proof-explorer"]]
    ];

    topbar.querySelectorAll("[data-nav-item]").forEach((link) => {
      const key = link.getAttribute("data-nav-item");
      const rule = rules.find(([k]) => k === key);
      const active = Boolean(rule && rule[1].some((prefix) => path === prefix || path.startsWith(prefix + "/")));
      link.classList.toggle("active", active);
    });
  }

  function wireEvents(topbar, panels) {
    const closePanels = () => {
      Object.values(panels).forEach((panel) => panel.classList.remove("open"));
      topbar.querySelectorAll("[data-panel]").forEach((button) => button.setAttribute("aria-expanded", "false"));
    };

    topbar.querySelectorAll("[data-panel]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        const panel = panels[button.dataset.panel || ""];
        const willOpen = panel && !panel.classList.contains("open");
        closePanels();
        if (willOpen) {
          panel.classList.add("open");
          button.setAttribute("aria-expanded", "true");
        }
      });
    });

    topbar.querySelectorAll(".ftp-levels button").forEach((button) => {
      button.addEventListener("click", () => {
        topbar.querySelectorAll(".ftp-levels button").forEach((other) => other.classList.remove("active"));
        button.classList.add("active");
        document.body.dataset.ftpReadingLevel = button.dataset.level || "";
        document.dispatchEvent(new CustomEvent("ftp:reading-level", { bubbles: true, detail: { level: button.dataset.level } }));
      });
    });

    topbar.querySelectorAll(".ftp-domain-pill").forEach((pill) => {
      pill.addEventListener("click", () => {
        pill.classList.toggle("active");
        document.dispatchEvent(new CustomEvent("ftp:domain-toggle", { bubbles: true, detail: { domain: pill.dataset.domain, active: pill.classList.contains("active") } }));
      });
    });

    document.addEventListener("click", (event) => {
      if (!event.target.closest(".ftp-drop-panel") && !event.target.closest("[data-panel]")) {
        closePanels();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closePanels();
      }
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        const search = panels.search;
        const willOpen = search && !search.classList.contains("open");
        closePanels();
        if (willOpen) {
          search.classList.add("open");
        }
        document.dispatchEvent(new CustomEvent("ftp:search", { bubbles: true }));
      }
    });
  }

  function init() {
    if (document.querySelector('[data-ftp-topbar="true"]')) {
      return;
    }

    const config = getConfig();
    document.body.classList.add("ftp-topbar-enabled", "ftp-topbar-final-enabled");

    if (config.replaceLegacyNav) {
      removeLegacyNavs();
    }

    const topbar = renderTopbar(config);
    const labelMap = renderLabelMap();
    const panelWrap = document.createElement("div");
    panelWrap.className = "ftp-panel-root";
    panelWrap.dataset.slot = "topbar-panels";
    panelWrap.innerHTML = renderSeriesPanel() + renderProofPanel(config) + renderSearchPanel();

    document.body.prepend(panelWrap);
    document.body.prepend(labelMap);
    document.body.prepend(topbar);

    const panels = {
      series: panelWrap.querySelector("#ftpSeriesPanel"),
      proof: panelWrap.querySelector("#ftpProofPanel"),
      search: panelWrap.querySelector("#ftpSearchPanel")
    };

    markActiveNav(topbar);
    wireEvents(topbar, panels);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
