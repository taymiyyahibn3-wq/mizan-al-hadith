import sqlite3
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('file:data/hadith-kg.db?mode=ro', uri=True)
c = conn.cursor()

total = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3").fetchone()[0]
count_taraf = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3 AND taraf_nass LIKE '%أبو عيسى%'").fetchone()[0]
count_qala_taraf = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3 AND taraf_nass LIKE '%قال أبو عيسى%'").fetchone()[0]
count_hasan = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3 AND taraf_nass LIKE '%حديث حسن%'").fetchone()[0]
count_sahih = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3 AND taraf_nass LIKE '%حديث صحيح%'").fetchone()[0]
count_hasan_sahih = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3 AND (taraf_nass LIKE '%حسن صحيح%' OR taraf_nass LIKE '%حسن غريب%')").fetchone()[0]

print(f"Book 3 (Jami' al-Tirmidhi) Total Hadiths: {total:,}")
print(f"taraf_nass containing 'أبو عيسى': {count_taraf:,} ({count_taraf/total*100:.1f}%)")
print(f"taraf_nass containing 'قال أبو عيسى': {count_qala_taraf:,} ({count_qala_taraf/total*100:.1f}%)")
print(f"taraf_nass containing 'حديث حسن': {count_hasan:,} ({count_hasan/total*100:.1f}%)")
print(f"taraf_nass containing 'حسن صحيح / حسن غريب': {count_hasan_sahih:,} ({count_hasan_sahih/total*100:.1f}%)")

print("\n--- SAMPLE EXTRACTED STATEMENTS FROM JAMI' AL-TIRMIDHI ---")
rows = c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 3 AND taraf_nass LIKE '%قال أبو عيسى%' LIMIT 10").fetchall()
for r in rows:
    taraf = r[2]
    # find where "قال أبو عيسى" starts
    idx = taraf.find("قال أبو عيسى")
    stmt = taraf[idx:]
    print(f"Hadith #{r[0]} (No in book {r[1]}): {stmt[:120]}...")

conn.close()
