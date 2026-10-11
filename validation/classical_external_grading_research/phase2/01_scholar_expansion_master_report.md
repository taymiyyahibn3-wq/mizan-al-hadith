# MĪZĀN AL-ḤADĪTH — CLASSICAL SCHOLAR EXPANSION PROGRAM
## PHASE 2: EXTERNAL HADITH-LEVEL EVIDENCE MASTER RESEARCH REPORT

**Program Status:** Complete Research Audit  
**Program Architecture:** Zero-Trust Scholarly Provenance & Multi-Layer Classical Evidence  
**Scope:** Priority 1 & Priority 2 Classical Hadith Critics (Aḥmad, al-Dāraquṭnī, al-Bukhārī, Ibn Ḥajar, Abū Dāwūd, al-Nasāʾī, ʿAlī ibn al-Madīnī)  
**Certified Baseline:** Imām al-Tirmidhī (2,726 autographic records; 1,918 Explicit Grades, 808 Hadith Criticism)  
**Date:** October 7, 2026  

---

## 1. Executive Summary & Core Research Decision

The purpose of Phase 2 is to determine whether additional classical hadith critics possess **verified, attributable, machine-usable, hadith-level evaluations** that can safely be integrated into Mīzān al-Ḥadīth without violating scholarly integrity rules.

### Core Scholarly Principle
> **EVIDENCE > COVERAGE**  
> **PRIMARY SOURCES > AGGREGATORS**  
> **PROVENANCE > CONVENIENCE**  
> **DETERMINISTIC MAPPING > ASSUMPTION**  
> **EXACT TERMINOLOGY > NORMALIZATION**  
> **SCHOLARLY FIDELITY > UI COMPLETENESS**  

### Master Assessment Findings
1. **Certified Implemented Authority:**
   - **al-Imām al-Tirmidhī (d. 279 AH):** 2,726 records in `data/classical_scholar_evidence.db` (1,918 Explicit Grades, 808 Classical Criticism). 100% deterministic row-level mapping in Book 3.
2. **Prime Candidates for Dedicated Phase 3 Ingestion Pass:**
   - **Abū Dāwūd al-Sijistānī (d. 275 AH):** 585 explicit authorial remarks (`قال أبو داود`) directly preserved in Book 4 (`taraf_nass`) of Mīzān's canonical database. These constitute valuable **Classical Hadith Criticism** (e.g. *Munkar*, isnād defects, variant comparisons). *Status: DEFER_MANUAL_VERIFICATION* (to prevent premature scalar grade conflation; silence rule strictly observed).
   - **al-Nasāʾī (d. 303 AH):** 151 explicit authorial remarks (`قال أبو عبد الرحمن`) directly preserved in Book 5 (`taraf_nass`). These constitute valuable **Classical Hadith Criticism & Variant Preference** (e.g. *Ashbahu bi-al-Ṣawāb*, *Khaṭaʾ*, *Mursal*). *Status: DEFER_MANUAL_VERIFICATION*.
3. **Scholars Requiring Specialized Relational Mapping Subsystems (Deferred):**
   - **al-Dāraquṭnī (d. 385 AH):** *al-ʿIlal al-Wāridah* (4,136 monographs across 15 volumes) contains peerless isnād defect analysis. However, its question/answer structure cannot be compressed into a scalar grade without destroying its scholarly value. Requires a specialized *ʿIlal Variant Relational Schema*. *Status: DEFER_SPECIALIZED_MAPPING*.
   - **Aḥmad ibn Ḥanbal (d. 241 AH):** *al-ʿIlal wa-Maʿrifat al-Rijāl* (4,115 entries) and *Masāʾil* contain ~600 hadith-level judgments. However, entries are indexed only by question number and lack an open, machine-actionable crosswalk to Sihah Sittah hadith IDs. *Status: DEFER_SPECIALIZED_MAPPING*.
   - **al-Bukhārī (d. 256 AH):** Collection inclusion in *Ṣaḥīḥ al-Bukhārī* is collection metadata, not an explicit grade. Oral rulings transmitted via Tirmidhī in *al-Jāmiʿ* require a secondary compiler attribution model. *Status: DEFER_SPECIALIZED_MAPPING*.
   - **Ibn Ḥajar al-ʿAsqalānī (d. 852 AH):** *Bulūgh al-Marām* (~1,500 hadiths) contains explicit rulings, but ~70% are quotations of earlier authorities (al-Tirmidhī, Ibn Ḥibbān, al-Ḥākim, al-Dāraquṭnī). Ingesting them requires an automated attribution parser to prevent misattributing quoted verdicts to Ibn Ḥajar. *Status: DEFER_SPECIALIZED_MAPPING*.
4. **Scholars Without Discrete Hadith-Level Grading Data (Rejected from Hadith Layer):**
   - **ʿAlī ibn al-Madīnī (d. 234 AH):** Evidence is overwhelmingly narrator-level (*Madār al-Isnād* and biographical criticism), already indexed in Mīzān's `aqwal` layer (720+ statements).
   - **Yaḥyā ibn Maʿīn (d. 233 AH):** Pure transmitter evaluation (*Jarḥ wa Taʿdīl*), already indexed in Mīzān's `aqwal` layer (3,293 statements). Rule 1 strictly forbids inferring hadith grades from narrator evaluations.

---

## 2. Generalized Classical Scholarly Evidence Model (Part 16)

To support multiple classical scholars without hardcoded ad-hoc logic, Mīzān establishes a generalized, extensible data architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    SCHOLAR ENTITY                           │
│  (id, name_en, name_ar, death_year, era, primary_field)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     WORK / CORPUS                           │
│  (id, scholar_id, title_en, title_ar, genre, transmission)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  SCHOLARLY EVALUATION                       │
│  - evaluation_id                                            │
│  - scholar_id (Original Authority)                          │
│  - compiler_id (Compiler / Work Author)                     │
│  - transmitter_id (Intermediate Transmitter, if any)       │
│  - work_id                                                  │
│  - evidence_type (EXPLICIT_GRADE | CRITICISM | ILAL | etc.) │
│  - canonical_term (Ḥasan Ṣaḥīḥ | Munkar | etc.)             │
│  - verbatim_arabic (Exact original text)                    │
│  - full_context_arabic (Full passage)                       │
│  - hadith_id (Mīzān Hadith ID)                              │
│  - source_reference (Book, Chapter, Hadith #, Question #)   │
│  - mapping_level (A_DETERMINISTIC | B_MULTI_KEY | etc.)     │
│  - attribution_model (DIRECT | QUOTED | TRANSMITTED)        │
│  - license (Public Domain / CC-BY-SA)                       │
│  - verification_status (VERIFIED_PRIMARY_SOURCE)            │
└─────────────────────────────────────────────────────────────┘
```

This model guarantees:
1. **Multi-Scholar Extensibility:** Can store Tirmidhī, Abū Dāwūd, al-Nasāʾī, Aḥmad, Dāraquṭnī, and Ibn Ḥajar in identical normalized tables.
2. **Attribution Separation:** Distinguishes the original speaker from the quoting author (preventing the "Ibn Ḥajar said X" error when he was quoting al-Dāraquṭnī).
3. **Controlled Evidence Classification:** Keeps Explicit Hadith Grades cleanly segregated from Isnād Defect remarks and Narrator Jarḥ wa Taʿdīl.

---

## 3. Decision Summary Table

| Scholar | Death AH | Primary Work | Candidate Evidence | Mapping Level | Implementation Decision |
|---|---|---|---|---|---|
| **al-Tirmidhī** | 279 | *al-Jāmiʿ al-Kabīr* | 2,726 authorial statements | LEVEL A | **IMPLEMENT (Certified Baseline)** |
| **Abū Dāwūd** | 275 | *al-Sunan* | 585 remarks in Book 4 | LEVEL A | **DEFER_MANUAL_VERIFICATION (Phase 3 Candidate)** |
| **al-Nasāʾī** | 303 | *al-Sunan al-Ṣughrā* | 151 remarks in Book 5 | LEVEL A | **DEFER_MANUAL_VERIFICATION (Phase 3 Candidate)** |
| **Aḥmad ibn Ḥanbal** | 241 | *al-ʿIlal wa-Maʿrifat al-Rijāl* | 4,115 question entries | LEVEL D | **DEFER_SPECIALIZED_MAPPING** |
| **al-Dāraquṭnī** | 385 | *al-ʿIlal al-Wāridah* | 4,136 variant monographs | LEVEL D | **DEFER_SPECIALIZED_MAPPING** |
| **al-Bukhārī** | 256 | *al-Tārīkh* / *al-ʿIlal via Tirmidhī* | ~450 oral rulings in Tirmidhī | LEVEL C | **DEFER_SPECIALIZED_MAPPING** |
| **Ibn Ḥajar** | 852 | *Bulūgh al-Marām* | 1,596 takhrīj & rulings | LEVEL B | **DEFER_SPECIALIZED_MAPPING** |
| **ʿAlī ibn al-Madīnī** | 234 | *Kitāb al-ʿIlal* | Transmitter notices only | LEVEL E | **DO_NOT_IMPLEMENT_NO_DATA** |
| **Yaḥyā ibn Maʿīn** | 233 | *Tārīkh Ibn Maʿīn* | Narrator evaluations only | LEVEL E | **DO_NOT_IMPLEMENT_NO_DATA** |

---

## 4. Final Recommendation & Overall Status

In accordance with Part 24:
> "It is completely acceptable for the final result to be: Tirmidhī → IMPLEMENT, Aḥmad → DEFER, Dāraquṭnī → DEFER, Bukhārī → DEFER, Ibn Ḥajar → DEFER, Abū Dāwūd → DEFER, Nasāʾī → DEFER, if that is what the evidence actually supports. Do not force implementation."

Therefore, the certified final status for Phase 2 is:

```
CLASSICAL SCHOLAR EXPANSION — RESEARCH COMPLETE, PARTIAL IMPLEMENTATION
```