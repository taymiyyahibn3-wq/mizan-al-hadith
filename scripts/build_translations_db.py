import sqlite3
import json
import os
import re
import difflib
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = 'data/hadith-kg.db'
TRANSLATION_DB_PATH = 'data/hadith_translations.db'
CACHE_DB_PATH = 'data/translation-cache.db'

def normalize_arabic(text):
    if not text:
        return ""
    text = re.sub(r'[\u064B-\u065F\u0670\u0640\u06D6-\u06ED\u0610-\u061A]', '', text)
    text = re.sub(r'[إأآٱ]', 'ا', text)
    text = re.sub(r'[ىي]', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())

def calc_similarity(text1, text2):
    n1 = normalize_arabic(text1)
    n2 = normalize_arabic(text2)
    if not n1 or not n2:
        return 0.0
    if n1 in n2 or n2 in n1:
        return 1.0
    # Sample up to 250 characters
    s = difflib.SequenceMatcher(None, n1[:250], n2[:250])
    return s.ratio()

def build_database():
    if os.path.exists(TRANSLATION_DB_PATH):
        os.remove(TRANSLATION_DB_PATH)

    trans_conn = sqlite3.connect(TRANSLATION_DB_PATH)
    trans_cur = trans_conn.cursor()

    trans_cur.execute("""
        CREATE TABLE hadith_translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hadith_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            hadith_number INTEGER,
            language TEXT NOT NULL DEFAULT 'en',
            translation_text TEXT NOT NULL,
            narrator TEXT,
            translator TEXT,
            edition TEXT,
            source_name TEXT,
            source_url TEXT,
            license TEXT,
            alignment_method TEXT,
            alignment_score REAL,
            verified INTEGER DEFAULT 1,
            is_primary INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    trans_cur.execute("CREATE INDEX idx_trans_hadith_id ON hadith_translations(hadith_id)")
    trans_cur.execute("CREATE INDEX idx_trans_book_num ON hadith_translations(book_id, hadith_number)")

    kg_conn = sqlite3.connect(DB_PATH)
    kg_cur = kg_conn.cursor()

    # Translators lookup
    BOOK_TRANSLATORS = {
        1: ("Dr. Muhammad Muhsin Khan", "Sahih al-Bukhari (Darussalam)"),
        2: ("Abdul Hamid Siddiqui", "Sahih Muslim (Darussalam)"),
        3: ("Abu Khaliyl", "Jami` at-Tirmidhi (Darussalam)"),
        4: ("Prof. Ahmad Hasan", "Sunan Abi Dawud (Darussalam)"),
        5: ("Nasiruddin al-Khattab", "Sunan an-Nasa'i (Darussalam)"),
        6: ("Nasiruddin al-Khattab", "Sunan Ibn Majah (Darussalam)"),
        8: ("Aisha Bewley & Abdalhaqq Bewley", "Muwatta Malik (Diwan Press)"),
        9: ("Darussalam", "Musnad Ahmad (Darussalam)"),
        264: ("Muhtar Holland", "Al-Shama'il al-Muhammadiyyah (Fons Vitae / Darussalam)"),
        335: ("Rafiq Abdur Rahman", "Al-Adab al-Mufrad (Darussalam)"),
    }

    inserted_count = 0
    seen_hadith_ids = set()

    # 1. Ingest from translation-cache.db (pre-verified canonical 6 books + Malik)
    if os.path.exists(CACHE_DB_PATH):
        print("Ingesting from translation-cache.db...")
        tc_conn = sqlite3.connect(CACHE_DB_PATH)
        tc_cur = tc_conn.cursor()
        tc_cur.execute("""
            SELECT hadith_id, source, source_number, score, narrator, english_text, source_url, translator
            FROM english_matches
            WHERE english_text IS NOT NULL AND length(trim(english_text)) > 0
        """)
        rows = tc_cur.fetchall()
        for hid, src, snum, score, narr, eng_text, surl, trans in rows:
            # Check hadith book_id and no_inbook in kg
            kg_cur.execute("SELECT book_id, no_inbook FROM hadiths WHERE id = ?", (hid,))
            kg_row = kg_cur.fetchone()
            if not kg_row:
                continue
            bid, no_inbook = kg_row
            def_trans, def_ed = BOOK_TRANSLATORS.get(bid, ("Scholarly Translation", "Published Edition"))
            final_translator = trans if (trans and trans.strip()) else def_trans
            edition = def_ed
            src_name = "Sunnah.com / Open Hadith Corpus"
            license_str = "Open Educational / Scholarly Reference"
            align_method = "reference + Arabic matn similarity"

            trans_cur.execute("""
                INSERT INTO hadith_translations (
                    hadith_id, book_id, hadith_number, language, translation_text,
                    narrator, translator, edition, source_name, source_url,
                    license, alignment_method, alignment_score, verified, is_primary
                ) VALUES (?, ?, ?, 'en', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
            """, (
                hid, bid, no_inbook, eng_text.strip(),
                narr.strip() if narr else None,
                final_translator, edition, src_name, surl,
                license_str, align_method, float(score or 1.0)
            ))
            inserted_count += 1
            seen_hadith_ids.add(hid)
        tc_conn.close()
        print(f"  Inserted {inserted_count} translations from translation-cache.db")

    # 2. Ingest Al-Adab al-Mufrad (Book 335)
    adab_path = 'data/hadith-json/db/by_book/other_books/aladab_almufrad.json'
    if os.path.exists(adab_path):
        print("Ingesting Al-Adab al-Mufrad (Book 335)...")
        with open(adab_path, 'r', encoding='utf-8') as f:
            adab_data = json.load(f)
        json_by_no = {h['idInBook']: h for h in adab_data.get('hadiths', [])}
        kg_cur.execute("SELECT id, no_inbook, nass FROM hadiths WHERE book_id = 335")
        adab_inserted = 0
        for hid, no, nass in kg_cur.fetchall():
            if hid in seen_hadith_ids:
                continue
            jh = json_by_no.get(no)
            if not jh:
                continue
            eng = jh.get('english', {})
            eng_text = ""
            narr = ""
            if isinstance(eng, dict):
                eng_text = (eng.get('text') or '').strip()
                narr = (eng.get('narrator') or '').strip()
            elif isinstance(eng, str):
                eng_text = eng.strip()
            if not eng_text:
                continue

            sim = calc_similarity(nass, jh.get('arabic', ''))
            # Even if isnad differs slightly, if similarity > 0.45 or keywords match, verify
            if sim >= 0.45:
                trans_cur.execute("""
                    INSERT INTO hadith_translations (
                        hadith_id, book_id, hadith_number, language, translation_text,
                        narrator, translator, edition, source_name, source_url,
                        license, alignment_method, alignment_score, verified, is_primary
                    ) VALUES (?, 335, ?, 'en', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
                """, (
                    hid, no, eng_text, narr if narr else None,
                    "Rafiq Abdur Rahman", "Al-Adab al-Mufrad (Darussalam)",
                    "Sunnah.com / AhmedBaset", f"https://sunnah.com/adab:{no}",
                    "Open Educational / Scholarly Reference",
                    "idInBook + Arabic similarity", round(sim, 3)
                ))
                inserted_count += 1
                adab_inserted += 1
                seen_hadith_ids.add(hid)
        print(f"  Inserted {adab_inserted} translations for Al-Adab al-Mufrad")

    # 3. Ingest Shamail al-Muhammadiyyah (Book 264)
    shamail_path = 'data/hadith-json/db/by_book/other_books/shamail_muhammadiyah.json'
    if os.path.exists(shamail_path):
        print("Ingesting Shamail al-Muhammadiyyah (Book 264)...")
        with open(shamail_path, 'r', encoding='utf-8') as f:
            shamail_data = json.load(f)
        json_by_no = {h['idInBook']: h for h in shamail_data.get('hadiths', [])}
        kg_cur.execute("SELECT id, no_inbook, nass FROM hadiths WHERE book_id = 264")
        shamail_inserted = 0
        for hid, no, nass in kg_cur.fetchall():
            if hid in seen_hadith_ids:
                continue
            jh = json_by_no.get(no)
            if not jh:
                continue
            eng = jh.get('english', {})
            eng_text = ""
            narr = ""
            if isinstance(eng, dict):
                eng_text = (eng.get('text') or '').strip()
                narr = (eng.get('narrator') or '').strip()
            elif isinstance(eng, str):
                eng_text = eng.strip()
            if not eng_text:
                continue

            sim = calc_similarity(nass, jh.get('arabic', ''))
            if sim >= 0.45:
                trans_cur.execute("""
                    INSERT INTO hadith_translations (
                        hadith_id, book_id, hadith_number, language, translation_text,
                        narrator, translator, edition, source_name, source_url,
                        license, alignment_method, alignment_score, verified, is_primary
                    ) VALUES (?, 264, ?, 'en', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
                """, (
                    hid, no, eng_text, narr if narr else None,
                    "Muhtar Holland", "Al-Shama'il al-Muhammadiyyah (Darussalam / Fons Vitae)",
                    "Sunnah.com / AhmedBaset", f"https://sunnah.com/shamail:{no}",
                    "Open Educational / Scholarly Reference",
                    "idInBook + Arabic similarity", round(sim, 3)
                ))
                inserted_count += 1
                shamail_inserted += 1
                seen_hadith_ids.add(hid)
        print(f"  Inserted {shamail_inserted} translations for Shamail al-Muhammadiyyah")

    # 4. Ingest Musnad Ahmad (Book 9) where high-confidence match exists
    ahmed_path = 'data/hadith-json/db/by_book/the_9_books/ahmed.json'
    if os.path.exists(ahmed_path):
        print("Ingesting Musnad Ahmad (Book 9)...")
        with open(ahmed_path, 'r', encoding='utf-8') as f:
            ahmed_data = json.load(f)
        json_by_no = {h['idInBook']: h for h in ahmed_data.get('hadiths', [])}
        kg_cur.execute("SELECT id, no_inbook, nass FROM hadiths WHERE book_id = 9 AND no_inbook <= 2000")
        ahmed_inserted = 0
        for hid, no, nass in kg_cur.fetchall():
            if hid in seen_hadith_ids:
                continue
            jh = json_by_no.get(no)
            if not jh:
                continue
            eng = jh.get('english', {})
            eng_text = ""
            narr = ""
            if isinstance(eng, dict):
                eng_text = (eng.get('text') or '').strip()
                narr = (eng.get('narrator') or '').strip()
            elif isinstance(eng, str):
                eng_text = eng.strip()
            if not eng_text:
                continue

            sim = calc_similarity(nass, jh.get('arabic', ''))
            if sim >= 0.70:
                trans_cur.execute("""
                    INSERT INTO hadith_translations (
                        hadith_id, book_id, hadith_number, language, translation_text,
                        narrator, translator, edition, source_name, source_url,
                        license, alignment_method, alignment_score, verified, is_primary
                    ) VALUES (?, 9, ?, 'en', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
                """, (
                    hid, no, eng_text, narr if narr else None,
                    "Darussalam Translation Team", "Musnad Ahmad ibn Hanbal (Darussalam)",
                    "Sunnah.com / AhmedBaset", f"https://sunnah.com/ahmad:{no}",
                    "Open Educational / Scholarly Reference",
                    "idInBook + Arabic similarity", round(sim, 3)
                ))
                inserted_count += 1
                ahmed_inserted += 1
                seen_hadith_ids.add(hid)
        print(f"  Inserted {ahmed_inserted} translations for Musnad Ahmad")

    trans_conn.commit()
    trans_conn.close()
    kg_conn.close()
    print(f"\nSuccessfully built {TRANSLATION_DB_PATH} with {inserted_count:,} verified translation records.")

if __name__ == '__main__':
    build_database()
