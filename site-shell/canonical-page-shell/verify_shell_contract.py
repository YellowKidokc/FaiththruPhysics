from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "shell-contract.v2.5.1.json"
DEFAULT_TOP = ROOT / "shell-top.html"
DEFAULT_CONTENT = ROOT / "content-slot.example.html"
DEFAULT_BOTTOM = ROOT / "shell-bottom.html"
DEFAULT_FULL = ROOT / "index-shell-v2.5.1.full.html"

CONTENT_START = "<!-- FTP_CONTENT_SLOT:START"
CONTENT_END = "<!-- FTP_CONTENT_SLOT:END"


@dataclass
class PieceStats:
    chars: int
    bytes: int
    sha256: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def stats(text: str) -> PieceStats:
    raw = text.encode("utf-8")
    return PieceStats(chars=len(text), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def piece_record(path: Path) -> dict[str, object]:
    text = read(path)
    s = stats(text)
    return {"path": str(path), "chars": s.chars, "bytes": s.bytes, "sha256": s.sha256}


def split_page(html: str) -> tuple[str, str, str]:
    start = html.index(CONTENT_START)
    start_line_end = html.index("\n", start) + 1
    end = html.index(CONTENT_END, start_line_end)
    return html[:start_line_end], html[start_line_end:end], html[end:]


def make_manifest() -> dict[str, object]:
    return {
        "contract": "ftp-shell-v2.5.1",
        "notes": [
            "shell-top.html and shell-bottom.html are canonical and should be byte-for-byte stable.",
            "content-slot.example.html is the swappable page/data layer.",
            "Use SHA-256 plus length checks; character count alone is not enough.",
        ],
        "pieces": {
            "top": piece_record(DEFAULT_TOP),
            "content_example": piece_record(DEFAULT_CONTENT),
            "bottom": piece_record(DEFAULT_BOTTOM),
            "full": piece_record(DEFAULT_FULL),
        },
        "required_content_signals": [
            "id=\"shell-data\"",
            "data-reader-layer=\"highschool\"",
            "data-reader-layer=\"college\"",
            "data-reader-layer=\"phd\"",
            "ftp-claim-sentence",
            "ftp-mtl",
        ],
        "required_top_signals": [
            "id=\"ftpTopBar\"",
            "id=\"ftpPanel\"",
            "id=\"ftpPlayerBand\"",
            "FTP_CONTENT_SLOT:START",
        ],
        "required_bottom_signals": [
            "FTP_CONTENT_SLOT:END",
            "Proof Layer",
            "MTL Layer",
            "window.ftp",
            "DOMContentLoaded",
        ],
    }


def save_manifest(path: Path) -> None:
    manifest = make_manifest()
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


def compare_piece(name: str, text: str, expected: dict[str, object], errors: list[str]) -> None:
    actual = stats(text)
    if actual.chars != expected["chars"]:
        errors.append(f"{name}: char count mismatch actual={actual.chars} expected={expected['chars']}")
    if actual.bytes != expected["bytes"]:
        errors.append(f"{name}: byte count mismatch actual={actual.bytes} expected={expected['bytes']}")
    if actual.sha256 != expected["sha256"]:
        errors.append(f"{name}: sha256 mismatch actual={actual.sha256} expected={expected['sha256']}")


def require_signals(name: str, text: str, signals: list[str], errors: list[str]) -> None:
    for signal in signals:
        if signal not in text:
            errors.append(f"{name}: missing required signal {signal!r}")


def validate_json_payload(content: str, errors: list[str]) -> None:
    match = re.search(r'<script[^>]*id="shell-data"[^>]*>\s*(.*?)\s*</script>', content, re.S)
    if not match:
        errors.append("content: missing shell-data JSON script")
        return
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"content: invalid shell-data JSON: {exc}")
        return

    for key in ("page", "verification", "claims", "proofs", "mtl", "audio"):
        if key not in data:
            errors.append(f"content JSON: missing key {key!r}")

    audio = data.get("audio", [])
    kinds = {item.get("kind") for item in audio if isinstance(item, dict)}
    for required in ("tts", "debate", "deep_dive", "critique"):
        if required not in kinds:
            errors.append(f"content JSON: missing audio kind {required!r}")


def check_page(path: Path, manifest_path: Path, strict_content: bool = False) -> int:
    manifest = json.loads(read(manifest_path))
    html = read(path)
    errors: list[str] = []

    try:
        top, content, bottom = split_page(html)
    except ValueError as exc:
        print(f"FAIL {path}")
        print(f"- page: missing content slot boundary: {exc}")
        return 1

    compare_piece("top", top, manifest["pieces"]["top"], errors)
    compare_piece("bottom", bottom, manifest["pieces"]["bottom"], errors)
    if strict_content:
        compare_piece("content", content, manifest["pieces"]["content_example"], errors)

    require_signals("top", top, manifest["required_top_signals"], errors)
    require_signals("content", content, manifest["required_content_signals"], errors)
    require_signals("bottom", bottom, manifest["required_bottom_signals"], errors)
    validate_json_payload(content, errors)

    if errors:
        print(f"FAIL {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK {path}")
    print(f"- top chars: {len(top)}")
    print(f"- content chars: {len(content)}")
    print(f"- bottom chars: {len(bottom)}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the FTP v2.5.1 shell contract.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_manifest = sub.add_parser("manifest", help="Write a manifest from the current canonical pieces.")
    p_manifest.add_argument("--out", type=Path, default=DEFAULT_MANIFEST)

    p_check = sub.add_parser("check", help="Check a page against the canonical top/bottom shell contract.")
    p_check.add_argument("page", type=Path)
    p_check.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p_check.add_argument("--strict-content", action="store_true", help="Also require the content slot to match the example exactly.")

    args = parser.parse_args()
    if args.cmd == "manifest":
        save_manifest(args.out)
    elif args.cmd == "check":
        raise SystemExit(check_page(args.page, args.manifest, args.strict_content))


if __name__ == "__main__":
    main()
