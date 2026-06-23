# Top Bar + Bottom Bar Component Spec
## faiththruphysics.com · June 22, 2026
## For: Codex / GitHub build

---

## What this is

Two injectable HTML/CSS/JS components that go on every article page:
1. **Top bar** — domain classification pills + percentage bar + reading path tabs
2. **Bottom bar** — audio dock (read aloud / deep dive / debate / critique) + speed control + prev/next nav
3. **Sticky mini-player** — appears bottom-right when user scrolls past the audio dock

---

## Theme handling

Articles have TWO background contexts:
- **Dark** (MDA series, GTQ) — near-black backgrounds (#050505)
- **Light** (one-pagers, convergence) — white/light backgrounds

The components must detect which context they're in OR accept a `data-theme="dark|light"` attribute.

For dark context: bars use dark surface (#0a0a0a) with light text, subtle borders
For light context: bars use white surface with dark text, subtle borders

Use CSS custom properties so both themes work from the same code.

---

## Top bar spec

### Domain pills row
- Horizontal row of pills, left-aligned, wrapping on narrow screens
- Each pill: rounded (border-radius: 20px), colored background (light tint), dark text from same color family
- Format: "Physics 40%" — name + percentage on the pill itself
- Pill colors are passed in via meta.json classification array: `{tag, pct, color}`
- Color mapping: use the hex as the base, derive light tint (10% opacity) for background, full color for text

### Percentage bar
- Below the pills
- Height: 10px, rounded ends
- Segments proportional to percentages, 2px gap between segments
- Same colors as the pills above
- Always sums to 100%

### Reading path tabs
- Below the bar, separated by a thin border
- Four tabs: Story path | Plain path | Test path | Proof path
- Active tab: bottom border accent, slightly different background
- Tabs switch content via JS (swap which .md content is rendered)
- If a reading level doesn't exist for this article, tab shows but is grayed/disabled

---

## Bottom bar spec

### Audio dock row
- Four audio buttons in pill style: Read aloud | Deep dive | Debate | Critique
- Active button gets accent color (blue tint)
- Critique button only appears if `meta.json.audio.critique` is not null
- Speed toggle group on the right: 1x | 1.5x | 2x (pill toggle, one active)
- Audio source URLs come from the faith-audio-pipeline API:
  `GET https://faith-audio-pipeline.davidokc28.workers.dev/api/audio?slug={article-slug}`

### Navigation row
- Below audio dock, separated by thin border
- Left: "← Previous article title" (from meta.json.prev)
- Center: "N of M" position indicator
- Right: "Next article title →" (from meta.json.next)

### Sticky mini-player
- Appears fixed bottom-right (16px from edges) when audio dock scrolls out of viewport
- Small rounded card: play/pause button + track name + time + speed
- Disappears when user scrolls back to the audio dock
- Uses IntersectionObserver on the audio dock element

---

## Injection method

These are standalone components. Injection script:
1. Find `<body>` or first content container
2. Insert top bar as first child
3. Find end of content / before `</body>`
4. Insert bottom bar before it
5. Append sticky mini-player to body

The injection script reads `meta.json` from a known path (same directory as the HTML or from a `<script id="article-meta" type="application/json">` block embedded in the page).

---

## File deliverables

```
components/
  tp-top-bar.html        ← standalone demo page
  tp-top-bar.css
  tp-top-bar.js
  tp-bottom-bar.html     ← standalone demo page
  tp-bottom-bar.css
  tp-bottom-bar.js
  tp-sticky-player.js
  tp-inject.js           ← master injector script
  tp-theme.css           ← shared theme variables (dark/light)
```

---

## Data contract

Components read from this structure (embedded in page or loaded from meta.json):

```json
{
  "slug": "the-same-equation",
  "title": "The Same Equation",
  "series": "one-pagers",
  "series_order": 3,
  "series_total": 53,
  "prev": {"slug": "character-of-god", "title": "Character of God from Physics"},
  "next": {"slug": "the-24-anti-properties", "title": "The 24 Anti-Properties"},
  "classification": [
    {"tag": "Physics", "pct": 40, "color": "#378ADD"},
    {"tag": "Theology", "pct": 30, "color": "#D85A30"},
    {"tag": "Mathematics", "pct": 15, "color": "#7F77DD"},
    {"tag": "Info theory", "pct": 10, "color": "#1D9E75"},
    {"tag": "Consciousness", "pct": 5, "color": "#D4537E"}
  ],
  "reading_levels": ["story", "plain", "test", "proof"],
  "audio_api": "https://faith-audio-pipeline.davidokc28.workers.dev/api/audio"
}
```

---

## Design notes

- No framework dependencies (no React, no Tailwind CDN). Pure HTML/CSS/JS.
- Must work when injected into existing pages without breaking their styles.
- All styles scoped with `.tp-` prefix to avoid collisions.
- Mobile responsive: pills wrap, tabs stack or scroll horizontally.
- Transitions: subtle fade on tab switch, smooth slide for sticky player.
- Accessible: keyboard navigation on tabs, aria labels on audio controls.
