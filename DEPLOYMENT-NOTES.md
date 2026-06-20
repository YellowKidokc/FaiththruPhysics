# Deployment Notes — FaithThruPhysics Site Update

> Last updated: 2026-06-17
>
> This file lists every changed/added file grouped by feature layer.
> Upload each group to the server to deploy the latest MDA + MTL work.

---

## Layer 1 — Pill-Strip Audio Player

Top audio bar with Deep Dive / Debate / Critique / TTS / Web pills, playback, speed control.

| File | Path | Notes |
|------|------|-------|
| Player CSS | `/mda/components/tp-pill-player.css` | Shared styles for card + thin bar |
| Player JS | `/mda/components/tp-pill-player.js` | Audio switching, play/pause, seek, speed |
| Player bar snippet | `/mda/components/tp-pill-player-bar.html` | Source template |
| Player bar snippet | `/mda/components/tp-pill-player-bar-snippet.html` | Source template |
| Site-root copy | `/components/tp-pill-player.css` | Backup copy |
| Site-root copy | `/components/tp-pill-player.js` | Backup copy |
| Site-root copy | `/components/tp-pill-player.html` | Backup copy |
| Site-root copy | `/components/tp-pill-player-bar.html` | Backup copy |
| Site-root copy | `/components/tp-pill-player-bar-snippet.html` | Backup copy |
| Injected HTML | `/index.html` | Bar inserted below header |
| Injected HTML | `/mda/index.html` | Bar inserted below header |
| Injected HTML | `/mda/*/*.html` | All 63 MDA articles updated |

---

## Layer 2 — Math Translation Layer (MTL) Overlay

Auto-translates equations on the page. Now loads reviewed translations from JSON.

| File | Path | Notes |
|------|------|-------|
| Overlay JS | `/shared/js/mtl-overlay.js` | Built from `D:\GitHub\Math-Translation-Layer` |
| Overlay loader | `/shared/js/mtl-overlay-loader.js` | Fetches reviewed translations |
| Reviewed translations | `/shared/data/mtl-overlay-translations.json` | Start empty; populated by uploader |
| Injected HTML | `/index.html` | Loader + overlay scripts added |
| Injected HTML | `/mda/index.html` | Loader + overlay scripts added |
| Injected HTML | `/mda/*/*.html` | All 63 MDA articles updated |

---

## Layer 3 — Claim Sentence Highlighting

Claims tab in the top bar highlights claim sentences and lists them per paragraph.

| File | Path | Notes |
|------|------|-------|
| Claims CSS | `/shared/css/mtl-claims.css` | Highlight + chip styles |
| Claims JS | `/shared/js/mtl-claims.js` | Scans paragraphs, wraps claim sentences |
| Injected HTML | `/index.html` | Claims script added |
| Injected HTML | `/mda/index.html` | Claims script added |
| Injected HTML | `/mda/*/*.html` | All 63 MDA articles updated |

---

## Layer 4 — MTL Reader Bar

Thin top bar with reading-level tabs and link to `/equation/`.

| File | Path | Notes |
|------|------|-------|
| Bar CSS | `/mda/components/mtl-reader-bar.css` | Tab styles |
| Bar snippet | `/mda/components/mtl-reader-bar.html` | Source template |
| Site-root copy | `/components/mtl-reader-bar.css` | Backup copy |
| Site-root copy | `/components/mtl-reader-bar.html` | Backup copy |
| MTL equation CSS | `/shared/css/mtl-equation.css` | Reading-level callout styles |
| MTL equation JS | `/shared/js/mtl-equation.js` | Tab behavior, `.mtl-callout` rendering |
| Injected HTML | `/index.html` | Bar + assets inserted |
| Injected HTML | `/mda/index.html` | Bar + assets inserted |
| Injected HTML | `/mda/*/*.html` | All 63 MDA articles updated |

---

## Layer 5 — Cloudflare D1 Hook (optional)

Audio metadata lookup for the pill player. Not deployed to production yet; schema/worker ready.

| File | Path | Notes |
|------|------|-------|
| D1 schema | `/mda/components/d1-audio-schema.sql` | SQL to create audio_tracks table |
| D1 worker | `/mda/components/d1-audio-worker.js` | Cloudflare Worker example |
| Site-root copy | `/components/d1-audio-schema.sql` | Backup copy |
| Site-root copy | `/components/d1-audio-worker.js` | Backup copy |

---

## Layer 6 — Admin / Local Tools

These live on your local machine. **Do not upload to the server** unless you want them publicly accessible.

| File | Path | Purpose |
|------|------|---------|
| MTL Uploader app | `/mtl-admin/mtl_uploader.pyw` | Desktop tool for reviewed translations |
| Uploader launcher | `/mtl-admin/Open MTL Uploader.bat` | Double-click to open app |
| Standalone template | `/mtl-admin/standalone-mtl-template.html` | Copy/paste template for other series |
| Setup guide | `/mtl-admin/README.md` | Quick uploader instructions |

---

## Quick Deploy Command (if using Wrangler / Cloudflare Pages)

From `D:\GitHub\faiththruphysics-site`:

```bash
wrangler pages deploy .
```

### ⚠️ Large-file workaround

Cloudflare Pages rejects individual files over 25 MiB. This repo contains two such files that are **not referenced by the site** but live inside the project:

```text
subdomains/shared/media/mda/audio/mda-of-america.mp3   (35 MiB)
subdomains/rigor/openintel-platform/source-app/node_modules/@cloudflare/workerd-windows-64/bin/workerd.exe   (71 MiB)
```

Before deploying, temporarily move them out (e.g. to `D:\_deploy-excluded\`), run the deploy command, then move them back.

Example PowerShell/Bash:

```bash
mkdir ../_deploy-excluded
mv subdomains/shared/media/mda/audio/mda-of-america.mp3 ../_deploy-excluded/
mv subdomains/rigor/openintel-platform/source-app/node_modules/@cloudflare/workerd-windows-64/bin/workerd.exe ../_deploy-excluded/
wrangler pages deploy . --branch=main --commit-dirty=true
mv ../_deploy-excluded/mda-of-america.mp3 subdomains/shared/media/mda/audio/
mv ../_deploy-excluded/workerd.exe subdomains/rigor/openintel-platform/source-app/node_modules/@cloudflare/workerd-windows-64/bin/
rmdir ../_deploy-excluded
```

Or upload the entire folder through the Cloudflare Pages dashboard (which respects `.gitignore` and skips the media folder).

---

## Manual Upload Checklist

Upload these at minimum:

- [ ] All HTML files in `/mda/*/*.html`
- [ ] `/index.html`
- [ ] `/mda/index.html`
- [ ] `/shared/js/mtl-overlay.js`
- [ ] `/shared/js/mtl-overlay-loader.js`
- [ ] `/shared/js/mtl-claims.js`
- [ ] `/shared/js/mtl-equation.js`
- [ ] `/shared/css/mtl-equation.css`
- [ ] `/shared/css/mtl-claims.css`
- [ ] `/shared/data/mtl-overlay-translations.json`
- [ ] `/mda/components/tp-pill-player.css`
- [ ] `/mda/components/tp-pill-player.js`
- [ ] `/mda/components/mtl-reader-bar.css`

---

## Verification After Deploy

1. Open any MDA article.
2. Confirm pill-strip audio player is below the header.
3. Confirm Math layer bar is below the audio player.
4. Click **Claims** — claim sentences should highlight and chips appear below paragraphs.
5. On an article with `.equation-block`, the overlay should insert a translation card.
6. Test a podcast pill — audio should play.
