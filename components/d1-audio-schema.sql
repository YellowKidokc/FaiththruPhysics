-- Cloudflare D1 schema for the TP pill-player audio catalog.
-- Each row maps one article+mode to a podcast/audio URL and optional metadata.

CREATE TABLE IF NOT EXISTS audio_tracks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  article_slug TEXT NOT NULL,           -- e.g. "MDA-001-story-introduction"
  series TEXT,                          -- e.g. "mda"
  mode TEXT NOT NULL,                   -- "deep" | "debate" | "critique" | "tts" | "web"
  url TEXT NOT NULL,
  title TEXT,
  duration_seconds INTEGER,
  file_size_bytes INTEGER,
  transcript_url TEXT,
  is_default BOOLEAN DEFAULT FALSE,     -- fallback track when a mode is missing
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(article_slug, mode)
);

-- Index for fast per-article lookups.
CREATE INDEX IF NOT EXISTS idx_audio_tracks_slug ON audio_tracks(article_slug);
CREATE INDEX IF NOT EXISTS idx_audio_tracks_series ON audio_tracks(series);

-- Example seed data (replace URLs with real ones before deploying).
INSERT INTO audio_tracks (article_slug, series, mode, url, title, is_default)
VALUES
  ('mda-series-home', 'mda', 'deep',  'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Deep Dive', TRUE),
  ('mda-series-home', 'mda', 'debate','https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Debate', TRUE),
  ('mda-series-home', 'mda', 'critique','https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Critique', TRUE),
  ('mda-series-home', 'mda', 'tts',   'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: TTS', TRUE),
  ('mda-series-home', 'mda', 'web',   'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Web', TRUE)
ON CONFLICT(article_slug, mode) DO UPDATE SET
  url = excluded.url,
  title = excluded.title,
  updated_at = CURRENT_TIMESTAMP;
