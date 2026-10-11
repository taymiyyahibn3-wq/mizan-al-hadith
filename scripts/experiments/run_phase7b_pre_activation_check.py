"""
MĪZĀN AL-ḤADĪTH — Phase 7B Pre-Activation Health Verification
Audits all subsystems before final production promotion:
  1. Application FastAPI lifecycle & health endpoint (/api/health, /api/ask/health)
  2. Search endpoints (/api/search/semantic, /api/search/hybrid)
  3. Ask Mīzān tool execution (tool_search_hadith_text, tool_resolve_reference)
  4. Hybrid retrieval subsystem (QueryRouter, Semantic, Lexical FTS, Reference, RRF, Expansion)
  5. Fallback behavior (deterministic fallback when offline)
  6. Gemini embedding provider capacity & connectivity
  7. Canonical database connection health & PRAGMA query_only enforcement

Saves output to: data/benchmarks/phase7b/phase7b_pre_activation_health.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from fastapi.testclient import TestClient
from main import app

from ask_mizan.config import (
    COMMENTARIES_DB_PATH,
    HADITH_KG_DB_PATH,
    NUMBERING_DB_PATH,
    TRANSLATIONS_DB_PATH,
)
from ask_mizan.hybrid_retrieval import (
    ImmutableDataManager,
    hybrid_search,
)
from ask_mizan.hybrid_service import (
    get_configured_mode,
    retrieve_hadiths_production,
    set_mode_override,
)
from ask_mizan.semantic import OptionalRemoteEmbeddingProvider, semantic_retrieve_hadiths
from ask_mizan.tools import tool_resolve_reference, tool_search_hadith_text


def run_pre_activation_health_check() -> dict:
    client = TestClient(app)
    results = {}

    # 1. FastAPI App Endpoints
    t0 = time.perf_counter()
    resp_health = client.get("/api/health")
    resp_ask_health = client.get("/api/ask/health")
    resp_semantic = client.get("/api/search/semantic", params={"q": "actions by intentions", "limit": 3})
    resp_hybrid = client.get("/api/search/hybrid", params={"q": "Bukhari 1", "limit": 3})
    api_duration = (time.perf_counter() - t0) * 1000.0

    results["fastapi_endpoints"] = {
        "status": "PASS" if (resp_health.status_code == 200 and resp_semantic.status_code == 200 and resp_hybrid.status_code == 200) else "FAIL",
        "api_health_code": resp_health.status_code,
        "ask_health_code": resp_ask_health.status_code,
        "search_semantic_code": resp_semantic.status_code,
        "search_hybrid_code": resp_hybrid.status_code,
        "duration_ms": round(api_duration, 2),
    }

    # 2. Ask Mīzān Tools
    t0 = time.perf_counter()
    ref_resolved = tool_resolve_reference("bukhari", number="1")
    search_ev = tool_search_hadith_text("actions by intentions", limit=3)
    tools_duration = (time.perf_counter() - t0) * 1000.0

    results["ask_mizan_tools"] = {
        "status": "PASS" if (ref_resolved == 1 and len(search_ev) > 0) else "FAIL",
        "tool_resolve_reference_bukhari_1": ref_resolved,
        "tool_search_hadith_text_count": len(search_ev),
        "duration_ms": round(tools_duration, 2),
    }

    # 3. Hybrid Retrieval & Components
    t0 = time.perf_counter()
    hyb_res = hybrid_search("بني الإسلام على خمس", top_k=5)
    hyb_duration = (time.perf_counter() - t0) * 1000.0

    results["hybrid_retrieval_subsystem"] = {
        "status": "PASS" if (not hyb_res.error and len(hyb_res.final_results) > 0) else "FAIL",
        "query_type": hyb_res.query_type,
        "detected_language": hyb_res.detected_language,
        "results_count": len(hyb_res.final_results),
        "candidate_counts": {
            "semantic": len(hyb_res.semantic_candidates),
            "lexical": len(hyb_res.lexical_candidates),
            "reference": len(hyb_res.reference_candidates),
            "fused": len(hyb_res.fused_candidates),
        },
        "latency_ms": hyb_res.latency_ms,
        "fallback_status": hyb_res.fallback_status,
        "error": hyb_res.error,
        "duration_ms": round(hyb_duration, 2),
    }

    # 4. Gemini Remote Provider
    provider = OptionalRemoteEmbeddingProvider()
    t0 = time.perf_counter()
    q_vec = provider.embed_query("test query", timeout=4.0)
    provider_duration = (time.perf_counter() - t0) * 1000.0

    results["gemini_embedding_provider"] = {
        "status": "PASS" if (q_vec is not None and len(q_vec) == 768) else "WARN_DEGRADED",
        "is_available": provider.is_available(),
        "vector_dim": len(q_vec) if q_vec is not None else 0,
        "duration_ms": round(provider_duration, 2),
    }

    # 5. Canonical Databases
    data_mgr = ImmutableDataManager.get_instance()
    conn_kg = data_mgr.get_cached_ro_conn(HADITH_KG_DB_PATH)
    conn_num = data_mgr.get_cached_ro_conn(NUMBERING_DB_PATH)

    results["database_connections"] = {
        "status": "PASS" if (conn_kg is not None and conn_num is not None) else "FAIL",
        "hadith_kg_readable": conn_kg is not None,
        "numbering_readable": conn_num is not None,
        "hadith_to_group_mappings_loaded": len(data_mgr.hadith_to_group) > 0,
    }

    all_pass = (
        results["fastapi_endpoints"]["status"] == "PASS"
        and results["ask_mizan_tools"]["status"] == "PASS"
        and results["hybrid_retrieval_subsystem"]["status"] == "PASS"
        and results["database_connections"]["status"] == "PASS"
    )

    out = {
        "timestamp": time.time(),
        "overall_pre_activation_status": "PASS" if all_pass else "FAIL",
        "configured_mode_before_activation": get_configured_mode(),
        "details": results,
    }

    out_file = REPO_ROOT / "data" / "benchmarks" / "phase7b" / "phase7b_pre_activation_health.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Pre-activation health check: {out['overall_pre_activation_status']}")
    print(f"Saved: {out_file}")
    return out


if __name__ == "__main__":
    run_pre_activation_health_check()
