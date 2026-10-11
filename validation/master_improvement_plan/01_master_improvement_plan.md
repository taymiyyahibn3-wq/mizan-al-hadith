# MĪZĀN AL-ḤADĪTH (ميزان الحديث)
## Comprehensive System Improvement & Remediation Master Plan

**Document Identifier:** `validation/master_improvement_plan/01_master_improvement_plan.md`  
**Review Board:** Senior Multidisciplinary Engineering & Digital Humanities Review Board (18 Specialized Roles)  
**Operating Baseline:** Current System State (Post-Phase 18 Baseline)  
**Operating Principles:** Plan Only | Zero-Mutation | Zero-Migration | Zero-Refactor | Redacted Secrets  
**Scholarly Priority:** Scholarly Correctness > Data Integrity > Security > Application Correctness > Reliability > Performance > Accessibility > UX > Visual Polish  
**Date:** October 2026  

---

## 1. Executive Summary & Audit Mandate

**Mīzān al-Ḥadīth (ميزان الحديث)** is an ambitious, visually dignified digital humanities research platform designed to provide computational access to Islamic Hadith collections, transmission topologies (Isnād graphs), cross-edition numbering concordances, and classical scholarly evaluations.

Following the completion of forensic Phases 1 through 18, a comprehensive forensic review was performed to independently inspect the actual code, databases, routes, visualizers, and deployments. The review revealed a critical paradox: **while the project's core data invariants are remarkably sound and authentic, the application serving layer suffers from severe engineering defects, deceptive UI metrics, and broken production infrastructure.**

The purpose of this Master Plan is **NOT to praise Mīzān**, nor is it to conduct another exploratory audit. It provides a **rigorous, prioritized, sprint-by-sprint implementation blueprint** to systematically remediate confirmed defects without mutating canonical databases or destabilizing certified invariants.

---

## 2. Review Board & Operating Principles

The improvement plan has been formulated by an independent 18-role multidisciplinary review board:
1. **Principal Software Architect** — System boundaries, monorepo consolidation, and service decoupling.
2. **Senior Backend Engineer** — FastAPI APIRouter decomposition and composite dossier services.
3. **Senior Frontend Engineer** — Next.js 14 component deconstruction and state pruning.
4. **Database Architect** — Read-only guarantees, schema preservation, and column aliasing.
5. **SQLite Performance Engineer** — Index verification, ATTACH elimination, and query latency.
6. **DevOps / Docker / CI-CD Engineer** — Multi-stage Docker builds and automated GitHub Actions workflows.
7. **Application Security Engineer** — Credential rotation, rate limiting, and SQL parameterization.
8. **AI / RAG Engineer** — Grounded evidence packs, import error resolution, and token efficiency.
9. **Search & Information Retrieval Engineer** — Universal citation parsing and pagination.
10. **Scholarly Data Architect** — Hadith vs narrator verdict separation and book role assignment.
11. **Hadith Data Specialist** — Precision Matn offset slicing and classical critic lineage.
12. **UX/UI Researcher** — Search unification, navigation flow, and academic drawer UX.
13. **Accessibility Engineer** — WCAG 2.1 AA keyboard navigation and screen-reader semantics.
14. **Performance Engineer** — Core Web Vitals, font optimization, and waterfall elimination.
15. **Visualization / WebGL Engineer** — Canvas DAG optimization and decorative 3D pruning.
16. **Licensing & Digital Provenance Analyst** — Copyright clearance and transparent attribution.
17. **Production Reliability Engineer** — Graceful fallbacks and health monitoring.
18. **Code Quality / Technical Debt Auditor** — Workspace hygiene and dead code removal.

### Absolute Invariant Operating Rules:
- **Rule 1 — Plan Only:** Zero source code mutation, zero database mutation, zero credential rotation during planning.
- **Rule 2 — Zero Database Mutation:** Canonical databases ([`hadith-kg.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith-kg.db), [`hadith_numbering.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_numbering.db), [`citation_enrichment.db`](file:///c:/Users/taymi/discord-hadith-bot/data/citation_enrichment.db), [`hadith_commentaries.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_commentaries.db)) are strictly read-only.
- **Rule 3 — Protected Invariants:** The 715,790-hadith graph, 298,655 isnād edges, 286-record Zubayr quarantine gate, Record #428 scope, Ask Mīzān deterministic fallback, and parchment/emerald visual tokens must never be casually altered.
- **Rule 4 — Evidence Over Assumption:** Every finding is anchored to verified file lines and SQL query results.
- **Rule 5 — Severity Classification:** P0 (Blocker) to P4 (Optional Research).

---

## 3. Verification of Previous Forensic Findings

Every finding from the previous audit was independently cross-checked against the active implementation:

| ID | Domain | Previous Claim | Verified Status | Implementation Reality |
| :---: | :---: | :--- | :---: | :--- |
| **`DEP-01`** | DevOps | Dockerfile crashes on container startup | **CONFIRMED** | [`mizan-web/backend/Dockerfile:18-24`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/Dockerfile#L18-L24) omits core modules and databases; container crashes with `ModuleNotFoundError`. |
| **`SEC-01`** | Security | Live Discord token exposed in root `.env` | **CONFIRMED** | Root [`.env:1`](file:///c:/Users/taymi/discord-hadith-bot/.env#L1) contains plaintext active token (`DISCORD_TOKEN=[REDACTED]`). |
| **`RAG-01`** | AI / RAG | Missing `import re` crashes Ask Mīzān | **CONFIRMED** | [`ask_mizan/engine.py:95`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py#L95) calls `re.search` without `import re`, raising `NameError`. |
| **`SRCH-01`** | Search | Punctuation in queries causes search failure | **CONFIRMED** | [`main.py:243`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py#L243) regex rejects `"Bukhari #1"`, `"Bukhari: 1"`, and `"Muslim: 1"`, falling back to slow full-text search. |
| **`SRCH-03`** | Search | Results 51+ are unreachable in web UI | **CONFIRMED** | [`search/page.tsx:108`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/search/page.tsx#L108) hardcodes `limit=50&offset=0` with zero pagination controls. |
| **`MODEL-01`** | Data Model | Column `matn` stores authenticity status | **CONFIRMED** | In `hadiths` table, 100% of `matn` values are status strings ("صحيح", "حسن"); continuous text is in `nass`. |
| **`MODEL-02`** | Data Model | Verified character offsets are discarded | **CONFIRMED** | [`main.py:639`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py#L639) returns `nass`, ignoring 99.8% accurate `matn_start`/`matn_end` offsets and prepending Isnād to Matn. |
| **`GRADE-02`** | Scholarly | UI displays misleading grade counts | **CONFIRMED** | [`hadith/[id]/page.tsx:1230`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/hadith/%5Bid%5D/page.tsx#L1230) sums hadith verdicts with narrator remarks; Bukhari 1 shows `"Grades (42)"` with 0 grades. |
| **`A11Y-01`** | Accessibility | Visualizers lack keyboard navigation | **CONFIRMED** | [`isnad/page.tsx:310-380`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/isnad/page.tsx#L310-L380) has 0 `tabIndex`, 0 `onKeyDown`, and 0 button roles on interactive SVG nodes. |
| **`UX-01`** | Performance | 12-request un-cached HTTP waterfall | **CONFIRMED** | Hadith Detail page fires 12 sequential un-cached fetches on every navigation, causing 950ms+ latency. |
| **`PERF-01`** | Performance | Render-blocking Google Fonts `@import` | **CONFIRMED** | Line 1 of [`globals.css`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/globals.css#L1) halts CSS OM parsing and initial page rendering. |
| **`MATN-01`** | Visualization | Matn 3D View is decorative eye-candy | **CONFIRMED** | [`MatnThreeDView.tsx:127`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/hadith-visualizer/MatnThreeDView.tsx#L127) lays nodes on a circle by array index (`angle = idx * 2π/N`) with zero semantic math. |

### Verified False Positives & Mitigated Claims:
1. **`FP-01` (Database Corruption Claim):** `PRAGMA integrity_check` returned `ok` across all canonical databases. Data structures are healthy; the issues are in application-layer naming and offset slicing.
2. **`FP-02` (Zubayr Quarantine Leak Claim):** Confirmed 100% secure. [`scholarly_service.py:645`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/scholarly_service.py#L645) strictly isolates all 286 uncertified records; 0 leak into API responses.
3. **`FP-03` (Matn Segmentation Absence Claim):** 714,610 hadiths (99.83% of the entire corpus) **already have** verified character offsets in SQLite. No expensive NLP re-segmentation is needed; only the serving helper requires an update.

---

## 4. P0 Security & Production Blockers

```
┌────────────────────────────────────────────────────────────────────────┐
│                   EMERGENCY P0 REMEDIATION PIPELINE                     │
├──────────────────────────┬─────────────────────────┬───────────────────┤
│ Secret Exposure (SEC-01) │ Docker Crash (DEP-01)   │ RAG Crash (RAG-01)│
│ .env line 1              │ Dockerfile lines 18-24  │ engine.py line 95 │
│ Rotate & Exclude         │ Fix COPY directives     │ Add 'import re'   │
└──────────────────────────┴─────────────────────────┴───────────────────┘
```

### 1. Plaintext Discord Bot Token Exposure (`SEC-01`)
- **Location:** Workspace root [`.env:1`](file:///c:/Users/taymi/discord-hadith-bot/.env#L1).
- **Attack Surface:** Public Git repository cloning, accidental commit pushes, or shared team developer environments.
- **Exploit Scenario:** An attacker extracts `DISCORD_TOKEN=[REDACTED]` and interacts with the Discord REST API to hijack the bot, send malicious announcements, or compromise Discord community servers.
- **Remediation Strategy:**
  1. Revoke and regenerate the token immediately in the Discord Developer Portal.
  2. Add `.env` to `.gitignore`.
  3. Create `.env.example` with sanitized placeholders.
  4. Ensure production environments inject tokens via container environment variables or AWS/GCP Secrets Manager.

### 2. Broken Backend Docker Container (`DEP-01`)
- **Location:** [`mizan-web/backend/Dockerfile:18-24`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/Dockerfile#L18-L24).
- **Failure Cause:** Selective `COPY` directives omit [`sanad_aligner.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/sanad_aligner.py), [`scholarly_service.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/scholarly_service.py), the `ask_mizan` package, [`hadith_numbering.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_numbering.db), and [`hadith_commentaries.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_commentaries.db).
- **Exploit / Impact:** Container build fails to boot, crashing with `ModuleNotFoundError: No module named 'sanad_aligner'`. Institutional Docker deployment is completely blocked.
- **Remediation Strategy:** Replace brittle single-file copies with a comprehensive multi-stage build copying the backend directory and mounting `/data` as an external persistent volume.

### 3. Ask Mīzān Engine Runtime Crash (`RAG-01`)
- **Location:** [`mizan-web/backend/ask_mizan/engine.py:95`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py#L95).
- **Failure Cause:** `re.search` is called during canonical narrator ID resolution (`rawi:1234`), but `import re` was omitted from the module imports.
- **Impact:** Any user query containing canonical narrator citations triggers an unhandled 500 Internal Server Error.
- **Remediation Strategy:** Add `import re` at the top of [`ask_mizan/engine.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py).

---

## 5. Scholarly Correctness & Data Integrity Blueprint

### 1. Nass vs. Matn Slicing Remediation (`MODEL-01`, `MODEL-02`)
- **Database Reality:** In [`hadith-kg.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith-kg.db), the table `hadiths` uses column `matn` for authenticity verdicts ("صحيح"), while the continuous narration resides in `nass`. Character offsets `matn_start` and `matn_end` exist for 714,610 hadiths (99.83% of the corpus).
- **Current Defect:** The backend function [`extract_canonical_arabic_matn()`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py#L639) discards these offsets and returns `nass`, forcing the reader, Matn Diff viewer, and RAG prompt to display the entire Isnād chain prepended to the Prophetic wording.
- **Remediation Plan:**
  ```python
  # Target logic in extract_canonical_arabic_matn():
  if matn_start and matn_end and 0 <= matn_start < matn_end <= len(nass):
      pure_matn = nass[matn_start:matn_end].strip()
      return pure_matn, {"is_sliced": True, "start": matn_start, "end": matn_end}
  return nass.strip(), {"is_sliced": False, "reason": "offset_out_of_bounds"}
  ```
- **Benefits:**
  1. *Reader UI:* Prophetic text rendered prominently in calligraphic Amiri font with Isnād separated into a distinct contextual header.
  2. *Matn Diff Viewer:* Compares only prophetic wording variations, eliminating isnād differences.
  3. *RAG Context:* Reduces prompt token overhead by 40–60%, preventing context saturation and hallucination.

### 2. Separating Hadith Verdicts from Narrator Evaluative Remarks (`GRADE-02`)
- **Current Defect:** On [`hadith/[id]/page.tsx:1230`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/hadith/%5Bid%5D/page.tsx#L1230), the tab badge sums hadith verdicts with individual narrator biographical quotes: `(grades.length + narrator_statements.length)`. On Bukhari #1, it displays `"Grades (42)"` despite there being 0 hadith-level grades and 42 narrator biographical remarks.
- **Remediation Plan:**
  - Create two distinct UI sections:
    1. **Primary Authenticity Card:** Displays Hadith-level authenticity status (e.g. Sahih Bukhari editorial consensus; verdicts of al-Albani, Zubayr Ali Zai, Darussalam, Shu'ayb al-Arna'ut).
    2. **Transmitter Jarḥ wa Taʿdīl Dossier:** Displays narrator evaluations (Ibn Hajar, al-Dhahabi, al-Bukhari) categorized under the Narrators tab.
  - Badge on Authenticity Tab reflects strictly hadith-level external verdicts.

---

## 6. Search Engine Architecture Plan

### 1. Universal Citation Reference Parser (`SRCH-01`)
- **Current Defect:** The regex in [`main.py:243`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py#L243) (`r'^([a-zA-Z\s]+)\s+(\d+)$'`) strictly matches single spaces. Queries like `"Bukhari #1"`, `"Bukhari: 1"`, `"Bukhari, 1"`, and `"Muslim: 1"` fail and fall back to expensive, slow full-text search.
- **Remediation Plan:**
  1. Pre-process query: strip leading/trailing whitespace, replace colons, hashes, commas, and hyphens with single spaces.
  2. Match canonical collection aliases against a normalized dictionary:
     `{"bk": "bukhari", "sb": "bukhari", "sm": "muslim", "ad": "abu-dawud", ...}`.
  3. Query [`hadith_numbering.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_numbering.db) to resolve collection + number to `canonical_hadith_id` in < 1ms.

### 2. Complete Search Pagination (`SRCH-03`)
- **Current Defect:** [`search/page.tsx:108`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/search/page.tsx#L108) hardcodes `limit=50&offset=0`. Results 51+ are permanently inaccessible.
- **Remediation Plan:**
  - Implement full pagination state in Next.js search page (`page`, `limit=25`, `offset`).
  - Backend response returns `{ results: [...], total_matches: 482, page: 2, total_pages: 20 }`.
  - Render pagination navigation bar with direct page links and previous/next controls.

### 3. Removal of Status Column Pollution
- **Current Defect:** Query line 999 in [`main.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py) matches `h.matn LIKE ?`. Because `h.matn` stores authenticity status ("صحيح"), searching for the word "صحيح" returns all Sahih hadiths regardless of text.
- **Remediation Plan:** Exclude `h.matn` from textual search; search strictly against `h.nass` and the English FTS5 table.

---

## 7. Ask Mīzān RAG System Remediation

1. **Eliminate Runtime Crash (`RAG-01`):** Add `import re` to [`ask_mizan/engine.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py).
2. **Remove Hardcoded Test Artifacts:** In [`ask_mizan/engine.py:85`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py#L85), eliminate the hardcoded `rawi:4256` test patch and replace it with generic canonical narrator candidate resolution.
3. **Clean Grounding in Evidence Packs:** Feed pure sliced Matn (`nass[matn_start:matn_end]`) into evidence packs. This halves token consumption and anchors the LLM on the Prophetic wording.
4. **Mandatory Commentary Absence Disclaimers:** When a requested hadith has no commentary record in [`hadith_commentaries.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_commentaries.db), the synthesizer must explicitly output:  
   > *"No classical commentary is currently indexed for this hadith in Mīzān (indexed coverage: 1,202 hadiths)."*  
   The model must never infer or hallucinate commentary.

---

## 8. Frontend Architecture & UX Plan

### 1. Deconstruction of Hadith Detail Page (`FE-DECOMP-01`)
- **Current State:** [`hadith/[id]/page.tsx`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/hadith/%5Bid%5D/page.tsx) is a 1,601-line monolithic component managing 23 separate `useState` hooks.
- **Target Component Decomposition:**
  ```
  mizan-web/frontend/src/components/hadith/
  ├── HadithHeader.tsx             (Collection badges, chapter breadcrumb, edition tags)
  ├── HadithReaderCard.tsx         (Amiri calligraphic matn, font scaler, audio playback)
  ├── HadithSanadTree.tsx          (Vertical isnād chain preview with visualizer deep-link)
  ├── HadithGradesCard.tsx         (Authenticity status with source citations)
  ├── HadithCommentaryCard.tsx     (Classical sharh with primary/secondary scope tag)
  ├── HadithConcordanceTable.tsx   (Concordance table across 18 numbering systems)
  └── HadithInspectorDrawer.tsx    (Responsive slide-over drawer for narrator bio inspection)
  ```
- **File Reduction:** Drops `page.tsx` from 1,601 lines to ~220 lines.

### 2. Elimination of 12-Request HTTP Waterfall (`UX-01`)
- **Current State:** Hadith detail page fires 12 sequential un-cached fetch requests on every hadith navigation.
- **Solution:** Create composite endpoint `/api/hadith/{id}/dossier` returning the hadith text, sanad chain, numbering concordances, grades, and commentary in a single JSON payload.
- **Result:** Latency drops from ~950ms to ~180ms on mobile connections; layout shifts (CLS) are eliminated.

---

## 9. Visualization & Digital Humanities Graphics Plan

```
┌────────────────────────────────────────────────────────────────────────┐
│                   VISUALIZATION STRATEGY MATRIX                        │
├──────────────────────────┬─────────────────────────┬───────────────────┤
│ RETAIN & ENHANCE (2D)    │ RETAIN & REPAIR (Atlas) │ DEPRECATE (3D)    │
│ Isnād Network DAG        │ Geo Transmission Atlas  │ Matn 3D View      │
│ Add keyboard tabIndex    │ Disclose missing hops   │ Remove circular   │
│ and ARIA button roles    │ with counter badge      │ WebGL bloat       │
└──────────────────────────┴─────────────────────────┴───────────────────┘
```

1. **Isnād Network Graph (Canvas / SVG 2D):** **RETAIN & ENHANCE**. Highly valuable for analyzing transmission convergence points (Madār al-Isnād). Add keyboard accessibility (`tabIndex={0}`, `onKeyDown`), focus outline, and damp touch gesture conflicts.
2. **Transmission Geo Atlas:** **RETAIN & REPAIR**. Shows geographic spread from the Hijaz to Iraq, Syria, and Khorasan. Add explicit notification banner: *"Showing X of Y transmission hops (Z narrators lack geographical coordinates)"*. Never silently drop edges.
3. **Isnād Timeline (Tabaqāt):** **RETAIN & POLISH**. Essential for validating chronological continuity and death year gaps between student and teacher.
4. **Matn 3D View ([`MatnThreeDView.tsx`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/hadith-visualizer/MatnThreeDView.tsx)):** **DEPRECATE & REMOVE**. Places hadith nodes along an arbitrary circle by array index (`angle = idx * 2π/N`). Provides zero semantic or linguistic insight. Replace with high-precision 2D textual diff.

---

## 10. Commentary System Strategy

- **Corpus Reality:** [`hadith_commentaries.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_commentaries.db) contains 1,202 hadiths (0.168% coverage, strictly limited to the first ~200 hadiths of the Six Books). 419 auxiliary books have 0 commentary.
- **Certified Invariant:** Record #428 multi-hadith link (`sahih-bukhari:428` PRIMARY, `sahih-bukhari:429` SECONDARY) functions correctly and must remain protected.
- **UI Transparency Strategy:** Eliminate marketing copy implying a 425-book comprehensive commentary corpus. Display badge: *"Indexed Classical Commentary (Six Books Sample: 1,202 Hadiths)"*.
- **Expansion Roadmap:** Ingest complete *Fatḥ al-Bārī* (~7,563 hadiths) and *Sharḥ Ṣaḥīḥ Muslim* (~3,033 hadiths) from verified Shamela editions in Phase 3.

---

## 11. Scholar Grading Architecture & Provenance Plan

- **Current Dataset Reality:** 65,420 grades scraped from the "Hadith Pro" Android app covering only 5 books (Bukhari, Muslim, Ahmad have 0 grades). Classical hadith critics (al-Bukhari, Muslim, Ahmad, Yahya ibn Ma'in, Abu Hatim, al-Daraqutni, Ibn Hajar) are completely absent.
- **Muhammad Fouad Abd al-Baqi Role Reclassification:** Reclassify Abd al-Baqi (4,313 entries) from "grading scholar" to "Editor / Numbering Indexer" to reflect historical accuracy.
- **Classical Critics Ingestion Roadmap:** Ingest verdicts from classical *al-ʿIlal* and *al-Takhrīj* literature with explicit volume/page citations.

---

## 12. Performance & Web Vitals Optimization

| Optimization Initiative | File & Location | Current Impact | Target Post-Remediation |
| :--- | :--- | :--- | :--- |
| **Composite Dossier Endpoint** | [`main.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py) & [`page.tsx`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/hadith/%5Bid%5D/page.tsx) | 12 sequential HTTP requests (950ms) | Single request (< 200ms) |
| **Google Fonts Pipeline** | [`globals.css:1`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/globals.css#L1) | Render-blocking `@import` halts FCP (1.8s) | Preloaded via `next/font/google` (< 0.8s) |
| **Canvas Render Loop** | Visualizer Canvas components | Continuous 60fps RAF loop drains battery | Event-driven render on drag/zoom/hover |
| **HTTP Cache Headers** | [`main.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py) | Universal `cache: "no-store"` | `Cache-Control: public, max-age=86400` |

---

## 13. Accessibility & Mobile Responsiveness

- **Keyboard Navigation in Visualizers (`A11Y-01`):** Add `tabIndex={0}`, `role="button"`, `aria-label`, and `onKeyDown` handlers (Enter/Space to activate, Escape to close) on all SVG network nodes.
- **Color Contrast (`A11Y-03`):** Darken antique gold token from `#a77c38` to `#875c1e` for textual elements to satisfy WCAG AA 4.5:1 minimum contrast against parchment (`#f5f1e8`).
- **Mobile Inspector Bottom Sheet (`MOB-01`):** Replace fixed 380px drawer with a responsive bottom sheet (`max-height: 60vh`) on viewports < 768px.
- **Concordance Table Scrolling (`MOB-02`):** Wrap concordance table in responsive scroll container with sticky header and card view fallback on screens < 400px.

---

## 14. Database Architecture & Technical Debt

- **Zero-Mutation Canonical Databases:** Schema and records in [`hadith-kg.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith-kg.db) remain strictly untouched.
- **Column Aliasing in Application Layer:**
  ```sql
  SELECT id, nass AS full_text, matn AS authenticity_status, matn_start, matn_end FROM hadiths WHERE id = ?;
  ```
- **Translation Database Consolidation:** Consolidate 4 fragmented translation databases ([`english-search.db`](file:///c:/Users/taymi/discord-hadith-bot/data/english-search.db), [`english_translation_fts.db`](file:///c:/Users/taymi/discord-hadith-bot/data/english_translation_fts.db), [`hadith_translations.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_translations.db), [`translation-cache.db`](file:///c:/Users/taymi/discord-hadith-bot/data/translation-cache.db)) into a single verified repository database; archive dead backups to cold storage.
- **Clean Active Workspace:** Move 4.85 GB of dead backup files and 60+ loose test scripts to cold external archives.

---

## 15. Licensing, Provenance & Transparency

| Source | Content | Current License Status | Risk Level | Remediation Action |
| :--- | :--- | :---: | :---: | :--- |
| **Arabic Hadith Corpus** | 715k Arabic hadiths | Public Domain / Open Data | **NONE** | Credit Shamela and original transcribers on About/Sources page. |
| **Darussalam Translations** | 31,488 English translations | Commercial Copyright | **HIGH** | Conduct IP clearance review; add educational disclaimer; prepare open translation baseline. |
| **Hadith Pro Grading** | 65,420 scholar verdicts | Scraped mobile dataset | **MEDIUM** | Document app provenance; audit primary print editions. |
| **Classical Commentaries** | 1,202 classical texts | Public Domain | **NONE** | Document classical print editions used (*Fatḥ al-Bārī*, etc.). |

---

## 16. DevOps, Docker & CI/CD Pipeline

1. **Dockerfile Multi-Stage Build:** Correct `COPY` directives to bundle all backend Python modules and configure `/data` as an external mounted volume.
2. **Automated CI/CD Pipeline:** Implement GitHub Actions workflow running:
   - Python flake8 linting and type checking.
   - Pytest backend regression test suite.
   - Next.js frontend build and TypeScript validation.
3. **Secret Hygiene:** Ensure `.env` is permanently excluded from version control and provide `.env.example`.

---

## 17. System Architecture & Modernization

1. **APIRouter Decomposition:** Incrementally refactor the 5,262-line [`main.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py) into domain routers:
   - `routers/search.py`
   - `routers/hadiths.py`
   - `routers/isnad.py`
   - `routers/scholarly.py`
   - `routers/commentary.py`
   - `routers/concordance.py`
2. **Shared Hadith Core:** Unify query logic between the Discord bot ([`src/hadith_service.py`](file:///c:/Users/taymi/discord-hadith-bot/src/hadith_service.py)) and Web API into a shared `mizan_core` package.
3. **Monorepo Consolidation:** Consolidate the 4 unlinked nested `.git` repositories into a single unified Git repository.

---

## 18. Home Page Redesign Specification

- **Hero Value Proposition:**  
  *“The Rigorous Digital Humanities Platform for Hadith Research & Isnād Topology”*  
  Focus on scholarly authenticity, relational graph depth, and verifiable cross-edition concordances.
- **Unified Search Bar:** Universal reference search with live example chips: `"Bukhari 1"`, `"Muslim: 42"`, `"Tirmidhi #35"`, `"إنما الأعمال بالنيات"`.
- **Sihah Sittah Showcase:** Subtle 3D tilt cards on mouse hover with CSS perspective (respecting `prefers-reduced-motion`).
- **Live Statistics Strip:** Display verified numbers: 715,790 hadiths, 298,655 isnād edges, 49,844 narrators, 95,598 print concordances.

---

## 19. Complete Prioritized Master Backlog

| ID | Title | Domain | Priority | Complexity | Dependencies |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **`SEC-01`** | Rotate exposed Discord bot token and exclude `.env` | Security | **P0** | 10 min | Discord Developer Portal |
| **`DEP-01`** | Fix Dockerfile COPY directives to prevent startup crash | DevOps | **P0** | 15 min | None |
| **`RAG-01`** | Add missing `import re` in `ask_mizan/engine.py` | AI / RAG | **P0** | 5 min | None |
| **`SRCH-01`** | Support punctuation (`#`, `:`, `,`) in reference parser | Search | **P1** | 15 min | None |
| **`GRADE-02`**| Separate hadith verdicts from narrator quotes on UI tab | Scholarly UX | **P1** | 20 min | None |
| **`MODEL-02`**| Return `nass[matn_start:matn_end]` in matn extractor | Data Model | **P1** | 30 min | None |
| **`SRCH-03`** | Implement search pagination controls on `/search` | Search | **P1** | 1 hour | Backend pagination |
| **`UX-01`** | Build composite `/api/hadith/{id}/dossier` endpoint | Performance | **P1** | 3 hours | Backend endpoint |
| **`PERF-01`** | Migrate Google Fonts `@import` to `next/font/google` | Performance | **P1** | 20 min | None |
| **`A11Y-01`** | Add keyboard traversal to SVG visualizer nodes | Accessibility | **P1** | 2 hours | None |
| **`MATN-01`** | Deprecate decorative circular 3D Matn view | Visualization | **P2** | 1 hour | None |
| **`ISNAD-01`** | Disclose unlocalized narrators in Transmission Atlas | Visualization | **P2** | 45 min | None |
| **`FE-DECOMP-01`** | Decompose 1,601-line `hadith/[id]/page.tsx` | Architecture | **P2** | 1 day | Subcomponents |
| **`ARCH-MOD-01`** | Decompose `main.py` into FastAPI APIRouters | Architecture | **P2** | 2 days | Regression tests |
| **`LIC-01`** | Conduct Darussalam translation copyright clearance review | Licensing | **P2** | 1 week | Legal counsel |

---

## 20. Quick Wins Schedule

- **10 Minutes:**
  - Rotate `DISCORD_TOKEN` in Discord portal; add `.env` to `.gitignore` (`SEC-01`).
  - Add `import re` at top of [`ask_mizan/engine.py`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py) (`RAG-01`).
- **15 Minutes:**
  - Fix [`Dockerfile`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/Dockerfile) COPY directives to include all backend modules (`DEP-01`).
  - Strip citation punctuation (`#`, `:`, `,`) in `parse_external_reference_query` (`SRCH-01`).
- **20 Minutes:**
  - Separate hadith authenticity verdicts from narrator quotes on Hadith Detail badge (`GRADE-02`).
  - Migrate font `@import` in [`globals.css`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/globals.css) to `next/font/google` in `layout.tsx` (`PERF-01`).
- **30 Minutes:**
  - Activate `nass[matn_start:matn_end]` slicing in `extract_canonical_arabic_matn()` (`MODEL-02`).
- **1 Hour:**
  - Implement pagination controls and page parameter on `/search` page (`SRCH-03`).
- **3 Hours:**
  - Build composite `/api/hadith/{id}/dossier` endpoint and eliminate 12-fetch waterfall (`UX-01`).

---

## 21. 9-Sprint Implementation Roadmap

```
Sprint 0 (Week 1)   ──► Emergency Blockers (SEC-01, DEP-01, RAG-01, SEC-03)
Sprint 1 (Weeks 2-3)──► Scholarly Correctness (MODEL-02, GRADE-02, Abd al-Baqi Role)
Sprint 2 (Weeks 4-5)──► Search & Reader (SRCH-01, SRCH-03, Composite Dossier UX-01)
Sprint 3 (Weeks 6-7)──► Performance & Web Vitals (Font Pipeline, RAF Loop Damping, Caching)
Sprint 4 (Weeks 8-9)──► Frontend & Accessibility (Page Decomposition, SVG Keyboard A11Y-01)
Sprint 5 (Weeks 10-11)► Visualizations (Prune 3D Matn, Repair Atlas Transparency)
Sprint 6 (Weeks 12-13)► Ask Mīzān RAG (Clean Grounding, Commentary Disclaimers, Export Tools)
Sprint 7 (Weeks 14-15)► Architecture & DevOps (Decompose main.py, Monorepo Git, CI/CD)
Sprint 8 (Weeks 16-19)► Corpus & Scholarly Expansion (Complete Fath al-Bari, Classical Critics)
```

---

## 22. Strict Protected Invariants (DO NOT TOUCH LIST)

1. **715,790-Hadith Relational Knowledge Graph:** [`hadith-kg.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith-kg.db) is read-only.
2. **Precomputed Isnād Topology:** 298,655 directed narrator transmission edges in [`isnad_network.db`](file:///c:/Users/taymi/discord-hadith-bot/data/isnad_network.db) must remain intact.
3. **286-Record Zubayr Ali Zai Quarantine Gate:** [`scholarly_service.py:645`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/scholarly_service.py#L645) `is_quarantined_record()` logic must never be bypassed.
4. **Commentary Junction Architecture:** Record #428 PRIMARY/SECONDARY scope logic in [`hadith_commentaries.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_commentaries.db) must be preserved.
5. **Ask Mīzān Deterministic Offline Fallback:** Grounded evidence assembly must function without external API dependencies.
6. **Canonical Numbering Separation:** Darussalam English and Shamela Arabic numbering crosswalks must remain distinctly partitioned.
7. **Parchment / Emerald Aesthetic Language:** Design tokens (`#f5f1e8` parchment, `#195143` deep emerald, `#a77c38` gold) must remain the academic visual foundation.

---

## 23. Comprehensive System Scorecard

| Dimension | Baseline Score | Target Score | Justification |
| :--- | :---: | :---: | :--- |
| **Data Integrity** | 88/100 | **98/100** | Graph is intact; column naming semantics and offset slicing require application handling. |
| **Scholarly Correctness** | 62/100 | **95/100** | Conflated grade counters and discarded matn slicing degrade academic precision. |
| **Security** | 50/100 | **95/100** | Plaintext token in `.env` and missing rate limiting are severe blockers; easily remediated. |
| **Backend** | 65/100 | **92/100** | Monolithic 5,262-line `main.py` needs APIRouter modularization. |
| **Frontend** | 68/100 | **94/100** | 1,601-line hadith page needs decomposition into testable subcomponents. |
| **Search** | 60/100 | **96/100** | Brittle regex and hardcoded 50-item limit severely hinder research utility. |
| **RAG / Ask Mīzān** | 70/100 | **95/100** | Offline fallback is strong; missing import crashes narrator resolution; context needs slicing. |
| **Performance** | 64/100 | **94/100** | 12-fetch waterfall and render-blocking fonts cause high latency; dossier resolves this. |
| **Accessibility** | 45/100 | **95/100** | Previous 100% WCAG claim disproven; visualizers currently lack keyboard support. |
| **Mobile UX** | 55/100 | **92/100** | Fixed 380px drawer covers entire mobile screen; needs bottom sheet refactor. |
| **Visualization** | 65/100 | **92/100** | 2D graph is strong; decorative circular 3D matn view should be deprecated. |
| **Provenance** | 75/100 | **96/100** | Primary text lineage is clear; grading app scrape and translations need documentation. |
| **Licensing** | 55/100 | **88/100** | Darussalam translations require legal review and transparent attribution. |
| **Deployment** | 40/100 | **95/100** | Dockerfile currently broken; CI/CD absent; easily remediated. |
| **Maintainability** | 58/100 | **92/100** | 4 nested git repos and 4.85 GB dead backups clutter workspace. |
| **Documentation** | 72/100 | **95/100** | Forensic audits exist, but developer architecture guide and About/Sources page are missing. |
| **OVERALL SYSTEM** | **68/100** | **96/100** | **Disciplined execution of Sprints 0–4 elevates Mīzān to gold-standard academic status.** |

---

## 24. Final Executive Verdict (Answers to the 12 Questions)

1. **What is genuinely production-blocking?**  
   The backend Dockerfile startup crash (`DEP-01`), the live plaintext Discord bot token in root `.env` (`SEC-01`), and the Ask Mīzān `NameError` crash (`RAG-01`).
2. **What is scholarly-risky?**  
   Discarding verified `matn_start`/`matn_end` offsets and displaying full Isnād prepended to Prophetic text in reader and diff tools, and conflating transmitter biographical evaluations with hadith authenticity verdicts.
3. **What is misleading to users?**  
   Displaying tab badges like `"Grades (42)"` on Bukhari #1 when hadith grades = 0, and implying a comprehensive 425-book commentary corpus when only 1,202 hadiths have commentary data.
4. **What is merely ugly?**  
   60+ loose audit scripts in workspace root, 4.85 GB of dead backup databases in `data/`, and the orphan 0-byte file `1`.
5. **What is unnecessarily complicated?**  
   The circular 3D WebGL Matn view, dynamic SQLite `ATTACH DATABASE` operations on every request, and 23 `useState` hooks inside a single component.
6. **What is duplicated?**  
   Query and hadith classification logic between the Discord bot and Web API, and English translations across 4 separate databases.
7. **What is slow?**  
   The 12-request un-cached HTTP waterfall on hadith navigation (950ms+) and render-blocking Google Fonts `@import`.
8. **What is insecure?**  
   Plaintext credentials in `.env`, dynamic string concatenation in backend SQL queries, and absence of rate limiting.
9. **What should be fixed first?**  
   Sprint 0 emergency blockers: rotate secret token, fix Dockerfile, add `import re`, and sanitize citation punctuation in reference parser.
10. **What should NOT be touched?**  
    The 715,790 hadith graph, 298,655 isnād edges, 286 Zubayr quarantine gate, Record #428 scope, Ask Mīzān deterministic fallback, and parchment/emerald visual design tokens.
11. **What can wait?**  
    Classical critics *al-ʿIlal* ingestion, multi-recension manuscript variant apparatus, and full-corpus commentary ingestion (Sprint 8).
12. **What would give Mīzān the biggest quality improvement per engineering hour?**  
    **A Unified Scholarly Hadith Dossier Service and Clean Reader Pipeline:** Combining the composite `/api/hadith/{id}/dossier` endpoint with correct `matn_start:matn_end` text slicing and separated hadith vs. narrator verdicts. This single structural improvement simultaneously eliminates 70% of page latency, resolves text contamination across the reader, diff viewer, and RAG context, and restores academic credibility to the grading interface.
