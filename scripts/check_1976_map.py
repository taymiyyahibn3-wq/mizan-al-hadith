import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
num = sqlite3.connect('data/hadith_numbering.db')
kg = sqlite3.connect('data/hadith-kg.db')

row = num.execute("SELECT hadith_id FROM hadith_numbers WHERE scheme_id = 18 AND primary_number = '1976'").fetchone()
if row:
    hid = row[0]
    h = kg.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE id = ?", (hid,)).fetchone()
    print("Darussalam 1976 maps to canonical hadith_id:", hid, "no_inbook:", h[1], "taraf:", h[2][:60])
