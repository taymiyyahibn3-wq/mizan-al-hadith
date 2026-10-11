# MĪZĀN AL-ḤADĪTH — FORENSIC RE-AUDIT PHASE REPORT
## Jāmiʿ al-Tirmidhī — Shaykh Zubayr ʿAlī Zaʾī Grading Provenance & Identity Recovery

**Audit Date**: October 2, 2026  
**Auditor**: Forensic Hadith Integrity Agent (Mīzān al-Ḥadīth MVAP Engine v2.1)  
**Scope**: 100% Census Population Audit of All Hadith Grading Attributions to Ḥāfiẓ Zubayr ʿAlī Zaʾī in *Jāmiʿ al-Tirmidhī* (Book ID 3)  
**Execution Mode**: **STRICT ZERO-MUTATION (READ-ONLY)**  
**Target Directory**: `validation/zubayr_tirmidhi_reaudit/`

---

## 1. Executive Summary & Verdict

Following the forensic methodology proven during the *Sunan Ibn Mājah* investigation, a **complete, ground-up, read-only forensic re-audit** was conducted on all 3,858 grading records attributed to Shaykh Zubayr ʿAlī Zaʾī in *Jāmiʿ al-Tirmidhī* (`جامع الترمذي`).

### High-Level Verdict:
> **STOP — CRITICAL GRADING INTEGRITY FAILURE**
> 
> The current *Jāmiʿ al-Tirmidhī* Zubayr grading dataset in `hadith-kg.db` is **catastrophically compromised** and completely unsafe for production use.
> 
> - Only **39.45% (1,522 records)** match Shaykh Zubayr's actual verdict, and even those matches are largely **coincidental artifacts** of sequential displacement.
> - Fully **56.19% (2,168 records)** of the database gradings are **demonstrably WRONG**.
> - Fully **1,201 records (31.13% of the entire collection)** represent **CRITICAL GRADE INVERSIONS** (where Ṣaḥīḥ was falsely assigned to Ḍaʿīf narrations, or Ḍaʿīf was falsely assigned to authentic Ṣaḥīḥ narrations).

### Core Forensic Metrics Table

| Metric | Count | Percentage of Population | Forensic Status |
| :--- | :--- | :--- | :--- |
| **Total Tirmidhī Zubair Records** | **3,858** | **100.00%** | Full census population audited |
| **Identity Successfully Mapped** | **3,690** | **95.65%** | Textual sanad & matn verified |
| ↳ *Exact Textual Matches* | 3,150 | 81.65% | Substring containment in Darussalam Arabic |
| ↳ *Probable Textual Matches* | 540 | 14.00% | Jaccard lexical overlap $\ge 0.35$ |
| **Unmapped in Crosswalk (`hadith_numbers` Scheme 9)** | **168** | **4.35%** | Missing Darussalam scheme 9 mapping |
| **Authoritatively Source-Verified** | **3,629** | **94.06%** | Corroborated in Darussalam printed reference |
| **Correct Database Grades** | **1,522** | **39.45%** | Categorical agreement with true grade |
| **WRONG Database Grades** | **2,168** | **56.19%** | **Documented in `discrepancies.csv`** |
| **Numbering Displacements (`no_inbook` $\ne$ Darussalam)** | **3,666** | **95.02%** | Displaced across 216 offset transitions |
| **CRITICAL Grade Inversions** | **1,201** | **31.13%** | **Documented in `grade_inversion_cases.json`** |
| ↳ *Stored Ṣaḥīḥ $\rightarrow$ True Ḍaʿīf* | 432 | 11.20% | False authentication of weak hadiths |
| ↳ *Stored Ḍaʿīf $\rightarrow$ True Ṣaḥīḥ* | 437 | 11.33% | False rejection of authentic Sunnah |
| ↳ *Stored Ḥasan $\rightarrow$ True Ḍaʿīf* | 166 | 4.30% | False elevation of defective chains |
| ↳ *Stored Ḍaʿīf $\rightarrow$ True Ḥasan* | 166 | 4.30% | Suppression of sound narrations |
| **Source Conflicts (English Summary vs Arabic Isnād)** | **118** | **3.06%** | **Documented in `source_conflicts.csv`** |
| **Unresolved Cases** | **168** | **4.35%** | **Documented in `unresolved_cases.csv`** |

---

## 2. Definitive Answers to the 12 Mandatory Questions (Section 25)

### Q1: Is the current Tirmidhī Zubayr grading dataset reliable?
**ANSWER: NO. IT IS CATASTROPHICALLY UNRELIABLE.**  
With a defect rate of **56.19%** and **1,201 critical grading inversions**, over half the database claims in *Jāmiʿ al-Tirmidhī* contradict the published research of Ḥāfiẓ Zubayr ʿAlī Zaʾī.

### Q2: What percentage is demonstrably correct?
**ANSWER: 39.45% (1,522 records).**  
However, of these 1,522 matching records, **over 95%** match purely by accident because consecutive narrations in *Jāmiʿ al-Tirmidhī* happen to share the same broad grading category (e.g., blocks of Ṣaḥīḥ hadiths). The underlying database pointer is still structurally displaced.

### Q3: How many records are wrong?
**ANSWER: 2,168 records (56.19%).**  
Every one of these 2,168 records assigns a grade that is demonstrably false and contradicts the Darussalam reference edition.

### Q4: How many are critical grade inversions?
**ANSWER: Exactly 1,201 records (31.13% of the entire collection).**  
- **432 hadiths**: Stored as **Ṣaḥīḥ**, but Zubayr graded **Ḍaʿīf**.
- **437 hadiths**: Stored as **Ḍaʿīf**, but Zubayr graded **Ṣaḥīḥ**.
- **166 hadiths**: Stored as **Ḥasan**, but Zubayr graded **Ḍaʿīf**.
- **166 hadiths**: Stored as **Ḍaʿīf**, but Zubayr graded **Ḥasan**.

### Q5: How many errors are caused by numbering?
**ANSWER: 2,168 errors (100% of wrong grades).**  
In total, **3,666 out of 3,858 hadiths (95.02%)** suffer from numbering displacement between Shamela catalog sequence (`no_inbook`) and Darussalam continuous numbering. When the displaced numbers land on hadiths with different grades, a grading defect occurs (2,168 cases).

### Q6: How many are caused by duplicate/conflicting records?
**ANSWER: 0 duplicate rows exist in `hadith_grades` for Book 3.**  
Every hadith in Book 3 has exactly 1 grading row for Zubair Ali Zai. The errors stem entirely from cross-edition displacement, not duplicate rows.

### Q7: How many cannot currently be verified?
**ANSWER: Exactly 168 records (4.35%).**  
These 168 narrations currently lack a Darussalam continuous number in `hadith_numbers` (Scheme 9) and are fully cataloged in [unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/unresolved_cases.csv).

### Q8: What is the exact root cause?
**ANSWER:**  
In `hadith-pro/import_grades.py` (lines 87–98), the import pipeline executed:
```sql
SELECT id FROM hadiths WHERE book_id = ? AND no_inbook = ?
```
The script took `hadithnumber` from Hadith Pro (which represents **Darussalam continuous numbering**) and naively joined it against `hadiths.no_inbook` (which represents the **Shamela digital sequence**).  
Because Shamela and Darussalam undergo **216 separate offset transitions** across *Jāmiʿ al-Tirmidhī* (with offsets ranging from $+0$ to $+84$), `no_inbook` diverged from the true Darussalam number for **95.02% of the collection**. As a direct consequence, the database imported the grade of Hadith Pro Hadith #`no_inbook` onto Hadith ID `no_inbook` (which was actually Darussalam Hadith #`no_inbook + offset`).

### Q9: Which numbering scheme is responsible?
**ANSWER: The collision between `tirmidhi_shamela_seq` (Scheme 7) and `tirmidhi_darussalam_en` (Scheme 9).**  
The ETL joined the Darussalam scheme onto the Shamela scheme without using the numbering crosswalk.

### Q10: Can the current grading table safely be used in production?
**ANSWER: ABSOLUTELY NOT. (Verdict: STOP).**  
Production release with 1,201 critical grading inversions would propagate serious false authentications and false rejections of prophetic narrations.

### Q11: Which records require post-audit migration?
**ANSWER: 2,168 records require immediate grading correction, and 3,666 records require reference metadata re-alignment.**  
All 3,858 records should be migrated to derive their Zubayr grade directly through `hadith_numbering.db` Scheme 9.

### Q12: What exact architectural change is required to prevent recurrence?
**ANSWER:**  
1. **Abolish direct integer joins**: Permanently prohibit any ETL script from joining external grading sources to `hadiths.no_inbook`.
2. **Mandate Scheme-Grounded Grades**: The `hadith_grades` table must be foreign-keyed through `hadith_numbers.scheme_id` and `hadith_numbers.numeric_value`, explicitly binding every grade to its source edition.
3. **Dual Verdict Architecture**: Separate summary edition grades (e.g. Darussalam English) from specific isnād takhrij rulings (*Anwār al-Ṣaḥīfah*).

---

## 3. Forensic Case Studies & Landmark Proofs

### Case 1: `REG-ZUB-TIR-0001` — The Mandatory Landmark Guard (Repeating Intercourse)
- **Canonical Hadith ID**: `12529`
- **Database `no_inbook`**: `131`
- **True Darussalam Number**: `#141` (Offset: $+10$)
- **Arabic Sanad**:
  > حَدَّثَنَا هَنَّادٌ، حَدَّثَنَا حَفْصُ بْنُ غِيَاثٍ، عَنْ عَاصِمٍ الْأَحْوَلِ، عَنْ أَبِي الْمُتَوَكِّلِ، عَنْ أَبِي سَعِيدٍ الْخُدْرِيّ...
- **Arabic Matn**:
  > إذا أتى أحدكم أهله ثم أراد أن يعود فليتوضأ بينهما وضوءا...
- **Database Stored Grade**: `Daif`
- **True Zubayr Grade**: `Sahih Bukhari And Sahih Muslim` (Sahih Muslim #308)
- **Forensic Autopsy**:
  In Hadith Pro, Hadith `#131` is the narration of Ibn Umar regarding the menstruating woman reciting the Quran (`لا يقرأ الجنب ولا الحائض شيئا من القرآن`), which Shaykh Zubayr graded `Daif`.  
  The ETL pipeline imported `#131`'s weak grade onto Hadith ID `12529` solely because its `no_inbook` was `131`. But Hadith ID `12529` is actually Darussalam Hadith `#141` (the repeating intercourse narration, authentic in Sahih Muslim #308)!  
  This single displacement caused **all four scholars** on Hadith ID 12529 (Ahmad Shakir, Al-Albani, Bashar Awad, Zubair Ali Zai) to receive the false grade `Daif`.

---

### Case 2: `REG-ZUB-TIR-0057` — The Devil of Wudu (False Authentication)
- **Canonical Hadith ID**: `12450`
- **Database `no_inbook`**: `52`
- **True Darussalam Number**: `#57` (Offset: $+5$)
- **Arabic Matn**:
  > إن للوضوء شيطانا يقال له الولهان فاتقوا وسواس الماء...
- **Database Stored Grade**: `Sahih Muslim`
- **True Zubayr Grade**: `Daif`
- **Forensic Autopsy**:
  The database claims this notoriously weak narration regarding the devil of wudu (*al-Walhān*) is in **Ṣaḥīḥ Muslim**!  
  In reality, Shaykh Zubayr graded Darussalam Hadith `#57` as **Ḍaʿīf** (weak). The database assigned it `Sahih Muslim` because Darussalam Hadith `#52` was in Sahih Muslim, and the database imported `#52`'s grade onto `no_inbook = 52`.

---

### Case 3: `REG-ZUB-TIR-0062` — Maymunah Ghusl (False Rejection of Muttafaq 'Alayh)
- **Canonical Hadith ID**: `12455`
- **Database `no_inbook`**: `57`
- **True Darussalam Number**: `#62` (Offset: $+5$)
- **Arabic Matn**:
  > كنت أغتسل أنا ورسول الله صلى الله عليه وسلم من إناء واحد...
- **Database Stored Grade**: `Daif`
- **True Zubayr Grade**: `Sahih`
- **Forensic Autopsy**:
  The database labeled a **Muttafaq ʿAlayh hadith** (Bukhari #250, Muslim #321) as **Ḍaʿīf**!  
  Why? Because Darussalam Hadith `#57` was the weak *al-Walhān* narration, and the database imported `#57`'s weak grade onto `no_inbook = 57`.

---

## 4. Numbering Offset Shift Landscape across Jāmiʿ al-Tirmidhī

The displacement between Shamela catalog sequence (`no_inbook`) and Darussalam continuous numbering undergoes **216 distinct transition points**, with offsets reaching up to $+84$:

| Offset ($\Delta = \text{Dar} - \text{DB}$) | Number of Hadiths Affected | Percentage of Collection |
| :---: | :---: | :---: |
| **$+57$** | **322** | 8.35% |
| **$+81$** | **297** | 7.70% |
| **$+38$** | **217** | 5.62% |
| **$+84$** | **192** | 4.98% |
| **$+83$** | **192** | 4.98% |
| **$+56$** | **157** | 4.07% |
| **$+55$** | **152** | 3.94% |
| **$+74$** | **138** | 3.58% |
| **$+63$** | **127** | 3.29% |
| **$+54$** | **121** | 3.14% |
| **$+82$** | **118** | 3.06% |
| **$+35$** | **102** | 2.64% |
| **$+36$** | **90** | 2.33% |
| **$+0$ (No shift)** | **24** | **0.62%** |
| **Other Offsets** | **1,407** | 36.47% |

Only the first **24 hadiths** of *Jāmiʿ al-Tirmidhī* have $\Delta = 0$. For the remaining **95.02%**, raw integer joins are entirely invalid.

---

## 5. Source Conflict Analysis: English Summary vs. Arabic Isnād Takhrij

Our audit discovered **118 records** where the summary grade published in the Darussalam English translation diverges from Shaykh Zubayr's specific Arabic isnād ruling recorded in *Anwār al-Ṣaḥīfah*:

1. **Hadith #21**:
   - Darussalam English: `Hasan`
   - Arabic Notes: `ضعيف، إسناده ضعيف، ابو داود (27) ترمذي (21) ابن ماجه (304) انوار الصحيفه، صفحه نمبر 393`
2. **Hadith #34**:
   - Darussalam English: `Sahih`
   - Arabic Notes: `ضعيف¤ إسناده ضعيف¤ سنن أبي داود (129) ترمذي (34)¤ انوار الصحيفه، صفحه نمبر 394`
3. **Hadith #50**:
   - Darussalam English: `Hasan`
   - Arabic Notes: `ضعيف¤ إسناده ضعيف¤ ترمذي (50)¤ انوار الصحيفه، صفحه نمبر 394`
4. **Hadith #65**:
   - Darussalam English: `Sahih`
   - Arabic Notes: `ضعيف¤ إسناده ضعيف¤ سنن أبي داود (68) ترمذي (65) نسائي (326)¤ انوار الصحيفه، صفحه نمبر 395`

All 118 instances are preserved in [source_conflicts.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/source_conflicts.csv).

---

## 6. Zero-Mutation Verification & Cryptographic Proof

To ensure complete read-only integrity, SHA-256 hashes of all canonical database files were calculated immediately prior to the audit and verified immediately following execution:

| Database File | Pre-Audit SHA-256 Hash | Post-Audit SHA-256 Hash | Integrity Status |
| :--- | :--- | :--- | :---: |
| `data/hadith-kg.db` | `f2639d4c6249603ec0aeb83abdc3acd9701f477eac0a5f3560b1c0d428de04e3` | `f2639d4c6249603ec0aeb83abdc3acd9701f477eac0a5f3560b1c0d428de04e3` | **IMMUTABLE (100% BYTE MATCH)** |
| `data/hadith_numbering.db` | `ecfe3079dba318bde09f544eaf84764a9095a1ec12e0bd3446acf5f6428a66cb` | `ecfe3079dba318bde09f544eaf84764a9095a1ec12e0bd3446acf5f6428a66cb` | **IMMUTABLE (100% BYTE MATCH)** |
| `data/citation_enrichment.db` | `8e3a1d03ee6d3668314448acfbb227476cfd85c88b5fb8e57cb92abf5c6d4c37` | `8e3a1d03ee6d3668314448acfbb227476cfd85c88b5fb8e57cb92abf5c6d4c37` | **IMMUTABLE (100% BYTE MATCH)** |

Pre- and post-hashes are cryptographically recorded in:
- [database_hashes_pre.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/database_hashes_pre.json)
- [database_hashes_post.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/database_hashes_post.json)

---

## 7. Deliverables Manifest & Artifact Index

All deliverables for this re-audit have been written to the isolated directory:
`validation/zubayr_tirmidhi_reaudit/`

1. **[phase_report.md](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/phase_report.md)**: Full forensic report answering all 12 mandatory reliability questions.
2. **[population_manifest.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/population_manifest.json)**: Full census inventory of all 3,858 candidate records.
3. **[verified_grading_records.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/verified_grading_records.json)**: Complete audit entry for every single candidate record with textual identity matching evidence.
4. **[discrepancies.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/discrepancies.csv)**: 2,168 discrepancy records adhering strictly to the 16-column MVAP schema.
5. **[grade_inversion_cases.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/grade_inversion_cases.json)**: 1,201 severe grading inversions with textual comparisons and root-cause autopsies.
6. **[source_conflicts.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/source_conflicts.csv)**: 118 confirmed divergences between English summary grades and Arabic isnād takhrij.
7. **[unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/unresolved_cases.csv)**: 168 narrations lacking Darussalam continuous crosswalk mappings.
8. **[numbering_crosswalk_audit.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/numbering_crosswalk_audit.json)**: Full collation of DB `no_inbook`, Shamela sequence, and Darussalam number with offset distribution across 216 transition points.
9. **[zubayr_source_registry.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/zubayr_source_registry.json)**: Complete registry of ground-truth editions, volumes, and formats.
10. **[regression_results.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/regression_results.json)**: Regression test suite results, including `REG-ZUB-TIR-0001`, `0057`, `0062`, `REG-ZUB-IBNMAJAH-1986`, `0579`, and `REG-ZUB-0002`.
11. **[sampling_audit.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/sampling_audit.json)**: Stratified and adversarial audit samples across all 8 requested categories.
12. **[machine_validation_report.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/machine_validation_report.json)**: Machine-readable summary metrics and production safety status (`STOP`).
13. **[database_hashes_pre.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/database_hashes_pre.json)** & **[database_hashes_post.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_tirmidhi_reaudit/database_hashes_post.json)**: Cryptographic proof of zero database mutation.
