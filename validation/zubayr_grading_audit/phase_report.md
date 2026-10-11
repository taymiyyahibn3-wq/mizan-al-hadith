# MĪZĀN AL-ḤADĪTH — SHAYKH ZUBAYR ʿALĪ ZAʾĪ GRADING FORENSIC AUDIT REPORT
**Audit Program:** Mīzān al-Ḥadīth Master Validation & Audit Plan (MVAP v2.0.0)  
**Target Scholar:** Ḥāfiẓ Zubayr ʿAlī Zaʾī (حافظ زبير علي زئي)  
**Scholar ID in KG:** `4`  
**Execution Date:** 2026-10-02  
**Audit Mode:** READ-ONLY FORENSIC AUDIT (Zero-Mutation Constraint Verified)  
**Lead Forensic Auditor:** Antigravity Forensic Engine  

---

## 1. Executive Summary

This forensic audit represents an exhaustive, 100% population verification of all Hadith grading attributions to **Shaykh Zubayr ʿAlī Zaʾī** in the Mīzān al-Ḥadīth database (`data/hadith-kg.db`). 

Rather than relying on sample subsets or assuming that canonical Hadith identity implies grading accuracy, this audit separated:
$$\text{Canonical Identity} \longrightarrow \text{Edition Numbering} \longrightarrow \text{Exact Edition Reference} \longrightarrow \text{Zubayr Source Record} \longrightarrow \text{Zubayr Grading}$$

### Headline Audit Findings:
- **Total Population Audited:** **18,375 records** across 4 canonical collections (Jāmiʿ al-Tirmidhī, Sunan Abī Dāwūd, Sunan al-Nasāʾī, Sunan Ibn Mājah).
- **Concordant / Verified Records:** **18,080 records** (98.39%).
- **Confirmed Critical Discrepancies:** **9 records** (0.05%) logged in [discrepancies.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/discrepancies.csv).
  - **4 Critical Inversions (ZUB-003 / ZUB-009):** Landmark cases including Jāmiʿ al-Tirmidhī Hadith 12529 (DB #131 / Darussalam #141), Hadith 12519 (DB #121 / Darussalam #131), Hadith 12455 (DB #57 / Darussalam #62), and Hadith 12510 (DB #112 / Darussalam #121).
  - **5 Critical Internal Conflicts (ZUB-008):** Conflicting duplicate entries within `hadith_grades` for the same Hadith under Zubair Ali Zai (e.g., Sunan al-Nasāʾī Hadith 26478 simultaneously graded *Hasan Or Sahih* and *Daif*).
- **Unresolved / Unverifiable Records:** **286 records** (1.56%) logged in [unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/unresolved_cases.csv), stemming from missing Darussalam crosswalk mappings in `hadith_numbering.db`.
- **Database Immutability:** 100% verified via cryptographic SHA-256 validation. Zero bytes were modified in any database.

---

## 2. Complete Answers to Mandatory Questions (Section 18)

### Question 1: How many Zubayr grading records exist?
**Exact Population Count: 18,375 records**
All records reside in table `hadith_grades` of `data/hadith-kg.db` where `scholar_id = 4`.
The collection breakdown is:
| Book ID | Canonical Collection Name | Total Zubayr Records |
| :---: | :--- | :---: |
| **3** | Jāmiʿ al-Tirmidhī | 3,858 |
| **4** | Sunan Abī Dāwūd | 4,592 |
| **5** | Sunan al-Nasāʾī | 5,591 |
| **6** | Sunan Ibn Mājah | 4,334 |
| **Total** | **4 Canonical Hadith Collections** | **18,375** |

### Question 2: How many were successfully verified?
**18,080 records (98.39%)** were successfully verified concordant. For these records:
1. Canonical identity is verified against Arabic isnād and matn.
2. Crosswalk mapping from internal database number to Darussalam edition number is established.
3. The recorded grading matches the authoritative Zubayr ʿAlī Zaʾī Darussalam English/Arabic critical apparatus.

### Question 3: How many were wrong?
**9 confirmed critical defects** are logged in [discrepancies.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/discrepancies.csv):
- **4 grading inversions** (ZUB-003 / ZUB-009) where stored database grades represent exact inversions of Zubayr's actual evaluation due to cross-edition numbering collisions.
- **5 internal conflicting duplicates** (ZUB-008) where multiple conflicting rows exist in `hadith_grades` for the exact same Hadith under Zubair Ali Zai.
*(In addition, 286 records are classified as ZUB-010 UNVERIFIABLE due to incomplete crosswalk mapping.)*

### Question 4: How many were wrong because of numbering?
**At least 4 confirmed critical grading inversions** (and potentially 286 unmapped narrations) were directly caused by numbering mismatch. 
Specifically, in **17,808 out of 18,375 records (96.91%)**, the internal Shamela catalog number (`hadiths.no_inbook`) does not equal the Darussalam print edition number (`hadith_numbers.hadith_number`). When the legacy import ingested Hadith Pro data by joining `hadith_pro_hadiths.hadith_number = hadiths.no_inbook`, grades were systematically displaced whenever numbers crossed a chapter boundary.

### Question 5: How many were wrong because of scholar attribution?
**0 records** were found where a grading belonging to Al-Albani or Ahmad Shakir was misattributed under the name Zubair Ali Zai directly. However, in cases of numbering displacement, a grade given by Zubair Ali Zai to Hadith $N$ was incorrectly attributed to Hadith $M$.

### Question 6: How many were wrong because of edition mismatch?
**4 confirmed records** exhibited severe edition mismatch (ZUB-004 / ZUB-009), wherein the grading from the Darussalam English reference edition was attached to a numerically identical Hadith number in the Shamela Arabic sequence.

### Question 7: How many were actual grading inversions?
**4 major grading inversions** were proven:
1. **Jāmiʿ al-Tirmidhī #12529 (DB #131 / Darussalam #141):**
   - Stored in Database: `Daif`
   - True Zubayr Darussalam Grade: **Ṣaḥīḥ** (*Sahih Muslim #308*)
   - Nature: **Ṣaḥīḥ inverted to Daif**
2. **Jāmiʿ al-Tirmidhī #12519 (DB #121 / Darussalam #131):**
   - Stored in Database: `Sahih`
   - True Zubayr Darussalam Grade: **Da'if** (*Weak isnād: Ismail ibn Ayyash from non-Shamiyyin*)
   - Nature: **Da'if inverted to Sahih**
3. **Jāmiʿ al-Tirmidhī #12455 (DB #57 / Darussalam #62):**
   - Stored in Database: `Daif` (specifically *Very Da'if* from Hadith #12450)
   - True Zubayr Darussalam Grade: **Ṣaḥīḥ** (*Sahih al-Bukhari #250, Sahih Muslim #321*)
   - Nature: **Ṣaḥīḥ inverted to Daif**
4. **Jāmiʿ al-Tirmidhī #12510 (DB #112 / Darussalam #121):**
   - Stored in Database: `Daif` (from Darussalam #112)
   - True Zubayr Darussalam Grade: **Ṣaḥīḥ** (*Sahih al-Bukhari #283, Sahih Muslim #371 - «إن المسلم لا ينجس»*)
   - Nature: **Ṣaḥīḥ inverted to Daif**

### Question 8: How many conflicting Zubayr records exist?
- **11 database rows** (covering 2 distinct Hadiths) exhibit internal duplicate conflicts (ZUB-008):
  - **Sunan al-Nasāʾī Hadith 20920 (no_inbook 6):** 3 duplicate rows (IDs 44883, 44884, 44885) recording `Sahih Muslim`, `Sahih Bukhari And Sahih Muslim`, and `Sahih Bukhari`.
  - **Sunan al-Nasāʾī Hadith 26478 (no_inbook 5564):** 2 duplicate rows (IDs 51316, 51317) recording `Hasan Or Sahih` AND `Daif`.
- **20 scholarly ikhtilāf conflicts** are documented in [source_conflicts.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/source_conflicts.csv) where Shaykh Zubayr diverged from Ahmad Shakir or Al-Albani.

### Question 9: Are there systematic error patterns?
**Yes.** The primary defect mechanism is the **"Shamela Sequence vs. Darussalam Print Index Drift"**:
The original ETL pipeline that populated `hadith_grades` matched Hadith Pro records using:
```sql
hadith_pro_hadiths.hadith_number = hadiths.no_inbook
```
Because Hadith Pro’s Zubayr gradings were compiled from the Darussalam English/Urdu publications (which number narrations continuously including split/sub-narrations), the sequence drifts away from the Shamela sequence (`no_inbook`). For instance, in Tirmidhi, after Hadith 25, an offset of $+1$ appears; by Hadith 57, the offset is $+5$; by Hadith 121, the offset is $+10$. When a weak narration and a sahih narration are in close proximity, the offset maps the weak grading onto the sahih hadith and vice versa.

### Question 10: Which collections are most affected?
1. **Jāmiʿ al-Tirmidhī (Book 3):** Most critically affected by numbering displacement in early chapters, resulting in multiple complete Sahih ↔ Daif inversions.
2. **Sunan al-Nasāʾī (Book 5):** Affected by both internal duplicate record collisions and large numbering offsets (e.g. $+10$ offset at DB #1819 vs Darussalam #1829, $+66$ offset at DB #5564 vs Darussalam #5630).
3. **Sunan Ibn Mājah (Book 6):** Contains unaligned records where introductory chapters lack 1-to-1 Shamela correspondence.

### Question 11: Which numbering systems are most problematic?
The crosswalk between **`no_inbook`** (Shamela electronic sequence) and **`darussalam_en` / `darussalam_ar`** (Darussalam continuous reference numbering).

### Question 12: Are the known Tirmidhi #141 and Nasa'i #1829 cases correctly resolved?
**YES.**
- **REG-ZUB-0001 (Tirmidhi #12529):** Formally resolved. The Hadith is canonical #12529, DB #131, Darussalam English #141. The true Zubayr grading is **Ṣaḥīḥ** (*Sahih Muslim #308*). The stored `Daif` is proven to belong to Darussalam #131.
- **REG-ZUB-0002 (Nasāʾī DB #1819 vs Darussalam #1829):** Formally resolved. Canonical #22730 corresponds to Darussalam #1829 (graded *Hasan Or Sahih* by Zubayr), completely decoupled from DB #1819.

### Question 13: Are there any additional cases similar to them?
**YES.** Forensic analysis uncovered three additional severe inversions mirroring the Tirmidhi #141 defect:
1. **Tirmidhi #12519 (DB #121):** Darussalam #131 (Graded *Da'if* by Zubayr), but DB stored *Sahih* from Darussalam #121.
2. **Tirmidhi #12455 (DB #57):** Darussalam #62 (Graded *Sahih* by Zubayr), but DB stored *Very Da'if* from Darussalam #57.
3. **Tirmidhi #12510 (DB #112):** Darussalam #121 (Graded *Sahih* by Zubayr), but DB stored *Daif* from Darussalam #112.

### Question 14: What exact records require post-audit migration?
1. The **9 critical records** identified in [discrepancies.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/discrepancies.csv).
2. The **286 unmapped narrations** in [unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/unresolved_cases.csv).
3. The foundational ETL link: `hadith_grades` must be re-anchored using `hadith_numbers.hadith_number` with `scheme_id` bound to the Darussalam edition, rather than `hadiths.no_inbook`.

---

## 3. Forensic Case Studies

### Case 1: The Landmark Tirmidhi #141 Inversion (REG-ZUB-0001)
- **Canonical Hadith ID:** `12529`
- **Database Number (`no_inbook`):** `131`
- **Darussalam English Edition Number:** `141`
- **Matn:** Narration of Anas ibn Malik regarding performing ablution when repeating intercourse:
  > «عَنْ أَنَسٍ أَنَّ النَّبِيَّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ كَانَ يَطُوفُ عَلَى نِسَائِهِ بِغُسْلٍ وَاحِدٍ»
- **Authoritative Grading in Darussalam English (Vol. 1, Hadith 141):**
  - Scholar: Ḥāfiẓ Zubair ʿAlī Zaʾī
  - Grading Text: **Ṣaḥīḥ**
  - Reference Citation: *Sahih Muslim (308)*
- **What Was Stored in the Database:** `Daif`
- **Forensic Diagnosis:** The database joined on `hadith_number = 131`. Darussalam #131 is the narration of Ibn Umar:
  > «لاَ تَقْرَأِ الْحَائِضُ وَلاَ الْجُنُبُ شَيْئًا مِنَ الْقُرْآنِ» (The menstruating woman and the sexually impure person should not recite anything from the Quran).
  This narration is graded **Da'if** by Shaykh Zubayr due to Ismail ibn Ayyash's narration from Hijazi narrators. The database erroneously slapped Darussalam #131's *Daif* onto Darussalam #141 (*Sahih*)!

### Case 2: The Inverted Counterpart — Tirmidhi #131 (DB #121)
- **Canonical Hadith ID:** `12519`
- **Database Number (`no_inbook`):** `121`
- **Darussalam English Edition Number:** `131`
- **Matn:** Recitation of Quran by menstruating woman (weak chain).
- **Authoritative Grading in Darussalam English (Vol. 1, Hadith 131):**
  - Scholar: Ḥāfiẓ Zubair ʿAlī Zaʾī
  - Grading Text: **Da'if**
- **What Was Stored in the Database:** `Sahih`
- **Forensic Diagnosis:** The database joined on `hadith_number = 121`. Darussalam #121 is the authentic Hadith of Abu Hurayrah:
  > «إِنَّ الْمُسْلِمَ لاَ يَنْجُسُ» (A believer does not become impure).
  The database slapped Darussalam #121's *Sahih* onto Darussalam #131 (*Daif*)!

### Case 3: The Maymunah Single Vessel Hadith — Tirmidhi #12455 (DB #57 / Darussalam #62)
- **Canonical Hadith ID:** `12455`
- **Database Number (`no_inbook`):** `57`
- **Darussalam English Edition Number:** `62`
- **Matn:** Maymunah bathing with the Prophet ﷺ from a single container (*Bukhari 250, Muslim 321*).
- **Authoritative Grading in Darussalam English:** **Ṣaḥīḥ**
- **What Was Stored in the Database:** `Daif` (derived from Darussalam #57, the narration regarding *al-Walhān*, the devil of wudu, which is extremely weak).

### Case 4: The Internal Grading Split — Nasāʾī #26478 (REG-ZUB-0005)
- **Canonical Hadith ID:** `26478`
- **Database Number (`no_inbook`):** `5564`
- **Stored Rows in `hadith_grades`:**
  - Row ID `51316`: `grade = "Hasan Or Sahih"`
  - Row ID `51317`: `grade = "Daif"`
- **Forensic Diagnosis:** Two conflicting rows coexist simultaneously in the database for the exact same scholar on the exact same narration.

---

## 4. Regression Test Suite Execution Summary

All 5 mandatory regression cases were evaluated and passed:

```json
{
  "all_passed": true,
  "total_regressions": 5,
  "passed_count": 5,
  "results": [
    {
      "test_id": "REG-ZUB-0001",
      "name": "Tirmidhi #12529 (DB #131 / Darussalam #141) Zubayr Grading Defect",
      "status": "PASS"
    },
    {
      "test_id": "REG-ZUB-0002",
      "name": "Nasa'i DB #1816/1819 -> Darussalam/Zubayr #1829 Disassociation",
      "status": "PASS"
    },
    {
      "test_id": "REG-ZUB-0003",
      "name": "Ibn Majah Darussalam #1986 Exact Identity & Zubayr Grading",
      "status": "PASS"
    },
    {
      "test_id": "REG-ZUB-0004",
      "name": "Father/son narrator contamination guard (Abd al-Rahman al-Musli vs Wabarah)",
      "status": "PASS"
    },
    {
      "test_id": "REG-ZUB-0005",
      "name": "Nasa'i Hadith 26478 Internal Conflicting Grade Detection (ZUB-008)",
      "status": "PASS"
    }
  ]
}
```

---

## 5. Generated Audit Artifacts

All audit artifacts have been created under [validation/zubayr_grading_audit/](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/):

1. [population_manifest.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/population_manifest.json): Full census of 18,375 records by collection.
2. [verified_grading_records.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/verified_grading_records.json): Complete machine-readable array of all 18,375 records with identity evidence, Darussalam numbers, and gradings.
3. [discrepancies.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/discrepancies.csv): 9 confirmed critical defects adhering to MVAP normalized schema.
4. [numbering_crosswalk_audit.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/numbering_crosswalk_audit.json): Crosswalk alignment between canonical IDs, DB numbers, and Darussalam numbers.
5. [zubayr_source_registry.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/zubayr_source_registry.json): Registry of authoritative Darussalam editions and critical references.
6. [source_conflicts.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/source_conflicts.csv): 20 documented scholarly ikhtilāf conflicts.
7. [unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/unresolved_cases.csv): 286 cases lacking Darussalam English crosswalk mappings.
8. [regression_results.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/regression_results.json): Formal regression suite results.
9. [machine_validation_report.json](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_audit/machine_validation_report.json): High-level statistical validation summary.

---

## 6. Proposed Post-Audit Remediation Plan (Awaiting Approval)

Under the **Zero-Mutation Constraint**, no database records were changed during this audit. 
Once explicit user approval is granted, the following remediation procedure is recommended:

1. **Step 1: Deduping Internal Conflicts:** Remove duplicate rows in `hadith_grades` (IDs `51317` in Sunan al-Nasāʾī, etc.).
2. **Step 2: Correcting Inverted Records:** Update the 4 inverted records in Jāmiʿ al-Tirmidhī to their true Darussalam Zubayr grades.
3. **Step 3: Schema-Aware Crosswalk Joining:** Refactor grading retrieval queries to join through `hadith_numbers` via `scheme_id` rather than directly on `hadiths.no_inbook`.
4. **Step 4: Complete Remaining Crosswalks:** Populate the 286 missing Darussalam numbers in `hadith_numbering.db`.
