import json
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = REPO_ROOT / "notebooks" / "embeddinggemma2_colab.ipynb"

nb = json.load(open(NB_PATH, "r", encoding="utf-8"))

# We want to make sure the Phase 5 cells are completely clean, self-contained, and foolproof.
# Let's inspect cells 21-29 and replace them with pristine Phase 5 cells.

cell_21_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "======================================================================\n",
        "# PHASE 5: CORRECTED CONTROLLED RETRIEVAL BENCHMARK\n",
        "======================================================================\n",
        "\n",
        "This section executes the **Phase 5 Corrected Controlled Benchmark**:\n",
        "1. Reuses the existing 20,744-vector candidate database (`derived_embeddinggemma2_768d.db`) from Google Drive without regeneration.\n",
        "2. Encodes all 500 benchmark queries using Google's official `SearchQuery` task instruction (`prompt_name=\"SearchQuery\"` -> `task: search result | query: `).\n",
        "3. Emits the corrected artifact `embeddinggemma2_corrected_run_v1.json`."
    ]
}

cell_22_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 11: Environment Setup & Candidate DB Resolution\n",
        "Auto-mounts Google Drive, locates the existing 20,744-vector `derived_embeddinggemma2_768d.db`,\n",
        "ensures the model is loaded in memory, and loads `embeddinggemma2_benchmark_v1.jsonl`."
    ]
}

cell_23_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import os\n",
        "import sys\n",
        "import json\n",
        "import sqlite3\n",
        "from pathlib import Path\n",
        "import torch\n",
        "import numpy as np\n",
        "\n",
        "# 1. Auto-mount Google Drive if not mounted\n",
        "if not os.path.exists(\"/content/drive/MyDrive\"):\n",
        "    print(\"[INFO] Mounting Google Drive to access candidate database...\")\n",
        "    from google.colab import drive\n",
        "    drive.mount(\"/content/drive\")\n",
        "\n",
        "# 2. Locate existing 20,744-vector derived_embeddinggemma2_768d.db on Google Drive\n",
        "candidate_db_locations = [\n",
        "    Path(\"/content/drive/MyDrive/mizan/derived_embeddinggemma2_768d.db\"),\n",
        "    Path(\"/content/drive/MyDrive/mizan_hadith/derived_embeddinggemma2_768d.db\"),\n",
        "    Path(\"/content/drive/MyDrive/derived_embeddinggemma2_768d.db\"),\n",
        "    Path(\"/content/derived_embeddinggemma2_768d.db\"),\n",
        "]\n",
        "\n",
        "OUTPUT_DB_PATH = None\n",
        "for p in candidate_db_locations:\n",
        "    if p.exists():\n",
        "        try:\n",
        "            conn = sqlite3.connect(f\"file:{p.resolve()}?mode=ro\", uri=True)\n",
        "            c = conn.cursor()\n",
        "            count = c.execute(\"SELECT count(*) FROM group_embedding;\").fetchone()[0]\n",
        "            conn.close()\n",
        "            if count == 20744:\n",
        "                OUTPUT_DB_PATH = p\n",
        "                print(f\"[SUCCESS] Located existing candidate database: {OUTPUT_DB_PATH} ({count} vectors verified).\")\n",
        "                break\n",
        "            else:\n",
        "                print(f\"[WARN] Found {p} but row count is {count} (expected 20744).\")\n",
        "        except Exception as e:\n",
        "            print(f\"[WARN] Could not inspect {p}: {e}\")\n",
        "\n",
        "if OUTPUT_DB_PATH is None:\n",
        "    raise FileNotFoundError(\n",
        "        \"Could not locate the 20,744-vector derived_embeddinggemma2_768d.db on Google Drive!\\n\" \n",
        "        f\"Checked locations: {[str(p) for p in candidate_db_locations]}\"\n",
        "    )\n",
        "\n",
        "# Define global constants\n",
        "TARGET_DIM = 768\n",
        "MODEL_NAME = \"google/embeddinggemma-2\"\n",
        "DEVICE = \"cuda\" if torch.cuda.is_available() else \"cpu\"\n",
        "DTYPE = torch.bfloat16 if (torch.cuda.is_available() and torch.cuda.is_bf16_supported()) else (torch.float16 if torch.cuda.is_available() else torch.float32)\n",
        "\n",
        "# 3. Ensure EmbeddingGemma 2 model is loaded into memory\n",
        "if \"model\" not in globals() or model is None:\n",
        "    from sentence_transformers import SentenceTransformer\n",
        "    print(f\"[INFO] Loading {MODEL_NAME} onto {DEVICE} ({DTYPE})...\")\n",
        "    model_kwargs = {\"torch_dtype\": DTYPE} if DEVICE == \"cuda\" else {}\n",
        "    # Read HF_TOKEN if available in secrets\n",
        "    hf_token = None\n",
        "    try:\n",
        "        from google.colab import userdata\n",
        "        hf_token = userdata.get(\"HF_TOKEN\")\n",
        "    except Exception:\n",
        "        pass\n",
        "    model = SentenceTransformer(MODEL_NAME, device=DEVICE, model_kwargs=model_kwargs, token=hf_token)\n",
        "    print(f\"[SUCCESS] {MODEL_NAME} loaded successfully.\")\n",
        "else:\n",
        "    print(\"[SUCCESS] EmbeddingGemma 2 model already active in memory.\")\n",
        "\n",
        "# 4. Load benchmark dataset (500 queries)\n",
        "benchmark_locations = [\n",
        "    Path(\"/content/drive/MyDrive/mizan/embeddinggemma2_benchmark_v1.jsonl\"),\n",
        "    Path(\"/content/drive/MyDrive/mizan_hadith/embeddinggemma2_benchmark_v1.jsonl\"),\n",
        "    Path(\"/content/embeddinggemma2_benchmark_v1.jsonl\"),\n",
        "]\n",
        "BENCHMARK_PATH = None\n",
        "for bp in benchmark_locations:\n",
        "    if bp.exists():\n",
        "        BENCHMARK_PATH = bp\n",
        "        break\n",
        "\n",
        "if BENCHMARK_PATH is None:\n",
        "    print(\"[ACTION REQUIRED] Please upload embeddinggemma2_benchmark_v1.jsonl:\")\n",
        "    from google.colab import files\n",
        "    uploaded = files.upload()\n",
        "    BENCHMARK_PATH = Path(list(uploaded.keys())[0])\n",
        "\n",
        "benchmark_queries = []\n",
        "with open(BENCHMARK_PATH, \"r\", encoding=\"utf-8\") as f:\n",
        "    for line in f:\n",
        "        if line.strip():\n",
        "            benchmark_queries.append(json.loads(line))\n",
        "\n",
        "print(f\"[SUCCESS] Loaded {len(benchmark_queries)} benchmark queries from {BENCHMARK_PATH.name}\")\n"
    ]
}

cell_24_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 12: GPU Query Encoding & Vector Retrieval (Phase 5 Official SearchQuery Run)\n",
        "- **Official Query Prompt:** Uses `prompt_name=\"SearchQuery\"` (`\"task: search result | query: \"`), strictly removing the legacy 19-token prefix.\n",
        "- **Candidate Universe:** Loads the verified 20,744 document vectors from `OUTPUT_DB_PATH`.\n",
        "- **Retrieval:** Evaluates top-50 cosine similarity per query.\n",
        "- **Validation:** Confirms top-25 queries match independent NumPy CPU dot products exactly."
    ]
}

cell_25_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import time\n",
        "import sqlite3\n",
        "import numpy as np\n",
        "import torch\n",
        "from datetime import datetime, timezone\n",
        "\n",
        "# 1. Load all 20,744 candidate document vectors from derived database\n",
        "print(f\"Loading candidate vectors from {OUTPUT_DB_PATH}...\")\n",
        "conn = sqlite3.connect(f\"file:{OUTPUT_DB_PATH.resolve()}?mode=ro\", uri=True)\n",
        "cursor = conn.cursor()\n",
        "cursor.execute(\"SELECT group_id, vector FROM group_embedding ORDER BY group_id ASC;\")\n",
        "db_rows = cursor.fetchall()\n",
        "conn.close()\n",
        "\n",
        "assert len(db_rows) == 20744, f\"Expected 20,744 candidate vectors, found {len(db_rows)}!\"\n",
        "corpus_group_ids = np.array([r[0] for r in db_rows], dtype=np.int32)\n",
        "raw_bytes = b\"\".join(r[1] for r in db_rows)\n",
        "corpus_vectors = np.frombuffer(raw_bytes, dtype=np.float32).reshape((len(db_rows), TARGET_DIM))\n",
        "# Verify unit L2 normalization\n",
        "norms = np.linalg.norm(corpus_vectors, axis=1, keepdims=True)\n",
        "norms[norms == 0] = 1.0\n",
        "corpus_vectors = (corpus_vectors / norms).astype(np.float32)\n",
        "print(f\"[SUCCESS] Loaded {len(corpus_group_ids)} candidate document vectors into RAM.\")\n",
        "\n",
        "# Move corpus to PyTorch tensor on GPU for high-throughput matrix multiplication\n",
        "use_gpu = torch.cuda.is_available()\n",
        "corpus_tensor = torch.from_numpy(corpus_vectors).to(\"cuda\" if use_gpu else \"cpu\")\n",
        "\n",
        "# 2. Official EmbeddingGemma 2 Query Encoding\n",
        "# Phase 5 Requirement: Zero legacy prefix. Uses official prompt_name='SearchQuery'\n",
        "# Official task instruction applied by model: 'task: search result | query: '\n",
        "raw_queries = [q[\"query\"] for q in benchmark_queries]\n",
        "\n",
        "print(f\"[INFO] Encoding {len(raw_queries)} queries with official SearchQuery prompt on {DEVICE}...\")\n",
        "t_enc_start = time.perf_counter()\n",
        "query_embeddings = model.encode(\n",
        "    raw_queries,\n",
        "    prompt_name=\"SearchQuery\",\n",
        "    batch_size=32,\n",
        "    show_progress_bar=True,\n",
        "    normalize_embeddings=True,\n",
        "    convert_to_numpy=True,\n",
        ")\n",
        "enc_duration = time.perf_counter() - t_enc_start\n",
        "enc_qps = len(raw_queries) / max(enc_duration, 0.001)\n",
        "print(f\"[SUCCESS] Encoded {len(raw_queries)} queries in {enc_duration:.2f} s ({enc_qps:.1f} QPS).\")\n",
        "\n",
        "# 3. GPU Cosine Vector Retrieval (Top-50)\n",
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
        "print(f\"[SUCCESS] Vector search complete across {len(candidate_results)} queries!\")\n",
        "print(f\"Latency Profile: P50: {p50:.2f} ms | P95: {p95:.2f} ms | P99: {p99:.2f} ms\")\n",
        "\n",
        "# 4. Mathematical Equivalence Verification on first 25 queries (Section 13)\n",
        "print(\"Running independent mathematical verification on first 25 queries...\")\n",
        "for check_i in range(min(25, len(benchmark_queries))):\n",
        "    check_sims = np.dot(corpus_vectors, query_embeddings[check_i])\n",
        "    check_top = np.argsort(check_sims)[::-1][:top_k]\n",
        "    gpu_top = [r[\"group_id\"] for r in candidate_results[check_i][\"retrieved\"]]\n",
        "    cpu_top = [int(corpus_group_ids[idx]) for idx in check_top]\n",
        "    assert gpu_top == cpu_top, f\"Discrepancy detected at query index {check_i}!\"\n",
        "print(\"[VERIFICATION PASSED] GPU matrix multiplication matches independent NumPy cosine rankings 100%.\")\n"
    ]
}

cell_26_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 13: Export Corrected Run Artifact (`embeddinggemma2_corrected_run_v1.json`)\n",
        "Serializes the corrected results to `/content/embeddinggemma2_corrected_run_v1.json` with complete audit metadata."
    ]
}

cell_27_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "RUN_OUTPUT_PATH = Path(\"/content/embeddinggemma2_corrected_run_v1.json\")\n",
        "run_data = {\n",
        "    \"run_id\": \"embeddinggemma2_corrected_v1\",\n",
        "    \"provider\": \"embeddinggemma2\",\n",
        "    \"model\": MODEL_NAME,\n",
        "    \"dimensions\": TARGET_DIM,\n",
        "    \"query_task_prompt\": \"task: search result | query: \",\n",
        "    \"prompt_name\": \"SearchQuery\",\n",
        "    \"candidate_db\": str(OUTPUT_DB_PATH.name),\n",
        "    \"total_candidates\": len(corpus_group_ids),\n",
        "    \"top_k\": top_k,\n",
        "    \"timestamp\": datetime.now(timezone.utc).isoformat(),\n",
        "    \"is_dry_run\": False,\n",
        "    \"status\": \"COMPLETED\",\n",
        "    \"hardware\": {\n",
        "        \"device\": str(DEVICE),\n",
        "        \"gpu_name\": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,\n",
        "        \"torch_version\": torch.__version__,\n",
        "    },\n",
        "    \"latency\": {\n",
        "        \"total_encoding_sec\": round(enc_duration, 2),\n",
        "        \"encoding_qps\": round(enc_qps, 2),\n",
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
}

cell_28_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 14: Download Corrected Run Artifact\n",
        "Downloads `embeddinggemma2_corrected_run_v1.json` to place into `data/benchmarks/runs/`."
    ]
}

cell_29_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "from google.colab import files\n",
        "files.download(str(RUN_OUTPUT_PATH))\n"
    ]
}

# Replace cells from index 21 to 29
new_phase5_cells = [
    cell_21_md,
    cell_22_md,
    cell_23_code,
    cell_24_md,
    cell_25_code,
    cell_26_md,
    cell_27_code,
    cell_28_md,
    cell_29_code,
]

# Keep any subsequent cells (e.g. Step 15) or replace up to cell 30
prefix_cells = nb["cells"][:21]
suffix_cells = nb["cells"][30:] if len(nb["cells"]) > 30 else []

nb["cells"] = prefix_cells + new_phase5_cells + suffix_cells

with open(NB_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"[SUCCESS] Rebuilt Phase 5 cells in {NB_PATH}. Total cells: {len(nb['cells'])}")
