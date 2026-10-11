import sqlite3
import sys
import re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

def scan_terminology(book_id, marker, scholar_name):
    c.execute(f"SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = ? AND taraf_nass LIKE ?", (book_id, f'%{marker}%'))
    rows = c.fetchall()
    
    terms = [
        ("صحيح", "SAHIH"),
        ("حسن", "HASAN"),
        ("ضعيف", "DAIF"),
        ("منكر", "MUNKAR"),
        ("مرسل", "MURSAL"),
        ("معضل", "MU'DAL"),
        ("منقطع", "MUNQATI'"),
        ("ليس بالقوي", "LAYSA_BIL_QAWI"),
        ("ليس بقوي", "LAYSA_BI_QAWI"),
        ("ليس بذاك", "LAYSA_BI_DHAK"),
        ("لا بأس به", "LA_BA'SA_BIH"),
        ("وهم", "WAHM"),
        ("خطأ", "KHATA'"),
        ("أشبه بالصواب", "ASHBAHU_BIS_SAWAB"),
        ("هو الصواب", "HUWA_AS_SAWAB"),
        ("والصواب", "WAS_SAWAB"),
        ("أصح", "ASAHH"),
        ("أثبت", "ATHBAT"),
        ("أتم", "ATAMM"),
        ("أولى", "AWLA"),
        ("لم يسمع", "LAM_YASMA'"),
        ("لم يلقه", "LAM_YALQAH"),
        ("لم يروه إلا", "TAFARRUD"),
        ("لم يسنده إلا", "TAFARRUD_ISNAD"),
        ("لا أعلم أحدا تابع", "MUTABA'AH_NEGATION"),
        ("ما نعلم أحدا تابع", "MUTABA'AH_NEGATION"),
        ("موقوف", "MAWQUF"),
        ("مرفوع", "MARFU'"),
        ("مسند", "MUSNAD"),
    ]
    
    counts = Counter()
    samples = {t[1]: [] for t in terms}
    
    for r in rows:
        hid, no_inbook, taraf = r
        idx = taraf.find(marker)
        text = taraf[idx:]
        
        matched_any = False
        for arabic, code in terms:
            if re.search(r'\b' + re.escape(arabic), text):
                counts[code] += 1
                matched_any = True
                if len(samples[code]) < 3:
                    samples[code].append((hid, no_inbook, text[:100]))
                    
        if not matched_any:
            counts["OTHER_OBSERVATION"] += 1
            if len(samples.get("OTHER_OBSERVATION", [])) < 5:
                samples.setdefault("OTHER_OBSERVATION", []).append((hid, no_inbook, text[:100]))
                
    print(f"\n==========================================")
    print(f"Term frequencies for {scholar_name} (Total rows: {len(rows)}):")
    for code, cnt in counts.most_common():
        print(f"  {code:25s}: {cnt}")
        
    print(f"\nSamples of OTHER_OBSERVATION:")
    for hid, no_inbook, txt in samples.get("OTHER_OBSERVATION", [])[:5]:
        print(f"  [{hid} - #{no_inbook}] {txt}")

scan_terminology(4, "قال أبو داود", "Abu Dawud")
scan_terminology(5, "قال أبو عبد الرحمن", "Al-Nasai")
