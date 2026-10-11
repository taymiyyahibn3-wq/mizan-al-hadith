import os
import sys
import random
import json

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(REPO_ROOT, "mizan-web", "backend")
sys.path.insert(0, BACKEND_DIR)

from main import get_hadith_grades

print("=== EXECUTING SECTION 7 API VERIFICATION ===")

required_ids = [12399, 12400, 12426, 12427, 12428, 16322]
random.seed(42)
# 20 random IDs in Tirmidhi range (12399-16322)
random_ids = random.sample(range(12399, 16323), 20)
test_ids = required_ids + random_ids

api_results = []
all_passed = True

for hid in test_ids:
    resp = get_hadith_grades(hid)
    
    # 1. Check structure
    assert "hadith_id" in resp and resp["hadith_id"] == hid
    assert "classical_evaluations" in resp
    
    ce_list = resp["classical_evaluations"]
    
    # Check duplicates
    ids_seen = set()
    no_dups = True
    for ce in ce_list:
        if ce["id"] in ids_seen:
            no_dups = False
        ids_seen.add(ce["id"])
    assert no_dups, f"Duplicate found in classical evaluations for hadith {hid}"
    
    # Check content integrity
    for ce in ce_list:
        assert ce["scholar_id"] == "al_tirmidhi", f"Unrelated scholar in {hid}"
        assert ce["hadith_id"] == hid, f"Unrelated hadith in {hid}"
        assert ce["evidence_type"] in ["explicit_hadith_grade", "hadith_criticism"], f"Invalid evidence type in {hid}"
        assert len(ce["verbatim_arabic"]) > 0, f"Empty Arabic in {hid}"
        assert len(ce["canonical_term"]) > 0, f"Empty canonical term in {hid}"
        assert ce["work_en"] == "al-Jāmiʿ al-Kabīr (Sunan al-Tirmidhī)", f"Invalid work in {hid}"
        assert "attributed" in ce["attribution"] or "authorial" in ce["attribution"]
        
    api_results.append({
        "hadith_id": hid,
        "count": len(ce_list),
        "terms": [ce["canonical_term"] for ce in ce_list],
        "evidence_types": [ce["evidence_type"] for ce in ce_list],
        "status": "PASS"
    })

print(f"Tested {len(test_ids)} Hadith IDs via API.")
print("Required ID results:")
for r in api_results[:len(required_ids)]:
    print(f"  Hadith #{r['hadith_id']}: count={r['count']}, terms={r['terms']}, types={r['evidence_types']}")

print(f"\nAll {len(test_ids)} Hadith IDs passed API validation with zero defects, zero duplicates, and exact attribution.")
