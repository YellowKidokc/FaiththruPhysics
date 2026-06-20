# Article Classification Taxonomy
## faiththruphysics.com · 20 Categories
## June 19, 2026

---

## The 20 Categories

| # | Tag | Label | Color | What it covers |
|---|-----|-------|-------|----------------|
| 1 | physics | Physics | #4a9eff | Laws, forces, equations, physical processes |
| 2 | theology | Theology | #c87050 | Scripture, doctrine, church history |
| 3 | math | Mathematics & Proof | #a855f7 | Lean 4, formal verification, derivations |
| 4 | info-theory | Information Theory | #3bb39a | Shannon, entropy, signal/noise, Logos |
| 5 | consciousness | Consciousness | #f59e0b | Observer, measurement, hard problem |
| 6 | trinity | The Trinity | #d4af37 | Father, Son, Spirit, triadic structure |
| 7 | grace | Grace & Salvation | #22c55e | Atonement, Cross, restoration, phase transition |
| 8 | entropy | Sin & Entropy | #ef4444 | Decoherence, decay, Second Law, moral decline |
| 9 | justice | Justice & Mercy | #e879a0 | Courts, paradox, substitution, uniqueness |
| 10 | free-will | Free Will | #8b5cf6 | Choice, determinism, the W variable |
| 11 | adversary | The Adversary | #6b7280 | Satan, anti-properties, attack surface, entropy agent |
| 12 | genesis | Genesis & Creation | #92400e | Fall, quantum event, original coherence, Garden |
| 13 | ten-laws | The Ten Laws | #d4af37 | Law-by-law mappings, symmetry pairs |
| 14 | master-eq | Master Equation | #f0c659 | Chi field, ten variables, product structure |
| 15 | method | Method & Epistemology | #9a7c3a | 7Q, bilateral audit, isomorphic event density |
| 16 | evidence | Empirical Evidence | #2dd4bf | PEAR, GCP, MDA 5.7σ, Genesis curve, data |
| 17 | society | History & Society | #64748b | Moral decline, politics, civilization, Amish |
| 18 | cross-domain | Cross-Domain Bridge | #e2725b | Isomorphism, mapping, convergence, dual projection |
| 19 | story | Personal & Narrative | #f5d0a9 | David's journey, testimony, how it started |
| 20 | ai | AI & Collaboration | #60a5fa | David Effect, multi-AI convergence, preference engine |

---

## How it works on the site

Every article gets 2-5 tags from this list. A JSON file maps them:

```json
{
  "articles": [
    {
      "file": "salvation-algorithm.html",
      "folder": "one-page-stories",
      "title": "The Salvation Algorithm",
      "tags": ["grace", "math", "theology", "cross-domain"],
      "audience": ["believer", "skeptic"],
      "reading_level": ["story", "framework"]
    }
  ]
}
```

The site uses this to:
- Filter by tag on any series page
- Show "Related articles" at the bottom of each page
- Power the entrance-by-identity paths (believer/skeptic/researcher/story)
- Let readers click a tag and see every article across all series that covers it

---

## Next step

Tag all 160+ articles. Could be done by:
1. NLP station (auto-classify based on content keywords)
2. Manual pass (David reviews, most accurate)
3. Hybrid (NLP proposes, David approves/corrects)

The JSON file lives at `D:\GitHub\faiththruphysics-site\article-taxonomy.json` and every page reads from it.
