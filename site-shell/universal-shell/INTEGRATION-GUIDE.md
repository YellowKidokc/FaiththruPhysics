# Faith thru Physics — Universal Page Shell Integration Guide

**Version:** 1.0  
**Date:** 2026-07-02  
**Project:** POF 2828 — Theophysics Research Initiative  
**Site:** faiththruphysics.com

---

## Table of Contents

1. [Quick Start (3-Step Integration)](#quick-start)
2. [Architecture Overview](#architecture)
3. [JSON Data Schema](#json-schema)
4. [Insertion Points](#insertion-points)
5. [Layer-by-Layer Reference](#layer-reference)
6. [CSS Customization](#css-customization)
7. [JavaScript API](#javascript-api)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## 1. Quick Start (3-Step Integration) <a name="quick-start"></a>

### Step 1: Copy the shell markup

Copy the HTML between `<!-- SHELL-START -->` and `<!-- SHELL-END -->` comments from `shell.html` into your page. Place it:
- **Top half** (Layers 1+2): immediately after `<body>`
- **Bottom half** (Layers 3+4): immediately before `</body>`

### Step 2: Add the data block

Insert a `<script id="shell-data" type="application/json">` block in your page's `<head>` or at the top of `<body>`, populated with article-specific data (see [JSON Schema](#json-schema)).

### Step 3: Include the script

```html
<script src="/site-shell/shell.js"></script>
```

Or embed inline from `shell.js`.

**That's it.** The shell auto-wires everything from the JSON data.

---

## 2. Architecture Overview <a name="architecture"></a>

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: TOP BAR (fixed, z-index: 1000)        │
│  Brand | Domains | Chi | Tools | Levels | Search │
├─────────────────────────────────────────────────┤
│  PANEL TOGGLE (fixed, z-index: 999)              │
│  "Verification & Proof ▼"                        │
├─────────────────────────────────────────────────┤
│  LAYER 2: EXPANDABLE PANEL (fixed, z-index: 998) │
│  ┌─────────┬─────────┬─────────┐                │
│  │Verify   │Proofs   │MTL      │  ← tabs        │
│  │Axioms   │Proof 1  │Equation │                │
│  │Laws     │Proof 2  │Named    │                │
│  │Chi Score│Proof 3  │Plain    │                │
│  │Claims   │         │Feature  │                │
│  └─────────┴─────────┴─────────┘                │
├─────────────────────────────────────────────────┤
│                                                   │
│  YOUR PAGE CONTENT GOES HERE                     │
│  <article class="ftp-article">...</article>      │
│                                                   │
│  (Audio Dock appears within article flow)        │
│                                                   │
├─────────────────────────────────────────────────┤
│  LAYER 3 (cont.): MINI-PLAYER (fixed, z-index:   │
│  9999, appears when full dock scrolls off)       │
├─────────────────────────────────────────────────┤
│  LAYER 4: FOOTER SYSTEM                          │
│  Light Nav → Final Audit → Subdomain Grids →     │
│  Series Nav → Bottom Bar → The Door              │
└─────────────────────────────────────────────────┘
```

### File Inventory

| File | Purpose | Required? |
|------|---------|-----------|
| `shell.html` | Complete working demo with all 4 layers | Reference only |
| `shell.js` | Shell controller — powers all layers from JSON | **Yes** |
| `shell.css` | (Extract from shell.html `<style>` block) | **Yes** |
| `INTEGRATION-GUIDE.md` | This document | Reference |
| `shell-schema.md` | Full JSON schema reference | Reference |

---

## 3. JSON Data Schema <a name="json-schema"></a>

Every page provides one `<script id="shell-data" type="application/json">` block. All shell rendering is driven from this data.

### Minimal Example (required fields only)

```json
{
  "page": {
    "title": "Article Title",
    "slug": "article-slug",
    "series": "GTQ"
  }
}
```

### Full Example (all fields)

```json
{
  "page": {
    "title": "The Measurement That Collapsed Reality",
    "subtitle": "When observation itself becomes the force that binds matter to meaning.",
    "author": "David Lowe",
    "series": "GTQ",
    "series_name": "Genesis to Quantum",
    "series_home": "/genesis-to-quantum/",
    "slug": "gtq-01-measurement",
    "date": "June 2026",
    "prev": { "title": "Series Introduction", "url": "/genesis-to-quantum/" },
    "next": { "title": "Free Will — Two Frames", "url": "/genesis-to-quantum/gtq-02.html" }
  },
  "domains": [
    { "name": "Theology", "key": "theology", "pct": 28, "color": "#d4af37" },
    { "name": "Physics", "key": "physics", "pct": 22, "color": "#7cc7ff" },
    { "name": "Cross-Domain", "key": "cross-domain", "pct": 15, "color": "#3bb39a" },
    { "name": "Evidence", "key": "evidence", "pct": 15, "color": "#7fc77f" },
    { "name": "Consciousness", "key": "consciousness", "pct": 10, "color": "#a78bfa" },
    { "name": "Mathematics", "key": "mathematics", "pct": 7, "color": "#ff7d90" },
    { "name": "Speculative", "key": "speculative", "pct": 3, "color": "#aeb8d6" }
  ],
  "verification": {
    "axioms": { "tested": 94, "total": 188 },
    "laws": { "active": [1, 3, 4, 7, 10] },
    "chi": { "raw": 7.42, "normalized": 8.3 },
    "fruits": { "score": 7 },
    "isomorphisms": {
      "count": 12,
      "physics_processes": 5,
      "trinity_mappings": 3,
      "meq_variables": 8
    },
    "claims": {
      "total": 24,
      "load_bearing": 8,
      "kill_conditions": 3,
      "contradictions": 0
    },
    "proofs": [
      {
        "id": "p1",
        "title": "Observer-Dependence Derivation",
        "status": "verified",
        "summary": "The measurement problem is not epistemic...",
        "url": "/proof-explorer/gtq-01/measurement"
      }
    ]
  },
  "mtl": [
    {
      "latex": "\\frac{d\\chi}{dt} = G_{\\text{ext}} \\cdot \\eta(K) - \\lambda S(\\chi)",
      "named": "Rate of coherence = External grace times receptivity minus entropy",
      "plain": "Coherence changes based on grace input minus entropy...",
      "feature": "Multiplicative: if either term goes to zero, growth vanishes."
    }
  ],
  "audio": [
    { "src": "read", "label": "Read Aloud", "url": "https://r2.../read-aloud.mp3" },
    { "src": "debate", "label": "Debate", "url": "https://r2.../debate.mp3" },
    { "src": "deep", "label": "Deep Dive", "url": "https://r2.../deep-dive.mp3" },
    { "src": "critique", "label": "Critique" }
  ],
  "audit": {
    "right": ["Claim 1 survived the check.", "Derivation holds at 6.35σ."],
    "overstated": ["Language ran ahead of evidence in section 3."],
    "wrong": ["Entropy calculation was off by 2x — corrected in v4."]
  }
}
```

### Field Reference

#### `page` (object, required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | **Yes** | Article title, shown in document.title context |
| `subtitle` | string | No | Article subtitle |
| `author` | string | No | Author name |
| `series` | string | **Yes** | Series code: "MDA", "GTQ", "Convergence", "Logos", "OPS" |
| `series_name` | string | No | Human-readable series name (e.g., "Genesis to Quantum") |
| `series_home` | string | No | URL to series index page |
| `slug` | string | No | URL-safe article identifier |
| `date` | string | No | Publication date |
| `prev` | object | No | `{ title, url }` for previous article |
| `next` | object | No | `{ title, url }` for next article |

#### `domains` (array)

Domain coverage for the classification bar and verification panel.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Domain name (e.g., "Theology") |
| `key` | string | Machine key (e.g., "theology") |
| `pct` | number | Percentage coverage (0-100) |
| `color` | string | Hex color for this domain |

**Standard domain colors:**
- Theology: `#d4af37` (gold)
- Physics: `#7cc7ff` (blue)
- Mathematics: `#ff7d90` (red)
- Cross-Domain: `#3bb39a` (teal)
- Evidence: `#7fc77f` (green)
- Consciousness: `#a78bfa` (purple)
- Information: `#e8a040` (orange)

#### `verification` (object)

All verification metrics for the expandable panel.

| Field | Type | Description |
|-------|------|-------------|
| `axioms.tested` | number | Number of axioms tested |
| `axioms.total` | number | Total axioms available (default: 188) |
| `laws.active` | number[] | Array of active law numbers (1-10) |
| `chi.raw` | number | Raw chi score |
| `chi.normalized` | number | Normalized chi score (0-10) |
| `fruits.score` | number | Fruits score (0-9) |
| `isomorphisms.count` | number | Number of cross-domain bridges |
| `isomorphisms.physics_processes` | number | Physics processes detected |
| `isomorphisms.trinity_mappings` | number | Trinity mappings found |
| `isomorphisms.meq_variables` | number | Master Equation variables (0-10) |
| `claims.total` | number | Total claims extracted |
| `claims.load_bearing` | number | Load-bearing claims |
| `claims.kill_conditions` | number | Falsification conditions |
| `claims.contradictions` | number | Contradictions found |
| `proofs` | array | See `proofs` below |

#### `verification.proofs` (array)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique proof identifier |
| `title` | string | Proof title |
| `status` | string | `"verified"`, `"partial"`, or `"pending"` |
| `summary` | string | Plain-text proof summary |
| `url` | string | Link to full proof in Proof Explorer |

#### `mtl` (array)

Math Translation Layer entries.

| Field | Type | Description |
|-------|------|-------------|
| `latex` | string | LaTeX equation (renders via MathJax) |
| `named` | string | Equation written with named variables |
| `plain` | string | Plain-English explanation |
| `feature` | string | Structural feature to highlight (multiplicative, boundary, etc.) |

#### `audio` (array)

Audio track definitions for the dock.

| Field | Type | Description |
|-------|------|-------------|
| `src` | string | Source key: `"read"`, `"debate"`, `"deep"`, `"critique"` |
| `label` | string | Display label |
| `url` | string | MP3 URL. **Omit to show as "coming soon"** |

#### `audit` (object)

Final Audit content (3-column structure).

| Field | Type | Description |
|-------|------|-------------|
| `right` | string[] | What we got right — list items |
| `overstated` | string[] | What we overstated — list items |
| `wrong` | string[] | What we got wrong — list items |

---

## 4. Insertion Points <a name="insertion-points"></a>

Your page content goes between Layer 2 (end) and Layer 3 (start). The shell reserves space for fixed elements, so content flows naturally below the top bar.

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Your head content -->
  <style> /* shell CSS (extract from shell.html) */ </style>
  <script id="shell-data" type="application/json">
    { /* your article data */ }
  </script>
</head>
<body>

  <!-- ═══ LAYER 1: TOP BAR ═══ -->
  <header class="ftp-top">...</header>

  <!-- PANEL TOGGLE -->
  <div class="ftp-panel-toggle">...</div>

  <!-- ═══ LAYER 2: EXPANDABLE PANEL ═══ -->
  <div class="ftp-panel">...</div>

  <!-- ═══ YOUR CONTENT HERE ═══ -->
  <article class="ftp-article">
    <!-- Audio dock can appear anywhere in your content -->
    <div class="ftp-audio-dock">...</div>

    <h1>Your Title</h1>
    <p>Your content...</p>
  </article>

  <!-- ═══ LAYER 3: MINI PLAYER ═══ -->
  <div class="ftp-dock-mini">...</div>

  <!-- ═══ LAYER 4: FOOTER SYSTEM ═══ -->
  <nav class="ftp-light-nav">...</nav>
  <section class="ftp-audit">...</section>
  <!-- ... subdomain grids, series nav, bottom bar, door ... -->

  <script src="shell.js"></script>
</body>
</html>
```

### Content Padding

The top bar + panel toggle reserve `calc(46px + 34px)` = **80px** of vertical space. The `.ftp-article` class already includes this padding:

```css
.ftp-article {
  padding-top: calc(var(--header-h) + var(--panel-h) + 24px);
  /* = 80px + breathing room */
}
```

If you use your own content container instead of `.ftp-article`, add this padding manually.

---

## 5. Layer-by-Layer Reference <a name="layer-reference"></a>

### Layer 1: Top Bar

**Elements rendered from JSON:**
- Domain pills (from `domains`, top 4 by percentage)
- Chi badge (from `verification.chi.normalized`)

**Interactive elements:**
- Reading level tabs (High School / College / PhD) — persists to localStorage
- Tool links (MTL, Proof, Grader) — standard `<a>` tags
- Search button — dispatches `ftp-search-open` event (listen for this)

**Events dispatched:**
- `ftp-layer-change` — when reading level changes. The MTL worker client listens for this.

### Layer 2: Expandable Panel

**Tabs:**
1. **Verification** — axioms, laws, chi score, isomorphisms, claims, domains
2. **Proofs** — expandable proof list with status indicators
3. **Math Translation** — equation callouts with named variables, plain English, structural features

**Collapsible proofs:** Click any proof header to expand/collapse its body.

### Layer 3: Audio Dock

**Behavior:**
- Pill buttons switch between audio sources
- Unavailable pills (no URL) are dimmed and non-interactive
- Play/pause, seek bar, volume mute, speed control
- When the full dock scrolls off-screen, a mini-player appears (bottom-right)
- Mini-player shows play/pause + current source label

**Keyboard shortcut:** Spacebar toggles play/pause (when not typing)

### Layer 4: Footer

**Sections (top to bottom):**
1. **Light Navigation** — prev/next links + series home + site home (replaces heavy big-nav boxes)
2. **Final Audit** — three-column: Right / Overstated / Wrong
3. **Subdomain Grids** — Proof & Research, Reference & Media, Bible Studies
4. **Series Navigation** — horizontal strip of all series
5. **Bottom Bar** — equation, copyright, vow
6. **The Door** — "15 + 15 = 100"

---

## 6. CSS Customization <a name="css-customization"></a>

### CSS Variables

All colors and layout values are CSS custom properties. Override them in your page's `<style>`:

```css
:root {
  --gold: #d4af37;           /* Primary accent */
  --bg: #050505;             /* Page background */
  --surface: #0a0a0a;        /* Card backgrounds */
  --header-h: 46px;          /* Top bar height */
  --panel-h: 34px;           /* Panel toggle height */
  --max: 1180px;             /* Content max-width */
}
```

### Existing Site Compatibility

The shell uses the same CSS variable names as the existing `faiththruphysics-template-5.html` and `verification-bar.html`. If your page already defines these variables, the shell will use them.

### Dark Theme Assumption

The shell assumes a dark theme. The base `body` styles are:

```css
body {
  background: var(--bg, #050505);
  color: var(--text, #e5e3df);
}
```

---

## 7. JavaScript API <a name="javascript-api"></a>

After the shell initializes, `window.ftp` exposes:

| Method | Description |
|--------|-------------|
| `ftp.togglePanel()` | Open/close the expandable panel |
| `ftp.switchTab(name)` | Switch panel tab (`"verify"`, `"proofs"`, `"mtl"`) |
| `ftp.toggleProof(header)` | Expand/collapse a proof item |
| `ftp.audioToggle()` | Play/pause audio |
| `ftp.audioSeek(event)` | Seek to click position on track |
| `ftp.audioMute()` | Toggle mute |
| `ftp.audioSetSpeed()` | Apply speed from dropdown |
| `ftp.getData()` | Get the parsed shell-data JSON |
| `ftp.refresh()` | Re-render all layers from current data |

### Events dispatched by the shell:

| Event | When | Detail |
|-------|------|--------|
| `ftp-layer-change` | Reading level changes | `{ level: "highschool"\|"college"\|"phd" }` |
| `ftp-search-open` | Search button or Ctrl+K pressed | none |

### Events the shell listens for:

| Event | Action |
|-------|--------|
| `ftp-layer-change` | Re-renders MTL tab content |

---

## 8. Production Deployment <a name="production-deployment"></a>

### Option A: Inline (single file, no dependencies)

Copy the CSS from `shell.html` `<style>` into your page's `<style>` block, copy the HTML markup, and copy `shell.js` into a `<script>` tag at the bottom. Zero external dependencies.

### Option B: External files (recommended for multi-page)

1. Save `shell.css` to `/site-shell/shell.css`
2. Save `shell.js` to `/site-shell/shell.js`
3. In each page:

```html
<link rel="stylesheet" href="/site-shell/shell.css"/>
<!-- ... page content ... -->
<script src="/site-shell/shell.js"></script>
```

### Option C: frame.js injection (matches existing workflow)

If you're already using `topbar.py` to inject `frame.js`, you can adapt the migrator to inject the shell markup and data block instead. The shell is designed to replace the existing `.tp-top` + `.tp-class` + `.tp-player-block` elements that `topbar.py` currently strips.

### Batch Integration (Python helper)

For bulk application across many pages, use a script that:

1. Reads each HTML file
2. Inserts the shell CSS before `</head>`
3. Inserts the shell markup after `<body>`
4. Inserts `shell.js` before `</body>`
5. Generates per-page JSON from your content database

Example Python pattern:

```python
import json
from pathlib import Path

SHELL_CSS = Path("shell.css").read_text()
SHELL_TOP = Path("shell-top.html").read_text()  # Layers 1+2 markup
SHELL_BOTTOM = Path("shell-bottom.html").read_text()  # Layers 3+4 markup
SHELL_JS = '<script src="/site-shell/shell.js"></script>'

def inject_shell(page_path, article_data):
    html = Path(page_path).read_text(encoding="utf-8")

    # Insert CSS
    html = html.replace("</head>", f"<style>{SHELL_CSS}</style></head>")

    # Insert data + top layers after <body>
    data_block = f'<script id="shell-data" type="application/json">{json.dumps(article_data)}</script>'
    html = html.replace("<body>", f"<body>\n{data_block}\n{SHELL_TOP}")

    # Insert bottom layers + JS before </body>
    html = html.replace("</body>", f"{SHELL_BOTTOM}\n{SHELL_JS}\n</body>")

    Path(page_path).write_text(html, encoding="utf-8")
```

---

## 9. Troubleshooting <a name="troubleshooting"></a>

| Problem | Cause | Fix |
|---------|-------|-----|
| Shell doesn't render | `shell-data` JSON is invalid | Check browser console for parse errors |
| No domain pills shown | `domains` array missing or empty | Populate `domains` in shell-data |
| Audio pills all dimmed | No `url` fields in `audio` array | Add MP3 URLs, or omit `url` to show "coming soon" |
| Panel won't open | JavaScript not loaded | Ensure `shell.js` is after the markup |
| Mini-player never appears | `ftpAudioDock` ID missing | Check the audio dock markup has `id="ftpAudioDock"` |
| Reading level doesn't persist | localStorage blocked | Check browser privacy settings |
| Math equations not rendering | MathJax not loaded | Include MathJax 3 before shell.js |
| Content hidden under top bar | Missing `.ftp-article` class or padding | Add `padding-top: 80px` to your content container |
| Styles conflict with existing CSS | Variable name collision | Scope shell styles or rename variables |

### Console Debugging

The shell logs initialization status to the console:

```
[shell] Initialized for: The Measurement That Collapsed Reality
```

If you see `[shell] No #shell-data block found`, the JSON data block is missing or has the wrong ID.

### Verifying Data Loading

In the browser console:

```javascript
ftp.getData()  // Should return the full parsed JSON object
```

---

## Appendix: JSON Output from Pipeline

The evaluation pipeline (Excel → JSON) already produces output compatible with this shell. The `loadVerification()` function in the original `verification-bar.html` maps directly to the `verification` object in the shell schema.

If you have existing pipeline JSON, wrap it like this:

```json
{
  "page": { "title": "...", "series": "..." },
  "verification": { /* your existing pipeline output */ },
  "domains": [ /* your existing domain data */ ],
  "audio": [ /* your existing audio config */ ],
  "audit": { /* your existing audit data */ }
}
```

---

*POF 2828 — Theophysics Research Initiative*  
*faiththruphysics.com*
