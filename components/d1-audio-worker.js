/**
 * Cloudflare Worker + D1 example for serving audio track metadata.
 *
 * Bindings required in wrangler.toml:
 *   [[d1_databases]]
 *   binding = "DB"
 *   database_name = "faiththruphysics-audio"
 *   database_id = "<your-database-id>"
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json"
};

const MODE_ALIASES = {
  read: "read",
  tts: "read",
  "read-aloud": "read",
  narrated: "read",
  podcast: "podcast",
  debate: "podcast",
  dbt: "podcast",
  pod: "podcast",
  deep: "deep",
  "deep-dive": "deep",
  critique: "critique",
  critical: "critique",
  review: "critique"
};

const LEGACY_MODE_ALIASES = {
  read: ["read", "tts"],
  podcast: ["podcast", "debate"],
  deep: ["deep"],
  critique: ["critique"]
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: CORS_HEADERS });
}

function normalizeMode(mode) {
  const key = String(mode || "").trim().toLowerCase().replace(/_/g, "-");
  return MODE_ALIASES[key] || "";
}

function normalizeSlug(slug) {
  return String(slug || "")
    .trim()
    .replace(/\\/g, "/")
    .replace(/^\/+|\/+$/g, "")
    .replace(/\.html$/i, "")
    .split("/")
    .filter(Boolean)
    .map((part) =>
      part
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "")
    )
    .filter(Boolean)
    .join("/");
}

function slugCandidates(slug) {
  const normalized = normalizeSlug(slug);
  const bare = normalized.includes("/") ? normalized.split("/").pop() : normalized;
  return Array.from(new Set([normalized, bare].filter(Boolean)));
}

function normalizeTrack(row) {
  if (!row) return null;
  const mode = normalizeMode(row.mode);
  if (!mode) return null;
  return { ...row, mode };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    if (path === "/health") {
      return json({ status: "ok", timestamp: new Date().toISOString() });
    }

    if (path === "/api/audio") {
      const slug = normalizeSlug(url.searchParams.get("slug"));
      const mode = normalizeMode(url.searchParams.get("mode"));

      if (!slug) {
        return json({ error: "Missing ?slug parameter" }, 400);
      }

      const slugs = slugCandidates(slug);
      const primarySlug = slugs[0];
      const fallbackSlug = slugs[1] || slugs[0];

      try {
        let stmt;
        let result;

        if (mode) {
          const modes = LEGACY_MODE_ALIASES[mode] || [mode];
          stmt = env.DB.prepare(
            `SELECT *
             FROM audio_tracks
             WHERE (article_slug = ? OR article_slug = ?)
               AND (mode = ? OR mode = ?)
             ORDER BY CASE WHEN article_slug = ? THEN 0 ELSE 1 END
             LIMIT 1`
          ).bind(primarySlug, fallbackSlug, modes[0], modes[1] || modes[0], slug);

          result = normalizeTrack(await stmt.first());

          if (!result) {
            result = normalizeTrack(
              await env.DB.prepare(
                `SELECT *
                 FROM audio_tracks
                 WHERE (article_slug = ? OR article_slug = ?)
                   AND is_default = TRUE
                 ORDER BY CASE WHEN article_slug = ? THEN 0 ELSE 1 END
                 LIMIT 1`
              ).bind(primarySlug, fallbackSlug, slug).first()
            );
          }

          return json({ track: result });
        }

        stmt = env.DB.prepare(
          `SELECT id, article_slug, series, mode, url, title, duration_seconds, transcript_url, is_default
           FROM audio_tracks
           WHERE article_slug = ? OR article_slug = ?
           ORDER BY CASE WHEN article_slug = ? THEN 0 ELSE 1 END, mode`
        ).bind(primarySlug, fallbackSlug, slug);

        const { results } = await stmt.all();
        const byMode = new Map();

        for (const row of results || []) {
          const track = normalizeTrack(row);
          if (track && !byMode.has(track.mode)) byMode.set(track.mode, track);
        }

        return json({ tracks: Array.from(byMode.values()) });
      } catch (err) {
        return json({ error: err.message }, 500);
      }
    }

    return json({ error: "Not found" }, 404);
  }
};
