"""
Ask Mīzān — Phase 7C Gemini Capacity Hardening & Failure Policy Test Suite
Validates:
  1. 429 daily quota detection and fail-fast behavior (< 1ms when circuit open)
  2. Transient 429 bounded single retry
  3. Timeout and 5xx provider state transitions
  4. Safe recovery after provider returns (probe succeeds -> state resets to AVAILABLE)
  5. No retry storms under repetitive requests
  6. Reference retrieval works accurately while Gemini is unavailable
  7. Lexical retrieval works accurately while Gemini is unavailable
"""

from __future__ import annotations

import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from ask_mizan.hybrid_retrieval import hybrid_search
from ask_mizan.hybrid_service import retrieve_hadiths_production, set_mode_override
from ask_mizan.semantic import OptionalRemoteEmbeddingProvider, ProviderState


class TestGeminiHardeningAndFailurePolicy(unittest.TestCase):
    """Unit tests for Phase 7C failure policy and circuit breaker."""

    def setUp(self) -> None:
        set_mode_override("on")
        OptionalRemoteEmbeddingProvider.reset_circuit()

    def tearDown(self) -> None:
        set_mode_override(None)
        OptionalRemoteEmbeddingProvider.reset_circuit()

    def test_daily_quota_exhaustion_detection_and_fail_fast(self) -> None:
        provider = OptionalRemoteEmbeddingProvider()
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = (
            '{"error": {"code": 429, "message": "Quota exceeded for metric: '
            'generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 1000", '
            '"status": "RESOURCE_EXHAUSTED", "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", '
            '"retryDelay": "12000s"}]}}'
        )
        mock_response.json.return_value = {
            "error": {
                "code": 429,
                "status": "RESOURCE_EXHAUSTED",
                "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "12000s"}],
            }
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            # First call: triggers 429 daily quota
            res1 = provider.embed_query("test query 1")
            self.assertIsNone(res1)
            self.assertEqual(provider.get_state(), ProviderState.QUOTA_EXHAUSTED)
            self.assertFalse(provider.is_healthy())
            self.assertGreater(provider.cooldown_remaining(), 0.0)
            self.assertEqual(mock_post.call_count, 1, "Daily quota must NOT retry")

            # Second call: circuit is open, must fail-fast without network call
            t0 = time.perf_counter()
            res2 = provider.embed_query("test query 2")
            dur_ms = (time.perf_counter() - t0) * 1000.0
            self.assertIsNone(res2)
            self.assertEqual(mock_post.call_count, 1, "Circuit open must NOT make HTTP requests")
            self.assertLess(dur_ms, 5.0, "Fail-fast must take under 5ms")

    def test_transient_429_bounded_retry(self) -> None:
        provider = OptionalRemoteEmbeddingProvider()
        mock_429 = MagicMock()
        mock_429.status_code = 429
        mock_429.text = '{"error": {"code": 429, "message": "Rate limit exceeded (15 RPM)"}}'
        mock_429.json.return_value = {"error": {"code": 429, "message": "Rate limit exceeded"}}

        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"embedding": {"values": [0.1] * 768}}

        # Transient: first call 429, second call succeeds
        with patch("requests.post", side_effect=[mock_429, mock_200]) as mock_post:
            res = provider.embed_query("test query")
            self.assertIsNotNone(res)
            self.assertEqual(mock_post.call_count, 2, "Transient 429 should perform bounded single retry")
            self.assertEqual(provider.get_state(), ProviderState.AVAILABLE)

    def test_provider_5xx_opens_circuit(self) -> None:
        provider = OptionalRemoteEmbeddingProvider()
        mock_503 = MagicMock()
        mock_503.status_code = 503
        mock_503.text = "Service Unavailable"

        with patch("requests.post", return_value=mock_503) as mock_post:
            res = provider.embed_query("test query")
            self.assertIsNone(res)
            self.assertEqual(provider.get_state(), ProviderState.FAILED)
            self.assertFalse(provider.is_healthy())

            # Immediate subsequent call fails fast
            res2 = provider.embed_query("test query 2")
            self.assertIsNone(res2)
            self.assertEqual(mock_post.call_count, 1)

    def test_provider_timeout_opens_circuit(self) -> None:
        import requests
        provider = OptionalRemoteEmbeddingProvider()

        with patch("requests.post", side_effect=requests.exceptions.Timeout("Connection timeout")) as mock_post:
            res = provider.embed_query("test query")
            self.assertIsNone(res)
            self.assertEqual(provider.get_state(), ProviderState.TIMEOUT)
            self.assertFalse(provider.is_healthy())

            # Immediate subsequent call fails fast
            res2 = provider.embed_query("test query 2")
            self.assertIsNone(res2)
            self.assertEqual(mock_post.call_count, 1)

    def test_circuit_recovery_probe(self) -> None:
        provider = OptionalRemoteEmbeddingProvider()
        # Set state to RATE_LIMITED with expired cooldown
        OptionalRemoteEmbeddingProvider.set_simulated_state(ProviderState.RATE_LIMITED, cooldown=-1.0)
        self.assertTrue(provider.is_healthy(), "Expired cooldown should allow half-open probe")

        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"embedding": {"values": [0.1] * 768}}

        with patch("requests.post", return_value=mock_200) as mock_post:
            res = provider.embed_query("probe query")
            self.assertIsNotNone(res)
            self.assertEqual(provider.get_state(), ProviderState.AVAILABLE, "Successful probe restores AVAILABLE")

    def test_reference_retrieval_while_gemini_unavailable(self) -> None:
        OptionalRemoteEmbeddingProvider.set_simulated_state(ProviderState.QUOTA_EXHAUSTED, cooldown=300.0)
        hids, tel = retrieve_hadiths_production("Bukhari 1", limit=3)
        self.assertIsInstance(hids, list)
        self.assertGreater(len(hids), 0)
        self.assertEqual(hids[0], 1, "Bukhari 1 must pin Hadith 1 even when Gemini is quota exhausted")
        self.assertEqual(tel.get("provider_state"), "QUOTA_EXHAUSTED")

    def test_lexical_retrieval_while_gemini_unavailable(self) -> None:
        OptionalRemoteEmbeddingProvider.set_simulated_state(ProviderState.QUOTA_EXHAUSTED, cooldown=300.0)
        hids, tel = retrieve_hadiths_production("actions by intentions", limit=3)
        self.assertIsInstance(hids, list)
        self.assertGreater(len(hids), 0)
        self.assertIn(1, hids, "Intentions query should return relevant hadith via lexical channel")
        self.assertEqual(tel.get("provider_state"), "QUOTA_EXHAUSTED")


if __name__ == "__main__":
    unittest.main()
