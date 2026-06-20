# KIMI DEPLOYMENT HANDOFF
**Written by: Claude Opus 4.6 | June 17, 2026**
**For: Kimi | Purpose: Content deployment to faiththruphysics.com**

---

## MISSION

Deploy production-ready HTML articles from the Master HTML archive to the live site repo. Get as much quality content up as possible before the John Templeton Foundation OFI deadline (August 14, 2026). When Templeton reviewers Google David Lowe, they need to find real published work backing up the claims in the application.

**Philosophy: Deploy forward, fix retroactively.** Don't hold content back for perfection. Get it up. If something is wrong, we'll take it down or fix it later. The mistake before was taking things down — don't repeat that.

---

## PATHS

### Source (content to deploy)

**NAS (primary source — production-ready content):**
```
\\dlowenas\h_hp\Desktop\Folders\Master HTML\K-Production-Ready\
  ├── 02-genesis-to-quantum\    ← GTQ series (~35 HTML files, flagship content)
  └── 03-moral-decline\         ← MDA series (~40 HTML files)
```

**NAS (secondary — standalone articles, may need review):**
```
\\dlowenas\h_hp\Desktop\Folders\Master HTML\Standalone-Articles\
  ├── the-same-equation.html
  ├── math-is-moral.html
  ├── i-didnt-write-the-math.html
  ├── gold-standard-test-battery.html
  └── ... (10 total)
```

**NAS (reference — project docs):**
```
\\dlowenas\h_hp\Desktop\Folders\Master HTML\_KIMI-READ-FIRST\
  ├── README.md
  ├── PROJECT-STATE.md
  ├── FILE-NAMING-SYSTEM.md
  ├── AUDIT-REPORT.md
  └── QA-HANDOFF-2026-05-13.md
```

### Destination (live site repo)
```
D:\GitHub\faiththruphysics-site\
  ├── index.html                 ← Homepage (already exists, needs nav links updated)
  ├── genesis-to-quantum\        ← CREATE THIS — deploy GTQ series here
  ├── moral-decline\             ← Already exists (MDA partially deployed)
  ├── one-page-stories\          ← CREATE THIS — standalone articles go here
  ├── site-shell.js              ← Vanilla JS injector (replaces React/Vite)
  ├── glossary-linker.js         ← Glossary overlay
  └── shared\                    ← Shared CSS/JS assets
```

---

## WORKFLOW (repeat for each article)

### Step 1: CHECK the source HTML
- Open the file from K-Production-Ready
- Verify it has: proper HTML structure, content renders, no broken placeholder text
- Check that internal links use relative paths (../index.html, not absolute file:// paths)
- If it looks structurally sound → proceed. Don't nitpick styling.

### Step 2: COPY to site repo
- GTQ files → `D:\GitHub\faiththruphysics-site\genesis-to-quantum\`
- MDA files → `D:\GitHub\faiththruphysics-site\moral-decline\`
- Standalone articles → `D:\GitHub\faiththruphysics-site\one-page-stories\`
- Create directories if they don't exist

### Step 3: ADD the MTL wrapper (Math Translation Layer)
The site uses an "easy academic math translation layer" overlay that makes equations accessible to non-math readers. Check if the article already includes MTL markup. If not, the overlay should be wired via the site-shell.js injector or inline. Reference existing deployed articles in `moral-decline\` for the pattern.

Key assets that should be linked:
- `/site-shell.js` — the vanilla JS shell injector
- `/glossary-linker.js` — auto-links glossary terms
- Check `/shared/` for any common CSS

### Step 4: UPDATE homepage navigation
- The homepage (`index.html`) has a "Reading Ladder" section and series catalog
- When adding a new series (like GTQ), make sure it's linked from the homepage
- The homepage already references `genesis-to-quantum/index.html` in multiple places — the directory just needs to exist with content

### Step 5: PUSH to Cloudflare
- The site deploys via Cloudflare Pages from the GitHub repo
- `git add . && git commit -m "Deploy [series/article name]" && git push`
- Site is at faiththruphysics.com

### Step 6: STOP AND TELL DAVID
- After each batch push, stop and tell David what went up
- David will verify in browser before you continue
- Don't push 30 articles without checking — do batches of 3-5

---

## PRIORITY ORDER

1. **GTQ Series** (genesis-to-quantum) — This is the flagship. The homepage already links to it but the directory doesn't exist yet. Deploy the index.html and at least the first 5 articles. This is the #1 thing Templeton reviewers need to see.

2. **Standalone Articles** — "The Same Equation", "Math is Moral", "I Didn't Write the Math", "Gold Standard Test Battery" — these are self-contained, impressive, and fast to deploy.

3. **MDA Series** (moral-decline) — Partially deployed already. Check what's there, fill gaps.

---

## KNOWN ISSUES

- **Bash doesn't work in your environment.** Use PowerShell, cmd, or Python for file operations. The Desktop Commander MCP or Windows-MCP PowerShell tool can create directories and copy files.
- **UNC paths (\\dlowenas\...) sometimes return 0 bytes** through certain tools. If a copy produces a 0-byte file, try a different method (cmd `copy`, PowerShell `Copy-Item`, or read+write).
- **Images may be missing.** GTQ references images at `/genesis-to-quantum/images/`. If the images aren't in the source, deploy the HTML anyway — broken meta images won't stop readers.
- **Audio URLs point to R2 buckets.** These should work as-is if the R2 bucket (theophysics-media) is still serving.

---

## WHAT NOT TO DO

- Don't rewrite content. Deploy what exists.
- Don't take anything down unless David specifically asks.
- Don't restructure the file naming. The K-Production-Ready files use a naming system documented in `_KIMI-READ-FIRST\FILE-NAMING-SYSTEM.md`.
- Don't wait for everything to be perfect. Get it up.

---

## TEMPLETON CONTEXT

David is applying to the John Templeton Foundation Open Funding Inquiry. Deadline: August 14, 2026. The application itself is nearly done. But when reviewers Google "David Lowe Theophysics" or visit faiththruphysics.com, they need to find a body of published work — not an empty site. Every article deployed is evidence that the research program is real and producing output.

The site also needs a curated review page (something like `/review` or `/portfolio`) that David will share as a direct link in the application. This is a separate task — focus on getting content deployed first, and David or another AI partner will build the review landing page.

---

*End of handoff. Questions → post to comms or ask David directly.*
