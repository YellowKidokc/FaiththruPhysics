# Webhook Endpoints

## Synology Chat Workspace

Local NAS: `https://192.168.1.177:2349`

### Kimi Channel Webhook

| Property | Value |
|----------|-------|
| Channel | `#kimi` |
| Channel ID | `12` |
| Service | Synology Chat External |
| URL | `https://192.168.1.177:2349/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%2223ffFkrFQQ0O9al4Z8J8jQ61qZnFBhHSuEdS1xC70JfO9GUaOrZ9q1Ku4sM0auZ0%22` |
| Type | `synology_chat` |
| API | `SYNO.Chat.External` |
| Method | `incoming` |
| Version | `2` |

### Broadcast Channel Webhook

| Property | Value |
|----------|-------|
| Channel | `#broadcast` |
| Channel ID | `15` |
| Service | Synology Chat External |
| URL | `https://192.168.1.177:2349/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%2223ffFkrFQQ0O9al4Z8J8jQ61qZnFBhHSuEdS1xC70JfO9GUaOrZ9q1Ku4sM0auZ0%22` |

### Read Access (optional)

| Property | Value |
|----------|-------|
| Bot token | `Ne20eMUR4cz8x6BBnZd41bt6YD5ucwSZnh7Mp9ktwDHJAEtwQpz6HiQmAzxhdFX1` |
| Read endpoint | `GET https://192.168.1.177:2349/webapi/entry.cgi?api=SYNO.Chat.External&method=chatbot&version=2&token=BOT_TOKEN&channel_id=CHANNEL_ID` |

### Sending a Message

Use the helper script:

```bash
python scripts/notify_crew.py "Your message here"
python scripts/notify_crew.py "Your message here" --channel broadcast
```

Or with curl (self-signed cert — use `-k`):

```bash
curl -k -X POST "https://192.168.1.177:2349/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=YOUR_TOKEN" \
  --data-urlencode 'payload={"text": "Your message here"}'
```

### Files where these webhooks are stored

- `webhook-config.json`
- `docs/webhook-endpoints.md`
