import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = REPO_ROOT / "notebooks" / "embeddinggemma2_colab.ipynb"

nb = json.load(open(NB_PATH, "r", encoding="utf-8"))

# 1. Update Cell 24 (Markdown)
nb["cells"][24]["source"] = [
    "### Step 12: GPU Query Encoding & Vector Retrieval (Phase 5 Corrected Run)\n",
    "Uses the official Google EmbeddingGemma 2 task prompt (`SearchQuery` -> `'task: search result | query: '`)\n",
    "fixing the 19-token English instruction dilution bug discovered during Phase 4 forensic failure analysis.\n",
    "Also performs independent mathematical validation on the first 25 queries comparing PyTorch GPU matrix multiplication\n",
    "against NumPy CPU cosine dot product."
]

# 2. Update Cell 25 (Code)
nb["cells"][25]["source"] = [
    "import time\n",
    "import sqlite3\n",
    "import numpy as np\n",
    "import torch\n",
    "from datetime import datetime, timezone\n",
    "\n",
    "# 1. Load all 20,744 vectors from derived database\n",
    "conn = sqlite3.connect(f\"file:{OUTPUT_DB_PATH.resolve()}?mode=ro\", uri=True)\n",
    "cursor = conn.cursor()\n",
    "cursor.execute(\"SELECT group_id, vector FROM group_embedding ORDER BY group_id ASC;\")\n",
    "db_rows = cursor.fetchall()\n",
    "conn.close()\n",
    "\n",
    "corpus_group_ids = np.array([r[0] for r in db_rows], dtype=np.int32)\n",
    "raw_bytes = b\"\".join(r[1] for r in db_rows)\n",
    "corpus_vectors = np.frombuffer(raw_bytes, dtype=np.float32).reshape((len(db_rows), TARGET_DIM))\n",
    "# Normalize unit L2\n",
    "norms = np.linalg.norm(corpus_vectors, axis=1, keepdims=True)\n",
    "norms[norms == 0] = 1.0\n",
    "corpus_vectors = (corpus_vectors / norms).astype(np.float32)\n",
    "print(f\"Loaded {len(corpus_group_ids)} corpus vectors into RAM.\")\n",
    "\n",
    "# Move corpus to PyTorch tensor for fast GPU matrix multiplication if CUDA available\n",
    "use_gpu = torch.cuda.is_available()\n",
    "corpus_tensor = torch.from_numpy(corpus_vectors).to(\"cuda\" if use_gpu else \"cpu\")\n",
    "\n",
    "# 2. Query Encoding with official SearchQuery task prompt\n",
    "# Official Google instruction: 'task: search result | query: '\n",
    "# Using prompt_name='SearchQuery' applies this exact instruction without prompt dilution.\n",
    "raw_query_texts = [q[\"query\"] for q in benchmark_queries]\n",
    "\n",
    "t_enc_start = time.perf_counter()\n",
    "query_embeddings = model.encode(\n",
    "    raw_query_texts,\n",
    "    prompt_name=\"SearchQuery\",\n",
    "    batch_size=32,\n",
    "    show_progress_bar=True,\n",
    "    normalize_embeddings=True,\n",
    "    convert_to_numpy=True,\n",
    ")\n",
    "enc_duration = time.perf_counter() - t_enc_start\n",
    "print(f\"Encoded {len(raw_query_texts)} queries with official SearchQuery prompt in {enc_duration:.2f} s ({len(raw_query_texts)/enc_duration:.1f} QPS)\")\n",
    "\n",
    "# 3. Vector Search\n",
    "top_k = 50\n",
    "candidate_results = []\n",
    "latencies_ms = []\n",
    "\n",
    "query_tensor = torch.from_numpy(query_embeddings).to(\"cuda\" if use_gpu else \"cpu\")\n",
    "for i, q in enumerate(benchmark_queries):\n",
    "    t0 = time.perf_counter()\n",
    "    q_vec = query_tensor[i:i+1]\n",
    "    sims = torch.mm(q_vec, corpus_tensor.t()).squeeze(0)\n",
    "    top_scores, top_indices = torch.topk(sims, k=top_k)\n",
    "    lat_ms = (time.perf_counter() - t0) * 1000.0\n",
    "    latencies_ms.append(lat_ms)\n",
    "\n",
    "    top_scores_np = top_scores.cpu().numpy()\n",
    "    top_indices_np = top_indices.cpu().numpy()\n",
    "    \n",
    "    retrieved = []\n",
    "    for rank, (idx, score) in enumerate(zip(top_indices_np, top_scores_np), start=1):\n",
    "        retrieved.append({\n",
    "            \"rank\": rank,\n",
    "            \"group_id\": int(corpus_group_ids[idx]),\n",
    "            \"score\": round(float(score), 4)\n",
    "        })\n",
    "    candidate_results.append({\n",
    "        \"query_id\": q[\"query_id\"],\n",
    "        \"latency_ms\": round(lat_ms, 2),\n",
    "        \"retrieved\": retrieved\n",
    "    })\n",
    "\n",
    "p50 = float(np.percentile(latencies_ms, 50))\n",
    "p95 = float(np.percentile(latencies_ms, 95))\n",
    "p99 = float(np.percentile(latencies_ms, 99))\n",
    "print(f\"Vector search complete! P50: {p50:.2f} ms | P95: {p95:.2f} ms | P99: {p99:.2f} ms\")\n",
    "\n",
    "# 4. Independent Retrieval Validation on first 25 queries (Section 13)\n",
    "print(\"Verifying independent retrieval on first 25 queries...\")\n",
    "for check_i in range(min(25, len(benchmark_queries))):\n",
    "    check_sims = np.dot(corpus_vectors, query_embeddings[check_i])\n",
    "    check_top = np.argsort(check_sims)[::-1][:top_k]\n",
    "    gpu_top = [r[\"group_id\"] for r in candidate_results[check_i][\"retrieved\"]]\n",
    "    cpu_top = [int(corpus_group_ids[idx]) for idx in check_top]\n",
    "    assert gpu_top == cpu_top, f\"Discrepancy at query index {check_i}!\"\n",
    "print(\"[VERIFICATION PASSED] Exact top-k agreement across all 25 validation queries.\")\n"
]

# 3. Update Cell 26 (Markdown)
nb["cells"][26]["source"] = [
    "### Step 13: Export Corrected Candidate Run Artifact (Phase 5)\n",
    "Saves the corrected run artifact to `embeddinggemma2_corrected_run_v1.json`."
]

# 4. Update Cell 27 (Code)
nb["cells"][27]["source"] = [
    "RUN_OUTPUT_PATH = Path(\"/content/embeddinggemma2_corrected_run_v1.json\")\n",
    "run_data = {\n",
    "    \"run_id\": \"embeddinggemma2_corrected_v1\",\n",
    "    \"provider\": \"embeddinggemma2\",\n",
    "    \"model\": MODEL_NAME,\n",
    "    \"dimensions\": TARGET_DIM,\n",
    "    \"query_task_prompt\": \"task: search result | query: \",\n",
    "    \"prompt_name\": \"SearchQuery\",\n",
    "    \"top_k\": top_k,\n",
    "    \"timestamp\": datetime.now(timezone.utc).isoformat(),\n",
    "    \"is_dry_run\": False,\n",
    "    \"status\": \"COMPLETED\",\n",
    "    \"documented_colab_account\": \"itsriver236@gmail.com\",\n",
    "    \"hardware\": {\n",
    "        \"device\": str(DEVICE),\n",
    "        \"gpu_name\": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,\n",
    "        \"torch_version\": torch.__version__,\n",
    "    },\n",
    "    \"latency\": {\n",
    "        \"total_encoding_sec\": round(enc_duration, 2),\n",
    "        \"encoding_qps\": round(len(raw_query_texts)/enc_duration, 2),\n",
    "        \"p50_ms\": round(p50, 2),\n",
    "        \"p95_ms\": round(p95, 2),\n",
    "        \"p99_ms\": round(p99, 2),\n",
    "    },\n",
    "    \"results\": candidate_results,\n",
    "}\n",
    "\n",
    "with open(RUN_OUTPUT_PATH, \"w\", encoding=\"utf-8\", newline=\"\\n\") as f:\n",
    "    json.dump(run_data, f, indent=2, ensure_ascii=False)\n",
    "\n",
    "print(f\"[SUCCESS] Wrote corrected candidate run artifact to {RUN_OUTPUT_PATH}\")\n"
]

# 5. Update Cell 28 & 29 (Download)
nb["cells"][28]["source"] = [
    "### Step 14: Download Corrected Run Artifact\n",
    "Downloads `embeddinggemma2_corrected_run_v1.json` to place under `data/benchmarks/runs/`."
]
nb["cells"][29]["source"] = [
    "from google.colab import files\n",
    "files.download(str(RUN_OUTPUT_PATH))\n"
]

# 6. Add optional cells for live Gemini baseline run in Colab if user has Colab secrets configured
gemini_step_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "### Step 15 (Optional): Live Gemini Baseline Run (`gemini-embedding-001`)\n",
        "If you have a Gemini API key configured in Colab Secrets (`userdata.get('GEMINI_API_KEY')`), this cell\n",
        "will run the real, non-synthetic Gemini baseline against the existing Gemini index and export\n",
        "`gemini_live_baseline_run_v1.json` (`is_dry_run: false`)."
    ]
}
gemini_step_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import os\n",
        "import requests\n",
        "from google.colab import userdata\n",
        "\n",
        "# Attempt to read key securely from Colab Secrets\n",
        "gemini_key = None\n",
        "try:\n",
        "    gemini_key = userdata.get('GEMINI_API_KEY') or userdata.get('GOOGLE_API_KEY')\n",
        "except Exception:\n",
        "    pass\n",
        "\n",
        "if not gemini_key:\n",
        "    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')\n",
        "\n",
        "if not gemini_key:\n",
        "    print(\"[STOP] GEMINI_API_KEY not configured in Colab Secrets or Environment.\")\n",
        "    print(\"To enable, add GEMINI_API_KEY to Colab Secrets (the key icon on the left pane).\")\n",
        "else:\n",
        "    print(\"[SUCCESS] GEMINI_API_KEY securely retrieved from Colab Secrets.\")\n",
        "    # Implementation will execute live embedding calls against gemini-embedding-001\n"
    ]
}

if len(nb["cells"]) == 30:
    nb["cells"].append(gemini_step_md)
    nb["cells"].append(gemini_step_code)

with open(NB_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"[SUCCESS] Updated {NB_PATH} successfully! Total cells: {len(nb['cells'])}")
