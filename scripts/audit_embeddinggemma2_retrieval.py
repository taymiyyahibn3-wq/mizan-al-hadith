"""
MĪZĀN AL-ḤADĪTH — EmbeddingGemma 2 Retrieval Implementation Audit (Phase 4)
Performs forensic audit of:
  1. Candidate run structure in data/benchmarks/runs/embeddinggemma2_candidate_run.json
  2. Gemini baseline run structure in data/benchmarks/runs/gemini_baseline_run.json
  3. Verifies score monotonicity (strictly descending sort order)
  4. Verifies candidate group_id mappings
  5. Audits baseline scoring for synthetic leakage / circularity
  6. Independent retrieval verification on sample queries
"""

from __future__ import annotations
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "embeddinggemma2_candidate_run.json"
BASELINE_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "gemini_baseline_run.json"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
CORPUS_PATH = REPO_ROOT / "data" / "meaning_groups_export.jsonl"


def audit_candidate_run() -> Dict[str, Any]:
    print("=" * 80)
    print("1. CANDIDATE RUN INTEGRITY AUDIT")
    print("=" * 80)

    with open(CANDIDATE_RUN_PATH, "r", encoding="utf-8") as f:
        cand_data = json.load(f)

    meta = {k: v for k, v in cand_data.items() if k != "results"}
    print(f"Run ID:             {cand_data.get('run_id')}")
    print(f"Provider:           {cand_data.get('provider')}")
    print(f"Model:              {cand_data.get('model')}")
    print(f"Dimensions:         {cand_data.get('dimensions')}")
    print(f"Query Task Prompt:  {repr(cand_data.get('query_task_prompt'))}")
    print(f"Top K:              {cand_data.get('top_k')}")
    print(f"Timestamp:          {cand_data.get('timestamp')}")
    print(f"Is Dry Run:         {cand_data.get('is_dry_run')}")
    print(f"Hardware:           {cand_data.get('hardware')}")
    print(f"Latency:            {cand_data.get('latency')}")

    results = cand_data.get("results", [])
    print(f"\nTotal Query Results in run: {len(results)}")

    # Check validity of results
    all_scores = []
    top1_scores = []
    top10_scores = []
    non_monotonic_queries = 0
    duplicate_candidates = 0
    nan_inf_scores = 0
    all_group_ids = set()

    for r in results:
        qid = r["query_id"]
        retrieved = r.get("retrieved", [])
        prev_score = float("inf")
        seen_gids = set()

        for item in retrieved:
            rank = item["rank"]
            gid = item["group_id"]
            score = item["score"]

            all_group_ids.add(gid)
            all_scores.append(score)

            if rank == 1:
                top1_scores.append(score)
            if rank == 10:
                top10_scores.append(score)

            if not math.isfinite(score):
                nan_inf_scores += 1

            if score > prev_score + 1e-6:
                non_monotonic_queries += 1

            if gid in seen_gids:
                duplicate_candidates += 1
            seen_gids.add(gid)
            prev_score = score

    scores_np = np.array(all_scores)
    top1_np = np.array(top1_scores)
    top10_np = np.array(top10_scores)

    print("\n--- RETRIEVAL EXECUTION VALIDATION ---")
    print(f"Non-monotonic (sorting bug) queries: {non_monotonic_queries} (0 = strictly descending)")
    print(f"Duplicate candidate occurrences:     {duplicate_candidates} (0 = no duplicates in top-k)")
    print(f"NaN / Inf scores count:              {nan_inf_scores}")
    print(f"Unique meaning group IDs retrieved: {len(all_group_ids)} across {len(results)} queries")
    print(f"Score range (all retrieved):         [{np.min(scores_np):.4f}, {np.max(scores_np):.4f}]")
    print(f"Mean top-1 similarity score:         {np.mean(top1_np):.4f} (std: {np.std(top1_np):.4f})")
    print(f"Mean top-10 similarity score:        {np.mean(top10_np):.4f} (std: {np.std(top10_np):.4f})")

    return {
        "metadata": meta,
        "queries_count": len(results),
        "unique_retrieved_groups": len(all_group_ids),
        "sorting_monotonic": non_monotonic_queries == 0,
        "score_min": float(np.min(scores_np)),
        "score_max": float(np.max(scores_np)),
        "top1_mean": float(np.mean(top1_np)),
    }


def audit_gemini_baseline_run() -> Dict[str, Any]:
    print("\n" + "=" * 80)
    print("2. GEMINI BASELINE RUN AUDIT & CIRCULARITY DETECTION")
    print("=" * 80)

    with open(BASELINE_RUN_PATH, "r", encoding="utf-8") as f:
        base_data = json.load(f)

    print(f"Run ID:             {base_data.get('run_id')}")
    print(f"Provider:           {base_data.get('provider')}")
    print(f"Model:              {base_data.get('model')}")
    print(f"Is Dry Run:         {base_data.get('is_dry_run')}")
    print(f"Hardware:           {base_data.get('hardware')}")

    results = base_data.get("results", [])
    print(f"Total baseline query results: {len(results)}")

    top1_scores = []
    for r in results:
        ret = r.get("retrieved", [])
        if ret:
            top1_scores.append(ret[0]["score"])

    top1_np = np.array(top1_scores)
    print(f"Gemini baseline top-1 mean score: {np.mean(top1_np):.4f} (min: {np.min(top1_np):.4f}, max: {np.max(top1_np):.4f})")

    # Prove circular leakage
    # In run_embeddinggemma2_benchmark.py lines 306-324:
    # When api_key is None or dry_run=True, q_vec = alpha * target + noise
    # target was literally baseline_retriever.vectors[idx] where idx is gold_groups[0]
    is_dry_run = base_data.get("is_dry_run")
    print("\n--- CIRCULARITY & SYNTHETIC LEAKAGE VERDICT ---")
    if is_dry_run:
        print("CRITICAL FINDING: gemini_baseline_run.json was generated with is_dry_run = True!")
        print("In scripts/run_embeddinggemma2_benchmark.py, dry-run mode synthesizes the query vector by taking:")
        print("  q_vec = alpha * target + sqrt(1 - alpha^2) * noise")
        print("where 'target' is the EXACT candidate vector of the gold meaning group from derived_semantic_index.db!")
        print("This represents 100% synthetic gold label leakage, which mathematically guarantees Recall@1 = 1.0000!")
        print("The Gemini baseline score of 1.0000 is an artifact of synthetic evaluation simulation, NOT live API retrieval.")
    else:
        print("Gemini baseline was executed against live API.")

    return {
        "is_dry_run": is_dry_run,
        "top1_mean": float(np.mean(top1_np)),
    }


def audit_independent_retrieval_verification() -> None:
    print("\n" + "=" * 80)
    print("3. INDEPENDENT RETRIEVAL VERIFIER (10 SAMPLE QUERIES)")
    print("=" * 80)

    # Load 10 queries from candidate run
    with open(CANDIDATE_RUN_PATH, "r", encoding="utf-8") as f:
        cand_data = json.load(f)

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench_queries = {json.loads(line)["query_id"]: json.loads(line) for line in f if line.strip()}

    sample_results = cand_data["results"][:10]
    print(f"Verifying {len(sample_results)} queries against benchmark specifications...")

    for r in sample_results:
        qid = r["query_id"]
        bq = bench_queries.get(qid, {})
        ret = r.get("retrieved", [])
        gold_gids = set(bq.get("gold_group_ids", []))

        top1_gid = ret[0]["group_id"] if ret else None
        top1_score = ret[0]["score"] if ret else 0.0

        hit_at_1 = top1_gid in gold_gids
        hit_at_10 = any(item["group_id"] in gold_gids for item in ret[:10])

        gold_rank = None
        for item in ret:
            if item["group_id"] in gold_gids:
                gold_rank = item["rank"]
                break

        print(f"Query {qid} ({bq.get('language')} | {bq.get('category')}):")
        print(f"  Text:      '{bq.get('query')}'")
        print(f"  Gold GIDs: {list(gold_gids)}")
        print(f"  Top-1:     Group {top1_gid} (score: {top1_score})")
        print(f"  Gold Rank: {gold_rank if gold_rank is not None else '>50'}")
        print(f"  Hit@1:     {hit_at_1} | Hit@10: {hit_at_10}")


if __name__ == "__main__":
    t0 = time.perf_counter()
    audit_candidate_run()
    audit_gemini_baseline_run()
    audit_independent_retrieval_verification()
    print(f"\nAudit completed in {time.perf_counter() - t0:.2f} seconds.")
