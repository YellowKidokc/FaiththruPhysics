import psycopg2, re

conn = psycopg2.connect(host='192.168.1.93', port=5432, dbname='theophysics',
                        user='postgres', password='Moss9pep28$')
conn.autocommit = True
cur = conn.cursor()

# Add canonical_id column
cur.execute('ALTER TABLE site_pages ADD COLUMN IF NOT EXISTS canonical_id TEXT')
cur.execute('CREATE INDEX IF NOT EXISTS idx_site_pages_canonical ON site_pages(canonical_id)')

# Get all pages
cur.execute('SELECT id, filename, rel_path, series FROM site_pages')
rows = cur.fetchall()

updated = 0
for pid, fname, rel, series in rows:
    name = fname.replace('.html','')
    cid = None

    # MDA: MDA-001-story-introduction -> MDA-001
    m = re.match(r'(MDA-\d{3})', name, re.I)
    if m: cid = m.group(1).upper()

    # GTQ: gtq-01-xxx -> GTQ-01
    if not cid:
        m = re.match(r'(gtq-\d{2})', name, re.I)
        if m: cid = m.group(1).upper()

    # ISO: iso-001-xxx -> ISO-001
    if not cid:
        m = re.match(r'(iso-\d{3})', name, re.I)
        if m: cid = m.group(1).upper()

    # CNS: cns-01-xxx -> CNS-01
    if not cid:
        m = re.match(r'(cns-\d{2})', name, re.I)
        if m: cid = m.group(1).upper()

    # CDT: cdt-01-xxx -> CDT-01
    if not cid:
        m = re.match(r'(cdt-\d{2})', name, re.I)
        if m: cid = m.group(1).upper()

    # BGL: bgl-01-xxx -> BGL-01
    if not cid:
        m = re.match(r'(bgl-\d{2})', name, re.I)
        if m: cid = m.group(1).upper()

    # SW: sw-xxx -> SW-SLUG
    if not cid and series == 'spiritual-warfare' and fname != 'index.html':
        cid = 'SW-' + name.replace('sw-','').upper()[:20]

    # Logos papers: logos-01 -> LOGOS-01
    if not cid:
        m = re.match(r'(logos-\d{2})', name, re.I)
        if m: cid = m.group(1).upper()

    # One-page stories by slug
    if not cid and series == 'one-page-stories':
        slug = name.replace('_','-').upper()[:30]
        cid = 'OPS-' + slug

    # Index pages get series code
    if not cid and fname == 'index.html':
        cid = series.upper().replace('-','_') + '-INDEX'

    # Fallback: series + filename slug
    if not cid:
        slug = name.replace('_','-').upper()[:25]
        cid = series.upper()[:10] + '-' + slug

    cur.execute('UPDATE site_pages SET canonical_id = %s WHERE id = %s', (cid, pid))
    updated += 1

# Stats
cur.execute('SELECT COUNT(DISTINCT canonical_id) FROM site_pages WHERE canonical_id IS NOT NULL')
unique = cur.fetchone()[0]

print(f'Updated {updated} rows, {unique} unique canonical IDs')
print()

# MDA sample
cur.execute("SELECT canonical_id, title, rel_path FROM site_pages WHERE canonical_id LIKE 'MDA-%' ORDER BY canonical_id LIMIT 15")
for cid, title, path in cur.fetchall():
    t = (title or 'untitled')[:45]
    print(f'  {cid:12s} | {t:45s} | {path}')

print()
# GTQ sample
cur.execute("SELECT canonical_id, title, rel_path FROM site_pages WHERE canonical_id LIKE 'GTQ-%' ORDER BY canonical_id LIMIT 10")
for cid, title, path in cur.fetchall():
    t = (title or 'untitled')[:45]
    print(f'  {cid:12s} | {t:45s} | {path}')

print()
# ISO sample
cur.execute("SELECT canonical_id, title, rel_path FROM site_pages WHERE canonical_id LIKE 'ISO-%' ORDER BY canonical_id LIMIT 10")
for cid, title, path in cur.fetchall():
    t = (title or 'untitled')[:45]
    print(f'  {cid:12s} | {t:45s} | {path}')

print()
# Series breakdown
cur.execute("""
    SELECT split_part(canonical_id, '-', 1) as prefix, COUNT(*) as cnt 
    FROM site_pages WHERE canonical_id IS NOT NULL 
    GROUP BY prefix ORDER BY cnt DESC LIMIT 20
""")
print('By prefix:')
for prefix, cnt in cur.fetchall():
    print(f'  {prefix:15s} {cnt:>4d}')

conn.close()
print()
print('DONE. Codex query: SELECT canonical_id, rel_path, title FROM site_pages WHERE canonical_id = $1')
