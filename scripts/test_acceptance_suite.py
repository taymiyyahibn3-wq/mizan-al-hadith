import os
import sys
import json
import random

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mizan-web", "backend")))

from main import get_hadith_grades

def run_tests():
    print("=== RUNNING ACCEPTANCE TEST SUITE ===")
    
    # Required test hadith IDs
    test_ids = [1, 29, 100, 428, 12426, 12427, 12428]
    
    # 20 random hadiths
    random.seed(42)
    random_ids = random.sample(range(1, 20000), 20)
    all_check_ids = test_ids + random_ids
    
    print(f"Testing {len(all_check_ids)} Hadith IDs...")
    
    passed_checks = 0
    total_checks = 0
    
    for hid in all_check_ids:
        total_checks += 1
        try:
            grades_resp = get_hadith_grades(hid)
            
            # Check 1: Structure integrity
            assert "grades" in grades_resp, f"Missing grades in #{hid}"
            assert "classical_evaluations" in grades_resp, f"Missing classical_evaluations in #{hid}"
            assert "narrator_statements" in grades_resp, f"Missing narrator_statements in #{hid}"
            
            # Check 2: No conflation (all grades must be from modern editions or classical_evaluations must be classical critics)
            for g in grades_resp["grades"]:
                assert g.get("scholar") or g.get("scholar_en"), f"Grade missing scholar in #{hid}"
                
            for ce in grades_resp["classical_evaluations"]:
                assert ce["scholar_id"] == "al_tirmidhi", f"Unexpected scholar {ce['scholar_id']} in #{hid}"
                assert ce["evidence_type"] in ["explicit_hadith_grade", "hadith_criticism"], f"Invalid evidence type in #{hid}"
                assert ce["verbatim_arabic"], f"Missing verbatim Arabic in #{hid}"
                assert ce["canonical_term"], f"Missing canonical term in #{hid}"
                assert ce["attribution"] == "Direct Primary Authorial Text (Autographic transmission)", f"Invalid attribution in #{hid}"
                assert ce["verification_status"] == "VERIFIED_PRIMARY_SOURCE", f"Unverified status in #{hid}"
            
            # Check 3: Rawi #4256 quarantine check on Hadith #428
            if hid == 428:
                for ns in grades_resp["narrator_statements"]:
                    if ns.get("rawi_id") == 4256 and ns.get("alem_id") == 2821:
                        assert False, "Quarantined collision escaped into verified narrator_statements for #428!"
            
            passed_checks += 1
        except Exception as e:
            print(f"FAILED on Hadith #{hid}: {e}")
            raise e
            
    print(f"PASSED {passed_checks}/{total_checks} Hadith checks!")
    
    # Test specific Tirmidhi items
    print("\nVerifying specific Sunan al-Tirmidhi items:")
    # Hadith #12427 is Sunan al-Tirmidhi #29
    tirmidhi_29 = get_hadith_grades(12427)
    assert len(tirmidhi_29["classical_evaluations"]) == 1
    eval_29 = tirmidhi_29["classical_evaluations"][0]
    print(f"Hadith #12427 (Tirmidhi #29) evaluation: {ascii(eval_29['canonical_term'])} | {ascii(eval_29['verbatim_arabic'])}")
    assert eval_29["canonical_term"] == "Ḥasan Ṣaḥīḥ"
    assert "حسن صحيح" in eval_29["verbatim_arabic"]
    
    # Hadith #12426 (Tirmidhi #28)
    tirmidhi_28 = get_hadith_grades(12426)
    assert len(tirmidhi_28["classical_evaluations"]) == 1
    eval_28 = tirmidhi_28["classical_evaluations"][0]
    print(f"Hadith #12426 (Tirmidhi #28) evaluation: {ascii(eval_28['canonical_term'])} | {eval_28['evidence_type']}")
    assert eval_28["evidence_type"] == "hadith_criticism"
    
    print("\nALL ACCEPTANCE CRITERIA RIGOROUSLY SATISFIED!")

if __name__ == "__main__":
    run_tests()
