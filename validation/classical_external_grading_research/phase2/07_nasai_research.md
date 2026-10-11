# RESEARCH REPORT: AL-IMĀM AL-NASĀʾĪ (d. 303 AH)
## Investigation of *al-Sunan al-Ṣughrā (al-Mujtabā)*

---

## 1. Corpus Investigated
1. **al-Sunan al-Ṣughrā (al-Mujtabā)**:
   - Mīzān Book 5 (5,758 narrations).
2. **al-Sunan al-Kubrā** (ed. Ḥasan ʿAbd al-Munʿim Shalabī, 12 volumes, Mu'assasat al-Risālah).
3. **al-Ḍuʿafāʾ wa-al-Matrūkūn** (ed. Būrān al-Ḍannāwī).
4. **Tasmiyat Fuqahāʾ al-Amṣār**.

---

## 2. Discovery in Mīzān Canonical Database
A forensic scan of Book 5 in `data/hadith-kg.db` revealed **151 explicit authorial statements (`قال أبو عبد الرحمن`)** in `taraf_nass`:
- **Examples:**
  - Hadith #20965 (Sunan #51): `قال أبو عبد الرحمن هذا أشبه بالصواب من حديث شريك` (Variant Preference: *Ashbahu bi-al-Ṣawāb*).
  - Hadith #21039 (Sunan #125): `قال أبو عبد الرحمن ما نعلم أحدا تابع أبا قيس... والصحيح عن المغيرة أن النبي صلى الله عليه وسلم مسح على الخفين` (Tafarrod & Variant Preference).
  - Hadith #21084 (Sunan #170): `قال أبو عبد الرحمن ليس في هذا الباب حديث أحسن من هذا الحديث وإن كان مرسلا` (Comparative judgment & Mursal defect).
  - Hadith #21106 (Sunan #192): `قال أبو عبد الرحمن هذا خطأ والصواب أشعث عن الحسن` (Defect identification: *Khaṭaʾ*).

---

## 3. Nature of al-Nasāʾī's Methodology
- al-Nasāʾī's primary method in *al-Sunan* is to assemble all variant routes of a narration together, deliberately highlighting where narrators differed in wording or chain continuity.
- His statements are virtually never modern scalar grades (*Ṣaḥīḥ*, *Ḥasan*). They are **comparative variant criticisms** (*Naqd al-Asānīd*).
- They represent exceptionally high-value evidence for classical hadith methodology, but must strictly be presented as **Classical Hadith Criticism**, never converted into binary grades.

---

## 4. Mapping Feasibility
- **Mapping Level:** **LEVEL A — DETERMINISTIC (100%)**.
- The 151 statements are physically located in Book 5 (`taraf_nass`) of `hadith-kg.db`. The row-level join to Mīzān Hadith IDs (`20943` to `26620`) is 100% deterministic.

---

## 5. Implementation Recommendation

```
STATUS: DEFER — MANUAL VERIFICATION (PRIME PHASE 3 CANDIDATE)
```

**Rationale:**
1. 100% deterministic mapping and authentic primary transmission.
2. Must be ingested alongside Abū Dāwūd in a dedicated Phase 3 pass dedicated to **Classical Hadith Criticism & Variant Preference**.