# ARTICLE VISUAL UPGRADE SPEC
## For AI Page Improvement Passes
### POF 2828 | June 30, 2026 | From David's notes, compiled by Opus

---

## THE GOAL

Every article page should be 2-3x more visually engaging than plain prose.
Not by adding content — by using visual blocks to break up walls of text
and make the structure scannable.

Pages don't all need to look the same, but they all need visual variety.

---

## WHAT DAVID LIKES (observed from existing pages)

1. **Drop caps** — Big first letter on opening paragraphs. Gold or white.
2. **Gold accents** — Gold (#d4af37) left borders, gold section labels,
   gold equation labels. The signature color.
3. **Math in callout boxes** — Equations should never sit inline in prose.
   Always in a styled eq-block with a label and plain-English translation.
4. **Centered section titles** — Major section headings (like "III. The
   Axiom Chain") should be larger, centered, and visually distinct.
5. **Three-card stat blocks** — Numbers/metrics in a row of 3 cards.
6. **Varied block types** — Don't use the same block type twice in a row.
   Alternate between stats, insights, equations, step cards, comparison
   grids.
7. **Bullet points must be styled** — Never plain HTML bullets. Use step
   cards, split icon boxes, or axiom boxes instead.

---

## THE FIVE BLOCK ORIENTATIONS

Use these five patterns. Rotate through them so no article feels repetitive.

### ORIENTATION 1: Triple Stat Row
Three metrics side by side. Use for data points, sigma values, counts.

```html
<div class="block-grid block-grid-3">
  <div class="block-stat">
    <div class="number">6.35σ</div>
    <div class="label">PEAR-LAB Correlation</div>
  </div>
  <div class="block-stat">
    <div class="number">10</div>
    <div class="label">Chi Variables</div>
  </div>
  <div class="block-stat">
    <div class="number">R²=.888</div>
    <div class="label">Lifespan Decoherence</div>
  </div>
</div>
```

### ORIENTATION 2: Step Cards (Numbered Sequence)
Gold left border, large step number, title + body. Use for processes,
derivation steps, argument sequences.

```html
<div style="margin:2.5rem 0;">
  <div style="background:linear-gradient(135deg,rgba(212,175,55,0.05) 0%,rgba(10,10,10,0.98) 100%);border:1px solid #222;border-left:4px solid #d4af37;border-radius:.5rem;padding:2rem 2.5rem;margin-bottom:1.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;color:#d4af37;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.5rem;">Step 1</div>
    <div style="font-family:'Crimson Text',serif;font-size:clamp(1.4rem,3.5vw,2rem);color:#fff;font-weight:600;line-height:1.3;margin-bottom:1rem;">Audit the Borrowed Foundations</div>
    <p style="font-size:1.05rem;color:#bbb;line-height:1.7;">Before testing any claim, identify what both sides must assume before the conversation begins. Most inquiry skips this step.</p>
  </div>
  <div style="background:linear-gradient(135deg,rgba(212,175,55,0.05) 0%,rgba(10,10,10,0.98) 100%);border:1px solid #222;border-left:4px solid #d4af37;border-radius:.5rem;padding:2rem 2.5rem;margin-bottom:1.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;color:#d4af37;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.5rem;">Step 2</div>
    <div style="font-family:'Crimson Text',serif;font-size:clamp(1.4rem,3.5vw,2rem);color:#fff;font-weight:600;line-height:1.3;margin-bottom:1rem;">Map the Structural Stages</div>
    <p style="font-size:1.05rem;color:#bbb;line-height:1.7;">Decompose the physics process into stages. Find the correspondent in the other domain. Not vocabulary — stages.</p>
  </div>
</div>
```

### ORIENTATION 3: Side-by-Side Comparison
Two columns with accent borders. Use for physics↔theology mappings,
before/after, pro/con, domain comparisons.

```html
<div class="block-grid block-grid-2">
  <div class="block-accent" style="border-top:3px solid #4a9eff;">
    <h3 style="color:#4a9eff;"><i class="fas fa-atom"></i> Physics Domain</h3>
    <p>V(r) = −αs/r + k·r describes the strong force potential between quarks. At the ground state, the system exhibits nine measurable properties.</p>
  </div>
  <div class="block-accent" style="border-top:3px solid #d4af37;">
    <h3 style="color:#d4af37;"><i class="fas fa-cross"></i> Theology Domain</h3>
    <p>Galatians 5:22-23 lists nine Fruits of the Spirit. Each maps one-to-one to a ground-state property of the confinement potential.</p>
  </div>
</div>
```

### ORIENTATION 4: Candidate/Option Cards (Stacked, Color-Coded)
Vertical stack with different left-border colors. Use for listing
alternative explanations, competing theories, or multiple claims.

```html
<div style="display:grid;grid-template-columns:1fr;gap:1.25rem;margin:2rem 0;">
  <div style="background:var(--surface3,#1a1a1a);border:1px solid #222;border-left:4px solid #4a9eff;border-radius:.5rem;padding:2rem 2.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:1.4rem;color:#4a9eff;font-weight:600;">Copenhagen Interpretation</div>
    <p style="font-size:1.1rem;color:#cfcfcf;line-height:1.7;margin:0;">Measurement causes collapse. Cannot define measurement without infinite regress.</p>
  </div>
  <div style="background:var(--surface3,#1a1a1a);border:1px solid #222;border-left:4px solid #a855f7;border-radius:.5rem;padding:2rem 2.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:1.4rem;color:#a855f7;font-weight:600;">Many-Worlds</div>
    <p style="font-size:1.1rem;color:#cfcfcf;line-height:1.7;margin:0;">Removes collapse but cannot explain why any observer experiences one outcome.</p>
  </div>
  <div style="background:var(--surface3,#1a1a1a);border:1px solid #222;border-left:4px solid #d4af37;border-radius:.5rem;padding:2rem 2.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:1.4rem;color:#d4af37;font-weight:600;">Triadic Composition (Framework)</div>
    <p style="font-size:1.1rem;color:#cfcfcf;line-height:1.7;margin:0;">Three functions in one operation: generate, structure, actualize. Chain terminates. No regress.</p>
  </div>
</div>
```

### ORIENTATION 5: Insight + Equation Pair
Key observation box followed immediately by the supporting equation.
Use when a conceptual point needs its math shown.

```html
<div class="insight" style="background:rgba(212,175,55,0.04);border-left:4px solid #d4af37;border-radius:0 .5rem .5rem 0;padding:1.5rem 2rem;margin:2rem 0 0.5rem 0;">
  <span class="label" style="font-family:'Oswald',sans-serif;font-size:.75rem;color:#d4af37;text-transform:uppercase;letter-spacing:.1em;">— Key Observation</span>
  <p style="font-size:1.15rem;color:#e0e0e0;line-height:1.7;margin:.5rem 0 0;">Every closed system decays. Set the grace term to zero and the equation reduces to pure exponential decay. The Second Law applied to moral systems.</p>
</div>
<div class="eq-block" style="background:rgba(74,144,255,0.04);border:1px solid #222;border-radius:.5rem;padding:1.5rem 2rem;margin:0 0 2rem 0;text-align:center;">
  <div class="eq-label" style="font-family:'Oswald',sans-serif;font-size:.75rem;color:#4a9eff;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.75rem;">Coherence Equation — Zero Grace Regime</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:1.3rem;color:#fff;">dC/dt = −S · C</div>
  <p style="margin:.75rem 0 0;font-size:.85rem;color:#999;font-style:italic;">Without external input, coherence decays exponentially. The decay is always running.</p>
</div>
```


---

## RULES FOR THE UPGRADE PASS

1. **DO NOT change any content text.** Only add visual structure.
2. **DO NOT remove anything.** Only wrap existing content in blocks.
3. **Every page needs at least 3 visual blocks** spread through it.
4. **Never use the same block type twice in a row.**
5. **All bullet-point lists** must be converted to Step Cards (Orientation 2)
   or Split Icon Boxes.
6. **All equations** must be in eq-block callouts with a label and
   plain-English translation underneath.
7. **Opening paragraphs** get a drop cap (CSS `::first-letter`):
   ```css
   .drop-cap::first-letter {
     font-size: 3.5em;
     float: left;
     line-height: 0.8;
     padding-right: 0.1em;
     color: #d4af37;
     font-family: 'Crimson Text', serif;
   }
   ```
8. **Section headers** for major sections should be centered with
   Oswald font, larger size, gold accent line underneath.
9. **Stat blocks** (Orientation 1) near the top of articles to anchor
   the reader with concrete numbers.
10. **Falsification sections** use the red gradient block (Block 11
    from BLOCKS.md).

---

## PROMPT TEMPLATE FOR OTHER AIs

Copy this prompt and give it to the AI along with the article HTML:

```
You are upgrading the visual presentation of a Theophysics article.

RULES:
- DO NOT change any text content. Only add visual structure.
- DO NOT remove anything.
- Add at least 3 visual blocks spread through the article.
- Never use the same block type consecutively.
- Convert all bullet lists to Step Cards or Split Icon Boxes.
- Put all equations in styled eq-block callouts with labels.
- Add a drop cap to the opening paragraph.
- Use gold (#d4af37) as the primary accent color.
- Background: #0a0a0a. Text: #c9d1d9.
- Headings: Oswald. Body: Inter. Equations: JetBrains Mono.
  Quotes: Crimson Text italic.

BLOCK TYPES AVAILABLE (use HTML from the spec):
1. Triple Stat Row — three metric cards in a row
2. Step Cards — gold-bordered numbered sequence
3. Side-by-Side Comparison — two-column physics↔theology
4. Candidate Cards — stacked options with color-coded borders
5. Insight + Equation Pair — observation box + math callout

COLORS:
- Gold: #d4af37 (primary accent, borders, labels)
- Blue: #4a9eff (physics, info, links)
- Purple: #a855f7 (alternatives, competing theories)
- Red: #ef4444 (falsification, kill conditions)
- Green: #22c55e (confirmed, pass)
- White: #ffffff (emphasis text)
- Gray: #999 (secondary text, translations)

Output the complete upgraded HTML file.
```

---

## TIMING NOTES

David is going to time how long it takes an AI to upgrade one page.
Target: under 5 minutes per page. If it takes longer, simplify the spec.
At 200+ pages, this needs to be fast and repeatable.

---

*POF 2828 | Theophysics Research Initiative*
