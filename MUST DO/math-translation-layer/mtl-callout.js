/**
 * MTL Callout — progressive enhancement for .mtl-callout blocks.
 *
 * Behavior:
 *  - Attaches toggle listeners to each callout's header button.
 *  - Respects data-default="open" to expand on load.
 *  - Integrates with master-equation-explorer if a .me-explorer block is
 *    nested inside the callout.
 *  - Does NOT inject shells, nav bars, or audio players (handled by
 *    components/tp-inject.js).
 */
(function () {
  'use strict';

  const CALLOUT_SELECTOR = '.mtl-callout';
  const TOGGLE_SELECTOR = '.mtl-callout__toggle';
  const PANEL_SELECTOR = '.mtl-callout__panel';

  function setOpen(callout, open) {
    const toggle = callout.querySelector(TOGGLE_SELECTOR);
    const panel = callout.querySelector(PANEL_SELECTOR);
    if (!toggle || !panel) return;

    toggle.setAttribute('aria-expanded', String(open));
    panel.classList.toggle('open', open);

    const textEl = toggle.querySelector('.mtl-callout__toggle-text');
    if (textEl) {
      textEl.textContent = open ? 'Hide translation' : 'Read the translation';
    }

    // Forward state to any nested master-equation-explorer.
    const meTrigger = panel.querySelector('.me-trigger');
    if (meTrigger && typeof window.MEExplorer !== 'undefined') {
      window.MEExplorer.setOpen(meTrigger.closest('.me-explorer'), open);
    }
  }

  function attach(callout) {
    if (callout.dataset.mtlAttached) return;
    callout.dataset.mtlAttached = 'true';

    const toggle = callout.querySelector(TOGGLE_SELECTOR);
    if (!toggle) return;

    toggle.addEventListener('click', () => {
      const currentlyOpen = toggle.getAttribute('aria-expanded') === 'true';
      setOpen(callout, !currentlyOpen);
    });

    // Default state.
    const defaultOpen = callout.dataset.default === 'open' ||
                        callout.classList.contains('is-open');
    if (defaultOpen) {
      setOpen(callout, true);
    }
  }

  function init(scope) {
    const root = scope || document;
    root.querySelectorAll(CALLOUT_SELECTOR).forEach(attach);
  }

  // Public API for manual control and dynamic content.
  window.MTLCallout = {
    init,
    attach,
    setOpen
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => init());
  } else {
    init();
  }
})();
