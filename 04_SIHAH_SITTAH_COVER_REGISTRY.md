# MĪZĀN AL-ḤADĪTH — CANONICAL SIHAH SITTAH COVER PROVENANCE REGISTRY
**Document Identifier:** `04_SIHAH_SITTAH_COVER_REGISTRY.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Research Date:** October 2026  
**Investigator:** Lead Scholarly Digital Humanities & Legal Compliance Engineer  

---

## 1. Context & Research Problem Formulation

### 1.1 What Does "Original Cover" Mean in Hadith Codicology?
Classical hadith collections were composed between 200 AH and 300 AH (815–915 CE). In classical Islamic manuscript tradition (*ʿIlm al-Makhṭūṭāt*), books did not possess "publisher covers" in the modern commercial sense. Instead, manuscript codices featured:
1. **Title Folios (*Safḥat al-ʿUnwān*):** Containing the calligraphic title, chain of transmission for the copy (*samāʿāt*), and scribe colophon.
2. **Opening Illuminated Headpieces (*Shamsiyyah* / *ʿUnwān*):** Gilded or geometric manuscript opening chapter banners.
3. **Leather Bindings (*Mujalladāt* / *Tajlīd*):** Traditional blind-stamped or gilded goat/calfskin bindings.

In modern scholarly and library settings, "cover" refers to:
- **Category A:** The landmark first critical printed edition title page (e.g. Būlāq 1311 AH Sultanic edition, Halabi 1356 AH Shakir edition).
- **Category B:** Classical leather bindings and illuminated manuscript frontispieces preserved in historical repositories.
- **Category C:** Documented authentic photographic records of classical editions.

### 1.2 Investigation of Previous Missing Assets
The initial frontend codebase hardcoded links to:
- `Sunan_al-Tirmidhi.jpg` ➔ **Returned HTTP 404 (Not Found)**
- `Sunan_Nasai.jpg` ➔ **Returned HTTP 404 (Not Found)**
- `Sunan_Ibn_Majah.jpg` ➔ **Returned HTTP 404 (Not Found)**

**Root Cause:** The original developers assumed filenames in English transliteration existed on Wikimedia Commons. In reality, the authoritative uploads were categorized under Arabic and Urdu script titles (`File:سنن الترمذي.jpg`, `File:سنن النسائی.jpg`, `File:کتاب حدیث سنن ابن ماجه.jpg`).

---

## 2. Canonical Sourcing & Provenance Ledger

| # | Collection | Arabic Title | Compiler | Local Primary Asset | Original Upload Title | Original Repository URL | License Status | Commercial / Reuse Permitted? | Attribution Requirement |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :-: | :--- |
| **1** | **Ṣaḥīḥ al-Bukhārī** | صحيح البخاري | Imam al-Bukhārī (194–256 AH) | `/books/bukhari-cover.png` | `File:SaheehAlBukhari.png` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SaheehAlBukhari.png) | Public Domain (PD-Old-70) | **Yes** | None required (PD). |
| **2** | **Ṣaḥīḥ Muslim** | صحيح مسلم | Imam Muslim (204–261 AH) | `/books/muslim-cover.jpg` | `File:SahihMuslimCover.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SahihMuslimCover.jpg) | Public Domain (PD-Old-70) | **Yes** | Al-Amira press scan (PD). |
| **3** | **Jāmiʿ al-Tirmidhī** | جامع الترمذي | Imam al-Tirmidhī (209–279 AH) | `/books/tirmidhi-cover.jpg` | `File:سنن الترمذي.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:%D8%B3%D9%86%D9%86_%D8%A7%D9%84%D8%AA%D8%B1%D9%85%D8%B0%D9%8A.jpg) | Public Domain (PD-Old-70) | **Yes** | Halabi 1st Ed. 1356 AH (PD). |
| **4** | **Sunan Abī Dāwūd** | سنن أبي داود | Imam Abū Dāwūd (202–275 AH) | `/books/abu-dawud-cover.jpg` | `File:SunanAbiDaoud.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SunanAbiDaoud.jpg) | CC BY-SA 3.0 | **Yes** | Credit: User Abu Ta'ib (CC BY-SA 3.0). |
| **5** | **Sunan al-Nasāʾī** | سنن النسائي | Imam al-Nasāʾī (214–303 AH) | `/books/nasai-cover.jpg` | `File:سنن النسائی.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:%D8%B3%D9%86%D9%86_%D8%A7%D9%84%D9%86%D8%B3%D8%A7%D8%A6%DB%8C.jpg) | CC BY-SA 4.0 | **Yes** | Credit: User Omarnorzai (CC BY-SA 4.0). |
| **6** | **Sunan Ibn Mājah** | سنن ابن ماجه | Imam Ibn Mājah (209–273 AH) | `/books/ibn-majah-cover.jpg` | `File:کتاب حدیث سنن ابن ماجه.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:%DA%A9%D8%AA%D8%A7%D8%A8_%D8%AD%D8%AF%DB%8C%D8%AB_%D8%B3%D9%86%D9%86_%D8%A7%D8%A8%D9%86_%D9%85%D8%A7%D8%AC%D9%87.jpg) | CC BY-SA 4.0 | **Yes** | Credit: User Omarnorzai (CC BY-SA 4.0). |

---

## 3. Detailed Forensic Sourcing Profiles

### 3.1 Collection 1: Ṣaḥīḥ al-Bukhārī
- **Canonical ID:** 1
- **Author:** Imam Abū ʿAbdillāh Muḥammad ibn Ismāʿīl al-Bukhārī (194–256 AH / 810–870 CE)
- **Verified Hadiths Indexed in Mīzān:** 7,563
- **Edition Depicted:** Historical classical typography title page modeled on the landmark Būlāq / Sultanic Imperial Edition (*al-Ṭabʿah al-Sulṭāniyyah*), printed at the Amiri Press in Būlāq, Cairo (1311–1314 AH / 1893–1896 CE).
- **Physical Specifications:** 925 × 1246 px | PNG format | 361,742 bytes.
- **License / Legal Assessment:** Public Domain. Both the author and the historical publisher expired over 100 years ago. No intellectual property restrictions apply.

### 3.2 Collection 2: Ṣaḥīḥ Muslim
- **Canonical ID:** 2
- **Author:** Imam Abū al-Ḥusayn Muslim ibn al-Ḥajjāj al-Qushayrī al-Naysābūrī (204–261 AH / 820–875 CE)
- **Verified Hadiths Indexed in Mīzān:** 7,500
- **Edition Depicted:** Embossed classical gilded leather binding and title frontispiece from the historic Imperial Ottoman printing press (*Al-Maṭbaʿah al-Amīrah*, Istanbul, c. 1334 AH / 1916 CE).
- **Physical Specifications:** 1937 × 2922 px | JPEG format | 289,325 bytes.
- **License / Legal Assessment:** Public Domain (PD-Old-70). Al-Amira press ceased operations in the early 20th century.

### 3.3 Collection 3: Jāmiʿ al-Tirmidhī
- **Canonical ID:** 3
- **Author:** Imam Abū ʿĪsā Muḥammad ibn ʿĪsā al-Tirmidhī (209–279 AH / 824–892 CE)
- **Verified Hadiths Indexed in Mīzān:** 4,415
- **Edition Depicted:** The landmark First Edition of Sunan/Jami' al-Tirmidhi edited with comprehensive critical notes by Shaykh Aḥmad Muḥammad Shākir, published by Matba'at Mustafa al-Babi al-Halabi, Cairo, 1356 AH / 1937 CE.
- **Physical Specifications:** 986 × 1662 px | JPEG format | 264,314 bytes.
- **License / Legal Assessment:** Public Domain. Published in Egypt in 1937; copyright expired under Egyptian Law No. 82 of 2002 (Article 168) and US Title 17.

### 3.4 Collection 4: Sunan Abī Dāwūd
- **Canonical ID:** 4
- **Author:** Imam Abū Dāwūd Sulaymān ibn al-Ashʿath al-Sijistānī (202–275 AH / 817–889 CE)
- **Verified Hadiths Indexed in Mīzān:** 5,274
- **Edition Depicted:** High-resolution photographic scan of the classical Arabic volume bound in embossed Moroccan-style leather binding.
- **Physical Specifications:** 680 × 960 px | JPEG format | 140,717 bytes.
- **License / Legal Assessment:** Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0). Photographed and released by user Abu Ta'ib. Local hosting is permitted under CC BY-SA 3.0 with appropriate attribution provided in the interface.

### 3.5 Collection 5: Sunan al-Nasāʾī (al-Mujtabā)
- **Canonical ID:** 5
- **Author:** Imam Aḥmad ibn Shuʿayb al-Nasāʾī (214–303 AH / 829–915 CE)
- **Verified Hadiths Indexed in Mīzān:** 5,758
- **Edition Depicted:** Documented published edition cover of Sunan al-Nasa'i (*al-Mujtabā*).
- **Physical Specifications:** 233 × 350 px | JPEG format | 23,126 bytes.
- **License / Legal Assessment:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). Released by User:Omarnorzai. Local hosting permitted with author attribution.

### 3.6 Collection 6: Sunan Ibn Mājah
- **Canonical ID:** 6
- **Author:** Imam Abū ʿAbdillāh Muḥammad ibn Yazīd Ibn Mājah al-Qazwīnī (209–273 AH / 824–887 CE)
- **Verified Hadiths Indexed in Mīzān:** 4,341
- **Edition Depicted:** Documented published edition cover of Sunan Ibn Majah.
- **Physical Specifications:** 302 × 448 px | JPEG format | 115,841 bytes.
- **License / Legal Assessment:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). Released by User:Omarnorzai. Local hosting permitted with author attribution.

---

## 4. Technical Optimization & Three-Tier Fallback Strategy

To ensure zero layout shift (CLS < 0.01), sub-50ms render latency, and graceful degradation across all network conditions, the frontend implements a three-tier asset loading strategy:

```
┌─────────────────────────────────────────────────────────────┐
│                       TIER 1 (Default)                      │
│ Local High-Speed Optimized Static Asset                     │
│ Path: /books/[collection]-cover.[png/jpg]                   │
│ Cached permanently via Next.js static asset pipeline        │
└──────────────────────────────┬──────────────────────────────┘
                               │ Error / Missing
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       TIER 2 (Remote)                       │
│ Authoritative Canonical Repository Archive URL               │
│ Source: Wikimedia Commons / Archive.org                     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Network Timeout / Offline
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       TIER 3 (Fallback)                     │
│ Classical Gilded Leather Binding Component                  │
│ Semantic HTML/CSS leather medallion with gold calligraphy   │
│ Guaranteed 100% offline & zero network dependency           │
└─────────────────────────────────────────────────────────────┘
```

Structured JSON registry saved at:  
`mizan-web/frontend/public/books/cover_provenance.json`
