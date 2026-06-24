/**
 * TP Inject — unified top bar + bottom bar + sticky player injector.
 *
 * Include once per page, ideally just before </body>:
 *   <script src="/components/tp-inject.js"></script>
 *
 * Reads metadata from (in order of priority):
 *   1. <script id="article-meta" type="application/json">...</script>
 *   2. meta.json in the same directory as the HTML file
 *   3. Graceful fallback: empty meta (bars still render, navigation empty)
 *
 * Optional data attributes on the script tag:
 *   data-theme="dark|light" — override theme detection
 *   data-component-base="/components/" — override component base URL
 */
(function () {
  "use strict";

  const COMPONENT_BASE = document.currentScript?.dataset.componentBase || "/components/";
  const CSS_FILES = ["tp-theme.css", "tp-top-bar.css", "tp-bottom-bar.css"];
  const JS_FILES = ["tp-sticky-player.js", "tp-top-bar.js", "tp-domain-ribbon.js", "tp-bottom-bar.js"];
  const SUBDOMAINS = [
    { label: "Home", href: "/" },
    { label: "Audio Library", href: "/audio/" },
    { label: "Podcast", href: "/podcast/" },
    { label: "Glossary", href: "/glossary/" },
    { label: "Master Equation", href: "/master-equation/" },
    { label: "Axiom Layer", href: "/Axiom%20Layer/axioms.html" },
    { label: "Proof Explorer", href: "/proof-explorer/" },
    { label: "Rigor", href: "/rigor/" },
    { label: "Lean 4", href: "/lean4/lean4-index.html" },
    { label: "Bidirectional Audit", href: "/the-bidirectional-audit/" },
    { label: "Convergence", href: "/convergence-series/" },
    { label: "Blue Series", href: "/blue/" },
    { label: "One-Page Stories", href: "/one-page-stories/" },
    { label: "Moral Decline", href: "/moral-decline/" },
    { label: "Genesis to Quantum", href: "/genesis-to-quantum/" },
    { label: "Isomorphisms", href: "/isomorphism/" }
  ];

  function componentUrl(file) {
    return new URL(file, new URL(COMPONENT_BASE, location.href)).href;
  }

  function loadCss(file) {
    const href = componentUrl(file);
    if (document.querySelector(`link[href="${href}"]`)) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  }

  function loadScript(file) {
    return new Promise((resolve, reject) => {
      const ns = file.replace(/\.js$/, "").replace(/-/g, "");
      const global = ns === "tpstickyplayer" ? "TPStickyPlayer"
        : ns === "tptopbar" ? "TPTopBar"
        : ns === "tpdomainribbon" ? "TPDomainRibbon"
        : ns === "tpbottombar" ? "TPBottomBar"
        : null;
      if (global && window[global]) return resolve();

      const script = document.createElement("script");
      script.src = componentUrl(file);
      script.defer = true;
      script.onload = resolve;
      script.onerror = () => reject(new Error("Failed to load " + file));
      document.head.appendChild(script);
    });
  }

  function parseEmbeddedMeta() {
    const node = document.getElementById("article-meta");
    if (!node) return null;
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      console.warn("Could not parse #article-meta JSON", error);
      return null;
    }
  }

  async function loadMetaJson() {
    try {
      const path = location.pathname.replace(/\/[^/]*$/, "/meta.json");
      const res = await fetch(path, { credentials: "same-origin" });
      if (!res.ok) return {};
      return await res.json();
    } catch (error) {
      return {};
    }
  }

  async function loadMeta() {
    const embedded = parseEmbeddedMeta();
    if (embedded) return embedded;
    return await loadMetaJson();
  }

  function hasExistingShell() {
    return !!document.querySelector(
      ".ftp-topbar, .ftp-subdomain-strip, .tp-top-bar, .tp-subdomains, .site-nav-bar, .mda-topbar-v2, #tp-top-bar, #tp-bottom-bar, .tp-bottom-bar"
    );
  }

  function detectTheme(meta) {
    const scriptTheme = document.currentScript?.dataset.theme;
    if (scriptTheme === "dark" || scriptTheme === "light") return scriptTheme;

    if (meta.theme === "dark" || meta.theme === "light") return meta.theme;

    const bodyTheme = document.body?.dataset.theme;
    if (bodyTheme === "dark" || bodyTheme === "light") return bodyTheme;

    const htmlTheme = document.documentElement?.dataset.theme;
    if (htmlTheme === "dark" || htmlTheme === "light") return htmlTheme;

    // Infer from background color if we can compute it.
    try {
      const bg = getComputedStyle(document.body).backgroundColor;
      const values = bg.match(/\d+/g)?.map(Number) || [255, 255, 255];
      const luminance = (0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]) / 255;
      return luminance < 0.35 ? "dark" : "light";
    } catch (e) {
      return "dark";
    }
  }

  function firstContentContainer() {
    return document.querySelector("main, article, .content, .article, #content") || document.body;
  }

  function currentSubdomainHref() {
    const path = decodeURIComponent(location.pathname).toLowerCase();
    return SUBDOMAINS.find((item) => {
      const href = decodeURIComponent(item.href).toLowerCase();
      return href !== "/" && path.startsWith(href);
    })?.href || "/";
  }

  function buildSubdomains() {
    const nav = document.createElement("nav");
    nav.className = "tp-subdomains";
    nav.setAttribute("aria-label", "Faith Through Physics sections");

    const inner = document.createElement("div");
    inner.className = "tp-subdomains-inner";

    const current = currentSubdomainHref();
    SUBDOMAINS.forEach((item) => {
      const link = document.createElement("a");
      link.className = "tp-sub-link";
      link.href = item.href;
      if (item.href === current) link.setAttribute("aria-current", "page");
      link.innerHTML = `<span class="tp-sub-dot" aria-hidden="true"></span><span>${item.label}</span>`;
      inner.appendChild(link);
    });

    nav.appendChild(inner);
    return nav;
  }

  function inferMetaDefaults(meta) {
    const out = { ...meta };

    // Derive slug from filename if missing.
    if (!out.slug) {
      const filename = location.pathname.split("/").pop();
      out.slug = filename.replace(/\.html?$/i, "").replace(/[^a-z0-9-]+/gi, "-").replace(/^-|-$/g, "").toLowerCase();
    }

    // Provide a minimal classification so the top bar has something to show.
    if (!Array.isArray(out.classification) || out.classification.length === 0) {
      out.classification = [{ tag: "theophysics", pct: 100, color: "#d4af37" }];
    }

    // Default audio API.
    if (!out.audio_api) {
      out.audio_api = "https://faith-audio-pipeline.davidokc28.workers.dev/api/audio";
    }

    return out;
  }

  function inject(meta) {
    if (hasExistingShell()) {
      console.info("TP Inject: existing shell detected; skipping injection.");
      return;
    }

    const theme = detectTheme(meta);
    const enriched = inferMetaDefaults(meta);

    const content = firstContentContainer();

    const top = document.createElement("div");
    top.id = "tp-top-bar";
    top.dataset.theme = theme;
    content.insertBefore(top, content.firstChild);

    const bottom = document.createElement("div");
    bottom.id = "tp-bottom-bar";
    bottom.dataset.theme = theme;

    const subdomains = buildSubdomains();
    document.body.appendChild(subdomains);
    document.body.appendChild(bottom);

    if (window.TPTopBar) window.TPTopBar.render(top, { ...enriched, theme });
    if (window.TPDomainRibbon) window.TPDomainRibbon.render(top, { ...enriched, theme });
    if (window.TPBottomBar) window.TPBottomBar.render(bottom, { ...enriched, theme });
  }

  async function init() {
    CSS_FILES.forEach(loadCss);
    await JS_FILES.reduce((promise, file) => promise.then(() => loadScript(file)), Promise.resolve());
    const meta = await loadMeta();
    inject(meta);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
