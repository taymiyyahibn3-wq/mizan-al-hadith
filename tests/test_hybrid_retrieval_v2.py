"""
MĪZĀN AL-ḤADĪTH — Phase 6B Test Suite
Tests Hybrid Retrieval v2 Engine:
  1. Query Router classification
  2. Reciprocal Rank Fusion (RRF) logic & edge cases
  3. Graceful fallback on provider outages
  4. Canonical Expansion & immutability guarantees
"""

from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

# Add backend directory to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from ask_mizan.hybrid_retrieval import (
    CandidateItem,
    CanonicalExpander,
    FusedCandidateItem,
    FusionEngine,
    HybridSearchEngine,
    ImmutableDataManager,
    QueryRoute,
    QueryRouter,
    QueryType,
    hybrid_search,
)


class TestQueryRouter(unittest.TestCase):
    """Test deterministic query classification."""

    def test_reference_citations(self):
        cases = [
            ("Bukhari 1", QueryType.REFERENCE),
            ("Muslim 1907", QueryType.REFERENCE),
            ("Sahih al-Bukhari #1", QueryType.REFERENCE),
            ("hadith 123", QueryType.REFERENCE),
            ("صحيح البخاري 1", QueryType.REFERENCE),
            ("جامع الترمذي 29", QueryType.REFERENCE),
            ("sunan abu dawud 4", QueryType.REFERENCE),
        ]
        for q, expected in cases:
            route = QueryRouter.classify_query(q)
            self.assertEqual(
                route.query_type,
                expected,
                f"Failed for query '{q}': expected {expected}, got {route.query_type}",
            )

    def test_verbatim_arabic(self):
        cases = [
            ("انما الاعمال بالنيات", QueryType.VERBATIM_ARABIC, "ar"),
            ("طلب العلم فريضة", QueryType.VERBATIM_ARABIC, "ar"),
            ("لا يؤمن احدكم حتى يحب لاخيه", QueryType.VERBATIM_ARABIC, "ar"),
        ]
        for q, expected, lang in cases:
            route = QueryRouter.classify_query(q)
            self.assertEqual(route.query_type, expected)
            self.assertEqual(route.detected_language, lang)

    def test_cross_lingual_english(self):
        cases = [
            ("What does Islam say about intentions?", QueryType.CROSS_LINGUAL, "en"),
            ("Rewards for patience during trials and suffering", QueryType.CROSS_LINGUAL, "en"),
            ("Hadith regarding honesty and speaking the truth", QueryType.CROSS_LINGUAL, "en"),
        ]
        for q, expected, lang in cases:
            route = QueryRouter.classify_query(q)
            self.assertEqual(route.query_type, expected)
            self.assertEqual(route.detected_language, lang)

    def test_cross_lingual_urdu(self):
        cases = [
            ("نماز کے فضائل اور احکام", QueryType.CROSS_LINGUAL, "ur"),
            ("سچ بولنے کی فضیلت اور جھوٹ کے نقصانات", QueryType.CROSS_LINGUAL, "ur"),
            ("والدین کے ساتھ حسن سلوک کی احادیث", QueryType.CROSS_LINGUAL, "ur"),
        ]
        for q, expected, lang in cases:
            route = QueryRouter.classify_query(q)
            self.assertEqual(route.query_type, expected)
            self.assertEqual(route.detected_language, lang)

    def test_mixed_queries(self):
        cases = [
            ("Bukhari hadith about intentions and sincerity", QueryType.MIXED),
            ("Muslim narrations on fasting and Ramadan", QueryType.MIXED),
            ("bukhari on charity", QueryType.MIXED),
        ]
        for q, expected in cases:
            route = QueryRouter.classify_query(q)
            self.assertEqual(route.query_type, expected)


class TestReciprocalRankFusion(unittest.TestCase):
    """Test RRF fusion logic and boundary conditions."""

    def test_candidate_in_both_pools(self):
        # Candidate 101 is in both semantic (rank 1) and lexical (rank 1)
        # Candidate 102 is only semantic (rank 2)
        # Candidate 103 is only lexical (rank 2)
        sem = [
            CandidateItem(group_id=101, score=0.9, rank=1, source="semantic"),
            CandidateItem(group_id=102, score=0.8, rank=2, source="semantic"),
        ]
        lex = [
            CandidateItem(group_id=101, score=0.95, rank=1, source="lexical"),
            CandidateItem(group_id=103, score=0.7, rank=2, source="lexical"),
        ]
        ref = []

        fused = FusionEngine.fuse(
            semantic_pool=sem,
            lexical_pool=lex,
            reference_pool=ref,
            w_sem=1.0,
            w_lex=0.4,
            k=60.0,
        )

        self.assertEqual(len(fused), 3)
        # Candidate 101 must be Rank 1 due to reinforcement from both pools
        self.assertEqual(fused[0].group_id, 101)
        self.assertEqual(fused[0].fused_rank, 1)
        self.assertEqual(fused[0].semantic_rank, 1)
        self.assertEqual(fused[0].lexical_rank, 1)
        self.assertIn("semantic", fused[0].sources)
        self.assertIn("lexical", fused[0].sources)

        # Expected score for 101: 1.0 / (60 + 1) + 0.4 / (60 + 1) = 1.4 / 61
        expected_score_101 = round((1.0 / 61.0) + (0.4 / 61.0), 6)
        self.assertAlmostEqual(fused[0].rrf_score, expected_score_101, places=5)

    def test_candidate_only_in_one_pool(self):
        sem = [CandidateItem(group_id=201, score=0.85, rank=1, source="semantic")]
        lex = []
        ref = []

        fused = FusionEngine.fuse(sem, lex, ref, w_sem=1.0, w_lex=0.4, k=60.0)
        self.assertEqual(len(fused), 1)
        self.assertEqual(fused[0].group_id, 201)
        self.assertEqual(fused[0].semantic_rank, 1)
        self.assertIsNone(fused[0].lexical_rank)

    def test_empty_pools(self):
        fused = FusionEngine.fuse([], [], [], k=60.0)
        self.assertEqual(fused, [])

    def test_reference_pinning(self):
        sem = [CandidateItem(group_id=301, score=0.99, rank=1, source="semantic")]
        lex = [CandidateItem(group_id=302, score=0.95, rank=1, source="lexical")]
        ref = [CandidateItem(group_id=319, score=1.0, rank=1, source="reference")]

        # With pin_reference=True, 319 must be Rank 1
        fused = FusionEngine.fuse(sem, lex, ref, pin_reference=True)
        self.assertEqual(fused[0].group_id, 319)
        self.assertEqual(fused[0].fused_rank, 1)


class TestFallbackAndSafety(unittest.TestCase):
    """Test engine resilience when components or keys are offline."""

    def test_graceful_lexical_fallback_when_gemini_offline(self):
        engine = HybridSearchEngine.get_instance()
        # Force mode="lexical_only" to simulate Gemini unavailable
        res = engine.search("Bukhari 1", mode="lexical_only")
        self.assertIsNotNone(res)
        self.assertGreater(len(res.fused_candidates), 0)
        self.assertGreater(len(res.final_results), 0)
        self.assertIn("lexical_ms", res.latency_ms)

    def test_all_failed_clean_response(self):
        # Empty query
        res = hybrid_search("")
        self.assertIsNotNone(res)
        self.assertEqual(len(res.final_results), 0)
        self.assertIn(res.fallback_status, ("empty_candidates", "all_failed"))


class TestCanonicalImmutability(unittest.TestCase):
    """Test database connection query_only safety."""

    def test_query_only_enforced(self):
        data_mgr = ImmutableDataManager.get_instance()
        conn = data_mgr.open_ro_conn(Path("data/hadith-kg.db"))
        self.assertIsNotNone(conn)
        try:
            # Querying must succeed
            row = conn.execute("SELECT count(*) AS c FROM hadiths;").fetchone()
            self.assertGreater(row["c"], 0)

            # Any mutation attempt MUST raise sqlite3.OperationalError (attempt to write a readonly database)
            with self.assertRaises(sqlite3.OperationalError):
                conn.execute("UPDATE hadiths SET group_id = 999 WHERE id = 1;")
        finally:
            conn.close()

    def test_canonical_expansion_deterministic(self):
        expander = CanonicalExpander(ImmutableDataManager.get_instance())
        # Group 319 is the famous Innamal A'malu bin-Niyyat
        fused = [FusedCandidateItem(group_id=319, rrf_score=0.03, fused_rank=1)]
        expanded = expander.expand(fused, per_group_limit=3)
        self.assertGreater(len(expanded), 0)
        # Verify first hadith is Bukhari (book_id=1)
        self.assertEqual(expanded[0].book_id, 1)
        self.assertEqual(expanded[0].group_id, 319)


class TestPhase6CAdversarialAndPinning(unittest.TestCase):
    """Phase 6C Adversarial validation, pinning correctness, and leakage checks."""

    def test_unseen_valid_references(self):
        engine = HybridSearchEngine.get_instance()
        # Bukhari 2 and Muslim 45 are real canonical hadiths outside the original benchmark
        for query_str in ["Bukhari 2", "Muslim 45", "البخاري 2"]:
            res = engine.search(query_str, mode="lexical_only")
            self.assertIsNotNone(res)
            self.assertEqual(res.query_type, "REFERENCE")
            self.assertGreater(len(res.reference_candidates), 0)
            self.assertEqual(res.fused_candidates[0].group_id, res.reference_candidates[0].group_id)
            self.assertEqual(res.fused_candidates[0].fused_rank, 1)

    def test_malformed_and_out_of_bounds_citations(self):
        engine = HybridSearchEngine.get_instance()
        # Bukhari 999999 and Muslim abc do NOT exist in canonical databases
        malformed = ["Bukhari 999999", "Muslim abc", "Bukhari"]
        for q in malformed:
            res = engine.search(q, mode="lexical_only")
            self.assertIsNotNone(res)
            # Reference candidates MUST be empty
            self.assertEqual(len(res.reference_candidates), 0, f"Expected 0 reference hits for malformed query '{q}'")
            # If fused candidates exist via lexical fallback, reference_rank must be None
            for fc in res.fused_candidates:
                self.assertIsNone(fc.reference_rank)

    def test_pinning_only_on_resolved_reference(self):
        # 1. Valid reference candidate must be pinned
        ref_cand = [CandidateItem(group_id=500, score=1.0, rank=1, source="reference")]
        sem_cand = [CandidateItem(group_id=600, score=0.99, rank=1, source="semantic")]
        fused_pinned = FusionEngine.fuse(sem_cand, [], ref_cand, pin_reference=True)
        self.assertEqual(fused_pinned[0].group_id, 500)
        self.assertEqual(fused_pinned[0].fused_rank, 1)

        # 2. When reference pool is empty, pin_reference=True must NOT pin anything arbitrarily
        fused_unpinned = FusionEngine.fuse(sem_cand, [], [], pin_reference=True)
        self.assertEqual(fused_unpinned[0].group_id, 600)
        self.assertIsNone(fused_unpinned[0].reference_rank)

    def test_zero_benchmark_leakage(self):
        # Audit source code of hybrid_retrieval.py for benchmark query IDs or gold shortcuts
        code_path = REPO_ROOT / "mizan-web" / "backend" / "ask_mizan" / "hybrid_retrieval.py"
        content = code_path.read_text(encoding="utf-8")
        self.assertNotIn("AR_EXACT", content)
        self.assertNotIn("AR_PARA", content)
        self.assertNotIn("REF_EDGE", content)
        self.assertNotIn("embeddinggemma2_benchmark", content)


if __name__ == "__main__":
    unittest.main()
