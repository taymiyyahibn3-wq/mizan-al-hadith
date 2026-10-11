import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
kg = sqlite3.connect('data/hadith-kg.db')
num = sqlite3.connect('data/hadith_numbering.db')

collections = {
    'abudawud': (4, 12),
    'ibnmajah': (6, 18),
    'nasai': (5, 15),
    'tirmidhi': (3, 9),
}

for col, (book_id, scheme_id) in collections.items():
    mismatches = 0
    matches = 0
    missing_in_num = 0
    rows = kg.execute("SELECT DISTINCT hadith_number FROM hadith_pro_hadiths WHERE collection = ?", (col,)).fetchall()
    for row in rows:
        d_num = str(row[0])
        num_row = num.execute("SELECT hadith_id FROM hadith_numbers WHERE scheme_id = ? AND primary_number = ?", (scheme_id, d_num)).fetchone()
        kg_row = kg.execute("SELECT id FROM hadiths WHERE book_id = ? AND no_inbook = ?", (book_id, int(d_num))).fetchone()
        
        if num_row and kg_row:
            if num_row[0] != kg_row[0]:
                mismatches += 1
            else:
                matches += 1
        elif not num_row:
            missing_in_num += 1

    print(f"Collection {col}: Matches={matches}, Mismatches={mismatches}, MissingInScheme={missing_in_num}")
