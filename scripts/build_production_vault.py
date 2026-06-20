#!/usr/bin/env python3
"""
Build a production Markdown vault from verified Markdown sources and HTML pages.

The script accepts only high-confidence source Markdown matches by default, writes a
review manifest, then converts every remaining HTML page into Markdown.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag


DEFAULT_REPORTS = [
    "reports/html-title-md-report-d-vault-used-sources-first500.csv",
    "reports/html-title-md-report-o-vault-master-equation-first500.csv",
    "reports/html-title-md-report-d-canonical-first500.csv",
    "reports/html-title-md-report-d-mda-merge-first500.csv",
    "reports/html-title-md-report-o-theophysics-v3-first500.csv",
]

EXCLUDED_HTML_PARTS = {
    ".git",
    ".wrangler",
    "node_modules",
    "Kimi_Agent_ONEPAGE_GLOWINGBALL",
    "subdomains",
}

ARTIFACT_PATTERNS = [
    r"<!doctype\s+html",
    r"<html[\s>]",
    r"<body[\s>]",
    r"<div[\s>]",
    r"<script[\s>]",
    r"webpackJsonp",
    r"vite/preload-helper",
    r"^={6,}$",
]


@dataclass
class Candidate:
    html_path: str
    html_title: str
    score: int
    match_type: str
    source_path: Path


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def sanitize_rel(path_value: str, suffix: str = ".md") -> Path:
    path_value = path_value.replace("\\", "/")
    path = Path(path_value)
    parts = [sanitize_part(part) for part in path.parts if part not in ("", ".")]
    if not parts:
        parts = ["untitled"]
    out = Path(*parts)
    return out.with_suffix(suffix)


def sanitize_part(value: str) -> str:
    value = re.sub(r"[<>:\"|?*\x00-\x1f]", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value.rstrip(". ") or "untitled"


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def load_candidates(report_paths: list[Path], min_score: int) -> list[Candidate]:
    candidates: dict[str, Candidate] = {}
    for report in report_paths:
        if not report.exists():
            continue
        with report.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                source = row.get("best_md_path", "").strip()
                if not source:
                    continue
                try:
                    score = int(row.get("best_score") or 0)
                except ValueError:
                    score = 0
                match_type = row.get("match_type", "")
                if score < min_score or not match_type.startswith("exact"):
                    continue
                html_path = row.get("html_path", "").strip()
                current = candidates.get(html_path)
                candidate = Candidate(
                    html_path=html_path,
                    html_title=row.get("html_title", "").strip(),
                    score=score,
                    match_type=match_type,
                    source_path=Path(source),
                )
                if current is None or candidate.score > current.score:
                    candidates[html_path] = candidate
    return sorted(candidates.values(), key=lambda item: item.html_path.lower())


def review_markdown(path: Path) -> dict[str, object]:
    exists = path.exists()
    text = read_text(path) if exists else ""
    lower = text.lower()
    artifact_hits = sum(1 for pattern in ARTIFACT_PATTERNS if re.search(pattern, lower, re.M))
    html_tags = len(re.findall(r"<[a-z][^>]*>", lower))
    headings = len(re.findall(r"^#{1,6}\s+", text, re.M))
    links = len(re.findall(r"\[[^\]]+\]\([^)]+\)", text))
    words = len(re.findall(r"\b[\w'-]+\b", text))
    replacement_chars = text.count("\ufffd")
    very_long_lines = sum(1 for line in text.splitlines() if len(line) > 600)
    ok = (
        exists
        and words >= 80
        and artifact_hits == 0
        and html_tags <= 10
        and replacement_chars == 0
    )
    reasons = []
    if not exists:
        reasons.append("missing")
    if words < 150:
        reasons.append("too-short")
    if artifact_hits:
        reasons.append(f"artifact-patterns:{artifact_hits}")
    if html_tags > 10:
        reasons.append(f"html-tags:{html_tags}")
    if replacement_chars:
        reasons.append(f"encoding-replacements:{replacement_chars}")
    if very_long_lines > 2:
        reasons.append(f"long-lines-note:{very_long_lines}")
    return {
        "exists": exists,
        "words": words,
        "chars": len(text),
        "headings": headings,
        "links": links,
        "html_tags": html_tags,
        "artifact_hits": artifact_hits,
        "replacement_chars": replacement_chars,
        "very_long_lines": very_long_lines,
        "accepted": ok,
        "review_notes": ";".join(reasons),
    }


def add_frontmatter(body: str, metadata: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        escaped = str(value).replace('"', '\\"')
        lines.append(f'{key}: "{escaped}"')
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def copy_source(candidate: Candidate, vault_root: Path) -> Path:
    text = read_text(candidate.source_path)
    destination = vault_root / "source-md" / sanitize_rel(candidate.html_path)
    body = add_frontmatter(
        text,
        {
            "title": candidate.html_title,
            "source_type": "verified_markdown",
            "html_path": candidate.html_path,
            "source_md_path": str(candidate.source_path),
            "match_type": candidate.match_type,
            "match_score": str(candidate.score),
        },
    )
    write_text(destination, body)
    return destination


def html_files(root: Path, include_all_html: bool = False) -> list[Path]:
    files = []
    for path in list(root.rglob("*.html")) + list(root.rglob("*.htm")):
        rel = path.relative_to(root)
        if not include_all_html and any(part in EXCLUDED_HTML_PARTS for part in rel.parts):
            continue
        if not include_all_html and ("backup" in str(rel).lower() or ".bak" in str(rel).lower()):
            continue
        files.append(path)
    return sorted(files)


def html_title(soup: BeautifulSoup, fallback: str) -> str:
    if soup.title and soup.title.get_text(strip=True):
        return clean(soup.title.get_text(" ", strip=True))
    h1 = soup.find("h1")
    if h1:
        return clean(h1.get_text(" ", strip=True))
    return fallback


def clean(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "")
    return value.strip()


def node_to_md(node: Tag | NavigableString) -> str:
    if isinstance(node, Comment):
        return ""
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in {"script", "style", "noscript", "svg", "canvas", "button", "form", "nav", "header", "footer", "audio", "iframe"}:
        return ""
    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(name[1])
        return "\n\n" + ("#" * level) + " " + clean(children_to_md(node)) + "\n\n"
    if name == "p":
        return "\n\n" + clean(children_to_md(node)) + "\n\n"
    if name == "br":
        return "\n"
    if name in {"strong", "b"}:
        return f"**{clean(children_to_md(node))}**"
    if name in {"em", "i"}:
        return f"*{clean(children_to_md(node))}*"
    if name == "code":
        return "`" + node.get_text("", strip=True).replace("`", "\\`") + "`"
    if name == "pre":
        code = node.get_text("\n").strip()
        return "\n\n```text\n" + code + "\n```\n\n"
    if name == "a":
        label = clean(children_to_md(node)) or clean(node.get_text(" ", strip=True))
        href = node.get("href", "")
        return f"[{label}]({href})" if href and label else label
    if name == "img":
        alt = clean(node.get("alt", ""))
        src = node.get("src", "")
        return f"![{alt}]({src})" if src else ""
    if name in {"ul", "ol"}:
        chunks = []
        ordered = name == "ol"
        for index, child in enumerate(node.find_all("li", recursive=False), start=1):
            marker = f"{index}. " if ordered else "- "
            chunks.append(marker + clean(children_to_md(child)))
        return "\n\n" + "\n".join(chunks) + "\n\n"
    if name == "blockquote":
        text = clean(children_to_md(node))
        return "\n\n" + "\n".join("> " + line for line in text.splitlines()) + "\n\n"
    if name in {"table"}:
        return "\n\n" + clean(node.get_text(" | ", strip=True)) + "\n\n"
    return children_to_md(node)


def children_to_md(node: Tag) -> str:
    return "".join(node_to_md(child) for child in node.children)


def html_to_markdown(path: Path, repo_root: Path) -> tuple[str, str]:
    soup = BeautifulSoup(read_text(path), "html.parser")
    chrome_selectors = [
        "script",
        "style",
        "noscript",
        "svg",
        "canvas",
        "nav",
        "header",
        "footer",
        "audio",
        "iframe",
        ".top-bar",
        ".top-nav",
        ".bot-nav",
        ".bnav-grid",
        ".audio-bar",
        ".ring-nav",
        ".tp-ribbon",
        ".site-shell",
        ".breadcrumb",
        ".breadcrumbs",
    ]
    for selector in chrome_selectors:
        for tag in soup.select(selector):
            tag.decompose()
    title = html_title(soup, path.stem)
    container = soup.find("main") or soup.find("article") or soup.body or soup
    markdown = children_to_md(container)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = "\n".join(
        line
        for line in markdown.splitlines()
        if not re.match(r"^\s*[═─━\-]{6,}\s*$", line)
    )
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.strip()
    if not markdown.startswith("#"):
        markdown = f"# {title}\n\n{markdown}"
    rel = str(path.relative_to(repo_root))
    markdown = add_frontmatter(
        markdown,
        {
            "title": title,
            "source_type": "html_rip",
            "html_path": rel,
        },
    )
    return title, markdown


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def display_path(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create production-vault Markdown corpus.")
    parser.add_argument("--vault-root", default="production-vault")
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument("--min-score", type=int, default=100)
    parser.add_argument("--clear", action="store_true", help="Delete the generated vault folders first.")
    parser.add_argument(
        "--include-all-html",
        action="store_true",
        help="Import every .html/.htm file, including subdomains, generated apps, and backup-like files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    vault_root = (repo_root / args.vault_root).resolve()
    reports = [Path(path) for path in (args.report or DEFAULT_REPORTS)]

    if args.clear and vault_root.exists():
        shutil.rmtree(vault_root)

    candidates = load_candidates(reports, args.min_score)
    accepted_html: set[str] = set()
    review_rows: list[dict[str, object]] = []

    for candidate in candidates:
        review = review_markdown(candidate.source_path)
        destination = ""
        if review["accepted"]:
            destination = display_path(copy_source(candidate, vault_root), repo_root)
            accepted_html.add(candidate.html_path.replace("/", "\\"))
        row = {
            "html_path": candidate.html_path,
            "html_title": candidate.html_title,
            "match_score": candidate.score,
            "match_type": candidate.match_type,
            "source_md_path": str(candidate.source_path),
            "accepted": review["accepted"],
            "destination": destination,
            **review,
        }
        review_rows.append(row)

    rip_rows: list[dict[str, object]] = []
    for html_path in html_files(repo_root, args.include_all_html):
        rel = str(html_path.relative_to(repo_root))
        if rel in accepted_html:
            continue
        title, markdown = html_to_markdown(html_path, repo_root)
        destination = vault_root / "ripped-md" / sanitize_rel(rel)
        write_text(destination, markdown)
        words = len(re.findall(r"\b[\w'-]+\b", markdown))
        status = "content"
        if words < 100:
            status = "low_signal"
        if "redirecting to" in title.lower() or "redirecting to" in markdown[:300].lower():
            status = "redirect"
        if "\\components\\" in rel or rel.startswith("components\\"):
            status = "component"
        rip_rows.append(
            {
                "html_path": rel,
                "title": title,
                "destination": display_path(destination, repo_root),
                "words": words,
                "status": status,
            }
        )

    write_csv(
        vault_root / "manifests" / "source-md-review.csv",
        review_rows,
        [
            "html_path",
            "html_title",
            "match_score",
            "match_type",
            "source_md_path",
            "accepted",
            "destination",
            "exists",
            "words",
            "chars",
            "headings",
            "links",
            "html_tags",
            "artifact_hits",
            "replacement_chars",
            "very_long_lines",
            "review_notes",
        ],
    )
    write_csv(
        vault_root / "manifests" / "html-rip-manifest.csv",
        rip_rows,
        ["html_path", "title", "destination", "words", "status"],
    )
    status_counts: dict[str, int] = {}
    for row in rip_rows:
        status_counts[str(row["status"])] = status_counts.get(str(row["status"]), 0) + 1
    status_lines = "\n".join(f"  - {key}: {value}" for key, value in sorted(status_counts.items()))
    summary = (
        "# Production Vault Build\n\n"
        f"- Candidate exact Markdown matches reviewed: {len(review_rows)}\n"
        f"- Source Markdown files accepted: {sum(1 for row in review_rows if row['accepted'])}\n"
        f"- HTML files ripped to Markdown: {len(rip_rows)}\n"
        f"- HTML rip status counts:\n{status_lines}\n"
        f"- Source review: `manifests/source-md-review.csv`\n"
        f"- HTML rip manifest: `manifests/html-rip-manifest.csv`\n"
    )
    write_text(vault_root / "README.md", summary)
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
