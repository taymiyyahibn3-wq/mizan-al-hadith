# MĪZĀN AL-ḤADĪTH — SCHOLARLY RESEARCH WORKSPACE
## PHASE A — ARCHITECTURE AND SECURITY AUDIT REPORT

**Date:** 2026-10-10  
**Status:** COMPLETE & VERIFIED  
**Integrity Level:** Canonical Read-Only | Evidence-Preserving | Isolated Persistence

---

## 1. EXECUTIVE SUMMARY & REPOSITORY OVERVIEW

This audit establishes the baseline architectural patterns, database boundaries, API contracts, security realities, and frontend component conventions across the **Mīzān al-Ḥadīth** codebase prior to implementing the **Scholarly Research Workspace**.

### Repository Structure
- **Backend Root:** `c:\Users\taymi\discord-hadith-bot\mizan-web\backend`
  - Framework: FastAPI (`main.py`)
  - Database access: `db_manager.py` (centralized connection manager enforcing read-only pragma & connection pools)
  - Scholarly Services: `scholarly_evidence.py`, `scholarly_annotations.py`, `hadith_service.py`, `isnad_graph_service.py`
  - Port: Runs on `:8000` via Uvicorn.
- **Frontend Root:** `c:\Users\taymi\discord-hadith-bot\mizan-web\frontend`
  - Framework: Next.js 16.3.6 (Turbopack, App Router)
  - UI Library: TailwindCSS + Lucide React + Framer Motion
  - Styling System: Warm Islamic scholarly aesthetic (`bg-stone-900`, `text-stone-100`, `amber-500/emerald-500` accents, Scheherazade New & Amiri Arabic typography)
  - Navigation: `SiteChrome.tsx` (`/books`, `/search`, `/hadith-visualizer`, `/isnad`, `/narrators`, `/info`, `/ask`)
- **Data Stores Directory:** `c:\Users\taymi\discord-hadith-bot\data`
  - 33 Canonical / Reference databases strictly read-only (`hadith-kg.db`, `classical_scholar_evidence.db`, `isnad_network.db`, `hadith_commentaries.db`, etc.)
  - Derived/User-specific databases: `ask_mizan.db`, `user_annotations.db`.

---

## 2. CANONICAL DATABASE INVENTORY & INTEGRITY INVARIANTS

### 2.1 The 33 Protected Canonical Databases
The repository contains 33 canonical databases verified under `forensic_pass_pre_hashes.json`. Every canonical database is accessed exclusively through `open_readonly_connection` using URI parameters (`file:...?...&mode=ro`) and `PRAGMA query_only = ON;`.

1. `data/hadith-kg.db` — Primary knowledge graph (Hadiths, narrators, collections, isnads, grades)
2. `data/classical_scholar_evidence.db` — 3,462 frozen classical hadith evaluations (Tirmidhī, Abū Dāwūd, al-Nasāʾī)
3. `data/isnad_network.db` — Graph structure of chains
4. `data/hadith_commentaries.db` — Sharh and classical commentaries (Fath al-Bari, etc.)
5. `data/citation_enrichment.db` — Cross-references and shamela volume/page anchors
6. `data/hadith_numbering.db` — Concordance across numbering editions
7. `data/shamela_crosswalk.db` — Shamela cross-references
8. Additional 26 canonical/reference databases listed in `forensic_pass_pre_hashes.json`.

**Integrity Mandate:** No migrations, no table creation, no schema mutations, no triggers, and no writes can be executed against any canonical database.

### 2.2 Phase 4 Frozen Classical Scholar Expansion
The classical scholar evidence expansion is permanently frozen at **3,462 records**:
- Imām al-Tirmidhī: 2,726 records (1,918 grades, 808 criticisms)
- Imām Abū Dāwūd: 585 records
- Imām al-Nasāʾī: 151 records
- Phase 4 Lock File: `PHASE_4_CLASSICAL_SCHOLAR_EVIDENCE_FINAL.lock`
- This boundary is strictly respected. Private notes and research hypotheses must never be commingled with or labeled as classical evidence.

---

## 3. PROPOSED ISOLATED STORAGE STRATEGY

Following the established precedent in `scholarly_annotations.py` and `user_annotations.db`:
- **Database File:** `data/research_workspace.db`
- **Connection Helper:** `db_manager.py` will expose `get_workspace_db_context()` utilizing `open_writable_connection(RESEARCH_WORKSPACE_DB_PATH, "research_workspace")` with `PRAGMA foreign_keys = ON;` and `PRAGMA journal_mode = WAL;`.
- **Entity Schemas:**
  1. `workspace_projects`: Research project metadata (`id`, `title`, `description`, `research_question`, `scope`, `tags`, `status`, `user_id`, `created_at`, `updated_at`, `is_archived`).
  2. `workspace_evidence_items`: Source-linked evidence records (`id`, `project_id`, `entity_type`, `source_id`, `collection_name`, `display_title`, `source_route`, `snapshot_meta`, `role`, `notes`, `tags`, `created_at`).
  3. `workspace_notes`: Researcher-authored annotations (`id`, `project_id`, `evidence_item_id`, `title`, `content`, `tags`, `is_pinned`, `status`, `created_at`, `updated_at`).
  4. `workspace_claims`: Structured claims / hypotheses (`id`, `project_id`, `claim_text`, `rationale`, `status`, `open_questions`, `created_at`, `updated_at`).
  5. `workspace_claim_evidence`: Association junction (`id`, `claim_id`, `evidence_item_id`, `relation_type`, `notes`, `created_at`).
  6. `workspace_activity_events`: Audit log of research actions (`id`, `project_id`, `event_type`, `description`, `metadata_json`, `created_at`).

---

## 4. AUTHENTICATION & ACCESS CONTROL REALITIES

### 4.1 Current Repository Status
The current Mīzān platform operates as a dedicated research server without an external multi-tenant OAuth/JWT gateway.
- `scholarly_annotations.py` supports an optional `user_id` query parameter, defaulting to `"default_user"`.
- In the Research Workspace, every project, note, and evidence link will store an explicit `user_id`.
- The API will read an optional `X-Researcher-Id` header (fallback: `"default_researcher"`), allowing multi-researcher support if deployed behind an authentication proxy while working seamlessly in the local academic environment.
- Cross-user data leakage is prevented via user scoping on all project queries.

---

## 5. EXISTING APIS & SOURCE RESOLUTION

Existing read-only endpoints in `main.py` will be used to resolve live entity metadata without duplicating canonical text:
- `/api/hadith/{id}` — Canonical hadith text, isnad, book, chapter, and grades.
- `/api/books` & `/api/books/{id}` — Collection and book details.
- `/api/rawis/{id}` — Narrator biographies and rijal records.
- `/api/scholarly-evidence/hadith/{id}` — Classical evidence records.
- `/api/commentaries/hadith/{id}` — Canonical commentaries.

When an entity is added to the Research Workspace, only its canonical reference (`entity_type` + `source_id`), collection name, and brief title snippet are stored as a lightweight fallback snapshot. Live resolution is attempted when viewing. If an entity is deleted or unavailable upstream, the workspace marks it as "Source unresolved" rather than failing silently.

---

## 6. FRONTEND INVARIANTS & INTEGRATION PLAN

### 6.1 React Hook Order Invariants
- `src/app/hadith/[id]/page.tsx` was previously certified with exactly **36 React hooks**.
- Any UI addition on the hadith detail page (e.g. "Save to Workspace" modal button) must be encapsulated in a subcomponent or placed strictly within unconditioned rendering flows without altering the 36 top-level hook invocations.

### 6.2 New Research Workspace Views
- Navigation: Add `/workspace` with `FolderKanban` / `Bookmark` icon in `SiteChrome.tsx`.
- `/workspace`: Dashboard showing projects, quick stats, recent evidence, unresolved claims, and creation modal.
- `/workspace/[projectId]`: Multi-tab scholarly canvas:
  1. **Overview & Scope** (Project research question, status, tags, activity feed).
  2. **Evidence Library** (Hadiths, narrators, classical grades, commentaries with filtering and role tagging).
  3. **Research Notes** (RTL Arabic Markdown/plain-text editor, pinning, tags).
  4. **Claims & Evidence Matrix** (Claims mapped to supporting/challenging evidence, with non-authoritative warning).
  5. **Side-by-Side Comparison** (Compare 2-4 hadiths / narrators side by side).
  6. **Dossier Export** (Compile project into structured Markdown or printable HTML with complete provenance).

---

## 7. AUTOMATED TEST & VERIFICATION PROTOCOL

The following verification commands are established:
1. Canonical Hash Verification: `python scripts/verify_forensic_pass_hashes.py` (Must yield 33/33 matches).
2. Phase 4 Classical Evidence Record Count: 3,462 records in `classical_scholar_evidence.db`.
3. Frontend Production Build: `cd mizan-web/frontend && npm run build` (Turbopack, 0 errors).
4. Backend Functional Verification: Automated pytest or python integration test verifying all workspace CRUD, linking, search, and export routines against `data/research_workspace.db`.
