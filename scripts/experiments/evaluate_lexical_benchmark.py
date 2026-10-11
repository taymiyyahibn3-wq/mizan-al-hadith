"""
MĪZĀN AL-ḤADĪTH — Phase 6 Forensic Lexical & Hybrid Fusion Evaluator
READ-ONLY Experimental Script.
Evaluates:
  1. Pure Lexical / FTS Retrieval on the 500 benchmark queries
  2. Pure Gemini Live Semantic Retrieval
  3. Hybrid Fusion v2 (Reciprocal Rank Fusion - RRF)
  4. Recovery rate on the 147 "Neither" queries
"""

from __future__ import annotations
import json
import math
import re
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(r"c:\Users\taymi\discord-hadith-bot")
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
KG_DB_PATH = REPO_ROOT / "data" / "hadith-kg.db"
SEARCH_INDEX_DB_PATH = REPO_ROOT / "data" / "hadith-search-index.db"
ENGLISH_FTS_DB_PATH = REPO_ROOT / "data" / "english_translation_fts.db"
NUMBERING_DB_PATH = REPO_ROOT / "data" / "hadith_numbering.db"
GEMINI_RUN_PATH = REPO_ROOT / "data" / "benchmarks" / "runs" / "gemini_live_baseline_run_v1.json"
OUTPUT_REPORT_PATH = REPO_ROOT / "data" / "benchmarks" / "phase6" / "hybrid_retrieval_v2_simulation.json"

# Arabic normalization
def normalize_arabic(text: str) -> str:
    if not text:
        return ""
    t = re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED]", "", text) # Tashkeel
    t = re.sub(r"[إأٱآ]", "ا", t)
    t = t.replace("ة", "ه").replace("ى", "ي")
    t = re.sub(r"[^\w\s]", " ", t)
    return " ".join(t.split()).strip()

# 1. Load canonical hadith -> group_id mapping
print("[INFO] Loading canonical hadith -> group_id mapping...")
hadith_to_group: Dict[int, int] = {}
conn_kg = sqlite3.connect(f"file:{KG_DB_PATH}?mode=ro", uri=True)
conn_kg.execute("PRAGMA query_only = ON;")
for hid, gid in conn_kg.execute("SELECT id, group_id FROM hadiths WHERE group_id > 0;").fetchall():
    hadith_to_group[int(hid)] = int(gid)
conn_kg.close()
print(f"[INFO] Loaded {len(hadith_to_group)} hadiths mapped to meaning groups.")

# 2. Reference Resolver (Book + Scheme + Number)
COLLECTION_PATTERNS = {
    1: r"(?:sahih\s+al[- ]bukhari|sahih\s+bukhari|bukhari|صحيح\s+البخاري|البخاري)",
    2: r"(?:sahih\s+muslim|muslim|صحيح\s+مسلم|مسلم)",
    3: r"(?:jami[']?\s+al[- ]tirmidhi|tirmidhi|جامع\s+الترمذي|الترمذي)",
    4: r"(?:sunan\s+abi\s+dawud|abu\s+dawud|سنن\s+أ?بي\s+داود|أ?بو\s+داود)",
    5: r"(?:sunan\s+an[- ]nasai|nasai|سنن\s+النسائي|النسائي)",
    6: r"(?:sunan\s+ibn\s+majah|ibn\s+majah|سنن\s+ابن\s+ماجه|ابن\s+ماجه)",
}

def resolve_reference_query(query_text: str) -> Optional[int]:
    """Resolves queries like 'Bukhari 1', 'Muslim 1907' to a group_id."""
    clean = query_text.strip().lower()
    for book_id, pat in COLLECTION_PATTERNS.items():
        m = re.search(rf"\b{pat}\b\s*(?:#|no\.?\s*)?(\d+)", clean, re.IGNORECASE)
        if m:
            num = int(m.group(1))
            conn_kg = sqlite3.connect(f"file:{KG_DB_PATH}?mode=ro", uri=True)
            row = conn_kg.execute(
                "SELECT id, group_id FROM hadiths WHERE book_id = ? AND no_inbook = ? LIMIT 1;",
                (book_id, num),
            ).fetchone()
            conn_kg.close()
            if row and row[1]:
                return row[1]
    return None

# 3. Lexical Search Executors
def search_arabic_lexical(query_text: str, top_k: int = 50) -> List[int]:
    """Queries hadith_fts and aggregates matching hadiths into unique meaning groups."""
    norm_q = normalize_arabic(query_text)
    tokens = [t for t in norm_q.split() if len(t) >= 2]
    if not tokens:
        return []

    # FTS query
    fts_expr = " AND ".join(f'"{t}"*' for t in tokens[:5])
    conn_fts = sqlite3.connect(f"file:{SEARCH_INDEX_DB_PATH}?mode=ro", uri=True)
    try:
        rows = conn_fts.execute(
            "SELECT rowid FROM hadith_fts WHERE hadith_fts MATCH ? LIMIT 200;",
            (fts_expr,),
        ).fetchall()
    except Exception:
        # Fallback to phrase or individual tokens
        try:
            fts_expr_or = " OR ".join(f'"{t}"*' for t in tokens[:3])
            rows = conn_fts.execute(
                "SELECT rowid FROM hadith_fts WHERE hadith_fts MATCH ? LIMIT 200;",
                (fts_expr_or,),
            ).fetchall()
        except Exception:
            rows = []
    finally:
        conn_fts.close()

    # Aggregate hadiths by meaning group with frequency-based rank
    group_scores: Dict[int, float] = defaultdict(float)
    for rank_idx, r in enumerate(rows, start=1):
        hid = r[0]
        gid = hadith_to_group.get(hid)
        if gid:
            group_scores[gid] += 1.0 / math.sqrt(rank_idx)

    sorted_groups = sorted(group_scores.items(), key=lambda x: x[1], reverse=True)
    return [gid for gid, _ in sorted_groups[:top_k]]

def search_english_lexical(query_text: str, top_k: int = 50) -> List[int]:
    """Queries english_fts and aggregates matching hadiths into unique meaning groups."""
    clean_q = re.sub(r"[^\w\s]", " ", query_text).strip()
    stopwords = {"hadith", "about", "what", "where", "which", "who", "the", "a", "an", "is", "are", "tell", "show"}
    tokens = [t.lower() for t in clean_q.split() if len(t) > 2 and t.lower() not in stopwords]
    if not tokens:
        tokens = [t.lower() for t in clean_q.split() if len(t) > 2]
    if not tokens:
        return []

    fts_expr = " AND ".join(f'"{t}"*' for t in tokens[:6])
    conn_en = sqlite3.connect(f"file:{ENGLISH_FTS_DB_PATH}?mode=ro", uri=True)
    try:
        rows = conn_en.execute(
            """
            SELECT t.hadith_id, rank
            FROM english_fts f
            JOIN english_translations t ON t.id = f.rowid
            WHERE english_fts MATCH ?
            ORDER BY rank
            LIMIT 200;
            """,
            (fts_expr,),
        ).fetchall()
    except Exception:
        try:
            fts_expr_or = " OR ".join(f'"{t}"*' for t in tokens[:4])
            rows = conn_en.execute(
                """
                SELECT t.hadith_id, rank
                FROM english_fts f
                JOIN english_translations t ON t.id = f.rowid
                WHERE english_fts MATCH ?
                ORDER BY rank
                LIMIT 200;
                """,
                (fts_expr_or,),
            ).fetchall()
        except Exception:
            rows = []
    finally:
        conn_en.close()

    group_scores: Dict[int, float] = defaultdict(float)
    for rank_idx, (hid, rank_val) in enumerate(rows, start=1):
        gid = hadith_to_group.get(hid)
        if gid:
            group_scores[gid] += 1.0 / math.sqrt(rank_idx)

    sorted_groups = sorted(group_scores.items(), key=lambda x: x[1], reverse=True)
    return [gid for gid, _ in sorted_groups[:top_k]]

def search_lexical_router(q: Dict[str, Any], top_k: int = 50) -> List[int]:
    """Routes query to appropriate lexical subsystem."""
    q_text = q["query"]
    lang = q["language"]
    cat = q["category"]

    # 1. Reference check
    if cat in ("reference_lookup", "edge_case") or any(k in q_text.lower() for k in ["bukhari", "muslim", "tirmidhi"]):
        ref_gid = resolve_reference_query(q_text)
        if ref_gid:
            # Put resolved group at rank 1, fill remainder with text search
            rest = search_arabic_lexical(q_text, top_k=top_k) if lang == "ar" else search_english_lexical(q_text, top_k=top_k)
            return [ref_gid] + [g for g in rest if g != ref_gid][:top_k - 1]

    # 2. English text
    if lang == "en" or cat.endswith("english"):
        return search_english_lexical(q_text, top_k=top_k)

    # 3. Arabic & Urdu text (search Arabic FTS)
    return search_arabic_lexical(q_text, top_k=top_k)

# 4. Metric Computation
def compute_metrics(queries: List[Dict[str, Any]], run_lookup: Dict[str, List[int]]) -> Dict[str, float]:
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

# 5. Execute Evaluation
print("\n[INFO] Loading benchmark queries...")
bench_queries = [json.loads(l) for l in open(BENCHMARK_PATH, encoding="utf-8") if l.strip()]
semantic_queries = [q for q in bench_queries if q["category"] not in ("reference_lookup", "edge_case")]
ref_queries = [q for q in bench_queries if q["category"] in ("reference_lookup", "edge_case")]

print(f"[INFO] Executing Lexical Search across all {len(bench_queries)} benchmark queries...")
lexical_lookup: Dict[str, List[int]] = {}
t0_lex = time.perf_counter()
for q in bench_queries:
    lexical_lookup[q["query_id"]] = search_lexical_router(q, top_k=50)
dur_lex = time.perf_counter() - t0_lex
print(f"[INFO] Lexical search complete in {dur_lex:.2f} s ({len(bench_queries)/dur_lex:.1f} QPS).")

# Load Gemini Live Baseline
gem_run = json.load(open(GEMINI_RUN_PATH, encoding="utf-8"))
gemini_lookup = {r["query_id"]: [item["group_id"] for item in r["retrieved"]] for r in gem_run.get("results", [])}

# 6. Hybrid Fusion Simulator (RRF)
def reciprocal_rank_fusion(
    run_a: Dict[str, List[int]],
    run_b: Dict[str, List[int]],
    w_a: float = 1.0,
    w_b: float = 1.0,
    k: int = 60,
    top_k: int = 50,
) -> Dict[str, List[int]]:
    fused: Dict[str, List[int]] = {}
    all_qids = set(run_a.keys()) | set(run_b.keys())
    for qid in all_qids:
        scores: Dict[int, float] = defaultdict(float)
        list_a = run_a.get(qid, [])
        list_b = run_b.get(qid, [])
        for rank, doc in enumerate(list_a, start=1):
            scores[doc] += w_a / (k + rank)
        for rank, doc in enumerate(list_b, start=1):
            scores[doc] += w_b / (k + rank)
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        fused[qid] = [doc for doc, _ in sorted_docs[:top_k]]
    return fused

print("[INFO] Simulating Hybrid Fusion strategies...")
rrf_equal = reciprocal_rank_fusion(gemini_lookup, lexical_lookup, w_a=1.0, w_b=1.0, k=60)
rrf_gem_favored = reciprocal_rank_fusion(gemini_lookup, lexical_lookup, w_a=1.0, w_b=0.4, k=60)
rrf_lex_favored = reciprocal_rank_fusion(gemini_lookup, lexical_lookup, w_a=0.4, w_b=1.0, k=60)

# 7. Metrics Summaries
print("\n" + "=" * 80)
print("PHASE 6 RETRIEVAL PERFORMANCE MATRIX (450 Scored Semantic Queries)")
print("=" * 80)
print(f"{'Method / Configuration':<32} | {'Recall@1':<9} | {'Recall@5':<9} | {'Recall@10':<9} | {'MRR':<8} | {'nDCG@10':<8}")
print("-" * 80)

met_lex = compute_metrics(semantic_queries, lexical_lookup)
met_gem = compute_metrics(semantic_queries, gemini_lookup)
met_rrf_eq = compute_metrics(semantic_queries, rrf_equal)
met_rrf_gem = compute_metrics(semantic_queries, rrf_gem_favored)
met_rrf_lex = compute_metrics(semantic_queries, rrf_lex_favored)

for name, m in [
    ("1. Pure Lexical / FTS", met_lex),
    ("2. Pure Gemini Live (Baseline)", met_gem),
    ("3. Hybrid RRF (Equal w=1.0/1.0)", met_rrf_eq),
    ("4. Hybrid RRF (Gemini-Weighted 1.0/0.4)", met_rrf_gem),
    ("5. Hybrid RRF (Lexical-Weighted 0.4/1.0)", met_rrf_lex),
]:
    print(f"{name:<32} | {m['recall_1']:<9.4f} | {m['recall_5']:<9.4f} | {m['recall_10']:<9.4f} | {m['mrr']:<8.4f} | {m['ndcg_10']:<8.4f}")

# 8. Reference / Edge Queries Matrix
print("\n" + "=" * 80)
print("REFERENCE / EDGE CASE RETRIEVAL (50 Isolated Queries)")
print("=" * 80)
ref_lex = compute_metrics(ref_queries, lexical_lookup)
ref_gem = compute_metrics(ref_queries, gemini_lookup)
ref_rrf = compute_metrics(ref_queries, rrf_gem_favored)
print(f"Pure Lexical Recall@10:       {ref_lex['recall_10']:.4f} (MRR: {ref_lex['mrr']:.4f})")
print(f"Pure Gemini Recall@10:        {ref_gem['recall_10']:.4f} (MRR: {ref_gem['mrr']:.4f})")
print(f"Hybrid RRF Recall@10:         {ref_rrf['recall_10']:.4f} (MRR: {ref_rrf['mrr']:.4f})")

# 9. Language Breakdown for Hybrid RRF (Gemini-Weighted)
print("\n" + "=" * 80)
print("PER-LANGUAGE COMPARISON: GEMINI VS HYBRID RRF (1.0 / 0.4)")
print("=" * 80)
for lang_name, filter_fn in [
    ("Arabic Semantic (150)", lambda q: q["language"] == "ar"),
    ("Urdu Semantic (100)", lambda q: q["language"] == "ur" and not q["category"].startswith("cross_lingual")),
    ("English Semantic (100)", lambda q: q["language"] == "en" and not q["category"].startswith("cross_lingual")),
    ("Cross-Lingual (100)", lambda q: q["category"].startswith("cross_lingual")),
]:
    sub = [q for q in semantic_queries if filter_fn(q)]
    sub_lex = compute_metrics(sub, lexical_lookup)
    sub_gem = compute_metrics(sub, gemini_lookup)
    sub_hyb = compute_metrics(sub, rrf_gem_favored)
    print(f"  {lang_name:<25}: Lex MRR={sub_lex['mrr']:.4f} | Gem MRR={sub_gem['mrr']:.4f} | Hybrid MRR={sub_hyb['mrr']:.4f} (R@10: {sub_hyb['recall_10']:.4f})")

# 10. Recovery of the 147 "Neither" Cases
print("\n" + "=" * 80)
print("RECOVERY AUDIT: THE 147 'NEITHER' CASES")
print("=" * 80)
# Group D: neither gemini nor eg2 in top 10
eg2_run = json.load(open(REPO_ROOT / "data" / "benchmarks" / "runs" / "embeddinggemma2_candidate_run.json", encoding="utf-8"))
eg2_lookup = {r["query_id"]: [item["group_id"] for item in r["retrieved"]] for r in eg2_run.get("results", [])}

neither_qids = []
for q in semantic_queries:
    qid = q["query_id"]
    gold = set(q["gold_group_ids"])
    g_hit = bool(set(gemini_lookup.get(qid, [])[:10]).intersection(gold))
    e_hit = bool(set(eg2_lookup.get(qid, [])[:10]).intersection(gold))
    if not g_hit and not e_hit:
        neither_qids.append(q)

print(f"Total Neither Queries: {len(neither_qids)}")
lex_recovered_10 = 0
hyb_recovered_10 = 0
recovered_examples = []

for q in neither_qids:
    qid = q["query_id"]
    gold = set(q["gold_group_ids"])
    lex_ret = set(lexical_lookup.get(qid, [])[:10])
    hyb_ret = set(rrf_gem_favored.get(qid, [])[:10])

    l_hit = bool(lex_ret.intersection(gold))
    h_hit = bool(hyb_ret.intersection(gold))

    if l_hit:
        lex_recovered_10 += 1
    if h_hit:
        hyb_recovered_10 += 1
        recovered_examples.append((q, [gid for gid in rrf_gem_favored[qid][:5]]))

print(f"Lexical ALONE recovered into Top-10: {lex_recovered_10} / {len(neither_qids)} ({lex_recovered_10/len(neither_qids)*100:.1f}%)")
print(f"Hybrid RRF recovered into Top-10:   {hyb_recovered_10} / {len(neither_qids)} ({hyb_recovered_10/len(neither_qids)*100:.1f}%)")

# Save results
out_payload = {
    "evaluation_timestamp": time.time(),
    "benchmark": "embeddinggemma2_benchmark_v1.jsonl",
    "total_queries": len(bench_queries),
    "semantic_queries": len(semantic_queries),
    "reference_queries": len(ref_queries),
    "metrics": {
        "pure_lexical": met_lex,
        "pure_gemini_live": met_gem,
        "hybrid_rrf_equal": met_rrf_eq,
        "hybrid_rrf_gemini_weighted": met_rrf_gem,
        "hybrid_rrf_lexical_weighted": met_rrf_lex,
    },
    "reference_metrics": {
        "lexical": ref_lex,
        "gemini": ref_gem,
        "hybrid": ref_rrf,
    },
    "neither_recovery": {
        "total_neither": len(neither_qids),
        "lexical_recovered_top10": lex_recovered_10,
        "hybrid_recovered_top10": hyb_recovered_10,
    }
}

OUTPUT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
    json.dump(out_payload, f, indent=2)

print(f"\n[SUCCESS] Wrote experimental simulation payload to {OUTPUT_REPORT_PATH}")
