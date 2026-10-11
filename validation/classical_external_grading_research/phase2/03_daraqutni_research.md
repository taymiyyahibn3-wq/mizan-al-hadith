# RESEARCH REPORT: AL-IMĀM AL-DĀRAQUṬNĪ (d. 385 AH)
## Investigation of *al-ʿIlal al-Wāridah fī al-Aḥādīth al-Nabawiyyah*

---

## 1. Corpus Investigated
- **Primary Work:** *al-ʿIlal al-Wāridah fī al-Aḥādīth al-Nabawiyyah* (العلل الواردة في الأحاديث النبوية).
- **Compiler / Scribe:** Abū Bakr Aḥmad ibn Muḥammad al-Barqānī (d. 425 AH) dictated directly by al-Dāraquṭnī from memory.
- **Critical Edition:** Dr. Maḥfūẓ al-Raḥmān Zayn Allāh al-Salafī (15 volumes + comprehensive indexes, Dār Ṭaybah, Riyadh, 1405–1416 AH / 1985–1996 CE).
- **Scope:** 4,136 detailed monographs analyzing hadith transmission variants.

---

## 2. Scholarly Structure & The Inadequacy of Scalar Grading
al-Dāraquṭnī's *al-ʿIlal* represents the pinnacle of classical hadith defect analysis. Each entry possesses a complex, multi-branch relational structure:
1. **The Inquiry:** Al-Barqānī presents a specific hadith (e.g. Entry #1240: "وسئل عن حديث عائشة في كذا...").
2. **Branch Analysis (Wujūh al-Ikhtilāf):** al-Dāraquṭnī enumerates every variant chain:
   - Route A: Transmitted by Narrator $X$ from $Y$ as *Marfūʿ* (connected to the Prophet).
   - Route B: Transmitted by Narrator $Z$ from $Y$ as *Mawqūf* (halting at the Companion).
   - Route C: Transmitted by Narrator $W$ as *Mursal* (dropping the Companion).
3. **Identification of Error / Defect (al-Wahm / al-ʿIllah):** Names the exact transmitter responsible for the variation.
4. **Tarjīḥ (Scholarly Verdict):** Renders a verdict on which route is preserved (*al-Maḥfūẓ*) and which is erroneous (*al-Khaṭaʾ*).

### The Inadequacy of a Scalar Grade Table
Forcing al-Dāraquṭnī's analysis into a scalar column (`hadith_id -> Ṣaḥīḥ / Ḍaʿīf`) is a **grave scholarly distortion**.
- One route of the hadith may be authentic while another is defective.
- al-Dāraquṭnī is evaluating the **variants of transmission**, not giving a modern binary stamp to the entire hadith entity.

---

## 3. Required Data Architecture for al-Dāraquṭnī's ʿIlal
To accurately reflect al-Dāraquṭnī's scholarship, Mīzān requires a dedicated relational sub-schema:

```
Table: daraqutni_illal_inquiries
  - inquiry_id (PK, 1 to 4136)
  - companion_musnad (e.g., Musnad Abi Hurayrah, Musnad 'A'ishah)
  - topic_summary_ar
  - mizan_primary_hadith_id (FK to hadiths.id)
  - volume_page_ref

Table: daraqutni_variant_routes
  - route_id (PK)
  - inquiry_id (FK)
  - route_description_ar
  - route_type (Marfu' / Mawquf / Mursal / Munqati')
  - transmitters_chain
  - is_preferred (Boolean: Mahfuz vs Wahm)

Table: daraqutni_verdicts
  - verdict_id (PK)
  - inquiry_id (FK)
  - verbatim_verdict_ar (e.g. "والصحيح هو الموقوف", "والحديث مضطرب")
  - defect_type (Waqf_over_Raf' | Irsal_over_Wasl | Idtirab | Ziyadah_Da'ifah)
  - erring_narrator_id (FK to rawi)
```

---

## 4. Mapping Feasibility & Current Status
- **Mapping Level:** **LEVEL D — PROBABLE (UNMAPPED)**.
- **Status:** No complete public crosswalk mapping al-Dāraquṭnī's 4,136 questions to Sihah Sittah hadith IDs currently exists in machine-readable form.
- The Musnad-based arrangement (organized by Companion) makes manual lookup straightforward for a scholar, but automated joining across 4,136 entries requires dedicated crosswalk curation.

---

## 5. Licensing & Legal Reusability
- Classical Arabic text dictated by al-Dāraquṭnī: Public Domain.
- Salafī's editorial apparatus: Copyrighted.

---

## 6. Implementation Recommendation

```
STATUS: DEFER — SPECIALIZED MAPPING & VARIANT SCHEMA REQUIRED
```

**Rationale:**
1. al-Dāraquṭnī's *al-ʿIlal* is an invaluable treasure of hadith science, but it **must not be flattened into a scalar grade table**.
2. Integrating it requires building the relational *ʿIlal Variant Architecture* documented above.
3. It must remain deferred until that architecture is developed and deterministic mappings to Mīzān hadith IDs are established.