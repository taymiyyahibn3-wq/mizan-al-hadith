import sqlite3

db = sqlite3.connect("/data/hadith-kg.db")

print("=== TABLES ===")
for row in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(row[0])

db.close()
