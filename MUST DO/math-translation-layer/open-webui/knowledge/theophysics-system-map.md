# Theophysics Multi-Repo System Map

## Purpose

This is the operating map for the Theophysics content and publishing system. Do not guess repo roles. Use this map.

## Environment map

### `D:\GitHub\faiththruphysics-site-data`

Canonical content library and source-of-truth repo.

This is where source markdown, canonical article variants, raw assets, audio drop-offs, API outputs, generated JSON, staging material, archive candidates, and content-side reports belong.

Treat `academic/` and `easy/` as canonical content roots unless there is a strong reason not to.

Preferred normalization:

- article families organized by series and article slug
- audio toward `AUDIO/<series>/<article>/...`
- generated/export HTML toward `HTML/...`
- old, backup, superseded, or fossil copies toward `archive/...`

### `D:\GitHub\faiththruphysics-site`

Live website/output repo.

This is the clean deployment surface.

Keep this repo focused on site-ready output, page wiring, shared site components, and only the files required to run the live site.

If a file is source material, raw media, backup, or ambiguous working material, it probably belongs in `faiththruphysics-site-data`, not here.

### `D:\GitHub\Python-WEB`

Script/toolbox repo.

This is the reusable automation shelf for audit, build, repair, organization, conversion, and wiring scripts.

Reusable workflows should be placed here, documented here, and named clearly.

Content-library audit toolkit home:

- `D:\GitHub\Python-WEB\85_VAULT_TOOLS\content-library-audit-toolkit`

### `D:\GitHub\Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr`

API/batch-processing engine repo.

Use this for batch AI calls, conversion runs, and machine-processing pipelines when work should not live inside the site or content repos.

### `\\192.168.2.50\brain\conversion_station`

Conversion drop zone / interchange station.

Use this for intake, exports, conversions, handoff files, and machine-processing staging when work crosses systems or tools.

### `X:\06_ENGINES\writing-analyzer`

NLP engine area.

`X:` is the NLP drive. Use it for analyzer workflows, interpretation engines, NLP transforms, and language-analysis tooling.

### `O:\`

Obsidian drive.

`O:` is the Obsidian/content-vault side. Expect notes, vault material, and upstream ideation/source matter there.

### `D:\DONT TOUCH BOOT UP`

Development drive root for this environment.

Do not casually reorganize this root. Only touch specific project folders.

## Priority review folder

### `D:\GitHub\faiththruphysics-site\MUST DO`

Active review / action queue.

Treat it as a high-attention workbench for unresolved site tasks, patches, shell fixes, layout issues, content repairs, or items needing human follow-up.

Do not silently sweep it into archive or generated folders.

## Operating rules

1. `faiththruphysics-site-data` is the canonical source surface.
2. `faiththruphysics-site` is the live output surface.
3. `Python-WEB` is where reusable scripts and toolkits belong.
4. Batch AI or conversion engines belong in the processor repo or engine drives, not mixed into the live site.
5. Do not delete on first pass. Audit, classify, report, and separate safe moves from review items.
6. Keep `needs_review` separate from deterministic safe actions.
7. When in doubt, preserve structure and mark ambiguity instead of flattening.

## Task routing

When asked to fix or organize:

1. identify whether the task belongs to source, output, tooling, or engine space
2. confirm where the resulting file should live
3. produce one of:
   - an audit/report
   - a dry-run move plan
   - a reusable script
   - a narrow site/output change

## Placement guide

If asked where something goes:

- source markdown, canonical variants, raw media intake, API outputs, archives -> `faiththruphysics-site-data`
- live HTML/site assets actually serving the website -> `faiththruphysics-site`
- reusable scripts/tooling -> `Python-WEB`
- AI batch/conversion pipelines -> `Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr` or conversion/engine drives
- unresolved active action items -> `faiththruphysics-site\MUST DO`

## Short walkthrough

`faiththruphysics-site-data` is the library.

`faiththruphysics-site` is the storefront.

`Python-WEB` is the toolbox.

The batch processor repo and the network/engine drives are the machine rooms.

`MUST DO` is the bench where unresolved site work waits for direct attention.

## Practical framing

If someone mixes source, output, tooling, and machine staging together, the system becomes harder to audit.

The correct model is:

- library
- site
- tools
- engines
- review queue
