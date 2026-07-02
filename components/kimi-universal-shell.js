/**
 * Faith thru Physics — Universal Shell Controller v1.0
 * ======================================================
 *
 * Powers all 4 permanent layers of the page shell from a JSON data block.
 *
 * USAGE:
 *   1. Include this script at the bottom of every page, after all shell markup.
 *   2. Provide a <script id="shell-data" type="application/json"> block with
 *      article-specific data (see INTEGRATION-GUIDE.md for schema).
 *   3. The script auto-initializes on DOMContentLoaded.
 *
 * LAYERS CONTROLLED:
 *   Layer 1 — Top Bar (domains, chi badge, reading levels, tools, search)
 *   Layer 2 — Expandable Panel (verification, proofs, MTL tabs)
 *   Layer 3 — Audio Dock (pill player + mini-player on scroll)
 *   Layer 4 — Footer (light nav, audit, subdomain grids, series nav, bottom bar)
 *
 * EXTERNAL CONTRACTS:
 *   - Dispatches 'ftp-layer-change' CustomEvent when reading level changes
 *     (MTL worker client listens for this to re-render translations).
 *   - Expects markup with specific IDs and class names (see shell.html).
 *
 * POF 2828 | faiththruphysics.com
 */
(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════════

  var CONFIG = {
    dataId: 'shell-data',
    chiTotal: 10,
    fruitsTotal: 9,
    axiomTotal: 188,
    meqTotal: 10,
    colors: {
      deep: '#4a9eff',
      read: '#d4af37',
      debate: '#a855f7',
      critique: '#2dd4bf'
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // STATE
  // ═══════════════════════════════════════════════════════════════════════════

  var data = null;
  var audio = null;
  var activeAudioKey = null;
  var audioMuted = false;

  // ═══════════════════════════════════════════════════════════════════════════
  // UTILITIES
  // ═══════════════════════════════════════════════════════════════════════════

  function $(sel) { return document.querySelector(sel); }
  function $$(sel) { return document.querySelectorAll(sel); }

  function fmtTime(s) {
    if (!s || isNaN(s)) return '0:00';
    var m = Math.floor(s / 60), sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  function loadData() {
    var el = document.getElementById(CONFIG.dataId);
    if (!el) { console.warn('[shell] No #' + CONFIG.dataId + ' block found'); return false; }
    try { data = JSON.parse(el.textContent); return true; }
    catch(e) { console.error('[shell] Invalid JSON in ' + CONFIG.dataId + ':', e); return false; }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // LAYER 1: TOP BAR
  // ═══════════════════════════════════════════════════════════════════════════

  function renderDomains() {
    if (!data || !data.domains) return;
    var container = document.getElementById('ftpDomains');
    if (!container) return;
    // Show top 4 domains by percentage
    var topDomains = data.domains.slice().sort(function(a,b){ return b.pct - a.pct; }).slice(0, 4);
    container.innerHTML = topDomains.map(function(d) {
      var key = d.key || d.name.toLowerCase().replace(/[^a-z]/g, '');
      return '<button class="ftp-domain-pill" data-domain="' + key + '" title="' + d.name + ' (' + d.pct + '%)">' +
        '<span class="ddot" style="background:' + d.color + '"></span>' +
        '<span>' + d.name + '</span></button>';
    }).join('');
  }

  function renderChiBadge() {
    if (!data || !data.verification || !data.verification.chi) return;
    var chi = data.verification.chi.normalized || 0;
    var el = document.getElementById('ftpChiValue');
    if (el) el.textContent = '\u03C7 ' + chi.toFixed(1);
  }

  function initReadingLevels() {
    $$('.ftp-level').forEach(function(btn) {
      btn.addEventListener('click', function() {
        $$('.ftp-level').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        try { localStorage.setItem('ftp-reader-mode', btn.dataset.level); } catch(_){}
        document.dispatchEvent(new CustomEvent('ftp-layer-change', {
          detail: { level: btn.dataset.level }
        }));
      });
    });
    // Restore persisted level
    try {
      var saved = localStorage.getItem('ftp-reader-mode');
      if (saved) {
        var btn = $('.ftp-level[data-level="' + saved + '"]');
        if (btn) {
          $$('.ftp-level').forEach(function(b){ b.classList.remove('active'); });
          btn.classList.add('active');
        }
      }
    } catch(_){}
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // LAYER 2: EXPANDABLE PANEL
  // ═══════════════════════════════════════════════════════════════════════════

  function togglePanel() {
    var panel = document.getElementById('ftpPanel');
    var toggle = document.getElementById('ftpPanelToggle');
    if (!panel || !toggle) return;
    var isOpen = panel.classList.toggle('open');
    toggle.classList.toggle('open', isOpen);
    // Update toggle text
    var chevron = toggle.querySelector('.fa-chevron-down, .fa-chevron-up');
    if (chevron) chevron.className = isOpen ? 'fas fa-chevron-up' : 'fas fa-chevron-down';
  }

  function switchTab(tabName) {
    $$('.ftp-panel-tab').forEach(function(t) {
      t.classList.toggle('active', t.dataset.tab === tabName);
    });
    $$('.ftp-panel-section').forEach(function(s) {
      s.classList.toggle('active', s.id === 'tab-' + tabName);
    });
  }

  function renderVerificationTab() {
    if (!data || !data.verification) return;
    var v = data.verification;

    // Axioms
    var axiomCount = v.axioms ? v.axioms.tested : 0;
    var axiomTotal = v.axioms ? v.axioms.total : CONFIG.axiomTotal;
    var axiomPct = Math.round((axiomCount / axiomTotal) * 100);
    var axiomCountEl = document.getElementById('v-axiom-count');
    if (axiomCountEl) axiomCountEl.textContent = axiomCount + '/' + axiomTotal;
    var axiomPctEl = document.getElementById('v-axiom-pct');
    if (axiomPctEl) axiomPctEl.textContent = axiomPct + '%';
    var axiomMeter = document.getElementById('v-axiom-meter');
    if (axiomMeter) {
      axiomMeter.style.width = axiomPct + '%';
      axiomMeter.className = 'ftp-meter-fill ' + (axiomPct > 50 ? 'high' : axiomPct > 20 ? 'mid' : 'low');
    }

    // Laws
    if (v.laws && v.laws.active) {
      v.laws.active.forEach(function(lawNum) {
        var tag = document.querySelector('.ftp-law-tag[data-law="' + lawNum + '"]');
        if (tag) tag.classList.add('active');
      });
    }

    // Chi
    var chiNorm = v.chi ? (v.chi.normalized || 0) : 0;
    var chiRawEl = document.getElementById('v-chi-raw');
    if (chiRawEl) chiRawEl.textContent = v.chi ? v.chi.raw : '\u2014';
    var chiNormEl = document.getElementById('v-chi-norm');
    if (chiNormEl) chiNormEl.textContent = chiNorm.toFixed(1) + '/' + CONFIG.chiTotal;
    var fruitsEl = document.getElementById('v-fruits');
    if (fruitsEl) fruitsEl.textContent = (v.fruits ? v.fruits.score : '\u2014') + '/' + CONFIG.fruitsTotal;
    var chiMeter = document.getElementById('v-chi-meter');
    if (chiMeter) {
      chiMeter.style.width = (chiNorm * (100 / CONFIG.chiTotal)) + '%';
      chiMeter.className = 'ftp-meter-fill ' + (chiNorm >= 7 ? 'high' : chiNorm >= 4 ? 'mid' : 'low');
    }

    // Isomorphisms
    var iso = v.isomorphisms || {};
    var isoCountEl = document.getElementById('v-iso-count');
    if (isoCountEl) isoCountEl.textContent = iso.count || '\u2014';
    var physicsEl = document.getElementById('v-physics');
    if (physicsEl) physicsEl.textContent = iso.physics_processes || '\u2014';
    var trinityEl = document.getElementById('v-trinity');
    if (trinityEl) trinityEl.textContent = iso.trinity_mappings || '\u2014';
    var meqEl = document.getElementById('v-meq');
    if (meqEl) meqEl.textContent = (iso.meq_variables || '\u2014') + '/' + CONFIG.meqTotal;

    // Claims
    var claims = v.claims || {};
    var claimsEl = document.getElementById('v-claims');
    if (claimsEl) claimsEl.textContent = claims.total || '\u2014';
    var loadEl = document.getElementById('v-load-bearing');
    if (loadEl) loadEl.textContent = claims.load_bearing || '\u2014';
    var killEl = document.getElementById('v-kill');
    if (killEl) killEl.textContent = claims.kill_conditions || '\u2014';
    var contradictionsEl = document.getElementById('v-contradictions');
    if (contradictionsEl) contradictionsEl.textContent = claims.contradictions || '0';

    // Domains
    if (data.domains) {
      var domContainer = document.getElementById('v-domains');
      if (domContainer) {
        domContainer.innerHTML = data.domains.slice().sort(function(a,b){ return b.pct - a.pct; }).map(function(d) {
          return '<div class="ftp-vrow"><span class="ftp-vrow-label">' + d.name + '</span>' +
            '<span class="ftp-vrow-value">' + d.pct + '%</span></div>';
        }).join('');
      }
    }

    // Panel badge
    var proofs = v.proofs || [];
    var verifiedCount = proofs.filter(function(p){ return p.status === 'verified'; }).length;
    var badge = document.getElementById('ftpPanelBadge');
    if (badge) {
      badge.textContent = verifiedCount + ' of ' + proofs.length + ' verified';
      badge.className = 'p-badge ' + (verifiedCount === proofs.length && proofs.length > 0 ? 'ok' : proofs.length > 0 ? 'warn' : '');
    }
  }

  function renderProofsTab() {
    if (!data || !data.verification || !data.verification.proofs) return;
    var container = document.getElementById('v-proof-list');
    if (!container) return;

    container.innerHTML = data.verification.proofs.map(function(p) {
      var statusColor = p.status === 'verified' ? 'var(--teal)' : p.status === 'partial' ? 'var(--gold)' : 'var(--text-muted)';
      var statusIcon = p.status === 'verified' ? 'fa-check-circle' : p.status === 'partial' ? 'fa-adjust' : 'fa-circle';
      var statusLabel = p.status === 'verified' ? 'Verified' : p.status === 'partial' ? 'Partial' : 'Pending';
      return '<div class="ftp-proof-item" data-proof="' + p.id + '">' +
        '<div class="ftp-proof-header" onclick="window.ftp.toggleProof(this)">' +
        '<span><i class="fas ' + statusIcon + '" style="color:' + statusColor + ';margin-right:.5rem"></i>' +
        p.title + '<span style="color:' + statusColor + ';margin-left:.5rem;font-size:.65rem;text-transform:uppercase;letter-spacing:.05em">' + statusLabel + '</span></span>' +
        '<i class="fas fa-chevron-right" style="font-size:.55rem;color:var(--gold)"></i></div>' +
        '<div class="ftp-proof-body">' +
        '<p>' + p.summary + '</p>' +
        (p.url ? '<a href="' + p.url + '" style="display:inline-flex;align-items:center;gap:.4rem;margin-top:.5rem;font-size:.78rem;color:var(--blue)"><i class="fas fa-external-link-alt" style="font-size:.6rem"></i> View in Proof Explorer</a>' : '') +
        '</div></div>';
    }).join('');
  }

  function toggleProof(header) {
    var item = header.closest('.ftp-proof-item');
    if (item) item.classList.toggle('open');
  }

  function renderMTLTab() {
    if (!data || !data.mtl) return;
    var container = document.getElementById('v-mtl-list');
    if (!container) return;

    container.innerHTML = data.mtl.map(function(m) {
      var eqHtml = m.latex ? '<div class="ftp-mtl-eq">\\[' + m.latex + '\\]</div>' : '';
      var namedHtml = m.named ? '<div class="ftp-mtl-named">' + escapeHtml(m.named) + '</div>' : '';
      var plainHtml = m.plain ? '<div class="ftp-mtl-plain">' + escapeHtml(m.plain) + '</div>' : '';
      var featureHtml = m.feature ? '<div class="ftp-mtl-feature"><i class="fas fa-lightbulb"></i> ' + escapeHtml(m.feature) + '</div>' : '';
      return '<div class="ftp-mtl-callout">' + eqHtml + namedHtml + plainHtml + featureHtml + '</div>';
    }).join('');

    // Trigger MathJax if available
    if (typeof MathJax !== 'undefined' && MathJax.startup && MathJax.startup.promise) {
      MathJax.startup.promise.then(function() { MathJax.typesetPromise([container]); });
    }
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // LAYER 3: AUDIO DOCK
  // ═══════════════════════════════════════════════════════════════════════════

  function initAudio() {
    var dock = document.getElementById('ftpAudioDock');
    if (!dock) return;

    audio = new Audio();
    audio.preload = 'metadata';

    var pills = dock.querySelectorAll('.ftp-dock-pill');
    var body = document.getElementById('ftpDockBody');
    var empty = document.getElementById('ftpDockEmpty');

    pills.forEach(function(p) { if (!p.dataset.url) p.classList.add('unavailable'); });

    pills.forEach(function(p) {
      p.addEventListener('click', function() {
        var key = p.dataset.src;
        var url = p.dataset.url;
        if (!url) return;
        if (key === activeAudioKey) {
          if (audio.paused) audio.play(); else audio.pause();
          return;
        }
        audio.pause();
        audio.src = url;
        var speedEl = document.getElementById('ftpDockSpeed');
        audio.playbackRate = speedEl ? parseFloat(speedEl.value) || 1 : 1;
        activeAudioKey = key;
        pills.forEach(function(q) { q.classList.remove('active'); });
        p.classList.add('active');
        var fill = document.getElementById('ftpDockFill');
        if (fill) fill.style.background = CONFIG.colors[key] || CONFIG.colors.read;
        if (body) body.classList.remove('hidden');
        if (empty) empty.classList.remove('visible');
        updateMiniLabel();
        audio.play();
      });
    });

    var firstAvail = dock.querySelector('.ftp-dock-pill[data-url]');
    if (firstAvail) {
      activeAudioKey = firstAvail.dataset.src;
      audio.src = firstAvail.dataset.url;
      var speedEl = document.getElementById('ftpDockSpeed');
      audio.playbackRate = speedEl ? parseFloat(speedEl.value) || 1 : 1;
      firstAvail.classList.add('active');
      var fill = document.getElementById('ftpDockFill');
      if (fill) fill.style.background = CONFIG.colors[activeAudioKey] || CONFIG.colors.read;
      updateMiniLabel();
    } else {
      if (body) body.classList.add('hidden');
      if (empty) empty.classList.add('visible');
    }

    audio.addEventListener('play', function() { setAudioIcons(false); });
    audio.addEventListener('pause', function() { setAudioIcons(true); });
    audio.addEventListener('ended', function() {
      setAudioIcons(true);
      var fill = document.getElementById('ftpDockFill');
      if (fill) fill.style.width = '0%';
      var curEl = document.getElementById('ftpDockCurrent');
      if (curEl) curEl.textContent = '0:00';
    });
    audio.addEventListener('timeupdate', function() {
      if (!audio.duration) return;
      var fill = document.getElementById('ftpDockFill');
      if (fill) fill.style.width = (audio.currentTime / audio.duration * 100) + '%';
      var curEl = document.getElementById('ftpDockCurrent');
      if (curEl) curEl.textContent = fmtTime(audio.currentTime);
    });
    audio.addEventListener('loadedmetadata', function() {
      var durEl = document.getElementById('ftpDockDuration');
      if (durEl) durEl.textContent = fmtTime(audio.duration);
    });

    // Mini-player via IntersectionObserver
    var mini = document.getElementById('ftpDockMini');
    if (dock && mini) {
      var observer = new IntersectionObserver(function(entries) {
        var shouldShow = !entries[0].isIntersecting && !!audio.src;
        mini.classList.toggle('visible', shouldShow);
        mini.setAttribute('aria-hidden', shouldShow ? 'false' : 'true');
      }, { threshold: 0 });
      observer.observe(dock);
    }
  }

  function setAudioIcons(paused) {
    var iconClass = paused ? 'fas fa-play' : 'fas fa-pause';
    var iconEl = document.getElementById('ftpDockPlayIcon');
    var miniIcon = document.getElementById('ftpMiniIcon');
    var playBtn = document.getElementById('ftpDockPlay');
    if (iconEl) iconEl.className = iconClass;
    if (miniIcon) miniIcon.className = iconClass;
    if (playBtn) playBtn.classList.toggle('playing', !paused);
  }

  function updateMiniLabel() {
    var pill = document.querySelector('.ftp-dock-pill.active');
    var label = document.getElementById('ftpMiniLabel');
    if (label) label.textContent = pill ? pill.textContent.trim() : 'Audio';
  }

  function audioToggle() {
    if (!audio || !audio.src) return;
    if (audio.paused) audio.play(); else audio.pause();
  }

  function audioSeek(e) {
    if (!audio || !audio.duration) return;
    var track = document.getElementById('ftpDockTrack');
    if (!track) return;
    var rect = track.getBoundingClientRect();
    var p = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    audio.currentTime = p * audio.duration;
  }

  function audioMute() {
    audioMuted = !audioMuted;
    if (audio) audio.muted = audioMuted;
    var volBtn = document.getElementById('ftpDockVol');
    if (volBtn) volBtn.innerHTML = audioMuted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>';
  }

  function audioSetSpeed() {
    var speedEl = document.getElementById('ftpDockSpeed');
    if (speedEl && audio) audio.playbackRate = parseFloat(speedEl.value) || 1;
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // LAYER 4: FOOTER
  // ═══════════════════════════════════════════════════════════════════════════

  function renderFooter() {
    if (!data || !data.page) return;
    var p = data.page;

    // Prev/Next navigation
    var prevLink = document.getElementById('ftpPrevLink');
    var prevTitle = document.getElementById('ftpPrevTitle');
    if (prevLink) {
      if (p.prev && p.prev.url) {
        prevLink.href = p.prev.url;
        if (prevTitle) prevTitle.textContent = p.prev.title || 'Previous';
        prevLink.style.visibility = '';
      } else {
        prevLink.style.visibility = 'hidden';
      }
    }

    var nextLink = document.getElementById('ftpNextLink');
    var nextTitle = document.getElementById('ftpNextTitle');
    if (nextLink) {
      if (p.next && p.next.url) {
        nextLink.href = p.next.url;
        if (nextTitle) nextTitle.textContent = p.next.title || 'Next';
        nextLink.style.visibility = '';
      } else {
        nextLink.style.visibility = 'hidden';
      }
    }

    // Series home link
    var seriesHome = document.getElementById('ftpSeriesHome');
    if (seriesHome) {
      if (p.series_home) seriesHome.href = p.series_home;
      if (p.series_name) seriesHome.textContent = p.series_name + ' Home';
      else if (p.series) seriesHome.textContent = p.series + ' Series Home';
    }

    // Series strip active state
    if (p.series) {
      var seriesMap = {
        'MDA': '/moral-decline/',
        'GTQ': '/genesis-to-quantum/',
        'Convergence': '/Convergence_Series/',
        'Logos': '/Logos_Papers/',
        'OPS': '/one-page-stories/'
      };
      $$('.ftp-series-strip a').forEach(function(a) {
        a.classList.remove('active');
        var href = a.getAttribute('href');
        if (seriesMap[p.series] && href === seriesMap[p.series]) {
          a.classList.add('active');
        }
      });
    }

    // Audit content
    if (data.audit) {
      var rightEl = document.getElementById('ftpAuditRight');
      if (rightEl && data.audit.right && data.audit.right.length) {
        rightEl.innerHTML = data.audit.right.map(function(item){ return '<li>' + escapeHtml(item) + '</li>'; }).join('');
      }
      var overEl = document.getElementById('ftpAuditOver');
      if (overEl && data.audit.overstated && data.audit.overstated.length) {
        overEl.innerHTML = data.audit.overstated.map(function(item){ return '<li>' + escapeHtml(item) + '</li>'; }).join('');
      }
      var wrongEl = document.getElementById('ftpAuditWrong');
      if (wrongEl && data.audit.wrong && data.audit.wrong.length) {
        wrongEl.innerHTML = data.audit.wrong.map(function(item){ return '<li>' + escapeHtml(item) + '</li>'; }).join('');
      }
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // KEYBOARD SHORTCUTS
  // ═══════════════════════════════════════════════════════════════════════════

  function initKeyboard() {
    document.addEventListener('keydown', function(e) {
      // Ctrl/Cmd + K → Search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Dispatch search event — your search modal should listen for this
        document.dispatchEvent(new CustomEvent('ftp-search-open'));
      }
      // Space → Toggle audio (when not typing)
      if (e.key === ' ' && !e.target.matches('input, textarea, [contenteditable]')) {
        if (audio && audio.src) { e.preventDefault(); audioToggle(); }
      }
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PUBLIC API
  // ═══════════════════════════════════════════════════════════════════════════

  window.ftp = {
    // Panel
    togglePanel: togglePanel,
    switchTab: switchTab,
    // Proofs
    toggleProof: toggleProof,
    // Audio
    audioToggle: audioToggle,
    audioSeek: audioSeek,
    audioMute: audioMute,
    audioSetSpeed: audioSetSpeed,
    // Data access
    getData: function() { return data; },
    // Re-render (call after dynamic data changes)
    refresh: function() {
      loadData();
      renderDomains();
      renderChiBadge();
      renderVerificationTab();
      renderProofsTab();
      renderMTLTab();
      renderFooter();
    }
  };

  // ═══════════════════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════════════════════════════════════════

  function init() {
    var hasData = loadData();
    if (hasData && data) {
      renderDomains();
      renderChiBadge();
      renderVerificationTab();
      renderProofsTab();
      renderMTLTab();
      renderFooter();
    }
    initReadingLevels();
    initAudio();
    initKeyboard();
    console.log('[shell] Initialized' + (data && data.page ? ' for: ' + data.page.title : ''));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
