# AL-BUKHĀRĪ SCHOLARLY EVIDENCE AUDIT REPORT
## Investigation of *Ṣaḥīḥ al-Bukhārī*, *al-Tārīkh al-Kabīr*, and Oral ʿIlal Material

---

### 1. Corpus Audited
- **Primary Work:** *al-Jāmiʿ al-Musnad al-Ṣaḥīḥ* (Mīzān Book 1, 7,563 narrations).
- **Biographical / Critical Works:** *al-Tārīkh al-Kabīr* (9 vols.), *al-Tārīkh al-Awsaṭ*.
- **Transmitted Critical Records:** *al-ʿIlal al-Kabīr* of al-Tirmidhī (oral rulings of Bukhārī recorded by his pupil al-Tirmidhī).

---

### 2. Strict Application of Project Rule 2
> **RULE:** Collection inclusion is NOT an explicit hadith grade.  
> Do NOT create: `Bukhārī Grade = Ṣaḥīḥ` simply because a hadith appears in *Ṣaḥīḥ al-Bukhārī*.

- While Imām al-Bukhārī stipulated that his collection contains only authentic narrations, an authorial compilation is classified as `COLLECTION_METADATA`, not a standalone grading event.
- Stamping 7,563 hadiths with "Bukhārī graded this Ṣaḥīḥ" would conflate collection membership with explicit scholarly grading statements.

---

### 3. Authorial Remarks Embedded in *Ṣaḥīḥ al-Bukhārī*
Forensic scan of Book 1 (`taraf_nass`) identified **67 authorial statements** (`قال أبو عبد الله`):
- **Isnād Suspensions / Variants:** e.g. Hadith #9: `قال أبو عبد الله وقال أبو معاوية حدثنا داود...`
- **Isnād Comparisons:** e.g. Hadith #247: `قال أبو عبد الله كان ابن عيينة يقول أخيرا عن ابن عباس عن ميمونة والصحيح ما روى أبو نعيم`
- **Linguistic / Lexical Notes:** e.g. Hadith #521: `قال أبو عبد الله يتركم وترت الرجل إذا قتلت له قتيلا...`
- **Narrator Clarifications:** e.g. Hadith #836: `قال أبو عبد الله هو أخو محمد بن المنكدر`

These statements are invaluable scholarly metadata, but they are transmission observations, not scalar hadith grades.

---

### 4. Bukhārī's Oral Rulings in *Jāmiʿ al-Tirmidhī*
- al-Tirmidhī frequently records Bukhārī's oral rulings: e.g. *"سألت محمدا عن هذا الحديث فقال: هو حديث صحيح"*, or *"فقال: لا أعلم أحدا رواه غير فلان"*.
- In Mīzān's strict attribution architecture, these statements belong to the **al-Tirmidhī transmission apparatus** and are already preserved within Tirmidhī's certified records with multi-layer attribution.

---

### 5. Implementation Decision
- **Status:** `DEFER_MANUAL_VERIFICATION`.
- **Reasoning:** In accordance with zero-trust scholarly standards, collection inclusion remains collection metadata, and biographical notes in *al-Tārīkh* remain in `aqwal`.
