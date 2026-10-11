import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

collections = db.execute("""
SELECT DISTINCT collection
FROM hadith_pro_hadiths
ORDER BY collection
""").fetchall()

print("=== COLLECTIONS ===")

for (collection,) in collections:
    print(collection)

db.close()
