#!/usr/bin/env python3
"""
Generate a triage report from Open-AI-CALL response files.

Usage:
  python scripts/generate_api_response_report.py
"""

import re
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
API_ROOT = Path(r"D:\GitHub\Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr")
OUT = ROOT / "work" / "api-response-triage-report.md"


def parse_metadata(text: str):
    meta = {}
    # Parse HTML comment metadata
    m = re.search(r"<!--\s*(.*?)\s*-->", text, re.DOTALL)
    if m:
        comment = m.group(1)
        for line in comment.strip().splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip().lower()] = val.strip()
    return meta


def parse_content(text: str):
    # Remove HTML comment metadata
    content = re.sub(r"<!--\s*.*?\s*-->", "", text, flags=re.DOTALL, count=1).strip()
    # Collapse whitespace
    content = re.sub(r"\s+", " ", content)
    return content


def main():
    records = []

    for outbox in sorted(API_ROOT.glob("api_call_*/outbox")):
        call_name = outbox.parent.name
        for resp_file in sorted(outbox.glob("*.response.md")):
            text = resp_file.read_text(encoding="utf-8", errors="ignore")
            meta = parse_metadata(text)
            content = parse_content(text)
            article = resp_file.stem.replace(".response", "")
            records.append({
                "call": call_name,
                "article": article,
                "source_html": (resp_file.with_name(f"{article}.input.html")).name,
                "provider": meta.get("provider", ""),
                "model": meta.get("model", ""),
                "finished": meta.get("finished", ""),
                "tokens_in": meta.get("tokens", "").split("/")[0].strip() if "tokens" in meta else "",
                "tokens_out": meta.get("tokens", "").split("/")[1].strip() if "tokens" in meta and "/" in meta.get("tokens", "") else "",
                "cost": meta.get("est cost", ""),
                "seconds": meta.get("seconds", ""),
                "summary": content,
                "word_count": len(content.split()),
            })

    records.sort(key=lambda r: (r["call"], r["article"]))

    lines = [
        "# API Response Triage Report",
        f"Generated: {datetime.now().isoformat()}",
        f"Source: {API_ROOT}",
        f"Total responses: {len(records)}",
        "",
        "## Summary by API call",
        "",
    ]

    by_call = {}
    for r in records:
        by_call.setdefault(r["call"], []).append(r)

    for call, items in sorted(by_call.items()):
        lines.append(f"- **{call}**: {len(items)} responses")
    lines.append("")

    # Quick quality flags
    empty_count = sum(1 for r in records if r["word_count"] < 5)
    short_count = sum(1 for r in records if 5 <= r["word_count"] < 30)
    good_count = sum(1 for r in records if r["word_count"] >= 30)

    lines.extend([
        "## Quality flags",
        "",
        f"- Empty / near-empty (< 5 words): {empty_count}",
        f"- Short (5–29 words): {short_count}",
        f"- Substantial (≥ 30 words): {good_count}",
        "",
        "---",
        "",
        "## Detailed responses",
        "",
    ])

    for r in records:
        lines.extend([
            f"### {r['article']} ({r['call']})",
            "",
            f"- **Provider:** {r['provider']}",
            f"- **Model:** {r['model']}",
            f"- **Finished:** {r['finished']}",
            f"- **Tokens:** {r['tokens_in']} in / {r['tokens_out']} out",
            f"- **Cost:** {r['cost']}",
            f"- **Seconds:** {r['seconds']}",
            f"- **Word count:** {r['word_count']}",
            "",
            "**Summary:**",
            "",
            r["summary"][:800] + ("..." if len(r["summary"]) > 800 else ""),
            "",
            "---",
            "",
        ])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Total responses: {len(records)}")
    print(f"Empty: {empty_count}, Short: {short_count}, Good: {good_count}")


if __name__ == "__main__":
    main()
