import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

tables = [
    "hadiths",
    "books",
    "meaning_groups",
    "group_embedding",
    "hadith_pro_hadiths",
    "tarafs",
    "hadith_rawis",
    "hadith_grades"
]

for table in tables:
    print("\n" + "=" * 80)
    print(table)
    print("=" * 80)

    rows = db.execute(f"PRAGMA table_info({table})").fetchall()

    for row in rows:
        print(row)

db.close()
