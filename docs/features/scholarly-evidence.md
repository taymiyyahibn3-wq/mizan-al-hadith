# FEATURE — SCHOLARLY EVIDENCE & TAKHRIJ ENGINE

**Document Identifier:** `docs/features/scholarly-evidence.md`  
**Frontend Route:** `/hadith/[id]` (Grading & Takhrij Sections)  
**Backend Endpoints:** `/api/hadith/{id}/grades`, `/api/hadith/{id}/takhrij`  

---

## 1. Overview & Scholarly Objective

In classical Islamic methodology, evaluating a hadith requires analyzing multiple independent expert opinions (*Aḥkām al-Aʾimmah*) rather than relying on a single modern grading.

Mīzān al-Ḥadīth provides a **Multi-Scholar Evidence Matrix** presenting primary classical evaluations side by side with modern academic verifications.

---

## 2. Integrated Scholarly Authorities

### 2.1 Classical Primary Evaluations (`classical_scholar_evidence.db`)
- **Imam Abū ʿĪsā al-Tirmidhī (d. 279 AH):** Direct verdicts from *al-Jāmiʿ* (*Ḥasan Ṣaḥīḥ*, *Ḥasan Gharīb*, *Ḍaʿīf*, etc.).
- **Imam Muḥammad ibn Ismāʿīl al-Bukhārī (d. 256 AH):** Classical remarks recorded in *al-Tārīkh al-Kabīr* and transmitted commentaries.
- **Ibn Ḥajar al-ʿAsqalānī (d. 852 AH):** Critical judgments from *Fatḥ al-Bārī*, *Tahdhīb al-Tahdhīb*, and *Talkhīṣ al-Ḥabīr*.

### 2.2 Modern Editorial & Research Verifications (`citation_enrichment.db`)
- **Shaykh Zubayr ʿAlī Zaʾī (d. 2013 CE):** Verified gradings across the Four Sunan (14,398 reference records).
- **Shaykh Muḥammad Nāṣir al-Dīn al-Albānī (d. 1999 CE):** Rigorous reference cross-checks from *Ṣaḥīḥ/Ḍaʿīf Sunan Abī Dāwūd, al-Tirmidhī, al-Nasāʾī, Ibn Mājah*.
- **Shaykh Shuʿayb al-Arnāʾūṭ (d. 2016 CE):** Critical annotations on the Six Books and Musnad Ahmad.

---

## 3. UI Presentation & Provenance Badges

In `ScholarlyStatementCard.tsx`:
- **Green Badge:** Ṣaḥīḥ (Authentic).
- **Teal Badge:** Ḥasan (Sound / Good).
- **Amber / Rose Badge:** Ḍaʿīf (Weak) or Maqlūb (Inverted).
- **Attribution & Page Tag:** Every grade cites the specific volume, chapter, and hadith number.
- **Caveat Guard:** Unresolved or conflicting judgments are displayed with explicit notes.
