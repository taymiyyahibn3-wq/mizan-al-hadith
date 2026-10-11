# AL-NASĀʾĪ EXTRACTION AUDIT (151 RECORDS)

## 1. Corpus & Methodology
- **Source:** Canonical `data/hadith-kg.db`, Book 5 (*al-Sunan al-Ṣughrā*), column `taraf_nass`.
- **Search Key:** `قال أبو عبد الرحمن`.
- **Total Discovered & Extracted:** Exactly **151 records**.
- **Mapping:** 100% deterministic Level A row-level join to Mīzān Hadith IDs (`20943` to `26620`).

## 2. Taxonomy Distribution
- **Explicit Hadith Grades:** 2 records:
  - Hadith #24095 (Sunan #3181): `قال أبو عبد الرحمن الأوزاعي لم يسمع هذا الحديث من الزهري وهذا حديث صحيح قد رواه يونس عن الزهري`.
  - Hadith #24827 (Sunan #3913): `قال أبو عبد الرحمن هذان الحديثان صحيحان عن عبدة`.
- **Classical Hadith Criticism:** 149 records:
  - *Comparative Tarjīḥ (Ashbah bi-al-Ṣawāb):* 39 records (e.g. `أشبه بالصواب`, `أولى بالصواب`, `والصواب`).
  - *Khaṭaʾ (Transmission Defect):* 14 records (e.g. Hadith #21106 / Sunan #192: `هذا خطأ والصواب أشعث عن الحسن`).
  - *Transmitter Defect / Weakness:* 13 records (e.g. `ضعيف`, `ليس بالقوي`).
  - *Inqitāʿ / Disconnection:* 11 records (e.g. `لم يسمع`, `انقطع`).
  - *Tafarrud / Lack of Corroboration:* 4 records (e.g. `لا أعلم أحدا تابع`).
  - *Mursal (Isnād Defect):* 3 records.
  - *Munkar:* 3 records.
  - *Waqf / Rafʿ Distinction:* 1 record.
  - *Classical Transmission Remarks:* 61 records.

## 3. Auditable Sample Verifications
- **Sample 1 (#20965, Sunan #51):** `قال أبو عبد الرحمن هذا أشبه بالصواب من حديث شريك والله سبحانه وتعالى أعلم` -> Correctly classified as *Comparative Tarjīḥ (Ashbah bi-al-Ṣawāb)*.
- **Sample 2 (#21039, Sunan #125):** `قال أبو عبد الرحمن ما نعلم أحدا تابع أبا قيس... والصحيح عن المغيرة أن النبي صلى الله عليه وسلم مسح على الخفين` -> Correctly classified as *Comparative Tarjīḥ / Isnād Preference*.
- **Sample 3 (#21084, Sunan #170):** `قال أبو عبد الرحمن ليس في هذا الباب حديث أحسن من هذا الحديث وإن كان مرسلا` -> Correctly classified as *Comparative Judgment & Mursal Defect*.
