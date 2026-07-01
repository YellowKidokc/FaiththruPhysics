# Prompt: Image Placement Feedback Loop (Assistant + Human Review)

You are helping place article images in the `revolution-of-truth` series pages.

Use this loop:

1. Ask for the user’s preference first:
   - Which pages to do next (1, then 2–3).
   - Which image to place.
   - Where it should go (before intro / after a specific section / near a table).
2. Propose the exact markdown block with absolute image path (e.g., `/media/media/<filename>.webp`).
3. Confirm no other conflicting section placement exists.
4. Apply to the markdown source file(s) only for the target reading variants.
5. Run one-page dry-run with report before apply.
6. Report changed summary and next placement option.

Decision guardrails:

- Prefer not adding more than 1–2 images per page while user is in pilot mode.
- Keep style explicit via `style="display:block; width:100%; max-width:980px; margin:...`.
- Validate that image paths are valid under `/media/media/`.
- Keep script changes limited to the existing page-shell builder unless a repeated gap remains.
