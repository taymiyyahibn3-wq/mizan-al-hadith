import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('file:data/hadith_commentaries.db?mode=ro', uri=True)
c = conn.cursor()

print("--- commentary_sources ---")
for r in c.execute("SELECT id, slug, name_en, author_en, author_death_year, publisher, license FROM commentary_sources").fetchall():
    print(r)

print("\n--- commentators in hadith_commentaries ---")
for r in c.execute("SELECT commentator_en, count(*) FROM hadith_commentaries GROUP BY commentator_en").fetchall():
    print(r)

conn.close()
