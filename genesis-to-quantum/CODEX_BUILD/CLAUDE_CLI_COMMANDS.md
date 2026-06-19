# CLAUDE CLI COMMAND LINES — Genesis to Quantum Build
# POF 2828 | May 5, 2026
# Run these in order. Each one is a separate Claude Code session.

---

## COMMAND LINE 1 — Build GTQ-01 (the reference article)

```
Read the template at "E:\faiththru Physics\Cannon\genesis-to-quantum\template-main.html" and the article markdown at "E:\GTQ\GTQ_01_Why_Time_Is_Grace.md" (361 lines of clean markdown). Build a finished production HTML page.

Hero image: "E:\faiththru Physics\Cannon\genesis-to-quantum\images\series-opener.png" — goes in the hero-main panel.
Hero side panel LEFT: Executive summary — pull from the first 2 paragraphs of the article (the "Two observers" section). Make it 3-4 sentences.
Hero side panel RIGHT: Core kill condition — "Kill if: any single measurement in standard QM should collapse a wavefunction regardless of observer identity. The Eve-Adam asymmetry requires a new principle."

Tab order: Executive Summary tab shows FIRST (set it as active instead of "The Paper"). The Paper tab has the full article. Rigor & Kill Conditions tab gets content from the "The Audit" section at the bottom of the markdown (three tiers: load-bearing, suggestive, carried away). Blackboard tab gets the Master Equation and the moral superposition equation from the article.

Audio dock: Read Aloud pill → "E:\faiththru Physics\Cannon\genesis-to-quantum\audio\GTQ_01_Why_Time_Is_Grace.mp3". Deep Dive pill → no data-url (coming soon). Debate pill → no data-url. Critique pill → no data-url. Use relative paths assuming the audio folder is at ../audio/ from the HTML file.

Slide images from "E:\faiththru Physics\Cannon\genesis-to-quantum\images\gtq-01\slide_01.webp" through slide_15.webp — inject one slide image between each major section (## heading) as a figure with caption.

Navigation: No previous (this is article 01). Next = "gtq-02-collapse-threshold.html" title "The Collapse Threshold". Next main = "gtq-03-first-quantum-state.html" title "The First Quantum State". Set class="current" on article 01 in the sidebar.

Status pill: "Main Article" (gold).

Output to: "E:\faiththru Physics\Cannon\genesis-to-quantum\CODEX_BUILD\examples\gtq-01-finished.html"
Also copy to: "E:\faiththru Physics\Cannon\genesis-to-quantum\gtq-01-measurement-collapsed-reality.html"
```

---

## COMMAND LINE 2 — Build GTQ-02 deep dive (the second reference)

```
Using the same template at "E:\faiththru Physics\Cannon\genesis-to-quantum\template-main.html", build GTQ-02 "The Collapse Threshold" from the markdown at "E:\GTQ\GTQ_01A_Collapse_Threshold.md".

This is a DEEP DIVE article. Change the status pill to: <span class="status-pill" style="background:rgba(74,158,255,.12);color:#4a9eff;">Deep Dive</span>

Hero image: "E:\faiththru Physics\Cannon\genesis-to-quantum\images\gtq-01a.webp"
Hero side LEFT: Summary of what this deep dive adds to the parent article.
Hero side RIGHT: Key kill condition from the article content.

Tab order: Executive Summary first (active), then The Paper, then Rigor, then Blackboard.

Audio: "E:\faiththru Physics\Cannon\genesis-to-quantum\audio\GTQ_01A_Collapse_Threshold.mp3" for Read Aloud pill. Others → no data-url.

Navigation: Previous = "gtq-01-measurement-collapsed-reality.html" title "The Measurement That Collapsed Reality". Next = "gtq-03-first-quantum-state.html" title "The First Quantum State". Add a "Return to main thread" skip link pointing to gtq-03.

Sidebar: Set class="current" on article 02.

Output to: "E:\faiththru Physics\Cannon\genesis-to-quantum\CODEX_BUILD\examples\gtq-02-finished.html"
Also copy to: "E:\faiththru Physics\Cannon\genesis-to-quantum\gtq-02-collapse-threshold.html"
```

---

## COMMAND LINE 3 — Batch build remaining 24 articles

```
Read the two finished examples at "E:\faiththru Physics\Cannon\genesis-to-quantum\CODEX_BUILD\examples\gtq-01-finished.html" and "gtq-02-finished.html". These are your reference for exactly how articles should look.

Read the full article sequence from "E:\faiththru Physics\Cannon\genesis-to-quantum\CODEX_BUILD\reading-order.md".

Read the template at "E:\faiththru Physics\Cannon\genesis-to-quantum\template-main.html".

For articles 03 through 26, the source markdowns are at "E:\GTQ\" with the filenames listed in reading-order.md (the "Source MD" column). Read each one.

For each article:
1. Copy the template
2. Inject the markdown content (convert to HTML) into the article body
3. Pull the executive summary from the first 1-2 paragraphs
4. Write 2-4 kill conditions from the article's claims (look for "audit" sections if they exist, otherwise identify the falsifiable claims)
5. Set hero side panels: LEFT = summary, RIGHT = primary kill condition
6. Wire audio: check "E:\faiththru Physics\Cannon\genesis-to-quantum\audio\" for matching MP3 files. The naming pattern is GTQ_XX_Title.mp3. Wire what exists to the Read Aloud pill. If an MP4 video exists, note it for the Watch & Listen tab.
7. Check "E:\faiththru Physics\Cannon\genesis-to-quantum\images\" for hero images (gtq-XX.webp) and slide folders (gtq-XX/slide_01.webp etc). Wire what exists.
8. Set navigation: previous/next based on the 26-article sequence
9. Main articles (01,03,04,08,11,15,16,18,22,25): gold status pill, "Skip to next main" link
10. Deep dives (all others): blue status pill, "Return to main thread" skip link
11. Set class="current" on the correct sidebar link
12. Executive Summary tab active by default

Output all 24 files to: "E:\faiththru Physics\Cannon\genesis-to-quantum\" with filename pattern gtq-XX-slug.html matching the reading order.
```

---

## COMMAND LINE 4 — Wire the index and cross-navigation

```
Read all 26 HTML files in "E:\faiththru Physics\Cannon\genesis-to-quantum\" (the ones just built: gtq-01 through gtq-26).

Verify:
1. Every article's previous/next links point to files that exist
2. Every sidebar nav link points to a file that exists
3. Every "Skip to next main" / "Return to main thread" link is correct
4. No broken audio or image references (check that referenced files exist)

Update the series index at "E:\faiththru Physics\Cannon\genesis-to-quantum\index.html" (or create one if missing) with all 26 articles listed, grouped by main articles and deep dives, with clickable links.

Report: list any missing audio files, missing images, broken links, or articles that couldn't be built due to missing markdown.
```

---

## COMMAND LINE 5 (OPTIONAL) — Generate hero images for articles missing them

```
The following articles need hero images (1200x630 WebP):
02, 06, 09, 10, and all deep dive articles that don't have a gtq-XX.webp in "E:\faiththru Physics\Cannon\genesis-to-quantum\images\".

For each missing image, generate a dark-register hero image that matches the aesthetic of the existing images (dark background, gold/blue accent, physics-themed). Use the article title and a relevant physics concept as the visual.

Save as gtq-XX.webp in the images folder.
Then update the corresponding HTML file's hero-main img src to point to the new image.
```

---

## NOTES FOR DAVID

- Run commands 1 and 2 first. Check the output. If it looks right, run 3.
- Command 4 is cleanup/verification — run after 3.
- Command 5 is optional — images can be added later.
- The template has the audio dock, sticky corner player, hero grid, kill conditions sidebar, and all tabs already built in. Claude CLI just needs to inject content and wire paths.
- All source markdowns are in E:\GTQ\ with clean content (not the Pandoc-converted versions in the MD folder).
- Audio files are in E:\faiththru Physics\Cannon\genesis-to-quantum\audio\
- Images are in E:\faiththru Physics\Cannon\genesis-to-quantum\images\
