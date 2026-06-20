/**
 * Faith Through Physics - shared site shell.
 *
 * Drop this script into any HTML page:
 *   <script src="/components/site-shell.js"></script>
 *
 * Optional data attributes:
 *   data-active-tab="academic"
 *   data-prev-href="/previous/"
 *   data-next-href="/next/"
 *   data-series-href="/series/"
 *   data-hide-tabs="true"
 *   data-audio-slug="article-slug"
 *   data-audio-api="https://faith-audio-pipeline.davidokc28.workers.dev/api/audio"
 *   data-hide-player="true"
 */
(function () {
  'use strict';

  if (window.__ftpSiteShellLoaded) return;
  window.__ftpSiteShellLoaded = true;

  const script = document.currentScript;
  const cfg = {
    activeTab: script?.getAttribute('data-active-tab') || 'academic',
    prevHref: script?.getAttribute('data-prev-href') || '',
    nextHref: script?.getAttribute('data-next-href') || '',
    seriesHref: script?.getAttribute('data-series-href') || '/proof-explorer/',
    hideTabs: script?.getAttribute('data-hide-tabs') === 'true',
    audioSlug: script?.getAttribute('data-audio-slug') || document.body?.dataset?.audioSlug || '',
    audioApi: script?.getAttribute('data-audio-api') || 'https://faith-audio-pipeline.davidokc28.workers.dev/api/audio',
    hidePlayer: script?.getAttribute('data-hide-player') === 'true',
    shellAccent: script?.getAttribute('data-shell-accent') || '',
  };

  const SUBDOMAINS = [
    { label: 'Home', href: '/' },
    { label: 'Convergence Series', href: '/convergence-series/' },
    { label: 'Convergence Deep', href: '/convergence-deep/' },
    { label: 'Blue Series', href: '/blue/' },
    { label: 'One-Page Stories', href: '/one-page-stories/' },
    { label: 'Master Equation', href: '/master-equation/' },
    { label: 'Moral Decline', href: '/moral-decline/' },
    { label: 'Genesis to Quantum', href: '/genesis-to-quantum/' },
    { label: 'Axiom Layer', href: '/Axiom%20Layer/axioms-layer-0-core.html' },
    { label: 'Proof Explorer', href: '/proof-explorer/' },
    { label: 'Lean 4 Corpus', href: '/lean4/' },
    { label: 'Bidirectional Audit', href: '/the-bidirectional-audit/' },
  ];

  const LAYERS = [
    { id: 'easy', label: 'Easy' },
    { id: 'academic', label: 'Academic' },
    { id: 'math', label: 'Math Translation Layer' },
    { id: 'proof', label: 'Proof-Claims' },
  ];

  const STYLES = `
    .ftp-topbar {
      position: sticky; top: 0; z-index: 1000;
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; min-height: 44px; padding: 0.35rem 1rem;
      background: rgba(5,5,5,0.97); border-bottom: 1px solid color-mix(in srgb, var(--ftp-shell-accent, #d4af37) 38%, transparent);
      font-family: 'Oswald', system-ui, sans-serif; color: rgba(255,255,255,0.62);
    }
    .ftp-topbar a { color: inherit; text-decoration: none; transition: color 0.15s, background 0.15s; }
    .ftp-topbar a:hover { color: var(--ftp-shell-accent, #d4af37); }
    .ftp-tb-home, .ftp-tb-series { display: inline-flex; align-items: center; gap: 0.4rem; white-space: nowrap; }
    .ftp-tb-home { font-family: 'Cinzel', serif; color: var(--ftp-shell-accent, #d4af37); letter-spacing: 0.08em; font-size: 0.72rem; }
    .ftp-tb-series { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; }
    .ftp-tb-center { display: flex; align-items: center; justify-content: center; gap: 0.75rem; min-width: 0; }
    .ftp-tb-nav { opacity: 0.38; font-size: 0.62rem; letter-spacing: 0.08em; text-transform: uppercase; }
    .ftp-tb-nav.active { opacity: 0.85; }
    .ftp-layer-tabs { display: flex; gap: 0.25rem; flex-wrap: wrap; justify-content: center; }
    .ftp-layer-tab {
      border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03);
      color: rgba(255,255,255,0.48); padding: 0.33rem 0.62rem; border-radius: 999px;
      font: 600 0.58rem 'JetBrains Mono', ui-monospace, monospace;
      cursor: pointer; text-transform: uppercase; letter-spacing: 0.08em;
    }
    .ftp-layer-tab:hover, .ftp-layer-tab.active {
      color: var(--ftp-shell-accent, #d4af37);
      border-color: color-mix(in srgb, var(--ftp-shell-accent, #d4af37) 42%, transparent);
      background: color-mix(in srgb, var(--ftp-shell-accent, #d4af37) 10%, transparent);
    }
    .ftp-subdomain-strip {
      border-top: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.04);
      background: #0a0a0f; padding: 0.75rem 1rem; font-family: 'JetBrains Mono', ui-monospace, monospace;
    }
    .ftp-subdomain-inner {
      display: flex; justify-content: center; flex-wrap: wrap; gap: 0.25rem 0.65rem;
      max-width: 1180px; margin: 0 auto;
    }
    .ftp-sub-link {
      display: flex; align-items: center; gap: 0.35rem; padding: 0.3rem 0.48rem; border-radius: 0.35rem;
      color: rgba(255,255,255,0.38); text-decoration: none; font-size: 0.58rem;
      letter-spacing: 0.06em; text-transform: uppercase; transition: color 0.15s, background 0.15s;
    }
    .ftp-sub-link:hover, .ftp-sub-link.active {
      color: var(--ftp-shell-accent, #d4af37);
      background: color-mix(in srgb, var(--ftp-shell-accent, #d4af37) 9%, transparent);
    }
    .ftp-sub-dot { width: 4px; height: 4px; border-radius: 50%; background: currentColor; opacity: 0.55; }
    .ftp-footer-credit {
      text-align: center; padding: 0.8rem 1rem; font-family: 'JetBrains Mono', ui-monospace, monospace;
      font-size: 0.56rem; color: rgba(255,255,255,0.22); background: #050505;
    }
    .ftp-coming-soon-overlay { display: flex; align-items: center; justify-content: center; min-height: 300px; padding: 3rem; }
    .ftp-coming-soon-box {
      text-align: center; padding: 2.5rem 3rem; border: 1px solid rgba(212,175,55,0.15);
      border-radius: 8px; background: color-mix(in srgb, var(--ftp-shell-accent, #d4af37) 3%, transparent); max-width: 500px;
    }
    .ftp-coming-soon-box h2 {
      font-size: 1.1rem; color: var(--ftp-shell-accent, #d4af37); margin: 0 0 0.5rem; text-transform: uppercase;
      letter-spacing: 0.08em; font-weight: 500;
    }
    .ftp-coming-soon-box p { font-size: 0.85rem; color: rgba(255,255,255,0.4); margin: 0; line-height: 1.6; }
    @media (max-width: 780px) {
      .ftp-topbar { align-items: stretch; flex-direction: column; }
      .ftp-tb-center { order: 3; }
      .ftp-tb-nav, .ftp-tb-series span, .ftp-tb-home span { display: none; }
    }
  `;

  const homeIcon = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>';
  const listIcon = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>';

  function normalizePath(path) {
    return decodeURIComponent(path || '/').replace(/\/index\.html$/i, '/').replace(/\/+$/, '/') || '/';
  }

  function isActiveHref(href) {
    const current = normalizePath(window.location.pathname);
    const target = normalizePath(new URL(href, window.location.origin).pathname);
    return target === '/' ? current === '/' : current.startsWith(target);
  }

  function loadAsset(tag, attrs, existsSelector) {
    if (document.querySelector(existsSelector)) return;
    const el = document.createElement(tag);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    document.head.appendChild(el);
  }

  function setReaderMode(mode) {
    document.documentElement.dataset.readerMode = mode;
    localStorage.setItem('ftp-reader-mode', mode);
    document.querySelectorAll('[data-reader-mode]').forEach(el => {
      if (el.classList.contains('ftp-layer-tab')) return;
      const modes = (el.getAttribute('data-reader-mode') || '').split(/\s+/);
      el.hidden = modes.length && !modes.includes(mode);
    });
    document.querySelectorAll('.layer-panel').forEach(panel => {
      panel.classList.toggle('active', panel.classList.contains(mode) || panel.getAttribute('data-layer') === mode);
    });
    document.dispatchEvent(new CustomEvent('ftp-layer-change', { detail: { layer: mode } }));
  }

  function buildTopbar() {
    const bar = document.createElement('header');
    bar.className = 'ftp-topbar';
    bar.setAttribute('data-site-shell', 'top');

    const prev = cfg.prevHref ? `<a href="${cfg.prevHref}" class="ftp-tb-nav active">Prev</a>` : '<span class="ftp-tb-nav">Prev</span>';
    const next = cfg.nextHref ? `<a href="${cfg.nextHref}" class="ftp-tb-nav active">Next</a>` : '<span class="ftp-tb-nav">Next</span>';
    const storedMode = localStorage.getItem('ftp-reader-mode');
    const activeMode = LAYERS.some(l => l.id === storedMode) ? storedMode : cfg.activeTab;
    const tabs = cfg.hideTabs ? '' : `<div class="ftp-layer-tabs">${LAYERS.map(l =>
      `<button class="ftp-layer-tab${l.id === activeMode ? ' active' : ''}" type="button" data-reader-mode="${l.id}" aria-pressed="${l.id === activeMode ? 'true' : 'false'}">${l.label}</button>`
    ).join('')}</div>`;

    bar.innerHTML = `
      <a href="/" class="ftp-tb-home">${homeIcon}<span>Faith Through Physics</span></a>
      <div class="ftp-tb-center">${prev}${tabs}${next}</div>
      <a href="${cfg.seriesHref}" class="ftp-tb-series">${listIcon}<span>Series</span></a>
    `;

    bar.addEventListener('click', (event) => {
      const btn = event.target.closest('.ftp-layer-tab');
      if (!btn) return;
      const mode = btn.getAttribute('data-reader-mode');
      bar.querySelectorAll('.ftp-layer-tab').forEach(tab => {
        const active = tab === btn;
        tab.classList.toggle('active', active);
        tab.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      setReaderMode(mode);
    });

    requestAnimationFrame(() => setReaderMode(activeMode));
    return bar;
  }

  function buildSubdomainStrip() {
    const nav = document.createElement('nav');
    nav.className = 'ftp-subdomain-strip';
    nav.setAttribute('data-site-shell', 'bottom');
    nav.setAttribute('aria-label', 'Faith Through Physics sections');
    const links = SUBDOMAINS.map(s => {
      const active = isActiveHref(s.href) ? ' active' : '';
      return `<a href="${s.href}" class="ftp-sub-link${active}"><span class="ftp-sub-dot"></span>${s.label}</a>`;
    }).join('');
    nav.innerHTML = `<div class="ftp-subdomain-inner">${links}</div>`;
    return nav;
  }

  function buildFooter() {
    const footer = document.createElement('div');
    footer.className = 'ftp-footer-credit';
    footer.setAttribute('data-site-shell', 'credit');
    footer.textContent = '(c) 2024-2026 David Lowe - Faith Through Physics';
    return footer;
  }

  function buildPlayer() {
    if (cfg.hidePlayer || document.querySelector('.tp-pill-player, .tp-pill-bar')) return null;

    loadAsset('link', { rel: 'stylesheet', href: '/components/tp-pill-player.css' }, 'link[href="/components/tp-pill-player.css"]');
    loadAsset('script', { src: '/components/tp-pill-player.js', defer: 'defer' }, 'script[src="/components/tp-pill-player.js"]');

    const player = document.createElement('div');
    player.className = 'tp-pill-bar';
    player.id = 'tpPillBar';
    if (cfg.audioSlug) player.setAttribute('data-audio-slug', cfg.audioSlug);
    if (cfg.audioApi) player.setAttribute('data-audio-api', cfg.audioApi);
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
    return player;
  }

  function processComingSoon() {
    document.querySelectorAll('.ftp-coming-soon').forEach(el => {
      const name = el.getAttribute('data-section-name') || 'This Section';
      el.innerHTML = `
        <div class="ftp-coming-soon-overlay">
          <div class="ftp-coming-soon-box">
            <h2>Coming Soon</h2>
            <p>${name} is currently being built.<br>Check back soon or subscribe for updates.</p>
          </div>
        </div>
      `;
    });
  }

  function init() {
    if (cfg.shellAccent) document.documentElement.style.setProperty('--ftp-shell-accent', cfg.shellAccent);

    const style = document.createElement('style');
    style.textContent = STYLES;
    document.head.appendChild(style);

    document.body.insertBefore(buildTopbar(), document.body.firstChild);
    const player = buildPlayer();
    if (player) document.body.insertBefore(player, document.querySelector('[data-site-shell="top"]')?.nextSibling || document.body.firstChild);
    document.body.appendChild(buildSubdomainStrip());
    document.body.appendChild(buildFooter());
    processComingSoon();

    if (window.TPPillPlayer?.initAll) window.TPPillPlayer.initAll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
