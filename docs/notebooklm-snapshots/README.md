# Cursor — NotebookLM Studio Snapshots (2026-06-22)

Screenshots collected by **Cursor** during the NotebookLM upload/download audit workflow. Each image captures the **Sources** (uploaded files), **Chat** summary, and **Studio** panel (generated outputs: Audio Overview, Slide Deck, Video Overview, etc.).

## MDA notebooks

| File | Notebook |
| --- | --- |
| `mda/mda-03-notebooklm-studio-snapshot-mda2-parts-03-04-05-2026-06-22.png` | MDA Parts 03–05 (shared snapshot) |
| `mda/mda-04-notebooklm-studio-snapshot-mda2-parts-03-04-05-2026-06-22.png` | Same as above (duplicate filename for MDA-04) |
| `mda/mda-05-notebooklm-studio-snapshot-mda2-parts-03-04-05-2026-06-22.png` | Same as above (duplicate filename for MDA-05) |
| `mda/mda-06-notebooklm-studio-snapshot-2026-06-22.png` | MDA 3: Part 06 — Signal Went Dark |
| `mda/mda-07-notebooklm-studio-snapshot-mda4-part-07-2026-06-22.png` | MDA Part 07 |
| `mda/mda-08-notebooklm-studio-snapshot-mda5-part-08-2026-06-22.png` | MDA Part 08 |
| `mda/mda-09-notebooklm-studio-snapshot-mda6-part-09-2026-06-22.png` | MDA Part 09 |
| `mda/mda-10-notebooklm-studio-snapshot-mda7-part-10-2026-06-22.png` | MDA Part 10 |

## One-page story notebooks

| File | Notebook |
| --- | --- |
| `one-page-stories/convergence-series-scientific-method-notebooklm-studio-snapshot-2026-06-22.png` | Convergence Series: Scientific Method (23 sources) |
| `one-page-stories/lean4-theophysics-corpus-notebooklm-studio-snapshot-2026-06-22.png` | Theophysics Research Initiative: Lean 4 Corpus |

## Audit report

See `notebooklm-output-audit-2026-06-22.md` for the full download-status audit of the 15-story NotebookLM batch.

## Copy to desktop share

From a machine on your LAN that can reach `\\192.168.2.50\h_hp\Desktop\Notebook LM`, run:

```powershell
.\copy-to-notebook-lm-desktop.ps1
```

Files land in a subfolder so they stay separate from your live NotebookLM work:

```
\\192.168.2.50\h_hp\Desktop\Notebook LM\Cursor - NotebookLM\
```

## Studio rename rules (pinned audio)

See `RENAME-WORKFLOW.md` for the full steps. Short version:

| Studio label | Rename prefix |
| --- | --- |
| Deep Dive | `DD` |
| Debate | `AD` |
| Critique | `AC` |

Three dots → Rename → add prefix at front. Screenshot Studio after each notebook.
