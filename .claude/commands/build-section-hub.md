# Build Section Hub

Sets up the three-level navigation structure for any site section:

**Level 1 — Main Home** (`/index.html`) links to the section  
**Level 2 — Site Home** (`/section/index.html`) — theme grid + reading spine, links to folders  
**Level 3 — Theme Folders** (`/section/theme/index.html`) — video + article cards  
**Level 4 — Individual Articles** — "Back" / "Hub" button returns to site home  

## Arguments

`$ARGUMENTS` — the section path, e.g. `one-page-stories` or `moral-decline`

## What to do

The user will provide a section name or path. Follow these steps:

### Step 1 — Audit the section

Scan the section folder and report:
- Does `/section/index.html` exist? Is it a site home (theme grid) or an old catalog?
- What sub-folders exist? Do they each have an `index.html`?
- Do those folder indexes have a `<video>` or audio dock?
- Do individual article pages have a `site-nav-bar` or bottom nav?
- Does the root `/index.html` already link to this section?

### Step 2 — Build or fix the site home (`/section/index.html`)

The site home must have:
- A **hero** section with title, subtitle, and stat pills (stories count, themes count)
- A **theme grid** — one card per sub-folder, each card links to `./theme-folder/`
- A **reading spine** — numbered list of all individual articles in recommended reading order
- A **bottom series nav strip** — links to other site sections + this one marked active
- A **top bar** — brand link to `/`, Home nav link to `/`, no link that circles back to itself
- NO `<base target="_blank">` (kills internal navigation)
- Dark theme: `--bg:#050505`, gold: `#d4af37`, Crimson Text serif, Inter sans, Oswald display, JetBrains Mono mono

Each theme card style:
```html
<a class="tp-theme-card" href="./folder-name/" style="--theme-color:var(--teal)">
  <div class="tp-theme-header">
    <span class="tp-theme-tag">Tag</span>
    <span class="tp-theme-arrow"><i class="fas fa-arrow-right"></i></span>
  </div>
  <h3 class="tp-theme-title">Theme Name</h3>
  <p class="tp-theme-desc">One sentence description.</p>
  <div class="tp-theme-meta"><span><i class="fas fa-file-alt"></i> N articles</span></div>
</a>
```

### Step 3 — Fix theme folder indexes (`/section/theme/index.html`)

Each folder index must have in its bottom `site-nav-bar`:
```html
<a href="/section/" class="sn-home"><i class="fas fa-home"></i><span>Site Home</span></a>
<div class="sns"></div>
<a href="../index.html"><i class="fas fa-layer-group"></i><span>Section Hub</span></a>
```

If the folder index was pointing `href="/"` for Home, change it to `href="/section/"`.

### Step 4 — Fix individual article pages

Each article page with a `site-nav-bar` or `site-nav-center` must have a "Hub" or "Home" link pointing to `/section/` (NOT to `/`).

Pattern to restore/add (inside `.site-nav-center` before its closing `</div>`):
```html
<div class="sns"></div>
<a href="/section/" class="sn-home"><i class="fas fa-home"></i><span>Hub</span></a>
```

If the link was previously pointing to `https://faiththruphysics.com` or `/`, update the `href` to `/section/`. Do NOT remove the link — fix the destination.

### Step 5 — Wire the main home

Check `/index.html` for a card or link pointing to `/section/`. If missing, add a `start-card` in the `start-grid` section:
```html
<a class="start-card start-gold" href="/section/">
  <div class="start-num">XXX</div>
  <h3>Section Title</h3>
  <p>One sentence description.</p>
  <div class="start-meta">Section type</div>
</a>
```

### Step 6 — Verify

Run a grep across the section for `href="/"` and `href="/index.html"` in nav contexts (exclude footer attribution text, `<link rel="canonical">`, og:url meta tags, analytics scripts, and brand links). Report any remaining circular nav links.

## Rules

- **Never remove a nav link** — fix its `href` destination instead
- **Footer attributions are not nav links** — lines like "Written by David Lowe · faiththruphysics.com · 2026" stay untouched
- **Brand links stay** — `class="brand"`, `class="pe-brand"`, `class="tp-brand"` pointing to `/` or `https://faiththruphysics.com` are standard UX, not circular
- **`<base target="_blank">` must be removed** if present — it breaks all internal links
- Folder links must use URL-encoded paths if folder names have spaces: `Math%20all/`
- The section site home's own series nav strip should mark itself `class="active"`
