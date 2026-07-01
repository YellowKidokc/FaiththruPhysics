(function (global) {
  'use strict';

  function toggleVerification() {
    const toggle = document.getElementById('verificationToggle');
    const body = document.getElementById('verificationBody');
    if (!toggle || !body) return;
    toggle.classList.toggle('open');
    body.classList.toggle('open');
  }

  function loadVerification(data) {
    if (!data) return;
    const axiomCount = data.axioms?.tested || 0;
    const axiomTotal = data.axioms?.total || 188;
    const axiomPct = Math.round((axiomCount / axiomTotal) * 100);
    const set = (id, text, cls) => {
      const el = document.getElementById(id);
      if (!el) return;
      if (text != null) el.textContent = text;
      if (cls) el.className = cls;
    };
    set('vb-axioms', `${axiomCount}/${axiomTotal} axioms`, `v-badge ${axiomPct > 50 ? 'pass' : axiomPct > 20 ? 'partial' : 'info'}`);
    const lawCount = data.laws?.active?.length || 0;
    set('vb-laws', `${lawCount}/10 laws`, `v-badge ${lawCount >= 3 ? 'pass' : 'info'}`);
    const chiNorm = data.chi?.normalized || 0;
    set('vb-chi', `χ ${chiNorm.toFixed(1)}`, `v-badge ${chiNorm >= 7 ? 'pass' : chiNorm >= 4 ? 'partial' : 'fail'}`);
    const isoCount = data.isomorphisms?.count || 0;
    set('vb-iso', `${isoCount} bridges`, 'v-badge info');
    set('vc-axiom-count', `${axiomCount}/${axiomTotal}`);
    set('vc-axiom-pct', `${axiomPct}%`);
    const meter = document.getElementById('vc-axiom-meter');
    if (meter) {
      meter.style.width = `${axiomPct}%`;
      meter.className = `v-meter-fill ${axiomPct > 50 ? 'high' : axiomPct > 20 ? 'mid' : 'low'}`;
    }
    if (data.laws?.active) {
      data.laws.active.forEach(lawNum => {
        document.querySelector(`.v-law-tag[data-law="${lawNum}"]`)?.classList.add('active');
      });
    }
    set('vc-chi-raw', data.chi?.raw ?? '—');
    set('vc-chi-norm', `${chiNorm.toFixed(1)}/10`);
    set('vc-fruits', `${data.fruits?.score ?? '—'}/9`);
    const chiMeter = document.getElementById('vc-chi-meter');
    if (chiMeter) {
      chiMeter.style.width = `${chiNorm * 10}%`;
      chiMeter.className = `v-meter-fill ${chiNorm >= 7 ? 'high' : chiNorm >= 4 ? 'mid' : 'low'}`;
    }
    set('vc-iso-count', isoCount);
    set('vc-physics', data.isomorphisms?.physics_processes ?? '—');
    set('vc-trinity', data.isomorphisms?.trinity_mappings ?? '—');
    set('vc-meq-vars', `${data.isomorphisms?.meq_variables ?? '—'}/10`);
    set('vc-claims', data.claims?.total ?? '—');
    set('vc-load-bearing', data.claims?.load_bearing ?? '—');
    set('vc-kill', data.claims?.kill_conditions ?? '—');
    set('vc-contradictions', data.claims?.contradictions ?? '0');
    if (data.domains) {
      const container = document.getElementById('vc-domains');
      if (container) {
        container.innerHTML = '';
        Object.entries(data.domains).sort((a, b) => b[1] - a[1]).forEach(([name, pct]) => {
          const row = document.createElement('div');
          row.className = 'v-row';
          row.innerHTML = `<span class="v-row-label">${name}</span><span class="v-row-value">${pct}%</span>`;
          container.appendChild(row);
        });
      }
    }
    if (data.slug) {
      const link = document.getElementById('vc-proof-link');
      if (link) link.href = `/proof-explorer/${data.slug}/`;
    }
    if (data.domains) {
      const chipRow = document.getElementById('vDomainChips');
      if (chipRow) {
        chipRow.innerHTML = '';
        const colors = {
          theology: '#d4af37', physics: '#7cc7ff', 'cross-domain': '#3bb39a',
          'cross_domain': '#3bb39a', evidence: '#7fc77f', mathematics: '#a78bfa',
          'information theory': '#f97316', epistemology: '#5b9bd5'
        };
        Object.entries(data.domains).sort((a, b) => b[1] - a[1]).forEach(([name, pct]) => {
          const chip = document.createElement('span');
          const on = pct > 0;
          chip.className = 'v-chip' + (on ? ' on' : '');
          const key = String(name).toLowerCase();
          if (on && colors[key]) chip.style.setProperty('--chip-color', colors[key]);
          chip.textContent = `${name} ${pct}%`;
          chipRow.appendChild(chip);
        });
      }
    }
  }

  function deriveSlugFromUrl() {
    // /revolution-of-truth/drv-01-the-architecture.html -> "revolution-of-truth/drv-01-the-architecture"
    const parts = location.pathname.split('/').filter(Boolean);
    if (parts.length < 2) return null;
    const file = parts[parts.length - 1].replace(/\.html?$/i, '');
    const series = parts[parts.length - 2];
    if (!file || !series || file.startsWith('_')) return null;
    return `${series}/${file}`;
  }

  async function autoLoad() {
    const bar = document.getElementById('verificationBar');
    if (!bar) return;
    const slug = bar.dataset.verificationSlug && bar.dataset.verificationSlug !== 'SERIES/filename'
      ? bar.dataset.verificationSlug
      : deriveSlugFromUrl();
    if (!slug) return;
    const safe = slug.replace(/\//g, '-');
    const paths = [
      `/data-viz/verification-${safe}.json`,
      `../data-viz/verification-${safe}.json`,
      `/data-viz/verification.json`
    ];
    for (const path of paths) {
      try {
        const res = await fetch(path);
        if (!res.ok) continue;
        loadVerification(await res.json());
        break;
      } catch (e) { /* try next */ }
    }
    const toggle = document.getElementById('verificationToggle');
    if (toggle && !toggle.dataset.bound) {
      toggle.dataset.bound = '1';
      toggle.addEventListener('click', toggleVerification);
    }
  }

  global.toggleVerification = toggleVerification;
  global.loadVerification = loadVerification;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoLoad);
  } else {
    autoLoad();
  }
})(window);
