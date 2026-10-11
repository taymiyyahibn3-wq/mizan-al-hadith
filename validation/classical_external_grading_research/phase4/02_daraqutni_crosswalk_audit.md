# AL-DĀRAQUṬNĪ CROSSWALK AUDIT: *AL-ʿILAL AL-WĀRIDAH*

## 1. Corpus Investigated
- **Work:** *al-ʿIlal al-Wāridah fī al-Aḥādīth al-Nabawiyyah* (العلل الواردة في الأحاديث النبوية).
- **Scope:** 4,136 complex multi-route inquiries dictated by Imām al-Dāraquṭnī to Abū Bakr al-Barqānī (15 volumes, ed. Dr. Maḥfūẓ al-Salafī, Dār Ṭaybah).

## 2. Mapping Feasibility & Crosswalk Obstacles
- *al-ʿIlal al-Wāridah* is arranged by Companion Musnads (e.g. Musnad Abī Hurayrah, Musnad ʿĀ'ishah).
- Each entry is an oral inquiry (*"وسئل عن حديث كذا وكذا"*).
- **Crosswalk Obstacle:** No open, machine-readable dataset currently aligns these 4,136 inquiry numbers to canonical Sihah Sittah hadith IDs.
- Performing fuzzy matn matching across 4,136 inquiries violates Phase 4's zero-trust mandate, as many inquiries discuss subtle single-word discrepancies across obscure chains.

## 3. Decision: `DEFER_SPECIALIZED_MAPPING`
Automated ingestion is deferred. A dedicated crosswalk curated by hadith scholars is required before these entries can be attached to Mīzān Hadith IDs.
