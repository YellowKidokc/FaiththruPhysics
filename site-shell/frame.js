/**
 * FaithThruPhysics — ubiquitous site shell
 * Injects the global top bar + bottom audio dock into any page.
 *
 * Usage on a page:
 *   <script src="https://faiththruphysics.com/site-shell/frame.js" defer></script>
 *
 * Optional per-page profile (domain weights, etc.):
 *   <script id="page-profile" type="application/json">
 *     {"domains":[{"name":"History","pct":20,"color":"#8aa1ff"}, ...]}
 *   </script>
 */
(function(){
  'use strict';

  const WORKER_BASE = 'https://faith-audio-pipeline.davidokc28.workers.dev';
  const SITE_HOME = 'https://faiththruphysics.com';
  const SERIES_PATH = '/00-entry-and-series-map/index.html';

  const DEFAULT_DOMAINS = [
    { name:'History',       pct:20, color:'#8aa1ff' },
    { name:'Family',        pct:14, color:'#8fe6b0' },
    { name:'Religion',      pct:12, color:'#d6aa45' },
    { name:'Law / Order',   pct:12, color:'#ff7d90' },
    { name:'Education',     pct:11, color:'#7cc7ff' },
    { name:'Economy',       pct:10, color:'#ffb86b' },
    { name:'Media',         pct:9,  color:'#c79bff' },
    { name:'Institutions',  pct:8,  color:'#aeb8d6' },
    { name:'Synthesis',     pct:4,  color:'#f59e0b' }
  ];

  const MODE_LABELS = {
    read:'Read Aloud', debate:'Debate', deep:'Deep Dive', critique:'Critique', podcast:'Podcast'
  };
  const MODE_ORDER = ['read','debate','deep','critique'];
  const MODE_MAP = { tts:'read', debate:'debate', deep:'deep', critique:'critique', podcast:'podcast' };

  const CSS = `
  :root {
    --shell-bg:#070707; --shell-panel:#0f0f0f; --shell-border:#222;
    --shell-text:#e0e0e0; --shell-muted:#888; --shell-topbar-h:150px; --shell-dock-h:84px;
    --shell-gold:#d4af37; --shell-gold-rgb:212,175,55;
    --shell-blue:#4a9eff; --shell-purple:#a855f7; --shell-teal:#2dd4bf; --shell-red:#dc2626;
  }
  html {
    background:#050505 !important;
    color:var(--shell-text);
  }
  body {
    background:#050505 !important;
    color:var(--shell-text);
  }
  html { scroll-padding-top: var(--shell-topbar-h); }
  body { padding-top: var(--shell-topbar-h); padding-bottom: var(--shell-dock-h); }

  .site-shell-topbar {
    position: fixed; top:0; left:0; right:0; min-height: var(--shell-topbar-h);
    background: rgba(7,7,7,.97); border-bottom:1px solid var(--shell-border);
    backdrop-filter: blur(14px); z-index:9999;
    display:flex; flex-direction:column; overflow:hidden;
    font-family: 'Inter', system-ui, sans-serif;
  }
  .shell-gold-wave {
    position:absolute; top:0; left:0; right:0; bottom:0; pointer-events:none;
    background: linear-gradient(90deg, transparent 0%, rgba(var(--shell-gold-rgb),.18) 35%, rgba(var(--shell-gold-rgb),.55) 50%, rgba(var(--shell-gold-rgb),.18) 65%, transparent 100%);
    transform: translateX(-100%); opacity:0; z-index:0;
  }
  .shell-gold-wave.active { animation: shellKnightRider .9s ease-out forwards; }
  @keyframes shellKnightRider {
    0%   { transform: translateX(-100%); opacity:0; }
    12%  { opacity:1; }
    88%  { opacity:1; }
    100% { transform: translateX(100%); opacity:0; }
  }
  .shell-tb-row { display:flex; align-items:center; width:100%; padding:0 1.1rem; position:relative; z-index:1; }
  .shell-tb-top { justify-content:space-between; gap:1rem; min-height:54px; border-bottom:1px solid rgba(255,255,255,.06); padding-top:.25rem; padding-bottom:.25rem; }
  .shell-tb-bottom { justify-content:center; gap:1.2rem; min-height:calc(var(--shell-topbar-h) - 54px); padding-top:.35rem; padding-bottom:.5rem; }

  .shell-tb-home, .shell-tb-series {
    flex-shrink:0; color:#999; text-decoration:none; font-size:.95rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase;
    display:flex; align-items:center; gap:.45rem; transition:color .2s ease;
  }
  .shell-tb-home:hover { color:var(--shell-gold); }
  .shell-tb-series { color:var(--shell-red); }
  .shell-tb-series:hover { color:#f87171; }

  .shell-tb-domains {
    flex:1; display:flex; align-items:center; justify-content:center; gap:.55rem;
    overflow-x:auto; padding:.2rem .3rem; scrollbar-width:none;
  }
  .shell-tb-domains::-webkit-scrollbar { display:none; }
  .shell-domain-pill { --pill:var(--shell-gold); flex-shrink:0; display:inline-flex; align-items:center; gap:.35rem;
    border:1px solid rgba(255,255,255,.1); background:rgba(255,255,255,.03); border-radius:999px;
    padding:.3rem .7rem; font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace;
    font-size:.72rem; font-weight:600; color:#aaa; letter-spacing:.04em; text-transform:uppercase;
    cursor:pointer; transition:all .18s ease; white-space:nowrap;
  }
  .shell-domain-pill:hover { border-color:var(--pill); color:#fff; background:rgba(255,255,255,.06); }
  .shell-domain-pill b { color:#fff; font-weight:900; }
  .shell-domain-dot { width:6px; height:6px; border-radius:50%; background:var(--pill); box-shadow:0 0 10px color-mix(in srgb, var(--pill) 70%, transparent); }

  .shell-ladder-link { flex-shrink:0; color:#555; font-size:.8rem; font-weight:700; text-transform:uppercase; letter-spacing:.1em; text-decoration:none; white-space:nowrap; transition:color .2s; }
  .shell-ladder-link:hover { color:var(--shell-red); }
  .shell-ladder-tabs { display:inline-flex; border:1px solid #333; border-radius:999px; overflow:hidden; background:rgba(0,0,0,.35); }
  .shell-ladder-tab { padding:.7rem 1.3rem; border:none; background:transparent; color:#7d7d7d;
    font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace;
    font-size:1.05rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; cursor:pointer;
    transition:all .25s ease; border-left:1px solid #333; white-space:nowrap;
  }
  .shell-ladder-tab:first-child { border-left:none; }
  .shell-ladder-tab:hover { color:#fff; background:rgba(255,255,255,.04); }
  .shell-ladder-tab.active { color:var(--shell-gold); background:#000; border-color:var(--shell-gold); box-shadow:inset 0 0 22px rgba(var(--shell-gold-rgb),.12); }
  .shell-ladder-tab.active + .shell-ladder-tab { border-left-color:var(--shell-gold); }

  @media (max-width:1100px){
    :root { --shell-topbar-h:190px; }
    .shell-tb-top { min-height:58px; }
    .shell-tb-bottom { min-height:calc(var(--shell-topbar-h) - 58px); gap:.7rem; }
    .shell-ladder-tab { font-size:.92rem; padding:.6rem 1rem; }
    .shell-tb-domains { justify-content:flex-start; }
  }
  @media (max-width:720px){
    :root { --shell-topbar-h:230px; }
    .shell-tb-row { padding:0 .75rem; }
    .shell-tb-top { flex-wrap:wrap; gap:.4rem; min-height:auto; padding-top:.4rem; padding-bottom:.3rem; }
    .shell-tb-home, .shell-tb-series { font-size:.78rem; }
    .shell-tb-domains { order:3; flex-basis:100%; justify-content:center; margin-top:.2rem; }
    .shell-tb-bottom { gap:.35rem; min-height:auto; padding-top:.4rem; padding-bottom:.55rem; flex-wrap:wrap; }
    .shell-ladder-link { display:none; }
    .shell-ladder-tabs { border-radius:.6rem; flex-wrap:wrap; justify-content:center; }
    .shell-ladder-tab { font-size:.85rem; padding:.55rem .85rem; border-left:none; border-bottom:1px solid #222; flex:1 1 auto; }
    .shell-ladder-tab:last-child { border-bottom:none; }
  }

  .site-shell-dock {
    position:fixed; left:0; right:0; bottom:0; height:var(--shell-dock-h); background:var(--shell-panel);
    border-top:1px solid var(--shell-border); display:flex; flex-direction:column; z-index:9998;
    font-family:'Inter', system-ui, sans-serif;
  }
  .shell-dock-pills { display:flex; gap:0; border-bottom:1px solid var(--shell-border); height:36px; }
  .shell-dock-pill { flex:1; display:flex; align-items:center; justify-content:center; gap:.45rem; padding:.55rem .6rem;
    background:transparent; border:none; cursor:pointer;
    font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace;
    font-size:.72rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:#777; transition:all .25s ease; position:relative;
  }
  .shell-dock-pill::after { content:''; position:absolute; bottom:0; left:20%; right:20%; height:2.5px; border-radius:1.5px; background:transparent; transition:all .25s ease; }
  .shell-dock-pill:hover { color:var(--shell-text); background:rgba(255,255,255,.03); }
  .shell-dock-pill[data-mode="read"]     { --pill-c:var(--shell-gold); }
  .shell-dock-pill[data-mode="debate"]   { --pill-c:var(--shell-purple); }
  .shell-dock-pill[data-mode="deep"]     { --pill-c:var(--shell-blue); }
  .shell-dock-pill[data-mode="critique"] { --pill-c:var(--shell-teal); }
  .shell-dock-pill.active { color:var(--pill-c); background:rgba(255,255,255,.02); }
  .shell-dock-pill.active::after { background:var(--pill-c); box-shadow:0 0 10px color-mix(in srgb, var(--pill-c) 50%, transparent); }
  .shell-dock-pill .shell-pill-dot { width:5px; height:5px; border-radius:50%; background:currentColor; opacity:.5; transition:opacity .25s; }
  .shell-dock-pill.active .shell-pill-dot { opacity:1; }
  .shell-dock-pill.unavailable { opacity:.25; cursor:default; pointer-events:none; }
  .shell-dock-body { display:flex; align-items:center; gap:.75rem; padding:.65rem 1rem; flex:1; }
  .shell-dock-play { width:36px; height:36px; border-radius:50%; border:1.5px solid var(--shell-gold); background:transparent; color:var(--shell-gold); font-size:.75rem; cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0; transition:all .2s ease; }
  .shell-dock-play:hover { background:rgba(212,175,55,.1); transform:scale(1.05); }
  .shell-dock-track-wrap { flex:1; display:flex; flex-direction:column; gap:.25rem; min-width:0; }
  .shell-dock-track { width:100%; height:5px; background:#222; border-radius:2.5px; cursor:pointer; overflow:hidden; position:relative; }
  .shell-dock-fill { height:100%; width:0%; border-radius:2.5px; background:var(--shell-gold); transition:width .15s linear, background .3s; }
  .shell-dock-times { display:flex; justify-content:space-between; font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace; font-size:.62rem; color:#666; }
  .shell-dock-vol { background:none; border:none; color:#666; cursor:pointer; font-size:.85rem; flex-shrink:0; padding:2px; transition:color .2s; }
  .shell-dock-vol:hover { color:var(--shell-text); }
  .shell-dock-speed { flex-shrink:0; height:32px; min-width:72px; border:1px solid var(--shell-border); border-radius:.4rem; background:#111; color:#888; font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace; font-size:.65rem; font-weight:700; cursor:pointer; outline:none; padding:0 .45rem; }
  .shell-dock-empty { display:none; align-items:center; justify-content:center; flex:1; font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace; font-size:.7rem; letter-spacing:.06em; text-transform:uppercase; color:#555; }
  .shell-dock-body.hidden { display:none; } .shell-dock-empty.visible { display:flex; }

  .shell-dock-mini { position:fixed; right:1rem; bottom:calc(var(--shell-dock-h) + .85rem); z-index:9999; display:flex; align-items:center; gap:.6rem;
    padding:.6rem .85rem; border:1px solid rgba(212,175,55,.28); border-radius:.6rem; background:rgba(15,15,15,.94);
    box-shadow:0 16px 40px rgba(0,0,0,.38); opacity:0; transform:translateY(12px); pointer-events:none; transition:opacity .2s ease, transform .2s ease;
  }
  .shell-dock-mini.visible { opacity:1; transform:translateY(0); pointer-events:auto; }
  .shell-mini-play { width:38px; height:38px; border-radius:50%; border:1.5px solid var(--shell-gold); background:transparent; color:var(--shell-gold); display:flex; align-items:center; justify-content:center; cursor:pointer; transition:transform .2s, background .2s; }
  .shell-mini-play:hover { transform:scale(1.05); background:rgba(212,175,55,.1); }
  .shell-mini-label { max-width:120px; color:#777; font-family:ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace; font-size:.6rem; font-weight:700; letter-spacing:.07em; line-height:1.2; text-transform:uppercase; }

  @media (max-width:520px){
    :root { --shell-dock-h:130px; }
    .shell-dock-pills { flex-wrap:wrap; height:auto; }
    .shell-dock-pill { flex-basis:50%; min-height:38px; }
    .shell-dock-body { flex-wrap:wrap; }
    .shell-dock-track-wrap { flex-basis:calc(100% - 50px); }
    .shell-dock-speed { margin-left:50px; }
    .shell-dock-mini { right:.75rem; bottom:calc(var(--shell-dock-h) + .6rem); }
  }
  `;

  let _pageMeta = null;
  function getPageMeta(){
    if (_pageMeta) return _pageMeta;
    const ids = ['page-profile','article-meta'];
    for (const id of ids) {
      const el = document.getElementById(id);
      if (!el) continue;
      try { _pageMeta = JSON.parse(el.textContent); return _pageMeta; }
      catch(e){ /* ignore malformed */ }
    }
    _pageMeta = {};
    return _pageMeta;
  }

  function getProfile(){
    const meta = getPageMeta();
    if (Array.isArray(meta.domains)) return meta.domains;
    if (Array.isArray(meta.classification)) {
      // article-meta uses {tag,label,pct,color}; map to {name,pct,color}
      return meta.classification.map(c => ({
        name: c.label || c.tag || 'Domain',
        pct: c.pct,
        color: c.color
      }));
    }
    return DEFAULT_DOMAINS;
  }

  function getReadingMode(){
    const meta = getPageMeta();
    const level = (meta.reading_level || meta.readingLevel || '').toString().toLowerCase();
    const map = { easy:'easy', story:'easy', plain:'standard', standard:'standard', academic:'academic', test:'academic', proof:'proof', math:'math', claims:'math' };
    return map[level] || 'standard';
  }

  function fmt(s){
    if(!s||isNaN(s)) return '0:00';
    const m=Math.floor(s/60), sec=Math.floor(s%60);
    return m+':'+(sec<10?'0':'')+sec;
  }

  function deriveSlug(){
    const path = window.location.pathname.replace(/^\/+/,'').replace(/\.html?$/i,'');
    if (window.location.protocol === 'file:' || path.includes('ubiquitous-frame')) {
      return 'genesis-to-quantum/gtq-01-measurement-collapsed-reality';
    }
    return path;
  }

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  function buildTopBar(){
    const domains = getProfile();
    const domainPills = domains.map(d => `<span class="shell-domain-pill" data-domain="${escapeHtml(d.name)}" style="--pill:${d.color||'#d4af37'}"><span class="shell-domain-dot"></span>${escapeHtml(d.name)} <b>${Number(d.pct)||0}%</b></span>`).join('');
    const nav = document.createElement('header');
    nav.className = 'site-shell-topbar';
    nav.id = 'siteShellTopbar';
    nav.innerHTML = `
      <div class="shell-gold-wave" id="shellGoldWave"></div>
      <div class="shell-tb-row shell-tb-top">
        <a class="shell-tb-home" href="${SITE_HOME}">⌂ Home</a>
        <nav class="shell-tb-domains" aria-label="Domain profile">${domainPills}</nav>
        <a class="shell-tb-series" href="${SITE_HOME}${SERIES_PATH}">☰ Series</a>
      </div>
      <div class="shell-tb-row shell-tb-bottom">
        <a class="shell-ladder-link" href="#prev">← Prev</a>
        <div class="shell-ladder-tabs" role="tablist" aria-label="Reading ladder">
          <button class="shell-ladder-tab" data-reader-mode="easy" type="button">Story</button>
          <button class="shell-ladder-tab active" data-reader-mode="standard" type="button">Plain</button>
          <button class="shell-ladder-tab" data-reader-mode="academic" type="button">Test</button>
          <button class="shell-ladder-tab" data-reader-mode="proof" type="button">Proof</button>
          <button class="shell-ladder-tab" data-reader-mode="math" type="button">Math</button>
        </div>
        <a class="shell-ladder-link" href="#next">Next →</a>
      </div>`;
    return nav;
  }

  function buildDock(){
    const dock = document.createElement('div');
    dock.className = 'site-shell-dock';
    dock.id = 'siteShellDock';
    dock.innerHTML = `
      <div class="shell-dock-pills">
        ${MODE_ORDER.map(m => `<button class="shell-dock-pill" data-mode="${m}" type="button"><span class="shell-pill-dot"></span>${MODE_LABELS[m]}</button>`).join('')}
      </div>
      <div class="shell-dock-body" id="shellDockBody">
        <button class="shell-dock-play" id="shellDockPlay" aria-label="Play or pause"><i class="fas fa-play" id="shellDockPlayIcon"></i></button>
        <div class="shell-dock-track-wrap">
          <div class="shell-dock-track" id="shellDockTrack"><div class="shell-dock-fill" id="shellDockFill"></div></div>
          <div class="shell-dock-times"><span id="shellDockCurrent">0:00</span><span id="shellDockDuration">0:00</span></div>
        </div>
        <button class="shell-dock-vol" id="shellDockVol" aria-label="Mute"><i class="fas fa-volume-up"></i></button>
        <select class="shell-dock-speed" id="shellDockSpeed" aria-label="Playback speed">
          <option value="0.75">0.75x</option><option value="1" selected>1x</option>
          <option value="1.25">1.25x</option><option value="1.5">1.5x</option>
          <option value="1.75">1.75x</option><option value="2">2x</option>
        </select>
      </div>
      <div class="shell-dock-empty" id="shellDockEmpty"><span style="margin-right:.5rem;">◷</span> No audio for this page yet</div>
      <div class="shell-dock-mini" id="shellDockMini" aria-hidden="true">
        <button class="shell-mini-play" id="shellDockMiniPlay" type="button" aria-label="Play or pause"><i class="fas fa-play" id="shellDockMiniIcon"></i></button>
        <div class="shell-mini-label" id="shellDockMiniLabel">Audio</div>
      </div>`;
    return dock;
  }

  function injectStyles(){
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
  }

  function initTopBar(){
    const topbar = buildTopBar();
    document.body.insertBefore(topbar, document.body.firstChild);

    // Set initial active ladder tab from page meta
    const initialMode = getReadingMode();
    document.querySelectorAll('.shell-ladder-tab').forEach(t => t.classList.remove('active'));
    const initialTab = document.querySelector(`.shell-ladder-tab[data-reader-mode="${initialMode}"]`);
    if (initialTab) initialTab.classList.add('active');

    // Wire prev/next from article-meta if available
    const meta = getPageMeta();
    const prevLink = topbar.querySelector('.shell-ladder-link[href="#prev"]');
    const nextLink = topbar.querySelector('.shell-ladder-link[href="#next"]');
    if (prevLink && meta.prev) prevLink.href = meta.prev;
    if (nextLink && meta.next) nextLink.href = meta.next;

    const wave = document.getElementById('shellGoldWave');
    function triggerWave(){
      wave.classList.remove('active');
      void wave.offsetWidth;
      wave.classList.add('active');
      setTimeout(() => wave.classList.remove('active'), 900);
    }
    document.querySelectorAll('.shell-ladder-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.shell-ladder-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        triggerWave();
        const mode = tab.dataset.readerMode;
        document.body.dispatchEvent(new CustomEvent('shell:readerMode', {detail:{mode}}));
      });
    });
    document.querySelectorAll('.shell-domain-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        const domain = pill.dataset.domain;
        // Future: navigate to domain-matching page.
        console.log('domain selected:', domain);
      });
    });
  }

  async function initDock(){
    const slug = deriveSlug();
    document.body.appendChild(buildDock());

    const playBtn = document.getElementById('shellDockPlay');
    const icon    = document.getElementById('shellDockPlayIcon');
    const fill    = document.getElementById('shellDockFill');
    const curEl   = document.getElementById('shellDockCurrent');
    const durEl   = document.getElementById('shellDockDuration');
    const volBtn  = document.getElementById('shellDockVol');
    const speedEl = document.getElementById('shellDockSpeed');
    const track   = document.getElementById('shellDockTrack');
    const body    = document.getElementById('shellDockBody');
    const empty   = document.getElementById('shellDockEmpty');
    const mini    = document.getElementById('shellDockMini');
    const miniPlay= document.getElementById('shellDockMiniPlay');
    const miniIcon= document.getElementById('shellDockMiniIcon');
    const miniLbl = document.getElementById('shellDockMiniLabel');
    const pills   = document.querySelectorAll('.shell-dock-pill');

    const audio = new Audio(); audio.preload = 'metadata';
    let muted = false;

    function setIcon(paused){ const cls=paused?'fas fa-play':'fas fa-pause'; icon.className=cls; miniIcon.className=cls; }
    function setUnavailable(p){ p.classList.add('unavailable'); p.removeAttribute('data-url'); }

    function selectPill(pill){
      const mode = pill.dataset.mode, url = pill.dataset.url;
      if(!url) return;
      audio.pause();
      audio.src = url;
      audio.playbackRate = parseFloat(speedEl.value)||1;
      pills.forEach(q=>q.classList.remove('active'));
      pill.classList.add('active');
      const c = getComputedStyle(document.documentElement).getPropertyValue(`--shell-${mode==='read'?'gold':mode==='deep'?'blue':mode==='debate'?'purple':'teal'}`).trim() || '#d4af37';
      fill.style.background = c;
      playBtn.style.borderColor = c;
      playBtn.style.color = c;
      miniLbl.textContent = MODE_LABELS[mode];
      body.classList.remove('hidden'); empty.classList.remove('visible');
    }

    pills.forEach(p => p.addEventListener('click', () => {
      if(!p.dataset.url) return;
      if(p.classList.contains('active')){ audio.paused?audio.play():audio.pause(); return; }
      selectPill(p); audio.play();
    }));

    const toggle = () => audio.src && (audio.paused?audio.play():audio.pause());
    playBtn.addEventListener('click', toggle);
    miniPlay.addEventListener('click', toggle);
    speedEl.addEventListener('change', () => { audio.playbackRate = parseFloat(speedEl.value)||1; });
    audio.addEventListener('play', ()=>setIcon(false));
    audio.addEventListener('pause', ()=>setIcon(true));
    audio.addEventListener('ended', ()=>{ setIcon(true); fill.style.width='0%'; curEl.textContent='0:00'; });
    audio.addEventListener('timeupdate', ()=>{
      if(!audio.duration) return;
      fill.style.width = (audio.currentTime/audio.duration*100)+'%';
      curEl.textContent = fmt(audio.currentTime);
    });
    audio.addEventListener('loadedmetadata', ()=>{ durEl.textContent = fmt(audio.duration); });
    track.addEventListener('click', e=>{
      if(!audio.duration) return;
      const r=track.getBoundingClientRect();
      const p=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width));
      audio.currentTime = p*audio.duration;
    });
    volBtn.addEventListener('click', ()=>{
      muted=!muted; audio.muted=muted;
      volBtn.innerHTML = muted?'<i class="fas fa-volume-mute"></i>':'<i class="fas fa-volume-up"></i>';
    });

    const obs = new IntersectionObserver((entries)=>{
      const show = !entries[0].isIntersecting && !!audio.src;
      mini.classList.toggle('visible', show);
      mini.setAttribute('aria-hidden', show?'false':'true');
    }, {threshold:0});
    obs.observe(document.getElementById('siteShellDock'));

    try {
      const resp = await fetch(`${WORKER_BASE}/api/audio?slug=${encodeURIComponent(slug)}`);
      const data = resp.ok ? await resp.json() : {};
      const tracks = data.tracks || [];
      let any = false;
      tracks.forEach(t => {
        const mapped = MODE_MAP[t.mode] || t.mode;
        const pill = document.querySelector(`.shell-dock-pill[data-mode="${mapped}"]`);
        if(pill && t.url){ pill.dataset.url = t.url; any = true; }
      });
      if(!any){
        MODE_ORDER.forEach(m => setUnavailable(document.querySelector(`.shell-dock-pill[data-mode="${m}"]`)));
        body.classList.add('hidden'); empty.classList.add('visible');
      } else {
        const first = document.querySelector('.shell-dock-pill[data-url]');
        if(first) selectPill(first);
      }
    } catch(e){
      MODE_ORDER.forEach(m => setUnavailable(document.querySelector(`.shell-dock-pill[data-mode="${m}"]`)));
      body.classList.add('hidden'); empty.classList.add('visible');
    }
  }

  function init(){
    if (document.getElementById('siteShellTopbar')) return;
    injectStyles();
    initTopBar();
    initDock();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
