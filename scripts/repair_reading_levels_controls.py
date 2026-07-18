from __future__ import annotations

import argparse
from pathlib import Path


TARGET_RELATIVE = Path("components") / "reading-levels.js"

REPAIRED_JS = r"""(function () {
  'use strict';

  const DEFAULT = 'college';
  const STORAGE_KEY = 'tpReadingLevel';

  const SYSTEMS = [
    {
      buttonSelector: '.tp-level[data-level]',
      panelSelector: '.tp-level-panel[data-reading-level]',
      panelLevel: panel => panel.dataset.readingLevel,
      containers: ['.tp-levels', '.mtl-reader-tabs'],
    },
    {
      buttonSelector: '.ftp-level[data-level]',
      panelSelector: '.ftp-reader-layer[data-reader-layer]',
      panelLevel: panel => panel.dataset.readerLayer,
      containers: ['#ftpReadingLevels', '.ftp-levels'],
    },
  ];

  function unique(items) {
    return Array.from(new Set(items.filter(Boolean)));
  }

  function setHidden(el, hidden) {
    if (!el) return;
    el.hidden = hidden;
    el.setAttribute('aria-hidden', hidden ? 'true' : 'false');
    el.dataset.readingLevelsAvailable = hidden ? 'false' : 'true';
  }

  function controlContainers(buttons, selectors) {
    const containers = [];
    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => containers.push(el));
    });
    buttons.forEach(button => {
      const local = button.closest('[role="tablist"], .tp-levels, .ftp-levels, .mtl-reader-tabs');
      if (local) containers.push(local);
    });
    return unique(containers);
  }

  function availablePanels(system) {
    return Array.from(document.querySelectorAll(system.panelSelector)).filter(panel => {
      const level = system.panelLevel(panel);
      return level && panel.textContent.trim();
    });
  }

  function setLevel(system, level) {
    const panels = availablePanels(system);
    const buttons = Array.from(document.querySelectorAll(system.buttonSelector));
    if (!panels.length) return false;

    const available = new Set(panels.map(panel => system.panelLevel(panel)));
    const activeLevel = available.has(level) ? level : (available.has(DEFAULT) ? DEFAULT : panels[0] && system.panelLevel(panels[0]));
    if (!activeLevel) return false;

    buttons.forEach(btn => {
      const btnLevel = btn.dataset.level;
      const exists = available.has(btnLevel);
      const on = btnLevel === activeLevel;
      btn.hidden = !exists;
      btn.disabled = !exists;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-selected', on ? 'true' : 'false');
      btn.setAttribute('aria-disabled', exists ? 'false' : 'true');
    });

    panels.forEach(panel => {
      const on = system.panelLevel(panel) === activeLevel;
      panel.hidden = !on;
      panel.classList.toggle('active', on);
    });

    document.body.dataset.readingLevel = activeLevel;
    try { localStorage.setItem(STORAGE_KEY, activeLevel); } catch (e) { /* ignore */ }
    return true;
  }

  function initSystem(system) {
    const buttons = Array.from(document.querySelectorAll(system.buttonSelector));
    if (!buttons.length) return false;

    const panels = availablePanels(system);
    const levels = unique(panels.map(panel => system.panelLevel(panel)));
    const containers = controlContainers(buttons, system.containers);

    if (levels.length <= 1) {
      containers.forEach(container => setHidden(container, true));
      if (levels.length === 1) setLevel(system, levels[0]);
      return false;
    }

    containers.forEach(container => setHidden(container, false));
    buttons.forEach(btn => {
      btn.addEventListener('click', () => setLevel(system, btn.dataset.level));
    });

    let saved = DEFAULT;
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      if (value && levels.includes(value)) saved = value;
    } catch (e) { /* ignore */ }

    setLevel(system, saved);
    return true;
  }

  function init() {
    SYSTEMS.forEach(initSystem);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hide dead reading-level controls and support both tp and ftp shells."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    target = args.root / TARGET_RELATIVE
    if not target.exists():
        raise SystemExit(f"Missing target: {target}")

    current = target.read_text(encoding="utf-8")
    if current == REPAIRED_JS:
        print(f"UNCHANGED {target}")
        return 0

    print(f"{'APPLY' if args.apply else 'DRY'} {target}")
    print("Fix: hide reading controls when no real switchable reading layers exist.")
    print("Fix: support legacy .tp-level panels and canonical .ftp-reader-layer panels.")

    if args.apply:
        target.write_text(REPAIRED_JS, encoding="utf-8", newline="\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
