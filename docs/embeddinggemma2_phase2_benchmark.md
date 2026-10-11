# MĪZĀN AL-ḤADĪTH — EMBEDDINGGEMMA 2 PHASE 2 BENCHMARK GUIDE
## Benchmark Dataset Construction, Methodology & Comparative Evaluation Suite

---

## 1. PHASE 2 OBJECTIVE & GOVERNANCE

The primary objective of **Phase 2** is to establish an authoritative, mathematically rigorous, reproducible benchmark to evaluate whether:

```text
EmbeddingGemma 2 (google/embeddinggemma-2, 768-D)
```

is a viable semantic retrieval candidate for Mīzān al-Ḥadīth compared with the active production baseline:

```text
Gemini (gemini-embedding-001, 768-D)
```

### Absolute Production Safety Invariants
1. **Zero Production Mutation:** Production remains strictly configured with `SEMANTIC_EMBEDDING_PROVIDER=gemini`.
2. **Canonical Data Immutability:** `data/hadith-kg.db` is strictly read-only and immutable (`SHA-256: 08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd`).
3. **Gemini Semantic Store Immutability:** `data/derived_semantic_index.db` is strictly frozen (`SHA-256: 0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875`).
4. **Scholarly Authority:** Canonical hadith IDs and meaning groups remain authoritative; embedding vectors are strictly derived experimental caches.

---

## 2. GOOGLE COLAB ACCOUNT SPECIFICATION

Google Colab GPU execution for this pipeline is associated with:

```text
itsriver236@gmail.com
```

### Security Invariants:
- The email address is an operator reference and **never** a credential.
- No passwords, OAuth tokens, API keys, or Hugging Face access tokens are committed or stored in repository code.
- Credentials in Colab are managed exclusively via Google Colab Secrets (`userdata.get(...)`) and environment variables.

---

## 3. BENCHMARK DATASET SPECIFICATION

The authoritative benchmark dataset is stored at:
- **File:** `data/benchmarks/embeddinggemma2_benchmark_v1.jsonl`
- **SHA-256 Digest:** `data/benchmarks/embeddinggemma2_benchmark_v1.sha256`
- **Manifest:** `data/benchmarks/embeddinggemma2_benchmark_manifest.json`

### 3.1 Taxonomy & Distribution (500 Total Queries)

```text
Category               Queries   Language    Characteristics
──────────────────────────────────────────────────────────────────────────────────────────────────
Arabic                     150   ar          Exact wording, synonyms, paraphrases, thematic, theology
Urdu                       100   ur          Natural Urdu phrasing, Urdu paraphrases, research inquiries
English                    100   en          Natural English inquiries, academic terms, thematic queries
Cross-Lingual              100   ur & en     50 Urdu -> Arabic hadiths, 50 English -> Arabic hadiths
Reference & Edge            50   mixed       Book citations, numbers, boundary cases (System Safety)
──────────────────────────────────────────────────────────────────────────────────────────────────
TOTAL                      500               Strictly mapped to canonical meaning groups
```

### 3.2 Gold Relevance Ground-Truth Methodology

> [!IMPORTANT]
> **Zero Circular Dependency Rule:**  
> Gold relevance labels were established deterministically from canonical relationships in `data/hadith-kg.db` (linking meaning groups and hadiths) and classical scholarly mappings. Under no circumstances was candidate EmbeddingGemma 2 or Gemini embedding similarity used to generate gold labels.

Every record follows a structured JSONL schema:

```json
{
  "query_id": "AR_EXACT_001",
  "language": "ar",
  "category": "exact_wording",
  "query": "الأعمال بالنيات",
  "gold_group_ids": [319],
  "gold_hadith_ids": [1, 53, 2356],
  "difficulty": "easy",
  "provenance_source": "canonical_meaning_group:319",
  "notes": "Exact core prophetic wording: Hadith of intention, Bukhari 1 / Muslim 1907"
}
```

---

## 4. QUERY TASK CONFIGURATIONS

Model embedding architectures require task-specific instruction prompts to optimize retrieval density:

### 4.1 Gemini Baseline Configuration
- **Model:** `gemini-embedding-001`
- **Output Dimensionality:** `768`
- **Task Type:** `RETRIEVAL_QUERY`
- **Normalization:** Unit L2 ($||v|| = 1.0$)

### 4.2 EmbeddingGemma 2 Candidate Configuration
- **Model:** `google/embeddinggemma-2`
- **Output Dimensionality:** `768`
- **Task Prompt Template:**
  ```text
  task: Given a web search query, retrieve relevant passages that answer the query\nquery: {query}
  ```
- **Normalization:** Unit L2 ($||v|| = 1.0$)

---

## 5. EVALUATION METRIC FORMULATIONS

### 5.1 Primary Semantic Metrics (450 Scored Semantic Queries)
1. **Recall@K ($K \in \{1, 5, 10\}$):**
   $$\text{Recall@K}(q) = \begin{cases} 1.0 & \text{if } \text{Top-K}(q) \cap G_q \neq \emptyset \\ 0.0 & \text{otherwise} \end{cases}$$
2. **Mean Reciprocal Rank (MRR):**
   $$\text{MRR} = \frac{1}{|Q|} \sum_{q \in Q} \frac{1}{\text{rank}(q)}$$
   where $\text{rank}(q)$ is the 1-indexed rank of the first relevant gold group.
3. **Normalized Discounted Cumulative Gain (nDCG@10):**
   $$\text{DCG@10} = \sum_{i=1}^{10} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}, \quad \text{nDCG@10} = \frac{\text{DCG@10}}{\text{IDCG@10}}$$
   Graded relevance scale:
   - $\text{rel} = 3$: Primary gold meaning group
   - $\text{rel} = 2$: Secondary gold meaning group
   - $\text{rel} = 1$: Meaning group containing a gold hadith ID
   - $\text{rel} = 0$: Irrelevant

### 5.2 Cross-Lingual Gap Analysis
Calculates degradation when querying across languages against Arabic source hadiths:
$$\Delta_{\text{Cross-Lingual}} = \text{MRR}(\text{Arabic}) - \text{MRR}(\text{Cross-Lingual})$$
$$\Delta_{\text{Urdu}\to\text{Arabic}} = \text{MRR}(\text{Arabic}) - \text{MRR}(\text{Urdu}\to\text{Arabic})$$
$$\Delta_{\text{English}\to\text{Arabic}} = \text{MRR}(\text{Arabic}) - \text{MRR}(\text{English}\to\text{Arabic})$$

### 5.3 Reference & Edge Cases Safety Suite (50 Queries)
*Isolated from primary semantic score.* Evaluates exact reference lookup ("Bukhari 1", "صحيح مسلم 1907") to ensure deterministic resolvers and edge query boundaries remain non-regressive without distorting semantic embedding evaluation.

---

## 6. GOOGLE COLAB EXECUTION RUNBOOK (`itsriver236@gmail.com`)

When executing heavy candidate embedding computation on Google Colab:

1. Open `notebooks/embeddinggemma2_colab.ipynb` in Google Colab signed in with `itsriver236@gmail.com`.
2. Connect to a GPU Runtime (**T4, A100, or V100**).
3. Execute **Steps 1 through 10** to generate all 20,744 meaning group embeddings into `data/derived_embeddinggemma2_768d.db`.
4. Execute **Steps 11 through 14** (Phase 2 Suite):
   - Loads `embeddinggemma2_benchmark_v1.jsonl`.
   - Encodes 500 queries with `EG2_QUERY_PREFIX` on GPU.
   - Executes matrix multiplication against all 20,744 vectors.
   - Exports `embeddinggemma2_candidate_run.json`.
5. Download the run artifact and copy it to:
   ```bash
   data/benchmarks/runs/embeddinggemma2_candidate_run.json
   ```
6. Run the local evaluation suite:
   ```bash
   python scripts/evaluate_embeddinggemma2.py
   python scripts/validate_embeddinggemma2_phase2.py
   ```

---

## 7. DECISION GATE LOGIC & MIGRATION CRITERIA

The evaluation outputs exactly one decision:
- **`PASS`**: Candidate demonstrates comparable or superior retrieval quality ($ \Delta \text{MRR} \ge 0 $), with no material Arabic or Urdu regression, and acceptable P95 latency. Deserves progression to dark-launch shadow mode.
- **`FAIL`**: Candidate exhibits material retrieval regression ($ \Delta \text{MRR} < -0.05 $) or unacceptable operational latency. Recommendation: Retain Gemini.
- **`INCONCLUSIVE`**: Results are within statistical noise or candidate vectors are pending Colab execution.

**Current Production Status:**
```bash
SEMANTIC_EMBEDDING_PROVIDER=gemini
```
Production remains 100% on Gemini. No migration has occurred.
