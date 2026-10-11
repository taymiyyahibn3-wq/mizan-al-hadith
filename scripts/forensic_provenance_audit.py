import sqlite3
import os
import json

out = {}

def default_serializer(obj):
    if isinstance(obj, bytes):
        return f"<bytes: len={len(obj)}>"
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def audit_all_dbs():
    dbs = {
        'hadith_kg': 'data/hadith-kg.db',
        'hadith_numbering': 'data/hadith_numbering.db',
        'hadith_commentaries': 'data/hadith_commentaries.db',
        'hadith_translations': 'data/hadith_translations.db',
        'citation_enrichment': 'data/citation_enrichment.db',
        'classical_scholar_evidence': 'data/classical_scholar_evidence.db'
    }
    
    for db_name, db_path in dbs.items():
        if not os.path.exists(db_path):
            continue
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [r[0] for r in c.fetchall()]
        db_res = {}
        for t in tables:
            c.execute(f"PRAGMA table_info(\"{t}\")")
            cols = [col[1] for col in c.fetchall()]
            c.execute(f"SELECT COUNT(*) FROM \"{t}\"")
            cnt = c.fetchone()[0]
            c.execute(f"SELECT * FROM \"{t}\" LIMIT 5")
            sample = c.fetchall()
            db_res[t] = {
                'count': cnt,
                'columns': cols,
                'samples': sample
            }
        conn.close()
        out[db_name] = db_res

audit_all_dbs()

os.makedirs('scratch', exist_ok=True)
with open('scratch/forensic_provenance_dump.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False, default=default_serializer)

print("Dynamic audit complete! Saved to scratch/forensic_provenance_dump.json")
