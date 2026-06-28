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

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: CORS_HEADERS });
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
      let slug = url.searchParams.get("slug");
      const mode = url.searchParams.get("mode");

      // Normalize path-style slugs: "genesis-to-quantum/gtq-01-foo" → "gtq-01-foo"
      // Pages send folder/filename slugs but D1 stores bare article slugs.
      if (slug && slug.includes("/")) {
        slug = slug.split("/").pop();
      }

      if (!slug) {
        return json({ error: "Missing ?slug parameter" }, 400);
      }

      try {
        let stmt, result;
        if (mode) {
          stmt = env.DB.prepare(
            "SELECT * FROM audio_tracks WHERE article_slug = ? AND mode = ? LIMIT 1"
          ).bind(slug, mode);
          result = await stmt.first();
          if (!result) {
            // Fallback to default track for this article if the requested mode is missing.
            result = await env.DB.prepare(
              "SELECT * FROM audio_tracks WHERE article_slug = ? AND is_default = TRUE LIMIT 1"
            ).bind(slug).first();
          }
          return json({ track: result });
        } else {
          stmt = env.DB.prepare(
            "SELECT id, article_slug, series, mode, url, title, duration_seconds, transcript_url, is_default FROM audio_tracks WHERE article_slug = ? ORDER BY mode"
          ).bind(slug);
          const { results } = await stmt.all();
          return json({ tracks: results });
        }
      } catch (err) {
        return json({ error: err.message }, 500);
      }
    }

    return json({ error: "Not found" }, 404);
  }
};
