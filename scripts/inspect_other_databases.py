import sqlite3
import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

def inspect_db(db_path):
    print(f"\n==================== {db_path} ====================")
    if not os.path.exists(db_path):
        print("Does not exist!")
        return
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in c.fetchall()]
    for t in tables:
        c.execute(f"SELECT COUNT(*) FROM `{t}`")
        cnt = c.fetchone()[0]
        c.execute(f"PRAGMA table_info(`{t}`)")
        cols = [col[1] for col in c.fetchall()]
        print(f"Table '{t}': {cnt:,} rows | Columns: {cols}")
        if cnt > 0 and t in ['metadata', 'subsystem_metadata', 'version', 'sources', 'authors']:
            c.execute(f"SELECT * FROM `{t}` LIMIT 5")
            print(f"  Sample metadata rows: {c.fetchall()}")
    conn.close()

def main():
    dbs = [
        "data/citation_enrichment.db",
        "data/isnad_network.db",
        "data/derived_embeddinggemma2_768d.db",
        "data/derived_semantic_index.db",
        "data/classical_scholar_evidence.db",
        "data/english_enrichment.db"
    ]
    for db in dbs:
        inspect_db(db)

if __name__ == '__main__':
    main()
