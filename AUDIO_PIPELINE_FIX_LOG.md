# Audio Pipeline Fix Log
**June 27, 2026 — Claude (Opus) responding to Kimi's audit**

## What was fixed (3 files modified)

### 1. `components/d1-audio-worker.js` — Slug normalization + health endpoint
- **Problem:** Pages send path-style slugs (`genesis-to-quantum/gtq-01-foo`) but D1 stores bare slugs (`gtq-01-foo`). Worker did exact match → always empty.
- **Fix:** Added slug normalization: `if (slug.includes("/")) slug = slug.split("/").pop();`
- **Bonus:** Added `/health` endpoint for diagnostics.

### 2. `components/d1-audio-schema.sql` — Mode name alignment
- **Problem:** Schema/seed used mode `debate` but the player UI uses `data-mode="podcast"` and `tpBindTracks()` looks up `art['podcast']`.
- **Fix:** Changed `debate` → `podcast` in the schema comment and seed data.

### 3. `scripts/build_media_manifest.py` — IMAGE_EXTS + mode name
- **Problem 1:** `IMAGE_EXTS` was `{".png", ".webp"}` — 18 JPGs in faiththruphysics-site-data were excluded from manifests.
- **Fix:** Added `.jpg` and `.jpeg` to IMAGE_EXTS.
- **Problem 2:** `MODE_PATTERNS` mapped debate-style files to mode `debate` instead of `podcast`.
- **Fix:** Changed pattern output from `debate` to `podcast`, added `podcast|pod` to the regex.

## What still needs to happen (manual steps)

### Step 1: Regenerate the manifest and companion scripts
```powershell
cd D:\GitHub\faiththruphysics-site
python scripts/build_media_manifest.py --include-local-paths
```
This creates/updates:
- `assets/media-manifest.json` (full manifest)
- `work/register-audio-tracks.sql` (D1 registration — now with `podcast` mode)
- `work/prepare-r2-media.ps1` (staging script)
- `work/upload-r2-media.ps1` (R2 upload script)

### Step 2: Stage audio files
```powershell
.\work\prepare-r2-media.ps1
```

### Step 3: Upload to R2
```powershell
.\work\upload-r2-media.ps1
```

### Step 4: Apply SQL to D1
```powershell
# First apply the schema if not already done:
wrangler d1 execute faiththruphysics-audio --file=components/d1-audio-schema.sql
# Then register all tracks:
wrangler d1 execute faiththruphysics-audio --file=work/register-audio-tracks.sql
```

### Step 5: Redeploy the worker
```powershell
cd workers/audio-pipeline   # or wherever the wrangler project lives
wrangler deploy
```

### Step 6: Verify
```powershell
# Health check
curl https://faith-audio-pipeline.davidokc28.workers.dev/health

# Test a slug that pages actually send (path-style):
curl "https://faith-audio-pipeline.davidokc28.workers.dev/api/audio?slug=genesis-to-quantum/gtq-01-measurement-collapsed-reality"

# Should now return tracks instead of empty array
```

## Items NOT addressed (lower priority)

1. **Consciousness script conflicts** — `work/upload-consciousness-r2-media.ps1` and `work/register-consciousness-audio-tracks.sql` are redundant. After regenerating the manifest, the main scripts include all consciousness tracks. Delete the standalone consciousness scripts.

2. **Verifier/injector class mismatch** — `mda/verify_pill_player.py` and `mda/inject_pill_player.py` look for `.tp-pill-bar` but pages use `.tp-player-block`. These scripts need to be updated to match the actual class name.

3. **Landing page players** — `index.html`, `mda/index.html`, and other directory index files have the CSS/JS loaded but no player markup. These are intentionally player-less (they're navigation pages, not articles).

4. **Stale `shared/data/media-manifest.json`** — This is an older hand-maintained file with different schema and placeholder R2 URLs. Once the generated manifest is confirmed working, this file should be removed or replaced with a symlink to `assets/media-manifest.json`.
