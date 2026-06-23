# 06_blocks — Visual Block Components
## Every type of visual break used in articles

## 1. STAT BLOCK (numbers/metrics)
```html
<div class="block-grid block-grid-3">
  <div class="block-stat">
    <div class="number">6.35σ</div>
    <div class="label">PEAR-LAB Correlation</div>
  </div>
  <div class="block-stat">
    <div class="number">10</div>
    <div class="label">Super-Factors</div>
  </div>
  <div class="block-stat">
    <div class="number">R²=.888</div>
    <div class="label">Lifespan Decoherence</div>
  </div>
</div>
```

## 2. INSIGHT BOX (key observation)
```html
<div class="insight">
  <span class="label">— Key Observation</span>
  <p>{{INSIGHT_TEXT}}</p>
</div>
```

## 3. AXIOM BOX (framework claim)
```html
<div class="axiom-box">
  {{AXIOM_TEXT}}
</div>
```

## 4. LAW BOX (law reference)
```html
<div class="law-box">
  <div class="law-label">Framework Principle</div>
  <p>{{LAW_TEXT}}</p>
</div>
```

## 5. EQUATION BLOCK (MathJax)
```html
<div class="eq-block">
  <div class="eq-label">{{EQUATION_NAME}}</div>
  $${{LATEX_EQUATION}}$$
  <p style="margin:.75rem 0 0;font-size:.8rem;color:var(--text-secondary);font-style:italic;">
    {{PLAIN_ENGLISH_TRANSLATION}}
  </p>
</div>
```

## 6. STEP CARDS (numbered sequence)
```html
<div style="margin:2.5rem 0;">
  <div style="background:linear-gradient(135deg,rgba(212,175,55,0.05) 0%,rgba(10,10,10,0.98) 100%);border:1px solid #222;border-left:4px solid #d4af37;border-radius:.5rem;padding:2rem 2.5rem;margin-bottom:1.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;color:#d4af37;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.5rem;">Step 1</div>
    <div style="font-family:'Crimson Text',serif;font-size:clamp(1.4rem,3.5vw,2rem);color:#fff;font-weight:600;line-height:1.3;margin-bottom:1rem;">{{STEP_TITLE}}</div>
    <p style="font-size:1.05rem;color:#bbb;line-height:1.7;">{{STEP_TEXT}}</p>
  </div>
  <!-- Repeat for Step 2, 3, etc. -->
</div>
```

## 7. COMPARISON GRID (side by side)
```html
<div class="block-grid block-grid-2">
  <div class="block-accent">
    <h3><i class="fas fa-{{ICON_LEFT}}"></i> {{LEFT_TITLE}}</h3>
    <p>{{LEFT_TEXT}}</p>
  </div>
  <div class="block-accent">
    <h3><i class="fas fa-{{ICON_RIGHT}}"></i> {{RIGHT_TITLE}}</h3>
    <p>{{RIGHT_TEXT}}</p>
  </div>
</div>
```

## 8. CANDIDATE/OPTION CARDS (multiple explanations)
```html
<div style="display:grid;grid-template-columns:1fr;gap:1.25rem;margin:2rem 0;">
  <div style="background:var(--surface3);border:1px solid var(--border);border-left:4px solid #4a9eff;border-radius:.5rem;padding:2rem 2.5rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:1.4rem;color:#4a9eff;font-weight:600;">{{OPTION_TITLE}}</div>
    <p style="font-size:1.1rem;color:#cfcfcf;line-height:1.7;margin:0;">{{OPTION_TEXT}}</p>
  </div>
  <!-- Use #4a9eff (blue), #a855f7 (purple), #d4af37 (gold, for preferred) -->
</div>
```

## 9. PULLQUOTE (large serif quote)
```html
<blockquote>
  <p>"{{QUOTE_TEXT}}"</p>
</blockquote>
```

## 10. DISCLAIMER BOX
```html
<div class="disclaimer-box">
  <div class="disclaimer-label"><i class="fas fa-cross"></i> The Disclaimer</div>
  <p>We are finite minds reasoning about infinite God. Every model is projection of 
  higher-dimensional reality onto lower-dimensional surface we can comprehend. We do not 
  claim to have captured God in equations. We claim that when we look at His creation 
  honestly — with the tools of physics and the revelation of Scripture — the same structure 
  appears in both. Where our model limits what God can be, the limitation is ours, not His. 
  We offer this work as worship, not as containment.</p>
</div>
```

## 11. FALSIFICATION CRITERIA (red gradient)
```html
<div style="background:linear-gradient(180deg,rgba(201,64,64,0.08) 0%,rgba(201,64,64,0.02) 60%,transparent 100%);border-top:3px solid #c94040;border-radius:.75rem;padding:2.5rem 2rem;margin:2.5rem 0;">
  <h2 style="color:#ef4444;margin-top:0;">Falsification Criteria</h2>
  <p style="color:#999;margin-bottom:2rem;">The framework survives or falls on testable claims:</p>
  
  <div style="background:rgba(201,64,64,0.06);border:1px solid rgba(201,64,64,0.25);border-left:4px solid #ef4444;border-radius:.5rem;padding:1.75rem 2rem;margin-bottom:1.25rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:clamp(1.4rem,3.5vw,2rem);font-weight:700;color:#ef4444;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.5rem;">Claim 1</div>
    <p style="font-size:1.05rem;color:#ccc;line-height:1.7;margin:0;">{{CLAIM_TEXT}}</p>
  </div>
  <!-- Each subsequent claim reduces opacity: 0.85, 0.65, 0.45 on the red -->
</div>
```

## 12. SPLIT ICON BOX (icon + text)
```html
<div class="block-split">
  <div class="icon"><i class="fas fa-{{ICON}}"></i></div>
  <div>
    <div class="text-title">{{TITLE}}</div>
    <div class="text-desc">{{DESCRIPTION}}</div>
  </div>
</div>
```

## 13. IMAGE EMBED (with caption)
```html
<div style="margin:2rem 0;border-radius:.5rem;overflow:hidden;border:1px solid #222;">
  <img src="{{IMAGE_URL}}" alt="{{ALT_TEXT}}" style="width:100%;display:block;">
  <div style="padding:.75rem 1rem;font-size:.8rem;color:var(--text-secondary);background:var(--surface3);">
    {{CAPTION_TEXT}}
  </div>
</div>
```

## 14. DATA TABLE
```html
<table class="data-table">
  <thead>
    <tr>
      <th>{{COL1}}</th>
      <th>{{COL2}}</th>
      <th>{{COL3}}</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong style="color:#fff;">{{CELL}}</strong></td>
      <td>{{CELL}}</td>
      <td>{{CELL}}</td>
    </tr>
  </tbody>
</table>
```

## 15. TANGENT CARD (expandable)
```html
<div class="tangent-card">
  <div class="tangent-label"><i class="fas fa-code-branch"></i> Tangent {{NUM}}</div>
  <h3>{{TANGENT_TITLE}}</h3>
  <button class="tangent-toggle" onclick="toggleTangent(this)">
    <i class="fas fa-chevron-right"></i> Expand Tangent Article
  </button>
  <div class="tangent-body">
    <!-- Full tangent article content goes here -->
  </div>
</div>
```

## 16. SELF-AUDIT SECTION
```html
<h2>The Audit</h2>
<p><em>What we got right, what we're less sure about, and where we got carried away.</em></p>

<h3>What's load-bearing — we'd bet on this</h3>
<p>{{CONFIRMED_CLAIMS}}</p>

<h3>What's suggestive but needs more work</h3>
<p>{{SUGGESTIVE_CLAIMS}}</p>

<h3>Where we got carried away</h3>
<p>{{OVERSTATED_CLAIMS}}</p>

<p><em>The article above is what we believe. This audit is what we know we haven't proven yet. Both matter.</em></p>
```
