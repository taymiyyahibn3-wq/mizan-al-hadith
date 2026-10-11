# FEATURE — SCHOLARLY RESEARCH WORKSPACE

**Document Identifier:** `docs/features/research-workspace.md`  
**Frontend Routes:** `/workspace`, `/workspace/[projectId]`  
**Backend Endpoints:** 25 REST endpoints under `/api/workspace/*`  

---

## 1. Overview & Scholarly Objective

The Scholarly Research Workspace provides an isolated, persistent research laboratory for hadith scholars, students of knowledge, and academic researchers.

It allows researchers to organize investigations into structured projects, curate private evidence libraries, formulate scholarly claims, assemble claim-evidence matrices (supporting vs. challenging evidence), and export dossiers—all while maintaining absolute isolation from canonical datasets.

---

## 2. Core Functional Capabilities

```
+-----------------------------------------------------------------------------------+
|                        SCHOLARLY WORKSPACE SUBSYSTEM                              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  1. RESEARCH PROJECTS                                                             |
|     - Unique UUID, Title (Arabic/English), Description, Tags, Creation Timestamp  |
|                                                                                   |
|  2. EVIDENCE LIBRARY                                                              |
|     - Bookmarked Canonical Hadiths & Transmitters with Verified Snapshot Data     |
|     - Duplicate Protection Guard (409 Conflict)                                   |
|                                                                                   |
|  3. RESEARCH NOTES                                                                |
|     - Rich Text & Arabic Markdown Notes with Pinning and Color Categorization     |
|                                                                                   |
|  4. CLAIM-EVIDENCE MATRIX                                                         |
|     - Hypothesis Formulation (e.g., "Transmission Divergence in Kufa")           |
|     - Bi-directional Linking: "SUPPORTING" vs. "CHALLENGING" Evidence             |
|                                                                                   |
|  5. SIDE-BY-SIDE HADITH COMPARISON                                                |
|     - On-the-fly Lexical Overlap and Variant Alignment                            |
|                                                                                   |
|  6. PUBLICATION EXPORT                                                            |
|     - Single-Click Export to Markdown Dossier or Structured JSON                  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Privacy & Architectural Safeguards

1. **Complete Database Isolation:** All workspace tables reside strictly in `data/research_workspace.db`. It never writes to `hadith-kg.db` or any canonical database.
2. **Attribution Demarcation:** Workspace records are stamped with:
   ```json
   {
     "source_tier": "RESEARCHER_WORKSPACE",
     "is_canonical": false
   }
   ```
3. **Multi-User Header Isolation:** Enforced via `X-Researcher-Id` HTTP header. User A cannot view, mutate, or export User B's projects.
4. **Git Safety:** `data/research_workspace.db` is strictly ignored by `.gitignore` and never committed to source control.

---

## 4. Test Verification

The workspace subsystem is verified by `scripts/test_workspace_backend.py` covering 15 automated scenarios with 100% pass rate.
