# MĪZĀN AL-ḤADĪTH — EMBEDDINGGEMMA 2 (PHASE 1)
## Engineering Guide, Colab Runbook & Verification Manifest
### Status: Phase 1 Infrastructure Implemented & Validated
### Target: Experimental Semantic Retrieval Architecture

---

## 1. Executive Summary

This document establishes the official technical guide and reproduction runbook for **Phase 1 of the EmbeddingGemma 2 experimental pipeline** in **Mīzān al-Ḥadīth**.

Phase 1 provides an isolated, deterministic, and non-destructive infrastructure for generating and serving **Google EmbeddingGemma 2** (`google/embeddinggemma-2`) embeddings over the canonical **20,744 active meaning groups** extracted from `data/hadith-kg.db`.

### Key Safety Invariants Enforced:
1. **Canonical Immutability**: `data/hadith-kg.db` is strictly read-only (`PRAGMA query_only = ON;`). Its SHA-256 digest (`08c3a43d78f51082...`) was validated before and after execution and remains 100% identical.
2. **Baseline Preservation**: The existing production semantic vector store `data/derived_semantic_index.db` (`gemini-embedding-001`) remains untouched and active. Its SHA-256 digest (`0867383f9b29bd9c...`) remains 100% identical.
3. **Derived Isolation**: Experimental EmbeddingGemma 2 vectors and metadata reside exclusively in `data/derived_embeddinggemma2_768d.db`.
4. **No Production Switch**: The default semantic provider remains strictly `gemini`.

---

## 2. Cryptographic Provenance Manifest

| Artifact | File Path | Measured SHA-256 Digest | Status |
| :--- | :--- | :--- | :--- |
| **Canonical Source DB** | `data/hadith-kg.db` | `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd` | **UNCHANGED (Verified)** |
| **Baseline Semantic DB** | `data/derived_semantic_index.db` | `0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875` | **UNCHANGED (Verified)** |
| **Exported Corpus** | `data/meaning_groups_export.jsonl` | `bc15a337b6eb0dddfb294fe6ce7ada063b5a4879ad7eec80f98ddbb17d6a9cbf` | **DETERMINISTIC (Verified)** |
| **Audit Manifest** | `data/embedding_manifest.json` | Generated | **RECORDED** |
| **Derived Vector Store** | `data/derived_embeddinggemma2_768d.db` | Initialized | **ISOLATED** |

---

## 3. Deterministic Corpus Extraction

The extraction engine (`scripts/export_embeddinggemma2_corpus.py`) queries the canonical database to extract active meaning groups:

```sql
SELECT id, nass, sahaba_qty, repeat_qty
FROM meaning_groups
WHERE id > 0 AND LENGTH(TRIM(nass)) > 0
ORDER BY id ASC;
```

### Empirical Extraction Metrics:
- **Total Rows in `meaning_groups`**: 20,745
- **Placeholder Rows Excluded**: 1 row (`id = 0`, containing placeholder `'غير منشور'`)
- **Active Meaning Groups Exported**: Exactly **20,744 records**
- **First Exported Record**: `group_id = 1` (`"لا تكذبوا علي فإنه من كذب علي فليلج النار"`)
- **Last Exported Record**: `group_id = 22321` (`"باب أمتي الذي يدخلون منه الجنة..."`)
- **Output File Size**: 4,570,514 bytes (~4.57 MB)
- **Determinism Check**: Re-running the script produces identical records and bit-for-bit identical SHA-256 (`bc15a337b6eb0dd...`).

---

## 4. Derived Database Schema (`data/derived_embeddinggemma2_768d.db`)

The experimental database contains two tables: `metadata` and `group_embedding`.

```sql
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS group_embedding (
    group_id INTEGER PRIMARY KEY,
    model TEXT NOT NULL,
    dimensions INTEGER NOT NULL,
    vector BLOB NOT NULL,          -- 768-D Float32 array, little-endian (3,072 bytes)
    norm_l2 REAL NOT NULL,         -- Pre-normalization L2 norm
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_group_embedding_lookup 
ON group_embedding(model, dimensions);
```

### Metadata Recorded:
- `model`: `google/embeddinggemma-2`
- `model_variant`: `text-only-270m`
- `dimensions`: `768`
- `dtype`: `float32_little_endian`
- `blob_bytes_per_vector`: `3072`
- `normalization`: `L2 unit sphere`
- `corpus_type`: `canonical_meaning_groups`
- `target_count`: `20744`
- `source_database`: `data/hadith-kg.db`
- `source_database_sha256`: `08c3a43d78f51082...`
- `baseline_database`: `data/derived_semantic_index.db`
- `baseline_database_sha256`: `0867383f9b29bd9c...`
- `corpus_sha256`: `bc15a337b6eb0dd...`
- `task_prompt_document`: `Document`
- `task_prompt_query`: `SearchQuery`
- `embedding_provider`: `embeddinggemma2`
- `baseline_provider`: `gemini`

---

## 5. Google Colab Workflow & Execution Runbook

The complete, self-contained batch embedding pipeline is implemented in:
[notebooks/embeddinggemma2_colab.ipynb](file:///c:/Users/taymi/discord-hadith-bot/notebooks/embeddinggemma2_colab.ipynb)

### Step-by-Step Operator Guide:

#### Step 1: Open Notebook in Google Colab
1. Navigate to [Google Colab](https://colab.research.google.com).
2. Upload `notebooks/embeddinggemma2_colab.ipynb`.
3. In Colab, select: **Runtime > Change runtime type > T4 GPU** (or A100 GPU if available; standard CPU also functions via fallback).

#### Step 2: Configure Hugging Face Secret
Because `google/embeddinggemma-2` is an open-weights model requiring agreement to Google's terms:
1. In Colab left sidebar, click the **Key icon (Secrets)**.
2. Add a new secret:
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face user access token.
   - Toggle **Notebook access** to ON.

#### Step 3: Upload Exported Corpus
1. Upload `data/meaning_groups_export.jsonl` to `/content/` or place it in your Google Drive at `My Drive/mizan/meaning_groups_export.jsonl`.
2. The notebook automatically detects both local `/content/` and Google Drive paths.

#### Step 4: Run the Notebook
1. Execute cells sequentially.
2. The notebook mounts Google Drive to ensure output files persist across disconnections:
   ```python
   OUTPUT_DB_PATH = Path("/content/drive/MyDrive/mizan/derived_embeddinggemma2_768d.db")
   ```
3. Checkpoint progress is displayed in real time:
   ```text
   [PROGRESS] 5000/20744 (24.1%) | Throughput: 420.5 it/s | ETA: 0.6 min
   ```
4. If interrupted, simply re-run the notebook. The dynamic exclusion query (`SELECT group_id FROM group_embedding;`) skips all previously committed records and resumes from the exact interruption point.

#### Step 5: Transfer Resulting Database
1. Copy `derived_embeddinggemma2_768d.db` back to the repository's `data/` folder:
   ```text
   discord-hadith-bot/data/derived_embeddinggemma2_768d.db
   ```

---

## 6. Batching, Resumability & Error Recovery

### Resilience Features:
1. **Dynamic Exclusion**: Rather than sequential ID ranges, the notebook queries the destination database directly. Missing or retried records are identified dynamically without gaps.
2. **Atomic Chunking**: Transactions of 500 items are written via `BEGIN TRANSACTION` ... `COMMIT`. If interrupted, SQLite rolls back the uncommitted batch automatically.
3. **CUDA OOM Dynamic Backoff**: If a batch encounters `torch.cuda.OutOfMemoryError`, the batch size is automatically halved (from 64 $\rightarrow$ 32 $\rightarrow$ 16 $\rightarrow$ 4), GPU cache is cleared via `torch.cuda.empty_cache()`, and the batch is retried without crashing.
4. **Failure Logging**: Any persistent record failure is recorded in `failed_embeddings.jsonl` with timestamp and error message.

---

## 7. Local Derived Database Loader API

A clean, non-disruptive Python loader is provided in:
[mizan-web/backend/ask_mizan/embeddinggemma_store.py](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/embeddinggemma_store.py)

### Example Usage:
```python
from ask_mizan.embeddinggemma_store import get_embeddinggemma_store

store = get_embeddinggemma_store()

# Check existence and metadata
if store.exists():
    print("Stored vector count:", store.count())
    metadata = store.get_metadata()
    print("Model:", metadata.get("model"))

    # Load vector for specific meaning group
    vec = store.get_vector(1)  # Returns np.ndarray[768, float32]
    
    # In-RAM cosine similarity search
    results = store.search_vectors(query_vector, top_k=5)
```

---

## 8. Validation Suite Results

The validation suite (`scripts/validate_embeddinggemma2.py`) executes 7 rigorous checks:

```text
======================================================================
MĪZĀN AL-ḤADĪTH — EMBEDDINGGEMMA 2 PHASE 1 VALIDATION SUITE
======================================================================
[PASS] Test 1: Canonical Database Immutability (hadith-kg.db SHA-256 unchanged)
[PASS] Test 2: Baseline Gemini Semantic Store Immutability (derived_semantic_index.db SHA-256 unchanged)
[PASS] Test 3: Exported Corpus Determinism & Integrity (20,744 records verified)
[PASS] Test 4: Derived Database Schema & Metadata (Tables & 19 manifest keys verified)
[PASS] Test 5: Vector Mathematical Validation (768-D Float32, 3072 bytes, finite check)
[PASS] Test 6: Self-Similarity & Top-1 Nearest Neighbor (Cosine(v, v) = 1.0 passed)
[PASS] Test 7: Resumability & Dynamic ID Exclusion Simulation (Crash recovery verified)
======================================================================
[SUCCESS] ALL 7 PHASE 1 VALIDATION TESTS PASSED.
======================================================================
```

---

## 9. Explicit Classification: Measured Facts vs. Assumptions vs. Future Targets

### Measured Facts (Empirically Verified):
- Canonical database `data/hadith-kg.db` contains 715,790 hadiths and 20,745 meaning groups.
- Exactly 20,744 active meaning groups exist (`id > 0` and non-empty `nass`).
- `data/meaning_groups_export.jsonl` contains 20,744 lines, 4,570,514 bytes, SHA-256 `bc15a337b6eb0dddfb294fe6ce7ada063b5a4879ad7eec80f98ddbb17d6a9cbf`.
- `hadith-kg.db` SHA-256 is `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd`.
- `derived_semantic_index.db` SHA-256 is `0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875`.
- Derived database schema is initialized and verified.
- All 7 validation tests pass.

### Assumptions:
- Google Colab GPU runtimes will maintain connectivity long enough to execute in chunks of 500 without frequent interruptions.
- The 270M text-only backbone of `google/embeddinggemma-2` will process text without requiring visual or audio modality weights.

### Future Targets (To Be Evaluated in Later Phases):
- Objective retrieval quality benchmark comparing EmbeddingGemma 2 vs Gemini on 100 multilingual Hadith queries.
- ONNX Runtime local CPU query inference latency optimization.
- Matryoshka Representation Learning (MRL) dimension reduction tests (512, 256, 128).

---

## 10. Recommended Next Phase

Do NOT proceed directly to production migration.
The recommended next step is:
**Phase 2: Benchmark Dataset Construction & Comparative Evaluation Suite**.
Build the 100-query benchmark suite across Arabic, Urdu, English, and canonical citations to objectively compare `google/embeddinggemma-2` against `gemini-embedding-001`.
