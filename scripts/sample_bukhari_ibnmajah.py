import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect("file:data/hadith-kg.db?mode=ro", uri=True)

print("=== SAMPLE REMARKS IN BOOK 1 (BUKHARI) ===")
rows_b = conn.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 1 AND taraf_nass LIKE '%قال أبو عبد الله%' LIMIT 10").fetchall()
for r in rows_b:
    idx = r[2].find("قال أبو عبد الله")
    snippet = r[2][idx:idx+150].strip().replace('\n', ' ')
    print(f"Hadith #{r[0]} (Sahih #{r[1]}): {snippet}")

print("\n=== SAMPLE REMARKS IN BOOK 6 (IBN MAJAH) ===")
rows_im = conn.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 6 AND (taraf_nass LIKE '%قال أبو الحسن%' OR taraf_nass LIKE '%قال ابن ماجه%') LIMIT 10").fetchall()
for r in rows_im:
    snippet = r[2].strip().replace('\n', ' ')
    print(f"Hadith #{r[0]} (Sunan #{r[1]}): {snippet[:150]}")

conn.close()
