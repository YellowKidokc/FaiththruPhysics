# GTQ Series — Brief for Kimi (Styling + Template)
## From: Opus Session | May 5, 2026

---

## WHAT HAPPENED

The Genesis to Quantum series had 10 main articles and 17 "tangent" sub-articles (labeled 01a, 03b, 03c, etc.). We removed the tangent system entirely. Here's why:

1. **Google was burying the best content.** The letter-suffix naming (01a, 03b) told Google these pages were subordinate footnotes. Some of the "tangents" were actually stronger than the mains. Google ranked them below the parents instead of letting them compete independently.

2. **The Master Story Index requires speakable flow.** The entire site is being structured so every page title weaves into a single spoken paragraph — the site's story from beginning to end. You can't speak "01, 01a, 02, 03, 03a, 03b, 03c" as a narrative. It breaks the rhythm.

3. **Reader confusion.** Nobody knew if tangents were optional, mandatory, or where they fit in the reading order.

## WHAT WE'RE DOING NOW

All 26 articles are numbered sequentially: GTQ-01 through GTQ-26. No letters. No subordination. Every page is equal in Google's eyes and ranks independently.

But we still need readers to know which articles are the **main narrative thread** (the 10 original spine articles) and which are **deep dives** (the 17 former tangents that go deeper on a specific topic).

## THE TWO-TIER VISUAL SYSTEM (what Kimi needs to design)

### Tier 1 — Main Articles (10 articles)
These tell the complete story by themselves. A reader who only reads these gets the full arc.

- Wider layout, more whitespace
- Full treatment: executive summary, blackboard section, kill conditions sidebar, audio dock (the compact one with debate/deep-dive/critique/TTS tabs)
- Hero image or header visual
- Gold accent color (existing brand)
- Navigation at bottom: "Next in series" + "Skip to next main article" (for readers who want the fast path)

**The 10 mains:** 01, 03, 04, 08, 11, 15, 16, 18, 22, 25

### Tier 2 — Deep Dives (16 articles + 1 new Judgment Layer)
These stand alone but visually signal "this goes deeper." Someone landing from Google sees a complete article. Someone reading in sequence sees "I'm in the evidence room now."

- Tighter column, more technical density
- "DEEP DIVE" badge or tag in the header — subtle, not loud
- Different accent color? Maybe teal or silver instead of gold — enough to visually distinguish without breaking the aesthetic
- Same audio dock format where audio exists
- Navigation at bottom: "Back to [parent main article]" + "Continue to next article"
- More equations, more charts, more data — the styling should accommodate heavier technical content

### Both Tiers Share:
- Same dark register (black/near-black backgrounds)
- Same font stack (Inter, Crimson Text, Oswald, JetBrains Mono)
- Same sidebar nav showing the full 26-article series with current position highlighted
- Same MathJax support
- Same responsive behavior

## THE FULL READING ORDER

| # | Title | Tier |
|---|-------|------|
| 01 | The Measurement That Collapsed Reality | MAIN |
| 02 | The Collapse Threshold | Deep Dive |
| 03 | The First Quantum State | MAIN |
| 04 | Free Will in Two Frames | MAIN |
| 05 | MacArthur and the Equation | Deep Dive |
| 06 | The Three Pathways | Deep Dive |
| 07 | Why Did God Drown Everybody? | Deep Dive |
| 08 | The Day Time Began | MAIN |
| 09 | The Decoherence Curve | Deep Dive |
| 10 | How Lies Kill | Deep Dive |
| 11 | The Substrate Fractured | MAIN |
| 12 | The Trinity Mechanism | Deep Dive |
| 13 | The Trinity Timeline | Deep Dive |
| 14 | Why Physics Is Broken in Two | Deep Dive |
| 15 | Why Reality Needs Three | MAIN |
| 16 | The Photon Isn't Watching You Back | MAIN |
| 17 | We Actually Ran the Numbers | Deep Dive |
| 18 | The Eraser and the Cross | MAIN |
| 19 | The Temporal Trap | Deep Dive |
| 20 | How God Restores | Deep Dive |
| 21 | The Science Behind the Restoration | Deep Dive |
| 22 | The Same God in Both Testaments | MAIN |
| 23 | Regime-Dependent Theology | Deep Dive |
| 24 | Societies Die the Same Way People Do | Deep Dive |
| 25 | The Counter-Move | MAIN |
| 26 | Why the Pattern Is the Signal | Deep Dive |

## COMPONENTS EACH ARTICLE NEEDS

1. **Executive Summary** — 3-5 sentences at top, the "if you read nothing else" version
2. **The Article** — the main content body
3. **Kill Conditions** — sidebar or right panel, the falsifiable conditions for this article's claims
4. **Audio Dock** — the compact player bar with tabs: Debate | Deep Dive | Critique | TTS. Only appears on articles that have audio files.
5. **Blackboard** — interactive element (specifics TBD, but reserve space for it)
6. **Video Embed** — where video exists, embedded at top or in a collapsible section
7. **Navigation** — bottom of page: Previous | Next | Skip to Next Main (on Deep Dives)

## WHAT KIMI DELIVERS

Two HTML templates:
1. `template-main.html` — Tier 1 main article template
2. `template-deepdive.html` — Tier 2 deep dive template

Both should be drop-in: replace placeholder content with actual article content, swap the metadata, deploy. The template IS the styling. Once we have these two, we can generate all 26 pages.

## FILES AND LOCATIONS

- Markdown source files: `E:\faiththru Physics\Cannon\genesis-to-quantum\MD\`
- Reading order doc: `E:\faiththru Physics\Cannon\genesis-to-quantum\MD\GTQ_UNIFIED_READING_ORDER_v2.md`
- Existing HTML articles (old template): `E:\faiththru Physics\Cannon\genesis-to-quantum\` and `C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum\`
- Existing template reference: `E:\GTQ\gtq-01-template.html`
- Three Gates document (for Judgment Layer article): `O:\_Theophysics_v5\01_Tik Tok\THREE_GATES_AND_SELF_REFUTATION.md`

## CONTEXT KIMI SHOULD KNOW

- The existing articles use the Adversary-v2 dark register — black backgrounds, gold (#d4af37) accents, Tailwind CSS, MathJax, Font Awesome
- The site is faiththruphysics.com, deployed via Cloudflare
- David works via voice-to-text so all drafts should be expected to have STT artifacts
- The Judgment Layer article (covering Genesis 3 as the origin of moral evaluation, self-refuting arguments, Plantinga's EAAN) will be inserted as a new article — probably GTQ-04 with everything after shifting +1
- This series is the flagship content for the site launch

---

*Prepared by Opus | Session: May 5, 2026 | For Kimi (Moonshot AI)*