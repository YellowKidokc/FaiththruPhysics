"""Generate proof-packet HTML pages from a review manifest."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


_DARK_RESET = "<style>html,body{background:#050505;color:#e0e0e0;}</style>"


def _safe_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def _series_index_html(series: str, slugs: list[str]) -> str:
    title = _safe_title(series)
    toc = "\n".join(
        f'<li><a href="./{slug}.html">{_safe_title(slug)}</a></li>'
        for slug in sorted(set(slugs))
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{_DARK_RESET}
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} — Proof Packet</title>
<link rel="canonical" href="https://papers.faiththruphysics.com/{series}/"/>
<script src="https://faiththruphysics.com/site-shell/frame.js" defer></script>
<style>
:root{{--bg:#050505;--surface:#0a0a0a;--border:#222;--text:#e0e0e0;--text-dim:#999;--gold:#d4af37;}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;max-width:900px;margin:0 auto;padding:8rem 1.5rem 6rem;}}
h1{{font-family:'Crimson Text',serif;color:var(--gold);font-weight:400;}}
a{{color:var(--gold);text-decoration:none;}}
ul{{list-style:none;padding:0;}}
li{{padding:.6rem 0;border-bottom:1px solid var(--border);}}
</style>
</head>
<body>
<h1>{title}</h1>
<p>Proof packet containing derived artifacts for this series.</p>
<ul>{toc}</ul>
</body>
</html>"""


def _article_html(series: str, slug: str, artifacts: list[dict]) -> str:
    title = _safe_title(slug)
    by_type: dict[str, list[str]] = {}
    for art in artifacts:
        atype = art.get("artifactType", "unknown")
        by_type.setdefault(atype, []).append(art.get("source", ""))

    sections = []
    if "academic-md" in by_type:
        paths = "\n".join(f"<li>{p}</li>" for p in sorted(set(by_type["academic-md"])))
        sections.append(f"<h2>Academic Version</h2><ul>{paths}</ul><p><em>Embedded markdown rendering TBD in next iteration.</em></p>")
    if "easy-md" in by_type:
        paths = "\n".join(f"<li>{p}</li>" for p in sorted(set(by_type["easy-md"])))
        sections.append(f"<h2>Accessible Version</h2><ul>{paths}</ul><p><em>Embedded markdown rendering TBD in next iteration.</em></p>")
    if "api-json" in by_type:
        paths = "\n".join(f"<li>{p}</li>" for p in sorted(set(by_type["api-json"])))
        sections.append(f"<h2>API Analysis</h2><ul>{paths}</ul><p><em>API rendering TBD in next iteration.</em></p>")
    if "nlp-summary" in by_type:
        paths = "\n".join(f"<li>{p}</li>" for p in sorted(set(by_type["nlp-summary"])))
        sections.append(f"<h2>NLP Summary</h2><ul>{paths}</ul><p><em>Summary rendering TBD.</em></p>")
    body = "\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{_DARK_RESET}
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} — Proof Packet</title>
<link rel="canonical" href="https://papers.faiththruphysics.com/{series}/{slug}.html"/>
<script src="https://faiththruphysics.com/site-shell/frame.js" defer></script>
<style>
:root{{--bg:#050505;--surface:#0a0a0a;--border:#222;--text:#e0e0e0;--text-dim:#999;--gold:#d4af37;}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;max-width:900px;margin:0 auto;padding:8rem 1.5rem 6rem;}}
h1{{font-family:'Crimson Text',serif;color:var(--gold);font-weight:400;}}
h2{{font-family:'Crimson Text',serif;color:var(--text);font-weight:400;border-bottom:1px solid var(--border);padding-bottom:.5rem;}}
a{{color:var(--gold);text-decoration:none;}}
pre{{background:var(--surface);padding:1rem;border:1px solid var(--border);overflow:auto;font-size:.8rem;}}
ul{{list-style:none;padding:0;}}
li{{padding:.4rem 0;border-bottom:1px solid var(--border);font-size:.9rem;}}
</style>
</head>
<body>
<h1>{title}</h1>
<p>Series: <a href="./index.html">{_safe_title(series)}</a> · <a href="https://faiththruphysics.com/{series}/{slug}.html">Main article ↗</a></p>
{body}
</body>
</html>"""


def _landing_html(series_list: list[str]) -> str:
    toc = "\n".join(
        f'<li><a href="./{series}/index.html">{_safe_title(series)}</a></li>'
        for series in sorted(set(series_list))
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{_DARK_RESET}
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Proof Packets — FaithThruPhysics</title>
<link rel="canonical" href="https://papers.faiththruphysics.com/"/>
<script src="https://faiththruphysics.com/site-shell/frame.js" defer></script>
<style>
:root{{--bg:#050505;--surface:#0a0a0a;--border:#222;--text:#e0e0e0;--text-dim:#999;--gold:#d4af37;}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;max-width:900px;margin:0 auto;padding:8rem 1.5rem 6rem;}}
h1{{font-family:'Crimson Text',serif;color:var(--gold);font-weight:400;}}
a{{color:var(--gold);text-decoration:none;}}
ul{{list-style:none;padding:0;}}
li{{padding:.6rem 0;border-bottom:1px solid var(--border);}}
</style>
</head>
<body>
<h1>Proof Packets</h1>
<p>Derived artifacts, academic and accessible versions, and API analyses organized by series.</p>
<ul>{toc}</ul>
</body>
</html>"""


def generate(manifest: dict, website: Path, force: bool = False) -> None:
    target = Path(manifest["targetRoot"])
    target.mkdir(parents=True, exist_ok=True)

    by_series = defaultdict(list)
    for item in manifest["items"]:
        if item.get("action") != "generate":
            continue
        by_series[item["series"]].append(item)

    # landing (always regenerate so new series appear)
    landing_path = target / "index.html"
    landing_path.write_text(_landing_html(list(by_series.keys())), encoding="utf-8")

    for series, items in by_series.items():
        series_dir = target / series
        series_dir.mkdir(parents=True, exist_ok=True)

        by_slug = defaultdict(list)
        for item in items:
            by_slug[item["slug"]].append(item)

        # series index (always regenerate so new slugs appear)
        series_index = series_dir / "index.html"
        series_index.write_text(
            _series_index_html(series, list(by_slug.keys())),
            encoding="utf-8",
        )

        # articles
        for slug, artifacts in by_slug.items():
            article_path = series_dir / f"{slug}.html"
            if force or not article_path.exists():
                article_path.write_text(
                    _article_html(series, slug, artifacts),
                    encoding="utf-8",
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--website", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    generate(manifest, args.website, force=args.force)
    print(f"Generated proof packets under {manifest['targetRoot']}")
