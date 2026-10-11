import sqlite3
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

def extract_and_classify_records():
    records = []
    
    # 1. Abu Dawud (Book 4)
    c.execute("SELECT id, book_id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 4 AND taraf_nass LIKE '%قال أبو داود%' ORDER BY id")
    ad_rows = c.fetchall()
    
    for hid, bid, no_inbook, taraf in ad_rows:
        idx = taraf.find("قال أبو داود")
        full_text = taraf[idx:].strip()
        
        # Determine core verbatim statement (up to first major sentence or punctuation, or full text if short)
        sentences = re.split(r'[\.\n\r]+', full_text)
        verbatim = sentences[0].strip() if sentences else full_text
        if len(verbatim) < 20 and len(sentences) > 1:
            verbatim = (sentences[0] + " " + sentences[1]).strip()
            
        # Classify
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
            
        records.append({
            "hadith_id": hid,
            "book_id": bid,
            "no_inbook": no_inbook,
            "scholar_id": "abu_dawud",
            "scholar_en": "al-Imām Abū Dāwūd",
            "scholar_ar": "أبو داود السجستاني",
            "work_en": "Sunan Abī Dāwūd",
            "work_ar": "سنن أبي داود",
            "evidence_type": ev_type,
            "canonical_term": term,
            "verbatim_arabic": verbatim,
            "full_context_arabic": full_text,
            "attribution": "Direct authorial remark preserved in transmitted text of Sunan Abī Dāwūd",
            "license": "Public Domain (Classical Work, d. 275 AH)",
            "verification_status": "verified"
        })
        
    print(f"Extracted Abu Dawud records: {len([r for r in records if r['scholar_id'] == 'abu_dawud'])}")
    
    # 2. al-Nasai (Book 5)
    c.execute("SELECT id, book_id, no_inbook, taraf_nass FROM hadiths WHERE book_id = 5 AND taraf_nass LIKE '%قال أبو عبد الرحمن%' ORDER BY id")
    ns_rows = c.fetchall()
    
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
            
        records.append({
            "hadith_id": hid,
            "book_id": bid,
            "no_inbook": no_inbook,
            "scholar_id": "al_nasai",
            "scholar_en": "al-Imām al-Nasāʾī",
            "scholar_ar": "أبو عبد الرحمن النسائي",
            "work_en": "al-Sunan al-Ṣughrā (al-Mujtabā)",
            "work_ar": "السنن الصغرى (المجتبى)",
            "evidence_type": ev_type,
            "canonical_term": term,
            "verbatim_arabic": verbatim,
            "full_context_arabic": full_text,
            "attribution": "Direct authorial remark preserved in transmitted text of al-Sunan al-Ṣughrā",
            "license": "Public Domain (Classical Work, d. 303 AH)",
            "verification_status": "verified"
        })
        
    print(f"Extracted Al-Nasai records: {len([r for r in records if r['scholar_id'] == 'al_nasai'])}")
    print(f"Total extracted new records: {len(records)}")
    
    # Evidence type distribution
    for sid in ["abu_dawud", "al_nasai"]:
        sub = [r for r in records if r["scholar_id"] == sid]
        print(f"\n{sid} Breakdown:")
        eg = len([r for r in sub if r["evidence_type"] == "explicit_hadith_grade"])
        hc = len([r for r in sub if r["evidence_type"] == "hadith_criticism"])
        print(f"  Explicit Hadith Grades: {eg}")
        print(f"  Hadith Criticism:       {hc}")
        
    return records

extract_and_classify_records()
