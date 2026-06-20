# Faith Through Physics Audio Pipeline

Deployable Cloudflare Worker for turning site pages into playable audio.

This replaces the scattered experiments with one repo-owned pipeline:

1. Extract clean narration text from a page or supplied HTML.
2. Generate TTS audio through Workers AI.
3. Store generated MP3 and transcript text in R2.
4. Register the track in D1.
5. Serve `/api/audio?slug=...` for the site pill player.
6. Serve generated R2 files back through `/audio/generated/...` so the bucket does not have to be public for the first trial.

## Files

| File | Purpose |
| --- | --- |
| `src/index.js` | Worker implementation. |
| `schema.sql` | D1 audio catalog schema. |
| `wrangler.jsonc` | Ready-to-fill Wrangler config. |

## Required Cloudflare Resources

Suggested names:

| Resource | Name |
| --- | --- |
| Worker | `faith-audio-pipeline` |
| D1 | `faiththruphysics-audio` |
| R2 | `faiththruphysics-audio` or existing `theophysics-media` |

## Current Deployment

Deployed Worker:

```text
https://faith-audio-pipeline.davidokc28.workers.dev
```

Created resources:

| Resource | Name / ID |
| --- | --- |
| D1 | `faiththruphysics-audio` / `5d669471-8282-4d35-85a3-d19fede07f57` |
| R2 | `faiththruphysics-audio` |
| Secret | `ADMIN_TOKEN` set in Cloudflare and locally stored in ignored file `workers/audio-pipeline/admin-token.local.secret` |

Smoke test track:

```text
GET /api/audio?slug=smoke-test&mode=tts
```

## Setup

Already completed for the current deployment. For a rebuild from scratch, run from this folder:

```powershell
wrangler d1 create faiththruphysics-audio
wrangler r2 bucket create faiththruphysics-audio
```

Copy the returned D1 `database_id` into `wrangler.jsonc`, then run:

```powershell
wrangler d1 execute faiththruphysics-audio --file .\schema.sql --remote
wrangler secret put ADMIN_TOKEN
wrangler deploy
```

If using the existing `theophysics-media` bucket, change the `bucket_name` in `wrangler.jsonc` before deploying.

## Public Endpoints

```text
GET /health
GET /api/audio?slug=<article-slug>
GET /api/audio?slug=<article-slug>&mode=tts
GET /audio/generated/<series>/<slug>/<mode>.mp3
```

`/api/audio` matches the existing site player expectation.

By default, generated audio URLs use the Worker origin. If you later add a public R2 custom domain, set `PUBLIC_AUDIO_BASE_URL` in `wrangler.jsonc`.

## Admin Endpoints

Send either:

```text
Authorization: Bearer <ADMIN_TOKEN>
```

or:

```text
X-Admin-Token: <ADMIN_TOKEN>
```

Generate audio from a live page:

```powershell
$body = @{
  url = "https://faiththruphysics.com/one-page-stories/example.html"
  slug = "example"
  title = "Example"
  series = "one-page-stories"
  mode = "tts"
  speaker = "luna"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "https://faith-audio-pipeline.<your-subdomain>.workers.dev/api/generate" `
  -Headers @{ Authorization = "Bearer $env:FAITH_AUDIO_ADMIN_TOKEN" } `
  -Body $body `
  -ContentType "application/json"
```

Preview extraction without generating audio:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "https://faith-audio-pipeline.<your-subdomain>.workers.dev/api/extract" `
  -Headers @{ Authorization = "Bearer $env:FAITH_AUDIO_ADMIN_TOKEN" } `
  -Body (@{ url = "https://faiththruphysics.com/" } | ConvertTo-Json) `
  -ContentType "application/json"
```

Register an already-hosted audio URL:

```powershell
$body = @{
  slug = "example"
  series = "one-page-stories"
  mode = "tts"
  url = "https://media.example/audio/example.mp3"
  title = "Example"
  isDefault = $true
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "https://faith-audio-pipeline.<your-subdomain>.workers.dev/api/register" `
  -Headers @{ Authorization = "Bearer $env:FAITH_AUDIO_ADMIN_TOKEN" } `
  -Body $body `
  -ContentType "application/json"
```

## Page Markup Contract

Best extraction target:

```html
<main data-tts-source data-audio-slug="example-slug">
  ...
</main>
```

Exclude definitions, notes, footnotes, widgets, and navigation:

```html
<aside data-tts-exclude>
  This will not be narrated.
</aside>
```

The extractor also removes common page chrome automatically: `script`, `style`, `nav`, `header`, `footer`, `audio`, `video`, forms, buttons, and site shell/player elements.

## Voice Testing

The inherited `mda-tts-sampler` experiment used Deepgram Aura voices:

```text
luna, orpheus, athena, apollo, atlas, aurora, hera, hermes, odysseus, thalia, zeus
```

This Worker defaults to `luna`. Change `speaker` per request while testing.

## Old Cloudflare Experiments

Do not delete these until `faith-audio-pipeline` is deployed and verified:

| Resource | Action After Verification |
| --- | --- |
| `mda-tts-sampler` | Keep as voice sampler or delete after voice choice is finalized. |
| `theophysics-media-pipeline` | Delete or archive after this Worker handles real TTS generation. |
| `theophysics-tts` / `nerve-tts-pwa` | Keep only if still useful for manual testing. |
