# SITE STRUCTURE SPEC — faiththruphysics.com
## June 22, 2026 · Opus · For Kimi and Codex

---

## THREE-TIER NAVIGATION

### Tier 1 — Homepage (index.html)
- Clickable Master Equation explorer (DONE — Codex built it)
- Master Story section with audio per act (REPLACE current act list with master_story_index.html content)
- Series cards: each series gets a card with title, count, color, one-line description
- Click "Browse all N →" → Tier 2 landing page
- Click individual card → Tier 2 landing page for that series
- Reading Ladder, Browse by Theme sections stay as-is

### Tier 2 — Series Landing Page (series-folder/index.html)
- Template: use moral-decline/index.html as reference
- Structure:
  - Top bar with reading path tabs (Story/Plain/Test/Proof)
  - Domain classification bar with percentage badges
  - Series title + subtitle
  - **VIDEO EMBED** — NotebookLM deep dive or best available video
  - Chapter list: number, title, one-line summary (from NLP `one_sentence_hook`)
  - Pill player for audio
- This is where the visitor watches. TWO clicks from home.
- Every series needs one. Currently only MDA has it properly.

### Tier 3 — Article Page (series-folder/article.html)
- Full article with:
  - Top bar + reading path tabs
  - Audio player (pill player with Deep Dive/Debate/Critique/TTS/Web options)
  - MTL equation callouts (clickable, word-form, per equation-presentation-templates.html)
  - Glossary underlines for terms above 8th grade
  - Domain classification bar
  - Prev/Next navigation within series
  - Bottom bar with subdomain links
- THREE clicks from home. But video was at Tier 2, so they're already committed.

---

## SERIES THAT NEED TIER 2 LANDING PAGES

| Series | Folder | Articles | Has Landing? | Priority |
|---|---|---|---|---|
| Moral Decline of America | moral-decline/ | 61 | YES (reference) | Done |
| One Pagers — God Stories | one-page-stories/ | 23 | Bare index | HIGH |
| Genesis to Quantum | genesis-to-quantum/ | 26 | Bare index | HIGH |
| Convergence Deep | convergence-deep/ | 6 | None | MEDIUM |
| Consciousness | consciousness/ | 10 | None | MEDIUM |
| Three Truths | three-truths/ | 3 | None | MEDIUM |
| Three Gates | three-gates/ | 1 | None | LOW |
| Master Equation / 10 Laws | master-equation/ | 10 | None | MEDIUM |
| Formal Papers | formal-papers/ | 10 | None | LOW |
| Proof Architecture | proof-architecture/ | 13 | None | LOW |
| Logos Papers | needs folder | 14 | None | HIGH |
| Be Glad You're a Loser | needs folder | ? | None | LOW |
| Family Tests | needs folder | ? | None | LOW |

---

## MASTER STORY INTEGRATION

Replace the current "Master Narrative" section on the homepage with:
1. The full master_story_index.html narrative text
2. Audio player per act (NotebookLM chapter podcasts)
3. Bold phrases are clickable links to articles (already wired in the master story)
4. Each act can expand/collapse or link to a dedicated act page

File: D:\GitHub\faiththruphysics-site\master_story_index.html

---

## CONTENT PIPELINE (feeds into Tier 2 and 3)

1. NLP Summary Generator runs on each article → outputs JSON per article
2. JSON fields feed:
   - Tier 2 chapter list (title + one_sentence_hook)
   - Tier 2 domain classification bar (domain_classification percentages)
   - Tier 3 meta tags (title, description, og:tags)
   - Tier 3 glossary underlines (terms_above_8th_grade)
   - Tier 3 executive summary tab
3. Prompt: D:\GitHub\faiththruphysics-site-data\_summaries\_prompts\nlp-summary-generator.prompt.md
4. Output: D:\GitHub\faiththruphysics-site-data\_summaries\by-source\{slug}.summary.json

---

## COMPONENT CHECKLIST PER PAGE

Every HTML page on the site must have:
- [ ] site-shell.js loaded
- [ ] Top bar with reading path tabs
- [ ] Bottom bar with subdomain links
- [ ] Pill player (if audio exists)
- [ ] MTL equation callouts (if equations present)
- [ ] Meta description from NLP summary
- [ ] Canonical URL
- [ ] og:title, og:description, og:image

---

## USER PREFERENCES (cookie/localStorage)

Three toggles, persistent across site:
1. **Definitions** — on/off (underlined glossary terms)
2. **Math Translation Layer** — on/off (word-form equations)
3. **Default reading level** — Story/Plain/Test/Proof

---

## BUILD ORDER

1. Run NLP summaries on corpus (DeepSeek batch)
2. Build series landing pages (Tier 2) using MDA as template
3. Wire master story into homepage Master Narrative section
4. Inject top/bottom bars across all pages
5. Add meta tags from NLP JSONs
6. Fix remaining broken links (Codex did homepage, check inner pages)
7. Push to Cloudflare

---

*Site Structure Spec v1.0 · POF 2828 · June 22, 2026*
*Reference implementations: moral-decline/index.html (Tier 2), equation-presentation-templates.html (MTL)*