import psycopg2
import os
import re
from pathlib import Path
from datetime import datetime

SITE_ROOT = Path(r"D:\GitHub\faiththruphysics-site")
PG_HOST = "192.168.1.93"
PG_PORT = 5432
PG_DB = "theophysics"
PG_USER = "postgres"
PG_PASS = os.environ.get("PGPASSWORD", "Moss9pep28$")

def extract_meta(filepath):
    """Extract title, description, and other meta from an HTML file."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    
    meta = {}
    # Title
    m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    meta["title"] = m.group(1).strip() if m else None
    
    # Meta description
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', text, re.S | re.I)
    meta["description"] = m.group(1).strip() if m else None
    
    # OG title
    m = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', text, re.S | re.I)
    meta["og_title"] = m.group(1).strip() if m else None
    
    # Canonical URL
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', text, re.S | re.I)
    meta["canonical_url"] = m.group(1).strip() if m else None
    
    # File size
    meta["file_size"] = filepath.stat().st_size
    meta["modified"] = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
    
    # Count approximate word count (strip tags)
    cleaned = re.sub(r'<script.*?</script>', '', text, flags=re.S | re.I)
    cleaned = re.sub(r'<style.*?</style>', '', cleaned, flags=re.S | re.I)
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    words = len(cleaned.split())
    meta["word_count"] = words
    
    # Has MathJax?
    meta["has_mathjax"] = "mathjax" in text.lower() or "\\(" in text or "\\[" in text
    
    # Has audio player?
    meta["has_audio"] = "audio" in text.lower() and ("<audio" in text.lower() or "audio-player" in text.lower())
    
    return meta

def classify_path(rel_path):
    """Classify a file by its directory into series/lane."""
    parts = rel_path.parts
    series = parts[0] if len(parts) > 1 else "root"
    lane = parts[1] if len(parts) > 2 else None
    return series, lane

def main():
    # Scan all HTML files
    html_files = [f for f in SITE_ROOT.rglob("*.html") 
                  if not any(p.startswith('.') for p in f.relative_to(SITE_ROOT).parts)]
    
    print(f"Found {len(html_files)} HTML files")
    
    # Extract metadata
    records = []
    for f in html_files:
        rel = f.relative_to(SITE_ROOT)
        series, lane = classify_path(rel)
        meta = extract_meta(f)
        if "error" in meta:
            print(f"  SKIP {rel}: {meta['error']}")
            continue
        records.append({
            "rel_path": str(rel).replace("\\", "/"),
            "filename": f.name,
            "series": series,
            "lane": lane,
            "title": meta.get("title"),
            "description": meta.get("description"),
            "og_title": meta.get("og_title"),
            "canonical_url": meta.get("canonical_url"),
            "file_size": meta.get("file_size", 0),
            "word_count": meta.get("word_count", 0),
            "has_mathjax": meta.get("has_mathjax", False),
            "has_audio": meta.get("has_audio", False),
            "modified": meta.get("modified"),
        })
    
    print(f"Extracted metadata from {len(records)} files")
    
    # Connect to Postgres
    print(f"Connecting to {PG_HOST}:{PG_PORT}/{PG_DB}...")
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB, 
        user=PG_USER, password=PG_PASS
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create table
    cur.execute("""
    DROP TABLE IF EXISTS site_pages CASCADE;
    CREATE TABLE site_pages (
        id SERIAL PRIMARY KEY,
        rel_path TEXT UNIQUE NOT NULL,
        filename TEXT NOT NULL,
        series TEXT,
        lane TEXT,
        title TEXT,
        description TEXT,
        og_title TEXT,
        canonical_url TEXT,
        file_size INTEGER DEFAULT 0,
        word_count INTEGER DEFAULT 0,
        has_mathjax BOOLEAN DEFAULT FALSE,
        has_audio BOOLEAN DEFAULT FALSE,
        modified TIMESTAMP,
        review_status TEXT DEFAULT 'pending',
        review_notes TEXT,
        synced_at TIMESTAMP DEFAULT NOW()
    );
    """)
    print("Created site_pages table")
    
    # Also create the series catalog table from the homepage JS data
    cur.execute("""
    DROP TABLE IF EXISTS site_series CASCADE;
    CREATE TABLE site_series (
        id SERIAL PRIMARY KEY,
        code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        href TEXT,
        tier INTEGER,
        cluster TEXT,
        color TEXT,
        article_count TEXT,
        note TEXT,
        featured BOOLEAN DEFAULT FALSE,
        external_link BOOLEAN DEFAULT FALSE
    );
    """)
    print("Created site_series table")
    
    # Insert pages
    insert_sql = """
    INSERT INTO site_pages (rel_path, filename, series, lane, title, description, 
        og_title, canonical_url, file_size, word_count, has_mathjax, has_audio, modified)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (rel_path) DO UPDATE SET
        title = EXCLUDED.title, description = EXCLUDED.description,
        file_size = EXCLUDED.file_size, word_count = EXCLUDED.word_count,
        has_mathjax = EXCLUDED.has_mathjax, has_audio = EXCLUDED.has_audio,
        modified = EXCLUDED.modified, synced_at = NOW()
    """
    for r in records:
        cur.execute(insert_sql, (
            r["rel_path"], r["filename"], r["series"], r["lane"],
            r["title"], r["description"], r["og_title"], r["canonical_url"],
            r["file_size"], r["word_count"], r["has_mathjax"], r["has_audio"],
            r["modified"]
        ))
    print(f"Inserted {len(records)} page records")
    
    # Insert series catalog
    SERIES = [
        ("STORY","★ The Master Story","Master Story.html",1,"Foundations","gold","~12 min",True,False),
        ("DOOR","Theophysics — The Full Explanation","one-page-stories/theophysics-the-full-explanation.html",1,"Foundations","gold","7200 words",True,False),
        ("LETTER","Everybody's Got It Wrong","one-page-stories/everybodys-got-it-wrong.html",1,"Foundations","gold","Personal",True,False),
        ("CNS","The Convergence","Convergence_Series/index.html",1,"Foundations","gold","7 articles",False,False),
        ("GTQ","Genesis to Quantum","genesis-to-quantum/index.html",1,"Foundations","red","10+17 articles",True,False),
        ("LGS","The Logos Story","Logos_Papers/index.html",1,"Foundations","gold","12 articles",False,False),
        ("BLUE","Family Briefing","blue/index.html",1,"Foundations","blue","9 articles",False,False),
        ("BGL","Be Glad You're a Loser","be-glad-youre-a-loser/index.html",1,"Gospel","gold","2 articles",False,False),
        ("MDA-S","The Lowe Family Stories","/mda/#stories",1,"Decline","red","7 stories",False,False),
        ("SAME","The Same Equation","one-page-stories/the-same-equation.html",1,"Architecture","gold","Visual proof",False,False),
        ("LOGOS-T","The Logos Thesis","one-page-stories/The_Logos_Thesis_v3.html",2,"Foundations","gold","Full paper",True,False),
        ("CDT","Convergence — Deep Theory","convergence-deep/index.html",2,"Foundations","gold","6 articles",False,False),
        ("CON","Consciousness","consciousness/index.html",2,"Consciousness","teal","10 papers",True,False),
        ("MEQ","The 10 Laws of Theophysics","master-equation/index.html",2,"Architecture","gold","10 law pages",False,False),
        ("TENLAWS","Ten Laws — Full Treatment","one-page-stories/ten-laws-full-treatment.html",2,"Architecture","gold","Reference",False,False),
        ("NODRIFT","The No-Drift Law Synthesis","one-page-stories/no-drift-law-synthesis.html",2,"Architecture","gold","Master ref",False,False),
        ("FLOOR","The Floor Beneath the Floor","one-page-stories/the-floor-beneath-the-floor.html",2,"Architecture","gold","Derivation",False,False),
        ("ITBIT","It from Bit from Logos","one-page-stories/it-from-bit-from-logos.html",2,"Architecture","gold","Extension",False,False),
        ("FATHER","The Father as Source Field","one-page-stories/the-father-as-source-field.html",2,"Architecture","gold","Derivation",False,False),
        ("GOD","Character of God — from Physics","one-page-stories/character-of-god-from-physics.html",2,"Warfare","gold","24 properties",False,False),
        ("ADV","Character of the Adversary","spiritual-warfare/sw-character-of-adversary-from-physics.html",2,"Warfare","red","12 properties",False,False),
        ("ATTACK","The Attack Surface","spiritual-warfare/sw-the-attack-surface.html",2,"Warfare","red","9 vectors",False,False),
        ("ANTI","The 24 Anti-Properties","one-page-stories/the-24-anti-properties.html",2,"Warfare","red","Taxonomy",False,False),
        ("SW","Spiritual Warfare","spiritual-warfare/index.html",2,"Warfare","red","7 pages",False,False),
        ("SALV","The Salvation Algorithm","one-page-stories/salvation-algorithm.html",2,"Gospel","gold","6 steps",True,False),
        ("PHASE","Salvation Is a Phase Transition","one-page-stories/salvation-phase-transition.html",2,"Gospel","gold","12 stages",False,False),
        ("GRACE","Why Grace Has to Come from Outside","one-page-stories/why-grace-from-outside.html",2,"Gospel","gold","Proof",False,False),
        ("ATTRACT","Heaven and Hell as Attractor States","one-page-stories/heaven-hell-attractor-states.html",2,"Gospel","gold","Dynamical sys",False,False),
        ("MDA","The Moral Decline of America","/moral-decline/",2,"Decline","red","61 articles",True,False),
        ("CD","Cross-Domain Applications","cross-domain/index.html",2,"Reference","blue","12 articles",False,False),
        ("BDL","Bible DataLab","bible-datalab/index.html",2,"Reference","purple","8 studies",False,False),
        ("PS","The Prophetic Synthesis","prophetic-synthesis/index.html",2,"Reference","purple","7 articles",False,False),
        ("SA","The Socratic Axioms","socratic-axioms/index.html",2,"Reference","teal","9 axioms",False,False),
        ("DRV","De Revolutionibus Veritatis","revolution-of-truth/index.html",2,"Reference","blue","6 books",False,False),
        ("DP","The Duality Project","duality-project/index.html",2,"Reference","purple","22 sim logs",False,False),
        ("ISO","Isomorphism Registry","genesis-to-quantum/iso/iso-001-gravity-sin.html",2,"Reference","red","10 mappings",False,False),
        ("TBA","The Bidirectional Audit","the-bidirectional-audit/index.html",2,"Evidence","teal","1 article",False,False),
        ("FT","Formal Theophysics","https://zenodo.org/communities/theophysics/",3,"Papers","blue","16 papers",True,True),
        ("SP","Supplementary Papers","https://zenodo.org/communities/theophysics/",3,"Papers","blue","17 papers",False,True),
        ("FP","Algorithmic Foundations","formal-papers/index.html",3,"Papers","blue","10 papers",False,False),
        ("LOGOS-F","Logos Papers (Formal)","logos-papers/logos-01.html",3,"Papers","gold","14 papers",False,False),
        ("PA","Proof Architecture","proof-architecture/index.html",3,"Papers","teal","13 pages",False,False),
        ("PE","Proof Explorer","proof-explorer/axioms-layer-0-core.html",3,"Papers","teal","6 pages",False,False),
        ("TESTS","We Ran the Tests","family-tests/we-ran-the-tests.html",3,"Evidence","blue","7 tests",True,False),
        ("HOLD","Holding God Accountable","one-page-stories/holding-god-accountable.html",3,"Evidence","blue","39/50 vs 21/50",False,False),
        ("GOLD","Gold Standard Test Battery","blue/gold-standard-test-battery.html",3,"Evidence","blue","Test battery",False,False),
        ("FACTS","FACTS — The Academic Case","/mda/",3,"Evidence","red","Formal paper",False,False),
        ("FT-PAPER","Family Tests","family-tests/index.html",3,"Evidence","blue","3 articles",False,False),
    ]
    
    for s in SERIES:
        cur.execute("""
        INSERT INTO site_series (code, title, href, tier, cluster, color, article_count, featured, external_link)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (code) DO UPDATE SET title=EXCLUDED.title, href=EXCLUDED.href, 
            tier=EXCLUDED.tier, cluster=EXCLUDED.cluster
        """, s)
    print(f"Inserted {len(SERIES)} series records")
    
    # Master narrative / reading order
    cur.execute("""
    DROP TABLE IF EXISTS site_narrative CASCADE;
    CREATE TABLE site_narrative (
        act_number INTEGER PRIMARY KEY,
        act_label TEXT NOT NULL,
        title TEXT NOT NULL,
        href TEXT,
        is_live BOOLEAN DEFAULT TRUE
    );
    """)
    NARRATIVE = [
        (1,"ACT 1","The Moral Decline of America","/moral-decline/",True),
        (2,"ACT 2","The Three Truths","#",False),
        (3,"ACT 3","The Playing Field","Convergence_Series/cns-01-the-playing-field.html",True),
        (4,"ACT 4","The Evidence","Convergence_Series/cns-02-the-evidence.html",True),
        (5,"ACT 5","Math Is Moral","convergence-deep/cdt-01-math-is-moral.html",True),
        (6,"ACT 6","The Measurement That Collapsed Reality","genesis-to-quantum/intro/gtq-01-measurement-collapsed-reality.html",True),
        (7,"ACT 7","Genesis to Quantum — Full Series","genesis-to-quantum/index.html",True),
        (8,"ACT 8","The Judgment Layer","Convergence_Series/cns-05-the-judgment-layer.html",True),
        (9,"ACT 9","The Logos Story","Logos_Papers/index.html",True),
        (10,"ACT 10","The Logos Papers","one-page-stories/The_Logos_Thesis_v3.html",True),
        (11,"ACT 11","Be Glad You're a Loser","be-glad-youre-a-loser/bgl-01-be-glad-youre-a-loser.html",True),
        (12,"ACT 12","We Ran the Tests","family-tests/we-ran-the-tests.html",True),
        (13,"ACT 13","The One Truth","#",False),
    ]
    for n in NARRATIVE:
        cur.execute("INSERT INTO site_narrative VALUES (%s,%s,%s,%s,%s)", n)
    print(f"Inserted {len(NARRATIVE)} narrative acts")
    
    # Summary stats
    cur.execute("SELECT COUNT(*) FROM site_pages")
    pages = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM site_series")
    series = cur.fetchone()[0]
    cur.execute("SELECT series, COUNT(*) FROM site_pages GROUP BY series ORDER BY COUNT(*) DESC LIMIT 15")
    by_series = cur.fetchall()
    
    print(f"\n{'='*60}")
    print(f"SYNC COMPLETE")
    print(f"  site_pages:    {pages} rows")
    print(f"  site_series:   {series} rows")
    print(f"  site_narrative: {len(NARRATIVE)} rows")
    print(f"\nTop directories:")
    for s, c in by_series:
        print(f"  {s:40s} {c:>4d} pages")
    print(f"{'='*60}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
