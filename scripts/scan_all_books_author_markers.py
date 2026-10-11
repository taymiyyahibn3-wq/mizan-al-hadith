import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

books = [
    (1, 'Sahih al-Bukhari'),
    (2, 'Sahih Muslim'),
    (3, 'Jami al-Tirmidhi'),
    (4, 'Sunan Abi Dawud'),
    (5, 'Sunan al-Nasai'),
    (6, 'Sunan Ibn Majah')
]

markers = [
    ('Bukhari', 'قال أبو عبد الله'),
    ('Muslim', 'قال مسلم'),
    ('Tirmidhi', 'قال أبو عيسى'),
    ('Abu Dawud', 'قال أبو داود'),
    ('Nasai', 'قال أبو عبد الرحمن'),
    ('Ibn Majah', 'قال ابن ماجه'),
    ('Ibn Majah (kunya)', 'قال أبو عبد الله ابن ماجه'),
    ('Abu al-Hasan (Ibn al-Qattan)', 'قال أبو الحسن')
]

print("=== SCANNING CANONICAL SIX BOOKS FOR AUTHORIAL REMARKS IN taraf_nass ===")
for b_id, b_name in books:
    print(f"\n--- Book {b_id}: {b_name} ---")
    for scholar_label, marker in markers:
        c.execute("SELECT count(*) FROM hadiths WHERE book_id = ? AND taraf_nass LIKE ?", (b_id, f'%{marker}%'))
        cnt = c.fetchone()[0]
        if cnt > 0:
            print(f"  {scholar_label} ('{marker}'): {cnt} records")
