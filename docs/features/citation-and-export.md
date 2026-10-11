# FEATURE — CITATION GENERATOR & DOSSIER EXPORT

**Document Identifier:** `docs/features/citation-and-export.md`  
**Frontend Route:** Integrated in `/hadith/[id]` & `/workspace/[projectId]`  
**Backend Endpoints:** `/api/workspace/projects/{id}/export`, `/api/hadith/{id}/citation`  

---

## 1. Overview & Scholarly Objective

To support academic publication and traditional research papers, Mīzān provides automated citation generation adhering to recognized international and Arabic bibliographical standards.

---

## 2. Citation Formats Generated

### 2.1 Chicago Manual of Style (Notes & Bibliography)
```text
محمد بن إسماعيل البخاري. صحيح البخاري, hadith no. 1. Mīzān al-Ḥadīth Canonical Digital Corpus.
```

### 2.2 Standard Arabic Classical Citation
```text
محمد بن إسماعيل البخاري، صحيح البخاري، حديث رقم 1، مستودع ميزان الحديث الرقمي.
```

### 2.3 Comprehensive Provenance & Crosswalk Citation
Includes In-Book Chapter and International Concordance number:
```text
Ṣaḥīḥ al-Bukhārī, Book 1 (Revelation), Hadith 1; In-Book #1; Darussalam Edition #1.
```

---

## 3. Dossier Export Subsystem

Within the Research Workspace (`/workspace/[projectId]`), scholars can export their entire investigation into a publication-ready package:
- **Markdown Dossier (`.md`):** Contains executive summary, project description, categorized evidence table, research notes, and formulated claims with their supporting/challenging matrices.
- **Machine-Readable JSON (`.json`):** Full relational dump for integration with Python data science pipelines or digital humanities platforms.
