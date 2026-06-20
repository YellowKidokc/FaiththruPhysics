# Cloudflare Audio/TTS Pipeline Audit

Date: 2026-06-19
Repo: `faiththruphysics-site`

This file exists so the Cloudflare audio/TTS experiment is not lost. It records what is already live in Cloudflare, what exists only in this repo, and the lowest-risk path for testing automated page-to-audio generation.

## Current Status

Cloudflare has partial/experimental TTS and media pieces. A repo-owned replacement pipeline now exists at `workers/audio-pipeline/` and has been deployed.

The missing finished workflow is:

1. Extract clean article text from a site page.
2. Generate TTS audio from that clean text.
3. Store the audio file in R2.
4. Save article-to-audio metadata in D1.
5. Let the site audio player resolve `/api/audio?slug=...` and play the generated file.

## Canonical Implementation To Use

Use this folder for the next implementation/deploy attempt:

```text
workers/audio-pipeline/
```

Current deployment:

```text
https://faith-audio-pipeline.davidokc28.workers.dev
```

Current resources:

| Resource | Name / ID |
| --- | --- |
| Worker | `faith-audio-pipeline` |
| D1 | `faiththruphysics-audio` / `5d669471-8282-4d35-85a3-d19fede07f57` |
| R2 | `faiththruphysics-audio` |
| Worker secret | `ADMIN_TOKEN` |

Operational note: Aura-2 currently rejects chunks over 2,000 input characters. The deployed Worker uses `CHUNK_CHARS=1800` and rejects AI error responses instead of saving them as audio.

Smoke tests passed after deployment:

| Test | Result |
| --- | --- |
| `GET /health` | `ok: true` |
| `POST /api/generate` from short text | Generated MP3 with `luna` voice |
| `GET /api/audio?slug=smoke-test&mode=tts` | Returned registered track |
| `GET /audio/generated/system/smoke-test/tts.mp3` | Returned `audio/mpeg` |
| `POST /api/extract` with sample HTML | Removed nav/footer/internal notes and kept main text |

It contains:

| File | Purpose |
| --- | --- |
| `workers/audio-pipeline/src/index.js` | End-to-end Worker: clean text extraction, Workers AI TTS, R2 storage, D1 registration, and `/api/audio` lookup. |
| `workers/audio-pipeline/schema.sql` | D1 schema for `audio_tracks` and generation jobs. |
| `workers/audio-pipeline/wrangler.jsonc` | Ready-to-fill Cloudflare config for Worker, AI, D1, and R2 bindings. |
| `workers/audio-pipeline/README.md` | Deployment, testing, voice-selection, and cleanup instructions. |

This implementation reuses the known-good part of `mda-tts-sampler`: Workers AI Deepgram Aura TTS with selectable voices. It does not reuse the incomplete `theophysics-media-pipeline` TTS behavior because that Worker appeared to store text chunks as `.mp3` placeholders rather than finished audio.

## Live Cloudflare Resources Found

Account inspected by Cloudflare API: David's Cloudflare account.

Relevant Workers:

| Worker | Status | Notes |
| --- | --- | --- |
| `mda-tts-sampler` | Live experiment | Uses Workers AI with `@cf/deepgram/aura-2-en`; exposes sample voice endpoints. No routes and no cron triggers found. |
| `theophysics-media-pipeline` | Live experiment | Has upload/transcription/TTS-related API paths and binds AI, D1, and R2, but the TTS handler stores text chunks as `.mp3` placeholders rather than real generated audio. |
| `theophysics-ingestion-engine` | Live related pipeline | Binds AI, D1, and R2 for ingestion-style processing. Not the site audio player pipeline. |
| `theophysics-rss` | Live related utility | RSS-oriented Worker. No bindings and no cron triggers found. |
| `nerve-tts-pwa` | Live Pages/Worker asset app | Appears to be a separate TTS PWA experiment. |

Relevant Pages projects:

| Pages Project | Domains |
| --- | --- |
| `faiththruphysics` | `faiththruphysics.pages.dev`, `faiththruphysics.com`, `idex.faiththruphysics.com` |
| `theophysics-tts` | `theophysics-tts.pages.dev` |
| `nerve-tts-pwa` | `nerve-tts-pwa.pages.dev` |

Relevant D1 databases:

| D1 Database | Finding |
| --- | --- |
| `faiththruphysics-pages` | Has `_cf_KV` and `pages`; `pages` count was 0 at audit time. |
| `theophysics-pipeline` | Has media/pipeline tables, but `media` count was 0 at audit time. |
| `theophysics-ingestion` | Ingestion/job/result tables. |
| `theophysics-axioms` | Axiom data tables, not audio metadata. |

Relevant R2 buckets:

| R2 Bucket | Notes |
| --- | --- |
| `theophysics-media` | Existing audio references in site docs mention this bucket. |
| `theophysics` | Existing general bucket. |

No live D1 database inspected had the site player's `audio_tracks` table.

Cleanup rule: do not delete live Cloudflare resources until `workers/audio-pipeline/` is deployed, tested against one real page, and the site player successfully plays the generated `/api/audio?slug=...` result. After verification, `theophysics-media-pipeline` can be archived or deleted, while `mda-tts-sampler` can either stay as a voice sampler or be deleted after a voice is chosen.

## Local Repo Artifacts Found

These files are already in the repo and should be preserved:

| File | Purpose |
| --- | --- |
| `components/d1-audio-worker.js` | Prototype Worker for `/api/audio?slug=...` metadata lookup. |
| `components/d1-audio-schema.sql` | Prototype `audio_tracks` D1 schema. |
| `mda/components/d1-audio-worker.js` | MDA copy of the metadata Worker. |
| `mda/components/d1-audio-schema.sql` | MDA copy of the metadata schema. |
| `components/tp-pill-player.js` | Site audio player; expects `/api/audio` by default. |
| `shared/js/mda-browser-tts.js` | Browser speech-synthesis fallback, not generated audio. |
| `DEPLOYMENT-NOTES.md` | Says the D1 audio hook is optional and not deployed to production yet. |
| `KIMI-DEPLOYMENT-HANDOFF.md` | Notes existing audio URLs point to R2 bucket `theophysics-media`. |

## Recommended Trial Architecture

Use Cloudflare as a reversible experiment, not as the only audio source.

Recommended resources:

| Resource | Suggested Name | Purpose |
| --- | --- | --- |
| Worker | `faith-audio-pipeline` | Admin-only page extraction + TTS generation API. |
| D1 | `faiththruphysics-audio` | Canonical audio metadata table using `audio_tracks`. |
| R2 | `theophysics-media` or `faiththruphysics-audio` | Store generated `.mp3` files. |
| Worker route | `/api/audio*` on `faiththruphysics.com` | Public metadata endpoint for player lookup. |
| Admin endpoint | protected path only | Generate or regenerate audio for a slug. |

Keep generation manual/admin-triggered first. Do not set a site-wide cron until quality, cost, and file naming are proven.

## Clean Text Extraction Rules

The extraction step should use browser DOM parsing, not raw HTML or Markdown.

Preferred extraction:

1. Fetch the page HTML.
2. Parse with `HTMLRewriter` or a controlled DOM parser in a build/admin script.
3. Select the main article container, such as `main`, `article`, `[data-tts-source]`, or `.content`.
4. Remove `script`, `style`, `nav`, `footer`, `header`, `audio`, `video`, forms, buttons, and injected components.
5. Remove definition drawers, citations, internal notes, and navigation unless explicitly marked for narration.
6. Normalize whitespace.
7. Store the extracted text preview before generating audio.

Recommended page markup:

```html
<main data-tts-source data-audio-slug="example-slug">
  ...
</main>
```

Optional exclusion marker:

```html
<aside data-tts-exclude>
  Definitions, notes, or navigation not meant for narration.
</aside>
```

## Minimal D1 Contract

Use the existing local schema as the starting point:

```sql
audio_tracks(article_slug, series, mode, url, title, duration_seconds, transcript_url, is_default)
```

The player can then call:

```text
/api/audio?slug=<article-slug>
/api/audio?slug=<article-slug>&mode=tts
```

## Safety Notes

Do not copy Cloudflare secrets into this repo. During audit, at least one existing Worker showed plain-text environment values in its settings. Those should be rotated or moved to proper secret bindings before relying on that Worker.

Do not overwrite the current R2 audio catalog. Generated trial files should go under a new prefix first, for example:

```text
audio/generated/<slug>/<mode>.mp3
```

## How To Re-Find This Later

Search terms:

```powershell
rg -n "Cloudflare Audio/TTS Pipeline|faith-audio-pipeline|audio_tracks|mda-tts-sampler|theophysics-media-pipeline" .
```

Cloudflare resources to check:

```powershell
wrangler whoami
wrangler d1 list
wrangler r2 bucket list
wrangler deployments list --name mda-tts-sampler
wrangler deployments list --name theophysics-media-pipeline
```

This audit file is the canonical handoff for the Cloudflare audio/TTS experiment unless a later implementation README supersedes it.
