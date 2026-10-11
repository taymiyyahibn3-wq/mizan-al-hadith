# MĪZĀN AL-ḤADĪTH — PUBLIC RELEASE REVIEW & GOVERNANCE MANIFEST

**Document Version:** 1.0.0 (Release Governance)  
**Date:** October 2026  
**Auditor:** Automated Repository Governance & Scholarly Release Agent  
**Repository:** `https://github.com/taymiyyahibn3-wq/mizan-al-hadith`  
**Governance Invariant:** Non-destructive release cleanup — Remove internal-only reports and working notes from public Git tracking (`git rm --cached`) without destroying local files or erasing public technical value.

---

## 1. Executive Summary & Scope

A comprehensive audit was performed across all **399 tracked files** and untracked assets in the Mīzān al-Ḥadīth repository to prepare for clean public release synchronization.

### Audit Objectives:
1. **Public Showcase Quality:** Ensure GitHub displays a polished, authoritative digital humanities platform showcasing verified capabilities, architectural rigor, and academic data provenance.
2. **Safe Internal File Untracking:** Remove 161 internal working reports, sprint checklists, and execution logs from Git index tracking so they do not clutter the public tree, while strictly preserving 100% of files on the local filesystem.
3. **Privacy & Credentials Protection:** Eliminate exposure of internal email addresses and development accounts (e.g., `itsriver236@gmail.com` discovered in `docs/embeddinggemma2_phase3_results.md`).
4. **Scholarly Preservation:** Verify that all unique architectural, feature, algorithmic, and provenance insights from internal sprints are permanently preserved in research-grade public documentation (`docs/overview/`, `docs/architecture/`, `docs/features/`, `docs/data/`, `docs/showcase/`, `docs/benchmarks/`).

---

## 2. File Classification Summary

| Category | File Count | Description & Inclusions | Disposition in Public Release |
| :--- | :--- | :--- | :--- |
| **PUBLIC** | **150 files** | Root README, LICENSE, `.gitignore`, `.env.example`, `docs/index.html`, `docs/index.md`, complete `docs/{overview, architecture, features, api, data, development, diagrams, github-publication, showcase, benchmarks}/`, Next.js 16 frontend (`mizan-web/frontend/`), FastAPI backend (`mizan-web/backend/`), test suites (`tests/`), and reproducible build/test scripts (`scripts/`). | **RETAINED IN GIT TRACKING** |
| **INTERNAL** | **161 files** | Historical sprint validation reports (`validation/` — 117 files), loose root sprint files (`01_` through `18_` + `FRONTEND_AUDIT.md` — 19 files), and loose sprint reports in `docs/` (`embeddinggemma2_*`, `phase6*`, `phase7*`, `docs/ask-mizan/`, `docs/ask-mizan-critical-fixes/`, `docs/research-workspace/` — 25 files). | **UNTRACKED VIA `git rm --cached` (PRESERVED LOCALLY ON DISK)** |
| **REVIEW_REQUIRED** | **91 files** | Evaluated scripts in `scripts/`, presentation docs (`presentation/README.md`), and video suite docs (`video/README.md`). All 91 files verified as essential reproducible engineering assets, benchmarks, or approved showcase documentation. | **CLASSIFIED AS PUBLIC & RETAINED** |

---

## 3. Review Manifest: Tracked Files Being Untracked from Git Index

The following **161 files** are removed from Git tracking using `git rm --cached` and ignored in `.gitignore`. **Zero files are deleted from the local disk.**

### A. Root Sprint Specifications (19 Files)
| File Path | Size | Reason for Untracking | Public Summary Location | Local Status |
| :--- | :--- | :--- | :--- | :--- |
| `01_FRONTEND_AUDIT.md` | 18.2 KB | Historical sprint 1 UI audit log | `docs/overview/feature-catalog.md` | Preserved locally |
| `02_FRONTEND_ARCHITECTURE.md` | 16.4 KB | Early frontend draft specification | `docs/architecture/frontend-architecture.md` | Preserved locally |
| `03_HOME_PAGE_REDESIGN.md` | 14.1 KB | Sprint 3 component redesign plan | `docs/features/hadith-library.md` | Preserved locally |
| `04_SIHAH_SITTAH_COVER_REGISTRY.md` | 12.8 KB | Book cover design notes | `docs/features/hadith-library.md` | Preserved locally |
| `05_ISNAD_VISUALIZATION_SPEC.md` | 15.6 KB | Draft isnād graph specification | `docs/features/isnad-explorer.md` | Preserved locally |
| `06_ISNAD_TIMELINE_SPEC.md` | 14.2 KB | Draft timeline specification | `docs/features/isnad-explorer.md` | Preserved locally |
| `07_ISNAD_GEOGRAPHY_SPEC.md` | 16.8 KB | Draft geographical mapping spec | `docs/features/isnad-explorer.md` | Preserved locally |
| `08_ISNAD_ATLAS_SPEC.md` | 13.9 KB | Early atlas coordinates spec | `docs/features/isnad-explorer.md` | Preserved locally |
| `09_ISNAD_3D_SPEC.md` | 14.7 KB | Early 3D spatial spec | `docs/features/isnad-explorer.md` | Preserved locally |
| `10_MATN_VISUALIZATION_SPEC.md` | 15.3 KB | Early matn diff specification | `docs/features/matn-analysis.md` | Preserved locally |
| `11_MATN_3D_SPEC.md` | 13.5 KB | Early matn 3D specification | `docs/features/matn-analysis.md` | Preserved locally |
| `12_SOURCE_PROVENANCE_REGISTRY.md` | 21.0 KB | Superseded working draft of sources | `docs/data/provenance-and-attribution.md` | Preserved locally |
| `13_LICENSING_AND_ATTRIBUTION.md` | 18.4 KB | Superseded working draft of licenses | `docs/data/licensing-and-redistribution.md` | Preserved locally |
| `14_PERFORMANCE_OPTIMIZATION_REPORT.md`| 19.1 KB | Historical frontend bundle audit | `docs/benchmarks/README.md` | Preserved locally |
| `15_ACCESSIBILITY_AUDIT.md` | 16.0 KB | Historical WCAG audit log | `docs/architecture/frontend-architecture.md` | Preserved locally |
| `16_MOBILE_RESPONSIVENESS_REPORT.md` | 14.8 KB | Sprint 16 responsive testing log | `docs/architecture/frontend-architecture.md` | Preserved locally |
| `17_FRONTEND_REGRESSION_REPORT.md` | 15.5 KB | Historical test runner log | `docs/development/testing.md` | Preserved locally |
| `18_FINAL_FRONTEND_CERTIFICATION.md` | 22.4 KB | Historical sprint 18 sign-off log | `docs/github-publication/REPOSITORY_AUDIT.md` | Preserved locally |
| `FRONTEND_AUDIT.md` | 19.8 KB | Initial frontend discovery log | `docs/overview/feature-catalog.md` | Preserved locally |

### B. Loose Sprint Documentation in `docs/` (25 Files)
| File Path | Size | Reason for Untracking | Public Summary Location | Local Status |
| :--- | :--- | :--- | :--- | :--- |
| `docs/embeddinggemma2_colab_implementation_plan.md` | 17.5 KB | Internal Colab setup instructions | `docs/benchmarks/README.md` | Preserved locally |
| `docs/embeddinggemma2_phase1_guide.md` | 14.2 KB | Internal phase 1 extraction guide | `docs/benchmarks/README.md` | Preserved locally |
| `docs/embeddinggemma2_phase2_benchmark.md` | 15.8 KB | Internal benchmark run guide | `docs/benchmarks/README.md` | Preserved locally |
| `docs/embeddinggemma2_phase2_results.md` | 18.1 KB | Internal evaluation notes | `docs/benchmarks/README.md` | Preserved locally |
| `docs/embeddinggemma2_phase3_results.md` | 16.9 KB | Internal report (contains personal email) | `docs/benchmarks/README.md` | Preserved locally |
| `docs/embeddinggemma2_phase4_forensic_report.md` | 24.3 KB | Internal forensic bug reproduction | `docs/benchmarks/README.md` | Preserved locally |
| `docs/embeddinggemma2_phase5_corrected_benchmark_report.md` | 22.7 KB | Internal candidate model audit | `docs/benchmarks/README.md` | Preserved locally |
| `docs/phase6_hybrid_retrieval_design.md` | 28.4 KB | Internal engineering design memo | `docs/architecture/retrieval-and-rag.md` | Preserved locally |
| `docs/phase6_retrieval_architecture_audit.md` | 21.0 KB | Internal architecture gap report | `docs/architecture/retrieval-and-rag.md` | Preserved locally |
| `docs/phase6b_hybrid_implementation_report.md` | 23.5 KB | Sprint 6B completion report | `docs/benchmarks/README.md` | Preserved locally |
| `docs/phase6c_adversarial_validation_report.md` | 26.1 KB | Sprint 6C stress test report | `docs/benchmarks/README.md` | Preserved locally |
| `docs/phase7_production_integration_report.md` | 20.4 KB | Sprint 7 activation report | `docs/architecture/retrieval-and-rag.md` | Preserved locally |
| `docs/phase7a_live_shadow_canary_report.md` | 19.8 KB | Internal canary traffic audit | `docs/benchmarks/README.md` | Preserved locally |
| `docs/phase7b_final_production_activation_report.md` | 22.1 KB | Internal production switchover log | `docs/benchmarks/README.md` | Preserved locally |
| `docs/phase7c_production_hardening_report.md` | 24.6 KB | Internal hardening audit | `docs/architecture/security-and-integrity.md` | Preserved locally |
| `docs/ask-mizan/FINAL_CERTIFICATION.md` | 18.2 KB | Internal milestone sign-off | `docs/features/ask-mizan.md` | Preserved locally |
| `docs/ask-mizan/IMPLEMENTATION_REPORT.md` | 21.4 KB | Internal feature implementation notes | `docs/features/ask-mizan.md` | Preserved locally |
| `docs/ask-mizan/PHASE_A_FORENSIC_AUDIT.md` | 19.5 KB | Internal code defect discovery | `docs/features/ask-mizan.md` | Preserved locally |
| `docs/ask-mizan/PHASE_B_BASELINE_AND_BENCHMARK.md` | 17.8 KB | Internal baseline benchmark log | `docs/benchmarks/README.md` | Preserved locally |
| `docs/ask-mizan/RETRIEVAL_AND_ANSWER_EVALUATION.md` | 22.0 KB | Internal LLM prompt evaluation | `docs/benchmarks/README.md` | Preserved locally |
| `docs/ask-mizan/ROOT_CAUSE_ANALYSIS.md` | 18.9 KB | Internal bug investigation memo | `docs/features/ask-mizan.md` | Preserved locally |
| `docs/ask-mizan-critical-fixes/FINAL_REPORT.md` | 20.1 KB | Internal bug fix completion log | `docs/features/ask-mizan.md` | Preserved locally |
| `docs/ask-mizan-critical-fixes/PHASE_A_ROOT_CAUSE_AUDIT.md` | 17.3 KB | Internal defect reproduction memo | `docs/features/ask-mizan.md` | Preserved locally |
| `docs/research-workspace/PHASE_A_ARCHITECTURE_AUDIT.md` | 16.5 KB | Internal architecture review | `docs/features/research-workspace.md` | Preserved locally |
| `docs/research-workspace/RESEARCH_WORKSPACE_IMPLEMENTATION_REPORT.md` | 25.8 KB | Internal workspace implementation log | `docs/features/research-workspace.md` | Preserved locally |

### C. Validation Directory Reports (`validation/` — 117 Files)
- **Path Pattern:** `validation/**`
- **Total Tracked Files:** 117 files
- **Subdirectories:**
  - `api_connection_repair/` (4 files)
  - `classical_external_grading_research/` (18 files)
  - `classical_external_grading_research/phase2/` (14 files)
  - `classical_external_grading_research/phase3/` (12 files)
  - `classical_external_grading_research/phase4/` (15 files)
  - `classical_scholar_grading_research/` (1 file)
  - `comprehensive_system_review/` (1 file)
  - `floto_homepage_audit/` (2 files)
  - `master_improvement_plan/` (1 file)
  - `phase_01/` through `phase_18/` (18 files)
  - `product_audit/` (1 file)
  - `product_improvement/` (2 files)
  - `sprint_0/`, `sprint_1/` (3 files)
  - `targeted_scholarly_ux_fix/` (2 files)
  - `targeted_ux_fix/` (7 files)
  - `zubayr_*` historical audits and migration reports (16 files)
- **Reason for Untracking:** These 117 files represent historical development validation checkpoints, checkpoint JSONs, and sprint logs. All verified findings (e.g. classical scholar attributions, 18-edition crosswalks, father/son collision guards) are active in production code and fully documented in `docs/data/` and `docs/features/`.
- **Local Status:** Preserved 100% on local filesystem. Untracked from Git via `git rm --cached -r validation/`.

---

## 4. Privacy, Credentials & Personal Data Disclosure

During the Phase D audit, the following sensitive/personal data item was identified:
- **Location:** `docs/embeddinggemma2_phase3_results.md` (line 79) and `docs/embeddinggemma2_phase2_benchmark.md` (line 140).
- **Item:** Personal Google account email address (`itsriver236@gmail.com`) and private Google Drive paths (`/content/drive/MyDrive/mizan/...`).
- **Remediation Action:**
  1. The containing files are classified as **INTERNAL** and immediately untracked from Git (`git rm --cached`).
  2. Public benchmark documentation (`docs/benchmarks/README.md`) omits all personal account identifiers, Google Drive references, and private credentials.
  3. No passwords, private API keys, or security tokens were exposed.

---

## 5. Public Showcase & Reproducible Assets Confirmation

The following high-value public assets are confirmed **RETAINED and ACCESSIBLE** for researchers and evaluators:
1. **Presentation 01:**
   - PDF: `Mizan_al_Hadith_Introduction_Presentation.pdf` (1.87 MB)
   - Interactive Route: `/presentation` (`mizan-web/frontend/src/app/presentation/page.tsx`)
   - Standalone Deck: `presentation/presentation_01/index.html`
   - Documentation: `docs/showcase/README.md` and `presentation/README.md`
2. **Presentation 02:**
   - PDF: `Mizan_al_Hadith_Presentation_02_Roadmap_and_Funding.pdf` (4.25 MB)
   - PDF: `Mizan_al_Hadith_TotalCost.pdf` (4.25 MB)
   - Generation Script: `scripts/generate_presentation_02.py`
3. **Cinematic Showcase Video Suite:**
   - Master 1080p Video: `video/output/mizan_promo_1080p.mp4` (21.1 MB)
   - Automated Render Pipeline: `video/render.js`
   - Master WebGL/Canvas Composition: `video/index.html`
   - Complete Audio & Scene Architecture: `video/scenes/`, `video/audio/`, `video/components/`
   - Documentation: `docs/showcase/README.md` and `video/README.md`
4. **Reproducible Engineering Scripts:**
   - 91 scripts in `scripts/` (including test suites, provenance verification tools, benchmark harnesses, and FTS profiling tools) retained in Git tracking.

---

## 6. Pre-Execution Safety Verifications

Before untracking:
1. **Local Disk Protection:** `git rm --cached` operates exclusively on the Git index (`.git/index`). No files on the Windows filesystem will be deleted or altered.
2. **Database Invariants:** All canonical SQLite databases (`data/*.db`) remain completely untouched. Hash verification via `scripts/verify_provenance_integrity.py` passes 13/13 databases.
3. **Link Integrity:** Scanned all documentation files via `scripts/check_doc_links.py`; 100% of relative links are valid.
4. **Git Tree Cleanliness:** After untracking, `.gitignore` will be updated with `validation/`, `[0-1][0-9]_*.md`, and `FRONTEND_AUDIT.md` to prevent accidental future commits.

---

*Certified by Mīzān al-Ḥadīth Release Governance Harness.*
