# CODEX BUILD PACKAGE — Genesis to Quantum
## Everything needed to batch-build 26 HTML articles
## POF 2828 | May 5, 2026

---

## WHAT THIS IS

This folder contains everything needed to build the entire 26-article Genesis to Quantum series as production HTML pages. Two finished examples are in `examples/` so you can see exactly what the output looks like.

## FOLDER STRUCTURE

```
CODEX_BUILD/
├── README.md                    ← YOU ARE HERE
├── template-main.html           ← The production template (all articles use this)
├── reading-order.md             ← The full 26-article sequence with metadata
├── examples/
│   ├── gtq-01-finished.html     ← Finished MAIN article (reference)
│   └── gtq-02-finished.html     ← Finished DEEP DIVE article (reference)
└── markdown/                    ← All source markdowns + tangents/ + academic/
```

## HOW TO BUILD EACH ARTICLE

1. Copy `template-main.html` → `gtq-XX-slug.html`
2. Find/replace ALL `[[PLACEHOLDER]]` values (list below)
3. Read the matching markdown file from `markdown/`
4. Inject the markdown content (converted to HTML) into the article body section between `<!-- ARTICLE BODY -->` comments
5. Pull the first paragraph as the executive summary
6. Write 2-4 kill conditions based on the article's falsifiable claims
7. Set `class="current"` on the correct sidebar nav link
8. Set the status pill: `Main Article` (gold) or `Deep Dive` (blue)
9. Wire audio dock `data-url` attributes to R2 URLs, or remove `data-url` for missing audio
10. Wire previous/next navigation links

## PLACEHOLDER REFERENCE

```
[[ARTICLE TITLE]]              → e.g., "The Measurement That Collapsed Reality"
[[SUBTITLE / ONE-LINE HOOK]]   → e.g., "One choice collapsed Eden's coherent state"
[[XX]]                         → Article number, zero-padded: 01, 02, ... 26
[[HERO_IMAGE_SRC]]             → WebP image path or leave commented out for placeholder
[[AUDIO_DEEP_SRC]]             → https://r2.faiththruphysics.com/GTQ-XX/audio/deep-dive.mp3
[[AUDIO_READ_SRC]]             → https://r2.faiththruphysics.com/GTQ-XX/audio/read-aloud.mp3
[[AUDIO_DEBATE_SRC]]           → https://r2.faiththruphysics.com/GTQ-XX/audio/debate.mp3
[[PREVIOUS_ARTICLE_HREF]]      → Relative link: gtq-XX-slug.html
[[PREV_TITLE]]                 → Previous article title
[[NEXT_ARTICLE_HREF]]          → Relative link: gtq-XX-slug.html
[[NEXT_TITLE]]                 → Next article title
[[NEXT_MAIN_ARTICLE_HREF]]     → Skip link (deep dives only)
[[NEXT_MAIN_TITLE]]            → Title of next main article
[[MONTH YEAR]]                 → "May 2026"
[[READ_TIME]]                  → Estimated minutes (word count / 250)
```

## AUDIO DOCK

Four pill buttons: Deep Dive, Read Aloud, Debate, Critique.
Each pill has `data-url` attribute pointing to R2.
If MP3 doesn't exist: REMOVE the `data-url` attribute entirely (don't set it to empty string).
The pill will automatically dim and show "Coming Soon."

Audio URL pattern: `https://r2.faiththruphysics.com/GTQ-{OLD_ID}/audio/{type}.mp3`
Example: `https://r2.faiththruphysics.com/GTQ-02/audio/deep-dive.mp3`

Note: R2 uses OLD article IDs (GTQ-01, GTQ-01A, GTQ-02, etc.), not new sequential numbers.

## MAIN vs DEEP DIVE

Main articles (10): 01, 03, 04, 08, 11, 15, 16, 18, 22, 25
Deep dives (16): everything else

Differences:
- Status pill color: Main = gold, Deep Dive = blue  
- Deep dives get "Return to main thread" skip link in bottom nav
- Deep dives have `class="deep-dive"` in sidebar nav (indented with └ prefix)

## THE 26-ARTICLE SEQUENCE

| # | Title | Type | Old ID |
|---|-------|------|--------|
| 01 | The Measurement That Collapsed Reality | MAIN | GTQ-01 |
| 02 | The Collapse Threshold | DEEP | GTQ-01A |
| 03 | The First Quantum State | MAIN | GTQ-02 |
| 04 | Free Will in Two Frames | MAIN | GTQ-03 |
| 05 | MacArthur and the Equation | DEEP | GTQ-03A |
| 06 | The Three Pathways | DEEP | GTQ-03B |
| 07 | Why Did God Drown Everybody? | DEEP | GTQ-03C |
| 08 | The Day Time Began | MAIN | GTQ-04 |
| 09 | The Decoherence Curve | DEEP | GTQ-04A |
| 10 | How Lies Kill | DEEP | GTQ-04B |
| 11 | The Substrate Fractured | MAIN | GTQ-05 |
| 12 | The Trinity Mechanism | DEEP | GTQ-05A |
| 13 | The Trinity Timeline | DEEP | GTQ-05B |
| 14 | Why Physics Is Broken in Two | DEEP | GTQ-05C |
| 15 | Why Reality Needs Three | MAIN | GTQ-06 |
| 16 | The Photon Isn't Watching You Back | MAIN | GTQ-07 |
| 17 | We Actually Ran the Numbers | DEEP | GTQ-07A |
| 18 | The Eraser and the Cross | MAIN | GTQ-08 |
| 19 | The Temporal Trap | DEEP | GTQ-08A |
| 20 | How God Restores | DEEP | GTQ-08B |
| 21 | The Science Behind the Restoration | DEEP | GTQ-08C |
| 22 | The Same God in Both Testaments | MAIN | GTQ-09 |
| 23 | Regime-Dependent Theology | DEEP | GTQ-09A |
| 24 | Societies Die the Same Way People Do | DEEP | GTQ-09B |
| 25 | The Counter-Move | MAIN | GTQ-10 |
| 26 | Why the Pattern Is the Signal | DEEP | GTQ-10A |

## DEPLOYMENT

Output folder: `E:\faiththru Physics\Cannon\genesis-to-quantum\`
Live site: `faiththruphysics.com/genesis-to-quantum/`
R2 bucket: `theophysics` on Cloudflare

## DO NOT MODIFY

- CSS `:root` variables — locked aesthetic
- Sidebar navigation structure — already lists all 26 articles correctly
- Sticky tab bar — order is final
- Audio dock JS engine — self-contained, just wire data-url attributes
- Sticky corner mini-player — automatic, zero config
- Footer equation — canonical
