import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")
db.row_factory = sqlite3.Row

print("=== BUKHARI #1 ===")

h = db.execute("""
    SELECT
        h.*,
        b.name AS book_name,
        b.english_name
    FROM hadiths h
    LEFT JOIN books b ON b.id = h.book_id
    WHERE h.book_id = 1
      AND h.no_inbook = 1
    LIMIT 1
""").fetchone()

print("\nHADITH:")
print(dict(h) if h else None)

if h:
    print("\nSAME GROUP:")
    rows = db.execute("""
        SELECT
            h.id,
            h.book_id,
            b.name AS book_name,
            b.english_name,
            h.no_inbook,
            h.group_id,
            substr(h.matn, 1, 120) AS matn
        FROM hadiths h
        LEFT JOIN books b ON b.id = h.book_id
        WHERE h.group_id = ?
        ORDER BY h.book_id, h.no_inbook
    """, (h["group_id"],)).fetchall()

    for r in rows:
        print(dict(r))

    print("\nPRO HADITH LINKS:")
    rows = db.execute("""
        SELECT *
        FROM hadith_pro_hadiths
        WHERE
            (collection = '1' AND hadith_number = 1)
            OR
            (reference_book = 1 AND reference_hadith = 1)
        LIMIT 100
    """).fetchall()

    for r in rows:
        print(dict(r))

db.close()
