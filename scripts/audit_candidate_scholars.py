import sqlite3
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('file:data/hadith-kg.db?mode=ro', uri=True)
c = conn.cursor()

candidates = [
    {
        "name": "al-Bukhari",
        "ar_name": "البخاري",
        "full_name": "Muḥammad ibn Ismāʿīl al-Bukhārī",
        "death": 256,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 1125 OR name LIKE '%محمد بن إسماعيل بن إبراهيم بن المغيرة%'",
    },
    {
        "name": "Ahmad ibn Hanbal",
        "ar_name": "أحمد بن حنبل",
        "full_name": "Aḥmad ibn Muḥammad ibn Ḥanbal",
        "death": 241,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 751 OR name LIKE '%أحمد بن محمد بن حنبل%'",
    },
    {
        "name": "Yahya ibn Ma'in",
        "ar_name": "يحيى بن معين",
        "full_name": "Yaḥyā ibn Maʿīn",
        "death": 233,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 2821 OR name LIKE '%يحيى بن معين%'",
    },
    {
        "name": "Ibn Hajar al-Asqalani",
        "ar_name": "ابن حجر العسقلاني",
        "full_name": "Aḥmad ibn ʿAlī ibn Ḥajar al-ʿAsqalānī",
        "death": 852,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 1011 OR name LIKE '%ابن حجر%'",
    },
    {
        "name": "Ali ibn al-Madini",
        "ar_name": "علي بن المديني",
        "full_name": "ʿAlī ibn ʿAbd Allāh ibn al-Madīnī",
        "death": 234,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id IN (2135, 2136) OR name LIKE '%المديني%'",
    },
    {
        "name": "Abu Zur'ah al-Razi",
        "ar_name": "أبو زرعة الرازي",
        "full_name": "ʿUbayd Allāh ibn ʿAbd al-Karīm al-Rāzī (Abū Zurʿah)",
        "death": 264,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 466 OR shuhra LIKE '%أبو زرعة الرازي%'",
    },
    {
        "name": "Abu Hatim al-Razi",
        "ar_name": "أبو حاتم الرازي",
        "full_name": "Muḥammad ibn Idrīs al-Rāzī (Abū Ḥātim)",
        "death": 277,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 429 OR shuhra LIKE '%أبو حاتم الرازي%'",
    },
    {
        "name": "al-Daraqutni",
        "ar_name": "الدارقطني",
        "full_name": "ʿAlī ibn ʿUmar al-Dāraquṭnī",
        "death": 385,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 1264 OR shuhra LIKE '%الدارقطني%'",
    },
    {
        "name": "al-Dhahabi",
        "ar_name": "الذهبي",
        "full_name": "Muḥammad ibn Aḥmad al-Dhahabī",
        "death": 748,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 1268 OR shuhra LIKE '%الذهبي%'",
    },
    {
        "name": "Ibn Abi Hatim",
        "ar_name": "ابن أبي حاتم الرازي",
        "full_name": "ʿAbd al-Raḥmān ibn Muḥammad ibn Abī Ḥātim",
        "death": 327,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 924 OR shuhra LIKE '%ابن أبي حاتم%'",
    },
    {
        "name": "Ibn Hibban",
        "ar_name": "ابن حبان",
        "full_name": "Muḥammad ibn Ḥibbān al-Bustī",
        "death": 354,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 431 OR shuhra LIKE '%ابن حبان%'",
    },
    {
        "name": "al-Tirmidhi",
        "ar_name": "الترمذي",
        "full_name": "Muḥammad ibn ʿĪsā al-Tirmidhī",
        "death": 279,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 621 OR shuhra LIKE '%أبو عيسى الترمذي%'",
    },
    {
        "name": "Abu Dawud",
        "ar_name": "أبو داود",
        "full_name": "Sulaymān ibn al-Ashʿath al-Sijistānī",
        "death": 275,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 459 OR shuhra LIKE '%أبو داود السجستاني%'",
    },
    {
        "name": "al-Nasa'i",
        "ar_name": "النسائي",
        "full_name": "Aḥmad ibn Shuʿayb al-Nasāʾī",
        "death": 303,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 767 OR shuhra LIKE '%النسائي%'",
    },
    {
        "name": "Malik ibn Anas",
        "ar_name": "مالك بن أنس",
        "full_name": "Mālik ibn Anas",
        "death": 179,
        "alem_query": "SELECT id, name, shuhra, death_year, aqwal_qty FROM alems WHERE id = 2289 OR name LIKE '%مالك بن أنس%'",
    }
]

print("AUDITING CANDIDATES...")
audit_results = []
for cand in candidates:
    # 1. Hadith-level grades
    c.execute("SELECT count(*) FROM hadith_grades WHERE scholar LIKE ? OR scholar LIKE ?", (f"%{cand['name']}%", f"%{cand['ar_name']}%"))
    hg_count = c.fetchone()[0]

    # 2. Alem presence
    c.execute(cand['alem_query'])
    alem_rows = c.fetchall()
    alem_ids = [r[0] for r in alem_rows]
    alem_aqwal_sum = sum(r[4] for r in alem_rows)

    # 3. Direct count in aqwal table
    if alem_ids:
        placeholders = ','.join('?' * len(alem_ids))
        c.execute(f"SELECT count(*) FROM aqwal WHERE alem_id IN ({placeholders})", alem_ids)
        aqwal_count = c.fetchone()[0]

        # Sample 3 aqwal
        c.execute(f"""
            SELECT a.qawl, r.name 
            FROM aqwal a 
            JOIN rawis r ON r.id = a.rawi_id 
            WHERE a.alem_id IN ({placeholders}) 
            LIMIT 3
        """, alem_ids)
        samples = [{"qawl": row[0], "narrator": row[1]} for row in c.fetchall()]
    else:
        aqwal_count = 0
        samples = []

    res = {
        "candidate": cand["name"],
        "arabic_name": cand["ar_name"],
        "full_name": cand["full_name"],
        "death_year_ah": cand["death"],
        "exists_in_hadith_grades": hg_count > 0,
        "hadith_grade_count": hg_count,
        "exists_in_alems": len(alem_rows) > 0,
        "alem_ids": alem_ids,
        "narrator_aqwal_count": aqwal_count,
        "sample_aqwal": samples
    }
    audit_results.append(res)
    print(f"[{cand['name']}] Hadith Grades: {hg_count} | Alems: {len(alem_rows)} (IDs: {alem_ids}) | Narrator Aqwal: {aqwal_count:,}")

conn.close()

with open("scripts/audit_candidates_out.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, ensure_ascii=False, indent=2)
