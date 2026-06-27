# Note from Kimi — 2026-06-26

## Done today
- Built a ubiquitous site frame (top bar + bottom audio dock).
  - Files: `site-shell/frame.js`, `prototypes/ubiquitous-frame.html`
- Applied the frame to **~1,200 HTML pages** across the site.
- Fixed a color-stripping bug caused by the legacy-UI stripper removing whole `<style>` blocks.
- The frame now reads existing `article-meta` data:
  - Domain percentages/colors for the top bar.
  - `reading_level` to set the active ladder tab.
- Legacy MDA top bars and audio players were removed; the new frame replaces them.

## Current files
- `site-shell/frame.js` — the live shell script.
- `Python-WEB/apply_site_frame.py` — script used to inject the frame.
- `prototypes/ubiquitous-frame.html` — standalone design prototype.

## Next up (whenever you’re ready)
1. Add images to MDA pages.
2. Fill domain profiles / reading-ladder layers / math-translation layers for pages that don’t have them.
3. Finish audio API/worker integration.
4. Build out subdomain shells (equation, glossary, isomorphism, lean4, media, podcast, proof-explorer, rigor).

Get some sleep — we can pick this up tomorrow.
