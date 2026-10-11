import sqlite3
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

def classify_abu_dawud(text):
    """
    Classifies an Abu Dawud remark according to controlled taxonomy:
    - HADITH_CRITICISM
    - ISNAD_DEFECT
    - VARIANT_PREFERENCE
    - COMPARATIVE_TARJIH
    - EXPLICIT_HADITH_GRADE (only if explicit sahih/hasan/da'if of hadith)
    - MATN_CRITICISM
    """
    # Check for explicit hadith grade
    # e.g. "هذا حديث صحيح", "حديث حسن", "هذا حديث منكر"
    if re.search(r'حديث\s+صحيح', text):
        return ("explicit_hadith_grade", "Ṣaḥīḥ (Explicit)", "Explicit Hadith Grade")
    if re.search(r'حديث\s+حسن', text):
        return ("explicit_hadith_grade", "Ḥasan (Explicit)", "Explicit Hadith Grade")
    if "حديث منكر" in text or "هذا منكر" in text:
        return ("hadith_criticism", "Munkar (Hadith Criticism)", "Hadith Criticism: Munkar")
    if "ضعيف" in text:
        if "رواه فلان... وهو ضعيف" in text or "فلان ضعيف" in text:
            return ("hadith_criticism", "Transmitter Weakness / Ḍaʿīf", "Hadith Criticism: Isnād Weakness")
        return ("hadith_criticism", "Ḍaʿīf (Criticism)", "Hadith Criticism: Weakness")
    if "مرسل" in text:
        return ("hadith_criticism", "Mursal (Isnād Defect)", "Isnād Defect: Irsaal")
    if "معضل" in text or "منقطع" in text or "انقطع" in text or "لم يسمع" in text or "لم يلقه" in text:
        return ("hadith_criticism", "Inqitāʿ / Disconnection (Isnād Defect)", "Isnād Defect: Disconnection")
    if "وهم" in text or "خطأ" in text:
        return ("hadith_criticism", "Transmission Error / Wahm", "Hadith Criticism: Error")
    if "أصح" in text or "أثبت" in text or "أتم" in text or "أولى" in text or "الصواب" in text:
        return ("hadith_criticism", "Comparative Tarjīḥ / Variant Preference", "Comparative Tarjīḥ: Variant Preference")
    if "لم يسنده إلا" in text or "لم يروه إلا" in text or "تفرد" in text:
        return ("hadith_criticism", "Tafarrud / Solitary Route (Isnād Analysis)", "Isnād Analysis: Solitary Transmission")
    if "موقوف" in text or "مرفوع" in text:
        return ("hadith_criticism", "Waqf / Rafʿ Distinction", "Isnād Analysis: Waqf vs Rafʿ")
    if "ليس بالقوي" in text or "ليس بقوي" in text or "ليس بذاك" in text:
        return ("hadith_criticism", "Laysa bi-Qawī (Criticism)", "Hadith Criticism: Laysa bi-Qawī")
        
    return ("hadith_criticism", "Classical Transmission Remark", "Classical Hadith Remark")

def classify_nasai(text):
    """
    Classifies an al-Nasai remark:
    - VARIANT_PREFERENCE / COMPARATIVE_TARJIH
    - ISNAD_DEFECT
    - HADITH_CRITICISM
    - EXPLICIT_HADITH_GRADE
    """
    if re.search(r'حديث\s+صحيح', text):
        return ("explicit_hadith_grade", "Ṣaḥīḥ (Explicit)", "Explicit Hadith Grade")
    if "أشبه بالصواب" in text or "هو الصواب" in text or "والصواب" in text or "أولى بالصواب" in text or "أثبت" in text or "أصح" in text:
        return ("hadith_criticism", "Comparative Tarjīḥ (Ashbah bi-al-Ṣawāb)", "Comparative Tarjīḥ: Variant Preference")
    if "خطأ" in text:
        return ("hadith_criticism", "Khaṭaʾ (Transmission Defect)", "Hadith Criticism: Transmission Defect")
    if "مرسل" in text:
        return ("hadith_criticism", "Mursal (Isnād Defect)", "Isnād Defect: Irsaal")
    if "لم يسمع" in text or "منقطع" in text or "لم يلقه" in text:
        return ("hadith_criticism", "Inqitāʿ / Disconnection (Isnād Defect)", "Isnād Defect: Disconnection")
    if "لا أعلم أحدا تابع" in text or "ما نعلم أحدا تابع" in text or "لم يتابع" in text:
        return ("hadith_criticism", "Tafarrud / Lack of Corroboration", "Isnād Analysis: Lack of Mutaba'ah")
    if "ضعيف" in text or "ليس بالقوي" in text or "ليس بقوي" in text or "متروك" in text:
        return ("hadith_criticism", "Transmitter Defect / Weakness", "Hadith Criticism: Transmitter Weakness")
    if "منكر" in text:
        return ("hadith_criticism", "Munkar (Hadith Criticism)", "Hadith Criticism: Munkar")
    if "موقوف" in text or "مرفوع" in text:
        return ("hadith_criticism", "Waqf / Rafʿ Distinction", "Isnād Analysis: Waqf vs Rafʿ")
        
    return ("hadith_criticism", "Classical Transmission Remark", "Classical Hadith Remark")

# Test Abu Dawud distribution
c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 4 AND taraf_nass LIKE '%قال أبو داود%'")
ad_rows = c.fetchall()
ad_types = {}
for r in ad_rows:
    idx = r[2].find("قال أبو داود")
    txt = r[2][idx:].strip()
    ev_type, term, desc = classify_abu_dawud(txt)
    ad_types[term] = ad_types.get(term, 0) + 1

print("Abu Dawud Taxonomy Distribution (585 records):")
for term, cnt in sorted(ad_types.items(), key=lambda x: -x[1]):
    print(f"  {term:45s}: {cnt}")

# Test Nasai distribution
c.execute("SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 5 AND taraf_nass LIKE '%قال أبو عبد الرحمن%'")
ns_rows = c.fetchall()
ns_types = {}
for r in ns_rows:
    idx = r[2].find("قال أبو عبد الرحمن")
    txt = r[2][idx:].strip()
    ev_type, term, desc = classify_nasai(txt)
    ns_types[term] = ns_types.get(term, 0) + 1

print("\nAl-Nasai Taxonomy Distribution (151 records):")
for term, cnt in sorted(ns_types.items(), key=lambda x: -x[1]):
    print(f"  {term:45s}: {cnt}")
