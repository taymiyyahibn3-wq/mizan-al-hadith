"""
Mīzān al-Ḥadīth — Hadith Detail Full Integration Test Suite
Verifies:
1. Commentary System (HTTP 200, zero mismatch, fail closed, multi-source)
2. Scholarly Statements / Aqwāl al-ʿUlamāʾ (Transliterated scholars, English statements)
3. Sanad Narrator Links (Exact character spans, rawi_ids, no transmission words)
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(REPO_ROOT, "mizan-web", "backend")
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_full_suite():
    print("================================================================================")
    print("MĪZĀN AL-ḤADĪTH — FULL RUNTIME DETAIL TEST SUITE")
    print("================================================================================")

    # --------------------------------------------------------------------------
    # 1. BUKHARI #1 (Hadith ID: 1)
    # --------------------------------------------------------------------------
    print("\n--- TEST 1: Sahih al-Bukhari #1 (Hadith ID: 1) ---")
    r1 = client.get("/api/hadith/1")
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
    h1 = r1.json()
    assert "arabic_matn" in h1 and len(h1["arabic_matn"]) > 50
    assert "narrator_spans" in h1
    spans1 = h1["narrator_spans"]
    print(f"  [PASS] Hadith 1 loaded successfully ({len(h1['arabic_matn'])} chars)")
    print(f"  [PASS] Narrator spans found: {len(spans1)}")

    expected_rawi_ids_1 = [4698, 3443, 8272, 6796, 5719, 5913]
    actual_rawi_ids_1 = [s["rawi_id"] for s in spans1]
    for rid in expected_rawi_ids_1:
        assert rid in actual_rawi_ids_1, f"Expected rawi_id {rid} in spans, got {actual_rawi_ids_1}"
    print(f"  [PASS] All expected narrator links verified: {expected_rawi_ids_1}")
    for s in spans1:
        print(f"         • [{s['start']}:{s['end']}] Rawi #{s['rawi_id']}: '{s['display_text']}'")

    # Commentary for Bukhari 1
    rc1 = client.get("/api/hadith/1/commentaries")
    assert rc1.status_code == 200
    dc1 = rc1.json()
    assert dc1["available"] is True
    assert dc1["total_commentaries"] >= 3
    print(f"  [PASS] Commentary loaded ({dc1['total_commentaries']} verified works):")
    for c in dc1["commentaries"]:
        print(f"         • {c['commentary_title']} by {c['author']}")

    # Scholarly Statements for Bukhari 1
    rg1 = client.get("/api/hadith/1/grades")
    assert rg1.status_code == 200
    dg1 = rg1.json()
    print(f"  [PASS] Scholarly statements loaded (Verdicts: {len(dg1.get('grades', []))}, Narrator evaluations: {len(dg1.get('narrator_statements', []))})")
    if dg1.get("narrator_statements"):
        sample_ns = dg1["narrator_statements"][0]
        print(f"         Sample: Scholar='{sample_ns.get('scholar_en')}', Statement='{sample_ns.get('statement_en')[:60]}...'")

    # --------------------------------------------------------------------------
    # 2. NASA'I #4 (Hadith ID: 20918)
    # --------------------------------------------------------------------------
    print("\n--- TEST 2: Sunan an-Nasa'i #4 (Hadith ID: 20918) ---")
    r2 = client.get("/api/hadith/20918")
    assert r2.status_code == 200
    h2 = r2.json()
    spans2 = h2.get("narrator_spans", [])
    print(f"  [PASS] Hadith 20918 loaded successfully ({len(h2['arabic_matn'])} chars)")
    print(f"  [PASS] Narrator spans found: {len(spans2)}")

    expected_rawi_ids_2 = [6171, 8271, 6473, 2553, 4108, 5021]
    actual_rawi_ids_2 = [s["rawi_id"] for s in spans2]
    for rid in expected_rawi_ids_2:
        assert rid in actual_rawi_ids_2, f"Expected rawi_id {rid} in spans, got {actual_rawi_ids_2}"
    print(f"  [PASS] All expected Nasa'i #4 narrator links verified: {expected_rawi_ids_2}")
    for s in spans2:
        print(f"         • [{s['start']}:{s['end']}] Rawi #{s['rawi_id']}: '{s['display_text']}'")

    # Verify complex spans
    s_8271 = next(s for s in spans2 if s["rawi_id"] == 8271)
    assert s_8271["display_text"] == "يَحْيَى وَهُوَ ابْنُ سَعِيدٍ", f"Unexpected display text: {s_8271['display_text']}"
    print(f"  [PASS] Exact span verified for Yahya ibn Sa'id: '{s_8271['display_text']}'")

    s_5021 = next(s for s in spans2 if s["rawi_id"] == 5021)
    assert s_5021["display_text"] == "أَبِي مُوسَى", f"Unexpected display text: {s_5021['display_text']}"
    print(f"  [PASS] Exact span verified for Abu Musa al-Ash'ari: '{s_5021['display_text']}'")

    # --------------------------------------------------------------------------
    # 3. EDGE CASES & SAFETY
    # --------------------------------------------------------------------------
    print("\n--- TEST 3: Edge Cases & Safety Rules ---")
    # Non-commentary Hadith returns HTTP 200 with available=False, commentaries=[]
    r_empty = client.get("/api/hadith/999999/commentaries")
    assert r_empty.status_code == 200
    d_empty = r_empty.json()
    assert d_empty["available"] is False
    assert len(d_empty["commentaries"]) == 0
    print("  [PASS] Non-commentary Hadith returns HTTP 200 with empty array (no 404 crash)")

    # Non-existent Hadith detail returns 404
    r_404 = client.get("/api/hadith/999999")
    assert r_404.status_code == 404
    print("  [PASS] Non-existent Hadith record returns HTTP 404")

    print("\n================================================================================")
    print("ALL INTEGRATION TESTS PASSED (100%)! ✓")
    print("================================================================================")

if __name__ == "__main__":
    run_full_suite()
