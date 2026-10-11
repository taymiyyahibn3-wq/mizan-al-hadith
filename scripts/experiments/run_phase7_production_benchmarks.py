"""
MĪZĀN AL-ḤADĪTH — Phase 7 Production Benchmark Runner
Executes:
  1. Shadow Validation Benchmark (Legacy vs Hybrid Comparison)
  2. Production Latency Profiling (Component-by-component breakdown)
  3. Controlled Concurrency Scaling Test (1, 5, 10, 25, 50 parallel workers)

Outputs:
  data/benchmarks/phase7/phase7_shadow_validation.json
  data/benchmarks/phase7/phase7_latency_profile.json
  data/benchmarks/phase7/phase7_concurrency_test.json
"""

from __future__ import annotations

import concurrent.futures
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

from ask_mizan.hybrid_retrieval import (
    HybridSearchEngine,
    HybridSearchResult,
    hybrid_search,
)
from ask_mizan.hybrid_service import (
    retrieve_hadiths_production,
    set_mode_override,
)
from ask_mizan.semantic import semantic_retrieve_hadiths


sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)


def load_test_queries() -> List[Dict[str, Any]]:
    """Loads a balanced mix of 30 benchmark and citation queries across all language and query types."""
    queries = []

    # 1. Load from frozen Phase 2 benchmark (20 queries: 5 ar_exact, 5 ar_para, 5 en_cross, 5 ur_cross)
    bm_path = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
    if bm_path.exists():
        with open(bm_path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]

        target_cats = {
            "ar_exact": 5,
            "ar_paraphrase": 5,
            "en_crosslingual": 5,
            "ur_crosslingual": 5,
        }
        curr_counts = defaultdict(int)
        for item in lines:
            cat = item.get("category", "")
            if curr_counts[cat] < target_cats.get(cat, 0):
                queries.append({
                    "query": item["query"],
                    "category": cat,
                    "language": item.get("language", "ar"),
                })
                curr_counts[cat] += 1

    # 2. Load from Phase 6C unseen citations (10 queries: 5 en_citation, 5 ar_citation)
    unseen_path = REPO_ROOT / "data" / "benchmarks" / "phase6c" / "phase6c_unseen_reference_queries.jsonl"
    if unseen_path.exists():
        with open(unseen_path, "r", encoding="utf-8") as f:
            unseen_lines = [json.loads(line) for line in f if line.strip()]

        curr_unseen = defaultdict(int)
        target_unseen = {
            "unseen_english_citation": 5,
            "unseen_arabic_citation": 5,
        }
        for item in unseen_lines:
            cat = item.get("category", "")
            if curr_unseen[cat] < target_unseen.get(cat, 0):
                queries.append({
                    "query": item["query"],
                    "category": cat,
                    "language": item.get("language", "ar"),
                })
                curr_unseen[cat] += 1

    return queries


def run_shadow_validation(queries: List[Dict[str, Any]]) -> Dict[str, Any]:
    print(f"\n--- Running Shadow Validation on {len(queries)} queries ---", flush=True)
    set_mode_override("on")

    agreements = 0
    disagreements = 0
    overlap_counts = []
    jaccard_scores = []
    legacy_latencies = []
    hybrid_latencies = []
    reference_activations = 0
    lexical_contributions = 0
    hybrid_fallbacks = 0
    hybrid_errors = 0

    per_category = defaultdict(lambda: {"total": 0, "agree": 0, "disagree": 0, "avg_jaccard": []})

    for idx, q_item in enumerate(queries, 1):
        q = q_item["query"]
        cat = q_item["category"]
        print(f"[{idx}/{len(queries)}] Evaluating '{q[:35]}' ({cat})...", flush=True)

        # Run legacy
        t0 = time.perf_counter()
        leg_hids, _ = semantic_retrieve_hadiths(q, limit=5)
        leg_ms = (time.perf_counter() - t0) * 1000.0
        legacy_latencies.append(leg_ms)

        # Run hybrid
        t1 = time.perf_counter()
        hyb_res = hybrid_search(q, top_k=5)
        hyb_ms = (time.perf_counter() - t1) * 1000.0
        hybrid_latencies.append(hyb_ms)

        hyb_hids = [h.hadith_id for h in hyb_res.final_results]

        if hyb_res.error:
            hybrid_errors += 1
        if hyb_res.fallback_status != "none":
            hybrid_fallbacks += 1
        if hyb_res.reference_candidates:
            reference_activations += 1
        if hyb_res.lexical_candidates:
            lexical_contributions += 1

        top1_agree = bool(leg_hids and hyb_hids and leg_hids[0] == hyb_hids[0])
        if top1_agree:
            agreements += 1
        else:
            disagreements += 1

        set_leg = set(leg_hids)
        set_hyb = set(hyb_hids)
        intersection = len(set_leg & set_hyb)
        union = len(set_leg | set_hyb)
        jaccard = (intersection / union) if union > 0 else 0.0

        overlap_counts.append(intersection)
        jaccard_scores.append(jaccard)

        per_category[cat]["total"] += 1
        if top1_agree:
            per_category[cat]["agree"] += 1
        else:
            per_category[cat]["disagree"] += 1
        per_category[cat]["avg_jaccard"].append(jaccard)

    total_q = len(queries)
    agree_rate = (agreements / total_q) if total_q > 0 else 0.0
    disagree_rate = (disagreements / total_q) if total_q > 0 else 0.0

    cat_summary = {}
    for cat, data in per_category.items():
        cat_summary[cat] = {
            "total_queries": data["total"],
            "top1_agreement_rate": round(data["agree"] / data["total"], 4) if data["total"] > 0 else 0.0,
            "top1_disagreement_rate": round(data["disagree"] / data["total"], 4) if data["total"] > 0 else 0.0,
            "mean_jaccard_similarity": round(float(np.mean(data["avg_jaccard"])), 4) if data["avg_jaccard"] else 0.0,
        }

    out = {
        "dataset_size": total_q,
        "agreement_count": agreements,
        "disagreement_count": disagreements,
        "agreement_rate": round(agree_rate, 4),
        "disagreement_rate": round(disagree_rate, 4),
        "mean_top5_overlap_count": round(float(np.mean(overlap_counts)), 2),
        "mean_jaccard_similarity": round(float(np.mean(jaccard_scores)), 4),
        "reference_activations": reference_activations,
        "lexical_contributions": lexical_contributions,
        "hybrid_fallbacks": hybrid_fallbacks,
        "hybrid_errors": hybrid_errors,
        "latency_comparison": {
            "legacy_ms": {
                "p50": round(float(np.percentile(legacy_latencies, 50)), 2),
                "p95": round(float(np.percentile(legacy_latencies, 95)), 2),
                "p99": round(float(np.percentile(legacy_latencies, 99)), 2),
                "mean": round(float(np.mean(legacy_latencies)), 2),
            },
            "hybrid_ms": {
                "p50": round(float(np.percentile(hybrid_latencies, 50)), 2),
                "p95": round(float(np.percentile(hybrid_latencies, 95)), 2),
                "p99": round(float(np.percentile(hybrid_latencies, 99)), 2),
                "mean": round(float(np.mean(hybrid_latencies)), 2),
            },
        },
        "per_category_analysis": cat_summary,
    }

    print(f"Agreement Rate: {agree_rate:.2%} | Disagreement Rate: {disagree_rate:.2%}")
    print(f"Mean Jaccard: {np.mean(jaccard_scores):.4f} | Fallbacks: {hybrid_fallbacks} | Errors: {hybrid_errors}")
    return out


def run_latency_profiling(queries: List[Dict[str, Any]]) -> Dict[str, Any]:
    print("\n--- Running Latency Profiling (Component-by-component) ---")
    comp_times = defaultdict(list)

    for q_item in queries:
        q = q_item["query"]
        res = hybrid_search(q, top_k=5)
        for comp, ms in res.latency_ms.items():
            comp_times[comp].append(ms)

    profile = {}
    for comp, times in comp_times.items():
        profile[comp] = {
            "p50_ms": round(float(np.percentile(times, 50)), 2),
            "p95_ms": round(float(np.percentile(times, 95)), 2),
            "p99_ms": round(float(np.percentile(times, 99)), 2),
            "max_ms": round(float(np.max(times)), 2),
            "mean_ms": round(float(np.mean(times)), 2),
        }

    return profile


def run_concurrency_benchmarks(queries: List[Dict[str, Any]]) -> Dict[str, Any]:
    print("\n--- Running Concurrency Benchmarks (1, 5, 10, 25, 50 workers) ---", flush=True)
    concurrency_levels = [1, 5, 10, 25, 50]
    results = {}

    set_mode_override("on")

    for concurrency in concurrency_levels:
        print(f"Testing concurrency level: {concurrency} ...", flush=True)
        latencies = []
        errors = 0
        sqlite_errors = 0
        n_req = 25

        t_start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = []
            for i in range(n_req):
                q = queries[i % len(queries)]["query"]
                futures.append(executor.submit(retrieve_hadiths_production, q, 5))

            for f in concurrent.futures.as_completed(futures):
                try:
                    hids, tel = f.result()
                    lat = tel.get("total_ms", 0.0)
                    if lat > 0:
                        latencies.append(lat)
                except Exception as exc:
                    errors += 1
                    if "sqlite" in str(exc).lower():
                        sqlite_errors += 1

        total_wall_s = time.perf_counter() - t_start
        qps = round(n_req / total_wall_s, 2)

        results[f"concurrency_{concurrency}"] = {
            "concurrency_level": concurrency,
            "requests_submitted": n_req,
            "requests_succeeded": n_req - errors,
            "success_rate": round((n_req - errors) / float(n_req), 4),
            "total_wall_time_s": round(total_wall_s, 3),
            "throughput_qps": qps,
            "sqlite_errors": sqlite_errors,
            "unhandled_exceptions": errors,
            "latency_p50_ms": round(float(np.percentile(latencies, 50)), 2) if latencies else 0.0,
            "latency_p95_ms": round(float(np.percentile(latencies, 95)), 2) if latencies else 0.0,
            "latency_p99_ms": round(float(np.percentile(latencies, 99)), 2) if latencies else 0.0,
        }
        print(f"  Level {concurrency}: QPS={qps}, P50={np.percentile(latencies, 50):.2f}ms, Errors={errors}")

    return results


def main() -> None:
    queries = load_test_queries()
    print(f"Loaded {len(queries)} evaluation queries.")

    # 1. Shadow Validation
    shadow_data = run_shadow_validation(queries)
    shadow_file = REPO_ROOT / "data" / "benchmarks" / "phase7" / "phase7_shadow_validation.json"
    with open(shadow_file, "w", encoding="utf-8") as f:
        json.dump(shadow_data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {shadow_file}")

    # 2. Latency Profiling
    latency_data = run_latency_profiling(queries)
    latency_file = REPO_ROOT / "data" / "benchmarks" / "phase7" / "phase7_latency_profile.json"
    with open(latency_file, "w", encoding="utf-8") as f:
        json.dump(latency_data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {latency_file}")

    # 3. Concurrency Benchmarks
    concurrency_data = run_concurrency_benchmarks(queries)
    concurrency_file = REPO_ROOT / "data" / "benchmarks" / "phase7" / "phase7_concurrency_test.json"
    with open(concurrency_file, "w", encoding="utf-8") as f:
        json.dump(concurrency_data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {concurrency_file}")

    # Reset mode back to default OFF
    set_mode_override(None)
    print("\nPhase 7 benchmark suite successfully completed. Default mode restored to OFF.")


if __name__ == "__main__":
    main()
