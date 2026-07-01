---
name: top-bar
description: >-
  Two faiththruphysics page-shell workflows. (1) White-site restore: detect,
  fix, verify, and archive HTML pages that render white due to missing
  dark-theme CSS (:root variables and body background). (2) Universal top bar
  + bottom dock migration: strip legacy .tp-top/.tp-class shell and inject
  /site-shell/frame.js via topbar.py. Use when the user reports white pages,
  broken templates, missing dark theme, var(--bg) not defined, or asks to
  apply/migrate/audit the top bar and bottom dock, fix merged h1, or
  fix/restore/archive site batches.
---

# Top Bar

Two related but distinct page-shell jobs. Pick by symptom:

| Symptom | Job | Section |
|---------|-----|---------|
| Page is white / black text / no accents | **White-site restore** (theme CSS) | Part A |
| Missing/duplicate top bar or bottom dock; legacy `.tp-top` | **Shell migration** (`topbar.py`) | Part B |
| Title + subtitle merged into one `<h1>` | **fix-h1** (`topbar.py`) | Part B |

They fix different defects. A page can need both. When both apply, **restore the dark theme first**, then run the shell migration.

---

# Part A — White Site Restore

Fix HTML pages that **look white** because theme CSS variables are used but never defined.

## Root cause (confirmed by runtime)

| Symptom | Cause |
|---------|-------|
| White/transparent background | `body` has no `background` rule, or `var(--bg)` is undefined |
| Black text on white | Browser default `color: rgb(0,0,0)` |
| Gold/surface accents missing | `--gold`, `--surface2`, etc. undefined in `:root` |

**Common trigger:** shell migration or partial inject stripped the top of `<style>` (the `:root` block and `body{background:var(--bg)}` rule) while leaving `var(--*)` references in the rest of the page.

`/assets/site-shell.css` only defines `--shell-*` vars — it does **not** supply `--bg`, `--gold`, `--text`.

## Pre-fix runtime check (required)

Before editing, confirm the page is actually white in the browser:

```javascript
// CDP Runtime.evaluate — expect pre-fix: bg "rgba(0,0,0,0)", col "rgb(0,0,0)", bgVar ""
(() => {
  const cs = getComputedStyle(document.body);
  return {
    bg: cs.backgroundColor,
    col: cs.color,
    bgVar: getComputedStyle(document.documentElement).getPropertyValue('--bg').trim()
  };
})();
```

**Pass after fix:** `bg: "rgb(5, 5, 5)"`, `col: "rgb(229, 227, 223)"`, `bgVar: "#050505"`.

Use cache-busting (`?cb=1`) or disable cache when re-testing — stale HTML will show pre-fix values.

## Fast workflow

```
Task Progress:
- [ ] 1. Scan folder or site for candidates
- [ ] 2. Classify each hit (fixable / stub / already dark via linked CSS)
- [ ] 3. Fix (inject theme OR full restore from backup)
- [ ] 4. Runtime verify computed bg/color on each fixed page
- [ ] 5. Archive fixed batch to _site_archives
- [ ] 6. Re-scan — folder should flag 0 (except known stubs)
```

### 1. Scan

```bash
python "MUST DO/TOP BAR/scripts/white_scan.py" "D:\GitHub\faiththruphysics-site"
python "MUST DO/TOP BAR/scripts/white_scan.py" "D:\GitHub\faiththruphysics-site\Templates David"
```

Flag reasons:
- `uses theme var, no :root` — **fixable** (inject theme block)
- `no <style> or stylesheet` — check file size; may be a **stub** (skip)
- `explicit white background` — inspect; may be print CSS only

### 2. Classify before fixing

| Type | Action |
|------|--------|
| Uses `var(--bg)` etc., no `:root` | Inject `theme-restore-dark` (see below) |
| Corrupt prefix before `<!DOCTYPE` | Strip junk, then inject or restore |
| Missing entire stylesheet | Full restore from `_inject_backups` or `_inject_preview` |
| Linked theme CSS works at runtime (e.g. `iso-theme.css`) | **No fix** — scanner false positive |
| File is <20 lines, no real content | **Stub** — skip (e.g. `article-template-v2.html`) |

Backup locations:
- `D:\GitHub\faiththruphysics-site-data\_inject_backups\{folder}\`
- `D:\GitHub\faiththruphysics-site-data\_inject_preview\{folder}\`

Gold-standard theme source: `index.html` or `genesis-to-quantum/gtq-01-measurement-collapsed-reality.html` (`:root` + `body` rules).

### 3. Fix — inject theme (default)

```bash
# Preview
python "MUST DO/TOP BAR/scripts/white_fix.py" --dry-run path/to/page.html

# Apply
python "MUST DO/TOP BAR/scripts/white_fix.py" path/to/page.html path/to/other.html
```

Injects `<style id="theme-restore-dark">` immediately before `</head>`:

```css
:root{
  --bg:#050505; --surface:#0a0a0a; --surface2:#111; --surface3:#1a1a1a;
  --border:#222; --border-2:#2a2a2a; --border-hi:#3a3a3a; --border-hover:#3a3a3a;
  --text:#e5e3df; --text-dim:#9a9a9a; --text-muted:#5a5a5a;
  --text-primary:#e5e3df; --text-secondary:#9a9a9a;
  --gold:#d4af37; --gold-dim:rgba(212,175,55,.1); --gold-glow:rgba(212,175,55,.3);
  --highlight:#d4af37; --accent-gold:#d4af37;
  --red:#c94040; --red-dim:rgba(201,64,64,.1);
  --teal:#3bb39a; --teal-dim:rgba(59,179,154,.1);
  --blue:#5b9bd5; --blue-dim:rgba(91,155,213,.1);
  --purple:#a78bfa; --purple-dim:rgba(167,139,250,.1); --green:#7fc77f;
  --serif:'Crimson Text',Georgia,serif; --mono:'JetBrains Mono',ui-monospace,monospace;
  --display:'Oswald','Inter',sans-serif; --sans:'Inter',system-ui,sans-serif;
  --max:1180px; --header-h:48px;
}
html{background:var(--bg)}
body{background:var(--bg);color:var(--text);font-family:var(--sans)}
```

Skips files that already have `theme-restore-dark` or full `:root` + `body{background:var(--bg)}`.

### 3b. Fix — full restore (when inject is not enough)

Use when:
- Visible JS blob appears above `<!DOCTYPE html>`
- Page is dark but layout/CSS is broken (missing hundreds of rules)
- Backup has complete document

Restore from first `<!DOCTYPE html>` in backup file. Preserve encoding (utf-8, fallback latin-1).

### 4. Runtime verify

After fix, reload with cache disabled and run the CDP probe above on **at least one page per batch**.

Optional screenshot for visual proof (dark bg, gold accents, light text).

### 5. Archive

Zip fixed folders/files to:

```
D:\GitHub\faiththruphysics-site-data\_site_archives\{Series Name} GOOD.zip
```

PowerShell pattern:

```powershell
$arc = "D:\GitHub\faiththruphysics-site-data\_site_archives"
New-Item -ItemType Directory -Force -Path $arc | Out-Null
Compress-Archive -Path "D:\GitHub\faiththruphysics-site\{folder}\*" `
  -DestinationPath "$arc\{folder} GOOD.zip" -Force
```

### 6. Re-scan

```bash
python "MUST DO/TOP BAR/scripts/white_scan.py" "D:\GitHub\faiththruphysics-site\{folder}"
```

Expect **0 flagged** except known stubs.

## Batch sizing

Work in increasing batches per user preference:
1. One site → verify → archive
2. Two sites → verify → archive
3. Three to four → verify → archive
4. Five to six when confidence is high

Do not bulk-fix the entire site without runtime proof on each batch.

## What NOT to do (Part A)

- Do not regenerate article body text from markdown
- Do not fix scanner false positives (pages dark at runtime via linked CSS)
- Do not overwrite stubs expecting a full article layout
- Do not claim fixed without computed-style proof (`rgb(5,5,5)` bg)

---

# Part B — Universal Top Bar + Bottom Dock Migration

Apply the consistent top bar and bottom audio dock to every page by injecting
`/site-shell/frame.js` and stripping legacy embedded shell. Driven by one tool:

```
D:\GitHub\Python-WEB\topbar\topbar.py
```

Requires `beautifulsoup4` + `lxml` (`pip install beautifulsoup4 lxml`).

## Modules

| Module | Does |
|--------|------|
| `audit` | Scan and report shell state for every HTML file (no writes) |
| `fix-h1` | Fix merged `<h1>` (title + subtitle concatenated) and empty subtitle |
| `migrate` | Strip legacy shell elements, inject `/site-shell/frame.js` exactly once |

Legacy elements stripped by `migrate`: `.tp-top`, `.tp-class`, `.tp-player-block`,
`.tp-bignav`, `.tp-header-lip`, `.tp-verify-top`, `dock-mini`.

## Safety (built into topbar.py)

- **Default mode is DRY-RUN.** Pass `--apply` to write.
- Per-file `.bak` backups on first apply (`--no-backup` to skip).
- Encoding preserved: UTF-8 first, latin-1 fallback.
- `migrate` skips already-framed pages; **blocks if the `<h1>` is mangled** (run `fix-h1` first).

## Commands

```bash
# Audit the whole site (read-only)
python D:\GitHub\Python-WEB\topbar\topbar.py audit

# Dry-run full pipeline on one folder
python D:\GitHub\Python-WEB\topbar\topbar.py migrate --path consciousness

# Apply audit -> fix-h1 -> migrate on one folder
python D:\GitHub\Python-WEB\topbar\topbar.py audit fix-h1 migrate --path revolution-of-truth --apply

# Apply only the migrator site-wide
python D:\GitHub\Python-WEB\topbar\topbar.py migrate --apply

# Skip a module you don't need
python D:\GitHub\Python-WEB\topbar\topbar.py audit migrate --skip fix-h1 --path blue --apply
```

Paths: default root `D:/GitHub/faiththruphysics-site`; override with `--root`,
target a subfolder with `--path` (relative to root).

## Migration verification (per folder)

Required pass criteria after a folder migration:

- `DOUBLE_SHELL = 0` (top bar appears exactly once)
- `old element present, no frame.js = 0`
- `framed pages with mangled h1 = 0`

Then confirm on at least one live page per folder: top bar once, bottom dock
once, no white background (run the Part A CDP probe), `h1` and subtitle separate.

## Batch order (proven rollout)

1. one-page-stories
2. consciousness, revolution-of-truth, three-gates
3. convergence-series, cross-domain
4. remaining mixed-legacy folders

## What NOT to do (Part B)

- Do not migrate already-correct framed pages (the migrator skips them — keep it that way)
- Do not create double shells; if `frame.js` is already present, do not re-add
- Do not run `migrate` on a page with a mangled `<h1>` before `fix-h1`
- Do not touch admin/auth/security pages or unrelated content
- Do not mix dead-CSS cleanup into the shell pass

---

## Related tools

| Tool | Purpose |
|------|---------|
| `MUST DO/TOP BAR/scripts/white_scan.py` | Find likely-white pages (Part A) |
| `MUST DO/TOP BAR/scripts/white_fix.py` | Inject theme-restore-dark (Part A) |
| `D:\GitHub\Python-WEB\topbar\topbar.py` | Shell audit / fix-h1 / migrate (Part B) |
| `MUST DO/PAGE-SHELL-GOLD-STANDARD/skills/page-shell-builder.md` | Full page shell + reading levels |
| `faiththruphysics-site-data/_inject_backups/` | Full HTML restores |

## Proven fixes (reference)

| Page | Fix applied |
|------|-------------|
| `Axiom Layer/7Q Axioms.html` | Full restore from `_inject_preview` |
| `isomorphism/Isomorphic.html` | No fix — `iso-theme.css` already dark |
| `forge-proofs/01 unavoidable-conclusion-complete.html` | Strip corrupt JS prefix + restore from `_inject_backups` |
| `index _site.html` | Inject `theme-restore-dark` |
| `genesis-to-quantum/intro/gtq-01-...-N.html` | Inject `theme-restore-dark` |
| `Templates David/` (4 templates + index) | Inject `theme-restore-dark` |
| `Templates David/article-template-v2.html` | Skipped — 6-line stub |
