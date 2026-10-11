# MĪZĀN AL-ḤADĪTH — PUBLIC SHOWCASE & PRESENTATION SUITE

This document catalogs the approved public demonstration assets, presentation slide decks, cinematic promotional video production suite, and visual architecture galleries for **Mīzān al-Ḥadīth** (ميزان الحديث).

---

## 📽️ Approved Showcase Assets Index

| Asset Type | Title / Focus | Deliverables & Artifacts | Target Audience | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Presentation Deck 01** | *Mīzān al-Ḥadīth: Digital Humanities Infrastructure & Relational Research Platform* | `Mizan_al_Hadith_Introduction_Presentation.pdf` (1.87 MB)<br/>Interactive Next.js route: `/presentation`<br/>Offline deck: `presentation/presentation_01/index.html` | Academic colleagues, digital humanities researchers, Islamic studies faculty | **APPROVED & AVAILABLE** |
| **Presentation Deck 02** | *Computational Roadmap, Architecture & Institutional Research Funding* | `Mizan_al_Hadith_Presentation_02_Roadmap_and_Funding.pdf` (4.25 MB)<br/>Slide deck source: `scripts/generate_presentation_02.py` | Research sponsors, institutional funders, digital infrastructure committees | **APPROVED & AVAILABLE** |
| **Cinematic Showcase Video** | *1080p Cinematic Promotional Video (82.0s, 30 FPS)* | Master Video: `video/output/mizan_promo_1080p.mp4` (21.1 MB)<br/>Automated render pipeline: `video/render.js`<br/>Interactive WebGL player: `video/index.html?controls=1` | General public, developers, conference attendees, open-source community | **APPROVED & AVAILABLE** |
| **Interactive Graphs** | *7 Standalone WebGL / SVG Research Visualizers* | Live in documentation portal: `docs/index.html`<br/>Live application routes: `/isnad`, `/hadith-visualizer`, `/books`, `/narrators`, `/workspace` | Scholars, students, researchers, developers | **APPROVED & LIVE** |

---

## 🖥️ Presentation Decks Detail

### Presentation 01: Platform Introduction & Digital Humanities Infrastructure
- **Purpose:** Comprehensive introduction to Mīzān's scholarly rationale, computational architecture, and digital humanities capabilities.
- **Slide Count:** 15 Master Folios.
- **Key Themes:**
  1. *The Challenge of Hadith Fragmentation:* 1,400 years of dispersed texts, divergent print editions, and unlinked biographical dictionaries.
  2. *The Mīzān Solution:* Unified graph database connecting 715k hadiths, 49.8k transmitters, 298k isnād edges, and 127k jarḥ wa taʿdīl critiques.
  3. *Forensic Crosswalks:* Deterministic alignment across 18 international print editions.
  4. *Live Workbench Demo:* Isnād network topology, matn textual variant alignment, and grounded Ask Mīzān dialogue.
- **Available Delivery Formats:**
  - **Integrated Next.js Client:** Live interactive presentation at `http://localhost:3000/presentation` with keyboard controls (`Space`, `←`, `→`, `N` for Speaker Notes, `O` for Slide Overview Grid, `F` for Fullscreen).
  - **Standalone Zero-Dependency Deck:** Open `presentation/presentation_01/index.html` directly in any web browser without server requirements.
  - **PDF Folio:** `Mizan_al_Hadith_Introduction_Presentation.pdf` (1.87 MB).

### Presentation 02: Computational Roadmap & Research Funding
- **Purpose:** Institutional proposal detailing technical milestones, infrastructure costs, and long-term academic sustainability.
- **Slide Count:** 20 Rigorous Slides.
- **Key Themes:**
  1. *Infrastructure Scale:* Storage economics of 1.64 GB relational KG, FTS5 indices, and vector embeddings.
  2. *Scholarly Integrity Architecture:* Immutable canonical databases (`mode=ro`), cryptographic SHA-256 verification, and strict demarcation between historical consensus and experimental models.
  3. *Five-Year Roadmap:* Expansion to Sunan al-Bayhaqi, Musnad Ahmad deep enrichment, and open-source model fine-tuning.
- **Available Delivery Formats:**
  - **PDF Folio:** `Mizan_al_Hadith_Presentation_02_Roadmap_and_Funding.pdf` (4.25 MB).
  - **Summary Specification:** `Mizan_al_Hadith_TotalCost.pdf` (4.25 MB).

---

## 🎬 1080p Cinematic Promotional Video Suite

The `video/` directory contains the complete source code, scene assets, audio stems, screen captures, and automated rendering pipeline for the **Mīzān al-Ḥadīth 1080p Cinematic Showcase Video**.

### Video Technical Specifications
- **Resolution:** Full HD 1920×1080 (16:9 widescreen)
- **Framerate:** 30 FPS (2,460 total frames)
- **Duration:** 82.0 Seconds
- **Audio:** 48 kHz Stereo AAC (320 kbps) with neural documentary narration, contemplative ambient soundtrack (55 Hz analog drone), and synchronized UI Foley sound effects (keystrokes, whooshes, chimes).
- **Master Output:** `video/output/mizan_promo_1080p.mp4`

### 8-Scene Narrative Architecture
1. **Scene 1: Sacred Geometry Opening (0.0s – 7.5s):** Atmospheric procedural Islamic 8-fold star rosette and golden Mīzān crest reveal.
2. **Scene 2: Scholarly Pain Points (7.5s – 18.0s):** 3D floating cards visualizing the fragmentation of traditional print indices.
3. **Scene 3: Computational Convergence (18.0s – 28.5s):** Animated counters for verified database records (715,790 hadiths, 49,844 transmitters, 298,655 isnāds).
4. **Scene 4: Instant Multi-Modal Search (28.5s – 39.5s):** Real-time search query demonstration for *"إنما الأعمال بالنيات"*, keyboard Foley, and instant FTS5 results.
5. **Scene 5: Hadith Context & Scholarly Grading (39.5s – 50.5s):** Breakdown of Bukhari #1 with canonical grading badge (`صحيح`), word-level narrator alignments, and classical commentary excerpts.
6. **Scene 6: Isnād Transmission Network (50.5s – 61.5s):** Interactive 8-step transmission chain for Hadith 1 and Imam al-Bukhari biographical profile with 41 classical *aqwāl*.
7. **Scene 7: Matn Variant Visualizer (61.5s – 72.5s):** Algorithmic textual crosswalk connecting Bukhari #1 with Muslim #3537, Tirmidhi #1569, and Musnad Ahmad #166 & #291.
8. **Scene 8: Hero Finale (72.5s – 82.0s):** 3D perspective pullback, golden Mīzān emblem, and call to action (*Search • Investigate • Connect • Research*).

### Reproducible Video Pipeline
The showcase video is fully reproducible from code via Puppeteer and FFmpeg:
```bash
# 1. Preview interactively in browser
# Open video/index.html?controls=1 in Chrome or Edge

# 2. Render master video to disk
node video/render.js

# 3. Generate vertical cut (9:16) for mobile platforms
ffmpeg -i video/output/mizan_promo_1080p.mp4 -vf "crop=608:1080:656:0" -c:v libx264 -crf 17 -c:a copy video/output/mizan_promo_9x16.mp4
```

---

## 🌐 Interactive Research Visualizers Showcase

The documentation portal (`docs/index.html`) embeds 7 zero-dependency, high-performance interactive research visualizers:

1. **System Architecture Diagram:** Multi-tier client/backend/database topology with live status badges.
2. **2D Isnād Network Topology:** Interactive force-directed graph rendering transmitter relationships, common links (*madār*), and transmission bottlenecks.
3. **Historical Islamic Geographical Atlas:** 12-center historical mapping (Madīnah, Makkah, Kūfah, Baṣrah, Baghdād, Damascus, Cairo, Bukhārā, Nīsābūr, Rayy, Qayrawān, Yemen) with transmitter counts and biographical movement routes.
4. **Chronological Generational Timeline:** Transmitters organized by *ṭabaqāt* (generations 1–12) across the 1st through 3rd Islamic centuries.
5. **Interactive Data Lineage Explorer:** End-to-end provenance traces showing which upstream datasets feed each application view.
6. **Forensic Database Inventory:** Searchable and filterable matrix of all 18 database files and upstream sources with record counts and cryptographic verification status.
7. **Interactive API Explorer:** Visual catalog of all 95 REST API endpoints with request and response schemas.

---

*For detailed technical architecture and implementation specifics, see [Architecture Overview](../architecture/system-overview.md) and [Feature Catalog](../features/hadith-library.md).*
