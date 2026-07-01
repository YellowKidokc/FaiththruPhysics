#!/usr/bin/env python3
"""
site_master_loop.py

POF 2828 website orchestration scaffold.

This is the code spine for the repeatable website loop:

    scan -> classify -> deterministic fix -> batch unresolved
    -> apply -> verify -> repeat

Current goal:
- provide one place to organize the passes
- emit per-series reports
- reuse existing fixers instead of inventing five disconnected scripts

This is intentionally conservative. It does not attempt AI calls yet.
It prepares the exact series-level batches and reports that an AI layer can consume.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


SITE_ROOT = Path(r"D:\GitHub\faiththruphysics-site")
REPORT_ROOT = SITE_ROOT / "reports" / "site-master-loop"
REGISTRY_PATH = SITE_ROOT / "scripts" / "site_label_registry.seed.json"
PREDICTION_REGISTRY_PATH = SITE_ROOT / "scripts" / "site_prediction_engines.seed.json"
WORK_ORDER_PATH = SITE_ROOT / "scripts" / "site_stage_work_order.seed.json"
QUEUE_ROOT = REPORT_ROOT / "jobs"
SCREENSHOT_ROOT = REPORT_ROOT / "screenshots"
PREDICTION_ROOT = REPORT_ROOT / "predictions"

HTML_EXTENSIONS = {".html", ".htm"}

TP_INJECT_RE = re.compile(r"tp-inject\.js", re.IGNORECASE)
FRAME_RE = re.compile(r"/site-shell/frame\.js", re.IGNORECASE)
AUDIT_INTRO_RE = re.compile(
    r"what we got right.*what we overstated.*what we got wrong",
    re.IGNORECASE | re.DOTALL,
)
WHITE_BG_RE = re.compile(
    r"background\s*:\s*(?:#fff|#ffffff|white|rgb\s*\(\s*255\s*,\s*255\s*,\s*255)",
    re.IGNORECASE,
)
DATA_TP_ROLE_RE = re.compile(r'data-tp-role\s*=\s*"([^"]+)"', re.IGNORECASE)

DEFAULT_SERIES = [
    "consciousness",
    "revolution-of-truth",
    "genesis-to-quantum",
    "one-page-stories",
    "mda",
    "moral-decline",
    "convergence-series",
    "convergence-deep",
    "cross-domain",
    "three-truths",
    "proof-architecture",
    "blue",
]

DEFAULT_CADENCE_SEQUENCE = [3, 10, 4, 6, 5, 2, 3]
DEFAULT_CADENCE_FLOOR = 3
PIPELINE_STAGES = [
    "labels",
    "headers",
    "footers",
    "audit",
    "score",
    "pressure",
    "predict",
    "blocks",
    "dashboard",
    "verify",
]
IGNORED_PATH_PART_MARKERS = (
    "_site_archives",
    "_link-fix-backup",
    "_archives",
    "archive",
    "archive-",
    "codex_build",
    "backup-",
)

TEXTUAL_TAGS = {"p", "blockquote", "figcaption"}
URL_ATTRS = ("src", "href")
TEXT_PREVIEW_LIMIT = 160


@dataclass
class UnknownSnippet:
    tag: str
    parent_tag: str
    classes: list[str]
    identifier: str | None
    suggested_role: str | None
    text_preview: str
    source_path: str


@dataclass
class UnknownSignature:
    signature: str
    tag: str
    parent_tag: str
    classes: list[str]
    identifier: str | None
    suggested_role: str | None
    count: int = 0
    sample_paths: list[str] = field(default_factory=list)
    samples: list[UnknownSnippet] = field(default_factory=list)


@dataclass
class UnknownRoleValue:
    role: str
    count: int
    sample_paths: list[str]


@dataclass
class LabelPayload:
    series: str
    registry_path: str
    pages_scanned: int
    unknown_signature_count: int
    unknown_element_count: int
    unknown_signatures: list[UnknownSignature]
    unknown_role_values: list[UnknownRoleValue]


@dataclass
class PageFinding:
    path: str
    header_ok: bool
    footer_ok: bool
    labels_present: bool
    white_bg_marker: bool
    unresolved: list[str]


@dataclass
class SeriesReport:
    series: str
    root: str
    pages_scanned: int
    pages_clean: int
    unresolved_pages: int
    unresolved_items: int
    findings: list[PageFinding]
    label_payload: LabelPayload | None = None


@dataclass
class CadenceState:
    sequence: list[int]
    floor: int
    index: int = 0

    def next_interval(self) -> int:
        if not self.sequence:
            return self.floor
        value = self.sequence[self.index % len(self.sequence)]
        self.index += 1
        return max(self.floor, value)


@dataclass
class SkipLedgerEntry:
    loop_name: str
    scheduled_for: str
    status: str
    reason: str
    previous_failure: str
    next_action: str


@dataclass
class JobRecord:
    job_id: str
    series: str
    page_path: str
    page_relpath: str
    stage: str
    status: str
    attempts: int
    created_at: str
    updated_at: str
    history: list[dict[str, str]]


@dataclass
class PredictionEngine:
    engine_id: str
    label: str
    family: str
    enabled: bool
    stage: str
    sequence: int
    consumes: list[str]
    produces: list[str]
    confidence_weight: float
    notes: str = ""


@dataclass
class PredictionRunRecord:
    job_id: str
    page_relpath: str
    series: str
    stage: str
    engine_id: str
    status: str
    created_at: str
    updated_at: str
    inputs: dict[str, str | float | int | bool | list[str]]
    outputs: dict[str, str | float | int | bool | list[str]]
    actuals: dict[str, str | float | int | bool | list[str]]
    metrics: dict[str, float | int | str]


@dataclass
class BrowserAuditFinding:
    page_relpath: str
    url: str
    ok: bool
    white_page: bool
    js_errors: list[str]
    request_failures: list[str]
    console_errors: list[str]
    topbar_count: int
    dock_count: int
    background: str
    body_background: str
    unresolved: list[str]


@dataclass
class StageWorkPolicy:
    stage: str
    priority: int
    worker_type: str
    depends_on: list[str]
    min_upstream_done: int
    notes: str = ""


@dataclass
class StageQueueStatus:
    stage: str
    priority: int
    worker_type: str
    pending: int
    locked: int
    done: int
    failed: int
    depends_on: list[str]
    min_upstream_done: int
    upstream_done: dict[str, int]
    unlocked: bool
    blocking_reason: str


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stage_dirs(stage: str) -> dict[str, Path]:
    root = QUEUE_ROOT / stage
    return {
        "root": root,
        "pending": root / "pending",
        "locked": root / "locked",
        "done": root / "done",
        "failed": root / "failed",
    }


def ensure_queue_dirs() -> list[Path]:
    created: list[Path] = []
    for stage in PIPELINE_STAGES:
        for path in stage_dirs(stage).values():
            if path.name == "root":
                continue
            path.mkdir(parents=True, exist_ok=True)
            created.append(path)
    SCREENSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    PREDICTION_ROOT.mkdir(parents=True, exist_ok=True)
    return created


def ensure_prediction_dirs() -> list[Path]:
    created: list[Path] = []
    for name in ("runs", "actuals", "leaderboards", "chains"):
        path = PREDICTION_ROOT / name
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)
    return created


def load_prediction_registry() -> dict:
    return json.loads(PREDICTION_REGISTRY_PATH.read_text(encoding="utf-8"))


def load_work_order() -> dict:
    return json.loads(WORK_ORDER_PATH.read_text(encoding="utf-8"))


def work_policies_by_stage() -> dict[str, StageWorkPolicy]:
    data = load_work_order()
    items = data.get("stages", [])
    return {item["stage"]: StageWorkPolicy(**item) for item in items}


def registry_engines_by_stage(registry: dict) -> dict[str, list[PredictionEngine]]:
    stage_map: dict[str, list[PredictionEngine]] = defaultdict(list)
    for item in registry.get("engines", []):
        engine = PredictionEngine(**item)
        if engine.enabled:
            stage_map[engine.stage].append(engine)
    for stage in stage_map:
        stage_map[stage].sort(key=lambda engine: engine.sequence)
    return dict(stage_map)


def write_prediction_run(record: PredictionRunRecord) -> Path:
    ensure_prediction_dirs()
    out = PREDICTION_ROOT / "runs" / f"{record.job_id}__{record.stage}__{record.engine_id}.json"
    out.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")
    return out


def append_prediction_actual(page_relpath: str, actuals: dict[str, str | float | int | bool | list[str]]) -> Path:
    ensure_prediction_dirs()
    out = PREDICTION_ROOT / "actuals" / "actuals.jsonl"
    payload = {
        "page_relpath": page_relpath,
        "recorded_at": now_utc(),
        "actuals": actuals,
    }
    with out.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload) + "\n")
    return out


def build_prediction_leaderboard() -> Path:
    ensure_prediction_dirs()
    runs_dir = PREDICTION_ROOT / "runs"
    scores: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {
            "runs": 0,
            "resolved_actuals": 0,
            "mean_confidence": 0.0,
            "mean_accuracy": 0.0,
            "weighted_score": 0.0,
        }
    )

    for path in sorted(runs_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        engine_id = data["engine_id"]
        metrics = data.get("metrics", {})
        bucket = scores[engine_id]
        bucket["runs"] += 1
        bucket["mean_confidence"] += float(metrics.get("confidence", 0.0))
        if "accuracy" in metrics:
            bucket["resolved_actuals"] += 1
            bucket["mean_accuracy"] += float(metrics.get("accuracy", 0.0))
            bucket["weighted_score"] += float(metrics.get("accuracy", 0.0)) * float(
                metrics.get("confidence", 0.0)
            )

    leaderboard: list[dict[str, float | int | str]] = []
    for engine_id, bucket in scores.items():
        runs = int(bucket["runs"])
        resolved = int(bucket["resolved_actuals"])
        mean_confidence = float(bucket["mean_confidence"]) / runs if runs else 0.0
        mean_accuracy = float(bucket["mean_accuracy"]) / resolved if resolved else 0.0
        weighted_score = float(bucket["weighted_score"]) / resolved if resolved else 0.0
        leaderboard.append(
            {
                "engine_id": engine_id,
                "runs": runs,
                "resolved_actuals": resolved,
                "mean_confidence": round(mean_confidence, 4),
                "mean_accuracy": round(mean_accuracy, 4),
                "weighted_score": round(weighted_score, 4),
            }
        )

    leaderboard.sort(
        key=lambda item: (
            -float(item["weighted_score"]),
            -float(item["mean_accuracy"]),
            -int(item["resolved_actuals"]),
            item["engine_id"],
        )
    )

    out = PREDICTION_ROOT / "leaderboards" / "prediction-engine-leaderboard.json"
    out.write_text(json.dumps(leaderboard, indent=2), encoding="utf-8")
    return out


def build_prediction_chain_plan() -> Path:
    ensure_prediction_dirs()
    registry = load_prediction_registry()
    stage_map = registry_engines_by_stage(registry)
    plan = {
        "generated_at": now_utc(),
        "stages": {
            stage: [asdict(engine) for engine in engines]
            for stage, engines in stage_map.items()
        },
        "rule": "Run all enabled engines per stage, compare hit rates over time, and allow stronger engines to feed downstream stages through recorded outputs rather than replacing the whole ensemble.",
    }
    out = PREDICTION_ROOT / "chains" / "prediction-chain-plan.json"
    out.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return out


def path_to_file_url(path: Path) -> str:
    return "file:///" + quote(str(path.resolve()).replace("\\", "/"), safe="/:.-_")


def path_to_audit_url(path: Path, base_url: str | None) -> str:
    if base_url:
        rel = str(path.relative_to(SITE_ROOT)).replace("\\", "/")
        return base_url.rstrip("/") + "/" + quote(rel, safe="/:.-_")
    return path_to_file_url(path)


def collect_browser_audit_targets(series_roots: list[Path], limit: int | None = None) -> list[Path]:
    targets: list[Path] = []
    for series_root in series_roots:
        for page_path in iter_html_files(series_root):
            targets.append(page_path)
            if limit is not None and len(targets) >= limit:
                return targets
    return targets


async def audit_single_page(browser, page_path: Path, base_url: str | None = None) -> BrowserAuditFinding:
    page = await browser.new_page(viewport={"width": 1440, "height": 1600})
    js_errors: list[str] = []
    request_failures: list[str] = []
    console_errors: list[str] = []

    page.on("pageerror", lambda exc: js_errors.append(str(exc)))
    def handle_request_failed(req) -> None:
        failure = getattr(req, "failure", None)
        if callable(failure):
            failure = failure()
        if isinstance(failure, dict):
            detail = failure.get("errorText", "failed")
        elif hasattr(failure, "error_text"):
            detail = failure.error_text
        elif isinstance(failure, str):
            detail = failure
        else:
            detail = "failed"
        request_failures.append(f"{req.method} {req.url} :: {detail}")

    page.on("requestfailed", handle_request_failed)

    def handle_console(msg) -> None:
        try:
            level = msg.type
        except Exception:
            level = "log"
        if level == "error":
            console_errors.append(msg.text)

    page.on("console", handle_console)

    url = path_to_audit_url(page_path, base_url)
    unresolved: list[str] = []
    topbar_count = 0
    dock_count = 0
    background = ""
    body_background = ""
    white_page = False

    try:
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(600)
        audit = await page.evaluate(
            """() => {
                const body = document.body;
                const root = document.documentElement;
                const bg = getComputedStyle(root).backgroundColor || "";
                const bodyBg = body ? getComputedStyle(body).backgroundColor || "" : "";
                const topbar = document.querySelectorAll('.tp-top, .site-shell-topbar, [data-site-shell="topbar"]').length;
                const dock = document.querySelectorAll('.tp-player, .site-shell-dock, [data-site-shell="dock"]').length;
                return { bg, bodyBg, topbar, dock };
            }"""
        )
        background = str(audit.get("bg", ""))
        body_background = str(audit.get("bodyBg", ""))
        topbar_count = int(audit.get("topbar", 0))
        dock_count = int(audit.get("dock", 0))

        white_markers = {
            "rgb(255, 255, 255)",
            "rgba(255, 255, 255, 1)",
            "white",
        }
        white_page = background in white_markers or body_background in white_markers
        if white_page:
            unresolved.append("white_page")
        if topbar_count == 0:
            unresolved.append("missing_topbar_runtime")
        if dock_count == 0:
            unresolved.append("missing_dock_runtime")
        if js_errors:
            unresolved.append("pageerror")
        if request_failures:
            unresolved.append("requestfailed")
        if console_errors:
            unresolved.append("console_error")
    except Exception as exc:
        unresolved.append("navigation_error")
        js_errors.append(str(exc))
    finally:
        await page.close()

    return BrowserAuditFinding(
        page_relpath=str(page_path.relative_to(SITE_ROOT)),
        url=url,
        ok=not unresolved,
        white_page=white_page,
        js_errors=js_errors[:20],
        request_failures=request_failures[:20],
        console_errors=console_errors[:20],
        topbar_count=topbar_count,
        dock_count=dock_count,
        background=background,
        body_background=body_background,
        unresolved=unresolved,
    )


async def run_browser_audit_async(targets: list[Path], base_url: str | None = None) -> list[BrowserAuditFinding]:
    findings: list[BrowserAuditFinding] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            for page_path in targets:
                findings.append(await audit_single_page(browser, page_path, base_url=base_url))
        finally:
            await browser.close()
    return findings


def write_browser_audit_report(findings: list[BrowserAuditFinding]) -> tuple[Path, Path]:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_ROOT / "browser-audit.json"
    review_path = REPORT_ROOT / "browser-audit-review.jsonl"

    unresolved_counter: Counter[str] = Counter()
    for finding in findings:
        unresolved_counter.update(finding.unresolved)

    payload = {
        "generated_at": now_utc(),
        "pages_scanned": len(findings),
        "pages_clean": sum(1 for item in findings if item.ok),
        "pages_with_issues": sum(1 for item in findings if not item.ok),
        "issue_counts": dict(unresolved_counter),
        "findings": [asdict(item) for item in findings],
    }
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with review_path.open("w", encoding="utf-8") as fh:
        for finding in findings:
            if finding.ok:
                continue
            fh.write(
                json.dumps(
                    {
                        "page_relpath": finding.page_relpath,
                        "issue_type": "browser_audit",
                        "severity": "high" if "white_page" in finding.unresolved or "navigation_error" in finding.unresolved else "medium",
                        "unresolved": finding.unresolved,
                        "next_action": "route_to_verify_or_shell_fix",
                    }
                )
                + "\n"
            )

    return report_path, review_path


def count_stage_files(stage: str) -> dict[str, int]:
    dirs = stage_dirs(stage)
    return {
        "pending": len(list(dirs["pending"].glob("*.json"))),
        "locked": len(list(dirs["locked"].glob("*.json"))),
        "done": len(list(dirs["done"].glob("*.json"))),
        "failed": len(list(dirs["failed"].glob("*.json"))),
    }


def build_queue_status() -> list[StageQueueStatus]:
    ensure_queue_dirs()
    policies = work_policies_by_stage()
    statuses: list[StageQueueStatus] = []

    for stage in PIPELINE_STAGES:
        policy = policies.get(
            stage,
            StageWorkPolicy(
                stage=stage,
                priority=999,
                worker_type="unknown",
                depends_on=[],
                min_upstream_done=0,
                notes="No policy entry found.",
            ),
        )
        counts = count_stage_files(stage)
        upstream_done = {
            dependency: count_stage_files(dependency)["done"] for dependency in policy.depends_on
        }

        if not policy.depends_on:
            unlocked = True
            blocking_reason = ""
        else:
            unlocked = all(
                upstream_done.get(dependency, 0) >= policy.min_upstream_done
                for dependency in policy.depends_on
            )
            if unlocked:
                blocking_reason = ""
            else:
                shortage = ", ".join(
                    f"{dependency}:{upstream_done.get(dependency, 0)}/{policy.min_upstream_done}"
                    for dependency in policy.depends_on
                )
                blocking_reason = f"waiting_for_lead({shortage})"

        statuses.append(
            StageQueueStatus(
                stage=stage,
                priority=policy.priority,
                worker_type=policy.worker_type,
                pending=counts["pending"],
                locked=counts["locked"],
                done=counts["done"],
                failed=counts["failed"],
                depends_on=list(policy.depends_on),
                min_upstream_done=policy.min_upstream_done,
                upstream_done=upstream_done,
                unlocked=unlocked,
                blocking_reason=blocking_reason,
            )
        )

    statuses.sort(key=lambda item: (item.priority, item.stage))
    return statuses


def write_queue_status_report() -> Path:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    out = REPORT_ROOT / "queue-status.json"
    payload = {
        "generated_at": now_utc(),
        "stages": [asdict(item) for item in build_queue_status()],
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def job_filename_for(relpath: str) -> str:
    digest = hashlib.md5(relpath.encode("utf-8")).hexdigest()[:12]
    safe_name = relpath.replace("\\", "__").replace("/", "__").replace(":", "")
    return f"{digest}__{safe_name}.json"


def write_job(path: Path, record: JobRecord) -> None:
    path.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")


def read_job(path: Path) -> JobRecord:
    return JobRecord(**json.loads(path.read_text(encoding="utf-8")))


def queue_page_job(series_root: Path, page_path: Path, initial_stage: str = "labels") -> Path:
    relative_to_site = str(page_path.relative_to(SITE_ROOT))
    pending_dir = stage_dirs(initial_stage)["pending"]
    pending_dir.mkdir(parents=True, exist_ok=True)
    job_path = pending_dir / job_filename_for(relative_to_site)
    timestamp = now_utc()
    record = JobRecord(
        job_id=job_path.stem.split("__", 1)[0],
        series=series_root.name,
        page_path=str(page_path),
        page_relpath=relative_to_site,
        stage=initial_stage,
        status="pending",
        attempts=0,
        created_at=timestamp,
        updated_at=timestamp,
        history=[{"timestamp": timestamp, "event": "queued", "stage": initial_stage}],
    )
    write_job(job_path, record)
    return job_path


def job_path_for_stage_and_relpath(stage: str, relpath: str, bucket: str) -> Path:
    return stage_dirs(stage)[bucket] / job_filename_for(relpath)


def any_job_exists_for_stage(stage: str, relpath: str) -> bool:
    filename = job_filename_for(relpath)
    dirs = stage_dirs(stage)
    return any((dirs[bucket] / filename).exists() for bucket in ("pending", "locked", "done", "failed"))


def stage_job_done(stage: str, relpath: str) -> bool:
    return job_path_for_stage_and_relpath(stage, relpath, "done").exists()


def enqueue_page_for_stage(
    record: JobRecord,
    stage: str,
    event_note: str,
) -> Path:
    pending_dir = stage_dirs(stage)["pending"]
    pending_dir.mkdir(parents=True, exist_ok=True)
    job_path = pending_dir / job_filename_for(record.page_relpath)
    next_record = JobRecord(
        job_id=record.job_id,
        series=record.series,
        page_path=record.page_path,
        page_relpath=record.page_relpath,
        stage=stage,
        status="pending",
        attempts=0,
        created_at=record.created_at,
        updated_at=record.updated_at,
        history=record.history
        + [{"timestamp": record.updated_at, "event": "queued", "stage": stage, "notes": event_note}],
    )
    write_job(job_path, next_record)
    return job_path


def downstream_stages_for(stage: str) -> list[str]:
    policies = work_policies_by_stage()
    return [
        candidate_stage
        for candidate_stage, policy in policies.items()
        if stage in policy.depends_on
    ]


def enqueue_series_jobs(series_roots: list[Path]) -> list[Path]:
    ensure_queue_dirs()
    queued: list[Path] = []
    for series_root in series_roots:
        for page_path in iter_html_files(series_root):
            relative_to_site = str(page_path.relative_to(SITE_ROOT))
            if any(any_job_exists_for_stage(stage, relative_to_site) for stage in PIPELINE_STAGES):
                continue
            queued.append(queue_page_job(series_root, page_path))
    return queued


def claim_next_job(stage: str, worker: str) -> Path | None:
    queue_status = {item.stage: item for item in build_queue_status()}
    stage_state = queue_status.get(stage)
    if stage_state is not None and not stage_state.unlocked:
        return None

    dirs = stage_dirs(stage)
    dirs["locked"].mkdir(parents=True, exist_ok=True)
    for candidate in sorted(dirs["pending"].glob("*.json")):
        destination = dirs["locked"] / candidate.name
        try:
            candidate.replace(destination)
        except FileNotFoundError:
            continue
        record = read_job(destination)
        record.status = "locked"
        record.attempts += 1
        record.updated_at = now_utc()
        record.history.append(
            {"timestamp": record.updated_at, "event": "claimed", "stage": stage, "worker": worker}
        )
        write_job(destination, record)
        return destination
    return None


async def capture_page_screenshot(source: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if source.startswith(("http://", "https://", "file://")):
        target = source
    else:
        target = Path(source).resolve().as_uri()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 2200})
        await page.goto(target, wait_until="networkidle")
        await page.screenshot(path=str(output_path), full_page=True)
        await browser.close()


def screenshot_path_for(record: JobRecord, stage: str) -> Path:
    stem = Path(record.page_relpath).stem
    return SCREENSHOT_ROOT / stage / f"{stem}.png"


def build_gallery() -> Path:
    SCREENSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    gallery_path = SCREENSHOT_ROOT / "index.html"
    images = sorted(
        [
            path.relative_to(SCREENSHOT_ROOT).as_posix()
            for path in SCREENSHOT_ROOT.rglob("*.png")
            if path.name.lower() != "index.html"
        ]
    )
    slides = "\n".join(
        f'<img class="slide" src="{src}" alt="{src}" loading="lazy">' for src in images
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="30">
  <title>Site Master Loop Screenshots</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; background: #050505; color: #e7e2d3; font-family: Inter, Arial, sans-serif; }}
    .bar {{ position: sticky; top: 0; z-index: 2; padding: 10px 14px; background: rgba(5,5,5,.92); border-bottom: 1px solid rgba(212,175,55,.25); }}
    .meta {{ font-size: 12px; color: #d4af37; letter-spacing: .04em; text-transform: uppercase; }}
    .stage {{ font-size: 14px; color: #bdb8aa; margin-top: 4px; }}
    .deck {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px; padding: 14px; }}
    .slide {{ width: 100%; height: auto; border: 1px solid rgba(212,175,55,.18); border-radius: 10px; background: #111; }}
  </style>
</head>
<body>
  <div class="bar">
    <div class="meta">POF 2828 - Site Master Loop Gallery</div>
    <div class="stage">{len(images)} screenshot(s) - auto-refresh every 30s</div>
  </div>
  <div class="deck">
    {slides or '<p>No screenshots yet.</p>'}
  </div>
</body>
</html>
"""
    gallery_path.write_text(html, encoding="utf-8")
    return gallery_path


def complete_locked_job(
    locked_job_path: Path,
    result: str,
    worker: str,
    notes: str = "",
    screenshot_source: str | None = None,
) -> tuple[Path, list[Path], Path]:
    record = read_job(locked_job_path)
    current_stage = record.stage
    dirs = stage_dirs(current_stage)
    record.updated_at = now_utc()
    record.status = result
    record.history.append(
        {
            "timestamp": record.updated_at,
            "event": result,
            "stage": current_stage,
            "worker": worker,
            "notes": notes,
        }
    )

    screenshot_path = None
    if screenshot_source:
        screenshot_path = screenshot_path_for(record, current_stage)
        asyncio.run(capture_page_screenshot(screenshot_source, screenshot_path))

    destination = dirs["done"] / locked_job_path.name if result == "done" else dirs["failed"] / locked_job_path.name
    write_job(locked_job_path, record)
    locked_job_path.replace(destination)

    next_job_paths: list[Path] = []
    if result == "done":
        policies = work_policies_by_stage()
        for next_stage in downstream_stages_for(current_stage):
            policy = policies[next_stage]
            if any_job_exists_for_stage(next_stage, record.page_relpath):
                continue
            if not all(stage_job_done(dep_stage, record.page_relpath) for dep_stage in policy.depends_on):
                continue
            next_job_paths.append(
                enqueue_page_for_stage(
                    record=record,
                    stage=next_stage,
                    event_note=f"dependencies resolved: {', '.join(policy.depends_on)}",
                )
            )

    gallery_path = build_gallery()
    return destination, next_job_paths, gallery_path


def iter_html_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() in HTML_EXTENSIONS and path.is_file():
            name = path.name.lower()
            if ".bak" in name or ".pre-" in name:
                continue
            lower_parts = [part.lower() for part in path.parts]
            if any(marker in part for part in lower_parts for marker in IGNORED_PATH_PART_MARKERS):
                continue
            yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def normalize_text(value: str) -> str:
    compact = " ".join(value.split())
    if len(compact) > TEXT_PREVIEW_LIMIT:
        return compact[: TEXT_PREVIEW_LIMIT - 3].rstrip() + "..."
    return compact


def element_text_preview(element) -> str:
    if element.name in TEXTUAL_TAGS or element.name.startswith("h") or element.name in {"li", "td", "th", "a"}:
        text = normalize_text(element.get_text(" ", strip=True))
        if text:
            return text

    for attr in ("alt", "title", "aria-label", *URL_ATTRS):
        value = element.get(attr)
        if value:
            return normalize_text(str(value))

    return ""


def signature_for(element, suggested_role: str | None) -> str:
    classes = ".".join(sorted(element.get("class", []))[:4]) or "-"
    parent_tag = element.parent.name if getattr(element.parent, "name", None) else "root"
    identifier = element.get("id") or "-"
    return f"{element.name}|{parent_tag}|{classes}|{identifier}|{suggested_role or '-'}"


def should_track_element(element, registry: dict) -> bool:
    if element.name is None:
        return False
    if element.has_attr("data-tp-role"):
        return False
    if element.name in set(registry.get("skip_tags", [])):
        return False
    if element.name not in set(registry.get("candidate_tags", [])):
        return False
    if element.find_parent(attrs={"data-tp-role": True}) and element.name in {"li", "td", "th", "figcaption"}:
        return False
    return True


def suggested_role_for(element, registry: dict) -> str | None:
    tag_hints = registry.get("tag_role_hints", {})
    return tag_hints.get(element.name)


def extract_label_payload(series_root: Path, html_paths: list[Path], registry: dict) -> LabelPayload:
    max_paths = int(registry.get("max_paths_per_signature", 4))
    max_samples = int(registry.get("max_samples_per_signature", 3))
    max_signatures = int(registry.get("max_signatures_per_series", 80))

    signatures: dict[str, UnknownSignature] = {}
    unknown_role_counter: Counter[str] = Counter()
    unknown_role_paths: dict[str, list[str]] = defaultdict(list)

    for path in html_paths:
        text = read_text(path)
        relative_path = str(path.relative_to(SITE_ROOT))

        for role in DATA_TP_ROLE_RE.findall(text):
            if role not in registry.get("known_roles", []):
                unknown_role_counter[role] += 1
                if len(unknown_role_paths[role]) < max_paths:
                    unknown_role_paths[role].append(relative_path)

        soup = BeautifulSoup(text, "lxml")
        body = soup.body or soup

        for element in body.find_all(True):
            if not should_track_element(element, registry):
                continue

            preview = element_text_preview(element)
            if not preview and element.name in {"section", "article", "div", "nav", "header", "footer", "aside"}:
                continue

            suggested_role = suggested_role_for(element, registry)
            signature = signature_for(element, suggested_role)
            item = signatures.get(signature)
            if item is None:
                item = UnknownSignature(
                    signature=signature,
                    tag=element.name,
                    parent_tag=element.parent.name if getattr(element.parent, "name", None) else "root",
                    classes=sorted(element.get("class", [])),
                    identifier=element.get("id"),
                    suggested_role=suggested_role,
                )
                signatures[signature] = item

            item.count += 1
            if len(item.sample_paths) < max_paths and relative_path not in item.sample_paths:
                item.sample_paths.append(relative_path)
            if len(item.samples) < max_samples:
                item.samples.append(
                    UnknownSnippet(
                        tag=element.name,
                        parent_tag=item.parent_tag,
                        classes=item.classes,
                        identifier=item.identifier,
                        suggested_role=suggested_role,
                        text_preview=preview,
                        source_path=relative_path,
                    )
                )

    ranked = sorted(
        signatures.values(),
        key=lambda item: (-item.count, item.tag, item.parent_tag, item.signature),
    )[:max_signatures]
    unknown_role_values = [
        UnknownRoleValue(role=role, count=count, sample_paths=unknown_role_paths[role])
        for role, count in unknown_role_counter.most_common()
    ]

    return LabelPayload(
        series=series_root.name,
        registry_path=str(REGISTRY_PATH),
        pages_scanned=len(html_paths),
        unknown_signature_count=len(ranked),
        unknown_element_count=sum(item.count for item in ranked),
        unknown_signatures=ranked,
        unknown_role_values=unknown_role_values,
    )


def inspect_page(path: Path) -> PageFinding:
    text = read_text(path)

    header_ok = bool(TP_INJECT_RE.search(text) or FRAME_RE.search(text))
    footer_ok = bool(AUDIT_INTRO_RE.search(text))
    labels_present = bool(DATA_TP_ROLE_RE.search(text))
    white_bg_marker = bool(WHITE_BG_RE.search(text))

    unresolved: list[str] = []
    if not header_ok:
        unresolved.append("missing_header_shell")
    if not footer_ok:
        unresolved.append("missing_footer_audit")
    if not labels_present:
        unresolved.append("missing_structural_labels")
    if white_bg_marker:
        unresolved.append("white_background_marker")

    return PageFinding(
        path=str(path.relative_to(SITE_ROOT)),
        header_ok=header_ok,
        footer_ok=footer_ok,
        labels_present=labels_present,
        white_bg_marker=white_bg_marker,
        unresolved=unresolved,
    )


def build_series_report(series_root: Path, registry: dict, include_payloads: bool) -> SeriesReport:
    html_paths = list(iter_html_files(series_root))
    findings = [inspect_page(path) for path in html_paths]
    pages_clean = sum(1 for f in findings if not f.unresolved)
    unresolved_pages = sum(1 for f in findings if f.unresolved)
    unresolved_items = sum(len(f.unresolved) for f in findings)
    label_payload = extract_label_payload(series_root, html_paths, registry) if include_payloads else None

    return SeriesReport(
        series=series_root.name,
        root=str(series_root),
        pages_scanned=len(findings),
        pages_clean=pages_clean,
        unresolved_pages=unresolved_pages,
        unresolved_items=unresolved_items,
        findings=findings,
        label_payload=label_payload,
    )


def write_report(report: SeriesReport) -> Path:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    out = REPORT_ROOT / f"{report.series}.json"
    payload = asdict(report)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def render_label_prompt(payload: LabelPayload) -> str:
    lines = [
        f"# Label Batch: {payload.series}",
        "",
        "Goal: resolve missing structural labels conservatively.",
        "Use the canonical roles already in the registry unless a genuinely new role is required.",
        "",
        f"- Pages scanned: {payload.pages_scanned}",
        f"- Unknown structural signatures: {payload.unknown_signature_count}",
        f"- Unknown structural element count (capped to retained signatures): {payload.unknown_element_count}",
        f"- Registry: `{payload.registry_path}`",
        "",
        "## Unknown structural signatures",
    ]

    for item in payload.unknown_signatures:
        lines.extend(
            [
                f"### {item.signature}",
                f"- tag: `{item.tag}`",
                f"- parent: `{item.parent_tag}`",
                f"- classes: `{', '.join(item.classes) if item.classes else '-'}`",
                f"- id: `{item.identifier or '-'}`",
                f"- suggested role from tag hint: `{item.suggested_role or '-'}`",
                f"- count: {item.count}",
                f"- sample paths: {', '.join(item.sample_paths) if item.sample_paths else '-'}",
                "- sample text:",
            ]
        )
        for sample in item.samples:
            lines.append(f"  - `{sample.source_path}` -> {sample.text_preview or '[no text preview]'}")
        lines.append("")

    if payload.unknown_role_values:
        lines.append("## Unknown existing data-tp-role values")
        for item in payload.unknown_role_values:
            lines.append(
                f"- `{item.role}`: {item.count} occurrence(s) | sample paths: {', '.join(item.sample_paths)}"
            )
        lines.append("")

    lines.extend(
        [
            "## Required output",
            "For each signature, return:",
            "1. keep unlabeled / skip",
            "2. map to an existing canonical role",
            "3. propose a new canonical role with one-sentence justification",
            "",
            "Do not rename content. Do not rewrite text. This batch is for structural labeling only.",
        ]
    )
    return "\n".join(lines)


def write_label_payloads(report: SeriesReport) -> tuple[Path, Path] | None:
    if report.label_payload is None:
        return None

    payload_root = REPORT_ROOT / "label-batches"
    payload_root.mkdir(parents=True, exist_ok=True)

    json_path = payload_root / f"{report.series}.unknowns.json"
    md_path = payload_root / f"{report.series}.prompt.md"

    json_path.write_text(json.dumps(asdict(report.label_payload), indent=2), encoding="utf-8")
    md_path.write_text(render_label_prompt(report.label_payload), encoding="utf-8")
    return json_path, md_path


def render_summary(report: SeriesReport) -> str:
    lines = [
        f"Series: {report.series}",
        f"Root:   {report.root}",
        f"Pages:  {report.pages_scanned}",
        f"Clean:  {report.pages_clean}",
        f"Open:   {report.unresolved_pages} page(s), {report.unresolved_items} unresolved item(s)",
    ]

    if report.label_payload is not None:
        lines.append(
            "Labels: "
            f"{report.label_payload.unknown_signature_count} signature(s), "
            f"{report.label_payload.unknown_element_count} retained unknown element(s)"
        )

    if report.unresolved_pages:
        lines.append("Top unresolved pages:")
        shown = 0
        for finding in report.findings:
            if not finding.unresolved:
                continue
            joined = ", ".join(finding.unresolved)
            lines.append(f"  - {finding.path}: {joined}")
            shown += 1
            if shown >= 6:
                break

    return "\n".join(lines)


def build_cadence_state() -> CadenceState:
    return CadenceState(
        sequence=list(DEFAULT_CADENCE_SEQUENCE),
        floor=DEFAULT_CADENCE_FLOOR,
    )


def write_skip_ledger_entry(entry: SkipLedgerEntry) -> Path:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    out = REPORT_ROOT / "skip-ledger.jsonl"
    with out.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(entry)) + "\n")
    return out


def maybe_record_skip(args: argparse.Namespace) -> None:
    if not args.record_skip:
        return
    entry = SkipLedgerEntry(
        loop_name=args.loop_name,
        scheduled_for=datetime.now(timezone.utc).isoformat(),
        status=args.skip_status,
        reason=args.skip_reason,
        previous_failure=args.previous_failure,
        next_action=args.next_action,
    )
    out = write_skip_ledger_entry(entry)
    print(f"Skip ledger updated: {out}")


def resolve_series(args: argparse.Namespace) -> list[Path]:
    if args.series:
        roots = [SITE_ROOT / s for s in args.series]
    else:
        roots = [SITE_ROOT / s for s in DEFAULT_SERIES]
    return [r for r in roots if r.exists() and r.is_dir()]


def maybe_run_queue_actions(args: argparse.Namespace) -> int | None:
    if args.init_queues:
        created = ensure_queue_dirs()
        created.extend(ensure_prediction_dirs())
        gallery = build_gallery()
        queue_status = write_queue_status_report()
        print(f"Initialized queue directories: {len(created)}")
        print(f"Gallery: {gallery}")
        print(f"Queue status: {queue_status}")
        return 0

    if args.enqueue:
        series_roots = resolve_series(args)
        queued = enqueue_series_jobs(series_roots)
        gallery = build_gallery()
        queue_status = write_queue_status_report()
        print(f"Queued jobs: {len(queued)}")
        print(f"Gallery: {gallery}")
        print(f"Queue status: {queue_status}")
        return 0

    if args.queue_status:
        out = write_queue_status_report()
        print(f"Queue status: {out}")
        return 0

    if args.claim_stage:
        claimed = claim_next_job(args.claim_stage, args.worker)
        if claimed is None:
            print(f"No pending jobs available for stage: {args.claim_stage}")
            write_queue_status_report()
            return 0
        print(claimed)
        write_queue_status_report()
        return 0

    if args.complete_job:
        destination, next_jobs, gallery = complete_locked_job(
            locked_job_path=Path(args.complete_job),
            result=args.job_result,
            worker=args.worker,
            notes=args.job_notes,
            screenshot_source=args.screenshot_source,
        )
        print(f"Completed: {destination}")
        for next_job in next_jobs:
            print(f"Next stage queued: {next_job}")
        print(f"Gallery: {gallery}")
        queue_status = write_queue_status_report()
        print(f"Queue status: {queue_status}")
        return 0

    if args.build_gallery:
        gallery = build_gallery()
        print(f"Gallery: {gallery}")
        return 0

    if args.build_prediction_plan:
        ensure_prediction_dirs()
        plan = build_prediction_chain_plan()
        leaderboard = build_prediction_leaderboard()
        print(f"Prediction plan: {plan}")
        print(f"Leaderboard: {leaderboard}")
        return 0

    if args.log_prediction_run:
        ensure_prediction_dirs()
        run_payload = json.loads(Path(args.log_prediction_run).read_text(encoding="utf-8"))
        record = PredictionRunRecord(**run_payload)
        out = write_prediction_run(record)
        leaderboard = build_prediction_leaderboard()
        print(f"Prediction run stored: {out}")
        print(f"Leaderboard: {leaderboard}")
        return 0

    if args.record_actuals:
        ensure_prediction_dirs()
        actual_payload = json.loads(Path(args.record_actuals).read_text(encoding="utf-8"))
        out = append_prediction_actual(
            page_relpath=actual_payload["page_relpath"],
            actuals=actual_payload["actuals"],
        )
        print(f"Actuals appended: {out}")
        return 0

    if args.browser_audit:
        series_roots = resolve_series(args)
        targets = collect_browser_audit_targets(series_roots, limit=args.audit_limit)
        findings = asyncio.run(run_browser_audit_async(targets, base_url=args.audit_base_url))
        report_path, review_path = write_browser_audit_report(findings)
        print(f"Browser audit report: {report_path}")
        print(f"Browser audit review queue: {review_path}")
        return 0

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold the repeatable website master loop.")
    parser.add_argument(
        "--series",
        nargs="*",
        help="Optional series folder names under the site root.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write JSON reports under reports/site-master-loop.",
    )
    parser.add_argument(
        "--write-payloads",
        action="store_true",
        help="Write per-series label unknown payloads and prompt markdown.",
    )
    parser.add_argument(
        "--init-queues",
        action="store_true",
        help="Create the multi-stage worker queue folders and screenshot gallery shell.",
    )
    parser.add_argument(
        "--enqueue",
        action="store_true",
        help="Queue all matching series pages into the labels stage pending folder.",
    )
    parser.add_argument(
        "--claim-stage",
        choices=PIPELINE_STAGES,
        help="Atomically claim the next job from the given stage pending queue.",
    )
    parser.add_argument(
        "--complete-job",
        help="Complete a locked job file and optionally advance it to the next stage.",
    )
    parser.add_argument(
        "--job-result",
        choices=["done", "failed"],
        default="done",
        help="Result when completing a locked job.",
    )
    parser.add_argument(
        "--job-notes",
        default="",
        help="Optional notes to append to the job history when completing a job.",
    )
    parser.add_argument(
        "--worker",
        default="worker-1",
        help="Worker identifier for claim and completion events.",
    )
    parser.add_argument(
        "--screenshot-source",
        help="Optional URL or local HTML path to capture on job completion.",
    )
    parser.add_argument(
        "--build-gallery",
        action="store_true",
        help="Rebuild the screenshot gallery HTML from current PNG outputs.",
    )
    parser.add_argument(
        "--queue-status",
        action="store_true",
        help="Write queue-status.json showing per-stage counts, unlock state, and lead thresholds.",
    )
    parser.add_argument(
        "--browser-audit",
        action="store_true",
        help="Run a browser-side audit for white pages, JS errors, request failures, and missing shell runtime elements.",
    )
    parser.add_argument(
        "--audit-limit",
        type=int,
        help="Optional cap on how many pages browser-audit should visit.",
    )
    parser.add_argument(
        "--audit-base-url",
        help="Optional base URL for browser-audit, such as http://127.0.0.1:8792 or a deployed site URL.",
    )
    parser.add_argument(
        "--build-prediction-plan",
        action="store_true",
        help="Build the prediction ensemble chain plan and refresh the leaderboard file.",
    )
    parser.add_argument(
        "--log-prediction-run",
        help="Path to a JSON file matching PredictionRunRecord to append to the ensemble run log.",
    )
    parser.add_argument(
        "--record-actuals",
        help="Path to a JSON file with page_relpath and actuals to append to the actuals ledger.",
    )
    parser.add_argument(
        "--record-skip",
        action="store_true",
        help="Write a skip ledger entry instead of silently missing a scheduled pass.",
    )
    parser.add_argument(
        "--loop-name",
        default="site_master_loop",
        help="Name of the loop when writing a skip entry.",
    )
    parser.add_argument(
        "--skip-status",
        default="deferred",
        help="Skip status: skipped, blocked, or deferred.",
    )
    parser.add_argument(
        "--skip-reason",
        default="no reason provided",
        help="Reason the pass did not run.",
    )
    parser.add_argument(
        "--previous-failure",
        default="not recorded",
        help="What went wrong the last time.",
    )
    parser.add_argument(
        "--next-action",
        default="retry on next cadence slot",
        help="What should happen next.",
    )
    args = parser.parse_args()
    queue_result = maybe_run_queue_actions(args)
    if queue_result is not None:
        return queue_result

    maybe_record_skip(args)

    cadence = build_cadence_state()
    next_interval = cadence.next_interval()
    registry = load_registry()

    series_roots = resolve_series(args)
    if not series_roots:
        print("No matching series roots found.")
        return 1

    total_pages = 0
    total_open = 0
    total_unknown_signatures = 0

    for series_root in series_roots:
        report = build_series_report(
            series_root,
            registry=registry,
            include_payloads=args.write or args.write_payloads,
        )
        total_pages += report.pages_scanned
        total_open += report.unresolved_items
        if report.label_payload is not None:
            total_unknown_signatures += report.label_payload.unknown_signature_count

        print("=" * 72)
        print(render_summary(report))
        if args.write:
            out = write_report(report)
            print(f"Report: {out}")
        if args.write_payloads:
            payload_paths = write_label_payloads(report)
            if payload_paths:
                print(f"Label payloads: {payload_paths[0]}")
                print(f"Prompt markdown: {payload_paths[1]}")

    print("=" * 72)
    print(f"Total pages scanned: {total_pages}")
    print(f"Total unresolved items: {total_open}")
    print(f"Total retained unknown signatures: {total_unknown_signatures}")
    print("Loop shape: scan -> batch unresolved -> fix -> verify -> repeat")
    print(f"Next cadence interval: {next_interval} (floor={cadence.floor}, sequence={cadence.sequence})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
