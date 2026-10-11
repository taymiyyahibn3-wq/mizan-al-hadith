import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/hadith-kg.db')
conn.row_factory = sqlite3.Row

print("=== CHECK hadith_pro_hadiths FOR ibnmajah AROUND 1970-2000 ===")
rows = conn.execute("""
    SELECT * FROM hadith_pro_hadiths 
    WHERE collection = 'ibnmajah' AND (hadith_number BETWEEN 1970 AND 2000 OR reference_hadith IN (132, 142))
    ORDER BY id
""").fetchall()
for r in rows:
    print(dict(r))
