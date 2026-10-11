import sys
import sqlite3

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/hadith-kg.db')
conn.row_factory = sqlite3.Row

print("=== RAWI 4256 (Abdur Rahman al-Musli) ===")
r = conn.execute("SELECT * FROM rawis WHERE id = 4256").fetchone()
print(dict(r))
print("\nAQWAL FOR 4256:")
for a in conn.execute("SELECT a.id, a.alem_id, al.name, al.shuhra, a.qawl FROM aqwal a LEFT JOIN alems al ON al.id = a.alem_id WHERE a.rawi_id = 4256").fetchall():
    print(dict(a))

print("\n=== RAWI 8145 (Wabarah ibn Abdur Rahman al-Musli) ===")
r2 = conn.execute("SELECT * FROM rawis WHERE id = 8145").fetchone()
print(dict(r2))
print("\nAQWAL FOR 8145:")
for a in conn.execute("SELECT a.id, a.alem_id, al.name, al.shuhra, a.qawl FROM aqwal a LEFT JOIN alems al ON al.id = a.alem_id WHERE a.rawi_id = 8145").fetchall():
    print(dict(a))

conn.close()
