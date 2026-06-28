#!/usr/bin/env python3
"""
Build components/universal-shell-v5.html from faiththruphysics-template-5.html
by injecting MathJax, MTL reader bar, audio player block, and MTL client script.

Usage:
  python scripts/build_universal_shell.py
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path(r"D:\GitHub\Python-WEB\faiththruphysics-template-5.html")
OUT = ROOT / "components" / "universal-shell-v5.html"

# Markers for where to insert dynamic content in v5 template.
PLACEHOLDERS = {
    "title": "{{PAGE_TITLE}}",
    "canonical": "{{PAGE_CANONICAL}}",
    "article_h1": "{{ARTICLE_H1}}",
    "article_subtitle": "{{ARTICLE_SUBTITLE}}",
    "article_byline": "{{ARTICLE_BYLINE}}",
    "article_body": "{{ARTICLE_BODY}}",
    "audio_player": "{{AUDIO_PLAYER_BLOCK}}",
    "prev_title": "{{PREV_TITLE}}",
    "prev_href": "{{PREV_HREF}}",
    "next_title": "{{NEXT_TITLE}}",
    "next_href": "{{NEXT_HREF}}",
    "series_home_href": "{{SERIES_HOME_HREF}}",
    "series_home_label": "{{SERIES_HOME_LABEL}}",
    "audit_right": "{{AUDIT_RIGHT}}",
    "audit_over": "{{AUDIT_OVER}}",
    "audit_wrong": "{{AUDIT_WRONG}}",
}


def main():
    if not TEMPLATE.exists():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    html = TEMPLATE.read_text(encoding="utf-8")

    # Inject MathJax config before </head>
    mathjax_block = """
<!-- MathJax + MTL support -->
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'], ['\\(','\\)']], displayMath: [['$$','$$'], ['\\[','\\]']] },
  svg: { fontCache: 'global' },
  startup: {
    pageReady: function() {
      return MathJax.startup.defaultPageReady().then(function() {
        if (MathJax.startup.document && MathJax.startup.document.math) {
          MathJax.startup.document.math.forEach(function(item) {
            if (item.typesetRoot) {
              item.typesetRoot.dataset.latex = item.math;
              item.typesetRoot.dataset.display = item.display ? 'block' : 'inline';
            }
          });
        }
      });
    }
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<link rel="stylesheet" href="/shared/css/mtl-worker-client.css"/>
"""
    html = html.replace("</head>", mathjax_block + "\n</head>")

    # Inject MTL reader bar after the top header (before classification bar)
    mtl_bar = """
<!-- ═══════ MTL READER BAR ═══════ -->
<div class="mtl-reader-bar" id="mtlReaderBar" aria-label="Math reading level">
  <a href="/equation/" class="mtl-reader-label" title="Open the Master Equation explorer">Math Layer</a>
  <div class="mtl-reader-tabs" role="tablist" aria-label="Reading levels">
    <button class="mtl-reader-tab active" type="button" data-reader-mode="easy" aria-selected="true">Easy Reader</button>
    <button class="mtl-reader-tab" type="button" data-reader-mode="standard" aria-selected="false">Standard Reader</button>
    <button class="mtl-reader-tab" type="button" data-reader-mode="academic" aria-selected="false">Academic Reader</button>
    <button class="mtl-reader-tab" type="button" data-reader-mode="proof" aria-selected="false">Proof</button>
  </div>
</div>
"""
    # Insert before classification bar
    html = html.replace('<!-- ═══════ CLASSIFICATION BAR ═══════ -->', mtl_bar + '\n<!-- ═══════ CLASSIFICATION BAR ═══════ -->')

    # Replace demo title
    html = html.replace("<title>Faith thru Physics — Unified Template</title>", f"<title>{PLACEHOLDERS['title']}</title>")

    # Replace demo article content with placeholders
    article_pattern = re.compile(
        r'(<article class="tp-article">)\s*<h1>The Measurement That Collapsed Reality</h1>\s*<p class="subtitle">.*?</p>\s*<div class="byline">.*?</div>(.*?)(</article>)',
        re.DOTALL
    )
    replacement = (
        r'\1\n'
        f'  <h1>{PLACEHOLDERS["article_h1"]}</h1>\n'
        f'  <p class="subtitle">{PLACEHOLDERS["article_subtitle"]}</p>\n'
        f'  <div class="byline">{PLACEHOLDERS["article_byline"]}</div>\n'
        f'  {PLACEHOLDERS["audio_player"]}\n'
        f'  {PLACEHOLDERS["article_body"]}\n'
        r'\3'
    )
    html = article_pattern.sub(replacement, html)

    # Replace prev/next demo titles/hrefs
    html = html.replace('href="#" class="tp-bignav-prev"', f'href="{PLACEHOLDERS["prev_href"]}" class="tp-bignav-prev"')
    html = html.replace('<span class="tp-bignav-title">The First Quantum State</span>', f'<span class="tp-bignav-title">{PLACEHOLDERS["prev_title"]}</span>')
    html = html.replace('href="#" class="tp-bignav-next"', f'href="{PLACEHOLDERS["next_href"]}" class="tp-bignav-next"')
    html = html.replace('<span class="tp-bignav-title">Free Will — Two Frames</span>', f'<span class="tp-bignav-title">{PLACEHOLDERS["next_title"]}</span>')
    html = html.replace('href="/genesis-to-quantum/" class="tp-bignav-series">GTQ Series Home</a>', f'href="{PLACEHOLDERS["series_home_href"]}" class="tp-bignav-series">{PLACEHOLDERS["series_home_label"]}</a>')

    # Replace audit demo content
    html = html.replace(
        '<li>Load-bearing claims, clear definitions, and the parts that clearly survived the check.</li>\n          <li>The Master Equation derivation holds at 6.35σ.</li>\n          <li>The isomorphism between Yukawa potential and agapē is formally complete.</li>',
        PLACEHOLDERS['audit_right']
    )
    html = html.replace(
        '<li>Strong direction, but the language ran ahead of the evidence or the proof.</li>\n          <li>The consciousness bridge is suggestive but not yet rigorously closed.</li>\n          <li>We used "proof" where "high-confidence inference" would be more honest.</li>',
        PLACEHOLDERS['audit_over']
    )
    html = html.replace(
        '<li>Claims that need correction, tightening, or weaker formulation.</li>\n          <li>The initial entropy calculation was off by a factor of 2 — corrected in v4.</li>\n          <li>We attributed a source incorrectly; the citation has been fixed.</li>',
        PLACEHOLDERS['audit_wrong']
    )

    # Inject MTL client script before </body>
    client_script = """
<!-- MTL worker client -->
<script src="/shared/js/mtl-worker-client.js" defer></script>
"""
    html = html.replace("</body>", client_script + "\n</body>")

    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
