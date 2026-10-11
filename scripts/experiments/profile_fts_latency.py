"""
MĪZĀN AL-ḤADĪTH — Phase 6C Comprehensive Latency Profiler & Artifact Generator
Profiles all components of Hybrid Retrieval v2 across benchmark queries:
  - QueryRouter
  - LexicalCandidateRetriever (Optimized)
  - ReferenceCandidateRetriever
  - FusionEngine
  - CanonicalExpander
  - Total local pipeline overhead

Saves payload to: data/benchmarks/phase6c/phase6c_latency_profile.json
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from ask_mizan.hybrid_retrieval import (
    CandidateItem,
    CanonicalExpander,
    FusionEngine,
    ImmutableDataManager,
    LexicalCandidateRetriever,
    QueryRoute,
    QueryRouter,
    QueryType,
    ReferenceCandidateRetriever,
    DEFAULT_RRF_CONFIG,
)

BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
OUTPUT_PATH = REPO_ROOT / "data" / "benchmarks" / "phase6c" / "phase6c_latency_profile.json"


def main() -> None:
    print("=" * 80)
    print("MĪZĀN AL-ḤADĪTH — PHASE 6C COMPREHENSIVE LATENCY PROFILING")
    print("=" * 80)

    data_mgr = ImmutableDataManager.get_instance()
    data_mgr.load_hadith_to_group_mapping()
    router = QueryRouter()
    lex_retriever = LexicalCandidateRetriever(data_mgr)
    ref_retriever = ReferenceCandidateRetriever(data_mgr)
    expander = CanonicalExpander(data_mgr)

    queries = [json.loads(l) for l in open(BENCHMARK_PATH, encoding="utf-8") if l.strip()]
    print(f"[INFO] Profiling all {len(queries)} benchmark queries...")

    latencies_routing: List[float] = []
    latencies_lexical: List[float] = []
    latencies_reference: List[float] = []
    latencies_fusion: List[float] = []
    latencies_expansion: List[float] = []
    latencies_total_local: List[float] = []

    arabic_lex_latencies: List[float] = []
    english_lex_latencies: List[float] = []

    per_query_records: List[Dict[str, Any]] = []

    for q in queries:
        qid = q["query_id"]
        q_text = q["query"]

        t_total_start = time.perf_counter()

        # 1. Routing
        t0 = time.perf_counter()
        route = router.classify_query(q_text)
        d_route = (time.perf_counter() - t0) * 1000.0
        latencies_routing.append(d_route)

        # 2. Reference candidate
        t0 = time.perf_counter()
        ref_cands = []
        if route.query_type in (QueryType.REFERENCE, QueryType.MIXED) or route.detected_reference:
            ref_cands = ref_retriever.resolve(route)
        d_ref = (time.perf_counter() - t0) * 1000.0
        latencies_reference.append(d_ref)

        # 3. Lexical candidates
        t0 = time.perf_counter()
        lex_cands = []
        backend = "none"
        if route.detected_language == "ar":
            backend = "arabic_fts"
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
            d_lex = (time.perf_counter() - t0) * 1000.0
            arabic_lex_latencies.append(d_lex)
        elif route.detected_language == "en":
            backend = "english_fts"
            lex_cands = lex_retriever.retrieve_english(q_text, top_k=50)
            d_lex = (time.perf_counter() - t0) * 1000.0
            english_lex_latencies.append(d_lex)
        else:
            backend = "arabic_fts_loanword"
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
            d_lex = (time.perf_counter() - t0) * 1000.0
            arabic_lex_latencies.append(d_lex)
        latencies_lexical.append(d_lex)

        # 4. Fusion simulation (with mock semantic candidates of depth 50)
        t0 = time.perf_counter()
        mock_sem = [CandidateItem(group_id=100 + i, score=1.0 / (i + 1), rank=i + 1, source="semantic") for i in range(50)]
        q_type_str = route.query_type.value.lower()
        cfg = DEFAULT_RRF_CONFIG.get(q_type_str, DEFAULT_RRF_CONFIG["default"])
        pin_ref = (route.query_type == QueryType.REFERENCE and bool(ref_cands))
        fused = FusionEngine.fuse(
            semantic_pool=mock_sem,
            lexical_pool=lex_cands,
            reference_pool=ref_cands,
            w_sem=cfg.get("w_sem", 1.0),
            w_lex=cfg.get("w_lex", 0.4),
            w_ref=cfg.get("w_ref", 2.0),
            k=cfg.get("k", 60.0),
            top_k=10,
            pin_reference=pin_ref,
        )
        d_fuse = (time.perf_counter() - t0) * 1000.0
        latencies_fusion.append(d_fuse)

        # 5. Canonical expansion
        t0 = time.perf_counter()
        expanded = expander.expand(fused, per_group_limit=2)
        d_exp = (time.perf_counter() - t0) * 1000.0
        latencies_expansion.append(d_exp)

        d_total_local = (time.perf_counter() - t_total_start) * 1000.0
        latencies_total_local.append(d_total_local)

        per_query_records.append({
            "query_id": qid,
            "query": q_text,
            "query_type": route.query_type.value,
            "language": route.detected_language,
            "backend": backend,
            "lex_cands_count": len(lex_cands),
            "ref_cands_count": len(ref_cands),
            "expanded_hadiths_count": len(expanded),
            "d_route_ms": round(d_route, 3),
            "d_ref_ms": round(d_ref, 3),
            "d_lex_ms": round(d_lex, 3),
            "d_fuse_ms": round(d_fuse, 3),
            "d_exp_ms": round(d_exp, 3),
            "d_total_local_ms": round(d_total_local, 3),
        })

    def get_stats(data: List[float]) -> Dict[str, float]:
        return {
            "p50": round(float(np.percentile(data, 50)), 2),
            "p95": round(float(np.percentile(data, 95)), 2),
            "p99": round(float(np.percentile(data, 99)), 2),
            "mean": round(float(np.mean(data)), 2),
            "max": round(float(np.max(data)), 2),
        }

    stats = {
        "router": get_stats(latencies_routing),
        "reference_resolver": get_stats(latencies_reference),
        "lexical_retriever_total": get_stats(latencies_lexical),
        "arabic_fts_only": get_stats(arabic_lex_latencies),
        "english_fts_only": get_stats(english_lex_latencies),
        "rrf_fusion": get_stats(latencies_fusion),
        "canonical_expander": get_stats(latencies_expansion),
        "total_local_pipeline_overhead": get_stats(latencies_total_local),
    }

    print("\n" + "=" * 80)
    print("HYBRID RETRIEVAL v2 — OPTIMIZED LATENCY PROFILE (500 Queries)")
    print("=" * 80)
    print(f"{'Component':<32} | {'P50 (ms)':<9} | {'P95 (ms)':<9} | {'P99 (ms)':<9} | {'Max (ms)':<9}")
    print("-" * 80)
    for comp, st in stats.items():
        print(f"{comp:<32} | {st['p50']:<9.2f} | {st['p95']:<9.2f} | {st['p99']:<9.2f} | {st['max']:<9.2f}")

    # Identify slowest queries in the optimized pipeline
    slowest = sorted(per_query_records, key=lambda x: x["d_total_local_ms"], reverse=True)[:5]
    print("\nTop 5 Slowest Local Queries:")
    for s in slowest:
        print(f"  [{s['d_total_local_ms']:6.2f} ms] [{s['query_id']}]: {s['query'][:70]} (lex: {s['d_lex_ms']} ms, exp: {s['d_exp_ms']} ms)")

    payload = {
        "benchmark_queries_count": len(queries),
        "optimization_applied": [
            "ARABIC_COMMON_PARTICLES exact-token formatting (eliminating prefix wildcard explosion)",
            "SQLite read-only connection pooling and handle reuse in ImmutableDataManager",
            "PRAGMA mmap_size = 268435456 (256MB memory mapped I/O)",
            "PRAGMA cache_size = -16000 (16MB cache)",
        ],
        "latency_percentiles_ms": stats,
        "slowest_queries": slowest,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\n[SUCCESS] Wrote latency profile artifact to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
