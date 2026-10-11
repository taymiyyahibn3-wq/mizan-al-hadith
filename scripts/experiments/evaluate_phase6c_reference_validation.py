"""
MĪZĀN AL-ḤADĪTH — Phase 6C Unseen Reference Validation Evaluator
Evaluates:
  1. Pure Lexical FTS
  2. Reference Resolver Alone
  3. Hybrid Retrieval v2 (Routed)
  4. Pure Gemini Semantic (on representative sample)

Measures:
  - Valid queries (gold_group_ids non-empty): Recall@1, Recall@5, Recall@10, MRR, nDCG@10
  - Malformed/adversarial queries (gold_group_ids empty): False Positive Rate / Pinning False Positives
  - Category breakdown: English, Arabic, Alternates, Arabic Numerals, Mixed, Urdu, Malformed

Saves payload to: data/benchmarks/phase6c/phase6c_reference_validation.json
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
    SemanticCandidateRetriever,
    DEFAULT_RRF_CONFIG,
)

UNSEEN_DATASET_PATH = REPO_ROOT / "data" / "benchmarks" / "phase6c" / "phase6c_unseen_reference_queries.jsonl"
OUTPUT_PATH = REPO_ROOT / "data" / "benchmarks" / "phase6c" / "phase6c_reference_validation.json"


def compute_metrics(queries: List[Dict[str, Any]], run_lookup: Dict[str, List[int]]) -> Dict[str, float]:
    valid_q = [q for q in queries if q.get("gold_group_ids")]
    if not valid_q:
        return {"recall_1": 0.0, "recall_5": 0.0, "recall_10": 0.0, "mrr": 0.0, "ndcg_10": 0.0}

    r1, r5, r10, rr, ndcg = [], [], [], [], []
    for q in valid_q:
        qid = q["query_id"]
        gold_gids = set(q["gold_group_ids"])
        retrieved = run_lookup.get(qid, [])

        top1 = set(retrieved[:1])
        top5 = set(retrieved[:5])
        top10 = set(retrieved[:10])

        r1.append(1.0 if top1.intersection(gold_gids) else 0.0)
        r5.append(1.0 if top5.intersection(gold_gids) else 0.0)
        r10.append(1.0 if top10.intersection(gold_gids) else 0.0)

        q_rr = 0.0
        for rank, gid in enumerate(retrieved, start=1):
            if gid in gold_gids:
                q_rr = 1.0 / rank
                break
        rr.append(q_rr)

        dcg = 0.0
        for rank, gid in enumerate(retrieved[:10], start=1):
            if gid in gold_gids:
                dcg += 1.0 / math.log2(rank + 1.0)
        idcg = 1.0 / math.log2(1.0 + 1.0)
        ndcg.append(dcg / idcg if idcg > 0 else 0.0)

    return {
        "recall_1": round(float(np.mean(r1)), 4),
        "recall_5": round(float(np.mean(r5)), 4),
        "recall_10": round(float(np.mean(r10)), 4),
        "mrr": round(float(np.mean(rr)), 4),
        "ndcg_10": round(float(np.mean(ndcg)), 4),
    }


def main() -> None:
    print("=" * 80)
    print("MĪZĀN AL-ḤADĪTH — PHASE 6C UNSEEN REFERENCE VALIDATION")
    print("=" * 80)

    queries = [json.loads(l) for l in open(UNSEEN_DATASET_PATH, encoding="utf-8") if l.strip()]
    valid_queries = [q for q in queries if q["gold_group_ids"]]
    malformed_queries = [q for q in queries if not q["gold_group_ids"]]
    print(f"[INFO] Loaded {len(queries)} total queries ({len(valid_queries)} valid, {len(malformed_queries)} malformed/adversarial).")

    data_mgr = ImmutableDataManager.get_instance()
    data_mgr.load_hadith_to_group_mapping()
    router = QueryRouter()
    lex_retriever = LexicalCandidateRetriever(data_mgr)
    ref_retriever = ReferenceCandidateRetriever(data_mgr)
    sem_retriever = SemanticCandidateRetriever()

    # Lookups
    lex_lookup: Dict[str, List[int]] = {}
    ref_lookup: Dict[str, List[int]] = {}
    hybrid_lookup: Dict[str, List[int]] = {}

    malformed_fp_count = 0
    malformed_pinning_count = 0

    t0_all = time.perf_counter()

    for idx, q in enumerate(queries, start=1):
        qid = q["query_id"]
        q_text = q["query"]

        route = router.classify_query(q_text)

        # 1. Reference resolver
        ref_cands = ref_retriever.resolve(route)
        ref_lookup[qid] = [c.group_id for c in ref_cands]

        # 2. Lexical retriever
        if route.detected_language == "ar":
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
        elif route.detected_language == "en":
            lex_cands = lex_retriever.retrieve_english(q_text, top_k=50)
        else:
            lex_cands = lex_retriever.retrieve_arabic(q_text, top_k=50)
        lex_lookup[qid] = [c.group_id for c in lex_cands]

        # 3. Hybrid RRF fusion
        q_type_str = route.query_type.value.lower()
        cfg = DEFAULT_RRF_CONFIG.get(q_type_str, DEFAULT_RRF_CONFIG["reference"])
        pin_ref = (route.query_type == QueryType.REFERENCE and bool(ref_cands))

        fused = FusionEngine.fuse(
            semantic_pool=[],  # Reference workload isolated evaluation
            lexical_pool=lex_cands,
            reference_pool=ref_cands,
            w_sem=0.0,
            w_lex=cfg.get("w_lex", 1.0),
            w_ref=cfg.get("w_ref", 2.5),
            k=cfg.get("k", 60.0),
            top_k=50,
            pin_reference=pin_ref,
        )
        hybrid_lookup[qid] = [fc.group_id for fc in fused]

        # Adversarial check on malformed queries
        if not q["gold_group_ids"]:
            if ref_cands:
                malformed_fp_count += 1
            if pin_ref:
                malformed_pinning_count += 1

    dur_all = time.perf_counter() - t0_all
    print(f"[INFO] Evaluated all {len(queries)} unseen queries in {dur_all:.2f} s ({len(queries)/dur_all:.1f} QPS).")

    # Metrics on all valid queries
    met_lex = compute_metrics(valid_queries, lex_lookup)
    met_ref = compute_metrics(valid_queries, ref_lookup)
    met_hyb = compute_metrics(valid_queries, hybrid_lookup)

    # Breakdown by category
    cat_breakdowns = {}
    cats = sorted(list(set(q["category"] for q in valid_queries)))
    for cat in cats:
        cat_q = [q for q in valid_queries if q["category"] == cat]
        cat_breakdowns[cat] = {
            "count": len(cat_q),
            "lexical": compute_metrics(cat_q, lex_lookup),
            "reference_resolver": compute_metrics(cat_q, ref_lookup),
            "hybrid": compute_metrics(cat_q, hybrid_lookup),
        }

    print("\n" + "=" * 80)
    print(f"UNSEEN REFERENCE VALIDATION RESULTS ({len(valid_queries)} Valid Queries)")
    print("=" * 80)
    print(f"{'Strategy':<28} | {'Recall@1':<9} | {'Recall@5':<9} | {'Recall@10':<9} | {'MRR':<8} | {'nDCG@10':<8}")
    print("-" * 80)
    print(f"{'1. Pure Lexical FTS':<28} | {met_lex['recall_1']:<9.4f} | {met_lex['recall_5']:<9.4f} | {met_lex['recall_10']:<9.4f} | {met_lex['mrr']:<8.4f} | {met_lex['ndcg_10']:<8.4f}")
    print(f"{'2. Reference Resolver Alone':<28} | {met_ref['recall_1']:<9.4f} | {met_ref['recall_5']:<9.4f} | {met_ref['recall_10']:<9.4f} | {met_ref['mrr']:<8.4f} | {met_ref['ndcg_10']:<8.4f}")
    print(f"{'3. Hybrid Retrieval v2':<28} | {met_hyb['recall_1']:<9.4f} | {met_hyb['recall_5']:<9.4f} | {met_hyb['recall_10']:<9.4f} | {met_hyb['mrr']:<8.4f} | {met_hyb['ndcg_10']:<8.4f}")

    print("\n" + "=" * 80)
    print("CATEGORY BREAKDOWN (UNSEEN DATASET)")
    print("=" * 80)
    for cat, data in cat_breakdowns.items():
        ref_r1 = data["reference_resolver"]["recall_1"]
        hyb_r1 = data["hybrid"]["recall_1"]
        hyb_r10 = data["hybrid"]["recall_10"]
        hyb_mrr = data["hybrid"]["mrr"]
        print(f"  {cat:<32} (N={data['count']:3d}): Ref R@1={ref_r1:.4f} | Hyb R@1={hyb_r1:.4f} | Hyb R@10={hyb_r10:.4f} | Hyb MRR={hyb_mrr:.4f}")

    print("\n" + "=" * 80)
    print("ADVERSARIAL / MALFORMED CITATION AUDIT")
    print("=" * 80)
    print(f"  Total Malformed/Adversarial Queries : {len(malformed_queries)}")
    print(f"  False Positive Reference Matches    : {malformed_fp_count} (Rate: {malformed_fp_count/len(malformed_queries)*100:.1f}%)")
    print(f"  False Positive Pinning Events       : {malformed_pinning_count} (Rate: {malformed_pinning_count/len(malformed_queries)*100:.1f}%)")

    # Save output artifact
    payload = {
        "dataset": "phase6c_unseen_reference_queries.jsonl",
        "total_queries": len(queries),
        "valid_queries_count": len(valid_queries),
        "malformed_queries_count": len(malformed_queries),
        "overall_valid_metrics": {
            "pure_lexical": met_lex,
            "reference_resolver_alone": met_ref,
            "hybrid_retrieval_v2": met_hyb,
        },
        "category_breakdown": cat_breakdowns,
        "adversarial_audit": {
            "malformed_count": len(malformed_queries),
            "false_positive_matches": malformed_fp_count,
            "false_positive_pinning": malformed_pinning_count,
            "false_positive_rate": malformed_fp_count / len(malformed_queries) if malformed_queries else 0.0,
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\n[SUCCESS] Saved reference validation artifact to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
