import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('file:data/hadith-kg.db?mode=ro', uri=True)
c = conn.cursor()

print("--- sanads.hukum inspection ---")
c.execute("SELECT count(*) FROM sanads WHERE hukum IS NOT NULL AND hukum != ''")
non_null_hukum = c.fetchone()[0]
print(f"Non-null hukum in sanads: {non_null_hukum:,}")

if non_null_hukum > 0:
    c.execute("SELECT hukum, count(*) FROM sanads WHERE hukum IS NOT NULL AND hukum != '' GROUP BY hukum ORDER BY count(*) DESC LIMIT 20")
    for r in c.fetchall():
        print(f"  Hukum: '{r[0]}' ({r[1]:,})")

print("\n--- hadiths.takhrij inspection ---")
c.execute("SELECT count(*) FROM hadiths WHERE takhrij IS NOT NULL AND takhrij != ''")
non_null_takhrij = c.fetchone()[0]
print(f"Non-null takhrij in hadiths: {non_null_takhrij:,}")
if non_null_takhrij > 0:
    c.execute("SELECT takhrij, count(*) FROM hadiths WHERE takhrij IS NOT NULL AND takhrij != '' LIMIT 10")
    for r in c.fetchall():
        print(f"  Takhrij: '{r[0]}'")

conn.close()
