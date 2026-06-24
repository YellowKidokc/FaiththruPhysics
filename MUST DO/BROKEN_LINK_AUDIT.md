# BROKEN LINK AUDIT — faiththruphysics.com Homepage
## June 22, 2026 · Opus audit for Codex/Kimi

---

## THE PROBLEM

The homepage (index.html) has ~40+ internal links. Most are broken because:

1. **One-page-stories files don't exist at root level.** Homepage links to `one-page-stories/theophysics-the-full-explanation.html` but the actual files are in subdirectories like `one-page-stories/truth-and-pushback/` and `one-page-stories/starting-point/`. Also, most only have `-interlude.html` versions, not the base filenames the homepage expects.

2. **Case-sensitive path mismatches.** Homepage links to `Convergence_Series/` but the directory is `convergence-series/` (if it exists at all).

3. **Directories that don't exist.** Several link targets point to directories not in the repo.

---

## BROKEN LINKS — ONE-PAGE-STORIES

All of these homepage links point to files that DO NOT EXIST at the expected path:

| Homepage link | Status | Nearest match |
|---|---|---|
| `one-page-stories/theophysics-the-full-explanation.html` | MISSING | `truth-and-pushback/theophysics-the-full-explanation-interlude.html` |
| `one-page-stories/The_Logos_Thesis_v3.html` | MISSING | `truth-and-pushback/The_Logos_Thesis_v3-interlude.html` |
| `one-page-stories/everybodys-got-it-wrong.html` | MISSING | `truth-and-pushback/everybodys-got-it-wrong-interlude.html` |
| `one-page-stories/character-of-god-from-physics.html` | MISSING | `truth-and-pushback/character-of-god-from-physics-interlude.html` |
| `one-page-stories/salvation-algorithm.html` | MISSING | Needs search |
| `one-page-stories/ten-laws-full-treatment.html` | MISSING | Needs search |
| `one-page-stories/the-same-equation.html` | MISSING | `truth-and-pushback/the-same-equation-interlude.html` |
| `one-page-stories/heaven-hell-attractor-states.html` | MISSING | Needs search |
| `one-page-stories/no-drift-law-synthesis.html` | MISSING | `truth-and-pushback/no-drift-law-synthesis-interlude.html` |

## BROKEN LINKS — SERIES DIRECTORIES

| Homepage link | Status | Notes |
|---|---|---|
| `Convergence_Series/cns-01-the-playing-field.html` | MISSING | Dir doesn't exist. Case mismatch? Should be convergence-series? |
| `Convergence_Series/cns-02-the-evidence.html` | MISSING | Same |
| `Convergence_Series/cns-05-the-judgment-layer.html` | MISSING | Same |
| `Logos_Papers/index.html` | MISSING | No Logos_Papers directory in repo |
| `logos-papers/logos-01.html` | MISSING | No logos-papers directory in repo |
| `be-glad-youre-a-loser/bgl-01-be-glad-youre-a-loser.html` | MISSING | No directory in repo |
| `family-tests/we-ran-the-tests.html` | MISSING | No family-tests directory in repo |

## LINKS THAT WORK (confirmed)

| Link | Status |
|---|---|
| `moral-decline/index.html` | OK — file exists |
| `genesis-to-quantum/index.html` | OK — file exists |
| `convergence-deep/` | Directory exists, needs index.html check |
| `consciousness/` | Directory exists, needs index.html check |
| `master-equation/` | Directory exists, needs index.html check |
| `formal-papers/` | Directory exists, needs index.html check |
| `proof-architecture/` | Directory exists, needs index.html check |
| `proof-explorer/` | Directory exists, needs index.html check |
| Zenodo external links | OK — external |

---

## FIX OPTIONS

### Option A: Fix the links (update index.html to point to actual file locations)
Fastest. Just rewrite the href values to match where the files actually are.

### Option B: Fix the files (create files at the expected locations, or add redirects)
Better long-term. Either move/copy files to where the links expect them, or create a `_redirects` file for Cloudflare Pages.

### Option C: Both (recommended)
1. For one-page-stories: create flat copies or symlinks at the root of `one-page-stories/` so `one-page-stories/theophysics-the-full-explanation.html` resolves.
2. For missing directories (Convergence_Series, Logos_Papers, etc.): either create them with content or update index.html links to point to where the content actually lives.
3. Add entries to `_redirects` for any legacy URLs that might be bookmarked.

---

## CODEX PROMPT

```
Audit and fix all broken internal links in D:\GitHub\faiththruphysics-site\index.html.

The homepage has ~40+ href values pointing to files and directories that don't exist at the expected paths.

Key problems:
1. one-page-stories/ links point to root-level filenames but actual files are in subdirectories (starting-point/, truth-and-pushback/, etc.) and have -interlude.html suffixes.
2. Convergence_Series/ doesn't exist (case mismatch or missing).
3. Logos_Papers/ and logos-papers/ don't exist.
4. be-glad-youre-a-loser/ and family-tests/ don't exist.

For each broken link:
1. Search the repo for the nearest matching file.
2. If found: update the href to the correct path.
3. If not found: comment it out with <!-- BROKEN: original-href --> and add a TODO.
4. Add a _redirects entry mapping the old path to the new one.

Do NOT delete any content. Do NOT change anything except href values.
After fixing, list all changes in a summary table.
```

---

*Audited by Opus · June 22, 2026*