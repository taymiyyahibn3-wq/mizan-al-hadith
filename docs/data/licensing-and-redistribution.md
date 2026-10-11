# MĪZĀN AL-ḤADĪTH — LICENSING & REDISTRIBUTION DIRECTIVE

**Document Identifier:** `docs/data/licensing-and-redistribution.md`  
**Certified Baseline:** Complete Repository Audit & Intellectual Property Matrix  
**Compliance Standard:** Open Academic Research, CC Attribution & Fair Use Demarcation  

---

## 1. Compliance Principles & Intellectual Property Safeguards

Mīzān al-Ḥadīth operates under strict adherence to intellectual property ethics, classical heritage norms, and open-source licensing principles:
1. **No False Claims:** No copyrighted modern work or licensed dataset is claimed as "Public Domain" or "MIT" without verified legal justification.
2. **Strict Demarcation of Tiers:**
   - **Software Codebase:** The entire application code (Next.js frontend, FastAPI backend, CLI scripts, test suites) is licensed under the permissive **MIT License**.
   - **Primary Classical Mutūn & Asānīd:** Classical Arabic texts authored by historical compilers (150–850 AH) reside in the **Universal Public Domain**.
   - **Third-Party Datasets:** Datasets compiled by modern researchers (Emaad Jumaah, Ali Bin Shahid, HadithPro, Muhammad Hashim) carry specific open licenses (CC-BY-4.0, ODbL 1.0, GPL-compatible) that require explicit scholarly credit.
   - **Modern English Translations:** Modern translations (Darussalam, Dr. Muhsin Khan, etc.) carry publisher copyrights and are utilized strictly under **Academic & Educational Fair Use** for non-commercial research, search indexing, and bilingual study.
   - **Media Assets:** Photographic cover bindings carry verified Creative Commons or Public Domain licenses (CC BY-SA 3.0, CC BY-SA 4.0, PD-Old-70).

---

## 2. Resource-by-Resource Licensing & Redistribution Matrix

The following matrix distinguishes permissions for:
- **Attribute:** Can the resource be attributed and acknowledged?
- **Local Use:** Can the resource be executed and queried on a local installation?
- **Derived Metadata:** Can statistical properties, embeddings, or indices derived from the data be published?
- **Complete Redistribution:** Can the unedited underlying raw database be redistributed publicly?
- **GitHub Release:** Can the file be bundled directly into GitHub release assets?
- **Downloadable Mirror:** Can the file be hosted on public mirrors (e.g. Zenodo, Hugging Face, academic archive)?

| Resource / Corpus | Attribute | Local Use | Publish Derived Metadata | Redistribute Complete Contents | Include in GitHub Releases | Include in Public Downloadable Artifacts | Applicable License / Terms | Action / Governance Protocol |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Mīzān Software Codebase** | Yes | Yes | Yes | Yes | Yes | Yes | **MIT License** | Full open-source freedom. Included in git repository. |
| **Hadith Knowledge Graph** (`hadith-kg.db`) | **Mandatory** | Yes | Yes | Yes (with attribution) | Conditional (Size > 100MB) | Yes (with attribution) | **CC-BY-4.0** (Emaad Jumaah) / Classical Public Domain | Must cite Emaad Jumaah. Excluded from raw git commits via `.gitignore`; hosted on Zenodo/HuggingFace with CC-BY-4.0 credit. |
| **HadithPro Gradings** (`hadith_grades`) | **Mandatory** | Yes | Yes | Yes | Yes | Yes | **Open Research Data / GPL** (HadithPro) | Preserves individual scholar attributions (Albani, Zubair, Arnaut). Allowed for open redistribution. |
| **Classical Evaluations** (`classical_scholar_evidence.db`) | Yes | Yes | Yes | Yes | Yes | Yes | **Public Domain** (Classical Texts) / **CC-BY-4.0** (Compilation) | Phase 4 frozen certification artifact. Completely redistributable. |
| **Commentary Corpus** (*Fatḥ al-Bārī*, etc. 6 works) | **Mandatory** | Yes | Yes | Yes (ODbL terms) | Yes | Yes | **ODbL 1.0** (Muhammad Hashim) / Public Domain (Text) | Must credit Open-Hadith-Data project under ODbL 1.0 terms. |
| **Commentary Corpus** (*ʿUmdat al-Qārī*, *Irshād*) | Yes | Yes | Yes | Non-Commercial | Yes | Yes | **Public Domain** (Classical Text) / Shamela non-commercial | Free for non-commercial scholarly research and quotation. |
| **English Translations** (`hadith_translations.db`) | **Mandatory** | Yes | Yes | **RESTRICTED** | **NO** | **RESTRICTED** | **Modern Publisher Copyright / Educational Fair Use** | **RESTRICTED:** Modern publisher translations (Darussalam) cannot be redistributed as raw bulk commercial downloads. Retained locally for search and study; excluded from public raw git release blobs. |
| **Multi-Numbering Schemes** (`hadith_numbering.db`) | Yes | Yes | Yes | Yes | Yes | Yes | **Open Scholarly Metadata** | Concordance crosswalk metadata is non-copyrightable factual data under international law. |
| **Itqan Narrator Database** (`english_enrichment.db`) | **Mandatory** | Yes | Yes | Yes (with attribution) | Yes | Yes | **Open Access / Academic** (Ali Bin Shahid, DOI 10.5281/zenodo.19453612) | Must cite Ali Bin Shahid / Itqan paper DOI. Allowed for open research redistribution. |
| **Isnād Topology Multigraph** (`isnad_network.db`) | Yes | Yes | Yes | Yes | Yes | Yes | **MIT License** (Application Derived Artifact) | Purely computed from canonical sanads. Fully redistributable. |
| **FTS5 Search Indices** (`hadith-search-index.db`) | Yes | Yes | Yes | Yes | Yes | Yes | **MIT License** (Application Derived Artifact) | Rebuildable search index derived from canonical texts. |
| **Semantic Vector Cache** (`derived_semantic_index.db`) | Yes | Yes | Yes | Yes | Yes | Yes | **Application Derived Cache** | Rebuildable mathematical vector cache generated via Gemini API embeddings. |
| **Cover Photographs** (`public/books/*.jpg`) | **Mandatory** | Yes | Yes | Yes | Yes | Yes | **CC BY-SA 3.0 / CC BY-SA 4.0 / PD-Old-70** | Wikimedia Commons attribution statements preserved in Section 3. |

---

## 3. Media Asset Licenses (Sihah Sittah Covers)

All visual book bindings in `public/books/` have been audited and verified:

| Asset Path | Subject | Stated License | Author / Source | Permitted Use | Verified Attribution Statement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `public/books/bukhari-cover.png` | Ṣaḥīḥ al-Bukhārī Title Page | Public Domain (PD-Old-70) | Būlāq Amiri Press (1311 AH / 1893 CE) | Worldwide Commercial & Research | Public domain classical printing title page. |
| `public/books/muslim-cover.jpg` | Ṣaḥīḥ Muslim Binding | Public Domain (PD-Old-70) | Al-Amīrah Imperial Press (c. 1912 CE) | Worldwide Commercial & Research | Public domain Ottoman printing binding. |
| `public/books/tirmidhi-cover.jpg` | Jāmiʿ al-Tirmidhī 1st Ed. | Public Domain (PD-Old-70) | Mustafa al-Babi al-Halabi (1356 AH / 1937 CE) | Worldwide Commercial & Research | Public domain 1st edition critical cover. |
| `public/books/abu-dawud-cover.jpg` | Sunan Abī Dāwūd Volume | CC BY-SA 3.0 Unported | User: Abu Ta'ib (Wikimedia Commons) | Free sharing & adaptation | Photo by Abu Ta'ib, licensed under CC BY-SA 3.0. |
| `public/books/nasai-cover.jpg` | Sunan al-Nasāʾī Volume | CC BY-SA 4.0 International | User: Omarnorzai (Wikimedia Commons) | Free sharing & adaptation | Photo by Omarnorzai, licensed under CC BY-SA 4.0. |
| `public/books/ibn-majah-cover.jpg` | Sunan Ibn Mājah Volume | CC BY-SA 4.0 International | User: Omarnorzai (Wikimedia Commons) | Free sharing & adaptation | Photo by Omarnorzai, licensed under CC BY-SA 4.0. |

---

## 4. GitHub Release & Git Repository Policy

1. **Git Commit Exclusions:**
   - In accordance with GitHub repository guidelines and copyright safety, binary database files (`*.db`, `*.sqlite`) are **strictly excluded from Git tracking** via `.gitignore`.
   - No tracked SQLite database files are currently checked into Git, and no rewriting of Git history is necessary or performed.
2. **Release Distribution Channel:**
   - Public code releases on GitHub contain the complete, standalone application code, frontend interfaces, backend routers, documentation suite, and schema creation migrations.
   - For researchers wishing to reproduce the data tier, a documented verification script (`scripts/verify_preflight_hashes.py`) verifies the integrity of databases acquired from verified scholarly release mirrors (e.g., Zenodo / Hugging Face).
