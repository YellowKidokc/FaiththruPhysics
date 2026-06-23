(function () {
  "use strict";

  const TRACKS = [
    { key: "read_aloud", apiKeys: ["read_aloud", "tts", "tts-athena", "voice-sample-athena"], label: "Read aloud" },
    { key: "deep_dive", apiKeys: ["deep_dive", "deep", "deep-dive"], label: "Deep dive" },
    { key: "debate", apiKeys: ["debate"], label: "Debate" },
    { key: "critique", apiKeys: ["critique"], label: "Critique", optional: true }
  ];

  function slugUrl(slug) {
    return slug ? `/${slug}/` : "#";
  }

  function formatTime(seconds) {
    if (!Number.isFinite(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  function trackMapFromApi(data) {
    const map = {};
    const tracks = Array.isArray(data?.tracks) ? data.tracks : [];
    tracks.forEach((track) => {
      if (track.mode) map[track.mode] = track.url || track.src || "";
      if (track.kind) map[track.kind] = track.url || track.src || "";
    });
    if (data?.audio && typeof data.audio === "object") {
      Object.assign(map, data.audio);
    }
    return map;
  }

  function sourceFor(track, meta, apiMap) {
    const localAudio = meta.audio && typeof meta.audio === "object" ? meta.audio : {};
    for (const key of track.apiKeys) {
      if (apiMap[key]) return apiMap[key];
      if (localAudio[key]) return localAudio[key];
    }
    return "";
  }

  async function loadApiAudio(meta) {
    if (!meta.slug || !meta.audio_api) return {};
    try {
      const res = await fetch(`${meta.audio_api}?slug=${encodeURIComponent(meta.slug)}`);
      if (!res.ok) return {};
      return trackMapFromApi(await res.json());
    } catch (error) {
      return {};
    }
  }

  function render(target, meta) {
    const root = typeof target === "string" ? document.querySelector(target) : target;
    if (!root) return null;

    const data = meta || {};
    const theme = root.dataset.theme || data.theme || "light";
    root.className = "tp-bottom-bar tp-theme";
    root.dataset.theme = theme;
    root.innerHTML = "";

    const audio = document.createElement("audio");
    audio.preload = "metadata";

    const state = { label: "Read aloud" };
    const inner = document.createElement("div");
    inner.className = "tp-bottom-inner";

    const dock = document.createElement("div");
    dock.className = "tp-audio-dock";
    dock.id = root.id ? `${root.id}-audio-dock` : "tp-audio-dock";

    const buttonWrap = document.createElement("div");
    buttonWrap.className = "tp-audio-buttons";
    buttonWrap.setAttribute("aria-label", "Audio tracks");

    const status = document.createElement("div");
    status.className = "tp-audio-status";
    status.textContent = "0:00 / 0:00";

    const speedWrap = document.createElement("div");
    speedWrap.className = "tp-speed-group";
    speedWrap.setAttribute("aria-label", "Playback speed");
    [1, 1.5, 2].forEach((rate) => {
      const button = document.createElement("button");
      button.className = "tp-speed-button";
      button.type = "button";
      button.dataset.speed = String(rate);
      button.setAttribute("aria-pressed", rate === 1 ? "true" : "false");
      button.textContent = `${rate}x`;
      button.addEventListener("click", () => {
        audio.playbackRate = rate;
        speedWrap.querySelectorAll(".tp-speed-button").forEach((item) => {
          item.setAttribute("aria-pressed", item === button ? "true" : "false");
        });
      });
      speedWrap.appendChild(button);
    });

    function selectTrack(button, autoplay) {
      buttonWrap.querySelectorAll(".tp-audio-button").forEach((item) => {
        item.setAttribute("aria-pressed", item === button ? "true" : "false");
      });
      state.label = button.textContent || "Audio";
      if (button.dataset.src) {
        const wasPlaying = !audio.paused;
        if (audio.src !== button.dataset.src) {
          audio.src = button.dataset.src;
          audio.load();
        }
        if (autoplay || wasPlaying) audio.play().catch(() => {});
      }
      document.dispatchEvent(new CustomEvent("tp:audio-track-change", { detail: { track: button.dataset.track } }));
    }

    const visibleTracks = TRACKS.filter((track) => {
      if (!track.optional) return true;
      return data.audio?.critique !== null;
    });
    visibleTracks.forEach((track, index) => {
      const button = document.createElement("button");
      button.className = "tp-audio-button";
      button.type = "button";
      button.dataset.track = track.key;
      button.setAttribute("aria-pressed", index === 0 ? "true" : "false");
      button.textContent = track.label;
      button.addEventListener("click", () => selectTrack(button, true));
      buttonWrap.appendChild(button);
    });

    dock.append(buttonWrap, status, speedWrap);

    const nav = document.createElement("nav");
    nav.className = "tp-article-nav";
    nav.setAttribute("aria-label", "Article navigation");
    const prev = data.prev || {};
    const next = data.next || {};
    const position = [data.series_order, data.series_total].filter(Boolean).join(" of ");

    const prevLink = document.createElement("a");
    prevLink.className = "tp-nav-link tp-nav-prev";
    prevLink.href = slugUrl(prev.slug);
    prevLink.textContent = prev.title ? `\u2190 ${prev.title}` : "";

    const positionEl = document.createElement("span");
    positionEl.className = "tp-nav-position";
    positionEl.textContent = position || "";

    const nextLink = document.createElement("a");
    nextLink.className = "tp-nav-link tp-nav-next";
    nextLink.href = slugUrl(next.slug);
    nextLink.textContent = next.title ? `${next.title} \u2192` : "";

    nav.append(prevLink, positionEl, nextLink);

    inner.append(dock, nav, audio);
    root.appendChild(inner);

    audio.addEventListener("timeupdate", () => {
      status.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
    });
    audio.addEventListener("loadedmetadata", () => {
      status.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
    });

    loadApiAudio(data).then((apiMap) => {
      buttonWrap.querySelectorAll(".tp-audio-button").forEach((button) => {
        const track = TRACKS.find((item) => item.key === button.dataset.track);
        button.dataset.src = sourceFor(track, data, apiMap);
      });
      const first = buttonWrap.querySelector(".tp-audio-button");
      if (first) selectTrack(first, false);
    });

    if (window.TPStickyPlayer) {
      window.TPStickyPlayer.attach(dock, audio, state);
    }

    return root;
  }

  window.TPBottomBar = { render };
})();
