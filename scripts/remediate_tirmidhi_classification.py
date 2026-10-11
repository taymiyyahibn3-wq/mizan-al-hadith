import sqlite3
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def classify_tirmidhi_text(stmt):
    clean = stmt.strip()
    
    # Remove prefix "قال أبو عيسى"
    body = re.sub(r'^قال أبو عيسى\s*', '', clean).strip()
    
    # -------------------------------------------------------------------------
    # 1. NEGATIVE OR DEFECT EVALUATIONS (CRITICISM)
    # -------------------------------------------------------------------------
    
    # "ليس إسناده بصحيح"
    if re.search(r'ليس\s+إسناده\s+(?:بـ?|ب)صحيح', body):
        m = re.search(r'(?:هذا حديث\s+)?ليس\s+إسناده\s+(?:بـ?|ب)صحيح[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "ليس إسناده بصحيح"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Laysa Isnāduhu bi-Ṣaḥīḥ",
            "verbatim_arabic": vb,
        }

    # "ليس إسناده بذاك" or "ليس إسناده بالقوي" or "ليس إسناده بذلك القوي"
    if re.search(r'ليس\s+إسناده\s+(?:بذاك|بذلك|بالقوي)', body):
        m = re.search(r'(?:هذا حديث\s+)?ليس\s+إسناده\s+(?:بذاك|بذلك|بالقوي)[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "ليس إسناده بذاك"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Laysa Isnāduhu bi-Dhāk",
            "verbatim_arabic": vb,
        }

    # "غير محفوظ"
    if re.search(r'غير\s+محفوظ', body):
        m = re.search(r'(?:هذا حديث\s+)?غير\s+محفوظ[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "هذا حديث غير محفوظ"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Ghayr Maḥfūẓ",
            "verbatim_arabic": vb,
        }

    # "حديث منكر" or "هذا حديث منكر"
    if re.search(r'(?:هذا حديث|هذا الحديث|حديث\s+\w+)\s+منكر', body):
        m = re.search(r'(?:هذا حديث|هذا الحديث|حديث\s+\w+)\s+منكر', body)
        vb = m.group(0).strip()
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Munkar",
            "verbatim_arabic": vb,
        }

    # "أصح شيء في هذا الباب" (Comparative Tarjih)
    if "أصح شيء في هذا الباب" in body:
        m = re.search(r'(?:هذا الحديث\s+)?أصح شيء في هذا الباب[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "أصح شيء في هذا الباب"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Aṣaḥḥu Shayʾin fī al-Bāb",
            "verbatim_arabic": vb,
        }

    # "والصحيح ما روي عن..." where it's variant preference
    if body.startswith("والصحيح ما رو") or ("والصحيح ما رو" in body and not re.search(r'هذا حديث\s+(?:حسن|صحيح)', body)):
        m = re.search(r'والصحيح ما رو[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "والصحيح ما روي"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Tarjīḥ al-Wajh al-Ṣaḥīḥ",
            "verbatim_arabic": vb,
        }

    # -------------------------------------------------------------------------
    # 2. EXPLICIT HADITH GRADES
    # Must explicitly predicate a grading term on the hadith itself:
    # "هذا حديث حسن صحيح غريب"
    # "هذا حديث حسن صحيح"
    # "هذا حديث حسن غريب"
    # "هذا حديث صحيح غريب"
    # "هذا حديث حسن"
    # "هذا حديث صحيح"
    # "هذا حديث غريب"
    # "هذا حديث ضعيف"
    # Or "حديث فلان حسن صحيح", etc.
    # -------------------------------------------------------------------------
    
    # Grade formula regex
    # Match: (هذا حديث | هذا الحديث | حديث [فلان] | وكلا الحديثين) followed immediately by grading terms
    m_exp = re.search(
        r'(هذا حديث|هذا الحديث|حديث\s+[^\n،\.]+?|وكلا الحديثين[^\n،\.]*?)\s+'
        r'(حسنٌ?\s+صحيحٌ?\s+غريبٌ?|حسنٌ?\s+صحيحٌ?|حسنٌ?\s+غريبٌ?|صحيحٌ?\s+غريبٌ?|صحيحٌ?|حسنٌ?|غريبٌ?|ضعيفٌ?)'
        r'(?=\s+(?:لا نعرفه|من هذا|وقد روي|وفي الباب|سمعت|حدثنا|والعمل|وروي|\.|\n|،|$|إلا|ورواه))',
        body
    )
    
    if m_exp:
        full_match = m_exp.group(0).strip()
        subject = m_exp.group(1).strip()
        grade_term = m_exp.group(2).strip()
        
        # Guard against narrator names like "حديث عبد الرحمن بن حسنة"
        if "حسنة" in grade_term:
            pass # Not a grade
        else:
            if "حسن" in grade_term and "صحيح" in grade_term and "غريب" in grade_term:
                ct = "Ḥasan Ṣaḥīḥ Gharīb"
            elif "حسن" in grade_term and "صحيح" in grade_term:
                ct = "Ḥasan Ṣaḥīḥ"
            elif "حسن" in grade_term and "غريب" in grade_term:
                ct = "Ḥasan Gharīb"
            elif "صحيح" in grade_term and "غريب" in grade_term:
                ct = "Ṣaḥīḥ Gharīb"
            elif "حسن" in grade_term:
                ct = "Ḥasan"
            elif "صحيح" in grade_term:
                ct = "Ṣaḥīḥ"
            elif "غريب" in grade_term:
                ct = "Gharīb"
            elif "ضعيف" in grade_term:
                ct = "Ḍaʿīf"
            else:
                ct = None
                
            if ct:
                return {
                    "evidence_type": "explicit_hadith_grade",
                    "canonical_term": ct,
                    "verbatim_arabic": full_match,
                }

    # Also match simpler anchor: body starts directly with "هذا حديث [grade]"
    m_start = re.match(
        r'^(هذا حديث|هذا الحديث)\s+(حسنٌ?\s+صحيحٌ?\s+غريبٌ?|حسنٌ?\s+صحيحٌ?|حسنٌ?\s+غريبٌ?|صحيحٌ?\s+غريبٌ?|صحيحٌ?|حسنٌ?|غريبٌ?|ضعيفٌ?)',
        body
    )
    if m_start:
        grade_term = m_start.group(2).strip()
        if "حسن" in grade_term and "صحيح" in grade_term and "غريب" in grade_term:
            ct = "Ḥasan Ṣaḥīḥ Gharīb"
        elif "حسن" in grade_term and "صحيح" in grade_term:
            ct = "Ḥasan Ṣaḥīḥ"
        elif "حسن" in grade_term and "غريب" in grade_term:
            ct = "Ḥasan Gharīb"
        elif "صحيح" in grade_term and "غريب" in grade_term:
            ct = "Ṣaḥīḥ Gharīb"
        elif "حسن" in grade_term:
            ct = "Ḥasan"
        elif "صحيح" in grade_term:
            ct = "Ṣaḥīḥ"
        elif "غريب" in grade_term:
            ct = "Gharīb"
        elif "ضعيف" in grade_term:
            ct = "Ḍaʿīf"
        else:
            ct = None
        if ct:
            return {
                "evidence_type": "explicit_hadith_grade",
                "canonical_term": ct,
                "verbatim_arabic": m_start.group(0).strip(),
            }

    # -------------------------------------------------------------------------
    # 3. SCHOLARLY REMARK (CRITICISM / COMMENTARY)
    # -------------------------------------------------------------------------
    first_clause = body.split('.')[0].split('،')[0][:120].strip()
    return {
        "evidence_type": "hadith_criticism",
        "canonical_term": "Qawl Abī ʿĪsā (Scholarly Remark)",
        "verbatim_arabic": first_clause if first_clause else body[:120],
    }

def run_test():
    conn = sqlite3.connect("file:data/hadith-kg.db?mode=ro", uri=True)
    rows = conn.execute("""
        SELECT id, no_inbook, taraf_nass
        FROM hadiths
        WHERE book_id = 3
        ORDER BY no_inbook
    """).fetchall()
    
    total = 0
    grades = 0
    crits = 0
    counts = {}
    
    for hid, no, taraf in rows:
        if not taraf: continue
        idx = taraf.find("قال أبو عيسى")
        if idx == -1: continue
        
        stmt = taraf[idx:].strip()
        res = classify_tirmidhi_text(stmt)
        total += 1
        ev = res["evidence_type"]
        ct = res["canonical_term"]
        if ev == "explicit_hadith_grade":
            grades += 1
        else:
            crits += 1
        counts[ct] = counts.get(ct, 0) + 1
        
    conn.close()
    print(f"Total authorial statements: {total}")
    print(f"Explicit hadith grades: {grades}")
    print(f"Hadith criticism: {crits}")
    print("\nCanonical Term Breakdown:")
    for ct, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {c}")

if __name__ == "__main__":
    run_test()
