(function (global) {
  'use strict';

  const THRESHOLD = 100;

  function closeLip() {
    const lip = document.getElementById('tpHeaderLip');
    const toggle = document.getElementById('tpLipToggle');
    if (lip) {
      lip.classList.remove('open');
      lip.setAttribute('aria-hidden', 'true');
    }
    if (toggle) {
      toggle.classList.remove('active');
      toggle.setAttribute('aria-expanded', 'false');
    }
  }

  function collapseVerification() {
    document.getElementById('verificationToggle')?.classList.remove('open');
    document.getElementById('verificationBody')?.classList.remove('open');
  }

  function updateScrollChrome() {
    const y = window.scrollY || window.pageYOffset || 0;
    const shouldCompact = y > THRESHOLD;
    const isCompact = document.body.classList.contains('tp-scrolled');

    if (shouldCompact !== isCompact) {
      document.body.classList.toggle('tp-scrolled', shouldCompact);
      if (shouldCompact) {
        closeLip();
        collapseVerification();
      }
    }
  }

  function injectCss() {
    if (document.getElementById('tp-scroll-chrome-css')) return;
    const script = document.currentScript || document.querySelector('script[src*="tp-scroll-chrome.js"]');
    const href = script?.src ? script.src.replace(/\.js(\?.*)?$/, '.css$1') : '../components/tp-scroll-chrome.css';
    const link = document.createElement('link');
    link.id = 'tp-scroll-chrome-css';
    link.rel = 'stylesheet';
    link.href = href;
    document.head.appendChild(link);
  }

  function init() {
    injectCss();
    if (document.body.dataset.scrollChromeBound) return;
    document.body.dataset.scrollChromeBound = '1';
    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateScrollChrome();
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    document.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    updateScrollChrome();
  }

  global.tpScrollChrome = { update: updateScrollChrome };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})(window);
