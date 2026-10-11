import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")
db.row_factory = sqlite3.Row

print("=== hadith_pro_hadiths SAMPLE ===")

rows = db.execute("""
    SELECT
        id,
        collection,
        hadith_number,
        reference_book,
        reference_hadith
    FROM hadith_pro_hadiths
    LIMIT 30
""").fetchall()

for r in rows:
    print(dict(r))

db.close()
