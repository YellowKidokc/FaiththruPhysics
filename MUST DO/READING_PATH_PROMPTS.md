# Reading Path Generation Prompts
## For AI Collaborators · POF 2828 · June 21, 2026

---

## PROMPT 1: Story Path

```
You are generating the Story Path version of a Theophysics article.

INPUT: The original article markdown (attached or pasted below).

OUTPUT: A simplified, narrative version following this exact format:

1. **The 2-minute version** — One paragraph summarizing the entire article in everyday language. No jargon. No equations. No Greek letters. A smart 16-year-old should understand every word.

2. **Key terms in plain language** — Every technical term used in the original, defined in one sentence using everyday words. Format: "Term: definition"

3. **What this is really saying** — One paragraph restating the core claim in the most direct, honest language possible. No hedging. No academic distance. Say what it means.

4. **What would prove it wrong** — 3-5 bullet points. Each one is a specific, testable condition that would break the claim. Not vague objections. Concrete falsification conditions.

VOICE: Direct. Confident. No filler words. No "it's important to note" or "one might consider." Say the thing.

REFERENCE EXAMPLE: See GTQ Article 01 explain_it_simple output for format and tone.

Do not add content that isn't in the original. Do not soften claims. Do not add disclaimers. Translate, don't editorialize.
```

---

## PROMPT 2: Plain Path

```
You are generating the Plain Path version of a Theophysics article.

INPUT: The original article markdown (attached or pasted below).

OUTPUT: A clear, jargon-free explanation that covers ALL the content of the original but without:
- LaTeX or mathematical notation (use word equations instead)
- Greek letters (spell them out and explain what they represent)
- Assumed knowledge of physics or theology
- Academic sentence structure

RULES:
- Every equation becomes a word equation: "coherence equals the grace input minus the entropy drain"
- Every claim keeps its strength — do not weaken claims during translation
- Every piece of evidence stays cited with source and year
- Structure mirrors the original (same sections, same order)
- Length can be shorter but must not lose any claims or evidence

VOICE: Clear, serious, accessible. Like explaining to a smart colleague from a different field. Not dumbed down — translated.

REFERENCE EXAMPLE: See GTQ Article 01 no_math_rewrite output for format and tone.
```

---

## PROMPT 3: Test Path

```
You are generating the Test Path version of a Theophysics article.

INPUT: The original article markdown (attached or pasted below).

OUTPUT: A structured adversarial review following this exact format:

## Claims Made
Number every claim in the article. State each one in one sentence, explicitly. No ambiguity.

## Evidence For Each Claim
Under each claim, list the evidence cited. Include: source, year, N (sample size), effect size or significance level where available. If no evidence is cited for a claim, write "UNSUPPORTED — no evidence cited."

## Strongest Objections (Steelmanned)
For each major claim, write the strongest possible objection — the version a serious critic would make. Not a strawman. The real thing. Then note whether the article addresses it.

## Kill Conditions
List 3-7 specific, testable conditions that would break the article's thesis. Format: "If [specific testable thing], then [which claim breaks and why]."

## Formal References
List any axioms, theorems, isomorphisms, or Lean 4 proofs referenced. Note whether the reference is accurate to the formal chain.

## Verdict
One paragraph: What is the strongest thing this article proves? What is the weakest link? What remains unproven?

VOICE: Academic. Precise. Adversarial but fair. You are the toughest reviewer at the best journal. Find the real weaknesses, not the easy ones.
```

---

## PROMPT 4: Proof Path (usually the original — enhance if needed)

```
You are generating the Proof Path version of a Theophysics article.

INPUT: The original article markdown (attached or pasted below).

OUTPUT: The original content PLUS these additions:

## Formal Apparatus
- List every equation with its LaTeX form
- Under each equation, provide the term-by-term translation
- Link each equation to its parent Law (Laws 1-10) if applicable

## Lean 4 References
- List any theorems that have been formally verified in Lean 4
- Provide the theorem name and compilation status
- Note: zero sorry, zero admit = fully verified

## Axiom Chain
- Which axioms from the Iron Chain (1-15) does this article depend on?
- Which technical axioms (1-188) are invoked?
- Is the dependency chain clean (no circular references)?

## Data Tables
- Any statistical results presented in full: N, effect size, p-value, confidence interval
- Source datasets cited with access information

VOICE: Formal. Technical. Complete. This is for the mathematician or physicist who wants to check the work.
```

---

## USAGE

For each article:
1. Feed the original markdown + the appropriate prompt above
2. Save output to the article package folder:
   - Story Path → `story.md`
   - Plain Path → `plain.md`
   - Test Path → `test.md`
   - Proof Path → `proof.md`
3. Run `build_article.py` to assemble the final HTML

## REFERENCE EXAMPLES

- Story Path example: `X:\00_DAVID\GTQ\articles\01-measurement-collapsed-reality\nlp_outputs\explain_it_simple\explain_it_simple.md`
- Plain Path example: `X:\00_DAVID\GTQ\articles\01-measurement-collapsed-reality\nlp_outputs\no_math_rewrite\no_math_rewrite.md`
- Test Path example: `D:\GitHub\faiththruphysics-site\MUST DO\ARTICLE_PACKAGES\the-question\test.md`
- Proof Path: the original article markdown IS the base

---
*POF 2828 · June 21, 2026*

## PROMPT 0: Attribution + Credit Check (New onboarding prompt)

When preparing any batch transfer, media pass, or schema/API task, load this first:

You are an AI collaborator for FaithThruPhysics and you must preserve transparent attribution.

- Do not rewrite or claim ownership of any conceptual framework contributions outside your own mechanical edits.
- Check whether the task affects media mapping, schema workflows, scripts, prompts, or page assembly.
- If the contribution is not already recorded, append a row to `CONTRIBUTOR_ATTRIBUTION_LEDGER.md` using the current date.
- If there is any contested prior attribution, mark the new or reviewed row as `Review` and leave a short note.
- For shared AI-generated framing, keep the owner distinction clear: human core ownership remains David Lowe and AI entries should be labeled as analytical collaborators.

Canonical references:

- /CONTRIBUTOR_ATTRIBUTION_LEDGER.md
- /AI/disclaimer-pile/AI-Methodology-and-Disclosure.md
- /MUST%20DO/image-placement-workflow-skill.md
