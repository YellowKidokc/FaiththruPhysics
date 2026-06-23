(function () {
  "use strict";

  function formatTime(seconds) {
    if (!Number.isFinite(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  function attach(dock, audio, state) {
    if (!dock || !audio) return null;

    const player = document.createElement("div");
    player.className = "tp-sticky-player tp-theme";
    player.dataset.theme = dock.closest(".tp-theme")?.dataset.theme || dock.dataset.theme || "light";
    player.setAttribute("aria-label", "Sticky audio player");
    player.innerHTML = [
      '<button class="tp-mini-button" type="button" aria-label="Play audio">Play</button>',
      '<div class="tp-mini-meta">',
      '<div class="tp-mini-track">Read aloud</div>',
      '<div class="tp-mini-time">0:00 / 0:00</div>',
      '</div>',
      '<div class="tp-mini-speed">1x</div>'
    ].join("");

    document.body.appendChild(player);

    const button = player.querySelector(".tp-mini-button");
    const track = player.querySelector(".tp-mini-track");
    const time = player.querySelector(".tp-mini-time");
    const speed = player.querySelector(".tp-mini-speed");

    function sync() {
      button.textContent = audio.paused ? "Play" : "Pause";
      button.setAttribute("aria-label", audio.paused ? "Play audio" : "Pause audio");
      track.textContent = state?.label || "Read aloud";
      time.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
      speed.textContent = `${audio.playbackRate || 1}x`;
    }

    button.addEventListener("click", () => {
      if (audio.paused) audio.play().catch(() => {});
      else audio.pause();
    });

    ["play", "pause", "timeupdate", "loadedmetadata", "ratechange"].forEach((name) => {
      audio.addEventListener(name, sync);
    });

    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0];
      player.classList.toggle("is-visible", !entry.isIntersecting);
    }, { threshold: 0.05 });
    observer.observe(dock);
    sync();

    return { player, sync, disconnect: () => observer.disconnect() };
  }

  window.TPStickyPlayer = { attach };
})();
