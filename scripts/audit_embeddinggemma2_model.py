"""
MĪZĀN AL-ḤADĪTH — EmbeddingGemma 2 Model & Tokenization Audit (Phase 4)
Performs forensic audit of:
  1. Model configuration, architecture, pooling, normalization, and precision.
  2. Prompting configuration and exact text steering (Document vs SearchQuery).
  3. Tokenizer max sequence length, sliding window, and actual sequence length distribution across all 20,744 meaning groups.
  4. Tracing sample documents and queries with token counts and truncation behavior.
"""

from __future__ import annotations
import glob
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = REPO_ROOT / "data" / "meaning_groups_export.jsonl"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"


def find_hf_snapshot_dir() -> Path:
    user_home = Path.home()
    hub_dir = user_home / ".cache" / "huggingface" / "hub" / "models--google--embeddinggemma-2" / "snapshots"
    snapshots = list(hub_dir.glob("*"))
    if snapshots:
        return snapshots[0]
    raise FileNotFoundError("EmbeddingGemma 2 snapshot not found in HuggingFace cache.")


def audit_model_config() -> Dict[str, Any]:
    print("=" * 80)
    print("1. MODEL LOADING & ARCHITECTURE AUDIT")
    print("=" * 80)

    snap_dir = find_hf_snapshot_dir()
    print(f"Snapshot directory: {snap_dir}")

    config_json = json.load(open(snap_dir / "config.json", "r", encoding="utf-8"))
    st_config = json.load(open(snap_dir / "config_sentence_transformers.json", "r", encoding="utf-8"))
    modules_json = json.load(open(snap_dir / "modules.json", "r", encoding="utf-8"))
    tok_config = json.load(open(snap_dir / "tokenizer_config.json", "r", encoding="utf-8"))

    # Pooling config
    pooling_config = {}
    pool_file = snap_dir / "1_Pooling" / "config.json"
    if pool_file.exists():
        pooling_config = json.load(open(pool_file, "r", encoding="utf-8"))

    print("\n--- ARCHITECTURE & HYPERPARAMETERS ---")
    print(f"Model ID:              google/embeddinggemma-2")
    print(f"Architectures:         {config_json.get('architectures')}")
    print(f"Model Type:            {config_json.get('model_type')}")
    print(f"Torch Dtype in config: {config_json.get('torch_dtype')}")
    print(f"Hidden Size:           {config_json.get('hidden_size')}")
    print(f"Intermediate Size:     {config_json.get('intermediate_size')}")
    print(f"Num Hidden Layers:     {config_json.get('num_hidden_layers')}")
    print(f"Num Attention Heads:   {config_json.get('num_attention_heads')}")
    print(f"Num Key Value Heads:   {config_json.get('num_key_value_heads')}")
    print(f"Max Position Embed:    {config_json.get('max_position_embeddings')}")
    print(f"Sliding Window:        {config_json.get('sliding_window')}")
    print(f"Head Dim:              {config_json.get('head_dim')}")

    print("\n--- MODULES & PIPELINE ---")
    for mod in modules_json:
        print(f"  idx {mod.get('idx')}: {mod.get('name')} -> {mod.get('type')} ({mod.get('path')})")

    print("\n--- POOLING BEHAVIOR ---")
    print(f"Pooling Config:        {pooling_config}")

    print("\n--- TOKENIZER CONFIG ---")
    print(f"Tokenizer Class:       {tok_config.get('tokenizer_class')}")
    print(f"Model Max Length:      {tok_config.get('model_max_length')}")
    print(f"Padding Side:          {tok_config.get('padding_side')}")
    print(f"Truncation Side:       {tok_config.get('truncation_side')}")
    print(f"Add BOS Token:         {tok_config.get('add_bos_token')}")
    print(f"Add EOS Token:         {tok_config.get('add_eos_token')}")

    print("\n--- OFFICIAL SENTENCE TRANSFORMERS PROMPTS ---")
    prompts = st_config.get("prompts", {})
    for k, v in prompts.items():
        print(f"  '{k}': {repr(v)}")

    return {
        "config": config_json,
        "st_config": st_config,
        "modules": modules_json,
        "pooling": pooling_config,
        "tok_config": tok_config,
    }


def audit_tokenization_and_lengths() -> Dict[str, Any]:
    print("\n" + "=" * 80)
    print("2. TOKENIZATION & CORPUS SEQUENCE LENGTH AUDIT")
    print("=" * 80)

    from transformers import AutoTokenizer

    snap_dir = find_hf_snapshot_dir()
    print("Loading AutoTokenizer from snapshot...")
    tokenizer = AutoTokenizer.from_pretrained(str(snap_dir))

    print(f"Tokenizer vocab size: {len(tokenizer)}")
    print(f"Tokenizer model_max_length: {tokenizer.model_max_length}")

    # Inspect all 20,744 meaning group texts
    print(f"Reading corpus from {CORPUS_PATH}...")
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    print(f"Loaded {len(records)} corpus records.")

    # Calculate token counts
    t0 = time.perf_counter()
    token_lengths = []
    # Test prefix "title: none | text: "
    prefix = "title: none | text: "
    prefix_tokens = len(tokenizer.tokenize(prefix))
    print(f"Document prefix '{prefix}' token count: {prefix_tokens}")

    exceed_512 = 0
    exceed_1024 = 0
    exceed_2048 = 0
    exceed_4096 = 0
    exceed_8192 = 0

    max_rec = None
    max_len = 0

    for i, r in enumerate(records):
        raw_text = r["text"]
        full_text = prefix + raw_text
        # Fast encoding length estimation
        # tokenizer.encode is fast
        tok_ids = tokenizer.encode(full_text, add_special_tokens=True)
        length = len(tok_ids)
        token_lengths.append(length)

        if length > 512:
            exceed_512 += 1
        if length > 1024:
            exceed_1024 += 1
        if length > 2048:
            exceed_2048 += 1
        if length > 4096:
            exceed_4096 += 1
        if length > 8192:
            exceed_8192 += 1

        if length > max_len:
            max_len = length
            max_rec = (r["group_id"], length, raw_text[:120])

    lengths_np = np.array(token_lengths)
    total = len(token_lengths)
    p50 = float(np.percentile(lengths_np, 50))
    p90 = float(np.percentile(lengths_np, 90))
    p95 = float(np.percentile(lengths_np, 95))
    p99 = float(np.percentile(lengths_np, 99))
    max_val = int(np.max(lengths_np))
    min_val = int(np.min(lengths_np))
    mean_val = float(np.mean(lengths_np))

    print("\n--- CORPUS TOKEN LENGTH DISTRIBUTION (ARABIC NASS + PREFIX) ---")
    print(f"Total documents:       {total}")
    print(f"Min tokens:            {min_val}")
    print(f"Median (P50) tokens:   {p50:.1f}")
    print(f"Mean tokens:           {mean_val:.1f}")
    print(f"P90 tokens:            {p90:.1f}")
    print(f"P95 tokens:            {p95:.1f}")
    print(f"P99 tokens:            {p99:.1f}")
    print(f"Max tokens:            {max_val} (Group ID: {max_rec[0]}, Sample: {max_rec[2]}...)")
    print(f"Exceeding 512 tokens:  {exceed_512} ({exceed_512/total*100:.2f}%)")
    print(f"Exceeding 1024 tokens: {exceed_1024} ({exceed_1024/total*100:.2f}%)")
    print(f"Exceeding 2048 tokens: {exceed_2048} ({exceed_2048/total*100:.2f}%)")
    print(f"Exceeding 4096 tokens: {exceed_4096} ({exceed_4096/total*100:.2f}%)")
    print(f"Exceeding 8192 tokens: {exceed_8192} ({exceed_8192/total*100:.2f}%)")

    # If model has sliding_window of 512, how many documents are truncated if max_seq_length was set to 512?
    # Or if SentenceTransformers model.max_seq_length default was 1000000000000000019884624838656?
    print("\n--- SLIDING WINDOW & CONTEXT IMPLICATIONS ---")
    print(f"Notice: config.json sliding_window = 512, max_position_embeddings = 262,144.")
    print(f"If the model sequence length is clamped at 512: {exceed_512} hadiths ({exceed_512/total*100:.2f}%) lose tokens.")
    print(f"If the model sequence length is clamped at 2048: {exceed_2048} hadiths ({exceed_2048/total*100:.2f}%) lose tokens.")

    # Benchmark query token lengths across languages
    print("\n--- BENCHMARK QUERY TOKEN LENGTHS BY LANGUAGE ---")
    benchmark_queries = []
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                benchmark_queries.append(json.loads(line))

    by_lang = {}
    for q in benchmark_queries:
        lang = q.get("language", "unknown")
        if lang not in by_lang:
            by_lang[lang] = []
        q_text = q["query"]
        toks = tokenizer.encode(q_text, add_special_tokens=False)
        by_lang[lang].append((len(toks), q_text))

    print(f"{'Language':<12} | {'Count':<6} | {'Median':<8} | {'P95':<8} | {'Max':<8}")
    print("-" * 55)
    for lang, items in sorted(by_lang.items()):
        cnt = len(items)
        lens = np.array([x[0] for x in items])
        med = np.median(lens)
        p95_l = np.percentile(lens, 95)
        mx = np.max(lens)
        print(f"{lang:<12} | {cnt:<6} | {med:<8.1f} | {p95_l:<8.1f} | {mx:<8}")

    return {
        "total_documents": total,
        "token_distribution": {
            "min": min_val,
            "median": p50,
            "mean": mean_val,
            "p90": p90,
            "p95": p95,
            "p99": p99,
            "max": max_val,
            "exceed_512": exceed_512,
            "exceed_1024": exceed_1024,
            "exceed_2048": exceed_2048,
            "exceed_4096": exceed_4096,
            "exceed_8192": exceed_8192,
        },
    }


def audit_prompt_sample_tracing() -> None:
    print("\n" + "=" * 80)
    print("3. PROMPTING TRACE AUDIT (5 SAMPLES)")
    print("=" * 80)

    from transformers import AutoTokenizer

    snap_dir = find_hf_snapshot_dir()
    tokenizer = AutoTokenizer.from_pretrained(str(snap_dir))

    # Official prompts
    official_doc_prefix = "title: none | text: "
    official_query_prefix = "task: search result | query: "
    # Colab query prefix that was actually used:
    used_query_prefix = "task: Given a web search query, retrieve relevant passages that answer the query\nquery: "

    print("\n--- SAMPLE 5 DOCUMENTS ---")
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
            if len(records) >= 5:
                break

    for r in records:
        gid = r["group_id"]
        raw = r["text"]
        intended_text = official_doc_prefix + raw
        toks = tokenizer.encode(intended_text, add_special_tokens=True)
        print(f"\n[Doc Group {gid}]")
        print(f"  Raw Text:          {raw[:80]}...")
        print(f"  Task Applied:      'Document' (expanded to '{official_doc_prefix}')")
        print(f"  Final Model Input: {intended_text[:100]}...")
        print(f"  Token Count:       {len(toks)}")

    print("\n--- SAMPLE 5 QUERIES (CONTRASTING INTENDED VS ACTUALLY USED) ---")
    queries = []
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                queries.append(json.loads(line))
            if len(queries) >= 5:
                break

    for q in queries:
        qid = q["query_id"]
        lang = q.get("language")
        raw = q["query"]

        intended_text = official_query_prefix + raw
        intended_toks = tokenizer.encode(intended_text, add_special_tokens=True)

        used_text = used_query_prefix + raw
        used_toks = tokenizer.encode(used_text, add_special_tokens=True)

        prefix_only_used = tokenizer.encode(used_query_prefix, add_special_tokens=False)
        prefix_only_intended = tokenizer.encode(official_query_prefix, add_special_tokens=False)

        print(f"\n[Query {qid} ({lang})]")
        print(f"  Raw Query:         '{raw}'")
        print(f"  INTENDED Prefix:   '{official_query_prefix}' ({len(prefix_only_intended)} tokens)")
        print(f"  USED Prefix:       '{used_query_prefix}' ({len(prefix_only_used)} tokens)")
        print(f"  INTENDED Input:    '{intended_text}' (Total tokens: {len(intended_toks)})")
        print(f"  USED Input:        '{used_text}' (Total tokens: {len(used_toks)})")
        print(f"  Token Overhead:    Used prefix added +{len(prefix_only_used) - len(prefix_only_intended)} tokens of English instruction!")


if __name__ == "__main__":
    t0 = time.perf_counter()
    audit_model_config()
    audit_tokenization_and_lengths()
    audit_prompt_sample_tracing()
    print(f"\nAudit complete in {time.perf_counter() - t0:.2f} seconds.")
