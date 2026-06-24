#!/usr/bin/env python3
"""Serve the site plus local media files for launch-preview playback."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


AUDIO_EXTENSIONS = {".mp3", ".m4a", ".aac", ".wav", ".ogg", ".flac"}


def load_audio_index(site_root: Path) -> tuple[dict[str, dict], dict[str, list[dict]], Path]:
    manifest_path = site_root / "assets" / "media-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    data_root = Path(manifest["dataRoot"])
    by_id: dict[str, dict] = {}
    by_slug: dict[str, list[dict]] = {}
    for item in manifest.get("items", []):
        if item.get("kind") != "audio":
            continue
        if item.get("extension", "").lower() not in {ext[1:] for ext in AUDIO_EXTENSIONS}:
            continue
        media_id = item["id"]
        source_path = data_root / item["relativePath"]
        if not source_path.exists():
            stage_path = Path(item.get("stagePath", ""))
            source_path = stage_path if stage_path.exists() else source_path
        record = {
            "id": media_id,
            "title": item.get("title") or item.get("slug") or media_id,
            "slug": item.get("slug"),
            "mode": item.get("mode") or "tts",
            "url": f"/__local_media/{media_id}",
            "mimeType": item.get("mimeType") or mimetypes.guess_type(source_path.name)[0] or "audio/mpeg",
            "sourcePath": str(source_path),
            "r2Key": item.get("r2Key"),
            "publicUrl": item.get("publicUrl"),
        }
        by_id[media_id] = record
        by_slug.setdefault(record["slug"], []).append(record)
    return by_id, by_slug, data_root


class LaunchPreviewHandler(SimpleHTTPRequestHandler):
    by_id: dict[str, dict] = {}
    by_slug: dict[str, list[dict]] = {}

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/__media_lookup":
            self.send_media_lookup(parsed.query)
            return
        if parsed.path.startswith("/__local_media/"):
            media_id = unquote(parsed.path.removeprefix("/__local_media/"))
            self.send_local_media(media_id)
            return
        super().do_GET()

    def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_media_lookup(self, query: str) -> None:
        slug = parse_qs(query).get("slug", [""])[0]
        tracks = list(self.by_slug.get(slug, []))
        if not tracks:
            tracks = [
                record
                for item_slug, records in self.by_slug.items()
                if item_slug and (item_slug.startswith(slug) or slug.startswith(item_slug))
                for record in records
            ][:8]
        public_tracks = [
            {key: value for key, value in record.items() if key != "sourcePath"}
            for record in tracks
        ]
        self.send_json({"tracks": public_tracks})

    def send_local_media(self, media_id: str) -> None:
        record = self.by_id.get(media_id)
        if not record:
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown media id")
            return
        source_path = Path(record["sourcePath"])
        if not source_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Media source missing")
            return
        size = source_path.stat().st_size
        range_header = self.headers.get("Range")
        start, end = 0, size - 1
        status = HTTPStatus.OK
        if range_header and range_header.startswith("bytes="):
            raw_start, _, raw_end = range_header.removeprefix("bytes=").partition("-")
            start = int(raw_start or 0)
            end = int(raw_end or end)
            end = min(end, size - 1)
            status = HTTPStatus.PARTIAL_CONTENT
        length = max(0, end - start + 1)
        self.send_response(status)
        self.send_header("Content-Type", record["mimeType"])
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        if status == HTTPStatus.PARTIAL_CONTENT:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with source_path.open("rb") as handle:
            handle.seek(start)
            remaining = length
            while remaining:
                chunk = handle.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    site_root = args.site_root.resolve()
    by_id, by_slug, data_root = load_audio_index(site_root)
    LaunchPreviewHandler.by_id = by_id
    LaunchPreviewHandler.by_slug = by_slug
    os.chdir(site_root)
    server = ThreadingHTTPServer((args.host, args.port), LaunchPreviewHandler)
    print(f"Serving {site_root} at http://{args.host}:{args.port}/")
    print(f"Local audio preview index: {len(by_id)} tracks from {data_root}")
    server.serve_forever()


if __name__ == "__main__":
    main()
