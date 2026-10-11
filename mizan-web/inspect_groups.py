import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")
db.row_factory = sqlite3.Row

print("=== BUKHARI HADITH GROUPS ===")

rows = db.execute("""
    SELECT
        h.id,
        h.book_id,
        h.no_inbook,
        h.group_id,
        substr(h.matn, 1, 120) AS matn
    FROM hadiths h
    WHERE h.book_id = 1
    ORDER BY h.no_inbook
    LIMIT 20
""").fetchall()

for r in rows:
    print(dict(r))

db.close()
