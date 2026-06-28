#!/usr/bin/env python3
"""
Post messages to the Synology Chat crew workspace.

Usage:
  python scripts/notify_crew.py "Your message here"
  python scripts/notify_crew.py "Your message here" --channel broadcast
"""

import argparse
import json
import ssl
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "webhook-config.json"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def get_webhook_url(config, channel="kimi"):
    if channel == "broadcast":
        return config.get("broadcast_webhook", {}).get("url")
    return config.get("crew_webhook", {}).get("url")


def post_message(text, channel="kimi"):
    config = load_config()
    url = get_webhook_url(config, channel)
    if not url:
        raise SystemExit(f"No webhook URL configured for channel: {channel}")

    payload = json.dumps({"text": text})
    data = urllib.parse.urlencode({"payload": payload}).encode("utf-8")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return resp.status, resp.read().decode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Message text to post")
    parser.add_argument("--channel", default="kimi", choices=["kimi", "broadcast"], help="Channel to post to")
    args = parser.parse_args()

    status, body = post_message(args.message, channel=args.channel)
    print(f"Posted to {args.channel}: HTTP {status}")
    print(body)


if __name__ == "__main__":
    main()
