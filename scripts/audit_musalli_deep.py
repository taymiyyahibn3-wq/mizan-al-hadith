import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/hadith-kg.db')
conn.row_factory = sqlite3.Row

print("=== RAWIS MATCHING المسلي OR مصلي ===")
rawis = conn.execute("""
    SELECT id, name, nickname, rank, tabaka, profession, nasab
    FROM rawis
    WHERE name LIKE '%مسلي%' OR nickname LIKE '%مسلي%' OR profession LIKE '%مسلي%'
       OR name LIKE '%مصلي%' OR nickname LIKE '%مصلي%' OR profession LIKE '%مصلي%'
""").fetchall()
for r in rawis:
    print(dict(r))

print("\n=== AQWAL FOR RAWI 4256 ===")
aqwal = conn.execute("""
    SELECT a.*, e.name as alem_name, e.shuhra as alem_shuhra
    FROM aqwal a
    LEFT JOIN alems e ON e.id = a.alem_id
    WHERE a.rawi_id = 4256
""").fetchall()
for a in aqwal:
    print(dict(a))

print("\n=== ALL AQWAL BY YAHYA IBN MA'IN (alem_id=2821) FOR THESE RAWIS ===")
for r in rawis:
    y_aqwal = conn.execute("""
        SELECT a.*, e.name as alem_name, e.shuhra as alem_shuhra
        FROM aqwal a
        LEFT JOIN alems e ON e.id = a.alem_id
        WHERE a.rawi_id = ? AND (a.alem_id = 2821 OR a.alem_id = 239)
    """, (r['id'],)).fetchall()
    if y_aqwal:
        print(f"Rawi {r['id']} ({r['nickname']}):")
        for ya in y_aqwal:
            print(f"   aqwal_id={ya['id']}, alem={ya['alem_shuhra']} ({ya['alem_id']}), qawl='{ya['qawl']}', source={ya['source_id']}")
