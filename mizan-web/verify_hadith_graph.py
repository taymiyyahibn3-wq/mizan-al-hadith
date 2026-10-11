import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

print("=" * 90)
print("REFERENCE BOOK MAPPING")
print("=" * 90)

for row in db.execute("""
    SELECT
        hp.reference_book,
        COUNT(*) AS cnt,
        b.id,
        b.name,
        b.english_name,
        b.transliteration
    FROM hadith_pro_hadiths hp
    LEFT JOIN books b
        ON b.id = hp.reference_book
    GROUP BY hp.reference_book
    ORDER BY cnt DESC
    LIMIT 60
"""):
    print(row)

print()
print("=" * 90)
print("SAMPLE WITH TARGET HADITH")
print("=" * 90)

for row in db.execute("""
    SELECT
        hp.collection,
        hp.hadith_number,
        hp.reference_book,
        hp.reference_hadith,
        b.name,
        b.english_name,
        h.id,
        h.book_id,
        h.no_inbook
    FROM hadith_pro_hadiths hp
    LEFT JOIN books b
        ON b.id = hp.reference_book
    LEFT JOIN hadiths h
        ON h.book_id = hp.reference_book
       AND h.no_inbook = hp.reference_hadith
    LIMIT 50
"""):
    print(row)

db.close()
