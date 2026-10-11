# ABŪ DĀWŪD EXTRACTION AUDIT (585 RECORDS)

## 1. Corpus & Methodology
- **Source:** Canonical `data/hadith-kg.db`, Book 4 (*Sunan Abī Dāwūd*), column `taraf_nass`.
- **Search Key:** `قال أبو داود`.
- **Total Discovered & Extracted:** Exactly **585 records**.
- **Mapping:** 100% deterministic Level A row-level join to Mīzān Hadith IDs (`16323` to `20942`).

## 2. Taxonomy Distribution
- **Explicit Hadith Grades:** 1 record (Hadith #19384 / Sunan #3062: `قال أبو داود وهو عندنا صحيح`).
- **Classical Hadith Criticism:** 584 records:
  - *Comparative Tarjīḥ / Variant Preference:* 31 records (e.g. `أتم`, `أصح`, `أثبت`).
  - *Tafarrud / Solitary Route:* 16 records (e.g. `تفرد به`, `لم يسنده إلا`).
  - *Mursal (Isnād Defect):* 16 records.
  - *Transmission Error / Wahm:* 15 records.
  - *Transmitter Defect / Ḍaʿīf:* 13 records (e.g. `رواه فلان وهو ضعيف`).
  - *Inqitāʿ / Disconnection:* 10 records (e.g. `لم يسمع`, `انقطع`).
  - *Waqf / Rafʿ Distinction:* 7 records.
  - *Munkar:* 6 records (e.g. Hadith #16340 / Sunan #18: `هذا حديث منكر`).
  - *Laysa bi-Qawī:* 3 records.
  - *Classical Transmission Remarks:* 468 records (e.g. alternative paths, lineage identifications, context).

## 3. Auditable Sample Verifications
- **Sample 1 (#16340, Sunan #18):** `قال أبو داود هذا حديث منكر وإنما يعرف عن ابن جريج عن زياد بن سعد عن الزهري عن أنس أن النبي صلى الله عليه وسلم اتخذ خاتما من ورق ثم ألقاه والوهم فيه من همام ولم يروه إلا همام` -> Correctly classified as *Hadith Criticism: Munkar*.
- **Sample 2 (#16335, Sunan #13):** `قال أبو داود رواه عبد السلام بن حرب عن الأعمش عن أنس بن مالك وهو ضعيف` -> Correctly classified as *Transmitter Defect / Ḍaʿīf*.
- **Sample 3 (#16336, Sunan #14):** `قال أبو داود هذا لم يسنده إلا عكرمة بن عمار` -> Correctly classified as *Isnād Analysis: Solitary Transmission*.
