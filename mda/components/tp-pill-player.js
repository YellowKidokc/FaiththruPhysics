/* ═══════════════════════════════════════════════════════════════
   TP Pill-Strip Audio Player — shared script
   Auto-initializes every .tp-pill-player and .tp-pill-bar on the page.
   ═══════════════════════════════════════════════════════════════ */

(function(){
  'use strict';

  const colors = {
    deep:     '#4a9eff',
    debate:   '#a855f7',
    critique: '#dc2626',
    tts:      '#3bb39a',
    web:      '#f59e0b',
    default:  '#d4af37'
  };

  function fmt(s){
    if(!isFinite(s) || isNaN(s)) return '0:00';
    const m = Math.floor(s/60), sec = Math.floor(s%60);
    return m + ':' + (sec<10?'0':'') + sec;
  }

  function lighten(hex, pct){
    const num = parseInt(hex.replace('#',''), 16);
    const amt = Math.round(2.55 * pct);
    const R = Math.min(255, (num >> 16) + amt);
    const G = Math.min(255, ((num >> 8) & 0x00FF) + amt);
    const B = Math.min(255, (num & 0x0000FF) + amt);
    return '#' + (0x1000000 + R*0x10000 + G*0x100 + B).toString(16).slice(1);
  }

  async function loadTracksFromAPI(root){
    const slug = root.dataset.audioSlug || '';
    const api  = root.dataset.audioApi  || '/api/audio';
    if(!slug) return false;
    try{
      const res = await fetch(`${api}?slug=${encodeURIComponent(slug)}`);
      if(!res.ok) return false;
      const data = await res.json();
      const tracks = data.tracks || [];
      if(!tracks.length) return false;
      const map = {};
      tracks.forEach(t=>{ if(t.mode) map[t.mode] = t.url || t.src; });
      const ttsFallback = map.tts || map['tts-athena'] || map['voice-sample-athena'] || map['tts-orpheus'] || map['voice-sample-orpheus'] || '';
      root.querySelectorAll('.tp-pill').forEach(pill=>{
        const mode = pill.dataset.mode;
        if(mode && map[mode]) pill.dataset.src = map[mode];
        else if(mode === 'tts' && ttsFallback) pill.dataset.src = ttsFallback;
      });
      return true;
    }catch(e){
      return false;
    }
  }

  async function initPlayer(root){
    if(root.dataset.tpInitialized === 'true') return;
    root.dataset.tpInitialized = 'true';

    const isBar = root.classList.contains('tp-pill-bar');
    const audio = root.querySelector('audio');
    const pills = root.querySelectorAll('.tp-pill');
    if(!audio || !pills.length) return;

    await loadTracksFromAPI(root);

    const playBtn = root.querySelector(isBar ? '.tp-bar-play' : '.tp-btn.play');
    const track   = root.querySelector(isBar ? '.tp-bar-track' : '.tp-track');
    const fill    = root.querySelector(isBar ? '.tp-bar-fill' : '.tp-fill');
    const speed   = root.querySelector(isBar ? '.tp-bar-speed' : '.tp-speed-select');
    const timeEl  = isBar ? root.querySelector('.tp-bar-time') : null;
    const curEl   = isBar ? null : root.querySelector('#tpCurrentTime');
    const durEl   = isBar ? null : root.querySelector('#tpDuration');
    const labelEl = isBar ? null : root.querySelector('#tpNowPlayingLabel');
    const dotEl   = isBar ? null : root.querySelector('#tpModeDot');
    const muteBtn = isBar ? root.querySelector('.tp-bar-mute') : root.querySelector('#tpMuteBtn');
    const volSl   = isBar ? root.querySelector('.tp-bar-volume') : root.querySelector('#tpVolumeSlider');

    function setVisuals(pill){
      pills.forEach(p=>p.classList.remove('active'));
      pill.classList.add('active');
      const mode = pill.dataset.mode || 'default';
      const color = colors[mode] || colors.default;
      fill.style.background = `linear-gradient(90deg, ${color}, ${lighten(color, 20)})`;
      if(isBar){
        playBtn.style.borderColor = color;
        playBtn.style.color = color;
      }
      if(labelEl) labelEl.textContent = pill.dataset.label || mode;
      if(dotEl) dotEl.style.background = color;
    }

    function loadPill(pill, autoplay){
      setVisuals(pill);
      if(!pill.dataset.src) return;
      const wasPlaying = !audio.paused;
      audio.pause();
      audio.src = pill.dataset.src;
      audio.load();
      if(speed) audio.playbackRate = parseFloat(speed.value);
      if(autoplay || wasPlaying) audio.play().catch(()=>{});
      updateIcon();
    }

    function updateIcon(){
      const icon = playBtn.querySelector('i');
      if(icon) icon.className = audio.paused ? 'fas fa-play' : 'fas fa-pause';
    }

    pills.forEach(pill=>{
      pill.addEventListener('click', ()=> loadPill(pill, true) );
    });

    playBtn.addEventListener('click', ()=>{
      if(!audio.src && pills.length) loadPill(pills[0], false);
      if(audio.paused) audio.play().catch(()=>{});
      else audio.pause();
    });

    audio.addEventListener('timeupdate', ()=>{
      if(audio.duration) fill.style.width = (audio.currentTime/audio.duration*100) + '%';
      if(timeEl) timeEl.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration||0);
      if(curEl) curEl.textContent = fmt(audio.currentTime);
    });
    audio.addEventListener('loadedmetadata', ()=>{
      if(timeEl) timeEl.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
      if(durEl) durEl.textContent = fmt(audio.duration);
    });
    audio.addEventListener('ended', ()=>{ updateIcon(); fill.style.width = '0%'; });
    audio.addEventListener('play', updateIcon);
    audio.addEventListener('pause', updateIcon);

    track.addEventListener('click', (e)=>{
      if(!audio.duration) return;
      const r = track.getBoundingClientRect();
      const pct = Math.max(0, Math.min(1, (e.clientX - r.left)/r.width));
      audio.currentTime = pct * audio.duration;
    });

    if(speed){
      speed.addEventListener('change', ()=>{ audio.playbackRate = parseFloat(speed.value); });
    }

    if(muteBtn){
      muteBtn.addEventListener('click', ()=>{
        audio.muted = !audio.muted;
        muteBtn.querySelector('i').className = 'fas fa-volume-' + (audio.muted ? 'mute' : 'up');
      });
    }

    if(volSl){
      volSl.addEventListener('input', ()=>{
        audio.volume = parseFloat(volSl.value);
        audio.muted = false;
        if(muteBtn) muteBtn.querySelector('i').className = 'fas fa-volume-up';
      });
    }

    if(isBar && root.dataset.dock !== 'false'){
      let lastY = window.scrollY;
      const updateDock = ()=>{
        const y = window.scrollY;
        root.classList.toggle('is-docked', y > 260 && y < lastY);
        lastY = y;
      };
      window.addEventListener('scroll', updateDock, { passive: true });
      updateDock();
    }

    // init first pill without playing
    const active = root.querySelector('.tp-pill.active') || pills[0];
    setVisuals(active);
    if(active.dataset.src){
      audio.src = active.dataset.src;
      audio.load();
    }
    if(timeEl) timeEl.textContent = '0:00 / 0:00';
  }

  function initAll(){
    document.querySelectorAll('.tp-pill-player, .tp-pill-bar').forEach(initPlayer);
  }

  window.TPPillPlayer = { initAll, initPlayer };

  // Initialize on DOM ready
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initAll);
  }else{
    initAll();
  }
})();
