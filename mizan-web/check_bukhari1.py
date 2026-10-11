import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

rows = db.execute("""
SELECT
    h.id,
    h.book_id,
    h.no_inbook,
    h.group_id,
    b.english_name,
    h.matn
FROM hadiths h
JOIN books b ON b.id = h.book_id
WHERE h.book_id = 1
  AND h.no_inbook = 1
""").fetchall()

print("=== BUKHARI #1 ===")
for row in rows:
    print(row)

db.close()
