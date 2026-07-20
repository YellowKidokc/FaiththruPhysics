from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".claude",
    "node_modules",
    "_link-fix-backups",
    "backups",
    "_backups",
    "archive",
    "_archive",
    "production-vault",
    "reports",
    "working-notes",
    "scripts",
    "docs",
    "Templates David",
    "MUST DO",
    "Kimi_Agent_ONEPAGE_GLOWINGBALL",
    "prototypes",
}

TEXT_EXTS = {
    ".html",
    ".htm",
}

MAX_TEXT_BYTES = 2_000_000

def replacement_for(match: re.Match[str]) -> str:
    value = match.group(0)
    if value.isupper():
        return "FAITH THROUGH PHYSICS"
    if value.islower():
        return "faith through physics"
    return "Faith Through Physics"


def replace_visible_branding(text: str) -> tuple[str, int]:
    # Standalone word only. This deliberately skips URLs, emails, slugs,
    # filenames, code identifiers, and hyphen/underscore compounds.
    pattern = re.compile(r"(?<![A-Za-z0-9_/@.-])theophysics(?![A-Za-z0-9_/@.-])", re.IGNORECASE)
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        changed += 1
        return replacement_for(match)

    updated = pattern.sub(repl, text)
    return updated, changed


def should_skip(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        return True
    if any("_backup" in part.lower() or "backup" in part.lower() for part in rel_parts):
        return True
    if path.suffix.lower() not in TEXT_EXTS:
        return True
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            return True
    except OSError:
        return True
    if path.name.endswith((".backup", ".bak", ".old", ".orig")):
        return True
    return False


def iter_files() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os_walk(ROOT):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            path = base / filename
            if path.is_file() and not should_skip(path):
                files.append(path)
    return sorted(files)


def os_walk(root: Path):
    import os

    return os.walk(root)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write changes. Default is dry-run.")
    parser.add_argument("--report", default=str(ROOT / "working-notes" / "theophysics_to_faiththroughphysics_report.csv"))
    args = parser.parse_args()

    rows: list[dict[str, str | int]] = []
    total_replacements = 0
    files_changed = 0

    for path in iter_files():
        original = read_text(path)
        if original is None or "theophysics" not in original.lower():
            continue
        updated, count = replace_visible_branding(original)
        if count == 0 or updated == original:
            continue
        files_changed += 1
        total_replacements += count
        rel = str(path.relative_to(ROOT))
        rows.append({"file": rel, "replacements": count})
        if args.apply:
            path.write_text(updated, encoding="utf-8", newline="")

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["file", "replacements"])
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "mode": "apply" if args.apply else "dry-run",
        "root": str(ROOT),
        "files_changed": files_changed,
        "total_replacements": total_replacements,
        "report": str(report_path),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
