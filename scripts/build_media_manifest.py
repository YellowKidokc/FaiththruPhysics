#!/usr/bin/env python3
"""Build the public media manifest and Cloudflare R2/D1 publish plan.

The source vault stays untouched. This script scans the local site-data repo,
dedupes by sha1, assigns stable R2 object keys, and can emit companion scripts
for staging web-ready media, uploading to R2, and registering audio tracks in D1.
"""

from __future__ import annotations

import argparse
import html
import hashlib
import json
import mimetypes
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
DOCUMENT_EXTS = {".pdf"}
IMAGE_EXTS = {".png", ".webp", ".jpg", ".jpeg"}
MEDIA_EXTS = AUDIO_EXTS | VIDEO_EXTS | DOCUMENT_EXTS | IMAGE_EXTS

CANONICAL_SERIES = {
    "axiom-layer": "axiom-layer",
    "axiom layer": "axiom-layer",
    "blue": "blue",
    "breakdown-and-coherence": "breakdown-and-coherence",
    "consciousness": "consciousness",
    "convergence-deep": "convergence-deep",
    "convergence-series": "convergence-series",
    "cross-domain": "cross-domain",
    "formal-papers": "formal-papers",
    "genesis-to-quantum": "genesis-to-quantum",
    "gtq": "genesis-to-quantum",
    "isomorphism": "isomorphism",
    "master-equation": "master-equation",
    "mda": "mda",
    "moral-decline": "mda",
    "one-page-stories": "one-page-stories",
    "one-pagers": "one-page-stories",
    "podcast": "podcast",
    "proof-architecture": "proof-architecture",
    "proof-explorer": "proof-explorer",
    "revolution-of-truth": "revolution-of-truth",
    "three-gates": "three-gates",
    "three-truths": "three-truths",
}

MODE_PATTERNS = [
    ("deep", re.compile(r"^DD-", re.I)),
    ("podcast", re.compile(r"^D-", re.I)),
    ("critique", re.compile(r"^C-", re.I)),
    ("read", re.compile(r"^AT-", re.I)),
]


@dataclass(frozen=True)
class SiteSlug:
    slug: str
    series: str
    path: str
    title: str


def slugify(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "media"


def title_from_path(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"__(DD|SD|VO|TTS|WEB)__", " - ", stem, flags=re.I)
    stem = re.sub(r"[-_]+", " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem.title() if stem else path.name


def media_kind(ext: str) -> str:
    ext = ext.lower()
    if ext in AUDIO_EXTS:
        return "audio"
    if ext in VIDEO_EXTS:
        return "video"
    if ext in DOCUMENT_EXTS:
        return "document"
    return "image"


def target_extension(kind: str, ext: str) -> str:
    ext = ext.lower()
    if kind == "audio":
        return ext if ext in {".mp3", ".m4a"} else ".mp3"
    if kind == "video":
        return ".mp4"
    if kind == "image":
        return ext if ext in {".png", ".webp"} else ".webp"
    return ".pdf"


def page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader  # type: ignore

        return len(PdfReader(str(path)).pages)
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["pdfinfo", str(path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.M)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return 0


def fingerprint(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_part(part: str) -> str:
    return slugify(part.replace("_", "-"))


def infer_series(rel: str) -> str:
    parts = [norm_part(part) for part in Path(rel).parts]
    joined = "/".join(parts)
    if "the-moral-decay-of-america-project" in parts or "moral-decline" in parts:
        return "mda"
    if "cng" in parts:
        return "convergence-series"
    if "genesis-to-quantum" in parts:
        return "genesis-to-quantum"
    if "articles" in parts and re.search(r"(^|/)0?\d+-", joined):
        return "genesis-to-quantum"
    if "papers" in parts or "formal-papers" in parts:
        return "formal-papers"
    if "notebooklm" in parts and "one-page-stories" in parts:
        return "one-page-stories"
    for part in parts:
        if part in CANONICAL_SERIES:
            return CANONICAL_SERIES[part]
    if "/cng/" in f"/{joined}/":
        return "convergence-series"
    if re.search(r"(^|/)gtq[-_ ]?\d+", joined):
        return "genesis-to-quantum"
    if re.search(r"(^|/)mda[-_ ]?\d+", joined):
        return "mda"
    return parts[0] if parts else "uncategorized"


def infer_mode(rel: str, kind: str) -> str | None:
    if kind != "audio":
        return None
    text = Path(rel.replace("\\", "/")).name
    for mode, pattern in MODE_PATTERNS:
        if pattern.search(text):
            return mode
    return None


def strip_mode_tokens(value: str) -> str:
    value = re.sub(r"^(AT|DD|D|C)-", "", value, flags=re.I)
    value = re.sub(r"__(DD|SD|VO|TTS|WEB)__", "-", value, flags=re.I)
    value = re.sub(r"\b(deep[-_ ]?dive|debate|critique|tts|voice|vo|read[-_ ]?aloud|narrated|full[-_ ]?read|audio|video)\b", "-", value, flags=re.I)
    value = re.sub(r"\b(mp3|m4a|mp4|pdf|webp|png)\b", "-", value, flags=re.I)
    return slugify(value)


def candidate_slug_from_path(rel: str, series: str) -> str:
    parts = [part for part in Path(rel).parts]
    stem = Path(rel).stem
    joined = "/".join(parts).lower()

    gtq_match = re.search(r"(gtq[-_ ]?\d+[a-z]?)[-_ ]+(.*?)(?:/|$)", joined)
    if gtq_match:
        prefix = slugify(gtq_match.group(1))
        tail = strip_mode_tokens(gtq_match.group(2))
        return slugify(f"{prefix}-{tail}") if tail else prefix

    mda_match = re.search(r"(mda[-_ ]?\d+)[-_ ]+(.*?)(?:/|$)", joined)
    if mda_match:
        prefix = slugify(mda_match.group(1))
        tail = strip_mode_tokens(mda_match.group(2))
        return slugify(f"{prefix}-{tail}") if tail else prefix

    if "notebooklm" in [part.lower() for part in parts]:
        idx = [part.lower() for part in parts].index("notebooklm")
        if idx + 1 < len(parts):
            return slugify(parts[idx + 1])

    cleaned = strip_mode_tokens(stem)
    if re.fullmatch(r"(00-)?(index|links|readme|master-index|media)", cleaned) and len(parts) > 1:
        context = [strip_mode_tokens(part) for part in parts[-4:-1]]
        context = [part for part in context if part and part not in {"audio", "video", "assets", "media"}]
        cleaned = slugify("-".join(context + [cleaned])) if context else strip_mode_tokens(parts[-2])
    if series and cleaned.startswith(series):
        return cleaned
    return cleaned


def load_site_slugs(site_root: Path | None) -> list[SiteSlug]:
    if not site_root or not site_root.exists():
        return []
    slugs: list[SiteSlug] = []
    title_re = re.compile(r"<title>(.*?)</title>", re.I | re.S)
    attr_re = re.compile(r"data-audio-slug\s*=\s*['\"]([^'\"]+)['\"]", re.I)
    for path in site_root.rglob("*.html"):
        if any(part.startswith(".") for part in path.relative_to(site_root).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = path.relative_to(site_root).as_posix()
        series = infer_series(rel)
        title_match = title_re.search(text)
        title = html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else path.stem
        attr_match = attr_re.search(text)
        if attr_match:
            slugs.append(SiteSlug(slugify(attr_match.group(1)), series, rel, title))
        fallback = slugify(path.stem if path.stem.lower() != "index" else path.parent.name)
        slugs.append(SiteSlug(fallback, series, rel, title))
    unique: dict[tuple[str, str], SiteSlug] = {}
    for item in slugs:
        unique[(item.series, item.slug)] = item
    return list(unique.values())


def choose_site_slug(candidate: str, series: str, site_slugs: list[SiteSlug]) -> tuple[str, str, str, str]:
    if not site_slugs:
        return candidate, series, "path", ""
    exact = [s for s in site_slugs if s.series == series and s.slug == candidate]
    if exact:
        return exact[0].slug, exact[0].series, "site-exact", exact[0].path
    starts = [s for s in site_slugs if s.series == series and (candidate.startswith(s.slug) or s.slug.startswith(candidate))]
    if len(starts) == 1:
        return starts[0].slug, starts[0].series, "site-prefix", starts[0].path
    global_exact = [s for s in site_slugs if s.slug == candidate]
    if len(global_exact) == 1:
        return global_exact[0].slug, global_exact[0].series, "site-global", global_exact[0].path
    global_prefix = [s for s in site_slugs if candidate.startswith(s.slug) or s.slug.startswith(candidate)]
    if len(global_prefix) == 1:
        return global_prefix[0].slug, global_prefix[0].series, "site-global-prefix", global_prefix[0].path
    return candidate, series, "path", ""


def r2_key_for(kind: str, series: str, slug: str, mode: str | None, filename_slug: str, target_ext: str) -> str:
    if kind == "audio":
        return f"audio/{series}/{slug}/{mode or 'needs-assignment'}{target_ext}"
    if kind == "video":
        return f"video/{series}/{slug}/web.mp4"
    if kind == "document":
        return f"documents/{series}/{slug}/{filename_slug}.pdf"
    return f"images/{series}/{slug}/{filename_slug}{target_ext}"


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def sql_quote(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def make_item(
    path: Path,
    root: Path,
    site_root: Path | None,
    site_slugs: list[SiteSlug],
    public_base: str | None,
    include_local_paths: bool,
    stage_root: Path,
) -> dict:
    rel = path.relative_to(root).as_posix()
    stat = path.stat()
    ext = path.suffix.lower()
    kind = media_kind(ext)
    series = infer_series(rel)
    mode = infer_mode(rel, kind)
    candidate_slug = candidate_slug_from_path(rel, series)
    slug, series, slug_source, matched_page = choose_site_slug(candidate_slug, series, site_slugs)
    target_ext = target_extension(kind, ext)
    filename_slug = strip_mode_tokens(path.stem)
    r2_key = r2_key_for(kind, series, slug, mode, filename_slug, target_ext)
    public_url = f"{public_base.rstrip('/')}/{r2_key}" if public_base else None
    available_on_site = bool(site_root and (site_root / rel).exists())
    needs_derivative = ext != target_ext or kind in {"audio", "video"}
    stage_path = stage_root / Path(r2_key)
    confidence = "high" if slug_source.startswith("site") or any(part in rel.lower() for part in [series, slug]) else "medium"

    item = {
        "id": slugify(r2_key),
        "title": title_from_path(path),
        "kind": kind,
        "series": series,
        "slug": slug,
        "slugSource": slug_source,
        "slugConfidence": confidence,
        "mode": mode,
        "extension": ext.lstrip("."),
        "targetExtension": target_ext.lstrip("."),
        "relativePath": rel,
        "r2Key": r2_key,
        "publicUrl": public_url,
        "availableOnSite": available_on_site,
        "matchedSitePage": matched_page or None,
        "mimeType": mimetypes.guess_type(f"file{target_ext}")[0] or mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "sourceMimeType": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "sizeBytes": stat.st_size,
        "modifiedUtc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "tags": sorted({part.lower() for part in path.relative_to(root).parts[:-1] if part}),
        "sha1": fingerprint(path),
        "needsDerivative": needs_derivative,
        "stagePath": str(stage_path),
    }
    if include_local_paths:
        item["sourcePath"] = str(path)
    return item


def make_pdf_page_items(document_item: dict, pdf_path: Path, include_local_paths: bool, public_base: str | None, stage_root: Path) -> list[dict]:
    pages = page_count(pdf_path)
    if pages <= 0:
        document_item.setdefault("publishNotes", []).append("pdf page count unavailable; no page images emitted")
        return []

    items: list[dict] = []
    series = document_item["series"]
    slug = document_item["slug"]
    source_sha = document_item["sha1"]
    for index in range(1, pages + 1):
        page_name = f"page-{index:03d}"
        r2_key = f"images/{series}/{slug}/pdf-pages/{page_name}.webp"
        stage_path = stage_root / Path(r2_key)
        item = {
            "id": slugify(r2_key),
            "title": f"{document_item['title']} - Page {index}",
            "kind": "image",
            "series": series,
            "slug": slug,
            "slugSource": document_item["slugSource"],
            "slugConfidence": document_item["slugConfidence"],
            "mode": "pdf-page",
            "extension": "pdf",
            "targetExtension": "webp",
            "relativePath": f"{document_item['relativePath']}#page={index}",
            "r2Key": r2_key,
            "publicUrl": f"{public_base.rstrip('/')}/{r2_key}" if public_base else None,
            "availableOnSite": False,
            "matchedSitePage": document_item.get("matchedSitePage"),
            "mimeType": "image/webp",
            "sourceMimeType": "application/pdf",
            "sizeBytes": 0,
            "modifiedUtc": document_item["modifiedUtc"],
            "tags": sorted(set(document_item["tags"] + ["pdf-page", f"page-{index:03d}"])),
            "sha1": f"{source_sha}-page-{index:03d}",
            "needsDerivative": True,
            "stagePath": str(stage_path),
            "sourceDocumentPath": document_item["relativePath"],
            "sourceDocumentR2Key": document_item["r2Key"],
            "pageNumber": index,
            "pageCount": pages,
        }
        if include_local_paths and document_item.get("sourcePath"):
            item["sourcePath"] = document_item["sourcePath"]
        items.append(item)

    document_item["derivedPageCount"] = pages
    document_item["derivedWebpPages"] = [item["r2Key"] for item in items]
    return items


def score_path(rel: str) -> int:
    score = 0
    parts = rel.lower().split("/")
    if parts and parts[0] == "assets":
        score += 20
    if "audio" in parts:
        score += 10
    if "video" in parts:
        score += 8
    if "mda" in parts:
        score += 5
    if "_archive" in parts:
        score -= 12
    if "flat-legacy" in parts:
        score -= 10
    score -= rel.count("/")
    return score


def dedupe_items(items: list[dict]) -> list[dict]:
    chosen: dict[str, dict] = {}
    for item in items:
        key = item["sha1"]
        current = chosen.get(key)
        if current is None or score_path(item["relativePath"]) > score_path(current["relativePath"]):
            chosen[key] = item
    return sorted(chosen.values(), key=lambda x: (x["kind"], x["series"], x["slug"], x["mode"] or "", x["title"]))


def with_suffix_before_ext(key: str, suffix: str) -> str:
    path = Path(key)
    return str(path.with_name(f"{path.stem}-{suffix}{path.suffix}")).replace("\\", "/")


def resolve_publish_collisions(items: list[dict]) -> None:
    r2_seen: dict[str, dict] = {}
    slug_mode_seen: dict[tuple[str, str], dict] = {}
    for item in items:
        r2_key = item["r2Key"]
        previous = r2_seen.get(r2_key)
        if previous and previous["sha1"] != item["sha1"]:
            item["r2Key"] = with_suffix_before_ext(r2_key, item["sha1"][:8])
            item["publicUrl"] = item["publicUrl"].rsplit("/", 1)[0] + "/" + Path(item["r2Key"]).name if item.get("publicUrl") else None
            item["id"] = slugify(item["r2Key"])
            item["stagePath"] = str(Path(item["stagePath"]).with_name(Path(item["r2Key"]).name))
            item.setdefault("publishNotes", []).append(f"r2 key disambiguated from {r2_key}")
        r2_seen[item["r2Key"]] = item

        if item["kind"] != "audio":
            continue
        slug_mode = (item["series"], item["slug"], item["mode"] or "needs-assignment")
        previous_audio = slug_mode_seen.get(slug_mode)
        if previous_audio and previous_audio["sha1"] != item["sha1"]:
            old_slug = item["slug"]
            item["slug"] = slugify(f"{old_slug}-{item['sha1'][:8]}")
            item["r2Key"] = item["r2Key"].replace(f"/{old_slug}/", f"/{item['slug']}/")
            if item.get("publicUrl"):
                item["publicUrl"] = item["publicUrl"].replace(f"/{old_slug}/", f"/{item['slug']}/")
            item["stagePath"] = item["stagePath"].replace(f"\\{old_slug}\\", f"\\{item['slug']}\\").replace(f"/{old_slug}/", f"/{item['slug']}/")
            item["id"] = slugify(item["r2Key"])
            item.setdefault("publishNotes", []).append(f"audio slug/mode disambiguated from {old_slug}/{slug_mode[2]}")
            slug_mode = (item["series"], item["slug"], item["mode"] or "needs-assignment")
        slug_mode_seen[slug_mode] = item


def find_exceptions(items: list[dict]) -> list[dict]:
    exceptions: list[dict] = []
    r2_seen: dict[str, dict] = {}
    for item in items:
        reasons: list[str] = []
        previous = r2_seen.get(item["r2Key"])
        if previous and previous["sha1"] != item["sha1"]:
            reasons.append(f"r2-key-collision:{previous['relativePath']}")
        else:
            r2_seen[item["r2Key"]] = item
        if item["slugConfidence"] != "high":
            reasons.append("slug-not-confirmed-by-site-page")
        if reasons:
            exceptions.append({
                "relativePath": item["relativePath"],
                "kind": item["kind"],
                "series": item["series"],
                "slug": item["slug"],
                "mode": item["mode"],
                "r2Key": item["r2Key"],
                "reasons": reasons,
            })
    return exceptions


def build_manifest(
    data_root: Path,
    site_root: Path | None,
    public_base: str | None,
    include_local_paths: bool,
    stage_root: Path,
) -> dict:
    site_slugs = load_site_slugs(site_root)
    files = [
        path
        for path in data_root.rglob("*")
        if path.is_file() and path.suffix.lower() in MEDIA_EXTS
    ]
    raw_items = [
        make_item(path, data_root, site_root, site_slugs, public_base, include_local_paths, stage_root)
        for path in files
    ]
    items = dedupe_items(raw_items)
    path_by_rel = {path.relative_to(data_root).as_posix(): path for path in files}
    pdf_page_items: list[dict] = []
    for item in items:
        if item["kind"] == "document" and item["extension"] == "pdf":
            pdf_path = path_by_rel.get(item["relativePath"])
            if pdf_path:
                pdf_page_items.extend(make_pdf_page_items(item, pdf_path, include_local_paths, public_base, stage_root))
    items.extend(pdf_page_items)
    resolve_publish_collisions(items)
    exceptions = find_exceptions(items)
    counts: dict[str, int] = {}
    bytes_by_kind: dict[str, int] = {}
    for item in items:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
        bytes_by_kind[item["kind"]] = bytes_by_kind.get(item["kind"], 0) + item["sizeBytes"]
    return {
        "schema": "faiththruphysics.media-manifest.v2",
        "generatedUtc": datetime.now(timezone.utc).isoformat(),
        "dataRoot": str(data_root),
        "siteRoot": str(site_root) if site_root else None,
        "publicBaseUrl": public_base,
        "stageRoot": str(stage_root),
        "totalItems": len(items),
        "rawItemsBeforeDedupe": len(raw_items),
        "siteSlugsDiscovered": len(site_slugs),
        "counts": counts,
        "bytesByKind": bytes_by_kind,
        "exceptionCount": len(exceptions),
        "items": items,
        "exceptions": exceptions,
    }


def emit_stage_script(manifest: dict, output: Path) -> None:
    bundled_bin = r"C:\Users\David\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin"
    bundled_pdftoppm = r"C:\Users\David\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe"
    bundled_python = r"C:\Users\David\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    pdf_groups: dict[str, dict] = {}
    for item in manifest["items"]:
        if item["kind"] == "image" and item.get("mode") == "pdf-page":
            source = item.get("sourcePath")
            if not source:
                continue
            group = pdf_groups.setdefault(source, {
                "source": source,
                "pngDir": str(Path(item["stagePath"]).parents[0] / "png"),
                "webpDir": str(Path(item["stagePath"]).parent),
            })
            group["webpDir"] = str(Path(item["stagePath"]).parent)

    lines = [
        "# Generated by scripts/build_media_manifest.py",
        "# Creates web-ready staged files without changing the source vault.",
        "param([switch]$PdfOnly)",
        "$ErrorActionPreference = 'Stop'",
        f"$bundledBin = {shell_quote(bundled_bin)}",
        f"$bundledPdftoppm = {shell_quote(bundled_pdftoppm)}",
        f"$bundledPython = {shell_quote(bundled_python)}",
        "$pdftoppm = Get-Command pdftoppm -ErrorAction SilentlyContinue",
        "if ((Test-Path $bundledPdftoppm)) { $pdftoppm = Get-Item $bundledPdftoppm }",
        "if (-not $pdftoppm -and (Test-Path (Join-Path $bundledBin 'pdftoppm.cmd'))) { $pdftoppm = Get-Item (Join-Path $bundledBin 'pdftoppm.cmd') }",
        "$python = Get-Command python -ErrorAction SilentlyContinue",
        "if ((Test-Path $bundledPython)) { $python = Get-Item $bundledPython }",
        "if (-not $pdftoppm) { throw 'pdftoppm is required for PDF page rendering. Install Poppler or use the bundled Codex runtime.' }",
        "if (-not $python) { throw 'Python with Pillow is required for PNG to WebP conversion.' }",
        "$pdftoppmPath = if ($pdftoppm.Source) { $pdftoppm.Source } else { $pdftoppm.FullName }",
        "$pythonPath = if ($python.Source) { $python.Source } else { $python.FullName }",
        "$webpHelper = Join-Path $PSScriptRoot 'convert-image-to-webp.py'",
        "@'",
        "from PIL import Image",
        "import sys",
        "src, dst = sys.argv[1], sys.argv[2]",
        "im = Image.open(src)",
        "if im.mode not in ('RGB', 'RGBA'):",
        "    im = im.convert('RGB')",
        "im.save(dst, 'WEBP', quality=82, method=6)",
        "'@ | Set-Content -LiteralPath $webpHelper -Encoding UTF8",
        "",
        "function Convert-PdfToWebpPages {",
        "  param([string]$SourcePdf, [string]$PngDir, [string]$WebpDir)",
        "  New-Item -ItemType Directory -Force -Path $PngDir | Out-Null",
        "  New-Item -ItemType Directory -Force -Path $WebpDir | Out-Null",
        "  Remove-Item -LiteralPath (Join-Path $PngDir '*.png') -ErrorAction SilentlyContinue",
        "  $prefix = Join-Path $PngDir 'page'",
        "  & $pdftoppmPath -r 160 -png $SourcePdf $prefix",
        "  $pngs = Get-ChildItem -LiteralPath $PngDir -Filter 'page-*.png' | Sort-Object Name",
        "  $i = 1",
        "  foreach ($png in $pngs) {",
        "    $webp = Join-Path $WebpDir ('page-{0:D3}.webp' -f $i)",
        "    & $pythonPath $webpHelper $png.FullName $webp",
        "    $i += 1",
        "  }",
        "}",
        "",
    ]
    for group in sorted(pdf_groups.values(), key=lambda value: value["source"]):
        lines.append(f"Convert-PdfToWebpPages -SourcePdf {shell_quote(group['source'])} -PngDir {shell_quote(group['pngDir'])} -WebpDir {shell_quote(group['webpDir'])}")
    lines.extend([
        "if ($PdfOnly) { return }",
        "$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue",
        "if (-not $ffmpeg) { throw 'ffmpeg is required for audio/video staging. Install ffmpeg or add it to PATH.' }",
        "",
    ])

    for item in manifest["items"]:
        if item["kind"] == "image" and item.get("mode") == "pdf-page":
            continue
        src = item.get("sourcePath")
        if not src:
            continue
        dest = item["stagePath"]
        lines.append(f"New-Item -ItemType Directory -Force -Path {shell_quote(str(Path(dest).parent))} | Out-Null")
        if item["kind"] == "audio":
            if item["targetExtension"] == "mp3":
                lines.append(f"& $ffmpeg.Source -hide_banner -y -i {shell_quote(src)} -vn -map_metadata 0 -af loudnorm=I=-16:TP=-1.5:LRA=11 -codec:a libmp3lame -b:a 96k {shell_quote(dest)}")
            else:
                lines.append(f"& $ffmpeg.Source -hide_banner -y -i {shell_quote(src)} -vn -map_metadata 0 -af loudnorm=I=-16:TP=-1.5:LRA=11 -codec:a aac -b:a 96k {shell_quote(dest)}")
        elif item["kind"] == "video":
            lines.append(f"& $ffmpeg.Source -hide_banner -y -i {shell_quote(src)} -map_metadata 0 -vf scale='min(1280,iw)':-2 -codec:v libx264 -crf 24 -preset medium -codec:a aac -b:a 128k -movflags +faststart {shell_quote(dest)}")
        else:
            lines.append(f"Copy-Item -LiteralPath {shell_quote(src)} -Destination {shell_quote(dest)} -Force")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit_upload_script(manifest: dict, output: Path, bucket: str) -> None:
    lines = [
        "# Generated by scripts/build_media_manifest.py",
        "# Run after the staging script. Uploads staged web-ready files to Cloudflare R2.",
        "$ErrorActionPreference = 'Stop'",
        "",
    ]
    for item in manifest["items"]:
        lines.append(
            "wrangler r2 object put "
            + f"{bucket}/{item['r2Key']} "
            + f"--file {shell_quote(item['stagePath'])} "
            + f"--content-type {shell_quote(item['mimeType'])}"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit_d1_sql(manifest: dict, output: Path) -> None:
    rows = [item for item in manifest["items"] if item["kind"] == "audio" and item.get("publicUrl") and item.get("mode")]
    lines = [
        "-- Generated by scripts/build_media_manifest.py",
        "-- Register R2-hosted audio tracks for the faith-audio-pipeline Worker.",
        "BEGIN TRANSACTION;",
    ]
    for item in rows:
        columns = [
            "article_slug",
            "series",
            "mode",
            "url",
            "title",
            "file_size_bytes",
            "r2_key",
            "is_default",
            "updated_at",
        ]
        values = [
            f"{item['series']}/{item['slug']}",
            item["series"],
            item["mode"],
            item["publicUrl"],
            item["title"],
            item["sizeBytes"],
            item["r2Key"],
            1 if item.get("mode") == "read" else 0,
            datetime.now(timezone.utc).isoformat(),
        ]
        lines.append(
            "INSERT INTO audio_tracks ("
            + ", ".join(columns)
            + ") VALUES ("
            + ", ".join(sql_quote(v) for v in values)
            + ") ON CONFLICT(article_slug, mode) DO UPDATE SET "
            + "series = excluded.series, url = excluded.url, title = excluded.title, "
            + "file_size_bytes = excluded.file_size_bytes, r2_key = excluded.r2_key, "
            + "is_default = excluded.is_default, updated_at = excluded.updated_at;"
        )
    lines.append("COMMIT;")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit_exceptions(manifest: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest["exceptions"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def public_manifest_copy(manifest: dict, include_local_paths: bool) -> dict:
    if include_local_paths:
        return manifest
    public_manifest = json.loads(json.dumps(manifest))
    for item in public_manifest["items"]:
        item.pop("sourcePath", None)
    return public_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default=r"D:\GitHub\faiththruphysics-site-data", help="Local source vault to scan.")
    parser.add_argument("--output", default=r"D:\GitHub\faiththruphysics-site\assets\media-manifest.json", help="Manifest JSON path to write inside the site repo.")
    parser.add_argument("--site-root", default=r"D:\GitHub\faiththruphysics-site", help="Deployable site root for discovering data-audio-slug values.")
    parser.add_argument("--public-base-url", default="https://r2.faiththruphysics.com", help="R2/custom-domain base URL for published media.")
    parser.add_argument("--stage-root", default=r"D:\GitHub\faiththruphysics-site\work\r2-media-stage", help="Ignored staging root for web-ready derivatives.")
    parser.add_argument("--include-local-paths", action="store_true", help="Include absolute source paths in the public manifest.")
    parser.add_argument("--emit-stage-script", default=r"D:\GitHub\faiththruphysics-site\work\prepare-r2-media.ps1", help="PowerShell script path for derivative staging.")
    parser.add_argument("--emit-upload-script", default=r"D:\GitHub\faiththruphysics-site\work\upload-r2-media.ps1", help="PowerShell script path for R2 uploads.")
    parser.add_argument("--emit-d1-sql", default=r"D:\GitHub\faiththruphysics-site\work\register-audio-tracks.sql", help="D1 SQL upsert file for audio_tracks.")
    parser.add_argument("--emit-exceptions", default=r"D:\GitHub\faiththruphysics-site\work\media-publish-exceptions.json", help="JSON report for ambiguous/colliding media.")
    parser.add_argument("--bucket", default="faiththruphysics-audio", help="Cloudflare R2 bucket name.")
    parser.add_argument("--no-exports", action="store_true", help="Only write the manifest.")
    args = parser.parse_args()

    data_root = Path(args.data_root).resolve()
    output = Path(args.output).resolve()
    site_root = Path(args.site_root).resolve() if args.site_root else None
    stage_root = Path(args.stage_root).resolve()
    if not data_root.exists():
        raise SystemExit(f"Data root not found: {data_root}")

    manifest_with_paths = build_manifest(
        data_root=data_root,
        site_root=site_root,
        public_base=args.public_base_url.strip() or None,
        include_local_paths=True,
        stage_root=stage_root,
    )
    manifest = public_manifest_copy(manifest_with_paths, args.include_local_paths)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not args.no_exports:
        emit_stage_script(manifest_with_paths, Path(args.emit_stage_script).resolve())
        emit_upload_script(manifest_with_paths, Path(args.emit_upload_script).resolve(), args.bucket)
        emit_d1_sql(manifest, Path(args.emit_d1_sql).resolve())
        emit_exceptions(manifest, Path(args.emit_exceptions).resolve())

    print(f"Wrote {manifest['totalItems']} media items to {output}")
    print(f"Raw files before dedupe: {manifest['rawItemsBeforeDedupe']}")
    print(f"Site slugs discovered: {manifest['siteSlugsDiscovered']}")
    print(f"Exceptions requiring review: {manifest['exceptionCount']}")
    print(json.dumps(manifest["counts"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
