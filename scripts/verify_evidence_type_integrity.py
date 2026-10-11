import sqlite3
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def verify_evidence_separation():
    conn = sqlite3.connect("data/classical_scholar_evidence.db")
    conn.row_factory = sqlite3.Row
    
    rows = conn.execute("SELECT id, hadith_id, no_inbook, evidence_type, canonical_term, verbatim_arabic, full_context_arabic FROM classical_hadith_evaluations").fetchall()
    
    print(f"Total rows inspected: {len(rows)}")
    
    explicit_grades = [r for r in rows if r["evidence_type"] == "explicit_hadith_grade"]
    criticisms = [r for r in rows if r["evidence_type"] == "hadith_criticism"]
    other = [r for r in rows if r["evidence_type"] not in ("explicit_hadith_grade", "hadith_criticism")]
    
    print(f"Explicit Hadith Grades: {len(explicit_grades)}")
    print(f"Hadith Criticism: {len(criticisms)}")
    print(f"Other: {len(other)}")
    
    # 1. Inspect Explicit Hadith Grades
    # Must refer to the narration (حديث / هذا حديث / إسناد / هذا الحديث / etc.)
    grade_narrator_leaks = []
    grade_non_hadith = []
    
    for r in explicit_grades:
        vb = r["verbatim_arabic"]
        fc = r["full_context_arabic"]
        
        # Check if it has hadith term
        if not any(k in vb for k in ["حديث", "الحديث", "إسناد", "إسناده"]):
            grade_non_hadith.append({
                "id": r["id"],
                "hadith_id": r["hadith_id"],
                "no_inbook": r["no_inbook"],
                "canonical_term": r["canonical_term"],
                "verbatim": vb
            })
            
    print(f"Explicit grades without explicit 'hadith' word in verbatim excerpt: {len(grade_non_hadith)}")
    if grade_non_hadith:
        print("Sample non-hadith word in verbatim (first 10):")
        for item in grade_non_hadith[:10]:
            print(f"  #{item['id']} (Hadith {item['hadith_id']}, Sunan #{item['no_inbook']}): [{item['canonical_term']}] {item['verbatim']}")
            
    # 2. Inspect Criticism records
    crit_breakdown = {}
    for r in criticisms:
        ct = r["canonical_term"]
        crit_breakdown[ct] = crit_breakdown.get(ct, 0) + 1
    print("\nCriticism breakdown:", json.dumps(crit_breakdown, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    verify_evidence_separation()
