"""
Mīzān al-Ḥadīth — Dedicated Scholarly Integrity & Numbering Regression Suite
Comprehensive verification of Ibn Majah Darussalam 1986, Al-Albani grading,
and Abdur Rahman al-Musli / Yahya ibn Ma'in narrator attribution.
"""

import os
import sys
import re
import json
import sqlite3
from pathlib import Path
import urllib.request
import urllib.error

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "mizan-web" / "backend"
sys.path.insert(0, str(BACKEND_PATH))
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from scholarly_service import (
    get_canonical_hadith_grades,
    get_verified_narrator_aqwal,
    HADITH_KG_PATH,
    HADITH_NUMBERING_PATH,
)
from ask_mizan.tools import (
    tool_get_scholarly_grades,
    tool_get_narrator_dossier,
    tool_get_hadith_detail,
    tool_resolve_reference,
)

def test_1_darussalam_ibn_majah_1986_resolution():
    """TEST 1: Darussalam Ibn Majah 1986 resolves to expected canonical hadiths.id (28581)."""
    print("\n--- TEST 1: Darussalam Ibn Majah 1986 Resolution ---")
    conn = sqlite3.connect(f"file:{HADITH_NUMBERING_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        # Scheme 18 is Sunan Ibn Majah - Darussalam
        row = conn.execute("""
            SELECT hn.hadith_id, hn.scheme_id, hn.primary_number, ns.display_name_en, ns.code
            FROM hadith_numbers hn
            JOIN numbering_schemes ns ON ns.id = hn.scheme_id
            WHERE hn.book_id = 6 AND hn.scheme_id = 18 AND hn.primary_number = '1986'
        """).fetchone()

        assert row is not None, "Darussalam 1986 record not found in hadith_numbering.db"
        assert row["hadith_id"] == 28581, f"Expected hadith_id=28581, got {row['hadith_id']}"
        print(f"✓ Darussalam 1986 correctly maps to canonical hadith_id = {row['hadith_id']}")
        print(f"  Edition: {row['display_name_en']} ({row['code']})")
    finally:
        conn.close()


def test_2_search_by_darussalam_1986():
    """TEST 2: Search by Darussalam 1986 opens the correct hadith."""
    print("\n--- TEST 2: Search / Lookup by Darussalam 1986 ---")
    hid = tool_resolve_reference("ibn majah", scheme="darussalam", number="1986")
    assert hid is not None, "Resolution of 'ibn majah' darussalam '1986' returned None"
    assert hid == 28581, f"Expected hadith_id 28581, got {hid}"
    
    h_detail = tool_get_hadith_detail(hid)
    assert h_detail is not None, f"Could not retrieve hadith detail for id {hid}"
    norm_matn = re.sub(r"[\u064B-\u065F\u0670]", "", h_detail.matn_arabic)
    assert "يسأل" in norm_matn or "يضرب" in norm_matn, "Arabic text does not match 'La yus'alu ar-rajul'"
    print(f"✓ Lookup by 'ibn majah 1986' successfully retrieved canonical Hadith #{h_detail.canonical_id}")


import unicodedata

def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def test_3_hadith_grading_lookup():
    """TEST 3: Hadith grading lookup returns only gradings belonging to that canonical hadith."""
    print("\n--- TEST 3: Hadith Grading Lookup for Canonical Hadith 28581 ---")
    grades = get_canonical_hadith_grades(28581)
    assert len(grades) > 0, "No grades returned for canonical Hadith 28581"

    print(f"✓ Retrieved {len(grades)} scholarly grading records:")
    for g in grades:
        print(f"  - Scholar: {g['scholar_en']} ({g['scholar_ar']}) -> {g['grade_en']} ({g['grade_ar']}) | Ref: {g.get('reference_formatted')} | Source: {g.get('provenance')}")

    albani_grade = next((g["grade_en"] for g in grades if "albani" in strip_accents(g.get("scholar_en", "")) or "الألباني" in g.get("scholar_ar", "")), None)
    assert albani_grade is not None, "Al-Albani grading missing"
    assert "da'if" in albani_grade.lower() or "weak" in albani_grade.lower() or "daif" in albani_grade.lower() or "ضعيف" in albani_grade, f"Al-Albani grade must be Da'if, got {albani_grade}"

    baqi_grade = next((g["grade_en"] for g in grades if "baqi" in strip_accents(g.get("scholar_en", "")) or "عبد الباقي" in g.get("scholar_ar", "")), None)
    if baqi_grade:
        assert "da'if" in baqi_grade.lower() or "weak" in baqi_grade.lower(), f"Abd al-Baqi grade must be Da'if, got {baqi_grade}"

    arnaut_grade = next((g["grade_en"] for g in grades if "arnaut" in strip_accents(g.get("scholar_en", "")) or "الأرنؤوط" in g.get("scholar_ar", "")), None)
    if arnaut_grade:
        assert "da'if" in arnaut_grade.lower() or "weak" in arnaut_grade.lower(), f"Arna'ut grade must be Da'if, got {arnaut_grade}"


def test_4_al_albani_grading_provenance():
    """TEST 4: al-Albānī grading: verify its exact source/provenance and canonical hadith mapping."""
    print("\n--- TEST 4: Al-Albani Exact Provenance Verification ---")
    grades = get_canonical_hadith_grades(28581)
    albani_grade = next((g for g in grades if "albani" in strip_accents(g.get("scholar_en", "")) or "الألباني" in g.get("scholar_ar", "")), None)
    assert albani_grade is not None, "Al-Albani grading not found"

    assert albani_grade["grade_ar"] == "ضعيف" or "ضعيف" in albani_grade["grade_ar"], f"Expected 'ضعيف', got {albani_grade['grade_ar']}"
    assert albani_grade["reference_book"] == 9, f"Expected reference_book=9 (Nikah), got {albani_grade['reference_book']}"
    assert albani_grade["reference_hadith"] == 142, f"Expected reference_hadith=142, got {albani_grade['reference_hadith']}"
    print(f"✓ Al-Albani grading verified:")
    print(f"  Scholar: {albani_grade['scholar_en']} ({albani_grade['scholar_ar']})")
    print(f"  Grade: {albani_grade['grade_en']} ({albani_grade['grade_ar']})")
    print(f"  Reference: Book {albani_grade['reference_book']}, Hadith {albani_grade['reference_hadith']}")
    print(f"  Provenance: {albani_grade.get('provenance')}")


def test_5_narrator_extraction_ibn_majah_1986():
    """TEST 5: Narrator extraction from Ibn Majah 1986 correctly identifies ʿAbd al-Raḥmān al-Muṣallī."""
    print("\n--- TEST 5: Narrator Extraction for Ibn Majah 1986 ---")
    conn = sqlite3.connect(f"file:{HADITH_KG_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rawis = conn.execute("""
            SELECT r.id, r.name, r.rank, r.nasab
            FROM rawis r
            JOIN hadith_rawis hr ON hr.rawi_id = r.id
            WHERE hr.hadith_id = 28581
        """).fetchall()

        musalli = next((r for r in rawis if r["id"] == 4256), None)
        assert musalli is not None, "Abdur Rahman al-Musli (rawi_id=4256) not found in isnad of Hadith 28581"
        print(f"✓ Found Rawi #4256 in isnad:")
        print(f"  Name: {musalli['name']}")
        print(f"  Nasab: {musalli['nasab']}")
        print(f"  Rank: {musalli['rank']}")
    finally:
        conn.close()


def test_6_narrator_scholarly_statements_attribution_guard():
    """TEST 6: Narrator scholarly statements: do NOT attach Yaḥyā ibn Maʿīn's statement as verified."""
    print("\n--- TEST 6: Narrator Attribution Safety Guard ---")
    aqwal = get_verified_narrator_aqwal(4256)
    assert len(aqwal) > 0, "No aqwal returned for rawi 4256"

    # Find Yahya ibn Ma'in statement (alem_id = 2821)
    maeen_qawl = next((q for q in aqwal if q.get("alem_id") == 2821), None)
    if maeen_qawl:
        assert maeen_qawl["is_verified"] is False, "Yahya ibn Ma'in statement must NOT be marked is_verified=True for Rawi 4256"
        assert maeen_qawl["attribution_status"] == "father_son_collision", f"Expected father_son_collision, got {maeen_qawl['attribution_status']}"
        assert maeen_qawl.get("provenance_caveat") is not None, "Provenance caveat must be provided for unresolved attribution"
        print(f"✓ Yahya ibn Ma'in statement is properly guarded:")
        print(f"  is_verified: {maeen_qawl['is_verified']}")
        print(f"  attribution_status: {maeen_qawl['attribution_status']}")
        print(f"  caveat: {maeen_qawl['provenance_caveat'][:100]}...")
    else:
        print("✓ Yahya ibn Ma'in statement is excluded from verified evaluations")


def test_7_similar_name_collision_test():
    """TEST 7: Similar-name collision test: father (4256) and son (8145)."""
    print("\n--- TEST 7: Similar-Name Father/Son Collision Verification ---")
    conn = sqlite3.connect(f"file:{HADITH_KG_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        # Father
        father = conn.execute("SELECT id, name, nasab FROM rawis WHERE id = 4256").fetchone()
        # Son
        son = conn.execute("SELECT id, name, nasab FROM rawis WHERE id = 8145").fetchone()

        assert father is not None and son is not None, "Both father and son must exist in rawis table"
        print(f"  Father: #{father['id']} {father['name']} ({father['nasab']})")
        print(f"  Son:    #{son['id']} {son['name']} ({son['nasab']})")

        # Son's evaluation from Yahya ibn Ma'in
        son_aqwal = conn.execute("""
            SELECT a.id, a.qawl, e.name as alem_name
            FROM aqwal a
            JOIN alems e ON e.id = a.alem_id
            WHERE a.rawi_id = 8145 AND a.alem_id = 2821
        """).fetchall()
        assert len(son_aqwal) > 0, "Son (Wabarah) must have Yahya ibn Ma'in's tawthiq in aqwal"
        print(f"✓ Son (Wabarah) has verified tawthiq from Yahya ibn Ma'in: '{son_aqwal[0]['qawl']}'")

        # Verify Father's verified list does not claim Yahya ibn Ma'in's tawthiq
        father_verified = [q for q in get_verified_narrator_aqwal(4256) if q.get("is_verified") is True]
        assert not any(q.get("alem_id") == 2821 for q in father_verified), "Father's verified evaluations must NOT include Yahya ibn Ma'in"
        print(f"✓ Father (Abdur Rahman) has {len(father_verified)} verified statements; none are from Yahya ibn Ma'in")
    finally:
        conn.close()


def test_8_numbering_crosswalk_stability():
    """TEST 8: Numbering crosswalk regression: Darussalam 1986 must remain stable and immutable."""
    print("\n--- TEST 8: Numbering Crosswalk Stability ---")
    conn = sqlite3.connect(f"file:{HADITH_NUMBERING_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
            SELECT hn.hadith_id, hn.scheme_id, hn.primary_number, ns.display_name_en, ns.code
            FROM hadith_numbers hn
            JOIN numbering_schemes ns ON ns.id = hn.scheme_id
            WHERE hn.hadith_id = 28581
        """).fetchall()

        schemes = {r["scheme_id"]: str(r["primary_number"]) for r in rows}
        print(f"✓ Canonical Hadith 28581 has {len(rows)} registered numbering aliases:")
        for r in rows:
            print(f"  - Scheme {r['scheme_id']}: {r['display_name_en']} #{r['primary_number']}")

        # Scheme 18 is Darussalam Sunan Ibn Majah
        assert 18 in schemes, "Scheme 18 (Darussalam) missing for hadith 28581"
        assert schemes[18] == "1986", f"Expected Darussalam number 1986, got {schemes[18]}"
        # Scheme 16 is Shamela Catalog Sequence
        assert 16 in schemes, "Scheme 16 (Shamela Catalog Sequence) missing for hadith 28581"
        assert schemes[16] == "1976", f"Expected Shamela number 1976, got {schemes[16]}"
        print("✓ Crosswalk is deterministic and verified against both Darussalam and Shamela editions")
    finally:
        conn.close()


def test_9_api_response():
    """TEST 9: API response: verify the backend HTTP API returns correct canonical data."""
    print("\n--- TEST 9: Backend HTTP API Responses ---")
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)

    # Test 1: Hadith grades endpoint
    resp1 = client.get("/api/hadith/28581/grades")
    assert resp1.status_code == 200, f"Expected 200, got {resp1.status_code}"
    data1 = resp1.json()
    assert data1["hadith_id"] == 28581, f"Expected hadith_id=28581, got {data1['hadith_id']}"
    grades = data1.get("grades", [])
    assert len(grades) > 0, "No grades in API response"

    albani_found = False
    for g in grades:
        if "albani" in strip_accents(g.get("scholar_en", "")):
            albani_found = True
            assert g["grade_en"].lower() in ["da'if", "daif", "weak", "ضعيف"] or "ضعيف" in g.get("grade_ar", ""), f"Expected Da'if from API, got {g['grade_en']}"
            print(f"✓ API /api/hadith/28581/grades confirmed Al-Albani grade: {g['grade_en']} ({g['grade_ar']})")
    assert albani_found, "Al-Albani grade not in API response"

    # Test 2: Narrator aqwal endpoint
    resp2 = client.get("/api/narrator/4256/aqwal")
    assert resp2.status_code == 200, f"Expected 200, got {resp2.status_code}"
    data2 = resp2.json()
    assert data2["rawi_id"] == 4256, f"Expected rawi_id=4256, got {data2['rawi_id']}"
    aqwal = data2.get("aqwal", [])
    for q in aqwal:
        if q.get("alem_id") == 2821:
            assert q.get("is_verified") is False, "API /api/narrator/4256/aqwal must have is_verified=False for Yahya ibn Ma'in"
            print(f"✓ API /api/narrator/4256/aqwal correctly marked Yahya ibn Ma'in statement as is_verified=False ({q.get('attribution_status')})")


def test_10_frontend_contract_and_evidence():
    """TEST 10: Frontend contract: verify rendered evidence matches backend structures."""
    print("\n--- TEST 10: Frontend Contract & Component Verification ---")
    # Verify that ScholarlyStatementCard component contract has isVerified and attributionStatus
    frontend_card = PROJECT_ROOT / "mizan-web" / "frontend" / "src" / "app" / "components" / "ScholarlyStatementCard.tsx"
    assert frontend_card.exists(), f"{frontend_card} does not exist"

    content = frontend_card.read_text(encoding="utf-8")
    assert "isVerified" in content, "ScholarlyStatementCard must handle isVerified prop"
    assert "Identity Attribution Unresolved" in content, "ScholarlyStatementCard must display unresolved attribution warning"
    print("✓ Frontend ScholarlyStatementCard implements strict identity warning and unresolved badges")

    # Verify Ask Mizan Narrator dossier does not present Yahya ibn Ma'in as verified
    dossier = tool_get_narrator_dossier(4256)
    assert dossier is not None, "Narrator dossier for 4256 is None"
    for v in dossier.scholarly_verdicts:
        if v.scholar_id == 2821:
            assert v.is_verified is False or v.attribution_status == "father_son_collision", (
                "Dossier must not present Yahya ibn Ma'in as a verified verdict"
            )
            print(f"✓ Ask Mizan dossier for Rawi 4256 correctly flagged Yahya ibn Ma'in verdict as: {v.attribution_status}")


if __name__ == "__main__":
    print("================================================================")
    print("RUNNING MĪZĀN AL-ḤADĪTH SCHOLARLY INTEGRITY REGRESSION SUITE")
    print("================================================================")

    test_1_darussalam_ibn_majah_1986_resolution()
    test_2_search_by_darussalam_1986()
    test_3_hadith_grading_lookup()
    test_4_al_albani_grading_provenance()
    test_5_narrator_extraction_ibn_majah_1986()
    test_6_narrator_scholarly_statements_attribution_guard()
    test_7_similar_name_collision_test()
    test_8_numbering_crosswalk_stability()
    test_9_api_response()
    test_10_frontend_contract_and_evidence()

    print("\n================================================================")
    print("ALL 10 SCHOLARLY INTEGRITY & REGRESSION TESTS PASSED SUCCESSFULLY!")
    print("================================================================")
