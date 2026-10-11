import sqlite3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

num_conn = sqlite3.connect('data/hadith_numbering.db')
num_conn.row_factory = sqlite3.Row
kg_conn = sqlite3.connect('data/hadith-kg.db')
kg_conn.row_factory = sqlite3.Row

print("=== NUMBERING SCHEMES ===")
for s in num_conn.execute("SELECT * FROM numbering_schemes").fetchall():
    print(dict(s))

print("\n=== LOOKUP 1986 IN hadith_numbers ===")
rows = num_conn.execute("""
    SELECT hn.*, ns.code, ns.display_name_en 
    FROM hadith_numbers hn
    JOIN numbering_schemes ns ON ns.id = hn.scheme_id
    WHERE hn.primary_number = '1986' OR hn.numeric_value = 1986
""").fetchall()
for r in rows:
    hid = r["hadith_id"]
    # Check book_id for this hadith_id in hadiths
    h = kg_conn.execute("SELECT id, book_id, no_inbook, taraf_nass, nass FROM hadiths WHERE id = ?", (hid,)).fetchone()
    if h and h["book_id"] == 6:
        print(f"Hadith ID {hid}: book_id={h['book_id']}, no_inbook={h['no_inbook']}, scheme={r['code']}:{r['primary_number']}")

print("\n=== CHECK IBN MAJAH HADITHS AROUND 1986 ===")
# What is in hadiths where book_id=6 and no_inbook in (1985, 1986, 1987) vs hadith_numbers?
h_rows = kg_conn.execute("""
    SELECT id, book_id, no_inbook, taraf_nass, nass 
    FROM hadiths 
    WHERE book_id = 6 AND (no_inbook BETWEEN 1970 AND 2000 OR id = 28581)
""").fetchall()
print(f"Found {len(h_rows)} hadiths in Ibn Majah in range.")
for h in h_rows:
    # Look for Abdur Rahman al-Musli in nass
    nass = str(h["nass"] or "")
    if "المسلي" in nass or "ضرب امرأته" in nass or h["no_inbook"] in (1976, 1986):
        print(f"Hadith ID {h['id']}: no_inbook={h['no_inbook']}, taraf={h['taraf_nass'][:50]}")
        # Check all numbers for this hadith
        nums = num_conn.execute("""
            SELECT hn.primary_number, ns.code, ns.display_name_en
            FROM hadith_numbers hn
            JOIN numbering_schemes ns ON ns.id = hn.scheme_id
            WHERE hn.hadith_id = ?
        """, (h["id"],)).fetchall()
        for nm in nums:
            print(f"   -> Numbering: {nm['code']} = {nm['primary_number']} ({nm['display_name_en']})")
        # Check all grades for this hadith
        grades = kg_conn.execute("SELECT * FROM hadith_grades WHERE hadith_id = ?", (h["id"],)).fetchall()
        for g in grades:
            print(f"   -> Grade: id={g['id']} scholar={g['scholar']} grade={g['grade']} ref_book={g['reference_book']} ref_hadith={g['reference_hadith']}")
