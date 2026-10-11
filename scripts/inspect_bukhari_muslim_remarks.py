import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

print("=== SAMPLE BUKHARI REMARKS IN BOOK 1 (67 total) ===")
c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 1 AND taraf_nass LIKE '%قال أبو عبد الله%' LIMIT 10")
for r in c.fetchall():
    idx = r[2].find("قال أبو عبد الله")
    print(f"Hadith #{r[0]} (Bukhari #{r[1]}): {r[2][idx:idx+150]}")
    print("-" * 50)

print("\n=== SAMPLE MUSLIM REMARKS IN BOOK 2 (15 total) ===")
c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 2 AND taraf_nass LIKE '%قال مسلم%' LIMIT 10")
for r in c.fetchall():
    idx = r[2].find("قال مسلم")
    print(f"Hadith #{r[0]} (Muslim #{r[1]}): {r[2][idx:idx+150]}")
    print("-" * 50)
