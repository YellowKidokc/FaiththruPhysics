# Canon Ingestion + Test Artifact Summary

Generated: 2026-07-02
Source run: `CANON` + `MASTER_EQUATION_TEST` from `\\192.168.2.50\h_hp\Desktop 2`
Destination: `Z:\_VAULTS\_Theophysics_v5\00_Canonical`

## Executive summary
- Copy-only migration to the 5-class canon structure completed with no source deletions.
- Desktop or ad hoc conversion output was not generated; all work stayed in the vault.
- Latest run completed with **8 unresolved copy errors** (missing/broken source references).

## Ingestion totals from latest two-folder run
| Artifact type | Files imported |
|---|---:|
| Python (`.py`) | 163 |
| Colab notebooks (`.ipynb`) | 128 |
| Verification artifacts | 78 |
| Publication docs | 30 |
| Copy errors | 8 |

## Current vault distribution (5 canonical classes + workflow folders)
| Folder | Files |
|---|---:|
| `00_CANON_LOCK` | 1565 |
| `01_REFERENCE_CANON` | 1690 |
| `02_PROOF_AND_TEST_CANON` | 557 |
| `03_EVIDENCE_CANON` | 279 |
| `04_HISTORICAL_CANON` | 0 |
| `05_PUBLICATION_CANON` | 769 |
| `_STAGING` | 1 |
| `_QUARANTINE` | 184 |
| `_ARCHIVED_FROM_CANONICAL` | 665 |
| `_TOOLS` | 4 |

## Proof/Test canon breakdown (newly mapped groups)

### Python groups (`02_PROOF_AND_TEST_CANON/Python`)
| Group | Files |
|---|---:|
| `desktop_import` | 189 |
| `Cross_Domain_Arsenal` | 5 |
| `TH_Philosophy` | 1 |
| `03_EVIDENCE_CANON` | 3 |

### Colab groups (`02_PROOF_AND_TEST_CANON/Colab_Notebooks`)
| Group | Files |
|---|---:|
| `desktop_import` | 180 |

### External verification groups (`02_PROOF_AND_TEST_CANON/External_Verification`)
| Group | Files |
|---|---:|
| `desktop_import` | 166 |
| `Cross_Domain_Arsenal` | 1 |
| `02_EXTERNAL_VERIFICATION` | 1 |

## Publication, Reference, and Evidence groups

### Publication groups (`05_PUBLICATION_CANON/articles`)
| Group | Files |
|---|---:|
| `desktop_import` | 542 |

### Reference groups (`01_REFERENCE_CANON`)
| Group | Files |
|---|---:|
| `Physics` | 783 |
| `Scripture` | 75 |
| `Theology` | 85 |
| `Philosophy` | 435 |
| `History` | 185 |
| `Information_Theory` | 86 |
| `Mathematics` | 41 |

### Evidence groups (`03_EVIDENCE_CANON`)
| Group | Files |
|---|---:|
| `Worldview_Comparisons` | 104 |
| `Worldviews` | 24 |
| `Isomorphism_Scorecards` | 151 |

## Why each class exists (for readers)
- `00_CANON_LOCK` = active ruling statements and current canonical framework.
- `01_REFERENCE_CANON` = external source material your framework relies on.
- `02_PROOF_AND_TEST_CANON` = executable evidence: scripts, notebooks, and verification runs.
- `03_EVIDENCE_CANON` = supporting studies, comparisons, and scorecards.
- `04_HISTORICAL_CANON` = superseded material retained for traceability (currently empty after cleanup).
- `05_PUBLICATION_CANON` = public-facing or publication-ready outputs.
- `_STAGING` / `_QUARANTINE` / `_ARCHIVED_FROM_CANONICAL` = uncertain, conflicting, or superseded holding areas.

## Significance of the latest run
1. This run operationalized a **source-to-canons** pipeline that separates raw artifacts from claims.
2. Most testable content from the two source folders landed in `02_PROOF_AND_TEST_CANON`, making reproducibility and audit pathways explicit.
3. Reference sources were normalized without being treated as proof claims.
4. Publication materials were kept distinct from canonical proof structures.
5. No destructive moves were done in this phase; this is safe for review and rerouting.

## Current next step (recommended)
Use the **TKE 4Q Folder Router** on `desktop_import` batches in `--dry-run`, then promote to final folders by confirmed `STATE / TYPE / SCOPE / ACTION` decisions.
