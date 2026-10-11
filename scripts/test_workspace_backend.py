"""
MĪZĀN AL-ḤADĪTH — Scholarly Research Workspace Automated Verification Suite
Tests all workspace modules, end-to-end CRUD, reference resolution, comparison,
citation, dossier export, user isolation, and canonical immutability.
"""

import sys
from pathlib import Path
import json

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "mizan-web" / "backend"
sys.path.insert(0, str(BACKEND_PATH))

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_workspace_tests():
    print("================================================================")
    print("RUNNING SCHOLARLY RESEARCH WORKSPACE VERIFICATION SUITE")
    print("================================================================")

    user_a = "researcher_fatima"
    user_b = "researcher_tariq"
    headers_a = {"X-Researcher-Id": user_a}
    headers_b = {"X-Researcher-Id": user_b}

    # 1. Dashboard empty state / initial metrics
    print("\n--- TEST 1: Research Dashboard Initial Metrics ---")
    res = client.get("/api/workspace/dashboard", headers=headers_a)
    assert res.status_code == 200, f"Dashboard failed: {res.text}"
    data = res.json()
    assert "metrics" in data
    assert data["user_id"] == user_a
    print(f"✓ Dashboard loaded for {user_a}. Initial projects count: {data['metrics']['total_projects']}")

    # 2. Project Creation (Arabic + Multilingual)
    print("\n--- TEST 2: Research Project Creation ---")
    project_payload = {
        "title": "دراسة حديث «إنما الأعمال بالنيات» ومروياته وشواهده",
        "description": "Comparative scholarly investigation into the isnad variations and narrators of the Hadith of Intentions.",
        "research_question": "ما هي المدارات الإسنادية لحديث عمر بن الخطاب في الصحيحين والسنن؟",
        "scope": "Ṣaḥīḥ al-Bukhārī, Ṣaḥīḥ Muslim, Sunan al-Tirmidhī",
        "tags": ["نية", "عمر_بن_الخطاب", "صحيحين", "تخريج"],
        "status": "Active"
    }
    res = client.post("/api/workspace/projects", json=project_payload, headers=headers_a)
    assert res.status_code == 200, f"Project creation failed: {res.text}"
    p_data = res.json()
    proj_id = p_data["id"]
    assert proj_id is not None
    print(f"✓ Created project: ID={proj_id}, Title='{p_data['title']}'")

    # 3. Project Detail & Retrieval
    print("\n--- TEST 3: Project Detail & Arabic Text Preservation ---")
    res = client.get(f"/api/workspace/projects/{proj_id}", headers=headers_a)
    assert res.status_code == 200
    p_detail = res.json()
    assert p_detail["title"] == project_payload["title"]
    assert p_detail["research_question"] == project_payload["research_question"]
    assert len(p_detail["tags"]) == 4
    assert len(p_detail["activities"]) >= 1
    print(f"✓ Project details and Arabic text verified bit-for-bit.")

    # 4. Evidence Linking & Canonical Resolution (Hadith #1 - Bukhari 1)
    print("\n--- TEST 4: Adding Evidence & Resolving Canonical Hadith #1 ---")
    ev_payload = {
        "entity_type": "hadith",
        "source_id": "1",
        "display_title": "Ṣaḥīḥ al-Bukhārī #1",
        "source_route": "/hadith/1",
        "role": "Supporting",
        "notes": "الحديث الأول في صحيح البخاري، رواية علقمة بن وقاص عن عمر.",
        "tags": ["أصل", "بخاري"]
    }
    res = client.post(f"/api/workspace/projects/{proj_id}/evidence", json=ev_payload, headers=headers_a)
    assert res.status_code == 200, f"Add evidence failed: {res.text}"
    ev_id = res.json()["id"]
    print(f"✓ Added Hadith #1 to evidence library: ID={ev_id}")

    # 5. Duplicate Evidence Rejection
    print("\n--- TEST 5: Duplicate Evidence Guard ---")
    res = client.post(f"/api/workspace/projects/{proj_id}/evidence", json=ev_payload, headers=headers_a)
    assert res.status_code == 409, "Expected 409 on duplicate evidence"
    print("✓ Duplicate evidence addition properly blocked with 409 Conflict.")

    # 6. Unresolved / Missing Reference Handling
    print("\n--- TEST 6: Non-existent Reference Graceful Resolution ---")
    res = client.get("/api/workspace/evidence/resolve?entity_type=hadith&source_id=999999999")
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["status"] == "unresolved"
    assert res_data["is_available"] == False
    print(f"✓ Unresolved reference gracefully handled: {res_data['message']}")

    # 7. Adding Narrator Evidence (Rawi #1)
    print("\n--- TEST 7: Linking Narrator Evidence ---")
    narrator_ev = {
        "entity_type": "narrator",
        "source_id": "1",
        "display_title": "Rawi #1",
        "role": "Contextual",
        "notes": "سجل الراوي المستخرج من الإسناد.",
        "tags": ["راوي"]
    }
    res = client.post(f"/api/workspace/projects/{proj_id}/evidence", json=narrator_ev, headers=headers_a)
    assert res.status_code == 200
    narrator_ev_id = res.json()["id"]
    print(f"✓ Linked narrator evidence ID={narrator_ev_id}")

    # 8. Research Notes (Creation, Arabic Markdown, Pinning)
    print("\n--- TEST 8: Research Note CRUD & Pinning ---")
    note_payload = {
        "title": "ملاحظة حول تفرد يحيى بن سعيد الأنصاري",
        "content": "يُعد يحيى بن سعيد الأنصاري مداراً رئيسياً لهذا الحديث؛ ومن طريقه انتشرت الروايات وكثرت الطرق.",
        "evidence_item_id": ev_id,
        "tags": ["علل", "مدار"],
        "is_pinned": True,
        "status": "Finalized"
    }
    res = client.post(f"/api/workspace/projects/{proj_id}/notes", json=note_payload, headers=headers_a)
    assert res.status_code == 200
    note_id = res.json()["id"]

    # Verify listing notes
    res = client.get(f"/api/workspace/projects/{proj_id}/notes", headers=headers_a)
    assert res.status_code == 200
    notes = res.json()["notes"]
    assert len(notes) >= 1
    assert notes[0]["is_pinned"] == True
    print(f"✓ Created and listed pinned note ID={note_id}")

    # 9. Research Claims & Evidence Matrix
    print("\n--- TEST 9: Formulating Claims & Matrix Linking ---")
    claim_payload = {
        "claim_text": "حديث الأعمال بالنيات غريب في طبقاته الأولى حتى يحيى بن سعيد الأنصاري",
        "rationale": "لم يروه عن النبي ﷺ إلا عمر، ولا عن عمر إلا علقمة، ولا عن علقمة إلا محمد بن إبراهيم، ولا عنه إلا يحيى.",
        "status": "Supported by Collected Evidence",
        "open_questions": "هل توجد متابعات معتبرة خارج الكتب الستة قبل يحيى بن سعيد؟"
    }
    res = client.post(f"/api/workspace/projects/{proj_id}/claims", json=claim_payload, headers=headers_a)
    assert res.status_code == 200
    claim_id = res.json()["id"]

    # Link supporting evidence to claim
    link_payload = {
        "evidence_item_id": ev_id,
        "relation_type": "Supports",
        "notes": "طريق البخاري يثبت تسلسل الرواية الفردية عبر يحيى بن سعيد."
    }
    res = client.post(f"/api/workspace/claims/{claim_id}/links", json=link_payload, headers=headers_a)
    assert res.status_code == 200
    print(f"✓ Formulated claim and linked supporting evidence (Claim ID={claim_id})")

    # Link challenging evidence to claim
    link_payload_2 = {
        "evidence_item_id": narrator_ev_id,
        "relation_type": "Challenges",
        "notes": "تحت الفحص لمسارات أخرى."
    }
    res = client.post(f"/api/workspace/claims/{claim_id}/links", json=link_payload_2, headers=headers_a)
    assert res.status_code == 200
    print(f"✓ Linked challenging evidence to claim matrix.")

    # Verify claims matrix
    res = client.get(f"/api/workspace/projects/{proj_id}/claims", headers=headers_a)
    assert res.status_code == 200
    claims = res.json()["claims"]
    assert len(claims) >= 1
    assert claims[0]["support_count"] == 1
    assert claims[0]["challenge_count"] == 1
    print("✓ Claim evidence matrix successfully maintains supporting and challenging relations.")

    # 10. Side-by-Side Comparison Workspace
    print("\n--- TEST 10: Side-by-Side Hadith Comparison (Hadiths #1 and #2) ---")
    compare_payload = {
        "entity_type": "hadith",
        "source_ids": ["1", "2"]
    }
    res = client.post("/api/workspace/compare", json=compare_payload)
    assert res.status_code == 200
    comp_data = res.json()
    assert comp_data["count"] == 2
    assert "pairwise_analysis" in comp_data
    assert len(comp_data["pairwise_analysis"]) == 1
    pair = comp_data["pairwise_analysis"][0]
    print(f"✓ Comparison successful: Pair={pair['labels']}, Exact={pair['exact_equality']}, Normalized={pair['normalized_equality']}, Lexical Overlap={pair['lexical_token_overlap']}")
    print(f"  Scholarly caveat preserved: '{pair['scholarly_caveat']}'")

    # 11. Citation & Provenance Generator
    print("\n--- TEST 11: Citation & Provenance Panel ---")
    res = client.get("/api/workspace/citation?entity_type=hadith&source_id=1")
    assert res.status_code == 200
    cit_data = res.json()
    assert "chicago" in cit_data["citations"]
    assert "arabic_scholarly" in cit_data["citations"]
    assert "provenance_disclosure" in cit_data
    print(f"✓ Chicago Citation: {cit_data['citations']['chicago']}")
    print(f"✓ Arabic Citation:  {cit_data['citations']['arabic_scholarly']}")

    # 12. Traceable Research Dossier Export
    print("\n--- TEST 12: Research Dossier Export (Markdown & JSON) ---")
    export_payload = {
        "include_notes": True,
        "include_claims": True,
        "include_unresolved": True,
        "format": "markdown"
    }
    res = client.post(f"/api/workspace/projects/{proj_id}/export", json=export_payload, headers=headers_a)
    assert res.status_code == 200
    dossier = res.json()
    assert "content" in dossier
    assert "MĪZĀN AL-ḤADĪTH — SCHOLARLY RESEARCH DOSSIER" in dossier["content"]
    assert "SCHOLARLY INTEGRITY NOTICE" in dossier["content"]
    assert project_payload["title"] in dossier["content"]
    print(f"✓ Exported Markdown dossier ({len(dossier['content'])} characters).")

    # 13. Dedicated Workspace Search
    print("\n--- TEST 13: Workspace Private Search ---")
    res = client.get("/api/workspace/search?q=النيات", headers=headers_a)
    assert res.status_code == 200
    search_data = res.json()
    assert search_data["domain"] == "SEARCH_MY_RESEARCH"
    assert len(search_data["projects"]) >= 1
    assert len(search_data["claims"]) >= 1
    print(f"✓ Private workspace search isolated and verified. Matches: {search_data['total_matches']}")

    # 14. User Privacy & Ownership Isolation
    print("\n--- TEST 14: User Isolation & Access Control ---")
    # User B should NOT see User A's project
    res = client.get(f"/api/workspace/projects/{proj_id}", headers=headers_b)
    assert res.status_code == 404, f"Expected 404 for User B, got {res.status_code}"

    res = client.get("/api/workspace/projects", headers=headers_b)
    assert res.status_code == 200
    assert len(res.json()["projects"]) == 0
    print("✓ Cross-user access strictly prevented: User B cannot access User A's private research.")

    # 15. Archival & Restoration
    print("\n--- TEST 15: Project Archival & Restoration ---")
    res = client.patch(f"/api/workspace/projects/{proj_id}", json={"is_archived": True}, headers=headers_a)
    assert res.status_code == 200
    res = client.get("/api/workspace/projects?archived=true", headers=headers_a)
    assert len(res.json()["projects"]) == 1

    res = client.patch(f"/api/workspace/projects/{proj_id}", json={"is_archived": False}, headers=headers_a)
    assert res.status_code == 200
    print("✓ Project archival and restoration validated.")

    print("\n================================================================")
    print("ALL 15 RESEARCH WORKSPACE BACKEND TESTS PASSED SUCCESSFULLY!")
    print("================================================================")

if __name__ == "__main__":
    run_workspace_tests()
