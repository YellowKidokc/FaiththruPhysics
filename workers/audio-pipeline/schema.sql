CREATE TABLE IF NOT EXISTS audio_tracks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  article_slug TEXT NOT NULL,
  series TEXT,
  mode TEXT NOT NULL DEFAULT 'tts',
  url TEXT NOT NULL,
  title TEXT,
  duration_seconds INTEGER,
  file_size_bytes INTEGER,
  transcript_url TEXT,
  r2_key TEXT,
  transcript_r2_key TEXT,
  tts_model TEXT,
  tts_speaker TEXT,
  text_char_count INTEGER,
  chunk_count INTEGER,
  is_default INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(article_slug, mode)
);

CREATE INDEX IF NOT EXISTS idx_audio_tracks_slug ON audio_tracks(article_slug);
CREATE INDEX IF NOT EXISTS idx_audio_tracks_series ON audio_tracks(series);
CREATE INDEX IF NOT EXISTS idx_audio_tracks_mode ON audio_tracks(mode);

CREATE TABLE IF NOT EXISTS audio_generation_jobs (
  id TEXT PRIMARY KEY,
  article_slug TEXT NOT NULL,
  source_url TEXT,
  mode TEXT NOT NULL DEFAULT 'tts',
  status TEXT NOT NULL,
  message TEXT,
  text_preview TEXT,
  text_char_count INTEGER,
  chunk_count INTEGER,
  audio_url TEXT,
  transcript_url TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audio_generation_jobs_slug ON audio_generation_jobs(article_slug);
CREATE INDEX IF NOT EXISTS idx_audio_generation_jobs_status ON audio_generation_jobs(status);

