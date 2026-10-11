import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = REPO_ROOT / "notebooks" / "embeddinggemma2_colab.ipynb"

nb = json.load(open(NB_PATH, "r", encoding="utf-8"))

# Cell 1 is Markdown: Step 1
# Cell 2 is Code: Step 1
nb["cells"][1]["source"] = [
    "### Step 1: Install & Upgrade Dependencies (Compatibility with EmbeddingGemma 2)\n",
    "Installs officially compatible library versions for `google/embeddinggemma-2`.\n",
    "The model architecture requires `transformers>=4.49.0` and `sentence-transformers>=6.1.0`.\n",
    "If the Colab runtime requires a restart after upgrading, the cell will automatically trigger it."
]

nb["cells"][2]["source"] = [
    "# 1. Upgrade dependencies to officially compatible versions\n",
    "# google/embeddinggemma-2 architecture requires sentence-transformers>=6.1.0 and transformers>=4.49.0\n",
    "!pip install --quiet -U \\\n",
    "    \"transformers>=4.49.0\" \\\n",
    "    \"sentence-transformers>=6.1.0\" \\\n",
    "    \"accelerate>=0.30.0\" \\\n",
    "    \"numpy>=1.24.0\"\n",
    "\n",
    "import os\n",
    "import transformers\n",
    "import sentence_transformers\n",
    "from packaging import version\n",
    "\n",
    "print(\"=\" * 60)\n",
    "print(\"MĪZĀN AL-ḤADĪTH — ENVIRONMENT DEPENDENCY VERIFICATION\")\n",
    "print(\"=\" * 60)\n",
    "print(f\"Transformers Version:         {transformers.__version__}\")\n",
    "print(f\"SentenceTransformers Version: {sentence_transformers.__version__}\")\n",
    "print(\"=\" * 60)\n",
    "\n",
    "# Check whether runtime restart is needed to unload stale C-extensions / register new architectures\n",
    "st_ver = version.parse(sentence_transformers.__version__)\n",
    "tf_ver = version.parse(transformers.__version__)\n",
    "if st_ver < version.parse(\"6.1.0\") or tf_ver < version.parse(\"4.49.0\"):\n",
    "    print(\"[ACTION REQUIRED] Dependencies were upgraded. Restarting Colab runtime automatically...\")\n",
    "    print(\"After kernel restarts in 2-3 seconds, re-run this cell to confirm versions.\")\n",
    "    os.kill(os.getpid(), 9)\n",
    "else:\n",
    "    print(\"[SUCCESS] Environment satisfies Sentence Transformers >= 6.1.0 and Transformers >= 4.49.0.\")\n"
]

# Step 6: Load EmbeddingGemma 2 Model & Smoke Test
nb["cells"][11]["source"] = [
    "### Step 6: Load EmbeddingGemma 2 Model\n",
    "Initializes `SentenceTransformer` with the text encoder backbone and verifies 768-dimensional output via smoke test."
]

nb["cells"][12]["source"] = [
    "import time\n",
    "import numpy as np\n",
    "from sentence_transformers import SentenceTransformer\n",
    "\n",
    "print(f\"[INFO] Loading {MODEL_NAME} onto {DEVICE}...\")\n",
    "t0 = time.perf_counter()\n",
    "\n",
    "model_kwargs = {\"torch_dtype\": DTYPE} if DEVICE == \"cuda\" else {}\n",
    "model = SentenceTransformer(\n",
    "    MODEL_NAME,\n",
    "    device=DEVICE,\n",
    "    model_kwargs=model_kwargs,\n",
    "    token=HF_TOKEN\n",
    ")\n",
    "\n",
    "load_time = time.perf_counter() - t0\n",
    "print(f\"[SUCCESS] Model loaded in {load_time:.2f} seconds.\")\n",
    "print(f\"Model Max Sequence Length: {model.max_seq_length}\")\n",
    "\n",
    "# Smoke test with official SearchQuery prompt\n",
    "test_emb = model.encode([\"إنما الأعمال بالنيات\"], prompt_name=\"SearchQuery\", normalize_embeddings=True)\n",
    "assert test_emb.shape == (1, TARGET_DIM), f\"Shape mismatch: {test_emb.shape} (expected (1, {TARGET_DIM}))\"\n",
    "assert np.isclose(np.linalg.norm(test_emb[0]), 1.0, atol=1e-3), \"Normalization check failed!\"\n",
    "print(f\"[SMOKE TEST PASSED] Output vector shape: {test_emb.shape}, L2 Norm: {np.linalg.norm(test_emb[0]):.4f}\")\n"
]

with open(NB_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"[SUCCESS] Updated Step 1 and Step 6 in {NB_PATH}")
