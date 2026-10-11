# 01 — EXTERNAL SOURCE DISCOVERY REPORT
**Evaluation Hierarchy:** Tier 1 (Primary digitized classical works) → Tier 2 (Academic scholarly repositories) → Tier 3 (Structured open datasets) → Tier 4 (Modern discovery websites).

---

## Tier 1: Primary Digitized Classical Works
1. **al-Jāmiʿ al-Kabīr (Sunan al-Tirmidhī)** — Imām Abū ʿĪsā al-Tirmidhī (d. 279 AH).
   - Critical Editions: ed. Bashshār ʿAwwād Maʿrūf (Dār al-Gharb al-Islāmī), ed. Aḥmad Shākir (Cairo).
   - Digital Corpora: Shamela (Book ID 21541), OpenITI (`0279Tirmidhi.JamiKabir`).
   - Usability: **Directly usable. Full text with verbatim authorial judgments.**

2. **al-ʿIlal al-Wāridah fī al-Aḥādīth al-Nabawiyyah** — Imām ʿAlī ibn ʿUmar al-Dāraquṭnī (d. 385 AH).
   - Critical Editions: ed. Maḥfūẓ al-Raḥmān al-Salafī (15 vols, Dār al-Ṭaybah), re-edited by Dār al-Taʾṣīl.
   - Digital Corpora: Shamela (Book ID 1122), OpenITI (`0385Daraqutni.Ilal`).
   - Usability: Detailed chain-discrepancy criticisms (*ʿIlal*). Does not assign binary grades; statements require expert per-hadith extraction.

3. **al-ʿIlal wa-Maʿrifat al-Rijāl** — Imām Aḥmad ibn Ḥanbal (d. 241 AH, transmitted by son ʿAbdullāh).
   - Critical Edition: ed. Waṣiyyullāh ʿAbbās (3 vols, al-Maktab al-Islāmī / Dār al-Khānī).
   - Digital Corpora: Shamela (Book ID 21545), OpenITI (`0241IbnHanbal.Ilal`).
   - Usability: 4,000+ entries covering narrators and specific hadith inquiries.

4. **ʿIlal al-Ḥadīth** — Ibn Abī Ḥātim al-Rāzī (d. 327 AH), recording Abū Ḥātim & Abū Zurʿah.
   - Critical Edition: ed. Saʿd al-Ḥumayyid & Khālid al-Juraysī (7 vols).
   - Digital Corpora: Shamela (Book ID 21543), OpenITI (`0327IbnAbiHatim.IlalHadith`).
   - Usability: 2,850+ hadith-level queries with explicit defect statements.

5. **Bulūgh al-Marām min Adillat al-Aḥkām** — al-Ḥāfiẓ Ibn Ḥajar al-ʿAsqalānī (d. 852 AH).
   - Critical Edition: ed. Samīr al-Zuhayrī, ed. Ṭāriq ʿIwaḍullāh.
   - Digital Corpora: OpenITI, Shamela, Sunnah.com API.
   - Usability: Contains Ibn Hajar's explicit hadith-level judgments for ~1,500 legal traditions.

---

## Tier 2 & Tier 3: Structured Open Datasets
1. **Sunnah.com Open API / Datasets:**
   - Provides full Sihah Sittah Arabic texts and metadata.
   - Caveat: The `grade` field frequently combines Darussalam, Al-Albani, and in-matn Tirmidhi statements under a generic string without distinct schema keys.
2. **OpenITI Corpus (Aga Khan University / University of Maryland / Leipzig):**
   - High-fidelity TEI/markdown transcriptions of classical Arabic texts.
   - Validated against physical print editions; open access (Creative Commons CC BY-NC-SA).
3. **Hugging Face (`meeAtif/hadith_datasets`, `quranlab/hadith`):**
   - Re-packaged Sunnah.com JSON/CSV extracts. Useful for cross-referencing but secondary.

---

## Tier 4: Modern Computational Datasets (REJECTED AS EVIDENCE)
* GitHub ML authenticity prediction models, chain-scoring algorithms, and majority-voting scripts were audited and **unanimously rejected**. Under Mīzān's Scholarly Integrity Rules, machine-learning inferences cannot be passed off as classical scholarly evaluations.
