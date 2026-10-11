# MĪZĀN AL-ḤADĪTH — DATA SOURCE PROVENANCE REGISTRY
**Document Identifier:** `12_SOURCE_PROVENANCE_REGISTRY.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Audit Date:** October 2026  
**Auditor:** Scholarly Digital Humanities Architect & Lead Compliance Engineer  

---

## 1. Registry Purpose & Institutional Standards

Mīzān al-Ḥadīth operates under strict principles of scholarly transparency. Every primary text, crosswalk mapping, biographical profile, commentary entry, and search index utilized by the application is cataloged with its exact provenance, upstream origin, license status, and modification history.

This document serves as the master registry governing data integrity, attribution, and scholarly verification.

---

## 2. Exhaustive Data Source Inventory

### 2.1 Primary Hadith Corpus & Knowledge Graph
- **Source Identifier:** `src-kg-01`
- **Dataset / Database Name:** `hadith-kg.db`
- **Local File Path:** `data/hadith-kg.db`
- **File Size:** 1,642,500,096 bytes (1.64 GB)
- **Phase 18 Certified SHA256 Hash:**  
  `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd`
- **Upstream Origin:** Open Islamic Knowledge Graph & al-Maktaba al-Shamelah historical archives.
- **Original Source URL:** [https://al-maktaba.org](https://al-maktaba.org)
- **Version:** Phase 18 Certified Release Baseline
- **Access Date:** September 2026
- **License:** Public Domain / Classical Islamic Heritage Texts
- **Copyright Status:** Historical classical works composed between 150 AH and 800 AH. Authors deceased centuries ago.
- **Permission Status:** Unrestricted academic, educational, and computational research use.
- **Required Attribution:** Classical Arabic mutūn and asānīd transcribed from printed editions; normalized for digital research.
- **Modifications Performed by Mīzān:** Relational entity separation (`hadiths`, `books`, `rawis`, `sanads`, `sanad_rawis`, `meaning_groups`, `tarafs`), Arabic orthographic normalization for FTS5, and Phase 18 forensic certification.
- **How Mīzān Uses This Source:** Core database powering all hadith text rendering, isnād chain traversal, narrator biographical profiles, and book catalog exploration.

---

### 2.2 Hadith Numbering & Concordance Systems
- **Source Identifier:** `src-num-02`
- **Dataset / Database Name:** `hadith_numbering.db`
- **Local File Path:** `data/hadith_numbering.db`
- **File Size:** 35,094,528 bytes (35.09 MB)
- **Phase 18 Certified SHA256 Hash:**  
  `ecfe3079dba318bde09f544eaf84764a9095a1ec12e0bd3446acf5f6428a66cb`
- **Upstream Origin:** Standard concordance mappings (Darussalam, Fu'ad ʿAbd al-Bāqī, A.J. Wensinck *Concordance et Indices de la Tradition Musulmane*).
- **Original Source URL:** [https://sunnah.com](https://sunnah.com)
- **Version:** Phase 18 Certified Numbering Crosswalk
- **License:** Open Scholarly Concordance Metadata
- **Copyright Status:** Standard bibliographical and concordancing citation data.
- **Permission Status:** Free scholarly cross-referencing and bibliographical lookup.
- **Required Attribution:** Concordance numbering based on standardized editions (Darussalam, Fu'ad ʿAbd al-Bāqī, Aḥmad Shākir).
- **Modifications Performed by Mīzān:** Book-aware offset alignment, canonical hadith identity resolution, and Phase 18 zero-escape quarantine enforcement.
- **How Mīzān Uses This Source:** Enables researchers to locate hadith records across international printings (In-Book #, Darussalam #, Wensinck volume/page, Chapter #).

---

### 2.3 Citation Enrichment & Cross-Collection Takhrij
- **Source Identifier:** `src-cit-03`
- **Dataset / Database Name:** `citation_enrichment.db`
- **Local File Path:** `data/citation_enrichment.db`
- **File Size:** 9,252,864 bytes (9.25 MB)
- **Phase 18 Certified SHA256 Hash:**  
  `8e3a1d03ee6d3668314448acfbb227476cfd85c88b5fb8e57cb92abf5c6d4c37`
- **Upstream Origin:** Mīzān al-Ḥadīth Forensic Takhrij Engine.
- **Original Source URL:** Internal Certified Database
- **Version:** Phase 18 Certified Takhrij Release
- **License:** Project Hikmah / Mīzān Research Data
- **Copyright Status:** Copyright © 2026 Mīzān al-Ḥadīth Research Project
- **Permission Status:** Authorized for query and display within Mīzān platform.
- **Required Attribution:** Mīzān al-Ḥadīth Forensic Takhrij Engine.
- **Modifications Performed by Mīzān:** Precision cross-phase validation, secondary citation filtering, and verified cross-collection relationship mapping.
- **How Mīzān Uses This Source:** Powers the Crosswalk and Takhrij tabs, displaying verified related narrations across the Six Canonical Books.

---

### 2.4 Classical Commentary Corpus (*Shurūḥ*)
- **Source Identifier:** `src-com-04`
- **Dataset / Database Name:** `hadith_commentaries.db`
- **Local File Path:** `data/hadith_commentaries.db`
- **File Size:** 9,056,256 bytes (9.05 MB)
- **Phase 18 Certified SHA256 Hash:**  
  `2fcd9ae4deeb006de25d6db23719abd2ecdaf9779a14f29f81e0cf3a9acebed1`
- **Upstream Origin:** Al-Maktaba al-Shamelah classical commentary corpus.
- **Original Source URL:** [https://shamela.ws](https://shamela.ws)
- **Version:** Phase 18 Certified Commentary Corpus
- **License:** Public Domain (Classical Islamic Historical Texts)
- **Copyright Status:** Classical historical commentary texts (Ibn Ḥajar al-ʿAsqalānī d. 852 AH, Imam al-Nawawī d. 676 AH, etc.).
- **Permission Status:** Public domain research, commentary, and quotation.
- **Required Attribution:** Texts from *Fatḥ al-Bārī*, *Sharḥ Ṣaḥīḥ Muslim*, *ʿAwn al-Maʿbūd*, and *Tuḥfat al-Aḥwadhī*.
- **Modifications Performed by Mīzān:** Scope validation, volume/page indexing, and relational linking to canonical hadith records (`commentary_hadith_links`).
- **How Mīzān Uses This Source:** Populates the Commentary section in the Hadith Detail reader.

---

### 2.5 Isnād Topology Graph Cache
- **Source Identifier:** `src-isnad-05`
- **Dataset / Database Name:** `isnad_network.db`
- **Local File Path:** `data/isnad_network.db`
- **File Size:** 52,092,928 bytes (52.09 MB)
- **Upstream Origin:** Synthesized from canonical `hadith-kg.db` transmission sequences.
- **Original Source URL:** Internal Computed Graph
- **License:** Mīzān Scholarly Topology Model
- **Copyright Status:** Copyright © 2026 Mīzān al-Ḥadīth Research Project
- **Permission Status:** Authorized for query and visualization within Mīzān platform.
- **Required Attribution:** Mīzān Isnād Graph Engine.
- **Modifications Performed by Mīzān:** Calculation of 298,655 directed narrator-to-narrator transmission edges, degree centrality metrics, and transitivity indexes.
- **How Mīzān Uses This Source:** Powers the Isnād Network, Timeline, Map, Atlas, and 3D Spatial visualizers.

---

### 2.6 English Translation Corpus
- **Source Identifier:** `src-trans-06`
- **Dataset / Database Name:** `hadith_translations.db` & `english_translation_fts.db`
- **Local File Path:** `data/hadith_translations.db`
- **File Size:** 24,051,712 bytes (24.05 MB)
- **Upstream Origin:** Public academic English translation archives.
- **Original Source URL:** [https://sunnah.com](https://sunnah.com)
- **License:** Open Scholarly & Educational Fair Use
- **Copyright Status:** Academic English translations of classical religious texts.
- **Permission Status:** Educational, non-commercial hadith study and search.
- **Required Attribution:** Translations credited per edition (e.g. Dr. Muhammad Muhsin Khan, Abdul Hamid Siddiqui, Nasiruddin al-Khattab).
- **Modifications Performed by Mīzān:** Precision identity mapping to Arabic hadith identifiers, narrator prefix separation, and FTS5 token index generation.
- **How Mīzān Uses This Source:** Powers the English full-text search and parallel translation viewer.

---

### 2.7 Historical Islamic Geography Gazetteer
- **Source Identifier:** `src-geo-07`
- **Dataset / Database Name:** `geoData.ts`
- **Local File Path:** `src/app/isnad/geoData.ts`
- **Upstream Origin:** Classical Islamic Geographical Tradition (*Muʿjam al-Buldān* li-Yāqūt al-Ḥamawī).
- **License:** Public Domain Geographic Facts
- **Permission Status:** Unrestricted research use.
- **Modifications Performed by Mīzān:** Exact latitude/longitude mapping for 12 canonical Islamic transmission centers.
- **How Mīzān Uses This Source:** Calculates 2D projected coordinates and 3D spatial points for MapView, AtlasView, and 3D Spatial View.
