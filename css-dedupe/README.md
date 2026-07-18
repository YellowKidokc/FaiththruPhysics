# CSS Dedupe Kit — strip duplicated inline CSS, exact-match-or-keep

**Approved by David, July 18 2026**: strip the copy-pasted inline CSS from all
in-scope families so the canonical top bar (pills + classification bar in the
header) can go on everything. `isomorphism/` is **excluded** by David's ruling —
scope-only there, no dedupe. Subdomains, components, and apps are out of scope
entirely.

## What's in the kit

| File | What it is |
|------|------------|
| `dedupe_table.json` | 50 promoted block hashes → shared file, deploy path, occurrence counts. Covers **679 of 752 (90%)** inline style blocks across the in-scope families. |
| `raw/*.css` | The exact bytes of each promoted block (first occurrence), UNSCOPED. 477 KB replacing ~11 MB of page-inline duplication. |
| `css_dedupe.py` | Drop-in lookup module for the migrator. Pure functions, no I/O side effects, no scoper. |

## The rule (constitutional shape: exact structure or keep)

While the migrator disassembles a page, each inline `<style>` block is hashed
(whitespace-normalized SHA-1). **Exact match** with a promoted block → the block
is replaced with a `<link>` to the shared file, in the same cascade position.
**Any miss → the block is kept on the page**, scoped by the migrator's existing
scoper, exactly as today. Nothing custom is ever deleted. Rendering of matched
pages is identical by construction — the same rules load from a file instead of
inline.

## Integration steps (operator, on the machine with the migrator)

1. Promote: run each `raw/*.css` through the migrator's **existing**
   `scope_legacy_css()` (single source of truth — do NOT write a second scoper)
   and write the scoped output to `/assets/legacy/<same-name>.css` in the site
   repo. The deploy paths in `dedupe_table.json` already point there.
2. Weld: in `migrate_canonical_shell.py`, at the point where inline style
   blocks are collected for scoping, add the lookup from `css_dedupe.py`
   (usage sketch in that file's docstring — ~10 lines).
3. Dry-run the 18-page test set, then a full family (recommend `mda/`: 84
   pages, 4 distinct blocks, 95% dupe). Verify: pages shrink, render
   identically, unmatched blocks still present and scoped.
4. David's YES per family, apply through the registered repair path, ledger as
   usual.

## Numbers by family (pages / distinct blocks / dupe rate)

genesis-to-quantum 110/8/93% · moral-decline 106/5/95% · one-page-stories
84/11/87% · mda 83/4/95% · duality-project 36/5/88% · master-equation 34/3/91% ·
consciousness 22/3/86% · formal-papers 16/3/81% · forge-proofs 15/2/87% ·
proof-architecture 15/2/87% · cross-domain 13/2/85% · three-truths 13/4/76% ·
Introduction to Theophysics 13/2/85% · Axiom Layer 11/1/91%

**Excluded**: isomorphism (58 distinct blocks in 92 pages — hand-styled,
David's ruling: leave alone), subdomains (837 pages, separate sites),
components/proof-explorer/data-viz (apps and snippets).

After this lands, a family's look is edited in ONE file (`/assets/legacy/
<family>.css`) and every page follows on rebuild — fix the generator, not the
instances.
