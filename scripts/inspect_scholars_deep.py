import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')


print("=== 1. HADITH_GRADES SCHOLARS & SOURCES ===")
conn = sqlite3.connect("file:data/hadith-kg.db?mode=ro", uri=True)
c = conn.cursor()

c.execute("SELECT scholar, source, count(*) FROM hadith_grades GROUP BY scholar, source ORDER BY count(*) DESC")
rows = c.fetchall()
for r in rows:
    print(f"Scholar: '{r[0]}' | Source: '{r[1]}' | Count: {r[2]:,}")

print("\nSample rows from hadith_grades:")
c.execute("SELECT * FROM hadith_grades LIMIT 10")
for r in c.fetchall():
    print(r)

print("\n=== 2. ALEMS (CRITICS/SCHOLARS OF RIJAL) IN HADITH-KG.DB ===")
# Let's search for candidate scholars:
candidates = [
    "البخاري", "أحمد", "يحيى بن معين", "ابن حجر", "ابن المديني", "أبو زرعة", 
    "أبو حاتم", "الدارقطني", "الذهبي", "ابن أبي حاتم", "ابن حبان", "الترمذي", 
    "أبو داود", "النسائي", "مالك", "الشافعي", "سفيان", "شعبة"
]

for cand in candidates:
    c.execute("SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE name LIKE ? OR shuhra LIKE ? OR nickname LIKE ?", (f"%{cand}%", f"%{cand}%", f"%{cand}%"))
    results = c.fetchall()
    print(f"\nCandidate '{cand}': {len(results)} matches:")
    for res in results[:5]:
        print(f"  ID {res[0]}: {res[1]} (shuhra: {res[2]}, d. {res[3]}, aqwal: {res[4]})")

print("\nTargeted Candidates Search:")
queries = [
    ("Ali ibn al-Madini", "%المديني%"),
    ("Malik ibn Anas", "%مالك بن أنس%"),
    ("al-Tirmidhi", "%الترمذي%"),
    ("Abu Dawud", "%أبو داود%"),
    ("Abu Zur'ah", "%أبو زرعة%"),
    ("Abu Hatim", "%أبو حاتم%"),
    ("al-Daraqutni", "%الدارقطني%"),
    ("al-Dhahabi", "%الذهبي%"),
    ("Yahya ibn Ma'in", "%يحيى بن معين%"),
    ("Ahmad ibn Hanbal", "%أحمد بن حنبل%"),
    ("al-Bukhari", "%البخاري%"),
    ("Ibn Hajar", "%ابن حجر%")
]
for title, pat in queries:
    c.execute("SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE name LIKE ? OR shuhra LIKE ? OR nickname LIKE ?", (pat, pat, pat))
    res = c.fetchall()
    print(f"[{title}] count: {len(res)}")
    for r in res[:3]:
        print(f"   ID {r[0]}: {r[1]} | {r[2]} | d. {r[3]} | aqwal: {r[4]}")


conn.close()
