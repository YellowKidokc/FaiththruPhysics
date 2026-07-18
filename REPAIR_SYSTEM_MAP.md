# Repair System Map — read this before touching site structure

**Ruling by David, July 18 2026.** This file is the pointer, not the toolbox.
Future sessions (Codex / Kimmy / Claude / anyone): orient here first.

## The two-repo rule

| What | Where | Rule |
|------|-------|------|
| **Live website** | `D:\GitHub\faiththruphysics-site-live` → GitHub `YellowKidokc/FaiththruPhysics`, branch `HTML` | The ONLY folder website work happens in. Everything in it deploys publicly via Cloudflare Pages. |
| **Repair/toolbox system** | `D:\GitHub\Python-WEB` → GitHub `YellowKidokc/Python-WEB` (private) | The factory: labeler REPAIR, locked shells, migrator, ledgers, experiments. **Never copy the whole toolbox into the live repo.** |

Deprecated drifted copies — do **not** work in them:
`D:\GitHub\faiththruphysics-site` (old) and `D:\faiththruphysics-site` (stale).

## Key paths in the toolbox

- Registered migrator:
  `D:\GitHub\Python-WEB\labeler REPAIR\08_repair_scripts\python\migrate_canonical_shell.py`
- Locked canonical shells + hash contract:
  `D:\GitHub\Python-WEB\topbar\canonical-page-shell\` (`shell-top.html`,
  `shell-bottom.html`, `verify_shell_contract.py`, `verify_migrated_page.py`,
  manifest)
- Repair ledger:
  `D:\GitHub\Python-WEB\labeler REPAIR\repair_ledger.jsonl`

Run repairs through the registered labeler REPAIR path (dry-run → exact YES →
apply → ledger). The bare `.py` files bypass the gates — don't.

## Promotion rule

Only small, blessed, site-supporting scripts get copied into this repo's
`scripts/` — individually, reviewed, like `scripts/repair_reading_levels_controls.py`.
The toolbox stays in Python-WEB.

## The law and the live coordination record

- Architecture law: `DESIGN_canonical-shell-migration.md`
  (PR: `YellowKidokc/DONT-TOUCH-BOOT-UP#2`) — locked shells are binary
  artifacts behind a SHA-256 gate; pages assemble at build time; after
  migration, content fragments + `page-data.json` are the source of truth and
  deployed HTML is a build artifact nobody hand-edits.
- Crew coordination, job specs, and current state: the AI Comms Hub at
  `https://comms.dlowehomelab.com` — see `prompts/the-workflow`,
  `prompts/shell-v2-pills`, `prompts/page-data-contract`, and
  `workflow/site-systems-map`.
