# Canonical Page Shell

Canonical date: 2026-07-10
Canonical version: `ftp-shell-v2.5.1`

This folder is the current reusable Faith Through Physics page shell.

It is separate from the older `topbar/` scripts that audit or inject legacy
topbar/component chains. Those scripts may still be useful for old repairs, but
this folder is the clean source for the full page shell built today.

## Files

| File | Purpose |
|---|---|
| `index-shell-v2.5.1.full.html` | Complete assembled reference page. |
| `index-shell-v2.full.html` | Older v2 reference retained for comparison only. |
| `shell-top.html` | Reusable top shell: document head, topbar, verification panel, v2.5.1 player band, article wrapper, and player/content boundary. |
| `content-slot.example.html` | Replaceable page data and article body: JSON payload, title, subtitle, byline, High School / College / PhD layers, claims, proofs, and inline MTL blocks. |
| `shell-bottom.html` | Reusable bottom shell: article close, mini player, layer carry marker, footer system, on-page Proof/MTL layers, and JavaScript runtime. |
| `assemble_shell.py` | Split, assemble, and exact-match check utility. |
| `split_v251_shell.py` | Rebuilds the canonical split from a full v2.5.1 shell file. |
| `verify_shell_contract.py` | Verifies top/bottom shell hashes, lengths, and required page signals. |
| `shell-contract.v2.5.1.json` | Locked manifest for the approved v2.5.1 shell pieces. |

## Important Shape

The JSON payload and title block belong in the content slot, not in `shell-top.html`.

That means `shell-top.html` can stay identical across a whole series, while each
page swaps only `content-slot.example.html` or a generated replacement.

The reusable page build is:

```text
shell-top.html + content-slot.html + shell-bottom.html = index-shell-v2.5.1.full.html
```

Check exact recomposition:

```powershell
python D:\GitHub\Python-WEB\topbar\canonical-page-shell\assemble_shell.py check
```

Check the shell contract on any assembled page:

```powershell
python D:\GitHub\Python-WEB\topbar\canonical-page-shell\verify_shell_contract.py check D:\path\to\page.html
```

The contract check is deliberately stricter than a visual scan:

- top shell must match the approved character count, byte count, and SHA-256
- bottom shell must match the approved character count, byte count, and SHA-256
- content must contain `shell-data`, High School / College / PhD layers, claims, MTL, and all four audio kinds
- `--strict-content` can be used only for the reference/example page, because real article content is supposed to differ

Assemble a new page:

```powershell
python D:\GitHub\Python-WEB\topbar\canonical-page-shell\assemble_shell.py assemble `
  --content D:\path\to\new-content-slot.html `
  --out D:\path\to\new-page.html
```

Re-split the full reference page:

```powershell
python D:\GitHub\Python-WEB\topbar\canonical-page-shell\assemble_shell.py split
```

## Content Slot Contract

The content slot starts with:

```html
<!-- FTP_CONTENT_SLOT:START insert page JSON + page-specific content below -->
```

It owns:

- `<h1 data-shell-part="article.title">`
- `<script id="shell-data" type="application/json">`
- `.ftp-subtitle`
- `.ftp-byline`
- `[data-reader-layer="highschool"]`
- `[data-reader-layer="college"]`
- `[data-reader-layer="phd"]`
- inline `.ftp-claim-sentence` spans
- inline `.ftp-mtl-block` and `.ftp-mtl-full` blocks

## JSON Inputs

The inline JSON lives in `content-slot.example.html` inside:

```html
<script id="shell-data" type="application/json">
```

Primary inputs:

- `page`: title, subtitle, series, date, prev, next
- `domains`: topbar domain pills
- `verification`: topbar chi badge and verification panel
- `claims`: claims tab and claim drawers
- `proofs`: proof tab
- `mtl`: math translation tab
- `audio`: audio dock slots
- `audit`: final audit footer

Audio slot convention:

| Slot | Meaning |
|---|---|
| 1 | Read Aloud / TTS |
| 2 | Debate |
| 3 | Deep Dive |
| 4 | Critique |

## Workflow We Proved

1. Start from a broken or legacy page.
2. Strip the old topbar/audio/player clutter.
3. Leave a clean white/content area where the article body belongs.
4. Keep the v2.5.1 `ftp-player-band` in the top shell, outside the article.
5. Build or generate the content slot:
   - page JSON
   - title
   - subtitle
   - byline
   - High School / College / PhD layers
   - claims
   - inline MTL/proof hooks
6. Assemble:

```text
shell-top + content-slot + shell-bottom
```

7. Verify:
   - JSON parses
   - JavaScript parses
   - topbar buttons work
   - MTL opens all MTL blocks
   - Proof opens all proof rows
   - audio slots hydrate from `audio[]`
   - contract checker passes for canonical top/bottom

Do not use the older inline article audio dock as the target. The v2.5.1 target
uses `#ftpPlayerBand` above the article and keeps the on-page Proof Layer and
MTL Layer in the bottom shell.

## Do Not Confuse With Old Topbar Work

The old slim/static topbar and the older `TOP_BAR_CANONICAL.html` workflow are
not the current final page shell.

The current shell is identified by:

- `FTP_SPLIT:TOP_SHELL_START`
- `FTP_CONTENT_SLOT:START`
- `FTP_SPLIT:BOTTOM_SHELL_START`
- `id="shell-data"`
- `id="ftpTopBar"`
- `id="ftpPanel"`
- `id="ftpAudioDock"`
- `id="ftpPlayerBand"`
- `ftp.openMTLLayer()`
- `ftp.openProofLayer()`
