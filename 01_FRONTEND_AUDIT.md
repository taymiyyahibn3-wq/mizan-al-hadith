# MĪZĀN AL-ḤADĪTH — FRONTEND AUDIT & BASELINE ASSESSMENT
**Document Identifier:** `01_FRONTEND_AUDIT.md` / `FRONTEND_AUDIT.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Evaluation Date:** October 2026  
**Auditor:** Lead Frontend Architect & Scholarly Digital Humanities Engineer  

---

## Executive Summary

Mīzān al-Ḥadīth is an academic-grade digital hadith research platform grounded in a 425-book primary Arabic corpus, comprising 715,790 hadith records, 49,844 biographed narrators (*rijāl*), and over 300,000 verified transmission links (*asānīd*). Phase 18 established the forensic certification of all canonical database schemas, scholar grading provenances, quarantine boundaries, and RAG grounding invariants.

This audit evaluates the frontend user experience, visual design architecture, data visualization engines, typography, performance, accessibility, and mobile responsiveness. It defines the technical blueprint for elevating the frontend into a world-class, fast, calm, trustworthy scholarly research environment without compromising any certified backend or database invariant.

---

## 1. Current Architecture

| Architectural Layer | Current Technology / Implementation | Observations & Status |
| :--- | :--- | :--- |
| **Framework & Engine** | Next.js 16.3.6 (App Router), React 19.2.8, React DOM 19.2.8 | Modern React 19 architecture with Server/Client component capabilities. |
| **Language & Types** | TypeScript 5, strict mode enabled in `tsconfig.json` | Strong type foundations; some visualizer components use loose `any[]`. |
| **Styling & Tokens** | Tailwind CSS v4 (`@tailwindcss/postcss`), `src/app/globals.css` | Classical Islamic parchment palette: warm ivory (`#f5f1e8`), deep emerald (`#195143`), antique gold (`#a77c38`), and charcoal ink (`#181c1a`). |
| **Icons & UI Symbols** | Lucide React v1.47.0 | Clean, lightweight icon suite with minimal bundle overhead. |
| **Routing & Pages** | Next.js App Router: `/`, `/books`, `/books/[id]`, `/hadith/[id]`, `/hadith-visualizer`, `/isnad`, `/narrators`, `/narrator/[id]`, `/search`, `/info`, `/ask`, `/contact` | Comprehensive page coverage across all core research workflows. |
| **State Management** | Native React Hooks (`useState`, `useEffect`, `useMemo`, `useCallback`, `useRef`) | Zero external state library overhead; requires careful memoization to avoid re-render cascades in visualization canvases. |
| **API Client Layer** | `src/lib/api.ts` with helper functions (`getApiBaseUrl`, `fetchStats`, `apiFetch`, `askMizanQuery`) | Mixed usage: some components use `apiFetch`, while others use inline raw `fetch()` calls with duplicated error logic. |
| **Backend Endpoint** | FastAPI at `http://127.0.0.1:8000/api` reading read-only SQLite databases | Stable read-only endpoints with fast local response times. |
| **Image Pipeline** | Standard HTML `<img>` tags with linter suppresses; `public/books` directory is currently empty | Broken cover image paths (`/books/*-cover.jpg`) fall back to Wikimedia or CSS faux leather. |
| **Font Pipeline** | External `@import url("https://fonts.googleapis.com/css2?family=...")` in `globals.css` | Render-blocking CSS import causing FOIT/FOUT and layout shift. |
| **Typography System** | Classical Arabic (`Amiri`, `Scheherazade New`), Serif Display (`Cinzel`, `Playfair Display`), Sans-Serif (`Inter`) | Dignified scholarly tone; requires font preloading and zero-CLS optimization. |
| **Isnād Visualizations** | Custom SVG (Network, Map, Atlas, Timeline) & HTML5 Canvas (3D Spatial Projection) | Custom math projections without heavy 3D library bloat. |
| **Matn Visualizations** | Radial SVG similarity graph in `/hadith-visualizer` | Displays variant match percentages, but lacks phrase-level alignment and side-by-side textual diffing. |

---

## 2. Current Strengths

1. **Substantive Scholarly Grounding:**  
   Unlike superficial or decorative hadith tools, Mīzān is tied directly to verified primary texts, authentic biographical dictionaries (*Taqrīb*, *Tahdhīb*), and multi-scholar verdicts.
2. **Calm, Academic Visual Dignity:**  
   The design eschews gaming aesthetics, excessive glassmorphism, and neon gradients in favor of an elegant, parchment-and-emerald palette inspired by classical Islamic manuscript illumination.
3. **Zero Heavy Visualization Bloat:**  
   All visualizations (Isnād networks, geographic projections, and 3D spatial layers) use vanilla SVG and HTML5 Canvas rather than multi-megabyte third-party bundles (e.g. Three.js, D3), preserving rapid load times.
4. **Biographical Depth:**  
   Transmitter nodes link directly to rich biographical profiles with student/teacher records and historical evaluations (*Jarḥ wa Taʿdīl*).
5. **Deterministic Text Normalization:**  
   Search handles Arabic diacritics, hamza variations, and alef/ya unification seamlessly with sub-50ms retrieval.

---

## 3. Current Weaknesses

1. **Missing Local Cover Assets:**  
   The `public/books` directory is empty. The Six Canonical Books (`Ṣaḥīḥ al-Bukhārī`, `Ṣaḥīḥ Muslim`, `Sunan Abī Dāwūd`, `Jāmiʿ al-Tirmidhī`, `Sunan al-Nasāʾī`, `Sunan Ibn Mājah`) rely on remote Wikimedia URLs which can fail, lag, or fail due to network restrictions.
2. **Lack of Cover Sourcing & Provenance Documentation:**  
   No structured metadata records which editions the covers belong to, what their copyright/license status is, or where their authoritative scans originated.
3. **Render-Blocking Typography:**  
   The `@import` of Google Fonts in `globals.css` halts browser rendering until external stylesheets download.
4. **Matn Comparison Deficiencies:**  
   The current Matn visualizer only displays radial node circles with similarity percentages. It does not provide side-by-side textual phrase alignment, color-coded variant differences, or synchronized scrolling between witness narrations.
5. **No 3D Matn Research Exploration:**  
   While Isnād has a 3D mode, Matn textual relationships have no 3D witness/variant cluster representation.
6. **Incomplete Isnād Timeline Interactivity:**  
   Timeline does not clearly articulate multi-chain convergence, diverging paths, or branching comparisons between multiple narrations of the same hadith.
7. **Sparse Provenance & Licensing Documentation in UI:**  
   The `/info` page describes theoretical methodology, but lacks a complete, transparent Data Provenance Registry detailing every corpus, numbering crosswalk, commentary database, and external dataset with exact licenses and attribution requirements.

---

## 4. Performance Problems

- **Cumulative Layout Shift (CLS):** Dynamic font loading from external Google Fonts causes text reflow upon font swap.
- **Image Pipeline Inefficiency:** Images lack modern WebP/AVIF formats, responsive `srcset` definitions, and blur placeholders.
- **Canvas Rendering Overhead:** In `ThreeDView.tsx` and `AtlasView.tsx`, animation loops trigger continuous recalculations even when the canvas is idle.
- **Direct Fetch Inconsistency:** Several components bypass the centralized `apiFetch` client, missing unified error handling and request caching.

---

## 5. User Experience (UX) Problems

- **Homepage Entry Point Clarity:** While aesthetically pleasant, the homepage hero does not immediately provide dedicated shortcuts to all six core research pillars (Hadith Search, Isnād Explorer, Matn Explorer, Narrator Research, Scholarly Grades, Commentaries).
- **Search Interaction:** Lacks immediate debounced preview, keyboard shortcut hints (`/` or `Cmd+K`), and clear indication of translation availability.
- **Visualizer Detail Panels:** When clicking a node in Isnād or Matn visualizers, the inspector panel can crowd smaller laptop screens.

---

## 6. Visualization Problems

- **Isnād Timeline:** Displays death years linearly, but lacks visual indicators for diverging transmission paths or common link (*Madār*) isolation.
- **Geographic Map:** Historical centers are plotted, but transmission edges between cities are only visible in Atlas mode. A unified view linking geography, time, and transmission is needed.
- **3D Spatial View:** Requires smoother camera control damping, depth cueing, clear axis labels, and an automatic 2D fallback for lower-spec devices.
- **Matn Comparison:** Completely lacks synchronized phrase-level highlighting and variant diffing.

---

## 7. Accessibility Problems

- **Screen Reader Fallbacks:** SVG and Canvas visualizations lack rich semantic table fallbacks for screen reader users.
- **Keyboard Navigation:** Nodes in SVG graphs need `tabIndex` and `onKeyDown` handlers for full keyboard-only traversal.
- **Motion Sensitivity:** While basic `prefers-reduced-motion` exists in CSS, canvas-based animation loops must explicitly respect the user's reduced-motion preference by halting auto-rotation and transitions.

---

## 8. Mobile Problems

- **Visualizer Canvas Sizing:** On narrow screens (<480px), canvas aspect ratios can compress node labels.
- **Drawer Stacking:** Narrator research drawers can occlude visualization controls on mobile devices.
- **Touch Gestures:** Pinch-to-zoom and pan on touch screens require dedicated touch event listeners with passive flags.

---

## 9. Recommended Implementation Order

```
[Phase 1] Architecture Blueprint & Specs
   │  ├── 01_FRONTEND_AUDIT.md
   │  ├── 02_FRONTEND_ARCHITECTURE.md
   │  └── Visualization & Data Specifications (05 - 13)
   │
[Phase 2] Visual Assets & Sihah Sittah Cover Registry
   │  ├── Sourcing authentic, documented covers for the 6 collections
   │  ├── Structured JSON metadata registry (04_SIHAH_SITTAH_COVER_REGISTRY.md)
   │  └── Optimized WebP local asset deployment
   │
[Phase 3] Homepage Redesign & Research Suite Entry Points
   │  ├── Hero section with immediate scholarly research clarity
   │  ├── 6-Book Collection Showcase with verified covers & metadata
   │  └── Unified entry points for Search, Isnād, Matn, Rijāl, Grades, Commentaries
   │
[Phase 4] Isnād Visualization Engine Upgrade
   │  ├── Coordinated Timeline with branching, divergence, and temporal clarity
   │  ├── Geographic Map with location clustering and detail drawers
   │  ├── Integrated Isnād Atlas (Geography + Time + Transmission Network)
   │  └── Optimized Isnād 3D Spatial View with 2D fallback & reduced-motion support
   │
[Phase 5] Matn Textual Research & Diffing Engine
   │  ├── Side-by-side textual variant comparison with synchronized scrolling
   │  ├── Phrase-level color-coded diffing (identical, variant, additions)
   │  └── Matn 3D Variant Cluster exploration
   │
[Phase 6] Data Provenance, About, & Licensing Registry
   │  ├── Complete Data Provenance Registry for all 425 books, commentaries, and indexes
   │  ├── Explicit Licensing & Attribution documentation (12 & 13)
   │  └── Verified external repository and publisher links
   │
[Phase 7] Performance, Mobile, Accessibility, & Regression Audit
   │  ├── Web Vitals measurement & bundle optimization
   │  ├── Mobile responsive hardening & touch controls
   │  ├── Full accessibility audit (WCAG 2.1 AA)
   │  └── Zero-regression verification against Phase 18 Certified Invariants
```
