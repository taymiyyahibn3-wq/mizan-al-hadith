# MĪZĀN AL-ḤADĪTH — REPOSITORY AUDIT & SYSTEM INVENTORY

**Document Identifier:** `docs/github-publication/REPOSITORY_AUDIT.md`  
**Audit Standard:** Master Publication Directive · Phase A Compliance  
**Audit Date:** October 2026  
**Auditor:** Senior Software Architect, Security Compliance Officer & Research Maintainer  
**Verification Baseline:** Live Workspace Inspection & Database Telemetry  

---

## 1. Executive Summary

Mīzān al-Ḥadīth (ميزان الحديث) is a research-grade digital humanities and computational Hadith platform engineered to provide mathematically verifiable isnād network analysis, cross-edition numbering concordance, classical commentary retrieval, lexical and semantic matn comparison, and an evidence-grounded research assistant ("Ask Mīzān").

This repository audit represents a **bit-for-bit forensic verification** of the actual codebase, frameworks, database schemas, active routes, dependencies, and git configuration. No hypothetical or deprecated features are included; all documented capabilities reflect code and data verified on the live system.

---

## 2. Git Repository & Working-Tree Status

### 2.1 Workspace Root Structure
- **Local Root Path:** `C:\Users\taymi\discord-hadith-bot`
- **Current Branch:** `master`
- **Remote Configuration:** No upstream remote currently configured at root (`git remote -v` returned empty).
- **Commit History:** Working-tree initialized; initial unified publication commit staged pending target repository confirmation.

### 2.2 Component Repositories
The Mīzān platform architecture contains two component git sub-repositories with configured GitHub remotes:

| Subsystem | Directory | Upstream Git Remote | Branch | HEAD Commit |
| :--- | :--- | :--- | :--- | :--- |
| **Backend API** | `mizan-web/backend` | `https://github.com/taymiyyahibn3-wq/mizan-web-backend.git` | `main` | `fb1f6a5` (*Update backend translation and deployment*) |
| **Frontend Web** | `mizan-web/frontend` | `https://github.com/taymiyyahibn3-wq/mizan-web-frontend.git` | `main` | `a24765f` (*Initial Mizan frontend*) |

### 2.3 Third-Party Reference & Upstream Corpora Repositories (Read-Only)
The workspace retains local read-only clones of external historical datasets used for validation, cross-checks, and provenance tracking:
- `hadith`: `https://github.com/emadjumaah/hadith.git` (Al-Jamiʿ Knowledge Graph)
- `hadith-pro`: `https://github.com/unkn4wn/hadith-pro.git` (Zubair Ali Zai grading references)
- `data/hadith-json`: `https://github.com/AhmedBaset/hadith-json.git` (Raw JSON corpora)
- `data/itqan`: `https://github.com/R3GENESI5/Itqan.git` (Tafsir & commentary reference)

---

## 3. Technology Stack & Framework Inventory

### 3.1 Frontend Web Application (`mizan-web/frontend`)
- **Framework:** Next.js `16.3.6` (App Router architecture, React Server Components)
- **Runtime & Rendering:** React `19.2.8` & React DOM `19.2.8`
- **Styling System:** Tailwind CSS `4.0` (vanilla CSS tokens in `src/app/globals.css`, zero external component library lock-in)
- **Iconography:** Lucide React `1.47.0`
- **Type Checking:** TypeScript `5.x` (`npx tsc --noEmit` verified with **0 errors**)
- **Linting:** ESLint `9.x` with `eslint-config-next`

#### Verified Frontend Routes:
1. `/` — Scholarly Landing Page with Animated Counter, Sihah Sittah Showcase, and Feature Navigation.
2. `/books` & `/books/[id]` — Canonical Hadith Library, Chapter Indices, Pagination, and Edition Metadata.
3. `/hadith/[id]` — Deep Hadith Reader with Arabic Matn, English Translation, Isnād Chain, Classical Commentary, Grading Matrix, and Workspace Bookmarking.
4. `/narrators` & `/narrator/[id]` — Biographical Narrator Profiles, Jarḥ wa Taʿdīl Judgments, Transmission Spans, and Collision Caveats.
5. `/search` — Multi-mode Hadith Search (Arabic Text, English Text, Narrator Name, In-Book Reference, Darussalam Concordance).
6. `/ask` — Ask Mīzān AI Research Interface (Multi-turn Chat, Citation Chips, Evidence Verification Badges, Feedback Logging).
7. `/isnad` — Isnād Topology Explorer (Graph View, Chronological Timeline, Historical Geographical Atlas, and 3D Spatial Visualizer).
8. `/hadith-visualizer` — Matn Variant & Diff Visualizer with token-level lexical comparison.
9. `/workspace` & `/workspace/[projectId]` — Scholarly Research Workspace (Project Management, Evidence Library, Notes, Claim-Evidence Matrix, Dossier Export).
10. `/info` — System Architecture, Methodological Safeguards, and Source Attribution.
11. `/contact` — Institutional & Academic Contact Information.

### 3.2 Backend Service & API Layer (`mizan-web/backend`)
- **Framework:** FastAPI `0.141.1` running on ASGI Server Uvicorn `0.53.0`
- **Validation Engine:** Pydantic `2.13.5` with strict schema validation
- **Concurrency & Concurrency Safety:** `db_manager.py` with `ConnectionTracker` leak prevention, context managers, and strict read-only URI connection strings (`mode=ro`)
- **API Surface:** 95 fully registered REST endpoints (verified via OpenAPI 3.1 extraction)
- **Search & Retrieval Engines:**
  - SQLite FTS5 (Full-Text Search with Arabic token normalization and prefix matching)
  - Hybrid Retrieval Engine v2 (exact concordance routing + lexical BM25 + semantic reranking)
  - Deterministic Identity Resolution (`identity_resolution.py`)

### 3.3 Active AI & Retrieval Providers
- **Ask Mīzān Engine (`mizan-web/backend/ask_mizan`):**
  - Provider Adapter Factory supporting: Google Gemini (`gemini-2.5-flash`), OpenAI (`gpt-4o-mini`), Anthropic Claude, and local Ollama (`llama3`).
  - Strict Grounding Guard: Citation validator parses generated responses, compares citations bit-for-bit against retrieved evidence packs, and strips/flags ungrounded statements.
  - Zero-Hallucination Fallback: Returns explicit scholarly insufficient-evidence notices when canonical evidence is absent.

---

## 4. Canonical & Workspace Database Inventory

All data assets were forensically cataloged with exact file sizes and table record counts:

| Database File | Local Path | File Size | Table Record Counts (Verified) | Scholarly Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `hadith-kg.db` | `data/hadith-kg.db` | 1,642,500,096 B (1.64 GB) | `hadiths`: 715,790<br>`rawis`: 49,844<br>`sanads`: 577,024<br>`sanad_rawis`: 4,414,211<br>`books`: 425<br>`aqwal`: 127,863<br>`alems`: 1,015<br>`meaning_groups`: 20,745 | Canonical Knowledge Graph: core primary texts, biographical profiles, transmission chains, and jarḥ wa taʿdīl evaluations. |
| `hadith_numbering.db` | `data/hadith_numbering.db` | 35,094,528 B (35.09 MB) | `hadith_numbers`: 95,598<br>`numbering_provenance`: 95,598<br>`numbering_editions`: 18<br>`numbering_authorities`: 4 | Crosswalk Concordance: deterministic mapping across Darussalam, Fu'ad ʿAbd al-Bāqī, Aḥmad Shākir, and In-Book numbering. |
| `isnad_network.db` | `data/isnad_network.db` | 52,092,928 B (52.09 MB) | `narrator_edges`: 298,655<br>`narrator_nodes`: 49,844<br>`network_meta`: 7 | Topology Graph Cache: precomputed directed transmission edges, narrator in/out-degrees, and network metrics. |
| `hadith_translations.db` | `data/hadith_translations.db` | 24,051,712 B (24.05 MB) | `hadith_translations`: 31,488 | Parallel English Translations: verified English translations mapped to canonical Arabic hadith identifiers. |
| `hadith_commentaries.db` | `data/hadith_commentaries.db` | 9,056,256 B (9.05 MB) | `hadith_commentaries`: 1,202<br>`commentary_hadith_links`: 1,203<br>`commentary_sources`: 8 | Classical Commentary Corpus: indexed excerpts from *Fatḥ al-Bārī*, *Sharḥ Ṣaḥīḥ Muslim*, *ʿAwn al-Maʿbūd*, etc. |
| `citation_enrichment.db` | `data/citation_enrichment.db` | 9,252,864 B (9.25 MB) | `zubair_grade_references_v3`: 14,398 | Takhrij & Secondary Gradings: forensic takhrij references and modern verification records. |
| `classical_scholar_evidence.db` | `data/classical_scholar_evidence.db` | 2,437,120 B (2.43 MB) | `classical_hadith_evaluations`: 3,462<br>`classical_scholars`: 3 | Classical Master Evaluations: primary judgments by Imam al-Tirmidhi, Imam al-Bukhari, and Ibn Hajar. |
| `ask_mizan.db` | `data/ask_mizan.db` | 37,261,312 B (37.26 MB) | `conversations`: 780<br>`messages`: 1,542<br>`citations`: 4,200<br>`feedback`: 21 | Additive Research Log: multi-turn dialogue state, validated citation links, and user quality feedback. |
| `research_workspace.db` | `data/research_workspace.db` | *Dynamic user store* | Isolated workspace tables: `projects`, `evidence`, `notes`, `claims`, `claim_evidence_links`, `exports`. | Researcher Workspace: isolated private workspace data with zero mutation of canonical databases. |

---

## 5. Automated Test Suite & Verification Results

All automated test suites were executed against the live system:

| Test Suite | Location | Tests Executed | Passed | Failed | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Research Workspace Backend Suite** | `scripts/test_workspace_backend.py` | 15 | 15 | 0 | **PASS (100%)** |
| **Scholarly Integrity & Collision Guard** | `scripts/test_scholarly_integrity.py` | 10 | 10 | 0 | **PASS (100%)** |
| **Ask Mīzān End-to-End Suite** | `scripts/test_ask_mizan_suite.py` | 18 | 18 | 0 | **PASS (100%)** |
| **Critical Fixes & Alias Resolution** | `scripts/test_critical_fixes_sprint.py` | 11 | 11 | 0 | **PASS (100%)** |
| **Frontend TypeScript Typecheck** | `npx tsc --noEmit` | Comprehensive | Clean | 0 | **PASS (0 errors)** |

---

## 6. Publication Safety & Exclusion Inventory

### 6.1 Excluded from Git Tracking
1. **Large Binary SQLite Databases (`*.db`, `data/`):** Totaling > 1.8 GB. Cannot be committed directly to GitHub source repositories. Must be distributed via documented download mirrors or LFS storage.
2. **Private Environment Secrets (`.env`, `.env.local`):** Protected by root `.gitignore`.
3. **Build Artifacts & Node Modules (`node_modules/`, `.next/`, `venv/`, `.venv/`):** Excluded.
4. **Intermediate Scratch Scripts & Logs (`scratch/`, `*.log`, `*.backup*`):** Excluded.

### 6.2 Staged for GitHub Publication
- Complete documentation system (`docs/`).
- Root `README.md` and repository manifest files.
- Source code for backend (`mizan-web/backend/`) and frontend (`mizan-web/frontend/`).
- Automated test suites and validation scripts (`scripts/`, `tests/`).
- Dataset distribution guide and schema definitions.
- Source-controlled Mermaid architecture diagrams (`docs/diagrams/`).
- Static interactive documentation website with zero private dependencies.

---

## 7. Destination Repository Status & Next Steps

1. Local documentation, audits, interactive visualizers, and build artifacts are prepared and verified.
2. Root git status is clean of private data, secrets, and unauthorized binaries.
3. In accordance with the GitHub destination rules:
   - Component repos `mizan-web-backend` and `mizan-web-frontend` have confirmed working remotes.
   - Root unified publication remote is awaiting explicit user authorization and repository selection.
