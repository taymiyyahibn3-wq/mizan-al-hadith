# PHASE 3 IMPLEMENTATION REPORT: ABŪ DĀWŪD + AL-NASĀʾĪ

## Executive Summary
Phase 3 of the Classical Scholar Expansion Program has been executed in full compliance with zero-trust scholarly standards.
Evidence has been ingested strictly for the two candidates certified by Phase 2 research as possessing directly attributable, Level A evidence in the canonical text:
1. **Imām Abū Dāwūd al-Sijistānī (d. 275 AH)**: 585 authorial remarks.
2. **Imām al-Nasāʾī (d. 303 AH)**: 151 authorial remarks.

Combined with the pre-existing **2,726 certified records of Imām al-Tirmidhī (d. 279 AH)**, the derived classical scholar database now houses **3,462 certified records**.

## Integrity & Preservation Baseline
- **Canonical Databases:** All 33 canonical databases were verified via SHA-256 before and after migration. **0 mutations (`PRE_HASH == POST_HASH`).**
- **Tirmidhī Baseline:** Exactly 2,726 records (1,918 explicit hadith grades, 808 criticisms) remain bit-for-bit invariant.
- **Derived Database:** `data/classical_scholar_evidence.db` was safely backed up to `data/classical_scholar_evidence.backup_before_phase3.db` prior to table population.

## Evidence Counts & Distribution
| Scholar | Total Records | Explicit Hadith Grades | Hadith Criticism / ʿIlal / Remarks | Primary Source | Mapping Level | Status |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **al-Imām al-Tirmidhī** | 2,726 | 1,918 | 808 | *Jāmiʿ al-Tirmidhī* | Level A | Certified Baseline |
| **al-Imām Abū Dāwūd** | 585 | 1 | 584 | *Sunan Abī Dāwūd* (`taraf_nass`) | Level A | **VERIFIED & IMPLEMENTED** |
| **al-Imām al-Nasāʾī** | 151 | 2 | 149 | *al-Sunan al-Ṣughrā* (`taraf_nass`) | Level A | **VERIFIED & IMPLEMENTED** |
| **TOTAL** | **3,462** | **1,921** | **1,541** | **Canonical Hadith Texts** | **Level A** | **VERIFIED** |

## Zero-Trust Boundary Enforcements
1. **No Inferred Grades from Silence:** Abū Dāwūd's silence principle was strictly respected as a general methodology, never converted into scalar grades.
2. **No Flattening into Binary Grades:** Critical remarks (*Munkar*, *Mursal*, *Laysa bi-qawī*, *Khaṭaʾ*, *Ashbahu bi-al-Ṣawāb*) are categorized under Classical Hadith Criticism with exact Arabic terminology preserved.
3. **No Deferred Scholars Implemented:** Aḥmad ibn Ḥanbal, al-Dāraquṭnī, al-Bukhārī, and Ibn Ḥajar remain deferred per Phase 2 decisions.
