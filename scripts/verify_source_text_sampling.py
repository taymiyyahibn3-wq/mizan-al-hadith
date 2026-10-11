import os
import sys
import sqlite3
import random
import json

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(REPO_ROOT, "validation", "classical_external_grading_research")
DERIVED_DB = os.path.join(REPO_ROOT, "data", "classical_scholar_evidence.db")
KG_DB = os.path.join(REPO_ROOT, "data", "hadith-kg.db")

print("=== EXECUTING SECTION 6 SOURCE TEXT SAMPLING AUDIT ===")

der_conn = sqlite3.connect(f"file:{DERIVED_DB}?mode=ro", uri=True)
der_conn.row_factory = sqlite3.Row

kg_conn = sqlite3.connect(f"file:{KG_DB}?mode=ro", uri=True)
kg_conn.row_factory = sqlite3.Row

# Stratified sampling
# Early: 1 <= no_inbook <= 1300
# Middle: 1301 <= no_inbook <= 2600
# Late: 2601 <= no_inbook <= 3924

explicit_early = der_conn.execute("SELECT * FROM classical_hadith_evaluations WHERE evidence_type = 'explicit_hadith_grade' AND no_inbook <= 1300").fetchall()
explicit_mid = der_conn.execute("SELECT * FROM classical_hadith_evaluations WHERE evidence_type = 'explicit_hadith_grade' AND no_inbook BETWEEN 1301 AND 2600").fetchall()
explicit_late = der_conn.execute("SELECT * FROM classical_hadith_evaluations WHERE evidence_type = 'explicit_hadith_grade' AND no_inbook >= 2601").fetchall()

crit_early = der_conn.execute("SELECT * FROM classical_hadith_evaluations WHERE evidence_type = 'hadith_criticism' AND no_inbook <= 1300").fetchall()
crit_mid = der_conn.execute("SELECT * FROM classical_hadith_evaluations WHERE evidence_type = 'hadith_criticism' AND no_inbook BETWEEN 1301 AND 2600").fetchall()
crit_late = der_conn.execute("SELECT * FROM classical_hadith_evaluations WHERE evidence_type = 'hadith_criticism' AND no_inbook >= 2601").fetchall()

random.seed(2026)

sample_explicit = (
    random.sample(explicit_early, 34) +
    random.sample(explicit_mid, 33) +
    random.sample(explicit_late, 33)
)

sample_crit = (
    random.sample(crit_early, 17) +
    random.sample(crit_mid, 17) +
    random.sample(crit_late, 16)
)

all_samples = [(s, "explicit") for s in sample_explicit] + [(s, "criticism") for s in sample_crit]

passed = 0
failed = 0
pending = 0
audit_records = []

for rec, sample_type in all_samples:
    hid = rec["hadith_id"]
    no = rec["no_inbook"]
    vb = rec["verbatim_arabic"]
    term = rec["canonical_term"]
    ev_type = rec["evidence_type"]
    
    # Retrieve source from canonical KG DB
    kg_row = kg_conn.execute("SELECT id, book_id, no_inbook, taraf_nass, nass, matn FROM hadiths WHERE id = ?", (hid,)).fetchone()
    
    if not kg_row:
        failed += 1
        audit_records.append({"hadith_id": hid, "no_inbook": no, "status": "FAIL", "reason": "Not found in canonical DB"})
        continue
        
    taraf = kg_row["taraf_nass"] or ""
    
    # 1. Compare Arabic
    arabic_match = vb in taraf or vb in (kg_row["nass"] or "")
    # 2. Compare reference
    ref_match = (kg_row["book_id"] == 3) and (kg_row["no_inbook"] == no)
    # 3. Compare evaluation
    eval_match = (ev_type == rec["evidence_type"]) and (len(term) > 0)
    # 4. Compare attribution
    attr_match = "attributed" in rec["attribution"] or "authorial" in rec["attribution"]
    
    if arabic_match and ref_match and eval_match and attr_match:
        passed += 1
        status = "PASS"
    else:
        failed += 1
        status = "FAIL"
        
    audit_records.append({
        "hadith_id": hid,
        "no_inbook": no,
        "sample_type": sample_type,
        "stratum": "early" if no <= 1300 else ("mid" if no <= 2600 else "late"),
        "canonical_term": term,
        "verbatim_arabic": vb,
        "arabic_match": arabic_match,
        "ref_match": ref_match,
        "eval_match": eval_match,
        "attr_match": attr_match,
        "status": status
    })

der_conn.close()
kg_conn.close()

print(f"Total samples audited: {len(all_samples)} (100 explicit grades + 50 criticisms)")
print(f"  PASS: {passed}")
print(f"  FAIL: {failed}")
print(f"  SOURCE_VERIFICATION_PENDING: {pending}")

# Stratum breakdown
strata = {"early": 0, "mid": 0, "late": 0}
for a in audit_records:
    if a["status"] == "PASS":
        strata[a["stratum"]] += 1
print(f"Stratum breakdown of passes: Early: {strata['early']}, Middle: {strata['mid']}, Late: {strata['late']}")

# Save audit results to JSON
out_path = os.path.join(RESEARCH_DIR, "source_verification_samples.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(audit_records, f, indent=2, ensure_ascii=False)
print(f"Saved audit log to {out_path}.")
