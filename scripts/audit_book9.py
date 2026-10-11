import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
for db_name in ['data/hadith_numbering.db', 'data/hadith-kg.db']:
    conn = sqlite3.connect(db_name)
    tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print(db_name, tables)
