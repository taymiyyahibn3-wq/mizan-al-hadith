import os
import sqlite3
import sys
import hashlib
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KG_DB_PATH = os.path.join(REPO_ROOT, "data", "hadith-kg.db")
DERIVED_DB_PATH = os.path.join(REPO_ROOT, "data", "classical_scholar_evidence.db")

print("=== STARTING PHASE 3 MIGRATION ===")

# 1. Connect to KG (READ-ONLY)
kg_conn = sqlite3.connect(f"file:{KG_DB_PATH}?mode=ro", uri=True)
kg_c = kg_conn.cursor()

# 2. Connect to Derived DB
derived_conn = sqlite3.connect(DERIVED_DB_PATH)
derived_c = derived_conn.cursor()

# Check initial baseline
initial_tirmidhi = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi'").fetchone()[0]
initial_grades = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi' AND evidence_type='explicit_hadith_grade'").fetchone()[0]
initial_crit = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi' AND evidence_type='hadith_criticism'").fetchone()[0]

print(f"Initial Tirmidhi total: {initial_tirmidhi} (Grades: {initial_grades}, Crit: {initial_crit})")
if initial_tirmidhi != 2726 or initial_grades != 1918 or initial_crit != 808:
    print("FATAL: Initial baseline corrupted before migration! Aborting.")
    sys.exit(1)

# Check scholars table
scholars_to_add = [
    (
        'abu_dawud',
        'al-Imām Abū Dāwūd',
        'أبو داود السجستاني',
        275,
        'Hadith Criticism, Isnād Analysis, and Fiqh al-Ḥadīth',
        'Early Classical (3rd Century AH)',
        'Direct authorial remarks, isnād defect diagnoses, and variant preferences preserved in Sunan Abī Dāwūd'
    ),
    (
        'al_nasai',
        'al-Imām al-Nasāʾī',
        'أبو عبد الرحمن النسائي',
        303,
        'Hadith Criticism, ʿIlal, and Comparative Isnād Evaluation',
        'Early Classical (4th Century AH)',
        'Direct authorial remarks, comparative tarjīḥ, and defect diagnoses preserved in al-Sunan al-Ṣughrā (al-Mujtabā)'
    )
]

for s in scholars_to_add:
    derived_c.execute("""
        INSERT OR REPLACE INTO classical_scholars (id, name_en, name_ar, death_year_ah, primary_field, era, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, s)

print("Inserted/updated classical_scholars table for abu_dawud and al_nasai.")

# Delete any previous records of abu_dawud or al_nasai in derived DB to ensure clean idempotence
derived_c.execute("DELETE FROM classical_hadith_evaluations WHERE scholar_id IN ('abu_dawud', 'al_nasai')")

# Extract Abu Dawud (Book 4)
kg_c.execute("SELECT id, book_id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 4 AND taraf_nass LIKE '%قال أبو داود%' ORDER BY id")
ad_rows = kg_c.fetchall()

ad_records = []
for hid, bid, no_inbook, taraf in ad_rows:
    idx = taraf.find("قال أبو داود")
    full_text = taraf[idx:].strip()
    
    sentences = re.split(r'[\.\n\r]+', full_text)
    verbatim = sentences[0].strip() if sentences else full_text
    if len(verbatim) < 20 and len(sentences) > 1:
        verbatim = (sentences[0] + " " + sentences[1]).strip()
        
    if re.search(r'وهو عندنا صحيح|هذا حديث صحيح|حديث\s+صحيح', full_text):
        ev_type = "explicit_hadith_grade"
        term = "Ṣaḥīḥ (Explicit)"
    elif re.search(r'حديث\s+حسن', full_text):
        ev_type = "explicit_hadith_grade"
        term = "Ḥasan (Explicit)"
    elif "حديث منكر" in full_text or "هذا منكر" in full_text or "هذا حديث منكر" in full_text:
        ev_type = "hadith_criticism"
        term = "Munkar (Hadith Criticism)"
    elif "ليس بصحيح" in full_text:
        ev_type = "hadith_criticism"
        term = "Laysa bi-Ṣaḥīḥ (Criticism)"
    elif "ضعيف" in full_text:
        ev_type = "hadith_criticism"
        term = "Transmitter Defect / Ḍaʿīf"
    elif "مرسل" in full_text:
        ev_type = "hadith_criticism"
        term = "Mursal (Isnād Defect)"
    elif "معضل" in full_text or "منقطع" in full_text or "انقطع" in full_text or "لم يسمع" in full_text or "لم يلقه" in full_text:
        ev_type = "hadith_criticism"
        term = "Inqitāʿ / Disconnection (Isnād Defect)"
    elif "وهم" in full_text or "خطأ" in full_text:
        ev_type = "hadith_criticism"
        term = "Transmission Error / Wahm"
    elif "أصح" in full_text or "أثبت" in full_text or "أتم" in full_text or "أولى" in full_text or "والصواب" in full_text or "هو الصواب" in full_text:
        ev_type = "hadith_criticism"
        term = "Comparative Tarjīḥ / Variant Preference"
    elif "لم يسنده إلا" in full_text or "لم يروه إلا" in full_text or "تفرد" in full_text:
        ev_type = "hadith_criticism"
        term = "Tafarrud / Solitary Route (Isnād Analysis)"
    elif "موقوف" in full_text or "مرفوع" in full_text:
        ev_type = "hadith_criticism"
        term = "Waqf / Rafʿ Distinction"
    elif "ليس بالقوي" in full_text or "ليس بقوي" in full_text or "ليس بذاك" in full_text:
        ev_type = "hadith_criticism"
        term = "Laysa bi-Qawī (Criticism)"
    else:
        ev_type = "hadith_criticism"
        term = "Classical Transmission Remark"
        
    ad_records.append((
        hid, bid, no_inbook,
        "abu_dawud", "al-Imām Abū Dāwūd", "أبو داود السجستاني",
        "Sunan Abī Dāwūd", "سنن أبي داود",
        ev_type, term, verbatim, full_text,
        "Direct authorial remark preserved in transmitted text of Sunan Abī Dāwūd",
        "Public Domain (Classical Work, d. 275 AH)",
        "verified"
    ))

# Extract Nasai (Book 5)
kg_c.execute("SELECT id, book_id, no_inbook, taraf_nass FROM hardiths WHERE book_id = 5" if False else "SELECT id, book_id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 5 AND taraf_nass LIKE '%قال أبو عبد الرحمن%' ORDER BY id")
ns_rows = kg_c.fetchall()

ns_records = []
for hid, bid, no_inbook, taraf in ns_rows:
    idx = taraf.find("قال أبو عبد الرحمن")
    full_text = taraf[idx:].strip()
    
    sentences = re.split(r'[\.\n\r]+', full_text)
    verbatim = sentences[0].strip() if sentences else full_text
    if len(verbatim) < 20 and len(sentences) > 1:
        verbatim = (sentences[0] + " " + sentences[1]).strip()
        
    if re.search(r'وهذا حديث صحيح|هذان الحديثان صحيحان', full_text):
        ev_type = "explicit_hadith_grade"
        term = "Ṣaḥīḥ (Explicit)"
    elif re.search(r'حديث\s+حسن', full_text):
        ev_type = "explicit_hadith_grade"
        term = "Ḥasan (Explicit)"
    elif "أشبه بالصواب" in full_text or "هو الصواب" in full_text or "والصواب" in full_text or "أولى بالصواب" in full_text or "أثبت" in full_text or "أصح" in full_text:
        ev_type = "hadith_criticism"
        term = "Comparative Tarjīḥ (Ashbah bi-al-Ṣawāb)"
    elif "خطأ" in full_text:
        ev_type = "hadith_criticism"
        term = "Khaṭaʾ (Transmission Defect)"
    elif "مرسل" in full_text:
        ev_type = "hadith_criticism"
        term = "Mursal (Isnād Defect)"
    elif "لم يسمع" in full_text or "منقطع" in full_text or "لم يلقه" in full_text:
        ev_type = "hadith_criticism"
        term = "Inqitāʿ / Disconnection (Isnād Defect)"
    elif "لا أعلم أحدا تابع" in full_text or "ما نعلم أحدا تابع" in full_text or "لم يتابع" in full_text:
        ev_type = "hadith_criticism"
        term = "Tafarrud / Lack of Corroboration"
    elif "ضعيف" in full_text or "ليس بالقوي" in full_text or "ليس بقوي" in full_text or "متروك" in full_text:
        ev_type = "hadith_criticism"
        term = "Transmitter Defect / Weakness"
    elif "منكر" in full_text:
        ev_type = "hadith_criticism"
        term = "Munkar (Hadith Criticism)"
    elif "موقوف" in full_text or "مرفوع" in full_text:
        ev_type = "hadith_criticism"
        term = "Waqf / Rafʿ Distinction"
    else:
        ev_type = "hadith_criticism"
        term = "Classical Transmission Remark"
        
    ns_records.append((
        hid, bid, no_inbook,
        "al_nasai", "al-Imām al-Nasāʾī", "أبو عبد الرحمن النسائي",
        "al-Sunan al-Ṣughrā (al-Mujtabā)", "السنن الصغرى (المجتبى)",
        ev_type, term, verbatim, full_text,
        "Direct authorial remark preserved in transmitted text of al-Sunan al-Ṣughrā",
        "Public Domain (Classical Work, d. 303 AH)",
        "verified"
    ))

print(f"Preparing to insert {len(ad_records)} Abu Dawud and {len(ns_records)} Nasai records...")

insert_sql = """
    INSERT INTO classical_hadith_evaluations (
        hadith_id, book_id, no_inbook, scholar_id, scholar_en, scholar_ar,
        work_en, work_ar, evidence_type, canonical_term, verbatim_arabic,
        full_context_arabic, attribution, license, verification_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

derived_c.executemany(insert_sql, ad_records)
derived_c.executemany(insert_sql, ns_records)
derived_conn.commit()

# Final validation checks
final_total = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations").fetchone()[0]
final_tirmidhi = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi'").fetchone()[0]
final_tirmidhi_grades = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi' AND evidence_type='explicit_hadith_grade'").fetchone()[0]
final_tirmidhi_crit = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi' AND evidence_type='hadith_criticism'").fetchone()[0]

final_ad = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='abu_dawud'").fetchone()[0]
final_ns = derived_c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_nasai'").fetchone()[0]

print(f"\n=== MIGRATION VERIFICATION ===")
print(f"Total Rows: {final_total} (Expected: 3462)")
print(f"Tirmidhi Rows: {final_tirmidhi} (Grades: {final_tirmidhi_grades}, Crit: {final_tirmidhi_crit})")
print(f"Abu Dawud Rows: {final_ad} (Expected: 585)")
print(f"Nasai Rows: {final_ns} (Expected: 151)")

if final_total != 3462 or final_tirmidhi != 2726 or final_ad != 585 or final_ns != 151:
    print("FATAL ERROR: Row counts mismatch! Aborting.")
    derived_conn.rollback()
    sys.exit(1)

# Clean up
kg_conn.close()
derived_conn.close()

# Hash post-state
h = hashlib.sha256()
with open(DERIVED_DB_PATH, "rb") as f:
    while chunk := f.read(1024*1024):
        h.update(chunk)
post_derived_sha = h.hexdigest()
print(f"Post-migration Derived DB SHA-256: {post_derived_sha}")

print("=== MIGRATION COMPLETED SUCCESSFULLY ===")
