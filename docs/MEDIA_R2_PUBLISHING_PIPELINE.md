# Media R2 Publishing Pipeline

This repo uses `scripts/build_media_manifest.py` to turn the local source vault at
`D:\GitHub\faiththruphysics-site-data` into a Cloudflare R2 publishing plan.

The script does not change source media. It scans, dedupes by sha1, assigns stable
R2 keys, writes the public manifest, and emits ignored working files under `work/`.

## Outputs

Default command:

```powershell
python .\scripts\build_media_manifest.py
```

Writes:

```text
assets/media-manifest.json
work/prepare-r2-media.ps1
work/upload-r2-media.ps1
work/register-audio-tracks.sql
work/media-publish-exceptions.json
```

## Publish Flow

1. Review `work/media-publish-exceptions.json` for ambiguous mappings.
2. Install or add `ffmpeg` to `PATH`.
3. Run `work/prepare-r2-media.ps1` to create web-ready staged files.
4. Run `work/upload-r2-media.ps1` to upload staged files to the `faiththruphysics-audio` R2 bucket.
5. Apply `work/register-audio-tracks.sql` to the `faiththruphysics-audio` D1 database.
6. Verify the site player with `/api/audio?slug=<slug>` and the public R2 URLs.

## R2 Layout

```text
audio/{series}/{slug}/{mode}.{ext}
video/{series}/{slug}/web.mp4
documents/{series}/{slug}/{filename}.pdf
images/{series}/{slug}/{filename}.{webp|png}
```

Audio modes match the site player:

```text
deep
debate
critique
tts
web
```

The public base URL defaults to:

```text
https://r2.faiththruphysics.com
```

Use `--public-base-url` to change it.
