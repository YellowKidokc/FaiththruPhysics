# OpenIntel — Cloudflare Workers + D1 Deployment Guide

## Overview

OpenIntel now runs as two Cloudflare services:

1. **Cloudflare Pages** — hosts the static React frontend (already in `subdomains/rigor/openintel-platform/`).
2. **Cloudflare Worker + D1** — hosts the TRPC API and OAuth callback.

## Prerequisites

- Cloudflare account
- Wrangler CLI authenticated: `npx wrangler login`
- Kimi OAuth app credentials (`APP_ID`, `APP_SECRET`, `KIMI_AUTH_URL`, `KIMI_OPEN_URL`)

## Step 1 — Create the D1 Database

```bash
npx wrangler d1 create openintel-db
```

Copy the `database_id` into `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "openintel-db"
database_id = "<your-database-id>"
```

## Step 2 — Set Secrets

```bash
npx wrangler secret put APP_ID
npx wrangler secret put APP_SECRET
npx wrangler secret put KIMI_AUTH_URL
npx wrangler secret put KIMI_OPEN_URL
npx wrangler secret put OWNER_UNION_ID
```

## Step 3 — Generate and Apply Migrations

```bash
npx drizzle-kit generate
npx wrangler d1 migrations apply openintel-db
```

## Step 4 — Seed the Database

After the Worker is running, trigger the seed endpoint:

```bash
curl -X POST https://<your-worker-host>/seed
```

Or run locally first:

```bash
npx wrangler dev
```

Then seed: `curl -X POST http://localhost:8787/seed`

## Step 5 — Deploy the Worker

```bash
npx wrangler deploy
```

Note the Worker URL (e.g. `https://openintel-api.your-account.workers.dev`).

## Step 6 — Connect the Frontend

Set the API endpoint in Cloudflare Pages environment variables (or in a local `.env` before rebuilding):

```bash
VITE_TRPC_API_URL=https://openintel-api.your-account.workers.dev/api/trpc
VITE_OAUTH_CALLBACK_URL=https://openintel-api.your-account.workers.dev/api/oauth/callback
```

If you want the frontend and API on the **same origin**, add a Worker route in the Cloudflare dashboard:

- Route: `faiththruphysics.com/api/trpc*` and `faiththruphysics.com/api/oauth/callback`
- Service: `openintel-api`

Then leave `VITE_TRPC_API_URL` unset (defaults to `/api/trpc`).

## Step 7 — Rebuild and Push the Frontend

```bash
npm run build
```

Copy `dist/public/` assets into `subdomains/rigor/openintel-platform/` if needed, then commit and push. Cloudflare Pages will redeploy automatically.
