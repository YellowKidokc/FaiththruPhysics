# TOP BAR

**Skill:** [SKILL.md](SKILL.md) (`top-bar`) — covers two page-shell jobs.

## Part A — White Site Restore

Detect, fix, verify, and archive HTML pages that render **white** because dark-theme CSS (`:root` + `body{background}`) was stripped.

| Script | Purpose |
|--------|---------|
| [scripts/white_scan.py](scripts/white_scan.py) | Find pages using `var(--bg)` without `:root` |
| [scripts/white_fix.py](scripts/white_fix.py) | Inject `<style id="theme-restore-dark">` before `</head>` |

```bash
# Scan a folder
python "MUST DO/TOP BAR/scripts/white_scan.py" "D:\GitHub\faiththruphysics-site\Templates David"

# Fix pages (dry-run first)
python "MUST DO/TOP BAR/scripts/white_fix.py" --dry-run path\to\page.html
python "MUST DO/TOP BAR/scripts/white_fix.py" path\to\page.html
```

Fixed batches go to `D:\GitHub\faiththruphysics-site-data\_site_archives\{name} GOOD.zip`.

## Part B — Universal Top Bar + Bottom Dock Migration

Strip legacy `.tp-top` / `.tp-class` shell and inject `/site-shell/frame.js`. Driven by `topbar.py` (needs `beautifulsoup4 lxml`).

```bash
python D:\GitHub\Python-WEB\topbar\topbar.py audit
python D:\GitHub\Python-WEB\topbar\topbar.py migrate --path consciousness --apply
```

Modules: `audit`, `fix-h1`, `migrate`. Default is dry-run; pass `--apply` to write. See SKILL.md Part B for full usage.

## Legacy files in this folder

- `verification-bar.html`, `merge_verification.py` — older verification-bar prototype
- Canonical verification bar docs: [../PAGE-SHELL-GOLD-STANDARD/03-verified-bar/README.md](../PAGE-SHELL-GOLD-STANDARD/03-verified-bar/README.md)

## Related

- Full page shell builder: [../PAGE-SHELL-GOLD-STANDARD/skills/page-shell-builder.md](../PAGE-SHELL-GOLD-STANDARD/skills/page-shell-builder.md)
