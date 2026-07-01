# NotebookLM-to-site picture placement skill (pilot workflow)

## Purpose
This is the operational method to place images inside canonical Markdown pages without guessing source labels. It is built for cross-AI reuse.

## Scope for this pass
- Consciousness
- Genesis to Quantum
- Moral Decline (MDA)

## Placement invariants
1. Do not place an image in the opening paragraph or first visible media block.
2. Put the first page image at or after the second paragraph unless there is a clear reason (e.g., long header-only pages).
3. Use only confirmed filenames.
4. If the only known visual is `/media/media/...`, prefer that route over broken `../images/...` paths.
5. Preserve existing local references if they are clearly correct. If they are old/invalid, migrate only when a safe target exists.
6. If label/title confidence is low, keep `REVIEW` status and leave file unchanged.

## Step-by-step for each page
1. Read the first 3 content blocks (excluding H1/H2 frontmatter and nav).
2. Detect existing image references:
   - `![](... )`
   - `<img ...>`
3. If no image exists and a confirmed series-level candidate exists in `/media/media`, insert one image after second paragraph.
4. If image exists too early (first paragraph), move it down:
   - Remove first image line.
   - Insert same/new image after second paragraph boundary.
5. For MDA and GTQ pages, keep image semantic to local topic where possible:
   - GTQ: use `gtq-*` assets where available.
   - MDA: use `mda/*` assets with matching names.
6. Add optional markdown style:
   - `![Alt text](/media/media/<filename>.webp){loading="lazy"}`
7. Append decision log (Committed / Reviewed / Blocked) in your notes.

## Commit convention for this workflow
- `Committed`: inserted/moved with explicit matching evidence.
- `Reviewed`: intentionally deferred because no confident match.
- `Blocked`: image exists but source was not recoverable.

## Pilot outcomes (2026-06-30)

| Series | Page | Action | Media used | Location decision | Notes |
|---|---|---|---|---|---|
| Consciousness | `consciousness/index.canonical.md` | Inserted | `/media/media/series-opener.webp` | After formula/intro, before article index | No original image existed on the page. Used series-level fallback. |
| Consciousness | `consciousness/consciousness-chi-field-action.canonical.md` | Inserted | `/media/media/law-4-information-truth-logos.webp` | After paragraph in SEC.0 | No previous image existed; candidate is provisional and should be reviewed for series fit. |
| Genesis to Quantum | `genesis-to-quantum/intro/index.canonical.md` | Inserted | `/media/media/gtq-series-grid.webp` | After opening paragraph | No existing page image; used GTQ series fallback. |
| Genesis to Quantum | `genesis-to-quantum/intro/gtq-01-measurement-collapsed-reality-N.canonical.md` | Moved | `/media/media/gtq-01-hero-measurement-that-collapsed-reality.webp` | After second-paragraph explanatory sentence | Replaced old `../images/gtq-01/slide_01.webp` slot to satisfy placement rule. |
| MDA | `mda/01-story-thread/MDA-001-story-introduction.canonical.md` | Moved | `/media/media/the-observer-collapsed-conv-6.webp` | Moved lower into page; replaced second image with local canonical path | Also migrated first/second image paths from `../images/...` to `/media/media/...` for deterministic references. |
| MDA | `mda/04-collapse-mechanisms/MDA-020-phase-transition.canonical.md` | Normalized path | `/media/media/phase-transition-conv-10.webp` | Kept in same structural location | Existing path converted to repository media URL; placement already acceptable. |

## Review queue (for another AI)
- Validate whether the newly inserted Consciousness images are semantically correct:
  - `consciousness/index.canonical.md`
  - `consciousness-chi-field-action.canonical.md`
- Confirm that converted `/media/media/...` paths render in production context.
- Continue the same method to remaining pages in series that still rely on unresolved `../images/...` references.

## Handoff notes
- Keep this conservative: if a page has a clearly better Studio-derived image URL/slug, replace these provisional choices.
- Do not add a page-leading hero unless style requires it; second-paragraph-or-later is the default for this site pass.

## Command-line handoff package

For machine-assisted continuation, use:
- [Python-WEB image placement runner](D:/GitHub/Python-WEB/workflows/image-placement-runner/README.md)

Dry run (show proposed moves/inserts):
```powershell
cd D:\\GitHub\\Python-WEB\\workflows\\image-placement-runner
.\\run-image-placement.ps1
```

Apply edits:
```powershell
.\\run-image-placement.ps1 -Apply
```
