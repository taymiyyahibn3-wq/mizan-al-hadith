import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

tables = [
    "books",
    "hadiths",
    "hadith_pro_hadiths",
    "meaning_groups",
    "group_embedding",
    "tarafs",
    "sanads",
    "hadith_rawis",
]

for table in tables:
    print("\n" + "=" * 80)
    print("TABLE:", table)
    print("=" * 80)

    rows = db.execute(f"PRAGMA table_info({table})").fetchall()
    for r in rows:
        print(f"{r[1]:30} {r[2]:15} PK={r[5]}")

db.close()
