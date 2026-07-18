# Kimmy Handoff: Canonical Topbar / Gold Master Shell

Date: 2026-07-18

## Current Ruling

Use the Python-WEB gold-master page system as the forward path for article pages.

Do not run older topbar-only systems as the primary fix unless David explicitly asks for a legacy patch. The current approved direction is:

- one canonical shell
- one page JSON contract per article
- builder creates standalone HTML
- validator gates every built page

The live repo is the deploy target. Python-WEB is the build/toolbox repo.

## Repos and Paths

Live deploy repo:

`D:\GitHub\faiththruphysics-site-live`

Toolbox/build repo:

`D:\GitHub\Python-WEB`

Gold master package:

`D:\GitHub\Python-WEB\topbar\canonical-page-shell`

Key files:

- `canonical-gold-master.html`
- `canonical-page.schema.json`
- `build-page.js`
- `validate-page.js`
- `GOLD_MASTER_SYSTEM.md`
- `ZONE_CATALOG.md`
- `GOLD_MASTER_UPGRADE_REVIEW.md`
- `CREDENTIAL_CARD_SHELL_INTEGRATION.md`

## What Is Implemented Now

The implemented gold master already includes:

- compact fixed topbar
- High School / College / PhD reading-level pills
- panel toggle under the topbar
- top panel with verification cards
- Claims / Proof / MTL controls
- term/title pills rendered from `terms[]`
- flip-card term dialog rendered from the same JSON
- claim drawers tied to sentence-level claim IDs
- MTL layer from `mtl[]`
- audit layer from `audit{}`
- four audio slots from `audio[]`, safely disabled when URLs are blank

Validation proof from Codex on 2026-07-18:

```powershell
cd D:\GitHub\Python-WEB\topbar\canonical-page-shell
node validate-page.js pages/faithfulness.json
node build-page.js pages/faithfulness.json --out dist/codex-handoff-faithfulness.html --validate
node validate-page.js dist/codex-handoff-faithfulness.html
```

Result:

- `faithfulness.json`: PASS, 19/19
- `dist/codex-handoff-faithfulness.html`: PASS, 48/48

## What Is Not Yet Implemented

`CREDENTIAL_CARD_SHELL_INTEGRATION.md` describes a future `credentials[]` card zone.

That is a spec, not the active contract yet. The active schema currently requires:

- `page`
- `terms`
- `claims`
- `proofs`
- `mtl`
- `verification`
- `audio`
- `audit`

If credential cards are desired, update `canonical-page.schema.json`, `build-page.js`, `validate-page.js`, and `canonical-gold-master.html` together, then validate the sample page again.

## Safe Operator Sequence

1. Work in Python-WEB only while building.

```powershell
cd D:\GitHub\Python-WEB\topbar\canonical-page-shell
```

2. Validate source JSON.

```powershell
node validate-page.js pages\faithfulness.json
```

3. Build a single showpiece page.

```powershell
node build-page.js pages\faithfulness.json --out dist\faithfulness.html --validate
```

4. Open/inspect the built page visually.

Check:

- topbar is the compact canonical one
- reading-level pills switch real layers
- verification cards render in the panel
- term pills appear near the title/article intro area
- term pills open the flip-card dialog
- claim drawers open from claim-marked sentences
- MTL opens and closes as expected
- no old second topbar remains above or below it

5. Only after David says YES, copy the built HTML into the live repo path that should be replaced.

6. Commit in the live repo.

```powershell
cd D:\GitHub\faiththruphysics-site-live
git status -sb
git add <changed-files>
git commit -m "Apply canonical gold master shell to showpiece page"
git push origin HTML
```

## Guardrails

- Do not patch random legacy bars page-by-page if the page is being rebuilt through the gold master.
- Do not use `apply_faith_topbar.py` as the gold-master route. That is an older topbar-only injector.
- Do not treat `credentials[]` as available until the schema/builder/validator all support it.
- Do not broadly rewrite hundreds of pages before one showpiece page gets David's visual YES.
- Homepage is special and currently uses its own simplified chrome. Do not force the article shell onto `index.html`.

## Current Live Site Status

The live repo branch is `HTML`.

Recent homepage commits:

- `420cc701` Clean homepage chrome and dock controls
- `99e8e7df` Make homepage audio playback deliberate

The homepage now has simplified chrome and deliberate audio playback. The article-page gold master is the next path for the topbar/title-card system.

## Current Article Chrome Scan

Codex ran a scoped scan of live HTML files on 2026-07-18, excluding obvious backup/archive/staging folders.

Approximate results:

- canonical gold-master markers in live repo: `0`
- older `tp-top` style topbar pages: `415`
- classification-bar pages: `416`
- `tp-header-lip` pages: `101`
- site-shell asset pages: `17`

Interpretation:

The homepage is now cleaned up, but the article corpus is not yet on the gold-master shell. There are still many legacy article bars. That is expected. Kimmy should not try to hand-clean them all at once. Start with one showpiece built from the gold master, get David's visual YES, then migrate by family.
