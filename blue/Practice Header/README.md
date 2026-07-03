# Practice Header Contest

Folder:

`D:\GitHub\faiththruphysics-site-v2\blue\Practice Header`

Voting page:

`header-vote.html`

Codex entry:

`codex-header.html`

Local rollout scripts copied into this folder:

- `prepare_topbar_pages.py`
- `inject_topbar.py`

Dry-run them from this folder like this:

```powershell
cd "D:\GitHub\faiththruphysics-site-v2\blue\Practice Header"

python prepare_topbar_pages.py --root D:\GitHub\faiththruphysics-site-v2 maxwell-truth-isomorphism.html
python inject_topbar.py --root D:\GitHub\faiththruphysics-site-v2 maxwell-truth-isomorphism.html
```

Apply only after the dry-run output looks right:

```powershell
python prepare_topbar_pages.py --root D:\GitHub\faiththruphysics-site-v2 maxwell-truth-isomorphism.html --apply
python inject_topbar.py --root D:\GitHub\faiththruphysics-site-v2 maxwell-truth-isomorphism.html --apply
```

## Assignment For Each AI

Build one header entry in this folder. Do not edit the copied Blue article pages. Do not overwrite another AI's entry.

Suggested filenames:

- Cursor: `cursor-header.html`
- Kimmy: `kimmy-header.html`
- Gemini: `gemini-header.html`
- AntiGravity: `antigravity-header.html`

## Required Labels

Every entry must label the page and the header.

Use:

```html
<header data-header-entry="your-name" data-header-author="Your Name" data-slot="top-frame">
```

Include a JSON label map:

```html
<script type="application/json" id="header-entry-labels">
{
  "entry": "your-name",
  "author": "Your Name",
  "page": "your-header.html"
}
</script>
```

## Required Slots

Use these `data-slot` names where possible:

- `top-frame`
- `top-frame-main-row`
- `brand-home`
- `brand-mark`
- `brand-name`
- `primary-nav`
- `nav-home`
- `nav-mtl`
- `nav-proof`
- `nav-series`
- `reading-level-control`
- `reading-level-high-school`
- `reading-level-college`
- `reading-level-phd`
- `search-command`
- `proof-dashboard-toggle`
- `domain-pill-row`
- `domain-row-metric-numbers`
- `metric-domains-number`
- `metric-laws-number`
- `metric-coherence-number`
- `metric-claims-number`
- `domain-pills`
- `domain-logic-mathematics`
- `domain-physics`
- `domain-information-theory`
- `domain-theology`
- `domain-developmental-psychology`
- `domain-philosophy`
- `domain-color-strip`

## Design Rules

- Keep CSS scoped to your own prefix.
- Keep the header fixed at the top.
- Do not squeeze the article width.
- Keep domain pills visible.
- Keep the metric numbers visually tied to the domain/pill row.
- Make buttons work enough to demonstrate intent.
- Keep mobile usable.

## Voting Criteria

- Best fit over existing article pages.
- Cleanest visual hierarchy.
- Best use of labels for JSON/API wiring.
- Least risk of breaking the rest of the site.
- Best desktop and mobile shape.

Codex may submit an entry but does not get a vote.
