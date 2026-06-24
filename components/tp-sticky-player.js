(function () {
  "use strict";

  function attach(dock, audio, state) {
    if (!dock || !audio) return null;

    const player = document.createElement("div");
    player.className = "tp-sticky-player tp-theme";
    player.dataset.theme = dock.closest(".tp-theme")?.dataset.theme || dock.dataset.theme || "light";
    player.setAttribute("aria-label", "Sticky audio player");
    player.innerHTML = [
      '<button class="tp-mini-button" type="button" aria-label="Play audio">Play</button>',
      '<div class="tp-mini-track">Read aloud</div>'
    ].join("");

    document.body.appendChild(player);

    const button = player.querySelector(".tp-mini-button");
    const track = player.querySelector(".tp-mini-track");

    function sync() {
      button.textContent = audio.paused ? "Play" : "Pause";
      button.setAttribute("aria-label", audio.paused ? "Play audio" : "Pause audio");
      track.textContent = state?.label || "Read aloud";
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
