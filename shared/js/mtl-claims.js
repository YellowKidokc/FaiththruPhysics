/**
 * MTL Claims Layer — v1.1
 *
 * Two modes:
 *  1. Auto-detection: scans paragraphs for claim-signal words (existing behaviour).
 *  2. Sidecar injection: reads {PAGE-ID}-claims.json and renders approved claims
 *     after their named sections. Spec: /shared/CLAIMS_SPEC.md
 */
(function(){
  'use strict';

  // ─── SIDECAR CLAIM RENDERER ──────────────────────────────────────────────

  const CLASSIFICATION_COLORS = {
    'load-bearing': { border: 'rgba(245,158,11,0.6)',  bg: 'rgba(245,158,11,0.06)',  label: '#f59e0b' },
    'suggestive':   { border: 'rgba(156,163,175,0.4)', bg: 'rgba(156,163,175,0.04)', label: '#9ca3af' },
    'overreached':  { border: 'rgba(220,38,38,0.5)',   bg: 'rgba(220,38,38,0.05)',   label: '#dc2626' },
  };

  function deriveClaimsUrl() {
    const path = window.location.pathname;
    const file = path.split('/').pop() || '';
    const parts = file.replace('.html','').split('-');
    if (parts.length < 2) return null;
    const dir  = path.substring(0, path.lastIndexOf('/') + 1);
    return dir + parts[0] + '-' + parts[1] + '-claims.json';
  }

  function buildSidecarClaimEl(claim) {
    const c = CLASSIFICATION_COLORS[claim.classification] || CLASSIFICATION_COLORS['suggestive'];
    const role = claim.series_role || '';
    const links = (claim.evidenced_in || []).length
      ? `<span class="mtl-sc-links">evidenced in: ${claim.evidenced_in.join(', ')}</span>`
      : '';

    const el = document.createElement('div');
    el.className = 'mtl-sidecar-claim';
    el.dataset.claimId = claim.claim_id;
    el.dataset.classification = claim.classification;
    el.style.cssText = `
      display:none;
      margin: 0.75rem 0 1.5rem;
      padding: 0.9rem 1.2rem;
      border-left: 3px solid ${c.border};
      background: ${c.bg};
      border-radius: 0 8px 8px 0;
    `;
    el.innerHTML = `
      <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.45rem;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;text-transform:uppercase;color:${c.label};">${claim.classification}</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(156,163,175,0.6);">${role}</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:rgba(156,163,175,0.4);">${claim.claim_id}</span>
      </div>
      <p style="font-family:'Crimson Text',Georgia,serif;font-size:1.05rem;line-height:1.7;color:#e5e7eb;margin:0 0 0.35rem;">${escapeHtml(claim.text)}</p>
      ${links ? `<div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:rgba(156,163,175,0.5);margin-top:0.3rem;">${links}</div>` : ''}
    `;
    return el;
  }

  function injectSidecarClaims(data) {
    const claims = (data.claims || []).filter(c => c.status === 'approved');
    if (!claims.length) return;

    claims.forEach(claim => {
      const anchor = document.querySelector(`[data-name="${claim.after}"]`);
      if (!anchor) return;
      const el = buildSidecarClaimEl(claim);
      anchor.insertAdjacentElement('afterend', el);
    });
  }

  function loadSidecarClaims() {
    const url = deriveClaimsUrl();
    if (!url) return;
    fetch(url)
      .then(r => r.ok ? r.json() : null)
      .catch(() => null)
      .then(data => { if (data) injectSidecarClaims(data); });
  }

  // ─── EXISTING AUTO-DETECTION ─────────────────────────────────────────────

  // Same signal words used by Python-WEB/modules/claim_map.py
  const CLAIM_RE = /\b(claim|argue|therefore|thesis|conclude|because|proves?|shows?|demonstrates?|thus|hence|so)\b/i;
  const SENTENCE_RE = /[^.!?]+[.!?]+/g;

  function isClaimSentence(sentence){
    return CLAIM_RE.test(sentence);
  }

  function splitSentences(text){
    return (text.match(SENTENCE_RE) || [text]).map(s => s.trim()).filter(Boolean);
  }

  function walkTextNodes(node, callback){
    if(node.nodeType === Node.TEXT_NODE){
      callback(node);
      return;
    }
    // Skip script/style/code blocks and already-processed nodes
    if(node.nodeName === 'SCRIPT' || node.nodeName === 'STYLE' || node.nodeName === 'CODE' || node.nodeName === 'PRE'){
      return;
    }
    Array.from(node.childNodes).forEach(child => walkTextNodes(child, callback));
  }

  function processParagraph(p){
    // Collect claim sentences from raw text first
    const rawText = p.textContent || '';
    const sentences = splitSentences(rawText);
    const claimSentences = sentences.filter(isClaimSentence);
    if(claimSentences.length === 0) return;

    p.classList.add('mtl-claim-paragraph');

    // Wrap claim sentences inside text nodes with <mark>
    walkTextNodes(p, function(textNode){
      const text = textNode.textContent;
      const parts = [];
      let lastIndex = 0;
      let m;
      SENTENCE_RE.lastIndex = 0;
      while((m = SENTENCE_RE.exec(text)) !== null){
        if(m.index > lastIndex){
          parts.push({text: text.slice(lastIndex, m.index), claim: false});
        }
        parts.push({text: m[0], claim: isClaimSentence(m[0])});
        lastIndex = SENTENCE_RE.lastIndex;
      }
      if(lastIndex < text.length){
        parts.push({text: text.slice(lastIndex), claim: false});
      }

      if(parts.some(part => part.claim)){
        const fragment = document.createDocumentFragment();
        parts.forEach(part => {
          if(part.claim){
            const mark = document.createElement('mark');
            mark.className = 'mtl-claim-sentence';
            mark.textContent = part.text;
            fragment.appendChild(mark);
          } else {
            fragment.appendChild(document.createTextNode(part.text));
          }
        });
        textNode.parentNode.replaceChild(fragment, textNode);
      }
    });

    // Build inline claim list below the paragraph
    const block = document.createElement('div');
    block.className = 'mtl-claim-block';
    block.innerHTML = '<div class="mtl-claim-label">Claims in this paragraph</div>' +
      claimSentences.map((s, i) =>
        `<button class="mtl-claim-chip" data-claim-index="${i}">${escapeHtml(s)}</button>`
      ).join('');

    block.querySelectorAll('.mtl-claim-chip').forEach((chip, i) => {
      chip.addEventListener('click', function(){
        const marks = p.querySelectorAll('.mtl-claim-sentence');
        marks.forEach(m => m.classList.remove('active'));
        if(marks[i]){
          marks[i].classList.add('active');
          marks[i].scrollIntoView({behavior: 'smooth', block: 'center'});
        }
      });
    });

    p.insertAdjacentElement('afterend', block);
  }

  function escapeHtml(text){
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function init(){
    // Load sidecar claims first (approved, authored claims from the pipeline)
    loadSidecarClaims();

    // Auto-detect claim sentences in prose
    const roots = document.querySelectorAll('main, article, .prose-body, [data-component="content"]');
    if(roots.length === 0) roots.push(document.body);

    roots.forEach(root => {
      root.querySelectorAll('p, li').forEach(processParagraph);
    });

    addToggleButton();
  }

  function addToggleButton(){
    const bar = document.getElementById('mtlReaderBar');
    if(!bar) return;

    const tabs = bar.querySelector('.mtl-reader-tabs');
    if(!tabs) return;

    const btn = document.createElement('button');
    btn.className = 'mtl-reader-tab';
    btn.type = 'button';
    btn.dataset.readerMode = 'claims';
    btn.setAttribute('aria-selected', 'false');
    btn.textContent = 'Claims';

    btn.addEventListener('click', function(){
      const active = document.body.classList.toggle('mtl-claims-active');
      if(active){
        tabs.querySelectorAll('.mtl-reader-tab:not([data-reader-mode="claims"])').forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
      }
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-selected', active ? 'true' : 'false');

      // Show/hide sidecar (approved, authored) claims
      document.querySelectorAll('.mtl-sidecar-claim').forEach(el => {
        el.style.display = active ? 'block' : 'none';
      });
    });

    tabs.appendChild(btn);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
