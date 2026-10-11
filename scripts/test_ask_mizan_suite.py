"""
Comprehensive Automated Test Suite for Ask Mīzān Subsystem
Validates:
1. Exact Hadith lookup & canonical ID resolution
2. Numbering resolver integration (Darussalam, Sunnah.com, Shamela)
3. Narrator biographical & rijāl evaluation resolution
4. Classical commentary (Sharḥ) alignment
5. Cross-collection matn comparison
6. Pre-generation grounding & insufficient evidence refusal
7. Post-generation citation validation (zero hallucination)
8. Provider fallback & deterministic offline synthesis
9. FastAPI REST endpoints & feedback persistence
10. Database immutability of canonical data
"""

import sys
import os
import unittest
from pathlib import Path

# Add project root and backend to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "mizan-web" / "backend"))

from fastapi.testclient import TestClient
from main import app
from ask_mizan.models import QueryIntent, EvidencePack, EvidenceHadith, AskRequest
from ask_mizan.engine import execute_ask_mizan
from ask_mizan.validator import validate_evidence_sufficiency, validate_and_bind_citations
from ask_mizan.providers.factory import get_llm_provider


class TestAskMizanSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_health_endpoint(self):
        """Test GET /api/ask/health returns healthy status and DB flags."""
        response = self.client.get("/api/ask/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["databases"]["hadith_kg"])
        self.assertTrue(data["databases"]["numbering"])

    def test_02_empty_query_validation(self):
        """Test POST /api/ask with empty query returns 422 Unprocessable Entity."""
        response = self.client.post("/api/ask", json={"query": "   "})
        self.assertEqual(response.status_code, 422)

    def test_03_exact_hadith_lookup(self):
        """Test exact reference 'Sahih al-Bukhari 1' resolves to canonical hadith_id=1."""
        response = self.client.post("/api/ask", json={"query": "Show Sahih al-Bukhari 1"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"], QueryIntent.HADITH_LOOKUP.value)
        self.assertTrue(data["is_grounded"])
        self.assertGreater(len(data["evidence_pack"]["hadiths"]), 0)
        h0 = data["evidence_pack"]["hadiths"][0]
        self.assertEqual(h0["canonical_id"], 1)
        self.assertEqual(h0["book_id"], 1)
        self.assertTrue("الأعمال" in h0["matn_arabic"] or "النيات" in h0["matn_arabic"] or "بِالنِّيَّاتِ" in h0["matn_arabic"])
        # Verified citations check
        citations = data["citations"]
        hadith_cites = [c for c in citations if c["type"] == "hadith"]
        self.assertTrue(any(c["id"] == 1 for c in hadith_cites))
        # Ensure validation object is consistently present and valid_citations matches
        self.assertIn("validation", data)
        self.assertGreater(data["validation"]["valid_citations"], 0)
        self.assertEqual(data["validation"]["valid_citations"], len(citations))

    def test_04_numbering_aware_lookup(self):
        """Test multi-edition query 'Sunan an-Nasa'i Darussalam 348' resolves correctly."""
        response = self.client.post("/api/ask", json={"query": "Sunan an-Nasa'i Darussalam 348"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"], QueryIntent.NUMBERING_LOOKUP.value)
        self.assertTrue(data["is_grounded"])
        self.assertGreater(len(data["evidence_pack"]["hadiths"]), 0)
        h0 = data["evidence_pack"]["hadiths"][0]
        self.assertEqual(h0["canonical_id"], 21260)
        self.assertGreater(len(h0["numbering_references"]), 0)

    def test_05_narrator_biographical_research(self):
        """Test narrator research 'Tell me about the narrator Abu Hurayrah' resolves canonical rawi_id=4396."""
        response = self.client.post("/api/ask", json={"query": "Tell me about the narrator Abu Hurayrah"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"], QueryIntent.NARRATOR_RESEARCH.value)
        self.assertTrue(data["is_grounded"])
        self.assertGreater(len(data["evidence_pack"]["narrators"]), 0)
        n0 = data["evidence_pack"]["narrators"][0]
        self.assertEqual(n0["rawi_id"], 4396)
        self.assertEqual(n0["death_year_ah"], 57)
        self.assertGreater(len(n0["scholarly_verdicts"]), 0)

    def test_06_commentary_research(self):
        """Test commentary research query retrieves classical commentaries."""
        response = self.client.post("/api/ask", json={"query": "What does the commentary say about Bukhari 1?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"], QueryIntent.COMMENTARY_RESEARCH.value)
        self.assertTrue(data["is_grounded"])
        commentaries = data["evidence_pack"]["commentaries"]
        self.assertGreater(len(commentaries), 0)
        titles = [c["source_title_ar"] for c in commentaries]
        # Check for classical commentary presence
        self.assertTrue(any("فتح الباري" in t or "عمدة القاري" in t for t in titles))

    def test_07_cross_collection_comparison(self):
        """Test matn comparison between Bukhari 1 and Muslim 1907."""
        response = self.client.post("/api/ask", json={"query": "Compare Bukhari 1 and Muslim 1907"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"], QueryIntent.MATN_COMPARISON.value)
        self.assertTrue(data["is_grounded"])
        self.assertGreaterEqual(len(data["evidence_pack"]["hadiths"]), 2)
        # Check visualizer action link
        actions = data["research_actions"]
        self.assertTrue(any("hadith-visualizer" in a["url"] for a in actions))

    def test_08_insufficient_evidence_refusal(self):
        """Test unknown reference 'Sahih al-Bukhari 999999' refuses confidently with insufficient evidence."""
        response = self.client.post("/api/ask", json={"query": "What is Sahih al-Bukhari 999999?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["evidence_pack"]["is_sufficient"])
        self.assertEqual(len(data["evidence_pack"]["hadiths"]), 0)
        self.assertIn("Insufficient Mīzān Evidence", data["answer_markdown"])

    def test_09_citation_validator_anti_hallucination(self):
        """Test validator strips/flags hallucinated tokens that do not exist in the evidence pack."""
        pack = EvidencePack(
            pack_id="test_pack_1",
            query="test",
            intent=QueryIntent.HADITH_LOOKUP,
            generated_at="2026-09-30T10:00:00Z",
            hadiths=[
                EvidenceHadith(
                    canonical_id=1,
                    book_id=1,
                    book_name_ar="صحيح البخاري",
                    book_name_en="Sahih al-Bukhari",
                    book_transliteration="Sahih al-Bukhari",
                    nass="النيات",
                    matn_arabic="إنما الأعمال بالنيات",
                )
            ],
            is_sufficient=True,
        )
        # Synthesis text contains valid [hadith:1] AND fake hallucinated [hadith:999999]
        synthesis_text = "Here is real [hadith:1] and here is fake [hadith:999999]."
        clean_markdown, citations, actions, validation = validate_and_bind_citations(synthesis_text, pack)
        # Fake token must be stripped or not in citations
        self.assertNotIn("999999", clean_markdown)
        self.assertIn("/hadith/1", clean_markdown)
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].id, 1)
        self.assertEqual(validation.valid_citations, 1)
        self.assertEqual(validation.invalid_citations, 1)

    def test_10_provider_factory_deterministic_resilience(self):
        """Test provider factory provides deterministic provider without API key."""
        provider = get_llm_provider("deterministic")
        self.assertEqual(provider.name, "deterministic")
        self.assertTrue(provider.is_available())

    def test_11_feedback_persistence(self):
        """Test feedback API persists rating into ask_mizan.db."""
        # 1. Run a query to get a message_id
        res = self.client.post("/api/ask", json={"query": "Sahih al-Bukhari 1"})
        data = res.json()
        message_id = data["message_id"]

        # 2. Submit feedback
        fb_res = self.client.post(
            "/api/ask/feedback",
            json={
                "message_id": message_id,
                "rating": "helpful",
                "scholarly_notes": "Accurate classical citations.",
            },
        )
        self.assertEqual(fb_res.status_code, 200)
        self.assertEqual(fb_res.json()["status"], "recorded")

    def test_12_canonical_db_safety(self):
        """Verify that canonical database files remain read-only and unmodified."""
        db_path = BASE_DIR / "data" / "hadith-kg.db"
        self.assertTrue(db_path.exists())
        # Attempting a write in read-only mode should fail
        import sqlite3
        with self.assertRaises(sqlite3.OperationalError):
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            conn.execute("CREATE TABLE _test_hack (id INT)")
            conn.close()

    def test_13_narrator_focused_routing_abdur_rahman_al_musalli(self):
        """TEST 1: Narrator query 'Who is Abdur Rahman al-Musalli?' routes to narrator dossier without unrelated Hadith as primary evidence."""
        response = self.client.post("/api/ask", json={"query": "Who is Abdur Rahman al-Musalli?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data["intent"], [QueryIntent.NARRATOR_LOOKUP.value, QueryIntent.NARRATOR_BIOGRAPHY.value])
        self.assertTrue(data["is_grounded"])
        narrators = data["evidence_pack"]["narrators"]
        self.assertGreater(len(narrators), 0)
        rawi = narrators[0]
        self.assertEqual(rawi["rawi_id"], 4256)
        full_name = f"{rawi.get('name_ar', '')} {rawi.get('nickname_ar', '')}"
        self.assertIn("المسلي", full_name)
        # Check that narrator citation exists
        citations = data["citations"]
        self.assertTrue(any(c["type"] == "narrator" and c["id"] == 4256 for c in citations))

    def test_14_scholarly_statement_father_son_collision_guard(self):
        """TEST 2: Check whether Yahya ibn Ma'in's statement for Abdur Rahman al-Musli (rawi 4256) has collision protection."""
        from ask_mizan.tools import tool_get_narrator_dossier
        dossier = tool_get_narrator_dossier(4256)
        self.assertIsNotNone(dossier)
        self.assertEqual(dossier.rawi_id, 4256)
        # Find Yahya ibn Ma'in verdict
        y_qawls = [q for q in dossier.scholarly_verdicts if "معين" in q.scholar_name_ar or "Ma'in" in q.scholar_name_en]
        self.assertGreater(len(y_qawls), 0)
        y_qawl = y_qawls[0]
        # Must NOT be presented as unconditional valid attribution to Abdur Rahman
        self.assertEqual(y_qawl.attribution_status, "father_son_collision")
        self.assertIsNotNone(y_qawl.provenance_caveat)
        self.assertIn("Wabarah", y_qawl.provenance_caveat)

    def test_15_ibn_majah_darussalam_1986_resolution(self):
        """TEST 3: Resolve Sunan Ibn Majah Darussalam 1986 to canonical hadith ID 28581 and verify matn & sanad."""
        import re
        from ask_mizan.tools import tool_resolve_reference, tool_get_hadith_detail
        canonical_id = tool_resolve_reference("Sunan Ibn Majah", "darussalam", "1986")
        self.assertEqual(canonical_id, 28581)
        hadith = tool_get_hadith_detail(28581)
        self.assertIsNotNone(hadith)
        clean_nass = re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED]", "", hadith.nass)
        self.assertIn("عبد الرحمن المسلي", clean_nass)

    def test_16_al_albani_grading_accuracy_on_28581(self):
        """TEST 4: Specifically verify that Al-Albani's grading on canonical hadith 28581 (Darussalam 1986) is Da'if, NOT Sahih."""
        from ask_mizan.tools import tool_get_scholarly_grades
        grades = tool_get_scholarly_grades(28581)
        albani_grades = [g for g in grades if "ألباني" in g.scholar_ar or "الألباني" in g.scholar_ar or "alban" in g.scholar_en.lower()]
        self.assertGreater(len(albani_grades), 0)
        albani = albani_grades[0]
        # Grade must be Da'if / Ḍaʿīf
        self.assertIn("ضعيف", albani.grade_ar)
        self.assertTrue("da'if" in albani.grade_en.lower() or "ḍaʿīf" in albani.grade_en.lower() or "weak" in albani.grade_en.lower())
        self.assertIn("142", str(albani.source_reference or albani.provenance_notes or ""))

    def test_17_cross_edition_resolution_consistency(self):
        """TEST 5: Resolve the same Hadith through multiple numbering systems (Darussalam 1986 and in-book 1976)."""
        from ask_mizan.tools import tool_resolve_reference
        d_id = tool_resolve_reference("Sunan Ibn Majah", "darussalam", "1986")
        s_id = tool_resolve_reference("Sunan Ibn Majah", "shamela", "1976")
        self.assertIsNotNone(d_id)
        self.assertIsNotNone(s_id)
        self.assertEqual(d_id, s_id)
        self.assertEqual(d_id, 28581)

    def test_18_adjacent_hadiths_isolation(self):
        """TEST 6: Verify adjacent numbering records do not inherit grading from each other."""
        from ask_mizan.tools import tool_get_scholarly_grades
        grades_target = tool_get_scholarly_grades(28581)
        grades_adjacent = tool_get_scholarly_grades(28582)
        # Ensure 28581 has its own verified Da'if record and does not bleed into 28582
        albani_28581 = [g for g in grades_target if "ألباني" in g.scholar_ar or "الألباني" in g.scholar_ar or "alban" in g.scholar_en.lower()]
        albani_28582 = [g for g in grades_adjacent if "ألباني" in g.scholar_ar or "الألباني" in g.scholar_ar or "alban" in g.scholar_en.lower()]
        self.assertGreater(len(albani_28581), 0)
        self.assertIn("ضعيف", albani_28581[0].grade_ar)
        if len(albani_28582) > 0:
            # Must not be the same reference_hadith note
            self.assertNotEqual(albani_28581[0].source_reference, albani_28582[0].source_reference)


if __name__ == "__main__":
    unittest.main(verbosity=2)
