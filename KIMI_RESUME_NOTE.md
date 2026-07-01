# Kimi Resume Note — left while rebooting Kimmy

**Date:** 2026-06-30
**Left off just before starting the first edit pass.**

## Current direction

User asked me to pick up the website lane with these priorities:

1. **Build/upgrade Tier 2 series landing pages** using `moral-decline/index.html` as reference.
   - First targets: `one-page-stories`, `genesis-to-quantum`, `consciousness`.
   - Model: series landing page → **video first** → real summary → chapter/article links → audio options carried across pages.
2. **Fill missing metadata layers** on pages that already render.
   - First targets: `consciousness`, `revolution-of-truth`.
   - Look for: missing domain profiles, missing reading-ladder state, missing MTL metadata, empty/under-described pages.
3. **Add real supporting images** to `mda`, `moral-decline`, `logos-papers`.
4. **Tighten subdomain shell consistency** for `equation`, `glossary`, `lean4`, `media`, `podcast`, `proof-explorer`, `rigor`.

Guardrails given:
- Do not flatten or redesign the whole site.
- Do not redo the shell unless there is a real bug.
- Do not break root-relative links.
- Preserve existing voice and design language.
- Prefer forward-only improvements.
- Work from the current site structure, not old assumptions about `Python-WEB`.

## What I was about to do first

Start with **Consciousness**:
- Edit `consciousness/index.html`:
  - Move the video section to the top (right after the hero).
  - Add a polished, multi-paragraph series summary.
  - Keep the chapter/article list and links.
  - Add a visible audio/podcast anchor section (series-level deep dive, etc.).
- Inject `article-meta` JSON into all 10 `consciousness-*.html` article pages using the existing NLP summaries at `D:\GitHub\faiththruphysics-site-data\_summaries\by-source\consciousness\root\*.summary.json`.
  - Include `classification` with colors, `reading_levels`, `reading_level`, `audio_api`, `series`, `slug`, `title`, and `prev`/`next` where obvious.

## Audio/video mapping notes

- Source material lives under `D:\GitHub\faiththruphysics-site-data`.
- **Consciousness** series audio is clear: `assets/OUTBOX/consciousness-INDEX.mp3` = series-level deep dive; per-article `*.canonical.mp3` = article-level deep dive. No debate/critique labels found, so treat as Deep Dive only unless user clarifies.
- **Genesis to Quantum** has many videos in `genesis-to-quantum/Video/` and audio in `genesis-to-quantum/audio/`. Some naming maps directly to chapters.
- **One-Page Stories** has videos inside each subfolder (`starting-point`, `Math all`, `Templeton`, etc.) and many NotebookLM voiceover files under `notebooklm/`.
- Several folders have ambiguous or duplicate audio files — I was going to flag those rather than guess.

## Key references already read

- `D:\GitHub\faiththruphysics-site\MUST DO\SITE_STRUCTURE_SPEC.md`
- `D:\GitHub\faiththruphysics-site\MUST DO\PAGE-SHELL-GOLD-STANDARD\WORKSPACE_CHECKIN_2026-06-29.md`
- `D:\GitHub\faiththruphysics-site\NOTE-FROM-KIMI.md`
- `D:\GitHub\faiththruphysics-site\COORDINATION_NOTE.md`
- `D:\GitHub\faiththruphysics-site\site-shell\frame.js` (reads `article-meta` / `page-profile` for top bar + bottom dock)

## Next steps after Consciousness

1. `one-page-stories/index.html` — convert to MDA-reference Tier 2 landing page.
2. `genesis-to-quantum/index.html` — restructure to video-first + real summary + article list + audio wiring.
3. `revolution-of-truth/drv-*.html` — add domain/reading-ladder metadata manually (no NLP summaries exist).
4. Images pass for `mda`, `moral-decline`, `logos-papers`.
5. Subdomain shell audit for `equation`, `glossary`, `lean4`, `media`, `podcast`, `proof-explorer`, `rigor`.

## One blocker to keep in mind

The **Math Translation Layer (MTL)** metadata is missing on Consciousness and Revolution-of-Truth pages. Full per-equation translations will need a dedicated pass; for now the priority is domain profiles, reading-ladder state, and audio wiring.
