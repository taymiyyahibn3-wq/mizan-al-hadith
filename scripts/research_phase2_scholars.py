import sqlite3
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect("file:data/hadith-kg.db?mode=ro", uri=True)

books = conn.execute("SELECT id, name, tasnif, hadith_qty FROM books ORDER BY id").fetchall()
print("=== BOOKS IN HADITH-KG.DB ===")
for b in books:
    print(f"Book #{b[0]}: {b[1]} ({b[2]}), qty={b[3]}")

queries = [
    ("Book 4 (Abu Dawud)", 4, "قال أبو داود"),
    ("Book 4 (Abu Dawud - alt)", 4, "أبو داود"),
    ("Book 5 (Nasai)", 5, "قال أبو عبد الرحمن"),
    ("Book 5 (Nasai - alt)", 5, "قال النسائي"),
    ("Book 1 (Bukhari)", 1, "قال البخاري"),
    ("Book 1 (Bukhari - alt)", 1, "قال أبو عبد الله"),
    ("Book 2 (Muslim)", 2, "قال مسلم"),
    ("Book 2 (Muslim - alt)", 2, "قال أبو الحسين"),
    ("Book 6 (Ibn Majah)", 6, "قال أبو الحسن"),
    ("Book 6 (Ibn Majah - alt)", 6, "قال ابن ماجه"),
]

print("\n=== AUTHORIAL REMARKS IN TARAF_NASS ===")
for label, bid, phrase in queries:
    cnt = conn.execute("SELECT COUNT(*) FROM hadiths WHERE book_id = ? AND taraf_nass LIKE ?", (bid, f"%{phrase}%")).fetchone()[0]
    print(f"{label} with '{phrase}': {cnt}")

# Check sample texts in Book 4 (Abu Dawud)
print("\n=== SAMPLE REMARKS IN BOOK 4 (ABU DAWUD) ===")
rows_ad = conn.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 4 AND taraf_nass LIKE '%قال أبو داود%' LIMIT 10").fetchall()
for r in rows_ad:
    idx = r[2].find("قال أبو داود")
    snippet = r[2][idx:idx+150].strip().replace('\n', ' ')
    print(f"Hadith #{r[0]} (Sunan #{r[1]}): {snippet}")

# Check sample texts in Book 5 (Nasai)
print("\n=== SAMPLE REMARKS IN BOOK 5 (NASAI) ===")
rows_nas = conn.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 5 AND taraf_nass LIKE '%قال أبو عبد الرحمن%' LIMIT 10").fetchall()
for r in rows_nas:
    idx = r[2].find("قال أبو عبد الرحمن")
    snippet = r[2][idx:idx+150].strip().replace('\n', ' ')
    print(f"Hadith #{r[0]} (Sunan #{r[1]}): {snippet}")

conn.close()
