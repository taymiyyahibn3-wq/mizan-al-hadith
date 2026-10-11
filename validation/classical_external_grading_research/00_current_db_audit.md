# 00 — CURRENT MĪZĀN DATABASE AUDIT: HADITH-LEVEL VS NARRATOR-LEVEL EVIDENCE
**Audit Date:** 2026-10-06  
**Auditor:** Anti Gravity Senior Hadith Database Architect & Security Auditor  
**Scope:** Forensic examination of all existing project databases, schemas, tables, and records.

---

## 1. Databases Inspected
The project contains 33 SQLite databases in `data/`:
1. `data/hadith-kg.db` (Primary Knowledge Graph, 1.64 GB)
2. `data/hadith_commentaries.db` (Commentaries and Sharḥ, 9.05 MB)
3. `data/hadith_numbering.db` (Multi-edition numbering systems, 35.09 MB)
4. `data/citation_enrichment.db` (Primary source citations for Zubayr Ali Zai, 9.25 MB)
5. `data/isnad_network.db` (Narrator graph edges and nodes, 52.09 MB)
6. `data/hadith_translations.db` (English translation texts, 24.05 MB)
7. `data/hadith-search-index.db` (FTS5 search index, 248.56 MB)
8. Ancillary and backup databases (`ask_mizan.db`, `english-search.db`, `translation-cache.db`, etc.)

---

## 2. Forensic Findings on Scholarly Evaluations

### A. Existing `hadith_grades` Table in `data/hadith-kg.db`
* **Total Rows:** 65,420
* **Scholar Breakdown:**
  - Zubair Ali Zai: 18,375 records
  - Al-Albani: 18,301 records
  - Shuaib Al Arnaut: 6,374 records
  - Abu Ghuddah: 5,627 records
  - Muhammad Muhyi Al-Din Abdul Hamid: 4,503 records
  - Muhammad Fouad Abd al-Baqi: 4,313 records
  - Ahmad Muhammad Shakir: 3,698 records
  - Bashar Awad Maarouf: 2,406 records
  - Salim al-Hilali: 1,823 records
* **Classical Scholars in `hadith_grades`:** **EXACTLY ZERO (0).**  
  Every single entry in `hadith_grades` originates from 20th/21st-century critical print editions (Darussalam, al-Maktab al-Islami, Mu'assasat al-Risalah).

### B. Existing `alems` and `aqwal` Tables in `data/hadith-kg.db`
* **Total Alems:** 1,015
* **Total Aqwal (Narrator Criticisms):** 127,863
* **Classical Scholars Present:**
  - Ibn Hibban (ID 431): 12,250 aqwal
  - al-Dhahabi (ID 1268): 11,501 aqwal
  - Ibn Hajar al-Asqalani (ID 1011): 10,377 aqwal
  - Abu Hatim al-Razi (ID 429): 5,227 aqwal
  - al-Bukhari (ID 1125): 4,783 aqwal
  - Ibn Abi Hatim al-Razi (ID 924): 3,845 aqwal
  - Yahya ibn Ma'in (ID 2821): 3,293 aqwal
  - al-Daraqutni (ID 1264): 2,984 aqwal
  - al-Nasa'i (ID 767): 2,735 aqwal
  - Ahmad ibn Hanbal (ID 751): 1,963 aqwal
  - Abu Zur'ah al-Razi (ID 466): 1,703 aqwal
  - Abu Dawud (ID 459): 1,206 aqwal
  - Ali ibn al-Madini (ID 2135/2136): 861 aqwal
  - al-Tirmidhi (ID 621): 238 aqwal
  - Malik ibn Anas (ID 2289): 76 aqwal
* **Critical Distinction:** These 63,445+ records are **NARRATOR-LEVEL** evaluations (Jarḥ wa Taʿdīl statements such as *Thiqah*, *Ḍaʿīf*, *Ṣadūq*, *Laysa bihi baʾs*). Under Part 0 of the Scholarly Integrity Rules, **narrator evaluations must NEVER be converted into hadith grades**.

### C. In-Matn Classical Evaluations Found in `hadiths.taraf_nass`
* **Discovery:** In `data/hadith-kg.db`, Book 3 (*Jāmiʿ al-Tirmidhī*, 3,924 hadiths), **2,726 hadiths (69.5%) contain Imam al-Tirmidhi's direct authorial evaluations in `taraf_nass`!**
* **Terminology:**
  - *Ḥasan Ṣaḥīḥ*: 1,110 hadiths
  - *Ḥasan Gharīb*: 401 hadiths
  - *Gharīb*: 276 hadiths
  - *Ḥasan*: 267 hadiths
  - *Ḥasan Ṣaḥīḥ Gharīb*: 167 hadiths
  - *Ṣaḥīḥ*: 49 hadiths
  - *Ḍaʿīf*: 9 hadiths
  - *Ṣaḥīḥ Gharīb*: 8 hadiths
  - *Laysa isnāduhu bi-dhāk*: 4 hadiths
  - *Munkar*: 4 hadiths
* **Status:** These are genuine primary authorial hadith-level evaluations directly from Imam al-Tirmidhi, previously unparsed into a structured table.

---

## 3. Current Project Gaps
1. **Gap 1:** No structured classical hadith-level grading table exists in canonical databases.
2. **Gap 2:** Imam al-Tirmidhi's authorial judgments were stored inside text blocks (`taraf_nass`) rather than an indexed table.
3. **Gap 3:** Classical critics (al-Bukhārī, Aḥmad, Yaḥyā ibn Maʿīn, al-Dāraquṭnī) had zero hadith-level entries in Mīzān's evaluation layer.
