# RESEARCH REPORT: IMĀM AL-BUKHĀRĪ (d. 256 AH)
## Distinction Between Collection Metadata and Hadith-Level Grading

---

## 1. Corpus Investigated
1. **Ṣaḥīḥ al-Bukhārī** (al-Jāmiʿ al-Musnad al-Ṣaḥīḥ al-Mukhtaṣar):
   - Mīzān Book 1 (7,563 narrations including repetitions).
2. **al-Tārīkh al-Kabīr** (التاريخ الكبير) (8 volumes, Hyderabadi / Dār al-Kutub al-ʿIlmiyyah editions).
3. **al-Tārīkh al-Awsaṭ / al-Ṣaghīr** (ed. Muḥammad Ibrāhīm al-Lihaydān).
4. **al-Ḍuʿafāʾ al-Ṣaghīr** (ed. Maḥmūd Ibrāhīm Zāyid).
5. **Oral Transmissions via al-Tirmidhī:** Preserved in *Jāmiʿ al-Tirmidhī* and *al-ʿIlal al-Kabīr* of al-Tirmidhī.

---

## 2. Absolute Integrity Rule: Collection Inclusion vs Hadith Grading
> **RULE:** Do NOT treat "Hadith appears in Ṣaḥīḥ al-Bukhārī" as "Imām al-Bukhārī explicitly graded this hadith Ṣaḥīḥ."

### Scholarly Rationale
- Inclusion in *al-Ṣaḥīḥ* is an **authorial selection criterion** (*Sharṭ al-Bukhārī*), which is properly classified as **COLLECTION_METADATA**.
- In classical ḥadīth methodology, an **Explicit Hadith Grade** is an explicit verbal verdict predicated on a narration (e.g. "هذا حديث صحيح", "هذا حديث حسن").
- Converting inclusion in *Ṣaḥīḥ al-Bukhārī* into a synthetic row in a `hadith_grades` table manufactures evidence that al-Bukhārī never verbally uttered in that form.
- Mīzān already displays collection identity and authoritative inclusion at the very top of every Hadith Detail Page (e.g. `Collection: Ṣaḥīḥ al-Bukhārī`, `Authority: Imām al-Bukhārī`). Duplicating this as a pseudo-grade creates redundant, unscholarly noise.

---

## 3. Actual Authorial Remarks in *Ṣaḥīḥ al-Bukhārī*
In Mīzān's canonical `hadith-kg.db`, Book 1 contains **67 explicit authorial remarks** (`قال أبو عبد الله`):
- **Content:**
  - Notes on corroborating chains (*Mutābaʿāt* / *Shawāhid*), e.g. Hadith #667: "وتابعه سعيد بن مسروق ومسعر".
  - Clarification of narrator discrepancies, e.g. Hadith #176: "ولم يقل غندر ويحيى عن شعبة الوضوء".
  - Occasional variant preferences, e.g. Hadith #247: "وكان ابن عيينة يقول أخيرا... والصحيح ما روى أبو نعيم".
  - Lexical and fiqh commentary.
- **Classification:** These 67 statements are **Classical Hadith Criticism / Isnād Commentary**, not scalar authenticity stamps.

---

## 4. Oral Critical Rulings Preserved via al-Tirmidhī
al-Tirmidhī frequently records his master al-Bukhārī's verbal judgments:
- "سألت محمدا عن هذا الحديث فقال: هو حديث صحيح"
- "سألت محمدا فقال: هذا حديث مضطرب"
- "سألت محمدا فقال: لا أعلم أحدا رواه غير فلان"
- **Nature:** High-value explicit hadith judgments.
- **Attribution Challenge:** The original authority is al-Bukhārī, but the transmitting compiler is al-Tirmidhī. This requires the generalized multi-layer attribution model designed in Phase 2.

---

## 5. Implementation Recommendation

```
STATUS: DEFER — SPECIALIZED MAPPING REQUIRED
```

**Rationale:**
1. Collection inclusion is already fully and prominently represented in Mīzān's collection metadata.
2. The 67 authorial remarks in Book 1 can be curated into Classical Hadith Criticism in a future pass.
3. Bukhārī's oral rulings quoted inside Tirmidhī require the multi-scholar attribution schema before exposure.