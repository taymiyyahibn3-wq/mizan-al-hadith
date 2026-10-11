# PHASE A — FORENSIC AUDIT OF THE EXISTING ASK MĪZĀN SYSTEM
**Project:** Mīzān al-Ḥadīth (ميزان الحديث)  
**Subsystem:** Ask Mīzān Question-Answering & Research Retrieval Subsystem  
**Audit Timestamp:** 2026-10-10T17:45:00+05:30  
**Audit Mode:** Complete Codebase Inspection, Static Analysis & Empirical Test Reproduction  
**Auditor:** Senior AI Retrieval Architect & Adversarial QA Specialist  

---

## 1. INVENTORY OF ACTUAL FILES AND RESPONSIBILITIES

### 1.1 Backend Core (`mizan-web/backend/ask_mizan/`)
- [`config.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/config.py): Configuration, environment resolution (`ASK_MIZAN_PROVIDER`, `ASK_MIZAN_MODEL`, `MIZAN_HYBRID_MODE`), read-only DB paths for Docker `/data/` and local repo root fallback.
- [`db.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/db.py): Conversation turn persistence and audit logging into `data/ask_mizan.db` (additive, non-canonical store).
- [`models.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/models.py): Strongly-typed Pydantic V2 schemas for 14 research intents (`QueryIntent`), `EvidencePack`, `EvidenceHadith`, `EvidenceNarrator`, `EvidenceCommentary`, `EvidenceGrade`, `EvidenceSanad`, `CitationItem`, `ResearchAction`, `AskRequest`, `AskResponse`, `FeedbackRequest`.
- [`parser.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/parser.py): Query classification and regex-based entity/reference extractor for English and basic Arabic.
- [`engine.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py): Central orchestration pipeline coordinating `parse_query` -> `_assemble_evidence_pack` -> `validate_evidence_sufficiency` -> `provider.generate_response` -> `validate_and_bind_citations` -> audit logging.
- [`tools.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/tools.py): Deterministic read-only SQLite retrieval tools (`tool_resolve_reference`, `tool_get_hadith_detail`, `tool_search_hadith_text`, `tool_get_narrator_dossier`, `tool_get_isnad_chain`, `tool_get_commentaries`, `tool_get_scholarly_grades`, `tool_get_parallel_narrations`, `tool_compare_hadiths`).
- [`validator.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/validator.py): Pre-generation sufficiency gate (`validate_evidence_sufficiency`) and post-generation citation binding & hallucination stripper (`validate_and_bind_citations`).
- [`semantic.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/semantic.py): In-RAM semantic index loader and cosine vector search against 20,744 canonical meaning groups in `data/derived_semantic_index.db`.
- [`hybrid_retrieval.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/hybrid_retrieval.py): Reciprocal Rank Fusion (RRF k=60) combining Gemini semantic candidates, Arabic/English lexical FTS5 candidates, and structured reference candidates.
- [`hybrid_service.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/hybrid_service.py): Production integration facade managing runtime modes (`off`, `shadow`, `canary`, `on`) with CRC32 query hashing for canary rollout.
- [`router.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/router.py): FastAPI APIRouter mounting `/api/ask`, `/api/ask/stream`, `/api/ask/health`, `/api/ask/conversations/{id}`, `/api/ask/feedback`.
- [`providers/`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/): LLM abstraction layer containing `base.py`, `factory.py`, `deterministic.py`, `gemini.py`, `openai.py`, `anthropic.py`, `ollama.py`.

### 1.2 Frontend Core (`mizan-web/frontend/`)
- [`src/app/ask/page.tsx`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/ask/page.tsx): Main Ask Mīzān user interface with query input, suggested research questions, answer cards, verified citation chips, research action links, expandable evidence drawer, and feedback rating.
- [`src/app/components/CitationChip.tsx`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/components/CitationChip.tsx): Interactive citation badge rendering links to `/hadith/{id}`, `/narrators/{id}`, `/commentary/{id}`, `/research-workspace`.
- [`src/lib/api.ts`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/lib/api.ts): Typed client SDK for `/api/ask` and `/api/ask/feedback`.

---

## 2. CURRENT END-TO-END QUERY FLOW

```
User Query (Frontend /api/ask)
       │
       ▼
1. Conversation & Message ID (`db.py`)
       │
       ▼
2. Query Parsing & Intent Classification (`parser.py`)
   ├── Regex collection matching -> `HADITH_LOOKUP` / `NUMBERING`
   ├── Narrator patterns -> `NARRATOR_LOOKUP` / `NARRATOR_BIOGRAPHY` / `JARH_TADIL` / `TEACHERS_STUDENTS`
   ├── Commentary keywords -> `COMMENTARY`
   ├── Hadith grading keywords -> `HADITH_GRADING`
   ├── Matn comparison keywords -> `HADITH_COMPARISON` / `SOURCE_COMPARISON`
   └── Fallback -> `THEMATIC` / `GENERAL_RESEARCH`
       │
       ▼
3. Deterministic Evidence Assembly (`engine.py::_assemble_evidence_pack` -> `tools.py`)
   ├── If Narrator Intent: Search identity -> get narrator dossier + aqwal + teachers/students
   ├── If Comparison Intent: Resolve references -> get hadith details -> compare texts & chains
   ├── If Reference Intent: Resolve reference -> get hadith detail + sanad + grades + commentary
   └── If Thematic Intent: Call `tool_search_hadith_text` (English FTS then Arabic FTS)
       │
       ▼
4. Sufficiency Gate (`validator.py::validate_evidence_sufficiency`)
   ├── If insufficient -> Short-circuit return refusal reason (Refuse to hallucinate)
   └── If sufficient -> Proceed to LLM Synthesis
       │
       ▼
5. LLM Synthesis (`providers/factory.py` -> `gemini.py` or fallback `deterministic.py`)
   └── Prompt includes SYSTEM_GROUNDING_PROMPT + JSON Evidence Pack
       │
       ▼
6. Citation Binding & Hallucination Guard (`validator.py::validate_and_bind_citations`)
   ├── Scans `[hadith:X]`, `[narrator:Y]`, `[commentary:Z]`, `[grade:W]`
   ├── Strips tokens NOT in Evidence Pack
   └── Formats valid tokens as interactive Markdown links
       │
       ▼
7. Persistence & Telemetry (`db.py::save_assistant_turn`)
       │
       ▼
8. Response to User (`AskResponse` JSON with answer, citations, actions, metrics)
```

---

## 3. MODEL AND PROVIDER CONFIGURATION

- Default provider: `gemini` (via environment `ASK_MIZAN_PROVIDER`).
- Default model: `gemini-1.5-flash` or `gemini-1.5-pro` (auto-selected).
- Offline fallback: `DeterministicSynthesizerProvider` (100% offline, guaranteed factual assembly).
- Hybrid retrieval mode: `MIZAN_HYBRID_MODE=off` by default, supports `shadow`, `canary` (10%), `on`.

---

## 4. CANONICAL DATA DEPENDENCIES & IMMUTABILITY

All canonical databases reside in `data/` and must remain strictly read-only:

| Database File | Size (Bytes) | Role |
| :--- | :--- | :--- |
| `hadith-kg.db` | 1,642,500,096 | Primary Hadith Knowledge Graph (715,790 narrations, narrators, sanads) |
| `isnad_network.db` | 52,092,928 | Narrator transmission edges and teacher-student relationships |
| `hadith_numbering.db` | 35,094,528 | Authoritative numbering crosswalks (Darussalam, Shamela, Abd al-Baqi) |
| `citation_enrichment.db` | 9,252,864 | Zubair Ali Zai grade references and takhrij notes (`zubair_grade_references_v3`) |
| `hadith_commentaries.db` | 9,056,256 | Classical commentaries (Fath al-Bari, Umdat al-Qari, etc.) |
| `classical_scholar_evidence.db`| 2,437,120 | Frozen Phase 4 classical scholar evaluations (3,462 records) |
| `hadith_translations.db` | 24,051,712 | 31,488 verified English translations |
| `english_translation_fts.db` | 32,796,672 | FTS5 full-text index for English translations |
| `hadith-search-index.db` | 248,565,760 | Arabic FTS index (`hadith_fts`) |
| `derived_semantic_index.db` | 85,180,416 | 20,744 meaning groups embedded in 768-D vectors |
| `ask_mizan.db` | 10,371,072 | Additive persistence DB (conversations, messages, feedback) |

### Cryptographic Baseline SHA-256 Hashes
The full 64-character SHA-256 hashes of all 35 databases have been computed and recorded in [`validation/baseline_db_hashes.json`](file:///c:/Users/taymi/discord-hadith-bot/validation/baseline_db_hashes.json). Key canonical records include:
- `hadith-kg.db`: `08c3a43d78f510828ab870a23203ef67d8ded7e55ce9e656e1b6f6580f4f72db`
- `isnad_network.db`: `d141026b306388b4ad30ee6c5c51fca7bf5a2ba2780702cae148e1467554bb76`
- `hadith_numbering.db`: `ecfe3079dba318bde09f544eaf84764a9095a1a1eb40be045f29c071d7967812`
- `citation_enrichment.db`: `8e3a1d03ee6d3668314448acfbb227476cfd85fa0a1a0df910e5aa0629ae6bf5`
- `classical_scholar_evidence.db`: `4fd1eb496e425240584441d0601906974b134dca954e7683151b72e5dc817d29`
- `hadith_commentaries.db`: `2fcd9ae4deeb006de25d6db23719abd2ecdaf9ebba23c8e42dbb958fbba9ad25`

---

## 5. REPRODUCED FAILURES & ROOT CAUSE IDENTIFICATION

### Failure 1: Provider Factory Crash on Deterministic Provider Request
- **Reproduced command:** `python scripts/test_ask_mizan_suite.py`
- **Output:** `AttributeError: 'GeminiProvider' object has no attribute 'name'` in `test_10_provider_factory_deterministic_resilience`.
- **Root Cause:** In [`mizan-web/backend/ask_mizan/providers/factory.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/providers/factory.py), `if choice == "deterministic"` was missing. The factory fell through to external providers where `GeminiProvider().is_available() == True`, returning a `GeminiProvider` that lacked the `name` attribute.

### Failure 2: Complete Absence of Urdu in Intent Parsing and Retrieval
- **Reproduced observation:** In [`parser.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/parser.py), no Urdu patterns existed for narrator extraction (e.g. `کون ہے`, `کے بارے میں`, `راوی`), scholar evaluations (`اقوال`, `جرح و تعدیل`), or collection references (`صحیح بخاری`, `سنن نسائی`, Urdu numerals `۱`, `۲`, `۳`).
- **Retrieval failure:** In [`hybrid_retrieval.py:954-958`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/hybrid_retrieval.py#L954-L958), when `detected_language == "ur"`, raw Urdu text was passed directly to Arabic FTS, resulting in **0.0% Recall@1, 0.0% Recall@5, 0.0% MRR**.
- **Thematic search failure:** In [`engine.py:168-171`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py#L168-L171), `tool_search_hadith_text` only accepted `"en"` or `"ar"`, returning empty hadiths for any Urdu query.

### Failure 3: Disconnected Classical Scholar Evidence Store
- **Reproduced observation:** [`data/classical_scholar_evidence.db`](file:///c:/Users/taymi/discord-hadith-bot/data/classical_scholar_evidence.db) contains 3,462 verified classical evaluations from al-Tirmidhi (2,726), Abu Dawud (585), and al-Nasai (151).
- **Root Cause:** [`tools.py::tool_get_scholarly_grades`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/tools.py#L685-L703) only queried `hadith_grades` and Darussalam crosswalk, completely omitting [`scholarly_service.py::get_verified_classical_hadith_evaluations`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/scholarly_service.py#L743-L770). Classical statements directly from the Sunan authors were unavailable to the Evidence Pack.

### Failure 4: Follow-up and Contextual Conversational Resolution Defect
- **Reproduced observation:** When a user asks "Who are his teachers?" or "What is its commentary?", the parser returned empty entities because the question relied on conversational history.
- **Root Cause:** [`engine.py::execute_ask_mizan`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py#L205-L220) loaded the conversation ID but never retrieved previous turns from `ask_mizan.db` to resolve anaphoric references (e.g. "this narrator", "this hadith", "his students").

### Failure 5: Frontend UX Flaws & Missing Academic Citations
- **Reproduced observation:** As audited in `validation/product_audit/09_ask_mizan_audit.json`:
  1. The UI reset session on page reload with no conversation history drawer.
  2. The evidence pack was collapsed by default in an accordion rather than accessible side-by-side.
  3. No one-click copy for academic citations (BibTeX, Chicago style).

---

## 6. PROPOSED CONTROLLED IMPLEMENTATION STRATEGY

1. **Step 1:** Fix `providers/factory.py` and assign `name: str` to all providers (`GeminiProvider`, `OpenAIProvider`, `AnthropicProvider`, `OllamaProvider`), verifying `test_ask_mizan_suite.py` achieves 100% pass.
2. **Step 2:** Expand `parser.py` with comprehensive Urdu NLP patterns, Urdu collection names, Arabic/Urdu numerals (`۰-۹`), and pronoun/context resolution.
3. **Step 3:** Connect `classical_scholar_evidence.db` to `tools.py::tool_get_scholarly_grades` using `get_verified_classical_hadith_evaluations`, preserving frozen Phase 4 rules.
4. **Step 4:** Implement Urdu cross-lingual and lexical enhancement in `hybrid_retrieval.py` and `tools.py` using Urdu text normalization and loanword/translation crosswalk.
5. **Step 5:** Implement multi-turn conversational context resolution in `engine.py` using prior turns from `db.py`.
6. **Step 6:** Upgrade frontend `src/app/ask/page.tsx` with split-pane / live evidence inspector, academic citation copy (BibTeX / Chicago), and conversation history persistence.
7. **Step 7:** Run full benchmark and regression suite across all 12 categories.
8. **Step 8:** Re-verify all 35 canonical database SHA-256 hashes.
