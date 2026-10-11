# MĪZĀN AL-ḤADĪTH — EMBEDDINGGEMMA 2
## PHASE 5: CORRECTED CONTROLLED BENCHMARK REPORT

**Project:** Mīzān al-Ḥadīth (`mizan-hadith-kg`)  
**Phase:** Phase 5 Corrected Controlled Benchmark  
**Author:** Antigravity AI Engineering & ML Systems Lead  
**Status:** REAL LIVE GEMINI BASELINE VERIFIED & COMPLETE — CANDIDATE COMPARISON COMPLETED  
**Production Provider:** `SEMANTIC_EMBEDDING_PROVIDER=gemini` (Unchanged & Strictly Retained)  
**Date:** 2026-10-08  

---

## 1. Executive Summary

Phase 4 forensic failure analysis demonstrated that the comparative retrieval benchmark evaluated in Phase 3 was scientifically invalid due to two distinct defects:
1. **Candidate Query Prompting Defect:** EmbeddingGemma 2 was evaluated using an unauthorized, legacy 19-token English instruction prefix (`task: Given a web search query...`). Combined with prompt-inclusive mean pooling (`"include_prompt": True`), the prompt diluted short Arabic and Urdu query embeddings by up to ~79%, causing severe manifold displacement.
2. **Synthetic Gemini Baseline Leakage:** The Gemini baseline was generated in dry-run mode (`is_dry_run: True`), where query vectors were synthesized by spherically blending the exact gold meaning group vector from `derived_semantic_index.db` with noise ($\alpha = 0.88$). This guaranteed an artificial `1.0000` recall score across all 450 semantic queries through circular label leakage.

### Phase 5 Corrective Achievements:
- **Corpus & Candidate Vector Audit:** Verified that the 20,744 document vectors generated in Google Colab used Google's official `"Document"` prompt (`"title: none | text: "`), unit L2 normalization, and mean pooling correctly. These vectors are verified and reused without mutation.
- **Candidate Implementation Hardening:** Corrected the query encoding specification in `notebooks/embeddinggemma2_colab.ipynb` to use the official Google `SearchQuery` prompt (`"task: search result | query: "`) via `prompt_name="SearchQuery"`. Updated Step 1 with `sentence-transformers>=6.1.0` and `transformers>=4.49.0`, automated Colab runtime restart, and hardened model loaders in Step 6 and Step 11 with offline-first cache inspection and exponential retry backoff.
- **Real Live Gemini Baseline Execution:** Executed `scripts/run_gemini_live_benchmark.py` using live production API calls (`gemini-embedding-001`, 768 dimensions, `taskType: RETRIEVAL_QUERY`). Zero synthetic vectors were generated. Evaluated all 500 benchmark queries against the exact 20,744 candidate vectors in `data/derived_semantic_index.db`.
- **Authoritative Comparative Finding:** Real live Gemini achieves **MRR = 0.5045**, **Recall@1 = 0.4267**, and **Recall@10 = 0.6622** on the 450 semantic queries. It significantly outperforms EmbeddingGemma 2 (MRR = 0.2356, Recall@1 = 0.1778, Recall@10 = 0.3444) across all evaluated metrics and languages.
- **Decision Gate & Production Recommendation:**
  - **GATE 1 (Implementation Valid):** PASS (Hardened and verified in `notebooks/embeddinggemma2_colab.ipynb`).
  - **GATE 2 (Gemini Baseline Valid):** **PASS** (`gemini_live_baseline_run_v1.json`, 500 queries, `is_dry_run: false`).
  - **GATE 3 (Model Quality Verdict):** **RETAIN GEMINI IN PRODUCTION**.
  - Production configuration remains strictly unchanged: `SEMANTIC_EMBEDDING_PROVIDER=gemini`.

---

## 2. Methodology & Scientific Controls

| Dimension | Phase 3 (Defective) | Phase 5 (Corrected & Controlled) | Control Status |
| :--- | :--- | :--- | :---: |
| **Benchmark Queries** | 500 queries (450 semantic, 50 ref/edge) | 500 queries (450 semantic, 50 ref/edge) | **IDENTICAL & FROZEN** |
| **Candidate Universe** | 20,744 active meaning groups | 20,744 active meaning groups | **IDENTICAL (1:1)** |
| **Candidate Document Vectors** | Precomputed 768d unit L2 vectors | Reused exact same 20,744 vectors | **READ-ONLY UNTOUCHED** |
| **EG2 Query Prompt** | Legacy 19-token English prompt | Official `SearchQuery` (`prompt_name="SearchQuery"`) | **CORRECTED** |
| **Gemini Query Source** | Synthetic label blending ($\alpha=0.88$) | Live HTTP API (`gemini-embedding-001`) | **REAL API (0 LEAKAGE)** |
| **Scoring Logic** | Monolithic average | 450 semantic scored, 50 reference isolated | **SCIENTIFICALLY CONTROLLED** |
| **Ranking Metric** | Cosine similarity top-50 | Cosine similarity top-50 (GPU + CPU verified) | **VERIFIED** |

---

## 3. Primary Retrieval Benchmark Results

Evaluated across the 450 scored semantic queries in [`data/benchmarks/embeddinggemma2_benchmark_v1.jsonl`](file:///c:/Users/taymi/discord-hadith-bot/data/benchmarks/embeddinggemma2_benchmark_v1.jsonl):

| Metric | Candidate: EmbeddingGemma 2 (`google/embeddinggemma-2`) | Baseline: Real Live Gemini (`gemini-embedding-001`) | Absolute Difference ($\Delta$) | Relative Difference | Winner |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Recall@1** | 0.1778 | **0.4267** | +0.2489 | **+140.0%** | **Gemini Live** |
| **Recall@5** | 0.3089 | **0.6067** | +0.2978 | **+96.4%** | **Gemini Live** |
| **Recall@10** | 0.3444 | **0.6622** | +0.3178 | **+92.3%** | **Gemini Live** |
| **MRR** | 0.2356 | **0.5045** | +0.2689 | **+114.1%** | **Gemini Live** |
| **nDCG@10** | 0.2569 | **0.5393** | +0.2824 | **+109.9%** | **Gemini Live** |

---

## 4. Per-Language & Cross-Lingual Breakdown

| Query Category | Query Count | EmbeddingGemma 2 MRR | Gemini Live MRR | Gemini Superiority | Winner |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Monolingual Arabic** | 150 | 0.3183 | **0.4987** | +56.7% | **Gemini Live** |
| **Monolingual Urdu** | 100 | 0.1770 | **0.4177** | +136.0% | **Gemini Live** |
| **Monolingual English** | 100 | 0.1498 | **0.4690** | +213.1% | **Gemini Live** |
| **Cross-Lingual (Urdu/En $\rightarrow$ Ar)** | 100 | 0.2561 | **0.6356** | +148.2% | **Gemini Live** |

### Key Linguistic Observations:
1. **Cross-Lingual Mastery:** Gemini demonstrates remarkable cross-lingual capability, reaching **0.6356 MRR** when matching English and Urdu queries directly to classical Arabic hadith text, whereas EmbeddingGemma 2 achieves only 0.2561 MRR.
2. **Classical Hadith Vocabulary:** On pure Arabic queries, EmbeddingGemma 2 performs moderately well (MRR 0.3183), but Gemini still holds a substantial margin (MRR 0.4987).
3. **English & Urdu Query Mismatch:** EmbeddingGemma 2 struggles noticeably on colloquial English and Urdu queries attempting to retrieve classical Arabic hadith passages (MRR 0.1498 and 0.1770 respectively).

---

## 5. Retrieval Disagreement Analysis

Analysis of Top-10 retrieval overlap across all 450 semantic queries:

| Retrieval Outcome (Top-10) | Query Count | Percentage | Interpretation |
| :--- | :---: | :---: | :--- |
| **Both Models Retrieved Gold** | 150 | 33.3% | Strong semantic consensus on well-represented topics. |
| **Gemini ONLY Retrieved Gold** | 148 | 32.9% | Queries where Gemini found gold meanings but EG2 ranked them outside top-10. |
| **EG2 ONLY Retrieved Gold** | 5 | 1.1% | Rare queries where EG2 captured semantic nuances missed by Gemini. |
| **Neither Model Retrieved Gold** | 147 | 32.7% | Difficult, highly specific, or abstract theological queries. |

**Net Advantage:** Gemini successfully retrieved gold targets in **+31.8% more queries** than EmbeddingGemma 2 across the dataset.

---

## 6. Reference & Edge Query Analysis (50 Queries)

Reference lookups (e.g., "Sahih Bukhari 1", "Muslim hadith 45", single-word terms) are intentionally isolated from semantic evaluation:

| Metric | EmbeddingGemma 2 | Gemini Live Baseline |
| :--- | :---: | :---: |
| **Total Isolated Queries** | 50 | 50 |
| **Recall@10** | 0.0600 (3/50) | **0.1200 (6/50)** |

**Architectural Confirmation:** Pure dense embedding models cannot replace structured citation parsers and lexical/FTS engines for reference lookups. Mīzān's hybrid architecture (lexical routing + semantic fallback) remains the correct design.

---

## 7. Latency & Operational Profile

| Metric | Candidate: EmbeddingGemma 2 (Colab A100 GPU) | Baseline: Gemini Live API (`gemini-embedding-001`) |
| :--- | :--- | :--- |
| **Embedding Generation Time (500 Queries)** | **0.97 sec total** (517.4 QPS) | 568.34 sec total (~1.14 sec/query) |
| **Embedding P50 Latency** | ~1.9 ms / query (batch GPU) | 1,184.03 ms / query (HTTP roundtrip) |
| **Embedding P95 Latency** | ~2.5 ms / query | 1,453.24 ms / query |
| **Vector Retrieval P50 (20,744 vectors)** | **0.17 ms** (GPU tensor dot product) | 3.91 ms (CPU NumPy dot product) |
| **Vector Retrieval P95** | **0.19 ms** | 4.88 ms |
| **Hosting & Hardware** | Requires Dedicated GPU (A100/T4) or CPU RAM | Serverless API (Zero local GPU infrastructure) |
| **Hosting Cost** | $0.50–$3.00/hr GPU instance | Pay-per-token API billing (Minimal at inference) |

---

## 8. Forensic Integrity & Math Verification

1. **Zero Synthetic Gemini Vectors:**
   - Artifact `data/benchmarks/runs/gemini_live_baseline_run_v1.json` confirmed with `"is_dry_run": false`.
   - Verified 500 individual API responses from `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent`.
   - Unit L2 normalization applied to each returned query embedding.
2. **Zero In-Memory Vector Leakage:**
   - Query vectors were generated purely from the text query string. No corpus vectors were blended.
3. **GPU vs. CPU Rank Verification:**
   - Section 13 mathematical equivalence check confirmed 100% identical rankings between PyTorch GPU matrix multiplication and NumPy CPU dot product across sample queries.
4. **Canonical Database Immutability:**
   - `data/hadith-kg.db`: Verified SHA-256 `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd` (**MATCH**).
   - `data/derived_semantic_index.db`: Verified SHA-256 `0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875` (**MATCH**).
   - `data/meaning_groups_export.jsonl`: Verified SHA-256 `bc15a337b6eb0dddfb294fe6ce7ada063b5a4879ad7eec80f98ddbb17d6a9cbf` (**MATCH**).

---

## 9. Final Decision Gates

### GATE 1 — IMPLEMENTATION VALID
- **Verdict:** **PASS**
- The official `prompt_name="SearchQuery"` specification, required package dependencies (`transformers>=4.49.0`, `sentence-transformers>=6.1.0`), automatic Colab restart, and offline-first resilient loaders are implemented and verified in `notebooks/embeddinggemma2_colab.ipynb`.

### GATE 2 — GEMINI BASELINE VALID
- **Verdict:** **PASS**
- Real, non-synthetic Gemini baseline run was successfully executed across all 500 benchmark queries against the 20,744 candidate vectors in `data/derived_semantic_index.db`. Zero synthetic leakage occurred. Output artifact `gemini_live_baseline_run_v1.json` is validated.

### GATE 3 — MODEL QUALITY VERDICT
- **Verdict:** **RETAIN GEMINI IN PRODUCTION**
- Empirical benchmark data definitively shows that Gemini leads EmbeddingGemma 2 by **+114.1% on MRR**, **+140.0% on Recall@1**, and **+92.3% on Recall@10**.
- Gemini exhibits decisive superiority in multilingual and cross-lingual retrieval (MRR 0.6356 vs. 0.2561).
- EmbeddingGemma 2 does **NOT** meet the quality threshold required to replace or compete with Gemini for production retrieval in Mīzān al-Ḥadīth.

---

## 10. Production Safety Confirmation

The following invariants remain strictly in effect:
- **`SEMANTIC_EMBEDDING_PROVIDER=gemini`** remains active in `mizan-web/backend/ask_mizan/config.py`.
- **Zero production cutover** has occurred or is permitted.
- **`data/hadith-kg.db`** remains read-only and unmutated.
- **`data/derived_semantic_index.db`** remains the sole production semantic index.
- All Phase 5 work was executed strictly within experimental benchmark boundaries.
