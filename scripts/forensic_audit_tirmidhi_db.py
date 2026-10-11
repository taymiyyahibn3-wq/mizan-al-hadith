import sqlite3
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def audit():
    conn = sqlite3.connect("data/classical_scholar_evidence.db")
    conn.row_factory = sqlite3.Row
    
    # 1. Tables and Schema
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    schema = {}
    for t in tables:
        cols = conn.execute(f"PRAGMA table_info({t})").fetchall()
        schema[t] = [{"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "dflt_value": c[4], "pk": c[5]} for c in cols]
        
    # 2. Row counts
    total_count = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations").fetchone()[0]
    grade_count = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE evidence_type = 'explicit_hadith_grade'").fetchone()[0]
    crit_count = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE evidence_type = 'hadith_criticism'").fetchone()[0]
    other_evidence_types = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE evidence_type NOT IN ('explicit_hadith_grade', 'hadith_criticism')").fetchone()[0]
    
    # 3. Duplicate checks
    dup_hadith_ids = conn.execute("SELECT hadith_id, COUNT(1) FROM classical_hadith_evaluations GROUP BY hadith_id HAVING COUNT(1) > 1").fetchall()
    dup_book_no = conn.execute("SELECT book_id, no_inbook, COUNT(1) FROM classical_hadith_evaluations GROUP BY book_id, no_inbook HAVING COUNT(1) > 1").fetchall()
    
    # 4. Null / empty checks
    null_hadith_id = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE hadith_id IS NULL OR hadith_id <= 0").fetchone()[0]
    null_scholar_id = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE scholar_id IS NULL OR TRIM(scholar_id) = ''").fetchone()[0]
    null_scholar_en = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE scholar_en IS NULL OR TRIM(scholar_en) = ''").fetchone()[0]
    null_scholar_ar = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE scholar_ar IS NULL OR TRIM(scholar_ar) = ''").fetchone()[0]
    null_work_en = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE work_en IS NULL OR TRIM(work_en) = ''").fetchone()[0]
    null_evidence_type = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE evidence_type IS NULL OR TRIM(evidence_type) = ''").fetchone()[0]
    null_canonical_term = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE canonical_term IS NULL OR TRIM(canonical_term) = ''").fetchone()[0]
    null_verbatim_ar = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE verbatim_arabic IS NULL OR TRIM(verbatim_arabic) = ''").fetchone()[0]
    null_context_ar = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE full_context_arabic IS NULL OR TRIM(full_context_arabic) = ''").fetchone()[0]
    null_attribution = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE attribution IS NULL OR TRIM(attribution) = ''").fetchone()[0]
    null_license = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE license IS NULL OR TRIM(license) = ''").fetchone()[0]
    null_status = conn.execute("SELECT COUNT(1) FROM classical_hadith_evaluations WHERE verification_status IS NULL OR TRIM(verification_status) = ''").fetchone()[0]
    
    # 5. Distinct values
    distinct_scholars = [dict(r) for r in conn.execute("SELECT DISTINCT scholar_id, scholar_en, scholar_ar FROM classical_hadith_evaluations").fetchall()]
    distinct_evidence_types = [dict(r) for r in conn.execute("SELECT evidence_type, COUNT(1) as cnt FROM classical_hadith_evaluations GROUP BY evidence_type").fetchall()]
    distinct_canonical_terms = [dict(r) for r in conn.execute("SELECT canonical_term, COUNT(1) as cnt FROM classical_hadith_evaluations GROUP BY canonical_term ORDER BY cnt DESC").fetchall()]
    distinct_statuses = [dict(r) for r in conn.execute("SELECT verification_status, COUNT(1) as cnt FROM classical_hadith_evaluations GROUP BY verification_status").fetchall()]
    
    # 6. Hadith ID range
    min_hadith_id = conn.execute("SELECT MIN(hadith_id) FROM classical_hadith_evaluations").fetchone()[0]
    max_hadith_id = conn.execute("SELECT MAX(hadith_id) FROM classical_hadith_evaluations").fetchone()[0]
    min_no_inbook = conn.execute("SELECT MIN(no_inbook) FROM classical_hadith_evaluations").fetchone()[0]
    max_no_inbook = conn.execute("SELECT MAX(no_inbook) FROM classical_hadith_evaluations").fetchone()[0]
    
    # 7. Malformed Arabic check
    rows = conn.execute("SELECT id, hadith_id, verbatim_arabic, full_context_arabic FROM classical_hadith_evaluations").fetchall()
    malformed_arabic_count = 0
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    for r in rows:
        vb = r["verbatim_arabic"] or ""
        fc = r["full_context_arabic"] or ""
        if not arabic_pattern.search(vb) or not arabic_pattern.search(fc):
            malformed_arabic_count += 1
            
    res = {
        "tables": tables,
        "schema": schema,
        "total_count": total_count,
        "grade_count": grade_count,
        "crit_count": crit_count,
        "other_evidence_types": other_evidence_types,
        "sum_match": (grade_count + crit_count == total_count) and (total_count == 2726),
        "dup_hadith_ids_count": len(dup_hadith_ids),
        "dup_book_no_count": len(dup_book_no),
        "null_counts": {
            "hadith_id": null_hadith_id,
            "scholar_id": null_scholar_id,
            "scholar_en": null_scholar_en,
            "scholar_ar": null_scholar_ar,
            "work_en": null_work_en,
            "evidence_type": null_evidence_type,
            "canonical_term": null_canonical_term,
            "verbatim_ar": null_verbatim_ar,
            "context_ar": null_context_ar,
            "attribution": null_attribution,
            "license": null_license,
            "verification_status": null_status,
        },
        "malformed_arabic_count": malformed_arabic_count,
        "distinct_scholars": distinct_scholars,
        "distinct_evidence_types": distinct_evidence_types,
        "distinct_canonical_terms": distinct_canonical_terms,
        "distinct_statuses": distinct_statuses,
        "id_ranges": {
            "min_hadith_id": min_hadith_id,
            "max_hadith_id": max_hadith_id,
            "min_no_inbook": min_no_inbook,
            "max_no_inbook": max_no_inbook,
        }
    }
    
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    audit()
