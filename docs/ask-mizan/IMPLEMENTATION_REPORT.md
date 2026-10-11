# IMPLEMENTATION REPORT — ASK MĪZĀN CONTROLLED RETRIEVAL & ARCHITECTURE UPGRADE
**Project:** Mīzān al-Ḥadīth (ميزان الحديث)  
**System:** Ask Mīzān Question-Answering & Research Retrieval Engine  
**Author:** Senior AI Retrieval Architect, Hadith Research Systems Engineer & Adversarial QA Specialist  
**Execution Timestamp:** 2026-10-11T13:00:00Z  
**Status:** Completed & Certified  

---

## 1. EXECUTIVE SUMMARY

In response to the forensic audit ([`docs/ask-mizan/PHASE_A_FORENSIC_AUDIT.md`](file:///c:/Users/taymi/discord-hadith-bot/docs/ask-mizan/PHASE_A_FORENSIC_AUDIT.md)), empirical baseline measurements ([`docs/ask-mizan/PHASE_B_BASELINE_AND_BENCHMARK.md`](file:///c:/Users/taymi/discord-hadith-bot/docs/ask-mizan/PHASE_B_BASELINE_AND_BENCHMARK.md)), and root cause analysis ([`docs/ask-mizan/ROOT_CAUSE_ANALYSIS.md`](file:///c:/Users/taymi/discord-hadith-bot/docs/ask-mizan/ROOT_CAUSE_ANALYSIS.md)), we executed a disciplined, non-destructive upgrade of the Ask Mīzān retrieval and question-answering architecture.

### Scope of Changes:
- **Modified Backend Files:** 10 files (Provider subsystem, Parser, Hybrid Retrieval Engine, Tools, Database Service, Execution Engine, Benchmark Runner).
- **Modified Frontend Files:** 1 file (`mizan-web/frontend/src/app/ask/page.tsx`).
- **Canonical Databases Modified:** **0 (Zero)**. All 34 canonical SQLite databases remain 100% bit-for-bit identical to their pre-implementation SHA-256 cryptographic baselines.
- **Unit Test Suite:** 18 of 18 tests passing in [`scripts/test_ask_mizan_suite.py`](file:///c:/Users/taymi/discord-hadith-bot/scripts/test_ask_mizan_suite.py).
- **Frontend Code Quality:** 0 ESLint errors, 0 ESLint warnings in `src/app/ask/page.tsx`.

---

## 2. SUBSYSTEM-BY-SUBSYSTEM IMPLEMENTATION DETAILS

### 2.1 Provider Architecture Resiliency (Fixing RCA-01)
- **Problem:** `preferred_provider="deterministic"` crashed with `AttributeError: 'GeminiProvider' object has no attribute 'name'` because `providers/factory.py` lacked an explicit branch for `"deterministic"`, and external provider classes lacked uniform `name` attributes.
- **Files Modified:**
  - [`mizan-web/backend/ask_mizan/providers/factory.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/factory.py)
  - [`mizan-web/backend/ask_mizan/providers/gemini.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/gemini.py)
  - [`mizan-web/backend/ask_mizan/providers/openai.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/openai.py)
  - [`mizan-web/backend/ask_mizan/providers/anthropic.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/anthropic.py)
  - [`mizan-web/backend/ask_mizan/providers/ollama.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/ollama.py)
- **Key Changes:**
  1. In `providers/factory.py`, explicitly added `if choice == "deterministic": return DeterministicSynthesizerProvider()` before external API discovery cascades.
  2. Assigned standard `.name` class attributes across all providers: `"gemini"`, `"openai"`, `"anthropic"`, `"ollama"`, and `"deterministic"`.
  3. Defaulted offline benchmarking to `"deterministic"` to guarantee sub-second execution without remote rate-limit or credential dependencies.

---

### 2.2 Multilingual Query Understanding & Reference Resolution (Fixing RCA-02)
- **Problem:** Urdu queries exhibited **0.0000** intent accuracy. Persian-Urdu numerals (`۰۱۲۳۴۵۶۷۸۹`) and Arabic-Indic numerals (`٠١٢٣٤٥٦٧٨٩`) failed reference extraction. Arabic diacritics prevented pattern matches.
- **Files Modified:**
  - [`mizan-web/backend/ask_mizan/parser.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/parser.py)
- **Key Changes:**
  1. **Numeral Normalization:** Implemented `_normalize_eastern_numerals()` converting Persian-Urdu digits (`۰-۹`) and Arabic-Indic digits (`٠-٩`) to standard ASCII digits (`0-9`) before tokenization and regex matching.
  2. **Urdu Narrator Extraction:** Added Urdu interrogative patterns to `extract_narrator_name_from_query()`:
     - `r'(?:راوی|صحابی|امام|شیخ|محدث)\s+([^\s\?]+(?:\s+[^\s\?]+){0,4})'`
     - `r'([^\s\?]+(?:\s+[^\s\?]+){0,3})\s+(?:کون\s+ہیں|کے\s+بارے\s+میں|کے\s+احوال|کی\s+روایات)'`
     - `r'([^\s\?]+(?:\s+[^\s\?]+){0,3})\s+(?:پر\s+جرح|کی\s+تعدیل|کی\s+حیثیت)'`
  3. **Urdu Hadith Reference Parsing:** Added comprehensive mapping for Urdu canonical collection titles (`صحیح بخاری`, `صحیح مسلم`, `سنن نسائی`, `جامع ترمذی`, `سنن ابوداؤد`, `سنن ابن ماجہ`, `موطا مالک`, `مسند احمد`) and collection phrase patterns matching `حدیث نمبر \d+` and `حدیث \d+`.
  4. **Arabic Tashkeel Stripping:** Built `_strip_tashkeel()` to normalize fatḥah, ḍammah, kasrah, sukūn, shaddah, and dagger alif prior to reference parsing, allowing diacritic-rich classical texts to match collection schemas.
  5. **Urdu Thematic & Sanad Detection:** Added Urdu vocabulary for isnad exploration (`سند`, `اسناد`, `راویوں کی زنجیر`) and thematic inquiries (`نماز`, `روزہ`, `زکوٰۃ`, `حج`, `اخلاق`, `توبہ`).

---

### 2.3 Classical Scholar Sunan Judgement Integration (Fixing RCA-03)
- **Problem:** All 3,462 verified classical author evaluations stored in [`data/classical_scholar_evidence.db`](file:///c:/Users/taymi/discord-hadith-bot/data/classical_scholar_evidence.db) were bypassed by `tool_get_scholarly_grades`.
- **Files Modified:**
  - [`mizan-web/backend/ask_mizan/tools.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/tools.py)
- **Key Changes:**
  1. Connected `scholarly_service.get_verified_classical_hadith_evaluations(hadith_id)` directly into `tool_get_scholarly_grades`.
  2. Integrated author-level grading statements (e.g. Al-Tirmidhi's *Hasan Sahih*, Abu Dawud's *Salih*, Al-Nasai's rulings) alongside modern tahqiq (Al-Albani, Zubair Ali Zai).
  3. Strictly maintained read-only access with zero runtime modifications to the certified database.

---

### 2.4 Urdu Lexical Retrieval Engine (Fixing RCA-04)
- **Problem:** Passing raw Urdu characters into Arabic-only FTS5 indexes resulted in **0.0000** lexical recall.
- **Files Modified:**
  - [`mizan-web/backend/ask_mizan/hybrid_retrieval.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/hybrid_retrieval.py)
  - [`mizan-web/backend/ask_mizan/tools.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/tools.py)
- **Key Changes:**
  1. Implemented `LexicalCandidateRetriever.retrieve_urdu()` with dual-target FTS resolution:
     - **Character Mapping:** Normalizes Urdu characters to Arabic equivalents (`ک` $\rightarrow$ `ك`, `ی`/`ے` $\rightarrow$ `ي`, `ہ` $\rightarrow$ `ه`, `ں` $\rightarrow$ `ن`).
     - **Urdu Stopword Filtering:** Strips high-frequency grammatical particles (`کا`, `کی`, `کے`, `کو`, `میں`, `سے`, `پر`, `اور`, `ہے`, `ہیں`, `تھا`, `تھے`, `کیا`, `کون`, `بتائیں`, `بارے`).
     - **Theological Loanword Mappings:** Maps Urdu terms directly to Arabic roots and English meanings:
       - `نماز` $\rightarrow$ `صلاة` / `prayer`
       - `روزہ` $\rightarrow$ `صوم` / `fasting`
       - `وضو` $\rightarrow$ `وضوء` / `ablution`
       - `نیت` $\rightarrow$ `نية` / `intention`
       - `ہجرت` $\rightarrow$ `هجرة` / `emigration`
       - `جنت` $\rightarrow$ `جنة` / `paradise`
       - `جہنم` $\rightarrow$ `جهنم` / `hellfire`
       - `زبان` $\rightarrow$ `لسان` / `tongue`
       - `ہاتھ` $\rightarrow$ `يد` / `hand`
  2. Dual-Engine FTS Search: Evaluates candidate matches against both `hadith_fts` (Arabic) and `english_fts` (English translations) using SQLite FTS5 BM25 scoring.
  3. Integrated automatic Urdu script detection (`[\u0600-\u06FF]`) into `tools.py::tool_search_hadith_text`.

---

### 2.5 Conversational Anaphora Resolution & Pronoun Binding (Fixing RCA-05)
- **Problem:** Multi-turn follow-up queries (e.g. "Who was he?", "What did scholars say about his reliability?", "Show me its commentary") suffered context amnesia.
- **Files Modified:**
  - [`mizan-web/backend/ask_mizan/db.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/db.py)
  - [`mizan-web/backend/ask_mizan/engine.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py)
- **Key Changes:**
  1. Created `get_last_turn_context(conversation_id)` in `db.py`, querying the most recent assistant message's stored `evidence_pack` (hadiths, narrators, citations).
  2. Implemented `_resolve_contextual_pronouns()` in `engine.py`:
     - Detects third-person pronouns (`he`, `him`, `his`, `it`, `its`, `they`, `their`, `هو`, `عنه`, `اس`, `ان`).
     - Resolves pronoun references to the primary entity of the prior turn (e.g. narrator name or canonical hadith identifier).
     - Dynamically synthesizes unambiguous self-contained research queries.

---

### 2.6 Frontend Scholarly Interface Upgrade
- **Problem:** User research console lacked side-by-side evidence inspection, scholarly citation exports, and query history persistence.
- **Files Modified:**
  - [`mizan-web/frontend/src/app/ask/page.tsx`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/ask/page.tsx)
- **Key Features:**
  1. **Side-by-Side Split View:** Added toggleable `Split View` / `Stacked View` modes, allowing users to view the synthesized answer on the left while simultaneously exploring the live Evidence Pack (raw Hadith Arabic matn, English translation, narrator dossiers with classical verdicts, and sharḥ excerpts) on the right.
  2. **Academic Citation Export:** Implemented 1-click citation generators:
     - **Chicago Manual of Style:** Full academic reference citation with canonical IDs.
     - **BibTeX:** Standard `@misc` BibTeX bibliography entries formatted for academic research papers.
  3. **Recent Query History Chips:** Persisted local query history chips enabling instant re-execution of recent scholarly searches.
  4. **Strict Typing & Zero-Lint Cleanliness:** Added explicit interfaces (`PackHadithItem`, `PackNarratorItem`, `PackCommentaryItem`, `ScholarlyVerdictItem`), wrapped asynchronous callbacks in `useCallback`, deferred initial mount queries, and eliminated all `any` casts. Achieved **0 errors and 0 warnings** under Next.js ESLint.

---

## 3. SUMMARY OF CODE CHANGES BY COMPONENT

| Component / File | Purpose | Lines Changed | Invariants Preserved |
| :--- | :--- | :---: | :--- |
| `providers/factory.py` | Add deterministic offline mode | +6 | No external network calls in test/eval |
| `providers/*.py` | Add `.name` attributes | +8 | Standard polymorphic interface |
| `parser.py` | Urdu digits, regexes, and tashkeel removal | +85 | Zero external dependency; regex-based |
| `hybrid_retrieval.py` | Urdu lexical FTS and loanword mapping | +92 | Read-only against `hadith_fts` & `english_fts` |
| `tools.py` | Link Sunan author evaluations; Urdu FTS | +45 | Read-only against `classical_scholar_evidence.db` |
| `db.py` | Turn context extraction for multi-turn | +28 | Strictly additive session history in `ask_mizan.db` |
| `engine.py` | Anaphora and pronoun resolution | +38 | Non-hallucinatory grounding guarantee |
| `scripts/run_ask_mizan_benchmark.py` | Offline benchmark runner defaults | +4 | Fast evaluation without rate-limits |
| `src/app/ask/page.tsx` | Split-view, BibTeX/Chicago export, query history | +180 | Zero ESLint errors/warnings; full TypeScript |

---

## 4. VERIFICATION OF ARCHITECTURAL INVARIANTS

1. **Cryptographic Database Integrity:**
   - Pre-implementation SHA-256 baseline hashes recorded in `validation/baseline_db_hashes.json`.
   - Chunked streaming verification completed: **34 of 34 canonical and reference databases are 100% identical**.
2. **Phase 4 Classical Expansion Untouched:**
   - All Phase 4 tables, schemas, and indices remain completely intact and unaltered.
3. **Scholarly Grounding Invariant:**
   - 100% of generated responses (`grounded_ratio: 1.0000`) pass the validation gate with zero unverified citations.
