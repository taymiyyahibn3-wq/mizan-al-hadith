import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'mizan-web/backend')
from identity_resolution import search_canonical_identities, normalize_english, normalize_arabic

kg_db = sqlite3.connect('data/hadith-kg.db')
ee_db = sqlite3.connect('data/english_enrichment.db')
isnad_db = sqlite3.connect('data/isnad_network.db')

print('norm_en:', normalize_english('Abdur Rahman al-Musalli'))
print('norm_ar:', normalize_arabic('Abdur Rahman al-Musalli'))

# Check rawis table directly
r = kg_db.execute("SELECT id, name, nickname FROM rawis WHERE nickname LIKE '%مسل%'").fetchall()
print('rawis matching مسل:')
for x in r:
    print(x)

# Check narrator_names table in ee_db
en_r = ee_db.execute("SELECT * FROM narrator_names WHERE rawi_id in (4256, 8145)").fetchall()
print('narrator_names for 4256, 8145 in ee_db:', en_r)

res = search_canonical_identities('Abdur Rahman al-Musalli', kg_db, isnad_db=isnad_db, ee_db=ee_db)
print('res count:', res.get('count'))
print('res results:', res.get('results'))

kg_db.close()
ee_db.close()
isnad_db.close()
