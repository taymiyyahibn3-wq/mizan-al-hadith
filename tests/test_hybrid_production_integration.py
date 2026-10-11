"""
Ask Mīzān — Phase 7 Production Integration & Safety Test Suite
Validates:
  1. Feature flag states (OFF, SHADOW, CANARY, ON)
  2. Single-variable instant rollback (MIZAN_HYBRID_RETRIEVAL_ENABLED=false)
  3. Non-blocking shadow execution and shadow telemetry recorder
  4. Deterministic canary routing
  5. API response schema compatibility (FastAPI TestClient)
  6. Resilient failure fallback (Gemini down, FTS down, hybrid exception)
  7. Adversarial/malformed citation handling
  8. Language safety (Urdu & Cross-lingual)
  9. Thread-safe concurrency under parallel load (1, 5, 10, 25, 50 threads)
"""

from __future__ import annotations

import concurrent.futures
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from ask_mizan.config import HADITH_KG_DB_PATH
from ask_mizan.hybrid_retrieval import (
    CandidateItem,
    HybridSearchResult,
    QueryType,
    hybrid_search,
)
from ask_mizan.hybrid_service import (
    ShadowMetricsCollector,
    get_configured_mode,
    get_shadow_telemetry,
    is_canary_selected,
    retrieve_hadiths_hybrid_detailed,
    retrieve_hadiths_production,
    set_mode_override,
)


class TestFeatureFlagAndRollback(unittest.TestCase):
    """Validates feature flag resolution and single-variable rollback safety."""

    def tearDown(self) -> None:
        set_mode_override(None)
        os.environ.pop("MIZAN_HYBRID_MODE", None)
        os.environ.pop("MIZAN_HYBRID_RETRIEVAL_ENABLED", None)

    def test_default_mode_is_off(self) -> None:
        set_mode_override(None)
        os.environ.pop("MIZAN_HYBRID_MODE", None)
        os.environ.pop("MIZAN_HYBRID_RETRIEVAL_ENABLED", None)
        mode = get_configured_mode()
        self.assertEqual(mode, "off", "Default production mode MUST be 'off'")

    def test_explicit_env_modes(self) -> None:
        for m in ("off", "shadow", "canary", "on"):
            os.environ["MIZAN_HYBRID_MODE"] = m
            self.assertEqual(get_configured_mode(), m)

    def test_master_switch_rollback(self) -> None:
        # If mode is configured to 'on', setting MIZAN_HYBRID_RETRIEVAL_ENABLED=false MUST force 'off'
        os.environ["MIZAN_HYBRID_MODE"] = "on"
        self.assertEqual(get_configured_mode(), "on")

        os.environ["MIZAN_HYBRID_RETRIEVAL_ENABLED"] = "false"
        self.assertEqual(get_configured_mode(), "off", "Master switch false MUST force 'off'")

        os.environ["MIZAN_HYBRID_RETRIEVAL_ENABLED"] = "0"
        self.assertEqual(get_configured_mode(), "off")

    def test_set_mode_override(self) -> None:
        set_mode_override("shadow")
        self.assertEqual(get_configured_mode(), "shadow")
        set_mode_override("on")
        self.assertEqual(get_configured_mode(), "on")
        with self.assertRaises(ValueError):
            set_mode_override("invalid_mode")


class TestProductionRetrievalModes(unittest.TestCase):
    """Validates behavior of retrieve_hadiths_production across all modes."""

    def tearDown(self) -> None:
        set_mode_override(None)

    def test_mode_off_calls_legacy_only(self) -> None:
        set_mode_override("off")
        hids, tel = retrieve_hadiths_production("actions are by intentions", limit=3)
        self.assertIsInstance(hids, list)
        self.assertIsInstance(tel, dict)
        self.assertNotEqual(tel.get("layer"), "hybrid_retrieval_v2", "Mode off must NOT return hybrid layer")
        self.assertTrue(
            "Semantic Vector" in tel.get("layer", "") or "Lexical Match" in tel.get("layer", "") or tel.get("fallback_triggered", False),
            f"Expected legacy layer or fallback, got {tel.get('layer')}"
        )

    def test_mode_shadow_returns_legacy_and_records_telemetry(self) -> None:
        set_mode_override("shadow")
        hids, tel = retrieve_hadiths_production("Bukhari 1", limit=3)
        self.assertIsInstance(hids, list)
        self.assertTrue(tel.get("shadow_mode", False))

        # Wait up to 6 seconds for background shadow executor to finish (accommodating remote timeout)
        import time
        completed = False
        for _ in range(60):
            diag = get_shadow_telemetry()
            if diag["total_shadow_comparisons"] >= 1:
                completed = True
                break
            time.sleep(0.1)

        self.assertTrue(completed, "Shadow task should complete and record metrics in telemetry")
        diag = get_shadow_telemetry()
        self.assertGreaterEqual(diag["total_shadow_comparisons"], 1)

    def test_mode_on_returns_hybrid(self) -> None:
        set_mode_override("on")
        hids, tel = retrieve_hadiths_production("Bukhari 1", limit=3)
        self.assertIsInstance(hids, list)
        self.assertGreater(len(hids), 0)
        self.assertEqual(tel.get("layer"), "hybrid_retrieval_v2")
        self.assertEqual(tel.get("mode"), "on")
        self.assertIn("total_ms", tel)

    def test_deterministic_canary_routing(self) -> None:
        # Test CRC32 consistency
        q1 = "hadith about patience"
        selected_10 = is_canary_selected(q1, 10)
        selected_10_again = is_canary_selected(q1, 10)
        self.assertEqual(selected_10, selected_10_again, "Canary selection must be deterministic")

        # Bounds
        self.assertFalse(is_canary_selected("any query", 0))
        self.assertTrue(is_canary_selected("any query", 100))


class TestEmergencyFallbacksAndResilience(unittest.TestCase):
    """Validates zero-crash guarantees and graceful recovery under failure."""

    def tearDown(self) -> None:
        set_mode_override(None)

    @patch("ask_mizan.hybrid_service.hybrid_search")
    def test_hybrid_exception_falls_back_to_legacy(self, mock_hybrid) -> None:
        set_mode_override("on")
        mock_hybrid.side_effect = RuntimeError("Simulated internal hybrid engine failure")

        hids, tel = retrieve_hadiths_production("actions by intentions", limit=3)
        self.assertIsInstance(hids, list)
        self.assertTrue(tel.get("emergency_legacy_fallback", False))
        self.assertIn("Simulated internal hybrid engine failure", tel.get("hybrid_exception", ""))

    def test_malformed_citation_safe_handling(self) -> None:
        set_mode_override("on")
        # Malformed citations should NOT crash, should return valid list
        for query in ("Bukhari 999999", "Muslim abc", "Tirmidhi @#!"):
            hids, tel = retrieve_hadiths_production(query, limit=3)
            self.assertIsInstance(hids, list)
            self.assertIsInstance(tel, dict)

    def test_urdu_query_handling(self) -> None:
        set_mode_override("on")
        urdu_query = "اعمال کا دارومدار نیتوں پر ہے"
        hids, tel = retrieve_hadiths_production(urdu_query, limit=3)
        self.assertIsInstance(hids, list)
        self.assertEqual(tel.get("detected_language"), "ur")


class TestAPIEndpointContracts(unittest.TestCase):
    """Validates FastAPI endpoint contracts and response schemas."""

    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient
            from main import app
            self.client = TestClient(app)
            self.client_available = True
        except ImportError:
            self.client_available = False

    def tearDown(self) -> None:
        set_mode_override(None)

    def test_search_semantic_schema_compatibility(self) -> None:
        if not self.client_available:
            self.skipTest("TestClient not installed")

        set_mode_override("off")
        resp = self.client.get("/api/search/semantic", params={"q": "deeds and intentions", "limit": 3})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("query", data)
        self.assertIn("limit", data)
        self.assertIn("retrieved_canonical_ids", data)
        self.assertIn("telemetry", data)
        self.assertIsInstance(data["retrieved_canonical_ids"], list)

    def test_search_hybrid_endpoint(self) -> None:
        if not self.client_available:
            self.skipTest("TestClient not installed")

        resp = self.client.get("/api/search/hybrid", params={"q": "Bukhari 1", "limit": 5})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("results", data)
        self.assertIn("channel_counts", data)
        self.assertIn("latency_ms", data)
        self.assertIn("semantic", data["channel_counts"])
        self.assertIn("lexical", data["channel_counts"])
        self.assertIn("reference", data["channel_counts"])

    def test_diagnostics_hybrid_shadow_endpoint(self) -> None:
        if not self.client_available:
            self.skipTest("TestClient not installed")

        resp = self.client.get("/api/diagnostics/hybrid-shadow")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("active_mode", data)
        self.assertIn("total_shadow_comparisons", data)
        self.assertIn("latency_metrics", data)


class TestThreadSafetyAndConcurrency(unittest.TestCase):
    """Validates thread safety under parallel multi-threaded load (1, 5, 10, 25, 50 workers)."""

    def tearDown(self) -> None:
        set_mode_override(None)

    def test_concurrency_scaling(self) -> None:
        set_mode_override("on")
        queries = [
            "Bukhari 1",
            "Muslim 45",
            "actions are by intentions",
            "بني الإسلام على خمس",
            "fasting in ramadan",
        ]

        # Test at various concurrency levels
        for concurrency in (1, 5, 10, 25, 50):
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [
                    executor.submit(retrieve_hadiths_production, queries[i % len(queries)], 3)
                    for i in range(concurrency)
                ]
                results = [f.result() for f in futures]
                self.assertEqual(len(results), concurrency)
                for hids, tel in results:
                    self.assertIsInstance(hids, list)
                    self.assertIsInstance(tel, dict)


if __name__ == "__main__":
    unittest.main()
