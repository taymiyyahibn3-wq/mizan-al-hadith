import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
kg = sqlite3.connect('data/hadith-kg.db')
kg.row_factory = sqlite3.Row
num = sqlite3.connect('data/hadith_numbering.db')
num.row_factory = sqlite3.Row

# Schemes in hadith_numbering.db:
# 3: bukhari_darussalam_en (book 1)
# 6: muslim_darussalam_en (book 2)
# 9: tirmidhi_darussalam_en (book 3)
# 12: abudawud_darussalam_en (book 4)
# 15: nasai_darussalam_en (book 5)
# 18: ibnmajah_darussalam_en (book 6)

collection_schemes = {
    'abudawud': (4, 12),
    'ibnmajah': (6, 18),
    'nasai': (5, 15),
    'tirmidhi': (3, 9),
}

# For Ibn Majah:
print("=== CHECK IBN MAJAH 1986 GRADES VIA PROPER RESOLVER ===")
# 1. Resolve canonical hadith_id from Darussalam 1986
r_num = num.execute("SELECT hadith_id FROM hadith_numbers WHERE scheme_id = 18 AND primary_number = '1986'").fetchone()
canonical_hid = r_num[0]
print(f"Darussalam 1986 -> canonical hadith_id: {canonical_hid}")

# 2. What hadith_pro row has collection='ibnmajah' and hadith_number=1986?
hp_row = kg.execute("SELECT * FROM hadith_pro_hadiths WHERE collection = 'ibnmajah' AND hadith_number = 1986").fetchone()
print(f"hadith_pro_hadiths: {dict(hp_row)}")

# 3. What grades in hadith_grades have reference_book=9 and reference_hadith=142?
hg_rows = kg.execute("SELECT * FROM hadith_grades WHERE reference_book = 9 AND reference_hadith = 142").fetchall()
print(f"Grades in hadith_grades for ref_book=9, ref_hadith=142 (total {len(hg_rows)}):")
for g in hg_rows:
    print(f"   id={g['id']} hadith_id={g['hadith_id']} scholar={g['scholar']} grade={g['grade']}")
