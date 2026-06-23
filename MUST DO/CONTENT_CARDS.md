# 07_content-cards — Structured Content Sections
## Specific named content patterns used across articles

## SELF-AUDIT CARD (the honesty section)
Used in: GTQ-01, 04, 05, 08 — needs porting to 02, 03, 07, 09, 10
```html
<div class="self-audit">
  <div class="self-audit__title">The Audit</div>
  <div class="self-audit__subtitle">What we got right, what we're less sure about, and where we got carried away.</div>
  
  <div class="self-audit__section self-audit__section--proven">
    <div class="self-audit__label">What's load-bearing — we'd bet on this</div>
    <div class="self-audit__body">
      <p><strong>{{CLAIM_1_TITLE}}</strong> {{CLAIM_1_TEXT}}</p>
      <p><strong>{{CLAIM_2_TITLE}}</strong> {{CLAIM_2_TEXT}}</p>
    </div>
  </div>
  
  <div class="self-audit__section">
    <div class="self-audit__label">What's suggestive but needs more work</div>
    <div class="self-audit__body">
      <p><strong>{{SUGGESTIVE_1_TITLE}}</strong> {{SUGGESTIVE_1_TEXT}}</p>
    </div>
  </div>
  
  <div class="self-audit__section">
    <div class="self-audit__label">Where we got carried away</div>
    <div class="self-audit__body">
      <p><strong>{{OVERSTATED_1_TITLE}}</strong> {{OVERSTATED_1_TEXT}}</p>
    </div>
  </div>
  
  <div class="self-audit__sign">
    <p><em>The article above is what we believe. This audit is what we know we haven't proven yet. Both matter.</em></p>
  </div>
</div>
```

## MEDIA CARD (video/audio embed)
```html
<div class="media-card">
  <span class="media-label"><i class="fas fa-film"></i> {{MEDIA_TITLE}}</span>
  <div style="position:relative;width:100%;padding-top:56.25%;background:#000;border-radius:.4rem;overflow:hidden;">
    <video controls preload="metadata" style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:contain;">
      <source src="{{VIDEO_URL}}" type="video/mp4">
    </video>
  </div>
  <p class="media-desc">{{MEDIA_DESCRIPTION}}</p>
</div>
```

## SHARE BAR
```html
<div class="share-section">
  <div class="share-label">Share this article</div>
  <div class="share-bar">
    <button class="share-btn x" onclick="shareX()"><i class="fab fa-x-twitter"></i></button>
    <button class="share-btn facebook" onclick="shareFB()"><i class="fab fa-facebook-f"></i></button>
    <button class="share-btn linkedin" onclick="shareLI()"><i class="fab fa-linkedin-in"></i></button>
    <button class="share-btn reddit" onclick="shareReddit()"><i class="fab fa-reddit-alien"></i></button>
    <button class="share-btn email" onclick="shareEmail()"><i class="fas fa-envelope"></i></button>
    <button class="share-btn copy" onclick="copyLink()"><i class="fas fa-link"></i></button>
  </div>
</div>
```

## REACTION BAR
```html
<div class="reaction-bar">
  <button class="reaction-btn" onclick="react(this,'mind')">🤯 <span class="reaction-label">Mind Blown</span> <span class="count">0</span></button>
  <button class="reaction-btn" onclick="react(this,'think')">🤔 <span class="reaction-label">Make Me Think</span> <span class="count">0</span></button>
  <button class="reaction-btn" onclick="react(this,'pray')">🙏 <span class="reaction-label">Amen</span> <span class="count">0</span></button>
</div>
```

## BORN RULE TRINITY VISUAL (GTQ-01 specific, reusable for Trinity articles)
Three-column grid: Father (gold) | Son (white) | Spirit (teal)
Source: GTQ-01 lines ~1250-1290, the oversized Born Rule section
This is one of the most impactful visuals — use in any article discussing the Trinity mechanism.
