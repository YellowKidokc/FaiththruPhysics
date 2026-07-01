# Cloudflare Worker Map

## Runtime translation service

- Worker folder: `D:\GitHub\faiththruphysics-site\workers\mtl-service`
- Config: `D:\GitHub\faiththruphysics-site\workers\mtl-service\wrangler.jsonc`
- Entry: `D:\GitHub\faiththruphysics-site\workers\mtl-service\src\index.js`
- Worker name: `faith-mtl-worker`
- D1 binding: `DB`
- D1 database name: `faiththruphysics-mtl`

## API

- `GET /health`
- `GET /api/translate?latex=...&mode=easy|standard|academic|audio_safe`
- `POST /api/batch`

Current client base URL in the live site:

- `https://faith-mtl-worker.davidokc28.workers.dev`

## Live page client

- File: `D:\GitHub\faiththruphysics-site\shared\js\mtl-worker-client.js`

Current behavior:

- Collects MathJax-rendered equations from the page.
- Sends them to the worker in batches.
- Inserts translation callouts after rendered math.
- Maps shell mode `math` to MTL mode `standard`.
- Re-renders on reader-mode change.

## Important distinction

There are two MTL systems in the repo:

### Legacy overlay path

- `shared/js/mtl-overlay.js`
- `shared/js/mtl-overlay-loader.js`
- `shared/data/mtl-overlay-translations.json`
- local uploader: `faiththruphysics-site-data\mtl-admin\mtl_uploader.pyw`

### Current worker path

- `workers/mtl-service`
- `shared/js/mtl-worker-client.js`

Prefer the worker path for new runtime translation work.
