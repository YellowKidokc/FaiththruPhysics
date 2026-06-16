import psycopg2
conn = psycopg2.connect(host='192.168.1.93', port=5432, dbname='theophysics',
                        user='postgres', password='Moss9pep28$')
conn.autocommit = True
cur = conn.cursor()
cur.execute('ALTER TABLE site_pages ADD COLUMN IF NOT EXISTS is_canonical BOOLEAN DEFAULT FALSE')
cur.execute('ALTER TABLE site_pages ADD COLUMN IF NOT EXISTS duplicate_of TEXT')

# Mark canonical: prefer moral-decline over mda, main over subdomains, non-backup over backup
cur.execute("""
UPDATE site_pages SET is_canonical = TRUE
WHERE id IN (
    SELECT DISTINCT ON (canonical_id) id FROM site_pages
    WHERE canonical_id IS NOT NULL
    ORDER BY canonical_id,
        CASE 
            WHEN rel_path LIKE '%%_backups%%' THEN 3
            WHEN rel_path LIKE 'subdomains/%%' THEN 2
            WHEN rel_path LIKE 'mda/%%' THEN 1
            ELSE 0
        END,
        modified DESC
)
""")

cur.execute('SELECT COUNT(*) FROM site_pages WHERE is_canonical = TRUE')
canon = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM site_pages WHERE is_canonical = FALSE')
dupes = cur.fetchone()[0]
print(f'Canonical: {canon}')
print(f'Duplicates: {dupes}')
print()

cur.execute("""SELECT canonical_id, rel_path FROM site_pages 
    WHERE is_canonical = TRUE AND canonical_id LIKE 'MDA-%%' 
    ORDER BY canonical_id LIMIT 20""")
print('Canonical MDA pages:')
for cid, path in cur.fetchall():
    print(f'  {cid:12s} -> {path}')

print()
cur.execute("""SELECT canonical_id, COUNT(*) as copies FROM site_pages 
    GROUP BY canonical_id HAVING COUNT(*) > 1 ORDER BY copies DESC LIMIT 15""")
print('Most duplicated IDs:')
for cid, cnt in cur.fetchall():
    print(f'  {cid:12s} x{cnt}')

conn.close()
print()
print('DONE.')
print('Codex reference query:')
print('  SELECT canonical_id, rel_path, title FROM site_pages')
print('  WHERE canonical_id = $1 AND is_canonical = TRUE')
