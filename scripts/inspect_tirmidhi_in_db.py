import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('file:data/hadith-kg.db?mode=ro', uri=True)
c = conn.cursor()

# Book 3 in hadith-kg.db is Jami' al-Tirmidhi
# Let's verify book 3
b = c.execute("SELECT id, name, author_name, english_name FROM books WHERE id = 3").fetchone()
print(f"Book 3: {b}")

# Check hadiths in book 3 for Abu Isa's statements: "قال أبو عيسى" or "حديث حسن"
sample_ids = [12426, 12427, 12428, 12429, 12430]
for hid in sample_ids:
    h = c.execute("SELECT id, no_inbook, page_no, taraf_nass, nass, matn FROM hadiths WHERE id = ?", (hid,)).fetchone()
    if h:
        nass_preview = (h[4][:200] if h[4] else "None").replace('\n', ' ')
        print(f"\nHadith ID {h[0]} (No in book {h[1]}):")
        print(f"  Taraf: {h[3]}")
        print(f"  Nass preview: {nass_preview}")
        has_abu_isa = "أبو عيسى" in (h[4] or "")
        has_hasan = "حسن" in (h[4] or "") or "صحيح" in (h[4] or "")
        print(f"  Contains 'أبو عيسى': {has_abu_isa} | Contains 'حسن/صحيح': {has_hasan}")

# Count how many hadiths in book 3 have "أبو عيسى" in nass
count_abu_isa = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3 AND nass LIKE '%أبو عيسى%'").fetchone()[0]
total_tirmidhi = c.execute("SELECT count(*) FROM hadiths WHERE book_id = 3").fetchone()[0]
print(f"\nTotal hadiths in Book 3: {total_tirmidhi:,}")
print(f"Hadiths containing 'أبو عيسى' in nass: {count_abu_isa:,} ({count_abu_isa/total_tirmidhi*100:.1f}%)")

conn.close()
