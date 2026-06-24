(function(){
  if(document.querySelector("[data-site-shell]")) return;

  const currentPath = decodeURIComponent(window.location.pathname).replace(/\/index\.html$/i, "/");
  const isHomePage = currentPath === "/";

  const sections = [
    {label:"Story", href:"/index.html#master-story", mode:"easy"},
    {label:"Plain", href:"/index.html#start", mode:"academic"},
    {label:"Deep", href:"/index.html#ladder", mode:"math"},
    {label:"Proof", href:"/index.html#proof-structure", mode:"proof"}
  ];

  const subdomains = [
    {label:"Home", href:"/"},
    {label:"Master Story", href:"/master_story_index.html"},
    {label:"Master Equation", href:"/equation/"},
    {label:"Isomorphism", href:"/isomorphism/"},
    {label:"Axiom Layer", href:"/Axiom%20Layer/axioms-layer-0-core.html"},
    {label:"Proof Architecture", href:"/proof-architecture/"},
    {label:"Lean 4 Corpus", href:"/lean4/"},
    {label:"Rigor", href:"/rigor/"},
    {label:"Bidirectional Audit", href:"/the-bidirectional-audit/"}
  ];

  function iconHome(){
    return '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>';
  }

  function iconSeries(){
    return '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>';
  }

  function currentSection(){
    const hash = window.location.hash || "#academic";
    return sections.find(section => section.href === hash) || sections[0];
  }

  function loadAsset(tag, attrs, existsSelector){
    if(document.querySelector(existsSelector)) return;
    const el = document.createElement(tag);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    document.head.appendChild(el);
  }

  function setReaderMode(mode){
    document.documentElement.dataset.readerMode = mode;
    try{ localStorage.setItem("ftp-reader-mode", mode); }catch(e){}
    document.querySelectorAll("[data-reader-mode]").forEach(el => {
      if(el.classList.contains("site-shell-tab")) return;
      const modes = (el.getAttribute("data-reader-mode") || "").split(/\s+/);
      el.hidden = modes.length && !modes.includes(mode);
    });
    document.dispatchEvent(new CustomEvent("ftp-layer-change", {detail:{layer:mode}}));
  }

  function renderTop(){
    const current = currentSection();
    const tabs = sections.map(section => {
      const active = section.label === current.label ? " is-active" : "";
      return `<a class="site-shell-tab${active}" href="${section.href}" data-reader-mode="${section.mode}">${section.label}</a>`;
    }).join("");

    const top = document.createElement("nav");
    top.className = "site-shell-top";
    top.setAttribute("data-site-shell", "top");
    top.setAttribute("aria-label", "Site frame");
    top.innerHTML = `
      <a class="site-shell-home" href="/">${iconHome()}<span>Home</span></a>
      <div class="site-shell-center">
        <span class="site-shell-side-label">Reading</span>
        <div class="site-shell-tabs" aria-label="Homepage sections">${tabs}</div>
        <span class="site-shell-side-label">Level</span>
      </div>
      <a class="site-shell-series" href="#all">${iconSeries()}<span>Series</span></a>
    `;
    document.body.prepend(top);
  }

  function renderBottom(){
    const nav = document.createElement("nav");
    nav.className = "site-shell-subdomains";
    nav.setAttribute("data-site-shell", "bottom");
    nav.setAttribute("aria-label", "Faith Through Physics network");
    nav.innerHTML = `
      <div class="site-shell-subdomain-inner">
        ${subdomains.map(item => {
          const target = decodeURIComponent(new URL(item.href, window.location.origin).pathname).replace(/\/index\.html$/i, "/");
          const active = target === "/" ? currentPath === "/" : currentPath.startsWith(target);
          return `<a class="site-shell-subdomain-link${active ? " is-active" : ""}" href="${item.href}"><span class="site-shell-dot"></span>${item.label}</a>`;
        }).join("")}
      </div>
    `;

    const audit = document.createElement("section");
    audit.className = "site-audit-footer";
    audit.setAttribute("data-site-shell", "audit");
    audit.innerHTML = `
      <div class="site-audit-inner">
        <div class="site-audit-title">Audit Layer</div>
        <div class="site-audit-note">Every page should end with the same three-part check: what we got right, what we overstated, and what we got wrong. Use it as the bright end cap, even when the page style changes.</div>
        <div class="site-audit-note"><strong>Epistemic covenant:</strong> we present these claims as openly, fairly, and truthfully as we can. The evidence can be checked; the mechanisms can be challenged; the proof burden is named. Where the work moves from how the science behaves to why it means something, the choice is yours. We think the pattern is worth believing, but we will not hide where faith begins.</div>
        <div class="site-audit-grid">
          <article class="site-audit-card is-green">
            <h3>What We Got Right</h3>
            <p>Load-bearing claims, clean definitions, and the parts that clearly survived the check.</p>
          </article>
          <article class="site-audit-card is-amber">
            <h3>What We Overstated</h3>
            <p>Strong direction, but the language ran ahead of the evidence, the mechanism, or the proof available on the page.</p>
          </article>
          <article class="site-audit-card is-red">
            <h3>What We Got Wrong</h3>
            <p>Claims that need correction, tightening, or a weaker formulation before publication.</p>
          </article>
        </div>
      </div>
    `;

    const credit = document.createElement("div");
    credit.className = "site-shell-credit";
    credit.setAttribute("data-site-shell", "credit");
    credit.textContent = "© 2024-2026 David Lowe · Faith Through Physics";

    const footer = document.querySelector("footer");
    if(footer){
      footer.parentNode.insertBefore(nav, footer);
      footer.parentNode.insertBefore(audit, footer);
      footer.insertAdjacentElement("afterend", credit);
    }else{
      document.body.append(nav, audit, credit);
    }
  }

  function markActiveTab(){
    const current = currentSection();
    document.querySelectorAll(".site-shell-tab").forEach(tab => {
      tab.classList.toggle("is-active", tab.textContent.trim() === current.label);
    });
    setReaderMode(current.mode);
  }

  function renderPlayer(){
    if(document.querySelector(".tp-pill-player, .tp-pill-bar")) return;

    loadAsset("link", {rel:"stylesheet", href:"/components/tp-pill-player.css"}, 'link[href="/components/tp-pill-player.css"]');
    loadAsset("script", {src:"/components/tp-pill-player.js", defer:"defer"}, 'script[src="/components/tp-pill-player.js"]');

    const slug = document.body.getAttribute("data-audio-slug") || location.pathname.replace(/^\/|\/$/g, "").replace(/[\/.]/g, "-") || "site-home";
    const player = document.createElement("div");
    player.className = "tp-pill-bar";
    player.id = "tpPillBar";
    player.setAttribute("data-audio-slug", slug);
    player.setAttribute("data-audio-api", "https://faith-audio-pipeline.davidokc28.workers.dev/api/audio");
    player.innerHTML = `
      <div class="tp-pill-strip">
        <button class="tp-pill active" data-mode="deep" data-src="" data-label="Podcast"><span class="dot"></span>Podcast</button>
        <button class="tp-pill" data-mode="tts" data-src="" data-label="TTS"><span class="dot"></span>TTS</button>
        <button class="tp-pill" data-mode="web" data-src="" data-label="Browser"><span class="dot"></span>Browser</button>
      </div>
      <div class="tp-bar-controls">
        <button class="tp-bar-play" type="button" aria-label="Play"><i class="fas fa-play"></i></button>
        <div class="tp-bar-track" aria-label="Audio seek"><div class="tp-bar-fill"></div></div>
        <span class="tp-bar-time">0:00 / 0:00</span>
        <select class="tp-bar-speed" aria-label="Playback speed">
          <option value="0.5">0.5x</option><option value="0.75">0.75x</option>
          <option value="1" selected>1x</option><option value="1.25">1.25x</option>
          <option value="1.5">1.5x</option><option value="1.75">1.75x</option><option value="2">2x</option>
        </select>
        <button class="tp-bar-mute" type="button" aria-label="Mute"><i class="fas fa-volume-up"></i></button>
        <input class="tp-bar-volume" type="range" min="0" max="1" step="0.01" value="1" aria-label="Volume">
      </div>
      <audio preload="metadata"></audio>
    `;
    const top = document.querySelector('[data-site-shell="top"]');
    if(top) top.insertAdjacentElement("afterend", player);
    else document.body.prepend(player);

    if(window.TPPillPlayer?.initAll) window.TPPillPlayer.initAll();
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("site-shell-enabled");
    if(!document.getElementById("site-audit-footer-styles")){
      const style = document.createElement("style");
      style.id = "site-audit-footer-styles";
      style.textContent = `
        .site-audit-footer {
          padding: 1.1rem 1rem 1.3rem;
          background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
          border-top: 1px solid rgba(255,255,255,0.06);
        }
        .site-audit-inner {
          max-width: 1100px;
          margin: 0 auto;
          display: grid;
          gap: 0.8rem;
        }
        .site-audit-title {
          font: 600 0.62rem 'JetBrains Mono', ui-monospace, monospace;
          letter-spacing: 0.18em;
          text-transform: uppercase;
          color: rgba(255,255,255,0.38);
        }
        .site-audit-note {
          color: rgba(255,255,255,0.28);
          font-size: 0.72rem;
          line-height: 1.6;
          max-width: 74ch;
        }
        .site-audit-note strong {
          color: #d4af37;
          font-weight: 600;
        }
        .site-audit-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.75rem;
        }
        .site-audit-card {
          padding: 0.95rem 1rem;
          border-radius: 0.85rem;
          border: 1px solid rgba(255,255,255,0.08);
          background: rgba(255,255,255,0.03);
          min-height: 92px;
        }
        .site-audit-card h3 {
          margin: 0 0 0.35rem;
          font: 600 0.74rem 'JetBrains Mono', ui-monospace, monospace;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }
        .site-audit-card p {
          margin: 0;
          color: rgba(255,255,255,0.42);
          font-size: 0.78rem;
          line-height: 1.55;
        }
        .site-audit-card.is-green { border-color: rgba(34,197,94,0.2); background: rgba(34,197,94,0.04); }
        .site-audit-card.is-green h3 { color: #22c55e; }
        .site-audit-card.is-amber { border-color: rgba(212,175,55,0.22); background: rgba(212,175,55,0.04); }
        .site-audit-card.is-amber h3 { color: #d4af37; }
        .site-audit-card.is-red { border-color: rgba(239,68,68,0.2); background: rgba(239,68,68,0.04); }
        .site-audit-card.is-red h3 { color: #ef4444; }
        @media (max-width: 780px) {
          .site-audit-grid { grid-template-columns: 1fr; }
        }
      `;
      document.head.appendChild(style);
    }
    if(!isHomePage) renderTop();
    renderPlayer();
    renderBottom();
    setReaderMode(currentSection().mode);
    document.addEventListener("click", event => {
      const tab = event.target.closest(".site-shell-tab[data-reader-mode]");
      if(!tab) return;
      setReaderMode(tab.getAttribute("data-reader-mode"));
    });
    window.addEventListener("hashchange", markActiveTab);
  });
})();
