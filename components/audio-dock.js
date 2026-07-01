/* ═══════════════════════════════════════════════════════════════
   COMPONENT: audio-dock
   Self-initializing sticky audio player.

   Markup:
   <div class="audio-dock" data-audio-dock>
     <div class="dock-pills">
       <button class="dock-pill" data-dock-src="URL" data-dock-label="Story">Story</button>
       <button class="dock-pill" data-dock-src="URL" data-dock-label="Deep">Deep</button>
     </div>
     <div class="dock-body"> …auto-rendered if omitted… </div>
   </div>
   <div class="dock-mini" data-audio-dock-mini></div>

   Or initialize manually:
   AudioDock.init({ container: el, mini: miniEl, tracks: [...] });
   ═══════════════════════════════════════════════════════════════ */

(function (global) {
  'use strict';

  const ACCENT = '#d4af37';
  const API_AUDIO = 'https://faith-audio-pipeline.davidokc28.workers.dev/api/audio';
  const API_TRACK_DEFS = [
    { modes: ['tts', 'read_aloud', 'read'], label: 'Read Aloud', dockMode: 'read' },
    { modes: ['deep', 'deep_dive', 'deep-dive'], label: 'Deep Dive', dockMode: 'deep' },
    { modes: ['podcast', 'debate'], label: 'Podcast', dockMode: 'debate' },
    { modes: ['critique'], label: 'Critique', dockMode: 'critique', optional: true }
  ];

  function trackMapFromApi(data) {
    const map = {};
    (data?.tracks || []).forEach(t => {
      if (t.mode) map[t.mode] = t.url || t.src || '';
      if (t.is_default) map.__default__ = t.url || t.src || '';
    });
    return map;
  }

  function resolveTrackUrl(def, artMap, serMap) {
    for (const mode of def.modes) {
      if (artMap[mode]) return artMap[mode];
    }
    for (const mode of def.modes) {
      if (serMap[mode]) return serMap[mode];
    }
    if (def.dockMode === 'read') {
      return artMap.__default__ || serMap.__default__ || '';
    }
    return '';
  }

  async function populateDockFromApi(container) {
    const lookup = container.dataset.audioLookup
      || (container.dataset.audioSlug ? `${API_AUDIO}?slug=${encodeURIComponent(container.dataset.audioSlug)}` : '');
    const seriesLookup = container.dataset.seriesLookup
      || (container.dataset.seriesSlug ? `${API_AUDIO}?slug=${encodeURIComponent(container.dataset.seriesSlug)}` : '');
    if (!lookup) return [];

    const [articleData, seriesData] = await Promise.all([
      fetch(lookup).then(r => r.ok ? r.json() : { tracks: [] }).catch(() => ({ tracks: [] })),
      seriesLookup && seriesLookup !== lookup
        ? fetch(seriesLookup).then(r => r.ok ? r.json() : { tracks: [] }).catch(() => ({ tracks: [] }))
        : Promise.resolve({ tracks: [] })
    ]);

    const artMap = trackMapFromApi(articleData);
    const serMap = trackMapFromApi(seriesData);
    let pillsWrap = container.querySelector('.dock-pills');
    if (!pillsWrap) {
      pillsWrap = document.createElement('div');
      pillsWrap.className = 'dock-pills';
      container.prepend(pillsWrap);
    }
    pillsWrap.innerHTML = '';

    const tracks = [];
    let idx = 0;
    API_TRACK_DEFS.forEach(def => {
      const url = resolveTrackUrl(def, artMap, serMap);
      if (!url && def.optional) return;
      const pill = document.createElement('button');
      pill.type = 'button';
      pill.className = 'dock-pill' + (url ? '' : ' unavailable');
      pill.dataset.dockIndex = String(idx);
      pill.dataset.dockSrc = url || '';
      pill.dataset.dockLabel = def.label;
      pill.dataset.dockMode = def.dockMode;
      pill.innerHTML = `<span class="pill-dot"></span>${def.label}`;
      if (!url) pill.disabled = true;
      pillsWrap.appendChild(pill);
      if (url) {
        tracks.push({ index: idx, src: url, label: def.label, mode: def.dockMode, el: pill });
      }
      idx += 1;
    });
    return tracks;
  }

  function fmtTime(s) {
    if (!s || !isFinite(s)) return '0:00';
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60).toString().padStart(2, '0');
    return `${m}:${sec}`;
  }

  class AudioDock {
    constructor(options) {
      this.container = options.container;
      this.mini = options.mini || null;
      this.tracks = options.tracks || this._readTracksFromMarkup();
      this.audio = new Audio();
      this.audio.preload = 'metadata';
      this.activeIndex = -1;
      this.muted = false;
      this._pendingSeek = null;

      this._build();
      this._bind();
      this._selectFirstAvailable();
    }

    static init(options) {
      return new AudioDock(options);
    }

    _readTracksFromMarkup() {
      const pills = [...this.container.querySelectorAll('.dock-pill[data-dock-src], [data-dock-src]')];
      return pills.map((el, i) => ({
        index: i,
        src: el.dataset.dockSrc,
        label: el.dataset.dockLabel || el.textContent.trim(),
        mode: el.dataset.dockMode || el.textContent.trim().toLowerCase().replace(/\s+/g, '-'),
        el
      })).filter(t => t.src);
    }

    _build() {
      // Ensure pills container exists
      let pillsWrap = this.container.querySelector('.dock-pills');
      if (!pillsWrap) {
        pillsWrap = document.createElement('div');
        pillsWrap.className = 'dock-pills';
        this.container.prepend(pillsWrap);
      }
      this.pillsWrap = pillsWrap;

      // If pills are already in markup, sync with tracks
      if (this.tracks.length && !this.container.querySelector('.dock-pill')) {
        pillsWrap.innerHTML = this.tracks.map(t =>
          `<button class="dock-pill" type="button" data-dock-index="${t.index}" data-dock-src="${t.src}" data-dock-label="${this._esc(t.label)}" data-dock-mode="${this._esc(t.mode)}">
             <span class="pill-dot"></span>${this._esc(t.label)}
           </button>`
        ).join('');
      }

      // Ensure body exists
      let body = this.container.querySelector('.dock-body');
      if (!body) {
        body = document.createElement('div');
        body.className = 'dock-body';
        body.innerHTML = `
          <button class="dock-play" type="button" aria-label="Play or pause"><i class="fas fa-play"></i></button>
          <div class="dock-track-wrap">
            <div class="dock-track"><div class="dock-fill"></div></div>
            <div class="dock-times"><span class="dock-current">0:00</span><span class="dock-duration">0:00</span></div>
          </div>
          <button class="dock-vol" type="button" aria-label="Mute or unmute"><i class="fas fa-volume-up"></i></button>
          <select class="dock-speed" aria-label="Playback speed">
            <option value="0.75">0.75x</option>
            <option value="1" selected>1x</option>
            <option value="1.25">1.25x</option>
            <option value="1.5">1.5x</option>
            <option value="1.75">1.75x</option>
            <option value="2">2x</option>
          </select>
        `;
        this.container.append(body);
      }
      this.body = body;

      // Ensure empty state exists
      let empty = this.container.querySelector('.dock-empty');
      if (!empty) {
        empty = document.createElement('div');
        empty.className = 'dock-empty';
        empty.innerHTML = '<i class="fas fa-clock" style="margin-right:.5rem;"></i> Audio coming soon';
        this.container.append(empty);
      }
      this.empty = empty;

      this.playBtn = body.querySelector('.dock-play');
      this.playIcon = this.playBtn ? this.playBtn.querySelector('i') : null;
      this.trackEl = body.querySelector('.dock-track');
      this.fillEl = body.querySelector('.dock-fill');
      this.curEl = body.querySelector('.dock-current');
      this.durEl = body.querySelector('.dock-duration');
      this.volBtn = body.querySelector('.dock-vol');
      this.speedEl = body.querySelector('.dock-speed');

      // Mini widget
      const simpleMini = this.mini && (
        this.mini.classList.contains('dock-mini-simple')
        || this.mini.dataset.dockMiniStyle === 'simple'
        || this.container.dataset.dockMiniStyle === 'simple'
      );
      if (this.mini && !this.mini.querySelector('.mini-play')) {
        if (simpleMini) {
          this.mini.classList.add('dock-mini-simple');
          this.mini.innerHTML = `
            <button class="mini-play" type="button" aria-label="Play or pause"><i class="fas fa-play"></i></button>
          `;
        } else {
          this.mini.innerHTML = `
            <button class="mini-play" type="button" aria-label="Play or pause"><i class="fas fa-play"></i></button>
            <div class="mini-label">
              <span class="mini-mode">Audio</span>
              <span class="mini-title">Choose a track</span>
            </div>
          `;
        }
      }
      if (this.mini) {
        this.miniPlay = this.mini.querySelector('.mini-play');
        this.miniIcon = this.miniPlay ? this.miniPlay.querySelector('i') : null;
        this.miniMode = this.mini.querySelector('.mini-mode');
        this.miniTitle = this.mini.querySelector('.mini-title');
      }
    }

    _esc(str) {
      return String(str || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    _selectFirstAvailable() {
      if (!this.tracks.length) {
        this.body.classList.add('hidden');
        this.empty.classList.add('visible');
        return;
      }
      this._selectTrack(0);
    }

    _selectTrack(index, autoplay = false) {
      const track = this.tracks[index];
      if (!track) return;

      const wasPlaying = !this.audio.paused;
      this.audio.pause();
      this.activeIndex = index;
      this.audio.src = track.src;
      this.audio.playbackRate = parseFloat(this.speedEl ? this.speedEl.value : 1) || 1;

      // UI state
      [...this.pillsWrap.querySelectorAll('.dock-pill')].forEach(p => p.classList.remove('active'));
      const pill = this.pillsWrap.querySelector(`[data-dock-index="${index}"]`) || track.el;
      if (pill) pill.classList.add('active');

      this._updateLabel(track);
      this.body.classList.remove('hidden');
      this.empty.classList.remove('visible');

      if (autoplay || wasPlaying) {
        this.audio.play().catch(() => {});
      } else {
        this._setIcons(true);
      }
    }

    _updateLabel(track) {
      if (this.miniMode) this.miniMode.textContent = track.mode || track.label;
      if (this.miniTitle) this.miniTitle.textContent = track.label;
    }

    _setIcons(paused) {
      const icon = paused ? 'fa-play' : 'fa-pause';
      if (this.playIcon) this.playIcon.className = `fas ${icon}`;
      if (this.miniIcon) this.miniIcon.className = `fas ${icon}`;
      if (this.playBtn) this.playBtn.classList.toggle('playing', !paused);
    }

    _toggle() {
      if (!this.audio.src) return;
      if (this.audio.paused) this.audio.play().catch(() => {});
      else this.audio.pause();
    }

    _seek(e) {
      if (!this.audio.duration) return;
      const rect = this.trackEl.getBoundingClientRect();
      const p = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      this.audio.currentTime = p * this.audio.duration;
    }

    _bind() {
      // Pills
      this.pillsWrap.addEventListener('click', e => {
        const pill = e.target.closest('.dock-pill');
        if (!pill) return;
        const idx = Number(pill.dataset.dockIndex);
        if (Number.isNaN(idx)) return;
        const isSame = idx === this.activeIndex;
        if (isSame) this._toggle();
        else this._selectTrack(idx, true);
      });

      // Controls
      if (this.playBtn) this.playBtn.addEventListener('click', () => this._toggle());
      if (this.miniPlay) this.miniPlay.addEventListener('click', () => this._toggle());
      if (this.trackEl) this.trackEl.addEventListener('click', e => this._seek(e));
      if (this.speedEl) this.speedEl.addEventListener('change', () => { this.audio.playbackRate = parseFloat(this.speedEl.value) || 1; });
      if (this.volBtn) this.volBtn.addEventListener('click', () => {
        this.muted = !this.muted;
        this.audio.muted = this.muted;
        this.volBtn.innerHTML = this.muted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>';
      });

      // Audio events
      this.audio.addEventListener('play', () => this._setIcons(false));
      this.audio.addEventListener('pause', () => this._setIcons(true));
      this.audio.addEventListener('ended', () => this._setIcons(true));
      this.audio.addEventListener('timeupdate', () => {
        if (!this.audio.duration) return;
        if (this.fillEl) this.fillEl.style.width = `${(this.audio.currentTime / this.audio.duration) * 100}%`;
        if (this.curEl) this.curEl.textContent = fmtTime(this.audio.currentTime);
      });
      this.audio.addEventListener('loadedmetadata', () => {
        if (this.durEl) this.durEl.textContent = fmtTime(this.audio.duration);
      });

      // Mini visibility — show corner box when main dock scrolls out of view
      if (this.mini) {
        const observer = new IntersectionObserver(entries => {
          const visible = entries[0].isIntersecting;
          const show = !visible && !!this.audio.src;
          this.mini.classList.toggle('visible', show);
          this.mini.setAttribute('aria-hidden', String(!show));
        }, { threshold: 0.1 });
        observer.observe(this.container);
      }
    }
  }

  // Auto-init every .audio-dock on the page
  async function autoInit() {
    const containers = [...document.querySelectorAll('[data-audio-dock]')];
    for (const container of containers) {
      const mini = container.dataset.audioDockMini
        ? document.querySelector(container.dataset.audioDockMini)
        : document.querySelector('[data-audio-dock-mini]');
      let tracks = null;
      if (container.dataset.audioLookup || container.dataset.audioSlug) {
        tracks = await populateDockFromApi(container);
      }
      new AudioDock({ container, mini, tracks: tracks || undefined });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoInit);
  } else {
    autoInit();
  }

  global.AudioDock = AudioDock;
})(window);
