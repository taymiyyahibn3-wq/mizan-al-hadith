import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

rows = db.execute("""
SELECT
    collection,
    hadith_number,
    reference_book,
    reference_hadith
FROM hadith_pro_hadiths
WHERE reference_book = 1
  AND reference_hadith = 1
ORDER BY collection, hadith_number
""").fetchall()

print("=== REFERENCES TO BUKHARI #1 ===")
for row in rows:
    print(row)

print("\nTOTAL:", len(rows))

db.close()
