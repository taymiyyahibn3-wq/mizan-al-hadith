"""
Mīzān al-Ḥadīth — FastAPI Commentary Endpoint Integration Tests
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Set up paths so both repo root (for src) and backend (for scholarly_service, etc.) are importable
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(REPO_ROOT, "mizan-web", "backend")
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_commentary_endpoints():
    print("Testing FastAPI Commentary Endpoints...")

    # 1. Bukhari Hadith 1 (Multi-Commentary)
    r1 = client.get("/api/hadith/1/commentaries")
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
    d1 = r1.json()
    assert d1["available"] is True
    assert d1["total_commentaries"] >= 3
    print(f"  [PASS] Bukhari #1 returned {d1['total_commentaries']} verified commentaries:")
    for c in d1["commentaries"]:
        print(f"         • {c['commentary_title']} by {c['author']} (Status: {c['mapping_status']}, Conf: {c['mapping_confidence']})")

    # 2. Muslim Hadith 7032
    r2 = client.get("/api/hadith/7032/commentaries")
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["available"] is True
    print(f"  [PASS] Muslim #7032 returned: {d2['commentaries'][0]['commentary_title']}")

    # 3. Abu Dawud Hadith 16323
    r3 = client.get("/api/hadith/16323/commentaries")
    assert r3.status_code == 200
    d3 = r3.json()
    assert d3["available"] is True
    print(f"  [PASS] Abu Dawud #16323 returned: {d3['commentaries'][0]['commentary_title']}")

    # 4. Tirmidhi Hadith 12399
    r4 = client.get("/api/hadith/12399/commentaries")
    assert r4.status_code == 200
    d4 = r4.json()
    assert d4["available"] is True
    print(f"  [PASS] Tirmidhi #12399 returned: {d4['commentaries'][0]['commentary_title']}")

    # 5. Nasa'i Hadith 20915
    r5 = client.get("/api/hadith/20915/commentaries")
    assert r5.status_code == 200
    d5 = r5.json()
    assert d5["available"] is True
    print(f"  [PASS] Nasa'i #20915 returned: {d5['commentaries'][0]['commentary_title']}")

    # 6. Ibn Majah Hadith 26606
    r6 = client.get("/api/hadith/26606/commentaries")
    assert r6.status_code == 200
    d6 = r6.json()
    assert d6["available"] is True
    print(f"  [PASS] Ibn Majah #26606 returned: {d6['commentaries'][0]['commentary_title']}")

    # 7. Fail-Closed for Non-Existent Hadith
    r7 = client.get("/api/hadith/999999/commentaries")
    assert r7.status_code == 200
    d7 = r7.json()
    assert d7["available"] is False
    assert len(d7["commentaries"]) == 0
    print("  [PASS] Non-existent Hadith fails closed gracefully (zero leaked records)")

    # 8. Unaltered Scholarly Statements / Grades
    rg = client.get("/api/hadith/1/grades")
    assert rg.status_code == 200
    print("  [PASS] Existing /grades endpoint untouched and functional")

    # 9. Single Commentary endpoint /api/hadith/{hadith_id}/commentary
    r9 = client.get("/api/hadith/1/commentary")
    assert r9.status_code == 200
    d9 = r9.json()
    assert d9["available"] is True
    assert "commentary" in d9
    print(f"  [PASS] /api/hadith/1/commentary returned primary commentary: {d9['commentary']['commentary_title']}")

    print("\nALL FASTAPI ENDPOINT INTEGRATION TESTS PASSED SUCCESSFULLY! (9/9)")

if __name__ == "__main__":
    test_commentary_endpoints()
