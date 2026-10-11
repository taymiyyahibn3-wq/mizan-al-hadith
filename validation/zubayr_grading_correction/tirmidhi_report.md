# MĪZĀN AL-ḤADĪTH — COLLECTION CORRECTION REPORT
## Jāmiʿ al-Tirmidhī (جامع الترمذي) — Book ID 3
### Shaykh Ḥāfiẓ Zubayr ʿAlī Zaʾī Grading Provenance Recovery

---

## 1. Scope & Population Summary
- **Collection**: Jāmiʿ al-Tirmidhī (Book ID 3)
- **Scholar**: Ḥāfiẓ Zubayr ʿAlī Zaʾī (`Zubair Ali Zai`)
- **Total Candidate Population**: **3,858 records**
- **Successfully Migrated**: **3,629 records (94.06%)**
- **Quarantined Unresolved**: **229 records (5.94%)**

---

## 2. Migration Breakdown & Inversion Statistics

| Category | Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **Total Population** | **3,858** | **100.00%** | All Zubair grading rows in Book 3 |
| **Rows Corrected (Wrong $\rightarrow$ True)** | **2,107** | **54.61%** | Displaced grades re-aligned to true hadith |
| **Rows Preserved (Already True)** | **1,522** | **39.45%** | Coincidental or true sequential matches |
| **CRITICAL Inversions Resolved** | **1,201** | **31.13%** | Major doctrinal grading flips corrected |
| ↳ *Legacy Ṣaḥīḥ $\rightarrow$ Corrected Ḍaʿīf* | 432 | 11.20% | False authentications eradicated |
| ↳ *Legacy Ḍaʿīf $\rightarrow$ Corrected Ṣaḥīḥ* | 437 | 11.33% | False rejections of Sunnah eradicated |
| ↳ *Legacy Ḥasan $\rightarrow$ Corrected Ḍaʿīf* | 166 | 4.30% | Defective chains downgraded |
| ↳ *Legacy Ḍaʿīf $\rightarrow$ Corrected Ḥasan* | 166 | 4.30% | Sound narrations restored |
| **Source Conflicts Documented** | **118** | **3.06%** | English summary vs Arabic isnād takhrij |

---

## 3. Key Regression Target Audits (Post-Migration)

### `REG-ZUB-TIR-0001` — Repeating Intercourse with Single Ghusl
- **Canonical Hadith ID**: `12529`
- **Database `no_inbook`**: `131`
- **Darussalam Reference**: Hadith `#141` (Vol. 1, Hadith 141)
- **Text**: `حَدَّثَنَا هَنَّادٌ، حَدَّثَنَا حَفْصُ بْنُ غِيَاثٍ... إذا أتى أحدكم أهله ثم أراد أن يعود فليتوضأ بينهما وضوءا...`
- **Legacy Grade in DB**: `Daif` (erroneously pulled from reciting Quran while junub #131)
- **Corrected Grade in DB**: **`Sahih Bukhari And Sahih Muslim`** (Sahih Muslim #308)
- **Updated Pointers**: `reference_book = 1`, `reference_hadith = 141`
- **Verification**: **PASS**

### `REG-ZUB-TIR-0057` — The Devil of Wudu (al-Walhān)
- **Canonical Hadith ID**: `12450`
- **Database `no_inbook`**: `52`
- **Darussalam Reference**: Hadith `#57` (Vol. 1, Hadith 57)
- **Text**: `إن للوضوء شيطانا يقال له الولهان فاتقوا وسواس الماء...`
- **Legacy Grade in DB**: `Sahih Muslim` (catastrophic false authentication from #52)
- **Corrected Grade in DB**: **`Daif`**
- **Updated Pointers**: `reference_book = 1`, `reference_hadith = 57`
- **Verification**: **PASS**

### `REG-ZUB-TIR-0062` — Maymunah Single-Vessel Ghusl
- **Canonical Hadith ID**: `12455`
- **Database `no_inbook`**: `57`
- **Darussalam Reference**: Hadith `#62` (Vol. 1, Hadith 62)
- **Text**: `كنت أغتسل أنا ورسول الله صلى الله عليه وسلم من إناء واحد...`
- **Legacy Grade in DB**: `Daif` (false rejection of Muttafaq 'Alayh from #57)
- **Corrected Grade in DB**: **`Sahih`**
- **Updated Pointers**: `reference_book = 1`, `reference_hadith = 62`
- **Verification**: **PASS**

---

## 4. Quarantined Unresolved Records (229 Cases)
All 229 narrations lacking Scheme 9 mappings or with insufficient text confidence have been quarantined in [unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_correction/unresolved_cases.csv) with zero guessing or artificial data injection.
