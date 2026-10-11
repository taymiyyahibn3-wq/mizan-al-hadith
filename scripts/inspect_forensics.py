import sqlite3
import os

db_path = "data/hadith-kg.db"
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
c = conn.cursor()

tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print(f"--- TABLES IN {db_path} ---")
for t in tables:
    try:
        count = c.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
        cols = [col[1] for col in c.execute(f'PRAGMA table_info("{t}")').fetchall()]
        print(f"{t}: {count:,} rows | columns: {cols}")
    except Exception as e:
        print(f"{t}: ERROR {e}")

conn.close()
