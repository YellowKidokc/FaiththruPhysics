"""Shared markdown → HTML utilities for faiththruphysics site articles."""

from __future__ import annotations

import re

YAML_FENCE_RE = re.compile(r"^```ya?ml\s*\n.*?\n```\s*", re.DOTALL | re.IGNORECASE)
REF_SECTION_HEADINGS = frozenset({"references", "bibliography", "works cited"})


def strip_frontmatter(md: str) -> str:
    return YAML_FENCE_RE.sub("", md.strip(), count=1)


def simple_md_to_html(md: str) -> str:
    """Minimal fallback when the markdown package is unavailable."""
    lines = md.splitlines()
    out: list[str] = []
    in_blockquote = False
    for line in lines:
        raw = line.rstrip()
        if not raw:
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            continue
        if raw.startswith("### "):
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append(f"<h3>{raw[4:]}</h3>")
        elif raw.startswith("## "):
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append(f"<h2>{raw[3:]}</h2>")
        elif raw.startswith("# "):
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append(f"<h1>{raw[2:]}</h1>")
        elif raw.startswith("> "):
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            out.append(f"<p>{raw[2:]}</p>")
        else:
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append(f"<p>{raw}</p>")
    if in_blockquote:
        out.append("</blockquote>")
    return "\n".join(out)


def wrap_article_sections(html: str) -> str:
    """Wrap top-level h2 blocks in <section> for article styling."""
    parts = re.split(r"(<h2[^>]*>.*?</h2>)", html, flags=re.DOTALL | re.IGNORECASE)
    if len(parts) <= 1:
        return html
    out: list[str] = []
    i = 0
    while i < len(parts):
        chunk = parts[i]
        if re.match(r"<h2", chunk, re.IGNORECASE):
            section_bits = [chunk]
            i += 1
            while i < len(parts) and not re.match(r"<h2", parts[i], re.IGNORECASE):
                section_bits.append(parts[i])
                i += 1
            heading = re.sub(r"<[^>]+>", "", chunk).strip().lower()
            cls = ' class="tp-refs"' if heading in REF_SECTION_HEADINGS else ""
            out.append(f"<section{cls}>\n" + "".join(section_bits) + "\n</section>")
        else:
            if chunk.strip():
                out.append(chunk)
            i += 1
    return "\n".join(out)


def md_to_html(md: str) -> str:
    md = strip_frontmatter(md)
    try:
        import markdown  # type: ignore

        html = markdown.markdown(
            md,
            extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        )
    except Exception:
        html = simple_md_to_html(md)
    return wrap_article_sections(html)
