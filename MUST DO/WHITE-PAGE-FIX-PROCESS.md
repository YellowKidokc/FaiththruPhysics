# White-Page Fix Process

When an HTML page renders with a white background instead of the site dark theme, the fix is to inject a dark reset as the very first style in the `<head>`.

## Quick fix (one file)

Open the HTML file and insert this line immediately after `<head>`:

```html
<head>
<style>html,body{background:#050505;color:#e0e0e0;}</style>
```

This prevents the white flash while the rest of the page CSS loads.

## Bulk fix (whole folder)

From the repo root, run this Python script against any folder. It adds the dark reset to every `.html` file that does not already have one.

```python
from pathlib import Path
import re

folder = Path('MUST DO')  # change to target folder
dark_reset = '<style>html,body{background:#050505;color:#e0e0e0;}</style>\n'

for f in sorted(folder.glob('*.html')):
    text = f.read_text(encoding='utf-8', errors='ignore')
    if re.search(r'background\s*:\s*#0[05]0505', text, re.I):
        print('skip (already dark):', f.name)
        continue
    new_text = re.sub(r'(<head>\s*)', r'\1' + dark_reset, text, count=1, flags=re.I)
    if new_text == text:
        print('skip (no <head>):', f.name)
        continue
    f.write_text(new_text, encoding='utf-8')
    print('fixed:', f.name)
```

## Verify

After editing, search the file for:

```
<style>html,body{background:#050505;color:#e0e0e0;}</style>
```

It should appear right after `<head>` and before any other stylesheets or meta tags.

## Commit and deploy

```bash
git add "MUST DO"
git commit -m "fix: dark reset for white HTML pages"
git push origin Other
cd <html-branch-checkout>
git fetch origin
git merge origin/Other -m "Merge Other into HTML: dark resets"
git push origin HTML
```

## Why this works

The browser paints the viewport as soon as it can. If `<body>` has no background color, it defaults to white. By setting `html,body{background:#050505;}` at the very top of `<head>`, the first paint is already dark, even before fonts, CSS files, or MathJax load.

## When it is not enough

If an inner container (e.g. `.page`, `.content`, `main`) has an explicit white background, the dark reset alone will not fix it. In that case, also add CSS variables and override the container:

```html
<style>
html,body{background:#050505;color:#e0e0e0;}
:root{
  --bg:#050505;--surface:#0a0a0a;--surface2:#111;
  --border:#222;--text:#e5e3df;--text-dim:#9a9a9a;
  --gold:#d4af37;--blue:#5b9bd5;--teal:#3bb39a;
}
.page{background:var(--bg);color:var(--text);min-height:100vh;}
</style>
```

Use the minimal reset first. Only add the expanded block if the page still shows white areas after the reset.
