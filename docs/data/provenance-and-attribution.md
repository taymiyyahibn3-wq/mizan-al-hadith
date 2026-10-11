# MĪZĀN AL-ḤADĪTH — DEDICATED PROVENANCE & SCHOLARLY ATTRIBUTION REGISTER

**Document Identifier:** `docs/data/provenance-and-attribution.md`  
**Certified System Baseline:** Phase 18 Forensic Relational Audit  
**Attribution Standard:** Rigorous Digital Humanities Evidence Hierarchy  

---

## Executive Summary & Provenance Protocol

Mīzān al-Ḥadīth (*ميزان الحديث*) is an open computational platform for hadith transmission analysis, isnād graph topology, cross-edition concordances, and grounded scholarly retrieval. The project operates under strict adherence to scholarly integrity, academic attribution, and ethical digital custody.

Rather than claiming to have independently gathered or digitized every underlying historical manuscript, Mīzān systematically ingests, validates, aligns, and enriches structured datasets produced by open-source digital humanists, academic compilers, and classical digitization initiatives.

This document traces every verified upstream dataset, API, source collection, transformation step, and external dependency that contributes data to Mīzān al-Ḥadīth.

---

## 1. Primary Hadith Corpus (`data/hadith-kg.db`)

### 1.1 Upstream Origin & Attribution
- **Creator / Maintainer:** **Emaad Jumaah (Emad Jumaah)**
- **Upstream Git Repository:** [https://github.com/emadjumaah/hadith](https://github.com/emadjumaah/hadith)
- **Hugging Face Dataset Card:** [https://huggingface.co/datasets/emadjumaah/hadith-kg](https://huggingface.co/datasets/emadjumaah/hadith-kg)
- **Stated License:** Creative Commons Attribution 4.0 International (**CC-BY-4.0**)
- **Original Upstream Dump Date:** 2017-10-12 (recorded in internal `meta` table as `mongodump hadithdb/hadith (2017-10-12) + rawa_cat.csv`)

### 1.2 Upstream vs. Classical Author Demarcation
To ensure historiographical precision, Mīzān strictly separates three layers of authority:
1. **Original Classical Compilers:** Historical authors of the classical hadith compilations (e.g., Imam Muḥammad ibn Ismāʿīl al-Bukhārī [d. 256 AH], Imam Muslim ibn al-Ḥajjāj [d. 261 AH], Imam Abū Dāwūd [d. 275 AH], Imam al-Tirmidhī [d. 279 AH], Imam al-Nasāʾī [d. 303 AH], Imam Ibn Mājah [d. 273 AH], Imam Mālik ibn Anas [d. 179 AH], Imam Aḥmad ibn Ḥanbal [d. 241 AH], Imam al-Dārimī [d. 255 AH]). Their original texts (*mutūn*) and transmission chains (*asānīd*) reside in the **universal public domain**.
2. **Upstream Knowledge Graph Creator:** Emaad Jumaah, who extracted, relationalized, and serialized these texts into structured entities, sanad sequences, and transmitter records.
3. **Mīzān al-Ḥadīth Application:** Consumes Jumaah's structured graph, verifies its internal relational integrity, indexes it for sub-millisecond querying via SQLite B-trees and FTS5, links it to modern concordances, and applies read-only safety invariants.

### 1.3 Local Artifact & Schema Lineage
- **Local Database:** `data/hadith-kg.db` (1,642,500,096 bytes; SHA-256: `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd`).
- **Core Tables Consumed:**
  - `books` (425 records): Classical compilation titles and author metadata.
  - `hadiths` (715,790 records): Hadith texts, chapters, and normalized Arabic strings.
  - `sanads` (577,024 records): Transmission chain sequences.
  - `sanad_rawis` (4,414,211 records): Ordered transmitter steps (`pos: 0 = compiler, ascending toward the Companion`).
  - `meaning_groups` (20,745 records): Thematic semantic groupings.
  - `tarafs` (20,745 records): Canonical transmission openings.
  - `hadith_ayas` (117,194 records): Hadith-to-Quranic verse cross-references.

### 1.4 Known Limitations
- The upstream dataset does not specify original print volume and page numbers for all 425 historical titles. Where modern scholarly citation requires print page provenance, Mīzān relies on its dedicated `hadith_numbering.db` concordance engine.

---

## 2. Hadith Grading and Scholarly Evaluations

### 2.1 HadithPro Grading Dataset
- **Upstream Creator / Project:** **HadithPro** (`unkn4wn`)
- **Upstream Repository:** [https://github.com/unkn4wn/hadith-pro](https://github.com/unkn4wn/hadith-pro)
- **License / Terms:** Open Source Research Data (GPL-compatible open reference archive).
- **Local Storage:** Integrated into `data/hadith-kg.db` in dedicated tables:
  - `hadith_grades` (**65,420 records**, 100% marked with `source = 'Hadith Pro'`).
  - `hadith_pro_hadiths` (**21,187 records**, cross-referencing HadithPro numbering to reference books).

### 2.2 Graders and Evaluation Distribution
Every grading entry preserves the exact evaluating scholar and reference book. The 65,420 records break down as follows:
- **Ḥāfiẓ Zubair ʿAlī Zaʾī:** 18,375 evaluations (Darussalam / Maktaba Islamia tahqīq).
- **Shaykh Muḥammad Nāṣir al-Dīn al-Albānī:** 18,301 evaluations (*Ṣaḥīḥ/Ḍaʿīf Sunan Abī Dāwūd*, *al-Tirmidhī*, *al-Nasāʾī*, *Ibn Mājah*, *Silsilat al-Aḥādīth al-Ṣaḥīḥah*).
- **Shaykh Shuʿayb al-Arnāʾūṭ:** 6,374 evaluations (*Tahqīq Musnad Aḥmad*, *Sunan Abī Dāwūd*).
- **Shaykh ʿAbd al-Fattāḥ Abū Ghuddah:** 5,627 evaluations (*Sunan al-Nasāʾī* tahqīq).
- **Muḥammad Muḥyī al-Dīn ʿAbd al-Ḥamīd:** 4,503 evaluations (*Sunan Abī Dāwūd* tahqīq).
- **Muḥammad Fuʾād ʿAbd al-Bāqī:** 4,313 evaluations (*Sunan Ibn Mājah* tahqīq).
- **Aḥmad Muḥammad Shākir:** 3,698 evaluations (*Musnad Aḥmad*, *Jāmiʿ al-Tirmidhī*).
- **Dr. Bashshār ʿAwwād Maʿrūf:** 2,406 evaluations (*Jāmiʿ al-Tirmidhī* tahqīq).
- **Salīm al-Hilālī:** 1,823 evaluations.

### 2.3 Methodological Safeguards
- **No Conflation of Narrator and Hadith Grades:** Mīzān strictly prohibits inferring a hadith-level grade (*ṣaḥīḥ*, *ḍaʿīf*) solely from an individual narrator's reliability (*thiqah*, *ḍaʿīf*). Hadith-level grades originate strictly from explicit scholarly rulings.
- **Attribution Preservation:** The Mīzān UI displays the specific evaluating scholar for every grade badge.

---

## 3. Narrator Biographies and Jarḥ wa Taʿdīl

### 3.1 Primary Classical Jarḥ Corpus (`hadith-kg.db`)
- **Upstream Origin:** Emaad Jumaah Knowledge Graph (`rawa_cat.csv` and classical rijal registers).
- **Records:**
  - `rawis` (49,844 records): Biographical demographics, generational tier (*ṭabaqah*), places of residence (*iqāmah*), and death dates.
  - `alems` (1,015 records): Classical evaluating critics (e.g. Yaḥyā ibn Maʿīn, Aḥmad ibn Ḥanbal, al-Bukhārī, Abū Ḥātim al-Rāzī, al-Nasāʾī, Ibn Ḥajar, al-Dhahabī).
  - `aqwal` (127,863 records): Historical verdicts and criticism quotes (*Jarḥ wa Taʿdīl*).

### 3.2 Itqan Unified Narrator Database (`data/itqan`, `data/english_enrichment.db`)
- **Upstream Creator:** **Ali Bin Shahid**
- **Upstream Repository:** [https://github.com/r3genesi5/Itqan](https://github.com/r3genesi5/Itqan)
- **Scholarly Publication / DOI:** [Zenodo DOI 10.5281/zenodo.19453612](https://doi.org/10.5281/zenodo.19453612)
- **Role in Mīzān:** Provides standardized English scholarly transliterations, historical name variants, and cross-references to 22 classical biographical works (*Tahdhīb al-Kamāl*, *Taqrīb al-Tahdhīb*, *Mīzān al-Iʿtidāl*, *al-Jarḥ wa al-Taʿdīl*, *al-Thiqāt*, *al-Kāmil fī Ḍuʿafāʾ al-Rijāl*, *Tārīkh Baghdād*).
- **Ingestion Pipeline:** Ingested via `build_english_database.py` and `cleanup_english_database.py` into `data/english_enrichment.db`:
  - `narrator_names` (49,844 rows): Linked directly by `rawi_id` to `itqan_id` and `itqan_full_name`.
  - `narrator_name_variants` (128,476 rows): Alternative Arabic names and normalized search aliases.
  - `narrator_grades` (91,094 rows): Consolidated classical narrator reliability grades.
  - `narrator_sources` (125,814 rows): Direct book-level references to classical rijal dictionaries.

---

## 4. Isnād and Sanad Relationships (`data/isnad_network.db`)

### 4.1 Topology Compilation
- **Creator / Maintainer:** Mīzān al-Ḥadīth Topology Compiler (`scripts/build_isnad_network.py`).
- **Nature of Artifact:** Application-generated multigraph compiled directly from canonical `hadith-kg.db` transmission sequences (`sanads`, `sanad_rawis`).
- **Graph Metrics:**
  - **Transmitter Nodes:** 49,844.
  - **Directed Transmission Edges:** 298,655.
  - **Cumulative Transmission Weight:** 3,836,193 historical teacher-student transmission instances.
  - **Maximum Single-Pair Weight:** 19,507 transmissions (verified high-density hubs like Mālik from Nāfiʿ from Ibn ʿUmar).
- **License:** MIT License (Application Derived Artifact).

---

## 5. Classical Commentaries (`data/hadith_commentaries.db`)

Mīzān integrates 1,202 commentary excerpts linked to 1,203 canonical hadiths across eight authoritative works. Digital origins are explicitly differentiated:

### 5.1 Open-Hadith-Data Corpus (Muhammad Hashim)
- **Upstream Project:** Open-Hadith-Data by Muhammad Hashim.
- **Repository URL:** [https://github.com/mhashim6/Open-Hadith-Data](https://github.com/mhashim6/Open-Hadith-Data)
- **Digital License:** Open Database License (**ODbL 1.0**) for the dataset; Public Domain for the underlying historical Arabic text.
- **Works Ingested:**
  1. *Fatḥ al-Bārī bi-Sharḥ Ṣaḥīḥ al-Bukhārī* by al-Ḥāfiẓ Ibn Ḥajar al-ʿAsqalānī (d. 852 AH). Edition: al-Maktabah al-Salafiyyah / Dār al-Maʿrifah.
  2. *al-Minhāj Sharḥ Ṣaḥīḥ Muslim ibn al-Ḥajjāj* by al-Imām Yaḥyā ibn Sharaf al-Nawawī (d. 676 AH). Edition: al-Maṭbaʿah al-Miṣriyyah / Dār Iḥyāʾ al-Turāth.
  3. *Tuḥfat al-Aḥwadhī bi-Sharḥ Jāmiʿ al-Tirmidhī* by Muḥammad ʿAbd al-Raḥmān al-Mubārakfūrī (d. 1353 AH). Edition: Dār al-Kutub al-ʿIlmiyyah.
  4. *ʿAwn al-Maʿbūd ʿalā Sunan Abī Dāwūd* by Muḥammad Ashraf al-ʿAẓīmābādī (d. 1329 AH). Edition: al-Anṣārī / Dār al-Kutub al-ʿIlmiyyah.
  5. *Ḥāshiyat al-Sindī ʿalā Sunan al-Nasāʾī* by Muḥammad ibn ʿAbd al-Hādī al-Sindī (d. 1138 AH). Edition: al-Maktabah al-Tijāriyyah al-Kubrā.
  6. *Ḥāshiyat al-Sindī ʿalā Sunan Ibn Mājah (Kifāyat al-Ḥājah)* by al-Sindī (d. 1138 AH). Edition: Dār al-Jīl.

### 5.2 Al-Maktaba al-Shamela Corpus
- **Upstream Digital Source:** Al-Maktaba al-Shamela ([shamela.ws](https://shamela.ws)).
- **License / Status:** Public Domain classical Arabic texts; digital transcription utilized for non-commercial scholarly research.
- **Works Ingested:**
  1. *ʿUmdat al-Qārī Sharḥ Ṣaḥīḥ al-Bukhārī* by Badr al-Dīn al-ʿAynī (d. 855 AH). Source: [https://shamela.ws/book/8302](https://shamela.ws/book/8302). Edition: Dār Iḥyāʾ al-Turāth al-ʿArabī.
  2. *Irshād al-Sārī li-Sharḥ Ṣaḥīḥ al-Bukhārī* by Shihāb al-Dīn al-Qasṭallānī (d. 923 AH). Source: [https://shamela.ws/book/10578](https://shamela.ws/book/10578). Edition: al-Maṭbaʿah al-Kubrā al-Amīriyyah, Būlāq.

---

## 6. English Translations (`data/hadith_translations.db`)

### 6.1 Corpus Overview & Alignment
- **Total Records:** 31,488 verified English translations.
- **Upstream Digital Source:** Sunnah.com Open Hadith Corpus ([sunnah.com](https://sunnah.com) / [GitHub](https://github.com/sunnah-com)).
- **Alignment Method:** Mapped to canonical Mīzān Hadith IDs using reference matching and Arabic matn similarity scoring (`alignment_score = 1.0`, `verified = 1`).

### 6.2 Translators and Publisher Distribution
- **Ṣaḥīḥ al-Bukhārī (6,653 hadiths):** Dr. Muhammad Muhsin Khan (Darussalam English Edition).
- **Ṣaḥīḥ Muslim (4,925 hadiths):** Abdul Hamid Siddiqui.
- **Jāmiʿ al-Tirmidhī (3,630 hadiths):** Abu Khaliyl (USA) / Darussalam.
- **Sunan Abī Dāwūd (4,337 hadiths):** Ahmad Hasan.
- **Sunan al-Nasāʾī (5,558 hadiths):** Darussalam Translation Team / Nasiruddin al-Khattab.
- **Sunan Ibn Mājah (4,222 hadiths):** Darussalam English Translation Team.
- **Muwaṭṭaʾ Mālik (1,739 hadiths):** Darussalam English Edition.
- **Sunan al-Dārimī (101 hadiths):** Darussalam Translation Team.
- **al-Adab al-Mufrad (176 hadiths):** Muhtar Holland.
- **Riyāḍ al-Ṣāliḥīn (147 hadiths):** Rafiq Abdur Rahman.

### 6.3 Licensing & Redistribution Terms
- **Status:** **LICENSE REVIEW REQUIRED / ACADEMIC FAIR USE**.
- Modern English translations published by commercial houses (e.g. Darussalam) are subject to modern literary copyright.
- **Redistribution Policy:** Mīzān utilizes these translations strictly for non-commercial educational reference, academic search, and cross-linguistic study under **Fair Use**. The translations are **not redistributed as raw commercial exports** or bundled in public GitHub release mirrors without restriction.

---

## 7. Numbering Systems and Crosswalks (`data/hadith_numbering.db`)

### 7.1 Concordance Architecture
- **Total Mapping Records:** 95,598 entries in `hadith_numbers` and `numbering_provenance`.
- **Numbering Authorities (4 Registered):**
  1. `shamela` (al-Maktabah al-Shāmilah Digital Cataloging Team).
  2. `darussalam` (Darussalam Research Division, Riyadh).
  3. `sunnah_com` (Sunnah.com Open Hadith Project).
  4. `abd_al_baqi` (Muḥammad Fuʾād ʿAbd al-Bāqī, Cairo).

### 7.2 Registered Editions (18 Schemes across Kutub al-Sittah)
For each canonical collection, Mīzān maintains three parallel numbering schemes:
1. **Continuous Hadith Numbering:** Modern single-sequence system (Darussalam).
2. **Catalog Sequence Numbering:** Shamela digital database sequence.
3. **Classical Print Scan Page:** Physical volume and page numbering (*Mujallad/Ṣafḥah*) from authoritative historical printings (e.g. Būlāq, Dār Iḥyāʾ al-Kutub al-ʿArabiyyah).

---

## 8. Classical Scholar Evidence (`data/classical_scholar_evidence.db`)

### 8.1 Frozen Certification Corpus
- **System Baseline:** Phase 4 Classical Evidence Certification (Frozen & Read-Only).
- **Total Records:** 3,462 authorial evaluations.
- **Scholars Registered:**
  1. **al-Imām al-Tirmidhī (d. 279 AH):** Direct verdicts (*Ḥadīth Ḥasan Ṣaḥīḥ*, *Gharīb*, isnād defect analysis) preserved in *Jāmiʿ al-Tirmidhī*.
  2. **al-Imām Abū Dāwūd (d. 275 AH):** Direct authorial defect diagnoses, silent admissions (*sukūt*), and transmission preferences preserved in *Sunan Abī Dāwūd*.
  3. **al-Imām al-Nasāʾī (d. 303 AH):** Comparative isnād judgments, variant evaluations, and transmitter defect diagnoses preserved in *al-Sunan al-Ṣughrā*.
- **Licensing:** Classical Islamic Cultural Heritage (Universal Public Domain). The relational compilation is licensed under CC-BY-4.0.

---

## 9. Geographical and Historical Reference Data (`geoData.ts`)

- **Primary Source:** Yāqūt al-Ḥamawī, *Muʿjam al-Buldān* (معجم البلدان, d. 626 AH), supplemented by biographical demographic registers in *Siyar Aʿlām al-Nubalāʾ* (al-Dhahabī).
- **Local Artifact:** `mizan-web/frontend/src/app/isnad/geoData.ts`.
- **Scope:** 12 canonical transmission hubs:
  - *Hejaz:* Madīnah al-Munawwarah, Makkah al-Mukarramah.
  - *Iraq:* al-Kūfah, al-Baṣrah, Baghdād.
  - *Levant:* Dimashq (Damascus).
  - *Egypt:* al-Fusṭāṭ / Cairo.
  - *Khorasan & Transoxiana:* Nīshāpūr, Bukhārā, Samarqand, al-Rayy.
  - *Yemen & Maghrib:* Ṣanʿāʾ, Cordoba/Qayrawān.
- **Zero-Speculation Rule:** Edges between cities are rendered strictly when a verified teacher-student link exists between transmitters active in those centers.

---

## 10. Search Indexes and Derived Artifacts

- **Arabic Full-Text Search:** `data/hadith-search-index.db` (248 MB). Generated offline using SQLite FTS5 with custom Arabic normalization (removal of tashkīl, unification of hamzah/alif and yāʾ/alif maqṣūrah).
- **English Translation FTS:** `data/english_translation_fts.db` (32.8 MB) and `data/english-search.db` (78 MB). FTS5 indices enabling full-text keyword queries over English translations.
- **Derived Semantic Index:** `data/derived_semantic_index.db` (85.1 MB). Contains 20,744 768-dimensional float32 vectors generated via Google `gemini-embedding-001` per semantic meaning group.
- **EmbeddingGemma-2 Store:** `data/derived_embeddinggemma2_768d.db` (20 KB). Experimental baseline schema targeting Google DeepMind's open `embeddinggemma-2` (270M) model.

---

## 11. AI, Embedding, and Evaluation Resources

### 11.1 Benchmark Corpora (`data/benchmarks/`)
- `ask_mizan_stratified_benchmark_v1.jsonl`: Curated ground-truth test suite covering hadith lookups, narrator criticism, topical questions, and false citation traps.
- `embeddinggemma2_benchmark_v1.jsonl`: Benchmark evaluating semantic similarity across Arabic meaning groups.
- `evaluation_summary.json`: Automated evaluation report measuring MRR@10, Hit@3, and citation precision.

---

## 12. External APIs and Services

| Provider | Service / Model | Role in Mīzān | Mode | Credentials | Privacy Safeguards |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Google Cloud** | Google Gemini 2.5 Flash / Pro (`google-generativeai`) | Ask Mīzān natural language answer synthesis | Runtime (Optional) | `GEMINI_API_KEY` | Zero user telemetry stored. Only the sanitized question and retrieved evidence pack are transmitted. |
| **Google Cloud** | Google `gemini-embedding-001` | Semantic meaning group vector generation | Offline Preparation | `GEMINI_API_KEY` | Used only during index pre-computation. |
| **OpenAI** | GPT-4o / GPT-4o-mini | Alternative provider for Ask Mīzān synthesis | Runtime (Optional) | `OPENAI_API_KEY` | Opt-in via `ASK_MIZAN_PROVIDER=openai`. |
| **Anthropic** | Claude 3.5 Sonnet | Alternative provider for Ask Mīzān synthesis | Runtime (Optional) | `ANTHROPIC_API_KEY` | Opt-in via `ASK_MIZAN_PROVIDER=anthropic`. |
| **Ollama** | Local LLaMA / Qwen models | 100% offline, privacy-preserving synthesis | Runtime (Local) | None required (`localhost:11434`) | Zero data leaves the local workstation. |

*Full specifications available in [docs/data/external-services.md](external-services.md).*

---

## 13. Attribution Obligations and Redistribution Restrictions

1. **Software License (MIT):** All application source code in `mizan-web`, backend routers, and analysis scripts are licensed under the MIT License.
2. **Emaad Jumaah Hadith KG:** Must be attributed under **CC-BY-4.0**.
3. **Ali Bin Shahid Itqan Project:** Must be attributed with citation to Zenodo DOI `10.5281/zenodo.19453612`.
4. **Muhammad Hashim Open-Hadith-Data:** Commentary tables shared under **ODbL 1.0**.
5. **English Translations:** Must remain strictly under educational fair use; commercial redistribution of translation texts is prohibited.
6. **Git Tree Integrity:** Large database binaries (`*.db`) are strictly excluded from GitHub commits via `.gitignore` to adhere to repository size policies and copyright safeguards.

---

## 14. Unresolved Provenance and Current Limitations

1. **Classical Manuscript Scans:** The primary knowledge graph does not link every individual hadith to an archival manuscript scan image URL.
2. **Third-Party Translation Commercial Rights:** Translations provided by Darussalam are copyrighted; users seeking commercial publication of translation text must license directly from Darussalam.
3. **Non-Canonical Commentary Coverage:** Commentary excerpts currently cover 1,202 hadiths; comprehensive coverage across all 715,000 texts remains an ongoing scholarly project.
