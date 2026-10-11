# RESEARCH REPORT: IMĀM AḤMAD IBN ḤANBAL (d. 241 AH)
## Investigation of Hadith-Level Evaluations and Mapping Feasibility

---

## 1. Corpus Investigated
1. **al-ʿIlal wa-Maʿrifat al-Rijāl** (العلل ومعرفة الرجال):
   - Primary transmission: ʿAbd Allāh ibn Aḥmad ibn Ḥanbal (d. 290 AH).
   - Secondary transmission: Abū Bakr al-Marwadhī (d. 275 AH).
   - Critical edition: Dr. Waṣiyyullāh ibn Muḥammad ʿAbbās (3 volumes, 4,115 numbered entries, Maktabat al-Rushd / Dār al-Khānī, Riyadh, 1408 AH / 1988 CE).
2. **Masāʾil al-Imām Aḥmad**:
   - Riwāyat Abī Dāwūd al-Sijistānī (ed. Muḥammad Bahjah al-Bayṭār).
   - Riwāyat Isḥāq ibn Manṣūr al-Kawsaj (ed. Khālid al-Ribāṭ).
   - Riwāyat Ibn Hāniʾ al-Naysābūrī (ed. Zuhayr al-Shāwīsh).

---

## 2. Scholarly Nature of Evidence
- **Not Modern Binary Grading:** Imām Aḥmad did not compose a systematic collection assigning modern scalar grades (*Ṣaḥīḥ* / *Ḥasan* / *Ḍaʿīf*) to standard lists of hadiths.
- **Oral Didactic Question-Answer Structure (*Suʾālāt*):**
  - "سألت أبي عن حديث فلان عن فلان... فقال: هذا منكر" (Isnād/Matn Munkar)
  - "سألت أبي عنه فقال: ليس إسناده بشيء" (Isnād Defect)
  - "فقال: لم يسمع فلان من فلان" (Inqiṭāʿ / Lack of Audition)
  - "فقال: الصواب ما رواه فلان موقوفا" (Variant Preference / Waqf)
  - "فقال: حديث حسن أو مقارب" (Occasional Hadith-Level Description)
- **Conflation Hazard:** Out of 4,115 entries in *al-ʿIlal*, approximately **75% are narrator evaluations** (*Jarḥ wa Taʿdīl* on individual transmitters, e.g. "فلان ثقة", "فلان ضعيف الحديث", "متروك"), which are already captured in Mīzān's `aqwal` table (1,963 statements). Only approximately **15–20% (~600–800 entries)** discuss specific hadith narrations.

---

## 3. Hadith Mapping Feasibility & Obstacles
- **Mapping Level:** **LEVEL D — PROBABLE (UNMAPPED)**.
- **The Core Roadblock:** Entries in Waṣiyyullāh ʿAbbās's edition of *al-ʿIlal* are referenced by arbitrary sequential entry numbers ($1$ to $4,115$).
- **Absence of Standard Crosswalk:** There is currently no open, public, machine-actionable dataset linking *al-ʿIlal* entry numbers to Sihah Sittah hadith IDs.
- **Ambiguity in Narration Citations:** Imām Aḥmad and his son ʿAbd Allāh frequently cite hadiths by shorthand narrator pairs (e.g. "حديث الزهري عن أنس في العقيقة") without quoting the full matn or complete chain, making automatic text matching hazardous.

---

## 4. Attribution Model
- **Original Authority:** Aḥmad ibn Muḥammad ibn Ḥanbal (d. 241 AH).
- **Transmitter / Compiler:** ʿAbd Allāh ibn Aḥmad ibn Ḥanbal (d. 290 AH).
- **Work:** *al-ʿIlal wa-Maʿrifat al-Rijāl*.
- **Integrity Rule:** Must be recorded as `Scholar = Aḥmad ibn Ḥanbal`, `Transmitter = ʿAbd Allāh ibn Aḥmad`.

---

## 5. Licensing & Legal Reusability
- **Classical Text:** Public Domain.
- **Waṣiyyullāh ʿAbbās's Apparatus / Footnotes:** Copyrighted critical edition. Only the classical Arabic text of Aḥmad and ʿAbd Allāh may be ingested.

---

## 6. Implementation Recommendation

```
STATUS: DEFER — SPECIALIZED MAPPING REQUIRED
```

**Rationale:**
1. Imām Aḥmad's narrator evaluations are already cleanly accessible in Mīzān's `aqwal` table (1,963 entries).
2. His ~600 hadith-level defect statements in *al-ʿIlal* cannot be mapped deterministically without a dedicated manual takhrīj alignment project.
3. Automatically guessing mappings based on narrator names would produce unverified false links, violating Part 0 (Rule 5).
4. Defer implementation until an auditable, verified *al-ʿIlal* question-to-hadith crosswalk is constructed.