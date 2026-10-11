# MĪZĀN AL-ḤADĪTH — SYSTEM CAPABILITIES & BENCHMARKS

**Document Identifier:** `docs/overview/system-capabilities.md`  
**System Baseline:** Verified Repository & Database Telemetry  

---

## 1. Computational Scale & Data Capacity

Mīzān al-Ḥadīth is architected to operate at institutional and research scale, serving high-concurrency requests over SQLite databases with sub-millisecond to low-millisecond query execution.

```
       +--------------------------------------------------------------+
       |               MĪZĀN AL-ḤADĪTH DATA METRICS                   |
       +--------------------------------------------------------------+
       |  Canonical Hadith Records:            715,790                |
       |  Biographical Narrator Profiles:       49,844                |
       |  Historical Scholars Cataloged:         1,015                |
       |  Jarḥ wa Taʿdīl Critical Opinions:    127,863                |
       |  Directed Isnād Network Edges:        298,655                |
       |  Transmission Sequences Recorded:     577,024                |
       |  Transmitter-Sequence Relations:    4,414,211                |
       |  Numbering Concordance Mappings:       95,598                |
       |  Verified English Translations:        31,488                |
       |  Classical Commentary Excerpts:         1,202                |
       |  Classical Primary Evaluations:         3,462                |
       |  Modern Analytical Verifications:      14,398                |
       +--------------------------------------------------------------+
```

---

## 2. Verified Subsystem Benchmarks

> [!NOTE]
> The performance metrics below represent empirical measurements captured during Phase 18 and Phase 7 production integration testing on the local benchmark hardware (Intel Core i7 / AMD equivalent, NVMe SSD storage).

### 2.1 Retrieval & Database Latency
- **Direct Primary Key Hadith Lookup (`/api/hadith/{id}`):** `< 4 ms`
- **Isnād Network Subgraph Traversal (`/api/isnad/{id}`):** `< 12 ms`
- **FTS5 Arabic Full-Text Search (Top 50 Results):** `< 25 ms`
- **Numbering Crosswalk Concordance Resolution (`/api/numbering/resolve`):** `< 6 ms`
- **Classical Commentary Retrieval (`/api/hadith/{id}/commentaries`):** `< 8 ms`

### 2.2 Ask Mīzān Pipeline Latency & Grounding
- **Exact Reference Parsing & Routing:** `< 2 ms`
- **Multi-Tier Candidate Retrieval:** `< 45 ms`
- **Evidence Assembly & Deduplication:** `< 15 ms`
- **Online LLM Generation (Gemini 2.5 Flash):** `650 ms – 1,400 ms`
- **Deterministic Citation Validation:** `< 12 ms`
- **Grounding Citation Accuracy:** `100%` (0 hallucinated citations admitted; ungrounded statements flagged or purged)

---

## 3. High-Concurrency Connection Safety

Under the centralized handle manager (`db_manager.py`), all database interactions obey:
1. **Zero Handle Leaks:** Verified by `ConnectionTracker` telemetry with automated unit assertion in test suites.
2. **Read-Only Concurrency:** Canonical databases open with immutable `file:...mode=ro` flags, preventing OS-level file lock contention during read bursts.
3. **Write Isolation:** Only `data/ask_mizan.db` and `data/research_workspace.db` allow write transactions, utilizing SQLite Write-Ahead Logging (WAL) mode for non-blocking concurrent reads and writes.
