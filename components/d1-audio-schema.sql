-- Cloudflare D1 schema for the TP pill-player audio catalog.
-- Each row maps one article+mode to a podcast/audio URL and optional metadata.
-- Canonical modes are read, podcast, deep, and critique.

CREATE TABLE IF NOT EXISTS audio_tracks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  article_slug TEXT NOT NULL,           -- e.g. "proof-architecture/pa-01-unavoidable-conclusion"
  series TEXT,                          -- e.g. "proof-architecture"
  mode TEXT NOT NULL CHECK (mode IN ('read', 'podcast', 'deep', 'critique')),
  url TEXT NOT NULL,
  title TEXT,
  duration_seconds INTEGER,
  file_size_bytes INTEGER,
  r2_key TEXT,
  transcript_url TEXT,
  is_default BOOLEAN DEFAULT FALSE,     -- fallback track when a mode is missing
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(article_slug, mode)
);

-- Index for fast per-article lookups.
CREATE INDEX IF NOT EXISTS idx_audio_tracks_slug ON audio_tracks(article_slug);
CREATE INDEX IF NOT EXISTS idx_audio_tracks_series ON audio_tracks(series);
CREATE INDEX IF NOT EXISTS idx_audio_tracks_mode ON audio_tracks(mode);

-- Example seed data (replace URLs with real ones before deploying).
INSERT INTO audio_tracks (article_slug, series, mode, url, title, is_default)
VALUES
  ('mda/mda-series-home', 'mda', 'read', 'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Read Aloud', TRUE),
  ('mda/mda-series-home', 'mda', 'deep', 'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Deep Dive', FALSE),
  ('mda/mda-series-home', 'mda', 'podcast', 'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Podcast', FALSE),
  ('mda/mda-series-home', 'mda', 'critique', 'https://pub-6e138de4ad2a4ad3917f2c404502b9e1.r2.dev/audio/moral-decline-of-america.m4a', 'Series Overview: Critique', FALSE)
ON CONFLICT(article_slug, mode) DO UPDATE SET
  url = excluded.url,
  title = excluded.title,
  updated_at = CURRENT_TIMESTAMP;
