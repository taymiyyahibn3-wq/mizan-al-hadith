# MĪZĀN AL-ḤADĪTH — COLLECTION CORRECTION REPORT
## Sunan Ibn Mājah (سنن ابن ماجه) — Book ID 6
### Shaykh Ḥāfiẓ Zubayr ʿAlī Zaʾī Grading Provenance Recovery

---

## 1. Scope & Population Summary
- **Collection**: Sunan Ibn Mājah (Book ID 6)
- **Scholar**: Ḥāfiẓ Zubayr ʿAlī Zaʾī (`Zubair Ali Zai`)
- **Total Candidate Population**: **4,334 records**
- **Successfully Migrated**: **4,309 records (99.42%)**
- **Quarantined Unresolved**: **25 records (0.58%)**

---

## 2. Migration Breakdown & Inversion Statistics

| Category | Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **Total Population** | **4,334** | **100.00%** | All Zubair grading rows in Book 6 |
| **Rows Corrected (Wrong $\rightarrow$ True)** | **1,791** | **41.32%** | Displaced grades re-aligned to true hadith |
| **Rows Preserved (Already True)** | **2,518** | **58.10%** | Coincidental or true sequential matches |
| **CRITICAL Inversions Resolved** | **792** | **18.27%** | Major doctrinal grading flips corrected |
| ↳ *Legacy Ṣaḥīḥ $\rightarrow$ Corrected Ḍaʿīf* | 10 | 0.23% | False authentications eradicated |
| ↳ *Legacy Ḍaʿīf $\rightarrow$ Corrected Ṣaḥīḥ* | 10 | 0.23% | False rejections eradicated |
| ↳ *Legacy Ḥasan $\rightarrow$ Corrected Ḍaʿīf* | 26 | 0.60% | Defective chains downgraded |
| ↳ *Legacy Ḍaʿīf $\rightarrow$ Corrected Ḥasan* | 746 | 17.21% | Sound narrations restored |
| **Source Conflicts Documented** | **126** | **2.91%** | English summary vs Arabic isnād takhrij |

---

## 3. Key Regression Target Audits (Post-Migration)

### `REG-ZUB-IBNMAJAH-1986` — The Umar Wife-Beating Hadith
- **Canonical Hadith ID**: `28581`
- **Database `no_inbook`**: `1976`
- **Darussalam Reference**: Hadith `#1986` (Vol. 9, Hadith 142)
- **Text**: `حَدَّثَنَا مُحَمَّدُ بْنُ يَحْيَى ، والْحَسَنُ بْنُ مُدْرِكٍ الطَّحَّانُ... لَا يُسْأَلُ الرَّجُلُ فِيمَ يَضْرِبُ امْرَأَتَهُ...`
- **Legacy Grade in DB**: `Daif` (erroneously pulled from Usamah stumbling narration #1976)
- **Corrected Grade in DB**: **`Hasan Or Sahih`** (`حَسَنٌ`)
- **Updated Pointers**: `reference_book = 9`, `reference_hadith = 142`
- **Verification**: **PASS**

### `REG-ZUB-IBNMAJAH-0579` — No Wudu After Janabah Ghusl
- **Canonical Hadith ID**: `27177`
- **Database `no_inbook`**: `572`
- **Darussalam Reference**: Hadith `#579` (Vol. 1, Hadith 313)
- **Text**: `لا يتوضأ بعد الغسل من الجنابة`
- **Legacy Grade in DB**: `Sahih` (false authentication from #572)
- **Corrected Grade in DB**: **`Daif`**
- **Updated Pointers**: `reference_book = 1`, `reference_hadith = 313`
- **Verification**: **PASS**

### `REG-ZUB-IBNMAJAH-0257` — Unifying All Worries
- **Canonical Hadith ID**: `26858`
- **Database `no_inbook`**: `253`
- **Darussalam Reference**: Hadith `#257` (Vol. 0, Hadith 257)
- **Text**: `من جعل الهموم هما واحدا هم آخرته كفاه الله هم دنياه...`
- **Legacy Grade in DB**: `Daif` (false rejection from #253)
- **Corrected Grade in DB**: **`Sahih`**
- **Updated Pointers**: `reference_book = 0`, `reference_hadith = 257`
- **Verification**: **PASS**

---

## 4. Quarantined Unresolved Records (25 Cases)
All 25 unmapped narrations lacking Scheme 18 mappings have been preserved in [unresolved_cases.csv](file:///c:/Users/taymi/discord-hadith-bot/validation/zubayr_grading_correction/unresolved_cases.csv) with zero guessing or artificial data injection.
