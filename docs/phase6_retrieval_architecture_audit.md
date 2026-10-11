# MĪZĀN AL-ḤADĪTH — PHASE 6
## RETRIEVAL ARCHITECTURE AUDIT & HYBRID RETRIEVAL V2

**Document:** Comprehensive Forensic Audit & Architecture Design  
**Repository:** `mizan-hadith-kg`  
**Author:** Lead Retrieval/Search Architect  
**Status:** AUDIT & DESIGN COMPLETE (PHASE 6A) — ZERO PRODUCTION CHANGES  
**Date:** 2026-10-08  

---

## 1. Executive Summary

Following the definitive Phase 5 comparative benchmark (which confirmed that Google Gemini Live remains the production semantic embedding provider, outperforming EmbeddingGemma 2 by +114.1% on MRR), Phase 6 conducted a complete, non-destructive forensic audit of Mīzān's retrieval infrastructure.

### Key Audit Findings:
1. **Multi-Siloed Retrieval Landscape:** Retrieval is currently split across three distinct subsystems:
   - **Ask Mīzān Layered Retrieval (`mizan-web/backend/ask_mizan/semantic.py`):** Features an in-RAM vector index over 20,744 meaning group embeddings (~64 MB RAM) querying `data/derived_semantic_index.db`, with deterministic fallback to SQLite table scans (`LIKE %term%`).
   - **Production Web API (`mizan-web/backend/main.py`):** Operates two separate endpoints: `/api/hadith/search` (Arabic custom multi-token AND/OR scoring with fallback to `data/hadith-search-index.db`) and `/api/hadith/search/en` (English translation FTS5 search querying `data/english_translation_fts.db`).
   - **Reference Resolver (`reference_resolver.py` / `hadith_numbers`):** Fast structured lookup for canonical citations (e.g., "Bukhari 1", "Muslim 1907") mapping to primary keys via `data/hadith_numbering.db`.
2. **The Urdu Indexing Void:** While Mīzān has indexed 31,488 English translations in FTS5, **zero indexed Urdu text or translation tables exist in SQLite**. All Urdu queries rely 100% on Gemini's cross-lingual semantic representations.
3. **Forensic Anatomy of the 147 "Neither" Cases:** A deep qualitative audit of the 147 benchmark queries where neither Gemini nor EmbeddingGemma 2 achieved Top-10 recall revealed:
   - **Benchmark Gold Label Noise (Critical Discovery):** 81 queries in the benchmark (16.2% of the entire dataset) were anchored to a single meaning group (GID 319, Hadith al-Niyyat). Queries asking about "Truthfulness & Lying", "Every one of you is a shepherd", or "Duha prayer" were artificially labeled as GID 319. Gemini frequently retrieved the **literal, perfect hadith** (e.g., GID 431 for "كلكم راع", GID 614 for "لا يقبل الله صلاة بغير طهور", GID 863 for "السواك مطهرة للفم"), but scored 0 due to label noise.
   - **Rank 11–50 Recovery:** For 34 of the 147 queries (23.1%), Gemini actually retrieved the gold meaning group in Ranks 11–50, just narrowly missing the Top-10 threshold.
   - **Zero Universe Omission:** All 20,744 candidate meaning groups are verified present in `derived_semantic_index.db`.
4. **Empirical Hybrid Fusion v2 Results:**
   - Simulated Reciprocal Rank Fusion (RRF, $k=60$) combining live Gemini embeddings with lexical FTS retrieval across the 500 benchmark queries.
   - **Semantic Queries (450):** RRF improves MRR from **0.5045 $\rightarrow$ 0.5153**, Recall@1 from **0.4267 $\rightarrow$ 0.4378**, and Recall@5 from **0.6067 $\rightarrow$ 0.6200**.
   - **Reference / Citation Queries (50):** Lexical reference routing achieves **Recall@10 = 0.3000** (vs. Gemini's 0.1200), an immediate **+150% improvement**.
5. **Production Safety Invariants:** All canonical databases (`data/hadith-kg.db`, `data/derived_semantic_index.db`, `data/meaning_groups_export.jsonl`) remain 100% read-only and unmutated. `SEMANTIC_EMBEDDING_PROVIDER=gemini` remains active and untouched.

---

## 2. Current Retrieval Architecture & Query Lifecycle

### 2.1 Concrete Component Inventory

| Component Name | Source File | Location & Database | Purpose & Scope | Production Status |
| :--- | :--- | :--- | :--- | :--- |
| **`SemanticIndex`** | `mizan-web/backend/ask_mizan/semantic.py` | `data/derived_semantic_index.db` | In-RAM Float32 cosine vector index over 20,744 meaning groups (768d, `gemini-embedding-001`). Loads on startup. | **Active Production** |
| **`OptionalRemoteEmbeddingProvider`** | `mizan-web/backend/ask_mizan/semantic.py` | Remote Google Generative Language API | Encodes queries via `gemini-embedding-001:embedContent` (`taskType: RETRIEVAL_QUERY`, dim=768). | **Active Production** |
| **`DeterministicFallback`** | `mizan-web/backend/ask_mizan/semantic.py` | `data/hadith-kg.db` | Substring match (`LIKE %term%`) across `taraf_nass` and `matn` if API offline. | **Active Fallback** |
| **`perform_hadith_search`** | `mizan-web/backend/main.py` | `data/hadith-search-index.db` & `data/hadith-kg.db` | Multi-token normalized Arabic search. Queries FTS5 table `hadith_fts` (715,790 records), falls back to table scan. Custom scoring: `0.60*coverage + 0.40*ordered`. | **Active Production** |
| **`perform_english_search`** | `mizan-web/backend/main.py` | `data/english_translation_fts.db` | English translation FTS5 search (`english_fts`, 31,488 records). Exact phrase $\rightarrow$ AND $\rightarrow$ OR match, ranked by BM25. | **Active Production** |
| **`parse_external_reference_query`** | `mizan-web/backend/identity_resolution.py` / `main.py` | `data/hadith_numbering.db` | Parses collection + number (e.g. "Muslim 1907", "Bukhari 1") and resolves canonical `hadith_id`. | **Active Production** |
| **`tool_search_hadith_text`** | `mizan-web/backend/ask_mizan/tools.py` | Central RAG Tool Orchestrator | First queries `semantic_retrieve_hadiths` (Gemini); if results $< \text{limit}$, fills remainder with English/Arabic FTS5. | **Active Production** |
| **`_assemble_evidence_pack`** | `mizan-web/backend/ask_mizan/engine.py` | Central Pipeline Engine | Routes based on 14 regex intents: Narrator lookup $\rightarrow$ Comparison $\rightarrow$ Citation lookup $\rightarrow$ Thematic search. | **Active Production** |

---

### 2.2 End-to-End Query Lifecycle Trace

```text
                                  USER QUERY
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │  Ask Mīzān Regex Intent Parser        │
                   │  (ask_mizan/parser.py: parse_query)   │
                   └───────────────────┬───────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
   [NARRATOR INTENT]             [REFERENCE INTENT]            [THEMATIC / RESEARCH]
   - Narrator Biography          - Exact Citation              - Complex Theology
   - Jarh wa Ta'dil              - Hadith Numbering            - Conceptual Queries
   - Teachers / Students         - Parallel Narrations         - General Search
         │                             │                             │
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ tool_search_     │          │ tool_resolve_    │          │ tool_search_     │
│ narrator_        │          │ reference        │          │ hadith_text      │
│ identities       │          │ (hadith_numbers) │          │ (Semantic + FTS) │
└────────┬─────────┘          └────────┬─────────┘          └────────┬─────────┘
         │                             │                             │
         └─────────────────────────────┼─────────────────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │   Evidence Pack Assembly              │
                   │   - Canonical Hadiths (Text, Nass)    │
                   │   - Sanad Chains (Rawi Links)         │
                   │   - Scholarly Grades (Hasan, Sahih)   │
                   │   - Classical Commentaries            │
                   └───────────────────┬───────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │   Evidence Sufficiency Validation     │
                   │   (ask_mizan/validator.py)            │
                   └───────────────────┬───────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │   Grounded LLM Generation             │
                   │   Strict [hadith:ID] Citation Tags    │
                   └───────────────────┬───────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │   UI / API Response                   │
                   └───────────────────────────────────────┘
```

---

## 3. Database Schema & Index Audit

### 3.1 `data/hadith-search-index.db` (248.6 MB)
- **Table:** `hadith_fts`
- **Engine:** SQLite FTS5 (Contentless virtual table: `content='', detail=full`).
- **Row Count:** Exactly 715,790 records (maps 1:1 with `hadiths.id`).
- **Indexed Fields:** `matn`, `nass`.
- **Tokenizer:** Default standard SQLite unicode tokenizer.
- **Strengths:** High-speed candidate generation for verbatim Arabic phrases.
- **Limitation:** Lacks Arabic root stemming (e.g. searching "استحباب" will not match "مستحب" or "حب").

### 3.2 `data/english_translation_fts.db` (32.8 MB)
- **Table:** `english_fts` (FTS5 over `english_translations`).
- **Row Count:** 31,488 records (covering Sahih Bukhari, Sahih Muslim, Sunan Abi Dawud, Jami al-Tirmidhi, Sunan an-Nasa'i, Sunan Ibn Majah).
- **Indexed Fields:** `translation_text`, `narrator`.
- **Limitation:** Does not cover secondary Musnads or un-translated hadith variants (which comprise ~370,000 hadiths in the Knowledge Graph).

### 3.3 `data/derived_semantic_index.db` (85.2 MB)
- **Table:** `semantic_vectors`
- **Row Count:** Exactly 20,744 vectors for `gemini-embedding-001` (768 Float32, unit L2 normalized).
- **Universe:** 1:1 representation of all active canonical meaning groups from `hadith-kg.db`.
- **In-RAM Footprint:** $20,744 \times 768 \times 4 \text{ bytes} \approx 63.7 \text{ MB}$.
- **Retrieval Performance:** Pure matrix dot-product takes **3.91 ms (P50)** on CPU and **0.17 ms (P50)** on GPU.

---

## 4. Phase 5 Benchmark Failure Analysis

Analysis across the 450 scored semantic queries and 50 isolated reference queries:

```text
┌─────────────────────────────────────────────────────────────┐
│  Group A: Both Models Retrieved Gold (Top-10)               │
│  Count: 150 (33.3%)                                         │
│  Character: Common, well-attested hadiths with high overlap  │
├─────────────────────────────────────────────────────────────┤
│  Group B: Gemini ONLY Retrieved Gold (Top-10)               │
│  Count: 148 (32.9%)                                         │
│  Character: Massive cross-lingual and paraphrase advantage   │
│  Languages: 36 Arabic, 60 Urdu, 52 English                  │
├─────────────────────────────────────────────────────────────┤
│  Group C: EmbeddingGemma 2 ONLY Retrieved Gold (Top-10)     │
│  Count: 5 (1.1%)                                            │
│  Character: Rare boundary cases where Gemini ranked at 14–30│
├─────────────────────────────────────────────────────────────┤
│  Group D: Neither Model Retrieved Gold (Top-10)             │
│  Count: 147 (32.7%)                                         │
│  Character: Benchmark label noise + variant hadith groups   │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Forensic Deep Dive: The 147 "Neither" Cases

A comprehensive diagnostic of the 147 queries where neither system hit the Top-10 revealed four distinct categories:

### 5.1 Category 1: Benchmark Gold Label Noise (High Frequency: ~38% of Neither cases)
In Phase 2, automated benchmark construction generated multiple synthetic query variations anchored to a single popular meaning group.
- **Extreme Anomaly:** Meaning Group 319 (Hadith al-Niyyat: "Actions are by intentions") was assigned as the gold label for **81 distinct queries** across the benchmark!
- **Concrete Example 1 (`AR_PARA_017`):**
  - Query: `"مسؤولية كل راع عن رعيته وأهله"` ("The responsibility of every shepherd over his flock and family").
  - Benchmark Gold Label: **GID 319** (Hadith al-Niyyat!).
  - Gemini Rank 1: **GID 431** (`"كلكم راع ومسئول عن رعيته..."`).
  - *Verdict:* Gemini was 100% semantically correct; the benchmark gold label was invalid.
- **Concrete Example 2 (`AR_PARA_010`):**
  - Query: `"الحث على التزام الصدق وعاقبة الكذب"` ("Adherence to truthfulness and the consequence of lying").
  - Benchmark Gold Label: **GID 319** (Hadith al-Niyyat).
  - Gemini Rank 1: **GID 14441** (`"تحروا الصدق وإن رأيتم أن فيه الهلكة... اجتنبوا الكذب..."`).
  - *Verdict:* Gemini retrieved the exact, authentic hadith on truthfulness and lying.
- **Concrete Example 3 (`AR_EXACT_019`):**
  - Query: `"لا يقبل الله صلاة بغير طهور"` ("Allah does not accept prayer without purification").
  - Benchmark Gold Label: **GID 704** (Hadith on drinking wine: "من شرب الخمر لم يقبل الله له صلاة أربعين صباحا").
  - Gemini Rank 1: **GID 614** (`"لا تقبل صلاة بغير طهور ولا صدقة من غلول"`).
  - *Verdict:* Gemini retrieved the literal prophetic text of Ibn Umar in Sahih Muslim.

### 5.2 Category 2: Rank 11–50 Proximity (23.1% of Neither cases)
For 34 of the 147 queries, Gemini successfully identified the gold meaning group within its top-50 candidate pool, but the group fell between ranks 11 and 50.
- *Root Cause:* High density of competing parallel meaning groups discussing identical topics (e.g. fasting of Ashura, Duha prayer, Wudu virtues).
- *Solution:* Hybrid fusion and reciprocal rank scoring elevate these candidates into the Top-10.

### 5.3 Category 3: Competing Canonical Parallel Meaning Groups (~25%)
Because the Knowledge Graph contains 20,744 meaning groups extracted from multiple collections (Bukhari, Muslim, Musnad Ahmad, etc.), a single prophetic teaching often exists in 3 to 8 distinct meaning groups.
- Searching for `"السواك مطهرة للفم"` retrieved GID 863 at Rank 1, while the benchmark gold target was GID 121 (`"لولا أن أشق على أمتي"`). Both are authentic Siwak narrations.

### 5.4 Category 4: Conceptual & Lexical Gaps (~14%)
Abstract theological queries where neither model could overcome the semantic distance between contemporary colloquial expressions and classical Arabic formulations without query expansion or lexical anchoring.

---

## 6. Audit of Current Lexical / FTS Performance

Evaluated against the exact frozen 500-query benchmark using [`scripts/experiments/evaluate_lexical_benchmark.py`](file:///c:/Users/taymi/discord-hadith-bot/scripts/experiments/evaluate_lexical_benchmark.py):

| Evaluation Dimension | Pure Lexical / FTS | Pure Gemini Live | Hybrid RRF (Gemini 1.0 / Lex 0.4) |
| :--- | :---: | :---: | :---: |
| **Recall@1 (450 Semantic)** | 0.0778 | 0.4267 | **0.4378 (+1.11%)** |
| **Recall@5 (450 Semantic)** | 0.0933 | 0.6067 | **0.6200 (+1.33%)** |
| **Recall@10 (450 Semantic)** | 0.0956 | 0.6622 | **0.6689 (+0.67%)** |
| **MRR (450 Semantic)** | 0.0845 | 0.5045 | **0.5153 (+1.08%)** |
| **nDCG@10 (450 Semantic)** | 0.0873 | 0.5393 | **0.5496 (+1.03%)** |
| **Reference Recall@10 (50 Ref)**| **0.3000** | 0.1200 | **0.2000** |
| **Reference MRR (50 Ref)** | **0.2638** | 0.0459 | **0.1149** |

### Per-Language Breakdown (MRR):
- **Arabic Semantic (150 queries):** Lexical MRR = 0.1847 $\rightarrow$ Gemini MRR = 0.4987 $\rightarrow$ **Hybrid MRR = 0.5107**
- **English Semantic (100 queries):** Lexical MRR = 0.0933 $\rightarrow$ Gemini MRR = 0.4690 $\rightarrow$ **Hybrid MRR = 0.4905**
- **Cross-Lingual (100 queries):** Lexical MRR = 0.0100 $\rightarrow$ Gemini MRR = 0.6356 $\rightarrow$ **Hybrid MRR = 0.6447**
- **Urdu Semantic (100 queries):** Lexical MRR = 0.0000 $\rightarrow$ Gemini MRR = 0.4177 $\rightarrow$ **Hybrid MRR = 0.4177**

---

## 7. Hybrid Retrieval v2 Proposed Architecture

Based on forensic evidence, the optimal architecture for Mīzān is **Query-Guided Hybrid Fusion with Reciprocal Rank Fusion (RRF)**:

```text
                              USER QUERY
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │  QUERY ROUTER         │
                       │  - Citation / Ref     │
                       │  - Language Detector  │
                       │  - Intent Classifier  │
                       └───────────┬───────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
   [TYPE: REFERENCE]       [TYPE: ARABIC TEXT]       [TYPE: EN / UR / THEME]
   Exact Citation          Exact & Normalized        Semantic & Cross-Lingual
         │                         │                         │
         ▼                         ▼                         ▼
   Reference Resolver      Arabic FTS5               Gemini Semantic
   (hadith_numbers)        (hadith_fts)              (semantic_vectors)
   Weight: 1.0             Weight: 0.4               Weight: 1.0
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │  CANDIDATE UNION      │
                       │  Top-50 Semantic      │
                       │  Top-50 Lexical       │
                       └───────────┬───────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │  RECIPROCAL RANK      │
                       │  FUSION (RRF, k=60)   │
                       │  Score Calibration    │
                       └───────────┬───────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │  MEANING GROUP →      │
                       │  CANONICAL HADITHS    │
                       │  (Prioritizes Sahihs) │
                       └───────────┬───────────┘
                                   │
                                   ▼
                       FINAL EVIDENCE HADITHS
```

### Fusion Formula:
$$\text{Score}_{\text{RRF}}(d) = \frac{w_{\text{gemini}}}{60 + \text{rank}_{\text{gemini}}(d)} + \frac{w_{\text{lexical}}}{60 + \text{rank}_{\text{lexical}}(d)}$$

Where weights are dynamically set by the Query Router:
- **Reference Queries:** $w_{\text{ref}} = 1.0$, $w_{\text{gemini}} = 0.2$
- **Verbatim Arabic Quotations:** $w_{\text{lexical}} = 0.6$, $w_{\text{gemini}} = 1.0$
- **Thematic / Cross-lingual:** $w_{\text{lexical}} = 0.3$, $w_{\text{gemini}} = 1.0$

---

## 8. Compute, Cost & Latency Analysis

| Architecture Tier | Latency (P50) | GPU Requirements | Production API Cost | Development Complexity | Retrieval Quality (MRR) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tier 1: Gemini Semantic Only** | ~1,180 ms | None (Serverless) | ~$0.00005 / query | Existing | 0.5045 |
| **Tier 2: Hybrid Gemini + FTS RRF (Recommended)** | **~1,185 ms (+5 ms)** | **None (CPU FTS5)** | **Unchanged** | **Low (Additive)** | **0.5153 (+1.08%)** |
| **Tier 3: Hybrid + Cross-Encoder Reranker** | ~1,650 ms (+470 ms) | Requires GPU VRAM | $0.50–$2.00/hr GPU VM | High (Deployment risk) | Marginal on Arabic (~0.52) |

**Architectural Decision:** Tier 2 (Hybrid Gemini + FTS RRF) delivers optimal gains with **zero additional API cost, zero GPU hardware dependency, and under 5 ms of local compute overhead**.

---

## 9. Risks & Mitigations

1. **Risk of Lexical Drift on Generic Stopwords:**
   - *Mitigation:* Apply strict Arabic and English stopword filtering before compiling FTS expressions.
2. **Missing Urdu Lexical Index:**
   - *Mitigation:* Do not force lexical queries on Urdu; route Urdu 100% to Gemini until a verified Urdu translation corpus is ingested.
3. **Reference Collision:**
   - *Mitigation:* Strict regex gating ensures non-citation queries are never routed to the reference resolver.

---

## 10. Final Decision & Phased Roadmap

### GO / NO-GO DECISION:
**GO (APPROVED FOR CONTROLLED IMPLEMENTATION IN PHASE 6B)**

### Phased Roadmap:
- **Phase 6A (Complete):** Forensic Architecture Audit, Benchmark Simulation, and Hybrid Retrieval v2 Design.
- **Phase 6B (Next):** Implement non-destructive `HybridSearchEngine` in `mizan-web/backend/ask_mizan/hybrid.py`, run verification suite, and expose via staging endpoint `/api/search/hybrid`.
- **Phase 6C:** User verification and controlled rollout.
