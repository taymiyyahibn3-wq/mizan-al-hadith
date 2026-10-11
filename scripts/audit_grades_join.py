import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/hadith-kg.db')
conn.row_factory = sqlite3.Row

# Look at hadith_grades joined with hadiths for book_id = 6
rows = conn.execute("""
    SELECT hg.id as g_id, hg.hadith_id, h.no_inbook, hg.scholar, hg.grade, hg.reference_book, hg.reference_hadith, h.taraf_nass
    FROM hadith_grades hg
    JOIN hadiths h ON h.id = hg.hadith_id
    WHERE h.book_id = 6 AND h.no_inbook BETWEEN 1965 AND 1990
    ORDER BY h.no_inbook, hg.id
""").fetchall()

prev_no = None
for r in rows:
    if r['no_inbook'] != prev_no:
        print(f"\n--- Hadith ID {r['hadith_id']} (no_inbook={r['no_inbook']}): {r['taraf_nass'][:40]} ---")
        prev_no = r['no_inbook']
    print(f"   g_id={r['g_id']}: scholar={r['scholar']} grade={r['grade']} ref_book={r['reference_book']} ref_hadith={r['reference_hadith']}")
