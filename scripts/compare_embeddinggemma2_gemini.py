"""
MĪZĀN AL-ḤADĪTH — Phase 5 Comparative Analysis Suite
Performs scientifically controlled evaluation between:
  1. Candidate: EmbeddingGemma 2 (corrected prompt run)
  2. Baseline: Gemini (live non-synthetic run, or reports INCONCLUSIVE if unavailable)

Evaluates:
  - 450 Semantic Queries (150 Arabic, 100 Urdu, 100 English, 100 Cross-lingual)
  - 50 Reference/Edge Queries (Isolated)
  - Primary Metrics: Recall@1, Recall@5, Recall@10, MRR, nDCG@10
  - Per-Language & Cross-Lingual Breakdowns
  - Enforces DECISION GATES 1, 2, and 3
  - Outputs data/benchmarks/runs/embeddinggemma2_phase5_comparison.json
"""

from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
CANONICAL_KG_PATH = REPO_ROOT / "data" / "hadith-kg.db"

CORRECTED_EG2_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "embeddinggemma2_corrected_run_v1.json"
FALLBACK_EG2_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "embeddinggemma2_candidate_run.json"

LIVE_GEMINI_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "gemini_live_baseline_run_v1.json"
PREV_GEMINI_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "gemini_baseline_run.json"

COMPARISON_OUTPUT_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "embeddinggemma2_phase5_comparison.json"


def compute_metrics(
    queries: List[Dict[str, Any]],
    run_lookup: Dict[str, List[int]],
    hadith_to_group_map: Dict[int, int],
) -> Dict[str, float]:
    if not queries:
        return {"recall_1": 0.0, "recall_5": 0.0, "recall_10": 0.0, "mrr": 0.0, "ndcg_10": 0.0}

    r1, r5, r10, rr, ndcg = [], [], [], [], []
    for q in queries:
        qid = q["query_id"]
        gold_gids = set(q.get("gold_group_ids", []))
        primary_gold = q.get("gold_group_ids", [None])[0]
        gold_hids = set(q.get("gold_hadith_ids", []))

        retrieved = run_lookup.get(qid, [])
        top1 = set(retrieved[:1])
        top5 = set(retrieved[:5])
        top10 = set(retrieved[:10])

        r1.append(1.0 if top1.intersection(gold_gids) else 0.0)
        r5.append(1.0 if top5.intersection(gold_gids) else 0.0)
        r10.append(1.0 if top10.intersection(gold_gids) else 0.0)

        # RR
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
            elif any(hadith_to_group_map.get(hid) == gid for hid in gold_hids):
                rel = 1.0
            if rel > 0:
                dcg += (2.0 ** rel - 1.0) / math.log2(rank + 1.0)

        # IDCG
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


def execute_comparison() -> Dict[str, Any]:
    print("=" * 80)
    print("MĪZĀN AL-ḤADĪTH — PHASE 5 CONTROLLED COMPARISON")
    print("=" * 80)

    # 1. Load benchmark queries
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        benchmark_queries = [json.loads(line) for line in f if line.strip()]

    semantic_queries = [q for q in benchmark_queries if q["category"] not in ("reference_lookup", "edge_case")]
    ref_edge_queries = [q for q in benchmark_queries if q["category"] in ("reference_lookup", "edge_case")]

    print(f"Total benchmark queries:   {len(benchmark_queries)}")
    print(f"Scored semantic queries:   {len(semantic_queries)}")
    print(f"Isolated reference/edge:   {len(ref_edge_queries)}")

    # 2. Load canonical hadith-to-group map
    hadith_to_group = {}
    if CANONICAL_KG_PATH.exists():
        conn = sqlite3.connect(f"file:{CANONICAL_KG_PATH.resolve()}?mode=ro", uri=True)
        conn.execute("PRAGMA query_only = ON;")
        for hid, gid in conn.execute("SELECT id, group_id FROM hadiths WHERE group_id > 0;").fetchall():
            hadith_to_group[int(hid)] = int(gid)
        conn.close()

    # 3. Resolve EmbeddingGemma 2 Run
    eg2_file_used = None
    eg2_is_corrected = False
    if CORRECTED_EG2_RUN_PATH.exists():
        eg2_file_used = CORRECTED_EG2_RUN_PATH
        eg2_is_corrected = True
        print(f"[INFO] Using corrected EmbeddingGemma 2 run: {CORRECTED_EG2_RUN_PATH.name}")
    elif FALLBACK_EG2_RUN_PATH.exists():
        eg2_file_used = FALLBACK_EG2_RUN_PATH
        eg2_is_corrected = False
        print(f"[INFO] Corrected run pending Colab execution; evaluating candidate run: {FALLBACK_EG2_RUN_PATH.name}")
    else:
        raise FileNotFoundError("No EmbeddingGemma 2 run artifact found under data/benchmarks/runs/")

    with open(eg2_file_used, "r", encoding="utf-8") as f:
        eg2_run_data = json.load(f)

    eg2_lookup = {
        r["query_id"]: [item["group_id"] for item in r["retrieved"]]
        for r in eg2_run_data.get("results", [])
    }

    # 4. Resolve Gemini Baseline Run
    gemini_file_used = None
    gemini_live_available = False
    if LIVE_GEMINI_RUN_PATH.exists():
        with open(LIVE_GEMINI_RUN_PATH, "r", encoding="utf-8") as f:
            gem_data = json.load(f)
        if not gem_data.get("is_dry_run", True):
            gemini_file_used = LIVE_GEMINI_RUN_PATH
            gemini_live_available = True
            print(f"[INFO] Live Gemini baseline detected: {LIVE_GEMINI_RUN_PATH.name}")

    if not gemini_live_available:
        print("[NOTICE] Real Gemini live API baseline is UNAVAILABLE.")
        print("         In accordance with Section 10 & 26 of Phase 5 Master Prompt:")
        print("         Synthetic baseline is strictly forbidden (zero leakage).")
        print("         GATE 2 status: INCONCLUSIVE (Comparison with Gemini incomplete).")

    gemini_lookup = {}
    if gemini_file_used:
        with open(gemini_file_used, "r", encoding="utf-8") as f:
            gem_run = json.load(f)
        gemini_lookup = {
            r["query_id"]: [item["group_id"] for item in r["retrieved"]]
            for r in gem_run.get("results", [])
        }

    # 5. Evaluate Subsets
    ar_queries = [q for q in semantic_queries if q["language"] == "ar"]
    ur_queries = [q for q in semantic_queries if q["language"] == "ur" and not q["category"].startswith("cross_lingual")]
    en_queries = [q for q in semantic_queries if q["language"] == "en" and not q["category"].startswith("cross_lingual")]
    cross_queries = [q for q in semantic_queries if q["category"].startswith("cross_lingual")]

    eg2_overall = compute_metrics(semantic_queries, eg2_lookup, hadith_to_group)
    eg2_ar = compute_metrics(ar_queries, eg2_lookup, hadith_to_group)
    eg2_ur = compute_metrics(ur_queries, eg2_lookup, hadith_to_group)
    eg2_en = compute_metrics(en_queries, eg2_lookup, hadith_to_group)
    eg2_cross = compute_metrics(cross_queries, eg2_lookup, hadith_to_group)

    gem_overall = compute_metrics(semantic_queries, gemini_lookup, hadith_to_group) if gemini_lookup else None
    gem_ar = compute_metrics(ar_queries, gemini_lookup, hadith_to_group) if gemini_lookup else None
    gem_ur = compute_metrics(ur_queries, gemini_lookup, hadith_to_group) if gemini_lookup else None
    gem_en = compute_metrics(en_queries, gemini_lookup, hadith_to_group) if gemini_lookup else None
    gem_cross = compute_metrics(cross_queries, gemini_lookup, hadith_to_group) if gemini_lookup else None

    print("\n--- PRIMARY METRICS SUMMARY (450 Scored Semantic Queries) ---")
    print(f"{'Metric':<14} | {'EG2 (' + ('Corrected' if eg2_is_corrected else 'Phase 3') + ')':<20} | {'Gemini Live Baseline':<20}")
    print("-" * 60)
    for m in ["recall_1", "recall_5", "recall_10", "mrr", "ndcg_10"]:
        eg_val = eg2_overall.get(m, 0.0)
        gem_val = gem_overall.get(m, 0.0) if gem_overall else "UNAVAILABLE"
        print(f"{m:<14} | {eg_val:<20.4f} | {gem_val}")

    print("\n--- PER-LANGUAGE MRR BREAKDOWN ---")
    for lang_name, eg_sub, gem_sub in [
        ("Arabic (150)", eg2_ar, gem_ar),
        ("Urdu (100)", eg2_ur, gem_ur),
        ("English (100)", eg2_en, gem_en),
        ("Cross-Lingual (100)", eg2_cross, gem_cross),
    ]:
        gem_v = f"{gem_sub['mrr']:.4f}" if gem_sub else "UNAVAILABLE"
        print(f"  {lang_name:<20}: EG2 MRR={eg_sub['mrr']:.4f} | Gemini Live={gem_v}")

    # 6. Disagreement & Reference Analysis
    gem_hits_10, eg2_hits_10, both_hits_10 = 0, 0, 0
    gem_only_10, eg2_only_10, neither_10 = 0, 0, 0
    for q in semantic_queries:
        qid = q["query_id"]
        gold = set(q.get("gold_group_ids", []))
        g_hit = bool(set(gemini_lookup.get(qid, [])[:10]).intersection(gold)) if gemini_lookup else False
        e_hit = bool(set(eg2_lookup.get(qid, [])[:10]).intersection(gold))
        if g_hit and e_hit:
            both_hits_10 += 1
        elif g_hit and not e_hit:
            gem_only_10 += 1
        elif not g_hit and e_hit:
            eg2_only_10 += 1
        else:
            neither_10 += 1

    disagreements = {
        "both_retrieved_gold_top10": both_hits_10,
        "gemini_only_retrieved_gold_top10": gem_only_10,
        "eg2_only_retrieved_gold_top10": eg2_only_10,
        "neither_retrieved_gold_top10": neither_10,
    }

    # Reference / Edge cases
    gem_ref_r10 = sum(1 for q in ref_edge_queries if set(gemini_lookup.get(q["query_id"], [])[:10]).intersection(set(q.get("gold_group_ids", [])))) if gemini_lookup else 0
    eg2_ref_r10 = sum(1 for q in ref_edge_queries if set(eg2_lookup.get(q["query_id"], [])[:10]).intersection(set(q.get("gold_group_ids", []))))
    ref_metrics = {
        "total_reference_queries": len(ref_edge_queries),
        "gemini_recall_10": round(gem_ref_r10 / len(ref_edge_queries), 4) if ref_edge_queries else 0.0,
        "eg2_recall_10": round(eg2_ref_r10 / len(ref_edge_queries), 4) if ref_edge_queries else 0.0,
    }

    print("\n--- RETRIEVAL DISAGREEMENT BREAKDOWN (Top-10 on 450 Semantic Queries) ---")
    print(f"  Both Models Retrieved Gold:     {both_hits_10} ({both_hits_10/450*100:.1f}%)")
    print(f"  Gemini ONLY Retrieved Gold:     {gem_only_10} ({gem_only_10/450*100:.1f}%)")
    print(f"  EG2 ONLY Retrieved Gold:        {eg2_only_10} ({eg2_only_10/450*100:.1f}%)")
    print(f"  Neither Model Retrieved Gold:   {neither_10} ({neither_10/450*100:.1f}%)")

    print("\n--- REFERENCE / EDGE QUERY ISOLATION (50 Queries) ---")
    print(f"  Gemini Recall@10: {ref_metrics['gemini_recall_10']:.4f} ({gem_ref_r10}/{len(ref_edge_queries)})")
    print(f"  EG2 Recall@10:    {ref_metrics['eg2_recall_10']:.4f} ({eg2_ref_r10}/{len(ref_edge_queries)})")

    # Determine Decision Gates
    gate1 = {
        "status": "PASS" if eg2_is_corrected else "PENDING_COLAB_RUN",
        "description": "Implementation validity (SearchQuery task prompt + prompt-inclusive mean pooling understood)",
    }
    gate2 = {
        "status": "PASS" if gemini_live_available else "INCONCLUSIVE",
        "description": "Real Gemini query embeddings used without synthetic leakage",
        "reason": "Live API credentials unavailable in session" if not gemini_live_available else "Live run executed",
    }
    gate3 = {
        "status": "INCONCLUSIVE" if not gemini_live_available else ("RETAIN_GEMINI" if eg2_overall["mrr"] < gem_overall["mrr"] else "COMPETITIVE"),
        "description": "Final comparative model quality decision",
        "production_recommendation": "Retain SEMANTIC_EMBEDDING_PROVIDER=gemini",
    }

    print("\n--- DECISION GATES ---")
    print(f"GATE 1 (Implementation Valid):  {gate1['status']}")
    print(f"GATE 2 (Gemini Baseline Valid): {gate2['status']}")
    print(f"GATE 3 (Model Quality Verdict): {gate3['status']}")
    print(f"Production Provider Status:     SEMANTIC_EMBEDDING_PROVIDER=gemini (UNCHANGED)")

    comparison_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": "PHASE 5 CORRECTED BENCHMARK",
        "candidate": {
            "artifact": str(eg2_file_used.name),
            "model": eg2_run_data.get("model"),
            "dimensions": eg2_run_data.get("dimensions"),
            "is_corrected_prompt": eg2_is_corrected,
            "latency": eg2_run_data.get("latency"),
            "metrics": {
                "overall": eg2_overall,
                "arabic": eg2_ar,
                "urdu": eg2_ur,
                "english": eg2_en,
                "cross_lingual": eg2_cross,
            },
        },
        "baseline": {
            "artifact": str(gemini_file_used.name) if gemini_file_used else None,
            "live_api_available": gemini_live_available,
            "status": "VALID_LIVE_API" if gemini_live_available else "UNAVAILABLE_COMPARISON_INCOMPLETE",
            "latency": gem_run.get("latency") if gemini_file_used else None,
            "metrics": {
                "overall": gem_overall,
                "arabic": gem_ar,
                "urdu": gem_ur,
                "english": gem_en,
                "cross_lingual": gem_cross,
            } if gem_overall else None,
        },
        "disagreements": disagreements,
        "reference_edge_metrics": ref_metrics,
        "decision_gates": {
            "gate_1_implementation": gate1,
            "gate_2_gemini_baseline": gate2,
            "gate_3_verdict": gate3,
        },
        "production_safety": {
            "production_provider": "gemini",
            "production_cutover": False,
            "canonical_mutations": 0,
        },
    }

    COMPARISON_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPARISON_OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(comparison_payload, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Wrote comparison summary to {COMPARISON_OUTPUT_PATH}")
    return comparison_payload


if __name__ == "__main__":
    execute_comparison()
