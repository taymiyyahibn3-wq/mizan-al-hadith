import sqlite3
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def deep_audit():
    conn = sqlite3.connect("data/classical_scholar_evidence.db")
    conn.row_factory = sqlite3.Row
    
    rows = conn.execute("SELECT * FROM classical_hadith_evaluations").fetchall()
    
    print(f"Auditing all {len(rows)} rows...")
    
    suspicious_grades = []
    suspicious_criticisms = []
    
    for r in rows:
        rid = r["id"]
        hid = r["hadith_id"]
        no = r["no_inbook"]
        ev = r["evidence_type"]
        term = r["canonical_term"]
        vb = r["verbatim_arabic"]
        fc = r["full_context_arabic"]
        
        # Check explicit grades
        if ev == "explicit_hadith_grade":
            # Is it really an explicit hadith grade?
            # Genuine Tirmidhi grade formulas:
            # "هذا حديث حسن صحيح"
            # "هذا حديث حسن"
            # "هذا حديث صحيح"
            # "هذا حديث حسن غريب"
            # "هذا حديث غريب"
            # "هذا حديث حسن صحيح غريب"
            # "هذا حديث ضعيف"
            # "حديث ... حسن"
            # "هذا الحديث حسن"
            
            # Let's check if the verbatim text actually contains a genuine grading formula
            is_valid_grade_formula = bool(re.search(r'(هذا حديث|حديث [^\n]+?حديث|هذا الحديث)\s+(حسن|صحيح|غريب|ضعيف)', vb)) or \
                                    bool(re.search(r'حديث\s+(حسن|صحيح|غريب|ضعيف)', vb))
            
            if not is_valid_grade_formula:
                suspicious_grades.append({
                    "id": rid,
                    "hadith_id": hid,
                    "no_inbook": no,
                    "term": term,
                    "verbatim": vb,
                    "full_context": fc[:120]
                })
                
    print(f"Total suspicious explicit grades found: {len(suspicious_grades)}")
    for sg in suspicious_grades[:30]:
        print(f"Row #{sg['id']} (Sunan #{sg['no_inbook']}, Hadith #{sg['hadith_id']}): Term='{sg['term']}'")
        print(f"  Verbatim: {sg['verbatim']}")
        print(f"  Context:  {sg['full_context']}\n")

if __name__ == "__main__":
    deep_audit()
