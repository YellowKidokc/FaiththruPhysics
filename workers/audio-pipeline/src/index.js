const DEFAULT_MODEL = "@cf/deepgram/aura-2-en";
const DEFAULT_SPEAKER = "luna";
const DEFAULT_MAX_TEXT_CHARS = 12000;
const DEFAULT_CHUNK_CHARS = 1800;

const SUPPORTED_SPEAKERS = new Set([
  "luna",
  "orpheus",
  "athena",
  "apollo",
  "atlas",
  "aurora",
  "hera",
  "hermes",
  "odysseus",
  "thalia",
  "zeus"
]);

const EXCLUDE_SELECTOR = [
  "script",
  "style",
  "noscript",
  "nav",
  "header",
  "footer",
  "audio",
  "video",
  "form",
  "button",
  "table",
  "[data-tts-exclude]",
  ".tp-pill-player",
  ".tp-pill-bar",
  ".site-shell",
  ".top-nav",
  ".bottom-nav",
  ".footnotes",
  ".references",
  ".citations",
  ".definition",
  ".definitions",
  ".glossary"
].join(",");

const SOURCE_SELECTOR = [
  "[data-tts-source]",
  "main",
  "article",
  "#main-content",
  ".main",
  ".content"
].join(",");

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(env) });
    }

    try {
      if (url.pathname === "/health" && request.method === "GET") {
        return json(env, { ok: true, service: "faith-audio-pipeline" });
      }

      if (url.pathname === "/api/audio" && request.method === "GET") {
        return handleAudioLookup(request, env);
      }

      if (url.pathname.startsWith("/audio/") && request.method === "GET") {
        return handleAudioFile(request, env);
      }

      if (url.pathname === "/api/extract" && request.method === "POST") {
        await requireAdmin(request, env);
        return handleExtract(request, env);
      }

      if (url.pathname === "/api/generate" && request.method === "POST") {
        await requireAdmin(request, env);
        return handleGenerate(request, env, ctx);
      }

      if (url.pathname === "/api/register" && request.method === "POST") {
        await requireAdmin(request, env);
        return handleRegister(request, env);
      }

      return json(env, { error: "Not found" }, 404);
    } catch (error) {
      const status = error.status || 500;
      console.error(JSON.stringify({
        level: "error",
        path: url.pathname,
        status,
        message: error.message
      }));
      return json(env, { error: error.message || "Internal server error" }, status);
    }
  }
};

async function handleAudioLookup(request, env) {
  const url = new URL(request.url);
  const slug = cleanSlug(url.searchParams.get("slug"));
  const mode = cleanMode(url.searchParams.get("mode"));

  if (!slug) {
    return json(env, { error: "Missing ?slug parameter" }, 400);
  }

  if (mode) {
    let track = await env.DB.prepare(
      `SELECT id, article_slug, series, mode, url, title, duration_seconds,
              transcript_url, is_default, tts_model, tts_speaker, updated_at
       FROM audio_tracks
       WHERE article_slug = ? AND mode = ?
       LIMIT 1`
    ).bind(slug, mode).first();

    if (!track) {
      track = await env.DB.prepare(
        `SELECT id, article_slug, series, mode, url, title, duration_seconds,
                transcript_url, is_default, tts_model, tts_speaker, updated_at
         FROM audio_tracks
         WHERE article_slug = ? AND is_default = 1
         LIMIT 1`
      ).bind(slug).first();
    }

    return json(env, { track: normalizeTrack(track) });
  }

  const result = await env.DB.prepare(
    `SELECT id, article_slug, series, mode, url, title, duration_seconds,
            transcript_url, is_default, tts_model, tts_speaker, updated_at
     FROM audio_tracks
     WHERE article_slug = ?
     ORDER BY is_default DESC, mode ASC`
  ).bind(slug).all();

  return json(env, { tracks: (result.results || []).map(normalizeTrack) });
}

async function handleExtract(request, env) {
  const body = await readJson(request);
  const html = await resolveHtml(body);
  const text = body.text ? normalizeWhitespace(String(body.text)) : await extractCleanText(html);
  const limited = enforceTextLimit(text, env);

  return json(env, {
    text: limited,
    charCount: limited.length,
    preview: limited.slice(0, 600)
  });
}

async function handleGenerate(request, env, ctx) {
  const body = await readJson(request);
  const slug = cleanSlug(body.slug);
  if (!slug) {
    return json(env, { error: "Missing slug" }, 400);
  }

  const mode = cleanMode(body.mode) || "tts";
  const series = optionalString(body.series);
  const title = optionalString(body.title) || slug;
  const sourceUrl = optionalString(body.url);
  const speaker = cleanSpeaker(body.speaker || env.DEFAULT_TTS_SPEAKER || DEFAULT_SPEAKER);
  const model = optionalString(body.model) || env.DEFAULT_TTS_MODEL || DEFAULT_MODEL;
  const dryRun = Boolean(body.dryRun);
  const jobId = crypto.randomUUID();

  if (!speaker) {
    return json(env, { error: "Unsupported speaker", supportedSpeakers: [...SUPPORTED_SPEAKERS] }, 400);
  }

  await upsertJob(env, {
    id: jobId,
    slug,
    sourceUrl,
    mode,
    status: "extracting",
    message: "Extracting clean page text"
  });

  const text = await resolveText(body, env);
  const chunks = chunkText(text, numberVar(env.CHUNK_CHARS, DEFAULT_CHUNK_CHARS));

  await upsertJob(env, {
    id: jobId,
    slug,
    sourceUrl,
    mode,
    status: dryRun ? "preview" : "generating",
    message: dryRun ? "Dry run complete" : "Generating audio",
    textPreview: text.slice(0, 600),
    textCharCount: text.length,
    chunkCount: chunks.length
  });

  if (dryRun) {
    return json(env, {
      jobId,
      slug,
      mode,
      speaker,
      model,
      charCount: text.length,
      chunkCount: chunks.length,
      preview: text.slice(0, 1000)
    });
  }

  const audioBytes = await generateMp3(env, model, speaker, chunks);
  const baseKey = `audio/generated/${safePathPart(series || "site")}/${safePathPart(slug)}/${safePathPart(mode)}`;
  const audioKey = `${baseKey}.mp3`;
  const transcriptKey = `${baseKey}.txt`;
  const now = new Date().toISOString();

  await env.AUDIO_BUCKET.put(audioKey, audioBytes, {
    httpMetadata: {
      contentType: "audio/mpeg",
      cacheControl: "public, max-age=31536000, immutable"
    },
    customMetadata: {
      slug,
      mode,
      speaker,
      model,
      generatedAt: now
    }
  });

  await env.AUDIO_BUCKET.put(transcriptKey, text, {
    httpMetadata: {
      contentType: "text/plain; charset=utf-8",
      cacheControl: "public, max-age=31536000, immutable"
    },
    customMetadata: {
      slug,
      mode,
      generatedAt: now
    }
  });

  const requestUrl = new URL(request.url);
  const audioUrl = publicUrl(env, audioKey, requestUrl.origin);
  const transcriptUrl = publicUrl(env, transcriptKey, requestUrl.origin);
  const isDefault = body.isDefault === false ? 0 : 1;

  await env.DB.prepare(
    `INSERT INTO audio_tracks
       (article_slug, series, mode, url, title, file_size_bytes, transcript_url,
        r2_key, transcript_r2_key, tts_model, tts_speaker, text_char_count,
        chunk_count, is_default, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
     ON CONFLICT(article_slug, mode) DO UPDATE SET
       series = excluded.series,
       url = excluded.url,
       title = excluded.title,
       file_size_bytes = excluded.file_size_bytes,
       transcript_url = excluded.transcript_url,
       r2_key = excluded.r2_key,
       transcript_r2_key = excluded.transcript_r2_key,
       tts_model = excluded.tts_model,
       tts_speaker = excluded.tts_speaker,
       text_char_count = excluded.text_char_count,
       chunk_count = excluded.chunk_count,
       is_default = excluded.is_default,
       updated_at = CURRENT_TIMESTAMP`
  ).bind(
    slug,
    series,
    mode,
    audioUrl,
    title,
    audioBytes.byteLength,
    transcriptUrl,
    audioKey,
    transcriptKey,
    model,
    speaker,
    text.length,
    chunks.length,
    isDefault
  ).run();

  await upsertJob(env, {
    id: jobId,
    slug,
    sourceUrl,
    mode,
    status: "completed",
    message: "Audio generated and registered",
    textPreview: text.slice(0, 600),
    textCharCount: text.length,
    chunkCount: chunks.length,
    audioUrl,
    transcriptUrl
  });

  ctx.waitUntil(logGeneration(jobId, slug, mode, audioKey));

  return json(env, {
    ok: true,
    jobId,
    slug,
    mode,
    series,
    title,
    speaker,
    model,
    charCount: text.length,
    chunkCount: chunks.length,
    fileSizeBytes: audioBytes.byteLength,
    audioUrl,
    transcriptUrl,
    playerLookup: `/api/audio?slug=${encodeURIComponent(slug)}&mode=${encodeURIComponent(mode)}`
  });
}

async function handleRegister(request, env) {
  const body = await readJson(request);
  const slug = cleanSlug(body.slug);
  const mode = cleanMode(body.mode) || "tts";
  const url = optionalString(body.url);

  if (!slug || !url) {
    return json(env, { error: "Missing slug or url" }, 400);
  }

  await env.DB.prepare(
    `INSERT INTO audio_tracks
       (article_slug, series, mode, url, title, duration_seconds, file_size_bytes,
        transcript_url, is_default, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
     ON CONFLICT(article_slug, mode) DO UPDATE SET
       series = excluded.series,
       url = excluded.url,
       title = excluded.title,
       duration_seconds = excluded.duration_seconds,
       file_size_bytes = excluded.file_size_bytes,
       transcript_url = excluded.transcript_url,
       is_default = excluded.is_default,
       updated_at = CURRENT_TIMESTAMP`
  ).bind(
    slug,
    optionalString(body.series),
    mode,
    url,
    optionalString(body.title) || slug,
    integerOrNull(body.durationSeconds),
    integerOrNull(body.fileSizeBytes),
    optionalString(body.transcriptUrl),
    body.isDefault === false ? 0 : 1
  ).run();

  return json(env, {
    ok: true,
    slug,
    mode,
    url,
    playerLookup: `/api/audio?slug=${encodeURIComponent(slug)}&mode=${encodeURIComponent(mode)}`
  });
}

async function handleAudioFile(request, env) {
  const url = new URL(request.url);
  const key = decodeURIComponent(url.pathname.replace(/^\/audio\//, "audio/"));
  if (!key.startsWith("audio/")) {
    return json(env, { error: "Invalid audio key" }, 400);
  }

  const object = await env.AUDIO_BUCKET.get(key);
  if (!object) {
    return json(env, { error: "Audio object not found" }, 404);
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("etag", object.httpEtag);
  headers.set("cache-control", headers.get("cache-control") || "public, max-age=31536000, immutable");
  headers.set("access-control-allow-origin", env.ALLOWED_ORIGIN || "*");
  return new Response(object.body, { headers });
}

async function resolveText(body, env) {
  if (body.text) {
    return enforceTextLimit(normalizeWhitespace(String(body.text)), env);
  }
  const html = await resolveHtml(body);
  return enforceTextLimit(await extractCleanText(html), env);
}

async function resolveHtml(body) {
  if (body.html) {
    return String(body.html);
  }

  if (!body.url) {
    throw httpError("Provide text, html, or url", 400);
  }

  const url = new URL(String(body.url));
  if (url.protocol !== "https:" && url.protocol !== "http:") {
    throw httpError("Only http/https URLs are supported", 400);
  }

  const response = await fetch(url.toString(), {
    headers: {
      "User-Agent": "faith-audio-pipeline/1.0"
    }
  });

  if (!response.ok) {
    throw httpError(`Failed to fetch source page: ${response.status}`, 502);
  }

  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("text/html")) {
    throw httpError("Source URL did not return HTML", 400);
  }

  return response.text();
}

async function extractCleanText(html) {
  const targeted = await extractTextWithSelector(html, SOURCE_SELECTOR);
  if (targeted.length >= 200) return targeted;
  const bodyFallback = await extractTextWithSelector(html, "body");
  return bodyFallback.length > targeted.length ? bodyFallback : targeted;
}

async function extractTextWithSelector(html, sourceSelector) {
  const extractor = new TextExtractor();
  const response = new HTMLRewriter()
    .on("title", new TitleHandler(extractor))
    .on(sourceSelector, new CaptureHandler(extractor))
    .on(EXCLUDE_SELECTOR, new ExcludeHandler(extractor))
    .transform(new Response(html, { headers: { "content-type": "text/html;charset=utf-8" } }));

  await response.arrayBuffer();
  return extractor.result();
}

class TextExtractor {
  constructor() {
    this.captureDepth = 0;
    this.skipDepth = 0;
    this.title = "";
    this.parts = [];
  }

  addText(value) {
    if (this.captureDepth < 1 || this.skipDepth > 0) return;
    const cleaned = normalizeWhitespace(value);
    if (cleaned) this.parts.push(cleaned);
  }

  result() {
    const joined = normalizeWhitespace(this.parts.join(" "));
    if (joined) return joined;
    return normalizeWhitespace(this.title);
  }
}

class TitleHandler {
  constructor(extractor) {
    this.extractor = extractor;
  }

  text(text) {
    this.extractor.title += text.text;
  }
}

class CaptureHandler {
  constructor(extractor) {
    this.extractor = extractor;
  }

  element(element) {
    this.extractor.captureDepth += 1;
    element.onEndTag(() => {
      this.extractor.captureDepth = Math.max(0, this.extractor.captureDepth - 1);
    });
  }

  text(text) {
    this.extractor.addText(text.text);
  }
}

class ExcludeHandler {
  constructor(extractor) {
    this.extractor = extractor;
  }

  element(element) {
    this.extractor.skipDepth += 1;
    element.onEndTag(() => {
      this.extractor.skipDepth = Math.max(0, this.extractor.skipDepth - 1);
    });
  }
}

async function generateMp3(env, model, speaker, chunks) {
  const buffers = [];
  let totalLength = 0;

  for (const chunk of chunks) {
    const aiResponse = await env.AI.run(
      model,
      { text: chunk, speaker, encoding: "mp3" },
      { returnRawResponse: true }
    );
    const arrayBuffer = await responseToArrayBuffer(aiResponse);
    const bytes = new Uint8Array(arrayBuffer);
    buffers.push(bytes);
    totalLength += bytes.byteLength;
  }

  const combined = new Uint8Array(totalLength);
  let offset = 0;
  for (const bytes of buffers) {
    combined.set(bytes, offset);
    offset += bytes.byteLength;
  }
  return combined;
}

async function responseToArrayBuffer(value) {
  if (value instanceof Response) {
    if (!value.ok) {
      throw httpError(await safeAiErrorMessage(value), value.status || 502);
    }
    return value.arrayBuffer();
  }
  if (value && typeof value.arrayBuffer === "function") {
    return value.arrayBuffer();
  }
  if (value && value.body) {
    return new Response(value.body).arrayBuffer();
  }
  if (value instanceof ArrayBuffer) {
    return value;
  }
  throw httpError("TTS model did not return audio bytes", 502);
}

async function safeAiErrorMessage(response) {
  try {
    const text = await response.text();
    if (!text) return "TTS model returned an error";
    const parsed = JSON.parse(text);
    return parsed.description || parsed.message || text.slice(0, 300);
  } catch {
    return "TTS model returned an error";
  }
}

function chunkText(text, maxChars) {
  const chunks = [];
  const paragraphs = text.split(/\n{2,}/).flatMap((paragraph) => paragraph.split(/(?<=[.!?])\s+/));
  let current = "";

  for (const part of paragraphs) {
    const candidate = normalizeWhitespace(part);
    if (!candidate) continue;

    if (candidate.length > maxChars) {
      if (current) {
        chunks.push(current);
        current = "";
      }
      for (let i = 0; i < candidate.length; i += maxChars) {
        chunks.push(candidate.slice(i, i + maxChars));
      }
      continue;
    }

    if ((current + " " + candidate).trim().length > maxChars && current) {
      chunks.push(current);
      current = candidate;
    } else {
      current = (current + " " + candidate).trim();
    }
  }

  if (current) chunks.push(current);
  return chunks;
}

async function upsertJob(env, job) {
  await env.DB.prepare(
    `INSERT INTO audio_generation_jobs
       (id, article_slug, source_url, mode, status, message, text_preview,
        text_char_count, chunk_count, audio_url, transcript_url, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
     ON CONFLICT(id) DO UPDATE SET
       status = excluded.status,
       message = excluded.message,
       text_preview = COALESCE(excluded.text_preview, audio_generation_jobs.text_preview),
       text_char_count = COALESCE(excluded.text_char_count, audio_generation_jobs.text_char_count),
       chunk_count = COALESCE(excluded.chunk_count, audio_generation_jobs.chunk_count),
       audio_url = COALESCE(excluded.audio_url, audio_generation_jobs.audio_url),
       transcript_url = COALESCE(excluded.transcript_url, audio_generation_jobs.transcript_url),
       updated_at = CURRENT_TIMESTAMP`
  ).bind(
    job.id,
    job.slug,
    job.sourceUrl || null,
    job.mode,
    job.status,
    job.message || null,
    job.textPreview || null,
    integerOrNull(job.textCharCount),
    integerOrNull(job.chunkCount),
    job.audioUrl || null,
    job.transcriptUrl || null
  ).run();
}

async function requireAdmin(request, env) {
  if (!env.ADMIN_TOKEN) {
    throw httpError("ADMIN_TOKEN secret is not configured", 500);
  }

  const auth = request.headers.get("authorization") || "";
  const bearer = auth.toLowerCase().startsWith("bearer ") ? auth.slice(7) : "";
  const headerToken = request.headers.get("x-admin-token") || "";
  const supplied = bearer || headerToken;

  if (!supplied || !(await timingSafeEqual(supplied, env.ADMIN_TOKEN))) {
    throw httpError("Unauthorized", 401);
  }
}

async function timingSafeEqual(left, right) {
  const encoder = new TextEncoder();
  const leftBytes = encoder.encode(left);
  const rightBytes = encoder.encode(right);
  if (leftBytes.byteLength !== rightBytes.byteLength) return false;
  const leftDigest = await crypto.subtle.digest("SHA-256", leftBytes);
  const rightDigest = await crypto.subtle.digest("SHA-256", rightBytes);
  const a = new Uint8Array(leftDigest);
  const b = new Uint8Array(rightDigest);
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) {
    diff |= a[i] ^ b[i];
  }
  return diff === 0;
}

function enforceTextLimit(text, env) {
  const cleaned = normalizeWhitespace(text);
  const max = numberVar(env.MAX_TEXT_CHARS, DEFAULT_MAX_TEXT_CHARS);
  if (!cleaned) {
    throw httpError("No narratable text found", 400);
  }
  if (cleaned.length > max) {
    throw httpError(`Narration text is ${cleaned.length} chars; limit is ${max}. Split the page or raise MAX_TEXT_CHARS.`, 413);
  }
  return cleaned;
}

function publicUrl(env, key, origin) {
  const base = optionalString(env.PUBLIC_AUDIO_BASE_URL);
  if (!base) return `${origin.replace(/\/+$/, "")}/${key.split("/").map(encodeURIComponent).join("/")}`;
  return `${base.replace(/\/+$/, "")}/${key.split("/").map(encodeURIComponent).join("/")}`;
}

function normalizeTrack(track) {
  if (!track) return null;
  return {
    ...track,
    is_default: Boolean(track.is_default)
  };
}

async function readJson(request) {
  try {
    return await request.json();
  } catch {
    throw httpError("Expected JSON body", 400);
  }
}

function json(env, body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      ...corsHeaders(env),
      "content-type": "application/json; charset=utf-8"
    }
  });
}

function corsHeaders(env) {
  return {
    "access-control-allow-origin": env.ALLOWED_ORIGIN || "*",
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "authorization, content-type, x-admin-token",
    "access-control-max-age": "86400"
  };
}

function httpError(message, status) {
  const error = new Error(message);
  error.status = status;
  return error;
}

function cleanSlug(value) {
  const text = optionalString(value);
  if (!text) return "";
  return text.replace(/\.html$/i, "").replace(/^\/+|\/+$/g, "").replace(/[^a-zA-Z0-9/_-]/g, "-").slice(0, 180);
}

function cleanMode(value) {
  const text = optionalString(value);
  if (!text) return "";
  return text.toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 40);
}

function cleanSpeaker(value) {
  const speaker = optionalString(value).toLowerCase();
  return SUPPORTED_SPEAKERS.has(speaker) ? speaker : "";
}

function safePathPart(value) {
  return String(value || "unknown").replace(/[^a-zA-Z0-9_-]/g, "-").replace(/-+/g, "-").slice(0, 120);
}

function optionalString(value) {
  if (value === undefined || value === null) return "";
  return String(value).trim();
}

function normalizeWhitespace(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function integerOrNull(value) {
  const number = Number(value);
  return Number.isFinite(number) ? Math.trunc(number) : null;
}

function numberVar(value, fallback) {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? Math.trunc(number) : fallback;
}

async function logGeneration(jobId, slug, mode, audioKey) {
  console.log(JSON.stringify({
    level: "info",
    event: "audio_generated",
    jobId,
    slug,
    mode,
    audioKey
  }));
}
