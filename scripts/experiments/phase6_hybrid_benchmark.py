"""
MĪZĀN AL-ḤADĪTH — Phase 6B Controlled Hybrid Retrieval v2 Benchmark Runner
Evaluates:
  1. Baseline A: Pure Gemini Semantic (gemini-embedding-001 live run)
  2. Baseline B: Pure Lexical / FTS5 (Arabic hadith_fts + English english_fts)
  3. System C: Hybrid Retrieval v2 (Query-Guided Multi-Retriever RRF)
  4. Separate Reference Sub-Evaluation (50 isolated reference/edge queries)

Measures:
  - Recall@1, Recall@5, Recall@10, MRR, nDCG@10
  - Breakdown by language: Arabic, Urdu, English, Cross-Lingual, Reference
  - Local component latencies: Routing, Lexical, Semantic, Fusion, Total (P50, P95, P99)
  - Programmatic calculation of absolute & relative deltas

Invariants:
  - Canonical databases remain 100% read-only.
  - Frozen benchmark labels are never modified.
  - Zero heavy rerankers.
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
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from ask_mizan.hybrid_retrieval import (
    CandidateItem,
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
GEMINI_LIVE_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "gemini_live_baseline_run_v1.json"
OUTPUT_BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "phase6" / "hybrid_retrieval_v2_benchmark.json"


def compute_metrics(queries: List[Dict[str, Any]], run_lookup: Dict[str, List[int]]) -> Dict[str, float]:
    """Computes Recall@1, Recall@5, Recall@10, MRR, nDCG@10."""
    if not queries:
        return {"recall_1": 0.0, "recall_5": 0.0, "recall_10": 0.0, "mrr": 0.0, "ndcg_10": 0.0}

    r1, r5, r10, rr, ndcg = [], [], [], [], []
    for q in queries:
        qid = q["query_id"]
        gold_gids = set(q.get("gold_group_ids", []))
        primary_gold = q.get("gold_group_ids", [None])[0]

        retrieved = run_lookup.get(qid, [])
        top1 = set(retrieved[:1])
        top5 = set(retrieved[:5])
        top10 = set(retrieved[:10])

        r1.append(1.0 if top1.intersection(gold_gids) else 0.0)
        r5.append(1.0 if top5.intersection(gold_gids) else 0.0)
        r10.append(1.0 if top10.intersection(gold_gids) else 0.0)

        # Reciprocal Rank
        q_rr = 0.0
        for rank, gid in enumerate(retrieved, start=1):
            if gid in gold_gids:
                q_rr = 1.0 / rank
                break
        rr.append(q_rr)

        # Graded nDCG@10
        dcg = 0.0
        for rank, gid in enumerate(retrieved[:10], start=1):
            rel = 0.0
            if gid == primary_gold:
                rel = 3.0
            elif gid in gold_gids:
                rel = 2.0
            if rel > 0:
                dcg += (2.0 ** rel - 1.0) / math.log2(rank + 1.0)

        ideal_rels = [3.0] if primary_gold else []
        for _ in range(len(gold_gids) - (1 if primary_gold else 0)):
            ideal_rels.append(2.0)
        idcg = sum((2.0 ** r - 1.0) / math.log2(rank + 1.0) for rank, r in enumerate(ideal_rels[:10], start=1))
        ndcg.append((dcg / idcg) if idcg > 0 else 0.0)

    return {
        "recall_1": round(float(np.mean(r1)), 4),
        "recall_5": round(float(np.mean(r5)), 4),
        "recall_10": round(float(np.mean(r10)), 4),
        "mrr": round(float(np.mean(rr)), 4),
        "ndcg_10": round(float(np.mean(ndcg)), 4),
    }


def compute_deltas(baseline: Dict[str, float], candidate: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """Computes absolute and percentage relative differences."""
    deltas = {}
    for metric, base_val in baseline.items():
        cand_val = candidate.get(metric, 0.0)
        abs_diff = round(cand_val - base_val, 4)
        rel_diff = round(((cand_val - base_val) / base_val * 100.0) if base_val > 0 else 0.0, 2)
        deltas[metric] = {
            "baseline": base_val,
            "candidate": cand_val,
            "absolute": abs_diff,
            "relative_pct": rel_diff,
        }
    return deltas


def main() -> None:
    print("=" * 80)
    print("MĪZĀN AL-ḤADĪTH — PHASE 6B HYBRID RETRIEVAL V2 BENCHMARK")
    print("=" * 80)

    # 1. Load benchmark queries
    print("\n[INFO] Loading frozen benchmark dataset...")
    queries = [json.loads(line) for line in open(BENCHMARK_PATH, encoding="utf-8") if line.strip()]
    semantic_queries = [q for q in queries if q["category"] not in ("reference_lookup", "edge_case")]
    reference_queries = [q for q in queries if q["category"] in ("reference_lookup", "edge_case")]
    print(f"[INFO] Loaded {len(queries)} total queries ({len(semantic_queries)} semantic, {len(reference_queries)} reference).")

    # 2. Load Gemini Live Baseline Run
    print("\n[INFO] Loading baseline Gemini live run...")
    gem_run = json.load(open(GEMINI_LIVE_RUN_PATH, encoding="utf-8"))
    gemini_lookup: Dict[str, List[int]] = {}
    for r in gem_run.get("results", []):
        gemini_lookup[r["query_id"]] = [item["group_id"] for item in r.get("retrieved", [])]
    print(f"[INFO] Loaded Gemini candidate pools for {len(gemini_lookup)} queries.")

    # 3. Initialize Staging Hybrid Components
    print("\n[INFO] Initializing Hybrid Retrieval v2 components...")
    data_mgr = ImmutableDataManager.get_instance()
    data_mgr.load_hadith_to_group_mapping()
    lex_retriever = LexicalCandidateRetriever(data_mgr)
    ref_retriever = ReferenceCandidateRetriever(data_mgr)
    router = QueryRouter()

    # 4. Execute Lexical, Reference, and Hybrid RRF across all 500 queries with latency profiling
    print("\n[INFO] Executing Hybrid Retrieval v2 pipeline across all 500 benchmark queries...")
    lexical_lookup: Dict[str, List[int]] = {}
    reference_resolver_lookup: Dict[str, List[int]] = {}
    hybrid_lookup: Dict[str, List[int]] = {}
    query_routes: Dict[str, str] = {}

    routing_latencies: List[float] = []
    lexical_latencies: List[float] = []
    fusion_latencies: List[float] = []
    total_latencies: List[float] = []

    t_bench_start = time.perf_counter()

    for q in queries:
        qid = q["query_id"]
        q_text = q["query"]

        t0_q = time.perf_counter()

        # Step 1: Routing
        t0_route = time.perf_counter()
        route = router.classify_query(q_text)
        dur_route = (time.perf_counter() - t0_route) * 1000.0
        routing_latencies.append(dur_route)
        query_routes[qid] = route.query_type.value

        # Step 2: Reference Candidate
        ref_candidates = ref_retriever.resolve(route)
        reference_resolver_lookup[qid] = [c.group_id for c in ref_candidates]

        # Step 3: Lexical Candidates
        t0_lex = time.perf_counter()
        if route.detected_language == "ar":
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
        elif route.detected_language == "en":
            lex_cands = lex_retriever.retrieve_english(q_text, top_k=50)
        elif route.detected_language == "ur":
            # Urdu queries use optional Arabic lexical loanword matching
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
        else:
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
        dur_lex = (time.perf_counter() - t0_lex) * 1000.0
        lexical_latencies.append(dur_lex)
        lexical_lookup[qid] = [c.group_id for c in lex_cands]

        # Step 4: Semantic Candidates (from baseline run)
        sem_gids = gemini_lookup.get(qid, [])
        sem_cands = [
            CandidateItem(group_id=gid, score=1.0 / math.sqrt(idx), rank=idx, source="semantic")
            for idx, gid in enumerate(sem_gids, start=1)
        ]

        # Step 5: Fusion (Query-Adaptive RRF)
        t0_fuse = time.perf_counter()
        q_type_str = route.query_type.value.lower()
        cfg = DEFAULT_RRF_CONFIG.get(q_type_str, DEFAULT_RRF_CONFIG["default"])
        w_sem = cfg.get("w_sem", 1.0)
        w_lex = cfg.get("w_lex", 0.4)
        w_ref = cfg.get("w_ref", 2.0)
        k_val = cfg.get("k", 60.0)

        pin_ref = (route.query_type == QueryType.REFERENCE and bool(ref_candidates))

        fused = FusionEngine.fuse(
            semantic_pool=sem_cands,
            lexical_pool=lex_cands,
            reference_pool=ref_candidates,
            w_sem=w_sem,
            w_lex=w_lex,
            w_ref=w_ref,
            k=k_val,
            top_k=50,
            pin_reference=pin_ref,
        )
        dur_fuse = (time.perf_counter() - t0_fuse) * 1000.0
        fusion_latencies.append(dur_fuse)

        hybrid_lookup[qid] = [fc.group_id for fc in fused]

        dur_total = (time.perf_counter() - t0_q) * 1000.0
        total_latencies.append(dur_total)

    t_bench_total = time.perf_counter() - t_bench_start
    print(f"[INFO] Completed full benchmark in {t_bench_total:.2f} s ({len(queries)/t_bench_total:.1f} QPS).")

    # 5. Compute Metrics Across All Segments
    # A. 450 Scored Semantic Queries
    metrics_gemini_sem = compute_metrics(semantic_queries, gemini_lookup)
    metrics_lexical_sem = compute_metrics(semantic_queries, lexical_lookup)
    metrics_hybrid_sem = compute_metrics(semantic_queries, hybrid_lookup)
    deltas_sem = compute_deltas(metrics_gemini_sem, metrics_hybrid_sem)

    # B. 50 Isolated Reference Queries
    ref_gemini = compute_metrics(reference_queries, gemini_lookup)
    ref_lexical = compute_metrics(reference_queries, lexical_lookup)
    ref_resolver = compute_metrics(reference_queries, reference_resolver_lookup)
    ref_hybrid = compute_metrics(reference_queries, hybrid_lookup)

    # C. Language Breakdown (Semantic Queries)
    breakdowns = {}
    for seg_name, filter_fn in [
        ("Arabic Semantic (150)", lambda q: q["language"] == "ar"),
        ("Urdu Semantic (100)", lambda q: q["language"] == "ur" and not q["category"].startswith("cross_lingual")),
        ("English Semantic (100)", lambda q: q["language"] == "en" and not q["category"].startswith("cross_lingual")),
        ("Cross-Lingual (100)", lambda q: q["category"].startswith("cross_lingual")),
    ]:
        sub_queries = [q for q in semantic_queries if filter_fn(q)]
        sub_gem = compute_metrics(sub_queries, gemini_lookup)
        sub_lex = compute_metrics(sub_queries, lexical_lookup)
        sub_hyb = compute_metrics(sub_queries, hybrid_lookup)
        breakdowns[seg_name] = {
            "count": len(sub_queries),
            "gemini": sub_gem,
            "lexical": sub_lex,
            "hybrid": sub_hyb,
            "delta": compute_deltas(sub_gem, sub_hyb),
        }

    # D. Router Distribution
    router_counts = defaultdict(int)
    for qtype in query_routes.values():
        router_counts[qtype] += 1

    # E. Latency Percentiles (ms)
    latency_stats = {
        "routing": {
            "p50": round(float(np.percentile(routing_latencies, 50)), 3),
            "p95": round(float(np.percentile(routing_latencies, 95)), 3),
            "p99": round(float(np.percentile(routing_latencies, 99)), 3),
        },
        "lexical": {
            "p50": round(float(np.percentile(lexical_latencies, 50)), 3),
            "p95": round(float(np.percentile(lexical_latencies, 95)), 3),
            "p99": round(float(np.percentile(lexical_latencies, 99)), 3),
        },
        "fusion": {
            "p50": round(float(np.percentile(fusion_latencies, 50)), 3),
            "p95": round(float(np.percentile(fusion_latencies, 95)), 3),
            "p99": round(float(np.percentile(fusion_latencies, 99)), 3),
        },
        "total_local_overhead": {
            "p50": round(float(np.percentile(total_latencies, 50)), 3),
            "p95": round(float(np.percentile(total_latencies, 95)), 3),
            "p99": round(float(np.percentile(total_latencies, 99)), 3),
        },
    }

    # 6. Display Performance Tables
    print("\n" + "=" * 80)
    print("PHASE 6B BENCHMARK RESULTS: 450 SCORED SEMANTIC QUERIES")
    print("=" * 80)
    print(f"{'Retriever System':<30} | {'Recall@1':<9} | {'Recall@5':<9} | {'Recall@10':<9} | {'MRR':<8} | {'nDCG@10':<8}")
    print("-" * 80)
    print(f"{'1. Pure Lexical / FTS':<30} | {metrics_lexical_sem['recall_1']:<9.4f} | {metrics_lexical_sem['recall_5']:<9.4f} | {metrics_lexical_sem['recall_10']:<9.4f} | {metrics_lexical_sem['mrr']:<8.4f} | {metrics_lexical_sem['ndcg_10']:<8.4f}")
    print(f"{'2. Pure Gemini Live (Baseline)':<30} | {metrics_gemini_sem['recall_1']:<9.4f} | {metrics_gemini_sem['recall_5']:<9.4f} | {metrics_gemini_sem['recall_10']:<9.4f} | {metrics_gemini_sem['mrr']:<8.4f} | {metrics_gemini_sem['ndcg_10']:<8.4f}")
    print(f"{'3. Hybrid Retrieval v2 (RRF)':<30} | {metrics_hybrid_sem['recall_1']:<9.4f} | {metrics_hybrid_sem['recall_5']:<9.4f} | {metrics_hybrid_sem['recall_10']:<9.4f} | {metrics_hybrid_sem['mrr']:<8.4f} | {metrics_hybrid_sem['ndcg_10']:<8.4f}")
    print("-" * 80)
    print("Deltas (Hybrid v2 vs Gemini Baseline):")
    for m in ["recall_1", "recall_5", "recall_10", "mrr", "ndcg_10"]:
        d = deltas_sem[m]
        sign = "+" if d["absolute"] >= 0 else ""
        print(f"  {m.upper():<10}: {d['baseline']:.4f} -> {d['candidate']:.4f} ({sign}{d['absolute']:.4f}, {sign}{d['relative_pct']}%)")

    print("\n" + "=" * 80)
    print("REFERENCE & CITATION QUERIES (50 Isolated Queries)")
    print("=" * 80)
    print(f"{'Retriever Strategy':<30} | {'Recall@1':<9} | {'Recall@5':<9} | {'Recall@10':<9} | {'MRR':<8} | {'nDCG@10':<8}")
    print("-" * 80)
    print(f"{'Pure Gemini Semantic':<30} | {ref_gemini['recall_1']:<9.4f} | {ref_gemini['recall_5']:<9.4f} | {ref_gemini['recall_10']:<9.4f} | {ref_gemini['mrr']:<8.4f} | {ref_gemini['ndcg_10']:<8.4f}")
    print(f"{'Pure Lexical FTS':<30} | {ref_lexical['recall_1']:<9.4f} | {ref_lexical['recall_5']:<9.4f} | {ref_lexical['recall_10']:<9.4f} | {ref_lexical['mrr']:<8.4f} | {ref_lexical['ndcg_10']:<8.4f}")
    print(f"{'Reference Resolver Alone':<30} | {ref_resolver['recall_1']:<9.4f} | {ref_resolver['recall_5']:<9.4f} | {ref_resolver['recall_10']:<9.4f} | {ref_resolver['mrr']:<8.4f} | {ref_resolver['ndcg_10']:<8.4f}")
    print(f"{'Hybrid Retrieval v2 (Routed)':<30} | {ref_hybrid['recall_1']:<9.4f} | {ref_hybrid['recall_5']:<9.4f} | {ref_hybrid['recall_10']:<9.4f} | {ref_hybrid['mrr']:<8.4f} | {ref_hybrid['ndcg_10']:<8.4f}")

    print("\n" + "=" * 80)
    print("LANGUAGE SEGMENT BREAKDOWNS (Semantic Queries)")
    print("=" * 80)
    for seg_name, bdata in breakdowns.items():
        g_mrr = bdata['gemini']['mrr']
        h_mrr = bdata['hybrid']['mrr']
        h_r10 = bdata['hybrid']['recall_10']
        d_mrr = bdata['delta']['mrr']['relative_pct']
        sign = "+" if d_mrr >= 0 else ""
        print(f"{seg_name:<25}: Gem MRR={g_mrr:.4f} | Hyb MRR={h_mrr:.4f} ({sign}{d_mrr}%) | Hyb R@10={h_r10:.4f}")

    print("\n" + "=" * 80)
    print("QUERY ROUTER CLASSIFICATION DISTRIBUTION (500 Queries)")
    print("=" * 80)
    for qtype, cnt in sorted(router_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {qtype:<20}: {cnt:3d} ({cnt/len(queries)*100:5.1f}%)")

    print("\n" + "=" * 80)
    print("LOCAL OVERHEAD LATENCIES (milliseconds)")
    print("=" * 80)
    for stage, perc in latency_stats.items():
        print(f"  {stage:<22}: P50={perc['p50']:6.2f} ms | P95={perc['p95']:6.2f} ms | P99={perc['p99']:6.2f} ms")

    # 7. Write Structured JSON Artifact
    output_payload = {
        "benchmark_metadata": {
            "version": "Phase 6B",
            "timestamp": time.time(),
            "benchmark_dataset": "embeddinggemma2_benchmark_v1.jsonl",
            "total_queries": len(queries),
            "semantic_queries_count": len(semantic_queries),
            "reference_queries_count": len(reference_queries),
            "total_eval_duration_sec": round(t_bench_total, 2),
            "rrf_parameters": DEFAULT_RRF_CONFIG,
        },
        "semantic_metrics": {
            "pure_lexical": metrics_lexical_sem,
            "pure_gemini_baseline": metrics_gemini_sem,
            "hybrid_retrieval_v2": metrics_hybrid_sem,
            "deltas_vs_gemini": deltas_sem,
        },
        "reference_metrics": {
            "pure_gemini": ref_gemini,
            "pure_lexical": ref_lexical,
            "reference_resolver": ref_resolver,
            "hybrid_retrieval_v2": ref_hybrid,
        },
        "segment_breakdowns": breakdowns,
        "router_distribution": dict(router_counts),
        "latency_profile_ms": latency_stats,
    }

    OUTPUT_BENCHMARK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_BENCHMARK_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    print(f"\n[SUCCESS] Wrote complete Phase 6B benchmark payload to: {OUTPUT_BENCHMARK_PATH}")


if __name__ == "__main__":
    main()
