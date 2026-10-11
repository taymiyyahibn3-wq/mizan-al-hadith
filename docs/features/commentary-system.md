# FEATURE — CLASSICAL COMMENTARY SYSTEM (*SHURŪḤ*)

**Document Identifier:** `docs/features/commentary-system.md`  
**Frontend Route:** Integrated in `/hadith/[id]`  
**Backend Endpoint:** `/api/hadith/{id}/commentaries`  

---

## 1. Overview & Scholarly Objective

A hadith cannot be fully understood from its matn in isolation. Classical commentaries (*Shurūḥ al-Ḥadīth*) provide critical linguistic elucidation, context of revelation (*Asbāb al-Wurūd*), legal implications, and resolution of apparent textual discrepancies.

---

## 2. Cataloged Classical Commentary Works

Mīzān indexes excerpts from eight recognized classical commentary works:

| Commentary Title | Arabic Name | Classical Author | Death Year | Target Hadith Collection |
| :--- | :--- | :--- | :--- | :--- |
| **Fatḥ al-Bārī** | فتح الباري شرح صحيح البخاري | Ibn Ḥajar al-ʿAsqalānī | 852 AH | Ṣaḥīḥ al-Bukhārī |
| **ʿUmdat al-Qārī** | عمدة القاري شرح صحيح البخاري | Badr al-Dīn al-ʿAynī | 855 AH | Ṣaḥīḥ al-Bukhārī |
| **al-Minhāj (Sharḥ Ṣaḥīḥ Muslim)** | المنهاج شرح صحيح مسلم بن الحجاج | Yaḥyā ibn Sharaf al-Nawawī | 676 AH | Ṣaḥīḥ Muslim |
| **ʿAwn al-Maʿbūd** | عون المعبود شرح سنن أبي داود | Muḥammad Shams al-Ḥaqq al-ʿAẓīm Ābādī | 1329 AH | Sunan Abī Dāwūd |
| **Badhl al-Majhūd** | بذل المجهود في حل سنن أبي داود | Khalīl Aḥmad al-Sahāranfūrī | 1346 AH | Sunan Abī Dāwūd |
| **Tuḥfat al-Aḥwadhī** | تحفة الأحوذي بشرح جامع الترمذي | Muḥammad ʿAbd al-Raḥmān al-Mubārakfūrī | 1353 AH | Jāmiʿ al-Tirmidhī |
| **Sharḥ al-Suyūṭī ʿalā Sunan al-Nasāʾī** | زهر الربى على المجتبى | Jalāl al-Dīn al-Suyūṭī | 911 AH | Sunan al-Nasāʾī |
| **Ḥāshiyat al-Sindī ʿalā Sunan Ibn Mājah** | حاشية السندي على سنن ابن ماجه | Muḥammad ibn ʿAbd al-Hādī al-Sindī | 1138 AH | Sunan Ibn Mājah |

---

## 3. Technical Implementation

- **Database:** `data/hadith_commentaries.db` (`commentary_sources`, `hadith_commentaries`, `commentary_hadith_links`).
- **Endpoint:** `GET /api/hadith/{id}/commentaries`
- **Frontend UI:** `HadithCommentarySection.tsx` embedded in the Hadith Detail reader.
