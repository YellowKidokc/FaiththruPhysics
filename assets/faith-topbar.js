(function () {
  "use strict";

  /**
   * Faith Through Physics — shared site topbar (v2).
   * Include on any page:
   *   <link rel="stylesheet" href="/assets/faith-topbar.css">
   *   <script defer src="/assets/faith-topbar.js"></script>
   * Optional override: window.FTP_TOPBAR = { equationHref: "/master-equation/" };
   */

  if (window.__ftpFaithTopbarLoaded) {
    return;
  }
  window.__ftpFaithTopbarLoaded = true;

  const DEFAULT_CONFIG = {
    replaceLegacyNav: true,
    compact: true,
    brandHref: "/index.html",
    equationHref: "auto",
    title: document.title || "Faith Through Physics"
  };

  const LEGACY_SELECTORS = [
    "header.ftp-top",
    ".ftp-panel-toggle",
    ".ftp-panel",
    ".topbar",
    "header.pe-header",
    "nav.tp-ribbon"
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

  function navItems(config) {
    const equationHref =
      config.equationHref && config.equationHref !== "auto"
        ? config.equationHref
        : "/master-equation/";
    return [
      { key: "home", label: "Home", href: "/index.html" },
      { key: "series", label: "Series", href: "/series.html" },
      { key: "proof", label: "Proof", href: "/proof-explorer/" },
      { key: "equation", label: "Equation", href: equationHref },
      { key: "media", label: "Media", href: "/media/" },
      { key: "podcast", label: "Podcast", href: "/podcast/" },
      { key: "glossary", label: "Glossary", href: "/glossary/" },
      { key: "all-pages", label: "All Pages", href: "/site-index.html" }
    ];
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

  function renderNavLinks(items, mobile) {
    const cls = mobile ? "ftp-nav ftp-nav--mobile" : "ftp-nav";
    const links = items
      .map(
        (item) =>
          `<a href="${escapeHtml(item.href)}" class="ftp-nav-link" data-nav-item="${escapeHtml(item.key)}">${escapeHtml(item.label)}</a>`
      )
      .join("");
    return `<nav class="${cls}" data-section="primary-navigation" aria-label="Primary">${links}</nav>`;
  }

  function renderTopbar(config) {
    const items = navItems(config);
    const topbar = document.createElement("header");
    topbar.className = "ftp-topbar" + (config.compact ? " ftp-topbar-compact" : "");
    topbar.dataset.ftpTopbar = "true";
    topbar.dataset.component = "ftp-topbar";
    topbar.dataset.version = "2.0";

    topbar.innerHTML = `
      <div class="ftp-main-row" data-section="topbar-main-row">
        <div class="ftp-brand" data-section="brand-block">
          <a href="${escapeHtml(config.brandHref)}" class="ftp-brand-mark" aria-label="Faith Through Physics Home">χ</a>
          <span class="ftp-brand-name">Faith Through Physics</span>
          <span class="ftp-divider ftp-divider--nav" aria-hidden="true"></span>
          ${renderNavLinks(items, false)}
        </div>
        <div class="ftp-actions" data-section="right-actions">
          <button type="button" class="ftp-menu-toggle" data-action="toggle-mobile-menu" aria-label="Open menu" aria-expanded="false">
            <span class="ftp-menu-bar"></span>
            <span class="ftp-menu-bar"></span>
            <span class="ftp-menu-bar"></span>
          </button>
          <div class="ftp-search" data-action="open-search" aria-label="Search shortcut" role="button" tabindex="0">
            <span>⌕</span> <span>Ctrl+K</span>
          </div>
        </div>
      </div>
      <div class="ftp-mobile-menu" data-section="mobile-menu" aria-hidden="true">
        ${renderNavLinks(items, true)}
      </div>
    `;

    return topbar;
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

  function markActiveNav(topbar) {
    const path = normalizePath(window.location.pathname);
    const rules = [
      ["home", ["/", "/index.html"]],
      ["series", ["/series", "/series.html"]],
      ["proof", ["/proof-explorer"]],
      ["equation", ["/equation", "/master-equation"]],
      ["media", ["/media"]],
      ["podcast", ["/podcast"]],
      ["glossary", ["/glossary"]],
      ["all-pages", ["/site-index", "/site-index.html"]]
    ];

    topbar.querySelectorAll("[data-nav-item]").forEach((link) => {
      const key = link.getAttribute("data-nav-item");
      const rule = rules.find(([k]) => k === key);
      if (!rule) {
        return;
      }
      const active = rule[1].some((prefix) => path === prefix || path.startsWith(prefix + "/"));
      link.classList.toggle("active", active);
    });
  }

  function wireEvents(topbar) {
    const menuToggle = topbar.querySelector("[data-action='toggle-mobile-menu']");
    const mobileMenu = topbar.querySelector("[data-section='mobile-menu']");
    const search = topbar.querySelector("[data-action='open-search']");

    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener("click", () => {
        const isOpen = topbar.classList.toggle("ftp-menu-open");
        mobileMenu.setAttribute("aria-hidden", String(!isOpen));
        menuToggle.setAttribute("aria-expanded", String(isOpen));
      });
    }

    if (search) {
      const openSearch = () => document.dispatchEvent(new CustomEvent("ftp:search", { bubbles: true }));
      search.addEventListener("click", openSearch);
      search.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openSearch();
        }
      });
    }

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && topbar.classList.contains("ftp-menu-open") && mobileMenu) {
        topbar.classList.remove("ftp-menu-open");
        mobileMenu.setAttribute("aria-hidden", "true");
        if (menuToggle) {
          menuToggle.setAttribute("aria-expanded", "false");
        }
      }
      const searchHotkey = event.key.toLowerCase() === "k" && (event.metaKey || event.ctrlKey);
      if (searchHotkey) {
        event.preventDefault();
        document.dispatchEvent(new CustomEvent("ftp:search", { bubbles: true }));
      }
    });

    document.addEventListener("click", (event) => {
      if (!topbar.classList.contains("ftp-menu-open") || !mobileMenu) {
        return;
      }
      const clickedInsideMenu = mobileMenu.contains(event.target);
      const clickedToggle = menuToggle && menuToggle.contains(event.target);
      if (!clickedInsideMenu && !clickedToggle) {
        topbar.classList.remove("ftp-menu-open");
        mobileMenu.setAttribute("aria-hidden", "true");
        if (menuToggle) {
          menuToggle.setAttribute("aria-expanded", "false");
        }
      }
    });
  }

  async function resolveEquationHref(config) {
    if (config.equationHref && config.equationHref !== "auto") {
      return config.equationHref;
    }
    try {
      const response = await fetch("/equation/index.html", { method: "HEAD", cache: "no-store" });
      if (response.ok) {
        return "/equation/";
      }
    } catch (_err) {
      /* offline or file:// preview */
    }
    return "/master-equation/";
  }

  function init() {
    if (document.querySelector(".ftp-topbar")) {
      return;
    }

    const config = getConfig();
    document.body.classList.add("ftp-topbar-enabled");
    if (config.compact) {
      document.body.classList.add("ftp-topbar-compact");
    }

    if (config.replaceLegacyNav) {
      removeLegacyNavs();
    }

    resolveEquationHref(config).then((equationHref) => {
      config.equationHref = equationHref;
      const topbar = renderTopbar(config);
      document.body.prepend(topbar);
      markActiveNav(topbar);
      wireEvents(topbar);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
