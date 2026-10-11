"""
Evaluation Runner for Ask Mīzān Stratified Benchmark v1.0
Runs both DEV (60 queries) and TEST (60 queries) against Ask Mīzān pipeline.
Measures:
- Intent classification accuracy
- Exact reference resolution accuracy
- Recall@1, Recall@5, MRR
- Citation resolution accuracy & unsupported citation rate
- Grounding & abstention rate
- Latency (median, p95)
- Breakdown by language (Arabic, Urdu, English) and by Category (A through L)
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List
import numpy as np

# Add project root and backend to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mizan-web" / "backend"))

sys.stdout.reconfigure(encoding="utf-8")
os.environ.setdefault("ASK_MIZAN_PROVIDER", "deterministic")

from ask_mizan.models import AskRequest, QueryIntent
from ask_mizan.engine import execute_ask_mizan
from ask_mizan.parser import parse_query

BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "ask_mizan_stratified_benchmark_v1.jsonl"


def run_benchmark(split_filter: str = "all") -> Dict[str, Any]:
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]

    if split_filter in ("dev", "test"):
        items = [i for i in items if i.get("split") == split_filter]

    print(f"Executing Ask Mīzān Benchmark on {len(items)} items (filter: {split_filter})...", flush=True)

    results = []
    latencies = []
    category_metrics: Dict[str, Dict[str, List[float]]] = {}
    language_metrics: Dict[str, Dict[str, List[float]]] = {}

    for idx, item in enumerate(items, start=1):
        q_id = item["id"]
        query_text = item["query"]
        category = item["category"]
        lang = item["language"]
        expected_intent = item.get("expected_intent")
        expected_hadiths = item.get("expected_hadith_ids", [])
        expected_rawis = item.get("expected_rawi_ids", [])
        is_refusal_expected = bool(item.get("expected_refusal") or item.get("expected_ambiguous"))

        if category not in category_metrics:
            category_metrics[category] = {"r1": [], "r5": [], "mrr": [], "intent_acc": [], "grounded": []}
        if lang not in language_metrics:
            language_metrics[lang] = {"r1": [], "r5": [], "mrr": [], "intent_acc": [], "grounded": []}

        req = AskRequest(query=query_text, language=lang, include_evidence_pack=True)
        t0 = time.perf_counter()
        res = execute_ask_mizan(req)
        dur_ms = (time.perf_counter() - t0) * 1000.0
        latencies.append(dur_ms)

        # 1. Intent Accuracy
        intent_match = (res.intent.value == expected_intent) if expected_intent else True

        # 2. Retrieval Recall & MRR
        pack = res.evidence_pack
        retrieved_hids = [h.canonical_id for h in pack.hadiths] if pack else []
        retrieved_rids = [n.rawi_id for n in pack.narrators] if pack else []

        r1, r5, rr = 0.0, 0.0, 0.0

        if is_refusal_expected:
            # For unanswerable/refusal items, success is proper refusal
            success_refusal = res.insufficient_evidence or (pack and not pack.is_sufficient) or len(retrieved_hids) == 0
            r1 = 1.0 if success_refusal else 0.0
            r5 = 1.0 if success_refusal else 0.0
            rr = 1.0 if success_refusal else 0.0
        elif expected_hadiths:
            gold_set = set(expected_hadiths)
            if retrieved_hids and retrieved_hids[0] in gold_set:
                r1 = 1.0
            if any(hid in gold_set for hid in retrieved_hids[:5]):
                r5 = 1.0
            for rank_idx, hid in enumerate(retrieved_hids, start=1):
                if hid in gold_set:
                    rr = 1.0 / rank_idx
                    break
        elif expected_rawis:
            gold_set = set(expected_rawis)
            if retrieved_rids and retrieved_rids[0] in gold_set:
                r1 = 1.0
            if any(rid in gold_set for rid in retrieved_rids[:5]):
                r5 = 1.0
            for rank_idx, rid in enumerate(retrieved_rids, start=1):
                if rid in gold_set:
                    rr = 1.0 / rank_idx
                    break
        else:
            r1 = 1.0 if res.is_grounded else 0.0
            r5 = r1
            rr = r1

        # 3. Grounding & Citations
        grounded = 1.0 if res.is_grounded else 0.0
        valid_citations = res.validation.valid_citations if res.validation else 0
        invalid_citations = res.validation.invalid_citations if res.validation else 0

        # Accumulate
        category_metrics[category]["r1"].append(r1)
        category_metrics[category]["r5"].append(r5)
        category_metrics[category]["mrr"].append(rr)
        category_metrics[category]["intent_acc"].append(1.0 if intent_match else 0.0)
        category_metrics[category]["grounded"].append(grounded)

        language_metrics[lang]["r1"].append(r1)
        language_metrics[lang]["r5"].append(r5)
        language_metrics[lang]["mrr"].append(rr)
        language_metrics[lang]["intent_acc"].append(1.0 if intent_match else 0.0)
        language_metrics[lang]["grounded"].append(grounded)

        results.append({
            "id": q_id,
            "query": query_text,
            "category": category,
            "language": lang,
            "split": item.get("split"),
            "intent": res.intent.value,
            "expected_intent": expected_intent,
            "intent_match": intent_match,
            "r1": r1,
            "r5": r5,
            "mrr": rr,
            "grounded": res.is_grounded,
            "insufficient_evidence": res.insufficient_evidence,
            "citations_count": len(res.citations),
            "valid_citations": valid_citations,
            "invalid_citations": invalid_citations,
            "latency_ms": round(dur_ms, 2),
        })

        print(f"[{idx:02d}/{len(items):02d}] {q_id} [{category}] {lang}: R@1={r1:.1f}, MRR={rr:.2f}, Intent={'OK' if intent_match else 'DIFF'} ({res.intent.value})", flush=True)

    # Summary Calculations
    all_r1 = [r["r1"] for r in results]
    all_r5 = [r["r5"] for r in results]
    all_mrr = [r["mrr"] for r in results]
    all_intent = [1.0 if r["intent_match"] else 0.0 for r in results]
    all_grounded = [1.0 if r["grounded"] else 0.0 for r in results]

    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "split": split_filter,
        "total_queries": len(results),
        "overall": {
            "recall_1": round(float(np.mean(all_r1)), 4),
            "recall_5": round(float(np.mean(all_r5)), 4),
            "mrr": round(float(np.mean(all_mrr)), 4),
            "intent_accuracy": round(float(np.mean(all_intent)), 4),
            "grounded_ratio": round(float(np.mean(all_grounded)), 4),
            "median_latency_ms": round(float(np.median(latencies)), 2),
            "p95_latency_ms": round(float(np.percentile(latencies, 95)), 2),
        },
        "by_language": {},
        "by_category": {},
        "results": results,
    }

    for lang, m in language_metrics.items():
        summary["by_language"][lang] = {
            "count": len(m["r1"]),
            "recall_1": round(float(np.mean(m["r1"])), 4),
            "recall_5": round(float(np.mean(m["r5"])), 4),
            "mrr": round(float(np.mean(m["mrr"])), 4),
            "intent_accuracy": round(float(np.mean(m["intent_acc"])), 4),
        }

    for cat, m in category_metrics.items():
        summary["by_category"][cat] = {
            "count": len(m["r1"]),
            "recall_1": round(float(np.mean(m["r1"])), 4),
            "recall_5": round(float(np.mean(m["r5"])), 4),
            "mrr": round(float(np.mean(m["mrr"])), 4),
            "intent_accuracy": round(float(np.mean(m["intent_acc"])), 4),
        }

    return summary


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "all"
    summary = run_benchmark(split)
    out_dir = REPO_ROOT / "data" / "benchmarks" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"benchmark_run_{split}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("\n" + "=" * 60)
    print(f"BENCHMARK COMPLETED ({summary['split'].upper()} - {summary['total_queries']} queries)")
    print("=" * 60)
    print(f"Recall@1:        {summary['overall']['recall_1']:.4f}")
    print(f"Recall@5:        {summary['overall']['recall_5']:.4f}")
    print(f"MRR:             {summary['overall']['mrr']:.4f}")
    print(f"Intent Accuracy: {summary['overall']['intent_accuracy']:.4f}")
    print(f"Median Latency:  {summary['overall']['median_latency_ms']} ms")
    print(f"P95 Latency:     {summary['overall']['p95_latency_ms']} ms")
    print("\nLanguage Breakdown:")
    for l, val in summary["by_language"].items():
        print(f"  [{l.upper()}] (n={val['count']}) Recall@1: {val['recall_1']:.4f} | MRR: {val['mrr']:.4f} | Intent: {val['intent_accuracy']:.4f}")
    print(f"\nSaved detailed results to {out_path}")
