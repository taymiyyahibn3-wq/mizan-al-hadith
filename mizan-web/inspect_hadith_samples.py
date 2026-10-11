import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

checks = [
    ("hadiths", "SELECT * FROM hadiths LIMIT 3"),
    ("meaning_groups", "SELECT * FROM meaning_groups LIMIT 10"),
    ("group_embedding", "SELECT * FROM group_embedding LIMIT 5"),
    ("hadith_pro_hadiths", "SELECT * FROM hadith_pro_hadiths LIMIT 10"),
    ("tarafs", "SELECT * FROM tarafs LIMIT 10"),
    ("hadith_rawis", "SELECT * FROM hadith_rawis LIMIT 10"),
    ("hadith_grades", "SELECT * FROM hadith_grades LIMIT 10"),
]

for name, query in checks:
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    try:
        rows = db.execute(query).fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("ERROR:", e)

db.close()
