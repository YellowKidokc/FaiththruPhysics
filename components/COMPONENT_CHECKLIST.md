# Site Component Checklist
## Faith Through Physics — Required Components per Page
### Run this checklist on every HTML page before deploy

---

## 1. TOP BAR — MTL Reader Bar
- [ ] `mtl-reader-bar.html` snippet present
- [ ] CSS loaded: `/shared/css/mtl-equation.css`
- [ ] JS loaded: `/shared/js/mtl-equation.js`
- [ ] Four tabs: Easy | Academic | Math Translation Layer | Proof-Claims
- [ ] Content blocks tagged with `data-reader-mode` attributes
- [ ] Default mode = "academic"

## 2. MINI PLAYER — TP Pill Player
- [ ] `tp-pill-player` component present
- [ ] Pill tabs wired to correct audio sources for this article
- [ ] Speed control (0.5x – 2x)
- [ ] Volume slider + mute button
- [ ] Progress bar with seek
- [ ] STICKY BEHAVIOR: docks to right side on scroll-up
- [ ] Audio sources point to valid R2 URLs

## 3. BOTTOM BAR — Subdomain Navigation
- [ ] All site sections listed and linked:
  - [ ] Home (/)
  - [ ] Convergence Series (/convergence-series/)
  - [ ] Convergence Deep (/convergence-deep/)
  - [ ] Blue Series (/blue/)
  - [ ] One-Page Stories (/one-page-stories/)
  - [ ] Master Equation (/master-equation/)
  - [ ] Moral Decline (/moral-decline/)
  - [ ] Genesis to Quantum (/genesis-to-quantum/)
  - [ ] Axiom Layer (/Axiom%20Layer/axioms-layer-0-core.html)
  - [ ] Proof Explorer (/proof-explorer/)
  - [ ] Lean 4 Corpus (/lean4/)
  - [ ] Bidirectional Audit (/the-bidirectional-audit/)
- [ ] Current section visually highlighted
- [ ] Links functional (no 404s)

## 4. SHARED RESOURCES
- [ ] Cinzel / Oswald / JetBrains Mono fonts loaded
- [ ] Near-black aesthetic: --void #050505
- [ ] Gold branding: --gold #d4af37
- [ ] site-shell.js loaded

## 5. PRE-DEPLOY VALIDATION
- [ ] No broken audio URLs
- [ ] No missing CSS/JS references
- [ ] Axiom content verified against canonical source
- [ ] No STT artifacts in body text
- [ ] Page renders correctly at 1920px and 375px
