# MĪZĀN AL-ḤADĪTH — VERIFIED FEATURE CATALOG

**Document Identifier:** `docs/overview/feature-catalog.md`  
**System Baseline:** Verified Implementation Status (October 2026)  

---

## 1. Verified Feature Matrix

The following catalog details every significant verified feature in the Mīzān platform. Each entry has been confirmed through automated regression tests, live API endpoints, and frontend component audits.

| Feature Module | Purpose | Main Capabilities | Technical Implementation | Verification Status | Documentation Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hadith Library** | Primary corpus exploration across the Six Canonical Books (*al-Kutub al-Sittah*). | Book navigation, chapter hierarchy, pagination, Arabic matn, English translation, isnād breakdown. | Next.js `/books`, `/books/[id]`, `/hadith/[id]`; FastAPI `/api/hadith/{id}`, `/api/books`. | **VERIFIED (Production)** | [Hadith Library](../features/hadith-library.md) |
| **Multi-Modal Search** | Instant retrieval of narrations across multiple textual dimensions. | Exact citation lookup, Arabic FTS5 root/prefix search, English full-text search, narrator lookup. | SQLite FTS5 with custom Arabic orthographic normalization; FastAPI `/api/search`. | **VERIFIED (Production)** | [Search & Retrieval](../features/search-and-retrieval.md) |
| **Ask Mīzān Assistant** | Grounded AI research assistant answering hadith inquiries with citations. | Natural language dialogue, intent parsing, multi-tier evidence pack assembly, citation validation. | FastAPI `/api/ask`; Gemini 2.5 Flash / OpenAI adapter; citation anti-hallucination guard. | **VERIFIED (Production)** | [Ask Mīzān](../features/ask-mizan.md) |
| **Narrator Research** | Biographical and critical assessment of hadith transmitters (*ʿIlm al-Rijāl*). | Transmitter dates, death years, locations, teachers/students, 127k jarḥ wa taʿdīl statements, collision guards. | Next.js `/narrators`, `/narrator/[id]`; FastAPI `/api/narrator/{id}`, `/api/narrator/{id}/aqwal`. | **VERIFIED (Production)** | [Narrator Research](../features/narrator-research.md) |
| **Isnād Topology Explorer** | Visual and computational analysis of transmission chains. | 2D directed transmission graph, generational timeline, 12-center historical geographical atlas, 3D space. | Next.js `/isnad`; precomputed `isnad_network.db` (298k edges); FastAPI `/api/isnad/{id}`. | **VERIFIED (Production)** | [Isnād Explorer](../features/isnad-explorer.md) |
| **Matn Variant Analysis** | Precise comparison of textual variants across collections. | Side-by-side text view, token-level insertions/deletions diffing, lexical overlap score calculation. | Next.js `/hadith-visualizer`; `MatnDiffViewer.tsx`; FastAPI `/api/matn/diff`, `/api/hadith/compare`. | **VERIFIED (Production)** | [Matn Analysis](../features/matn-analysis.md) |
| **Classical Commentary System** | Historical interpretation and linguistic analysis of narrations. | Direct access to *Fatḥ al-Bārī*, *Sharḥ Ṣaḥīḥ Muslim*, *ʿAwn al-Maʿbūd*, volume and page citations. | Next.js `HadithCommentarySection.tsx`; FastAPI `/api/hadith/{id}/commentaries`. | **VERIFIED (Production)** | [Commentary System](../features/commentary-system.md) |
| **Numbering Crosswalks** | Resolving discrepancies between international print editions. | Cross-edition concordance across 18 numbering editions (Darussalam, Fu'ad 'Abd al-Baqi, Wensinck). | `hadith_numbering.db` (95k records); FastAPI `/api/numbering/resolve`, `/api/hadith/{id}/crosswalk`. | **VERIFIED (Production)** | [Numbering Crosswalks](../features/numbering-and-crosswalks.md) |
| **Scholarly Evidence & Takhrij** | Multi-scholar evaluation matrix and cross-collection references. | Classical judgements (al-Tirmidhi, al-Bukhari) + modern verifications (Zubair Ali Zai, al-Albani). | `classical_scholar_evidence.db`; `citation_enrichment.db`; FastAPI `/api/hadith/{id}/grades`. | **VERIFIED (Production)** | [Scholarly Evidence](../features/scholarly-evidence.md) |
| **Research Workspace** | Private scholarly workbench for evidence formulation and note-taking. | Project creation, evidence bookmarks, structured notes, claim-evidence matrix (supporting/challenging). | Next.js `/workspace`; FastAPI `/api/workspace/*`; isolated `research_workspace.db`. | **VERIFIED (Production)** | [Research Workspace](../features/research-workspace.md) |
| **Citation & Dossier Export** | Publication-ready citations and comprehensive research exports. | Academic Chicago style and Arabic bibliographical citations; full research dossier export in Markdown/JSON. | `research_workspace.py`; `CitationChip.tsx`; FastAPI `/api/workspace/projects/{id}/export`. | **VERIFIED (Production)** | [Citation & Export](../features/citation-and-export.md) |
| **Identity Resolution Guard** | Preventing false attribution in similar-named scholars. | Disambiguation of father/son pairs (e.g., Abdur Rahman al-Musalli vs Wabarah) and famous aliases. | `identity_resolution.py`; verified by `scripts/test_scholarly_integrity.py`. | **VERIFIED (Production)** | [Security & Integrity](../architecture/security-and-integrity.md) |

---

## 2. Experimental & Planned Capabilities

To maintain strict truth-in-documentation standards, features undergoing research or planned for subsequent releases are explicitly categorized:

| Feature | Target Subsystem | Current Status | Notes |
| :--- | :--- | :--- | :--- |
| **Local Offline LLM Embedding (EmbeddingGemma2)** | Ask Mīzān Vector Store | Experimental (Phase 1 Baseline Tested) | 768-dimensional derived embeddings tested in Colab; current production defaults to Gemini embedding API. |
| **Audio Pronunciation of Chains** | Hadith Detail Reader | Prototype in scripts | Audio generation scripts exist in `scripts/generate_voiceover.py`; not yet wired to live frontend buttons. |
| **Automated Hadith Graph Export to Gephi/GraphML** | Isnād Explorer | Planned | JSON payload available via `/api/isnad/{id}/export`; direct XML/GEXF format pending. |
