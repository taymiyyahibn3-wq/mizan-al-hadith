import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

print("=== SAMPLE ABU DAWUD REMARKS ===")
c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 4 AND taraf_nass LIKE '%قال أبو داود%' LIMIT 5")
for r in c.fetchall():
    print(f"Hadith {r[0]} (Sunan {r[1]}):")
    # find where قال أبو داود starts
    idx = r[2].find("قال أبو داود")
    print(r[2][max(0, idx-20):idx+200])
    print("-" * 50)

print("\n=== SAMPLE NASAI REMARKS ===")
c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 5 AND taraf_nass LIKE '%قال أبو عبد الرحمن%' LIMIT 5")
for r in c.fetchall():
    print(f"Hadith {r[0]} (Sunan {r[1]}):")
    idx = r[2].find("قال أبو عبد الرحمن")
    print(r[2][max(0, idx-20):idx+200])
    print("-" * 50)
