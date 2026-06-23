(function () {
  "use strict";

  const LEVELS = [
    { key: "story", label: "Story path" },
    { key: "plain", label: "Plain path" },
    { key: "test", label: "Test path" },
    { key: "proof", label: "Proof path" }
  ];

  function slugUrl(slug) {
    if (!slug) return "";
    if (/^(https?:)?\/\//.test(slug) || slug.startsWith("/")) return slug;
    return `/${slug.replace(/^\/+/, "")}/`;
  }

  function hexToRgb(hex) {
    const clean = String(hex || "").replace("#", "").trim();
    if (!/^[0-9a-f]{6}$/i.test(clean)) return { r: 55, g: 138, b: 221 };
    const n = parseInt(clean, 16);
    return { r: n >> 16, g: (n >> 8) & 255, b: n & 255 };
  }

  function tint(hex, alpha) {
    const rgb = hexToRgb(hex);
    return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`;
  }

  function normalizeClassification(items) {
    const list = Array.isArray(items) ? items.filter((item) => item && item.tag) : [];
    const total = list.reduce((sum, item) => sum + Math.max(0, Number(item.pct) || 0), 0) || 100;
    return list.map((item) => ({
      tag: String(item.tag),
      pct: Math.max(0, Number(item.pct) || 0),
      width: Math.max(0, Number(item.pct) || 0) / total * 100,
      color: item.color || "#378ADD"
    }));
  }

  function availableLevels(meta) {
    if (Array.isArray(meta.reading_levels)) return new Set(meta.reading_levels);
    const panels = document.querySelectorAll("[data-reading-level]");
    return new Set(Array.from(panels).map((panel) => panel.dataset.readingLevel));
  }

  function setActiveLevel(root, level) {
    root.querySelectorAll(".tp-reading-tab").forEach((tab) => {
      const selected = tab.dataset.level === level;
      tab.setAttribute("aria-selected", selected ? "true" : "false");
      tab.tabIndex = selected ? 0 : -1;
    });

    document.querySelectorAll("[data-reading-level]").forEach((panel) => {
      panel.hidden = panel.dataset.readingLevel !== level;
      panel.classList.add("tp-reading-panel");
    });

    document.dispatchEvent(new CustomEvent("tp:reading-level-change", { detail: { level } }));
  }

  function render(target, meta) {
    const root = typeof target === "string" ? document.querySelector(target) : target;
    if (!root) return null;

    const data = meta || {};
    const theme = root.dataset.theme || data.theme || "light";
    const classes = ["tp-top-bar", "tp-theme"];
    root.className = classes.join(" ");
    root.dataset.theme = theme;
    root.innerHTML = "";

    const classification = normalizeClassification(data.classification);
    const levelSet = availableLevels(data);
    const firstEnabled = LEVELS.find((level) => levelSet.has(level.key)) || LEVELS[0];

    const main = document.createElement("div");
    main.className = "tp-top-main";

    const home = document.createElement("a");
    home.className = "tp-home-link";
    home.href = "/";
    home.innerHTML = `
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span>Faith Through Physics</span>
    `;

    const tabs = document.createElement("div");
    tabs.className = "tp-reading-tabs";
    tabs.setAttribute("role", "tablist");
    tabs.setAttribute("aria-label", "Reading paths");

    LEVELS.forEach((level) => {
      const enabled = levelSet.has(level.key);
      const tab = document.createElement("button");
      tab.className = "tp-reading-tab";
      tab.type = "button";
      tab.dataset.level = level.key;
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-selected", level.key === firstEnabled.key ? "true" : "false");
      tab.disabled = !enabled;
      if (!enabled) tab.setAttribute("aria-disabled", "true");
      tab.textContent = level.label;
      tab.addEventListener("click", () => {
        if (!tab.disabled) setActiveLevel(root, level.key);
      });
      tab.addEventListener("keydown", (event) => {
        if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
        const enabledTabs = Array.from(tabs.querySelectorAll(".tp-reading-tab:not(:disabled)"));
        const index = enabledTabs.indexOf(tab);
        let nextIndex = index;
        if (event.key === "ArrowLeft") nextIndex = Math.max(0, index - 1);
        if (event.key === "ArrowRight") nextIndex = Math.min(enabledTabs.length - 1, index + 1);
        if (event.key === "Home") nextIndex = 0;
        if (event.key === "End") nextIndex = enabledTabs.length - 1;
        enabledTabs[nextIndex].focus();
        enabledTabs[nextIndex].click();
        event.preventDefault();
      });
      tabs.appendChild(tab);
    });

    const nav = document.createElement("div");
    nav.className = "tp-top-nav";
    const prev = data.prev || {};
    const next = data.next || {};

    const prevHref = slugUrl(prev.slug);
    const nextHref = slugUrl(next.slug);

    const prevLink = document.createElement(prevHref ? "a" : "span");
    prevLink.className = "tp-top-nav-link";
    if (prevHref) prevLink.href = prevHref;
    prevLink.textContent = prev.title ? "\u2190 Prev" : "";
    if (prev.title) prevLink.title = prev.title;

    const nextLink = document.createElement(nextHref ? "a" : "span");
    nextLink.className = "tp-top-nav-link";
    if (nextHref) nextLink.href = nextHref;
    nextLink.textContent = next.title ? "Next \u2192" : "";
    if (next.title) nextLink.title = next.title;

    nav.append(prevLink, nextLink);
    main.append(home, tabs, nav);

    const classBar = document.createElement("div");
    classBar.className = "tp-class-bar";

    const classInner = document.createElement("div");
    classInner.className = "tp-class-inner";

    const classLabel = document.createElement("div");
    classLabel.className = "tp-class-label";
    classLabel.textContent = data.classification_label || "Article classification";

    const bar = document.createElement("div");
    bar.className = "tp-percent-bar";
    bar.setAttribute("aria-label", "Domain classification percentages");
    classification.forEach((item) => {
      const segment = document.createElement("span");
      segment.className = "tp-percent-segment";
      segment.style.width = `${item.width}%`;
      segment.style.setProperty("--tp-segment-color", item.color);
      segment.title = `${item.tag} ${item.pct}%`;
      bar.appendChild(segment);
    });

    const pills = document.createElement("ul");
    pills.className = "tp-domain-pills";
    classification.forEach((item) => {
      const pill = document.createElement("li");
      pill.className = "tp-domain-pill";
      pill.style.setProperty("--tp-pill-bg", tint(item.color, 0.12));
      pill.style.setProperty("--tp-pill-color", item.color);
      pill.innerHTML = `<span class="tp-domain-dot" aria-hidden="true"></span><span>${item.tag} ${item.pct}%</span>`;
      pills.appendChild(pill);
    });

    classInner.append(classLabel, bar, pills);
    classBar.appendChild(classInner);

    root.append(main, classBar);
    setActiveLevel(root, firstEnabled.key);
    return root;
  }

  window.TPTopBar = { render, setActiveLevel };
})();
