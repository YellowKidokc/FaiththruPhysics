(function (global) {
  'use strict';

  const DOMAIN_COLORS = [
    '#d4af37', '#4a9eff', '#a855f7', '#22c55e', '#f97316', '#2dd4bf', '#ef4444',
    '#8b7fc2', '#eab308', '#ec4899',
  ];

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function stat(num, label, gold, hint) {
    const wrap = el('div', 'tp-snapshot-stat');
    const n = el('div', gold ? 'num gold' : 'num', String(num));
    const l = el('div', 'lbl', label);
    wrap.appendChild(n);
    wrap.appendChild(l);
    if (hint) {
      wrap.appendChild(el('div', 'tp-snapshot-hint', hint));
    }
    return wrap;
  }

  function renderSnapshot(root, data) {
    if (!root || !data) return;
    root.innerHTML = '';
    const card = el('div', 'tp-snapshot-card');

    const label = el('span', 'tp-snapshot-label', 'Framework Snapshot');
    card.appendChild(label);
    card.appendChild(el('h2', 'tp-snapshot-title', data.title || data.series || 'Series'));
    if (data.core_question) {
      card.appendChild(el('p', 'tp-snapshot-question', data.core_question));
    }

    const metrics = el('div', 'tp-snapshot-metrics');
    if (Array.isArray(data.boxes) && data.boxes.length) {
      if (data.boxes.length === 4) metrics.classList.add('four-up');
      data.boxes.forEach((box) => {
        metrics.appendChild(stat(box.value, box.label, !!box.gold, box.hint));
      });
    } else {
      const ax = data.axioms || {};
      const axLabel = ax.label || 'Axioms';
      metrics.appendChild(stat(
        `${ax.tested ?? '—'}/${ax.total ?? 55}`,
        axLabel,
        true
      ));
      const laws = data.laws || {};
      metrics.appendChild(stat(
        `${laws.tested ?? (laws.active || []).length}/${laws.total || 10}`,
        'Laws',
        false
      ));
      const bridges = data.isomorphisms || {};
      metrics.appendChild(stat(
        `${bridges.built ?? bridges.count ?? '—'}/${bridges.total ?? 47}`,
        'Bridges',
        false
      ));
      const claims = data.claims || {};
      const solid = claims.solid ?? claims.load_bearing ?? '—';
      const push = claims.push ?? claims.contested ?? '—';
      const open = claims.open ?? '—';
      metrics.appendChild(stat(
        `${solid} / ${push} / ${open}`,
        'Claims',
        false,
        'solid · push · open'
      ));
    }
    card.appendChild(metrics);

    if (data.domains && Object.keys(data.domains).length) {
      const bar = el('div', 'tp-snapshot-domains');
      const tags = el('div', 'tp-snapshot-domain-tags');
      const entries = Object.entries(data.domains).sort((a, b) => b[1] - a[1]);
      entries.forEach(([name, pct], i) => {
        const color = DOMAIN_COLORS[i % DOMAIN_COLORS.length];
        const seg = el('div', 'seg');
        seg.style.flex = String(pct);
        seg.style.background = color;
        bar.appendChild(seg);
        const tag = el('span');
        const dot = el('i');
        dot.style.background = color;
        tag.appendChild(dot);
        tag.appendChild(document.createTextNode(`${name} ${pct}%`));
        tags.appendChild(tag);
      });
      card.appendChild(bar);
      card.appendChild(tags);
    }

    if (data.one_line) {
      card.appendChild(el('p', 'tp-snapshot-oneline', data.one_line));
    }
    if (data.arc?.length) {
      card.appendChild(el('p', 'tp-snapshot-arc', 'Arc: ' + data.arc.join(' → ')));
    }

    root.appendChild(card);
  }

  async function autoLoad() {
    document.querySelectorAll('[data-series-snapshot]').forEach(async (root) => {
      const series = root.dataset.seriesSnapshot;
      if (!series) return;
      const paths = [
        `/data-viz/snapshot-${series}.json`,
        `../data-viz/snapshot-${series}.json`,
        `/data-viz/snapshot.json`,
      ];
      for (const path of paths) {
        try {
          const res = await fetch(path);
          if (!res.ok) continue;
          renderSnapshot(root, await res.json());
          return;
        } catch (e) { /* try next */ }
      }
    });
  }

  global.renderSeriesSnapshot = renderSnapshot;
  global.loadSeriesSnapshot = renderSnapshot;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoLoad);
  } else {
    autoLoad();
  }
})(window);
