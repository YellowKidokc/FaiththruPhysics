(function () {
  'use strict';

  const DEFAULT = 'college';
  const STORAGE_KEY = 'tpReadingLevel';

  function setLevel(level) {
    const panels = document.querySelectorAll('.tp-level-panel');
    const buttons = document.querySelectorAll('.tp-level[data-level]');
    if (!panels.length) return;

    buttons.forEach(btn => {
      const on = btn.dataset.level === level;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-selected', on ? 'true' : 'false');
    });

    panels.forEach(panel => {
      const on = panel.dataset.readingLevel === level;
      panel.hidden = !on;
      panel.classList.toggle('active', on);
    });

    try { localStorage.setItem(STORAGE_KEY, level); } catch (e) { /* ignore */ }
  }

  function init() {
    const buttons = document.querySelectorAll('.tp-level[data-level]');
    if (!buttons.length) return;

    buttons.forEach(btn => {
      btn.addEventListener('click', () => setLevel(btn.dataset.level));
    });

    let saved = DEFAULT;
    try {
      const v = localStorage.getItem(STORAGE_KEY);
      if (v && document.querySelector(`.tp-level-panel[data-reading-level="${v}"]`)) saved = v;
    } catch (e) { /* ignore */ }

    setLevel(saved);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
