# PHASE B — BASELINE MEASUREMENT & STRATIFIED BENCHMARK REPORT
**Project:** Mīzān al-Ḥadīth (ميزان الحديث)  
**Target System:** Ask Mīzān Question-Answering & Retrieval Subsystem  
**Benchmark Version:** `ask_mizan_stratified_benchmark_v1.0`  
**Dataset Artifact:** [`data/benchmarks/ask_mizan_stratified_benchmark_v1.jsonl`](file:///c:/Users/taymi/discord-hadith-bot/data/benchmarks/ask_mizan_stratified_benchmark_v1.jsonl)  
**Execution Timestamp:** 2026-10-10T17:49:04Z  

---

## 1. STRATIFIED BENCHMARK DATASET COMPOSITION

To eliminate blind optimization and evaluate all scholarly research requirements, we constructed a versioned 12-category stratified benchmark consisting of **120 total annotated test cases**:
- **Development Split (DEV):** 60 queries (used strictly for tuning, error reproduction, and intermediate measurements).
- **Held-out Split (TEST):** 60 queries (unseen during implementation tuning, reserved strictly for acceptance certification).

### Category Coverage (10 queries per category: 5 DEV / 5 TEST):
1. **Category A — Exact Hadith references:** Known collection and Hadith numbers, in-book vs catalog numbering (Bukhari 1, Muslim 1907, Nasai 348, Ibn Majah 1986).
2. **Category B — Arabic queries:** Diacritic-rich phrases (`إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ`), orthographic variants (`علي` vs `على`), legal maxims (`لا ضرر ولا ضرار`).
3. **Category C — Urdu queries:** Urdu-script questions, Urdu Hadith numbering, Urdu questions regarding narrators (`ابو ہریرہ`, `عبدالرحمن المسلی`) and tahqiq.
4. **Category D — English queries:** Semantic concepts, english quotations, requests for scholarly evidence.
5. **Category E — Narrator research:** Rawi names, kunyas, tabaka, jarh wa ta'dil, and transmission relations.
6. **Category F — Scholarly grading and criticism:** Hadith-level grades (Al-Albani, Zubair Ali Zai, classical author statements in Tirmidhi/Abu Dawud) vs narrator evaluations.
7. **Category G — Commentary retrieval:** Classical sharh passages from Fath al-Bari and Umdat al-Qari.
8. **Category H — Isnad and transmission evidence:** Sanad chain extraction, companion identity, transmission integrity.
9. **Category I — Cross-reference and numbering:** Multi-edition crosswalks (Darussalam vs Shamela vs In-book).
10. **Category J — Ambiguous and unanswerable questions:** Non-existent identifiers (e.g. Bukhari 999999), under-specified queries, anachronistic questions requiring safe refusal/abstention.
11. **Category K — Cross-lingual retrieval:** Urdu and English questions seeking classical Arabic Hadith sources.
12. **Category L — Multi-part research questions:** Compound queries combining text, isnad, grading, and commentary.

---

## 2. EMPIRICAL BASELINE METRICS (DEV SPLIT: 60 QUERIES)

Run command: `python scripts/run_ask_mizan_benchmark.py dev`  
Raw run output: [`data/benchmarks/runs/benchmark_run_dev.json`](file:///c:/Users/taymi/discord-hadith-bot/data/benchmarks/runs/benchmark_run_dev.json)

### 2.1 Overall System Baseline
| Metric | Baseline Score | Target Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Recall@1** | **0.5833** (35/60) | $\ge 0.7500$ | Sub-optimal |
| **Recall@5** | **0.6000** (36/60) | $\ge 0.8500$ | Sub-optimal |
| **Mean Reciprocal Rank (MRR)** | **0.5889** | $\ge 0.7800$ | Sub-optimal |
| **Intent Classification Accuracy** | **0.6667** (40/60) | $\ge 0.9000$ | Defective in non-English |
| **Grounded Response Ratio** | **1.0000** (60/60) | $1.0000$ | Preserved (Zero hallucination) |
| **Median Response Latency** | **1,969.59 ms** | $\le 2,500$ ms | Pass |
| **P95 Response Latency** | **4,782.45 ms** | $\le 5,000$ ms | Pass |

### 2.2 Baseline Breakdown by Language
| Language | Query Count | Recall@1 | Recall@5 | MRR | Intent Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **English (`en`)** | 39 | **0.6154** | **0.6410** | **0.6154** | **0.8718** |
| **Arabic (`ar`)** | 13 | **0.6154** | **0.6154** | **0.6154** | **0.4615** |
| **Urdu (`ur`)** | 8 | **0.3750** | **0.3750** | **0.4167** | **0.0000** |

---

## 3. CRITICAL BASELINE FINDINGS

1. **Urdu Complete Intent Blindness:**
   - Urdu Intent Accuracy is exactly **0.0000** (0/8).
   - In `parser.py`, zero regular expressions or NLP patterns exist for Urdu query structures. Queries such as `"راوی ابو ہریرہ کے بارے میں بتائیں"` or `"صحیح بخاری حدیث نمبر 1 کا متن اور ترجمہ"` are silently misclassified into `THEMATIC` or `GENERAL_RESEARCH`.
   - The query router has zero knowledge of Urdu numerals (`۱, ۲, ۳...`), resulting in total reference resolution failure for Urdu-numbered queries.

2. **Arabic Intent Deficit:**
   - Arabic Intent Accuracy is only **0.4615** (6/13).
   - Queries with tashkeel or diacritics, or Arabic phrasing for collection numbering (`صحيح البخاري رقم 8`), fail regex matches and fall back into unstructured text search.

3. **Untapped Classical Evidence:**
   - All 3,462 verified classical author grading judgements in `classical_scholar_evidence.db` are currently bypassed during Ask Mīzān execution because `tool_get_scholarly_grades` does not query `classical_hadith_evaluations`.

4. **Zero Hallucination Invariant Verified:**
   - Grounded Response Ratio is **100%** (`1.0000`), and zero unsupported citations were generated, confirming that the validator gate strictly rejects ungrounded tokens.
