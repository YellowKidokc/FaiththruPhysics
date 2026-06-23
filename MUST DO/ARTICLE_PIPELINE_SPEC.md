# Article Pipeline — Standard Input/Output Specification
## Faith Through Physics · POF 2828 · June 21, 2026

---

## The Rule

**One folder per article. Standard structure. Any AI can produce it.**

The website is built from article packages. Each package is a folder containing
markdown content, metadata JSON, audio files, and media. A build script reads
the folder and outputs a complete HTML page with all site components wired.

No AI needs to know CSS. No AI needs to know the template. No AI needs to know
the deployment system. They produce the folder. The pipeline does the rest.

---

## Folder Structure

```
ARTICLE_PACKAGES/
└── article-slug/
    ├── meta.json              ← drives everything
    ├── story.md               ← Story Path (narrative, human, image-rich)
    ├── plain.md               ← Plain Path (clear explanation, no jargon)
    ├── test.md                ← Test Path (claims, objections, evidence, kill conditions)
    ├── proof.md               ← Proof Path (Lean refs, equations, datasets, rigor)
    ├── audio/
    │   ├── podcast.mp3        ← Deep Dive (NotebookLM or manual)
    │   ├── read-aloud.mp3     ← Read Aloud (Edge TTS from plain.md)
    │   ├── debate.mp3         ← Debate (NotebookLM or manual)
    │   └── tts-source.txt     ← Clean text for browser TTS engine
    └── media/
        ├── hero.jpg           ← Hero image (1200x630 recommended)
        └── fig-01.png         ← Figures referenced in content
```

---

## meta.json Specification

```json
{
  "slug": "the-question",
  "title": "The Question",
  "subtitle": "When Two Worlds Define the Same Word Differently",
  "author": "David Lowe",
  "date": "2026-06-21",

  "series": "cross-domain",
  "series_title": "Cross-Domain Analysis",
  "series_order": 1,
  "prev": null,
  "next": "the-floor",

  "status": "draft",

  "classification": [
    { "tag": "theology",     "pct": 28, "color": "#c87050" },
    { "tag": "psychology",   "pct": 22, "color": "#8fe6b0" },
    { "tag": "cross-domain", "pct": 18, "color": "#e2725b" },
    { "tag": "ethics",       "pct": 15, "color": "#ff7d90" },
    { "tag": "evidence",     "pct": 10, "color": "#2dd4bf" },
    { "tag": "story",        "pct": 7,  "color": "#f5d0a9" }
  ],

  "audio": {
    "podcast":    null,
    "read_aloud": null,
    "debate":     null,
    "critique":   null
  },

  "options": {
    "mtl_equations": false,
    "rigor_card": true,
    "glossary_links": true,
    "show_classification": true,
    "show_audio_dock": true,
    "reading_levels": ["story", "plain", "test", "proof"]
  },

  "formal_refs": {
    "axioms": ["A1.1", "A2.2"],
    "theorems": [],
    "isomorphisms": [],
    "kill_conditions": [
      "Find a stable society that functions without shared definitions"
    ]
  }
}
```

### Field Reference

| Field | Required | What it does |
|-------|----------|-------------|
| slug | yes | URL path and folder name |
| title | yes | Page title, h1 |
| subtitle | no | Italic subtitle under title |
| series | no | Which series this belongs to |
| series_order | no | Position in series (drives prev/next) |
| prev / next | no | Override auto-navigation |
| status | yes | draft / review / published |
| classification | yes | Array of {tag, pct, color} — drives the colored bar |
| audio | no | R2 URLs for each audio channel (null = unavailable) |
| options | no | Feature flags for this page |
| formal_refs | no | Links to axiom/theorem/isomorphism registry |

---

## Content Files (Markdown)

Each .md file is one reading level. All four are optional — if a level doesn't
exist, its tab is dimmed or hidden.

### story.md — Story Path
- Narrative, human-first
- Opens with a person, a scene, a question
- No equations unless they're explained in words
- Images welcome
- Target: anyone with curiosity

### plain.md — Plain Path
- Clear explanation for serious readers
- Technical concepts explained without jargon
- Can reference equations with word-equations underneath
- Target: educated non-specialist

### test.md — Test Path
- Claims stated explicitly
- Objections steelmanned
- Evidence cited
- Kill conditions listed
- Target: skeptic, reviewer, critic

### proof.md — Proof Path
- Lean 4 theorem references
- Full equations with LaTeX
- Datasets and statistical results
- Formal axiom chain references
- Target: mathematician, physicist, formal reviewer

---

## Pipeline Flow

```
┌──────────────────────┐
│  1. CREATION         │  Any AI writes 4 markdown files + meta.json
│     (AI or human)    │  Drops into ARTICLE_PACKAGES/slug/
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  2. NLP PIPELINE     │  classify_html.py → updates classification in meta.json
│     (automated)      │  claim_extractor → claims.json
│                      │  axiom_grounding → updates formal_refs
│                      │  mtl_detector → flags equations
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  3. AUDIO PIPELINE   │  Edge TTS: plain.md → read-aloud.mp3
│     (automated)      │  Extract: plain.md → tts-source.txt
│                      │  NotebookLM: manual → podcast.mp3
│                      │  Upload: rclone → R2 bucket
│                      │  Update: meta.json audio URLs
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  4. BUILD            │  MUST DO/build_article.py reads the folder
│     (one command)    │  Converts MD → HTML sections
│                      │  Injects into the shell template
│                      │  Wires classification bar, audio dock
│                      │  Copies local audio/media assets
│                      │  Output: MUST DO/_built/<slug>/index.html
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  5. DEPLOY           │  git push → Cloudflare Pages
│     (one command)    │  Audio → rclone to R2
└──────────────────────┘
```

---

## For AI Collaborators

**To create a new article:**
1. Create folder: `ARTICLE_PACKAGES/your-slug/`
2. Write `meta.json` with at minimum: slug, title, status, classification
3. Write at least `story.md` and `plain.md`
4. Drop any audio into `audio/` subfolder
5. Drop any images into `media/` subfolder
6. Run: `python "MUST DO/build_article.py" your-slug`
7. Preview the output HTML
8. Deploy when ready

**Classification colors (from ARTICLE_TAXONOMY.md):**
| Tag | Color |
|-----|-------|
| physics | #4a9eff |
| theology | #c87050 |
| math | #a855f7 |
| info-theory | #3bb39a |
| consciousness | #f59e0b |
| trinity | #d4af37 |
| grace | #22c55e |
| entropy | #ef4444 |
| justice | #e879a0 |
| free-will | #8b5cf6 |
| adversary | #6b7280 |
| genesis | #92400e |
| ten-laws | #d4af37 |
| master-eq | #f0c659 |
| method | #9a7c3a |
| evidence | #2dd4bf |
| society | #64748b |
| cross-domain | #e2725b |
| story | #f5d0a9 |
| ai | #60a5fa |

---

*This is the single source of truth for article creation.*
*All AI collaborators follow this spec.*
*POF 2828 · June 21, 2026*
