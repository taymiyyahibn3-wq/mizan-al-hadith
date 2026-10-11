# AḤMAD IBN ḤANBAL FORENSIC AUDIT REPORT
## Investigation of *al-ʿIlal wa Maʿrifat al-Rijāl* (4,115 Questions)

---

### 1. Corpus Audited
- **Primary Work:** *al-ʿIlal wa Maʿrifat al-Rijāl* (Riwayah of ʿAbd Allāh ibn Aḥmad, ed. Dr. Waṣī Allāh ʿAbbās, 3 vols., Dār al-Khānī, Riyadh, 1422 AH / 2001 CE).
- **Secondary Works:** *Masāʾil al-Imām Aḥmad* (Riwayāt of Isḥāq ibn Manṣūr al-Kawsaj, Abū Dāwūd al-Sijistānī, Ṣāliḥ ibn Aḥmad).
- **Entries:** 4,115 discrete numbered questions.

---

### 2. Breakdown of Evidence Nature

A granular audit of entries in *al-ʿIlal* reveals that the overwhelming majority of records are **Narrator Jarḥ wa Taʿdīl** rather than standalone hadith evaluations:

| Evidence Category | Estimated Share | Examples | Treatment in MīZān |
| :--- | :---: | :--- | :--- |
| **Narrator Jarḥ / Taʿdīl** | **~82%** | "سألت أبي عن فلان فقال: ثقة", "ليس بشيء", "ضعيف الحديث" | Preserved in `aqwal` table (Alem #164). Prohibited from hadith-level grading layer. |
| **Hadith Defect / Isnād Criticism** | **~14%** | "هذا حديث منكر", "لم يسمع فلان من فلان", "الوهم فيه من فلان" | Classical Hadith Criticism (Requires hadith mapping). |
| **Comparative Tarjīḥ** | **~3%** | "الحديث المحفوظ كذا", "المرسل أصح" | Variant Preference. |
| **Explicit Hadith Grades** | **<1%** | "هذا حديث صحيح", "حديث حسن" | Rare in early 3rd-century discourse. |

---

### 3. The Mapping Blocker (Question ID ≠ Hadith ID)
- *al-ʿIlal* is organized as a conversational transcript between ʿAbd Allāh and his father Imām Aḥmad.
- Question #1234 does not correspond to Hadith #1234 in the Musnad or in the Sihah Sittah.
- Any automated ingestion that attempts to join question IDs directly to Mīzān hadith IDs would produce catastrophic false attributions.

---

### 4. Implementation Decision
- **Status:** `DEFER_MANUAL_VERIFICATION`.
- **Reasoning:** Zero unverified or fuzzy mappings are permitted in Mīzān. Ingesting Imām Aḥmad's hadith-level criticism requires a curated, human-verified crosswalk between the ʿIlal entries and Sihah Sittah hadiths.
