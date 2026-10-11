import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

print("=" * 80)
print("hadith_pro_hadiths SAMPLE")
print("=" * 80)

rows = db.execute("""
    SELECT id, collection, hadith_number, reference_book, reference_hadith
    FROM hadith_pro_hadiths
    ORDER BY id
    LIMIT 30
""").fetchall()

for r in rows:
    print(r)

print()
print("=" * 80)
print("COUNTS")
print("=" * 80)

print("TOTAL:", db.execute("""
    SELECT COUNT(*) FROM hadith_pro_hadiths
""").fetchone()[0])

print("COLLECTIONS:")

for r in db.execute("""
    SELECT collection, COUNT(*)
    FROM hadith_pro_hadiths
    GROUP BY collection
    ORDER BY COUNT(*) DESC
"""):
    print(r)

print()
print("=" * 80)
print("REFERENCE BOOKS")
print("=" * 80)

for r in db.execute("""
    SELECT reference_book, COUNT(*)
    FROM hadith_pro_hadiths
    GROUP BY reference_book
    ORDER BY COUNT(*) DESC
    LIMIT 30
"""):
    print(r)

db.close()
