# RESEARCH REPORT: ABŪ DĀWŪD AL-SIJISTĀNĪ (d. 275 AH)
## Investigation of *Sunan Abī Dāwūd* and the Silence Principle

---

## 1. Corpus Investigated
1. **Sunan Abī Dāwūd** (Mīzān Book 4, 5,274 narrations).
2. **Risālat Abī Dāwūd ilā Ahli Makkah fī Waṣf Sunanih** (رسالة أبي داود إلى أهل مكة).
3. **Suʾālāt al-Ājurrī li-Abī Dāwūd al-Sijistānī fī al-Jarḥ wa-al-Taʿdīl** (ed. ʿAlī Muʿawwaḍ).

---

## 2. Discovery in Mīzān Canonical Database
A forensic scan of Book 4 in `data/hadith-kg.db` revealed **585 explicit authorial statements (`قال أبو داود`)** in `taraf_nass`:
- **Examples of Explicit Hadith Criticism:**
  - Hadith #16340 (Sunan #18): `قال أبو داود هذا حديث منكر وإنما يعرف عن ابن جريج... والوهم فيه من...` (Explicit *Munkar* judgment + diagnosis of error).
  - Hadith #16335 (Sunan #13): `قال أبو داود رواه عبد السلام بن حرب... وهو ضعيف` (Transmitter defect).
  - Hadith #16336 (Sunan #14): `قال أبو داود هذا لم يسنده إلا عكرمة بن عمار` (Tafarrod / Isnād critique).
  - Hadith #16363 (Sunan #41): `قال أبو داود وحديث الأسود بن عامر أتم` (Comparative variant judgment).

---

## 3. The Silence Principle (Risālat Abī Dāwūd)
Abū Dāwūd famously stated in his Letter to the People of Makkah:
> "وَمَا كَانَ فِي كِتَابِي هَذَا فِيهِ وَهَنٌ شَدِيدٌ بَيَّنْتُهُ، وَمَا لَمْ أَذْكُرْ فِيهِ شَيْئًا فَهُوَ صَالِحٌ"  
> *"Whatever in this book of mine has severe weakness, I have explained it; and whatever I was silent about, it is Ṣāliḥ (acceptable/sound)."*

### Strict Scholarly Rule (Part 6)
> **RULE:** Do NOT infer hadith grades from silence. Do NOT assume inclusion in Sunan means Ṣaḥīḥ.

- Inferring that every silent hadith in Abū Dāwūd is *Ṣaḥīḥ* or *Ḥasan* is a violation of scholarly integrity:
  - Classical scholars debated the meaning of *Ṣāliḥ* (some held it means usable for corroboration, others that it means Ḥasan li-dhātih, others that it merely means not fabricated).
  - An algorithmic expansion that marks thousands of un-commented hadiths as "Abū Dāwūd Grade: Ṣaḥīḥ" would fabricate evidence.
  - **Only Abū Dāwūd's explicit statements may enter Mīzān.**

---

## 4. Mapping Feasibility
- **Mapping Level:** **LEVEL A — DETERMINISTIC (100%)**.
- The 585 authorial remarks are physically located in Book 4 (`taraf_nass`) of `hadith-kg.db`. The row-level join to Mīzān Hadith IDs (`16323` to `20942`) is 100% deterministic, exactly like Tirmidhī.

---

## 5. Implementation Recommendation

```
STATUS: DEFER — MANUAL VERIFICATION (PRIME PHASE 3 CANDIDATE)
```

**Rationale:**
1. Abū Dāwūd's 585 statements are authentic primary evidence with 100% deterministic mapping.
2. However, they are **exclusively Hadith Criticism, Isnād Defects, and Variant Analysis**, with virtually zero explicit positive binary grades.
3. To prevent premature ingestion before complete categorization (separating narrator remarks from hadith remarks), this corpus is deferred for a dedicated Phase 3 pass focused specifically on **Classical Hadith Criticism**.