/**
 * Master Equation Explorer — toggle behavior.
 *
 * Usage:
 *   <div class="me-explorer" data-me-auto-init>
 *     <button class="me-trigger" aria-expanded="false" aria-controls="mePanel-1">...</button>
 *     <div class="me-panel" id="mePanel-1">...</div>
 *   </div>
 *
 * Or call manually:
 *   MasterEquationExplorer.init(container);
 */
(function () {
  'use strict';

  function init(container) {
    const triggers = container.querySelectorAll('.me-trigger');
    triggers.forEach(trigger => {
      if (trigger.dataset.meBound) return;
      trigger.dataset.meBound = 'true';

      const panelId = trigger.getAttribute('aria-controls');
      const panel = panelId ? document.getElementById(panelId) : container.querySelector('.me-panel');
      if (!panel) return;

      function setOpen(open) {
        trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
        panel.classList.toggle('open', open);
      }

      trigger.addEventListener('click', () => setOpen(trigger.getAttribute('aria-expanded') !== 'true'));
      trigger.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          setOpen(trigger.getAttribute('aria-expanded') !== 'true');
        }
      });
    });
  }

  function initAll(root) {
    root = root || document;
    root.querySelectorAll('.me-explorer').forEach(init);
  }

  window.MasterEquationExplorer = { init, initAll };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initAll());
  } else {
    initAll();
  }
})();
