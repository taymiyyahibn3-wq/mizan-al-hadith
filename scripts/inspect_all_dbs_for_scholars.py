import sqlite3
import os
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

dbs = sorted(glob.glob("data/*.db"))

print(f"Scanning {len(dbs)} databases in data/...")

for db in dbs:
    if "backup" in db:
        continue
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        c = conn.cursor()
        tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        print(f"\n============================\nDATABASE: {db}")
        for t in tables:
            try:
                count = c.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
                cols = [col[1] for col in c.execute(f'PRAGMA table_info("{t}")').fetchall()]
                print(f"  Table '{t}' ({count:,} rows): {cols}")
            except Exception as e:
                print(f"  Table '{t}': {e}")
        conn.close()
    except Exception as e:
        print(f"Error opening {db}: {e}")
