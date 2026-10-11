"""
Critical Bug Fix Sprint Regression Test Suite
Validates the 4 critical incidents:
1. Incident 1: Sufyān al-Thawrī entity resolution (rawi 3436, NOT 3432, 3443, or 4698)
2. Incident 2: Hadith of intentions query routing & retrieval across all 7 variants
3. Incident 3: Sahih al-Bukhari 1 English translation retrieval pipeline from hadith_translations.db
4. Incident 4: Insufficient-evidence notice format and clean rendering without raw markdown markers
"""

import re
import sys
import unittest
from pathlib import Path

# Setup sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "mizan-web" / "backend"))

from fastapi.testclient import TestClient
from main import app
from ask_mizan.parser import parse_query
from ask_mizan.models import QueryIntent
from identity_resolution import search_canonical_identities, FAMOUS_CLASSICAL_ALIASES
from db_manager import get_db, get_translations_db


def strip_tashkeel(text: str) -> str:
    """Removes Arabic diacritics / tashkeel."""
    if not text:
        return ""
    return re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED]", "", text)


class TestCriticalFixesSprint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # =========================================================================
    # INCIDENT 1: Sufyān al-Thawrī Entity Resolution & Cross-Contamination Guard
    # =========================================================================

    def test_01_famous_aliases_mapping_accuracy(self):
        """Verify that FAMOUS_CLASSICAL_ALIASES keys map to the exact canonical scholars."""
        # Key 3436 must be Sufyan al-Thawri
        self.assertIn(3436, FAMOUS_CLASSICAL_ALIASES)
        thawri_aliases = FAMOUS_CLASSICAL_ALIASES[3436]
        self.assertTrue(any("سفيان الثوري" in a["arabic"] for a in thawri_aliases))

        # Key 3443 must be Sufyan ibn Uyaynah
        self.assertIn(3443, FAMOUS_CLASSICAL_ALIASES)
        uyaynah_aliases = FAMOUS_CLASSICAL_ALIASES[3443]
        self.assertTrue(any("سفيان بن عيينة" in a["arabic"] for a in uyaynah_aliases))

        # Key 6659 must be Malik ibn Anas
        self.assertIn(6659, FAMOUS_CLASSICAL_ALIASES)
        malik_aliases = FAMOUS_CLASSICAL_ALIASES[6659]
        self.assertTrue(any("مالك بن أنس" in a["arabic"] for a in malik_aliases))

        # Key 3432 must NOT be in aliases as Sufyan al-Thawri
        if 3432 in FAMOUS_CLASSICAL_ALIASES:
            self.assertFalse(any("سفيان الثوري" in a["arabic"] for a in FAMOUS_CLASSICAL_ALIASES[3432]))

    def test_02_sufyan_al_thawri_canonical_resolution(self):
        """Query 'Tell me about Sufyan al-Thawri' must resolve to CANON-RAW-003436."""
        db = get_db()
        try:
            data = search_canonical_identities("Sufyan al-Thawri", db=db, limit=5)
            results = data["results"]
            self.assertGreater(len(results), 0)
            top = results[0]
            self.assertEqual(top["canonical_id"], "CANON-RAW-003436")
            self.assertEqual(top["anchor_rawi_id"], 3436)
            self.assertIn("سفيان بن سعيد", top["canonical_arabic_name"])
            self.assertIn("ثور", top["canonical_arabic_name"])
            # Sufyan al-Thawri has ~2917 narrations in HKG
            self.assertGreater(top["riwaya_qty"], 2000)
        finally:
            db.close()

    def test_03_negative_sufyan_ibn_hamzah_isolation(self):
        """Query 'Sufyan al-Thawri' must NOT resolve to Sufyan ibn Hamzah al-Aslami (3432)."""
        from ask_mizan.tools import tool_search_narrator_identities
        thawri_results = tool_search_narrator_identities("Sufyan al-Thawri", limit=5)
        self.assertGreater(len(thawri_results), 0)
        self.assertNotEqual(thawri_results[0].get("anchor_rawi_id", thawri_results[0].get("rawi_id")), 3432)
        self.assertEqual(thawri_results[0].get("anchor_rawi_id", thawri_results[0].get("rawi_id")), 3436)

        # But an explicit query for Sufyan ibn Hamzah MUST resolve to 3432
        aslami_results = tool_search_narrator_identities("Sufyan ibn Hamzah", limit=5)
        self.assertGreater(len(aslami_results), 0)
        self.assertEqual(aslami_results[0].get("anchor_rawi_id", aslami_results[0].get("rawi_id")), 3432)

    def test_04_negative_sufyan_ibn_uyaynah_isolation(self):
        """Query 'Sufyan ibn Uyaynah' must resolve to 3443, NOT 4698 (al-Humaydi)."""
        db = get_db()
        try:
            data = search_canonical_identities("Sufyan ibn Uyaynah", db=db, limit=5)
            results = data["results"]
            self.assertGreater(len(results), 0)
            self.assertEqual(results[0]["anchor_rawi_id"], 3443)
            self.assertNotEqual(results[0]["anchor_rawi_id"], 4698)
        finally:
            db.close()

    def test_05_ask_mizan_api_sufyan_al_thawri_narrator_dossier(self):
        """End-to-end Ask Mīzān API for 'Tell me about Sufyan al-Thawri'."""
        response = self.client.post("/api/ask", json={"query": "Tell me about Sufyan al-Thawri"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_grounded"])
        narrators = data["evidence_pack"]["narrators"]
        self.assertGreater(len(narrators), 0)
        top_rawi = narrators[0]
        self.assertEqual(top_rawi["rawi_id"], 3436)
        self.assertIn("سفيان بن سعيد", top_rawi["name_ar"])
        self.assertIn("ثور", top_rawi["name_ar"])
        # Ensure citations point to 3436
        narrator_citations = [c for c in data["citations"] if c["type"] == "narrator"]
        self.assertTrue(any(c["id"] == 3436 for c in narrator_citations))
        self.assertFalse(any(c["id"] == 3432 for c in narrator_citations))

    # =========================================================================
    # INCIDENT 2: Hadith of Intentions Query Routing & Retrieval (7 Variants)
    # =========================================================================

    def test_06_intentions_parser_routing(self):
        """Verify query parser routes all 7 intentions variants away from narrator lookup."""
        variants = [
            "Tell me about hadith of intentions",
            "Tell me the hadith about intentions",
            "Hadith of intentions",
            "Innama al-a'malu binniyat",
            "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ",
            "إنما الأعمال بالنيات",
            "Bukhari 1",
        ]
        for q in variants:
            with self.subTest(query=q):
                parsed = parse_query(q)
                self.assertNotIn(parsed.intent, [
                    QueryIntent.NARRATOR_LOOKUP,
                    QueryIntent.NARRATOR_BIOGRAPHY,
                    QueryIntent.JARH_TADIL,
                    QueryIntent.TEACHERS_STUDENTS,
                    QueryIntent.SCHOLARLY_STATEMENTS,
                ], f"Query '{q}' was mistakenly routed to narrator intent: {parsed.intent}")

    def test_07_intentions_end_to_end_retrieval(self):
        """Verify all 7 variants retrieve Sahih al-Bukhari 1 with verified evidence."""
        variants = [
            "Tell me about hadith of intentions",
            "Tell me the hadith about intentions",
            "Hadith of intentions",
            "Innama al-a'malu binniyat",
            "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ",
            "إنما الأعمال بالنيات",
            "Bukhari 1",
        ]
        for q in variants:
            with self.subTest(query=q):
                response = self.client.post("/api/ask", json={"query": q})
                self.assertEqual(response.status_code, 200, f"Query '{q}' returned status {response.status_code}")
                data = response.json()
                self.assertTrue(data["is_grounded"], f"Query '{q}' was not grounded")
                self.assertFalse(data.get("insufficient_evidence", False), f"Query '{q}' returned insufficient evidence")
                hadiths = data["evidence_pack"]["hadiths"]
                self.assertGreater(len(hadiths), 0, f"Query '{q}' returned 0 hadiths")
                top_h = hadiths[0]
                self.assertEqual(top_h["canonical_id"], 1, f"Query '{q}' returned canonical_id {top_h['canonical_id']} instead of 1")
                clean_matn = strip_tashkeel(top_h["matn_arabic"])
                self.assertIn("النيات", clean_matn)

    # =========================================================================
    # INCIDENT 3: English Translation Pipeline for Hadith Detail Page
    # =========================================================================

    def test_08_translations_db_connection(self):
        """Verify get_translations_db connects to canonical hadith_translations.db."""
        conn = get_translations_db()
        self.assertIsNotNone(conn, "get_translations_db() returned None")
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM hadith_translations")
        count = cur.fetchone()[0]
        self.assertEqual(count, 31488)
        conn.close()

    def test_09_bukhari_1_translation_api_endpoint(self):
        """GET /api/hadith/1/translations must return verified English translation."""
        response = self.client.get("/api/hadith/1/translations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["available"])
        self.assertEqual(data["hadith_id"], 1)
        self.assertGreater(len(data["translations"]), 0)
        t0 = data["translations"][0]
        self.assertEqual(t0["language"], "en")
        self.assertIn("Muhammad Muhsin Khan", t0["translator"])
        self.assertIn("Sahih al-Bukhari", t0["edition"])
        clean_text = re.sub(r"\s+", " ", t0["translation_text"].lower())
        self.assertIn("reward of deeds depends upon the intentions", clean_text)

    def test_10_missing_translation_graceful_handling(self):
        """GET /api/hadith/{id}/translations for hadith without translation returns available=False."""
        # Hadith ID 31 exists in hadith-kg.db but has no English translation in hadith_translations.db
        response = self.client.get("/api/hadith/31/translations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["available"])
        self.assertEqual(len(data["translations"]), 0)

        # For nonexistent hadith ID, endpoint returns 404
        nonexistent = self.client.get("/api/hadith/99999999/translations")
        self.assertEqual(nonexistent.status_code, 404)

    # =========================================================================
    # INCIDENT 4: Insufficient Evidence Formatting & Integrity
    # =========================================================================

    def test_11_insufficient_evidence_response_format(self):
        """When insufficient evidence is triggered, response must not contain raw blockquote alert markers."""
        response = self.client.post("/api/ask", json={"query": "What is Sahih al-Bukhari 999999?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("insufficient_evidence"))
        text = data["answer_markdown"]
        # Must not contain raw blockquote markers
        self.assertNotIn("> [!IMPORTANT]", text)
        self.assertNotIn("> [!NOTE]", text)
        self.assertNotIn("\n>", text)
        # Must preserve clean message
        self.assertIn("Insufficient Mīzān Evidence", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
