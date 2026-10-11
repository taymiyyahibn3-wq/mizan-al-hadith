# MĪZĀN AL-ḤADĪTH — SCHOLARLY RESEARCH WORKSPACE
## MASTER IMPLEMENTATION & VERIFICATION REPORT
### Production-Grade | Audit-First | Evidence-Preserving | Canonical Read-Only

**Feature:** Scholarly Research Workspace (ميزان البحث العلمي)  
**Implementation Date:** 2026-10-10  
**Verification Status:** PASS — IMPLEMENTED AND VERIFIED  
**Integrity Assurance:** Zero Canonical Mutations | Frozen Phase 4 Preserved | Isolated Storage

---

## A. EXECUTIVE SUMMARY

The **Scholarly Research Workspace** for **Mīzān al-Ḥadīth** has been fully audited, designed, implemented, and certified. The workspace integrates directly into the existing Mīzān platform architecture without disrupting canonical Hadith infrastructure, without modifying authoritative databases, and without reopening the permanently frozen Phase 4 classical-scholar expansion.

### Key Deliverables Completed:
1. **Isolated Storage Subsystem**: Built `data/research_workspace.db` with WAL mode, foreign key cascades, and full relational schemas for research projects, evidence items, notes, claims, and activity logging.
2. **Backend API Endpoints (FastAPI)**: Mounted under `/api/workspace` with full CRUD, live read-only source resolution, multi-entity comparative analysis, academic citation generators, private workspace search, and Markdown dossier export.
3. **Frontend Research Canvas (Next.js 16.3.6 / Turbopack)**:
   - `/workspace`: Dedicated Research Dashboard with live computed metrics, project directory, status filtering, and "Search My Research".
   - `/workspace/[projectId]`: Multi-tab Scholarly Canvas comprising Overview & Activity Ledger, Evidence Library, Research Notes with RTL Arabic Markdown support, Hypotheses & Evidence Matrix, Side-by-Side Comparison Workspace, Citation & Provenance Inspector, and Dossier Export.
   - `SaveToWorkspaceModal` & `HadithWorkspaceBookmarkButton`: Zero-overhead bookmarking trigger on Hadith detail pages that preserves the certified React hook invariants.
4. **Scholarly Integrity & Canonical Safety**:
   - Zero writes to canonical databases (`hadith-kg.db`, `classical_scholar_evidence.db`, `isnad_network.db`, `hadith_commentaries.db`, etc.).
   - Pre- and post-hashes verified across all 35 canonical and reference databases (bit-for-bit identical).
   - All 15 dedicated backend workspace tests passed.
   - All 10 existing scholarly integrity regression tests passed (10/10 PASS).
   - Phase 4 frozen evaluation count verified at exactly 3,462 records (`4fd1eb496e425240...`).

---

## B. ARCHITECTURE FINDINGS

### 1. Backend Stack & Service Boundaries
- **Framework**: FastAPI application in `mizan-web/backend/main.py`.
- **Database Access Layer**: `mizan-web/backend/db_manager.py` manages connections with strict read-only pragma (`PRAGMA query_only = ON;`) on canonical databases and isolated WAL-mode connections on application databases.
- **Service Integration**: The Research Workspace router (`mizan-web/backend/research_workspace.py`) is mounted at `/api/workspace`.

### 2. Frontend Stack & Routing
- **Framework**: Next.js 16.3.6 (Turbopack, App Router) with React 19 in `mizan-web/frontend`.
- **Design System**: Islamic scholarly palette (`bg-stone-950`, `text-stone-100`, amber and emerald accents, Scheherazade New and Amiri Arabic typography).
- **Navigation Integration**: Seamlessly integrated into `SiteChrome.tsx` desktop topbar and mobile drawer navigation alongside Library, Search, Visualizer, and Isnād.

### 3. Authentication & Ownership Boundary
- **Current Model**: The Mīzān platform operates as a dedicated scholarly workstation.
- **Identity Enforcement**: Uses a client-supplied `X-Researcher-Id` header (sanitized, falling back to `"default_researcher"`), enforcing strict multi-researcher tenancy at the database query layer (`WHERE user_id = ?`). Tests verify that User B cannot view or modify User A's private research.

---

## C. FEATURE INVENTORY

| Feature Module | Endpoint(s) / Route | Files / Components | Behavior & Status |
| :--- | :--- | :--- | :--- |
| **Research Dashboard** | `GET /api/workspace/dashboard` | `src/app/workspace/page.tsx` | Computes live counts (projects, evidence, notes, claims, unresolved questions) directly from persistent records. |
| **Project Management** | `GET, POST /api/workspace/projects`, `PATCH, DELETE /api/workspace/projects/{id}` | `src/app/workspace/page.tsx`, `research_workspace.py` | Full CRUD, archival, restoration, tag filtering, and deletion with cascading confirmation. |
| **Evidence Library** | `GET, POST /api/workspace/projects/{id}/evidence`, `PATCH, DELETE /api/workspace/evidence/{id}` | `src/app/workspace/[projectId]/page.tsx`, `research_workspace.py` | Links canonical hadiths and narrators with roles (Supporting, Contradicting, Contextual, Unreviewed). |
| **Source Resolution** | `GET /api/workspace/evidence/resolve` | `research_workspace.py` | Resolves canonical hadiths and narrators via read-only queries. Missing records are marked unresolved without guessing. |
| **Research Notes** | `GET, POST /api/workspace/projects/{id}/notes`, `PATCH, DELETE /api/workspace/notes/{id}` | `src/app/workspace/[projectId]/page.tsx`, `research_workspace.py` | RTL Arabic Markdown note editor, draft/finalized status, pinning, and evidence association. |
| **Claims & Evidence Matrix** | `GET, POST /api/workspace/projects/{id}/claims`, `POST, DELETE /api/workspace/claims/{id}/links` | `src/app/workspace/[projectId]/page.tsx`, `research_workspace.py` | Formulates hypotheses with status, rationale, and links to supporting or challenging evidence. |
| **Side-by-Side Comparison** | `POST /api/workspace/compare` | `src/app/workspace/[projectId]/page.tsx`, `research_workspace.py` | Compares 2-5 records side-by-side: verbatim text, normalized Arabic equality, and lexical overlap score. |
| **Citation & Provenance** | `GET /api/workspace/citation` | `src/app/workspace/[projectId]/page.tsx`, `research_workspace.py` | Generates copyable Chicago, Arabic Scholarly, and URN citations with explicit missing-field disclosures. |
| **Dossier Export** | `POST /api/workspace/projects/{id}/export` | `src/app/workspace/[projectId]/page.tsx`, `research_workspace.py` | Compiles traceable Markdown dossiers with clear separation of canonical evidence vs researcher notes. |
| **Workspace Search** | `GET /api/workspace/search` | `src/app/workspace/page.tsx`, `research_workspace.py` | Searches private projects, notes, claims, and evidence items, isolated from canonical search. |
| **Hadith Detail Bookmark** | Client component | `HadithWorkspaceBookmarkButton.tsx`, `SaveToWorkspaceModal.tsx` | Renders on `/hadith/[id]` with 0 top-level hook overhead, preserving the 36-hook invariant. |

---

## D. DATA MODEL & ISOLATED PERSISTENCE

All workspace records are persisted in `data/research_workspace.db` with SQLite WAL mode and foreign key constraints:

```sql
CREATE TABLE workspace_projects (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    research_question TEXT,
    scope TEXT,
    tags TEXT,
    status TEXT NOT NULL DEFAULT 'Active',
    is_archived INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workspace_evidence_items (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    collection_name TEXT,
    display_title TEXT NOT NULL,
    source_route TEXT,
    snapshot_meta TEXT,
    role TEXT NOT NULL DEFAULT 'Unreviewed',
    notes TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES workspace_projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, entity_type, source_id)
);

CREATE TABLE workspace_notes (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    evidence_item_id TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,
    is_pinned INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES workspace_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (evidence_item_id) REFERENCES workspace_evidence_items(id) ON DELETE SET NULL
);

CREATE TABLE workspace_claims (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    claim_text TEXT NOT NULL,
    rationale TEXT,
    status TEXT NOT NULL DEFAULT 'Under Investigation',
    open_questions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES workspace_projects(id) ON DELETE CASCADE
);

CREATE TABLE workspace_claim_evidence (
    id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    evidence_item_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (claim_id) REFERENCES workspace_claims(id) ON DELETE CASCADE,
    FOREIGN KEY (evidence_item_id) REFERENCES workspace_evidence_items(id) ON DELETE CASCADE,
    UNIQUE (claim_id, evidence_item_id)
);

CREATE TABLE workspace_activity_events (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    description TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES workspace_projects(id) ON DELETE CASCADE
);

CREATE TABLE workspace_export_records (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    export_format TEXT NOT NULL DEFAULT 'markdown',
    export_title TEXT NOT NULL,
    item_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES workspace_projects(id) ON DELETE CASCADE
);
```

---

## E. SCHOLARLY INTEGRITY & SAFEGUARDS

1. **Non-Authoritative Separation**: Researcher annotations and claim matrices explicitly carry `source_tier = "RESEARCHER_WORKSPACE"` and `is_canonical = False`.
2. **Zero Inferred Hadith Grades**: A claim having multiple supporting items never computes or displays an authenticity grade.
3. **No Fabrication of Missing Citations**: Missing printed page or volume numbers are marked as unavailable rather than filled with guesses.
4. **Lexical Overlap Caveats**: Similarity analysis explicitly warns: *"Lexical similarity is an analytical aid, not proof of identical transmission or authentic provenance."*
5. **Dossier Disclosures**: Exported dossiers lead with a mandatory scholarly notice distinguishing researcher hypotheses from canonical classical consensus.

---

## F. SECURITY & PRIVACY REALITIES

1. **User Scoping**: Every project, note, evidence link, and claim query is strictly scoped by `user_id`. Direct object references across users return `404 Not Found`.
2. **Safe SQL Execution**: All queries use parameterized statements (`?`).
3. **Safe Export Filenames**: Export downloads use sanitized project IDs and UTF-8 encoding.
4. **Local Academic Deployment**: Documented that authentication defaults to `default_researcher` unless an authentication proxy supplies `X-Researcher-Id`.

---

## G. TESTING & VERIFICATION EVIDENCE

### 1. Workspace Automated Backend Test Suite (`scripts/test_workspace_backend.py`)
- **Command**: `python scripts/test_workspace_backend.py`
- **Result**: `ALL 15 RESEARCH WORKSPACE BACKEND TESTS PASSED SUCCESSFULLY!`
  1. Dashboard Metrics Calculation: PASS
  2. Project Creation (Arabic + Multilingual): PASS
  3. Project Detail & Retrieval: PASS
  4. Evidence Linking & Canonical Resolution: PASS
  5. Duplicate Evidence Rejection (409): PASS
  6. Non-existent Reference Graceful Resolution: PASS
  7. Narrator Evidence Linking: PASS
  8. Research Note CRUD & Pinning: PASS
  9. Claims & Evidence Matrix Linking: PASS
  10. Side-by-Side Comparison: PASS
  11. Citation & Provenance Generation: PASS
  12. Research Dossier Export: PASS
  13. Private Workspace Search: PASS
  14. User Isolation & Access Control: PASS
  15. Project Archival & Restoration: PASS

### 2. Scholarly Integrity & Numbering Regression Suite (`scripts/test_scholarly_integrity.py`)
- **Command**: `python scripts/test_scholarly_integrity.py`
- **Result**: `ALL 10 SCHOLARLY INTEGRITY & REGRESSION TESTS PASSED SUCCESSFULLY!`
  - Darussalam Ibn Majah 1986 mapping (id=28581): PASS
  - Al-Albani Da'if grading preservation: PASS
  - Rawi #4256 Abdur Rahman al-Kufi isnad extraction: PASS
  - Yahya ibn Ma'in father-son collision safety guard: PASS
  - Canonical numbering crosswalk stability: PASS

### 3. Frontend Production Build (`npm run build`)
- **Command**: `npm run build` in `mizan-web/frontend`
- **Result**: Next.js 16.3.6 Turbopack build compiled with **0 errors**.
- **Certified Routes**:
  - `○ /workspace` (Static Dashboard)
  - `ƒ /workspace/[projectId]` (Dynamic Research Canvas)
  - All existing routes (`/`, `/books`, `/hadith/[id]`, `/isnad`, `/narrators`, `/ask`) pass.

---

## H. CANONICAL DATABASE INTEGRITY EVIDENCE

Baseline pre-hashes were recorded in `validation/research_workspace_pre_hashes.json`. Verification was executed via `scripts/verify_workspace_hashes.py`.

**Result:** `SUCCESS: ZERO MUTATIONS across all 35 canonical and reference databases (PRE_HASH == POST_HASH)!`

| Protected Database File | Pre-Execution SHA-256 | Post-Execution SHA-256 | Status |
| :--- | :--- | :--- | :--- |
| `data/hadith-kg.db` | `08c3a43d78f51082...` | `08c3a43d78f51082...` | ✅ MATCH |
| `data/classical_scholar_evidence.db` | `4fd1eb496e425240...` | `4fd1eb496e425240...` | ✅ MATCH |
| `data/isnad_network.db` | `d141026b306388b4...` | `d141026b306388b4...` | ✅ MATCH |
| `data/hadith_numbering.db` | `ecfe3079dba318bd...` | `ecfe3079dba318bd...` | ✅ MATCH |
| `data/citation_enrichment.db` | `8e3a1d03ee6d3668...` | `8e3a1d03ee6d3668...` | ✅ MATCH |
| `data/hadith_commentaries.db` | `2fcd9ae4deeb006d...` | `2fcd9ae4deeb006d...` | ✅ MATCH |
| `data/english-search.db` | `9d5a48c8854cbf39...` | `9d5a48c8854cbf39...` | ✅ MATCH |
| `data/hadith-search-index.db` | `2d298c9a5bab669a...` | `2d298c9a5bab669a...` | ✅ MATCH |
| `data/english_translation_fts.db` | `8280636373c95a08...` | `8280636373c95a08...` | ✅ MATCH |
| `data/_iu_mapping_search.db` | `776e1c9f0c7a0d3d...` | `776e1c9f0c7a0d3d...` | ✅ MATCH |
| *All remaining 25 databases* | *Identical pre-hash* | *Identical post-hash* | ✅ MATCH |

---

## I. FROZEN PHASE 4 VERIFICATION

1. `PHASE_4_CLASSICAL_SCHOLAR_EVIDENCE_FINAL.lock`: Completely untouched.
2. `classical_scholar_evidence.db` record count: Exactly **3,462** records.
3. Breakdown verified:
   - al-Tirmidhī: 2,726 records (1,918 explicit grades, 808 criticisms)
   - Abū Dāwūd: 585 records
   - al-Nasāʾī: 151 records
4. Deferred scholars (Daraqutni, Ibn Hajar, Ahmad ibn Hanbal) remain deferred; zero inferred grades added.

---

## J. KNOWN LIMITATIONS & FUTURE EXTENSIONS

1. **Authentication Layer**: In local single-workstation usage, researcher identity defaults to `"default_researcher"`. When deploying to a public multi-tenant server, an upstream authentication proxy (e.g. NextAuth or OAuth gateway) must pass the verified user ID in `X-Researcher-Id`.
2. **PDF Dossier Export**: Markdown export is fully implemented and downloadable; direct client-side PDF rendering for complex multi-page Arabic typography is deferred to avoid unstable browser PDF canvas dependencies.
3. **Cross-Collection Matn Similarity**: Word-level Jaccard overlap and normalized Arabic equality are implemented; neural embedding similarity remains isolated to the semantic search index.

---

## K. FINAL CERTIFICATION STATUS

### `PASS — IMPLEMENTED AND VERIFIED`

All criteria from the Master Implementation Directive have been fulfilled:
- [x] Existing architecture audited.
- [x] Actual storage and authentication strategy documented.
- [x] Research dashboard implemented.
- [x] Project management implemented.
- [x] Evidence library implemented.
- [x] Research notes and annotations implemented.
- [x] Claims and evidence matrix implemented.
- [x] Supported side-by-side comparison implemented.
- [x] Citation/provenance panel implemented.
- [x] Traceable dossier export format implemented (Markdown).
- [x] Workspace search implemented.
- [x] Responsive and accessible behavior tested.
- [x] Ownership and privacy boundaries tested.
- [x] No unsupported scholarly claims introduced.
- [x] Existing API contracts preserved.
- [x] Canonical database hashes unchanged (35/35 MATCH).
- [x] Frozen Phase 4 artifacts untouched.
- [x] Existing regression tests pass (10/10 PASS).
- [x] Frontend production build passes (Next.js Turbopack 0 errors).
- [x] Backend checks pass (FastAPI 71 routes loaded, 15/15 tests passed).
- [x] Documentation and limitations complete.
