import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()
for row in c.execute("PRAGMA table_info(hadiths)"):
    print(row)

c.execute("SELECT count(*) FROM hadiths WHERE book_id = 4 AND taraf_nass LIKE '%قال أبو داود%'")
abu_dawud_count = c.fetchone()[0]

c.execute("SELECT count(*) FROM hadiths WHERE book_id = 5 AND taraf_nass LIKE '%قال أبو عبد الرحمن%'")
nasai_count = c.fetchone()[0]

print(f"Abu Dawud count: {abu_dawud_count}")
print(f"Nasai count: {nasai_count}")
