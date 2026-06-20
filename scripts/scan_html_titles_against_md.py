#!/usr/bin/env python3
"""
Scan HTML files for page titles, then look for matching Markdown files.

Examples:
  python scripts/scan_html_titles_against_md.py --md-root docs --md-root three-truths/content
  python scripts/scan_html_titles_against_md.py --html-root genesis-to-quantum --md-root genesis-to-quantum/CODEX_BUILD/markdown --md-root docs
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    ".wrangler",
    "__pycache__",
    "node_modules",
    ".next",
    "dist",
    "build",
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "by",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


@dataclass
class HtmlPage:
    path: Path
    title: str


@dataclass
class MarkdownPage:
    path: Path
    title: str
    h1: str
    frontmatter_title: str


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._in_title = False
        self._in_h1 = False
        self._title_parts: list[str] = []
        self._h1_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._in_title = True
        elif tag.lower() == "h1":
            self._in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        elif tag.lower() == "h1":
            self._in_h1 = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        elif self._in_h1:
            self._h1_parts.append(data)

    @property
    def title(self) -> str:
        return clean_text(" ".join(self._title_parts))

    @property
    def h1(self) -> str:
        return clean_text(" ".join(self._h1_parts))


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_title(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"\|.*$", "", value).strip()
    suffixes = (
        "faith thru physics",
        "theophysics",
        "genesis to quantum",
        "proof explorer",
        "master equation",
        "the convergence series",
        "convergence series",
        "david lowe",
    )
    value = re.sub(rf"[-–—]\s*({'|'.join(suffixes)}).*$", "", value).strip()
    value = re.sub(r"^article\s+\d+[a-z]?\s*:\s*", "", value)
    value = re.sub(r"^(gtq|mda|pi_mda|iso|meq|pa|drv|cns|cdt)[-_ ]*\d+[a-z]?[-_ ]+", "", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_title(value)).strip("-")


def should_skip(path: Path, include_hidden: bool) -> bool:
    for part in path.parts:
        if part in DEFAULT_EXCLUDES:
            return True
        if not include_hidden and part.startswith("."):
            return True
    return False


def iter_files(
    root: Path,
    suffixes: tuple[str, ...],
    include_hidden: bool,
    max_depth: int | None = None,
    file_limit: int | None = None,
    excludes: list[Path] | None = None,
) -> list[Path]:
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")
    if root.is_file():
        return [root] if root.suffix.lower() in suffixes else []
    resolved_excludes = [path.resolve() for path in (excludes or [])]

    rg = shutil.which("rg")
    if rg:
        patterns = []
        for suffix in suffixes:
            patterns.extend(["-g", f"*{suffix}"])
        for name in DEFAULT_EXCLUDES:
            patterns.extend(["-g", f"!{name}/**"])
        command = [rg, "--files", "--no-messages", str(root), *patterns]
        if include_hidden:
            command.insert(2, "--hidden")
        if max_depth is not None:
            command[2:2] = ["--max-depth", str(max_depth)]
        if file_limit is not None:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            paths: list[Path] = []
            assert process.stdout is not None
            for line in process.stdout:
                line = line.strip()
                if line:
                    candidate = Path(line)
                    if not is_excluded(candidate, resolved_excludes):
                        paths.append(candidate)
                if len(paths) >= file_limit:
                    process.terminate()
                    break
            process.wait(timeout=10)
            return sorted(paths)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode in (0, 1):
            return sorted(
                candidate
                for line in (result.stdout or "").splitlines()
                if line.strip()
                for candidate in [Path(line)]
                if not is_excluded(candidate, resolved_excludes)
            )
        print(f"rg failed for {root}; falling back to Python scan.", file=sys.stderr)

    return sorted(
        path
        for index, path in enumerate(root.rglob("*"))
        if path.is_file()
        and path.suffix.lower() in suffixes
        and (max_depth is None or len(path.relative_to(root).parts) <= max_depth)
        and not should_skip(path.relative_to(root), include_hidden)
        and (file_limit is None or index < file_limit)
        and not is_excluded(path.resolve(), resolved_excludes)
    )


def is_excluded(path: Path, excludes: list[Path]) -> bool:
    for exclude in excludes:
        try:
            path.relative_to(exclude)
            return True
        except ValueError:
            continue
    return False


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def extract_html_title(path: Path) -> HtmlPage:
    parser = TitleParser()
    parser.feed(read_text(path))
    title = parser.title or parser.h1 or path.stem
    return HtmlPage(path=path, title=title)


def extract_frontmatter_title(text: str) -> str:
    if not text.startswith("---"):
        return ""
    match = re.match(r"---\s*\n(.*?)\n---\s*(?:\n|$)", text, flags=re.S)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        title_match = re.match(r"\s*title\s*:\s*(.+?)\s*$", line, flags=re.I)
        if title_match:
            return clean_text(title_match.group(1).strip("\"'"))
    return ""


def extract_markdown_page(path: Path, filename_only: bool = False) -> MarkdownPage:
    if filename_only:
        return MarkdownPage(path=path, title=path.stem, h1="", frontmatter_title="")
    text = read_text(path)
    frontmatter_title = extract_frontmatter_title(text)
    h1 = ""
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            h1 = clean_text(match.group(1))
            break
    title = frontmatter_title or h1 or path.stem
    return MarkdownPage(path=path, title=title, h1=h1, frontmatter_title=frontmatter_title)


def score_match(html_page: HtmlPage, md_page: MarkdownPage) -> tuple[int, str]:
    html_norm = normalize_title(html_page.title)
    html_slug = slugify(html_page.title)
    md_titles = [md_page.title, md_page.h1, md_page.frontmatter_title, md_page.path.stem]
    md_norms = [normalize_title(value) for value in md_titles if value]
    md_slugs = [slugify(value) for value in md_titles if value]

    if html_norm and html_norm in md_norms:
        return 100, "exact-title"
    if html_slug and html_slug in md_slugs:
        return 95, "exact-slug"
    if html_slug and html_slug == slugify(md_page.path.stem):
        return 90, "filename-slug"

    best = 0
    best_type = ""
    html_words = {word for word in html_norm.split() if word not in STOPWORDS}
    for md_norm in md_norms:
        if not md_norm:
            continue
        md_words = {word for word in md_norm.split() if word not in STOPWORDS}
        enough_title_signal = len(md_words) >= 2 or len(md_norm) >= 12
        if html_norm and enough_title_signal and (html_norm in md_norm or md_norm in html_norm):
            score = 80
            match_type = "contains-title"
        elif html_words and md_words:
            overlap = len(html_words & md_words) / max(len(html_words | md_words), 1)
            score = round(overlap * 75)
            match_type = "word-overlap"
        else:
            score = 0
            match_type = ""
        if score > best:
            best = score
            best_type = match_type
    return best, best_type


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def build_report(
    html_pages: list[HtmlPage],
    md_pages: list[MarkdownPage],
    repo_root: Path,
    min_score: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for html_page in html_pages:
        matches = []
        for md_page in md_pages:
            score, match_type = score_match(html_page, md_page)
            if score >= min_score:
                matches.append((score, match_type, md_page))
        matches.sort(key=lambda item: (-item[0], str(item[2].path).lower()))
        best = matches[0] if matches else None
        rows.append(
            {
                "html_path": relative(html_page.path, repo_root),
                "html_title": html_page.title,
                "md_match_count": len(matches),
                "best_score": best[0] if best else "",
                "match_type": best[1] if best else "",
                "best_md_path": relative(best[2].path, repo_root) if best else "",
                "best_md_title": best[2].title if best else "",
                "all_matches": "; ".join(
                    f"{score}:{relative(md.path, repo_root)}" for score, _, md in matches[:10]
                ),
            }
        )
    return rows


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "html_path",
        "html_title",
        "md_match_count",
        "best_score",
        "match_type",
        "best_md_path",
        "best_md_title",
        "all_matches",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan HTML titles and report which ones have matching Markdown files."
    )
    parser.add_argument(
        "--html-root",
        default=".",
        help="Folder or file to scan for .html/.htm files. Default: current folder.",
    )
    parser.add_argument(
        "--md-root",
        action="append",
        required=True,
        help="Folder or file to scan for Markdown. Use this twice for the two places you want checked.",
    )
    parser.add_argument(
        "--output",
        default="html-title-md-report.csv",
        help="CSV output path. Default: html-title-md-report.csv",
    )
    parser.add_argument(
        "--json-output",
        help="Optional JSON output path with the same rows as the CSV.",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=80,
        help="Minimum match score to count as a Markdown match. Default: 80.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden folders/files while scanning.",
    )
    parser.add_argument(
        "--md-max-depth",
        type=int,
        help="Optional max folder depth for Markdown scan roots. Useful for large network drives.",
    )
    parser.add_argument(
        "--md-filename-only",
        action="store_true",
        help="Do not read Markdown contents; match against Markdown filenames only. Useful for large network drives.",
    )
    parser.add_argument(
        "--md-limit",
        type=int,
        help="Optional maximum number of Markdown files to compare after discovery.",
    )
    parser.add_argument(
        "--md-exclude",
        action="append",
        default=[],
        help="Markdown folder/file to exclude. Can be used more than once.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    html_root = Path(args.html_root).resolve()
    md_roots = [Path(root).resolve() for root in args.md_root]
    md_excludes = [Path(path).resolve() for path in args.md_exclude]

    html_files = iter_files(html_root, (".html", ".htm"), args.include_hidden)
    md_files: list[Path] = []
    for md_root in md_roots:
        md_files.extend(
            iter_files(
                md_root,
                (".md", ".markdown", ".mdown"),
                args.include_hidden,
                args.md_max_depth,
                args.md_limit,
                md_excludes,
            )
        )
    md_files = sorted(set(md_files))

    html_pages = [extract_html_title(path) for path in html_files]
    md_pages = [extract_markdown_page(path, args.md_filename_only) for path in md_files]
    rows = build_report(html_pages, md_pages, repo_root, args.min_score)

    output = Path(args.output).resolve()
    write_csv(rows, output)
    if args.json_output:
        json_output = Path(args.json_output).resolve()
        json_output.parent.mkdir(parents=True, exist_ok=True)
        json_output.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    matched = sum(1 for row in rows if row["md_match_count"])
    missing = len(rows) - matched
    print(f"HTML files scanned: {len(html_pages)}")
    print(f"Markdown files scanned: {len(md_pages)}")
    print(f"HTML titles with Markdown matches: {matched}")
    print(f"HTML titles without Markdown matches: {missing}")
    print(f"CSV report: {output}")
    if args.json_output:
        print(f"JSON report: {Path(args.json_output).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
