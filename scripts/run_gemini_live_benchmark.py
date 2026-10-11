"""
MĪZĀN AL-ḤADĪTH — Live Gemini Baseline Runner (Phase 5)
Executes true, non-synthetic comparative retrieval using real Gemini API embeddings.

CRITICAL SAFETY RULES:
  - ZERO synthetic vector generation (no alpha * gold_target + noise).
  - If GEMINI_API_KEY is not configured: STOP immediately and report unavailable.
  - Read-only SQLite access on data/derived_semantic_index.db.
  - Do NOT print, log, or commit secret keys.
"""

from __future__ import annotations
import argparse
import hashlib
import json
import logging
import os
import platform
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import requests

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
DEFAULT_BASELINE_DB = REPO_ROOT / "data" / "derived_semantic_index.db"
DEFAULT_OUTPUT_RUN = REPO_ROOT / "data" / "benchmarks" / "runs" / "gemini_live_baseline_run_v1.json"

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mizan.gemini_live_runner")


def load_secret_key() -> str:
    """Securely resolves GEMINI_API_KEY without logging the secret."""
    key = (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip()
    if key:
        return key

    # Check Windows Registry (HKCU\Environment)
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as reg_key:
                for var_name in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
                    try:
                        val, _ = winreg.QueryValueEx(reg_key, var_name)
                        if val and val.strip():
                            return val.strip()
                    except FileNotFoundError:
                        pass
        except Exception:
            pass

    # Check root .env
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                    return v

    # Check backend .env
    backend_env = REPO_ROOT / "mizan-web" / "backend" / ".env"
    if backend_env.exists():
        for line in backend_env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                    return v

    return ""


def run_live_gemini_benchmark(
    benchmark_path: Path = DEFAULT_BENCHMARK_PATH,
    db_path: Path = DEFAULT_BASELINE_DB,
    output_path: Path = DEFAULT_OUTPUT_RUN,
    top_k: int = 50,
) -> bool:
    api_key = load_secret_key()
    if not api_key:
        print("\n" + "=" * 80)
        print("[STOP CONDITION ACTIVATED] GEMINI LIVE BASELINE UNAVAILABLE")
        print("=" * 80)
        print("Reason: No live GEMINI_API_KEY was found in environment or .env configuration.")
        print("Per Master Prompt Section 10 & 26:")
        print("  - ZERO synthetic baseline is permitted.")
        print("  - Evaluation comparison with Gemini is marked INCOMPLETE / INCONCLUSIVE.")
        print("To configure GEMINI_API_KEY securely:")
        print("  1. Add GEMINI_API_KEY=your_key_here to .env in repository root (or mizan-web/backend/.env)")
        print("  2. Or set it in your environment: $env:GEMINI_API_KEY='your_key_here'")
        print("=" * 80 + "\n")
        return False

    print(f"[INFO] Secure key detected (length {len(api_key)}). Initializing live Gemini baseline run...")

    # Load 20,744 baseline vectors
    uri = f"file:{db_path.resolve()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=30.0)
    conn.execute("PRAGMA query_only = ON;")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT group_id, vector FROM semantic_vectors WHERE model = ? AND dim = ? ORDER BY group_id ASC;",
        (GEMINI_MODEL, EMBEDDING_DIM),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise ValueError(f"No vectors found in {db_path} for {GEMINI_MODEL} {EMBEDDING_DIM}d")

    group_ids = np.array([r[0] for r in rows], dtype=np.int32)
    raw_bytes = b"".join(r[1] for r in rows)
    vecs = np.frombuffer(raw_bytes, dtype=np.float32).reshape((len(rows), EMBEDDING_DIM))
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    corpus_vectors = (vecs / norms).astype(np.float32)
    print(f"[INFO] Loaded {len(group_ids)} Gemini baseline vectors from {db_path.name}.")

    # Load benchmark queries
    queries = []
    with open(benchmark_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                queries.append(json.loads(line))

    print(f"[INFO] Loaded {len(queries)} benchmark queries. Beginning live API encoding...")

    results = []
    embedding_latencies = []
    retrieval_latencies = []
    t_start = time.perf_counter()

    for idx, q in enumerate(queries, start=1):
        clean_text = " ".join(q["query"].split()).strip()
        url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:embedContent?key={api_key}"
        payload = {
            "model": f"models/{GEMINI_MODEL}",
            "content": {"parts": [{"text": clean_text}]},
            "taskType": "RETRIEVAL_QUERY",
            "outputDimensionality": EMBEDDING_DIM,
        }

        t_emb0 = time.perf_counter()
        resp = None
        for attempt in range(5):
            try:
                resp = requests.post(url, json=payload, timeout=20.0)
                if resp.status_code == 200:
                    break
                if resp.status_code in (429, 500, 502, 503, 504):
                    wait_time = (2 ** attempt) + 0.5
                    time.sleep(wait_time)
                else:
                    break
            except (requests.exceptions.RequestException, TimeoutError):
                wait_time = (2 ** attempt) + 0.5
                time.sleep(wait_time)

        if resp is None or resp.status_code != 200:
            err_msg = resp.text[:150] if resp else "Connection timeout"
            logger.error("API error for query %s (HTTP %s): %s", q["query_id"], getattr(resp, "status_code", "None"), err_msg)
            continue
        emb_lat = (time.perf_counter() - t_emb0) * 1000.0
        embedding_latencies.append(emb_lat)

        vals = resp.json().get("embedding", {}).get("values")
        q_vec = np.array(vals, dtype=np.float32)
        norm = np.linalg.norm(q_vec)
        if norm > 0:
            q_vec = q_vec / norm

        t_ret0 = time.perf_counter()
        sims = np.dot(corpus_vectors, q_vec)
        top_indices = np.argsort(sims)[::-1][:top_k]
        ret_lat = (time.perf_counter() - t_ret0) * 1000.0
        retrieval_latencies.append(ret_lat)

        retrieved = []
        for rank, c_idx in enumerate(top_indices, start=1):
            retrieved.append({
                "rank": rank,
                "group_id": int(group_ids[c_idx]),
                "score": round(float(sims[c_idx]), 4),
            })

        results.append({
            "query_id": q["query_id"],
            "embedding_latency_ms": round(emb_lat, 2),
            "retrieval_latency_ms": round(ret_lat, 2),
            "total_latency_ms": round(emb_lat + ret_lat, 2),
            "retrieved": retrieved,
        })

        if idx % 50 == 0 or idx == len(queries):
            print(f"[PROGRESS] {idx}/{len(queries)} queries processed...")

    total_duration = time.perf_counter() - t_start

    run_payload = {
        "run_id": "gemini_live_baseline_v1",
        "provider": "gemini",
        "model": GEMINI_MODEL,
        "dimensions": EMBEDDING_DIM,
        "top_k": top_k,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "is_dry_run": False,
        "status": "COMPLETED",
        "benchmark_file": str(benchmark_path.name),
        "total_queries": len(results),
        "latency": {
            "total_duration_sec": round(total_duration, 2),
            "embedding_p50_ms": round(float(np.percentile(embedding_latencies, 50)), 2),
            "embedding_p95_ms": round(float(np.percentile(embedding_latencies, 95)), 2),
            "retrieval_p50_ms": round(float(np.percentile(retrieval_latencies, 50)), 2),
            "retrieval_p95_ms": round(float(np.percentile(retrieval_latencies, 95)), 2),
        },
        "results": results,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(run_payload, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Saved live Gemini baseline run to {output_path}")
    return True


if __name__ == "__main__":
    run_live_gemini_benchmark()
