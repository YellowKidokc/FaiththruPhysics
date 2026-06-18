/**
 * Faith Through Physics — Site Shell Injector v1.0
 * 
 * Drop this one script tag into any HTML page:
 *   <script src="/components/site-shell.js"></script>
 * 
 * It injects:
 *   1. Top navigation bar with home link, layer tabs, prev/next, series link
 *   2. Bottom subdomain strip with links to all major sections
 *   3. Footer credit line
 * 
 * Configuration via data attributes on the script tag:
 *   data-active-tab="standard"   (default reading level)
 *   data-prev-href="/prev-page"  (previous article link)
 *   data-next-href="/next-page"  (next article link)
 *   data-series-href="/series"   (series index link)
 *   data-hide-tabs="true"        (hide reading level tabs for non-article pages)
 */
(function () {
  'use strict';

  // --- Configuration ---
  const script = document.currentScript;
  const cfg = {
    activeTab: script?.getAttribute('data-active-tab') || 'standard',
    prevHref: script?.getAttribute('data-prev-href') || '',
    nextHref: script?.getAttribute('data-next-href') || '',
    seriesHref: script?.getAttribute('data-series-href') || '#',
    hideTabs: script?.getAttribute('data-hide-tabs') === 'true',
  };

  const SUBDOMAINS = [
    { label: 'Home', href: '/' },
    { label: 'Rigor', href: '/rigor/' },
    { label: 'Lexicon', href: '/glossary/' },
    { label: 'Equation', href: '/equation/' },
    { label: 'Master Equation', href: '/master-equation/' },
    { label: 'Proof Explorer', href: '/proof-explorer/' },
    { label: 'Isomorphism', href: '/isomorphism/' },
    { label: 'GTQ', href: '/genesis-to-quantum/' },
    { label: 'MDA', href: '/mda/' },
    { label: 'Moral Decline', href: '/moral-decline/' },
    { label: 'Media', href: '/media/' },
    { label: 'Audio', href: '/audio/' },
    { label: 'Podcast', href: '/podcast/' },
  ];

  const LAYERS = [
    { id: 'easy', label: 'Easy', color: 'rgba(74,222,128,0.8)' },
    { id: 'standard', label: 'Standard', color: 'rgba(245,158,11,0.9)' },
    { id: 'academic', label: 'Academic', color: 'rgba(91,155,213,0.9)' },
    { id: 'proof', label: 'Proof', color: 'rgba(212,175,55,0.9)' },
  ];

  // --- Styles ---
  const STYLES = `
    .ftp-topbar {
      position: sticky; top: 0; z-index: 1000;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 1rem; height: 42px;
      background: #0a0a0f; border-bottom: 1px solid rgba(255,255,255,0.06);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 0.72rem; color: rgba(255,255,255,0.55);
    }
    .ftp-topbar a { color: rgba(255,255,255,0.55); text-decoration: none; transition: color 0.15s; }
    .ftp-topbar a:hover { color: #d4af37; }
    .ftp-tb-home { display: flex; align-items: center; gap: 0.4rem; }
    .ftp-tb-center { display: flex; align-items: center; gap: 0.75rem; }
    .ftp-tb-nav { cursor: pointer; opacity: 0.4; transition: opacity 0.15s; }
    .ftp-tb-nav.active { opacity: 1; cursor: pointer; }
    .ftp-tb-nav.active:hover { color: #d4af37; }
    .ftp-layer-tabs { display: flex; gap: 2px; }
    .ftp-layer-tab {
      background: none; border: none; color: rgba(255,255,255,0.35);
      padding: 0.3rem 0.6rem; font-size: 0.65rem; font-family: inherit;
      cursor: pointer; border-radius: 3px; transition: all 0.15s;
      text-transform: uppercase; letter-spacing: 0.06em;
    }
    .ftp-layer-tab:hover { color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.04); }
    .ftp-layer-tab.active { color: #fff; background: rgba(212,175,55,0.15); }
    .ftp-tb-series { display: flex; align-items: center; gap: 0.35rem; }

    .ftp-subdomain-strip {
      border-top: 1px solid rgba(255,255,255,0.06);
      background: #0a0a0f; padding: 0.6rem 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .ftp-subdomain-inner {
      display: flex; justify-content: center; flex-wrap: wrap;
      gap: 0.25rem 1rem; max-width: 900px; margin: 0 auto;
    }
    .ftp-sub-link {
      display: flex; align-items: center; gap: 0.35rem;
      color: rgba(255,255,255,0.35); text-decoration: none;
      font-size: 0.65rem; letter-spacing: 0.04em;
      text-transform: uppercase; transition: color 0.15s;
    }
    .ftp-sub-link:hover { color: #d4af37; }
    .ftp-sub-dot {
      width: 4px; height: 4px; border-radius: 50%;
      background: rgba(212,175,55,0.3);
    }
    .ftp-footer-credit {
      text-align: center; padding: 0.8rem 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 0.6rem; color: rgba(255,255,255,0.2);
      background: #0a0a0f;
      border-top: 1px solid rgba(255,255,255,0.03);
    }

    .ftp-coming-soon-overlay {
      display: flex; align-items: center; justify-content: center;
      min-height: 300px; padding: 3rem;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .ftp-coming-soon-box {
      text-align: center; padding: 2.5rem 3rem;
      border: 1px solid rgba(212,175,55,0.15);
      border-radius: 8px; background: rgba(212,175,55,0.03);
      max-width: 500px;
    }
    .ftp-coming-soon-box h2 {
      font-size: 1.1rem; color: #d4af37; margin: 0 0 0.5rem 0;
      text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500;
    }
    .ftp-coming-soon-box p {
      font-size: 0.85rem; color: rgba(255,255,255,0.4); margin: 0;
      line-height: 1.6;
    }

    @media (max-width: 640px) {
      .ftp-topbar { padding: 0 0.5rem; }
      .ftp-layer-tab { padding: 0.25rem 0.4rem; font-size: 0.58rem; }
      .ftp-tb-series, .ftp-tb-home span { display: none; }
    }
  `;

  // --- SVG Icons ---
  const homeIcon = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>';
  const listIcon = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>';

  // --- Build Header ---
  function buildTopbar() {
    const bar = document.createElement('header');
    bar.className = 'ftp-topbar';

    // Left: Home
    const homeLink = `<a href="/" class="ftp-tb-home">${homeIcon}<span>Home</span></a>`;

    // Center: Nav + Tabs
    const prevClass = cfg.prevHref ? 'ftp-tb-nav active' : 'ftp-tb-nav';
    const nextClass = cfg.nextHref ? 'ftp-tb-nav active' : 'ftp-tb-nav';
    const prevLink = cfg.prevHref
      ? `<a href="${cfg.prevHref}" class="${prevClass}">← Prev</a>`
      : `<span class="${prevClass}">← Prev</span>`;
    const nextLink = cfg.nextHref
      ? `<a href="${cfg.nextHref}" class="${nextClass}">Next →</a>`
      : `<span class="${nextClass}">Next →</span>`;

    let tabsHTML = '';
    if (!cfg.hideTabs) {
      const tabs = LAYERS.map(l =>
        `<button class="ftp-layer-tab${l.id === cfg.activeTab ? ' active' : ''}" data-layer="${l.id}">${l.label}</button>`
      ).join('');
      tabsHTML = `<div class="ftp-layer-tabs">${tabs}</div>`;
    }

    const center = `<div class="ftp-tb-center">${prevLink}${tabsHTML}${nextLink}</div>`;

    // Right: Series
    const series = `<a href="${cfg.seriesHref}" class="ftp-tb-series">${listIcon}<span>Series</span></a>`;

    bar.innerHTML = `<div>${homeLink}</div>${center}<div>${series}</div>`;

    // Tab click handler: toggles .layer-panel visibility and dispatches event
    if (!cfg.hideTabs) {
      bar.addEventListener('click', (e) => {
        const btn = e.target.closest('.ftp-layer-tab');
        if (!btn) return;
        const layer = btn.getAttribute('data-layer');
        bar.querySelectorAll('.ftp-layer-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Toggle layer panels in the page
        document.querySelectorAll('.layer-panel').forEach(p => {
          p.classList.toggle('active', p.classList.contains(layer) || p.getAttribute('data-layer') === layer);
        });

        // Dispatch custom event for pages that want to handle it differently
        document.dispatchEvent(new CustomEvent('ftp-layer-change', { detail: { layer } }));
      });
    }

    return bar;
  }

  // --- Build Subdomain Footer ---
  function buildSubdomainStrip() {
    const nav = document.createElement('nav');
    nav.className = 'ftp-subdomain-strip';
    const links = SUBDOMAINS.map(s =>
      `<a href="${s.href}" class="ftp-sub-link"><span class="ftp-sub-dot"></span>${s.label}</a>`
    ).join('');
    nav.innerHTML = `<div class="ftp-subdomain-inner">${links}</div>`;
    return nav;
  }

  // --- Build Footer Credit ---
  function buildFooter() {
    const footer = document.createElement('div');
    footer.className = 'ftp-footer-credit';
    footer.textContent = '© 2024–2026 David Lowe · Faith Through Physics';
    return footer;
  }

  // --- "Coming Soon" helper ---
  // Usage: add class="ftp-coming-soon" to any section container
  // Optional: data-section-name="Proof Explorer" for custom text
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

  // --- Inject ---
  function init() {
    // Add styles
    const style = document.createElement('style');
    style.textContent = STYLES;
    document.head.appendChild(style);

    // Inject topbar at beginning of body
    const topbar = buildTopbar();
    document.body.insertBefore(topbar, document.body.firstChild);

    // Inject subdomain strip and footer at end of body
    document.body.appendChild(buildSubdomainStrip());
    document.body.appendChild(buildFooter());

    // Process any coming-soon sections
    processComingSoon();
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
