-- MTL (Math Translation Layer) worker schema
-- Stores equation translations keyed by normalized LaTeX hash.

CREATE TABLE IF NOT EXISTS mtl_equations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  eq_id TEXT UNIQUE,                 -- canonical ID, e.g. EQ-001
  latex_hash TEXT UNIQUE NOT NULL,   -- sha256 of normalized LaTeX
  latex TEXT NOT NULL,               -- original LaTeX string
  easy TEXT,                         -- plain-English translation
  standard TEXT,                     -- term-by-term / medium explanation
  academic TEXT,                     -- physics/theology/conceptual depth
  audio_safe TEXT,                   -- narration-friendly text
  source TEXT,                       -- workbook sheet / manual / llm
  source_file TEXT,                  -- originating article/file
  difficulty TEXT,                   -- basic | intermediate | advanced
  paper_ref TEXT,                    -- formal paper reference
  updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_mtl_latex_hash ON mtl_equations(latex_hash);
CREATE INDEX IF NOT EXISTS idx_mtl_eq_id ON mtl_equations(eq_id);
