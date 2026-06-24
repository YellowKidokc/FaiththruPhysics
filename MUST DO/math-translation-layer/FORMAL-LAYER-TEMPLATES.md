# Formal Layer Templates

These are the new templates for the formal layer redesign. They are separate from the old MTL callout files.

## Files

- `formal-layer-topbar-template.html` - article top layer template. Domain composition is on the left. What / How / Why jurisdiction is on the right. Domain clicks navigate away; jurisdiction clicks highlight claims on the article.
- `domain-composition-page-template.html` - destination page template for domain clicks. It reads `?domain=history`, `?domain=family`, etc. and shows where domain evidence, claim rows, and citation rows should render.
- `formal-layer-topbar-mockup.html` - first visual mockup kept for comparison.

## Wiring Rule

Structured data stays source of truth.

- `site_claims.db` drives claim jurisdiction, confidence, overreach, and POS mismatch review.
- `citations.db` drives citation bubbles and source cards.
- HTML renders from those databases and should be rebuildable from them.

## Intended Behavior

- Domain strip: opens a domain detail page.
- What / How / Why strip: stays in the article and highlights matching sentences.
- Sentence click: opens the explanation directly under the sentence.
- API depth pass: only low confidence, high overreach, or POS mismatch claims.
