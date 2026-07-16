from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_TOP = ROOT / "shell-top.html"
DEFAULT_CONTENT = ROOT / "content-slot.example.html"
DEFAULT_BOTTOM = ROOT / "shell-bottom.html"
DEFAULT_FULL = ROOT / "index-shell-v2.5.1.full.html"

CONTENT_START = "<!-- FTP_CONTENT_SLOT:START"
CONTENT_END = "<!-- FTP_CONTENT_SLOT:END -->"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def assemble(top: Path, content: Path, bottom: Path, out: Path) -> None:
    write(out, read(top) + read(content) + read(bottom))


def split(full: Path, out_dir: Path) -> None:
    html = read(full)
    start = html.index(CONTENT_START)
    end = html.index(CONTENT_END, start) + len(CONTENT_END)
    write(out_dir / "shell-top.html", html[:start])
    write(out_dir / "content-slot.example.html", html[start:end])
    write(out_dir / "shell-bottom.html", html[end:])


def check(top: Path, content: Path, bottom: Path, full: Path) -> None:
    assembled = read(top) + read(content) + read(bottom)
    expected = read(full)
    if assembled != expected:
        raise SystemExit("FAIL: top + content + bottom does not exactly match full shell")
    print("OK: top + content + bottom exactly matches full shell")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble or split the canonical FTP page shell.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_assemble = sub.add_parser("assemble")
    p_assemble.add_argument("--top", type=Path, default=DEFAULT_TOP)
    p_assemble.add_argument("--content", type=Path, default=DEFAULT_CONTENT)
    p_assemble.add_argument("--bottom", type=Path, default=DEFAULT_BOTTOM)
    p_assemble.add_argument("--out", type=Path, required=True)

    p_split = sub.add_parser("split")
    p_split.add_argument("--full", type=Path, default=DEFAULT_FULL)
    p_split.add_argument("--out-dir", type=Path, default=ROOT)

    p_check = sub.add_parser("check")
    p_check.add_argument("--top", type=Path, default=DEFAULT_TOP)
    p_check.add_argument("--content", type=Path, default=DEFAULT_CONTENT)
    p_check.add_argument("--bottom", type=Path, default=DEFAULT_BOTTOM)
    p_check.add_argument("--full", type=Path, default=DEFAULT_FULL)

    args = parser.parse_args()
    if args.cmd == "assemble":
        assemble(args.top, args.content, args.bottom, args.out)
    elif args.cmd == "split":
        split(args.full, args.out_dir)
    elif args.cmd == "check":
        check(args.top, args.content, args.bottom, args.full)


if __name__ == "__main__":
    main()
