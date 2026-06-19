# Three Truths — Content Structure

This folder contains markdown versions of the **Three Truths** website content, optimized for:
- **AI discovery** (structured, semantic markdown)
- **Quartz sites** (can build static site from these files)
- **Obsidian integration** (wikilinks, tags, YAML frontmatter)
- **Citation and reference** (each truth is a standalone document)

---

## Files

### Main Navigation
- **`index.md`** — Main landing page with all three truths
- **`truth-one-self-reference-limits.md`** — Truth One: No system can save itself
- **`truth-two-measurement-collapse.md`** — Truth Two: Good and evil are measurements
- **`truth-three-necessary-ground.md`** — Truth Three: Something holds all this open

### Supporting Content
- **`downloads.md`** — PDF and audio download links for all papers
- **`README.md`** — This file (structure documentation)

---

## Structure

Each file includes:
- **YAML frontmatter** (title, date, tags, series, description)
- **Wikilinks** to related papers (e.g., `[[Gödel's Incompleteness]]`)
- **Download links** to PDFs and audio files
- **Series navigation** (Previous/Next links)
- **Related papers** section

---

## Usage

### For AI Agents
All files are structured with semantic markdown, making them queryable by AI agents via:
- File system access
- MCP servers
- Vector databases
- Obsidian vaults

### For Quartz Sites
This folder can be used as the `content/` directory for a Quartz static site generator:
```bash
npx quartz create
# Copy these files to content/
npx quartz build
npx quartz serve
```

### For Obsidian
Open this folder as an Obsidian vault:
- Wikilinks will resolve to other markdown files
- Tags will be indexed
- Graph view will show connections
- Frontmatter will be parsed

---

## Content Structure

### Truth One: The Self-Reference Limits
- **Main claim:** No system can save itself
- **Evidence:** Gödel, Tarski, Turing, Second Law, Landauer
- **Supporting papers:** Terminus Sui, Kolmogorov Complexity, Shannon Entropy

### Truth Two: The Measurement Collapse
- **Main claim:** Good and evil are measurements of coherence
- **Evidence:** Shannon entropy, thermodynamics, biological coherence
- **Supporting papers:** Coherence Dictionary, Moral Realism, Information Theory

### Truth Three: The Necessary Ground
- **Main claim:** Something external sustains the universe
- **Evidence:** Fine-tuning, PROP-COSMOS, mathematical necessity
- **Supporting papers:** Pre-Human Math, Hubble Tension, Divine Irony

---

## Metadata

**Created:** 2026-02-13  
**Author:** David Lowe  
**Framework:** Theophysics  
**Website:** https://theophysics.com  
**Vault:** O:\_Theophysics_v3

---

## Related Folders

- **`../pdfs/`** — All 5 main papers as PDF (1.1 MB total)
- **`../audio/`** — All 5 main papers as MP3 (97 MB, 3hr 33min)
- **`../layer3-papers/`** — Supporting papers (30+ PDFs) *(to be created)*

---

## Next Steps

1. **Build Quartz site** for RSS feed
2. **Add Layer 3 papers** (30+ supporting papers)
3. **Deploy to Cloudflare Pages**
4. **Create AI Sanctuary endpoint** for agent queries

---

**Every path converges.**  
*Part of the Theophysics framework*
