/**
 * faith-mtl-worker
 * Serves math translation layer (MTL) equation translations from D1.
 *
 * API:
 *   GET /health
 *   GET /api/translate?latex=<latex>&mode=easy|standard|academic|audio_safe
 *   POST /api/batch  { latexList: [...], mode: "easy" }
 */

const DEFAULT_MODE = "easy";
const ALLOWED_MODES = new Set(["easy", "standard", "academic", "audio_safe"]);

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json"
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: corsHeaders() });
}

function optionalString(value) {
  if (value === undefined || value === null) return "";
  return String(value).trim();
}

function normalizeLatex(value) {
  const text = optionalString(value)
    .replace(/^\$+/, "")
    .replace(/\$+$/, "")
    .replace(/^\\\(|\\\)$/g, "")
    .replace(/^\\\[|\\\]$/g, "")
    .trim();
  return text;
}

async function sha256Hex(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
}

function cleanMode(value) {
  const text = optionalString(value).toLowerCase();
  if (ALLOWED_MODES.has(text)) return text;
  return DEFAULT_MODE;
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders() });
    }

    const url = new URL(request.url);

    try {
      if (url.pathname === "/health" && request.method === "GET") {
        return json({ ok: true, service: "faith-mtl-worker" });
      }

      if (url.pathname === "/api/translate" && request.method === "GET") {
        return await handleTranslate(request, env);
      }

      if (url.pathname === "/api/batch" && request.method === "POST") {
        return await handleBatch(request, env);
      }

      return json({ error: "Not found" }, 404);
    } catch (error) {
      console.error(JSON.stringify({ level: "error", path: url.pathname, message: error.message }));
      return json({ error: error.message || "Internal server error" }, 500);
    }
  }
};

async function handleTranslate(request, env) {
  const url = new URL(request.url);
  const rawLatex = url.searchParams.get("latex");
  const latex = normalizeLatex(rawLatex);
  const mode = cleanMode(url.searchParams.get("mode"));

  if (!latex) {
    return json({ error: "Missing ?latex parameter" }, 400);
  }

  const hash = await sha256Hex(latex);
  const row = await env.DB.prepare(
    `SELECT eq_id, latex_hash, latex, easy, standard, academic, audio_safe,
            source, source_file, difficulty, paper_ref
     FROM mtl_equations
     WHERE latex_hash = ?
     LIMIT 1`
  ).bind(hash).first();

  if (!row) {
    return json({
      found: false,
      latex_hash: hash,
      mode,
      translation: null,
      fallback: latex
    });
  }

  return json({
    found: true,
    eq_id: row.eq_id,
    latex_hash: row.latex_hash,
    mode,
    translation: row[mode] || row.easy || null,
    latex: row.latex,
    source: row.source,
    source_file: row.source_file,
    difficulty: row.difficulty,
    paper_ref: row.paper_ref
  });
}

async function handleBatch(request, env) {
  const body = await readJson(request);
  const latexList = Array.isArray(body.latexList) ? body.latexList : [];
  const mode = cleanMode(body.mode);

  if (latexList.length === 0) {
    return json({ error: "Missing latexList array" }, 400);
  }
  if (latexList.length > 50) {
    return json({ error: "Batch limit is 50 equations" }, 400);
  }

  const results = {};
  for (const raw of latexList) {
    const latex = normalizeLatex(raw);
    if (!latex) continue;
    const hash = await sha256Hex(latex);
    const row = await env.DB.prepare(
      `SELECT eq_id, latex_hash, latex, easy, standard, academic, audio_safe,
              source, source_file, difficulty, paper_ref
       FROM mtl_equations
       WHERE latex_hash = ?
       LIMIT 1`
    ).bind(hash).first();

    results[latex] = row
      ? {
          found: true,
          eq_id: row.eq_id,
          latex_hash: row.latex_hash,
          mode,
          translation: row[mode] || row.easy || null,
          latex: row.latex,
          source: row.source,
          source_file: row.source_file,
          difficulty: row.difficulty,
          paper_ref: row.paper_ref
        }
      : {
          found: false,
          latex_hash: hash,
          mode,
          translation: null,
          fallback: latex
        };
  }

  return json({ mode, count: Object.keys(results).length, results });
}

async function readJson(request) {
  try {
    return await request.json();
  } catch {
    throw new Error("Expected JSON body");
  }
}
