#!/usr/bin/env python3
"""
top_bar_bottom_bar.py â€” apply the unified page shell (top bar + verified band + page foot).

Reads _TEMPLATE.html, injects per-page metadata + three reading-level bodies:
  High School  â†’ faiththruphysics-site-data/{series}/highschool/{slug}.canonical.md
                 fallback: faiththruphysics-site-data/easy/{series}/{slug}.canonical.md
  College        â†’ existing HTML body, else faiththruphysics-site-data/{series}/{slug}.canonical.md,
                 fallback: APIs/input/{series}/{slug}.canonical.md
  PhD            â†’ faiththruphysics-site-data/{series}/phd/{slug}.canonical.md
                 fallback: faiththruphysics-site-data/academic/{series}/{slug}.canonical.md

Usage:
  python top_bar_bottom_bar.py --series revolution-of-truth --dry-run
  python top_bar_bottom_bar.py --series revolution-of-truth --apply
  python top_bar_bottom_bar.py --series revolution-of-truth --apply --page drv-01-the-architecture
  python top_bar_bottom_bar.py --series revolution-of-truth --organize-data --apply

Backups: faiththruphysics-site-data/_inject_backups/top-bar-bottom-bar-<timestamp>/
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

SITE = Path(r"D:\GitHub\faiththruphysics-site")
DATA = Path(r"D:\GitHub\faiththruphysics-site-data")
BACKUP_ROOT = DATA / "_inject_backups"
CANON_METADATA_CSV = Path(
    r"D:\GitHub\Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr\output\canon-ingest\canon-20260629-050303_metadata.csv"
)

LEGACY_LEVEL_SOURCES = {
    "highschool": DATA / "easy",
    "college": DATA / "APIs" / "input",
    "phd": DATA / "academic",
}

SERIES_LEVEL_DIRS = {
    "highschool": "highschool",
    "phd": "phd",
}

SERIES_PAGE_ORDER: dict[str, list[str]] = {
    "consciousness": [
        "consciousness-constraint-argument",
        "consciousness-coherence-bridge",
        "consciousness-chi-field-action",
        "consciousness-grace-source-term",
        "consciousness-reality-assessment",
        "consciousness-scientific-convergence",
        "consciousness-evidence-predictions",
        "consciousness-free-will-evil",
        "consciousness-parallel-laws",
        "consciousness-ontological-taxonomy",
    ],
}

CONSCIOUSNESS_NAV_TITLES = {
    "consciousness-constraint-argument": "01 The Constraint Argument",
    "consciousness-coherence-bridge": "02 The Coherence Bridge",
    "consciousness-chi-field-action": "03 The Ï‡-Field Action",
    "consciousness-grace-source-term": "04 The Grace Source Term",
    "consciousness-reality-assessment": "05 Reality Assessment",
    "consciousness-scientific-convergence": "06 Scientific Convergence",
    "consciousness-evidence-predictions": "07 Evidence & Predictions",
    "consciousness-free-will-evil": "08 Free Will & Evil",
    "consciousness-parallel-laws": "09 Parallel Laws",
    "consciousness-ontological-taxonomy": "10 Ontological Taxonomy",
}

SERIES_DEFAULT_LABELS = {
    "revolution-of-truth": "Revolution of Truth",
    "consciousness": "Consciousness",
}

DOMAIN_COLORS = {
    "theology": "#d4af37",
    "physics": "#7cc7ff",
    "cross-domain": "#3bb39a",
    "cross_domain": "#3bb39a",
    "evidence": "#7fc77f",
    "consciousness": "#14b8a6",
    "mathematics": "#ff7d90",
    "formal_math": "#ff7d90",
    "math": "#ff7d90",
    "information": "#a78bfa",
    "epistemology": "#aeb8d6",
    "ethics": "#7fc77f",
    "psychology": "#c9a0dc",
    "developmental_psychology": "#c9a0dc",
    "sociology": "#8b9dc3",
    "history": "#b8a088",
    "history_culture": "#b8a088",
    "speculative": "#aeb8d6",
    "philosophy": "#aeb8d6",
    "logic_mathematics": "#ff7d90",
    "information_theory": "#a78bfa",
    "empirical_data": "#7fc77f",
}

SLOT_LEVEL_PANELS = "<!-- SLOT:LEVEL_PANELS -->"
SLOT_AUDIT_RIGHT = "<!-- SLOT:AUDIT_RIGHT -->"
SLOT_AUDIT_OVER = "<!-- SLOT:AUDIT_OVER -->"
SLOT_AUDIT_WRONG = "<!-- SLOT:AUDIT_WRONG -->"

SEGMENT_TOP_BAR = "top-bar"
SEGMENT_BOTTOM_BAR = "bottom-bar"
SEGMENT_READING_PANELS = "reading-panels"
SEGMENT_AUDIT_PANELS = "audit-panels"
SEGMENT_METADATA = "metadata"
SEGMENT_ASSETS = "asset-hooks"
ALL_SEGMENTS = [
    SEGMENT_TOP_BAR,
    SEGMENT_BOTTOM_BAR,
    SEGMENT_READING_PANELS,
    SEGMENT_AUDIT_PANELS,
    SEGMENT_METADATA,
    SEGMENT_ASSETS,
]
SEGMENT_DEFAULTS = ALL_SEGMENTS

TOP_BAR_START_TOKEN = "TOP BAR"
TOP_BAR_END_TOKEN = "ARTICLE ENTRY"
BOTTOM_BAR_START_TOKEN = "BOTTOM BAR"
BOTTOM_BAR_END_TOKEN = "THE DOOR"
AUDIT_START_TOKEN = "FINAL AUDIT"
AUDIT_END_TOKEN = "GOLD DIVIDER"
READING_PANEL_START_TOKEN = '<div class="tp-level-panels" id="tpLevelPanels">'

LEVEL_PANEL_COMMENT_TOKEN = "ARTICLE BODY"
THEME_CSS = '<link rel="stylesheet" href="../components/top-bar-bottom-bar.css"/>'
HEADER_CIP_CSS = '<link rel="stylesheet" href="../components/tp-header-lip.css"/>'
VERIFICATION_CSS = '<link rel="stylesheet" href="../components/verification-bar.css"/>'
READING_SCRIPT = '<script src="../components/reading-levels.js"></script>'
TOPBAR_SCRIPT = '<script src="../components/tp-header-lip.js"></script>'
VERIFICATION_SCRIPT = '<script src="../components/verification-bar.js"></script>'

AUDIENCE_FULL = "full"
AUDIENCE_EASY = "easy"
AUDIENCE_ACADEMIC = "academic"
AUDIENCE_LEVELS = [AUDIENCE_FULL, AUDIENCE_EASY, AUDIENCE_ACADEMIC]

BOTTOM_BAR_RE = re.compile(
    r'(<div class="tp-bottom">)([\s\S]*?)(</div>\s*<!--\s*[\s\S]*?THE DOOR)',
    re.IGNORECASE,
)

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
SUBTITLE_RE = re.compile(
    r'<p class="subtitle"[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL | re.IGNORECASE)
BODY_AFTER_AUDIO_RE = re.compile(
    r'<div class="audio-dock-wrap">.*?</div>\s*(.*?)\s*</article>',
    re.DOTALL | re.IGNORECASE,
)
YAML_FENCE_RE = re.compile(r"^```ya?ml\s*\n.*?\n```\s*", re.DOTALL | re.IGNORECASE)


from article_html import md_to_html
from college_enrich import enrich_college_html


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def candidate_md_paths(level: str, series: str, slug: str) -> list[Path]:
    filename = f"{slug}.canonical.md"
    if level == "college":
        return [
            DATA / series / filename,
            LEGACY_LEVEL_SOURCES["college"] / series / filename,
        ]
    series_level_dir = SERIES_LEVEL_DIRS[level]
    return [
        DATA / series / series_level_dir / filename,
        LEGACY_LEVEL_SOURCES[level] / series / filename,
    ]


def load_md(level: str, series: str, slug: str) -> str | None:
    candidates = candidate_md_paths(level, series, slug)
    chosen = next((path for path in candidates if path.is_file()), None)
    if not chosen:
        return None
    return chosen.read_text(encoding="utf-8", errors="replace")


def organize_series_data(series: str, apply: bool, overwrite: bool) -> None:
    mappings = [
        ("highschool", LEGACY_LEVEL_SOURCES["highschool"] / series, DATA / series / "highschool"),
        ("phd", LEGACY_LEVEL_SOURCES["phd"] / series, DATA / series / "phd"),
    ]
    for level, src_dir, dest_dir in mappings:
        files = sorted(src_dir.glob("*.canonical.md")) if src_dir.is_dir() else []
        copied = skipped = 0
        for src in files:
            dest = dest_dir / src.name
            should_copy = overwrite or not dest.exists()
            if apply and should_copy:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            if should_copy:
                copied += 1
            else:
                skipped += 1
        action = "COPIED" if apply else "WOULD COPY"
        print(f"  {action}: {level} {copied} file(s) -> {dest_dir}")
        if skipped:
            print(f"  SKIPPED: {level} {skipped} existing file(s)")


def extract_college_body(existing_html: str) -> str | None:
    m = BODY_AFTER_AUDIO_RE.search(existing_html)
    if not m:
        return None
    body = m.group(1).strip()
    if not body or "tp-template-placeholder" in body:
        return None
    return body


def level_panel(level: str, inner_html: str, default: bool = False) -> str:
    hidden = "" if default else " hidden"
    active = " active" if default else ""
    return (
        f'<div class="tp-level-panel{active}" data-reading-level="{level}"{hidden}>\n'
        f"{inner_html}\n"
        f"</div>"
    )


def levels_for_audience(audience: str) -> list[str]:
    if audience == AUDIENCE_EASY:
        return ["highschool", "college"]
    if audience == AUDIENCE_ACADEMIC:
        return ["college", "phd"]
    return ["highschool", "college", "phd"]


def build_level_panels(
    series: str,
    slug: str,
    existing_html: str | None,
    audience: str,
) -> tuple[str, dict[str, str], list[str]]:
    missing: list[str] = []
    panels: list[str] = []
    college_body = None
    college_md = None
    if existing_html and "tp-level-panels" not in existing_html:
        college_body = extract_college_body(existing_html)

    if not college_body:
        college_md = load_md("college", series, slug)
        if college_md:
            college_body = md_to_html(college_md)
        else:
            college_body = "<p><em>College draft not found.</em></p>"
            missing.append("college")

    college_body = enrich_college_html(college_body)

    available = {
        "highschool": load_md("highschool", series, slug),
        "college": college_md,
        "phd": load_md("phd", series, slug),
    }
    level_order = levels_for_audience(audience)
    for level in level_order:
        if level == "college":
            body = college_body
        elif available.get(level):
            body = md_to_html(available[level])
        else:
            fallback = level_title(level)
            body = f"<p><em>{fallback} draft not found.</em></p>"
            missing.append(level)
        is_default = (level == "college")
        panels.append(level_panel(level, body, default=is_default))

    return (
        "\n".join(panels),
        {"audience": audience, "levels": ", ".join(level_order)},
        missing,
    )


def replace_region(html: str, start_marker: str, end_marker: str, replacement: str) -> tuple[str, bool]:
    start = html.find(start_marker)
    if start == -1:
        return html, False
    end = html.find(end_marker, start)
    if end == -1:
        return html, False
    return (
        html[:start]
        + start_marker
        + "\n"
        + replacement
        + "\n"
        + html[end:],
        True,
    )


def segment_list(raw: Iterable[str] | str | None) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, (list, tuple, set)):
        iterable = raw
    elif isinstance(raw, str):
        iterable = raw.split(",")
    else:
        iterable = list(raw)
    segments = [item.strip().lower() for item in iterable]
    return [seg for seg in segments if seg]


def parse_segments(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


def resolve_segments(explicit: list[str], disabled: list[str], defaults: Iterable[str]) -> list[str]:
    if explicit:
        requested = [seg for seg in explicit if seg in set(defaults)]
    else:
        requested = list(defaults)
    return [seg for seg in requested if seg not in set(disabled)]


def replace_comment_region(
    html: str, start_anchor: str, end_anchor: str, replacement: str
) -> tuple[str, bool]:
    start_anchor_idx = html.find(start_anchor)
    if start_anchor_idx == -1:
        return html, False
    start_comment = html.rfind("<!--", 0, start_anchor_idx + 1)
    if start_comment == -1:
        start_comment = start_anchor_idx
    end_anchor_idx = html.find(end_anchor, start_anchor_idx + 1)
    if end_anchor_idx == -1:
        return html, False
    end_comment = html.rfind("<!--", 0, end_anchor_idx + 1)
    if end_comment == -1 or end_comment < start_comment:
        end_comment = end_anchor_idx
    return html[:start_comment] + replacement + html[end_comment:], True


def replace_reading_panels(html: str, panels: str) -> tuple[str, bool]:
    start = html.find(READING_PANEL_START_TOKEN)
    if start == -1:
        return html, False
    markers = [m for m in re.finditer(r"<!--\s*[^>\n]*ARTICLE BODY[^>\n]*-->", html, re.IGNORECASE)]
    first = next((m for m in reversed(markers) if m.end() <= start), None)
    if not first:
        return html, False
    second = next((m for m in markers if m.start() > first.start()), None)
    if not second:
        return html, False
    if "tp-level-panels" not in html[start : second.start()]:
        return html, False
    return (
        html[:start]
        + f'{READING_PANEL_START_TOKEN}\n{panels}\n</div>\n'
        + html[second.end() :],
        True,
    )


def remove_asset_line(html: str, marker: str) -> str:
    escaped = re.escape(marker)
    return re.sub(rf"(?m)^.*{escaped}.*\r?\n", "", html)


def normalize_assets_html(html: str, enabled_assets: bool, has_reading_panels: bool) -> str:
    if not enabled_assets:
        for marker in (
            HEADER_CIP_CSS,
            VERIFICATION_CSS,
            THEME_CSS,
            TOPBAR_SCRIPT,
            VERIFICATION_SCRIPT,
            READING_SCRIPT,
        ):
            html = remove_asset_line(html, marker)
        return html

    html = ensure_top_bar_css_link(html)
    if has_reading_panels:
        html = ensure_reading_levels_script(html)
    return html


def level_title(level: str) -> str:
    if level == "highschool":
        return "High School"
    if level == "college":
        return "College"
    if level == "phd":
        return "PhD"
    return level.title()


def page_report(summary: dict[str, Any], indent: int = 2) -> str:
    return json.dumps(summary, indent=indent, sort_keys=True, ensure_ascii=False)


def domain_color(name: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    if key in DOMAIN_COLORS:
        return DOMAIN_COLORS[key]
    for token, color in DOMAIN_COLORS.items():
        if token and (token in key or key in token):
            return color
    return "#aeb8d6"


def slug_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _coerce_num(value: str) -> float:
    try:
        return float(re.sub(r"[^0-9.\-]", "", value))
    except (ValueError, TypeError):
        return 0.0


def _manual_frontmatter(text: str) -> dict:
    """Tiny parser for the claims-list + domains-map frontmatter shape."""
    result: dict = {}
    cur_key: str | None = None
    for line in text.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\S", line):
            key, _, rest = line.partition(":")
            cur_key = key.strip()
            rest = rest.strip()
            result[cur_key] = rest if rest else None
        elif cur_key is not None:
            stripped = line.strip()
            if stripped.startswith("- "):
                if not isinstance(result.get(cur_key), list):
                    result[cur_key] = []
                result[cur_key].append(stripped[2:].strip().strip('"').strip("'"))
            elif ":" in stripped:
                if not isinstance(result.get(cur_key), dict):
                    result[cur_key] = {}
                k, _, v = stripped.partition(":")
                result[cur_key][k.strip()] = _coerce_num(v.strip())
    return result


def parse_frontmatter(md: str) -> dict:
    """Extract the ```yaml --- ... --- ``` frontmatter block as a dict."""
    if not md:
        return {}
    m = YAML_FENCE_RE.search(md.strip())
    if not m:
        return {}
    inner = m.group(0)
    inner = re.sub(r"^```ya?ml\s*\n", "", inner, flags=re.IGNORECASE)
    inner = re.sub(r"\n```\s*$", "", inner)
    inner = re.sub(r"^---\s*\n", "", inner)
    inner = re.sub(r"\n---\s*$", "", inner.rstrip())
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(inner)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return _manual_frontmatter(inner)


def domain_profile_from_frontmatter(fm: dict) -> list[dict]:
    domains = fm.get("domains") if isinstance(fm, dict) else None
    if not isinstance(domains, dict) or not domains:
        return []
    items = sorted(domains.items(), key=lambda kv: _coerce_num(str(kv[1])), reverse=True)
    profile = []
    for name, pct in items[:7]:
        profile.append(
            {"name": name, "pct": round(_coerce_num(str(pct))), "color": domain_color(name)}
        )
    return profile


def claims_from_frontmatter(fm: dict) -> list[str]:
    claims = fm.get("claims") if isinstance(fm, dict) else None
    if isinstance(claims, list):
        return [str(c).strip() for c in claims if str(c).strip()]
    return []


def domain_profile_from_scan(series: str, slug: str) -> list[dict]:
    scan_path = DATA / "domain-scan" / series / f"{slug}.json"
    if not scan_path.is_file():
        return []
    data = json.loads(scan_path.read_text(encoding="utf-8"))
    domains = data.get("domains") or {}
    items = sorted(domains.items(), key=lambda kv: kv[1], reverse=True)
    profile = []
    for name, pct in items[:7]:
        key = name.lower().replace(" ", "_").replace("-", "_")
        color = DOMAIN_COLORS.get(key) or DOMAIN_COLORS.get(name.lower()) or "#aeb8d6"
        label = name.replace("_", " ").title()
        if key == "formal_math":
            label = "Mathematics"
        profile.append({"name": label, "pct": round(float(pct)), "color": color})
    return profile


def article_profile_js(profile: list[dict]) -> str:
    if not profile:
        profile = [
            {"name": "Theology", "pct": 28, "color": "#d4af37"},
            {"name": "Physics", "pct": 22, "color": "#7cc7ff"},
        ]
    return json.dumps(profile, indent=2)


def read_canon_metadata(csv_path: Path = CANON_METADATA_CSV) -> list[dict[str, str]]:
    if not csv_path.is_file():
        return []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


CANON_METADATA_ROWS = read_canon_metadata()


def article_metadata_from_csv(series: str, slug: str) -> dict:
    """Return header metadata exported by the canon-ingest batch, if a row matches."""
    slug_norm = slug_key(slug)
    series_norm = slug_key(series)

    def variants(value: str) -> set[str]:
        base = slug_key(value)
        if not base:
            return set()
        values = {base}
        values.add(re.sub(r"-canonical(?:-\d+)?$", "", base))
        values.add(re.sub(r"-\d+$", "", base))
        return {item for item in values if item}

    def row_keys(row: dict[str, str]) -> set[str]:
        keys = set()
        keys.update(variants(row.get("article_id", "")))
        keys.update(variants(Path(row.get("source_file", "")).stem))
        source_parts = [slug_key(part) for part in re.split(r"[\\/]+", row.get("source_file", "")) if part]
        for part in source_parts:
            keys.update(variants(part))
        return {key for key in keys if key}

    row = next(
        (
            item
            for item in CANON_METADATA_ROWS
            if slug_norm in row_keys(item)
            and (not item.get("series") or slug_key(item.get("series", "")) in {series_norm, slug_norm})
        ),
        None,
    )
    if not row:
        row = next((item for item in CANON_METADATA_ROWS if slug_norm in row_keys(item)), None)
    if not row:
        return {}

    fields = [
        "run_id",
        "article_id",
        "one_sentence",
        "executive_summary",
        "short_summary",
        "keywords",
        "primary_tags",
        "secondary_tags",
        "chi_variables",
        "series",
        "type",
        "reading_level",
        "framework_laws",
        "related_isos",
        "related_laws",
        "prerequisite_reading",
        "follow_up_reading",
        "source_file",
    ]
    return {key: (row.get(key) or "").strip() for key in fields if (row.get(key) or "").strip()}


def article_metadata_from_markdown(series: str, slug: str, meta: dict, frontmatter: dict) -> dict:
    metadata = {
        "article_id": slug,
        "series": series,
        "type": str(frontmatter.get("type") or "article"),
        "reading_level": str(frontmatter.get("reading_level") or "college"),
    }
    if meta.get("subtitle"):
        metadata["one_sentence"] = meta["subtitle"]
    if isinstance(frontmatter.get("primary_tags"), str):
        metadata["primary_tags"] = frontmatter["primary_tags"]
    if isinstance(frontmatter.get("keywords"), str):
        metadata["keywords"] = frontmatter["keywords"]
    return {k: v for k, v in metadata.items() if v}


def audit_lists(series: str, slug: str) -> tuple[list[str], list[str], list[str]]:
    """Future: load rigor JSON. For now, keep template placeholders."""
    audit_path = DATA / "rigor" / series / f"{slug}.json"
    if audit_path.is_file():
        data = json.loads(audit_path.read_text(encoding="utf-8"))
        return (
            data.get("got_right", []),
            data.get("overstated", []),
            data.get("got_wrong", []),
        )
    return (
        ["Load-bearing claims, clear definitions, and the parts that clearly survived the check."],
        ["Strong direction, but the language ran ahead of the evidence or the proof."],
        ["Claims that need correction, tightening, or weaker formulation."],
    )


def audit_ul(items: list[str]) -> str:
    return "\n".join(f"          <li>{item}</li>" for item in items)


def page_meta(existing_html: str | None, slug: str) -> dict[str, str]:
    title = slug.replace("-", " ").title()
    subtitle = ""
    doc_title = title
    if existing_html:
        m = H1_RE.search(existing_html)
        if m:
            title = strip_tags(m.group(1))
        m = SUBTITLE_RE.search(existing_html)
        if m:
            subtitle = strip_tags(m.group(1))
        m = TITLE_RE.search(existing_html)
        if m:
            doc_title = strip_tags(m.group(1))
    return {"h1": title, "subtitle": subtitle, "doc_title": doc_title}


def nav_title(slug: str) -> str:
    if slug in CONSCIOUSNESS_NAV_TITLES:
        return CONSCIOUSNESS_NAV_TITLES[slug]
    return slug.replace("drv-", "").replace("consciousness-", "").replace("-", " ").title()


def nav_links(pages: list[str], slug: str) -> dict[str, str]:
    idx = pages.index(slug) if slug in pages else -1
    prev_href = next_href = "#"
    prev_title = next_title = ""
    if idx > 0:
        prev_slug = pages[idx - 1]
        prev_href = f"{prev_slug}.html"
        prev_title = nav_title(prev_slug)
    if 0 <= idx < len(pages) - 1:
        next_slug = pages[idx + 1]
        next_href = f"{next_slug}.html"
        next_title = nav_title(next_slug)
    return {
        "prev_href": prev_href,
        "prev_title": prev_title,
        "next_href": next_href,
        "next_title": next_title,
    }


def ensure_top_bar_css_link(html: str) -> str:
    link = '<link rel="stylesheet" href="../components/top-bar-bottom-bar.css"/>'
    if "top-bar-bottom-bar.css" in html:
        return html
    return html.replace(
        '<link rel="stylesheet" href="../components/verification-bar.css"/>',
        '<link rel="stylesheet" href="../components/verification-bar.css"/>\n' + link,
    )


def ensure_reading_levels_script(html: str) -> str:
    script = '<script src="../components/reading-levels.js"></script>'
    if "reading-levels.js" in html:
        return html
    return html.replace(
        '<script src="../components/verification-bar.js"></script>',
        '<script src="../components/verification-bar.js"></script>\n' + script,
    )


def build_page(
    template: str,
    series: str,
    series_label: str,
    slug: str,
    pages: list[str],
    existing_html: str | None,
    segments: list[str],
    audience: str,
) -> tuple[str, dict[str, Any]]:
    meta = page_meta(existing_html, slug)
    nav = nav_links(pages, slug)
    frontmatter = parse_frontmatter(load_md("highschool", series, slug) or "")
    profile = domain_profile_from_frontmatter(frontmatter) or domain_profile_from_scan(series, slug)
    claims = claims_from_frontmatter(frontmatter)
    metadata = article_metadata_from_csv(series, slug) or article_metadata_from_markdown(series, slug, meta, frontmatter)
    got_right, overstated, got_wrong = audit_lists(series, slug)
    enabled_segments = [seg for seg in segments if seg in set(ALL_SEGMENTS)]
    enabled_set = set(enabled_segments)
    segment_status: dict[str, bool] = {seg: False for seg in ALL_SEGMENTS}
    notes: list[str] = []

    panels, panel_metadata, missing_levels = build_level_panels(
        series, slug, existing_html, audience
    )

    html = template
    html = html.replace("PAGE TITLE | Series", meta["doc_title"])
    html = html.replace("<h1>Paper Title</h1>", f"<h1>{meta['h1']}</h1>")
    html = html.replace(
        "<p class=\"subtitle\">Paper subtitle goes here</p>",
        f'<p class="subtitle">{meta["subtitle"]}</p>' if meta["subtitle"] else '<p class="subtitle"></p>',
    )
    html = html.replace("SERIES/PAGE-SLUG", f"{series}/{slug}")
    html = html.replace("SERIES%2FPAGE-SLUG", f"{series}%2F{slug}")
    html = html.replace('data-series-slug="SERIES"', f'data-series-slug="{series}"')
    html = html.replace(
        f"data-series-lookup=\"https://faith-audio-pipeline.davidokc28.workers.dev/api/audio?slug=SERIES\"",
        f"data-series-lookup=\"https://faith-audio-pipeline.davidokc28.workers.dev/api/audio?slug={series}\"",
    )
    html = html.replace('class="tp-bignav-series">Series Home</a>', f'class="tp-bignav-series">{series_label} Home</a>')
    html = html.replace('href="/revolution-of-truth/"', f'href="/{series}/"')
    html = html.replace('href="/consciousness/"', f'href="/{series}/"')

    # Hide the prev/next anchor entirely when there is no neighbor (e.g. first/last page),
    # otherwise wire up the href. Use a hidden attribute so the row keeps its layout.
    if nav["prev_href"] == "#":
        html = html.replace('href="#" class="tp-bignav-prev"', 'href="#" class="tp-bignav-prev" hidden aria-hidden="true"')
    else:
        html = html.replace('href="#" class="tp-bignav-prev"', f'href="{nav["prev_href"]}" class="tp-bignav-prev"')
    if nav["next_href"] == "#":
        html = html.replace('href="#" class="tp-bignav-next"', 'href="#" class="tp-bignav-next" hidden aria-hidden="true"')
    else:
        html = html.replace('href="#" class="tp-bignav-next"', f'href="{nav["next_href"]}" class="tp-bignav-next"')

    # Use function-based replacement (NOT a backreference string): titles can start with a
    # digit (e.g. "01 The Architecture") which would otherwise be parsed as an octal/group
    # escape like \101 -> 'A', corrupting the markup. See _navtest evidence.
    html = re.sub(
        r'(<a[^>]*class="tp-bignav-prev"[^>]*>.*?<span class="tp-bignav-title">)(.*?)(</span>)',
        lambda m, t=nav["prev_title"]: m.group(1) + t + m.group(3),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'(<a[^>]*class="tp-bignav-next"[^>]*>.*?<span class="tp-bignav-title">)(.*?)(</span>)',
        lambda m, t=nav["next_title"]: m.group(1) + t + m.group(3),
        html,
        count=1,
        flags=re.DOTALL,
    )

    if SEGMENT_TOP_BAR in enabled_set:
        segment_status[SEGMENT_TOP_BAR] = True
    else:
        html, changed = replace_comment_region(html, TOP_BAR_START_TOKEN, TOP_BAR_END_TOKEN, "")
        segment_status[SEGMENT_TOP_BAR] = changed
        if not changed:
            notes.append("Could not remove TOP BAR region.")

    if SEGMENT_READING_PANELS in enabled_set:
        html, changed = replace_reading_panels(html, panels)
        segment_status[SEGMENT_READING_PANELS] = changed
        if not changed:
            notes.append("Could not replace reading-panel region.")
    else:
        placeholder = (
            '<div class="tp-template-placeholder">Reading panels disabled for this run.</div>'
        )
        html, changed = replace_reading_panels(html, placeholder)
        segment_status[SEGMENT_READING_PANELS] = changed
        if not changed:
            notes.append("Could not replace reading-panel region for disabled mode.")

    if SEGMENT_AUDIT_PANELS in enabled_set:
        html = html.replace(SLOT_AUDIT_RIGHT, audit_ul(got_right))
        html = html.replace(SLOT_AUDIT_OVER, audit_ul(overstated))
        html = html.replace(SLOT_AUDIT_WRONG, audit_ul(got_wrong))
        segment_status[SEGMENT_AUDIT_PANELS] = True
    else:
        html, changed = replace_comment_region(
            html,
            AUDIT_START_TOKEN,
            AUDIT_END_TOKEN,
            "",
        )
        segment_status[SEGMENT_AUDIT_PANELS] = changed
        if not changed:
            html = html.replace(SLOT_AUDIT_RIGHT, "")
            html = html.replace(SLOT_AUDIT_OVER, "")
            html = html.replace(SLOT_AUDIT_WRONG, "")
            segment_status[SEGMENT_AUDIT_PANELS] = True
            notes.append("Could not remove audit region; audit slots were cleared.")

    if SEGMENT_BOTTOM_BAR in enabled_set:
        segment_status[SEGMENT_BOTTOM_BAR] = True
    else:
        html, changed = replace_comment_region(html, BOTTOM_BAR_START_TOKEN, BOTTOM_BAR_END_TOKEN, "")
        segment_status[SEGMENT_BOTTOM_BAR] = changed
        if not changed:
            notes.append("Could not remove BOTTOM BAR region.")

    if SEGMENT_METADATA in enabled_set:
        profile_js = article_profile_js(profile)
        claims_js = json.dumps(claims, indent=2, ensure_ascii=False)
        metadata_js = json.dumps(metadata, indent=2, ensure_ascii=False)
        replacement = (
            f"const ARTICLE_PROFILE={profile_js};\n"
            f"const ARTICLE_CLAIMS={claims_js};\n"
            f"const ARTICLE_METADATA={metadata_js};"
        )
        html = re.sub(
            r"const ARTICLE_PROFILE=\[[\s\S]*?\];(\s*const ARTICLE_CLAIMS=[\s\S]*?\];)?(\s*const ARTICLE_METADATA=\{[\s\S]*?\};)?",
            lambda _m: replacement,
            html,
            count=1,
        )
        segment_status[SEGMENT_METADATA] = True

    html = normalize_assets_html(
        html,
        enabled_assets=SEGMENT_ASSETS in enabled_set,
        has_reading_panels=SEGMENT_READING_PANELS in enabled_set,
    )
    segment_status[SEGMENT_ASSETS] = SEGMENT_ASSETS in enabled_set

    report = {
        "slug": slug,
        "audience": audience,
        "segments_requested": enabled_segments,
        "segment_status": segment_status,
        "reading_levels": panel_metadata,
        "missing_levels": missing_levels,
        "notes": notes,
    }
    return html, report


def list_series_pages(series_dir: Path, series: str) -> list[str]:
    if series in SERIES_PAGE_ORDER:
        return [
            slug
            for slug in SERIES_PAGE_ORDER[series]
            if (series_dir / f"{slug}.html").is_file()
            or (DATA / series / f"{slug}.canonical.md").is_file()
        ]
    return sorted(
        p.stem for p in series_dir.glob("drv-*.html") if p.name != "_TEMPLATE.html"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply top bar + bottom bar page shell")
    parser.add_argument("--series", default="revolution-of-truth")
    parser.add_argument("--series-label", default=None)
    parser.add_argument("--page", help="Single page slug (without .html)")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--segments",
        default=",".join(SEGMENT_DEFAULTS),
        help="Comma-separated segments to enable (default: all).",
    )
    parser.add_argument(
        "--disable-segments",
        default="",
        help="Comma-separated segments to disable.",
    )
    parser.add_argument(
        "--audience",
        default=AUDIENCE_FULL,
        choices=AUDIENCE_LEVELS,
        help="Reading level profile to include.",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Optional JSON report output path (for example reports/top-bar-build.json).",
    )
    parser.add_argument("--organize-data", action="store_true", help="Copy easy/academic variants into the series data folder.")
    parser.add_argument("--overwrite-data", action="store_true", help="Overwrite existing organized data files.")
    args = parser.parse_args()

    apply = args.apply and not args.dry_run
    series = args.series
    requested_segments = parse_segments(args.segments)
    disable_segments = parse_segments(args.disable_segments)
    invalid_requested = [item for item in requested_segments if item not in set(SEGMENT_DEFAULTS)]
    invalid_disabled = [item for item in disable_segments if item not in set(SEGMENT_DEFAULTS)]
    if invalid_requested or invalid_disabled:
        invalid_requested = ", ".join(sorted(set(invalid_requested + invalid_disabled)))
        print(f"Invalid segment(s): {invalid_requested}")
        return 1
    enabled_segments = resolve_segments(requested_segments, disable_segments, SEGMENT_DEFAULTS)
    if not enabled_segments:
        print("No segments enabled; nothing would be written.")
        return 1

    audience = args.audience
    disabled_segments = [seg for seg in SEGMENT_DEFAULTS if seg not in set(enabled_segments)]
    series_label = args.series_label or SERIES_DEFAULT_LABELS.get(series, series.replace("-", " ").title())
    series_dir = SITE / series
    template_path = series_dir / "_TEMPLATE.html"
    if not template_path.is_file():
        print(f"Missing template: {template_path}")
        return 1

    template = template_path.read_text(encoding="utf-8", errors="replace")
    pages = list_series_pages(series_dir, series)
    if args.page:
        pages = [args.page]

    backup_dir = None
    if apply:
        backup_dir = BACKUP_ROOT / f"top-bar-bottom-bar-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"Backups: {backup_dir}")

    all_pages = list_series_pages(series_dir, series)
    print(f"{'APPLY' if apply else 'DRY RUN'} -- {series} -- {len(pages)} page(s)")
    print(f"Audience: {audience}")
    print(
        "Segments enabled: "
        + (", ".join(enabled_segments) if enabled_segments else "(none)")
        + " | disabled: "
        + ", ".join(disabled_segments)
    )
    print()

    if args.organize_data:
        print("Organizing data into the series folder:")
        organize_series_data(series, apply=apply, overwrite=args.overwrite_data)
        print()

    page_reports: list[dict[str, Any]] = []

    for slug in pages:
        out_path = series_dir / f"{slug}.html"
        existing = out_path.read_text(encoding="utf-8", errors="replace") if out_path.is_file() else None
        built, page_report = build_page(
            template,
            series,
            series_label,
            slug,
            all_pages,
            existing,
            segments=enabled_segments,
            audience=audience,
        )
        changed = existing != built
        status = "WOULD WRITE" if not apply else ("WROTE" if changed else "UNCHANGED")
        print(f"  {status}: {series}/{slug}.html")
        if apply and changed:
            if backup_dir and out_path.is_file():
                dest = backup_dir / series / f"{slug}.html"
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(out_path, dest)
            out_path.write_text(built, encoding="utf-8", newline="\n")
        page_report["status"] = status
        page_report["changed"] = changed
        page_reports.append(page_report)

    run_report = {
        "series": series,
        "series_label": series_label,
        "page_count": len(pages),
        "audience": audience,
        "segments_enabled": enabled_segments,
        "segments_disabled": disabled_segments,
        "pages": page_reports,
    }

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(run_report, indent=2, ensure_ascii=False),
            encoding="utf-8",
            newline="\n",
        )
        print(f"Report written: {report_path}")

    if not apply:
        print("\nRe-run with --apply to write pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
