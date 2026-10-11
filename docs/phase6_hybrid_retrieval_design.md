# MĪZĀN AL-ḤADĪTH — HYBRID RETRIEVAL V2
## ENGINEERING SPECIFICATION & SYSTEM DESIGN

**Document:** Engineering Design & Implementation Specification  
**Subsystem:** Core Search & RAG Subsystem (`ask_mizan`)  
**Phase:** Phase 6 Architecture Design  
**Author:** Lead Retrieval/Search Architect  
**Status:** PROPOSED & APPROVED FOR PHASE 6B IMPLEMENTATION  
**Date:** 2026-10-08  

---

## 1. Objective & Design Philosophy

Hybrid Retrieval v2 combines:
1. **Google Gemini Live Semantic Embeddings (`gemini-embedding-001`):** Captures high-dimensional theological semantics, cross-lingual equivalence (Urdu/English $\rightarrow$ Arabic), and contextual paraphrases across 20,744 precomputed meaning group vectors.
2. **SQLite FTS5 Lexical Search (`hadith_fts` & `english_fts`):** Delivers exact keyword and verbatim phrase matching with zero semantic dilution.
3. **Deterministic Reference Routing (`hadith_numbers`):** Resolves structured book citations (e.g., "Bukhari 1", "Muslim 1907") with 100% precision.

### Core Design Rules:
- **Zero Mutation:** Canonical databases (`hadith-kg.db`, `derived_semantic_index.db`) remain strictly read-only.
- **Graceful Fallback:** If the remote Gemini API is unreachable or times out, the system automatically degrades to Lexical FTS5 without error.
- **Deterministic Fusion:** Uses Reciprocal Rank Fusion (RRF) with calibrated weights, avoiding fragile raw score normalization across disparate vector spaces.

---

## 2. Component Architecture

```text
                             USER INPUT (q)
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │       QUERY ROUTER            │
                   │  - Intent Classifier          │
                   │  - Citation Pattern Matcher   │
                   │  - Language Detector          │
                   └───────────────┬───────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
  [REFERENCE ROUTE]          [LEXICAL FTS ROUTE]        [SEMANTIC ROUTE]
  - Bukhari / Muslim #       - Arabic FTS5              - Gemini Remote API
  - hadith_numbers table     - English FTS5             - In-RAM 20,744 Index
  - Weight: w_ref = 1.0      - Weight: w_lex = 0.4      - Weight: w_sem = 1.0
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │    CANDIDATE GENERATION       │
                   │    - Top-50 Semantic GIDs     │
                   │    - Top-50 Lexical GIDs      │
                   │    - Top-1 Reference GID      │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │  RECIPROCAL RANK FUSION (RRF) │
                   │  k = 60, weighted sum         │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │    CANONICAL EXPANSION        │
                   │    group_id → hadith_id       │
                   │    Prioritize Bukhari/Muslim  │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                   FINAL EVIDENCE HADITH RESULTS
```

---

## 3. Detailed Algorithmic Specifications

### 3.1 Query Routing & Parameter Calibration

The Query Router inspects query string $q$ and emits configuration tuple $(w_{\text{sem}}, w_{\text{lex}}, \text{is\_ref})$:

```python
def route_query_parameters(query_text: str) -> Tuple[float, float, bool]:
    clean = query_text.strip()
    
    # Check 1: Citation pattern (e.g. Bukhari 1, Muslim 1907)
    if is_citation_pattern(clean):
        return (0.2, 1.0, True) # Favor reference/lexical heavily
        
    # Check 2: Verbatim Arabic quotation (quoted or >= 4 distinctive Arabic words)
    if is_verbatim_arabic(clean):
        return (1.0, 0.6, False) # Elevate lexical weight for verbatim text
        
    # Check 3: Standard English / Urdu / Thematic research query
    return (1.0, 0.3, False) # Gemini semantic primary, lexical auxiliary
```

### 3.2 Candidate Generation Layer

1. **Semantic Candidate Generator:**
   - Vector Dot-Product: $\mathbf{s} = \mathbf{V}_{\text{corpus}} \cdot \mathbf{q}_{\text{gemini}}$
   - Yields sorted candidates: $C_{\text{sem}} = [(g_1, r_1), (g_2, r_2), \dots, (g_{50}, r_{50})]$
2. **Lexical Candidate Generator:**
   - Arabic: Queries `hadith_fts MATCH fts_expr`, maps matched hadiths to `meaning_groups.id` via `hadith_to_group`, aggregates frequency:
     $$\text{Score}_{\text{lex}}(g) = \sum_{h \in \text{matches}(g)} \frac{1}{\sqrt{\text{rank}(h)}}$$
   - English: Queries `english_fts MATCH fts_expr`, aggregates matching hadith groups.
   - Yields sorted candidates: $C_{\text{lex}} = [(g_1, r_1), (g_2, r_2), \dots, (g_{50}, r_{50})]$

### 3.3 Dynamic Reciprocal Rank Fusion (RRF)

$$\text{RRF\_Score}(d) = \sum_{m \in \{\text{sem}, \text{lex}, \text{ref}\}} \frac{w_m}{k + \text{rank}_m(d)}$$

Where:
- $k = 60$ (smoothing constant preventing high-rank outliers from dominating).
- If candidate $d$ does not appear in subsystem $m$, its term is $0$.
- Candidates are sorted by descending $\text{RRF\_Score}(d)$ to produce top-$K$ meaning groups.

### 3.4 Meaning Group to Canonical Hadith Expansion

```sql
SELECT h.id, h.book_id, h.no_inbook, h.taraf_nass, h.matn, b.english_name
FROM hadiths h
LEFT JOIN books b ON b.id = h.book_id
WHERE h.group_id = ?
ORDER BY 
    CASE WHEN h.book_id IN (1, 2) THEN 0 ELSE 1 END, -- Prioritize Bukhari & Muslim
    h.book_id ASC,
    h.no_inbook ASC
LIMIT ?;
```

---

## 4. Planned Implementation Layout (Phase 6B)

The implementation will reside in dedicated, isolated files:
- **`mizan-web/backend/ask_mizan/hybrid.py`:** Core `HybridSearchEngine` class implementing the multi-retriever orchestrator and RRF fusion.
- **Staging Endpoint in `mizan-web/backend/main.py`:**
  - `GET /api/search/hybrid`: Exposes Hybrid Retrieval v2 for frontend testing without touching `/api/hadith/search` or `/api/search/semantic`.
- **Regression Verification Suite:**
  - `tests/test_hybrid_retrieval_v2.py`: Automated regression tests verifying latency, fallback behavior, reference routing, and invariant immutability.

---

## 5. Non-Destructive Guarantees

- **Production Provider:** `SEMANTIC_EMBEDDING_PROVIDER=gemini` remains 100% active.
- **SQLite Safety:** Zero write transactions; strict `query_only = ON` pragma enforced.
- **Deployment Safety:** Zero modifications to existing `/api/hadith/search` or `/api/search/semantic` until explicit validation.
