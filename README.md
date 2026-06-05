# faiththruphysics.com — Deployment Repository

> **Owner:** David Lowe (POF 2828)  
> **Domain:** faiththruphysics.com  
> **Hosting:** Cloudflare Pages (auto-deploys from GitHub)  
> **Media:** R2 bucket `theophysics-media` (audio, video, podcasts — NOT in this repo)

## Folder Structure

```
index.html              ← Homepage (standalone React bundle)
mda/                    ← Moral Decline of America series (62 articles, 8 lanes)
  00-entry-and-series-map/
  01-story-thread/
  02-method-and-metrics/
  03-evidence-chronology/
  04-collapse-mechanisms/
  05-amish-and-case-studies/
  06-recovery-and-synthesis/
  90-appendices-and-source-packets/
glossary/               ← Interactive glossary tool
equation/               ← Master Equation explorer
isomorphism/            ← Isomorphism browser (38 pages)
proof-explorer/         ← Proof explorer + scorecards
rigor/                  ← Rigor assessment tool
media/                  ← Image gallery + slide viewer
podcast/                ← Podcast hub + RSS feed
lean4/                  ← Lean 4 proof viewer
components/             ← Reusable components (audio dock, player)
shared/                 ← Shared CSS and JS
```

## Rules

1. **HTML/CSS/JS ONLY** in this repo. No audio, video, or large media.
2. **Media lives on R2.** Articles reference `pub-8ca8fed850be4a3b98d5b2ac32428fcf.r2.dev/...`
3. **Push to GitHub = auto-deploy.** Cloudflare Pages watches `main` branch.
4. **Don't generate new folders.** If a script creates output, it goes elsewhere first, gets reviewed, then gets placed here manually.
5. **Canonical source.** This folder IS the live site. If it's not here, it's not deployed.

## Deployment Workflow

```
Edit HTML → Test locally (python -m http.server 8080) → git add/commit/push → Live in ~60 seconds
```

## Media Workflow (separate from this repo)

```
New audio file → rclone copy file.mp3 r2:theophysics-media/audio/ → Update HTML src → Push
```
