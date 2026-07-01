# One-Page-Stories Visual Anchor Handoff (Mechanical Injection)

You are continuing the visual-anchor rollout for **one-page stories**.

Primary rule:
- One visual anchor per ~6 prose paragraphs.
- Never place anchor at article start.
- One anchor slot every interval; no two consecutive anchors with the same shape.

Workflow:

1. Load target files from `D:/GitHub/faiththruphysics-site-data/academic/one-page-stories`.
2. Run:
   - `python D:/GitHub/Python-WEB/workflows/visual-anchor-injector/inject_visual_anchors.py --series academic\\one-page-stories --shape-pool 1,4 --interval 6 --max-files 1 --report D:\\GitHub\\faiththruphysics-site\\reports\\ops-visual-anchor.json`
3. Review output and confirm slot count and shapes are appropriate.
4. Apply only once you want edits:
   - add `--apply`
5. If rerunning, use `--force` only if replacement is intended.

No layout invention:
- Keep block labels/claims/number/question from existing prose.
- Fill shape slots from article paragraph content only.
- Do not invent new formats in-place.

Canonical references:
- `/Python-WEB/workflows/visual-anchor-injector/inject_visual_anchors.py`
- `/Python-WEB/workflows/visual-anchor-injector/README.md`
- `/faiththruphysics-site-data/CONTRIBUTOR_ATTRIBUTION_LEDGER.md`
