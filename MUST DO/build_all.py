#!/usr/bin/env python3
"""
BUILD_ALL

One-command orchestrator for the HTML workflow.

The runner is intentionally conservative:
- prechecks run first
- the Math Translation Layer is checked during preflight
- each step is executed in order
- missing scripts are reported clearly
- the final report separates what we got right, what failed, and what is missing
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / "MUST DO" / "workflows"
REPORT_DIR = REPO_ROOT / "work" / "pipeline-reports"
MTL_DIR = REPO_ROOT / "MUST DO" / "math-translation-layer"

DEFAULT_CORE_STEPS = [
    {"name": "precheck", "kind": "builtin", "required": True},
    {"name": "canonical_gate", "kind": "builtin", "required": True},
    {
        "name": "classify_html",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/classify_html.py",
            "scripts/classify_html.py",
        ],
    },
    {
        "name": "stamp_shell",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/stamp_shell.py",
        ],
    },
    {
        "name": "inject_footer",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/inject_footer.py",
        ],
    },
    {
        "name": "inject_player",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/inject_player.py",
            "mda/inject_mtl_bar.py",
        ],
    },
    {
        "name": "wire_canonical_navigation",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/wire_canonical_navigation.py",
        ],
    },
    {
        "name": "wire_unified_media_players",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/wire_unified_media_players.py",
            "mda/cleanup_and_rebuild_bars.py",
        ],
    },
    {
        "name": "add_rigor_audits_to_html",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/add_rigor_audits_to_html.py",
        ],
    },
    {
        "name": "build_glossary",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/build_glossary.py",
            "glossary-linker.js",
        ],
    },
    {"name": "postcheck", "kind": "builtin", "required": True},
]

DEFAULT_SERIES_STEPS = {
    "mda": [
        {
            "name": "mda_audit_repair",
            "kind": "external",
            "required": False,
            "candidates": [
                "mda/cleanup_and_rebuild_bars.py",
                "mda/inject_mtl_bar.py",
                "mda/reposition_mtl_bar.py",
            ],
        },
        {
            "name": "fix_gtq_audio",
            "kind": "external",
            "required": False,
            "candidates": [
                "MUST DO/fix_gtq_audio.py",
            ],
        },
        {
            "name": "patch_series_polish_gaps",
            "kind": "external",
            "required": False,
            "candidates": [
                "MUST DO/patch_series_polish_gaps.py",
            ],
        },
    ],
    "gtq": [
        {
            "name": "fix_gtq_audio",
            "kind": "external",
            "required": False,
            "candidates": [
                "MUST DO/fix_gtq_audio.py",
            ],
        },
        {
            "name": "patch_series_polish_gaps",
            "kind": "external",
            "required": False,
            "candidates": [
                "MUST DO/patch_series_polish_gaps.py",
            ],
        },
    ],
}

DEFAULT_DEPLOY_STEPS = [
    {
        "name": "build_site",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/build_site.py",
            "BUILD_SITE.ps1",
        ],
    },
    {
        "name": "assemble_deploy",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/assemble_deploy.py",
        ],
    },
    {
        "name": "deploy_to_github",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/deploy_to_github.py",
            "wrangler pages deploy .",
        ],
    },
]

DEFAULT_CONVERT_STEPS = [
    {
        "name": "convert_html_to_clean_markdown",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/convert_html_to_clean_markdown.py",
        ],
    },
    {
        "name": "convert_canonical_html_to_tts_markdown",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/convert_canonical_html_to_tts_markdown.py",
        ],
    },
]

DEFAULT_MAINTENANCE_STEPS = [
    {
        "name": "toolbox_janitor",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/toolbox_janitor.py",
        ],
    },
    {
        "name": "dedup_html_master",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/dedup_html_master.py",
        ],
    },
    {
        "name": "scan_audio",
        "kind": "external",
        "required": False,
        "candidates": [
            "MUST DO/scan_audio.py",
        ],
    },
]

MTL_REQUIRED_FILES = [
    MTL_DIR / "site-shell.js",
    MTL_DIR / "mtl-overlay.js",
    MTL_DIR / "mtl-overlay-loader.js",
    MTL_DIR / "mtl-equation.js",
    MTL_DIR / "mtl-reader-bar.html",
]

FORBIDDEN_TARGET_MARKERS = [
    "_archive",
    "codex-delete",
    "production-vault",
    "_built",
]


@dataclass
class StepResult:
    name: str
    status: str
    detail: str = ""
    command: str = ""
    returncode: Optional[int] = None


def load_workflow(name: str, fallback: list[dict]) -> list[dict]:
    path = WORKFLOWS_DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8")).get("steps", fallback)
    return fallback


def normalize_target(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    return path


def iter_html_targets(target: Path) -> Iterable[Path]:
    if target.is_file():
        if target.suffix.lower() == ".html":
            yield target
        return
    if target.is_dir():
        yield from sorted(target.rglob("*.html"))


def print_header(title: str) -> None:
    print()
    print("=" * 76)
    print(title)
    print("=" * 76)


def builtin_precheck(targets: list[Path]) -> tuple[bool, str, list[str]]:
    messages: list[str] = []
    if not MTL_DIR.exists():
        messages.append(f"MTL folder missing: {MTL_DIR}")
    else:
        messages.append("MTL workspace found.")

    missing_mtl = [str(path) for path in MTL_REQUIRED_FILES if not path.exists()]
    if missing_mtl:
        messages.append("Missing MTL assets:")
        messages.extend(f"  - {item}" for item in missing_mtl)
    else:
        messages.append("MTL core assets present.")

    html_targets = [path for target in targets for path in iter_html_targets(target)]
    if not html_targets:
        messages.append("No HTML targets found.")
        return False, "Precheck failed: no HTML targets.", messages

    messages.append(f"HTML targets found: {len(html_targets)}")
    return True, "Precheck passed.", messages


def builtin_canonical_gate(targets: list[Path]) -> tuple[bool, str, list[str]]:
    issues: list[str] = []
    for target in targets:
        text = str(target).lower().replace("/", "\\")
        for marker in FORBIDDEN_TARGET_MARKERS:
            if marker in text:
                issues.append(f"Target is in a non-canonical area: {target}")
                break
    if issues:
        return False, "Canonical gate failed.", issues
    return True, "Canonical gate passed.", ["Target paths look canonical."]


def builtin_postcheck(targets: list[Path]) -> tuple[bool, str, list[str]]:
    html_targets = [path for target in targets for path in iter_html_targets(target)]
    messages = [f"HTML files reviewed: {len(html_targets)}"]
    if not html_targets:
        return False, "Postcheck failed: nothing to review.", messages

    # Lightweight checks that keep the runner honest even when the specialized
    # rewrite scripts are not present yet.
    missing_title = 0
    missing_mtl_refs = 0
    overstated_pages = 0
    for html_path in html_targets:
        text = html_path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        if "<title>" not in lower or "<h1" not in lower:
            missing_title += 1
        if ("math" in lower or "equation" in lower) and "mtl" not in lower:
            missing_mtl_refs += 1
        if any(
            phrase in lower
            for phrase in (
                "what we overstated",
                "overstated",
                "carried away",
                "too strong",
                "less sure",
            )
        ):
            overstated_pages += 1

    if missing_title:
        messages.append(f"Pages missing title or H1 markers: {missing_title}")
    if missing_mtl_refs:
        messages.append(f"Pages with math cues but no MTL markers: {missing_mtl_refs}")
    if overstated_pages:
        messages.append(f"Pages carrying overstated or hedge language: {overstated_pages}")

    return True, "Postcheck completed.", messages


def run_external(candidate: str, targets: list[Path], dry_run: bool) -> tuple[bool, str, str, Optional[int]]:
    candidate_path = (REPO_ROOT / candidate).resolve()
    if candidate_path.exists():
        if dry_run:
            return True, f"Would run {candidate_path}", str(candidate_path), None

        if candidate_path.suffix.lower() == ".py":
            command = [sys.executable, str(candidate_path), *[str(t) for t in targets]]
            proc = subprocess.run(command, cwd=REPO_ROOT)
            return proc.returncode == 0, f"Ran {candidate_path}", " ".join(command), proc.returncode

        if candidate_path.suffix.lower() == ".ps1":
            command = [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(candidate_path),
                *[str(t) for t in targets],
            ]
            proc = subprocess.run(command, cwd=REPO_ROOT)
            return proc.returncode == 0, f"Ran {candidate_path}", " ".join(command), proc.returncode

        if candidate_path.suffix.lower() in {".bat", ".cmd"}:
            command = ["cmd", "/c", str(candidate_path), *[str(t) for t in targets]]
            proc = subprocess.run(command, cwd=REPO_ROOT)
            return proc.returncode == 0, f"Ran {candidate_path}", " ".join(command), proc.returncode

        if candidate_path.suffix.lower() in {".js", ".mjs", ".cjs"}:
            command = ["node", str(candidate_path), *[str(t) for t in targets]]
            proc = subprocess.run(command, cwd=REPO_ROOT)
            return proc.returncode == 0, f"Ran {candidate_path}", " ".join(command), proc.returncode

    # Handle raw shell commands from configs, e.g. wrangler pages deploy .
    if " " in candidate and not candidate_path.exists():
        if dry_run:
            return True, f"Would run {candidate}", candidate, None
        proc = subprocess.run(candidate, cwd=REPO_ROOT, shell=True)
        return proc.returncode == 0, f"Ran {candidate}", candidate, proc.returncode

    return False, f"Missing script: {candidate}", candidate, None


def process_steps(
    steps: list[dict],
    targets: list[Path],
    dry_run: bool,
    strict: bool,
) -> list[StepResult]:
    results: list[StepResult] = []
    for step in steps:
        name = step["name"]
        kind = step.get("kind", "external")
        required = bool(step.get("required", False))
        print()
        print(f"-> {name}")

        if kind == "builtin":
            if name == "precheck":
                ok, detail, messages = builtin_precheck(targets)
            elif name == "canonical_gate":
                ok, detail, messages = builtin_canonical_gate(targets)
            elif name == "postcheck":
                ok, detail, messages = builtin_postcheck(targets)
            else:
                ok, detail, messages = True, f"{name} completed.", []

            for message in messages:
                print(f"   {message}")
            status = "ok" if ok else "failed"
            results.append(StepResult(name=name, status=status, detail=detail))
            if not ok and (strict or required):
                break
            continue

        candidates = list(step.get("candidates", []))
        ran = False
        for candidate in candidates:
            ok, detail, command, returncode = run_external(candidate, targets, dry_run)
            if ok and command:
                results.append(
                    StepResult(
                        name=name,
                        status="ok" if returncode in (None, 0) else "failed",
                        detail=detail,
                        command=command,
                        returncode=returncode,
                    )
                )
                print(f"   {detail}")
                ran = True
                if returncode not in (None, 0) and (strict or required):
                    break
                break

        if ran:
            continue

        missing_msg = f"Missing script(s) for {name}: {', '.join(candidates) if candidates else '(none)'}"
        print(f"   {missing_msg}")
        results.append(StepResult(name=name, status="missing", detail=missing_msg))
        if strict or required:
            break

    return results


def build_report(results: list[StepResult], targets: list[Path], workflow: str, series: Optional[str]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "build-all-report.md"

    right = [r for r in results if r.status == "ok"]
    wrong = [r for r in results if r.status == "failed"]
    missing = [r for r in results if r.status == "missing"]
    overstated = [r for r in results if "overstated" in r.detail.lower()]

    lines = [
        "# Build All Report",
        "",
        f"- Workflow: `{workflow}`",
        f"- Series: `{series or 'none'}`",
        f"- Targets: {len(targets)}",
        "",
        "## What We Got Right",
    ]
    if right:
        lines.extend(f"- `{r.name}`" for r in right)
    else:
        lines.append("- None")

    lines.extend(["", "## What We Got Wrong"])
    if wrong:
        lines.extend(f"- `{r.name}`: {r.detail}" for r in wrong)
    else:
        lines.append("- None")

    lines.extend(["", "## What's Missing"])
    if missing:
        lines.extend(f"- `{r.name}`: {r.detail}" for r in missing)
    else:
        lines.append("- None")

    lines.extend(["", "## What We Overstated"])
    if overstated:
        lines.extend(f"- `{r.name}`: {r.detail}" for r in overstated)
    else:
        lines.append("- None")

    lines.extend(["", "## Targets"])
    lines.extend(f"- `{target}`" for target in targets)
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the faiththruphysics HTML pipeline.")
    parser.add_argument("targets", nargs="*", help="HTML file(s) or folder(s) to process.")
    parser.add_argument("--workflow", default="core-html", help="Workflow config name under MUST DO/workflows.")
    parser.add_argument("--series", choices=["mda", "gtq"], help="Optional series-specific step set.")
    parser.add_argument("--deploy", action="store_true", help="Append deploy steps.")
    parser.add_argument("--convert", action="store_true", help="Append content conversion steps.")
    parser.add_argument("--maintenance", action="store_true", help="Append maintenance steps.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without changing files.")
    parser.add_argument("--strict", action="store_true", help="Fail on the first missing or failing step.")
    args = parser.parse_args(argv)

    targets = [normalize_target(value) for value in args.targets] if args.targets else [REPO_ROOT / "MUST DO"]
    for target in targets:
        if not target.exists():
            print(f"Target not found: {target}")
            return 2

    print_header("BUILD_ALL")
    print(f"Repo root: {REPO_ROOT}")
    print(f"Workflow:  {args.workflow}")
    print(f"Series:    {args.series or 'none'}")
    print(f"Dry run:   {args.dry_run}")
    print(f"Strict:    {args.strict}")
    for target in targets:
        print(f"Target:    {target}")

    steps = load_workflow(args.workflow, DEFAULT_CORE_STEPS)
    if args.series:
        steps = steps + DEFAULT_SERIES_STEPS.get(args.series, [])
    if args.deploy:
        steps = steps + DEFAULT_DEPLOY_STEPS
    if args.convert:
        steps = steps + DEFAULT_CONVERT_STEPS
    if args.maintenance:
        steps = steps + DEFAULT_MAINTENANCE_STEPS

    results = process_steps(steps, targets, args.dry_run, args.strict)
    report_path = build_report(results, targets, args.workflow, args.series)
    print()
    print(f"Report written to: {report_path}")

    failed = any(r.status == "failed" for r in results)
    missing = any(r.status == "missing" for r in results)
    if failed or (args.strict and missing):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
