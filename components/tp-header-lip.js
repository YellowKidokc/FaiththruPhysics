(function () {
  'use strict';

  const SERIES_CARDS = [
    { href: '/genesis-to-quantum/', icon: 'fa-atom', title: 'Genesis to Quantum', sub: 'Physics & faith' },
    { href: '/moral-decline/', icon: 'fa-chart-line', title: 'Moral Decline of America', sub: 'Evidence & history' },
    { href: '/convergence-series/', icon: 'fa-compress-arrows-alt', title: 'Convergence', sub: 'Framework comparison' },
    { href: '/cross-domain/', icon: 'fa-project-diagram', title: 'Cross-Domain', sub: 'Theophysics intro' },
    { href: '/one-page-stories/', icon: 'fa-file-alt', title: 'One-Page Stories', sub: 'Short proofs' },
    { href: '/blue/', icon: 'fa-book', title: 'Logos Papers', sub: 'Formal essays' },
    { href: '/consciousness/', icon: 'fa-brain', title: 'Consciousness', sub: 'Mind & matter' },
    { href: '/proof-architecture/', icon: 'fa-shield-alt', title: 'Proof Architecture', sub: 'Claims & grades' },
    { href: '/revolution-of-truth/', icon: 'fa-scroll', title: 'Revolution of Truth', sub: 'De Revolutionibus' }
  ];

  function renderSeriesGrid(container) {
    if (!container || container.children.length) return;
    container.innerHTML = SERIES_CARDS.map(c => `
      <a href="${c.href}" class="tp-subdomain-card">
        <i class="fas ${c.icon}"></i>
        <div><h4>${c.title}</h4><p>${c.sub}</p></div>
      </a>
    `).join('');
  }

  function initLip() {
    const toggle = document.getElementById('tpLipToggle');
    const lip = document.getElementById('tpHeaderLip');
    if (!toggle || !lip) return;

    const grid = lip.querySelector('[data-tp-series-grid]');
    renderSeriesGrid(grid);

    function setOpen(open) {
      lip.classList.toggle('open', open);
      toggle.classList.toggle('active', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      lip.setAttribute('aria-hidden', open ? 'false' : 'true');
    }

    toggle.addEventListener('click', e => {
      e.stopPropagation();
      setOpen(!lip.classList.contains('open'));
    });

    document.addEventListener('click', e => {
      if (!lip.contains(e.target) && !toggle.contains(e.target)) {
        setOpen(false);
      }
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLip);
  } else {
    initLip();
  }
})();
