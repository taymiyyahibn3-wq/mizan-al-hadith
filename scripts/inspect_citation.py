import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('file:data/citation_enrichment.db?mode=ro', uri=True)
c = conn.cursor()
tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('citation_enrichment.db tables:', tables)
for t in tables:
    count = c.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
    cols = [col[1] for col in c.execute(f'PRAGMA table_info("{t}")').fetchall()]
    print(f'  {t} ({count:,}): {cols}')

if 'citations' in tables or 'crosswalk' in tables:
    t_name = 'citations' if 'citations' in tables else tables[0]
    c.execute(f"SELECT * FROM \"{t_name}\" LIMIT 5")
    print("Sample:", c.fetchall())

conn.close()
